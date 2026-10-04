"""Load trusted local checkpoints and export inference-only payloads."""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Any


def load_training_source(path: Path) -> dict[str, Any]:
    """Accept a full PPO checkpoint, a BC state, or a policy-only payload.

    Checkpoints use pickle and must come from a trusted source.
    Starting a new BC stage does not restore the PPO optimizer.
    """
    from kaggriculture.training.checkpointing import policy_hash

    with path.open("rb") as stream:
        payload = pickle.load(stream)
    if "model_config" not in payload:
        raise ValueError("checkpoint is missing model_config")
    params = payload["state"]["params"] if "state" in payload else payload["params"]
    digest = policy_hash(params)
    if payload.get("policy_sha256", digest) != digest:
        raise ValueError("checkpoint parameter checksum mismatch")
    return {**payload, "state": {**payload.get("state", {}), "params": params}, "policy_sha256": digest}


def export_policy(source: Path, output: Path, *, sequential: bool | None = None) -> None:
    from dataclasses import replace
    from kaggriculture.model.policy import JaxModelConfig
    from kaggriculture.training.checkpointing import save_params_payload

    payload = load_training_source(source)
    model = JaxModelConfig(**payload["model_config"])
    if sequential is not None:
        model = replace(model, sequential_patch=sequential)
    model.validate()
    save_params_payload(
        output,
        payload["state"]["params"],
        model.to_dict(),
        int(payload["state"].get("completed_updates", payload.get("rl_completed_updates", 0))),
    )
