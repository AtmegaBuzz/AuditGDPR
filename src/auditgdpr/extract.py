"""PDF -> clean, style-annotated text segments (no structure decisions here)."""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass

import pymupdf


@dataclass
class Seg:
    page: int            # 1-based
    text: str
    size: float
    bold: bool
    block: int


_JUNK = re.compile(r"^(\d+|page \d+( of \d+)?|EN|L \d+/\d+|\d{1,2}\.\d{1,2}\.\d{4}|Official Journal of the European Union)$", re.I)


def _norm(t: str) -> str:
    return re.sub(r"\d+", "#", t.strip().lower())


def extract(path: str, drop_small: bool = True) -> tuple[list[Seg], float]:
    """Return (segments in reading order, dominant body font size)."""
    doc = pymupdf.open(path)
    raw: list[tuple[int, int, str, float, bool, float, float, float]] = []
    sizes: Counter[float] = Counter()
    for pno, page in enumerate(doc, 1):
        h = page.rect.height
        for bno, b in enumerate(page.get_text("dict")["blocks"]):
            for ln in b.get("lines", []):
                spans = [s for s in ln["spans"] if s["text"].strip()]
                if not spans:
                    continue
                dom = max(spans, key=lambda s: len(s["text"]))
                # drop superscript footnote markers ("damage13." -> "damage.")
                spans = [s for s in spans if not (s["size"] < dom["size"] * 0.8 and s["text"].strip().isdigit())]
                parts, prev_x1 = [], None
                for sp in spans:
                    if prev_x1 is not None and sp["bbox"][0] - prev_x1 > 1.5 and not parts[-1].endswith(" "):
                        parts.append(" ")
                    parts.append(sp["text"])
                    prev_x1 = sp["bbox"][2]
                text = "".join(parts).strip()
                if not text:
                    continue
                bold = "bold" in dom["font"].lower() or bool(dom["flags"] & 16)
                size = round(dom["size"], 1)
                raw.append((pno, bno, text, size, bold, ln["bbox"][1], ln["bbox"][3], h))
                sizes[size] += len(text)
    body = sizes.most_common(1)[0][0]

    # page furniture: margin lines that repeat across pages, or are bare numbers etc.
    pages = max(1, len(doc))
    margin_counts: Counter[str] = Counter()
    for pno, _, text, _, _, y0, y1, h in raw:
        if y0 < 0.07 * h or y1 > 0.93 * h:
            margin_counts[_norm(text)] += 1
    furniture = {k for k, c in margin_counts.items() if c >= max(3, 0.25 * pages)}

    segs: list[Seg] = []
    for pno, bno, text, size, bold, y0, y1, h in raw:
        in_margin = y0 < 0.07 * h or y1 > 0.93 * h
        if in_margin and (_norm(text) in furniture or _JUNK.match(text)):
            continue
        if _JUNK.match(text) and len(text) < 12:
            continue
        if drop_small and size < body - 1.0:   # footnotes / small print
            continue
        key = (pno, bno, size, bold)
        if segs and (segs[-1].page, segs[-1].block, segs[-1].size, segs[-1].bold) == key:
            prev = segs[-1].text
            segs[-1].text = (prev[:-1] + text) if (prev.endswith("-") and text[:1].islower()) else f"{prev} {text}"
        else:
            segs.append(Seg(pno, text, size, bold, bno))
    for s in segs:
        s.text = re.sub(r"\s+", " ", s.text).strip()
    return [s for s in segs if s.text], body
