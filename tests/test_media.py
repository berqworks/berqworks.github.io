import json
import unittest

from _helpers import ROOT
from sitegen.data import load_site, validate

ASSETS = ROOT / "site" / "assets"
FONT_NAMES = ("fraunces", "instrument-sans", "nunito", "baloo2-semibold", "aileron-regular", "aileron-bold")
TURKISH = "çÇğĞıİöÖşŞüÜ"


class MediaTest(unittest.TestCase):
    def setUp(self):
        self.site = load_site(ROOT)

    def test_every_game_has_media(self):
        for game in self.site["games"]:
            media = game["media"]
            self.assertTrue(media.get("icon"), game["id"])
            self.assertEqual(set(media["hero_video"]), {"en", "tr"})
            self.assertEqual(set(media["hero_poster"]), {"en", "tr"})
            for lang in ("en", "tr"):
                self.assertEqual(len(media["screens"][lang]), 6, (game["id"], lang))
                for shot in media["screens"][lang]:
                    self.assertTrue(shot["alt"].strip())
                    self.assertGreater(shot["w"], 0)
                    self.assertGreater(shot["h"], 0)

    def test_media_files_exist(self):
        self.assertEqual(validate(self.site), [])

    def test_puzzle_art_only_in_tile_swap(self):
        manifest = json.loads((ASSETS / "media" / "manifest.json").read_text(encoding="utf-8"))
        for out_path, src in manifest.items():
            if "puzzle-images" in src or "category-covers" in src:
                self.assertTrue(out_path.startswith("tile-swap-puzzle/"), out_path)

    def test_no_old_or_test_footage(self):
        manifest = json.loads((ASSETS / "media" / "manifest.json").read_text(encoding="utf-8"))
        for src in manifest.values():
            for bad in ("eski-kedi-ikonu", "_tablet-", "_desktop-preview-", "test-recording"):
                self.assertNotIn(bad, src)

    def test_fonts_have_turkish(self):
        try:
            from fontTools.ttLib import TTFont
        except ImportError:
            self.skipTest("fontTools not installed (run with .venv-tools/bin/python)")
        for name in FONT_NAMES:
            cmap = TTFont(ASSETS / "fonts" / f"{name}.woff2").getBestCmap()
            missing = [c for c in TURKISH if ord(c) not in cmap]
            self.assertEqual(missing, [], name)

    def test_fonts_and_licenses_present(self):
        for name in FONT_NAMES:
            self.assertTrue((ASSETS / "fonts" / f"{name}.woff2").is_file(), name)
        self.assertGreaterEqual(len(list((ASSETS / "fonts").glob("*LICENSE*.txt"))), 5)

    def test_assets_budget(self):
        total = sum(f.stat().st_size for f in ASSETS.rglob("*") if f.is_file())
        self.assertLess(total, 13 * 1024 * 1024)


if __name__ == "__main__":
    unittest.main()
