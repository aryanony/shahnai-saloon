"use strict";
const config = require("../../config/business.json");
const fallbackCatalog = require("../../config/catalog.fallback.json");
const { fetchCatalogRaw } = require("./appsScript");

const TTL_MS = 45 * 1000;
let cache = { at: 0, data: null };

function fallbackBusiness() {
  return {
    primaryBrand: config.primaryBrand,
    secondaryBrand: config.secondaryBrandEnabled ? config.secondaryBrand : "",
    descriptor: config.descriptor,
    phone: config.phone,
    altPhone: config.alternatePhone,
    whatsapp: config.whatsapp,
    address: [config.address.line1, config.address.locality, config.address.city, config.address.state + " " + config.address.postalCode].join(", "),
    mapsUrl: config.mapsUrl,
    instagramUrl: config.instagramUrl,
    websiteUrl: config.siteUrl,
    // Without the Sheet we cannot know the owner's choice, so fall back to the mode that needs no provider.
    whatsappMode: "CLICK_TO_CHAT",
    formCta: "Send Booking Request",
    successMessage: "Your booking request has been received. We\u2019ll contact you to confirm."
  };
}

/** Accepts only a well-formed Apps Script payload; anything else throws so callers fall back. */
function normalize(raw) {
  if (!raw || typeof raw !== "object" || raw.ok === false) throw new Error("catalog_bad_payload");
  if (!Array.isArray(raw.services) || !Array.isArray(raw.additionalServices) || !raw.business) throw new Error("catalog_bad_shape");
  return {
    business: Object.assign(fallbackBusiness(), raw.business),
    services: raw.services,
    additionalServices: raw.additionalServices
  };
}

async function getCatalog() {
  const now = Date.now();
  if (cache.data && now - cache.at < TTL_MS) return cache.data;
  try {
    const data = Object.assign(normalize(await fetchCatalogRaw()), { source: "sheet" });
    if (!data.services.length) throw new Error("catalog_empty");
    cache = { at: now, data };
    return data;
  } catch (err) {
    console.error("catalog: using fallback -", err.message);
    return {
      business: fallbackBusiness(),
      services: fallbackCatalog.services,
      additionalServices: fallbackCatalog.additionalServices,
      source: "fallback"
    };
  }
}

function _resetForTests() { cache = { at: 0, data: null }; }

module.exports = { getCatalog, fallbackBusiness, _resetForTests };
