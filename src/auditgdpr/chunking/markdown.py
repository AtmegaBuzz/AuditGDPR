"""Markdown parser (company documents): body text -> Sections, same contract as legal.py / guidance.py.

  * `#` (H1) is the document title (already in the content header) and is not part of the heading path.
  * `##`..`######` build the heading path; each heading starts a new Section.
  * Blank-line separated paragraphs are Paras. Fenced code stays whole. Lists stay with their lead-in sentence.
  * Tables are never cut mid-row: they are split into row groups with the header row repeated, so every chunk
    keeps its column meaning.
  * Markdown has no pages: every Para is page 1.
"""
from __future__ import annotations

import re

from .base import Para, Section

_HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_TABLE_SEP = re.compile(r"^\s*\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
TABLE_CHARS = 1200            # ~300 tokens per row group


def _blocks(lines: list[str]):
    """Yield ('heading', level, text) | ('para', text) | ('table', [rows])."""
    buf: list[str] = []
    fence = False

    def flush():
        if buf:
            text = "\n".join(buf).strip()
            buf.clear()
            if text:
                yield ("para", text)

    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.lstrip().startswith("```"):
            fence = not fence
            buf.append(ln)
        elif fence:
            buf.append(ln)
        elif m := _HEAD.match(ln):
            yield from flush()
            yield ("heading", len(m[1]), m[2])
        elif ln.strip().startswith("|") and i + 1 < len(lines) and _TABLE_SEP.match(lines[i + 1]):
            yield from flush()
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(lines[i].rstrip())
                i += 1
            yield ("table", rows)
            continue
        elif not ln.strip():
            yield from flush()
        else:
            buf.append(ln)
        i += 1
    yield from flush()


def _table_paras(rows: list[str]) -> list[Para]:
    head, body = rows[:2], rows[2:]
    if not body:
        return [Para("\n".join(rows), 1)]
    out, cur = [], []
    for r in body:
        if cur and len("\n".join(head + cur + [r])) > TABLE_CHARS:
            out.append(Para("\n".join(head + cur), 1))
            cur = []
        cur.append(r)
    if cur:
        out.append(Para("\n".join(head + cur), 1))
    return out


def parse(body: str) -> list[Section]:
    sections: list[Section] = []
    stack: list[tuple[int, str]] = []          # (level, title) for H2+
    cur = Section(path=[], kind="front_matter")
    for blk in _blocks(body.splitlines()):
        if blk[0] == "heading":
            _, level, text = blk
            if level == 1:                      # document title
                continue
            if cur.paras:
                sections.append(cur)
            while stack and stack[-1][0] >= level:
                stack.pop()
            stack.append((level, text))
            cur = Section(path=[t for _, t in stack], kind="section")
        elif blk[0] == "table":
            cur.paras += _table_paras(blk[1])
        else:
            cur.paras.append(Para(blk[1], 1))
    if cur.paras:
        sections.append(cur)
    return sections
