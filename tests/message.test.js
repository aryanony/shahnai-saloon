"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const Message = require("../src/js/message.js");

const booking = {
  bookingId: "SBP-260002",
  name: "Priya Kumari",
  mobile: "+919876543210",
  serviceName: "Bridal Makeup",
  addonNames: "Bridal Hairstyling, Saree / Dupatta Draping",
  preferredDate: "2026-10-12",
  preferredTime: "10:30",
  note: "Please call before confirming."
};

test("build() produces the exact required owner-message format", () => {
  const text = Message.build(booking);
  assert.match(text, /^\uD83D\uDD14 NEW WEBSITE BOOKING REQUEST/);
  assert.match(text, /ID: SBP-260002/);
  assert.match(text, /Name: Priya Kumari/);
  assert.match(text, /Mobile: \+91 98765 43210/);
  assert.match(text, /Service: Bridal Makeup/);
  assert.match(text, /Add-ons: Bridal Hairstyling, Saree \/ Dupatta Draping/);
  assert.match(text, /Preferred Date: 12 Oct 2026/);
  assert.match(text, /Preferred Time: 10:30 AM/);
  assert.match(text, /Note: Please call before confirming\./);
  assert.match(text, /Status: NEW$/);
  assert.doesNotMatch(text, /[{<]/); // no JSON, no HTML, per the brief's "no JSON, no HTML" rule
});

test("build() shows friendly defaults when add-ons/time/note are absent", () => {
  const text = Message.build(Object.assign({}, booking, { addonNames: "", preferredTime: "", note: "" }));
  assert.match(text, /Add-ons: None/);
  assert.match(text, /Preferred Time: Not specified/);
  assert.match(text, /Note: None/);
});

test("templateParams() returns 8 non-empty strings in a fixed order for the approved WhatsApp template", () => {
  const params = Message.templateParams(booking);
  assert.equal(params.length, 8);
  params.forEach((p) => assert.ok(p && p.length > 0));
  assert.equal(params[0], "SBP-260002");
  assert.equal(params[5], "12 Oct 2026");
});

test("fmtTime formats midnight and noon correctly", () => {
  assert.equal(Message.fmtTime("00:05"), "12:05 AM");
  assert.equal(Message.fmtTime("12:00"), "12:00 PM");
  assert.equal(Message.fmtTime("23:59"), "11:59 PM");
});

test("oneLine strips newlines/control characters so a note can never break the message layout", () => {
  assert.equal(Message.oneLine("line1\nline2\ttab"), "line1 line2 tab");
});
