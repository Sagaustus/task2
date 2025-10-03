# src/grammar_checker.py
from __future__ import annotations
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Tuple

import nltk
from nltk import CFG
from nltk.parse import ChartParser

@dataclass
class ParsedRow:
    sent_id: str
    ground_truth: int  # 1 = ungrammatical, 0 = grammatical (from dataset)
    pos_tokens: List[str]
    parsed: bool       # True if grammar can parse, else False

def load_cfg(grammar_path: str | Path) -> CFG:
    """
    Load an NLTK .cfg grammar file from disk.
    """
    grammar_path = Path(grammar_path)
    with grammar_path.open("r", encoding="utf-8") as f:
        grammar_text = f.read()
    return CFG.fromstring(grammar_text)

def build_parser(grammar: CFG) -> ChartParser:
    """
    Build a (top-down) chart parser for the provided grammar.
    """
    return ChartParser(grammar)

def try_parse_pos(parser: ChartParser, pos_tokens: Iterable[str]) -> bool:
    """
    Return True iff at least one parse exists for the given POS sequence.
    Efficiently checks existence by pulling a single tree without enumerating all trees.
    """
    # Ensure tokens are strings exactly matching preterminals in the grammar (e.g., 'DT', 'NN', '.')
    tokens = [t.strip() for t in pos_tokens if t.strip() != ""]
    try:
        tree_iter = parser.parse(tokens)
        # Pull at most one tree to test parseability
        next(tree_iter, None)
        # If we got here without StopIteration, a parse exists
        return True
    except StopIteration:
        return False
    except ValueError:
        # NLTK raises ValueError if a token is unknown to the grammar's terminals
        return False
    except Exception:
        # Be conservative: treat unexpected parser failures as unparseable
        return False

def read_tsv(input_tsv: str | Path) -> List[Tuple[str, int, List[str]]]:
    """
    Read the assignment TSV and return (id, ground_truth, pos_tokens).
    Expected columns: id, label, sentence, pos
    """
    rows: List[Tuple[str, int, List[str]]] = []
    with Path(input_tsv).open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f, delimiter="\t")
        required = {"id", "label", "sentence", "pos"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required TSV columns: {missing}")
        for r in reader:
            sent_id = str(r["id"]).strip()
            try:
                ground_truth = int(str(r["label"]).strip())
            except Exception:
                # Default to 0 if label is malformed
                ground_truth = 0
            pos_str = (r.get("pos") or "").strip()
            pos_tokens = pos_str.split() if pos_str else []
            rows.append((sent_id, ground_truth, pos_tokens))
    return rows

def parse_dataset(
    input_tsv: str | Path,
    grammar_path: str | Path,
) -> List[ParsedRow]:
    """
    High-level helper: load grammar, parse each example, and return ParsedRow objects.
    """
    grammar = load_cfg(grammar_path)
    parser = build_parser(grammar)
    data = read_tsv(input_tsv)

    results: List[ParsedRow] = []
    for sent_id, ground_truth, pos_tokens in data:
        parsed = try_parse_pos(parser, pos_tokens)
        results.append(ParsedRow(sent_id, ground_truth, pos_tokens, parsed))
    return results

# Optional quick smoke test (run: python -m src.grammar_checker path/to.tsv grammars/toy.cfg)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python -m src.grammar_checker <input.tsv> <grammar.cfg>")
        sys.exit(1)
    input_tsv, grammar_path = sys.argv[1], sys.argv[2]
    out = parse_dataset(input_tsv, grammar_path)
    # Print a tiny preview (first 5)
    for row in out[:5]:
        print(row.sent_id, "parsed=" + str(row.parsed), "labels_gt=" + str(row.ground_truth))
