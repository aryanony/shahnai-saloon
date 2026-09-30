(function () {
  "use strict";
  var grid = document.getElementById("home-services");
  if (!grid || !window.ShahnazCatalog) return;
  window.ShahnazCatalog.load().then(function (data) {
    var services = (data && data.services) || [];
    if (!services.length) { grid.innerHTML = '<p class="state-note">Please call or WhatsApp us for current services.</p>'; return; }
    var ul = document.createElement("ul");
    ul.className = "menu menu--2";
    services.slice(0, 8).forEach(function (s) {
      var li = document.createElement("li");
      li.innerHTML = '<span class="menu__name">' + s.name + '</span><span class="menu__price">' + window.ShahnazCatalog.formatPrice(s) + "</span>";
      ul.appendChild(li);
    });
    grid.innerHTML = "";
    grid.appendChild(ul);
  });
})();
