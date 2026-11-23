"""Minimal Cloudflare Workers AI REST client (stdlib only).

Credentials come from CLOUDFLARE_ACCOUNT_ID / CLOUDFLARE_API_TOKEN (env or a .env file at the repo root).

  chat_json  one call constrained to a JSON schema (falls back to prompt-only JSON if the model rejects response_format)
  chat_text  one call returning prose (used for long Markdown generation)
"""
from __future__ import annotations

import json
import logging
import os
import random
import re
import time
import urllib.error
import urllib.request

from .. import config

log = logging.getLogger("auditgdpr.ai")

API = "https://api.cloudflare.com/client/v4/accounts/{account}/ai/run/{model}"


def load_dotenv(path=config.ROOT / ".env") -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))


def extract_text(result) -> str | dict:
    """Pull the model output out of the several response shapes Workers AI models use."""
    if isinstance(result, str):
        return result
    if not isinstance(result, dict):
        raise TypeError(f"unexpected result type {type(result)}")
    if result.get("response") is not None:
        return result["response"]
    if result.get("choices"):                                  # OpenAI-compatible models
        msg = result["choices"][0].get("message") or {}
        if msg.get("content") is not None:
            return msg["content"]
        if result["choices"][0].get("text") is not None:
            return result["choices"][0]["text"]
    if result.get("output_text"):                              # Responses-API style
        return result["output_text"]
    for item in result.get("output") or []:
        for part in (item.get("content") or []) if isinstance(item, dict) else []:
            if isinstance(part, dict) and part.get("type") in ("output_text", "text") and part.get("text"):
                return part["text"]
    raise TypeError(f"no text in result keys={list(result)}")


def parse_json_loose(text: str | dict):
    """Parse JSON from model output that may be wrapped in prose or ``` fences."""
    if isinstance(text, dict):
        return text
    s = text.strip()
    s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        i, j = s.find("{"), s.rfind("}")
        if i >= 0 and j > i:
            return json.loads(s[i:j + 1])
        raise


def _preview(obj, n: int = 600) -> str:
    t = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, default=str)
    return t if len(t) <= n else t[:n] + f"...[+{len(t) - n} chars]"


def _short(model: str) -> str:
    return model.rsplit("/", 1)[-1]


def _finish_reason(result) -> str | None:
    if isinstance(result, dict) and result.get("choices"):
        return result["choices"][0].get("finish_reason")
    return None


class WorkersAI:
    def __init__(self, model: str, retries: int = 5, timeout: int = 120):
        load_dotenv()
        self.account = os.environ.get("CLOUDFLARE_ACCOUNT_ID")
        self.token = os.environ.get("CLOUDFLARE_API_TOKEN")
        if not self.account or not self.token:
            raise RuntimeError("Set CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN (env or .env).")
        self.model, self.retries, self.timeout = model, retries, timeout

    # Reasoning models (glm, gpt-oss, deepseek) can burn the whole max_tokens budget "thinking" and return empty content
    # (finish_reason=length). Ask them to think little; drop these knobs if the model rejects them.
    _THINK_OFF = {"reasoning_effort": "low", "chat_template_kwargs": {"enable_thinking": False}}

    def _post(self, body: dict):
        if not getattr(self, "_think_rejected", False):
            body = {**self._THINK_OFF, **body}
            try:
                return self._post_raw(body)
            except RuntimeError as e:
                if not str(e).startswith("HTTP 400"):
                    raise
                log.info("model has no reasoning-off option, continuing without it")
                log.debug("400 body: %s", e)
                self._think_rejected = True
                body = {k: v for k, v in body.items() if k not in self._THINK_OFF}
        return self._post_raw(body)

    def _post_raw(self, body: dict):
        """POST with retry on transient errors; returns payload['result']. 4xx (except 408/429) raise RuntimeError('HTTP n: ...')."""
        req = urllib.request.Request(
            API.format(account=self.account, model=self.model), data=json.dumps(body).encode(),
            headers={"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"})
        last: Exception | None = None
        for attempt in range(self.retries):
            t0 = time.time()
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as r:
                    payload = json.load(r)
                if not payload.get("success", True):
                    raise RuntimeError(f"Workers AI error: {payload.get('errors')}")
                log.debug("raw result: %s", _preview(payload["result"], 3000))
                log.info("ok %s %.1fs finish=%s", _short(self.model), time.time() - t0, _finish_reason(payload["result"]) or "-")
                return payload["result"]
            except urllib.error.HTTPError as e:
                last = e
                log.warning("HTTP %s from %s (try %d/%d)", e.code, _short(self.model), attempt + 1, self.retries)
                if e.code not in (408, 429, 500, 502, 503, 504):
                    raise RuntimeError(f"HTTP {e.code}: {e.read().decode()[:300]}") from e
            except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, TypeError) as e:
                last = e
                log.warning("%s: %s (try %d/%d)", type(e).__name__, e, attempt + 1, self.retries)
            time.sleep(min(30, 2 ** attempt) + random.random())
        raise RuntimeError(f"Workers AI call failed after {self.retries} attempts: {last}")

    @staticmethod
    def _messages(system: str, user: str) -> list[dict]:
        return [{"role": "system", "content": system}, {"role": "user", "content": user}]

    def chat_json(self, system: str, user: str, schema: dict, max_tokens: int = 1024, temperature: float = 0.4) -> dict:
        """One chat call constrained to a JSON schema; returns the parsed object."""
        body = {
            "messages": self._messages(system, user),
            "response_format": {"type": "json_schema", "json_schema": schema},
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        last: Exception | None = None
        base_tokens = max_tokens
        for attempt in range(self.retries):      # bad/empty/truncated JSON from the model: re-ask (retries inside _post cover HTTP)
            try:
                try:
                    log.info("ask %s json max_tokens=%d%s", _short(self.model), body["max_tokens"], "" if "response_format" in body else " (prompt-only)")
                    result = self._post(body)
                except RuntimeError as e:
                    if str(e).startswith("HTTP 400") and "response_format" in body:   # model has no JSON mode: prompt-only
                        log.info("model has no JSON mode, switching to prompt-only JSON")
                        self._prompt_only(body, system, user, schema)
                        result = self._post(body)
                    else:
                        raise
                text = extract_text(result)
                if not (text.strip() if isinstance(text, str) else text):
                    # Empty content: usually a reasoning model that spent the whole budget thinking, or JSON mode misbehaving.
                    raise TypeError(f"empty model output (finish_reason={_finish_reason(result)})")
                return parse_json_loose(text)
            except (json.JSONDecodeError, TypeError) as e:
                last = e
                log.warning("bad output, try %d/%d: %s", attempt + 1, self.retries, e)
                log.warning("  raw: %s", _preview(locals().get("text", ""), 500))
                body["max_tokens"] = min(int(body["max_tokens"] * 1.5), base_tokens * 4)    # maybe truncated / thinking ate the budget
                if attempt >= 1 and "response_format" in body:                              # JSON mode keeps failing: try prompt-only
                    log.info("JSON mode keeps failing, switching to prompt-only JSON")
                    self._prompt_only(body, system, user, schema)
        raise RuntimeError(f"no valid JSON after {self.retries} attempts: {last}")

    def _prompt_only(self, body: dict, system: str, user: str, schema: dict) -> None:
        body.pop("response_format", None)
        body["messages"] = self._messages(
            system + "\n\nReply with ONLY a JSON object matching this JSON schema, no prose:\n"
            + json.dumps(schema.get("schema", schema)), user)

    def chat_text(self, system: str, user: str, max_tokens: int = 4096, temperature: float = 0.7) -> str:
        """One chat call returning prose."""
        result = self._post({"messages": self._messages(system, user), "max_tokens": max_tokens, "temperature": temperature})
        out = extract_text(result)
        return out if isinstance(out, str) else json.dumps(out)
