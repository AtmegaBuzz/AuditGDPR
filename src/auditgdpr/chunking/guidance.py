"""Section parser for EDPB / WP29 guidance documents (font + numbering based headings)."""
from __future__ import annotations

import re

from ..extract import Seg
from .base import Para, Section

_DEC = re.compile(r"^(\d+(?:\.\d+)+|\d+)\.?\s+\S")
_ROMAN = re.compile(r"^[IVX]+\.\s+\S")
_LETTER = re.compile(r"^[A-Z]\.\s+\S")
_ALPHA = re.compile(r"^[a-z]\)\s+\S")
_NUMBERED = (_DEC, _ROMAN, _LETTER, _ALPHA)
_PARANUM = re.compile(r"^(\d{1,3})\.\s+(\S.*)$")
_LEADER = re.compile(r"\.{4,}|…{2,}")
_NOT_HEAD = re.compile(r"^(example|examples|note|footnote|adopted|version|figure|table)\b", re.I)
_TOC = re.compile(r"^(table of )?contents$", re.I)
_BULLET = re.compile(r"^[•\-–▪●○o]\s")
_START = re.compile(r"^(?:(?:\d+|[IVX]+)\.?\s+)?(executive summary|summary|introduction|preface|background)\b", re.I)
_BOILERPLATE = re.compile(r"^(the european data protection board|has adopted the following guidelines|"
                          r"the working party on the protection)", re.I)


def _signature(text: str, size: float) -> str:
    if _ROMAN.match(text):
        return "roman"
    if _LETTER.match(text):
        return "letter"
    if _ALPHA.match(text):
        return "alpha"
    if m := _DEC.match(text):
        return f"dec{m[1].count('.') + 1}"
    return f"sz{size}"


def _is_heading(s: Seg, body: float) -> bool:
    t = s.text
    if len(t) < 3 or len(t) > 160 or _NOT_HEAD.match(t) or _LEADER.search(t) or _BULLET.match(t):
        return False
    if re.fullmatch(r"[\d.\s]+", t):
        return False
    if t.endswith((".", ";", ",", ":")) and not _ROMAN.match(t):
        return False                         # sentences / numbered paragraphs end with punctuation
    larger = s.size >= body + 0.8
    boldish = s.bold and s.size >= body - 0.3 and len(t) < 120
    if boldish and not larger and not any(p.match(t) for p in _NUMBERED) and (not t[:1].isupper() or len(t) > 90):
        return False                          # bold run-in fragment, not a heading
    return larger or boldish


def _content_start(segs: list[Seg], body: float) -> int:
    """Index of the first real content seg: skips title page, version history, TOC, boilerplate."""
    toc_page = next((s.page for s in segs if _TOC.match(s.text)), None)
    first_prose_after_toc = 0
    if toc_page is not None:
        # TOC ends at the first long body-size paragraph after it
        first_prose_after_toc = next((s.page for s in segs if s.page > toc_page and len(s.text) > 250
                                      and abs(s.size - body) < 0.5 and not s.bold and not _LEADER.search(s.text)),
                                     toc_page)
    for i, s in enumerate(segs):
        if s.page < max(first_prose_after_toc - 1, 0) and toc_page is not None:
            continue
        if _is_heading(s, body) and _START.match(s.text) and (toc_page is None or s.page > toc_page):
            return i
    # fallback: content begins right after the "HAS ADOPTED THE FOLLOWING GUIDELINES" boilerplate
    for i, s in enumerate(segs):
        if re.match(r"has adopted the following guidelines", s.text, re.I):
            return i + 1
    return 0


def parse(segs: list[Seg], body: float) -> list[Section]:
    start = _content_start(segs, body)
    segs = segs[start:]
    sections: list[Section] = []
    stack: list[tuple[str, str]] = []           # (signature, heading text)
    cur: Section | None = None
    last_head: Seg | None = None

    for s in segs:
        t = s.text
        if _BOILERPLATE.match(t) or _TOC.match(t):
            continue
        if _is_heading(s, body):
            # a wrapped heading line: same style as the previous heading, no numbering, no body yet
            if (last_head and cur is not None and not cur.paras and stack
                    and s.page - last_head.page <= 1
                    and (s.size, s.bold) == (last_head.size, last_head.bold)
                    and not any(p.match(t) for p in _NUMBERED)):
                stack[-1] = (stack[-1][0], f"{stack[-1][1]} {t}")
                cur.path[-1] = stack[-1][1]
                continue
            sig = _signature(t, s.size)
            idx = next((i for i, (g, _) in enumerate(stack) if g == sig), None)
            if idx is not None:
                stack = stack[:idx]
            stack.append((sig, t))
            cur = Section(path=[h for _, h in stack])
            sections.append(cur)
            last_head = s
            continue
        if _LEADER.search(t):
            continue
        if cur is None:
            cur = Section(path=["Preamble"], kind="front_matter")
            sections.append(cur)
        m = _PARANUM.match(t)
        label = m[1] if m else None
        body_text = m[2] if m else t
        if cur.paras and not m and not _BULLET.match(t):
            prev = cur.paras[-1]
            if prev.text[-1:] not in ".:;?!”\")" and t[:1].islower():     # continuation across a block/page break
                prev.text += " " + t
                continue
        cur.paras.append(Para(body_text, s.page, label))
    return [x for x in sections if x.paras]
