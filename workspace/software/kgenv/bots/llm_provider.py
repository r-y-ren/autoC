"""Pluggable LLM decision provider -- DEFAULT OFF.

Compliance context (competition rules, captured 2026-08-28 via the official
Kaggle ListPages API):

  * "The use of external data and models is acceptable unless specifically
    prohibited by the Host." -- external models are permitted here.
  * Reasonableness Standard: "a small subscription charge to use additional
    elements of a large language model such as Gemini Advanced are
    acceptable if meeting the Reasonableness Standard" -- i.e. modest LLM
    subscription costs are fine; costs exceeding the prize pool are not.

Design (following the ProgRouter cost-routing idea, kb/tech/arxiv-2608.25992):
  * The provider is an OPTIONAL consultant. It never blocks, never throws
    into the game loop: on any error or timeout it returns None and the
    heuristic policy decides alone.
  * A strict budget guard (max calls per episode, per-call timeout) applies
    the Reasonableness Standard mechanically, echoing the Bayesian
    self-escalation control of kb/tech/arxiv-2608.24087.
  * Default provider is NullProvider (disabled). Enable explicitly with
    KG_LLM_PROVIDER=openai_compat plus KG_LLM_BASE_URL / KG_LLM_API_KEY /
    KG_LLM_MODEL environment variables.

NOT wired into the submission bot: main.py's agent() never requires this
module. It exists for local A/B experiments on whether an LLM consultant
improves sell-timing / crop-mix decisions over the heuristic policy.
"""

from __future__ import annotations

import json
import os
import time
import urllib.request
import urllib.error
from typing import Any, Dict, Optional, Protocol


class LLMProvider(Protocol):
    name: str

    def suggest(self, prompt: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        ...


class NullProvider:
    """Disabled provider: always declines to answer (default)."""

    name = "null"

    def suggest(self, prompt: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return None


class Budget:
    """Reasonableness Standard guard: call budget + wall-clock budget."""

    def __init__(self, max_calls: int, max_seconds: float):
        self.max_calls = max_calls
        self.max_seconds = max_seconds
        self.calls = 0
        self.seconds = 0.0

    @property
    def exhausted(self) -> bool:
        return self.calls >= self.max_calls or self.seconds >= self.max_seconds

    def spend(self, dt: float) -> None:
        self.calls += 1
        self.seconds += dt


class OpenAICompatProvider:
    """OpenAI-compatible chat completion provider (local or remote).

    Reads KG_LLM_BASE_URL, KG_LLM_API_KEY, KG_LLM_MODEL from the
    environment. Every call is bounded by the budget and a hard timeout;
    failures degrade to None (heuristic fallback).
    """

    name = "openai_compat"

    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None,
                 model: Optional[str] = None, timeout_s: float = 4.0,
                 max_calls: int = 8, max_seconds: float = 30.0):
        self.base_url = (base_url or os.environ.get("KG_LLM_BASE_URL", "")).rstrip("/")
        self.api_key = api_key or os.environ.get("KG_LLM_API_KEY", "")
        self.model = model or os.environ.get("KG_LLM_MODEL", "")
        self.timeout_s = timeout_s
        self.budget = Budget(max_calls, max_seconds)

    @property
    def configured(self) -> bool:
        return bool(self.base_url and self.model)

    def suggest(self, prompt: str, context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if not self.configured or self.budget.exhausted:
            return None
        body = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": (
                    "You are a farming-simulation strategy consultant. "
                    "Answer ONLY with a JSON object matching the requested schema.")},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 256,
        }).encode("utf-8")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions", data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}"},
            method="POST",
        )
        t0 = time.perf_counter()
        try:
            with urllib.request.urlopen(req, timeout=self.timeout_s) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
            content = payload["choices"][0]["message"]["content"]
            return json.loads(content)
        except (urllib.error.URLError, TimeoutError, KeyError, ValueError, json.JSONDecodeError):
            return None  # degrade to heuristic decision
        finally:
            self.budget.spend(time.perf_counter() - t0)


def provider_from_env() -> LLMProvider:
    """Factory: KG_LLM_PROVIDER unset/'null' -> NullProvider (default off)."""
    kind = os.environ.get("KG_LLM_PROVIDER", "null").strip().lower()
    if kind in ("", "null", "off", "none"):
        return NullProvider()
    if kind == "openai_compat":
        return OpenAICompatProvider()
    raise ValueError(f"unknown KG_LLM_PROVIDER: {kind!r}")
