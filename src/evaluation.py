# src/evaluation.py
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Tuple, Dict, Any
import json
from pathlib import Path

@dataclass
class Confusion:
    tp: int
    fp: int
    fn: int
    tn: int

def confusion_from_pairs(pairs: Iterable[Tuple[int, int]]) -> Confusion:
    tp = fp = fn = tn = 0
    for gt, pred in pairs:
        if pred == 1 and gt == 1:
            tp += 1
        elif pred == 1 and gt == 0:
            fp += 1
        elif pred == 0 and gt == 1:
            fn += 1
        else:
            tn += 1
    return Confusion(tp, fp, fn, tn)

def precision_recall(conf: Confusion) -> Tuple[float, float]:
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

def metrics_dict(conf: Confusion) -> Dict[str, Any]:
    prec, rec = precision_recall(conf)
    d: Dict[str, Any] = asdict(conf)
    d.update({
        "precision": prec,
        "recall": rec,
    })
    return d

def save_metrics_json(path: str | Path, conf: Confusion) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(metrics_dict(conf), f, indent=2)

def save_metrics_text(path: str | Path, conf: Confusion) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        f.write(format_summary(conf) + "\n")
