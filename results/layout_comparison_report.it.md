# Report di confronto dei layout

[English](layout_comparison_report.md)

_Generato da `python -m kbeval`. Non modificarlo a mano: riesegui la pipeline._

## Corpus

`data/it_top5000.csv`: 5,000 parole, 216,627,755 occorrenze, 889,950,219 caratteri.

## Pesi del punteggio

Punteggio più basso = migliore. I pesi negativi sono premi. Vedi `config/weights.json`.

| metric | weight |
|---|---|
| `mean_distance` | +1.00 |
| `same_finger_bigrams` | +2.50 |
| `pinky_load` | +1.50 |
| `hand_imbalance` | +1.00 |
| `bottom_row` | +0.75 |
| `top_row` | +0.50 |
| `number_row` | +1.00 |
| `accent_extra_keystrokes` | +0.50 |
| `word_end_space_hand` | +0.75 |
| `hand_alternation` | -0.75 |
| `roll_inward` | -0.50 |

## Layout

**QWERTY (Italian)** (`qwerty-it`): Standard Italian keyboard. Accented vowels have their own keys; é is Shift + è.

```
q w e r t   y u i o p
a s d f g   h j k l ò
z x c v b   n m , . -
```

**Dvorak (US)** (`dvorak-us`): Standard US Dvorak. It has no accented letters, so the same dead key as v1 (Quote key) is assumed.

```
' , . p y   f g c r l
a o e u i   d h t n s
; q j k x   b m w v z
```

**ItaDvorak v0.1** (`itadvorak-v0.1`): Earlier candidate from the project spec.

```
w f h k j   c d p m g
u o a e i   n t r l s
x y , . '   q v b z ;
```

**ItaDvorak v0.1b** (`itadvorak-v0.1b`): v0.1 with N and I swapped.

```
w f h k j   c d p m g
u o a e n   i t r l s
x y , . '   q v b z ;
```

**ItaDvorak v0.2-seed** (`itadvorak-v0.2-seed`): Earlier candidate from the project spec.

```
w h z k j   c d r p f
u i o e a   t l n s m
x y , . '   v q b g ;
```

**Italian-Dvorak v1** (`v1`): The current prototype, as in it_dvorak.json (dead key on the Quote key).

```
g w q z y   m l c h b
u a o e i   s n t r d
' . x k j   f p v , -
```

**v1 variant A (L on home row)** (`v1-a`): v1 with L and D swapped, so L is on the home row.

```
g w q z y   m d c h b
u a o e i   s n t r l
' . x k j   f p v , -
```

**v1 variant B (Q on the right)** (`v1-b`): v1 with Q and B swapped, so QU alternates hands.

```
g w b z y   m l c h q
u a o e i   s n t r d
' . x k j   f p v , -
```

**v1 variant C (C and H on different hands)** (`v1-c`): v1 with H and Z swapped, so CH alternates hands.

```
g w q h y   m l c z b
u a o e i   s n t r d
' . x k j   f p v , -
```

**v1 variant D (AltGr accents)** (`v1-d`): v1 letters, accents typed as AltGr + vowel instead of a dead key.

```
g w q z y   m l c h b
u a o e i   s n t r d
' . x k j   f p v , -
```

**v1 variants A+B+C combined** (`v1-abc`): v1 with L on the home row, Q on the right and H on the left.

```
g w b h y   m d c z q
u a o e i   s n t r l
' . x k j   f p v , -
```

## Punteggi

Valori in percentuale delle battute (righe, mani, mignoli) o dei bigrammi di tasti dentro le parole (SFB, alternanza, roll). La distanza è in larghezze di tasto per battuta. Il costo accenti è in battute extra ogni 100 caratteri.

| Pos. | Layout | Punteggio | Home | Alta | Bassa | Distanza | SFB | Alternanza | Roll verso l'interno | Roll verso l'esterno | Mignoli | Mano sinistra | Costo accenti |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | itadvorak-v0.2-seed | 0.2489 | 74.3 | 19.9 | 5.8 | 0.475 | 1.68 | 76.0 | 13.6 | 4.5 | 8.3 | 50.3 | 0.73 |
| 2 | v1-d | 0.3094 | 75.1 | 18.5 | 6.4 | 0.435 | 2.35 | 75.0 | 5.6 | 12.8 | 9.9 | 50.8 | 0.73 |
| 3 | v1 | 0.3146 | 75.2 | 18.4 | 6.4 | 0.438 | 2.34 | 75.0 | 5.6 | 12.9 | 10.5 | 50.5 | 0.73 |
| 4 | v1-b | 0.3163 | 75.2 | 18.4 | 6.4 | 0.438 | 2.46 | 74.8 | 6.3 | 12.2 | 10.3 | 50.8 | 0.73 |
| 5 | v1-a | 0.3268 | 77.0 | 16.6 | 6.4 | 0.421 | 2.94 | 75.0 | 6.0 | 11.9 | 12.3 | 50.5 | 0.73 |
| 6 | itadvorak-v0.1 | 0.3484 | 77.0 | 18.0 | 5.1 | 0.446 | 4.55 | 75.6 | 10.1 | 5.6 | 11.2 | 50.8 | 0.73 |
| 7 | v1-c | 0.3678 | 75.2 | 18.4 | 6.4 | 0.438 | 3.52 | 74.9 | 5.4 | 12.0 | 10.5 | 51.8 | 0.73 |
| 8 | v1-abc | 0.3804 | 77.0 | 16.6 | 6.4 | 0.421 | 4.20 | 74.7 | 6.7 | 10.2 | 12.0 | 52.1 | 0.73 |
| 9 | dvorak-us | 0.5239 | 71.5 | 20.9 | 7.6 | 0.444 | 1.88 | 74.5 | 9.8 | 9.7 | 23.5 | 51.3 | 0.73 |
| 10 | itadvorak-v0.1b | 0.6305 | 77.0 | 18.0 | 5.1 | 0.446 | 8.87 | 61.2 | 17.7 | 8.1 | 11.2 | 48.1 | 0.73 |
| 11 | qwerty-it | 1.6790 | 29.8 | 51.3 | 18.3 | 0.803 | 7.02 | 49.5 | 17.3 | 22.0 | 16.3 | 54.2 | 0.06 |

## Sensibilità ai pesi

2,000 campioni, ogni peso moltiplicato per un fattore casuale tra 0.5x e 1.5x.

| Layout | Posizione media | Primo posto | Intervallo posizioni |
|---|---|---|---|
| itadvorak-v0.2-seed | 1.00 | 99.7% | 1–3 |
| v1-d | 2.16 | 0.0% | 2–6 |
| v1 | 3.31 | 0.0% | 2–6 |
| v1-b | 3.96 | 0.0% | 3–6 |
| v1-a | 4.71 | 0.4% | 1–6 |
| itadvorak-v0.1 | 5.92 | 0.0% | 2–8 |
| v1-c | 7.03 | 0.0% | 6–8 |
| v1-abc | 7.89 | 0.0% | 6–8 |
| dvorak-us | 9.10 | 0.0% | 9–10 |
| itadvorak-v0.1b | 9.90 | 0.0% | 9–10 |
| qwerty-it | 11.00 | 0.0% | 11–11 |

## Carico per dito (% delle battute)

| Layout | LP | LR | LM | LI | RI | RM | RR | RP |
|---|---|---|---|---|---|---|---|---|
| qwerty-it | 12.4 | 5.7 | 19.1 | 17.0 | 15.7 | 9.8 | 16.4 | 3.9 |
| dvorak-us | 11.6 | 12.0 | 11.5 | 16.2 | 11.7 | 10.5 | 14.6 | 11.9 |
| itadvorak-v0.1 | 3.6 | 12.3 | 12.9 | 21.9 | 23.6 | 9.4 | 8.7 | 7.6 |
| itadvorak-v0.1b | 3.6 | 12.3 | 12.9 | 19.2 | 26.3 | 9.4 | 8.7 | 7.6 |
| itadvorak-v0.2-seed | 3.6 | 11.7 | 11.8 | 23.2 | 21.7 | 13.8 | 9.6 | 4.7 |
| v1 | 5.4 | 11.1 | 12.0 | 22.1 | 24.4 | 12.4 | 7.5 | 5.1 |
| v1-a | 5.4 | 11.1 | 12.0 | 22.1 | 22.7 | 12.4 | 7.5 | 6.8 |
| v1-b | 5.4 | 11.1 | 12.3 | 22.1 | 24.4 | 12.4 | 7.5 | 4.8 |
| v1-c | 5.4 | 11.1 | 12.0 | 23.4 | 24.4 | 12.4 | 6.2 | 5.1 |
| v1-d | 5.4 | 11.1 | 12.1 | 22.2 | 24.6 | 12.5 | 7.6 | 4.5 |
| v1-abc | 5.4 | 11.1 | 12.3 | 23.4 | 22.7 | 12.4 | 6.2 | 6.6 |

## Peggiori bigrammi stesso dito di Italian-Dvorak v1

Ordinati per quota x (1 + distanza tra i tasti). ◌ = tasto morto.

| Bigramma | Dito | Quota | Distanza tasti |
|---|---|---|---|
| `ie` | LI | 0.49% | 1.00 |
| `zi` | LI | 0.32% | 1.60 |
| `ei` | LI | 0.40% | 1.00 |
| `mp` | RI | 0.20% | 2.66 |
| `sp` | RI | 0.23% | 1.80 |
| `ns` | RI | 0.17% | 1.00 |
| `iz` | LI | 0.08% | 1.60 |
| `gu` | LP | 0.10% | 1.03 |
| `lm` | RI | 0.05% | 1.00 |
| `ez` | LI | 0.05% | 1.03 |

## N-grammi più frequenti nel corpus

**Caratteri:** `o` 11.21%, `e` 11.21%, `a` 10.99%, `i` 9.68%, `n` 7.09%, `t` 5.98%, `r` 5.67%, `s` 5.63%, `l` 5.14%, `c` 4.52%, `u` 3.54%, `d` 3.40%, `m` 3.01%, `p` 2.73%, `v` 1.97%, `h` 1.93%, `g` 1.31%, `b` 1.09%, `f` 1.01%, `q` 0.80%

**Bigrammi:** `no` 2.40%, `on` 2.18%, `er` 2.07%, `re` 2.02%, `to` 1.98%, `co` 1.67%, `di` 1.62%, `ch` 1.50%, `ta` 1.38%, `st` 1.36%, `en` 1.34%, `la` 1.29%, `ra` 1.28%, `an` 1.28%, `ar` 1.28%, `te` 1.22%, `ia` 1.21%, `or` 1.21%, `un` 1.19%, `he` 1.13%

**Trigrammi:** `che` 1.58%, `non` 1.34%, `per` 1.10%, `sta` 0.79%, `ent` 0.78%, `are` 0.77%, `que` 0.74%, `ell` 0.72%, `cos` 0.66%, `tto` 0.64%, `est` 0.63%, `ato` 0.59%, `con` 0.58%, `ono` 0.58%, `gli` 0.57%, `iam` 0.54%, `ere` 0.53%, `and` 0.53%, `lla` 0.53%, `sto` 0.53%

## Limiti del modello

- Il corpus è una lista di parole: i bigrammi non attraversano lo spazio e la punteggiatura è quasi assente.
- La distanza è misurata dal tasto di riposo di ogni dito; lo spostamento tra tasti consecutivi non è modellato.
- Shift e AltGr contano come battute extra ma non come pressioni delle dita.
- Si assume che lo spazio dopo una parola sia premuto con il pollice destro (`word_end_space_hand`).
- I layout senza accenti nativi usano un tasto morto sul tasto Quote, come v1.
