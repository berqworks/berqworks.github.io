import { test } from "node:test";
import assert from "node:assert/strict";
import { pickLang, shouldRedirect } from "../../site/js/lang.js";

test("section anchor picks its language", () => {
  assert.equal(pickLang("#tr-7", "en", "en-US"), "tr");
  assert.equal(pickLang("#en", "tr", "tr"), "en");
});

test("stored choice beats browser language", () => {
  assert.equal(pickLang("", "en", "tr-TR"), "en");
});

test("browser language is the fallback", () => {
  assert.equal(pickLang("", null, "tr-TR"), "tr");
  assert.equal(pickLang("", null, "de-DE"), "en");
});

test("first Turkish visit goes to /tr/", () => {
  assert.equal(shouldRedirect("/games/water-sort/", null, "tr-TR"), "/tr/games/water-sort/");
  assert.equal(shouldRedirect("/", null, "tr"), "/tr/");
});

test("explicit English choice is respected", () => {
  assert.equal(shouldRedirect("/", "en", "tr-TR"), null);
});

test("no redirect on Turkish pages, legal pages or non-Turkish browsers", () => {
  assert.equal(shouldRedirect("/tr/", null, "tr"), null);
  assert.equal(shouldRedirect("/games/water-sort/privacy-policy.html", null, "tr"), null);
  assert.equal(shouldRedirect("/", null, "en-GB"), null);
});

test("an anchor inside a language section keeps that language", () => {
  // EN terms link to #third-party-notices (no en- prefix); target sits in the lang="en" section.
  assert.equal(pickLang("#third-party-notices", "tr", "tr-TR", "en"), "en");
  assert.equal(pickLang("#tr-7", "en", "en-US", "tr"), "tr");
});

test("navigation inside the site never redirects (storage may be blocked)", () => {
  const origin = "https://berqworks.com";
  assert.equal(shouldRedirect("/", null, "tr-TR", origin + "/tr/", origin), null);
  assert.equal(shouldRedirect("/", null, "tr-TR", "https://www.google.com/", origin), "/tr/");
  assert.equal(shouldRedirect("/", null, "tr-TR", "", origin), "/tr/");
});
