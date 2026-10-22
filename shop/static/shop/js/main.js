(function () {
  var filters = document.getElementById("filters");
  var cards = document.getElementById("cards");
  if (!filters || !cards) return;

  filters.addEventListener("click", function (e) {
    var b = e.target.closest("button");
    if (!b) return;
    filters.querySelectorAll("button").forEach(function (x) {
      x.setAttribute("aria-pressed", x === b ? "true" : "false");
    });
    cards.querySelectorAll(".card").forEach(function (c) {
      c.hidden = b.dataset.f !== "all" && c.dataset.cat !== b.dataset.f;
    });
  });
})();
