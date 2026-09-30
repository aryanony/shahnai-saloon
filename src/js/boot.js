/* Runs synchronously in <head>. Keep it tiny. No inline scripts anywhere, so the CSP can forbid them. */
(function () {
  document.documentElement.classList.add("js");
  var link = document.createElement("link");
  link.rel = "stylesheet";
  link.href = "https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600&family=Jost:wght@400;500;600&display=swap";
  document.head.appendChild(link); // async by nature: doesn't delay first paint, text shows in fallback fonts first (display=swap)
})();
