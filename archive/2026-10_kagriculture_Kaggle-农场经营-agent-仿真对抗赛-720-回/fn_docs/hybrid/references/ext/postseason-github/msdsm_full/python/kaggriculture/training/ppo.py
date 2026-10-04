"""Native-JAX iterative-reference NashPG/PPO self-play."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pickle
import time
from contextlib import nullcontext
from dataclasses import replace
from pathlib import Path
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.training.batch_prefetch import CompletionQueue, prefetched_batches
from kaggriculture.training.behavior_parity import require_behavior_parity
from kaggriculture.training.behavior_parity import verification_indices as parity_indices
from kaggriculture.training.checkpointing import (
    LoopState,
    actor_hash,
    atomic_pickle,
    checkpoint_storage_pause,
    finish_inner_update,
    inherit_entropy_coefficients,
    load_checkpoint,
    policy_hash,
    refresh_reference,
    retain_checkpoint,
    retain_reference,
    save_checkpoint,
    save_evaluation_checkpoint,
    save_policy_payload,
)
from kaggriculture.training.distributed.aggregation import PPOCollectives
from kaggriculture.training.entropy_control import (
    HEAD_ENTROPY_DEFAULTS,
    HeadEntropyState,
    update_head_entropy,
)
from kaggriculture.training.entropy_control import (
    config_from_args as head_entropy_config_from_args,
)
from kaggriculture.training.fixed_entropy_override import (
    FIXED_ENTROPY_FIELDS,
    change_fixed_entropy,
    validate_fixed_entropy_override,
)
from kaggriculture.training.game_partition import GamePartition
from kaggriculture.model.policy import JaxModelConfig, Params, add_zero_value_head
from kaggriculture.training.sharding import select_data_parallel_devices
from kaggriculture.training.last_best import (
    commit_promotion,
    initialize_teacher_control,
    prepare_pending_promotion,
)
from kaggriculture.training.phase_entropy import (
    OPENING_ENTROPY_DEFAULTS,
    PHASE_PREFIX,
    phase_report,
    validate_opening_entropy,
)
from kaggriculture.training.purchase_entropy import (
    PURCHASE_ENTROPY_DEFAULTS,
    add_purchase_report,
    validate_purchase_entropy,
)
from kaggriculture.training.purchase_policy import (
    PURCHASE_POLICY_PREFIX,
    PURCHASE_TEMPERATURE_DEFAULTS,
    opening_purchase_report,
    purchase_temperature,
    validate_purchase_temperature,
)
from kaggriculture.training.objectives import (
    PPOConfig,
    make_full_value_update_step,
    make_log_prob_evaluator,
    make_optimizer,
    make_policy_diagnostics_evaluator,
    make_update_step,
    optimizer_step_number,
)
from kaggriculture.training.rollout import RolloutBatch, RolloutWorkspace, collect_self_play, make_sampler

RESUME_FIXED_FIELDS = (
    "initial_critic_checkpoint",
    "games",
    "horizon",
    "reference_interval",
    "freeze_reference",
    "snapshot_interval",
    "pinned_feature_buffer",
    "last_best_control_dir",
    "last_best_promotion_threshold",
    "ppo_epochs",
    "segments_per_minibatch",
    "minibatch",
    "inference_batch_size",
    "data_parallel_devices",
    "data_parallel_rollout",
    "learning_rate",
    "adam_epsilon",
    "lr_decay_steps",
    "lr_warmup_steps",
    "lr_min_ratio",
    "clip",
    "kl_coefficient",
    "teacher_divergence",
    "entropy_coefficient",
    "entropy_floor",
    "entropy_coefficient_growth",
    "entropy_coefficient_max",
    "reference_kl_samples",
    "normalize_advantages",
    "value_coefficient",
    "value_huber_delta",
    "gradient_norm",
    "gamma",
    "gae_lambda",
    "value_warmup_max_updates",
    "value_warmup_patience",
    "value_warmup_min_delta",
    "value_validation_games",
    "value_validation_seed_start",
    "seed",
    "environment_seed_start",
    "compute_dtype",
    "attention_backend",
    "rope_correction_backend",
    "smoke",
    *HEAD_ENTROPY_DEFAULTS,
    *OPENING_ENTROPY_DEFAULTS,
    *PURCHASE_ENTROPY_DEFAULTS,
    *PURCHASE_TEMPERATURE_DEFAULTS,
)


class TorchFreeBCUnpickler(pickle.Unpickler):
    """Load native-JAX BC checkpoints whose history records torch's version string."""

    def find_class(self, module: str, name: str) -> Any:
        if module == "torch.torch_version" and name == "TorchVersion":
            return str
        return super().find_class(module, name)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bc-checkpoint", type=Path, required=True)
    parser.add_argument(
        "--initial-critic-checkpoint",
        type=Path,
        help="separate-critic checkpoint used instead of in-process Value warm-up",
    )
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--resume", type=Path)
    parser.add_argument(
        "--allow-data-parallel-resize",
        action="store_true",
        help="allow proportional GPU/batch resizing while preserving per-device shapes and optimizer cadence",
    )
    parser.add_argument(
        "--inherit-entropy-checkpoint",
        type=Path,
        help="inherit per-head coefficients once, resetting EMA; later resumes retain the adapted controller",
    )
    parser.add_argument("--games", type=int, default=120)
    parser.add_argument("--horizon", type=int, default=719)
    parser.add_argument("--outer-iterations", type=int, default=10)
    parser.add_argument("--reference-interval", type=int, default=10)
    parser.add_argument("--freeze-reference", action="store_true")
    parser.add_argument(
        "--snapshot-interval",
        type=int,
        default=0,
        help="persist an immutable policy payload every N completed PPO updates; zero disables it",
    )
    parser.add_argument(
        "--pinned-feature-buffer",
        action="store_true",
        help="page-lock and reuse the Rust feature buffer for asynchronous GPU transfer",
    )
    parser.add_argument(
        "--last-best-control-dir",
        type=Path,
        help="shared durable handshake directory for asynchronous last-best promotion",
    )
    parser.add_argument(
        "--last-best-promotion-threshold",
        type=float,
        help="promote an evaluated snapshot when its win rate against the current teacher reaches this value",
    )
    parser.add_argument("--ppo-epochs", type=int, default=1)
    parser.add_argument("--segments-per-minibatch", type=int, default=8)
    parser.add_argument("--minibatch", type=int, default=240)
    parser.add_argument("--inference-batch-size", type=int, default=240)
    parser.add_argument(
        "--data-parallel-devices",
        type=int,
        default=1,
        help="number of local GPUs across which PPO updates are data-parallel",
    )
    parser.add_argument(
        "--data-parallel-rollout",
        action="store_true",
        help="also shard rollout inference and diagnostics; PPO updates are always sharded when device count exceeds one",
    )
    parser.add_argument("--diagnostics-transitions", type=int, default=15_360)
    parser.add_argument("--value-warmup-max-updates", type=int, default=0)
    parser.add_argument("--value-warmup-patience", type=int, default=8)
    parser.add_argument("--value-warmup-min-delta", type=float, default=1e-5)
    parser.add_argument("--value-validation-games", type=int)
    parser.add_argument("--value-validation-seed-start", type=int, default=10_000_000)
    parser.add_argument("--learning-rate", type=float, default=1e-4)
    parser.add_argument("--adam-epsilon", type=float, default=1e-5)
    parser.add_argument("--lr-decay-steps", type=int, default=150_000)
    parser.add_argument("--lr-warmup-steps", type=int, default=240)
    parser.add_argument("--lr-min-ratio", type=float, default=0.25)
    parser.add_argument("--clip", type=float, default=0.2)
    parser.add_argument(
        "--kl-coefficient",
        type=float,
        default=0.005,
        help="coefficient for the selected teacher divergence (legacy option name)",
    )
    parser.add_argument(
        "--teacher-divergence",
        choices=("kl", "js"),
        default="kl",
        help="teacher regularizer: KL(teacher || policy) or symmetric Jensen-Shannon distance",
    )
    parser.add_argument("--entropy-coefficient", type=float, default=1e-7)
    parser.add_argument("--opening-entropy-steps", type=int, default=48)
    parser.add_argument("--opening-entropy-multiplier", type=float, default=1.0)
    parser.add_argument("--purchase-entropy-coefficient", type=float, default=0.0)
    parser.add_argument("--purchase-entropy-steps", type=int, default=48)
    parser.add_argument("--purchase-entropy-metrics", action="store_true")
    parser.add_argument("--allow-purchase-entropy-change", action="store_true")
    parser.add_argument("--purchase-temperature-initial", type=float, default=1.0)
    parser.add_argument("--purchase-temperature-steps", type=int, default=5)
    parser.add_argument("--purchase-temperature-decay-updates", type=int, default=100)
    parser.add_argument("--purchase-temperature-start-update", type=int, default=0)
    parser.add_argument("--purchase-temperature-schedule", choices=("exponential", "linear"), default="exponential")
    parser.add_argument("--allow-purchase-temperature-change", action="store_true")
    parser.add_argument(
        "--allow-opening-entropy-change",
        action="store_true",
        help="explicitly change only the opening entropy schedule on resume, preserving optimizer state",
    )
    parser.add_argument(
        "--allow-fixed-entropy-change",
        action="store_true",
        help="explicitly replace only the fixed entropy coefficient on resume, preserving full optimizer state",
    )
    parser.add_argument(
        "--entropy-floor",
        type=float,
        help="raise the entropy coefficient when post-update normalized entropy falls below this value",
    )
    parser.add_argument("--entropy-coefficient-growth", type=float, default=2.0)
    parser.add_argument("--entropy-coefficient-max", type=float, default=1e-4)
    parser.add_argument(
        "--uncapped-entropy",
        action="store_true",
        help="remove the upper coefficient bound for the per-head entropy controller",
    )
    parser.add_argument("--unit-entropy-target", type=float)
    parser.add_argument("--market-entropy-target", type=float)
    parser.add_argument("--head-entropy-ema-decay", type=float, default=0.9)
    parser.add_argument("--head-entropy-interval", type=int, default=5)
    parser.add_argument("--head-entropy-relative-band", type=float, default=0.1)
    parser.add_argument("--head-entropy-change-factor", type=float, default=1.25)
    parser.add_argument("--head-entropy-coefficient-min", type=float, default=1e-9)
    parser.add_argument(
        "--allow-entropy-control-change",
        action="store_true",
        help="explicitly permit changing only the per-head entropy controller when resuming",
    )
    parser.add_argument("--reference-kl-samples", type=int, default=30)
    parser.add_argument(
        "--normalize-advantages",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    parser.add_argument("--value-coefficient", type=float, default=2.0)
    parser.add_argument("--value-huber-delta", type=float, default=1.0)
    parser.add_argument("--gradient-norm", type=float, default=5.0)
    parser.add_argument("--gamma", type=float, default=1.0)
    parser.add_argument("--gae-lambda", type=float, default=0.85)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--environment-seed-start", type=int, default=1_000_000)
    parser.add_argument("--compute-dtype", choices=("bfloat16", "float32"), default="bfloat16")
    parser.add_argument("--attention-backend", choices=("manual", "cudnn"), default="manual")
    parser.add_argument(
        "--rope-correction-backend",
        choices=("dense", "augmented", "partitioned"),
        default="dense",
    )
    parser.add_argument("--max-inner-updates", type=int)
    parser.add_argument("--smoke", action="store_true")
    parser.add_argument(
        "--max-env-steps", type=int, help="PPO decision budget across both seats; stop at an update boundary"
    )
    parser.add_argument(
        "--enable-sequential-masks", action="store_true", help="adapt an existing policy with Final B action masks"
    )
    from kaggriculture.config import parse_config_args

    return parse_config_args(parser)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_bc_checkpoint(path: Path) -> tuple[Params, JaxModelConfig]:
    with path.open("rb") as source:
        payload = TorchFreeBCUnpickler(source).load()
    if "params" not in payload or "model_config" not in payload:
        raise ValueError("BC checkpoint must contain params and model_config")
    config = JaxModelConfig(**payload["model_config"])
    config.validate()
    params = jax.tree_util.tree_map(jnp.asarray, payload["params"])
    return add_zero_value_head(params, config), config


def load_initial_critic_checkpoint(
    path: Path,
    policy_params: Params,
    model_config: JaxModelConfig,
) -> Params:
    """Load a separately fitted critic while proving that its actor is unchanged."""
    with path.open("rb") as source:
        payload = pickle.load(source)
    required = {"critic_params", "model_config", "policy_sha256"}
    missing = required.difference(payload)
    if missing:
        raise ValueError(f"initial critic checkpoint is missing: {sorted(missing)}")
    if payload["model_config"] != model_config.to_dict():
        raise ValueError("initial critic model config does not match PPO model config")
    if payload["policy_sha256"] != policy_hash(policy_params):
        raise ValueError("initial critic was fitted against a different fixed policy")

    critic_params = jax.tree_util.tree_map(jnp.asarray, payload["critic_params"])
    if actor_hash(critic_params) != actor_hash(policy_params):
        raise ValueError("initial critic checkpoint changed actor parameters")
    return critic_params


def serializable_args(args: argparse.Namespace) -> dict[str, Any]:
    return {name: str(value) if isinstance(value, Path) else value for name, value in vars(args).items()}


def initialize_state(
    params: Params,
    optimizer_state: Any,
    *,
    seed: int,
    environment_seed_start: int | None = None,
    entropy_coefficient: float = 0.0,
) -> LoopState:
    return LoopState(
        params=params,
        reference_params=params,
        optimizer_state=optimizer_state,
        rng=jax.random.PRNGKey(seed),
        outer_iteration=0,
        inner_iteration=0,
        seed_counter=seed * 1_000_000 if environment_seed_start is None else environment_seed_start,
        completed_updates=0,
        last_behavior_hash=policy_hash(params),
        entropy_coefficient=entropy_coefficient,
    )


def adjusted_entropy_coefficient(
    current: float,
    normalized_entropy: float,
    *,
    floor: float | None,
    growth: float,
    maximum: float,
) -> float:
    if floor is None or normalized_entropy >= floor:
        return current
    return min(maximum, current * growth)


def aggregate_device_metrics(
    metric_rows: list[dict[str, jax.Array | np.ndarray]],
    sample_counts: list[int],
) -> dict[str, Any]:
    # Cross-host metrics are already on CPU; sending every scalar back to the GPU is unnecessary.
    array = np if isinstance(next(iter(metric_rows[0].values())), np.ndarray) else jnp
    weights = array.asarray(sample_counts, dtype=array.float32)
    denominator = array.sum(weights)
    aggregated = {}
    raw_ratio_metrics = {
        "unit_teacher_kl_numerator",
        "unit_teacher_kl_denominator",
    }
    for name in metric_rows[0]:
        if (
            name == "sample_count"
            or name in raw_ratio_metrics
            or name.startswith((PHASE_PREFIX, PURCHASE_POLICY_PREFIX))
        ):
            continue
        values = array.stack([row[name] for row in metric_rows])
        if values.ndim > 1:
            values = array.mean(values, axis=tuple(range(1, values.ndim)))
        aggregated[name] = array.sum(values * weights) / denominator
    if raw_ratio_metrics <= metric_rows[0].keys():
        numerators = array.stack([row["unit_teacher_kl_numerator"] for row in metric_rows])
        denominators = array.stack([row["unit_teacher_kl_denominator"] for row in metric_rows])
        if numerators.ndim > 1:
            replica_axes = tuple(range(1, numerators.ndim))
            numerators = array.sum(numerators, axis=replica_axes)
            denominators = array.sum(denominators, axis=replica_axes)
        aggregated["unit_teacher_kl_per_factor"] = array.sum(numerators) / array.maximum(
            array.sum(denominators),
            1.0,
        )
        aggregated["unit_teacher_divergence_per_factor"] = aggregated["unit_teacher_kl_per_factor"]
    phase_totals = {
        name: array.sum(array.stack([row[name] for row in metric_rows]))
        for name in metric_rows[0]
        if name.startswith(PHASE_PREFIX)
    }
    result = {name: float(value) for name, value in jax.device_get(aggregated).items()}
    purchase_totals = {
        name: array.sum(array.stack([row[name] for row in metric_rows]))
        for name in metric_rows[0]
        if name.startswith(PURCHASE_POLICY_PREFIX)
    }
    if purchase_totals:
        result["opening_purchase"] = opening_purchase_report(
            {name: float(value) for name, value in jax.device_get(purchase_totals).items()}
        )
    if phase_totals:
        result["entropy_by_phase"] = phase_report(
            {name: float(value) for name, value in jax.device_get(phase_totals).items()}
        )
    return add_purchase_report(result)


def reverse_time_slice_starts(transitions: int, minibatch_size: int) -> tuple[int, ...]:
    if transitions <= 0 or minibatch_size <= 0 or transitions % minibatch_size:
        raise ValueError("reverse time slices require a positive exact partition")
    return tuple(range(transitions - minibatch_size, -1, -minibatch_size))


def segment_major_indices(
    game_indices: np.ndarray,
    *,
    games: int,
    horizon: int,
) -> np.ndarray:
    """Select complete game segments from time-major rollout storage."""
    selected_games = np.asarray(game_indices, dtype=np.int64)
    if selected_games.ndim != 1 or len(selected_games) == 0:
        raise ValueError("game indices must be a non-empty vector")
    if np.any(selected_games < 0) or np.any(selected_games >= games):
        raise ValueError("game index is outside the rollout")
    time = np.arange(horizon, dtype=np.int64)[None, :, None]
    game = selected_games[:, None, None]
    seat = np.arange(2, dtype=np.int64)[None, None, :]
    return (time * (games * 2) + game * 2 + seat).reshape(-1)


def gradient_accumulation_steps(
    *,
    segments_per_minibatch: int,
    horizon: int,
    microbatch_size: int,
) -> int:
    effective_batch_size = segments_per_minibatch * horizon * 2
    return (effective_batch_size + microbatch_size - 1) // microbatch_size


def gradient_microbatch_loss_scale(
    *,
    accumulation_steps: int,
    valid_count: int,
    effective_batch_size: int,
) -> float:
    if accumulation_steps <= 0 or valid_count < 0 or effective_batch_size <= 0:
        raise ValueError("gradient accumulation sizes must be positive and valid count nonnegative")
    if valid_count > effective_batch_size:
        raise ValueError("microbatch cannot exceed the effective minibatch")
    return accumulation_steps * valid_count / effective_batch_size


def padded_microbatch_indices(
    indices: np.ndarray,
    microbatch_size: int,
    *,
    steps: int | None = None,
) -> tuple[tuple[np.ndarray, int], ...]:
    if microbatch_size <= 0 or microbatch_size % 2:
        raise ValueError("microbatch size must be a positive number of seat pairs")
    selected = np.asarray(indices, dtype=np.int64)
    if selected.ndim != 1 or (len(selected) == 0 and steps is None) or len(selected) % 2:
        raise ValueError("effective minibatch must be a non-empty number of seat pairs")
    needed = (len(selected) + microbatch_size - 1) // microbatch_size
    if steps is not None and (steps <= 0 or steps < needed):
        raise ValueError("microbatch steps cannot omit real samples")
    padding_source = selected if len(selected) else np.asarray([0, 1], dtype=np.int64)
    microbatches = []
    for step in range(needed if steps is None else steps):
        start = step * microbatch_size
        valid = max(0, min(microbatch_size, len(selected) - start))
        batch_indices = selected[start : start + valid]
        if valid < microbatch_size:
            batch_indices = np.concatenate((batch_indices, np.resize(padding_source, microbatch_size - valid)))
        microbatches.append((batch_indices, valid))
    return tuple(microbatches)


def full_value_update(
    params: Params,
    optimizer_state: Any,
    rollout: RolloutBatch,
    *,
    update_step,
    log_prob_evaluator,
    minibatch_size: int,
    completed_warmup_updates: int,
) -> tuple[Params, Any, dict[str, float]]:
    paired_time_slice = rollout.games * 2
    if minibatch_size != paired_time_slice:
        raise ValueError("Value minibatch must contain one complete game-seat time slice")
    if rollout.behavior_hash != policy_hash(params):
        raise RuntimeError("Value warm-up rollout was not sampled by the supplied parameters")
    if "value" not in params:
        raise ValueError("Value warm-up requires a critic head")

    verification_batch = rollout.minibatch(np.arange(minibatch_size), minibatch_size)
    recomputed = np.asarray(
        jax.device_get(
            log_prob_evaluator(
                params,
                {name: jnp.asarray(values) for name, values in verification_batch.items()},
            )
        )
    )
    behavior_log_prob_error = float(np.max(np.abs(recomputed - rollout.old_log_prob[:minibatch_size])))
    if behavior_log_prob_error > 1e-3:
        raise RuntimeError(f"behavior log-prob mismatch before Value update: {behavior_log_prob_error}")

    metric_rows: list[dict[str, jax.Array]] = []
    sample_counts: list[int] = []
    starts = reverse_time_slice_starts(rollout.transitions, minibatch_size)
    for update_index, start in enumerate(starts):
        selected = np.arange(start, start + minibatch_size)
        host_batch = rollout.minibatch(selected, minibatch_size)
        device_batch = {name: jnp.asarray(values) for name, values in host_batch.items()}
        optimizer_step = completed_warmup_updates * rollout.horizon + update_index
        device_batch["optimizer_step"] = jnp.asarray(optimizer_step, dtype=jnp.int32)
        params, optimizer_state, device_metrics = update_step(
            params,
            optimizer_state,
            device_batch,
        )
        metric_rows.append(device_metrics)
        sample_counts.append(minibatch_size)

    metrics = aggregate_device_metrics(metric_rows, sample_counts)
    metrics.update(
        {
            "behavior_log_prob_max_abs_error": behavior_log_prob_error,
            "first_timestep": float(rollout.horizon - 1),
            "last_timestep": 0.0,
            "optimizer_steps": float(len(starts)),
        }
    )
    return params, optimizer_state, metrics


def ppo_update(
    state: LoopState,
    rollout: RolloutBatch,
    *,
    update_step,
    log_prob_evaluator,
    ppo_epochs: int,
    minibatch_size: int,
    segments_per_minibatch: int,
    accumulation_steps: int,
    parity_failure_dir: Path | None = None,
    collectives: PPOCollectives | None = None,
    prefetch: bool = True,
    partition: GamePartition | None = None,
) -> tuple[Params, Any, jax.Array, dict[str, float]]:
    if partition is None and rollout.games % segments_per_minibatch:
        raise ValueError("rollout games must be divisible by segments per minibatch")
    if partition is not None and (
        partition.games > rollout.games
        or (partition.processes > 1 and (collectives is None or collectives.processes != partition.processes))
    ):
        raise ValueError("game partition differs from rollout capacity or collective size")
    expected_accumulation_steps = gradient_accumulation_steps(
        segments_per_minibatch=segments_per_minibatch,
        horizon=rollout.horizon,
        microbatch_size=minibatch_size,
    )
    if partition is not None:
        expected_accumulation_steps = max(2, expected_accumulation_steps)
    if accumulation_steps != expected_accumulation_steps:
        raise ValueError(
            f"gradient accumulation mismatch: expected {expected_accumulation_steps}, got {accumulation_steps}"
        )
    expected_behavior_hash = policy_hash(state.params)
    if rollout.behavior_hash != expected_behavior_hash:
        raise RuntimeError(
            f"rollout policy hash {rollout.behavior_hash} != current policy hash {expected_behavior_hash}"
        )
    params = state.params
    starts_at_reference = (
        policy_hash(state.reference_params) == expected_behavior_hash and rollout.purchase_temperature == 1.0
    )
    zero_learning_signal = bool(np.all(rollout.advantages == 0.0) and np.array_equal(rollout.returns, rollout.value))
    if collectives is not None:
        zero_learning_signal = collectives.all_true(zero_learning_signal)
    optimizer_state = state.optimizer_state
    rng = state.rng
    device_metric_rows: list[dict[str, jax.Array]] = []
    metric_sample_counts: list[int] = []
    transitions = rollout.transitions
    verification_count = min(transitions, minibatch_size)
    verification_indices = parity_indices(transitions, verification_count)
    verification_batch = rollout.minibatch(verification_indices, verification_count)
    recomputed = np.asarray(
        jax.device_get(
            log_prob_evaluator(
                params,
                {name: jnp.asarray(values) for name, values in verification_batch.items()},
            )
        )
    )
    behavior_log_prob_error = require_behavior_parity(
        rollout.old_log_prob[verification_indices],
        recomputed[:verification_count],
        params=params,
        batch=verification_batch,
        completed_updates=state.completed_updates,
        diagnostic_dir=parity_failure_dir,
    )
    first_optimizer_step = True
    # Sharded staging starts with NumPy even when this process owns only one GPU.
    use_host_batch = (
        getattr(update_step, "data_parallel_device_count", 1) > 1
        or getattr(update_step, "prepare_batch", None) is not None
    )
    array = np.asarray if use_host_batch else jnp.asarray
    prepare_batch = getattr(update_step, "prepare_batch", None) if prefetch else None
    optimizer_steps_per_epoch = rollout.games // segments_per_minibatch if partition is None else partition.emissions
    initial_optimizer_step = optimizer_step_number(state.optimizer_state)
    microbatch_count = 0
    completions = CompletionQueue(jax.block_until_ready, capacity=2)
    for epoch in range(ppo_epochs):
        rng, permutation_key = jax.random.split(rng)
        game_order = np.asarray(
            jax.device_get(
                jax.random.permutation(permutation_key, rollout.games if partition is None else partition.games)
            )
        )
        step_indices = []
        for segment_batch_index in range(optimizer_steps_per_epoch):
            selection = (
                slice(segment_batch_index * segments_per_minibatch, (segment_batch_index + 1) * segments_per_minibatch)
                if partition is None
                else partition.group(segment_batch_index)
            )
            selected_games = game_order[selection]
            step_indices.append(
                segment_major_indices(selected_games, games=rollout.games, horizon=rollout.horizon)
                if len(selected_games)
                else np.empty(0, dtype=np.int64)
            )
        # One gather for every step's advantage moments instead of a rank-wide round trip per Adam step.
        if collectives is None:
            step_statistics = [
                (np.float32(rollout.advantages[indices].mean()), np.float32(rollout.advantages[indices].std()))
                for indices in step_indices
            ]
        else:
            step_statistics = collectives.statistics_batch([rollout.advantages[indices] for indices in step_indices])
        for segment_batch_index in range(optimizer_steps_per_epoch):
            effective_indices = step_indices[segment_batch_index]
            effective_batch_size = (
                len(effective_indices)
                if partition is None
                else partition.global_group_games(segment_batch_index) * rollout.horizon * 2
            )
            process_scale = 1 if partition is None else partition.processes
            advantage_mean, advantage_standard_deviation = step_statistics[segment_batch_index]
            microbatches = padded_microbatch_indices(
                effective_indices, minibatch_size, steps=None if partition is None else accumulation_steps
            )
            if len(microbatches) != accumulation_steps:
                raise RuntimeError("segment minibatch produced an unexpected accumulation count")
            optimizer_step = initial_optimizer_step + epoch * optimizer_steps_per_epoch + segment_batch_index
            suppress_exact_zero_kl = starts_at_reference and (first_optimizer_step or zero_learning_signal)

            def prepare_microbatch(
                item: tuple[np.ndarray, int],
                *,
                advantage_mean: np.float32 = advantage_mean,
                advantage_standard_deviation: np.float32 = advantage_standard_deviation,
                effective_batch_size: int = effective_batch_size,
                process_scale: int = process_scale,
                optimizer_step: int = optimizer_step,
                suppress_exact_zero_kl: bool = suppress_exact_zero_kl,
            ) -> tuple[Any, int]:
                selected, valid_count = item
                with jax.profiler.TraceAnnotation("ppo_stage_host"):
                    host_batch = rollout.minibatch(selected, valid_count)
                device_batch = {name: array(values) for name, values in host_batch.items()}
                device_batch.update(
                    {
                        "advantage_normalization_mean": array(advantage_mean),
                        "advantage_normalization_standard_deviation": array(advantage_standard_deviation),
                        "gradient_loss_scale": array(
                            gradient_microbatch_loss_scale(
                                accumulation_steps=accumulation_steps,
                                valid_count=valid_count,
                                effective_batch_size=effective_batch_size,
                            )
                            * process_scale,
                            dtype=np.float32,
                        ),
                        "optimizer_step": array(optimizer_step, dtype=np.int32),
                        "reference_kl_scale": array(
                            0.0 if suppress_exact_zero_kl else 1.0,
                            dtype=np.float32,
                        ),
                        "entropy_coefficient": array(state.entropy_coefficient, dtype=np.float32),
                    }
                )
                if state.entropy_control is not None:
                    device_batch.update(
                        unit_entropy_coefficient=array(state.entropy_control.unit.coefficient, dtype=np.float32),
                        market_entropy_coefficient=array(state.entropy_control.market.coefficient, dtype=np.float32),
                    )
                if state.runtime_coefficients is not None:
                    device_batch.update(
                        {name: array(value, dtype=np.float32) for name, value in state.runtime_coefficients.items()}
                    )
                if prepare_batch is None:
                    return device_batch, valid_count
                with jax.profiler.TraceAnnotation("ppo_stage_transfer"):
                    return prepare_batch(device_batch), valid_count

            batches = (
                nullcontext(map(prepare_microbatch, microbatches))
                if prepare_batch is None
                else prefetched_batches(microbatches, prepare_microbatch)
            )
            with batches as prepared:
                for device_batch, valid_count in prepared:
                    params, optimizer_state, device_metrics = update_step(
                        params,
                        state.reference_params,
                        optimizer_state,
                        device_batch,
                    )
                    # Bound GPU work as well as host staging, retaining one update of overlap.
                    completions.submit((params, optimizer_state))
                    device_metric_rows.append(device_metrics)
                    metric_sample_counts.append(valid_count)
                    microbatch_count += 1
            first_optimizer_step = False
    completions.drain()
    if collectives is not None:
        device_metric_rows, metric_sample_counts = collectives.metric_rows(device_metric_rows, metric_sample_counts)
        behavior_log_prob_error = collectives.maximum(behavior_log_prob_error)
    metrics = aggregate_device_metrics(device_metric_rows, metric_sample_counts)
    finalize = getattr(update_step, "finalize", None)
    if finalize is not None:
        params, optimizer_state = finalize(params, optimizer_state)
    metrics.update(
        {
            "behavior_log_prob_max_abs_error": behavior_log_prob_error,
            "optimizer_steps": float(ppo_epochs * optimizer_steps_per_epoch),
            "microbatches": float(microbatch_count),
            "segments_per_minibatch": float(segments_per_minibatch),
            "effective_minibatch_transitions": float(segments_per_minibatch * rollout.horizon * 2),
            "gradient_accumulation_steps": float(accumulation_steps),
            "segment_order_shuffled": 1.0,
            "valid_transitions": float(sum(metric_sample_counts) / ppo_epochs),
        }
    )
    if partition is not None:
        metrics["global_effective_minibatch_transitions"] = float(partition.games_per_step * rollout.horizon * 2)
    if starts_at_reference and zero_learning_signal and policy_hash(params) != expected_behavior_hash:
        raise RuntimeError("zero-advantage update changed a policy that was identical to its reference")
    return params, optimizer_state, rng, metrics


def value_diagnostics(targets: np.ndarray, predictions: np.ndarray) -> dict[str, float | None]:
    if targets.size == 0:
        return {
            "explained_variance": None,
            "return_mean": None,
            "return_standard_deviation": None,
            "value_mean": None,
            "value_standard_deviation": None,
            "value_bias": None,
            "value_rmse": None,
        }
    residual = targets - predictions
    target_variance = float(np.var(targets))
    explained_variance = 1.0 - float(np.var(residual)) / target_variance if target_variance > 1e-12 else None
    return {
        "explained_variance": explained_variance,
        "return_mean": float(np.mean(targets)),
        "return_standard_deviation": float(np.std(targets)),
        "value_mean": float(np.mean(predictions)),
        "value_standard_deviation": float(np.std(predictions)),
        "value_bias": float(np.mean(predictions - targets)),
        "value_rmse": float(np.sqrt(np.mean(np.square(residual)))),
    }


def grouped_value_diagnostics(
    rollout: RolloutBatch,
    predictions: np.ndarray,
    indices: np.ndarray | None = None,
    targets: np.ndarray | None = None,
) -> dict[str, Any]:
    agents_per_step = rollout.games * 2
    indices = np.arange(rollout.transitions) if indices is None else indices
    selected_targets = rollout.returns[indices] if targets is None else targets[indices]
    seats = indices % agents_per_step % 2
    steps = indices // agents_per_step
    quartile = np.minimum(steps * 4 // rollout.horizon, 3)
    return {
        "global": value_diagnostics(selected_targets, predictions),
        "seat_0": value_diagnostics(selected_targets[seats == 0], predictions[seats == 0]),
        "seat_1": value_diagnostics(selected_targets[seats == 1], predictions[seats == 1]),
        "step_first": value_diagnostics(selected_targets[steps == 0], predictions[steps == 0]),
        "step_last": value_diagnostics(
            selected_targets[steps == rollout.horizon - 1],
            predictions[steps == rollout.horizon - 1],
        ),
        "step_quartiles": [
            value_diagnostics(selected_targets[quartile == bucket], predictions[quartile == bucket])
            for bucket in range(4)
        ],
    }


def terminal_win_targets(rollout: RolloutBatch) -> np.ndarray:
    """Return unbiased gamma-one Monte Carlo outcomes for every state."""
    seat_zero = np.sign(rollout.money[:, 0] - rollout.money[:, 1]).astype(np.float32)
    paired = np.stack((seat_zero, -seat_zero), axis=-1).reshape(-1)
    return np.tile(paired, rollout.horizon)


def critic_validation_metrics(
    rollout: RolloutBatch,
    predictions: np.ndarray,
    indices: np.ndarray,
    *,
    huber_delta: float,
) -> dict[str, Any]:
    targets = terminal_win_targets(rollout)
    residual = targets[indices] - predictions
    absolute_residual = np.abs(residual)
    huber = np.where(
        absolute_residual <= huber_delta,
        0.5 * np.square(residual),
        huber_delta * (absolute_residual - 0.5 * huber_delta),
    )
    return {
        "huber_loss": float(np.mean(huber)),
        "diagnostics": grouped_value_diagnostics(
            rollout,
            predictions,
            indices,
            targets,
        ),
        "sample_transitions": len(indices),
    }


def update_early_stopping(
    best_loss: float,
    stale_updates: int,
    validation_loss: float,
    min_delta: float,
) -> tuple[float, int, bool]:
    improved = validation_loss < best_loss - min_delta
    return (
        validation_loss if improved else best_loss,
        0 if improved else stale_updates + 1,
        improved,
    )


def advantage_diagnostics(rollout: RolloutBatch) -> dict[str, Any]:
    advantages = rollout.advantages.reshape(rollout.horizon, rollout.games, 2)

    def summarize(values: np.ndarray) -> dict[str, float]:
        return {
            "absolute_mean": float(np.mean(np.abs(values))),
            "standard_deviation": float(np.std(values)),
            "nonzero_fraction_1e-8": float(np.mean(np.abs(values) > 1e-8)),
        }

    boundaries = np.linspace(0, rollout.horizon, 5, dtype=np.int64)
    return {
        "global": summarize(advantages),
        "step_quartiles": [summarize(advantages[boundaries[index] : boundaries[index + 1]]) for index in range(4)],
    }


def diagnostic_indices(rollout: RolloutBatch, maximum_transitions: int) -> np.ndarray:
    agents_per_step = rollout.games * 2
    sampled_steps = min(rollout.horizon, max(1, maximum_transitions // agents_per_step))
    steps = np.linspace(0, rollout.horizon - 1, sampled_steps, dtype=np.int64)
    return (steps[:, None] * agents_per_step + np.arange(agents_per_step)[None, :]).reshape(-1)


def evaluate_rollout_policy(
    params: Params,
    rollout: RolloutBatch,
    *,
    evaluator,
    batch_size: int,
    clip: float,
    maximum_transitions: int,
) -> tuple[np.ndarray, dict[str, float | str | int], np.ndarray]:
    evaluation_indices = diagnostic_indices(rollout, maximum_transitions)
    collected: dict[str, list[np.ndarray]] = {}
    for start in range(0, len(evaluation_indices), batch_size):
        stop = min(start + batch_size, len(evaluation_indices))
        valid_count = stop - start
        selected = evaluation_indices[start:stop]
        if valid_count < batch_size:
            selected = np.pad(selected, (0, batch_size - valid_count), mode="wrap")
        batch = {name: jnp.asarray(values[selected]) for name, values in rollout.states.items()}
        batch.update(
            {
                "unit_mask": jnp.asarray(rollout.unit_mask[selected]),
                "unit_action": jnp.asarray(rollout.unit_action[selected]),
                "market_action": jnp.asarray(rollout.market_action[selected]),
            }
        )
        outputs = jax.device_get(evaluator(params, batch))
        for name, values in outputs.items():
            collected.setdefault(name, []).append(np.asarray(values)[:valid_count])

    arrays = {name: np.concatenate(values) for name, values in collected.items()}
    log_ratio = arrays["log_prob"] - rollout.old_log_prob[evaluation_indices]
    ratio = np.exp(log_ratio)
    normalized_entropy = float(np.mean(arrays["normalized_entropy"]))
    status = "low" if normalized_entropy < 0.1 else "high" if normalized_entropy > 0.5 else "target_band"
    metrics: dict[str, float | str | int] = {
        "approx_kl": float(np.mean((ratio - 1.0) - log_ratio)),
        "approx_old_kl": float(np.mean(-log_ratio)),
        "clip_fraction": float(np.mean(np.abs(ratio - 1.0) > clip)),
        "ratio_mean": float(np.mean(ratio)),
        "ratio_standard_deviation": float(np.std(ratio)),
        "entropy": float(np.mean(arrays["entropy"])),
        "unit_entropy": float(np.mean(arrays["unit_entropy"])),
        "market_entropy": float(np.mean(arrays["market_entropy"])),
        "normalized_entropy": normalized_entropy,
        "unit_normalized_entropy": float(np.mean(arrays["unit_normalized_entropy"])),
        "market_normalized_entropy": float(np.mean(arrays["market_normalized_entropy"])),
        "normalized_entropy_status": status,
        "sample_transitions": len(evaluation_indices),
        "sample_fraction": len(evaluation_indices) / rollout.transitions,
    }
    return arrays["value"], metrics, evaluation_indices


def rollout_metrics(
    rollout: RolloutBatch,
    post_update_value: np.ndarray | None = None,
    post_update_indices: np.ndarray | None = None,
) -> dict[str, Any]:
    margins = rollout.money[:, 0] - rollout.money[:, 1]
    pre_update_value = grouped_value_diagnostics(rollout, rollout.value)
    post_update_value_metrics = (
        grouped_value_diagnostics(rollout, post_update_value, post_update_indices)
        if post_update_value is not None
        else None
    )
    return {
        "games": rollout.games,
        "transitions": rollout.transitions,
        "seat0_wins": int(np.sum(margins > 0)),
        "ties": int(np.sum(margins == 0)),
        "seat0_losses": int(np.sum(margins < 0)),
        "mean_margin": float(np.mean(margins)),
        "median_margin": float(np.median(margins)),
        "mean_squashed_margin": float(np.mean(np.tanh(margins / 20_000.0))),
        "advantage_mean": rollout.advantage_mean,
        "advantage_standard_deviation": rollout.advantage_standard_deviation,
        "advantage_diagnostics": advantage_diagnostics(rollout),
        "value_explained_variance": pre_update_value["global"]["explained_variance"],
        "value_pre_update": pre_update_value,
        "value_post_update": post_update_value_metrics,
        "collection_seconds": rollout.collection_seconds,
        "collection_stage_seconds": rollout.stage_seconds,
    }


def append_jsonl(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as destination:
        destination.write(json.dumps(row, sort_keys=True) + "\n")
        destination.flush()
        os.fsync(destination.fileno())


def last_recorded_inner_update(path: Path) -> int:
    if not path.is_file():
        return -1
    with path.open("rb") as source:
        source.seek(0, os.SEEK_END)
        size = source.tell()
        source.seek(max(0, size - 1024 * 1024))
        lines = source.read().splitlines()
    for line in reversed(lines):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("event") == "inner_update":
            return int(row["completed_updates"])
    return -1


def recover_checkpoint_metrics(payload: dict[str, Any], path: Path) -> bool:
    row = payload.get("metadata", {}).get("last_update_metrics")
    if row is None:
        return False
    completed_updates = int(row["completed_updates"])
    if last_recorded_inner_update(path) >= completed_updates:
        return False
    append_jsonl(path, row)
    print(json.dumps({"event": "recovered_checkpoint_metrics", "completed_updates": completed_updates}), flush=True)
    return True


def archive_uncheckpointed_metrics(path: Path, completed_updates: int) -> Path | None:
    if not path.exists():
        return None
    lines = path.read_text().splitlines(keepends=True)
    for index, line in enumerate(lines):
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            # A preemption may leave a partial final line that cannot be appended safely.
            break
        if row.get("event") == "inner_update" and int(row["completed_updates"]) > completed_updates:
            break
    else:
        return None
    archive = path.with_name(f"metrics_before_resume_{completed_updates:04d}_{time.time_ns()}.jsonl")
    retain_checkpoint(path, archive)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w") as destination:
        destination.writelines(lines[:index])
        destination.flush()
        os.fsync(destination.fileno())
    os.replace(temporary, path)
    print(json.dumps({"event": "archived_uncheckpointed_metrics", "archive": str(archive)}), flush=True)
    return archive


def validate_run(args: argparse.Namespace) -> None:
    validate_purchase_temperature(
        args.purchase_temperature_initial,
        args.purchase_temperature_steps,
        args.purchase_temperature_decay_updates,
        args.purchase_temperature_start_update,
        args.purchase_temperature_schedule,
    )
    if args.games <= 0 or args.horizon <= 0 or args.horizon > 719:
        raise ValueError("games must be positive and horizon must be in 1..719")
    if args.outer_iterations <= 0 or args.reference_interval <= 0:
        raise ValueError("outer iterations and reference interval must be positive")
    if args.snapshot_interval < 0:
        raise ValueError("snapshot interval must be non-negative")
    last_best_enabled = args.last_best_control_dir is not None
    if last_best_enabled != (args.last_best_promotion_threshold is not None):
        raise ValueError("last-best control directory and promotion threshold must be configured together")
    if last_best_enabled:
        if not 0.0 <= args.last_best_promotion_threshold <= 1.0:
            raise ValueError("last-best promotion threshold must be in [0, 1]")
        if args.snapshot_interval <= 0:
            raise ValueError("last-best promotion requires periodic policy snapshots")
        if not args.freeze_reference:
            raise ValueError("last-best promotion requires --freeze-reference")
    if args.ppo_epochs <= 0 or args.minibatch <= 0 or args.segments_per_minibatch <= 0:
        raise ValueError("PPO epochs and minibatch must be positive")
    if args.data_parallel_devices <= 0:
        raise ValueError("data-parallel device count must be positive")
    if args.minibatch % args.data_parallel_devices:
        raise ValueError("PPO microbatch must be divisible by the data-parallel device count")
    if (args.minibatch // args.data_parallel_devices) % 2:
        raise ValueError("each device's PPO shard must contain complete seat pairs")
    effective_minibatch = args.segments_per_minibatch * args.horizon * 2
    if effective_minibatch % (2 * args.data_parallel_devices):
        raise ValueError("each device's accumulated PPO shard must contain complete seat pairs")
    if args.data_parallel_rollout:
        if args.inference_batch_size % args.data_parallel_devices:
            raise ValueError("inference batch must be divisible by the data-parallel device count")
        if (args.inference_batch_size // args.data_parallel_devices) % 2:
            raise ValueError("each device's inference shard must contain complete seat pairs")
        if (args.games * 2) % args.data_parallel_devices:
            raise ValueError("parallel game seats must be divisible by the data-parallel device count")
    if args.value_warmup_max_updates < 0:
        raise ValueError("Value warm-up maximum updates must be non-negative")
    if args.initial_critic_checkpoint is not None and args.value_warmup_max_updates != 0:
        raise ValueError("an initial critic checkpoint requires --value-warmup-max-updates 0")
    if args.value_warmup_patience <= 0 or args.value_warmup_min_delta < 0.0:
        raise ValueError("Value warm-up patience must be positive and minimum delta non-negative")
    if args.value_validation_games is not None and args.value_validation_games <= 0:
        raise ValueError("Value validation games must be positive")
    paired_batch = args.games * 2
    if args.ppo_epochs != 1:
        raise ValueError("Full-game self-play uses exactly one PPO epoch")
    if args.reference_kl_samples <= 0 or args.reference_kl_samples % 2:
        raise ValueError("reference KL samples must be a positive number of seat pairs")
    if args.reference_kl_samples > args.minibatch:
        raise ValueError("reference KL samples must fit in one PPO microbatch")
    if args.kl_coefficient < 0.0 or args.entropy_coefficient < 0.0:
        raise ValueError("KL and entropy coefficients must be non-negative")
    validate_opening_entropy(args.opening_entropy_steps, args.opening_entropy_multiplier)
    validate_purchase_entropy(args.purchase_entropy_coefficient, args.purchase_entropy_steps)
    if args.allow_purchase_entropy_change and args.resume is None:
        raise ValueError("purchase entropy override requires --resume")
    if args.allow_opening_entropy_change and args.resume is None:
        raise ValueError("opening entropy override requires --resume")
    if args.allow_fixed_entropy_change and args.resume is None:
        raise ValueError("fixed entropy override requires --resume")
    if args.entropy_floor is not None and not 0.0 <= args.entropy_floor <= 1.0:
        raise ValueError("entropy floor must be in [0, 1]")
    if args.entropy_coefficient_growth <= 1.0:
        raise ValueError("entropy coefficient growth must exceed one")
    if args.entropy_coefficient_max < args.entropy_coefficient:
        raise ValueError("maximum entropy coefficient must not be below its initial value")
    head_config = head_entropy_config_from_args(args)
    if args.uncapped_entropy and head_config is None:
        raise ValueError("--uncapped-entropy requires both per-head targets")
    if args.inference_batch_size != paired_batch:
        raise ValueError("inference minibatch must equal games * 2 seats")
    if args.minibatch % 2:
        raise ValueError("PPO microbatch must contain complete seat pairs")
    if args.games % args.segments_per_minibatch:
        raise ValueError("games must be divisible by segments per minibatch")
    if args.value_warmup_max_updates > 0 and args.minibatch != paired_batch:
        raise ValueError("in-process Value warm-up requires one complete time slice per microbatch")
    if args.diagnostics_transitions < args.games * 2:
        raise ValueError("diagnostics transitions must cover both seats of every rollout game")
    if args.attention_backend == "cudnn" and args.compute_dtype != "bfloat16":
        raise ValueError("cuDNN attention requires bfloat16 compute")
    if args.environment_seed_start < 0:
        raise ValueError("environment seed start must be non-negative")
    training_seed_stop = args.environment_seed_start + args.games * args.value_warmup_max_updates
    validation_games = args.games if args.value_validation_games is None else args.value_validation_games
    validation_seed_stop = args.value_validation_seed_start + validation_games
    seeds_overlap = (
        args.environment_seed_start < validation_seed_stop and args.value_validation_seed_start < training_seed_stop
    )
    if args.value_validation_seed_start < 0 or seeds_overlap:
        raise ValueError("Value validation seeds must be non-negative and disjoint from warm-up seeds")
    if not 0.0 <= args.gae_lambda <= 1.0 or not 0.0 < args.gamma <= 1.0:
        raise ValueError("GAE lambda and gamma must be probabilities")
    if args.learning_rate <= 0.0 or args.adam_epsilon <= 0.0:
        raise ValueError("Adam learning rate and epsilon must be positive")
    if args.lr_decay_steps <= 0 or not 0.0 < args.lr_min_ratio <= 1.0:
        raise ValueError("LR decay steps and minimum ratio are invalid")
    if not args.smoke and args.horizon != 719:
        raise ValueError("non-smoke training must use the full 719-transition horizon")
    if args.max_env_steps is not None and args.max_env_steps <= 0:
        raise ValueError("max env steps must be positive")


RESIZE_FIELDS = frozenset(
    {"data_parallel_devices", "games", "segments_per_minibatch", "minibatch", "inference_batch_size"}
)


def validate_data_parallel_resize(saved: dict[str, Any], current: dict[str, Any]) -> None:
    for config in (saved, current):
        if not config.get("data_parallel_rollout"):
            raise ValueError("data-parallel resize requires sharded rollout")
        if any(not isinstance(config.get(name), int) or config[name] <= 0 for name in RESIZE_FIELDS):
            raise ValueError("data-parallel resize requires positive device and batch counts")
        if config["data_parallel_devices"] == 1:
            raise ValueError("data-parallel resize cannot change the single-device optimizer structure")
        if config["games"] % config["segments_per_minibatch"]:
            raise ValueError("data-parallel resize must preserve complete optimizer batches")
        if config["inference_batch_size"] != 2 * config["games"]:
            raise ValueError("data-parallel resize must preserve complete rollout seat pairs")
    old_devices, new_devices = saved["data_parallel_devices"], current["data_parallel_devices"]
    for name in RESIZE_FIELDS - {"data_parallel_devices"}:
        if saved[name] * new_devices != current[name] * old_devices:
            raise ValueError(f"data-parallel resize changes per-device {name}")
    for config in (saved, current):
        if config["minibatch"] % (2 * config["data_parallel_devices"]):
            raise ValueError("data-parallel resize must preserve per-device seat pairs")


def validate_resume_config(saved: dict[str, Any], current: dict[str, Any]) -> None:
    saved = {**saved}
    current = {**current}
    for name, default in HEAD_ENTROPY_DEFAULTS.items():
        saved.setdefault(name, default)
        current.setdefault(name, default)
    for name, default in OPENING_ENTROPY_DEFAULTS.items():
        saved.setdefault(name, default)
        current.setdefault(name, default)
    for name, default in PURCHASE_ENTROPY_DEFAULTS.items():
        saved.setdefault(name, default)
        current.setdefault(name, default)
    for name, default in PURCHASE_TEMPERATURE_DEFAULTS.items():
        saved.setdefault(name, default)
        current.setdefault(name, default)
    saved.setdefault("rope_correction_backend", "dense")
    if saved.get("data_parallel_devices") is None:
        saved["data_parallel_devices"] = 1
    if saved.get("data_parallel_rollout") is None:
        saved["data_parallel_rollout"] = False
    saved.setdefault("last_best_control_dir", None)
    saved.setdefault("last_best_promotion_threshold", None)
    saved.setdefault("entropy_floor", None)
    saved.setdefault("entropy_coefficient_growth", 2.0)
    saved.setdefault("entropy_coefficient_max", 1e-4)
    if current.get("allow_fixed_entropy_change", False):
        validate_fixed_entropy_override(saved, current)
    resize = current.get("allow_data_parallel_resize", False) and any(
        saved.get(name) != current.get(name) for name in RESIZE_FIELDS
    )
    if resize:
        validate_data_parallel_resize(saved, current)
    differences = {
        name: (saved.get(name), current.get(name))
        for name in RESUME_FIXED_FIELDS
        if saved.get(name) != current.get(name)
        and not (name in HEAD_ENTROPY_DEFAULTS and current.get("allow_entropy_control_change", False))
        and not (name in FIXED_ENTROPY_FIELDS and current.get("allow_fixed_entropy_change", False))
        and not (name in OPENING_ENTROPY_DEFAULTS and current.get("allow_opening_entropy_change", False))
        and not (name in PURCHASE_ENTROPY_DEFAULTS and current.get("allow_purchase_entropy_change", False))
        and not (name in PURCHASE_TEMPERATURE_DEFAULTS and current.get("allow_purchase_temperature_change", False))
        and not (resize and name in RESIZE_FIELDS)
    }
    if differences:
        raise ValueError(f"resume configuration mismatch: {differences}")


def run_value_warmup(
    initial_params: Params,
    model_config: JaxModelConfig,
    ppo_config: PPOConfig,
    args: argparse.Namespace,
    *,
    compute_dtype: jnp.dtype,
    source_checkpoint_sha256: str,
    log_prob_evaluator,
    policy_diagnostics_evaluator,
    sampler,
) -> tuple[Params, jax.Array, int]:
    if args.value_warmup_max_updates == 0:
        return initial_params, jax.random.PRNGKey(args.seed), args.environment_seed_start

    warmup_checkpoint = args.output_dir / "value_warmup_latest_jax.pkl"
    best_checkpoint = args.output_dir / "value_warmup_best_jax.pkl"
    resume_warmup = warmup_checkpoint.exists()
    warmup_training_config = {**serializable_args(args), "phase": "value_warmup"}
    value_optimizer = make_optimizer(ppo_config)
    initial_actor_hash = actor_hash(initial_params)
    if resume_warmup:
        state, payload = load_checkpoint(warmup_checkpoint)
        if payload["source_checkpoint_sha256"] != source_checkpoint_sha256:
            raise ValueError("Value warm-up checkpoint uses a different BC checkpoint")
        if payload["model_config"] != model_config.to_dict():
            raise ValueError("Value warm-up checkpoint model configuration mismatch")
        saved_warmup_config = {**payload["training_config"]}
        saved_warmup_config.pop("value_warmup_min_updates", None)
        if saved_warmup_config != warmup_training_config:
            raise ValueError("Value warm-up checkpoint training configuration mismatch")
        if state.completed_updates > args.value_warmup_max_updates:
            raise ValueError("Value warm-up checkpoint is ahead of the requested update count")
        early_stopping = payload.get("metadata", {}).get("early_stopping")
        if early_stopping is None:
            raise ValueError("Value warm-up checkpoint lacks early-stopping state")
        best_loss = float(early_stopping["best_loss"])
        best_update = int(early_stopping["best_update"])
        stale_updates = int(early_stopping["stale_updates"])
    else:
        state = initialize_state(
            initial_params,
            value_optimizer.init(initial_params),
            seed=args.seed,
            environment_seed_start=args.environment_seed_start,
        )
    validation_rollout, _ = collect_self_play(
        initial_params,
        model_config,
        games=args.games if args.value_validation_games is None else args.value_validation_games,
        horizon=args.horizon,
        seed_counter=args.value_validation_seed_start,
        rng=jax.random.fold_in(jax.random.PRNGKey(args.seed), 0x56414C),
        compute_dtype=compute_dtype,
        gamma=args.gamma,
        gae_lambda=args.gae_lambda,
        sampler=sampler,
        inference_batch_size=args.inference_batch_size,
        pinned_feature_buffer=args.pinned_feature_buffer,
    )
    baseline_value, baseline_policy, validation_indices = evaluate_rollout_policy(
        state.params,
        validation_rollout,
        evaluator=policy_diagnostics_evaluator,
        batch_size=args.inference_batch_size,
        clip=args.clip,
        maximum_transitions=args.diagnostics_transitions,
    )
    baseline_validation = critic_validation_metrics(
        validation_rollout,
        baseline_value,
        validation_indices,
        huber_delta=args.value_huber_delta,
    )
    if not resume_warmup:
        best_loss = float(baseline_validation["huber_loss"])
        best_update = 0
        stale_updates = 0
        metadata = {
            "early_stopping": {
                "best_loss": best_loss,
                "best_update": best_update,
                "stale_updates": stale_updates,
            }
        }
        save_checkpoint(
            best_checkpoint,
            state,
            model_config=model_config.to_dict(),
            training_config=warmup_training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metadata=metadata,
        )
        save_checkpoint(
            warmup_checkpoint,
            state,
            model_config=model_config.to_dict(),
            training_config=warmup_training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metadata=metadata,
        )
        baseline_row = {
            "event": "value_validation_baseline",
            "completed_updates": 0,
            "actor_sha256": initial_actor_hash,
            "validation": baseline_validation,
            "validation_policy": baseline_policy,
        }
        append_jsonl(args.output_dir / "value_warmup_metrics.jsonl", baseline_row)
        print(json.dumps(baseline_row, sort_keys=True), flush=True)

    value_update_step = make_full_value_update_step(model_config, ppo_config, compute_dtype, value_optimizer)
    patience_exhausted = stale_updates >= args.value_warmup_patience
    stop_reason = "patience" if patience_exhausted else "max_updates"
    while state.completed_updates < args.value_warmup_max_updates and not patience_exhausted:
        iteration_started = time.monotonic()
        rollout, rollout_rng = collect_self_play(
            state.params,
            model_config,
            games=args.games,
            horizon=args.horizon,
            seed_counter=state.seed_counter,
            rng=state.rng,
            compute_dtype=compute_dtype,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            sampler=sampler,
            inference_batch_size=args.inference_batch_size,
            pinned_feature_buffer=args.pinned_feature_buffer,
        )
        update_started = time.monotonic()
        params, optimizer_state, update_metrics = full_value_update(
            state.params,
            state.optimizer_state,
            rollout,
            update_step=value_update_step,
            log_prob_evaluator=log_prob_evaluator,
            minibatch_size=args.minibatch,
            completed_warmup_updates=state.completed_updates,
        )
        update_seconds = time.monotonic() - update_started
        diagnostics_started = time.monotonic()
        post_update_value, post_update_policy, post_update_indices = evaluate_rollout_policy(
            params,
            rollout,
            evaluator=policy_diagnostics_evaluator,
            batch_size=args.inference_batch_size,
            clip=args.clip,
            maximum_transitions=args.diagnostics_transitions,
        )
        validation_value, validation_policy, evaluated_validation_indices = evaluate_rollout_policy(
            params,
            validation_rollout,
            evaluator=policy_diagnostics_evaluator,
            batch_size=args.inference_batch_size,
            clip=args.clip,
            maximum_transitions=args.diagnostics_transitions,
        )
        if not np.array_equal(evaluated_validation_indices, validation_indices):
            raise RuntimeError("Value validation sample changed during warm-up")
        validation = critic_validation_metrics(
            validation_rollout,
            validation_value,
            validation_indices,
            huber_delta=args.value_huber_delta,
        )
        diagnostics_seconds = time.monotonic() - diagnostics_started
        state = replace(
            state,
            params=params,
            optimizer_state=optimizer_state,
            rng=rollout_rng,
            seed_counter=rollout.seed_end,
            completed_updates=state.completed_updates + 1,
            last_behavior_hash=rollout.behavior_hash,
        )
        best_loss, stale_updates, improved = update_early_stopping(
            best_loss,
            stale_updates,
            float(validation["huber_loss"]),
            args.value_warmup_min_delta,
        )
        if improved:
            best_update = state.completed_updates
        early_stopping = {
            "best_loss": best_loss,
            "best_update": best_update,
            "stale_updates": stale_updates,
            "improved": improved,
        }
        if improved:
            save_checkpoint(
                best_checkpoint,
                state,
                model_config=model_config.to_dict(),
                training_config=warmup_training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={"early_stopping": early_stopping},
            )
        save_checkpoint(
            warmup_checkpoint,
            state,
            model_config=model_config.to_dict(),
            training_config=warmup_training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metadata={"early_stopping": early_stopping},
        )
        row = {
            "event": "value_warmup_update",
            "completed_updates": state.completed_updates,
            "initial_actor_sha256": initial_actor_hash,
            "actor_sha256": actor_hash(state.params),
            "critic_policy_sha256": policy_hash(state.params),
            "iteration_seconds": time.monotonic() - iteration_started,
            "update_seconds": update_seconds,
            "diagnostics_seconds": diagnostics_seconds,
            "rollout": rollout_metrics(rollout, post_update_value, post_update_indices),
            "update": update_metrics,
            "post_update_policy": post_update_policy,
            "validation": validation,
            "validation_policy": validation_policy,
            "early_stopping": early_stopping,
        }
        append_jsonl(args.output_dir / "value_warmup_metrics.jsonl", row)
        print(json.dumps(row, sort_keys=True), flush=True)
        del rollout

        if stale_updates >= args.value_warmup_patience:
            stop_reason = "patience"
            break

    if not best_checkpoint.exists():
        raise RuntimeError("Value warm-up has no best checkpoint")
    best_state, best_payload = load_checkpoint(best_checkpoint)
    state = replace(state, params=best_state.params, reference_params=best_state.params)

    complete_row = {
        "event": "value_warmup_complete",
        "completed_updates": state.completed_updates,
        "best_update": best_update,
        "best_validation_loss": best_loss,
        "stop_reason": stop_reason,
        "initial_actor_sha256": initial_actor_hash,
        "actor_sha256": actor_hash(state.params),
        "critic_policy_sha256": policy_hash(state.params),
        "best_checkpoint_policy_sha256": best_payload["policy_sha256"],
    }
    append_jsonl(args.output_dir / "value_warmup_metrics.jsonl", complete_row)
    print(json.dumps(complete_row, sort_keys=True), flush=True)
    return state.params, state.rng, state.seed_counter


def apply_last_best_promotion(
    state: LoopState,
    *,
    control_dir: Path | None,
    checkpoint_path: Path,
    model_config: dict[str, Any],
    training_config: dict[str, Any],
    source_checkpoint_sha256: str,
    metrics_path: Path,
) -> LoopState:
    if control_dir is None:
        return state
    plan = prepare_pending_promotion(control_dir, state, model_config)
    if plan is None:
        return state

    state = plan.state
    save_checkpoint(
        checkpoint_path,
        state,
        model_config=model_config,
        training_config=training_config,
        source_checkpoint_sha256=source_checkpoint_sha256,
    )
    commit_promotion(control_dir, plan)
    event = {
        "event": "last_best_promotion",
        "teacher_generation": plan.next_teacher.generation,
        "teacher_source_update": plan.next_teacher.source_update,
        "reference_sha256": plan.next_teacher.policy_sha256,
        "wins": int(plan.request["wins"]),
        "ties": int(plan.request["ties"]),
        "losses": int(plan.request["losses"]),
        "win_rate": float(plan.request["win_rate"]),
        "promotion_threshold": plan.next_teacher.promotion_threshold,
    }
    append_jsonl(metrics_path, event)
    print(json.dumps(event, sort_keys=True), flush=True)
    return state


def main() -> None:
    args = parse_args()
    validate_run(args)
    head_entropy_config = head_entropy_config_from_args(args)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.output_dir / "latest_jax.pkl"
    policy_path = args.output_dir / "policy_latest_jax.pkl"
    source_checkpoint_sha256 = file_sha256(args.bc_checkpoint)
    ppo_config = PPOConfig(
        clip=args.clip,
        kl_coefficient=args.kl_coefficient,
        teacher_divergence=args.teacher_divergence,
        entropy_coefficient=args.entropy_coefficient,
        opening_entropy_steps=args.opening_entropy_steps,
        opening_entropy_multiplier=args.opening_entropy_multiplier,
        purchase_entropy_coefficient=args.purchase_entropy_coefficient,
        purchase_entropy_steps=args.purchase_entropy_steps,
        purchase_entropy_metrics=args.purchase_entropy_metrics,
        value_coefficient=args.value_coefficient,
        value_huber_delta=args.value_huber_delta,
        gradient_norm=args.gradient_norm,
        learning_rate=args.learning_rate,
        adam_epsilon=args.adam_epsilon,
        lr_decay_steps=args.lr_decay_steps,
        lr_warmup_steps=args.lr_warmup_steps,
        lr_min_ratio=args.lr_min_ratio,
        reference_kl_samples=args.reference_kl_samples,
        normalize_advantages=args.normalize_advantages,
    )
    compute_dtype = jnp.bfloat16 if args.compute_dtype == "bfloat16" else jnp.float32
    accumulation_steps = gradient_accumulation_steps(
        segments_per_minibatch=args.segments_per_minibatch,
        horizon=args.horizon,
        microbatch_size=args.minibatch,
    )
    data_parallel_devices = select_data_parallel_devices(args.data_parallel_devices)
    rollout_devices = data_parallel_devices if args.data_parallel_rollout else data_parallel_devices[:1]
    optimizer = make_optimizer(
        ppo_config,
        gradient_accumulation_steps=accumulation_steps,
        data_parallel_axis_name="data" if len(data_parallel_devices) > 1 else None,
    )
    initial_params, model_config = load_bc_checkpoint(args.bc_checkpoint)
    model_config = replace(
        model_config,
        attention_backend=args.attention_backend,
        rope_correction_backend=args.rope_correction_backend,
        dropout=0.0,
        sequential_patch=model_config.sequential_patch or args.enable_sequential_masks,
    )
    model_config.validate()
    initial_critic_checkpoint_sha256 = None
    if args.initial_critic_checkpoint is not None:
        initial_params = load_initial_critic_checkpoint(
            args.initial_critic_checkpoint,
            initial_params,
            model_config,
        )
        initial_critic_checkpoint_sha256 = file_sha256(args.initial_critic_checkpoint)

    training_config = {
        **serializable_args(args),
        "initial_critic_checkpoint_sha256": initial_critic_checkpoint_sha256,
        "effective_minibatch_transitions": args.segments_per_minibatch * args.horizon * 2,
        "gradient_accumulation_steps": accumulation_steps,
        "optimizer_steps_per_update": args.ppo_epochs * args.games // args.segments_per_minibatch,
        "data_parallel_device_names": [str(device) for device in data_parallel_devices],
        "rollout_device_names": [str(device) for device in rollout_devices],
        "xla_flags": os.environ.get("XLA_FLAGS", ""),
    }
    log_prob_evaluator = make_log_prob_evaluator(model_config, compute_dtype, rollout_devices)
    policy_diagnostics_evaluator = make_policy_diagnostics_evaluator(
        model_config,
        compute_dtype,
        rollout_devices,
    )
    sampler = make_sampler(model_config, compute_dtype, rollout_devices)

    if args.resume is not None:
        state, resume_payload = load_checkpoint(args.resume)
        if resume_payload["source_checkpoint_sha256"] != source_checkpoint_sha256:
            raise ValueError("resume checkpoint was initialized from a different BC checkpoint")
        if (
            resume_payload["training_config"].get("initial_critic_checkpoint_sha256")
            != initial_critic_checkpoint_sha256
        ):
            raise ValueError("resume checkpoint was initialized from a different critic checkpoint")
        resume_model_config = {**resume_payload["model_config"]}
        resume_model_config.setdefault("rope_correction_backend", "dense")
        if args.enable_sequential_masks:
            resume_model_config["sequential_patch"] = True
        if resume_model_config != model_config.to_dict():
            raise ValueError("resume checkpoint model config does not match the BC checkpoint")
        validate_resume_config(resume_payload["training_config"], serializable_args(args))
        archive_uncheckpointed_metrics(args.output_dir / "metrics.jsonl", state.completed_updates)
        recover_checkpoint_metrics(resume_payload, args.output_dir / "metrics.jsonl")
        previous_temperature = {
            name: resume_payload["training_config"].get(name, default)
            for name, default in PURCHASE_TEMPERATURE_DEFAULTS.items()
        }
        current_temperature = {name: getattr(args, name) for name in PURCHASE_TEMPERATURE_DEFAULTS}
        if previous_temperature != current_temperature:
            backup = args.output_dir / f"before_purchase_temperature_update_{state.completed_updates:04d}.pkl"
            retain_checkpoint(args.resume, backup)
            temperature_event = {
                "event": "purchase_temperature_schedule_changed",
                "completed_updates": state.completed_updates,
                "previous": previous_temperature,
                "current": current_temperature,
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
                "optimizer_sha256": policy_hash(state.optimizer_state),
                "rng_sha256": policy_hash(state.rng),
                "seed_counter": state.seed_counter,
                "backup": str(backup),
            }
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={**resume_payload.get("metadata", {}), "purchase_temperature_change": temperature_event},
            )
            append_jsonl(args.output_dir / "metrics.jsonl", temperature_event)
            print(json.dumps(temperature_event, sort_keys=True), flush=True)
        previous_purchase = {
            name: resume_payload["training_config"].get(name, default)
            for name, default in PURCHASE_ENTROPY_DEFAULTS.items()
        }
        current_purchase = {name: getattr(args, name) for name in PURCHASE_ENTROPY_DEFAULTS}
        if previous_purchase != current_purchase:
            backup = args.output_dir / f"before_purchase_entropy_update_{state.completed_updates:04d}.pkl"
            retain_checkpoint(args.resume, backup)
            purchase_event = {
                "event": "purchase_entropy_schedule_changed",
                "completed_updates": state.completed_updates,
                "previous": previous_purchase,
                "current": current_purchase,
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
                "optimizer_sha256": policy_hash(state.optimizer_state),
                "rng_sha256": policy_hash(state.rng),
                "seed_counter": state.seed_counter,
                "backup": str(backup),
            }
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={**resume_payload.get("metadata", {}), "purchase_entropy_change": purchase_event},
            )
            append_jsonl(args.output_dir / "metrics.jsonl", purchase_event)
            print(json.dumps(purchase_event, sort_keys=True), flush=True)
        old_opening = {
            name: resume_payload["training_config"].get(name, default)
            for name, default in OPENING_ENTROPY_DEFAULTS.items()
        }
        new_opening = {name: getattr(args, name) for name in OPENING_ENTROPY_DEFAULTS}
        if old_opening != new_opening:
            backup = args.output_dir / f"before_opening_entropy_update_{state.completed_updates:04d}.pkl"
            retain_checkpoint(args.resume, backup)
            opening_event = {
                "event": "opening_entropy_schedule_changed",
                "completed_updates": state.completed_updates,
                "previous": old_opening,
                "current": new_opening,
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
                "optimizer_sha256": policy_hash(state.optimizer_state),
                "rng_sha256": policy_hash(state.rng),
                "base_coefficient": state.entropy_coefficient,
                "backup": str(backup),
            }
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={**resume_payload.get("metadata", {}), "opening_entropy_change": opening_event},
            )
            append_jsonl(args.output_dir / "metrics.jsonl", opening_event)
            print(json.dumps(opening_event, sort_keys=True), flush=True)
        if resume_payload["training_config"].get("data_parallel_devices", 1) != args.data_parallel_devices:
            if int(state.optimizer_state.mini_step) != 0:
                raise ValueError("GPU resize requires a completed gradient-accumulation boundary")
            event = {
                "event": "data_parallel_resized",
                "completed_updates": state.completed_updates,
                "previous": {name: resume_payload["training_config"].get(name) for name in sorted(RESIZE_FIELDS)},
                "current": {name: training_config[name] for name in sorted(RESIZE_FIELDS)},
                "gradient_accumulation_steps": accumulation_steps,
                "optimizer_steps_per_update": training_config["optimizer_steps_per_update"],
                "optimizer_step": int(state.optimizer_state.gradient_step),
                "seed_counter": state.seed_counter,
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
                "entropy_control": None if state.entropy_control is None else state.entropy_control.to_dict(),
            }
            append_jsonl(args.output_dir / "metrics.jsonl", event)
            print(json.dumps(event, sort_keys=True), flush=True)
    else:
        warmed_params, warmed_rng, warmed_seed_counter = run_value_warmup(
            initial_params,
            model_config,
            ppo_config,
            args,
            compute_dtype=compute_dtype,
            source_checkpoint_sha256=source_checkpoint_sha256,
            log_prob_evaluator=log_prob_evaluator,
            policy_diagnostics_evaluator=policy_diagnostics_evaluator,
            sampler=sampler,
        )
        state = initialize_state(
            warmed_params,
            optimizer.init(warmed_params),
            seed=args.seed,
            environment_seed_start=warmed_seed_counter,
            entropy_coefficient=args.entropy_coefficient,
        )
        state = replace(state, rng=warmed_rng)

    training_config["ppo_seed_start"] = (
        resume_payload["training_config"].get("ppo_seed_start", state.seed_counter)
        if args.resume is not None
        else state.seed_counter
    )

    if args.inherit_entropy_checkpoint is not None:
        if head_entropy_config is None:
            raise ValueError("entropy inheritance requires both per-head entropy targets")
        state, inheritance_event = inherit_entropy_coefficients(
            state, args.inherit_entropy_checkpoint, head_entropy_config
        )
        if inheritance_event is not None:
            if args.resume is not None:
                backup_path = args.output_dir / f"before_entropy_inheritance_update_{state.completed_updates:04d}.pkl"
                if not backup_path.exists():
                    atomic_pickle(backup_path, resume_payload)
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={
                    **(resume_payload.get("metadata", {}) if args.resume is not None else {}),
                    "entropy_inheritance": inheritance_event,
                },
            )
            append_jsonl(args.output_dir / "metrics.jsonl", inheritance_event)
            print(json.dumps(inheritance_event, sort_keys=True), flush=True)

    if head_entropy_config is not None:
        if state.entropy_control is None:
            state = replace(
                state,
                entropy_control=HeadEntropyState.initialize(state.entropy_coefficient, head_entropy_config),
            )
            event = {
                "event": "head_entropy_control_enabled",
                "completed_updates": state.completed_updates,
                "unit_target": head_entropy_config.unit_target,
                "market_target": head_entropy_config.market_target,
                "initial_state": state.entropy_control.to_dict(),
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
            }
            append_jsonl(args.output_dir / "metrics.jsonl", event)
            print(json.dumps(event, sort_keys=True), flush=True)
        else:
            event = {
                "event": "head_entropy_control_resumed",
                "completed_updates": state.completed_updates,
                "coefficient_max": head_entropy_config.maximum,
                "state": state.entropy_control.to_dict(),
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
            }
            append_jsonl(args.output_dir / "metrics.jsonl", event)
            print(json.dumps(event, sort_keys=True), flush=True)
    elif state.entropy_control is not None:
        raise ValueError("cannot resume a per-head entropy controller without its targets")

    if args.allow_fixed_entropy_change:
        previous_coefficient = state.entropy_coefficient
        state, entropy_event = change_fixed_entropy(state, args.entropy_coefficient)
        if entropy_event is not None:
            backup = args.output_dir / (
                f"before_fixed_entropy_change_update_{state.completed_updates:04d}_"
                f"{previous_coefficient:g}_to_{args.entropy_coefficient:g}.pkl"
            )
            retain_checkpoint(args.resume, backup)
            entropy_event["previous_checkpoint_sha256"] = file_sha256(backup)
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
                metadata={**resume_payload.get("metadata", {}), "fixed_entropy_change": entropy_event},
            )
            append_jsonl(args.output_dir / "metrics.jsonl", entropy_event)
            print(json.dumps(entropy_event, sort_keys=True), flush=True)

    if state.reference_refresh_pending:
        state = retain_reference(state) if args.freeze_reference else refresh_reference(state)
        save_checkpoint(
            checkpoint_path,
            state,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
        )
    if args.resume is not None and state.outer_iteration > 0 and state.inner_iteration == 0:
        boundary_path = args.output_dir / f"outer_{state.outer_iteration:04d}_jax.pkl"
        if not boundary_path.exists():
            save_checkpoint(
                boundary_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
            )
        save_policy_payload(policy_path, state, model_config.to_dict())

    if args.resume is None:
        storage_pause = checkpoint_storage_pause(args.output_dir, state.completed_updates)
        if storage_pause is not None:
            append_jsonl(args.output_dir / "metrics.jsonl", storage_pause)
            print(json.dumps(storage_pause, sort_keys=True), flush=True)
            return

    if args.last_best_control_dir is not None:
        initialize_teacher_control(
            args.last_best_control_dir,
            state,
            model_config.to_dict(),
            promotion_threshold=args.last_best_promotion_threshold,
            resume=args.resume is not None,
        )

    if args.resume is None:
        save_checkpoint(
            checkpoint_path,
            state,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
        )
        save_policy_payload(policy_path, state, model_config.to_dict())

    if args.snapshot_interval and state.completed_updates % args.snapshot_interval == 0:
        retain_checkpoint(
            checkpoint_path,
            args.output_dir / "checkpoints" / f"checkpoint_update_{state.completed_updates:04d}_jax.pkl",
        )
        resume_snapshot = args.output_dir / "async_checkpoints" / f"policy_update_{state.completed_updates:04d}_jax.pkl"
        if not resume_snapshot.exists():
            save_policy_payload(resume_snapshot, state, model_config.to_dict())

    if args.last_best_control_dir is not None:
        state = apply_last_best_promotion(
            state,
            control_dir=args.last_best_control_dir,
            checkpoint_path=checkpoint_path,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metrics_path=args.output_dir / "metrics.jsonl",
        )

    update_step = make_update_step(
        model_config,
        ppo_config,
        compute_dtype,
        optimizer,
        data_parallel_devices,
    )
    print(
        json.dumps(
            {
                "event": "start",
                "xla_flags": os.environ.get("XLA_FLAGS", ""),
                "devices": [str(device) for device in data_parallel_devices],
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
                "source_checkpoint_sha256": source_checkpoint_sha256,
                "initial_critic_checkpoint_sha256": initial_critic_checkpoint_sha256,
                "config": training_config,
            },
            sort_keys=True,
        ),
        flush=True,
    )
    rollout_workspace = (
        RolloutWorkspace.create(
            games=args.games,
            horizon=args.horizon,
            compute_dtype=compute_dtype,
            pin_features=args.pinned_feature_buffer,
            legal_mask=model_config.legal_mask,
        )
        if model_config.rope_correction_backend == "partitioned"
        else None
    )

    last_update_metrics = None
    while state.outer_iteration < args.outer_iterations:
        env_steps = (state.seed_counter - training_config["ppo_seed_start"]) * 2 * args.horizon
        if args.max_env_steps is not None and env_steps >= args.max_env_steps:
            break
        if args.max_inner_updates is not None and state.completed_updates >= args.max_inner_updates:
            break
        storage_pause = checkpoint_storage_pause(args.output_dir, state.completed_updates)
        if storage_pause is not None:
            (args.output_dir / "storage_pause.json").write_text(json.dumps(storage_pause, indent=2) + "\n")
            append_jsonl(args.output_dir / "metrics.jsonl", storage_pause)
            print(json.dumps(storage_pause, sort_keys=True), flush=True)
            break
        state = apply_last_best_promotion(
            state,
            control_dir=args.last_best_control_dir,
            checkpoint_path=checkpoint_path,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metrics_path=args.output_dir / "metrics.jsonl",
        )
        iteration_started = time.monotonic()
        behavior_hash = policy_hash(state.params)
        rollout_temperature = purchase_temperature(
            state.completed_updates,
            args.purchase_temperature_initial,
            args.purchase_temperature_decay_updates,
            args.purchase_temperature_start_update,
            args.purchase_temperature_schedule,
        )
        rollout, rollout_rng = collect_self_play(
            state.params,
            model_config,
            games=args.games,
            horizon=args.horizon,
            seed_counter=state.seed_counter,
            rng=state.rng,
            compute_dtype=compute_dtype,
            gamma=args.gamma,
            gae_lambda=args.gae_lambda,
            sampler=sampler,
            inference_batch_size=args.inference_batch_size,
            pinned_feature_buffer=args.pinned_feature_buffer,
            workspace=rollout_workspace,
            purchase_temperature=rollout_temperature,
            purchase_temperature_steps=args.purchase_temperature_steps,
            purchase_temperature_enabled=args.purchase_temperature_initial != 1.0,
        )
        rollout_state = replace(state, rng=rollout_rng)
        update_started = time.monotonic()
        params, optimizer_state, update_rng, update_metrics = ppo_update(
            rollout_state,
            rollout,
            update_step=update_step,
            log_prob_evaluator=log_prob_evaluator,
            ppo_epochs=args.ppo_epochs,
            minibatch_size=args.minibatch,
            segments_per_minibatch=args.segments_per_minibatch,
            accumulation_steps=accumulation_steps,
            parity_failure_dir=args.output_dir / "behavior_parity_failures",
        )
        update_seconds = time.monotonic() - update_started
        diagnostics_started = time.monotonic()
        post_update_value, post_update_policy, post_update_indices = evaluate_rollout_policy(
            params,
            rollout,
            evaluator=policy_diagnostics_evaluator,
            batch_size=args.inference_batch_size,
            clip=args.clip,
            maximum_transitions=args.diagnostics_transitions,
        )
        diagnostics_seconds = time.monotonic() - diagnostics_started
        state = finish_inner_update(
            state,
            params=params,
            optimizer_state=optimizer_state,
            rng=update_rng,
            seed_counter=rollout.seed_end,
            behavior_hash=behavior_hash,
            reference_interval=args.reference_interval,
        )
        entropy_coefficient_used = state.entropy_coefficient
        normalized_entropy = float(post_update_policy["normalized_entropy"])
        if head_entropy_config is not None:
            controller, entropy_control_metrics = update_head_entropy(
                state.entropy_control,
                head_entropy_config,
                float(post_update_policy["unit_normalized_entropy"]),
                float(post_update_policy["market_normalized_entropy"]),
            )
            state = replace(state, entropy_control=controller)
        else:
            next_entropy_coefficient = adjusted_entropy_coefficient(
                state.entropy_coefficient,
                normalized_entropy,
                floor=args.entropy_floor,
                growth=args.entropy_coefficient_growth,
                maximum=args.entropy_coefficient_max,
            )
            state = replace(state, entropy_coefficient=next_entropy_coefficient)
            entropy_control_metrics = {
                "normalized_entropy": normalized_entropy,
                "floor": args.entropy_floor,
                "coefficient_used": entropy_coefficient_used,
                "coefficient_next": state.entropy_coefficient,
                "adjusted": state.entropy_coefficient != entropy_coefficient_used,
            }
        policy_snapshot = None
        if args.snapshot_interval and state.completed_updates % args.snapshot_interval == 0:
            policy_snapshot = (
                args.output_dir / "async_checkpoints" / f"policy_update_{state.completed_updates:04d}_jax.pkl"
            )

        row = {
            "event": "inner_update",
            "env_steps": (state.seed_counter - training_config["ppo_seed_start"]) * 2 * args.horizon,
            "rollout_env_steps": rollout.transitions,
            "outer_iteration": state.outer_iteration,
            "inner_iteration": state.inner_iteration,
            "completed_updates": state.completed_updates,
            "behavior_sha256": behavior_hash,
            "policy_sha256": policy_hash(state.params),
            "reference_sha256": policy_hash(state.reference_params),
            "reference_refresh_pending": state.reference_refresh_pending,
            "policy_snapshot": None if policy_snapshot is None else str(policy_snapshot),
            "iteration_seconds": time.monotonic() - iteration_started,
            "purchase_temperature": rollout_temperature,
            "purchase_temperature_steps": args.purchase_temperature_steps,
            "purchase_temperature_schedule": args.purchase_temperature_schedule,
            "update_seconds": update_seconds,
            "diagnostics_seconds": diagnostics_seconds,
            "rollout": rollout_metrics(rollout, post_update_value, post_update_indices),
            "update": update_metrics,
            "post_update_policy": post_update_policy,
            "entropy_control": entropy_control_metrics,
        }
        last_update_metrics = row
        save_evaluation_checkpoint(
            args.output_dir,
            state,
            snapshot_interval=args.snapshot_interval,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metadata={"last_update_metrics": row},
        )
        append_jsonl(args.output_dir / "metrics.jsonl", row)
        print(json.dumps(row, sort_keys=True), flush=True)

        state = apply_last_best_promotion(
            state,
            control_dir=args.last_best_control_dir,
            checkpoint_path=checkpoint_path,
            model_config=model_config.to_dict(),
            training_config=training_config,
            source_checkpoint_sha256=source_checkpoint_sha256,
            metrics_path=args.output_dir / "metrics.jsonl",
        )

        if state.reference_refresh_pending:
            boundary_event = "reference_retained" if args.freeze_reference else "reference_refresh"
            state = retain_reference(state) if args.freeze_reference else refresh_reference(state)
            save_checkpoint(
                checkpoint_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
            )
            boundary_path = args.output_dir / f"outer_{state.outer_iteration:04d}_jax.pkl"
            save_checkpoint(
                boundary_path,
                state,
                model_config=model_config.to_dict(),
                training_config=training_config,
                source_checkpoint_sha256=source_checkpoint_sha256,
            )
            boundary = {
                "event": boundary_event,
                "outer_iteration": state.outer_iteration,
                "policy_sha256": policy_hash(state.params),
                "reference_sha256": policy_hash(state.reference_params),
            }
            append_jsonl(args.output_dir / "metrics.jsonl", boundary)
            print(json.dumps(boundary, sort_keys=True), flush=True)

    save_evaluation_checkpoint(
        args.output_dir,
        state,
        snapshot_interval=args.snapshot_interval,
        model_config=model_config.to_dict(),
        training_config=training_config,
        source_checkpoint_sha256=source_checkpoint_sha256,
        metadata={} if last_update_metrics is None else {"last_update_metrics": last_update_metrics},
        force=True,
    )
    normal_completion = state.outer_iteration >= args.outer_iterations
    print(
        json.dumps(
            {
                "event": "stop",
                "normal_completion": normal_completion,
                "outer_iteration": state.outer_iteration,
                "inner_iteration": state.inner_iteration,
                "completed_updates": state.completed_updates,
            },
            sort_keys=True,
        ),
        flush=True,
    )


if __name__ == "__main__":
    main()
