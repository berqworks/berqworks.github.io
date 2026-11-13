import re
import unittest

from _helpers import ROOT
from sitegen.data import load_site
from sitegen.layout import page

CSS = (ROOT / "site" / "css" / "site.css").read_text(encoding="utf-8")


class LayoutTest(unittest.TestCase):
    def setUp(self):
        self.site = load_site(ROOT)
        self.html = page(site=self.site, lang="tr", title="BerqWorks", description="d",
                         path="/tr/", alt_path="/", body="<p>x</p>")

    def test_lang_and_canonical(self):
        self.assertIn('<html lang="tr">', self.html)
        self.assertIn('<link rel="canonical" href="https://berqworks.com/tr/">', self.html)

    def test_hreflang(self):
        self.assertIn('hreflang="en" href="https://berqworks.com/"', self.html)
        self.assertIn('hreflang="tr" href="https://berqworks.com/tr/"', self.html)
        self.assertIn('hreflang="x-default" href="https://berqworks.com/"', self.html)

    def test_contact_and_nav(self):
        self.assertIn('href="mailto:berqworks@gmail.com"', self.html)
        self.assertIn('id="contact"', self.html)
        self.assertIn("İletişim", self.html)
        self.assertIn('data-lang-switch="en"', self.html)

    def test_no_third_party(self):
        for host in ("googleapis", "gstatic", "cdn."):
            self.assertNotIn(host, self.html)
            self.assertNotIn(host, CSS)

    def test_theme_vars(self):
        game = self.site["games"][2]
        html = page(site=self.site, lang="en", title="t", description="d", path="/games/water-sort/",
                    alt_path="/tr/games/water-sort/", body="", theme=game["theme"], game_id="water-sort",
                    heading_font="aileron")
        self.assertIn('data-game="water-sort"', html)
        self.assertIn("--bg:#0F1424", html)
        self.assertIn("--heading-font:&#x27;Aileron&#x27;", html)

    def test_css_rules(self):
        compact = re.sub(r"\s+", "", CSS)
        self.assertIn("font-variant-ligatures:none", compact)
        self.assertIn("prefers-reduced-motion", CSS)
        self.assertRegex(CSS, r"url\(/assets/fonts/[a-z0-9-]+\.woff2\)")


if __name__ == "__main__":
    unittest.main()
