"""Command line entry point: python -m kbeval --help"""

from __future__ import annotations

import argparse
from pathlib import Path

from .corpus import load_corpus
from .layouts import load_layouts
from .metrics import analyze, summarize, worst_same_finger_bigrams
from .report import write_outputs
from .score import load_weights, score, sensitivity

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str] | None = None):
    p = argparse.ArgumentParser(prog="kbeval", description="Score keyboard layouts on a word frequency corpus.")
    p.add_argument("--corpus", type=Path, default=ROOT / "data" / "it_top5000.csv",
                   help="CSV with word,frequency columns")
    p.add_argument("--layouts", type=Path, default=ROOT / "layouts", help="directory of layout JSON files")
    p.add_argument("--weights", type=Path, default=ROOT / "config" / "weights.json", help="score weights JSON")
    p.add_argument("--out", type=Path, default=ROOT / "results", help="output directory")
    p.add_argument("--letters-only", action="store_true",
                   help="fold accents and drop non-letters, as in the original v1 optimisation")
    p.add_argument("--focus", default="v1", help="layout id detailed in the report")
    p.add_argument("--samples", type=int, default=2000, help="weight sensitivity samples")
    p.add_argument("--spread", type=float, default=0.5, help="weight sensitivity: max relative change")
    p.add_argument("--seed", type=int, default=1, help="random seed for the sensitivity analysis")
    args = p.parse_args(argv)

    corpus = load_corpus(args.corpus)
    if args.letters_only:
        corpus = corpus.letters_only()
    layouts = load_layouts(args.layouts)
    weights = load_weights(args.weights)

    analyses = {lay.id: analyze(lay, corpus) for lay in layouts}
    metrics = {lid: summarize(a) for lid, a in analyses.items()}
    scores = {lid: score(m, weights) for lid, m in metrics.items()}

    ngrams = {}
    for n in (1, 2, 3):
        counts = corpus.ngrams(n)
        total = sum(counts.values())
        ngrams[n] = [(g, c, c / total) for g, c in counts.most_common(50)]

    try:
        corpus_path = args.corpus.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        corpus_path = args.corpus.name

    ctx = {
        "corpus": corpus,
        "corpus_path": corpus_path,
        "letters_only": args.letters_only,
        "layouts": layouts,
        "weights": weights,
        "metrics": metrics,
        "scores": scores,
        "worst_sfb": {lid: worst_same_finger_bigrams(a) for lid, a in analyses.items()},
        "ngrams": ngrams,
        "sensitivity": sensitivity(metrics, weights, args.samples, args.spread, args.seed),
        "sensitivity_params": {"samples": args.samples, "spread": args.spread},
        "focus": args.focus,
    }
    write_outputs(args.out, ctx)

    for lay in sorted(layouts, key=lambda lay: scores[lay.id]):
        print(f"{scores[lay.id]:8.4f}  {lay.id}")
    print(f"Results written to {args.out}")


if __name__ == "__main__":
    main()
