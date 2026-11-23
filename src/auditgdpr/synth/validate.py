"""Stage 5: deterministic checks (cheap, run first) and the LLM judge.

Issue.section is the top-level section number ("4") the problem lives in, or "" for document-wide problems.
severity "error" forces a revision; "warn" is only reported.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

from .. import config
from . import prompts as P
from . import world
from .world import DocSpec, Fact

PLACEHOLDER_RES = [
    re.compile(r"\[(?:Company|Name|Insert|Date|Your|Customer|Title|Address)[^\]]*\]", re.I),
    re.compile(r"\bTBD\b|\bTODO\b|\bXXX+\b|lorem ipsum", re.I),
    re.compile(r"\bas an AI\b|\blanguage model\b|\bfictional\b|\bsynthetic\b|\bfor illustrative purposes\b", re.I),
]
EMAIL_RE = re.compile(r"[\w.+-]+@([\w-]+(?:\.[\w-]+)+)")
PHONE_RE = re.compile(r"(?<!\w)\+\d[\d ()-]{8,}\d")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.M)


@dataclass
class Issue:
    section: str
    kind: str
    msg: str
    severity: str = "error"

    def line(self) -> str:
        return f"[{self.severity}] {self.kind}" + (f" (section {self.section})" if self.section else "") + f": {self.msg}"


def major(n: str) -> str:
    return n.split(".")[0].strip() if n else ""


def locate(sections: dict[str, str], needle: str) -> str:
    """Find the section whose text contains `needle`."""
    for n, text in sections.items():
        if needle in text:
            return n
    return ""


def allowed_ids(spec: DocSpec, facts: list[Fact], related_ids: set[str]) -> set[str]:
    ids = {spec.id} | related_ids | world.find_ids(spec.notes) | world.find_ids(spec.title)
    for f in world.cleared_facts(spec, facts):
        ids |= world.find_ids(f.text)
    # Systems/queues defined at lower tiers on OTHER topics are fine too
    for f in facts:
        if f.tier <= spec.tier:
            ids |= world.find_ids(f.text)
    return ids


def check(spec: DocSpec, sections: dict[str, str], facts: list[Fact], seeds: dict, related_ids: set[str],
          required_by_section: dict[str, list[str]] | None = None) -> list[Issue]:
    """Deterministic checks over the assembled document. `sections` maps top-level section number -> markdown
    ("" key = front matter/title block)."""
    issues: list[Issue] = []
    doc = "\n\n".join(sections.values())
    required_by_section = required_by_section or {}

    # --- hygiene -----------------------------------------------------------------------------
    for rx in PLACEHOLDER_RES:
        for m in rx.finditer(doc):
            issues.append(Issue(locate(sections, m.group(0)), "hygiene", f"placeholder/meta text {m.group(0)!r}"))
    for m in EMAIL_RE.finditer(doc):
        if m.group(1).lower() != "acme.example":
            issues.append(Issue(locate(sections, m.group(0)), "hygiene", f"email outside acme.example: {m.group(0)!r}"))
    for m in PHONE_RE.finditer(doc):
        issues.append(Issue(locate(sections, m.group(0)), "hygiene", f"phone number {m.group(0)!r}", "warn"))

    # --- tier discipline -----------------------------------------------------------------------
    ok_ids = allowed_ids(spec, facts, related_ids)
    for ident in sorted(world.find_ids(doc)):
        t = world.tier_of_id(ident)
        if t > spec.tier:
            issues.append(Issue(locate(sections, ident), "leak", f"identifier {ident} belongs to the {config.TIERS[t]} tier"))
        elif ident not in ok_ids and not any(k.startswith(ident + "-") for k in ok_ids):
            issues.append(Issue(locate(sections, ident), "invented-id", f"identifier {ident} is not in the fact sheet or related documents"))
    for name in world.hidden_entities(seeds, spec.tier):
        if re.search(re.escape(name), doc):
            issues.append(Issue(locate(sections, name), "leak", f"{name!r} is known only at a higher tier"))
    visible_tokens: set[str] = world.distinctive_tokens(spec.notes + " " + spec.effective)
    hidden_tokens: set[str] = set()
    for f in facts:
        (visible_tokens if f.tier <= spec.tier else hidden_tokens).update(world.distinctive_tokens(f.text))
    doc_tokens = world.distinctive_tokens(doc)
    for tok in sorted((hidden_tokens - visible_tokens) & doc_tokens):
        where = next((n for n, t in sections.items() if tok in world.distinctive_tokens(t)), "")
        issues.append(Issue(where, "leak", f"figure/date {tok!r} appears only in higher-tier facts"))

    # --- structure -----------------------------------------------------------------------------
    for n, text in sections.items():
        if n and not re.search(rf"^##\s+{re.escape(n)}\b", text, re.M):
            issues.append(Issue(n, "structure", f"section {n} lacks its '## {n}.' heading"))
        for tbl in re.findall(r"(?:^\|.*\n){26,}", text, re.M):
            issues.append(Issue(n, "structure", "table has more than 25 rows; split it", "warn"))
    words = len(doc.split())
    if words < 0.6 * spec.target_words or words > 1.6 * spec.target_words:
        issues.append(Issue("", "length", f"{words} words vs target {spec.target_words}", "warn"))

    # --- coverage of required facts ------------------------------------------------------------
    by_id = {f.id: f for f in facts}
    covered = checked = 0
    low = doc.lower()
    squashed = re.sub(r"\s+", "", low)
    for n, fids in required_by_section.items():
        for fid in fids:
            f = by_id.get(fid)
            if not f:
                continue
            keys = world.find_ids(f.text) | world.distinctive_tokens(f.text)
            if not keys:
                continue
            checked += 1
            if any(k.lower() in low or k.lower() in squashed for k in keys):
                covered += 1
            else:
                issues.append(Issue(n, "coverage", f"required fact {fid} not reflected (expect one of {sorted(keys)[:4]})", "warn"))
    if checked and covered / checked < 0.6:
        issues.append(Issue("", "coverage", f"only {covered}/{checked} checkable required facts appear in the document"))
    return issues


# --------------------------------------------------------------------------------------------------
def judge(llm, spec: DocSpec, facts: list[Fact], document: str) -> tuple[dict, list[Issue]]:
    spec_txt = (f"id: {spec.id} | title: {spec.title} | classification: {P.TIER_LABEL[spec.tier]} | type: {spec.doc_type}\n"
                f"status: {spec.status} | extra instructions: {spec.notes or '(none)'}")
    user = P.JUDGE_USER.format(spec=spec_txt, all_facts=world.facts_block(
        [f for f in facts if f.topic in spec.topics or f.tier == 0], show_tier=True),
        gdpr_ref=world.load_gdpr_ref(), document=document)
    verdict = llm.json(P.JUDGE_SYSTEM, user, P.JUDGE_SCHEMA, max_tokens=2000, temperature=0)
    scores = verdict.get("scores", {})
    crit = verdict.get("critical", [])
    passed = bool(scores) and all(int(v) >= 4 for v in scores.values()) and not crit and verdict.get("verdict") == "pass"
    issues = [Issue(major(i.get("section", "")), "judge", f"{i.get('fix', '')} (quote: {i.get('quote', '')[:120]!r})")
              for i in verdict.get("issues", [])]
    for c in crit:
        issues.append(Issue("", "judge-critical", c))
    if not passed and not issues:
        issues.append(Issue("", "judge", f"judge scored {scores} but gave no issues"))
    verdict["passed"] = passed
    return verdict, ([] if passed else issues)
