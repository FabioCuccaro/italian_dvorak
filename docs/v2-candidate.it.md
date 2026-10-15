# Italian-Dvorak v2 (candidato)

[English](v2-candidate.md)

v2 è il primo layout prodotto dall'ottimizzatore di questa repo, con il verso dei roll corretto e
valutato su entrambi i corpus insieme. È un **candidato**: accenti, punteggiatura e prove di digitazione
reali sono ancora aperti.

```
K F ' Q X   B D S M J
U E I A O   C T L N R   ◌
W Z Y . ,   P G V H -
```

◌ è il tasto morto per gli accenti (tasto Quote), come in v1: tasto morto e poi vocale per l'accento
grave, Shift + tasto morto e poi vocale per l'accento acuto.

## Come è stato ottenuto

```sh
python -m kbeval.optimize --corpus data/it_top5000.csv --corpus data/it_wikipedia_top20000.csv \
    --vowels-left --seeds 1 2 3 4 5 6 7 8 --steps 300000 \
    --out layouts/20-v2.json --id v2 --name "Italian-Dvorak v2 (candidate)"
```

- **Obiettivo:** lo stesso punteggio pesato di `python -m kbeval` ([`config/weights.json`](../config/weights.json)),
  mediato sui corpus di sottotitoli e di Wikipedia. Un test verifica che ottimizzatore e pipeline diano
  lo stesso numero per lo stesso layout.
- **Ricerca:** simulated annealing a scambi di tasti sui 30 tasti principali (26 lettere, apostrofo,
  punto, virgola, trattino), ripartito da 8 seed. Esecuzioni con 2 milioni di passi e altri 24 seed non
  hanno trovato layout migliori; 9 di esse hanno raggiunto lo stesso punteggio migliore.
- **Vocali a sinistra:** la ricerca è stata fatta con e senza questo vincolo. Entrambe trovano lo stesso
  layout: le vocali finiscono sulla home row sinistra senza essere forzate.
- P e G (riga bassa, indice destro) si possono scambiare senza costo; tutte le metriche restano uguali.

## Risultati

| | v2 | v0.2-seed | v1 | QWERTY italiana |
|---|---|---|---|---|
| Punteggio, sottotitoli | **0,207** | 0,249 | 0,315 | 1,679 |
| Punteggio, Wikipedia | **0,206** | 0,307 | 0,371 | 1,624 |
| Home row (sottotitoli / Wikipedia) | 75,9 / 77,8% | 74,3 / 74,7% | 75,2 / 75,7% | 29,8 / 31,4% |
| Bigrammi stesso dito | **0,39 / 0,66%** | 1,68 / 1,97% | 2,34 / 3,06% | 7,02 / 7,79% |
| Roll verso l'interno / l'esterno (sottotitoli) | 13,0 / 7,8% | 13,6 / 4,5% | 5,6 / 12,9% | 17,3 / 22,0% |
| Alternanza delle mani (sottotitoli) | 74,7% | 76,0% | 75,0% | 49,5% |
| Mignoli (sottotitoli) | 10,1% | 8,3% | 10,5% | 16,3% |

v2 è prima nel 98,2% (sottotitoli) e nel 100% (Wikipedia) dei campioni dell'analisi di sensibilità ai
pesi. Tabelle complete: [results/corpus_comparison.it.md](../results/corpus_comparison.it.md).

## Quanto è reale

Le note di progetto avvertivano che ottimizzare e misurare con lo stesso modello sugli stessi dati è
circolare. v2 è ottimizzata su entrambi i corpus, quindi il punteggio qui sopra è "in-sample". Due
verifiche:

- **Test incrociato tra corpus.** Un layout ottimizzato solo sui sottotitoli ottiene 0,272 su
  Wikipedia, che non ha mai visto: comunque meglio di v0.2-seed (0,307) e di v1 (0,371). Un layout
  ottimizzato solo su Wikipedia ottiene 0,267 sui sottotitoli, peggio di v0.2-seed (0,249). Una parte
  del vantaggio di ogni layout ottimizzato viene dall'adattarsi al proprio corpus; ottimizzare su
  entrambi i corpus serve a limitarlo.
- **Metriche fuori dal punteggio.** I cambi di direzione (trigrammi a una mano che cambiano verso) non
  sono nel punteggio e peggiorano: 3,7% dei trigrammi sui sottotitoli, contro 2,9% di v1 e 1,6% di
  v0.2-seed. Anche la riga bassa è più usata (8,6% contro 6,4% di v1).

## Punti aperti

- **S sulla riga alta.** La S è frequente (5,6% / 4,8%) ma sta sulla riga alta (medio destro). Il
  punteggio la preferisce lì perché evita bigrammi stesso dito; una prova di digitazione dirà se è
  comoda.
- **Apostrofo sulla riga alta sinistra** (medio), accanto a F e Q. Nelle elisioni come *l'anno* o
  *dell'epoca* è di solito seguito da una vocale sulla stessa mano.
- **Scorciatoie:** Z, X, C, V non sono più sulla riga bassa sinistra (la C è sulla home row destra).
- **Non modellati:** maiuscole, cifre, punteggiatura diversa da apostrofo, punto, virgola e trattino, e
  bigrammi a cavallo dello spazio.
- **Accenti e punteggiatura** sono ancora da decidere (tasto morto, AltGr o è dedicata), prima di
  preparare il layout per l'uso quotidiano.
