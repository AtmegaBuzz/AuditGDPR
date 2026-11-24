"""Cross-encoder reranker (BAAI/bge-reranker-v2-m3 by default), run locally on Metal/MPS.

A bi-encoder (the embedder) scores query and passage separately; a cross-encoder reads them together, which is far more
precise but too slow for the whole corpus -> it only re-scores the ~40 fused candidates.
"""
from __future__ import annotations

from sentence_transformers import CrossEncoder

from . import config
from .embed import pick_device
from .store import Hit


class Reranker:
    def __init__(self, model: str = config.RERANK_MODEL, device: str = "auto"):
        self.device = pick_device(device)
        self.model = CrossEncoder(model, device=self.device, max_length=512)

    def rerank(self, query: str, hits: list[Hit], top_k: int) -> list[Hit]:
        """Return the best `top_k` hits, .score = relevance in [0, 1] (sigmoid of the cross-encoder logit)."""
        if not hits:
            return []
        pairs = [(query, _passage(h)) for h in hits]
        scores = self.model.predict(pairs, batch_size=16, activation_fn=__import__("torch").nn.Sigmoid(), show_progress_bar=False)
        ranked = sorted(zip(scores, hits), key=lambda t: t[0], reverse=True)[:top_k]
        return [Hit(float(s), {**h.payload, "fused_score": h.score}) for s, h in ranked]


def _passage(h: Hit) -> str:
    head = h.payload.get("header")
    return f"{head}\n{h.payload['text']}" if head else h.payload["text"]
