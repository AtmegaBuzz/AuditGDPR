# AuditGDPR — Progress & Architecture Map

Think of the system as a jigsaw. Each piece below has a **status**, a **contract** (what goes in / out) and
the **slot** it plugs into. When a new piece is built, flip its status and fill in its row — the picture
completes itself.

Legend: ✅ done · 🟡 partial / known gaps · ⬜ not started

```
                      ┌────────────────────────────────────────────────────────────┐
                      │                     AuditGDPR (RAG)                        │
                      └────────────────────────────────────────────────────────────┘

  [A] CORPUS ──► [B] EXTRACT ──► [C] STRUCTURE ──► [D] CHUNK ──► [E] EMBED ──► [F] STORE
   17 PDFs        PyMuPDF         parsers per        flag-driven    BAAI/bge      Qdrant
   ✅             ✅              doc profile 🟡     ✅             on Metal ✅   (local) ✅
                                                         │
                                                  --structure-aware
                                                  (headers + metadata)

  [G] RETRIEVE ───► [H] RERANK ───► [I] GENERATE ───► [J] EVAL ───► [K] API/UI
   search CLI 🟡     ⬜               ⬜                 ⬜            ⬜
```

## Pieces

### [A] Corpus — ✅
`data/` — 17 GDPR PDFs in 6 topical folders (see `README.md`). `src/auditgdpr/corpus.py` discovers them and derives
document-level metadata from the folder/file naming convention:
`doc_id, title, publisher (EU|EDPB|WP29), doc_type, profile (legal_act|guidance), category, reference, version, status`.
- **Slot:** feeds [B]. Adding a document = drop a PDF following the naming convention.

### [B] Extract — ✅  (`extract.py`)
PDF → ordered `Seg(page, text, size, bold, block)` list.
- Merges lines of one block/style into a segment; repairs hyphenation and number/title glue (`1APPLICATION` → `1 APPLICATION`).
- Drops running headers/footers (repeated margin text), footnotes (small font) and superscript footnote markers.
- GDPR text keeps small font (its `CHAPTER`/`Article` markers are 8.5pt) — `drop_small=False` for `legal_act`.

### [C] Structure parsers — 🟡  (`chunking/legal.py`, `chunking/guidance.py`)
Turn segments into `Section(path=[heading hierarchy], paras=[Para(text,page,label)])`.
| Profile | Used for | Strategy | Status |
|---|---|---|---|
| `legal_act` | GDPR regulation | Recitals `(N)`, `CHAPTER`→`Section`→`Article N — Title`, numbered paragraphs, Art. 4 definitions `(n)` | ✅ 173 recitals + 99 articles |
| `guidance` | 16 EDPB / WP29 docs | Skips title page/TOC/boilerplate; headings by font size / bold + numbering (`I.` `A.` `3.1.2` `a)`); hierarchy is learned per document with a signature stack | 🟡 |

Known gaps (candidates for next iteration):
- WP29 docs (esp. WP243, WP248): unnumbered headings → flat hierarchy; some bold lead-in sentences read as headings.
- Occasional wrong parent in deep nesting (e.g. a letter heading under a stale numbered parent in EDPB 09/2022).
- Tables / boxed examples are flattened to text.

### [D] Chunking — ✅  (`chunking/structure_aware.py`, `chunking/fixed.py`)
Selected by the pipeline flag **`--structure-aware`**.
| | `--structure-aware` (on) | default (off, baseline) |
|---|---|---|
| Boundaries | never crosses a heading; one article / section = unit; oversize paragraphs split by sentence with overlap; tiny sections merged forward | sliding 400-token window, 50 overlap |
| Content header | `"<doc title>\n<chapter > section > article>"` prepended to the embedded text | none |
| Metadata | doc info, `section_path/title/level/kind`, `page_start/end`, `para_labels` (paragraph or recital range), `article` / `chapter` / `section` for GDPR, `gdpr_articles_cited`, `chunk_in_section`, `token_count`, `header` | doc info, pages, token count |
| Budget | ≤ 450 tokens of *embedded* text (bge window = 512) | 400 tokens |

Result (BAAI tokenizer): **1,308** structure-aware chunks (tokens min/median/max 23/351/457) vs **1,258** fixed (97/400/400).

### [E] Embeddings — ✅  (`embed.py`)
`BAAI/bge-base-en-v1.5` (768-d, cosine, normalised) via sentence-transformers, **device = `mps` (Apple Metal GPU)**.
Queries use the BGE instruction prefix; documents don't. ~33 s for the full corpus.
- **Slot:** model is a CLI option (`--model BAAI/bge-m3`, `bge-large-en-v1.5`, …). Change `EMBED_DIM` handling is automatic.

### [F] Vector store — ✅  (`store.py`, `docker-compose.yml`)
**Qdrant server in Docker** (`docker compose up -d`; REST/dashboard `localhost:6333`, gRPC `6334`, named volume `qdrant_storage`). Client URL via `QDRANT_URL` env (default `http://localhost:6333`). Embeddings still run on the host Metal GPU (Docker can't use it). Two collections, so modes are A/B-comparable:
`gdpr_structure_aware`, `gdpr_fixed`. Deterministic point ids (uuid5 of `doc:index`); payload = metadata + `text`.
- Multiple processes (CLI, future API) can share the server.

### [G] Retrieval — 🟡  (`cli.py search`)
Dense top-k with optional `doc_id` filter (in `store.search`). No metadata filtering from the CLI yet, no hybrid/BM25.

### [H] Rerank — ⬜  ·  [I] Generation — ⬜  ·  [J] Evaluation — ⬜  ·  [K] API / UI — ⬜
Planned slots, contracts already implied:
- **[H]** takes top-k payloads → reordered list (cross-encoder, e.g. `BAAI/bge-reranker-*`).
- **[I]** takes question + payloads → answer with citations built from `title`, `section_path`, `page_start`, `para_labels`.
- **[J]** golden Q&A set (e.g. "72-hour breach rule → Art. 33(1)"); compare `gdpr_structure_aware` vs `gdpr_fixed` on recall@k / MRR.
  *First informal check: for "within how many hours must a breach be reported" neither mode put GDPR Art. 33 in the top 3 — needs [J] to quantify.*
- **[K]** thin service over [G]–[I].

## Pipeline entry points

```bash
docker compose up -d                            # start Qdrant
uv sync
uv run auditgdpr ingest --structure-aware      # headers + metadata aware chunking  -> gdpr_structure_aware
uv run auditgdpr ingest                         # baseline fixed windows             -> gdpr_fixed
uv run auditgdpr ingest --structure-aware --dry-run   # chunk + export JSONL only (no GPU, no Qdrant)
uv run auditgdpr ingest --only wp29 --structure-aware # subset of documents
uv run auditgdpr search "72 hour breach notification" --structure-aware --k 5
```
Chunk dumps for inspection are written to `artifacts/chunks_<mode>.jsonl` (git-ignored).

## Repo map
```
src/auditgdpr/
  config.py            paths + tunables (model, token budgets)
  corpus.py            [A] discovery + doc metadata
  extract.py           [B] PDF -> segments
  chunking/
    base.py            Section / Para / Chunk data model
    legal.py           [C] GDPR regulation parser
    guidance.py        [C] EDPB / WP29 parser
    structure_aware.py [D] headers + metadata chunker
    fixed.py           [D] baseline chunker
    tokens.py          tokenizer-accurate budgeting
  embed.py             [E] bge on MPS
  store.py             [F] Qdrant client (Docker)
  pipeline.py          orchestration (the flag lives here)
  cli.py               `auditgdpr ingest | search`
```

## Changelog
- 2026-11-23 — Qdrant moved from embedded local mode to Docker Compose; collections re-ingested.
- 2026-11-23 — [A]–[F] + basic [G]: structure-aware vs fixed ingestion pipeline running on Metal, Qdrant populated.
