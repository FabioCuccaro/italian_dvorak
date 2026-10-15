"""Download the FrequencyWords Italian list and write the top N words as CSV.

Usage: python scripts/fetch_corpus.py [--top 5000] [--out data/it_top5000.csv]
"""

import argparse
import csv
import urllib.request
from pathlib import Path

URL = "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/it/it_50k.txt"


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--top", type=int, default=5000, help="number of words to keep")
    p.add_argument("--out", type=Path, default=Path(__file__).resolve().parent.parent / "data" / "it_top5000.csv")
    p.add_argument("--url", default=URL)
    args = p.parse_args()

    with urllib.request.urlopen(args.url) as resp:
        lines = resp.read().decode("utf-8").splitlines()
    rows = [line.split() for line in lines[:args.top]]
    with open(args.out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["word", "frequency"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} words to {args.out}")


if __name__ == "__main__":
    main()
