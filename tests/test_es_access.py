"""Clearance enforcement in Elasticsearch (run `auditgdpr es-sync` first):  uv run python tests/test_es_access.py"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from elasticsearch import AuthorizationException  # noqa: E402
from auditgdpr import config, es_store  # noqa: E402

N = config.collection_name(True)
Q = "How do we handle a customer erasure request, fines, incident post-incident review?"


def test_bm25_never_above_clearance():
    for role, clr in config.ROLES.items():
        hits = es_store.search_bm25(es_store.reader_client(role), N, role, Q, 50)
        assert hits and all(h.payload["access_level"] <= clr for h in hits), role


def test_reader_cannot_bypass_alias():
    es = es_store.reader_client("intern")
    for kw in ({"index": N}, {"index": es_store.alias(N, 2)}):
        try:
            es.search(index=kw["index"], query={"match_all": {}})
        except AuthorizationException:
            continue
        raise AssertionError(f"intern could read {kw['index']}")


def test_unfiltered_alias_query_still_clamped():
    es = es_store.reader_client("intern")
    r = es.search(index=es_store.alias(N, 0), query={"match_all": {}}, size=100, aggs={"l": {"max": {"field": "access_level"}}})
    assert r["aggregations"]["l"]["value"] == 0


def test_unknown_role_fails_closed():
    try:
        es_store.reader_client("hacker")
    except ValueError:
        return
    raise AssertionError


if __name__ == "__main__":
    for n, f in list(globals().items()):
        if n.startswith("test_"):
            f(); print("ok", n)
