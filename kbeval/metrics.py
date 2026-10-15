"""Turn a corpus into keystrokes on a layout and measure them."""

from __future__ import annotations

import math
from collections import Counter
from dataclasses import dataclass, field

from .corpus import Corpus
from .keyboard import FINGER_RANK, FINGERS, Key, roll_direction
from .layouts import Layout


@dataclass
class Analysis:
    layout: Layout
    characters: int = 0
    unmapped: Counter = field(default_factory=Counter)
    extra_keystrokes: int = 0  # keystrokes beyond one per character (dead key, Shift, AltGr)
    modifiers: Counter = field(default_factory=Counter)
    presses: Counter = field(default_factory=Counter)  # Key -> count
    bigrams: Counter = field(default_factory=Counter)  # (Key, Key) -> count
    trigrams: Counter = field(default_factory=Counter)  # (Key, Key, Key) -> count
    word_ends: Counter = field(default_factory=Counter)  # Key -> count
    words: int = 0


def analyze(layout: Layout, corpus: Corpus) -> Analysis:
    """Type every word of the corpus on the layout.

    Each word is followed by a space, typed with a thumb. Modifier presses
    (Shift, AltGr) are counted as extra keystrokes but kept out of the key
    sequence, so a dead key sits directly between its neighbours while
    Shift + è does not. An unmapped character breaks the key sequence.
    """
    a = Analysis(layout)
    for word, freq in corpus.words:
        a.words += freq
        a.characters += len(word) * freq
        seq: list[Key | None] = []
        for ch in word:
            presses = layout.presses(ch)
            if presses is None:
                a.unmapped[ch] += freq
                seq.append(None)
                continue
            a.extra_keystrokes += (len(presses) - 1) * freq
            for p in presses:
                if p.key is None:
                    a.modifiers[p.label] += freq
                else:
                    seq.append(p.key)
        for k in seq:
            if k is not None:
                a.presses[k] += freq
        for x, y in zip(seq, seq[1:]):
            if x is not None and y is not None:
                a.bigrams[(x, y)] += freq
        for x, y, z in zip(seq, seq[1:], seq[2:]):
            if x is not None and y is not None and z is not None:
                a.trigrams[(x, y, z)] += freq
        if seq and seq[-1] is not None:
            a.word_ends[seq[-1]] += freq
    return a


def _share(part: float, whole: float) -> float:
    return part / whole if whole else 0.0


def key_distance(a: Key, b: Key) -> float:
    return math.hypot(a.x - b.x, a.row - b.row)


def bigram_kind(a: Key, b: Key) -> str:
    if a == b:
        return "repeat"
    if a.finger == b.finger:
        return "same_finger"
    if a.hand != b.hand:
        return "alternation"
    return roll_direction(a, b)  # "inward" or "outward"


def is_redirect(a: Key, b: Key, c: Key) -> bool:
    """One-hand trigram that changes direction, e.g. "sad" on QWERTY."""
    if not (a.hand == b.hand == c.hand):
        return False
    if a.finger == b.finger or b.finger == c.finger:
        return False
    first = FINGER_RANK[b.finger] - FINGER_RANK[a.finger]
    second = FINGER_RANK[c.finger] - FINGER_RANK[b.finger]
    return first * second < 0


def summarize(a: Analysis, space_thumb: str = "R") -> dict[str, float]:
    """Headline metrics, all as shares in [0, 1] except where noted."""
    total = sum(a.presses.values())
    by_row = Counter()
    by_hand = Counter()
    by_finger = Counter()
    distance = 0.0
    for k, n in a.presses.items():
        by_row[k.row_name] += n
        by_hand[k.hand] += n
        by_finger[k.finger] += n
        distance += k.distance * n

    bi_total = sum(a.bigrams.values())
    kinds = Counter()
    for (x, y), n in a.bigrams.items():
        kinds[bigram_kind(x, y)] += n

    tri_total = sum(a.trigrams.values())
    one_hand = redirect = 0
    for (x, y, z), n in a.trigrams.items():
        if x.hand == y.hand == z.hand:
            one_hand += n
            if is_redirect(x, y, z):
                redirect += n

    ends = sum(a.word_ends.values())
    ends_same_side = sum(n for k, n in a.word_ends.items() if k.hand == space_thumb)

    left, right = _share(by_hand["L"], total), _share(by_hand["R"], total)
    return {
        "home_row": _share(by_row["home"], total),
        "top_row": _share(by_row["top"], total),
        "bottom_row": _share(by_row["bottom"], total),
        "number_row": _share(by_row["number"], total),
        "mean_distance": _share(distance, total),  # key widths per keystroke
        "left_hand": left,
        "right_hand": right,
        "hand_imbalance": abs(left - right),
        "pinky_load": _share(by_finger["LP"] + by_finger["RP"], total),
        **{f"finger_{f}": _share(by_finger[f], total) for f in FINGERS},
        "same_finger_bigrams": _share(kinds["same_finger"], bi_total),
        "same_key_repeats": _share(kinds["repeat"], bi_total),
        "same_hand_bigrams": _share(kinds["same_finger"] + kinds["inward"] + kinds["outward"], bi_total),
        "hand_alternation": _share(kinds["alternation"], bi_total),
        "roll_inward": _share(kinds["inward"], bi_total),
        "roll_outward": _share(kinds["outward"], bi_total),
        "one_hand_trigrams": _share(one_hand, tri_total),
        "redirects": _share(redirect, tri_total),
        "word_end_space_hand": _share(ends_same_side, ends),
        "accent_extra_keystrokes": _share(a.extra_keystrokes, a.characters),  # per character
        "unmapped_characters": _share(sum(a.unmapped.values()), a.characters),
    }


def worst_same_finger_bigrams(a: Analysis, limit: int = 15) -> list[dict]:
    """Same-finger bigrams ranked by share x (1 + distance between the keys)."""
    labels = a.layout.labels
    bi_total = sum(a.bigrams.values())
    rows = []
    for (x, y), n in a.bigrams.items():
        if bigram_kind(x, y) != "same_finger":
            continue
        share = n / bi_total
        dist = key_distance(x, y)
        rows.append({
            "bigram": labels.get(x, "?") + labels.get(y, "?"),
            "finger": x.finger,
            "share": share,
            "key_distance": dist,
            "discomfort": share * (1 + dist),
        })
    rows.sort(key=lambda r: -r["discomfort"])
    return rows[:limit]
