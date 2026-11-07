# Italian-Dvorak v2

[English](v2-candidate.md)

v2 è il primo layout prodotto dall'ottimizzatore di questa repo, con il verso dei roll corretto,
valutato su entrambi i corpus insieme, e con un tasto dedicato per la è. Restano aperti la
punteggiatura fuori dal blocco principale e le prove di digitazione reali.

```
K F ' Q È   B D S M J   X
U E I A O   C T L N R   ◌
W Z Y . ,   P G V H -
```

- **è** ha un tasto suo; **Shift + è = é**, come sulla tastiera italiana (*perché*, *né*).
- **à ì ò ù** e le maiuscole accentate usano il tasto morto ◌ (tasto Quote): tasto morto e poi vocale
  per l'accento grave, Shift + tasto morto e poi vocale per l'acuto.
- **X** va sul tasto a destra della riga alta (BracketLeft su una tastiera QWERTY); è lo 0,01% delle
  lettere.

## Come è stato ottenuto

L'ottimizzatore ha prodotto prima `v2-base` ([`20-v2-base.json`](../layouts/20-v2-base.json)), con le
stesse lettere e il tasto morto per tutti gli accenti:

```sh
python -m kbeval.optimize --corpus data/it_top5000.csv --corpus data/it_wikipedia_top20000.csv \
    --vowels-left --seeds 1 2 3 4 5 6 7 8 --steps 300000 \
    --out layouts/20-v2-base.json --id v2-base --name "Italian-Dvorak v2 base (optimiser output)"
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
- **È dedicata** (scelta il 16/10/2026 tra tasto morto, AltGr, è dedicata o tutte le accentate su tasti
  propri). La sola è vale il 45% delle vocali accentate. La è è stata provata su ogni tasto principale,
  spostando la lettera sostituita sul tasto extra; il punteggio migliore è sulla riga alta sotto
  l'indice sinistro (al posto della X). La è sul mignolo destro accanto al tasto morto peggiora
  nettamente (0,222). Il risultato è `v2` ([`21-v2.json`](../layouts/21-v2.json)).

## Risultati

| | v2-base | v0.2-seed | v1 | QWERTY italiana |
|---|---|---|---|---|
| Punteggio, sottotitoli | **0,207** | 0,249 | 0,315 | 1,679 |
| Punteggio, Wikipedia | **0,206** | 0,307 | 0,371 | 1,624 |
| Home row (sottotitoli / Wikipedia) | 75,9 / 77,8% | 74,3 / 74,7% | 75,2 / 75,7% | 29,8 / 31,4% |
| Bigrammi stesso dito | **0,39 / 0,66%** | 1,68 / 1,97% | 2,34 / 3,06% | 7,02 / 7,79% |
| Roll verso l'interno / l'esterno (sottotitoli) | 13,0 / 7,8% | 13,6 / 4,5% | 5,6 / 12,9% | 17,3 / 22,0% |
| Alternanza delle mani (sottotitoli) | 74,7% | 76,0% | 75,0% | 49,5% |
| Mignoli (sottotitoli) | 10,1% | 8,3% | 10,5% | 16,3% |

Con la è dedicata, v2 mantiene le stesse lettere e cambia solo il modo di digitare gli accenti:

| | v2-base (solo tasto morto) | v2 (è dedicata) |
|---|---|---|
| Punteggio (sottotitoli / Wikipedia) | 0,207 / 0,206 | 0,209 / **0,204** |
| Battute extra per accenti, ogni 100 caratteri | 0,73 / 0,77 | **0,37 / 0,47** |
| Mignoli | 10,1 / 10,2% | **9,8 / 10,0%** |
| Home row | 75,9 / 77,8% | 75,4 / 77,4% |

v2 e v2-base occupano i primi due posti in quasi tutti i campioni dell'analisi di sensibilità ai pesi
(v0.2-seed è prima solo nell'1,5% dei campioni sui sottotitoli e mai su Wikipedia). Tabelle complete:
[results/corpus_comparison.it.md](../results/corpus_comparison.it.md).

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
- **Scorciatoie:** Z, X, C, V non sono più sulla riga bassa sinistra (la C è sulla home row destra,
  la X fuori dal blocco principale).
- **Non modellati:** maiuscole, cifre, punteggiatura diversa da apostrofo, punto, virgola e trattino, e
  bigrammi a cavallo dello spazio.
- **Punteggiatura e simboli** fuori dal blocco principale (riga dei numeri, parentesi, ; : ? !) seguono
  ancora la tastiera italiana e verranno definiti quando il layout sarà impacchettato.
