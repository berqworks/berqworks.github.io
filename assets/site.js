// Dil seçici (TR/EN) ve e-posta kopyalama. İlk dil, sayfa başındaki satır içi betikle seçilir
// (adres #tr/#en > kayıtlı tercih > cihaz dili); burada düğmeler ve sekme başlığı bağlanır.
(function () {
  var root = document.documentElement;
  function setLang(lang, save) {
    root.setAttribute("data-lang", lang);
    root.lang = lang;
    var title = document.querySelector('meta[name="bw-title-' + lang + '"]');
    if (title) document.title = title.getAttribute("content");
    document.querySelectorAll("[data-set-lang]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-set-lang") === lang));
    });
    if (save) try { localStorage.setItem("bw-lang", lang); } catch (e) {}
  }
  var fromHash = location.hash === "#tr" || location.hash === "#en";
  setLang(root.getAttribute("data-lang") === "tr" ? "tr" : "en", fromHash);
  document.querySelectorAll("[data-set-lang]").forEach(function (b) {
    b.addEventListener("click", function () { setLang(b.getAttribute("data-set-lang"), true); });
  });
  window.addEventListener("hashchange", function () {
    if (location.hash === "#tr" || location.hash === "#en") setLang(location.hash.slice(1), true);
  });

  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var old = btn.innerHTML;
      function done() {
        btn.textContent = root.getAttribute("data-lang") === "tr" ? "Kopyalandı" : "Copied";
        setTimeout(function () { btn.innerHTML = old; }, 1400);
      }
      function select() {
        var addr = btn.parentElement.querySelector(".mail-addr");
        var r = document.createRange(); r.selectNodeContents(addr);
        var s = getSelection(); s.removeAllRanges(); s.addRange(r);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(btn.getAttribute("data-copy")).then(done, select);
      else select();
    });
  });
})();
