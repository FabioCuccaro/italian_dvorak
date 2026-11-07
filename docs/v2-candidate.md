# Italian-Dvorak v2

[Italiano](v2-candidate.it.md)

v2 is the first layout produced by this repository's own optimiser, with the corrected roll direction
and scored on both corpora at once, plus a dedicated key for è. Punctuation beyond the main block and
real typing tests are still open.

```
K F ' Q È   B D S M J   X
U E I A O   C T L N R   ◌
W Z Y . ,   P G V H -
```

- **è** has its own key; **Shift + è = é**, as on the Italian keyboard (*perché*, *né*).
- **à ì ò ù** and accented capitals use the dead key ◌ (Quote key): dead key then vowel for the grave
  accent, Shift + dead key then vowel for the acute accent.
- **X** moves to the key right of the top row (BracketLeft on a QWERTY board); it is 0.01% of letters.

## How it was made

The optimiser first produced `v2-base` ([`20-v2-base.json`](../layouts/20-v2-base.json)), with the
same letters and the dead key for every accent:

```sh
python -m kbeval.optimize --corpus data/it_top5000.csv --corpus data/it_wikipedia_top20000.csv \
    --vowels-left --seeds 1 2 3 4 5 6 7 8 --steps 300000 \
    --out layouts/20-v2-base.json --id v2-base --name "Italian-Dvorak v2 base (optimiser output)"
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
- **Dedicated è** (chosen on 2026-10-16 among dead key, AltGr, dedicated è, or all accents on their own
  keys). è alone is 45% of accented vowels. Every main key was tried for è, moving the letter it
  replaced to the extra key; the left index top row (X's place) scored best. Putting è on the right
  pinky next to the dead key scored clearly worse (0.222). The result is `v2`
  ([`21-v2.json`](../layouts/21-v2.json)).

## Results

| | v2-base | v0.2-seed | v1 | Italian QWERTY |
|---|---|---|---|---|
| Score, subtitles | **0.207** | 0.249 | 0.315 | 1.679 |
| Score, Wikipedia | **0.206** | 0.307 | 0.371 | 1.624 |
| Home row (subtitles / Wikipedia) | 75.9 / 77.8% | 74.3 / 74.7% | 75.2 / 75.7% | 29.8 / 31.4% |
| Same-finger bigrams | **0.39 / 0.66%** | 1.68 / 1.97% | 2.34 / 3.06% | 7.02 / 7.79% |
| Inward / outward rolls (subtitles) | 13.0 / 7.8% | 13.6 / 4.5% | 5.6 / 12.9% | 17.3 / 22.0% |
| Hand alternation (subtitles) | 74.7% | 76.0% | 75.0% | 49.5% |
| Pinkies (subtitles) | 10.1% | 8.3% | 10.5% | 16.3% |

With the dedicated è, v2 keeps the same letters and changes only how accents are typed:

| | v2-base (dead key only) | v2 (dedicated è) |
|---|---|---|
| Score (subtitles / Wikipedia) | 0.207 / 0.206 | 0.209 / **0.204** |
| Extra keystrokes for accents, per 100 characters | 0.73 / 0.77 | **0.37 / 0.47** |
| Pinkies | 10.1 / 10.2% | **9.8 / 10.0%** |
| Home row | 75.9 / 77.8% | 75.4 / 77.4% |

v2 and v2-base take the first two places in nearly every weight sensitivity sample (v0.2-seed is first
in only 1.5% of the samples on subtitles and never on Wikipedia). Full tables:
[results/corpus_comparison.md](../results/corpus_comparison.md).

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
- **Shortcuts:** Z, X, C, V are no longer under the left hand's bottom row (C is on the right home row,
  X off the main block).
- **Not modelled:** capitals, digits, punctuation other than apostrophe, full stop, comma and hyphen,
  and bigrams across a space.
- **Punctuation and symbols** outside the main block (digits row, brackets, ; : ? !) still follow the
  Italian keyboard and will be set when the layout is packaged.
