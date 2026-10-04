"""Fail-closed behavior-probability checks with reproducible failure evidence."""

from __future__ import annotations

import gzip
import os
import pickle
import time
from pathlib import Path
from typing import Any

import jax
import numpy as np


def verification_indices(transitions: int, budget: int) -> np.ndarray:
    """Keep both seats together and spread a fixed probe across the full rollout."""
    if transitions < 2 or transitions % 2 or budget < 2 or budget % 2:
        raise ValueError("parity probes require complete seat pairs")
    pairs = np.linspace(0, transitions // 2 - 1, min(transitions, budget) // 2, dtype=np.int64)
    return (pairs[:, None] * 2 + np.arange(2)).reshape(-1)


def require_behavior_parity(
    expected: np.ndarray,
    recomputed: np.ndarray,
    *,
    params: Any,
    batch: dict[str, np.ndarray],
    completed_updates: int,
    diagnostic_dir: Path | None = None,
) -> float:
    if expected.shape != recomputed.shape:
        raise ValueError("behavior log-probability shapes differ")
    error = float(np.max(np.abs(recomputed - expected)))
    if np.isfinite(error) and error <= 1e-3:
        return error
    evidence = None
    if diagnostic_dir is not None:
        diagnostic_dir.mkdir(parents=True, exist_ok=True)
        evidence = diagnostic_dir / f"update_{completed_updates:04d}_{time.time_ns()}.pkl.gz"
        temporary = evidence.with_suffix(".tmp")
        # Keep the complete verification shape: backend dispatch can depend on batch size.
        payload = {
            "completed_updates": completed_updates,
            "params": jax.device_get(params),
            "batch": batch,
            "expected_log_prob": expected,
            "recomputed_log_prob": recomputed,
        }
        with temporary.open("wb") as raw:
            with gzip.GzipFile(fileobj=raw, mode="wb", compresslevel=1) as destination:
                pickle.dump(payload, destination, protocol=pickle.HIGHEST_PROTOCOL)
            raw.flush()
            os.fsync(raw.fileno())
        os.replace(temporary, evidence)
    raise RuntimeError(f"behavior log-prob mismatch before PPO update: {error}; evidence={evidence}")
