"use strict";
/* Server-only. APPS_SCRIPT_URL and BOOKING_SHARED_SECRET are Vercel environment variables;
 * neither ever reaches the browser. */

const TIMEOUT_MS = 9000;

async function call(url, options) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), TIMEOUT_MS);
  try {
    const res = await fetch(url, Object.assign({ redirect: "follow", signal: ctrl.signal }, options));
    if (!res.ok) throw new Error("apps_script_http_" + res.status);
    return await res.json();
  } finally {
    clearTimeout(timer);
  }
}

function endpoint() {
  const url = process.env.APPS_SCRIPT_URL;
  if (!url || !/^https:\/\/script\.google\.com\//.test(url)) throw new Error("APPS_SCRIPT_URL missing or invalid");
  return url;
}

async function fetchCatalogRaw() {
  return call(endpoint(), { method: "GET" });
}

async function postBooking(value) {
  const secret = process.env.BOOKING_SHARED_SECRET;
  if (!secret) throw new Error("BOOKING_SHARED_SECRET missing");
  return call(endpoint(), {
    method: "POST",
    headers: { "Content-Type": "text/plain;charset=utf-8" }, // avoids a CORS preflight-style edge case on Apps Script
    body: JSON.stringify(Object.assign({}, value, { apiKey: secret }))
  });
}

module.exports = { fetchCatalogRaw, postBooking };
