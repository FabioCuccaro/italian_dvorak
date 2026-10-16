import unittest
from pathlib import Path

from kbeval.corpus import load_corpus
from kbeval.keyboard import Key, roll_direction
from kbeval.layouts import load_layout, load_layouts
from kbeval.metrics import analyze, bigram_kind, is_redirect, summarize

ROOT = Path(__file__).resolve().parent.parent
QWERTY = ROOT / "layouts" / "01-qwerty-it.json"
V1 = ROOT / "layouts" / "10-v1.json"


def qkey(layout, ch):
    return layout.keys[ch]


class RollDirection(unittest.TestCase):
    """Inward means towards the index finger. The v1 optimiser had this backwards."""

    def setUp(self):
        self.q = load_layout(QWERTY)

    def roll(self, pair):
        return roll_direction(qkey(self.q, pair[0]), qkey(self.q, pair[1]))

    def test_left_hand(self):
        for pair in ("as", "sd", "df", "af", "qw", "zf"):
            self.assertEqual(self.roll(pair), "inward", pair)
        for pair in ("sa", "fd", "fa", "rw"):
            self.assertEqual(self.roll(pair), "outward", pair)

    def test_right_hand(self):
        for pair in ("lk", "kj", "oi", "lh"):
            self.assertEqual(self.roll(pair), "inward", pair)
        for pair in ("kl", "jk", "io", "hl"):
            self.assertEqual(self.roll(pair), "outward", pair)

    def test_not_a_roll(self):
        self.assertIsNone(self.roll("fg"))  # same finger
        self.assertIsNone(self.roll("aj"))  # different hands

    def test_bigram_kinds(self):
        k = lambda c: qkey(self.q, c)
        self.assertEqual(bigram_kind(k("f"), k("f")), "repeat")
        self.assertEqual(bigram_kind(k("f"), k("r")), "same_finger")
        self.assertEqual(bigram_kind(k("f"), k("j")), "alternation")

    def test_redirect(self):
        k = lambda c: qkey(self.q, c)
        self.assertTrue(is_redirect(k("s"), k("a"), k("d")))
        self.assertFalse(is_redirect(k("a"), k("s"), k("d")))


class Keys(unittest.TestCase):
    def test_home_keys_have_no_travel(self):
        for col in (0, 1, 2, 3, 6, 7, 8, 9):
            self.assertEqual(Key(1, col).distance, 0)
        self.assertAlmostEqual(Key(0, 3).distance, (1 + 0.25 ** 2) ** 0.5)

    def test_all_layouts_load(self):
        self.assertGreaterEqual(len(load_layouts(ROOT / "layouts")), 5)


class Accents(unittest.TestCase):
    def test_dead_key(self):
        v1 = load_layout(V1)
        self.assertEqual([p.label for p in v1.presses("è")], ["DK", "e"])
        self.assertEqual([p.label for p in v1.presses("é")], ["Shift", "DK", "e"])

    def test_italian_keyboard(self):
        q = load_layout(QWERTY)
        self.assertEqual([p.label for p in q.presses("è")], ["è"])
        self.assertEqual([p.label for p in q.presses("é")], ["Shift", "è"])


class ReproduceStato(unittest.TestCase):
    """Numbers verified in STATO.md section 5 (letters only, accents folded)."""

    @classmethod
    def setUpClass(cls):
        corpus = load_corpus(ROOT / "data" / "it_top5000.csv").letters_only()
        cls.chars = corpus.characters
        cls.v1 = summarize(analyze(load_layout(V1), corpus))
        cls.qwerty = summarize(analyze(load_layout(QWERTY), corpus))

    def check(self, metrics, expected):
        for name, value in expected.items():
            self.assertAlmostEqual(100 * metrics[name], value, delta=0.051, msg=name)

    def test_letter_count(self):
        self.assertEqual(self.chars, 885_044_099)

    def test_v1(self):
        self.check(self.v1, {"top_row": 18.6, "home_row": 75.5, "bottom_row": 5.9, "left_hand": 50.6,
                             "roll_inward": 5.7, "roll_outward": 12.8})

    def test_qwerty(self):
        self.check(self.qwerty, {"top_row": 51.8, "home_row": 29.8, "bottom_row": 18.4, "left_hand": 55.0,
                                 "roll_inward": 17.5, "roll_outward": 21.5})


class WikipediaCorpus(unittest.TestCase):
    def test_every_character_is_typeable_on_v1(self):
        corpus = load_corpus(ROOT / "data" / "it_wikipedia_top20000.csv")
        self.assertEqual(len(corpus.words), 20_000)
        self.assertEqual(summarize(analyze(load_layout(V1), corpus))["unmapped_characters"], 0)


if __name__ == "__main__":
    unittest.main()
