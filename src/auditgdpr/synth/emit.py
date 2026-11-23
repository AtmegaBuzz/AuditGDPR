"""Stage 6: front-matter (every value JSON-encoded, so the block is valid YAML and trivially parseable) + file layout.

access_level is written here, from the manifest tier. It is never taken from model output.
"""
from __future__ import annotations

import hashlib
import json

from .. import config
from . import prompts as P
from .world import DocSpec

PROMPT_HASH = hashlib.sha256((P.WRITER_SYSTEM + P.OUTLINE_TASK + P.SECTION_TASK + P.FRONT_TASK + P.JUDGE_SYSTEM).encode()).hexdigest()[:12]


def front_matter(spec: DocSpec, generator: dict, review: dict | None = None) -> str:
    fields = {
        "doc_id": spec.id, "title": spec.title, "company": "Acme Corp", "publisher": "ACME",
        "access_level": spec.tier, "classification": config.TIERS[spec.tier],
        "doc_type": spec.doc_type, "profile": "company_doc", "topic": spec.topics[0], "topics": spec.topics,
        "owner": spec.owner, "approver": spec.approver, "version": spec.version, "effective_date": spec.effective,
        "status": spec.status, "gdpr_articles": spec.articles, "related": spec.related,
        "generator": generator, "review": review or {},
    }
    return "---\n" + "\n".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fields.items()) + "\n---\n"


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    meta = {}
    for line in head.splitlines():
        k, _, v = line.partition(": ")
        meta[k] = json.loads(v)
    return meta, body.lstrip("\n")


def doc_path(root, spec: DocSpec):
    return root / config.TIERS[spec.tier] / f"{spec.id}.md"
