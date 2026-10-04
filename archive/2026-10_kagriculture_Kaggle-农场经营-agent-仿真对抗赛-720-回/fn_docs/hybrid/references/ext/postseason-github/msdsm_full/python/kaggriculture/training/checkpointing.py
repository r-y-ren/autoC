"""Durable two-phase checkpoints for iterative-reference self-play."""

from __future__ import annotations

import hashlib
import os
import pickle
import shutil
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.training.entropy_control import (
    EntropyChannel,
    HeadEntropyConfig,
    HeadEntropyState,
    validate_coefficient,
)
from kaggriculture.model.policy import Params

CHECKPOINT_SCHEMA_VERSION = 1
CHECKPOINT_FREE_SPACE_RESERVE = 1024**3


@dataclass(frozen=True)
class LoopState:
    params: Params
    reference_params: Params
    optimizer_state: Any
    rng: jax.Array
    outer_iteration: int
    inner_iteration: int
    seed_counter: int
    completed_updates: int
    last_behavior_hash: str
    reference_refresh_pending: bool = False
    entropy_coefficient: float = 0.0
    entropy_control: HeadEntropyState | None = None
    entropy_inheritance_sha256: str | None = None
    runtime_coefficients: dict[str, float] | None = None


def policy_hash(params: Params) -> str:
    digest = hashlib.sha256()
    leaves, tree = jax.tree_util.tree_flatten(jax.device_get(params))
    digest.update(str(tree).encode())
    for leaf in leaves:
        array = np.asarray(leaf)
        digest.update(str(array.dtype).encode())
        digest.update(str(array.shape).encode())
        digest.update(array.tobytes(order="C"))
    return digest.hexdigest()


def actor_hash(params: Params) -> str:
    """Hash every inference parameter except the critic head."""
    return policy_hash({name: values for name, values in params.items() if name != "value"})


def inherit_entropy_coefficients(
    state: LoopState, source: Path, config: HeadEntropyConfig
) -> tuple[LoopState, dict[str, Any] | None]:
    config.validate()
    source_bytes = source.read_bytes()
    source_hash = hashlib.sha256(source_bytes).hexdigest()
    if state.entropy_inheritance_sha256 is not None:
        if state.entropy_inheritance_sha256 != source_hash:
            raise ValueError("entropy inheritance source differs from the checkpoint's recorded source")
        return state, None

    payload = pickle.loads(source_bytes)
    if payload.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError("entropy inheritance requires a full PPO checkpoint")
    raw = payload["state"].get("entropy_control")
    if raw is None:
        raise ValueError("source checkpoint has no per-head entropy controller")
    previous = HeadEntropyState.from_dict(raw)
    for channel in (previous.unit, previous.market):
        validate_coefficient(channel.coefficient)
        if channel.coefficient < config.minimum or (
            config.maximum is not None and channel.coefficient > config.maximum
        ):
            raise ValueError("inherited entropy coefficient is outside the configured bounds")

    # The new policy visits a different state distribution; only the coefficients transfer.
    controller = HeadEntropyState(
        EntropyChannel(previous.unit.coefficient), EntropyChannel(previous.market.coefficient)
    )
    event = {
        "event": "entropy_coefficients_inherited",
        "completed_updates": state.completed_updates,
        "source_checkpoint": str(source),
        "source_checkpoint_sha256": source_hash,
        "source_completed_updates": payload["state"]["completed_updates"],
        "previous_controller": None if state.entropy_control is None else state.entropy_control.to_dict(),
        "inherited_controller": controller.to_dict(),
        "policy_sha256": policy_hash(state.params),
        "reference_sha256": policy_hash(state.reference_params),
    }
    return replace(state, entropy_control=controller, entropy_inheritance_sha256=source_hash), event


def finish_inner_update(
    state: LoopState,
    *,
    params: Params,
    optimizer_state: Any,
    rng: jax.Array,
    seed_counter: int,
    behavior_hash: str,
    reference_interval: int,
) -> LoopState:
    if state.reference_refresh_pending:
        raise RuntimeError("refresh the pending reference before another update")
    next_inner = state.inner_iteration + 1
    if next_inner > reference_interval:
        raise RuntimeError("inner iteration exceeded the reference interval")
    return replace(
        state,
        params=params,
        optimizer_state=optimizer_state,
        rng=rng,
        inner_iteration=next_inner,
        seed_counter=seed_counter,
        completed_updates=state.completed_updates + 1,
        last_behavior_hash=behavior_hash,
        reference_refresh_pending=next_inner == reference_interval,
    )


def refresh_reference(state: LoopState) -> LoopState:
    if not state.reference_refresh_pending:
        return state
    return replace(
        state,
        reference_params=state.params,
        outer_iteration=state.outer_iteration + 1,
        inner_iteration=0,
        reference_refresh_pending=False,
    )


def retain_reference(state: LoopState) -> LoopState:
    """Advance an outer interval without replacing its fixed teacher."""
    if not state.reference_refresh_pending:
        return state
    return replace(
        state,
        outer_iteration=state.outer_iteration + 1,
        inner_iteration=0,
        reference_refresh_pending=False,
    )


def _host_tree(tree: Any) -> Any:
    return jax.tree_util.tree_map(lambda value: np.asarray(jax.device_get(value)), tree)


def _device_tree(tree: Any) -> Any:
    return jax.tree_util.tree_map(jnp.asarray, tree)


def atomic_pickle(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("wb") as destination:
        pickle.dump(payload, destination, protocol=pickle.HIGHEST_PROTOCOL)
        destination.flush()
        os.fsync(destination.fileno())
    os.replace(temporary, path)


def retain_checkpoint(source: Path, destination: Path) -> None:
    """Retain an immutable state on the same PVC; latest is replaced atomically."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.link(source, destination)
    except FileExistsError:
        pass


def checkpoint_storage_pause(directory: Path, completed_updates: int) -> dict[str, Any] | None:
    free_bytes = shutil.disk_usage(directory).free
    if free_bytes >= CHECKPOINT_FREE_SPACE_RESERVE:
        return None
    return {
        "event": "checkpoint_storage_pause",
        "completed_updates": completed_updates,
        "free_bytes": free_bytes,
        "minimum_free_bytes": CHECKPOINT_FREE_SPACE_RESERVE,
        "reason": "preserve checkpoints and stop before exhausting the PVC",
    }


def save_checkpoint(
    path: Path,
    state: LoopState,
    *,
    model_config: dict[str, Any],
    training_config: dict[str, Any],
    source_checkpoint_sha256: str,
    metadata: dict[str, Any] | None = None,
) -> None:
    payload = {
        "schema_version": CHECKPOINT_SCHEMA_VERSION,
        "state": {
            "params": _host_tree(state.params),
            "reference_params": _host_tree(state.reference_params),
            "optimizer_state": _host_tree(state.optimizer_state),
            "rng": np.asarray(jax.device_get(state.rng)),
            "outer_iteration": state.outer_iteration,
            "inner_iteration": state.inner_iteration,
            "seed_counter": state.seed_counter,
            "completed_updates": state.completed_updates,
            "last_behavior_hash": state.last_behavior_hash,
            "reference_refresh_pending": state.reference_refresh_pending,
            "entropy_coefficient": state.entropy_coefficient,
            "entropy_control": None if state.entropy_control is None else state.entropy_control.to_dict(),
            "entropy_inheritance_sha256": state.entropy_inheritance_sha256,
            "runtime_coefficients": state.runtime_coefficients,
        },
        "model_config": model_config,
        "training_config": training_config,
        "source_checkpoint_sha256": source_checkpoint_sha256,
        "policy_sha256": policy_hash(state.params),
        "reference_sha256": policy_hash(state.reference_params),
        "engine_version": "1.32.7",
        "training_backend": "jax",
        "metadata": {} if metadata is None else metadata,
    }
    atomic_pickle(path, payload)


def save_evaluation_checkpoint(
    directory: Path,
    state: LoopState,
    *,
    snapshot_interval: int,
    model_config: dict[str, Any],
    training_config: dict[str, Any],
    source_checkpoint_sha256: str,
    metadata: dict[str, Any] | None = None,
    force: bool = False,
) -> bool:
    if not force and (snapshot_interval <= 0 or state.completed_updates % snapshot_interval != 0):
        return False
    latest = directory / "latest_jax.pkl"
    save_checkpoint(
        latest,
        state,
        model_config=model_config,
        training_config=training_config,
        source_checkpoint_sha256=source_checkpoint_sha256,
        metadata=metadata,
    )
    retain_checkpoint(latest, directory / "checkpoints" / f"checkpoint_update_{state.completed_updates:04d}_jax.pkl")
    save_policy_payload(directory / "policy_latest_jax.pkl", state, model_config)
    if snapshot_interval > 0 and state.completed_updates % snapshot_interval == 0:
        snapshot = directory / "async_checkpoints" / f"policy_update_{state.completed_updates:04d}_jax.pkl"
        if not snapshot.exists():
            save_policy_payload(snapshot, state, model_config)
    return True


def load_checkpoint(path: Path) -> tuple[LoopState, dict[str, Any]]:
    with path.open("rb") as source:
        payload = pickle.load(source)
    if payload.get("schema_version") != CHECKPOINT_SCHEMA_VERSION:
        raise ValueError(f"unsupported checkpoint schema: {payload.get('schema_version')}")
    raw = payload["state"]
    state = LoopState(
        params=_device_tree(raw["params"]),
        reference_params=_device_tree(raw["reference_params"]),
        optimizer_state=_device_tree(raw["optimizer_state"]),
        rng=jnp.asarray(raw["rng"]),
        outer_iteration=int(raw["outer_iteration"]),
        inner_iteration=int(raw["inner_iteration"]),
        seed_counter=int(raw["seed_counter"]),
        completed_updates=int(raw["completed_updates"]),
        last_behavior_hash=str(raw["last_behavior_hash"]),
        reference_refresh_pending=bool(raw["reference_refresh_pending"]),
        entropy_coefficient=float(
            raw.get("entropy_coefficient", payload["training_config"].get("entropy_coefficient", 0.0))
        ),
        entropy_control=(
            HeadEntropyState.from_dict(raw["entropy_control"]) if raw.get("entropy_control") is not None else None
        ),
        entropy_inheritance_sha256=raw.get("entropy_inheritance_sha256"),
        runtime_coefficients=raw.get("runtime_coefficients"),
    )
    if policy_hash(state.params) != payload["policy_sha256"]:
        raise ValueError("policy hash mismatch")
    if policy_hash(state.reference_params) != payload["reference_sha256"]:
        raise ValueError("reference hash mismatch")
    return state, payload


def save_params_payload(
    path: Path,
    params: Params,
    model_config: dict[str, Any],
    completed_updates: int,
    *,
    execution_variant: str = "baseline",
) -> None:
    """Write an inference-compatible native-JAX payload; the value leaf is harmless."""
    atomic_pickle(
        path,
        {
            "params": _host_tree(params),
            "model_config": model_config,
            "training_backend": "jax",
            "rl_completed_updates": completed_updates,
            "policy_sha256": policy_hash(params),
            "execution_variant": execution_variant,
        },
    )


def save_policy_payload(
    path: Path, state: LoopState, model_config: dict[str, Any], *, execution_variant: str = "baseline"
) -> None:
    save_params_payload(path, state.params, model_config, state.completed_updates, execution_variant=execution_variant)
