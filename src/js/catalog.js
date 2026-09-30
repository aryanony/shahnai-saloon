/* Shahnaz — catalog loader and generic [data-bind] hydration.
 * Every page ships static fallback text/links (baked from config/business.json at build time)
 * so first paint and crawlers always see correct info even with JS off. This script then
 * refreshes anything the owner has changed in the Sheet since the last deploy.
 *
 * Conventions:
 *   data-bind-text="phone|altPhone|whatsapp|address|brand|secondaryBrand|descriptor"
 *   data-bind-href="phone|whatsapp|maps|instagram"          (whatsapp uses data-wa-text as the prefilled message template)
 *   data-bind-optional                                       hide this element if its bound value is empty
 */
(function (window) {
  "use strict";

  var CATALOG_URL = "/api/catalog";
  var promise = null;

  function fetchJson(url) {
    return fetch(url, { headers: { Accept: "application/json" } }).then(function (res) {
      if (!res.ok) throw new Error("http_" + res.status);
      return res.json();
    });
  }

  function load() {
    if (!promise) {
      promise = fetchJson(CATALOG_URL).catch(function (err) {
        console.error("catalog: falling back to page defaults -", err.message);
        return null; // callers keep the static fallback already in the HTML
      });
    }
    return promise;
  }

  function digits(e164) { return String(e164 || "").replace(/[^\d]/g, ""); }

  function formatPrice(svc) {
    if (!svc || svc.priceType === "Enquiry" || !svc.price) return "Price on enquiry";
    var amount = "\u20B9" + Number(svc.price).toLocaleString("en-IN");
    return svc.priceType === "From" ? "From " + amount : amount;
  }

  function hydrateBusiness(root, business) {
    if (!business) return;
    (root || document).querySelectorAll("[data-bind-text]").forEach(function (el) {
      var key = el.getAttribute("data-bind-text");
      var val = business[key];
      if (val) el.textContent = val;
      if (el.hasAttribute("data-bind-optional")) el.hidden = !val;
    });
    (root || document).querySelectorAll("[data-bind-href]").forEach(function (el) {
      var key = el.getAttribute("data-bind-href");
      if (key === "phone" && business.phone) el.href = "tel:" + business.phone;
      else if (key === "whatsapp" && business.whatsapp) {
        var text = el.getAttribute("data-wa-text") || "";
        el.href = "https://wa.me/" + digits(business.whatsapp) + (text ? "?text=" + encodeURIComponent(text) : "");
      } else if (key === "maps" && business.mapsUrl) el.href = business.mapsUrl;
      else if (key === "instagram" && business.instagramUrl) el.href = business.instagramUrl;
      if (el.hasAttribute("data-bind-optional")) {
        var has = (key === "phone" && business.phone) || (key === "whatsapp" && business.whatsapp) || (key === "maps" && business.mapsUrl) || (key === "instagram" && business.instagramUrl);
        el.hidden = !has;
      }
    });
  }

  window.ShahnazCatalog = { load: load, formatPrice: formatPrice, hydrateBusiness: hydrateBusiness };
})(window);
