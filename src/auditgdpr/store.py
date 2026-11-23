"""Qdrant client. The server runs in Docker (see docker-compose.yml); URL via QDRANT_URL."""
from __future__ import annotations

from qdrant_client import QdrantClient, models

from .chunking.base import Chunk
from .config import QDRANT_URL


def client() -> QdrantClient:
    return QdrantClient(url=QDRANT_URL)


def recreate(c: QdrantClient, name: str, dim: int) -> None:
    if c.collection_exists(name):
        c.delete_collection(name)
    c.create_collection(name, vectors_config=models.VectorParams(size=dim, distance=models.Distance.COSINE))


def upsert(c: QdrantClient, name: str, chunks: list[Chunk], vectors: list[list[float]], batch: int = 128) -> None:
    for i in range(0, len(chunks), batch):
        c.upsert(name, points=[
            models.PointStruct(id=ch.chunk_id, vector=v, payload={**ch.metadata, "text": ch.text, "chunk_index": ch.index})
            for ch, v in zip(chunks[i:i + batch], vectors[i:i + batch])
        ])


def search(c: QdrantClient, name: str, vector: list[float], k: int = 5, doc_id: str | None = None):
    flt = models.Filter(must=[models.FieldCondition(key="doc_id", match=models.MatchValue(value=doc_id))]) if doc_id else None
    return c.query_points(name, query=vector, limit=k, query_filter=flt, with_payload=True).points
