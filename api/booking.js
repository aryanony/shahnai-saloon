"use strict";
const { getCatalog } = require("./_lib/catalog");
const { postBooking } = require("./_lib/appsScript");
const { validateBooking } = require("./_lib/validate");
const { notifyOwner } = require("./_lib/whatsapp");

const MAX_BODY_CHARS = 8000;
const MIN_FILL_MS = 2000;            // faster than this is almost certainly a script
const DONE_TTL_MS = 10 * 60 * 1000;  // idempotency window for a successfully saved token
const RATE_WINDOW_MS = 10 * 60 * 1000;
const RATE_MAX = 6;

// Best-effort, per warm serverless instance. Apps Script keeps the durable copy of both guards.
const done = new Map();      // requestToken -> { bookingId, at }
const pending = new Set();   // tokens currently being written
const hits = new Map();      // ip -> [timestamps]

function reply(res, status, body) { return res.status(status).json(body); }
const fail = (res, status, message) => reply(res, status, { ok: false, message });

function clientIp(req) {
  const xff = String(req.headers["x-forwarded-for"] || "");
  return xff.split(",")[0].trim() || (req.socket && req.socket.remoteAddress) || "unknown";
}

function rateLimited(ip, now) {
  const recent = (hits.get(ip) || []).filter((t) => now - t < RATE_WINDOW_MS);
  recent.push(now);
  hits.set(ip, recent);
  if (hits.size > 5000) hits.clear();
  return recent.length > RATE_MAX;
}

function sweep(now) {
  for (const [token, v] of done) if (now - v.at > DONE_TTL_MS) done.delete(token);
}

module.exports = async (req, res) => {
  res.setHeader("Cache-Control", "no-store");
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return fail(res, 405, "Method not allowed.");
  }

  let body = req.body;
  try {
    if (typeof body === "string") body = JSON.parse(body);
  } catch (e) {
    return fail(res, 400, "Invalid request.");
  }
  if (!body || typeof body !== "object") return fail(res, 400, "Invalid request.");
  if (JSON.stringify(body).length > MAX_BODY_CHARS) return fail(res, 413, "Request too large.");

  // Bots fill hidden fields. Pretend success, store nothing, remember nothing.
  if (body.honeypot) return reply(res, 200, { ok: true, bookingId: "SBP-000000", notify: "skipped" });

  const now = Date.now();
  sweep(now);
  if (rateLimited(clientIp(req), now)) return fail(res, 429, "Too many requests. Please call or WhatsApp us.");

  // Elapsed time is measured by the browser (performance.now), so a wrong phone clock cannot break it.
  const fill = Number(body.fillTimeMs);
  if (!Number.isFinite(fill) || fill < MIN_FILL_MS) return fail(res, 400, "Please try again.");

  const checked = validateBooking(body, now);
  if (!checked.ok) return fail(res, 400, checked.message);
  const value = checked.value;

  // Retried after a success? Return the same answer instead of a duplicate row.
  const already = done.get(value.requestToken);
  if (already) return reply(res, 200, { ok: true, bookingId: already.bookingId, notify: "skipped", duplicate: true });
  if (pending.has(value.requestToken)) return fail(res, 429, "Your request is already being sent.");

  const catalog = await getCatalog();
  if (!catalog.services.some((s) => s.id === value.serviceId)) return fail(res, 400, "That service is not available right now.");
  const activeAddons = new Set(catalog.additionalServices.map((a) => a.id));
  if (!value.addonIds.every((id) => activeAddons.has(id))) return fail(res, 400, "One of the add-ons is not available right now.");

  pending.add(value.requestToken);
  let saved;
  try {
    saved = await postBooking(value);
  } catch (err) {
    console.error("booking: Apps Script write failed -", err.message);
    return fail(res, 502, "Unable to submit request right now.");
  } finally {
    pending.delete(value.requestToken); // a failed attempt must never burn the token
  }
  if (!saved || saved.ok !== true || !saved.bookingId) {
    console.error("booking: Apps Script rejected the request");
    return fail(res, 502, "Unable to submit request right now.");
  }
  done.set(value.requestToken, { bookingId: saved.bookingId, at: now });

  // The row is saved. Notification problems must never turn this into a customer-facing failure.
  let notify = "click";
  if (catalog.business.whatsappMode === "AUTO_NOTIFY") {
    notify = await notifyOwner(catalog.business.whatsapp || catalog.business.phone, {
      bookingId: saved.bookingId,
      name: value.name,
      mobile: value.mobile,
      serviceName: saved.serviceName,
      addonNames: saved.addonNames,
      preferredDate: value.preferredDate,
      preferredTime: value.preferredTime,
      note: value.note
    });
  }
  return reply(res, 200, { ok: true, bookingId: saved.bookingId, notify });
};

module.exports._internals = { done, pending, hits };
