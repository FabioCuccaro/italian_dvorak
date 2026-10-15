"""Load a word frequency list and count character n-grams."""

from __future__ import annotations

import csv
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Corpus:
    words: list[tuple[str, int]]  # (lowercase NFC word, frequency)
    source: str

    @property
    def tokens(self) -> int:
        return sum(f for _, f in self.words)

    @property
    def characters(self) -> int:
        return sum(len(w) * f for w, f in self.words)

    def letters_only(self) -> "Corpus":
        """Accents folded to the base vowel, everything but a-z removed.

        This is the preprocessing used to optimise the v1 prototype; it is
        kept so the numbers in STATO.md can be reproduced.
        """
        merged: Counter = Counter()
        for word, freq in self.words:
            base = unicodedata.normalize("NFD", word)
            letters = "".join(ch for ch in base if "a" <= ch <= "z")
            if letters:
                merged[letters] += freq
        words = sorted(merged.items(), key=lambda item: (-item[1], item[0]))
        return Corpus(words=words, source=self.source + " (letters only)")

    def ngrams(self, n: int) -> Counter:
        """Character n-grams inside words, weighted by word frequency."""
        out: Counter = Counter()
        for word, freq in self.words:
            for i in range(len(word) - n + 1):
                out[word[i:i + n]] += freq
        return out


def load_corpus(path: Path) -> Corpus:
    """Read a CSV with "word,frequency" columns.

    Words are lowercased and NFC-normalised. Duplicate words after lowercasing
    are merged. Text between words is not available in a word list, so
    n-grams never cross word boundaries.
    """
    merged: Counter = Counter()
    with open(path, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            word = unicodedata.normalize("NFC", row["word"].strip().lower())
            if word:
                merged[word] += int(row["frequency"])
    words = sorted(merged.items(), key=lambda item: (-item[1], item[0]))
    return Corpus(words=words, source=str(path))
