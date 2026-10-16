# Data

## it_top5000.csv

The 5,000 most frequent words of Italian subtitles, with their counts (`word,frequency`).

- Source: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) by Hermit Dave,
  file `content/2018/it/it_50k.txt`, built from [OpenSubtitles 2018](http://opus.nlpl.eu/OpenSubtitles2018.php).
- License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), like the original content.
  This file is a subset of the original (first 5,000 lines, converted to CSV); no other change.
- Regenerate it with `python scripts/fetch_corpus.py subtitles`.

## it_wikipedia_top20000.csv

The 20,000 most frequent words of Italian Wikipedia, with their counts (`word,frequency`). Used as a
second corpus of written Italian.

- Source: [wikipedia-word-frequency](https://github.com/IlyaSemenov/wikipedia-word-frequency) by Ilya
  Semenov, file `results/itwiki-2022-08-30.txt`, built from the Italian Wikipedia dump of 30 August 2022.
  Words appearing in fewer than 3 articles are excluded at the source.
- License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), like the Wikipedia text it is
  derived from (text by the contributors of Italian Wikipedia).
- Changes: words containing characters other than a-z, Italian accented vowels and the apostrophe were
  dropped (0.5% of tokens: foreign names, other scripts), then the first 20,000 words were kept.
- Regenerate it with `python scripts/fetch_corpus.py wikipedia`.

The code in this repository is MIT licensed; these data files keep their own CC BY-SA 4.0 license.

---

# Dati (italiano)

`it_top5000.csv` contiene le 5.000 parole più frequenti dei sottotitoli italiani con le loro occorrenze.
Fonte: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) di Hermit Dave (file
`content/2018/it/it_50k.txt`, da OpenSubtitles 2018). Licenza CC BY-SA 4.0, come l'originale; il file è
un sottoinsieme (prime 5.000 righe convertite in CSV) e si rigenera con
`python scripts/fetch_corpus.py subtitles`.

`it_wikipedia_top20000.csv` contiene le 20.000 parole più frequenti di Wikipedia in italiano (dump del
30 agosto 2022), da [wikipedia-word-frequency](https://github.com/IlyaSemenov/wikipedia-word-frequency)
di Ilya Semenov. Licenza CC BY-SA 4.0, come il testo di Wikipedia da cui deriva. Sono state tolte le
parole con caratteri diversi da a-z, vocali accentate e apostrofo (0,5% delle occorrenze). Si rigenera
con `python scripts/fetch_corpus.py wikipedia`.
