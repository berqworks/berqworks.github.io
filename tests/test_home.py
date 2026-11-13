import re
import unittest

from _helpers import ROOT
from sitegen.data import load_site
from sitegen.home import render_home


class HomeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        site = load_site(ROOT)
        cls.site = site
        cls.en = render_home(site, "en")
        cls.tr = render_home(site, "tr")

    def test_intro_copy(self):
        for p in self.site["studio"]["intro"]["en"]:
            self.assertIn(p.replace("'", "&#x27;"), self.en)
        self.assertIn(self.site["studio"]["intro"]["tr"][0], self.tr)

    def test_game_links_in_order(self):
        self.assertEqual(re.findall(r'class="game-row[^"]*" href="([^"]+)"', self.en),
                         ["/games/mahjong-caravan/", "/games/tile-swap-puzzle/", "/games/water-sort/"])
        self.assertEqual(re.findall(r'class="game-row[^"]*" href="([^"]+)"', self.tr),
                         ["/tr/games/mahjong-caravan/", "/tr/games/tile-swap-puzzle/", "/tr/games/water-sort/"])

    def test_alternating_sides(self):
        self.assertEqual(re.findall(r"game-row--(left|right)", self.en), ["left", "right", "left"])

    def test_status_and_age(self):
        self.assertEqual(self.en.count("Coming soon · Android"), 3)
        self.assertEqual(self.en.count("Ages 3–8"), 1)
        self.assertEqual(self.tr.count("Yakında · Android"), 3)

    def test_no_puzzle_art_or_store_links(self):
        for bad in ("puzzle-images", "category-covers", "swap.webp", "play.google.com"):
            self.assertNotIn(bad, self.en)
            self.assertNotIn(bad, self.tr)

    def test_language_pair(self):
        self.assertIn('<html lang="tr">', self.tr)
        self.assertIn('hreflang="tr" href="https://berqworks.com/tr/"', self.en)


if __name__ == "__main__":
    unittest.main()
