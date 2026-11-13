// Language choice.
// The block between core:start and core:end is also inlined (without "export") as a classic
// script at the top of every <head>, so the language is set and the first-visit redirect runs
// before the first paint. This module then wires the switches and refines the legal-page
// language from the #hash target once the DOM exists.

// core:start
export function pickLang(hash, stored, navLang, targetLang = null) {
  if (targetLang === "tr" || targetLang === "en") return targetLang;
  const h = (hash || "").replace(/^#/, "");
  if (h === "tr" || h.startsWith("tr-")) return "tr";
  if (h === "en" || h.startsWith("en-")) return "en";
  if (stored === "tr" || stored === "en") return stored;
  return (navLang || "").toLowerCase().startsWith("tr") ? "tr" : "en";
}

// Moves within the site never redirect, so the EN switch works even when storage is blocked.
export function shouldRedirect(pathname, stored, navLang, referrer = "", origin = "") {
  if (stored !== null) return null;
  if (origin && referrer && referrer.startsWith(origin + "/")) return null;
  if (!(navLang || "").toLowerCase().startsWith("tr")) return null;
  if (pathname.startsWith("/tr/") || pathname.endsWith(".html")) return null;
  return "/tr" + pathname;
}

export function decide(env) {
  if (env.legal) return { lang: pickLang(env.hash, env.stored, env.navLang), redirect: null };
  return { lang: null, redirect: shouldRedirect(env.pathname, env.stored, env.navLang, env.referrer, env.origin) };
}
// core:end

const KEY = "bw-lang";

function readStored() {
  try { return localStorage.getItem(KEY); } catch (e) { return null; }
}

function store(lang) {
  try { localStorage.setItem(KEY, lang); } catch (e) { /* private mode */ }
}

function init() {
  const root = document.documentElement;

  if (root.hasAttribute("data-legal")) {
    const apply = () => {
      let target = null;
      try { target = document.getElementById(decodeURIComponent(location.hash.slice(1))); } catch (e) { /* bad hash */ }
      const holder = target && target.closest("section[lang]");
      const lang = pickLang(location.hash, readStored(), navigator.language || "", holder ? holder.lang : null);
      root.dataset.lang = lang;
      root.lang = lang;
      if (target) target.scrollIntoView();
    };
    apply();
    window.addEventListener("hashchange", apply);
    document.querySelectorAll("[data-legal-lang]").forEach((a) =>
      a.addEventListener("click", () => store(a.dataset.legalLang)));
    return;
  }

  document.querySelectorAll("[data-lang-switch]").forEach((a) =>
    a.addEventListener("click", () => store(a.dataset.langSwitch)));
}

if (typeof document !== "undefined") init();
