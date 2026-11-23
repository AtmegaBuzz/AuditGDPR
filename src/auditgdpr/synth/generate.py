"""Stages 3-6: outline -> sections -> validate/judge -> revise loop -> emit.

Docs run in dependency waves (`related`), docs inside a wave run in parallel. Everything is cached per LLM call and
resumable: an existing output file is skipped unless --force.
"""
from __future__ import annotations

import json
import re
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path

from .. import config
from . import emit, validate, world
from . import prompts as P
from .llm import CachedLLM
from .world import DocSpec, Fact


@dataclass
class Ctx:
    seeds: dict
    gdpr_ref: str
    facts: list[Fact]
    writer: CachedLLM
    judge: CachedLLM
    out_dir: Path
    retries: int
    log: callable
    run_id: str
    state: dict = field(default_factory=dict)
    lock: threading.Lock = field(default_factory=threading.Lock)

    @property
    def state_path(self) -> Path:
        return self.out_dir / "_state.json"

    def save_state(self) -> None:
        with self.lock:
            self.out_dir.mkdir(parents=True, exist_ok=True)
            self.state_path.write_text(json.dumps(self.state, indent=2, ensure_ascii=False))


# --------------------------------------------------------------------------------------------------
def _spec_text(spec: DocSpec) -> str:
    return P.DOC_SPEC.format(
        id=spec.id, title=spec.title, tier_label=P.TIER_LABEL[spec.tier], doc_type=spec.doc_type, owner=spec.owner,
        approver=spec.approver, version=spec.version, effective=spec.effective, status=spec.status,
        audience=spec.audience, articles=", ".join(f"Art. {a}" for a in spec.articles), notes=spec.notes or "(none)")


def _related_text(spec: DocSpec, ctx: Ctx) -> tuple[str, set[str]]:
    lines, ids = [], set()
    for rid in spec.related:
        st = ctx.state.get(rid)
        if st and st.get("summary"):
            lines.append(f"- {rid} \"{st['title']}\": {st['summary']}")
            ids.add(rid)
    return "\n".join(lines) or "(none)", ids


def _context(spec: DocSpec, ctx: Ctx, related_text: str) -> str:
    return P.CONTEXT_BLOCKS.format(
        spec=_spec_text(spec), company=world.company_block(ctx.seeds), world=world.world_block(ctx.seeds, spec.tier),
        tier_label=P.TIER_LABEL[spec.tier], facts=world.facts_block(world.cleared_facts(spec, ctx.facts)),
        gdpr_ref=ctx.gdpr_ref, related=related_text)


def _plan_outline(spec: DocSpec, ctx: Ctx, context: str, required: list[Fact]) -> dict:
    task = P.OUTLINE_TASK.format(doc_type=spec.doc_type, target_words=spec.target_words,
                                 required=", ".join(f.id for f in required) or "(none)")
    raw = ctx.writer.json(P.WRITER_SYSTEM, context + "\n\n" + task, P.OUTLINE_SCHEMA, max_tokens=3500, temperature=0.5)
    known = {f.id for f in world.cleared_facts(spec, ctx.facts)}
    secs = []
    for i, s in enumerate(raw.get("sections", []), 1):
        secs.append({"n": str(i), "heading": re.sub(r"^\d+(\.\d+)*\.?\s*", "", s["heading"]).strip(),
                     "brief": s["brief"], "fact_ids": [f for f in s.get("fact_ids", []) if f in known],
                     "target_words": max(80, int(s.get("target_words") or spec.target_words // max(1, len(raw["sections"]))))})
    if len(secs) < 2:
        raise RuntimeError(f"{spec.id}: outline has {len(secs)} sections")
    assigned = {f for s in secs for f in s["fact_ids"]}
    for j, f in enumerate(f for f in required if f.id not in assigned):     # make sure every required fact has a home
        secs[j % len(secs)]["fact_ids"].append(f.id)
    return {"sections": secs, "summary": " ".join((raw.get("summary") or spec.title).split())}


def _clean_section(text: str, n: str, heading: str) -> str:
    text = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", text.strip())
    lines = text.splitlines()
    want = f"## {n}. {heading}"
    if lines and lines[0].lstrip().startswith("#"):
        lines[0] = want
    else:
        lines.insert(0, want + "\n")
    return "\n".join(lines).strip()


def _write_section(spec: DocSpec, ctx: Ctx, context: str, sec: dict, prior: str, notes: list[str] | None = None,
                   previous: str = "") -> str:
    revision = ""
    if notes:
        revision = ("REVISION NOTES. Your previous draft of this section had these problems; fix every one, keep "
                    "everything that was correct:\n" + "\n".join(f"- {n}" for n in notes) +
                    f"\n\nPREVIOUS DRAFT\n{previous}\n\n")
    task = P.SECTION_TASK.format(prior=prior or "(nothing yet)", n=sec["n"], heading=sec["heading"], brief=sec["brief"],
                                 fact_ids=", ".join(sec["fact_ids"]) or "(none specific)",
                                 target_words=sec["target_words"], revision=revision)
    text = ctx.writer.text(P.WRITER_SYSTEM, context + "\n\n" + task, max_tokens=int(sec["target_words"] * 2.5) + 400, temperature=0.7)
    return _clean_section(text, sec["n"], sec["heading"])


def _write_front(spec: DocSpec, ctx: Ctx, context: str, notes: list[str] | None = None) -> str:
    task = P.FRONT_TASK.format(title=spec.title, tier_label=P.TIER_LABEL[spec.tier], doc_type=spec.doc_type)
    if notes:
        task += "\nFix these problems from the previous attempt:\n" + "\n".join(f"- {n}" for n in notes)
    text = ctx.writer.text(P.WRITER_SYSTEM, context + "\n\n" + task, max_tokens=900, temperature=0.3).strip()
    text = re.sub(r"^```(?:markdown|md)?\s*\n|\n```\s*$", "", text)
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        text = f"# {spec.title}\n\n{text}"
    return text


# --------------------------------------------------------------------------------------------------
def build_doc(spec: DocSpec, ctx: Ctx) -> dict:
    t0 = time.time()
    related_text, related_ids = _related_text(spec, ctx)
    context = _context(spec, ctx, related_text)
    required = world.required_facts(spec, ctx.facts)
    outline = _plan_outline(spec, ctx, context, required)
    secs = {s["n"]: s for s in outline["sections"]}
    required_by_section = {s["n"]: [f for f in s["fact_ids"] if any(r.id == f for r in required)] for s in outline["sections"]}

    sections: dict[str, str] = {"": _write_front(spec, ctx, context)}
    prior = sections[""]
    for n, sec in secs.items():                                  # sequential: each section sees what came before
        sections[n] = _write_section(spec, ctx, context, sec, prior)
        prior += "\n\n" + sections[n]

    status, verdict, issues, attempt = "needs_review", None, [], 0
    for attempt in range(ctx.retries + 1):
        issues = validate.check(spec, sections, ctx.facts, ctx.seeds, related_ids, required_by_section)
        errors = [i for i in issues if i.severity == "error"]
        verdict = None
        if not errors:
            verdict, errors = validate.judge(ctx.judge, spec, ctx.facts, "\n\n".join(sections.values()))
            issues = [i for i in issues if i.severity != "error"] + errors
        if not errors:
            status = "ok"
            break
        if attempt == ctx.retries:
            break
        # revise: group error notes by top-level section; doc-wide notes go to every section and the front block
        notes: dict[str, list[str]] = {}
        for i in errors:
            key = validate.major(i.section)
            targets = [key] if key in secs else list(secs) + [""]
            for t in targets:
                notes.setdefault(t, []).append(i.line())
        for n, ns in notes.items():
            if n == "":
                sections[""] = _write_front(spec, ctx, context, ns)
            else:
                sections[n] = _write_section(spec, ctx, context, secs[n], prior_before(sections, n), ns, sections[n])

    body = "\n\n".join(sections.values()).strip() + "\n"
    generator = {"writer": ctx.writer.model, "judge": ctx.judge.model, "run_id": ctx.run_id, "prompt_hash": emit.PROMPT_HASH}
    review = {"status": status, "attempts": attempt + 1, "issues_left": len([i for i in issues if i.severity == "error"]),
              "scores": (verdict or {}).get("scores", {})}
    text = emit.front_matter(spec, generator, review) + "\n" + body
    if status == "ok":
        path = emit.doc_path(ctx.out_dir, spec)
    else:
        path = config.SYNTH_DIR / "needs_review" / f"{spec.id}.md"
        (config.SYNTH_DIR / "needs_review").mkdir(parents=True, exist_ok=True)
        path.with_suffix(".issues.txt").write_text("\n".join(i.line() for i in issues))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    res = {"id": spec.id, "title": spec.title, "status": status, "attempts": attempt + 1, "words": len(body.split()),
           "scores": review["scores"], "summary": outline["summary"], "path": str(path),
           "issues": [i.line() for i in issues], "seconds": round(time.time() - t0)}
    with ctx.lock:
        ctx.state[spec.id] = res
    ctx.save_state()
    return res


def prior_before(sections: dict[str, str], n: str) -> str:
    """Text of everything that precedes section n (so a regenerated section keeps continuity)."""
    out = []
    for k, v in sections.items():
        if k == n:
            break
        out.append(v)
    return "\n\n".join(out)


# --------------------------------------------------------------------------------------------------
def select(specs: list[DocSpec], only: str | None, tier: str | None) -> list[DocSpec]:
    keys = [k.strip() for k in only.split(",")] if only else []
    out = [s for s in specs if (not keys or any(k in s.id for k in keys)) and (not tier or s.tier_name == tier)]
    return out


def plan(specs: list[DocSpec], facts: list[Fact]) -> list[str]:
    lines = []
    for w, layer in enumerate(world.waves(specs), 1):
        for s in layer:
            lines.append(f"wave {w}  {s.tier_name[:4]:<4} {s.id:<24} {s.doc_type:<15} ~{s.target_words:>4}w  "
                         f"cleared={len(world.cleared_facts(s, facts)):>3}  required={len(world.required_facts(s, facts)):>2}")
    return lines


def run(only: str | None = None, tier: str | None = None, writer_model: str = config.SYNTH_WRITER_MODEL,
        judge_model: str = config.SYNTH_JUDGE_MODEL, force: bool = False, concurrency: int = 4, retries: int = 2,
        out_dir: Path | None = None, log=print, writer: CachedLLM | None = None, judge: CachedLLM | None = None,
        facts: list[Fact] | None = None) -> dict:
    out_dir = out_dir or config.ACME_DIR
    manifest = world.load_manifest()
    facts = facts if facts is not None else world.load_bible()
    ctx = Ctx(world.load_seeds(), world.load_gdpr_ref(), facts, writer or CachedLLM(writer_model),
              judge or CachedLLM(judge_model), out_dir, retries, log, time.strftime("%Y%m%d-%H%M%S"))
    if ctx.state_path.exists():
        ctx.state = json.loads(ctx.state_path.read_text())
    chosen = {s.id for s in select(manifest, only, tier)}
    results = []

    def one(spec: DocSpec):
        path = emit.doc_path(out_dir, spec)
        if path.exists() and not force:
            log(f"  skip   {spec.id} (exists)")
            return {"id": spec.id, "status": "skipped"}
        try:
            r = build_doc(spec, ctx)
        except Exception as e:                                   # one bad doc must not kill the run
            log(f"  FAIL   {spec.id}: {e}")
            return {"id": spec.id, "status": "error", "error": str(e)}
        log(f"  {r['status']:<12} {spec.id:<24} {r['words']:>5}w attempts={r['attempts']} {r['seconds']}s scores={r['scores']}")
        return r

    for layer in world.waves(manifest):
        todo = [s for s in layer if s.id in chosen]
        if todo:
            with ThreadPoolExecutor(concurrency) as ex:
                results += list(ex.map(one, todo))
    by = {}
    for r in results:
        by[r["status"]] = by.get(r["status"], 0) + 1
    return {"by_status": by, "results": results, "writer_calls": ctx.writer.calls, "writer_cache_hits": ctx.writer.hits,
            "judge_calls": ctx.judge.calls, "out_dir": str(out_dir)}
