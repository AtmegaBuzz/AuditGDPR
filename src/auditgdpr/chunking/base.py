"""Shared data model for the chunking layer."""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Para:
    text: str
    page: int
    label: str | None = None     # recital "(12)", paragraph "34", article paragraph "2"


@dataclass
class Section:
    """A structural unit of a document: a heading path plus its body paragraphs."""
    path: list[str]                         # ["CHAPTER III — Rights of the data subject", "Article 15 — Right of access"]
    paras: list[Para] = field(default_factory=list)
    kind: str = "section"                   # section | article | recitals | front_matter
    extra: dict = field(default_factory=dict)   # e.g. {"article": "15", "chapter": "III"}

    @property
    def level(self) -> int:
        return len(self.path)


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    index: int
    text: str                    # clean body text (what you show/cite)
    embed_text: str              # header + body (what gets embedded)
    metadata: dict
