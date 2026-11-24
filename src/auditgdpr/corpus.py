"""Corpus discovery + document-level metadata derived from folder/file naming."""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, asdict, field
from pathlib import Path

from .config import DATA_DIR, DEFAULT_EXCLUDE, TIERS

_EDPB = re.compile(r"edpb_guidelines_(?P<num>\d+-\d{4})_(?P<topic>.+?)_v(?P<ver>[\d.]+)(?P<draft>_consultation)?$")
_WP29 = re.compile(r"wp29_wp(?P<num>\d+)rev(?P<rev>\d+)_(?P<topic>.+)$")
_GDPR = re.compile(r"gdpr_regulation_(?P<num>[\d-]+)$")


@dataclass(frozen=True)
class DocMeta:
    doc_id: str
    path: str
    title: str
    publisher: str       # EU | EDPB | WP29
    doc_type: str        # regulation | guidelines
    profile: str         # parsing profile: legal_act | guidance
    category: str        # folder, e.g. 03_edpb_lawful_bases
    reference: str       # e.g. "05/2020", "WP260 rev.01", "2016/679"
    version: str | None
    status: str          # final | consultation_draft
    access_level: int = 0                          # 0 public | 1 internal | 2 confidential  (drives row-level security)
    classification: str = "public"
    source_type: str = "pdf"                       # pdf | markdown  (detected from the file extension)
    extra: dict = field(default_factory=dict, compare=False)   # front-matter fields (access_level, topics, owner, ...)

    def to_payload(self) -> dict:
        d = asdict(self)
        d.pop("path")
        d.update(d.pop("extra"))
        return d


def _pretty(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ")


SUPPORTED = {".pdf": "pdf", ".md": "markdown"}


def _describe_markdown(path: Path) -> DocMeta:
    """Company documents carry YAML-ish front matter (see synth/emit.py); plain .md files fall back to the filename."""
    from .synth.emit import parse_front_matter
    meta, _ = parse_front_matter(path.read_text(encoding="utf-8"))
    skip = {"doc_id", "title", "publisher", "doc_type", "profile", "version", "status", "generator", "review",
            "access_level", "classification"}
    level = meta.get("access_level")
    if level not in TIERS:                           # missing/garbled label -> fail closed: treat as confidential
        level = max(TIERS)
    return DocMeta(
        doc_id=meta.get("doc_id", path.stem), path=str(path), title=meta.get("title", _pretty(path.stem)),
        publisher=meta.get("publisher", "ACME"), doc_type=meta.get("doc_type", "document"),
        profile=meta.get("profile", "company_doc"), category=path.parent.name,
        reference=meta.get("doc_id", path.stem), version=meta.get("version"), status=meta.get("status", "current"),
        access_level=level, classification=TIERS[level],
        source_type="markdown", extra={k: v for k, v in meta.items() if k not in skip})


def describe(path: Path) -> DocMeta:
    if path.suffix.lower() == ".md":
        return _describe_markdown(path)
    stem, category = path.stem, path.parent.name
    if m := _GDPR.match(stem):
        return DocMeta(stem, str(path), "GDPR — Regulation (EU) 2016/679", "EU", "regulation",
                       "legal_act", category, "2016/679", None, "final")
    if m := _EDPB.match(stem):
        n, y = m["num"].split("-")
        topic = _pretty(m["topic"])
        return DocMeta(stem, str(path), f"EDPB Guidelines {n}/{y} — {topic}", "EDPB", "guidelines",
                       "guidance", category, f"{n}/{y}", m["ver"],
                       "consultation_draft" if m["draft"] else "final")
    if m := _WP29.match(stem):
        topic = _pretty(m["topic"])
        return DocMeta(stem, str(path), f"WP29 WP{m['num']} rev.{m['rev']} — {topic}", "WP29", "guidelines",
                       "guidance", category, f"WP{m['num']} rev.{m['rev']}", m["rev"], "final")
    raise ValueError(f"Unrecognised corpus file name: {path.name}")


def _excluded(path: Path, root: Path, exclude: set[str]) -> bool:
    """A folder is excluded if its name, its path relative to root, or its absolute path is listed."""
    rel = path.relative_to(root).as_posix()
    return path.name in exclude or rel in exclude or str(path.resolve()) in exclude


def discover(root: Path = DATA_DIR, exclude: tuple[str, ...] | list[str] = DEFAULT_EXCLUDE) -> list[DocMeta]:
    """Find documents (.pdf, .md) under `root`; the type is detected from the extension. Excluded folders are pruned: the walk never descends into them."""
    root = Path(root).resolve()
    skip = {e.strip().rstrip("/") for e in exclude if e.strip()} | {str((root / e).resolve()) for e in exclude if e.strip()}
    paths: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(root):
        here = Path(dirpath)
        dirnames[:] = sorted(d for d in dirnames if not _excluded(here / d, root, skip))   # prune in place
        paths += [here / f for f in filenames if Path(f).suffix.lower() in SUPPORTED]
    return [describe(p) for p in sorted(paths)]
