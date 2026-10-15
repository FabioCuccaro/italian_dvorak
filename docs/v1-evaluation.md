# Evaluation of the Italian-Dvorak v1 prototype

[Italiano](v1-evaluation.it.md)

This answers the questions in the project's evaluation brief (sections A–H). Every number comes from
[`results/`](../results/layout_comparison_report.md) and can be regenerated with `python -m kbeval`.
Numbers labelled *claim* come from the original prototype and have **not** been validated.

Corpus: the 5,000 most frequent Italian words from OpenSubtitles 2018 ([FrequencyWords](../data/README.md)),
weighted by frequency. Accented vowels and apostrophes are kept, so the figures differ slightly from the
letters-only figures in the project notes (those are reproduced by the test suite with `--letters-only`).

## A. Verdict

**Layout to test, not final.** v1 is a solid Dvorak-style layout (75% of keystrokes on the home row,
balanced hands, 75% hand alternation), but it was optimised with a reversed roll bonus and it is
beaten by an earlier candidate (ItaDvorak v0.2-seed) under the spec's cost function. Keep it as
`v1-candidate`.

## B. Strengths

- **Home row:** 75.2% of keystrokes (QWERTY-IT: 29.8%). Mean finger travel 0.44 key widths per
  keystroke, the lowest of the non-variant layouts (QWERTY-IT: 0.80).
- **Hand balance:** 50.5% left / 49.5% right.
- **Alternation:** 75.0% of in-word bigrams switch hands, as high as Dvorak US (74.5%).
- **Space:** 84% of Italian words end in a vowel; with vowels on the left, 87% of word endings are typed
  by the left hand, so a right-thumb space alternates naturally.
- **Same-finger bigrams:** 2.34%, far below QWERTY-IT (7.02%).

## C. Weaknesses

- **Outward rolls.** Because of the reversed sign in the optimiser, v1 has more outward rolls (12.9% of
  bigrams) than inward ones (5.6%). Every other Italian candidate has the opposite ratio; v0.2-seed has
  13.6% inward and 4.5% outward.
- **E and I share the left index finger.** `ie` and `ei` are v1's two most frequent same-finger
  bigrams (0.49% and 0.40%), followed by `zi` (0.32%, Z is also on the left index).
- **L (question A).** L is more frequent than D (5.14% vs 3.40% of characters), but moving L to the
  home row (variant A) puts D above N on the right index and creates the `nd` same-finger bigram (0.66%).
  Variant A gains home row (77.0%) but loses on same-finger bigrams (2.94%) and pinky load (12.3%), and
  scores worse than v1. L is not a free win; it needs a rearrangement, not a swap.
- **QU (question B).** `qu` is 1.06% of bigrams. In v1 it is a same-hand outward roll (left middle to
  left pinky). Moving Q to the right (variant B) makes it alternate but barely changes the score
  (0.3163 vs 0.3146): QU is not a real problem.
- **CH (question C).** `ch` is 1.50% of bigrams and `che` is the most frequent trigram (1.58%). In v1 it
  is an outward roll on the right top row (middle to ring), which is comfortable. Moving H to the left
  (variant C) creates `hi` as a same-finger bigram and scores clearly worse (0.3678). Keep C and H together.
- **Accents.** Accented vowels cost 0.73 extra keystrokes per 100 characters with a dead key or AltGr,
  versus 0.06 on the Italian keyboard (only é needs Shift). `è` alone is the 10th most frequent word.
- **Corpus.** Subtitles over-represent dialogue; see E.

## D. The "39% effort reduction" claim

Not a result. It used the same model for optimising and for measuring, on the same data, with the
reversed roll bonus. The original script is lost and its total cost could not be reproduced from the
description (the letter and bigram statistics, however, are reproduced exactly by `tests/`). Under the
spec's cost function used here, v1 scores 0.315 against 1.679 for QWERTY-IT, but that ratio depends on
the weights and should not be quoted as an effort reduction either.

## E. Validation plan

1. Rerun this pipeline on a second, written Italian corpus (next step of the project plan) and check
   whether the ranking holds.
2. Compare with an established analyzer (e.g. Oxeylyzer, genkey) on the same corpus.
3. Add text with spaces and punctuation, so bigrams across words and the apostrophe are modelled.

## F. Variants tested

| Layout | Change | Score | Mean rank under random weights |
|---|---|---|---|
| v0.2-seed | earlier candidate | **0.2489** | 1.00 (first in 99.7% of samples) |
| v1-d | v1 with AltGr accents | 0.3094 | 2.16 |
| v1 | prototype | 0.3146 | 3.31 |
| v1-b | Q ↔ B | 0.3163 | 3.96 |
| v1-a | L ↔ D | 0.3268 | 4.71 |
| v1-c | H ↔ Z | 0.3678 | 7.03 |
| v1-abc | all three | 0.3804 | 7.89 |

Lower is better. Variant D only differs in how accents are typed: the extra press moves from the right
pinky (Quote key) to the thumb, which lowers pinky load from 10.5% to 9.9%. A dead key works on any
keyboard and handles capitals naturally; AltGr needs a right Alt key that acts as AltGr.

## G. Recommendation

Keep v1 as **v1-candidate**. Do not adopt it, and do not go back to v0.1 (more same-finger bigrams,
4.55%). Generate a new layout with the corrected roll direction (step 3 of the plan), using v0.2-seed
and v1 as starting points and the second corpus as a check.

On the weights (spec section 5): the top and bottom row penalties largely double-count the distance
term; the space penalty is a weak proxy because a word list has no real spaces; and a number-row
penalty was added (weight 1.0) so QWERTY-IT's apostrophe and ì are not free. These are worth revisiting
before step 3, but the sensitivity analysis shows the ranking at the top is stable when every weight
moves by ±50%.

## H. Next step

Run the same evaluation on a second, written corpus (step 2 of the plan).
