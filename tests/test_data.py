import copy
import re
import unittest

from _helpers import ROOT
from sitegen.build import load_forbidden_names
from sitegen.data import load_site, t, validate


def _strings(node):
    if isinstance(node, str):
        yield node
    elif isinstance(node, dict):
        for v in node.values():
            yield from _strings(v)
    elif isinstance(node, list):
        for v in node:
            yield from _strings(v)


class DataTest(unittest.TestCase):
    def setUp(self):
        self.site = load_site(ROOT)

    def test_game_order(self):
        self.assertEqual([g["id"] for g in self.site["games"]],
                         ["mahjong-caravan", "tile-swap-puzzle", "water-sort"])

    def test_valid(self):
        self.assertEqual(validate(self.site), [])

    def test_missing_translation_is_reported(self):
        broken = copy.deepcopy(self.site)
        del broken["games"][1]["card"]["tr"]
        errors = validate(broken)
        self.assertTrue(any("tile-swap-puzzle" in e and "card" in e for e in errors), errors)

    def test_no_forbidden_name(self):
        names = load_forbidden_names(ROOT)
        if not names:
            self.skipTest(".forbidden-names not present on this machine")
        pattern = re.compile(r"\b(" + "|".join(map(re.escape, names)) + r")\b")
        for s in _strings(self.site):
            self.assertIsNone(pattern.search(s), s)

    def test_no_prices(self):
        for s in _strings(self.site):
            for token in ("₺", "$", "USD"):
                self.assertNotIn(token, s)

    def test_studio_intro_exact(self):
        intro = self.site["studio"]["intro"]
        self.assertTrue(intro["en"][0].startswith("BerqWorks is an independent studio that makes games and apps."))
        self.assertEqual(intro["tr"][1], "Bu oyunların hiçbirinde süreye karşı yarışıp kaybetmezsin. "
                                         "Her bulmacanın bir çözümü var. Takıldığında oyun bunu açıkça söylüyor.")

    def test_t_helper(self):
        self.assertEqual(t({"en": "a", "tr": "b"}, "tr"), "b")
        self.assertEqual(t("same", "tr"), "same")

    def test_legal_docs(self):
        docs = {g["id"]: g["legal_docs"] for g in self.site["games"]}
        self.assertEqual(docs["tile-swap-puzzle"], ["privacy-policy", "terms-of-use"])
        self.assertEqual(docs["water-sort"], ["privacy-policy", "terms-of-use", "kvkk"])
        ws = self.site["games"][2]
        self.assertEqual(ws.get("legal_version"), 1)
        self.assertIsNone(self.site["games"][0].get("legal_version"))


if __name__ == "__main__":
    unittest.main()
