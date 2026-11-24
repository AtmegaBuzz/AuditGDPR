"""Golden-set evaluation of the retrieval stack: does the gold chunk appear in the top-k, and how high?"""
from __future__ import annotations

import json
from pathlib import Path

from .rag import Rag

CONFIGS = [("dense", dict(mode="dense", rerank=False)), ("bm25", dict(mode="bm25", rerank=False)),
           ("hybrid (RRF)", dict(mode="hybrid", rerank=False)), ("hybrid + rerank", dict(mode="hybrid", rerank=True))]


def run(path: Path, role: str, k: int, limit: int, log=print) -> dict:
    qs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
    qs = [q for q in qs if q.get("gold_chunk_ids")]                      # unanswerable questions have no gold chunk
    qs = qs[:limit] if limit else qs
    rag, out = Rag(), {}
    log(f"{len(qs)} answerable questions, role={role}, k={k}")
    for label, kw in CONFIGS:
        hit = rr = 0.0
        for q in qs:
            ids = rag.retrieve(q["question"], role, k, **kw).stages["final"]
            gold = set(q["gold_chunk_ids"])
            ranks = [i for i, c in enumerate(ids, 1) if c in gold]
            hit += bool(ranks)
            rr += 1 / ranks[0] if ranks else 0
        out[label] = {"recall@k": hit / len(qs), "mrr": rr / len(qs)}
        log(f"  {label:<18} recall@{k} = {hit / len(qs):.3f}   MRR = {rr / len(qs):.3f}")
    return out
