"""Kaggle bundle entry point. Configuration and weights live beside this file."""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys
import traceback

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
_agent = None


def bundle_root(configuration=None) -> Path:
    entry = globals().get("__file__")
    if entry is None and configuration is not None:
        entry = (
            configuration.get("__raw_path__")
            if hasattr(configuration, "get")
            else getattr(configuration, "__raw_path__", None)
        )
    candidates = [Path(entry).resolve().parent] if entry else []
    candidates.append(Path("/kaggle_simulations/agent"))
    for root in candidates:
        if (root / "agent.json").is_file() and (root / "model_jax.pkl").is_file():
            return root
    raise FileNotFoundError("agent.json and model_jax.pkl must be in the bundle root")


def agent(observation, configuration=None):
    global _agent
    try:
        if _agent is None:
            root = bundle_root(configuration)
            sys.path.insert(0, str(root))
            from kaggriculture.agents.final import FinalAgent

            settings = json.loads((root / "agent.json").read_text())
            _agent = FinalAgent(
                root / "model_jax.pkl", settings["variant"], heuristic_settings=settings.get("heuristics")
            )
        return _agent(observation, configuration)
    except Exception:
        if os.environ.get("KAGGRICULTURE_RAISE_AGENT_ERRORS") == "1":
            raise
        traceback.print_exc(file=sys.stderr)
        return {"farmer": ["PASS"], "hands": [], "market": []}
