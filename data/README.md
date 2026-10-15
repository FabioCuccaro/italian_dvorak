# Data

## it_top5000.csv

The 5,000 most frequent words of Italian subtitles, with their counts (`word,frequency`).

- Source: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) by Hermit Dave,
  file `content/2018/it/it_50k.txt`, built from [OpenSubtitles 2018](http://opus.nlpl.eu/OpenSubtitles2018.php).
- License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), like the original content.
  This file is a subset of the original (first 5,000 lines, converted to CSV); no other change.
- Regenerate it with `python scripts/fetch_corpus.py`.

The code in this repository is MIT licensed; this data file keeps its own CC BY-SA 4.0 license.

---

# Dati (italiano)

`it_top5000.csv` contiene le 5.000 parole più frequenti dei sottotitoli italiani con le loro occorrenze.
Fonte: [FrequencyWords](https://github.com/hermitdave/FrequencyWords) di Hermit Dave (file
`content/2018/it/it_50k.txt`, da OpenSubtitles 2018). Licenza CC BY-SA 4.0, come l'originale; il file è
un sottoinsieme (prime 5.000 righe convertite in CSV) e si rigenera con `python scripts/fetch_corpus.py`.
