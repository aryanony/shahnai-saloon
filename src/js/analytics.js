/* Shahnaz — analytics wrapper. Nothing loads or records until main.js calls .enable()
 * after the visitor accepts the on-page consent banner (opt-in-first).
 * Replace the two IDs below once issued; both loaders are inert until then.
 */
(function (window) {
  "use strict";

  var GTM_CONTAINER_ID = "GTM-XXXXXXX";
  var CLARITY_PROJECT_ID = "xxxxxxxxxx";
  var ALLOWED_KEYS = ["label", "service", "category", "page"];
  var enabled = false;

  window.dataLayer = window.dataLayer || [];

  function configured(id, placeholderFragment) {
    return Boolean(id) && id.toLowerCase().indexOf(placeholderFragment) === -1;
  }

  function loadGTM(id) {
    (function (w, d, s, l, i) {
      w[l] = w[l] || [];
      w[l].push({ "gtm.start": Date.now(), event: "gtm.js" });
      var f = d.getElementsByTagName(s)[0], j = d.createElement(s), dl = l !== "dataLayer" ? "&l=" + l : "";
      j.async = true;
      j.src = "https://www.googletagmanager.com/gtm.js?id=" + i + dl;
      f.parentNode.insertBefore(j, f);
    })(window, document, "script", "dataLayer", id);
  }

  function loadClarity(id) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r);
      t.async = 1;
      t.src = "https://www.clarity.ms/tag/" + i;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", id);
  }

  function sanitize(detail) {
    var out = {};
    if (!detail) return out;
    ALLOWED_KEYS.forEach(function (k) {
      if (detail[k]) out[k] = String(detail[k]).slice(0, 80);
    });
    return out;
  }

  function enable() {
    if (enabled) return;
    enabled = true;
    if (configured(GTM_CONTAINER_ID, "xxxx")) loadGTM(GTM_CONTAINER_ID);
    if (configured(CLARITY_PROJECT_ID, "xxxx")) loadClarity(CLARITY_PROJECT_ID);
  }

  function track(eventName, detail) {
    if (!enabled) return; // consent not granted: record nothing, not even locally
    var payload = sanitize(detail);
    payload.event = eventName;
    window.dataLayer.push(payload);
  }

  window.ShahnazAnalytics = { enable: enable, track: track };
})(window);
