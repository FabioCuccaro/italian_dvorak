"""Download an Italian word frequency list and write the top N words as CSV.

Usage:
    python scripts/fetch_corpus.py subtitles   # data/it_top5000.csv
    python scripts/fetch_corpus.py wikipedia   # data/it_wikipedia_top20000.csv
"""

import argparse
import csv
import re
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parent.parent / "data"

SOURCES = {
    # OpenSubtitles 2018, via hermitdave/FrequencyWords (CC BY-SA 4.0)
    "subtitles": {
        "url": "https://raw.githubusercontent.com/hermitdave/FrequencyWords/master/content/2018/it/it_50k.txt",
        "top": 5000,
        "out": DATA / "it_top5000.csv",
        "filter": False,
    },
    # Italian Wikipedia, 30 Aug 2022 dump, via IlyaSemenov/wikipedia-word-frequency (CC BY-SA 4.0)
    "wikipedia": {
        "url": "https://raw.githubusercontent.com/IlyaSemenov/wikipedia-word-frequency/master/results/itwiki-2022-08-30.txt",
        "top": 20000,
        "out": DATA / "it_wikipedia_top20000.csv",
        "filter": True,
    },
}

# Words written only with Italian letters, accented vowels and the apostrophe.
# Wikipedia also contains foreign names and other scripts, which are dropped.
ITALIAN_WORD = re.compile(r"^[a-zàèéìíòóù']+$")


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("source", choices=sorted(SOURCES))
    p.add_argument("--top", type=int, help="number of words to keep")
    p.add_argument("--out", type=Path, help="output CSV")
    args = p.parse_args()
    src = SOURCES[args.source]
    top = args.top or src["top"]
    out = args.out or src["out"]

    with urllib.request.urlopen(src["url"]) as resp:
        lines = resp.read().decode("utf-8").splitlines()
    rows = []
    for line in lines:
        word, freq = line.split()
        if src["filter"] and not ITALIAN_WORD.match(word):
            continue
        rows.append((word, freq))
        if len(rows) == top:
            break
    with open(out, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh, lineterminator="\n")
        writer.writerow(["word", "frequency"])
        writer.writerows(rows)
    print(f"Wrote {len(rows)} words to {out}")


if __name__ == "__main__":
    main()
