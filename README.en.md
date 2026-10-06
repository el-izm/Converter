# Interlinear-to-UD converter

Converts plain-text interlinear records, glossed following the Leipzig
Glossing Rules, into JSON documents whose tokens carry Universal Dependencies
feature–value pairs. Everything language-specific is declared in a single file,
`atr_val.py`, so the converter itself is not modified when a new language is
added.

## Requirements

Python 3, plus:

```bash
pip install stanza tqdm
```

## Setup

1. Place the language's gloss map at `src/translator/atr_val.py`.
2. Place the input files in `input/` in the repository root. Subdirectories are
   allowed, at any depth; the structure is mirrored in the output.

## Running

```bash
python src/main.py
```

For each `.txt` file found under `input/`, the converter writes:

| Path | Contents |
| ---- | -------- |
| `output/<name>.json`        | the sentences as JSON documents |
| `output/<name>_conllu.txt`  | the same sentences in CoNLL-U |
| `output/corpus_stats.json`  | per-text and corpus-level counts |
| `skipped/skipped_<name>.txt`| records that could not be read |
| `logs/gloss_issues_<name>.log`   | malformed or unparsable glossing |
| `logs/atr_val_issues_<name>.log` | glosses the map does not cover |

The two log files are the ones to read after a run: between them they list
every record the converter could not fully resolve, with the sentence
identifier, the segmentation and the gloss line.

## The gloss map

`atr_val.py` declares:

- `morphdict` — the gloss abbreviations and the feature–value pairs they
  resolve to, for example `CONV` to `VerbForm=Conv`. One gloss may map to
  several features, separated by `|`.
- `defaults` — the features a part of speech receives when the gloss line
  omits them, optionally conditioned on features already assigned. A condition
  has the form `Feature=Value` or `Feature!=Value`, and the order of the list
  matters, because an automatically assigned value may be used in the
  conditions of later ones.
- `adjectives` — whether the language has a distinct adjective class. If false
  or absent, adjectives are treated as verbs.
- `prefixes` — whether the language has prefixes. If false or absent, prefixes
  are treated as proclitics.

## Converting proclitics to prefixes

After the JSON files have been produced, an optional second pass rewrites
proclitics as prefixes, moving their person, number and reflexivity onto the
verb under the label `[obj]`:

```bash
python src/add_prefixes.py
```

A verb's own person and number are labelled `[subj]`, whether or not a
proclitic is present.

## Licence

The code is distributed under the MIT licence; see `LICENSE`.
