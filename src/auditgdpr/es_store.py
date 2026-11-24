"""Elasticsearch store: BM25 (lexical) + dense kNN over the same chunks, fused client-side with RRF.

Postgres stays the system of record for ingest state (and keeps its RLS); Elasticsearch is the retrieval index.

Access control is enforced by Elasticsearch itself, not by the caller:
  * one FILTERED ALIAS per clearance level:  <index>__clr<N>  ->  access_level <= N
  * one read-only ROLE per level that may only read that alias (never the index), one USER per role
  * retrieval authenticates as the user for the caller's role, so a bug or prompt-injection upstream cannot widen the filter.
Unknown role -> ValueError (fail closed). Every hit is additionally re-checked in Python (defence in depth).
"""
from __future__ import annotations

from elasticsearch import Elasticsearch, NotFoundError
from elasticsearch.helpers import bulk

from . import config
from .chunking.base import Chunk
from .store import Hit, clearance_for

LEVELS = sorted(set(config.ROLES.values()))


def alias(name: str, level: int) -> str:
    return f"{name}__clr{level}"


def reader_user(level: int) -> str:
    return f"es_reader_{level}"


def client() -> Elasticsearch:
    """Admin connection (ingest / sync / setup)."""
    return Elasticsearch(config.ES_URL, basic_auth=("elastic", config.ELASTIC_PASSWORD), request_timeout=60)


def reader_client(role: str) -> Elasticsearch:
    """Connection that can only read the alias for `role`'s clearance."""
    return Elasticsearch(config.ES_URL, basic_auth=(reader_user(clearance_for(role)), config.ES_READER_PASSWORD), request_timeout=60)


def search_text(text: str, metadata: dict) -> str:
    """What BM25 indexes: the structural header (doc title + chapter/article) plus the body."""
    h = metadata.get("header")
    return f"{h}\n{text}" if h else text


def ensure(es: Elasticsearch, name: str, dim: int) -> None:
    """Idempotent: index + mapping, per-clearance aliases, read-only roles and users. Never drops data."""
    if not es.indices.exists(index=name):
        es.indices.create(index=name, settings={"number_of_shards": 1, "number_of_replicas": 0}, mappings={
            "dynamic": "strict",
            "properties": {
                "doc_id": {"type": "keyword"},
                "chunk_index": {"type": "integer"},
                "access_level": {"type": "byte"},
                "text": {"type": "text", "index": False},                       # display only
                "search_text": {"type": "text", "analyzer": "english"},         # BM25
                "metadata": {"type": "object", "enabled": False},               # returned as-is, not indexed
                "embedding": {"type": "dense_vector", "dims": int(dim), "index": True, "similarity": "cosine"},
            },
        })
    for lvl in LEVELS:
        a = alias(name, lvl)
        es.indices.put_alias(index=name, name=a, filter={"range": {"access_level": {"lte": lvl}}})
        es.security.put_role(name=f"auditgdpr_clr{lvl}", indices=[{"names": [a], "privileges": ["read"]}])
        es.security.put_user(username=reader_user(lvl), password=config.ES_READER_PASSWORD, roles=[f"auditgdpr_clr{lvl}"])


def _action(index: str, ch_id: str, doc_id: str, idx: int, text: str, meta: dict, vec: list[float], level: int) -> dict:
    return {"_op_type": "index", "_index": index, "_id": ch_id, "_source": {
        "doc_id": doc_id, "chunk_index": idx, "access_level": int(level), "text": text,
        "search_text": search_text(text, meta), "metadata": meta, "embedding": vec}}


def replace_doc(es: Elasticsearch, name: str, doc_id: str, chunks: list[Chunk], vectors: list[list[float]]) -> None:
    delete_docs(es, name, [doc_id])
    bulk(es, [_action(name, c.chunk_id, c.doc_id, c.index, c.text, c.metadata, v, c.metadata["access_level"])
              for c, v in zip(chunks, vectors)], refresh=True)


def delete_docs(es: Elasticsearch, name: str, doc_ids: list[str]) -> None:
    try:
        es.delete_by_query(index=name, query={"terms": {"doc_id": doc_ids}}, refresh=True, conflicts="proceed")
    except NotFoundError:
        pass


def sync_from_pg(es: Elasticsearch, pg, name: str, dim: int, log=print) -> int:
    """Backfill / repair: copy every chunk (with its stored embedding) from Postgres into Elasticsearch. No re-embedding."""
    ensure(es, name, dim)
    present = {r[0] for r in pg.execute(f'SELECT DISTINCT doc_id FROM "{name}"').fetchall()}
    stale = {b["key"] for b in es.search(index=name, size=0, aggs={"d": {"terms": {"field": "doc_id", "size": 10000}}})
             ["aggregations"]["d"]["buckets"]} - present
    if stale:
        delete_docs(es, name, sorted(stale))
        log(f"  removed {len(stale)} stale docs from ES")

    def gen():
        with pg.transaction(), pg.cursor(name="es_sync") as cur:        # named (streaming) cursors need a transaction
            cur.execute(f'SELECT id, doc_id, chunk_index, text, metadata, embedding, access_level FROM "{name}"')
            for i, d, idx, text, meta, emb, lvl in cur:
                yield _action(name, i, d, idx, text, meta, emb.to_list(), lvl)
    ok, _ = bulk(es, gen(), chunk_size=200, refresh=True)
    return ok


def _hits(resp: dict, clearance: int) -> list[Hit]:
    out = []
    for h in resp["hits"]["hits"]:
        s = h["_source"]
        if s["access_level"] > clearance:                       # should be impossible (alias filter); never trust a single layer
            raise PermissionError(f"chunk {h['_id']} above clearance {clearance} was returned by Elasticsearch")
        out.append(Hit(h["_score"], {**s["metadata"], "text": s["text"], "chunk_index": s["chunk_index"], "chunk_id": h["_id"]}))
    return out


def search_dense(es: Elasticsearch, name: str, role: str, vector: list[float], k: int, doc_id: str | None = None) -> list[Hit]:
    lvl = clearance_for(role)
    knn = {"field": "embedding", "query_vector": vector, "k": k, "num_candidates": max(200, k * 5),
           "filter": [{"range": {"access_level": {"lte": lvl}}}] + ([{"term": {"doc_id": doc_id}}] if doc_id else [])}
    return _hits(es.search(index=alias(name, lvl), knn=knn, size=k, source_excludes=["embedding", "search_text"]), lvl)


def search_bm25(es: Elasticsearch, name: str, role: str, query: str, k: int, doc_id: str | None = None) -> list[Hit]:
    lvl = clearance_for(role)
    q = {"bool": {"must": [{"match": {"search_text": query}}],
                  "filter": [{"range": {"access_level": {"lte": lvl}}}] + ([{"term": {"doc_id": doc_id}}] if doc_id else [])}}
    return _hits(es.search(index=alias(name, lvl), query=q, size=k, source_excludes=["embedding", "search_text"]), lvl)


def rrf(rankings: list[list[Hit]], c: int = config.RRF_C, limit: int | None = None) -> list[Hit]:
    """Reciprocal rank fusion. Score = sum over lists of 1/(c + rank). Returns Hits whose .score is the fused score."""
    score: dict[str, float] = {}
    keep: dict[str, Hit] = {}
    for hits in rankings:
        for r, h in enumerate(hits, 1):
            cid = h.payload["chunk_id"]
            score[cid] = score.get(cid, 0.0) + 1.0 / (c + r)
            keep.setdefault(cid, h)
    ordered = sorted(score, key=score.get, reverse=True)[:limit]
    return [Hit(score[i], keep[i].payload) for i in ordered]
