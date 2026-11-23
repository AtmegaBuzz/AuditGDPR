"""Offline end-to-end test of the synth pipeline with a fake Workers AI backend (no network, no cost).

Run:  python tests/test_synth_offline.py
Checks: bible sanitising + freeze, tier-ordered generation, leak detection -> revision loop, needs_review path,
front-matter/access_level, resume, and that no higher-tier identifiers end up in lower-tier files.
"""
from __future__ import annotations

import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from auditgdpr import config                                    # noqa: E402
from auditgdpr.synth import bible, generate, world              # noqa: E402
from auditgdpr.synth.emit import parse_front_matter             # noqa: E402
from auditgdpr.synth.llm import CachedLLM                       # noqa: E402

ALWAYS_LEAKY = "PUB-NOTICE-001"          # writer never fixes this one -> must end in needs_review
LEAK_ONCE = "INT-SOP-ERASE-002"          # leaks until it receives revision notes -> must pass on attempt 2


class FakeWriter:
    def chat_json(self, system, user, schema, max_tokens=0, temperature=0):
        name = schema["name"]
        if name == "fact_sheet":
            topic = re.search(r"id: (\w+)", user).group(1)
            tags = [t.strip() for t in re.search(r"allowed tags: (.*)", user).group(1).split(",")]
            code = topic[:3].upper()
            facts = []
            for i in range(3):
                facts.append({"tier": "public", "tags": tags, "text": f"Acme tells customers {topic} item {i} within {10 + i} days."})
            for i in range(4):
                facts.append({"tier": "internal", "tags": tags, "text": f"Privacy Operations tracks {topic} step {i} in queue INT-Q-{code} with a {15 + i}% target."})
            for i in range(4):
                facts.append({"tier": "confidential", "tags": tags, "text": f"Board resolution CONF-BRD-{code}-{i} accepted {topic} risk of {20 + i}% on 2026-06-0{i + 1}."})
            facts.append({"tier": "public", "tags": [], "text": "BAD public fact citing CONF-BRD-LEAK-1."})      # must be dropped
            return {"facts": facts}
        if name == "outline":
            req = re.search(r"REQUIRED FACTS: (.*)", user).group(1)
            ids = [x.strip() for x in req.split(",") if x.strip().startswith("F-")]
            chunks = [ids[0::3], ids[1::3], ids[2::3]]
            return {"summary": "A document summary.", "sections": [
                {"n": str(k + 1), "heading": f"Part {k + 1}", "brief": "b", "fact_ids": c, "target_words": 100} for k, c in enumerate(chunks)]}
        raise AssertionError(name)

    def chat_text(self, system, user, max_tokens=0, temperature=0):
        spec_id = re.search(r"id: ([A-Z0-9-]+) \|", user).group(1)
        if "Write the opening of the document" in user:
            title = re.search(r"title: (.*?) \| classification", user).group(1)
            return f"# {title}\n\n| Field | Value |\n|---|---|\n| ID | {spec_id} |"
        n = re.search(r'Write section (\d+) "', user).group(1)
        want = re.search(r"Facts you must use \(.*?\): (.*?)\. Target", user).group(1).split(", ")
        lines = {m.group(1): m.group(2) for m in re.finditer(r"^\[(F-[A-Z]+-\d+)\] (.*)$", user, re.M)}
        body = "\n\n".join(lines.get(w, "") for w in want)
        out = f"## {n}. Part {n}\n\n{body}\n"
        revised = "REVISION NOTES" in user
        if n == "1" and ((spec_id == LEAK_ONCE and not revised) or spec_id == ALWAYS_LEAKY):
            out += "\nSee also CONF-BRD-2026-06-R3 for the board position.\n"
        return out


class FakeJudge:
    def chat_json(self, system, user, schema, max_tokens=0, temperature=0):
        return {"scores": {"fact_fidelity": 5, "tier_discipline": 5, "gdpr_accuracy": 5, "realism": 4, "retrievability": 5},
                "critical": [], "issues": [], "verdict": "pass"}


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="synth_test_"))
    config.SYNTH_DIR, config.ACME_DIR = tmp / "synth", tmp / "acme"
    logs: list[str] = []

    writer = CachedLLM("fake/writer", FakeWriter(), tmp / "cache")
    judge = CachedLLM("fake/judge", FakeJudge(), tmp / "cache")

    # --- stage 1: bible ---------------------------------------------------------------------------------
    r = bible.run(llm=writer, log=logs.append)
    draft = world.load_bible(world.draft_path())
    assert r["n"] == len(draft) == 9 * 11, (r["n"], len(draft))             # 11 good facts per topic; the BAD one is dropped
    assert not any("LEAK" in f.text for f in draft)
    assert all(not world.find_ids(f.text) or all(world.tier_of_id(i) <= f.tier for i in world.find_ids(f.text)) for f in draft)
    assert len({f.id for f in draft}) == len(draft)
    bible.freeze(logs.append)
    facts = world.load_bible()
    assert not bible.coverage_problems(facts), bible.coverage_problems(facts)

    # --- stages 3-6 --------------------------------------------------------------------------------------
    res = generate.run(writer=writer, judge=judge, facts=facts, concurrency=4, retries=2, log=logs.append)
    by = res["by_status"]
    assert by == {"ok": 36, "needs_review": 1}, (by, [l for l in logs if "FAIL" in l or "needs_review" in l][:5])
    state = {x["id"]: x for x in res["results"]}
    assert state[LEAK_ONCE]["status"] == "ok" and state[LEAK_ONCE]["attempts"] == 2, state[LEAK_ONCE]
    assert state[ALWAYS_LEAKY]["status"] == "needs_review" and state[ALWAYS_LEAKY]["attempts"] == 3
    assert (config.SYNTH_DIR / "needs_review" / f"{ALWAYS_LEAKY}.md").exists()
    assert not (config.ACME_DIR / "public" / f"{ALWAYS_LEAKY}.md").exists()

    # --- output invariants ----------------------------------------------------------------------------------
    specs = {s.id: s for s in world.load_manifest()}
    n_files = 0
    for path in config.ACME_DIR.rglob("*.md"):
        meta, body = parse_front_matter(path.read_text())
        spec = specs[meta["doc_id"]]
        n_files += 1
        assert meta["access_level"] == spec.tier and path.parent.name == config.TIERS[spec.tier]
        for ident in world.find_ids(body):
            assert world.tier_of_id(ident) <= spec.tier, (spec.id, ident)
        assert body.lstrip().startswith("# "), spec.id
    assert n_files == 36, n_files
    assert specs["INT-SOP-ERASE-001"].status == "superseded"

    # --- resume: second run touches nothing -------------------------------------------------------------------
    res2 = generate.run(writer=writer, judge=judge, facts=facts, concurrency=4, retries=2, log=logs.append)
    assert res2["by_status"] == {"skipped": 36, "ok": 0, "needs_review": 1} or res2["by_status"] == {"skipped": 36, "needs_review": 1}, res2["by_status"]

    # --- planning helpers ------------------------------------------------------------------------------------
    assert [s.id for s in generate.select(list(specs.values()), "ERASE", "internal")] == ["INT-SOP-ERASE-002", "INT-SOP-ERASE-001", "INT-RUN-ERASE-001"]
    print(f"OK  tmp={tmp}  files={n_files}  writer calls={writer.calls}")


if __name__ == "__main__":
    main()
