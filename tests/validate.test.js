"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const { validateBooking, normalizeMobile, isRealDate } = require("../api/_lib/validate");

const NOW = Date.parse("2026-09-30T06:00:00Z"); // ~11:30 IST
const TOKEN = "abcdefgh12345678";

function base(overrides) {
  return Object.assign(
    {
      name: "Priya Kumari",
      mobile: "9876543210",
      serviceId: "BRIDAL",
      addonIds: ["HAIR"],
      preferredDate: "2026-10-12",
      preferredTime: "10:30",
      note: "Please call before confirming.",
      requestToken: TOKEN,
      page: "/book/"
    },
    overrides
  );
}

test("accepts a well-formed booking", () => {
  const r = validateBooking(base(), NOW);
  assert.equal(r.ok, true);
  assert.equal(r.value.mobile, "+919876543210");
});

test("normalizes mobile numbers in every common format the client might send", () => {
  assert.equal(normalizeMobile("9876543210"), "+919876543210");
  assert.equal(normalizeMobile("+91-98765 43210"), "+919876543210");
  assert.equal(normalizeMobile("09876543210"), "+919876543210"); // 0-prefixed trunk-dial form
  assert.equal(normalizeMobile("+91 98765 43210"), "+919876543210");
  assert.equal(normalizeMobile("12345"), null);
  assert.equal(normalizeMobile("5876543210"), null); // starts with 5: not a valid Indian mobile prefix
});

test("rejects a landline-shaped / too-short number", () => {
  const r = validateBooking(base({ mobile: "12345" }), NOW);
  assert.equal(r.ok, false);
});

test("rejects an empty or whitespace-only name", () => {
  assert.equal(validateBooking(base({ name: "" }), NOW).ok, false);
  assert.equal(validateBooking(base({ name: "   " }), NOW).ok, false);
});

test("rejects a past preferred date", () => {
  const r = validateBooking(base({ preferredDate: "2020-01-01" }), NOW);
  assert.equal(r.ok, false);
});

test("accepts today's date (IST) as the earliest allowed date", () => {
  const r = validateBooking(base({ preferredDate: "2026-09-30" }), NOW);
  assert.equal(r.ok, true);
});

test("rejects a date far beyond the allowed horizon", () => {
  const r = validateBooking(base({ preferredDate: "2031-01-01" }), NOW);
  assert.equal(r.ok, false);
});

test("rejects a malformed time but allows an empty one", () => {
  assert.equal(validateBooking(base({ preferredTime: "25:99" }), NOW).ok, false);
  assert.equal(validateBooking(base({ preferredTime: "" }), NOW).ok, true);
});

test("rejects a note over the length cap", () => {
  const r = validateBooking(base({ note: "x".repeat(700) }), NOW);
  assert.equal(r.ok, false);
});

test("rejects an invalid or missing request token", () => {
  assert.equal(validateBooking(base({ requestToken: "" }), NOW).ok, false);
  assert.equal(validateBooking(base({ requestToken: "short" }), NOW).ok, false);
});

test("rejects a malformed service or add-on id", () => {
  assert.equal(validateBooking(base({ serviceId: "" }), NOW).ok, false);
  assert.equal(validateBooking(base({ addonIds: ["has space"] }), NOW).ok, false);
});

test("de-duplicates repeated add-on ids", () => {
  const r = validateBooking(base({ addonIds: ["HAIR", "HAIR", "DRAPING"] }), NOW);
  assert.equal(r.ok, true);
  assert.deepEqual(r.value.addonIds.sort(), ["DRAPING", "HAIR"]);
});

test("falls back to /book/ for a missing or unrecognised page path", () => {
  const r = validateBooking(base({ page: "https://evil.example/x" }), NOW);
  assert.equal(r.ok, true);
  assert.equal(r.value.page, "/book/");
});

test("isRealDate rejects calendar-invalid dates like 31 Feb", () => {
  assert.equal(isRealDate("2026-02-31"), false);
  assert.equal(isRealDate("2026-02-28"), true);
});
