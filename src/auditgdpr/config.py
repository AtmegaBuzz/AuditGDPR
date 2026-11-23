"""Central configuration: paths and defaults. Everything tunable lives here."""
from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
QDRANT_URL = os.environ.get("QDRANT_URL", "http://localhost:6333")   # Qdrant runs in Docker (docker-compose.yml)
EXPORT_DIR = ROOT / "artifacts"          # chunk dumps for inspection

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
