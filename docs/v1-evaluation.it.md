# Valutazione del prototipo Italian-Dvorak v1

[English](v1-evaluation.md)

Questo documento risponde alle domande della specifica di valutazione del progetto (sezioni A–H). Ogni
numero viene da [`results/`](../results/layout_comparison_report.it.md) e si rigenera con `python -m kbeval`.
I numeri indicati come *claim* vengono dal prototipo originale e **non** sono stati validati.

Corpus: le 5.000 parole italiane più frequenti di OpenSubtitles 2018 ([FrequencyWords](../data/README.md)),
pesate per frequenza. Vocali accentate e apostrofi sono mantenuti, quindi i valori differiscono di poco da
quelli "solo lettere" delle note di progetto (che i test riproducono con `--letters-only`).

## A. Giudizio

**Layout da testare, non definitivo.** v1 è un buon layout in stile Dvorak (75% delle battute in home
row, mani bilanciate, 75% di alternanza), ma è stato ottimizzato con il bonus dei roll invertito ed è
superato da un candidato precedente (ItaDvorak v0.2-seed) con la funzione di costo della specifica.
Va tenuto come `v1-candidate`.

## B. Punti forti

- **Home row:** 75,2% delle battute (QWERTY-IT: 29,8%). Spostamento medio delle dita 0,44 larghezze di
  tasto per battuta, il più basso tra i layout non varianti (QWERTY-IT: 0,80).
- **Bilanciamento:** 50,5% sinistra / 49,5% destra.
- **Alternanza:** il 75,0% dei bigrammi dentro le parole cambia mano, come Dvorak US (74,5%).
- **Spazio:** l'84% delle parole italiane finisce in vocale; con le vocali a sinistra, l'87% delle fini
  di parola è digitato dalla mano sinistra, quindi uno spazio col pollice destro alterna in modo naturale.
- **Bigrammi stesso dito:** 2,34%, molto meno di QWERTY-IT (7,02%).

## C. Punti deboli

- **Roll verso l'esterno.** A causa del segno invertito nell'ottimizzatore, v1 ha più roll verso
  l'esterno (12,9% dei bigrammi) che verso l'interno (5,6%). Tutti gli altri candidati italiani hanno il
  rapporto opposto; v0.2-seed ha 13,6% verso l'interno e 4,5% verso l'esterno.
- **E e I sullo stesso indice sinistro.** `ie` ed `ei` sono i due bigrammi stesso dito più frequenti di
  v1 (0,49% e 0,40%), seguiti da `zi` (0,32%, anche la Z è sull'indice sinistro).
- **L (domanda A).** La L è più frequente della D (5,14% contro 3,40% dei caratteri), ma portarla in
  home row (variante A) mette la D sopra la N sull'indice destro e crea il bigramma stesso dito `nd`
  (0,66%). La variante A guadagna home row (77,0%) ma perde su bigrammi stesso dito (2,94%) e carico dei
  mignoli (12,3%), e ha un punteggio peggiore di v1. La L non si sistema con uno scambio, serve un
  riordino.
- **QU (domanda B).** `qu` è l'1,06% dei bigrammi. In v1 è un roll verso l'esterno sulla stessa mano
  (dal medio al mignolo sinistro). Spostare la Q a destra (variante B) lo fa alternare ma cambia appena
  il punteggio (0,3163 contro 0,3146): QU non è un vero problema.
- **CH (domanda C).** `ch` è l'1,50% dei bigrammi e `che` è il trigramma più frequente (1,58%). In v1 è
  un roll verso l'esterno sulla riga alta destra (dal medio all'anulare), comodo. Spostare la H a
  sinistra (variante C) crea `hi` come bigramma stesso dito e peggiora nettamente il punteggio (0,3678).
  C e H vanno lasciate insieme.
- **Accenti.** Le vocali accentate costano 0,73 battute extra ogni 100 caratteri con tasto morto o
  AltGr, contro 0,06 sulla tastiera italiana (solo é richiede Shift). La sola `è` è la decima parola
  più frequente.
- **Corpus.** I sottotitoli sovrarappresentano il dialogo; vedi E.

## D. Il claim "39% di riduzione dello sforzo"

Non è un risultato. Usava lo stesso modello per ottimizzare e per misurare, sugli stessi dati, con il
bonus dei roll invertito. Lo script originale è perso e il suo costo totale non si riesce a ricostruire
dalla descrizione (le statistiche di lettere e bigrammi invece sono riprodotte esattamente dai `tests/`).
Con la funzione di costo della specifica usata qui, v1 ottiene 0,315 contro 1,679 di QWERTY-IT, ma il
rapporto dipende dai pesi e non va citato come riduzione dello sforzo.

## E. Piano di validazione

1. Rieseguire questa pipeline su un secondo corpus di italiano scritto e verificare se la classifica
   regge. Fatto: vedi [Secondo corpus](#secondo-corpus-wikipedia-in-italiano) più sotto.
2. Confrontare con un analyzer esistente (per esempio Oxeylyzer o genkey) sullo stesso corpus.
3. Aggiungere testo con spazi e punteggiatura, così da modellare i bigrammi tra parole e l'apostrofo.

## F. Varianti testate

| Layout | Modifica | Punteggio | Posizione media con pesi casuali |
|---|---|---|---|
| v0.2-seed | candidato precedente | **0,2489** | 1,00 (primo nel 99,7% dei campioni) |
| v1-d | v1 con accenti via AltGr | 0,3094 | 2,16 |
| v1 | prototipo | 0,3146 | 3,31 |
| v1-b | Q ↔ B | 0,3163 | 3,96 |
| v1-a | L ↔ D | 0,3268 | 4,71 |
| v1-c | H ↔ Z | 0,3678 | 7,03 |
| v1-abc | tutte e tre | 0,3804 | 7,89 |

Punteggio più basso = migliore. La variante D cambia solo il modo di digitare gli accenti: la battuta
extra passa dal mignolo destro (tasto Quote) al pollice, e il carico dei mignoli scende dal 10,5% al
9,9%. Il tasto morto funziona su qualunque tastiera e gestisce bene le maiuscole; AltGr richiede un Alt
destro che funzioni come AltGr.

## G. Raccomandazione

Tenere v1 come **v1-candidate**. Non adottarla e non tornare alla v0.1 (più bigrammi stesso dito,
4,55%). Generare un nuovo layout con il verso dei roll corretto (passo 3 del piano), partendo da
v0.2-seed e v1 e usando il secondo corpus come verifica.

Sui pesi (sezione 5 della specifica): le penalità per riga alta e bassa duplicano in buona parte il
termine di distanza; la penalità sullo spazio è un'approssimazione debole perché una lista di parole
non contiene spazi reali; è stata aggiunta una penalità per la riga dei numeri (peso 1,0) perché
l'apostrofo e la ì di QWERTY-IT non risultino gratis. Vanno rivisti prima del passo 3, ma l'analisi di
sensibilità mostra che la testa della classifica è stabile con ogni peso variato del ±50%.

## H. Prossimo passo

Generare un nuovo layout con il verso dei roll corretto, valutato su entrambi i corpus (passo 3 del piano).

## Secondo corpus: Wikipedia in italiano

La stessa valutazione sulle 20.000 parole più frequenti di Wikipedia in italiano
([risultati](../results/wikipedia/layout_comparison_report.it.md),
[confronto affiancato](../results/corpus_comparison.it.md)).

- **v0.2-seed resta prima** (prima nell'88,9% dei campioni di pesi, contro il 99,7% sui sottotitoli). Il
  suo vantaggio non dipende dal corpus.
- **v1 scende dal 3° al 6° posto.** L'italiano scritto ha più L (7,09% contro 5,14%), I e D, e molte meno
  O e H. I suoi bigrammi stesso dito salgono dal 2,3% al 3,1%, soprattutto `zi` (0,59%, da *-zione*)
  sull'indice sinistro, che porta anche E e I.
- **Le varianti si scambiano di posto.** Su Wikipedia separare C e H (variante C) e la combinazione
  A+B+C battono v1, mentre sui sottotitoli erano peggiori. Gli scambi di singole lettere stanno dentro
  la variabilità dovuta alla scelta del corpus: non bastano per scegliere una variante.
- **Robustezza:** la classifica è la stessa con le prime 5.000 o le prime 20.000 parole di Wikipedia,
  quindi la differenza viene dal tipo di testo, non dalla lunghezza della lista.

Conclusione per il passo 3: ottimizzare su entrambi i corpus insieme e considerare v0.2-seed il
riferimento da battere.
