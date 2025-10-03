# src/main.py
from __future__ import annotations
import argparse
import csv
from pathlib import Path

from grammar_checker import parse_dataset  # relies on src/grammar_checker.py


def write_output_tsv(output_path: str | Path, rows) -> None:
    """
    Write the required TSV with columns: id, ground_truth, prediction
    prediction = 1 if parse FAILED (ungrammatical), 0 if parse SUCCEEDED (grammatical).
    """
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerow(["id", "ground_truth", "prediction"])
        for r in rows:
            prediction = 0 if r.parsed else 1
            writer.writerow([r.sent_id, r.ground_truth, prediction])


def main():
    parser = argparse.ArgumentParser(
        description="Simple grammar checker over POS-tag sequences using an NLTK CFG."
    )
    parser.add_argument("input_tsv", type=str, help="Path to input TSV with columns: id, label, sentence, pos")
    parser.add_argument("grammar_cfg", type=str, help="Path to NLTK .cfg grammar (POS-only terminals)")
    parser.add_argument("output_tsv", type=str, help="Path to write output TSV: id, ground_truth, prediction")
    args = parser.parse_args()

    # Parse dataset with the provided grammar
    results = parse_dataset(args.input_tsv, args.grammar_cfg)

    # Write required output TSV
    write_output_tsv(args.output_tsv, results)


if __name__ == "__main__":
    main()
