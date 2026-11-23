"""Baseline chunking (flag off): structure-blind sliding token window. No headers, minimal metadata."""
from __future__ import annotations

import bisect
import uuid

from ..corpus import DocMeta
from ..extract import Seg
from .base import Chunk
from .tokens import Tok


def chunk_document(doc: DocMeta, segs: list[Seg], tok: Tok, window: int, overlap: int) -> list[Chunk]:
    text_parts, page_starts, pages, pos = [], [], [], 0
    for s in segs:
        page_starts.append(pos)
        pages.append(s.page)
        text_parts.append(s.text)
        pos += len(s.text) + 1
    text = "\n".join(text_parts)
    offs = tok.offsets(text)
    chunks: list[Chunk] = []
    step = window - overlap
    for i in range(0, len(offs), step):
        win = offs[i:i + window]
        a, b = win[0][0], win[-1][1]
        body = text[a:b]
        p0 = pages[max(0, bisect.bisect_right(page_starts, a) - 1)]
        p1 = pages[max(0, bisect.bisect_right(page_starts, b - 1) - 1)]
        idx = len(chunks)
        md = {**doc.to_payload(), "chunking": "fixed", "page_start": p0, "page_end": p1, "token_count": len(win)}
        chunks.append(Chunk(str(uuid.uuid5(uuid.NAMESPACE_URL, f"{doc.doc_id}:fixed:{idx}")), doc.doc_id, idx, body, body, md))
        if i + window >= len(offs):
            break
    return chunks
