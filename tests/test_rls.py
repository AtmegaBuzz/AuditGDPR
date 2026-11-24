"""Row-level-security tests against the live pgvector database (run `auditgdpr ingest` for both data/ and data/acme first).

  uv run python tests/test_rls.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import psycopg                       # noqa: E402

from auditgdpr import config, store  # noqa: E402

T = config.collection_name(True)


def _admin_vec(level: int) -> tuple[str, list[float]]:
    """A real stored chunk's own embedding at `level` -> querying with it must rank that chunk first (if visible)."""
    a = store.client()
    cid, emb = a.execute(f'SELECT id, embedding FROM "{T}" WHERE access_level = %s LIMIT 1', (level,)).fetchone()
    a.close()
    return cid, emb.to_list()


def test_no_leak_above_clearance():
    r = store.reader_client()
    for level in (1, 2):
        cid, vec = _admin_vec(level)
        for role, clr in config.ROLES.items():
            hits = store.search(r, T, vec, 50, role=role)
            assert hits, f"{role} got nothing"
            assert all(h.payload["access_level"] <= clr for h in hits), f"{role} saw a row above clearance {clr}"
            ids = {h.payload["chunk_index"] for h in hits}  # noqa: F841
            top = hits[0]
            if clr >= level:
                assert top.score > 0.99, f"{role} (clearance {clr}) should find the level-{level} chunk itself"
            else:
                assert top.score < 0.99, f"{role} must not see the level-{level} chunk"


def test_visible_counts_match_policy():
    a, r = store.client(), store.reader_client()
    total = {l: n for l, n in a.execute(f'SELECT access_level, count(*) FROM "{T}" GROUP BY 1')}
    for role, clr in config.ROLES.items():
        with r.transaction():
            r.execute("SELECT set_config('app.clearance', %s, true)", (str(clr),))
            seen = r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0]
        assert seen == sum(n for l, n in total.items() if l <= clr), (role, seen, total)


def test_fail_closed_when_clearance_unset_or_garbage():
    r = store.reader_client()
    assert r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0] == 0, "no clearance set must mean no rows"
    with r.transaction():
        r.execute("SELECT set_config('app.clearance', '', true)")
        assert r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0] == 0
    with r.transaction():
        r.execute("SELECT set_config('app.clearance', '-1', true)")
        assert r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0] == 0


def test_clearance_does_not_leak_between_transactions():
    r = store.reader_client()
    with r.transaction():
        r.execute("SELECT set_config('app.clearance', '2', true)")
        assert r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0] > 0
    assert r.execute(f'SELECT count(*) FROM "{T}"').fetchone()[0] == 0, "clearance must be transaction-local"


def test_reader_is_read_only_and_cannot_see_ingest_state():
    r = store.reader_client()
    for stmt in (f'DELETE FROM "{T}"', f'UPDATE "{T}" SET access_level = 0', "SELECT * FROM ingest_state"):
        try:
            r.execute(stmt)
        except psycopg.errors.InsufficientPrivilege:
            continue
        raise AssertionError(f"reader should be denied: {stmt}")


def test_search_refuses_a_bypassing_connection():
    a = store.client()
    try:
        store.search(a, T, [0.0] * config.EMBED_DIM, 1, role="compliance_director")
    except PermissionError:
        return
    raise AssertionError("search must refuse a superuser / BYPASSRLS connection")


def test_unknown_role_rejected():
    try:
        store.search(store.reader_client(), T, [0.0] * config.EMBED_DIM, 1, role="ceo")
    except ValueError:
        return
    raise AssertionError("unknown role must be rejected")


def test_every_row_labelled_consistently():
    a = store.client()
    bad = a.execute(f"""SELECT count(*) FROM "{T}" WHERE access_level <> (metadata->>'access_level')::int
                         OR metadata->>'classification' <> CASE access_level WHEN 0 THEN 'public' WHEN 1 THEN 'internal' ELSE 'confidential' END""").fetchone()[0]
    assert bad == 0, f"{bad} rows where the column and the metadata disagree"


if __name__ == "__main__":
    fails = 0
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            try:
                fn(); print("ok  ", name)
            except Exception as e:                       # noqa: BLE001
                fails += 1; print("FAIL", name, "-", repr(e))
    sys.exit(1 if fails else 0)
