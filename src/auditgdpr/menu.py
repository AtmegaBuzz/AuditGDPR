"""Interactive menu: `auditgdpr` (no arguments) or `auditgdpr menu`.

  1) Generate golden evaluation set      (Cloudflare Workers AI)
  2) Generate Acme company documents     (fact sheet -> public / internal / confidential docs)
  3) Exit

Before generating, the menu checks whether output already exists. If it does you choose: generate new (deletes the
existing output first) or exit back to the menu.
"""
from __future__ import annotations

import os
import shutil
from pathlib import Path

import typer

from . import config


# --------------------------------------------------------------------------------------------------
# State detection + deletion (pure functions; the menu below only wires prompts to them)
# --------------------------------------------------------------------------------------------------
def company_status() -> dict:
    from .synth import world
    docs = sorted(config.ACME_DIR.rglob("*.md")) if config.ACME_DIR.exists() else []
    review = sorted((config.SYNTH_DIR / "needs_review").glob("*.md")) if (config.SYNTH_DIR / "needs_review").exists() else []
    cache = list((config.SYNTH_DIR / "cache").glob("*.json")) if (config.SYNTH_DIR / "cache").exists() else []
    try:
        expected = len(world.load_manifest())
    except Exception:
        expected = 0
    return {"docs": len(docs), "expected": expected, "bible": world.bible_path().exists(), "needs_review": len(review),
            "cache": len(cache), "exists": bool(docs or world.bible_path().exists() or cache or review)}


def company_paths() -> list[Path]:
    return [p for p in (config.ACME_DIR, config.SYNTH_DIR) if p.exists()]


def golden_paths(structure_aware: bool) -> list[Path]:
    tag = "structure_aware" if structure_aware else "fixed"
    return [p for p in (config.GOLDEN_DIR / f"golden_{tag}.jsonl", config.GOLDEN_DIR / f"golden_{tag}.rejected.jsonl") if p.exists()]


def golden_count(structure_aware: bool) -> int:
    p = config.GOLDEN_DIR / f"golden_{'structure_aware' if structure_aware else 'fixed'}.jsonl"
    return sum(1 for _ in open(p)) if p.exists() else 0


def _safe_delete(paths: list[Path]) -> None:
    root = config.ROOT.resolve()
    for p in paths:
        rp = p.resolve()
        if root not in rp.parents:                      # never delete anything outside the repo
            raise RuntimeError(f"refusing to delete {rp}: outside {root}")
        shutil.rmtree(rp) if rp.is_dir() else rp.unlink()


def _have_credentials() -> bool:
    from .golden.cloudflare import load_dotenv
    load_dotenv()
    return bool(os.environ.get("CLOUDFLARE_ACCOUNT_ID") and os.environ.get("CLOUDFLARE_API_TOKEN"))


def _choose(title: str, options: list[str]) -> int:
    typer.echo(f"\n{title}")
    for i, o in enumerate(options, 1):
        typer.echo(f"  {i}) {o}")
    while True:
        raw = typer.prompt("Choose", default="1" if len(options) == 1 else None).strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return int(raw)
        typer.echo(f"  enter a number 1-{len(options)}")


def _rel(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(config.ROOT.resolve()))
    except ValueError:
        return str(p)


# --------------------------------------------------------------------------------------------------
# Actions
# --------------------------------------------------------------------------------------------------
def run_company_docs() -> None:
    st = company_status()
    resume = False
    if st["exists"]:
        typer.echo(f"\nCompany documents already exist: {st['docs']}/{st['expected']} docs, fact sheet "
                   f"{'frozen' if st['bible'] else 'missing'}, {st['needs_review']} awaiting review, {st['cache']} cached LLM calls.")
        partial = not (st["bible"] and st["docs"] >= st["expected"])
        opts = ["Generate new (deletes everything above, then regenerates)", "Exit"]
        if partial:
            opts.insert(1, "Continue (reuse everything already generated, only do what is missing)")
        pick = _choose("What now?", opts)
        if opts[pick - 1] == "Exit":
            return
        if opts[pick - 1].startswith("Continue"):
            resume = True
        else:
            targets = company_paths()
            typer.echo("This will delete:\n" + "\n".join(f"  - {_rel(p)}" for p in targets))
            if not typer.confirm("Delete and regenerate?", default=False):
                return
            _safe_delete(targets)
            typer.echo("deleted.")
    if not _have_credentials():
        typer.echo("\nSet CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN (env or .env) first.")
        return

    from .synth import bible, generate
    if not resume or not st["bible"]:
        typer.echo("\n[1/3] Building the fact sheet (one call per topic)...")
        bible.run(config.SYNTH_WRITER_MODEL, log=typer.echo)
        typer.echo(f"\nThe fact sheet is the single source of truth for every document. Review or edit it now if you want:\n  {_rel(bible.world.draft_path())}")
        if not typer.confirm("Continue to document generation?", default=True):
            typer.echo("Stopped. Resume later from the menu (or `auditgdpr synth bible --freeze`).")
            return
        bible.freeze(typer.echo)
    typer.echo("\n[2/3] Generating documents (public -> internal -> confidential)...")
    r = generate.run(writer_model=config.SYNTH_WRITER_MODEL, judge_model=config.SYNTH_JUDGE_MODEL, log=typer.echo)
    typer.echo(f"\n[3/3] done: {r['by_status']} | writer calls {r['writer_calls']} | judge calls {r['judge_calls']}"
               f"\n  docs: {_rel(config.ACME_DIR)}   needs review: {_rel(config.SYNTH_DIR / 'needs_review')}")


def run_golden() -> None:
    mode = _choose("Which chunking mode should the golden set match?",
                   ["structure-aware (recommended)", "fixed-window baseline"])
    sa = mode == 1
    from .golden import generate
    resume_size = None
    pend = generate.pending_run(sa)
    if pend:
        typer.echo(f"\nAn interrupted golden run was found: {pend[0]}/{pend[1]} tasks finished (target size {pend[2]}).")
        pick = _choose("What now?", ["Resume where it stopped", "Start over (discard that progress)", "Exit"])
        if pick == 3:
            return
        if pick == 1:
            resume_size = pend[2]
        else:
            generate.journal_path(sa).unlink(missing_ok=True)
    existing = golden_paths(sa) if resume_size is None else []
    if existing:
        typer.echo(f"\nA golden set already exists: {golden_count(sa)} items ({_rel(existing[0])}).")
        pick = _choose("What now?", ["Generate new (deletes the existing golden set, then regenerates)", "Exit"])
        if pick == 2:
            return
        typer.echo("This will delete:\n" + "\n".join(f"  - {_rel(p)}" for p in existing))
        if not typer.confirm("Delete and regenerate?", default=False):
            return
        _safe_delete(existing)
        typer.echo("deleted.")
    if not _have_credentials():
        typer.echo("\nSet CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN (env or .env) first.")
        return
    size = resume_size or typer.prompt("Golden set size", default=200, type=int)

    from .pipeline import build_chunks
    typer.echo("\nChunking the corpus...")
    chunks = build_chunks(sa, config.EMBED_MODEL, exclude=())
    r = generate.run(chunks, size, config.GOLDEN_MODEL, sa, 42, 8, typer.echo)
    typer.echo(f"\naccepted {r['accepted']} {r['by_type']} | rejected {r['rejected']} | failed calls {r['failed_calls']}\n  {r['path']}")
    if r.get("incomplete"):
        typer.echo("Some calls failed. Choose 'Generate golden evaluation set' again and pick 'Resume' to retry only those.")


def main_menu() -> None:
    typer.echo("AuditGDPR")
    while True:
        pick = _choose("Menu", ["Generate golden evaluation set", "Generate Acme company documents", "Exit"])
        if pick == 3:
            return
        try:
            (run_golden if pick == 1 else run_company_docs)()
        except (RuntimeError, FileNotFoundError) as e:           # surface a clean message, stay in the menu
            typer.echo(f"\nerror: {e}")
