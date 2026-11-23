"""Loaders and renderers for the fictional world: seeds, manifest, fact sheet (bible); tier-aware context blocks."""
from __future__ import annotations

import json
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from .. import config

HERE = Path(__file__).parent
TIER_BY_NAME = {v: k for k, v in config.TIERS.items()}
TIER_BY_PREFIX = {"PUB": 0, "INT": 1, "CONF": 2}

# Identifier canaries: PUB-/INT-/CONF- followed by dash-separated alphanumerics. Lookbehind keeps us from matching
# the tail of a longer token such as "ACME-CONF-1".
ID_RE = re.compile(r"(?<![A-Za-z0-9-])((?:PUB|INT|CONF)(?:-[A-Z0-9][A-Za-z0-9]*)+)")
# "distinctive" non-ID tokens used for leak/coverage checks
TOKEN_RE = re.compile(r"\d{1,3}(?:[.,]\d+)?%|[€$]\s?\d[\d.,]*\s?(?:[MKmk]|million|billion)?|\d{4}-\d{2}-\d{2}|\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}")


def tier_of_id(ident: str) -> int:
    return TIER_BY_PREFIX[ident.split("-", 1)[0]]


def find_ids(text: str) -> set[str]:
    return {m.rstrip("-") for m in ID_RE.findall(text)}


def distinctive_tokens(text: str) -> set[str]:
    return {re.sub(r"\s+", "", t.lower()) for t in TOKEN_RE.findall(text)}


# --------------------------------------------------------------------------------------------------
@dataclass(frozen=True)
class Fact:
    id: str
    topic: str
    tier: int
    tags: tuple[str, ...]
    text: str

    def to_json(self) -> dict:
        return {"id": self.id, "topic": self.topic, "tier": config.TIERS[self.tier], "tags": list(self.tags), "text": self.text}


@dataclass
class DocSpec:
    id: str
    title: str
    tier: int
    doc_type: str
    topics: list[str]
    tags: list[str]
    owner: str
    approver: str
    version: str
    effective: str
    audience: str
    articles: list[int]
    target_words: int
    related: list[str] = field(default_factory=list)
    notes: str = ""
    status: str = "current"

    @property
    def tier_name(self) -> str:
        return config.TIERS[self.tier]


def load_seeds() -> dict:
    return tomllib.loads((HERE / "seeds.toml").read_text())


def load_gdpr_ref() -> str:
    return (HERE / "gdpr_ref.md").read_text()


def load_manifest() -> list[DocSpec]:
    raw = tomllib.loads((HERE / "manifest.toml").read_text())["docs"]
    specs = [DocSpec(**{**d, "effective": str(d["effective"])}) for d in raw]
    by_id = {s.id: s for s in specs}
    if len(by_id) != len(specs):
        raise ValueError("duplicate doc ids in manifest")
    topics = {t["id"] for t in load_seeds()["topics"]}
    for s in specs:
        expected = {0: "PUB-", 1: "INT-", 2: "CONF-"}[s.tier]
        if not s.id.startswith(expected):
            raise ValueError(f"{s.id}: id prefix must be {expected} for tier {s.tier}")
        for t in s.topics:
            if t not in topics:
                raise ValueError(f"{s.id}: unknown topic {t}")
        for r in s.related:
            if r not in by_id:
                raise ValueError(f"{s.id}: related doc {r} not in manifest")
            if by_id[r].tier > s.tier:
                raise ValueError(f"{s.id}: related doc {r} has a higher tier (would leak)")
    waves(specs)    # raises on cycles
    return specs


def waves(specs: list[DocSpec]) -> list[list[DocSpec]]:
    """Topological layers over `related`; within a layer docs are independent and can run in parallel."""
    ids = {s.id for s in specs}
    done: set[str] = set()
    pending = list(specs)
    out: list[list[DocSpec]] = []
    while pending:
        layer = [s for s in pending if all(r in done or r not in ids for r in s.related)]
        if not layer:
            raise ValueError(f"cycle in `related` among: {[s.id for s in pending]}")
        out.append(layer)
        done |= {s.id for s in layer}
        pending = [s for s in pending if s.id not in done]
    return out


def bible_path() -> Path:
    return config.ACME_DIR / "bible.json"


def draft_path() -> Path:
    return config.SYNTH_DIR / "bible.draft.json"


def load_bible(path: Path | None = None) -> list[Fact]:
    p = path or bible_path()
    if not p.exists():
        raise FileNotFoundError(f"{p} not found. Run `auditgdpr synth bible`, review the draft, then `--freeze`.")
    return [Fact(f["id"], f["topic"], TIER_BY_NAME[f["tier"]], tuple(f.get("tags", [])), f["text"])
            for f in json.loads(p.read_text())["facts"]]


# --------------------------------------------------------------------------------------------------
# Tier-aware context blocks
# --------------------------------------------------------------------------------------------------
def company_block(seeds: dict) -> str:
    c = seeds["company"]
    lines = [f"{c['name']} ({c['legal_name']}): {c['pitch']}", f"Size: {c['size']}. EU base: {c['eu_hq']}. Parent: {c['parent']}.",
             f"GDPR roles: {c['roles']}", f"Privacy contact: {c['privacy_contact']}. 'Today' in this world is {c['today']}."]
    lines += [f"Rule: {r}" for r in c["rules"]]
    return "\n".join(lines)


def world_block(seeds: dict, tier: int) -> str:
    """People and systems the writer may know about (tier <= doc tier)."""
    people = [f"  - {p['name']}, {p['role']}" for p in seeds["people"] if p["tier"] <= tier]
    systems = [f"  - {s['name']}: {s['what']}" for s in seeds["systems"] if s["tier"] <= tier]
    return "People:\n" + "\n".join(people) + "\nSystems:\n" + "\n".join(systems)


def hidden_entities(seeds: dict, tier: int) -> list[str]:
    """Names of people/systems ABOVE `tier`; must not appear in a document of that tier."""
    return [p["name"] for p in seeds["people"] if p["tier"] > tier] + [s["name"] for s in seeds["systems"] if s["tier"] > tier]


def facts_block(facts: list[Fact], show_tier: bool = False) -> str:
    return "\n".join(f"[{f.id}]" + (f" ({config.TIERS[f.tier]})" if show_tier else "") + f" {f.text}" for f in facts) or "(none)"


def cleared_facts(spec: DocSpec, facts: list[Fact]) -> list[Fact]:
    return [f for f in facts if f.tier <= spec.tier and f.topic in spec.topics]


def required_facts(spec: DocSpec, facts: list[Fact]) -> list[Fact]:
    """Own-tier facts on the doc's topics (narrowed by its tags) that the document must cover."""
    if spec.status == "superseded":
        return []
    return [f for f in cleared_facts(spec, facts)
            if f.tier == spec.tier and (not spec.tags or set(f.tags) & set(spec.tags))]
