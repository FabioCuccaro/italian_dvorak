# Italian-Dvorak v2 (candidate)

[Italiano](v2-candidate.it.md)

v2 is the first layout produced by this repository's own optimiser, with the corrected roll direction
and scored on both corpora at once. It is a **candidate**: accents, punctuation and real typing tests
are still open.

```
K F ' Q X   B D S M J
U E I A O   C T L N R   ◌
W Z Y . ,   P G V H -
```

◌ is the accent dead key (Quote key), as in v1: dead key then vowel for the grave accent, Shift + dead
key then vowel for the acute accent.

## How it was made

```sh
python -m kbeval.optimize --corpus data/it_top5000.csv --corpus data/it_wikipedia_top20000.csv \
    --vowels-left --seeds 1 2 3 4 5 6 7 8 --steps 300000 \
    --out layouts/20-v2.json --id v2 --name "Italian-Dvorak v2 (candidate)"
```

- **Objective:** the same weighted score as `python -m kbeval` ([`config/weights.json`](../config/weights.json)),
  averaged over the subtitles and Wikipedia corpora. A test checks that the optimiser and the pipeline
  give the same number for the same layout.
- **Search:** simulated annealing on key swaps over the 30 main keys (26 letters, apostrophe, full stop,
  comma, hyphen), restarted from 8 seeds. Runs with 2 million steps and 24 other seeds found no better
  layout; 9 of them reached the same best score.
- **Vowels on the left:** the search was run with and without this constraint. Both found the same
  layout: the vowels end up on the left home row without being forced there.
- P and G (bottom row, right index) can be swapped at no cost; every metric is identical.

## Results

| | v2 | v0.2-seed | v1 | Italian QWERTY |
|---|---|---|---|---|
| Score, subtitles | **0.207** | 0.249 | 0.315 | 1.679 |
| Score, Wikipedia | **0.206** | 0.307 | 0.371 | 1.624 |
| Home row (subtitles / Wikipedia) | 75.9 / 77.8% | 74.3 / 74.7% | 75.2 / 75.7% | 29.8 / 31.4% |
| Same-finger bigrams | **0.39 / 0.66%** | 1.68 / 1.97% | 2.34 / 3.06% | 7.02 / 7.79% |
| Inward / outward rolls (subtitles) | 13.0 / 7.8% | 13.6 / 4.5% | 5.6 / 12.9% | 17.3 / 22.0% |
| Hand alternation (subtitles) | 74.7% | 76.0% | 75.0% | 49.5% |
| Pinkies (subtitles) | 10.1% | 8.3% | 10.5% | 16.3% |

v2 ranks first in 98.2% (subtitles) and 100% (Wikipedia) of the weight sensitivity samples. Full
tables: [results/corpus_comparison.md](../results/corpus_comparison.md).

## How much of this is real

The project notes warned that optimising and measuring with the same model on the same data is
circular. v2 is optimised on both corpora, so its score above is in-sample. Two checks:

- **Cross-corpus test.** A layout optimised on subtitles only scores 0.272 on Wikipedia, which it never
  saw: still better than v0.2-seed (0.307) and v1 (0.371). A layout optimised on Wikipedia only scores
  0.267 on subtitles, worse than v0.2-seed (0.249). Part of any optimised layout's advantage is
  fitting its own corpus; optimising on both corpora is the hedge.
- **Metrics outside the score.** Redirects (one-hand trigrams that change direction) are not in the
  score and get worse: 3.7% of trigrams on subtitles, against 2.9% for v1 and 1.6% for v0.2-seed. The
  bottom row is also used more (8.6% vs 6.4% for v1).

## Open points

- **S on the top row.** S is frequent (5.6% / 4.8%) but sits on the top row (right middle finger). The
  score prefers it there because it avoids same-finger bigrams; a typing test will tell whether it is
  comfortable.
- **Apostrophe on the left top row** (middle finger), next to F and Q. In elisions such as *l'anno* or
  *dell'epoca* it is usually followed by a vowel on the same hand.
- **Shortcuts:** Z, X, C, V are no longer under the left hand's bottom row (C is on the right home row).
- **Not modelled:** capitals, digits, punctuation other than apostrophe, full stop, comma and hyphen,
  and bigrams across a space.
- **Accents and punctuation** are still to be decided (dead key, AltGr, or a dedicated è), before
  packaging the layout for daily use.
