// Language choice. Pure functions are exported for tests; the DOM part runs in browsers only.

const KEY = "bw-lang";

// targetLang: lang of the section holding the #hash target, when the page has one.
export function pickLang(hash, stored, navLang, targetLang = null) {
  if (targetLang === "tr" || targetLang === "en") return targetLang;
  const h = (hash || "").replace(/^#/, "");
  if (h === "tr" || h.startsWith("tr-")) return "tr";
  if (h === "en" || h.startsWith("en-")) return "en";
  if (stored === "tr" || stored === "en") return stored;
  return (navLang || "").toLowerCase().startsWith("tr") ? "tr" : "en";
}

// referrer/origin: moves within the site never redirect, so the EN switch works
// even when localStorage is blocked and no choice can be stored.
export function shouldRedirect(pathname, stored, navLang, referrer = "", origin = "") {
  if (stored !== null) return null;
  if (origin && referrer && referrer.startsWith(origin + "/")) return null;
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
      let target = null;
      try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { /* bad hash */ }
      const holder = target && target.closest("section[lang]");
      const lang = pickLang(location.hash, readStored(), nav, holder ? holder.lang : null);
      root.dataset.lang = lang;
      root.lang = lang;
    };
    apply();
    window.addEventListener("hashchange", apply);
    document.querySelectorAll("[data-legal-lang]").forEach((a) =>
      a.addEventListener("click", () => store(a.dataset.legalLang)));
    return;
  }

  const target = shouldRedirect(location.pathname, readStored(), nav, document.referrer, location.origin);
  if (target) {
    location.replace(target + location.hash);
    return;
  }
  document.querySelectorAll("[data-lang-switch]").forEach((a) =>
    a.addEventListener("click", () => store(a.dataset.langSwitch)));
}

if (typeof document !== "undefined") init();
