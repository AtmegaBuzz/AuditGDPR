"""auditgdpr CLI.

  auditgdpr ingest --structure-aware        # structure-aware chunking (headers + metadata)
  auditgdpr ingest                          # baseline fixed-window chunking
  auditgdpr search "72 hours breach" --structure-aware
"""
from __future__ import annotations

import typer

from . import config

app = typer.Typer(add_completion=False, help="GDPR RAG ingestion pipeline")


@app.command()
def ingest(
    structure_aware: bool = typer.Option(False, "--structure-aware", help="Chunk along document structure; prepend content headers; attach hierarchy metadata."),
    model: str = typer.Option(config.EMBED_MODEL, help="BAAI embedding model (sentence-transformers id)."),
    device: str = typer.Option("auto", help="auto | mps | cpu"),
    only: str = typer.Option(None, help="Only docs whose id contains this substring."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Chunk + export JSONL only; skip embedding and Qdrant."),
):
    from .pipeline import run
    r = run(structure_aware, model, device, only, dry_run)
    sizes = sorted(c.metadata["token_count"] for c in r.chunks)
    typer.echo(f"\ndone in {r.seconds:.0f}s | {len(r.chunks)} chunks | tokens min/median/max = "
               f"{sizes[0]}/{sizes[len(sizes)//2]}/{sizes[-1]} | collection={r.collection}{' (dry run)' if dry_run else ''}")


@app.command()
def search(
    query: str,
    structure_aware: bool = typer.Option(False, "--structure-aware", help="Search the structure-aware collection."),
    k: int = 5,
    model: str = typer.Option(config.EMBED_MODEL),
    device: str = "auto",
):
    from . import store
    from .embed import Embedder
    emb = Embedder(model, device)
    c = store.client()
    for h in store.search(c, config.collection_name(structure_aware), emb.embed_query(query), k):
        p = h.payload
        where = " > ".join(p["section_path"]) if p.get("section_path") else "(no structure)"
        typer.echo(f"\n{h.score:.3f}  {p['title']}  p.{p['page_start']}-{p['page_end']}\n       {where}\n       {p['text'][:240]!r}")


if __name__ == "__main__":
    app()
