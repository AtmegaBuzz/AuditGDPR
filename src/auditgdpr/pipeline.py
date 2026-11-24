"""Ingestion pipeline:  PDF -> sections -> chunks -> (embeddings) -> pgvector.

The `structure_aware` flag swaps the chunking stage only; everything else is identical,
so the two collections (gdpr_structure_aware / gdpr_fixed) are directly comparable.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from dataclasses import dataclass, field

from . import config, corpus, es_store, store
from .corpus import DocMeta
from .chunking import fixed, guidance, legal, markdown, structure_aware
from .chunking.base import Chunk
from .chunking.tokens import Tok
from .extract import extract


@dataclass
class Result:
    chunks: list[Chunk]          # chunks produced in THIS run (new/changed docs only on an incremental run)
    collection: str
    seconds: float
    new: list[str] = field(default_factory=list)
    changed: list[str] = field(default_factory=list)
    unchanged: list[str] = field(default_factory=list)
    removed: list[str] = field(default_factory=list)


def fingerprint(doc: DocMeta, structure_aware_flag: bool, model: str) -> str:
    """Identity of a document's stored chunks: PDF bytes + every setting that changes the chunks or vectors."""
    h = hashlib.sha256()
    with open(doc.path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    h.update(json.dumps([structure_aware_flag, model, config.PIPELINE_VERSION, config.MAX_CHUNK_TOKENS,
                         config.MIN_SECTION_TOKENS, config.OVERLAP_TOKENS, config.FIXED_CHUNK_TOKENS]).encode())
    return h.hexdigest()


def _chunk_markdown(doc: DocMeta, structure_aware_flag: bool, tok: Tok) -> list[Chunk]:
    from .extract import Seg
    from .synth.emit import parse_front_matter
    _, body = parse_front_matter(Path(doc.path).read_text(encoding="utf-8"))
    sections = markdown.parse(body)
    if structure_aware_flag:
        return structure_aware.chunk_document(
            doc, sections, tok, config.MAX_CHUNK_TOKENS, config.MIN_SECTION_TOKENS, config.OVERLAP_TOKENS)
    segs = [Seg(p.page, p.text, 0.0, False, 0) for sec in sections for p in sec.paras]
    return fixed.chunk_document(doc, segs, tok, config.FIXED_CHUNK_TOKENS, config.OVERLAP_TOKENS)


def chunk_doc(doc: DocMeta, structure_aware_flag: bool, tok: Tok) -> list[Chunk]:
    if doc.source_type == "markdown":
        doc_chunks = _chunk_markdown(doc, structure_aware_flag, tok)
        for c in doc_chunks:
            c.metadata["doc_chunk_index"] = c.index
        return doc_chunks
    segs, body = extract(doc.path, drop_small=doc.profile != "legal_act")
    if structure_aware_flag:
        sections = legal.parse(segs) if doc.profile == "legal_act" else guidance.parse(segs, body)
        doc_chunks = structure_aware.chunk_document(
            doc, sections, tok, config.MAX_CHUNK_TOKENS, config.MIN_SECTION_TOKENS, config.OVERLAP_TOKENS)
    else:
        segs, _ = extract(doc.path, drop_small=True)
        doc_chunks = fixed.chunk_document(doc, segs, tok, config.FIXED_CHUNK_TOKENS, config.OVERLAP_TOKENS)
    for c in doc_chunks:
        c.metadata["doc_chunk_index"] = c.index
    return doc_chunks


def _select(docs: list[DocMeta], only: str | None) -> list[DocMeta]:
    return [d for d in docs if not only or only in d.doc_id]


def build_chunks(structure_aware_flag: bool, model: str, only: str | None = None, log=print,
                 root: Path = config.DATA_DIR, exclude=config.DEFAULT_EXCLUDE) -> list[Chunk]:
    """Chunk every document (no database involved). Used by dry runs and the golden-set generator."""
    tok = Tok(model)
    chunks: list[Chunk] = []
    for doc in _select(corpus.discover(root, exclude), only):
        doc_chunks = chunk_doc(doc, structure_aware_flag, tok)
        log(f"  {doc.doc_id:<75} {len(doc_chunks):>4} chunks")
        chunks += doc_chunks
    return chunks


def export(chunks: list[Chunk], structure_aware_flag: bool, replace_docs: set[str] | None = None) -> str:
    """Write the JSONL dump. With `replace_docs`, merge: keep lines of other docs, replace those docs' lines."""
    config.EXPORT_DIR.mkdir(exist_ok=True)
    path = config.EXPORT_DIR / f"chunks_{'structure_aware' if structure_aware_flag else 'fixed'}.jsonl"
    kept: list[str] = []
    if replace_docs is not None and path.exists():
        kept = [ln for ln in path.read_text().splitlines() if ln and json.loads(ln).get("doc_id") not in replace_docs]
    lines = kept + [json.dumps({"id": c.chunk_id, "text": c.text, "embed_text": c.embed_text, **c.metadata}, ensure_ascii=False)
                    for c in chunks]
    path.write_text("\n".join(lines) + ("\n" if lines else ""))
    return str(path)


def run(structure_aware_flag: bool, model: str = config.EMBED_MODEL, device: str = "auto",
        only: str | None = None, dry_run: bool = False, log=print,
        root: Path = config.DATA_DIR, exclude=config.DEFAULT_EXCLUDE,
        force: bool = False, prune: bool = False, es: bool = True) -> Result:
    """Incremental ingest. A document is skipped when the database already holds it with the same fingerprint
    (PDF content + chunking/embedding settings) and the expected number of chunks.
    force=True re-ingests everything; prune=True deletes stored docs that are no longer found under root."""
    t0 = time.time()
    name = config.collection_name(structure_aware_flag)
    mode = "structure-aware" if structure_aware_flag else "fixed-window"
    docs = _select(corpus.discover(root, exclude), only)

    if dry_run:
        log(f"[dry run] chunking  mode={mode}")
        chunks = build_chunks(structure_aware_flag, model, only, log, root, exclude)
        log(f"      -> {len(chunks)} chunks, exported to {export(chunks, structure_aware_flag, {d.doc_id for d in docs})}")
        return Result(chunks, name, time.time() - t0, new=[d.doc_id for d in docs])

    c = store.client()
    store.ensure(c, name, config.EMBED_DIM)
    ec = es_store.client() if es else None          # Elasticsearch retrieval index (BM25 + kNN), written alongside pgvector
    if ec is not None and force:
        ec.indices.delete(index=name, ignore_unavailable=True)
    if ec is not None:
        es_store.ensure(ec, name, config.EMBED_DIM)
    if force:
        store.recreate(c, name, config.EMBED_DIM)
    state, counts = ({}, {}) if force else (store.load_state(c, name), store.stored_counts(c, name))

    todo: list[tuple[DocMeta, str]] = []
    res = Result([], name, 0.0)
    for d in docs:
        fp = fingerprint(d, structure_aware_flag, model)
        old = state.get(d.doc_id)
        if old is None:
            res.new.append(d.doc_id); todo.append((d, fp))
        elif old[0] != fp or counts.get(d.doc_id, 0) != old[1]:     # content/settings changed, or rows went missing
            res.changed.append(d.doc_id); todo.append((d, fp))
        else:
            res.unchanged.append(d.doc_id)
    if prune and not only:
        found = {d.doc_id for d in docs}
        under = str(Path(root).resolve()) + "/"          # only docs that were ingested from this root can be pruned
        res.removed = sorted(i for i, (_, _, src) in state.items() if i not in found and (src or "").startswith(under))
    log(f"[plan] mode={mode}  new={len(res.new)} changed={len(res.changed)} unchanged={len(res.unchanged)}"
        f"{f' removed={len(res.removed)}' if prune else ''}")
    for label, ids in (("new", res.new), ("changed", res.changed), ("unchanged (skipped)", res.unchanged), ("removed", res.removed)):
        for i in ids:
            log(f"   {label:<20} {i}")
    if res.removed:
        store.delete_docs(c, name, res.removed)
        if ec is not None:
            es_store.delete_docs(ec, name, res.removed)
    if not todo:
        log("      nothing to do — everything is already chunked and stored")
        if res.removed:
            export([], structure_aware_flag, set(res.removed))
        c.close()
        res.seconds = time.time() - t0
        return res

    tok = Tok(model)
    from .embed import Embedder
    emb = Embedder(model, device)
    log(f"[embed] model={model} device={emb.device} dim={emb.dim}")
    for n, (d, fp) in enumerate(todo, 1):
        doc_chunks = chunk_doc(d, structure_aware_flag, tok)
        vectors = emb.embed_documents([ch.embed_text for ch in doc_chunks], progress=False)
        if ec is not None:
            es_store.replace_doc(ec, name, d.doc_id, doc_chunks, vectors)           # ES first: if it fails, PG state is not advanced -> retried
        store.replace_doc(c, name, d.doc_id, fp, doc_chunks, vectors, d.path)      # committed per document: an interrupted run resumes
        res.chunks += doc_chunks
        log(f"  [{n}/{len(todo)}] {d.doc_id:<70} {len(doc_chunks):>4} chunks stored")
    log(f"      exported to {export(res.chunks, structure_aware_flag, {d.doc_id for d, _ in todo} | set(res.removed))}")
    c.close()
    res.seconds = time.time() - t0
    return res
