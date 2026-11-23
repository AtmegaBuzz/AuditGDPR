"""Disk-cached, thread-safe wrapper around WorkersAI. Reruns are free and reproducible; keys include the model,
prompts and sampling params. `backend` can be any object with chat_text / chat_json (used by offline tests)."""
from __future__ import annotations

import hashlib
import json
import os
import threading
from pathlib import Path

from .. import config


class CachedLLM:
    def __init__(self, model: str, backend=None, cache_dir: Path | None = None):
        self.model = model
        self.cache_dir = Path(cache_dir or config.SYNTH_DIR / "cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        if backend is None:
            from ..golden.cloudflare import WorkersAI
            backend = WorkersAI(model, timeout=300)
        self.backend = backend
        self.calls = self.hits = 0
        self._lock = threading.Lock()

    def _key(self, kind: str, system: str, user: str, extra: dict) -> Path:
        h = hashlib.sha256(json.dumps([self.model, kind, system, user, extra], sort_keys=True).encode()).hexdigest()
        return self.cache_dir / f"{h}.json"

    def _cached(self, path: Path, produce):
        if path.exists():
            with self._lock:
                self.hits += 1
            return json.loads(path.read_text())["out"]
        out = produce()
        with self._lock:
            self.calls += 1
        tmp = path.with_suffix(f".{os.getpid()}.{threading.get_ident()}.tmp")
        tmp.write_text(json.dumps({"model": self.model, "out": out}, ensure_ascii=False))
        tmp.replace(path)
        return out

    def text(self, system: str, user: str, max_tokens: int = 4096, temperature: float = 0.7) -> str:
        p = self._key("text", system, user, {"m": max_tokens, "t": temperature})
        return self._cached(p, lambda: self.backend.chat_text(system, user, max_tokens, temperature))

    def json(self, system: str, user: str, schema: dict, max_tokens: int = 2048, temperature: float = 0.4) -> dict:
        p = self._key("json", system, user, {"m": max_tokens, "t": temperature, "s": schema})
        return self._cached(p, lambda: self.backend.chat_json(system, user, schema, max_tokens, temperature))
