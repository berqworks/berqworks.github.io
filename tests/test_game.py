import copy
import re
import unittest

from _helpers import ROOT
from sitegen.data import load_site
from sitegen.game import render_game

SECTIONS = ["hero", "how", "highlights", "screens", "details", "legal"]


class GameTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = load_site(ROOT)
        cls.games = {g["id"]: g for g in cls.site["games"]}

    def render(self, gid, lang):
        return render_game(self.site, self.games[gid], lang)

    def test_section_order(self):
        for gid in self.games:
            for lang in ("en", "tr"):
                html = self.render(gid, lang)
                found = [s for s in re.findall(r'<section[^>]* id="([a-z]+)"', html) if s in SECTIONS]
                self.assertEqual(found, SECTIONS, (gid, lang))

    def test_legal_links(self):
        mj = self.render("mahjong-caravan", "en")
        self.assertIn('href="/games/mahjong-caravan/kvkk.html#en"', mj)
        self.assertIn('href="/games/mahjong-caravan/privacy-policy.html#en"', mj)
        ts = self.render("tile-swap-puzzle", "tr")
        self.assertIn('href="/games/tile-swap-puzzle/terms-of-use.html#tr"', ts)
        self.assertNotIn("kvkk", ts)

    def test_portrait_only_for_water_sort(self):
        self.assertIn("hero--portrait", self.render("water-sort", "en"))
        self.assertNotIn("hero--portrait", self.render("mahjong-caravan", "en"))

    def test_video_per_language(self):
        self.assertIn("/assets/media/water-sort/hero-tr.mp4", self.render("water-sort", "tr"))
        self.assertIn("/assets/media/water-sort/hero-en.mp4", self.render("water-sort", "en"))
        self.assertIn("/assets/media/water-sort/screen-tr-1.webp", self.render("water-sort", "tr"))

    def test_coming_soon_until_play_url(self):
        html = self.render("water-sort", "en")
        self.assertIn("Coming soon to Google Play", html)
        self.assertNotIn("play.google.com", html)
        game = copy.deepcopy(self.games["water-sort"])
        game["play_url"] = "https://play.google.com/store/apps/details?id=com.berqworks.watersort"
        live = render_game(self.site, game, "en")
        self.assertIn('class="play" href="https://play.google.com/store/apps/details?id=com.berqworks.watersort"', live)
        self.assertNotIn("Coming soon to Google Play", live)

    def test_hero_video_has_size(self):
        self.assertRegex(self.render("water-sort", "en"), r'<video[^>]* width="540" height="900"')
        self.assertRegex(self.render("mahjong-caravan", "en"), r'<video[^>]* width="960" height="432"')

    def test_theme_applied(self):
        html = self.render("water-sort", "en")
        self.assertIn('data-game="water-sort"', html)
        self.assertIn("--bg:#0F1424", html)

    def test_no_puzzle_art_outside_tile_swap(self):
        for gid in ("mahjong-caravan", "water-sort"):
            self.assertNotIn("puzzle-images", self.render(gid, "en"))
            self.assertNotIn("swap.webp", self.render(gid, "en"))

    def test_details_rows(self):
        html = self.render("water-sort", "tr")
        self.assertIn("Android · telefon ve tablet · dikey", html)
        self.assertIn("Reklamsız Paket", html)

    def test_title(self):
        self.assertIn("<title>Water Sort: Renk Atlası · BerqWorks</title>", self.render("water-sort", "tr"))


if __name__ == "__main__":
    unittest.main()
