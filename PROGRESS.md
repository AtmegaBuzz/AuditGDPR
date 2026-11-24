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
   17 PDFs        PyMuPDF         parsers per        flag-driven    BAAI/bge      pgvector
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
Structure-aware is the default; `--fixed` selects the baseline (`--structure-aware/--fixed`).
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
**Postgres + pgvector in Docker** (`docker compose up -d`; `localhost:5432`, named volume `pgdata`). DSN via `DATABASE_URL` env (default `postgresql://auditgdpr:auditgdpr@localhost:5432/auditgdpr`). Embeddings still run on the host Metal GPU (Docker can't use it). Two tables (HNSW cosine index), so modes are A/B-comparable:
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

### [L] Synthetic company corpus (Acme Corp) — 🟡  (`synth/`)
Role-based RAG needs internal/confidential documents that don't exist, so they're generated with **Cloudflare Workers AI**
for a fictional SaaS company (Acme Beacon, Dublin EU base). 37 docs across tiers: public (0) / internal (1) / confidential (2).
```
seeds.toml ─► bible (fact sheet, tier-tagged) ─► [human review, --freeze] ─► manifest.toml (37 docs)
      ─► outline ─► sections (writer: glm-5.3) ─► code checks ─► judge (deepseek-v4-pro) ─► revise ≤2x ─► data/acme/<tier>/<id>.md
```
- **Writer only sees facts cleared for the doc's tier**; the judge sees all tiers (that asymmetry catches leakage).
- Identifier canaries: `INT-*` (internal) and `CONF-*` (confidential) ids; code checks fail any doc containing a higher-tier id,
  higher-tier people/systems, or figures that only exist in higher-tier facts. `access_level` is written from the manifest, never by the model.
- Docs generate in dependency waves (`related`); earlier docs' summaries feed later ones. Calls are cached (`artifacts/synth/cache`), runs resume.
- Failing docs land in `artifacts/synth/needs_review/` with an `.issues.txt`.
- Offline tests (no cost): `python tests/test_synth_offline.py`, `python tests/test_menu.py`.
- **Interactive menu:** run `auditgdpr` with no arguments (or `auditgdpr menu`): generate golden set / generate company docs. It detects existing output and offers *Generate new* (deletes it first, after a confirm) or *Exit*; *Continue* appears when a company-docs run is partial.
- **Not done yet:** a live run (needs `CLOUDFLARE_*` in `.env`; start with `synth bakeoff`), Markdown parser + `access_level` in the
  store/ingest, clearance filter / RLS in retrieval, role-aware golden set.

## Pipeline entry points

```bash
docker compose up -d                            # start Postgres+pgvector
uv sync
uv run auditgdpr ingest                         # (default) headers + metadata aware chunking  -> gdpr_structure_aware
uv run auditgdpr ingest --fixed                 # baseline fixed windows             -> gdpr_fixed
uv run auditgdpr ingest --structure-aware --dry-run   # chunk + export JSONL only (no GPU, no database)
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
  store.py             [F] pgvector store (psycopg, Docker)
  pipeline.py          orchestration (the flag lives here)
  cli.py               `auditgdpr ingest | search | golden | synth ...`
  synth/               [L] Acme corpus: seeds, manifest, prompts, bible, generate, validate, emit
```

## Changelog
- 2026-11-23 — interactive menu (`auditgdpr` / `auditgdpr menu`) with exists-check and generate-new/exit.
- 2026-11-23 — [L] synthetic Acme Corp corpus generator (Workers AI): bible → docs → validate; offline-tested, not yet run live.
- 2026-11-23 — Qdrant moved from embedded local mode to Docker Compose; collections re-ingested.
- 2026-11-23 — Qdrant replaced by Postgres + pgvector (Docker Compose); re-ingest required.
- 2026-11-23 — [A]–[F] + basic [G]: structure-aware vs fixed ingestion pipeline running on Metal, Qdrant populated.

## Access control (row-level security) — ✅
Every chunk carries `access_level` (0 public · 1 internal · 2 confidential), from the doc's front matter (GDPR/EDPB/WP29 PDFs = public;
unlabeled company docs = confidential, fail closed). Postgres RLS policy `clearance_read`: row visible iff `access_level <= app.clearance`.
| Role | Clearance | Sees |
|---|---|---|
| `intern` (default) | 0 | public |
| `compliance_officer` | 1 | public + internal |
| `compliance_director` | 2 | everything |
- Retrieval logs in as `auditgdpr_reader` (SELECT only, no BYPASSRLS, no access to `ingest_state`); `store.search(..., role=)` sets `app.clearance` per transaction and refuses a superuser connection.
- `uv run auditgdpr search "..." --role compliance_officer` · `uv run auditgdpr access-demo` (same query, every role) · `uv run python tests/test_rls.py`
- Ingest: `auditgdpr ingest` (data/, PDFs) and `auditgdpr ingest --root data/acme` (Markdown company docs) autodetect type by extension; incremental, `--force`/`--prune`.
