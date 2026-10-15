# Confronto tra corpus

[English](corpus_comparison.md)

_Generato da `python -m kbeval.compare`. Non modificarlo a mano._

## Classifica

Punteggio (più basso = migliore), posizione, e posizione media quando ogni peso è moltiplicato per un fattore casuale tra 0,5x e 1,5x.

| Layout | subtitles punteggio | subtitles pos. | subtitles pos. media | wikipedia punteggio | wikipedia pos. | wikipedia pos. media |
|---|---|---|---|---|---|---|
| itadvorak-v0.2-seed | 0.2489 | 1 | 1.00 | 0.3070 | 1 | 1.21 |
| v1-d | 0.3094 | 2 | 2.16 | 0.3503 | 2 | 2.46 |
| v1 | 0.3146 | 3 | 3.31 | 0.3706 | 6 | 6.37 |
| v1-b | 0.3163 | 4 | 3.96 | 0.3588 | 4 | 4.18 |
| v1-a | 0.3268 | 5 | 4.71 | 0.3788 | 7 | 6.74 |
| itadvorak-v0.1 | 0.3484 | 6 | 5.92 | 0.3853 | 8 | 7.23 |
| v1-c | 0.3678 | 7 | 7.03 | 0.3605 | 5 | 4.46 |
| v1-abc | 0.3804 | 8 | 7.89 | 0.3534 | 3 | 3.35 |
| dvorak-us | 0.5239 | 9 | 9.10 | 0.5946 | 9 | 9.03 |
| itadvorak-v0.1b | 0.6305 | 10 | 9.90 | 0.7907 | 10 | 9.97 |
| qwerty-it | 1.6790 | 11 | 11.00 | 1.6240 | 11 | 11.00 |

## Metriche principali

Percentuali delle battute, o dei bigrammi di tasti dentro le parole per SFB e roll.

| Layout | home row (subtitles) | home row (wikipedia) | SFB (subtitles) | SFB (wikipedia) | roll verso l'interno (subtitles) | roll verso l'interno (wikipedia) | roll verso l'esterno (subtitles) | roll verso l'esterno (wikipedia) | mignoli (subtitles) | mignoli (wikipedia) | mano sinistra (subtitles) | mano sinistra (wikipedia) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| itadvorak-v0.2-seed | 74.3 | 74.7 | 1.7 | 2.0 | 13.6 | 12.2 | 4.5 | 4.7 | 8.3 | 7.5 | 50.3 | 48.3 |
| v1-d | 75.1 | 75.5 | 2.4 | 3.1 | 5.6 | 5.2 | 12.8 | 12.2 | 9.9 | 10.4 | 50.8 | 49.9 |
| v1 | 75.2 | 75.7 | 2.3 | 3.1 | 5.6 | 5.1 | 12.9 | 12.4 | 10.5 | 11.0 | 50.5 | 49.6 |
| v1-b | 75.2 | 75.7 | 2.5 | 3.2 | 6.3 | 5.4 | 12.2 | 12.2 | 10.3 | 10.5 | 50.8 | 50.1 |
| v1-a | 77.0 | 78.5 | 2.9 | 3.5 | 6.0 | 5.5 | 11.9 | 11.6 | 12.3 | 13.8 | 50.5 | 49.6 |
| itadvorak-v0.1 | 77.0 | 78.5 | 4.5 | 4.8 | 10.1 | 7.5 | 5.6 | 6.4 | 11.2 | 10.5 | 50.8 | 48.6 |
| v1-c | 75.2 | 75.7 | 3.5 | 3.0 | 5.4 | 4.8 | 12.0 | 11.6 | 10.5 | 11.0 | 51.8 | 49.6 |
| v1-abc | 77.0 | 78.5 | 4.2 | 3.4 | 6.7 | 5.5 | 10.2 | 10.7 | 12.0 | 13.3 | 52.1 | 50.1 |
| dvorak-us | 71.5 | 70.3 | 1.9 | 1.9 | 9.8 | 8.5 | 9.7 | 9.2 | 23.5 | 24.9 | 51.3 | 49.6 |
| itadvorak-v0.1b | 77.0 | 78.5 | 8.9 | 11.0 | 17.7 | 16.1 | 8.1 | 8.6 | 11.2 | 10.5 | 48.1 | 44.7 |
| qwerty-it | 29.8 | 31.4 | 7.0 | 7.8 | 17.3 | 17.6 | 22.0 | 19.4 | 16.3 | 16.1 | 54.2 | 55.2 |

## Frequenze delle lettere che cambiano di più

Quota dei caratteri, in percentuale.

| Carattere | subtitles | wikipedia | differenza |
|---|---|---|---|
| `o` | 11.21 | 8.72 | -2.49 |
| `l` | 5.14 | 7.09 | +1.95 |
| `i` | 9.68 | 11.18 | +1.49 |
| `h` | 1.93 | 0.86 | -1.07 |
| `d` | 3.40 | 4.27 | +0.87 |
| `s` | 5.63 | 4.84 | -0.79 |
| `t` | 5.98 | 6.59 | +0.61 |
| `r` | 5.67 | 6.23 | +0.56 |
| `m` | 3.01 | 2.49 | -0.51 |
| `v` | 1.97 | 1.48 | -0.49 |
| `u` | 3.54 | 3.06 | -0.48 |
| `q` | 0.80 | 0.35 | -0.45 |
