"""RAG pipeline:  query -> [dense kNN  +  BM25] -> RRF fusion -> cross-encoder rerank -> cited answer.

Every stage runs as a given ROLE; Elasticsearch enforces clearance (see es_store), so nothing above the caller's
clearance can be retrieved, reranked or placed in the LLM prompt.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from . import config, es_store
from .store import Hit

SYSTEM = """You are a GDPR compliance assistant for Acme Corp. Answer ONLY from the numbered sources.
- Cite every claim with its source number in square brackets, e.g. [1] or [2][3].
- If the sources do not contain the answer, say exactly: "The available documents do not answer this." Do not use outside knowledge.
- Be concise and precise; quote article / paragraph numbers when the sources give them."""


@dataclass
class Retrieval:
    hits: list[Hit]                                  # final, reranked (or fused when rerank=False)
    stages: dict[str, list[str]] = field(default_factory=dict)   # stage -> chunk_ids in rank order (for eval / debugging)


class Rag:
    def __init__(self, collection: str | None = None, embed_model: str = config.EMBED_MODEL, device: str = "auto",
                 rerank_model: str = config.RERANK_MODEL):
        self.name = collection or config.collection_name(True)
        self._embed_model, self._device, self._rerank_model = embed_model, device, rerank_model
        self._emb = self._rr = None
        self._es: dict[str, object] = {}

    @property
    def emb(self):
        if self._emb is None:
            from .embed import Embedder
            self._emb = Embedder(self._embed_model, self._device)
        return self._emb

    @property
    def reranker(self):
        if self._rr is None:
            from .rerank import Reranker
            self._rr = Reranker(self._rerank_model, self._device)
        return self._rr

    def _client(self, role: str):
        if role not in self._es:
            self._es[role] = es_store.reader_client(role)
        return self._es[role]

    def retrieve(self, query: str, role: str = config.DEFAULT_ROLE, k: int = 6, *, mode: str = "hybrid",
                 rerank: bool = True, doc_id: str | None = None) -> Retrieval:
        """mode: hybrid | dense | bm25.  rerank=False returns the fused list (for A/B evaluation)."""
        es, st = self._client(role), {}
        lists = []
        if mode in ("hybrid", "dense"):
            d = es_store.search_dense(es, self.name, role, self.emb.embed_query(query), config.FETCH_K, doc_id)
            st["dense"] = [h.payload["chunk_id"] for h in d]; lists.append(d)
        if mode in ("hybrid", "bm25"):
            b = es_store.search_bm25(es, self.name, role, query, config.FETCH_K, doc_id)
            st["bm25"] = [h.payload["chunk_id"] for h in b]; lists.append(b)
        fused = es_store.rrf(lists, limit=config.FUSE_K)
        st["fused"] = [h.payload["chunk_id"] for h in fused]
        final = self.reranker.rerank(query, fused, k) if rerank else fused[:k]
        st["final"] = [h.payload["chunk_id"] for h in final]
        return Retrieval(final, st)

    def answer(self, query: str, role: str = config.DEFAULT_ROLE, k: int = 6, *, model: str = config.ANSWER_MODEL,
               min_score: float = config.MIN_RERANK_SCORE, **kw) -> dict:
        r = self.retrieve(query, role, k, **kw)
        best = r.hits[0].score if r.hits else 0.0
        if not r.hits or (kw.get("rerank", True) and best < min_score):
            return {"answer": "The available documents do not answer this.", "abstained": True, "sources": r.hits, "best_score": best}
        from .golden.cloudflare import WorkersAI, load_dotenv
        load_dotenv()
        ctx = "\n\n".join(f"[{i}] {cite(h)}\n{h.payload['text']}" for i, h in enumerate(r.hits, 1))
        text = WorkersAI(model).chat_text(SYSTEM, f"Sources:\n{ctx}\n\nQuestion: {query}", max_tokens=700, temperature=0.1)
        used = {int(n) for n in re.findall(r"\[(\d+)\]", text)}
        return {"answer": text.strip(), "abstained": False, "sources": r.hits, "cited": sorted(used), "best_score": best}


def cite(h: Hit) -> str:
    p = h.payload
    where = " > ".join(p["section_path"]) if p.get("section_path") else ""
    pages = f"p.{p['page_start']}" + (f"-{p['page_end']}" if p.get("page_end") != p.get("page_start") else "")
    return f"{p['title']} | {where} | {pages} | {p.get('classification', '?')}"
