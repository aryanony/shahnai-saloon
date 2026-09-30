"use strict";
/* Pure validation helpers — no network, no globals, easy to test (see tests/api.test.js). */

const MOBILE_RE = /^(?:\+?91|0)?([6-9]\d{9})$/;
const NAME_RE = /^[\p{L}\p{M}][\p{L}\p{M}\s.'\u2019-]{1,59}$/u;
const ID_RE = /^[A-Za-z0-9_-]{1,30}$/;
const TOKEN_RE = /^[A-Za-z0-9-]{16,64}$/;
const DATE_RE = /^(\d{4})-(\d{2})-(\d{2})$/;
const TIME_RE = /^([01]\d|2[0-3]):[0-5]\d$/;
const PAGE_RE = /^\/[a-z0-9\-/]{0,78}$/;
const IST_OFFSET_MS = 330 * 60 * 1000;
const MAX_DAYS_AHEAD = 548; // ~18 months

function clean(value, max) {
  return String(value == null ? "" : value)
    .replace(/[\u0000-\u001f\u007f]+/g, " ")
    .replace(/\s{2,}/g, " ")
    .trim()
    .slice(0, max);
}

/** "076458 12695", "+91 76458 12695", "7645812695" -> "+917645812695"; anything else -> null */
function normalizeMobile(raw) {
  const digits = String(raw == null ? "" : raw).replace(/[\s\-().]/g, "");
  const m = MOBILE_RE.exec(digits);
  return m ? "+91" + m[1] : null;
}

function istToday(nowMs) {
  return new Date(nowMs + IST_OFFSET_MS).toISOString().slice(0, 10);
}

function isRealDate(iso) {
  const m = DATE_RE.exec(iso);
  if (!m) return false;
  const d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
  return d.getUTCFullYear() === +m[1] && d.getUTCMonth() === +m[2] - 1 && d.getUTCDate() === +m[3];
}

function daysBetween(fromIso, toIso) {
  return Math.round((Date.parse(toIso + "T00:00:00Z") - Date.parse(fromIso + "T00:00:00Z")) / 86400000);
}

/**
 * @returns {{ok:true, value:object} | {ok:false, message:string}}
 * The message is safe to show to a customer.
 */
function validateBooking(body, nowMs) {
  const fail = (message) => ({ ok: false, message });
  if (!body || typeof body !== "object" || Array.isArray(body)) return fail("Invalid request.");

  const name = clean(body.name, 60);
  if (!NAME_RE.test(name)) return fail("Please enter your name.");

  const mobile = normalizeMobile(body.mobile);
  if (!mobile) return fail("Please enter a valid 10-digit mobile number.");

  const serviceId = String(body.serviceId || "").trim();
  if (!ID_RE.test(serviceId)) return fail("Please choose a service.");

  let addonIds = [];
  if (body.addonIds !== undefined && body.addonIds !== null) {
    if (!Array.isArray(body.addonIds) || body.addonIds.length > 10) return fail("Please check your add-on selection.");
    addonIds = Array.from(new Set(body.addonIds.map((v) => String(v).trim())));
    if (!addonIds.every((id) => ID_RE.test(id))) return fail("Please check your add-on selection.");
  }

  const preferredDate = String(body.preferredDate || "").trim();
  if (!isRealDate(preferredDate)) return fail("Please choose a valid preferred date.");
  const today = istToday(nowMs);
  const ahead = daysBetween(today, preferredDate);
  if (ahead < 0) return fail("Please choose today or a future date.");
  if (ahead > MAX_DAYS_AHEAD) return fail("Please choose a nearer date.");

  const preferredTime = String(body.preferredTime || "").trim();
  if (preferredTime && !TIME_RE.test(preferredTime)) return fail("Please choose a valid preferred time.");

  const note = clean(body.note, 300);
  if (String(body.note || "").length > 600) return fail("Please keep your note short.");

  const requestToken = String(body.requestToken || "");
  if (!TOKEN_RE.test(requestToken)) return fail("Invalid request.");

  const page = PAGE_RE.test(String(body.page || "")) ? String(body.page) : "/book/";

  return {
    ok: true,
    value: { name, mobile, serviceId, addonIds, preferredDate, preferredTime, note, source: "WEBSITE", page, requestToken }
  };
}

module.exports = { validateBooking, normalizeMobile, clean, istToday, isRealDate };
