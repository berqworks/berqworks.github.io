import re
import tempfile
import unittest
from pathlib import Path

from _helpers import ROOT
from sitegen.build import build, missing_required
from sitegen.data import load_site
from sitegen.legal import render_legal

CSS = (ROOT / "site" / "css" / "site.css").read_text(encoding="utf-8")


class LegalTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = load_site(ROOT)
        cls.games = {g["id"]: g for g in cls.site["games"]}

    def test_both_languages_and_dates(self):
        html = render_legal(self.site, self.games["water-sort"], "kvkk")
        for needle in ('id="tr"', 'id="en"', 'id="tr-1"', 'id="en-1"',
                       "Son güncelleme: 13 Kasım 2026", "Last updated: 13 November 2026",
                       "Sürüm 1", "Version 1", "data-legal"):
            self.assertIn(needle, html)

    def test_no_version_for_mahjong(self):
        html = render_legal(self.site, self.games["mahjong-caravan"], "privacy-policy")
        self.assertNotIn("Sürüm", html)
        self.assertNotIn("Version 1", html)

    def test_legacy_links_absolute(self):
        html = render_legal(self.site, self.games["mahjong-caravan"], "terms-of-use", legacy=True)
        self.assertNotIn('href="privacy-policy.html', html)
        self.assertIn('href="/games/mahjong-caravan/privacy-policy.html#tr-6"', html)
        self.assertIn('<link rel="canonical" href="https://berqworks.com/games/mahjong-caravan/terms-of-use.html">', html)

    def test_canonical_links_stay_relative(self):
        html = render_legal(self.site, self.games["water-sort"], "privacy-policy")
        self.assertIn('href="kvkk.html#tr"', html)

    def test_nav_follows_page_language(self):
        html = render_legal(self.site, self.games["water-sort"], "privacy-policy")
        self.assertIn('<a class="legal-tr" href="/tr/#games">Oyunlar</a>', html)
        self.assertIn('<a class="legal-en" href="/#games">Games</a>', html)
        self.assertIn('<span class="legal-tr">İletişim</span>', html)

    def test_titles_and_theme(self):
        html = render_legal(self.site, self.games["tile-swap-puzzle"], "terms-of-use")
        self.assertIn("Kullanım Koşulları", html)
        self.assertIn("Terms of Use", html)
        self.assertIn('data-game="tile-swap-puzzle"', html)

    def test_hiding_only_when_language_known(self):
        compact = re.sub(r"\s+", " ", CSS)
        self.assertRegex(compact, r'html\[data-lang="tr"\] \.legal-en')
        self.assertRegex(compact, r'html\[data-lang="en"\] \.legal-tr')
        for selectors, decl in re.findall(r"([^{}]+)\{([^}]*)\}", compact):
            if "display: none" in decl and ".legal-" in selectors:
                for sel in selectors.split(","):
                    if ".legal-en" in sel or ".legal-tr" in sel:
                        self.assertTrue(sel.strip().startswith("html[data-lang="), sel)

    def test_all_required_paths_built(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "public"
            build(ROOT, out)
            self.assertEqual(missing_required(out), [])
            legacy = (out / "tile-swap-puzzle/privacy-policy.html").read_text(encoding="utf-8")
            self.assertIn("Privacy Policy", legacy)


if __name__ == "__main__":
    unittest.main()
