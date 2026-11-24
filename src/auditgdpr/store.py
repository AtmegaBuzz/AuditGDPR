"""pgvector store. Postgres runs in Docker (see docker-compose.yml); DSN via DATABASE_URL.

One table per mode (config.collection_name) so structure-aware vs fixed are A/B-comparable.
"""
from __future__ import annotations

from dataclasses import dataclass

import psycopg
from psycopg import sql
from pgvector import Vector
from pgvector.psycopg import register_vector
from psycopg.types.json import Jsonb

from .chunking.base import Chunk
from .config import DATABASE_URL, READER_DATABASE_URL, READER_ROLE, READER_PASSWORD, ROLES


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


def reader_client() -> psycopg.Connection:
    """Connection for retrieval: logs in as the unprivileged reader role, so row-level security is enforced."""
    conn = psycopg.connect(READER_DATABASE_URL, autocommit=True)
    register_vector(conn)
    return conn


def ensure(c: psycopg.Connection, name: str, dim: int) -> None:
    """Create the chunk table, the ingest-state table, the reader role and the RLS policy (idempotent; never drops data).

    Row-level security:
      * access_level (0 public / 1 internal / 2 confidential) is a real column, NOT NULL, DEFAULT 2 -> unlabeled rows are confidential.
      * policy: a row is visible iff access_level <= the session's `app.clearance`. Unset/garbled clearance -> no rows (fail closed).
      * FORCE ROW LEVEL SECURITY applies it even to the table owner; the reader role has SELECT only, and no access to ingest_state.
    """
    c.execute(f"""CREATE TABLE IF NOT EXISTS "{name}" (
        id           text PRIMARY KEY,
        doc_id       text NOT NULL,
        chunk_index  integer NOT NULL,
        text         text NOT NULL,
        metadata     jsonb NOT NULL,
        embedding    vector({int(dim)}) NOT NULL,
        access_level smallint NOT NULL DEFAULT 2 CHECK (access_level BETWEEN 0 AND 2)
    )""")
    c.execute(f'ALTER TABLE "{name}" ADD COLUMN IF NOT EXISTS access_level smallint NOT NULL DEFAULT 2 CHECK (access_level BETWEEN 0 AND 2)')
    c.execute(f'CREATE INDEX IF NOT EXISTS "{name}_doc_id_idx" ON "{name}" (doc_id)')
    c.execute(f'CREATE INDEX IF NOT EXISTS "{name}_level_idx" ON "{name}" (access_level)')
    c.execute(f'CREATE INDEX IF NOT EXISTS "{name}_emb_idx" ON "{name}" USING hnsw (embedding vector_cosine_ops)')
    c.execute("""CREATE TABLE IF NOT EXISTS ingest_state (
        collection  text NOT NULL,
        doc_id      text NOT NULL,
        fingerprint text NOT NULL,
        n_chunks    integer NOT NULL,
        updated_at  timestamptz NOT NULL DEFAULT now(),
        PRIMARY KEY (collection, doc_id)
    )""")
    c.execute("ALTER TABLE ingest_state ADD COLUMN IF NOT EXISTS source text")

    role = sql.Identifier(READER_ROLE)
    if not c.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (READER_ROLE,)).fetchone():
        c.execute(sql.SQL("CREATE ROLE {} LOGIN PASSWORD {} NOSUPERUSER NOBYPASSRLS NOCREATEDB NOCREATEROLE")
                  .format(role, sql.Literal(READER_PASSWORD)))
    c.execute(sql.SQL("GRANT CONNECT ON DATABASE {} TO {}").format(
        sql.Identifier(c.info.dbname), role))
    tbl = sql.Identifier(name)
    c.execute(sql.SQL("REVOKE ALL ON {} FROM {}").format(tbl, role))
    c.execute(sql.SQL("GRANT SELECT ON {} TO {}").format(tbl, role))
    c.execute(sql.SQL("ALTER TABLE {} ENABLE ROW LEVEL SECURITY").format(tbl))
    c.execute(sql.SQL("ALTER TABLE {} FORCE ROW LEVEL SECURITY").format(tbl))
    c.execute(sql.SQL("DROP POLICY IF EXISTS clearance_read ON {}").format(tbl))
    c.execute(sql.SQL("""CREATE POLICY clearance_read ON {} FOR SELECT
        USING (access_level <= COALESCE(NULLIF(current_setting('app.clearance', true), '')::int, -1))""").format(tbl))


def load_state(c: psycopg.Connection, name: str) -> dict[str, tuple[str, int, str | None]]:
    """doc_id -> (fingerprint, n_chunks, source path) recorded at the last successful ingest."""
    rows = c.execute("SELECT doc_id, fingerprint, n_chunks, source FROM ingest_state WHERE collection = %s", (name,)).fetchall()
    return {d: (f, n, src) for d, f, n, src in rows}


def stored_counts(c: psycopg.Connection, name: str) -> dict[str, int]:
    return dict(c.execute(f'SELECT doc_id, count(*) FROM "{name}" GROUP BY doc_id').fetchall())


def replace_doc(c: psycopg.Connection, name: str, doc_id: str, fingerprint: str,
                chunks: list[Chunk], vectors: list[list[float]], source: str | None = None) -> None:
    """Atomically swap one document's chunks and record its fingerprint (all-or-nothing per document)."""
    with c.transaction():
        c.execute(f'DELETE FROM "{name}" WHERE doc_id = %s', (doc_id,))
        upsert(c, name, chunks, vectors)
        c.execute("""INSERT INTO ingest_state (collection, doc_id, fingerprint, n_chunks, source) VALUES (%s, %s, %s, %s, %s)
                     ON CONFLICT (collection, doc_id) DO UPDATE SET fingerprint = EXCLUDED.fingerprint,
                         n_chunks = EXCLUDED.n_chunks, source = EXCLUDED.source, updated_at = now()""",
                  (name, doc_id, fingerprint, len(chunks), source))


def delete_docs(c: psycopg.Connection, name: str, doc_ids: list[str]) -> None:
    with c.transaction():
        c.execute(f'DELETE FROM "{name}" WHERE doc_id = ANY(%s)', (doc_ids,))
        c.execute("DELETE FROM ingest_state WHERE collection = %s AND doc_id = ANY(%s)", (name, doc_ids))


def recreate(c: psycopg.Connection, name: str, dim: int) -> None:
    c.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(name)))
    c.execute("DELETE FROM ingest_state WHERE collection = %s", (name,)) if _has_state(c) else None
    ensure(c, name, dim)


def upsert(c: psycopg.Connection, name: str, chunks: list[Chunk], vectors: list[list[float]], batch: int = 128) -> None:
    sql = f"""INSERT INTO "{name}" (id, doc_id, chunk_index, text, metadata, embedding, access_level)
              VALUES (%s, %s, %s, %s, %s, %s, %s)
              ON CONFLICT (id) DO UPDATE SET doc_id = EXCLUDED.doc_id, chunk_index = EXCLUDED.chunk_index,
                  text = EXCLUDED.text, metadata = EXCLUDED.metadata, embedding = EXCLUDED.embedding,
                  access_level = EXCLUDED.access_level"""
    with c.cursor() as cur:
        for i in range(0, len(chunks), batch):
            cur.executemany(sql, [
                (ch.chunk_id, ch.doc_id, ch.index, ch.text, Jsonb(ch.metadata), Vector(v), int(ch.metadata["access_level"]))
                for ch, v in zip(chunks[i:i + batch], vectors[i:i + batch])
            ])


def _has_state(c: psycopg.Connection) -> bool:
    return c.execute("SELECT to_regclass('ingest_state')").fetchone()[0] is not None


def clearance_for(role: str) -> int:
    if role not in ROLES:
        raise ValueError(f"unknown role {role!r}; expected one of {sorted(ROLES)}")
    return ROLES[role]


def search(c: psycopg.Connection, name: str, vector: list[float], k: int = 5, *, role: str, doc_id: str | None = None) -> list[Hit]:
    """Nearest-neighbour search as `role`. Visibility is decided by Postgres (RLS) BEFORE anything reaches the caller,
    so nothing above the role's clearance can ever be retrieved, ranked, or passed to an LLM."""
    clearance = clearance_for(role)
    priv = c.execute("SELECT rolsuper OR rolbypassrls FROM pg_roles WHERE rolname = current_user").fetchone()[0]
    if priv:
        raise PermissionError("refusing to search over a connection that bypasses row-level security; use store.reader_client()")
    where = "WHERE doc_id = %(doc)s" if doc_id else ""
    with c.transaction():
        c.execute("SELECT set_config('app.clearance', %s, true)", (str(clearance),))      # transaction-local
        c.execute("SET LOCAL hnsw.iterative_scan = relaxed_order")        # keep scanning the index until k visible rows are found
        rows = c.execute(
            f"""SELECT 1 - (embedding <=> %(v)s::vector) AS score, text, chunk_index, metadata
                FROM "{name}" {where} ORDER BY embedding <=> %(v)s::vector LIMIT %(k)s""",
            {"v": Vector(vector), "k": k, "doc": doc_id},
        ).fetchall()
    return [Hit(score, {**meta, "text": text, "chunk_index": idx}) for score, text, idx, meta in rows]
