(function () {
  "use strict";

  document.querySelectorAll("[data-year]").forEach(function (el) { el.textContent = new Date().getFullYear(); });

  /* ---- Nav ---- */
  var header = document.querySelector("[data-header]");
  var toggle = document.querySelector("[data-menu-toggle]");
  if (header && toggle) {
    toggle.addEventListener("click", function () {
      var open = header.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    header.querySelectorAll(".nav ul a").forEach(function (a) {
      a.addEventListener("click", function () { header.classList.remove("open"); toggle.setAttribute("aria-expanded", "false"); });
    });
  }
  var here = location.pathname.replace(/index\.html$/, "");
  document.querySelectorAll(".nav ul a").forEach(function (a) {
    var href = a.getAttribute("href");
    if (href === here || (href !== "/" && here.indexOf(href) === 0)) a.setAttribute("aria-current", "page");
  });

  /* ---- Business info hydration (every page) ---- */
  if (window.ShahnazCatalog) {
    window.ShahnazCatalog.load().then(function (data) {
      if (data && data.business) window.ShahnazCatalog.hydrateBusiness(document, data.business);
    });
  }

  /* ---- Scroll reveal (progressive enhancement only; .reveal is visible without .js on <html>) ---- */
  var reveals = document.querySelectorAll(".reveal");
  if (reveals.length && "IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("in"); io.unobserve(entry.target); }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  /* ---- Consent-gated analytics ---- */
  var CONSENT_KEY = "shahnaz_consent"; // "granted" | "denied"
  var banner = document.querySelector("[data-consent]");

  function setConsent(value) {
    try { localStorage.setItem(CONSENT_KEY, value); } catch (e) { /* private browsing: ask again next visit */ }
    if (value === "granted" && window.ShahnazAnalytics) window.ShahnazAnalytics.enable();
    if (banner) banner.hidden = true;
  }
  var stored = null;
  try { stored = localStorage.getItem(CONSENT_KEY); } catch (e) { /* ignore */ }
  if (stored === "granted" && window.ShahnazAnalytics) window.ShahnazAnalytics.enable();
  if (banner) {
    if (stored) banner.hidden = true;
    else {
      banner.hidden = false;
      var yes = banner.querySelector("[data-consent-accept]");
      var no = banner.querySelector("[data-consent-decline]");
      if (yes) yes.addEventListener("click", function () { setConsent("granted"); });
      if (no) no.addEventListener("click", function () { setConsent("denied"); });
    }
  }

  /* ---- Generic click analytics: any element with data-analytics="event_name" ---- */
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-analytics]");
    if (!el || !window.ShahnazAnalytics) return;
    window.ShahnazAnalytics.track(el.getAttribute("data-analytics"), { label: el.getAttribute("data-analytics-label") || "" });
  });
  document.querySelectorAll("details.faq-item, .faq details").forEach(function (d) {
    d.addEventListener("toggle", function () {
      if (d.open && window.ShahnazAnalytics) window.ShahnazAnalytics.track("faq_open", { label: (d.querySelector("summary") || {}).textContent || "" });
    });
  });
})();
