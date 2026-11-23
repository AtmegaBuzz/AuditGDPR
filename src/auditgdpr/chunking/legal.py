"""Section parser for the GDPR text itself: recitals, chapters, sections, articles."""
from __future__ import annotations

import re

from ..extract import Seg
from .base import Para, Section

_RECITAL = re.compile(r"^\((\d{1,3})\)\s+(.*)$")
_CHAPTER = re.compile(r"^CHAPTER\s+([IVXL]+)$")
_SECTION = re.compile(r"^Section\s+(\d+)$")
_ARTICLE = re.compile(r"^Article\s+(\d+)$")
_PARA = re.compile(r"^(\d{1,2})\.\s+(.*)$")
_SUBPOINT = re.compile(r"^\(([a-z]{1,2}|[ivx]+)\)\s")
_ADOPTED = "HAVE ADOPTED THIS REGULATION"


def parse(segs: list[Seg]) -> list[Section]:
    sections: list[Section] = []
    chapter = chapter_title = section = section_title = None
    cur: Section | None = None
    in_body = False
    pending: tuple[str, str] | None = None     # (kind, label) awaiting its title line

    recitals = Section(path=["Recitals"], kind="recitals")
    sections.append(recitals)
    cur = recitals

    def path() -> list[str]:
        p = []
        if chapter:
            p.append(f"Chapter {chapter} — {chapter_title}")
        if section:
            p.append(f"Section {section} — {section_title}")
        return p

    body_size = max({x.size for x in segs}, key=lambda z: sum(len(x.text) for x in segs if x.size == z))
    structural = re.compile(r"^(CHAPTER [IVXL]+|Section \d+|Article \d+|HAVE ADOPTED)")
    for s in segs:
        t = s.text
        if s.size < body_size - 1.0 and not structural.match(t):   # footnotes
            continue
        if not in_body:
            if _ADOPTED in t:
                in_body = True
                continue
            if m := _RECITAL.match(t):
                recitals.paras.append(Para(m[2], s.page, f"({m[1]})"))
            elif recitals.paras and t[:1].islower() | (recitals.paras[-1].text[-1:] not in ".;:"):
                recitals.paras[-1].text += " " + t       # continuation
            elif recitals.paras:
                recitals.paras[-1].text += " " + t
            continue

        if pending:
            kind, label = pending
            pending = None
            if kind == "chapter":
                chapter, chapter_title, section, section_title = label, t, None, None
            elif kind == "section":
                section, section_title = label, t
            else:  # article
                cur = Section(path=path() + [f"Article {label} — {t}"], kind="article",
                              extra={"article": label, "chapter": chapter, "section": section})
                sections.append(cur)
            continue
        if m := _CHAPTER.match(t):
            pending = ("chapter", m[1]); continue
        if m := _SECTION.match(t):
            pending = ("section", m[1]); continue
        if m := _ARTICLE.match(t):
            pending = ("article", m[1]); continue
        if cur is None or cur.kind != "article":
            continue
        if cur.extra.get("article") == "4" and (m := re.match(r"^\((\d{1,2})\)\s+(.*)$", t)):
            cur.paras.append(Para(m[2], s.page, f"({m[1]})"))
        elif m := _PARA.match(t):
            cur.paras.append(Para(m[2], s.page, m[1]))
        elif re.fullmatch(r"\d{1,2}\.", t):                 # "1." alone on a line: text follows
            cur.paras.append(Para("", s.page, t[:-1]))
        elif cur.paras and not cur.paras[-1].text:
            cur.paras[-1].text = t
        elif _SUBPOINT.match(t) or not cur.paras:
            if cur.paras:
                cur.paras[-1].text += "\n" + t
            else:
                cur.paras.append(Para(t, s.page))
        else:
            cur.paras[-1].text += " " + t
    return [s for s in sections if s.paras]
