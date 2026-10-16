# Italian Dvorak

[English](README.md)

Un layout di tastiera in stile Dvorak pensato per l'italiano, e un metodo aperto e riproducibile per
progettarlo e valutarlo.

> **Stato: prototipo.** L'attuale candidato (v1) non è definitivo. Vedi la
> [valutazione di v1](docs/v1-evaluation.it.md) per cosa funziona e cosa no.

## Il layout (candidato v1)

```
G W Q Z Y   M L C H B
U A O E I   S N T R D
' . X K J   F P V , -
```

Le vocali stanno sulla home row sinistra, le consonanti frequenti a destra. Le vocali accentate
(à è é ì ò ù) si digitano con un tasto morto sul tasto a destra della home row: tasto morto e poi vocale
per l'accento grave, Shift + tasto morto e poi vocale per l'accento acuto.

| | v1 | QWERTY italiana |
|---|---|---|
| Battute in home row | 75,2% | 29,8% |
| Bigrammi stesso dito | 2,34% | 7,02% |
| Alternanza delle mani | 75,0% | 49,5% |
| Mano sinistra / destra | 50,5 / 49,5 | 54,2 / 45,8 |

Misurato sulle 5.000 parole italiane più frequenti (corpus di sottotitoli). Confronto completo con gli
altri layout: [results/layout_comparison_report.it.md](results/layout_comparison_report.it.md). La
stessa valutazione sull'italiano scritto (Wikipedia) è in
[results/wikipedia/](results/wikipedia/layout_comparison_report.it.md), e
[results/corpus_comparison.it.md](results/corpus_comparison.it.md) mette i due corpus a confronto.

### Provarlo

I file del layout per una copia self-hosted di [keybr](https://www.keybr.com) sono in
[`keybr/`](keybr/README.md). Le versioni installabili per i sistemi operativi arriveranno quando il
layout sarà definitivo.

## Valutare un layout

La pipeline di valutazione richiede solo Python 3.10+, senza pacchetti aggiuntivi.

```sh
python -m kbeval                  # valuta tutti i layout in layouts/ sul corpus di sottotitoli, scrive results/
python -m unittest discover tests # esegue i test
python -m kbeval --help           # tutte le opzioni
```

Per rigenerare tutto `results/`, compresi Wikipedia e il confronto:

```sh
python -m kbeval
python -m kbeval --corpus data/it_wikipedia_top20000.csv --out results/wikipedia
python -m kbeval.compare subtitles=results wikipedia=results/wikipedia --out results
```

Per valutare un tuo layout, aggiungi un file JSON in [`layouts/`](layouts/) (copia
[`10-v1.json`](layouts/10-v1.json) e modifica le righe) e riesegui. Per usare un altro corpus, passa un
CSV con colonne `word,frequency` con `--corpus`. I pesi del punteggio sono in
[`config/weights.json`](config/weights.json).

Output in `results/`:

| File | Contenuto |
|---|---|
| `layout_comparison_report.it.md` (e `.md` in inglese) | report leggibile con tutte le tabelle |
| `scores.csv` | tutte le metriche e il punteggio pesato, una riga per layout |
| `finger_load.csv` | quota di battute per dito |
| `worst_same_finger_bigrams.csv` | i bigrammi stesso dito più scomodi per layout |
| `top_ngrams.csv` | caratteri, bigrammi e trigrammi più frequenti nel corpus |
| `sensitivity.csv` | quanto è stabile la classifica al variare dei pesi |
| `wikipedia/` | gli stessi file per il corpus di Wikipedia |
| `corpus_comparison.it.md` (e `.md` in inglese) | classifiche e metriche principali dei due corpus affiancate |

### Cosa viene misurato

Ogni parola viene digitata sul layout, seguita da uno spazio. La pipeline conta le battute per riga,
mano e dito, lo spostamento delle dita dalla posizione di riposo, i bigrammi stesso dito, l'alternanza
delle mani, i roll verso l'interno e verso l'esterno (interno = verso l'indice), i trigrammi a una mano
e i cambi di direzione, e le battute extra per le vocali accentate (tasto morto, AltGr o Shift). Il
[report](results/layout_comparison_report.it.md) elenca i limiti del modello.

## Struttura della repo

| Percorso | Contenuto |
|---|---|
| `kbeval/` | pipeline di valutazione (Python, solo libreria standard) |
| `layouts/` | layout confrontati, un file JSON ciascuno |
| `config/` | pesi del punteggio |
| `data/` | corpus (sottotitoli, Wikipedia), con la loro [licenza](data/README.md) |
| `docs/` | analisi e note di progetto |
| `results/` | output generati |
| `keybr/` | file del layout per keybr |
| `scripts/` | script di supporto (download del corpus) |

## Roadmap

1. Pipeline di valutazione riproducibile e valutazione di v1. Fatto.
2. Secondo corpus di italiano scritto (Wikipedia), per verificare i risultati oltre i sottotitoli. Fatto.
3. Nuovo layout ottimizzato con il modello corretto.
4. Layout installabili (prima XKB per Linux) e integrazione con keybr.

## Licenza

Codice e documentazione: [MIT](LICENSE). I corpus in `data/` sono CC BY-SA 4.0, vedi
[data/README.md](data/README.md).
