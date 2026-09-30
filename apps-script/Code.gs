/**
 * SHAHNAZ BEAUTY PARLOUR — Google Sheet backend (Google Apps Script Web App)
 * ---------------------------------------------------------------------------
 * The ONLY code that touches the Sheet. The website calls the Vercel API, and
 * the Vercel API calls this Web App with a shared secret.
 *
 * Sheet tabs read/written (headers in row 1, never rename them — the README tab says so too):
 *   Settings            Key | Value | Owner note
 *   Services            service_id | service_name | category | price | price_type | active | display_order
 *   Additional Services addon_id | addon_name | price | active | display_order
 *   Bookings            created_at | booking_id | name | mobile | service | additional_services |
 *                       preferred_date | preferred_time | note | status
 *
 * One-time setup:
 *   1. Extensions > Apps Script, paste this file.
 *   2. Run setup() once. Copy the secret it logs into the Vercel env var BOOKING_SHARED_SECRET.
 *   3. Deploy > New deployment > Web app > Execute as: Me, Who has access: Anyone.
 *   4. Copy the /exec URL into the Vercel env var APPS_SCRIPT_URL.
 *   5. After ANY code change: Deploy > Manage deployments > Edit > New version.
 */

var TABS = { SETTINGS: "Settings", SERVICES: "Services", ADDONS: "Additional Services", BOOKINGS: "Bookings" };
var TZ = "Asia/Kolkata";
var DEDUPE_SECONDS = 600;
var MOBILE_MAX_PER_WINDOW = 3;
var TOKEN_RE = /^[A-Za-z0-9-]{16,64}$/;
var ID_RE = /^[A-Za-z0-9_-]{1,30}$/;

/** Run once from the editor. Creates the shared secret and logs it. */
function setup() {
  var props = PropertiesService.getScriptProperties();
  if (!props.getProperty("BOOKING_SHARED_SECRET")) {
    props.setProperty("BOOKING_SHARED_SECRET", Utilities.getUuid() + Utilities.getUuid().replace(/-/g, ""));
  }
  // Only needed if this script is NOT bound to the Sheet (Extensions > Apps Script from inside the Sheet is bound):
  // props.setProperty("SHEET_ID", "<spreadsheet id>");
  Logger.log("BOOKING_SHARED_SECRET = " + props.getProperty("BOOKING_SHARED_SECRET"));
}

/* ------------------------------ helpers ------------------------------ */

function spreadsheet_() {
  var id = PropertiesService.getScriptProperties().getProperty("SHEET_ID");
  return id ? SpreadsheetApp.openById(id) : SpreadsheetApp.getActiveSpreadsheet();
}

function json_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

function isYes_(v) { return String(v).trim().toLowerCase() === "yes"; }

function num_(v) {
  var n = Number(v);
  return isFinite(n) && n > 0 ? n : 0;
}

function safeUrl_(v) { var s = String(v || "").trim(); return /^https:\/\/\S+$/.test(s) ? s : ""; }

function safePhone_(v) {
  var s = String(v || "").replace(/[\s\-()]/g, "");
  return /^\+?[0-9]{8,15}$/.test(s) ? s : "";
}

/** Stops spreadsheet formula injection: text a customer typed must never be evaluated as a formula. */
function guard_(v) {
  var s = String(v == null ? "" : v);
  return /^[=+\-@\t\r]/.test(s) ? "'" + s : s;
}

/** Reads a tab as an array of objects keyed by the header names in row 1. */
function readTable_(tabName, requiredHeaders) {
  var sheet = spreadsheet_().getSheetByName(tabName);
  if (!sheet) throw new Error("Missing tab: " + tabName);
  var values = sheet.getDataRange().getValues();
  if (!values.length) throw new Error("Empty tab: " + tabName);
  var headers = values[0].map(function (h) { return String(h).trim(); });
  requiredHeaders.forEach(function (h) {
    if (headers.indexOf(h) === -1) throw new Error("Tab '" + tabName + "' is missing header '" + h + "'");
  });
  var rows = [];
  for (var r = 1; r < values.length; r++) {
    if (String(values[r][0]).trim() === "") continue;
    var obj = {};
    for (var c = 0; c < headers.length; c++) if (headers[c]) obj[headers[c]] = values[r][c];
    rows.push(obj);
  }
  return { sheet: sheet, headers: headers, rows: rows };
}

function settings_() {
  var t = readTable_(TABS.SETTINGS, ["Key", "Value"]);
  var map = {};
  t.rows.forEach(function (row) { map[String(row.Key).trim()] = row.Value; });
  return map;
}

function byOrder_(a, b) { return Number(a.display_order || 0) - Number(b.display_order || 0); }

function services_(activeOnly) {
  var t = readTable_(TABS.SERVICES, ["service_id", "service_name", "category", "price", "price_type", "active", "display_order"]);
  return t.rows
    .filter(function (s) { return !activeOnly || isYes_(s.active); })
    .sort(byOrder_)
    .map(function (s) {
      var price = num_(s.price);
      var type = String(s.price_type || "").trim();
      if (!price || (type !== "Fixed" && type !== "From")) { type = "Enquiry"; price = 0; }
      return { id: String(s.service_id).trim(), name: String(s.service_name).trim(), category: String(s.category || "").trim(), price: price, priceType: type };
    });
}

function addons_(activeOnly) {
  var t = readTable_(TABS.ADDONS, ["addon_id", "addon_name", "price", "active", "display_order"]);
  return t.rows
    .filter(function (a) { return !activeOnly || isYes_(a.active); })
    .sort(byOrder_)
    .map(function (a) { return { id: String(a.addon_id).trim(), name: String(a.addon_name).trim(), price: num_(a.price) }; });
}

/* ------------------------------ GET: public catalog ------------------------------ */

function buildCatalog_() {
  var s = settings_();
  return {
    business: {
      primaryBrand: String(s.PRIMARY_BRAND || "").trim(),
      secondaryBrand: String(s.SECONDARY_BRAND || "").trim(),
      descriptor: String(s.DESCRIPTOR || "").trim(),
      phone: safePhone_(s.PHONE),
      altPhone: safePhone_(s.ALT_PHONE),
      whatsapp: safePhone_(s.WHATSAPP) || safePhone_(s.PHONE),
      address: String(s.ADDRESS || "").trim(),
      mapsUrl: safeUrl_(s.MAPS_URL),
      instagramUrl: safeUrl_(s.INSTAGRAM_URL),
      websiteUrl: safeUrl_(s.WEBSITE_URL),
      whatsappMode: String(s.WHATSAPP_MODE).trim() === "AUTO_NOTIFY" ? "AUTO_NOTIFY" : "CLICK_TO_CHAT",
      formCta: String(s.FORM_CTA || "Send Booking Request").trim(),
      successMessage: String(s.SUCCESS_MESSAGE || "Your booking request has been received. We\u2019ll contact you to confirm.").trim()
    },
    services: services_(true),
    additionalServices: addons_(true)
  };
}

function doGet() {
  try {
    return json_(buildCatalog_());   // never includes Bookings or the secret
  } catch (err) {
    console.error(err);
    return json_({ ok: false, message: "catalog_unavailable" });
  }
}

/* ------------------------------ POST: one booking = one row ------------------------------ */

function nextBookingId_(sheet, headers) {
  var yy = Utilities.formatDate(new Date(), TZ, "yy");
  var col = headers.indexOf("booking_id") + 1;
  var last = sheet.getLastRow();
  var max = 0;
  if (last > 1) {
    var ids = sheet.getRange(2, col, last - 1, 1).getValues();
    var re = new RegExp("^SBP-" + yy + "(\\d{4})$");
    ids.forEach(function (row) {
      var m = re.exec(String(row[0]).trim());
      if (m) max = Math.max(max, parseInt(m[1], 10));
    });
  }
  return "SBP-" + yy + ("0000" + (max + 1)).slice(-4);
}

function istDate_(iso) {            // "2026-10-12" -> Date at 00:00 IST
  var p = iso.split("-");
  return new Date(Date.UTC(+p[0], +p[1] - 1, +p[2]) - 330 * 60000);
}

function doPost(e) {
  try {
    var p = JSON.parse(e.postData.contents);
    var secret = PropertiesService.getScriptProperties().getProperty("BOOKING_SHARED_SECRET");
    if (!secret || p.apiKey !== secret) return json_({ ok: false, message: "unauthorized" }); // fail closed

    if (!TOKEN_RE.test(String(p.requestToken || ""))) return json_({ ok: false, message: "bad_token" });
    if (!ID_RE.test(String(p.serviceId || ""))) return json_({ ok: false, message: "bad_service" });
    if (!/^\+91[6-9]\d{9}$/.test(String(p.mobile || ""))) return json_({ ok: false, message: "bad_mobile" });
    if (!/^\d{4}-\d{2}-\d{2}$/.test(String(p.preferredDate || ""))) return json_({ ok: false, message: "bad_date" });
    var time = String(p.preferredTime || "");
    if (time && !/^([01]\d|2[0-3]):[0-5]\d$/.test(time)) return json_({ ok: false, message: "bad_time" });

    var cache = CacheService.getScriptCache();
    var prior = cache.get("req_" + p.requestToken);
    if (prior) return json_(JSON.parse(prior));                       // idempotent retry

    var mobileKey = "mob_" + p.mobile;
    if (Number(cache.get(mobileKey) || 0) >= MOBILE_MAX_PER_WINDOW) return json_({ ok: false, message: "rate_limited" });

    // Authoritative catalog check: active service and active add-ons only.
    var svc = services_(true).filter(function (s) { return s.id === p.serviceId; })[0];
    if (!svc) return json_({ ok: false, message: "service_unavailable" });
    var activeAddons = addons_(true);
    var chosen = [];
    var ids = Array.isArray(p.addonIds) ? p.addonIds : [];
    for (var i = 0; i < ids.length; i++) {
      var a = activeAddons.filter(function (x) { return x.id === ids[i]; })[0];
      if (!a) return json_({ ok: false, message: "addon_unavailable" });
      chosen.push(a.name);
    }

    var lock = LockService.getScriptLock();
    lock.waitLock(15000);
    var result;
    try {
      var t = readTable_(TABS.BOOKINGS, ["created_at", "booking_id", "name", "mobile", "service", "additional_services", "preferred_date", "preferred_time", "note", "status"]);
      var sheet = t.sheet;
      var bookingId = nextBookingId_(sheet, t.headers);
      var now = new Date();
      var cells = {
        created_at: now,
        booking_id: bookingId,
        name: guard_(String(p.name || "").slice(0, 60)),
        mobile: String(p.mobile),
        service: svc.name,
        additional_services: chosen.join(", "),
        preferred_date: istDate_(String(p.preferredDate)),
        preferred_time: time,
        note: guard_(String(p.note || "").slice(0, 300)),
        status: "NEW"
      };
      var row = Math.max(sheet.getLastRow(), 1) + 1;
      var range = sheet.getRange(row, 1, 1, t.headers.length);
      var formats = t.headers.map(function (h) {
        if (h === "created_at") return "yyyy-mm-dd hh:mm";
        if (h === "preferred_date") return "yyyy-mm-dd";
        return "@";                                                     // everything else stays plain text
      });
      range.setNumberFormats([formats]);
      range.setValues([t.headers.map(function (h) { return cells.hasOwnProperty(h) ? cells[h] : ""; })]);

      result = { ok: true, bookingId: bookingId, serviceName: svc.name, addonNames: chosen.join(", "), createdAt: Utilities.formatDate(now, TZ, "yyyy-MM-dd HH:mm") };
      cache.put("req_" + p.requestToken, JSON.stringify(result), DEDUPE_SECONDS);
      cache.put(mobileKey, String(Number(cache.get(mobileKey) || 0) + 1), DEDUPE_SECONDS);
    } finally {
      lock.releaseLock();
    }
    return json_(result);
  } catch (err) {
    console.error(err);
    return json_({ ok: false, message: "Unable to submit request right now." });
  }
}
