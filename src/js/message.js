/* Shahnaz — owner WhatsApp message formatter.
 * UMD module: `require()` on the server (api/), `window.ShahnazMessage` in the browser.
 * One implementation = the click-to-chat text and the automatic notification are identical.
 */
(function (root, factory) {
  if (typeof module === "object" && module.exports) module.exports = factory();
  else root.ShahnazMessage = factory();
})(typeof self !== "undefined" ? self : this, function () {
  "use strict";

  var MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

  function oneLine(value, max) {
    return String(value == null ? "" : value)
      .replace(/[\u0000-\u001f\u007f]+/g, " ")
      .replace(/ {2,}/g, " ")
      .trim()
      .slice(0, max || 300);
  }

  function fmtDate(iso) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || "");
    if (!m) return "";
    return String(parseInt(m[3], 10)) + " " + MONTHS[parseInt(m[2], 10) - 1] + " " + m[1];
  }

  function fmtTime(hhmm) {
    var m = /^(\d{2}):(\d{2})$/.exec(hhmm || "");
    if (!m) return "";
    var h = parseInt(m[1], 10);
    var suffix = h >= 12 ? "PM" : "AM";
    var h12 = h % 12 === 0 ? 12 : h % 12;
    return (h12 < 10 ? "0" : "") + h12 + ":" + m[2] + " " + suffix;
  }

  function fmtMobile(e164) {
    var m = /^\+91([6-9]\d{4})(\d{5})$/.exec(e164 || "");
    return m ? "+91 " + m[1] + " " + m[2] : oneLine(e164, 20);
  }

  /* b: { bookingId, name, mobile (+91…), serviceName, addonNames, preferredDate (YYYY-MM-DD), preferredTime (HH:mm), note } */
  function build(b) {
    return [
      "\uD83D\uDD14 NEW WEBSITE BOOKING REQUEST",
      "",
      "ID: " + oneLine(b.bookingId, 20),
      "",
      "\uD83D\uDC64 Name: " + oneLine(b.name, 60),
      "\uD83D\uDCF1 Mobile: " + fmtMobile(b.mobile),
      "",
      "\uD83D\uDC84 Service: " + oneLine(b.serviceName, 80),
      "\u2795 Add-ons: " + (oneLine(b.addonNames, 200) || "None"),
      "",
      "\uD83D\uDCC5 Preferred Date: " + (fmtDate(b.preferredDate) || "Not specified"),
      "\uD83D\uDD50 Preferred Time: " + (fmtTime(b.preferredTime) || "Not specified"),
      "",
      "\uD83D\uDCDD Note: " + (oneLine(b.note, 300) || "None"),
      "",
      "Status: NEW"
    ].join("\n");
  }

  /* Values for an approved WhatsApp template with 8 body variables. Variables may not contain newlines and may not be empty. */
  function templateParams(b) {
    var dash = function (v) { return oneLine(v, 200) || "-"; };
    return [
      dash(b.bookingId), dash(b.name), dash(fmtMobile(b.mobile)), dash(b.serviceName),
      dash(b.addonNames), dash(fmtDate(b.preferredDate)), dash(fmtTime(b.preferredTime)), dash(b.note)
    ];
  }

  return { build: build, templateParams: templateParams, oneLine: oneLine, fmtDate: fmtDate, fmtTime: fmtTime, fmtMobile: fmtMobile };
});
