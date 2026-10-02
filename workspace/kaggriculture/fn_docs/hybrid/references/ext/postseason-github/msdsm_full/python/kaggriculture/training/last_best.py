"""Durable handshake for asynchronous last-best teacher promotion."""

from __future__ import annotations

import hashlib
import json
import os
import pickle
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import jax
import jax.numpy as jnp

from kaggriculture.training.checkpointing import LoopState, policy_hash, save_params_payload

CONTROL_SCHEMA_VERSION = 1
TEACHER_STATE_NAME = "teacher_state.json"
PROMOTION_REQUEST_NAME = "promotion_request.json"


@dataclass(frozen=True)
class TeacherState:
    generation: int
    source_update: int
    policy_sha256: str
    checkpoint: Path
    checkpoint_sha256: str
    promotion_threshold: float


@dataclass(frozen=True)
class PromotionPlan:
    state: LoopState
    request: dict[str, Any]
    next_teacher: TeacherState


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    os.replace(temporary, path)


def _teacher_payload(state: TeacherState) -> dict[str, Any]:
    return {
        "schema_version": CONTROL_SCHEMA_VERSION,
        "generation": state.generation,
        "source_update": state.source_update,
        "policy_sha256": state.policy_sha256,
        "checkpoint": str(state.checkpoint),
        "checkpoint_sha256": state.checkpoint_sha256,
        "promotion_threshold": state.promotion_threshold,
    }


def read_teacher_state(control_dir: Path) -> TeacherState:
    path = control_dir / TEACHER_STATE_NAME
    payload = json.loads(path.read_text())
    if payload.get("schema_version") != CONTROL_SCHEMA_VERSION:
        raise ValueError(f"unsupported last-best control schema: {payload.get('schema_version')}")
    state = TeacherState(
        generation=int(payload["generation"]),
        source_update=int(payload["source_update"]),
        policy_sha256=str(payload["policy_sha256"]),
        checkpoint=Path(payload["checkpoint"]),
        checkpoint_sha256=str(payload["checkpoint_sha256"]),
        promotion_threshold=float(payload["promotion_threshold"]),
    )
    if state.generation < 0 or state.source_update < 0:
        raise ValueError("last-best generation and source update must be non-negative")
    if not 0.0 <= state.promotion_threshold <= 1.0:
        raise ValueError("last-best promotion threshold must be in [0, 1]")
    if not state.checkpoint.is_file():
        raise FileNotFoundError(f"last-best teacher checkpoint is missing: {state.checkpoint}")
    if file_sha256(state.checkpoint) != state.checkpoint_sha256:
        raise ValueError("last-best teacher checkpoint hash mismatch")
    return state


def initialize_teacher_control(
    control_dir: Path,
    state: LoopState,
    model_config: dict[str, Any],
    *,
    promotion_threshold: float,
    resume: bool,
    execution_variant: str = "baseline",
) -> TeacherState:
    state_path = control_dir / TEACHER_STATE_NAME
    if state_path.is_file():
        teacher = read_teacher_state(control_dir)
        if teacher.promotion_threshold != promotion_threshold:
            raise ValueError("last-best promotion threshold changed across resume")
        current_reference = policy_hash(state.reference_params)
        pending = read_promotion_request(control_dir)
        pending_candidate = None if pending is None else pending.get("candidate_policy_sha256")
        if current_reference not in {teacher.policy_sha256, pending_candidate}:
            raise ValueError("checkpoint reference does not match last-best control state")
        return teacher
    if resume:
        raise FileNotFoundError("resuming last-best training requires its durable teacher_state.json")

    control_dir.mkdir(parents=True, exist_ok=True)
    checkpoint = control_dir / "teachers" / "teacher_0000_update_0000_jax.pkl"
    save_params_payload(
        checkpoint, state.reference_params, model_config, state.completed_updates, execution_variant=execution_variant
    )
    teacher = TeacherState(
        generation=0,
        source_update=state.completed_updates,
        policy_sha256=policy_hash(state.reference_params),
        checkpoint=checkpoint.resolve(),
        checkpoint_sha256=file_sha256(checkpoint),
        promotion_threshold=promotion_threshold,
    )
    _atomic_json(state_path, _teacher_payload(teacher))
    return teacher


def read_promotion_request(control_dir: Path) -> dict[str, Any] | None:
    path = control_dir / PROMOTION_REQUEST_NAME
    try:
        content = path.read_text()
    except FileNotFoundError:
        # The trainer archives and unlinks an acknowledged request atomically
        # with respect to its own state, but a reader can race that unlink.
        return None
    payload = json.loads(content)
    if payload.get("schema_version") != CONTROL_SCHEMA_VERSION:
        raise ValueError(f"unsupported promotion request schema: {payload.get('schema_version')}")
    return payload


def write_promotion_request(control_dir: Path, request: dict[str, Any]) -> None:
    existing = read_promotion_request(control_dir)
    payload = {"schema_version": CONTROL_SCHEMA_VERSION, **request}
    if existing is not None:
        if existing != payload:
            raise RuntimeError("a different last-best promotion request is already pending")
        return
    _atomic_json(control_dir / PROMOTION_REQUEST_NAME, payload)


def _load_candidate(
    request: dict[str, Any],
    model_config: dict[str, Any],
) -> tuple[dict[str, Any], str, str]:
    checkpoint = Path(request["candidate_checkpoint"])
    if not checkpoint.is_file():
        raise FileNotFoundError(f"promotion candidate is missing: {checkpoint}")
    if file_sha256(checkpoint) != request["candidate_checkpoint_sha256"]:
        raise ValueError("promotion candidate checkpoint hash mismatch")
    with checkpoint.open("rb") as source:
        payload = pickle.load(source)
    if payload.get("model_config") != model_config:
        raise ValueError("promotion candidate model config mismatch")
    if int(payload.get("rl_completed_updates", -1)) != int(request["candidate_update"]):
        raise ValueError("promotion candidate update mismatch")
    params = jax.tree.map(jnp.asarray, payload["params"])
    candidate_hash = policy_hash(params)
    if candidate_hash != request["candidate_policy_sha256"]:
        raise ValueError("promotion candidate policy hash mismatch")
    return params, candidate_hash, payload.get("execution_variant", "baseline")


def prepare_pending_promotion(
    control_dir: Path,
    state: LoopState,
    model_config: dict[str, Any],
) -> PromotionPlan | None:
    request = read_promotion_request(control_dir)
    if request is None:
        return None
    teacher = read_teacher_state(control_dir)
    request_generation = int(request["teacher_generation"])
    request_teacher_hash = str(request["teacher_policy_sha256"])
    already_committed = (
        request_generation + 1 == teacher.generation
        and str(request["candidate_policy_sha256"]) == teacher.policy_sha256
        and int(request["candidate_update"]) == teacher.source_update
    )
    if already_committed:
        _archive_promotion_request(control_dir, request, teacher)
        return None
    if request_generation != teacher.generation or request_teacher_hash != teacher.policy_sha256:
        raise ValueError("promotion request targets a stale or unknown teacher")
    if float(request["win_rate"]) < teacher.promotion_threshold:
        raise ValueError("promotion request does not meet the configured win-rate threshold")
    candidate_update = int(request["candidate_update"])
    if candidate_update > state.completed_updates:
        return None
    candidate_params, candidate_hash, execution_variant = _load_candidate(request, model_config)
    current_reference_hash = policy_hash(state.reference_params)
    if current_reference_hash == teacher.policy_sha256:
        state = replace(state, reference_params=candidate_params)
    elif current_reference_hash != candidate_hash:
        raise ValueError("training reference is neither current teacher nor pending candidate")

    next_checkpoint = (
        control_dir / "teachers" / f"teacher_{teacher.generation + 1:04d}_update_{candidate_update:04d}_jax.pkl"
    )
    if not next_checkpoint.is_file():
        save_params_payload(
            next_checkpoint, candidate_params, model_config, candidate_update, execution_variant=execution_variant
        )
    next_teacher = TeacherState(
        generation=teacher.generation + 1,
        source_update=candidate_update,
        policy_sha256=candidate_hash,
        checkpoint=next_checkpoint.resolve(),
        checkpoint_sha256=file_sha256(next_checkpoint),
        promotion_threshold=teacher.promotion_threshold,
    )
    return PromotionPlan(state=state, request=request, next_teacher=next_teacher)


def _archive_promotion_request(
    control_dir: Path,
    request: dict[str, Any],
    teacher: TeacherState,
) -> None:
    history = control_dir / "promotion_history"
    history.mkdir(parents=True, exist_ok=True)
    destination = history / (f"promotion_{teacher.generation:04d}_update_{teacher.source_update:04d}.json")
    _atomic_json(destination, request)
    request_path = control_dir / PROMOTION_REQUEST_NAME
    if request_path.is_file():
        request_path.unlink()


def commit_promotion(control_dir: Path, plan: PromotionPlan) -> None:
    previous_teacher = read_teacher_state(control_dir)
    _atomic_json(control_dir / TEACHER_STATE_NAME, _teacher_payload(plan.next_teacher))
    _archive_promotion_request(control_dir, plan.request, plan.next_teacher)
    previous_archive = (
        control_dir
        / "teacher_archives"
        / f"teacher_{previous_teacher.generation:04d}_{previous_teacher.policy_sha256[:12]}.tar.gz"
    )
    previous_archive.unlink(missing_ok=True)
