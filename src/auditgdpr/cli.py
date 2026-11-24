"""auditgdpr CLI.

  auditgdpr ingest                          # structure-aware chunking (default; headers + metadata)
  auditgdpr ingest --root data -x acme      # choose root + excluded folders (default: data, excl. acme)
  auditgdpr ingest --force                  # re-chunk + re-embed everything (default is incremental: only new/changed PDFs)
  auditgdpr ingest --fixed                  # baseline fixed-window chunking
  auditgdpr search "72 hours breach"        # add --fixed to query the baseline collection
  auditgdpr golden --size 200   # golden eval set via Cloudflare Workers AI
  auditgdpr                                 # interactive menu (golden set / company docs)
  auditgdpr synth plan | bible | docs | validate | bakeoff   # synthetic Acme Corp company corpus (see `synth --help`)
"""
from __future__ import annotations

from pathlib import Path

import typer

from . import config

app = typer.Typer(add_completion=False, help="GDPR RAG ingestion pipeline")
synth_app = typer.Typer(add_completion=False, help="Generate the synthetic Acme Corp public/internal/confidential corpus with Cloudflare Workers AI")
app.add_typer(synth_app, name="synth")


def _setup_dev_logging() -> None:
    """--dev: short coloured one-liners on the console (INFO+); everything incl. raw responses goes to logs/dev.log."""
    import logging
    import sys

    colors = {logging.DEBUG: "2", logging.INFO: "36", logging.WARNING: "33", logging.ERROR: "1;31"}

    class Pretty(logging.Formatter):
        def format(self, r):
            msg = r.getMessage()
            if not sys.stderr.isatty():
                return f"{self.formatTime(r, '%H:%M:%S')} {msg}"
            c = colors.get(r.levelno, "0")
            if msg.startswith("ok "):
                c = "32"
            return f"\033[2m{self.formatTime(r, '%H:%M:%S')}\033[0m \033[{c}m{msg}\033[0m"

    (config.ROOT / "logs").mkdir(exist_ok=True)
    root = logging.getLogger("auditgdpr")
    root.setLevel(logging.DEBUG)
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(Pretty())
    file = logging.FileHandler(config.ROOT / "logs" / "dev.log")
    file.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s", "%H:%M:%S"))
    root.addHandler(console)
    root.addHandler(file)
    root.info("dev mode: short log here, full detail in logs/dev.log")


@app.callback(invoke_without_command=True)
def _default(ctx: typer.Context, dev: bool = typer.Option(False, "--dev", help="Developer mode: verbose debug logs (LLM requests, raw responses, retries) to stderr and logs/dev.log.")):
    """Run with no arguments for the interactive menu."""
    if dev:
        _setup_dev_logging()
    if ctx.invoked_subcommand is None:
        from .menu import main_menu
        main_menu()


@app.command()
def menu():
    """Interactive menu: generate the golden set or the Acme company documents (asks before overwriting)."""
    from .menu import main_menu
    main_menu()


@app.command()
def ingest(
    structure_aware: bool = typer.Option(True, "--structure-aware/--fixed", help="Structure-aware chunking (default): chunk along document structure; prepend content headers; attach hierarchy metadata."),
    model: str = typer.Option(config.EMBED_MODEL, help="BAAI embedding model (sentence-transformers id)."),
    device: str = typer.Option("auto", help="auto | mps | cpu"),
    only: str = typer.Option(None, help="Only docs whose id contains this substring."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Chunk + export JSONL only; skip embedding and database."),
    force: bool = typer.Option(False, "--force", help="Re-chunk and re-embed every document (drops and rebuilds the table)."),
    prune: bool = typer.Option(False, "--prune", help="Also delete stored documents that are no longer found under --root."),
    es: bool = typer.Option(True, "--es/--no-es", help="Also index into Elasticsearch (hybrid retrieval). Use `es-sync` to backfill existing pgvector data."),
    root: Path = typer.Option(config.DATA_DIR, "--root", help="Root folder to search for PDFs."),
    exclude: list[str] = typer.Option(list(config.DEFAULT_EXCLUDE), "--exclude", "-x",
                                      help="Folder (name or path relative to --root) to skip; never descended into. Repeatable."),
):
    """Chunk every PDF under --root (skipping --exclude folders), embed, and store."""
    from .pipeline import run
    if not root.is_dir():
        raise typer.BadParameter(f"root folder not found: {root}", param_hint="--root")
    r = run(structure_aware, model, device, only, dry_run, root=root, exclude=exclude, force=force, prune=prune, es=es)
    sizes = sorted(c.metadata["token_count"] for c in r.chunks)
    stats = f" | tokens min/median/max = {sizes[0]}/{sizes[len(sizes)//2]}/{sizes[-1]}" if sizes else ""
    typer.echo(f"\ndone in {r.seconds:.0f}s | {len(r.chunks)} chunks processed{stats} | docs: {len(r.new)} new, "
               f"{len(r.changed)} changed, {len(r.unchanged)} unchanged | collection={r.collection}{' (dry run)' if dry_run else ''}")


def _print_hits(hits, role: str) -> None:
    for h in hits:
        p = h.payload
        where = " > ".join(p["section_path"]) if p.get("section_path") else "(no structure)"
        typer.echo(f"\n{h.score:.3f}  [{p.get('classification', '?')}] {p['title']}  p.{p['page_start']}-{p['page_end']}\n"
                   f"       {where}\n       {p['text'][:240]!r}")


@app.command()
def search(
    query: str,
    role: str = typer.Option(config.DEFAULT_ROLE, "--role", "-r", help=f"Who is asking: {' | '.join(config.ROLES)}. Row-level security hides everything above this role's clearance."),
    structure_aware: bool = typer.Option(True, "--structure-aware/--fixed", help="Search the structure-aware collection (default) or the fixed-window baseline."),
    k: int = 5,
    model: str = typer.Option(config.EMBED_MODEL),
    device: str = "auto",
):
    """Retrieve as a given user role (default: intern, the least privileged)."""
    from . import store
    from .embed import Embedder
    if role not in config.ROLES:
        raise typer.BadParameter(f"must be one of: {', '.join(config.ROLES)}", param_hint="--role")
    emb = Embedder(model, device)
    c = store.reader_client()
    _print_hits(store.search(c, config.collection_name(structure_aware), emb.embed_query(query), k, role=role), role)


@app.command("es-sync")
def es_sync(structure_aware: bool = typer.Option(True, "--structure-aware/--fixed")):
    """Create the Elasticsearch index/aliases/reader users and copy all chunks + embeddings from pgvector (no re-embedding)."""
    from . import es_store, store
    name = config.collection_name(structure_aware)
    n = es_store.sync_from_pg(es_store.client(), store.client(), name, config.EMBED_DIM, typer.echo)
    typer.echo(f"indexed {n} chunks into Elasticsearch index {name}")


def _print_final(hits) -> None:
    from .rag import cite
    for i, h in enumerate(hits, 1):
        typer.echo(f"\n[{i}] {h.score:.3f}  {cite(h)}\n    {h.payload['text'][:240]!r}")


@app.command()
def retrieve(
    query: str,
    role: str = typer.Option(config.DEFAULT_ROLE, "--role", "-r"),
    k: int = typer.Option(6, "--k", "-k"),
    mode: str = typer.Option("hybrid", help="hybrid | dense | bm25"),
    rerank: bool = typer.Option(True, "--rerank/--no-rerank"),
):
    """Hybrid retrieval (dense + BM25 -> RRF -> cross-encoder rerank) as a role."""
    from .rag import Rag
    _print_final(Rag().retrieve(query, role, k, mode=mode, rerank=rerank).hits)


@app.command()
def ask(
    query: str,
    role: str = typer.Option(config.DEFAULT_ROLE, "--role", "-r"),
    k: int = typer.Option(6, "--k", "-k"),
    mode: str = typer.Option("hybrid", help="hybrid | dense | bm25"),
    rerank: bool = typer.Option(True, "--rerank/--no-rerank"),
):
    """Full RAG: retrieve + rerank + cited answer (Cloudflare Workers AI). Abstains when evidence is weak."""
    from .rag import Rag
    r = Rag().answer(query, role, k, mode=mode, rerank=rerank)
    typer.echo(f"\n{r['answer']}\n\n(best rerank score {r['best_score']:.3f}{', abstained' if r['abstained'] else ''})\nSources:")
    _print_final(r["sources"])


@app.command("eval")
def eval_cmd(
    golden_path: Path = typer.Option(config.GOLDEN_DIR / "golden_structure_aware.jsonl", "--golden"),
    role: str = typer.Option("compliance_director", "--role", help="Role to evaluate as; needs clearance for the gold chunks."),
    k: int = 5,
    limit: int = typer.Option(0, help="Only the first N questions (0 = all)."),
):
    """recall@k / MRR on the golden set for: dense, bm25, hybrid, hybrid+rerank."""
    from .evaluate import run
    run(golden_path, role, k, limit, typer.echo)


@app.command("access-demo")
def access_demo(
    query: str = typer.Argument("What is our company's procedure when a customer requests deletion of their personal data?"),
    k: int = 5,
    model: str = typer.Option(config.EMBED_MODEL),
    device: str = "auto",
):
    """Run ONE query as every role and show that each gets different permissible evidence."""
    from . import store
    from .embed import Embedder
    emb = Embedder(model, device)
    vec = emb.embed_query(query)
    c = store.reader_client()
    name = config.collection_name(True)
    typer.echo(f"query: {query}")
    for role in config.ROLES:
        hits = store.search(c, name, vec, k, role=role)
        tiers = sorted({h.payload["classification"] for h in hits}, key=lambda t: list(config.TIERS.values()).index(t))
        typer.echo(f"\n=== {role} (clearance {config.ROLES[role]}) -> {len(hits)} hits, tiers seen: {tiers}")
        for h in hits:
            p = h.payload
            typer.echo(f"  {h.score:.3f} [{p['classification']:<12}] {p['doc_id']}: {(p['section_path'] or ['-'])[-1][:60]}")


@app.command()
def golden(
    structure_aware: bool = typer.Option(True, "--structure-aware/--fixed", help="Chunk like the structure-aware collection (gold chunk ids must match the collection you evaluate)."),
    size: int = typer.Option(200, help="Final golden-set size (65%% single, 25%% multi-chunk, 10%% unanswerable)."),
    cf_model: str = typer.Option(config.GOLDEN_MODEL, "--model", help="Workers AI model id used for generation and judging."),
    seed: int = typer.Option(42),
    concurrency: int = typer.Option(8),
    embed_model: str = typer.Option(config.EMBED_MODEL, help="Only used for the tokenizer, to reproduce chunking."),
    only: str = typer.Option(None, help="Only docs whose id contains this substring."),
    root: Path = typer.Option(config.DATA_DIR, "--root", help="Root folder to search (GDPR PDFs + Acme markdown)."),
    exclude: list[str] = typer.Option([], "--exclude", "-x", help="Folder to skip, e.g. -x acme for GDPR only. Repeatable."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show the sampling plan; make no API calls."),
    resume: bool = typer.Option(True, "--resume/--fresh", help="Continue an interrupted run with the same settings (default) or discard its progress."),
):
    """Generate a golden Q/A set with Cloudflare Workers AI (needs CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN)."""
    from .golden import generate
    from .pipeline import build_chunks
    chunks = build_chunks(structure_aware, embed_model, only, root=root, exclude=exclude)
    if dry_run:
        import random
        tasks = generate._plan(chunks, size, random.Random(seed))
        typer.echo(f"{len(tasks)} candidates planned for size={size}")
        return
    if not resume:
        generate.journal_path(structure_aware).unlink(missing_ok=True)
    r = generate.run(chunks, size, cf_model, structure_aware, seed, concurrency, typer.echo, resume=resume)
    if r.get("incomplete"):
        typer.echo("Incomplete: re-run the same command to retry only the failed tasks.")
        raise typer.Exit(1)
    typer.echo(f"\naccepted {r['accepted']} {r['by_type']} | rejected {r['rejected']} | failed calls {r['failed_calls']}"
               f"\n  {r['path']}\n  {r['rejected_path']}")


# ---------------------------------------------------------------------------------------------------
# synth: fictional company corpus for the role-based (public / internal / confidential) RAG
# ---------------------------------------------------------------------------------------------------
@synth_app.command("plan")
def synth_plan():
    """Show the document manifest in generation order (waves) with fact counts. No API calls."""
    from .synth import generate, world
    facts = world.load_bible() if world.bible_path().exists() else (world.load_bible(world.draft_path()) if world.draft_path().exists() else [])
    specs = world.load_manifest()
    for line in generate.plan(specs, facts):
        typer.echo(line)
    typer.echo(f"\n{len(specs)} docs, ~{sum(s.target_words for s in specs):,} target words; "
               f"{len(facts)} facts in {'frozen bible' if world.bible_path().exists() else 'draft' if facts else 'NO bible yet'}")


@synth_app.command("bible")
def synth_bible(
    model: str = typer.Option(config.SYNTH_WRITER_MODEL, help="Workers AI model for fact-sheet expansion."),
    topic: str = typer.Option(None, help="Only topics whose id contains this substring."),
    concurrency: int = typer.Option(4),
    freeze: bool = typer.Option(False, "--freeze", help="Promote the (reviewed/edited) draft to data/acme/bible.json."),
):
    """Stage 1: expand seeds.toml into the tier-tagged fact sheet. Review the draft, then --freeze."""
    from .synth import bible
    if freeze:
        bible.freeze(typer.echo)
        return
    r = bible.run(model, topic, concurrency=concurrency, log=typer.echo)
    typer.echo(f"api calls {r['api_calls']} | cache hits {r['cache_hits']}")


@synth_app.command("docs")
def synth_docs(
    tier: str = typer.Option(None, help="public | internal | confidential"),
    only: str = typer.Option(None, help="Comma-separated substrings of doc ids."),
    writer: str = typer.Option(config.SYNTH_WRITER_MODEL, help="Workers AI model that writes."),
    judge: str = typer.Option(config.SYNTH_JUDGE_MODEL, help="Workers AI model that audits (use a different family)."),
    force: bool = typer.Option(False, "--force", help="Regenerate docs that already exist."),
    concurrency: int = typer.Option(4),
    retries: int = typer.Option(2, help="Revision rounds per doc before it goes to needs_review."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Show what would be generated; no API calls."),
):
    """Stages 3-6: outline -> sections -> validate + judge -> revise -> data/acme/<tier>/<doc_id>.md"""
    from .synth import generate, world
    if tier and tier not in config.TIERS.values():
        raise typer.BadParameter("tier must be public, internal or confidential")
    if dry_run:
        facts = world.load_bible()
        chosen = {s.id for s in generate.select(world.load_manifest(), only, tier)}
        for line in generate.plan(world.load_manifest(), facts):
            if line.split()[3] in chosen:
                typer.echo(line)
        typer.echo(f"\n{len(chosen)} docs selected")
        return
    r = generate.run(only, tier, writer, judge, force, concurrency, retries, log=typer.echo)
    typer.echo(f"\n{r['by_status']} | writer calls {r['writer_calls']} (cache hits {r['writer_cache_hits']}) | judge calls {r['judge_calls']}"
               f"\nneeds_review: {config.SYNTH_DIR / 'needs_review'}")


@synth_app.command("validate")
def synth_validate(only: str = typer.Option(None, help="Substring of doc id.")):
    """Re-run the deterministic checks (leakage, ids, hygiene, structure) over data/acme/*. No API calls."""
    from .synth import world
    from .synth.validate import check
    from .synth.emit import parse_front_matter
    seeds, facts = world.load_seeds(), world.load_bible()
    specs = {s.id: s for s in world.load_manifest()}
    bad = n = 0
    for path in sorted(config.ACME_DIR.rglob("*.md")):
        meta, body = parse_front_matter(path.read_text())
        spec = specs.get(meta.get("doc_id", ""))
        if spec is None or (only and only not in spec.id):
            continue
        n += 1
        if meta["access_level"] != spec.tier or path.parent.name != config.TIERS[spec.tier]:
            typer.echo(f"{spec.id}: access_level/folder does not match manifest tier"); bad += 1
        parts = {"": body}
        issues = [i for i in check(spec, parts, facts, seeds, set(spec.related)) if i.severity == "error" and i.kind != "structure"]
        for i in issues:
            typer.echo(f"{spec.id}: {i.line()}")
        bad += bool(issues)
    typer.echo(f"\nchecked {n} docs, {bad} with errors")
    raise typer.Exit(1 if bad else 0)


@synth_app.command("bakeoff")
def synth_bakeoff(
    docs: str = typer.Option("INT-SOP-ERASE-002,CONF-MIN-BRD-2026Q2,PUB-NOTICE-001", help="Comma-separated doc ids (one per tier is ideal)."),
    models: str = typer.Option(",".join([config.SYNTH_WRITER_MODEL, config.SYNTH_JUDGE_MODEL, config.SYNTH_FALLBACK_MODEL]),
                               help="Comma-separated writer models to compare."),
    judge: str = typer.Option(config.SYNTH_JUDGE_MODEL),
    concurrency: int = typer.Option(3),
):
    """Generate the same docs with several writer models into artifacts/synth/bakeoff/<model>/ and compare judge scores."""
    from .synth import generate
    summary = []
    for m in models.split(","):
        slug = m.strip().replace("@cf/", "").replace("/", "_")
        typer.echo(f"\n=== writer {m} ===")
        r = generate.run(only=docs, writer_model=m.strip(), judge_model=judge, force=True, concurrency=concurrency,
                         retries=1, out_dir=config.SYNTH_DIR / "bakeoff" / slug, log=typer.echo)
        for x in r["results"]:
            sc = x.get("scores") or {}
            summary.append((m, x["id"], x["status"], x.get("attempts", "-"), x.get("words", "-"),
                            round(sum(sc.values()) / len(sc), 2) if sc else "-"))
    typer.echo("\nmodel | doc | status | attempts | words | mean judge score")
    for row in summary:
        typer.echo(" | ".join(str(c) for c in row))


if __name__ == "__main__":
    app()
