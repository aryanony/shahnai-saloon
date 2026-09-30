(function () {
  "use strict";

  var form = document.getElementById("booking-form");
  if (!form) return;

  var loadStamp = (window.performance && performance.now) ? performance.now() : Date.now();
  var serviceSel = document.getElementById("service");
  var addonBox = document.getElementById("addon-list");
  var submitBtn = document.getElementById("submit-btn");
  var panelForm = document.getElementById("panel-form");
  var panelOk = document.getElementById("panel-success");
  var panelErr = document.getElementById("panel-error");
  var bidEl = document.getElementById("booking-id");
  var okMsgEl = document.getElementById("success-message");
  var waFallback = document.getElementById("wa-fallback");
  var latestBusiness = null;

  function uuid() {
    if (window.crypto && crypto.randomUUID) return crypto.randomUUID();
    var b = new Uint8Array(16);
    (window.crypto || {}).getRandomValues ? crypto.getRandomValues(b) : b.forEach(function (_, i) { b[i] = Math.floor(Math.random() * 256); });
    b[6] = (b[6] & 0x0f) | 0x40; b[8] = (b[8] & 0x3f) | 0x80;
    var h = Array.prototype.map.call(b, function (x) { return x.toString(16).padStart(2, "0"); }).join("");
    return h.slice(0, 8) + "-" + h.slice(8, 12) + "-" + h.slice(12, 16) + "-" + h.slice(16, 20) + "-" + h.slice(20);
  }
  var requestToken = uuid();

  function groupByCategory(services) {
    var order = [], map = {};
    services.forEach(function (s) {
      var cat = s.category || "Other";
      if (!map[cat]) { map[cat] = []; order.push(cat); }
      map[cat].push(s);
    });
    return order.map(function (cat) { return { category: cat, items: map[cat] }; });
  }

  function fillServices(services) {
    serviceSel.innerHTML = '<option value="" disabled selected>Choose a service</option>';
    groupByCategory(services).forEach(function (group) {
      var og = document.createElement("optgroup");
      og.label = group.category;
      group.items.forEach(function (s) {
        var opt = document.createElement("option");
        opt.value = s.id;
        opt.textContent = s.name + (window.ShahnazCatalog ? " \u2014 " + window.ShahnazCatalog.formatPrice(s) : "");
        og.appendChild(opt);
      });
      serviceSel.appendChild(og);
    });
  }

  function fillAddons(addons) {
    addonBox.innerHTML = "";
    addons.forEach(function (a) {
      var id = "addon-" + a.id;
      var label = document.createElement("label");
      label.innerHTML = '<input type="checkbox" name="addonIds" value="' + a.id + '" id="' + id + '"><span>' + a.name + "</span>";
      addonBox.appendChild(label);
    });
  }

  if (window.ShahnazCatalog) {
    window.ShahnazCatalog.load().then(function (data) {
      latestBusiness = data && data.business;
      fillServices((data && data.services) || []);
      fillAddons((data && data.additionalServices) || []);
      if (data && data.business && data.business.successMessage && okMsgEl) okMsgEl.textContent = data.business.successMessage;
      if (data && data.business && data.business.formCta && submitBtn) submitBtn.querySelector(".label").textContent = data.business.formCta;
    });
  }

  function err(fieldId, message) {
    var wrap = document.getElementById(fieldId).closest(".field");
    var e = wrap.querySelector(".err");
    if (message) { wrap.classList.add("bad"); if (e) e.textContent = message; }
    else wrap.classList.remove("bad");
  }

  function validMobile(v) { return /^(?:\+?91|0)?[6-9]\d{9}$/.test(v.replace(/[\s\-().]/g, "")); }
  function validDate(v) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(v)) return false;
    var chosen = new Date(v + "T00:00:00");
    var today = new Date(); today.setHours(0, 0, 0, 0);
    return chosen >= today;
  }

  function validate() {
    var ok = true;
    if (form.name.value.trim().length < 2) { err("name", "Please enter your name."); ok = false; } else err("name");
    if (!validMobile(form.mobile.value)) { err("mobile", "Please enter a valid 10-digit mobile number."); ok = false; } else err("mobile");
    if (!form.serviceId.value) { err("service", "Please choose a service."); ok = false; } else err("service");
    if (!validDate(form.preferredDate.value)) { err("preferredDate", "Please choose today or a later date."); ok = false; } else err("preferredDate");
    if (form.note.value.length > 300) { err("note", "Please keep your note under 300 characters."); ok = false; } else err("note");
    return ok;
  }

  function show(panel) {
    [panelForm, panelOk, panelErr].forEach(function (p) { if (p) p.classList.remove("on"); });
    if (panel) panel.classList.add("on");
    if (panel) panel.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  var trackedStart = false;
  form.addEventListener("focusin", function () {
    if (!trackedStart && window.ShahnazAnalytics) { window.ShahnazAnalytics.track("booking_start", {}); trackedStart = true; }
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (form.classList.contains("busy") || !validate()) return;

    var addonIds = Array.prototype.map.call(form.querySelectorAll('input[name="addonIds"]:checked'), function (el) { return el.value; });
    var selectedOpt = serviceSel.options[serviceSel.selectedIndex];

    var payload = {
      name: form.name.value.trim(),
      mobile: form.mobile.value.trim(),
      serviceId: form.serviceId.value,
      addonIds: addonIds,
      preferredDate: form.preferredDate.value,
      preferredTime: form.preferredTime.value || "",
      note: form.note.value.trim(),
      page: location.pathname,
      requestToken: requestToken,
      honeypot: form.company.value,
      fillTimeMs: Math.round(((window.performance && performance.now) ? performance.now() : Date.now()) - loadStamp)
    };

    form.classList.add("busy");
    submitBtn.disabled = true;

    fetch("/api/booking", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload) })
      .then(function (res) { return res.json().then(function (data) { return { status: res.status, data: data }; }); })
      .then(function (result) {
        form.classList.remove("busy");
        submitBtn.disabled = false;
        if (result.data && result.data.ok) {
          if (bidEl) bidEl.textContent = result.data.bookingId;
          show(panelOk);
          if (window.ShahnazAnalytics) window.ShahnazAnalytics.track("booking_submit", { service: payload.serviceId });
        } else {
          throw new Error((result.data && result.data.message) || "submit_failed");
        }
      })
      .catch(function () {
        form.classList.remove("busy");
        submitBtn.disabled = false;
        if (waFallback) {
          var msg = "Hi, I tried to send a booking request on the website but it did not go through. " +
            "Name: " + (payload.name || "-") + ". Service: " + (selectedOpt ? selectedOpt.textContent : payload.serviceId) +
            ". Preferred date: " + (payload.preferredDate || "-") + ".";
          waFallback.setAttribute("data-wa-text", msg);
          if (window.ShahnazCatalog && latestBusiness) window.ShahnazCatalog.hydrateBusiness(waFallback.parentElement, latestBusiness);
        }
        show(panelErr);
        if (window.ShahnazAnalytics) window.ShahnazAnalytics.track("booking_error", {});
      });
  });
})();
