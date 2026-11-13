import re
import tempfile
import unittest
from pathlib import Path

from _helpers import ROOT, SOURCE  # noqa: F401  (sets sys.path)
from sitegen import urls
from sitegen.build import REQUIRED_PATHS, build, forbidden_hits, missing_required, total_size

EXPECTED = {
    "games/water-sort/privacy-policy.html", "games/water-sort/terms-of-use.html", "games/water-sort/kvkk.html",
    "games/mahjong-caravan/privacy-policy.html", "games/mahjong-caravan/terms-of-use.html", "games/mahjong-caravan/kvkk.html",
    "games/tile-swap-puzzle/privacy-policy.html", "games/tile-swap-puzzle/terms-of-use.html",
    "mahjong-caravan/privacy-policy.html", "mahjong-caravan/terms-of-use.html",
    "tile-swap-puzzle/privacy-policy.html", "tile-swap-puzzle/terms-of-use.html",
    "games/water-sort/config.json", "app-ads.txt", "index.html",
}


class BuildTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.TemporaryDirectory()
        cls.out = Path(cls._tmp.name) / "public"
        build(ROOT, cls.out)

    @classmethod
    def tearDownClass(cls):
        cls._tmp.cleanup()

    def test_required_paths_exact(self):
        self.assertEqual(set(REQUIRED_PATHS), EXPECTED)

    def test_passthrough_byte_identical(self):
        built = (self.out / "games/water-sort/config.json").read_bytes()
        self.assertEqual(built, (ROOT / "site/root/games/water-sort/config.json").read_bytes())
        src = SOURCE / "water-sort/config.json"
        if src.exists():
            self.assertEqual(built, src.read_bytes())
        self.assertIn("pub-3762683248469893", (self.out / "app-ads.txt").read_text())

    def test_build_output_has_all_required(self):
        self.assertEqual(missing_required(self.out), [])

    def test_build_output_has_no_forbidden_name(self):
        self.assertEqual(forbidden_hits(self.out), [])

    def test_sitemap(self):
        xml = (self.out / "sitemap.xml").read_text(encoding="utf-8")
        locs = re.findall(r"<loc>([^<]+)</loc>", xml)
        self.assertEqual(len(locs), 8)
        self.assertTrue(all(l.startswith("https://berqworks.com/") for l in locs))
        self.assertFalse(any(l.endswith(".html") for l in locs))
        self.assertIn('hreflang="tr"', xml)

    def test_robots_and_404(self):
        self.assertIn("Sitemap: https://berqworks.com/sitemap.xml",
                      (self.out / "robots.txt").read_text(encoding="utf-8"))
        page = (self.out / "404.html").read_text(encoding="utf-8")
        self.assertIn('href="/"', page)
        self.assertIn('href="/tr/"', page)

    def test_brand_assets(self):
        for rel in ("assets/brand/favicon.svg", "assets/brand/og.png", "assets/brand/og-mahjong-caravan.png",
                    "assets/brand/og-tile-swap-puzzle.png", "assets/brand/og-water-sort.png"):
            self.assertTrue((self.out / rel).is_file(), rel)

    def test_png_whitelist(self):
        pngs = sorted(p.relative_to(self.out).as_posix() for p in self.out.rglob("*.png"))
        self.assertEqual(pngs, ["assets/brand/og-mahjong-caravan.png", "assets/brand/og-tile-swap-puzzle.png",
                                "assets/brand/og-water-sort.png", "assets/brand/og.png",
                                "assets/media/water-sort/mask.png"])

    def test_size_budget(self):
        self.assertLess(total_size(self.out), 15 * 1024 * 1024)


class GuardTest(unittest.TestCase):
    def test_missing_required_lists_absent(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(len(missing_required(Path(d))), 15)

    def test_forbidden_hits(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)
            (p / "x.html").write_text("Merhaba Zeynep", encoding="utf-8")
            (p / "y.html").write_text("berqworks BerqWorks", encoding="utf-8")
            (p / "z.txt").write_text("Seher Hatipoğlu", encoding="utf-8")
            hits = forbidden_hits(p)
            self.assertIn("x.html", hits)
            self.assertNotIn("y.html", hits)
            self.assertNotIn("z.txt", hits)  # data controller named in legal texts

    def test_urls(self):
        self.assertEqual(urls.game_path("tr", "water-sort"), "/tr/games/water-sort/")
        self.assertEqual(urls.game_path("en", "water-sort"), "/games/water-sort/")
        self.assertEqual(urls.home_path("en"), "/")
        self.assertEqual(urls.home_path("tr"), "/tr/")
        self.assertEqual(urls.legal_path("water-sort", "kvkk"), "/games/water-sort/kvkk.html")


if __name__ == "__main__":
    unittest.main()
