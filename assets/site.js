// Dil seçici (TR/EN) ve e-posta kopyalama. Dil tercihi tarayıcıda saklanır; yoksa cihaz diline bakılır.
(function () {
  var root = document.documentElement;
  function setLang(lang) {
    root.setAttribute("data-lang", lang);
    root.lang = lang;
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-set-lang") === lang));
    });
    try { localStorage.setItem("bw-lang", lang); } catch (e) {}
  }
  var saved = null;
  try { saved = localStorage.getItem("bw-lang"); } catch (e) {}
  var fromHash = location.hash === "#tr" || location.hash === "#en" ? location.hash.slice(1) : null;
  setLang(fromHash || saved || ((navigator.language || "en").toLowerCase().indexOf("tr") === 0 ? "tr" : "en"));
  document.querySelectorAll("[data-set-lang]").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang")); });
  });

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var old = btn.innerHTML;
      function done() {
        btn.textContent = root.getAttribute("data-lang") === "tr" ? "Kopyalandı" : "Copied";
        setTimeout(function () { btn.innerHTML = old; }, 1400);
      }
      function select() {
        var code = btn.parentElement.querySelector("code");
        var r = document.createRange(); r.selectNodeContents(code);
        var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(btn.getAttribute("data-copy")).then(done, select);
      else select();
    });
  });
})();
