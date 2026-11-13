// Language choice. Pure functions are exported for tests; the DOM part runs in browsers only.

const KEY = "bw-lang";

export function pickLang(hash, stored, navLang) {
  const h = (hash || "").replace(/^#/, "");
  if (h === "tr" || h.startsWith("tr-")) return "tr";
  if (h === "en" || h.startsWith("en-")) return "en";
  if (stored === "tr" || stored === "en") return stored;
  return (navLang || "").toLowerCase().startsWith("tr") ? "tr" : "en";
}

export function shouldRedirect(pathname, stored, navLang) {
  if (stored !== null) return null;
  if (!(navLang || "").toLowerCase().startsWith("tr")) return null;
  if (pathname.startsWith("/tr/") || pathname.endsWith(".html")) return null;
  return "/tr" + pathname;
}

function readStored() {
  try { return localStorage.getItem(KEY); } catch (e) { return null; }
}

function store(lang) {
  try { localStorage.setItem(KEY, lang); } catch (e) { /* private mode */ }
}

function init() {
  const root = document.documentElement;
  const nav = navigator.language || "";

  if (root.hasAttribute("data-legal")) {
    const apply = () => {
      const lang = pickLang(location.hash, readStored(), nav);
      root.dataset.lang = lang;
      root.lang = lang;
    };
    apply();
    window.addEventListener("hashchange", apply);
    document.querySelectorAll("[data-legal-lang]").forEach((a) =>
      a.addEventListener("click", () => store(a.dataset.legalLang)));
    return;
  }

  const target = shouldRedirect(location.pathname, readStored(), nav);
  if (target) {
    location.replace(target + location.hash);
    return;
  }
  document.querySelectorAll("[data-lang-switch]").forEach((a) =>
    a.addEventListener("click", () => store(a.dataset.langSwitch)));
}

if (typeof document !== "undefined") init();
