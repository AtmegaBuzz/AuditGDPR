"""Central configuration: paths and defaults. Everything tunable lives here."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"


def _load_dotenv(path: Path = ROOT / ".env") -> None:
    """Load KEY=VALUE lines from the repo's .env into os.environ (real env vars win)."""
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


_load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://auditgdpr:auditgdpr@localhost:5432/auditgdpr")   # pgvector runs in Docker (docker-compose.yml)
DEFAULT_EXCLUDE = ("acme",)               # folders never ingested unless --exclude is overridden
EXPORT_DIR = ROOT / "artifacts"          # chunk dumps for inspection
GOLDEN_DIR = EXPORT_DIR / "golden"       # golden evaluation sets
GOLDEN_MODEL = "@cf/meta/llama-3.3-70b-instruct-fp8-fast"   # Cloudflare Workers AI

# --- Synthetic company corpus (Acme Corp) -------------------------------------------------------
ACME_DIR = DATA_DIR / "acme"                  # generated docs: acme/{public,internal,confidential}/<doc_id>.md
SYNTH_DIR = EXPORT_DIR / "synth"              # caches, drafts, needs_review, run logs
SYNTH_WRITER_MODEL = "@cf/zai-org/glm-5.3"                       # long-context writer
SYNTH_JUDGE_MODEL = "@cf/openai/gpt-oss-120b"                    # different family than the writer (deepseek-v4-pro-0813 was deprecated 2026-11-20)
SYNTH_FALLBACK_MODEL = "@cf/openai/gpt-oss-120b"
TIERS = {0: "public", 1: "internal", 2: "confidential"}

EMBED_MODEL = "BAAI/bge-base-en-v1.5"   # 768-d, 512-token window
EMBED_DIM = 768
QUERY_PREFIX = "Represent this sentence for searching relevant passages: "  # BGE query instruction

# Chunk budget is measured on the *embedded* text (header + body) in model tokens.
MAX_CHUNK_TOKENS = 450       # hard ceiling (model window is 512)
MIN_SECTION_TOKENS = 60      # structure-aware: smaller sections get merged forward
OVERLAP_TOKENS = 50          # only used when a single paragraph must be split / fixed chunking
FIXED_CHUNK_TOKENS = 400     # baseline (non structure-aware) window

EMBED_BATCH = 32


def collection_name(structure_aware: bool) -> str:
    return "gdpr_structure_aware" if structure_aware else "gdpr_fixed"
