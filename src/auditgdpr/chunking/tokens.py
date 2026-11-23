"""Token accounting against the embedding model's own tokenizer."""
from __future__ import annotations

from functools import cached_property

from transformers import AutoTokenizer


class Tok:
    def __init__(self, model_name: str):
        self.model_name = model_name

    @cached_property
    def _tok(self):
        t = AutoTokenizer.from_pretrained(self.model_name)
        t.model_max_length = 10**9          # we window ourselves; silence the length warning
        return t

    def count(self, text: str) -> int:
        return len(self._tok.encode(text, add_special_tokens=False))

    def offsets(self, text: str) -> list[tuple[int, int]]:
        enc = self._tok(text, add_special_tokens=False, return_offsets_mapping=True)
        return [o for o in enc["offset_mapping"]]
