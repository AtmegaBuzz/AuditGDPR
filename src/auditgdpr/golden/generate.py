"""Golden-set generation: sample chunks -> LLM writes Q/A -> LLM judge filters -> JSONL.

Record types
  single        answerable from one chunk
  multi         needs 2-3 chunks (same doc, or same-category cross-doc)
  unanswerable  plausible GDPR question the corpus does NOT answer (tests refusal)
"""
from __future__ import annotations

import hashlib
import json
import math
import threading
import random
import re
from difflib import SequenceMatcher
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

from .. import config
from ..chunking.base import Chunk
from . import prompts as P
from .cloudflare import WorkersAI

MIN_CHUNK_TOKENS = 80
MIN_PER_DOC = 3
OVERGENERATE = 1.3           # judge drops some; generate extra then trim to --size

DIFFICULTY_MIX = ["easy"] * 3 + ["medium"] * 4 + ["hard"] * 3


def _section(c: Chunk) -> str:
    return " > ".join(c.metadata.get("section_path") or []) or "(no section)"


def _ctx(chunks: list[Chunk]) -> str:
    return "\n\n".join(f'PASSAGE [{i+1}]\n  document: {c.metadata.get("title")}\n  section: {_section(c)}\n"""\n{c.text}\n"""'
                       for i, c in enumerate(chunks))


def _usable(c: Chunk) -> bool:
    t = c.text
    alpha = sum(ch.isalpha() for ch in t) / max(1, len(t))
    return c.metadata.get("token_count", 0) >= MIN_CHUNK_TOKENS and alpha > 0.7


def allocate(by_doc: dict[str, list[Chunk]], total: int) -> dict[str, int]:
    """sqrt-proportional allocation with a per-doc floor, so the GDPR text doesn't swamp 16 guideline docs."""
    w = {d: math.sqrt(len(cs)) for d, cs in by_doc.items()}
    s = sum(w.values())
    return {d: max(MIN_PER_DOC, round(total * w[d] / s)) for d in by_doc}


def _plan(chunks: list[Chunk], size: int, rng: random.Random, answerable_only_multi_share=0.25, unans_share=0.10):
    usable = [c for c in chunks if _usable(c)]
    by_doc: dict[str, list[Chunk]] = defaultdict(list)
    for c in usable:
        by_doc[c.doc_id].append(c)
    target = int(size * OVERGENERATE)
    n_unans = round(target * unans_share)
    n_multi = round(target * answerable_only_multi_share)
    n_single = target - n_unans - n_multi

    tasks: list[dict] = []
    for doc, k in allocate(by_doc, n_single).items():
        for c in rng.sample(by_doc[doc], min(k, len(by_doc[doc]))):
            tasks.append({"type": "single", "chunks": [c]})
    cats: dict[str, list[str]] = defaultdict(list)
    for d, cs in by_doc.items():
        cats[cs[0].metadata.get("category")].append(d)
    docs = list(by_doc)
    for i in range(n_multi):
        anchor = rng.choice(by_doc[rng.choice(docs)])
        peers = [c for c in by_doc[anchor.doc_id] if abs(c.index - anchor.index) <= 15 and c.chunk_id != anchor.chunk_id]
        if i % 3 == 2:     # cross-doc within the same topical category
            other_docs = [d for d in cats[anchor.metadata.get("category")] if d != anchor.doc_id]
            peers = by_doc[rng.choice(other_docs)] if other_docs else peers
        if peers:
            tasks.append({"type": "multi", "chunks": [anchor, rng.choice(peers)]})
    seeds = rng.sample(usable, min(n_unans, len(usable)))
    for c in seeds:
        tasks.append({"type": "unanswerable", "chunks": [c]})
    styles = list(P.STYLES)
    for i, t in enumerate(tasks):      # round-robin styles + angles so the set is diverse by construction
        t["style"] = styles[(i + rng.randrange(len(styles))) % len(styles)]
        t["difficulty"] = rng.choice(DIFFICULTY_MIX)
        t["angle"] = P.UNANS_ANGLES[i % len(P.UNANS_ANGLES)]
    return tasks


_canon = lambda s: re.sub(r"\s+", " ", s.lower().replace("\u2019", "'").replace("\u2018", "'")
                          .replace("\u201c", '"').replace("\u201d", '"').replace("\u2013", "-").replace("\u2014", "-")
                          .replace("-\n", "")).strip()


def _evidence_ok(quotes: list[str], chunks: list[Chunk], need_each: bool) -> tuple[bool, list[int]]:
    """Every quote must appear (near-)verbatim in some chunk; for multi items each needed chunk must be quoted.
    Returns (ok, index of the chunk each quote was found in, -1 if not found)."""
    texts = [_canon(c.text) for c in chunks]
    where = []
    for q in quotes:
        cq, hit = _canon(q), -1
        for i, t in enumerate(texts):
            if cq and cq in t:
                hit = i
                break
            m = SequenceMatcher(None, t, cq, autojunk=False).find_longest_match(0, len(t), 0, len(cq))
            if cq and m.size >= 0.9 * len(cq):     # tolerate PDF hyphenation / spacing noise
                hit = i
                break
        where.append(hit)
    ok = bool(quotes) and all(w >= 0 for w in where)
    if need_each:
        ok = ok and len({w for w in where if w >= 0}) >= 2
    return ok, where


def _generate(ai: WorkersAI, t: dict) -> dict:
    chunks: list[Chunk] = t["chunks"]
    style = t["style"]
    if t["type"] == "single":
        c = chunks[0]
        user = P.SINGLE_USER.format(title=c.metadata.get("title"), section=_section(c), context=c.text,
                                    style_name=style, style_desc=P.STYLES[style], difficulty=t["difficulty"])
        return ai.chat_json(P.GEN_SYSTEM, user, P.QA_SCHEMA, max_tokens=900, temperature=0.5)
    if t["type"] == "multi":
        user = P.MULTI_USER.format(n=len(chunks), context=_ctx(chunks), style_name=style, style_desc=P.STYLES[style])
        return ai.chat_json(P.GEN_SYSTEM, user, P.QA_SCHEMA, max_tokens=1100, temperature=0.5)
    c = chunks[0]
    user = P.UNANS_USER.format(title=c.metadata.get("title"), section=_section(c), excerpt=c.text[:1200], angle=t["angle"])
    return ai.chat_json(P.UNANS_SYSTEM, user, P.QA_SCHEMA, max_tokens=500, temperature=0.8)


def _judge(ai: WorkersAI, kind: str, chunks: list[Chunk], q: str, a: str) -> dict:
    if kind == "unanswerable":
        user = P.JUDGE_UNANSWERABLE_USER.format(context=_ctx(chunks), question=q, answer=a)
    else:
        crit = P.JUDGE_MULTI_CRITERION if kind == "multi" else P.JUDGE_SINGLE_CRITERION
        user = P.JUDGE_ANSWERABLE_USER.format(context=_ctx(chunks), kind=kind, question=q, answer=a, multi_criterion=crit)
    return ai.chat_json(P.JUDGE_SYSTEM, user, P.JUDGE_SCHEMA, max_tokens=400, temperature=0)


def _run_task(ai: WorkersAI, t: dict) -> dict | None:
    chunks: list[Chunk] = t["chunks"]
    kind = t["type"]
    qa = _generate(ai, t)
    q, a = (qa.get("question") or "").strip(), (qa.get("answer") or "").strip()
    if qa.get("skip") or not q or not a:
        return None
    evidence = [e for e in (qa.get("evidence") or []) if e.strip()]
    gold = chunks
    if kind == "multi" and qa.get("passages_used"):
        used = [chunks[i - 1] for i in qa["passages_used"] if isinstance(i, int) and 1 <= i <= len(chunks)]
        gold = used if len(used) >= 2 else chunks
    rec = {"type": kind, "question": q, "reference_answer": None if kind == "unanswerable" else a,
           "out_of_scope_reason": a if kind == "unanswerable" else None,
           "question_style": qa.get("question_style") or t["style"], "difficulty": qa.get("difficulty") or t["difficulty"],
           "evidence": [] if kind == "unanswerable" else evidence,
           "gold_chunk_ids": [] if kind == "unanswerable" else [c.chunk_id for c in gold],
           "gold_doc_ids": [] if kind == "unanswerable" else sorted({c.doc_id for c in gold}),
           "gold_access_level": None if kind == "unanswerable" else max(c.metadata.get("access_level", 0) for c in gold),
           "gold_classification": None if kind == "unanswerable" else [c.metadata.get("classification", "public") for c in gold],
           "gold_sections": [] if kind == "unanswerable" else [c.metadata.get("section_path") for c in gold],
           "gold_pages": [] if kind == "unanswerable" else [[c.metadata.get("page_start"), c.metadata.get("page_end")] for c in gold],
           "seed_chunk_ids": [c.chunk_id for c in chunks]}
    if kind != "unanswerable":
        ok, where = _evidence_ok(evidence, chunks, need_each=(kind == "multi"))
        rec["evidence_verified"] = ok
        if not ok:   # cheap hallucination filter: skip the judge call entirely
            rec["judge"], rec["accepted"] = {"reason": f"evidence not found verbatim in context (matches={where})"}, False
            return rec
    j = _judge(ai, kind, chunks, q, a)
    rec["judge"] = j
    rec["accepted"] = bool(j.get("self_contained") and j.get("grounded") and j.get("non_trivial")
                           and j.get("unambiguous") and j.get("requires_multiple")
                           and int(j.get("quality") or 0) >= P.MIN_QUALITY)
    return rec


_norm = lambda s: set(re.findall(r"[a-z0-9]+", s.lower()))


def _dedupe(recs: list[dict], thresh: float = 0.75) -> list[dict]:
    kept: list[dict] = []
    toks: list[set] = []
    for r in recs:
        t = _norm(r["question"])
        if any(len(t & o) / max(1, len(t | o)) >= thresh for o in toks):
            r["accepted"] = False
            r["judge"] = {**r.get("judge", {}), "reason": "near-duplicate question"}
            continue
        kept.append(r)
        toks.append(t)
    return kept


def journal_path(structure_aware: bool):
    return config.GOLDEN_DIR / f".progress_{'structure_aware' if structure_aware else 'fixed'}.jsonl"


def _signature(chunks: list[Chunk], size: int, model: str, seed: int, structure_aware: bool) -> str:
    """Identity of a run. The plan is deterministic given this, so task index i means the same task on every resume."""
    h = hashlib.sha256(json.dumps([size, model, seed, structure_aware, P.__dict__.get("PROMPT_VERSION", 0)]).encode())
    for c in sorted(chunks, key=lambda c: c.chunk_id):
        h.update(c.chunk_id.encode())
    return h.hexdigest()[:16]


def pending_run(structure_aware: bool) -> tuple[int, int, int] | None:
    """(tasks finished, tasks planned, requested size) of an interrupted run, or None."""
    p = journal_path(structure_aware)
    if not p.exists():
        return None
    try:
        lines = [json.loads(l) for l in p.read_text().splitlines() if l.strip()]
        return len(lines) - 1, lines[0]["planned"], lines[0]["size"]
    except Exception:
        return None


def run(chunks: list[Chunk], size: int, model: str, structure_aware: bool, seed: int = 42,
        concurrency: int = 8, log=print, resume: bool = True) -> dict:
    """Resumable: every finished task (kept, rejected or skipped by the model) is appended to a journal as it completes.
    If the run dies (network, Ctrl-C, crash), call run() again with the same settings and only the unfinished tasks are
    redone. Tasks whose API call raised are NOT journaled, so they are retried. The journal is deleted on success;
    changing size/model/seed/corpus starts fresh automatically."""
    rng = random.Random(seed)
    ai = WorkersAI(model)
    tasks = _plan(chunks, size, rng)
    sig = _signature(chunks, size, model, seed, structure_aware)
    jp = journal_path(structure_aware)
    jp.parent.mkdir(parents=True, exist_ok=True)
    done: dict[int, dict | None] = {}
    if resume and jp.exists():
        try:
            lines = [json.loads(l) for l in jp.read_text().splitlines() if l.strip()]
            if lines and lines[0].get("sig") == sig:
                done = {x["i"]: x["rec"] for x in lines[1:]}
                log(f"[golden] resuming: {len(done)}/{len(tasks)} tasks already finished")
            else:
                log("[golden] found a journal from different settings; starting fresh")
        except (json.JSONDecodeError, KeyError):
            log("[golden] unreadable journal; starting fresh")
    if not done:
        jp.write_text(json.dumps({"sig": sig, "planned": len(tasks), "size": size}) + "\n")
    lock = threading.Lock()
    jf = open(jp, "a", buffering=1)

    def work(i: int, t: dict):
        rec = _run_task(ai, t)
        with lock:
            jf.write(json.dumps({"i": i, "rec": rec}, ensure_ascii=False) + "\n")
        return i, rec
    log(f"[golden] model={model} planned {len(tasks)} candidates "
        f"(single={sum(t['type']=='single' for t in tasks)}, multi={sum(t['type']=='multi' for t in tasks)}, "
        f"unanswerable={sum(t['type']=='unanswerable' for t in tasks)})")
    results: list[dict] = [r for r in done.values() if r]
    failed = 0
    todo = [(i, t) for i, t in enumerate(tasks) if i not in done]
    ex = ThreadPoolExecutor(concurrency)
    try:
        futs = [ex.submit(work, i, t) for i, t in todo]
        for n, f in enumerate(as_completed(futs), 1):
            try:
                _, r = f.result()
                if r:
                    results.append(r)
            except Exception as e:   # one bad call must not kill a long run; it is retried on the next resume
                failed += 1
                log(f"  ! task failed (will be retried on resume): {e}")
            if n % 20 == 0:
                log(f"  {len(done) + n}/{len(tasks)} done")
    except KeyboardInterrupt:
        ex.shutdown(wait=False, cancel_futures=True)
        jf.close()
        log(f"\n[golden] interrupted - progress saved. Run again to resume ({jp.name}).")
        raise
    finally:
        ex.shutdown(wait=True)
        jf.close()
    if failed:
        log(f"[golden] {failed} task(s) failed and are not in the journal. Run again to retry just those; "
            f"nothing was written to the golden set yet.")
        return {"path": None, "rejected_path": None, "accepted": 0, "rejected": 0, "failed_calls": failed,
                "by_type": {}, "incomplete": True}
    results.sort(key=lambda r: (r["type"], r["seed_chunk_ids"]))
    accepted = _dedupe([r for r in results if r["accepted"]])
    accepted = [r for r in accepted if r["accepted"]]
    rng.shuffle(accepted)
    accepted = _trim(accepted, size)
    if len(accepted) < size:
        log(f"  ! only {len(accepted)} items survived filtering (wanted {size}); rerun with a larger --size or another --seed")
    rejected = [r for r in results if r not in accepted]
    for n, r in enumerate(accepted, 1):
        r["id"] = f"g{n:04d}"
    config.GOLDEN_DIR.mkdir(parents=True, exist_ok=True)
    tag = "structure_aware" if structure_aware else "fixed"
    out, rej = config.GOLDEN_DIR / f"golden_{tag}.jsonl", config.GOLDEN_DIR / f"golden_{tag}.rejected.jsonl"
    for path, rows in ((out, accepted), (rej, rejected)):
        with open(path, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
    jp.unlink(missing_ok=True)                       # finished cleanly: next "generate" starts fresh
    by_type = {k: sum(r["type"] == k for r in accepted) for k in ("single", "multi", "unanswerable")}
    return {"path": str(out), "rejected_path": str(rej), "accepted": len(accepted), "rejected": len(rejected),
            "failed_calls": failed, "by_type": by_type}


def _trim(accepted: list[dict], size: int) -> list[dict]:
    """Trim to `size` preserving the single/multi/unanswerable mix (65/25/10)."""
    quota = {"single": round(size * 0.65), "multi": round(size * 0.25)}
    quota["unanswerable"] = size - quota["single"] - quota["multi"]
    out = []
    for k, q in quota.items():
        out += [r for r in accepted if r["type"] == k][:q]
    spare = [r for r in accepted if r not in out and r["type"] != "unanswerable"]   # backfill short buckets
    return out + spare[:max(0, size - len(out))]
