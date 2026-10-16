# Italian Dvorak

[Italiano](README.it.md)

A Dvorak-style keyboard layout designed for Italian, and an open, reproducible method to design and
evaluate it.

> **Status: candidate.** The current candidate (v2) is not final: accents and punctuation are still
> open and it has not been tested by real typists. See [v2](docs/v2-candidate.md) and the
> [evaluation of the earlier v1](docs/v1-evaluation.md).

## The layout (v2 candidate)

```
K F ' Q X   B D S M J
U E I A O   C T L N R   ◌
W Z Y . ,   P G V H -
```

Vowels sit on the left home row, frequent consonants on the right. Accented vowels (à è é ì ò ù) are
typed with a dead key (◌) on the key right of the home row: dead key then vowel for the grave accent,
Shift + dead key then vowel for the acute accent.

| | v2 | v1 | Italian QWERTY |
|---|---|---|---|
| Keystrokes on the home row | 75.9% | 75.2% | 29.8% |
| Same-finger bigrams | 0.39% | 2.34% | 7.02% |
| Hand alternation | 74.7% | 75.0% | 49.5% |
| Left / right hand | 50.2 / 49.8 | 50.5 / 49.5 | 54.2 / 45.8 |

Measured on the 5,000 most frequent Italian words (subtitles corpus). Full comparison with other
layouts: [results/layout_comparison_report.md](results/layout_comparison_report.md). The same
evaluation on written Italian (Wikipedia) is in [results/wikipedia/](results/wikipedia/layout_comparison_report.md),
and [results/corpus_comparison.md](results/corpus_comparison.md) puts the two side by side.

### Try it

Layout files for a self-hosted [keybr](https://www.keybr.com) are in [`keybr/`](keybr/README.md).
They still contain v1. Installable versions for operating systems will come once the layout is final.

## Evaluate a layout

The evaluation pipeline needs only Python 3.10+ and no extra packages.

```sh
python -m kbeval                  # score every layout in layouts/ on the subtitles corpus, write results/
python -m unittest discover tests # run the tests
python -m kbeval --help           # all options
```

To regenerate everything in `results/`, including the Wikipedia run and the comparison:

```sh
python -m kbeval
python -m kbeval --corpus data/it_wikipedia_top20000.csv --out results/wikipedia
python -m kbeval.compare subtitles=results wikipedia=results/wikipedia --out results
```

To evaluate your own layout, add a JSON file to [`layouts/`](layouts/) (copy
[`20-v2.json`](layouts/20-v2.json) and edit the rows) and rerun. To search for a new layout, use
`python -m kbeval.optimize` (see [how v2 was made](docs/v2-candidate.md#how-it-was-made)). To use another corpus, pass any CSV
with `word,frequency` columns via `--corpus`. Score weights are in
[`config/weights.json`](config/weights.json).

Outputs in `results/`:

| File | Content |
|---|---|
| `layout_comparison_report.md` (and `.it.md`) | readable report with all tables |
| `scores.csv` | every metric and the weighted score, one row per layout |
| `finger_load.csv` | share of keystrokes per finger |
| `worst_same_finger_bigrams.csv` | the most uncomfortable same-finger bigrams per layout |
| `top_ngrams.csv` | most frequent characters, bigrams and trigrams in the corpus |
| `sensitivity.csv` | how stable the ranking is when the weights change |
| `wikipedia/` | the same files for the Wikipedia corpus |
| `corpus_comparison.md` (and `.it.md`) | rankings and key metrics on both corpora side by side |

### What is measured

Each word is typed on the layout, followed by a space. The pipeline counts keystrokes per row, hand
and finger, finger travel from the home position, same-finger bigrams, hand alternation, inward and
outward rolls (inward = towards the index finger), one-hand trigrams and redirects, and the extra
keystrokes needed for accented vowels (dead key, AltGr or Shift). The [report](results/layout_comparison_report.md)
lists the limits of the model.

## Repository layout

| Path | Content |
|---|---|
| `kbeval/` | evaluation pipeline and optimiser (Python, standard library only) |
| `layouts/` | layouts being compared, one JSON file each |
| `config/` | score weights |
| `data/` | corpora (subtitles, Wikipedia), with their own [license](data/README.md) |
| `docs/` | analysis and design notes |
| `results/` | generated outputs |
| `keybr/` | layout files for keybr |
| `scripts/` | helper scripts (corpus download) |

## Roadmap

1. Reproducible evaluation pipeline and v1 assessment. Done.
2. Second corpus of written Italian (Wikipedia), to check the results beyond subtitles. Done.
3. New optimised layout with the corrected model: [v2 candidate](docs/v2-candidate.md).
4. Installable layouts (Linux XKB first) and keybr integration.

## License

Code and documentation: [MIT](LICENSE). The corpora in `data/` are CC BY-SA 4.0, see
[data/README.md](data/README.md).
