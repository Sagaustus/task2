# src/evaluation.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple

@dataclass
class Confusion:
    tp: int
    fp: int
    fn: int
    tn: int

def confusion_from_pairs(pairs: Iterable[Tuple[int, int]]) -> Confusion:
    """
    Build confusion counts from (ground_truth, prediction) pairs.
    Convention (per assignment):
      ground_truth: 1 = ungrammatical, 0 = grammatical
      prediction:   1 = has grammar errors (parse failed)
                    0 = no errors (parse succeeded)
    """
    tp = fp = fn = tn = 0
    for gt, pred in pairs:
        if pred == 1 and gt == 1:
            tp += 1
        elif pred == 1 and gt == 0:
            fp += 1
        elif pred == 0 and gt == 1:
            fn += 1
        else:  # pred == 0 and gt == 0
            tn += 1
    return Confusion(tp, fp, fn, tn)

def precision_recall(conf: Confusion) -> Tuple[float, float]:
    """
    Precision = TP / (TP + FP)
    Recall    = TP / (TP + FN)
    Returns (precision, recall) with safe zero-division.
    """
    prec = conf.tp / (conf.tp + conf.fp) if (conf.tp + conf.fp) > 0 else 0.0
    rec  = conf.tp / (conf.tp + conf.fn) if (conf.tp + conf.fn) > 0 else 0.0
    return prec, rec

def format_summary(conf: Confusion) -> str:
    prec, rec = precision_recall(conf)
    lines = [
        "Evaluation (Grammar Checker)",
        "----------------------------",
        f"TP: {conf.tp}   FP: {conf.fp}   FN: {conf.fn}   TN: {conf.tn}",
        f"Precision: {prec:.4f}",
        f"Recall:    {rec:.4f}",
    ]
    return "\n".join(lines)
