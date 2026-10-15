"""Weighted score and weight sensitivity analysis."""

from __future__ import annotations

import json
import random
from pathlib import Path

# Starting weights from the project spec (lower score is better). Negative
# weights are rewards. Every metric is a share in [0, 1], except
# mean_distance (key widths per keystroke) and accent_extra_keystrokes
# (extra keystrokes per character).
DEFAULT_WEIGHTS = {
    "mean_distance": 1.0,
    "same_finger_bigrams": 2.5,
    "pinky_load": 1.5,
    "hand_imbalance": 1.0,
    "bottom_row": 0.75,
    "top_row": 0.5,
    "number_row": 1.0,
    "accent_extra_keystrokes": 0.5,
    "word_end_space_hand": 0.75,
    "hand_alternation": -0.75,
    "roll_inward": -0.5,
}


def load_weights(path: Path | None) -> dict[str, float]:
    if path is None:
        return dict(DEFAULT_WEIGHTS)
    weights = json.loads(Path(path).read_text(encoding="utf-8"))
    unknown = set(weights) - set(DEFAULT_WEIGHTS)
    if unknown:
        raise ValueError(f"unknown weights: {', '.join(sorted(unknown))}")
    return weights


def score(metrics: dict[str, float], weights: dict[str, float]) -> float:
    return sum(w * metrics[name] for name, w in weights.items())


def ranks(scores: dict[str, float]) -> dict[str, int]:
    ordered = sorted(scores, key=scores.get)
    return {name: i + 1 for i, name in enumerate(ordered)}


def sensitivity(all_metrics: dict[str, dict[str, float]], weights: dict[str, float],
                samples: int = 2000, spread: float = 0.5, seed: int = 1) -> list[dict]:
    """Rank stability when every weight is scaled by a random factor.

    Each sample multiplies every weight independently by a factor drawn
    uniformly from [1 - spread, 1 + spread]. Signs never change.
    """
    rng = random.Random(seed)
    names = list(all_metrics)
    rank_sum = {n: 0 for n in names}
    firsts = {n: 0 for n in names}
    best = {n: len(names) for n in names}
    worst = {n: 1 for n in names}
    for _ in range(samples):
        w = {k: v * rng.uniform(1 - spread, 1 + spread) for k, v in weights.items()}
        r = ranks({n: score(m, w) for n, m in all_metrics.items()})
        for n, pos in r.items():
            rank_sum[n] += pos
            firsts[n] += pos == 1
            best[n] = min(best[n], pos)
            worst[n] = max(worst[n], pos)
    return [
        {"layout": n, "mean_rank": rank_sum[n] / samples, "first_share": firsts[n] / samples,
         "best_rank": best[n], "worst_rank": worst[n]}
        for n in sorted(names, key=lambda n: rank_sum[n])
    ]
