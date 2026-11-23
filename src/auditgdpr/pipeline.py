"""Ingestion pipeline:  PDF -> sections -> chunks -> (embeddings) -> local Qdrant.

The `structure_aware` flag swaps the chunking stage only; everything else is identical,
so the two collections (gdpr_structure_aware / gdpr_fixed) are directly comparable.
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass

from . import config, corpus, store
from .chunking import fixed, guidance, legal, structure_aware
from .chunking.base import Chunk
from .chunking.tokens import Tok
from .extract import extract


@dataclass
class Result:
    chunks: list[Chunk]
    collection: str
    seconds: float


def build_chunks(structure_aware_flag: bool, model: str, only: str | None = None, log=print) -> list[Chunk]:
    tok = Tok(model)
    chunks: list[Chunk] = []
    for doc in corpus.discover():
        if only and only not in doc.doc_id:
            continue
        segs, body = extract(doc.path, drop_small=doc.profile != "legal_act")
        if structure_aware_flag:
            sections = legal.parse(segs) if doc.profile == "legal_act" else guidance.parse(segs, body)
            doc_chunks = structure_aware.chunk_document(
                doc, sections, tok, config.MAX_CHUNK_TOKENS, config.MIN_SECTION_TOKENS, config.OVERLAP_TOKENS)
        else:
            segs, _ = extract(doc.path, drop_small=True)
            doc_chunks = fixed.chunk_document(doc, segs, tok, config.FIXED_CHUNK_TOKENS, config.OVERLAP_TOKENS)
        for c in doc_chunks:               # make indices global-unique per collection
            c.metadata["doc_chunk_index"] = c.index
        log(f"  {doc.doc_id:<75} {len(doc_chunks):>4} chunks")
        chunks += doc_chunks
    return chunks


def export(chunks: list[Chunk], structure_aware_flag: bool) -> str:
    config.EXPORT_DIR.mkdir(exist_ok=True)
    path = config.EXPORT_DIR / f"chunks_{'structure_aware' if structure_aware_flag else 'fixed'}.jsonl"
    with open(path, "w") as f:
        for c in chunks:
            f.write(json.dumps({"id": c.chunk_id, "text": c.text, "embed_text": c.embed_text, **c.metadata}, ensure_ascii=False) + "\n")
    return str(path)


def run(structure_aware_flag: bool, model: str = config.EMBED_MODEL, device: str = "auto",
        only: str | None = None, dry_run: bool = False, log=print) -> Result:
    t0 = time.time()
    name = config.collection_name(structure_aware_flag)
    log(f"[1/3] chunking  mode={'structure-aware' if structure_aware_flag else 'fixed-window'}")
    chunks = build_chunks(structure_aware_flag, model, only, log)
    log(f"      -> {len(chunks)} chunks, exported to {export(chunks, structure_aware_flag)}")
    if dry_run:
        return Result(chunks, name, time.time() - t0)

    from .embed import Embedder
    log(f"[2/3] embedding model={model}")
    emb = Embedder(model, device)
    log(f"      device={emb.device} dim={emb.dim}")
    vectors = emb.embed_documents([c.embed_text for c in chunks])

    log(f"[3/3] upserting into Qdrant collection '{name}' ({config.QDRANT_URL})")
    c = store.client()
    store.recreate(c, name, emb.dim)
    store.upsert(c, name, chunks, vectors)
    c.close()
    return Result(chunks, name, time.time() - t0)
