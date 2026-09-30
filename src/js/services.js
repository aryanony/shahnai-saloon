(function () {
  "use strict";
  var svcRoot = document.getElementById("services-menu");
  var addonRoot = document.getElementById("addons-menu");
  if (!window.ShahnazCatalog) return;

  function group(services) {
    var order = [], map = {};
    services.forEach(function (s) {
      var cat = s.category || "Other";
      if (!map[cat]) { map[cat] = []; order.push(cat); }
      map[cat].push(s);
    });
    return order.map(function (cat) { return { category: cat, items: map[cat] }; });
  }

  window.ShahnazCatalog.load().then(function (data) {
    var services = (data && data.services) || [];
    var addons = (data && data.additionalServices) || [];

    if (svcRoot) {
      if (!services.length) {
        svcRoot.innerHTML = '<p class="state-note">Please call or WhatsApp us for current services and pricing.</p>';
      } else {
        svcRoot.innerHTML = "";
        group(services).forEach(function (g) {
          var section = document.createElement("div");
          section.className = "menu-group";
          var ul = g.items.map(function (s) {
            return '<li><span class="menu__name">' + s.name + '</span><span class="menu__price">' + window.ShahnazCatalog.formatPrice(s) + "</span></li>";
          }).join("");
          section.innerHTML = "<h3>" + g.category + '</h3><ul class="menu">' + ul + "</ul>";
          svcRoot.appendChild(section);
        });
      }
    }

    if (addonRoot) {
      if (!addons.length) {
        addonRoot.innerHTML = '<p class="state-note">No add-ons listed right now.</p>';
      } else {
        var ul2 = addons.map(function (a) {
          return '<li><span class="menu__name">' + a.name + '</span><span class="menu__price">' + window.ShahnazCatalog.formatPrice(a) + "</span></li>";
        }).join("");
        addonRoot.innerHTML = '<ul class="menu menu--2">' + ul2 + "</ul>";
      }
    }
  });
})();
