"""Structure-aware chunking.

Input : Sections (heading path + paragraphs) produced by the parsers in legal.py / guidance.py.
Output: Chunks that never cross a heading boundary, each carrying
          * a content header  (document title + full heading path) prepended to the embedded text
          * rich metadata     (doc, hierarchy, pages, paragraph/recital labels, GDPR articles cited)
"""
from __future__ import annotations

import re
import uuid

from ..corpus import DocMeta
from .base import Chunk, Para, Section
from .tokens import Tok

_SENT = re.compile(r"(?<=[.!?;:])\s+(?=[A-Z(“‘\"'])")
_ART = re.compile(
    r"\bArt(?:icles?|s?\.)\s*(\d{1,3})(?:\(\d+\))?(?:\s?\([a-z]\))?"
    r"((?:\s*(?:,|and|to|–|-)\s*\d{1,3}(?:\(\d+\))?(?:\s?\([a-z]\))?)*)"
    r"(?!\s*(?:TFEU|TEU|of (?:the )?(?:Directive|Charter|Treaty|Regulation \(EC\)|Convention)))")


def articles_cited(text: str) -> list[int]:
    found: set[int] = set()
    for m in _ART.finditer(text):
        found.add(int(m[1]))
        found.update(int(n) for n in re.findall(r"(?<![(\d])(\d{1,3})(?![\d)])", m[2] or ""))
    return sorted(a for a in found if 1 <= a <= 99)


def _header(doc: DocMeta, path: list[str]) -> str:
    return f"{doc.title}\n{' > '.join(path)}" if path else doc.title


def _merge_tiny(sections: list[Section], tok: Tok, min_tokens: int) -> list[Section]:
    """Fold heading-only / near-empty sections into the section that follows them."""
    out: list[Section] = []
    carry: list[Para] = []
    for i, sec in enumerate(sections):
        body = sum(tok.count(p.text) for p in sec.paras)
        nxt = sections[i + 1] if i + 1 < len(sections) else None
        if sec.kind == "section" and body < min_tokens and nxt is not None and nxt.kind == "section":
            is_parent = nxt.path[:len(sec.path)] == sec.path
            for p in sec.paras:
                carry.append(Para(p.text if is_parent else f"{sec.path[-1]}: {p.text}", p.page, p.label))
            continue
        if carry:
            sec = Section(sec.path, carry + sec.paras, sec.kind, sec.extra)
            carry = []
        out.append(sec)
    return out


def _split_long(text: str, budget: int, overlap: int, tok: Tok) -> list[str]:
    """Sentence-level split of one oversize paragraph, with a small sentence overlap."""
    sents = [s for s in _SENT.split(text) if s.strip()]
    pieces: list[str] = []
    cur: list[str] = []
    cur_tok = 0
    for s in sents:
        n = tok.count(s)
        if n > budget:                                   # pathological sentence: hard split by words
            words, buf = s.split(), []
            for w in words:
                buf.append(w)
                if tok.count(" ".join(buf)) > budget:
                    pieces.append(" ".join(buf[:-1]))
                    buf = [w]
            s, n = " ".join(buf), tok.count(" ".join(buf))
        if cur and cur_tok + n > budget:
            pieces.append(" ".join(cur))
            tail: list[str] = []
            t = 0
            for prev in reversed(cur):
                pt = tok.count(prev)
                if t + pt > overlap:
                    break
                tail.insert(0, prev)
                t += pt
            cur, cur_tok = tail, t
        cur.append(s)
        cur_tok += n
    if cur:
        pieces.append(" ".join(cur))
    return pieces


def _label_range(paras: list[Para]) -> str | None:
    labels = [p.label for p in paras if p.label]
    if not labels:
        return None
    return labels[0] if labels[0] == labels[-1] else f"{labels[0]}–{labels[-1]}"


def chunk_document(doc: DocMeta, sections: list[Section], tok: Tok,
                   max_tokens: int, min_tokens: int, overlap: int) -> list[Chunk]:
    sections = _merge_tiny(sections, tok, min_tokens)
    chunks: list[Chunk] = []
    for sec in sections:
        header = _header(doc, sec.path)
        budget = max_tokens - tok.count(header) - 4
        # explode oversize paragraphs, keeping label/page
        units: list[tuple[Para, int]] = []
        for p in sec.paras:
            n = tok.count(p.text)
            if n > budget:
                units += [(Para(piece, p.page, p.label), tok.count(piece))
                          for piece in _split_long(p.text, budget, overlap, tok)]
            else:
                units.append((p, n))
        groups: list[list[Para]] = []
        cur: list[Para] = []
        cur_tok = 0
        for p, n in units:
            if cur and cur_tok + n > budget:
                groups.append(cur)
                cur, cur_tok = [], 0
            cur.append(p)
            cur_tok += n
        if cur:
            groups.append(cur)

        for gi, g in enumerate(groups):
            body = "\n".join((f"{p.label} " if p.label and sec.kind == "recitals" else "") + p.text for p in g)
            if sec.kind == "article":
                body = "\n".join((f"{p.label}. " if p.label and not p.label.startswith("(") else
                                  f"{p.label} " if p.label else "") + p.text for p in g)
            embed_text = f"{header}\n\n{body}"
            idx = len(chunks)
            chunk_key = f"{doc.doc_id}:{idx}"
            md = {
                **doc.to_payload(),
                "chunking": "structure_aware",
                "section_kind": sec.kind,
                "section_path": sec.path,
                "section_title": sec.path[-1] if sec.path else None,
                "section_level": sec.level,
                "chunk_in_section": gi + 1,
                "chunks_in_section": len(groups),
                "page_start": min(p.page for p in g),
                "page_end": max(p.page for p in g),
                "para_labels": _label_range(g),
                "gdpr_articles_cited": articles_cited(body),
                "header": header,
                "token_count": tok.count(embed_text),
                **{k: v for k, v in sec.extra.items() if v is not None},
            }
            if sec.kind == "recitals":
                md["recital_range"] = md["para_labels"]
            chunks.append(Chunk(str(uuid.uuid5(uuid.NAMESPACE_URL, chunk_key)), doc.doc_id, idx, body, embed_text, md))
    return chunks
