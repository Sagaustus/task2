# Grammar Checker (Assignment 2 – CMPUT 461/501)

## Overview
This repository implements a simple grammar checker using a **toy context-free grammar (CFG)** in NLTK. Instead of parsing surface words, it parses **POS-tag sequences** (Penn Treebank tags). A sentence is judged grammatical if the parser can derive it from the CFG, and ungrammatical otherwise. The system also evaluates performance against labeled data with **precision and recall**.

## Repository Layout
```

grammars/       # toy grammar files (.cfg)
src/            # Python source code (main runner, parser, evaluation)
reports/        # Justifications, extension (if required), metrics outputs
data/           # Input TSV files (id, label, sentence, pos)
output/         # Generated TSV predictions

````

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install nltk
````

## Usage

Run the grammar checker on the provided dataset:

```bash
python3 src/main.py data/train.tsv grammars/toy.cfg output/train.tsv
```

This produces:

* **output/train.tsv** → columns: id, ground_truth, prediction
* **reports/metrics.json** and **reports/metrics.txt** → precision, recall, TP/FP/FN/TN summary

## Report Files

* `reports/justifications.md` → includes precision, recall, error analysis, iteration notes, and discussion of feasibility.
* `reports/extension.md` → (graduate extension) describes handling of colloquial expressions.

## Notes

* The grammar (`grammars/toy.cfg`) is deliberately simplistic.
* English is **not a context-free language**, so this checker cannot be perfect.
* The assignment requires focusing on toy CFG design, parser integration, and evaluation.

```
