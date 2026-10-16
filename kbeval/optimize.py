"""Search for a layout that minimises the weighted score on one or more corpora.

Usage:
    python -m kbeval.optimize --corpus data/it_top5000.csv --corpus data/it_wikipedia_top20000.csv \\
        --vowels-left --seeds 1 2 3 4 5 --out layouts/20-v2-base.json --id v2-base --name "Italian-Dvorak v2 base"

The search places 26 letters, the apostrophe, full stop, comma and hyphen on
the 30 main keys (3 rows x 10 columns). Accented vowels use a dead key on the
Quote key, as in v1. The score is the same one `python -m kbeval` reports,
averaged over the corpora with equal weight; `tests/` checks the two agree.

The optimiser is simulated annealing on key swaps, restarted from several
random seeds. The score is linear in symbol and bigram counts (apart from the
hand balance term), so it is precomputed per key and per key pair.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter
from pathlib import Path

from .corpus import Corpus, load_corpus
from .keyboard import Key
from .layouts import DEAD, Layout
from .metrics import bigram_kind
from .score import load_weights

ROOT = Path(__file__).resolve().parent.parent
SYMBOLS = list("abcdefghijklmnopqrstuvwxyz") + ["'", ".", ",", "-"]
VOWELS = set("aeiou")
SLOTS = [Key(r, c) for r in (0, 1, 2) for c in range(10)]
DEAD_KEY = Key(1, 10)
ROW_KEYS = ("top", "home", "bottom")


def _symbol_layout() -> Layout:
    """A layout whose only job is to expand characters into symbols."""
    keys = {s: SLOTS[i] for i, s in enumerate(SYMBOLS)}
    return Layout(id="symbols", name="symbols", description="", keys=keys,
                  accent_method="deadkey", dead_key=DEAD_KEY)


class CorpusCounts:
    """Symbol, symbol-bigram and word-end counts, independent of key placement."""

    def __init__(self, corpus: Corpus):
        expand = _symbol_layout()
        label = {k: s for s, k in expand.keys.items()}
        label[DEAD_KEY] = DEAD
        uni, bi, ends = Counter(), Counter(), Counter()
        extra = chars = 0
        for word, freq in corpus.words:
            chars += len(word) * freq
            seq = []
            for ch in word:
                presses = expand.presses(ch)
                if presses is None:
                    seq.append(None)
                    continue
                extra += (len(presses) - 1) * freq
                seq += [label[p.key] for p in presses if p.key is not None]
            for s in seq:
                if s is not None:
                    uni[s] += freq
            for a, b in zip(seq, seq[1:]):
                if a is not None and b is not None:
                    bi[(a, b)] += freq
            if seq and seq[-1] is not None:
                ends[seq[-1]] += freq
        self.uni, self.bi, self.ends = uni, bi, ends
        self.accent_extra = extra / chars


class Objective:
    """Weighted score of a placement, averaged over corpora."""

    def __init__(self, counts: list[CorpusCounts], weights: dict[str, float], space_thumb: str = "R"):
        self.w = weights
        self.space_thumb = space_thumb
        keys = SLOTS + [DEAD_KEY]
        self.keys = keys
        n = len(keys)
        idx = {s: i for i, s in enumerate(SYMBOLS)}
        idx[DEAD] = len(SYMBOLS)
        self.n_sym = len(SYMBOLS) + 1
        # Per-key unigram cost, left-hand flag, word-end flag.
        self.key_cost = [
            weights.get("mean_distance", 0) * k.distance
            + weights.get("pinky_load", 0) * (k.finger in ("LP", "RP"))
            + weights.get("top_row", 0) * (k.row == 0)
            + weights.get("bottom_row", 0) * (k.row == 2)
            for k in keys
        ]
        self.key_left = [k.hand == "L" for k in keys]
        self.key_end = [weights.get("word_end_space_hand", 0) * (k.hand == space_thumb) for k in keys]
        kind_w = {"same_finger": weights.get("same_finger_bigrams", 0),
                  "alternation": weights.get("hand_alternation", 0),
                  "inward": weights.get("roll_inward", 0),
                  "outward": 0.0, "repeat": 0.0}
        self.pair_cost = [[kind_w[bigram_kind(a, b)] for b in keys] for a in keys]
        self.constant = weights.get("accent_extra_keystrokes", 0) * sum(c.accent_extra for c in counts) / len(counts)
        # Normalised counts as index lists, averaged over corpora.
        uni = [0.0] * self.n_sym
        end = [0.0] * self.n_sym
        bi: dict[tuple[int, int], float] = {}
        for c in counts:
            tu, tb, te = sum(c.uni.values()), sum(c.bi.values()), sum(c.ends.values())
            for s, v in c.uni.items():
                uni[idx[s]] += v / tu / len(counts)
            for s, v in c.ends.items():
                end[idx[s]] += v / te / len(counts)
            for (a, b), v in c.bi.items():
                key = (idx[a], idx[b])
                bi[key] = bi.get(key, 0.0) + v / tb / len(counts)
        self.uni, self.end = uni, end
        self.bi = list((a, b, v) for (a, b), v in bi.items())
        self.per_corpus_uni = []
        for c in counts:
            tu = sum(c.uni.values())
            row = [0.0] * self.n_sym
            for s, v in c.uni.items():
                row[idx[s]] = v / tu
            self.per_corpus_uni.append(row)
        self.dead_index = idx[DEAD]
        self.dead_slot = len(SLOTS)

    def __call__(self, place: list[int]) -> float:
        """place[symbol index] = key index; the dead key is always last."""
        kc, pc = self.key_cost, self.pair_cost
        s = self.constant
        for i, k in enumerate(place):
            s += self.uni[i] * kc[k] + self.end[i] * self.key_end[k]
        for a, b, v in self.bi:
            s += v * pc[place[a]][place[b]]
        w_imb = self.w.get("hand_imbalance", 0)
        if w_imb:
            for row in self.per_corpus_uni:
                left = sum(row[i] for i, k in enumerate(place) if self.key_left[k])
                s += w_imb * abs(2 * left - 1) / len(self.per_corpus_uni)
        return s


def anneal(obj: Objective, seed: int, steps: int, vowels_left: bool,
           t_start: float = 0.05, t_end: float = 1e-5) -> tuple[float, list[int]]:
    rng = random.Random(seed)
    n = len(SYMBOLS)
    left_slots = [i for i, k in enumerate(SLOTS) if k.hand == "L"]
    vowel_ids = [i for i, s in enumerate(SYMBOLS) if s in VOWELS]

    def valid(p):
        return not vowels_left or all(p[v] in left_slots for v in vowel_ids)

    slots = list(range(n))
    while True:
        rng.shuffle(slots)
        place = slots[:] + [obj.dead_slot]
        if valid(place):
            break
    cur = obj(place)
    best, best_place = cur, place[:]
    ratio = (t_end / t_start) ** (1 / steps)
    t = t_start
    for _ in range(steps):
        a, b = rng.randrange(n), rng.randrange(n)
        if a == b:
            continue
        place[a], place[b] = place[b], place[a]
        if valid(place):
            new = obj(place)
            if new <= cur or rng.random() < math.exp((cur - new) / t):
                cur = new
                if cur < best:
                    best, best_place = cur, place[:]
                t *= ratio
                continue
        place[a], place[b] = place[b], place[a]
        t *= ratio
    return best, best_place


def placement(layout: Layout) -> list[int]:
    """Placement of an existing layout, for comparison with the full pipeline."""
    if layout.dead_key != DEAD_KEY:
        raise ValueError("layout must use the dead key on home:10")
    return [SLOTS.index(layout.keys[s]) for s in SYMBOLS] + [len(SLOTS)]


def to_json(place: list[int], layout_id: str, name: str, description: str) -> dict:
    rows = {r: ["_"] * 10 for r in ROW_KEYS}
    for i, s in enumerate(SYMBOLS):
        k = SLOTS[place[i]]
        rows[ROW_KEYS[k.row]][k.col] = s
    return {
        "id": layout_id, "name": name, "description": description, "source": "kbeval.optimize",
        "rows": {r: "".join(v) for r, v in rows.items()},
        "accents": {"method": "deadkey", "key": "home:10"},
    }


def main(argv=None):
    p = argparse.ArgumentParser(prog="kbeval.optimize", description="Optimise a layout on one or more corpora.")
    p.add_argument("--corpus", type=Path, action="append", required=True)
    p.add_argument("--weights", type=Path, default=ROOT / "config" / "weights.json")
    p.add_argument("--vowels-left", action="store_true", help="keep a e i o u on the left hand")
    p.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5])
    p.add_argument("--steps", type=int, default=200_000)
    p.add_argument("--out", type=Path, required=True, help="layout JSON to write")
    p.add_argument("--id", required=True)
    p.add_argument("--name", required=True)
    args = p.parse_args(argv)

    counts = [CorpusCounts(load_corpus(c)) for c in args.corpus]
    obj = Objective(counts, load_weights(args.weights))
    results = []
    for seed in args.seeds:
        score, place = anneal(obj, seed, args.steps, args.vowels_left)
        results.append((score, seed, place))
        print(f"seed {seed}: {score:.5f}")
    score, seed, place = min(results)
    corpora = ", ".join(c.name for c in args.corpus)
    description = (f"Optimised by kbeval.optimize on {corpora}"
                   f"{' with vowels on the left hand' if args.vowels_left else ''}"
                   f" (best of seeds {', '.join(map(str, args.seeds))}: seed {seed}, {args.steps:,} steps).")
    args.out.write_text(json.dumps(to_json(place, args.id, args.name, description), ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    print(f"best {score:.5f} (seed {seed}) -> {args.out}")


if __name__ == "__main__":
    main()
