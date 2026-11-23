"""pgvector store. Postgres runs in Docker (see docker-compose.yml); DSN via DATABASE_URL.

One table per mode (config.collection_name) so structure-aware vs fixed are A/B-comparable.
"""
from __future__ import annotations

from dataclasses import dataclass

import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .chunking.base import Chunk
from .config import DATABASE_URL


@dataclass
class Hit:
    score: float      # cosine similarity (1 - cosine distance)
    payload: dict


def client() -> psycopg.Connection:
    with psycopg.connect(DATABASE_URL, autocommit=True) as boot:
        boot.execute("CREATE EXTENSION IF NOT EXISTS vector")
    conn = psycopg.connect(DATABASE_URL, autocommit=True)
    register_vector(conn)
    return conn


def recreate(c: psycopg.Connection, name: str, dim: int) -> None:
    c.execute(f'DROP TABLE IF EXISTS "{name}"')
    c.execute(f"""CREATE TABLE "{name}" (
        id          text PRIMARY KEY,
        doc_id      text NOT NULL,
        chunk_index integer NOT NULL,
        text        text NOT NULL,
        metadata    jsonb NOT NULL,
        embedding   vector({int(dim)}) NOT NULL
    )""")
    c.execute(f'CREATE INDEX ON "{name}" (doc_id)')
    c.execute(f'CREATE INDEX ON "{name}" USING hnsw (embedding vector_cosine_ops)')


def upsert(c: psycopg.Connection, name: str, chunks: list[Chunk], vectors: list[list[float]], batch: int = 128) -> None:
    sql = f"""INSERT INTO "{name}" (id, doc_id, chunk_index, text, metadata, embedding)
              VALUES (%s, %s, %s, %s, %s, %s)
              ON CONFLICT (id) DO UPDATE SET doc_id = EXCLUDED.doc_id, chunk_index = EXCLUDED.chunk_index,
                  text = EXCLUDED.text, metadata = EXCLUDED.metadata, embedding = EXCLUDED.embedding"""
    with c.cursor() as cur:
        for i in range(0, len(chunks), batch):
            cur.executemany(sql, [
                (ch.chunk_id, ch.doc_id, ch.index, ch.text, Jsonb(ch.metadata), Vector(v))
                for ch, v in zip(chunks[i:i + batch], vectors[i:i + batch])
            ])


def search(c: psycopg.Connection, name: str, vector: list[float], k: int = 5, doc_id: str | None = None) -> list[Hit]:
    where = "WHERE doc_id = %(doc)s" if doc_id else ""
    rows = c.execute(
        f"""SELECT 1 - (embedding <=> %(v)s::vector) AS score, text, chunk_index, metadata
            FROM "{name}" {where} ORDER BY embedding <=> %(v)s::vector LIMIT %(k)s""",
        {"v": Vector(vector), "k": k, "doc": doc_id},
    ).fetchall()
    return [Hit(score, {**meta, "text": text, "chunk_index": idx}) for score, text, idx, meta in rows]
