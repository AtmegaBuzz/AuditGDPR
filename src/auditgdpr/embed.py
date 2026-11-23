"""BAAI/bge embeddings, run locally on the Apple-silicon GPU (Metal / MPS)."""
from __future__ import annotations

import torch
from sentence_transformers import SentenceTransformer

from .config import EMBED_BATCH, QUERY_PREFIX


def pick_device(requested: str = "auto") -> str:
    if requested != "auto":
        return requested
    return "mps" if torch.backends.mps.is_available() else "cpu"


class Embedder:
    def __init__(self, model_name: str, device: str = "auto"):
        self.device = pick_device(device)
        self.model = SentenceTransformer(model_name, device=self.device)
        self.model.max_seq_length = 512
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: list[str], progress: bool = True) -> list[list[float]]:
        vecs = self.model.encode(texts, batch_size=EMBED_BATCH, normalize_embeddings=True,
                                 show_progress_bar=progress, convert_to_numpy=True)
        return vecs.tolist()

    def embed_query(self, query: str) -> list[float]:
        return self.model.encode(QUERY_PREFIX + query, normalize_embeddings=True).tolist()
