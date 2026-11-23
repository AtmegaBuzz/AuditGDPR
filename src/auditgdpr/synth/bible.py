"""Stage 1: expand seeds.toml into the canonical, tier-tagged fact sheet (one LLM call per topic).

Output: artifacts/synth/bible.draft.json  ->  (human review/edit)  ->  data/acme/bible.json via `--freeze`.
"""
from __future__ import annotations

import json
import shutil
from collections import Counter
from concurrent.futures import ThreadPoolExecutor

from .. import config
from . import prompts as P
from . import world
from .llm import CachedLLM


def sanitize(topic: dict, raw_facts: list[dict]) -> tuple[list[world.Fact], list[str]]:
    """Assign ids, normalise tags, and drop facts that violate the identifier-namespace rules."""
    allowed_tags = set(topic["tags"])
    out: list[world.Fact] = []
    dropped: list[str] = []
    seen: set[str] = set()
    for rf in raw_facts:
        text = " ".join((rf.get("text") or "").split())
        tier = world.TIER_BY_NAME.get(rf.get("tier", ""))
        if not text or tier is None:
            dropped.append(f"malformed: {text[:60]!r}")
            continue
        ids = world.find_ids(text)
        if any(world.tier_of_id(i) > tier for i in ids):
            dropped.append(f"id above tier ({config.TIERS[tier]}): {text[:80]!r}")
            continue
        if tier == 0 and ids - {i for i in ids if world.tier_of_id(i) == 0}:
            dropped.append(f"identifier in public fact: {text[:80]!r}")
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        tags = tuple(t for t in rf.get("tags", []) if t in allowed_tags)
        out.append(world.Fact("", topic["id"], tier, tags, text))
    out.sort(key=lambda f: (f.tier,))
    numbered = [world.Fact(f"F-{topic['code']}-{i:02d}", f.topic, f.tier, f.tags, f.text) for i, f in enumerate(out, 1)]
    return numbered, dropped


def build_topic(llm: CachedLLM, seeds: dict, gdpr_ref: str, topic: dict, min_facts: int, max_facts: int) -> dict:
    user = P.BIBLE_USER.format(
        topic_id=topic["id"], question=topic["question"], gdpr=topic["gdpr"], tags=", ".join(topic["tags"]),
        tensions="\n".join(f"    - {t}" for t in topic.get("tensions", [])),
        company=world.company_block(seeds), world=world.world_block(seeds, 2), gdpr_ref=gdpr_ref)
    system = P.BIBLE_SYSTEM.format(min_facts=min_facts, max_facts=max_facts)
    raw = llm.json(system, user, P.BIBLE_SCHEMA, max_tokens=6000, temperature=0.7)
    facts, dropped = sanitize(topic, raw.get("facts", []))
    return {"topic": topic["id"], "facts": facts, "dropped": dropped}


def run(model: str = config.SYNTH_WRITER_MODEL, only: str | None = None, min_facts: int = 16, max_facts: int = 28,
        concurrency: int = 4, log=print, llm: CachedLLM | None = None) -> dict:
    seeds, gdpr_ref = world.load_seeds(), world.load_gdpr_ref()
    topics = [t for t in seeds["topics"] if not only or only in t["id"]]
    llm = llm or CachedLLM(model)
    results, failed = [], {}

    def one(t):
        try:
            r = build_topic(llm, seeds, gdpr_ref, t, min_facts, max_facts)
            log(f"  done {t['id']} ({len(results) + len(failed) + 1}/{len(topics)})")
            return r
        except Exception as e:                       # keep the other topics; finished calls are already cached on disk
            log(f"  FAILED {t['id']}: {e}")
            failed[t["id"]] = str(e)
            return None

    with ThreadPoolExecutor(concurrency) as ex:
        for r in ex.map(one, topics):
            if r:
                results.append(r)
    facts = [f for r in results for f in r["facts"]]
    for r in results:
        c = Counter(config.TIERS[f.tier] for f in r["facts"])
        log(f"  {r['topic']:<10} {len(r['facts']):>3} facts  pub={c['public']} int={c['internal']} conf={c['confidential']}"
            f"  dropped={len(r['dropped'])}")
        for d in r["dropped"]:
            log(f"      dropped: {d}")
    config.SYNTH_DIR.mkdir(parents=True, exist_ok=True)
    path = world.draft_path()
    path.write_text(json.dumps({"model": model, "facts": [f.to_json() for f in facts]}, indent=2, ensure_ascii=False))
    log(f"\nwrote {len(facts)} facts -> {path}\nReview/edit it, then: auditgdpr synth bible --freeze")
    if failed:
        raise RuntimeError(f"{len(failed)}/{len(topics)} topics failed ({', '.join(failed)}); partial draft saved, "
                           f"completed topics are cached, so re-running only retries the failed ones")
    return {"path": str(path), "n": len(facts), "api_calls": llm.calls, "cache_hits": llm.hits}


def coverage_problems(facts: list[world.Fact]) -> list[str]:
    """Each manifest doc must have required facts; each topic should have all three tiers."""
    problems = []
    tiers_by_topic: dict[str, set[int]] = {}
    for f in facts:
        tiers_by_topic.setdefault(f.topic, set()).add(f.tier)
    for t in world.load_seeds()["topics"]:
        missing = {0, 1, 2} - tiers_by_topic.get(t["id"], set())
        if missing:
            problems.append(f"topic {t['id']}: no facts at tier(s) {sorted(config.TIERS[m] for m in missing)}")
    for spec in world.load_manifest():
        if spec.status != "superseded" and not world.required_facts(spec, facts):
            problems.append(f"doc {spec.id}: no required facts (topics={spec.topics}, tags={spec.tags})")
    return problems


def freeze(log=print) -> None:
    src = world.draft_path()
    if not src.exists():
        raise FileNotFoundError(f"{src} not found; run `auditgdpr synth bible` first")
    facts = world.load_bible(src)
    problems = coverage_problems(facts)
    for p in problems:
        log(f"  WARNING: {p}")
    config.ACME_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, world.bible_path())
    log(f"froze {len(facts)} facts -> {world.bible_path()}" + ("" if not problems else f"  ({len(problems)} coverage warnings)"))
