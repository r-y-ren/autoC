"""Factored-action NashPG/PPO mathematics."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import optax
from jax.sharding import Mesh, NamedSharding, PartitionSpec

from kaggriculture.training.batch_prefetch import PreparedUpdateBatch
from kaggriculture.model.policy import JaxModelConfig, Params, cast_dense_params, policy_forward
from kaggriculture.training.sharding import flatten_pmap_batch, put_replicated, shard_batch, unreplicate
from kaggriculture.training.land_objective import land4_objective_terms
from kaggriculture.training.phase_entropy import entropy_weights, phase_sums
from kaggriculture.training.purchase_entropy import purchase_entropy_terms, tomato_floor_terms
from kaggriculture.training.purchase_policy import behavior_outputs, opening_purchase_sums
from kaggriculture.training.tomato_shop_objective import tomato_shop_bonus_terms

Array = jax.Array
MODEL_STATE_NAMES = frozenset(
    (
        "features",
        "memory_features",
        "coordinates",
        "spatial_mask",
        "rope_groups",
        "token_mask",
        "unit_indices",
        "market_indices",
        "legal_mask_stems",
    )
)


@dataclass(frozen=True)
class PPOConfig:
    clip: float = 0.2
    kl_coefficient: float = 0.005
    teacher_divergence: str = "kl"
    entropy_coefficient: float = 0.0
    opening_entropy_steps: int = 48
    opening_entropy_multiplier: float = 1.0
    purchase_entropy_coefficient: float = 0.0
    purchase_entropy_steps: int = 48
    purchase_entropy_metrics: bool = False
    tomato_floor_coefficient: float = 0.0
    tomato_floor_target: float = 0.0
    tomato_shop_bonus_coefficient: float = 0.0
    land4_probability_bonus_coefficient: float = 0.0
    land4_day_entropy_coefficient: float = 0.0
    value_coefficient: float = 2.0
    value_huber_delta: float = 1.0
    gradient_norm: float = 5.0
    learning_rate: float = 1e-4
    adam_epsilon: float = 1e-5
    lr_decay_steps: int = 150_000
    lr_min_ratio: float = 0.25
    lr_warmup_steps: int = 0
    # Optional live learning-rate change: blend linearly from the schedule built on `lr_ramp_from`
    # to the one built on `learning_rate` over `lr_ramp_steps` optimizer steps starting at
    # `lr_ramp_start_step`, so a warm Adam state is not hit by a step-size jump.
    lr_ramp_from: float | None = None
    lr_ramp_start_step: int = 0
    lr_ramp_steps: int = 0
    reference_kl_samples: int = 30
    normalize_advantages: bool = True

    def __post_init__(self) -> None:
        if self.lr_warmup_steps < 0:
            raise ValueError("LR warmup steps cannot be negative")
        if self.lr_ramp_steps < 0 or self.lr_ramp_start_step < 0:
            raise ValueError("LR ramp steps cannot be negative")
        if self.lr_ramp_steps > 0 and (self.lr_ramp_from is None or self.lr_ramp_from <= 0):
            raise ValueError("LR ramp requires the previous positive base learning rate")
        if self.teacher_divergence not in {"kl", "js"}:
            raise ValueError("teacher divergence must be 'kl' or 'js'")
        if not np.isfinite(self.tomato_floor_coefficient) or self.tomato_floor_coefficient < 0:
            raise ValueError("invalid tomato floor coefficient")
        if not np.isfinite(self.tomato_floor_target) or not 0 <= self.tomato_floor_target <= 1:
            raise ValueError("invalid tomato floor target")
        if self.tomato_floor_coefficient and self.tomato_floor_target == 0:
            raise ValueError("enabled tomato floor requires a measured positive target")
        if not np.isfinite(self.tomato_shop_bonus_coefficient) or self.tomato_shop_bonus_coefficient < 0:
            raise ValueError("invalid tomato shop bonus coefficient")
        land_coefficients = (self.land4_probability_bonus_coefficient, self.land4_day_entropy_coefficient)
        if any(not np.isfinite(value) or value < 0 for value in land_coefficients):
            raise ValueError("invalid fourth-land objective coefficient")


def normalize_masked_advantages(
    advantages: Array,
    sample_mask: Array,
    epsilon: float = 1e-8,
) -> Array:
    """Standardize valid advantages within one PPO minibatch."""
    weights = sample_mask.astype(advantages.dtype)
    denominator = jnp.maximum(jnp.sum(weights), 1.0)
    mean = jnp.sum(advantages * weights) / denominator
    variance = jnp.sum(jnp.square(advantages - mean) * weights) / denominator
    return (advantages - mean) / (jnp.sqrt(jnp.maximum(variance, 0.0)) + epsilon)


def selected_log_prob(logits: Array, actions: Array) -> Array:
    log_probs = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    return jnp.take_along_axis(log_probs, actions[..., None], axis=-1)[..., 0]


def joint_log_prob(
    outputs: dict[str, Array],
    unit_actions: Array,
    market_actions: Array,
    unit_mask: Array,
    unit_policy_mask: Array | None = None,
    market_policy_mask: Array | None = None,
) -> Array:
    unit = selected_log_prob(outputs["unit_action"], unit_actions)
    market = selected_log_prob(outputs["market_action"], market_actions)
    if unit_policy_mask is not None:
        unit = unit * unit_policy_mask
    if market_policy_mask is not None:
        market = market * market_policy_mask
    return jnp.sum(unit * unit_mask, axis=-1) + jnp.sum(market, axis=-1)


@jax.custom_vjp
def categorical_forward_kl(logits: Array, reference_logits: Array) -> Array:
    log_policy = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    log_reference = jax.nn.log_softmax(reference_logits.astype(jnp.float32), axis=-1)
    return jnp.sum(jnp.exp(log_policy) * (log_policy - log_reference), axis=-1)


def _categorical_forward_kl_forward(logits: Array, reference_logits: Array):
    log_policy = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    log_reference = jax.nn.log_softmax(reference_logits.astype(jnp.float32), axis=-1)
    probability = jnp.exp(log_policy)
    log_ratio = log_policy - log_reference
    divergence = jnp.sum(probability * log_ratio, axis=-1)
    dtype_token = jnp.zeros((), dtype=logits.dtype)
    reference_dtype_token = jnp.zeros((), dtype=reference_logits.dtype)
    return divergence, (probability, log_ratio, divergence, dtype_token, reference_dtype_token)


def _categorical_forward_kl_backward(residuals, cotangent):
    probability, log_ratio, divergence, dtype_token, reference_dtype_token = residuals
    policy_gradient = probability * (log_ratio - divergence[..., None])
    policy_gradient *= cotangent[..., None]
    return policy_gradient.astype(dtype_token.dtype), jnp.zeros_like(policy_gradient, dtype=reference_dtype_token.dtype)


categorical_forward_kl.defvjp(_categorical_forward_kl_forward, _categorical_forward_kl_backward)


def joint_forward_kl(
    outputs: dict[str, Array], reference_outputs: dict[str, Array], unit_mask: Array
) -> tuple[Array, Array, Array]:
    unit = jnp.sum(
        categorical_forward_kl(outputs["unit_action"], reference_outputs["unit_action"]) * unit_mask,
        axis=-1,
    )
    market = jnp.sum(
        categorical_forward_kl(outputs["market_action"], reference_outputs["market_action"]),
        axis=-1,
    )
    return unit + market, unit, market


def categorical_teacher_kl(logits: Array, teacher_logits: Array) -> Array:
    """Compute KL(teacher || policy), with the teacher treated as fixed."""
    log_policy = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    log_teacher = jax.lax.stop_gradient(jax.nn.log_softmax(teacher_logits.astype(jnp.float32), axis=-1))
    return jnp.sum(jnp.exp(log_teacher) * (log_teacher - log_policy), axis=-1)


def categorical_teacher_js(logits: Array, teacher_logits: Array) -> Array:
    """Compute JS(policy, teacher), with the teacher treated as fixed."""
    log_policy = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    log_teacher = jax.lax.stop_gradient(jax.nn.log_softmax(teacher_logits.astype(jnp.float32), axis=-1))
    log_mixture = jnp.logaddexp(log_policy, log_teacher) - jnp.log(2.0)
    policy_term = jnp.sum(jnp.exp(log_policy) * (log_policy - log_mixture), axis=-1)
    teacher_term = jnp.sum(jnp.exp(log_teacher) * (log_teacher - log_mixture), axis=-1)
    return 0.5 * (policy_term + teacher_term)


def categorical_teacher_divergence(logits: Array, teacher_logits: Array, mode: str) -> Array:
    if mode == "kl":
        return categorical_teacher_kl(logits, teacher_logits)
    if mode == "js":
        return categorical_teacher_js(logits, teacher_logits)
    raise ValueError(f"unsupported teacher divergence: {mode}")


def joint_teacher_divergence(
    outputs: dict[str, Array],
    teacher_outputs: dict[str, Array],
    unit_mask: Array,
    mode: str,
) -> tuple[Array, Array, Array]:
    unit = jnp.sum(
        categorical_teacher_divergence(outputs["unit_action"], teacher_outputs["unit_action"], mode) * unit_mask,
        axis=-1,
    )
    market = jnp.sum(
        categorical_teacher_divergence(outputs["market_action"], teacher_outputs["market_action"], mode),
        axis=-1,
    )
    return unit + market, unit, market


def joint_teacher_kl(
    outputs: dict[str, Array],
    teacher_outputs: dict[str, Array],
    unit_mask: Array,
) -> tuple[Array, Array, Array]:
    """Backward-compatible KL-only entry point."""
    return joint_teacher_divergence(outputs, teacher_outputs, unit_mask, "kl")


def categorical_entropy(logits: Array) -> Array:
    log_probs = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    return -jnp.sum(jnp.exp(log_probs) * log_probs, axis=-1)


def joint_entropy_components(outputs: dict[str, Array], unit_mask: Array) -> tuple[Array, Array]:
    unit = jnp.sum(categorical_entropy(outputs["unit_action"]) * unit_mask, axis=-1)
    market = jnp.sum(categorical_entropy(outputs["market_action"]), axis=-1)
    return unit, market


def joint_entropy(outputs: dict[str, Array], unit_mask: Array) -> Array:
    unit, market = joint_entropy_components(outputs, unit_mask)
    return unit + market


def normalized_joint_entropy(
    outputs: dict[str, Array],
    unit_mask: Array,
    *,
    legal: bool = True,
) -> tuple[Array, Array, Array]:
    """Normalize factorized entropy by the corresponding uniform-policy maximum."""
    unit, market = joint_entropy_components(outputs, unit_mask)
    active_units = jnp.sum(unit_mask, axis=-1)
    unit_maximum = active_units * jnp.log(outputs["unit_action"].shape[-1])
    market_maximum = outputs["market_action"].shape[1] * jnp.log(outputs["market_action"].shape[-1])
    if legal and "unit_legal_count" in outputs:
        unit_maximum = jnp.sum(jnp.log(jnp.maximum(outputs["unit_legal_count"], 1)) * unit_mask, axis=-1)
        market_maximum = outputs["market_action"].shape[1] * jnp.log(
            jnp.maximum(outputs["market_legal_count"][:, 0], 1)
        )
    unit_normalized = unit / jnp.maximum(unit_maximum, 1e-8)
    market_normalized = market / jnp.maximum(market_maximum, 1e-8)
    joint_normalized = (unit + market) / jnp.maximum(unit_maximum + market_maximum, 1e-8)
    return joint_normalized, unit_normalized, market_normalized


def paired_zero_sum_values(values: Array) -> Array:
    """Couple adjacent seats so every game has exactly antisymmetric values."""
    if values.shape[0] % 2:
        raise ValueError("zero-sum values require adjacent seat pairs")
    paired = values.reshape((-1, 2))
    return (2.0 * jax.nn.softmax(paired.astype(jnp.float32), axis=-1) - 1.0).reshape(values.shape)


def base_learning_rate_schedule(learning_rate: float, config: PPOConfig) -> optax.Schedule:
    decay = optax.linear_schedule(
        init_value=learning_rate,
        end_value=learning_rate * config.lr_min_ratio,
        transition_steps=config.lr_decay_steps,
    )
    if config.lr_warmup_steps == 0:
        return decay
    warmup = optax.linear_schedule(0.0, learning_rate, config.lr_warmup_steps)
    return optax.join_schedules([warmup, decay], [config.lr_warmup_steps])


def learning_rate_schedule(config: PPOConfig) -> optax.Schedule:
    target = base_learning_rate_schedule(config.learning_rate, config)
    if config.lr_ramp_from is None or config.lr_ramp_steps == 0:
        return target
    previous = base_learning_rate_schedule(config.lr_ramp_from, config)

    def ramped(step: Any) -> Any:
        progress = jnp.clip((step - config.lr_ramp_start_step) / config.lr_ramp_steps, 0.0, 1.0)
        return previous(step) + (target(step) - previous(step)) * progress

    return ramped


def optimizer_step_number(state: Any) -> int:
    if isinstance(state, optax.MultiStepsState):
        state = state.inner_opt_state
    leaves = jax.tree.leaves(state, is_leaf=lambda value: isinstance(value, optax.ScaleByAdamState))
    counts = [int(value.count) for value in leaves if isinstance(value, optax.ScaleByAdamState)]
    if len(counts) != 1:
        raise ValueError("expected exactly one Adam step counter")
    return counts[0]


def make_optimizer(
    config: PPOConfig,
    *,
    gradient_accumulation_steps: int = 1,
    data_parallel_axis_name: str | None = None,
) -> optax.GradientTransformation:
    if gradient_accumulation_steps <= 0:
        raise ValueError("gradient accumulation steps must be positive")

    def average_gradients(updates, state, params=None):
        del params
        if data_parallel_axis_name is not None:
            updates = jax.lax.pmean(updates, data_parallel_axis_name)
        return updates, state

    # Keep the EmptyState slot even at one device: resizing must preserve Adam's tree.
    transforms = [
        optax.GradientTransformation(
            lambda _: optax.EmptyState(),
            average_gradients,
        )
    ]
    transforms.append(
        optax.apply_if_finite(
            optax.chain(
                optax.clip_by_global_norm(config.gradient_norm),
                optax.adam(
                    learning_rate_schedule(config),
                    eps=config.adam_epsilon,
                ),
            ),
            max_consecutive_errors=np.iinfo(np.int32).max,
        )
    )
    # Reduce before deciding to skip, so one rank's overflow cannot split a collective.
    optimizer = optax.chain(*transforms)
    if gradient_accumulation_steps == 1:
        return optimizer
    accumulated = optax.MultiSteps(
        optimizer,
        every_k_schedule=gradient_accumulation_steps,
        use_grad_mean=True,
        accumulator_dtype=jnp.float32,
    )

    def update(gradients, state, params=None):
        updates, state = accumulated.update(gradients, state, params)
        state = state._replace(
            acc_grads=jax.tree.map(
                lambda value: jnp.where(state.mini_step == 0, jnp.zeros_like(value), value), state.acc_grads
            )
        )
        return updates, state

    return optax.GradientTransformation(accumulated.init, update)


def make_full_value_update_step(
    model_config: JaxModelConfig,
    ppo_config: PPOConfig,
    compute_dtype: jnp.dtype,
    optimizer: optax.GradientTransformation,
):
    """Compile a Value-only loss whose gradient reaches the complete shared model."""

    def loss_and_metrics(inference_params: Params, batch: dict[str, Array]):
        outputs = policy_forward(inference_params, batch, model_config, dtype=compute_dtype, training=False)
        sample_mask = batch["sample_mask"].astype(jnp.float32)
        denominator = jnp.maximum(jnp.sum(sample_mask), 1.0)
        value = paired_zero_sum_values(outputs["value"])
        value_loss = (
            jnp.sum(optax.huber_loss(value, batch["return"], delta=ppo_config.value_huber_delta) * sample_mask)
            / denominator
        )
        loss = ppo_config.value_coefficient * value_loss
        return loss, {
            "loss": loss,
            "value_loss": value_loss,
            "value_mean": jnp.sum(value * sample_mask) / denominator,
            "learning_rate": learning_rate_schedule(ppo_config)(batch["optimizer_step"]),
            "sample_count": jnp.sum(sample_mask),
        }

    value_and_gradient = jax.value_and_grad(loss_and_metrics, has_aux=True)

    @jax.jit
    def update_step_precast(
        params: Params,
        inference_params: Params,
        optimizer_state: Any,
        batch: dict[str, Array],
    ):
        (_, metrics), gradients = value_and_gradient(inference_params, batch)
        gradients = jax.tree.map(lambda gradient, parameter: gradient.astype(parameter.dtype), gradients, params)
        metrics = {**metrics, "gradient_norm": optax.tree.norm(gradients)}
        updates, optimizer_state = optimizer.update(gradients, optimizer_state, params)
        params = optax.apply_updates(params, updates)
        next_inference_params = cast_dense_params(params, compute_dtype)
        return params, next_inference_params, optimizer_state, metrics

    cached_master_params: Params | None = None
    cached_inference_params: Params | None = None

    def update_step(
        params: Params,
        optimizer_state: Any,
        batch: dict[str, Array],
    ):
        nonlocal cached_master_params, cached_inference_params
        if cached_master_params is not params:
            cached_inference_params = cast_dense_params(params, compute_dtype)
            cached_master_params = params
        assert cached_inference_params is not None
        params, next_inference_params, optimizer_state, metrics = update_step_precast(
            params,
            cached_inference_params,
            optimizer_state,
            batch,
        )
        cached_master_params = params
        cached_inference_params = next_inference_params
        return params, optimizer_state, metrics

    return update_step


def make_value_head_update_step(
    model_config: JaxModelConfig,
    ppo_config: PPOConfig,
    compute_dtype: jnp.dtype,
    optimizer: optax.GradientTransformation,
):
    """Compile a Value-only loss whose gradient reaches only the critic MLP."""

    def loss_and_metrics(value_params: Params, inference_actor_params: Params, batch: dict[str, Array]):
        inference_params = {
            **inference_actor_params,
            "value": cast_dense_params(value_params, compute_dtype),
        }
        outputs = policy_forward(inference_params, batch, model_config, dtype=compute_dtype, training=False)
        sample_mask = batch["sample_mask"].astype(jnp.float32)
        denominator = jnp.maximum(jnp.sum(sample_mask), 1.0)
        value = paired_zero_sum_values(outputs["value"])
        value_loss = (
            jnp.sum(optax.huber_loss(value, batch["return"], delta=ppo_config.value_huber_delta) * sample_mask)
            / denominator
        )
        loss = ppo_config.value_coefficient * value_loss
        return loss, {
            "loss": loss,
            "value_loss": value_loss,
            "value_mean": jnp.sum(value * sample_mask) / denominator,
            "learning_rate": learning_rate_schedule(ppo_config)(batch["optimizer_step"]),
            "sample_count": jnp.sum(sample_mask),
        }

    value_and_gradient = jax.value_and_grad(loss_and_metrics, has_aux=True)

    @jax.jit
    def update_step_precast(
        value_params: Params,
        inference_actor_params: Params,
        optimizer_state: Any,
        batch: dict[str, Array],
    ):
        (_, metrics), gradients = value_and_gradient(value_params, inference_actor_params, batch)
        gradients = jax.tree.map(lambda gradient, parameter: gradient.astype(parameter.dtype), gradients, value_params)
        metrics = {**metrics, "gradient_norm": optax.tree.norm(gradients)}
        updates, optimizer_state = optimizer.update(gradients, optimizer_state, value_params)
        value_params = optax.apply_updates(value_params, updates)
        return value_params, optimizer_state, metrics

    cached_actor_source: Params | None = None
    cached_inference_actor: Params | None = None

    def update_step(
        value_params: Params,
        actor_params: Params,
        optimizer_state: Any,
        batch: dict[str, Array],
    ):
        nonlocal cached_actor_source, cached_inference_actor
        if cached_actor_source is not actor_params:
            cached_inference_actor = cast_dense_params(actor_params, compute_dtype)
            cached_actor_source = actor_params
        assert cached_inference_actor is not None
        return update_step_precast(
            value_params,
            cached_inference_actor,
            optimizer_state,
            batch,
        )

    return update_step


def make_log_prob_evaluator(
    model_config: JaxModelConfig,
    compute_dtype: jnp.dtype,
    devices: Sequence[jax.Device] | None = None,
    *,
    collective_devices: Sequence[jax.Device] | None = None,
    partition_kernel: Callable | None = None,
    selected_partition_kernel: Callable | None = None,
    prune_final_queries: bool = False,
    remat_ffn_activation: bool = False,
):
    def evaluate_precast(inference_params: Params, batch: dict[str, Array]) -> Array:
        outputs = policy_forward(
            inference_params,
            batch,
            model_config,
            dtype=compute_dtype,
            training=False,
            partition_kernel=partition_kernel,
            selected_partition_kernel=selected_partition_kernel,
            prune_final_queries=prune_final_queries,
            remat_ffn_activation=remat_ffn_activation,
        )
        outputs = behavior_outputs(outputs, batch)
        return joint_log_prob(
            outputs,
            batch["unit_action"],
            batch["market_action"],
            batch["unit_mask"],
            batch.get("unit_policy_mask"),
            batch.get("market_policy_mask"),
        )

    selected_devices = tuple(jax.local_devices()[:1] if devices is None else devices)
    if len(selected_devices) == 1 and collective_devices is None:
        compiled_evaluator = jax.jit(evaluate_precast)

        def evaluate(params: Params, batch: dict[str, Array]) -> Array:
            return compiled_evaluator(cast_dense_params(params, compute_dtype), batch)

        return evaluate

    compiled_evaluator = jax.pmap(
        evaluate_precast, devices=selected_devices if collective_devices is None else tuple(collective_devices)
    )
    cached_params_source: Params | None = None
    cached_params: Params | None = None

    def evaluate(params: Params, batch: dict[str, Array]) -> Array:
        nonlocal cached_params_source, cached_params
        if cached_params_source is not params:
            cached_params = put_replicated(cast_dense_params(params, compute_dtype), selected_devices)
            cached_params_source = params
        assert cached_params is not None
        outputs = compiled_evaluator(cached_params, shard_batch(batch, selected_devices))
        return flatten_pmap_batch(outputs)

    return evaluate


def make_update_step(
    model_config: JaxModelConfig,
    ppo_config: PPOConfig,
    compute_dtype: jnp.dtype,
    optimizer: optax.GradientTransformation,
    devices: Sequence[jax.Device] | None = None,
    *,
    static_accumulation_steps: int | None = None,
    prune_final_tokens: bool = False,
    prune_final_queries: bool = False,
    compact_norm_backward: bool = False,
    partition_kernel: Callable | None = None,
    remat_ffn_activation: bool = False,
    selected_partition_kernel: Callable | None = None,
    collective_devices: Sequence[jax.Device] | None = None,
    allow_uneven_pairs: bool = False,
    memory_budget_fraction: float | None = None,
    global_update_arrays: bool = False,
    heterogeneous_local_backward: bool = False,
    external_gradient_sum: Callable | None = None,
    external_processes: int = 1,
):
    """Compile one deterministic, dropout-free PPO minibatch update."""
    selected_devices = tuple(jax.local_devices()[:1] if devices is None else devices)
    is_data_parallel = len(selected_devices) > 1 or collective_devices is not None
    if global_update_arrays and not is_data_parallel:
        raise ValueError("global update arrays require multiple devices")
    schedule = None
    accumulate = None
    if static_accumulation_steps is not None:
        from kaggriculture.model.kernels.deferred_optimizer import AccumulationSchedule, accumulate_only

        schedule = AccumulationSchedule(static_accumulation_steps)
        accumulate = accumulate_only
    reference_count = (
        (ppo_config.reference_kl_samples + len(selected_devices) - 1) // len(selected_devices)
        if is_data_parallel
        else ppo_config.reference_kl_samples
    )

    def loss_and_metrics(inference_params: Params, inference_reference_params: Params, batch: dict[str, Array]):
        outputs = policy_forward(
            inference_params,
            batch,
            model_config,
            dtype=compute_dtype,
            training=False,
            prune_final_tokens=prune_final_tokens,
            prune_final_queries=prune_final_queries,
            compact_norm_backward=compact_norm_backward,
            partition_kernel=partition_kernel,
            remat_ffn_activation=remat_ffn_activation,
            selected_partition_kernel=selected_partition_kernel,
        )
        raw_market_logits = outputs["market_action"]
        outputs = behavior_outputs(outputs, batch)
        local_reference_count = min(reference_count, batch["unit_mask"].shape[0])
        reference_batch = {
            name: values[:local_reference_count] for name, values in batch.items() if name in MODEL_STATE_NAMES
        }
        reference_outputs = policy_forward(
            inference_reference_params,
            reference_batch,
            model_config,
            dtype=compute_dtype,
            training=False,
            prune_final_tokens=prune_final_tokens,
            prune_final_queries=prune_final_queries,
            compact_norm_backward=compact_norm_backward,
            partition_kernel=partition_kernel,
            remat_ffn_activation=remat_ffn_activation,
            selected_partition_kernel=selected_partition_kernel,
        )
        log_prob = joint_log_prob(
            outputs,
            batch["unit_action"],
            batch["market_action"],
            batch["unit_mask"],
            batch.get("unit_policy_mask"),
            batch.get("market_policy_mask"),
        )
        sample_mask = batch["sample_mask"].astype(jnp.float32)
        denominator = jnp.maximum(jnp.sum(sample_mask), 1.0)

        def masked_mean(values: Array) -> Array:
            if "sample_mean_scale" in batch:
                return jnp.sum(values * sample_mask) * batch["sample_mean_scale"]
            return jnp.sum(values * sample_mask) / denominator

        policy_advantage = batch["advantage"]
        if ppo_config.normalize_advantages:
            normalization_mean = batch.get("advantage_normalization_mean")
            normalization_standard_deviation = batch.get("advantage_normalization_standard_deviation")
            policy_advantage = (
                normalize_masked_advantages(policy_advantage, sample_mask)
                if normalization_mean is None or normalization_standard_deviation is None
                else (policy_advantage - normalization_mean) / (normalization_standard_deviation + 1e-8)
            )
        ratio = jnp.exp(log_prob - batch["old_log_prob"])
        clipped_ratio = jnp.clip(ratio, 1.0 - ppo_config.clip, 1.0 + ppo_config.clip)
        surrogate = jnp.minimum(ratio * policy_advantage, clipped_ratio * policy_advantage)
        policy_valid = batch.get("policy_valid")
        policy_loss = -masked_mean(surrogate if policy_valid is None else surrogate * policy_valid.astype(jnp.float32))
        value = paired_zero_sum_values(outputs["value"])
        value_loss = masked_mean(optax.huber_loss(value, batch["return"], delta=ppo_config.value_huber_delta))
        reference_sample_mask = batch.get(
            "reference_sample_mask",
            sample_mask[:local_reference_count],
        ).astype(jnp.float32)
        reference_mean_scale = batch.get("reference_mean_scale")

        def reference_mean(values: Array) -> Array:
            numerator = jnp.sum(values * reference_sample_mask)
            if reference_mean_scale is not None:
                return numerator * reference_mean_scale
            return numerator / jnp.maximum(jnp.sum(reference_sample_mask), 1.0)

        total_divergence, unit_divergence, market_divergence = joint_teacher_divergence(
            {name: values[:local_reference_count] for name, values in outputs.items()},
            reference_outputs,
            batch["unit_mask"][:local_reference_count],
            ppo_config.teacher_divergence,
        )
        teacher_divergence = reference_mean(total_divergence)
        active_unit_factors = jnp.sum(batch["unit_mask"], axis=-1)
        reference_active_units = active_unit_factors[:local_reference_count]
        unit_factor_numerator = jnp.sum(unit_divergence * reference_sample_mask)
        unit_factor_denominator = jnp.sum(reference_active_units * reference_sample_mask)
        unit_teacher_divergence_per_factor = unit_factor_numerator / jnp.maximum(unit_factor_denominator, 1.0)
        reference_kl_scale = batch["reference_kl_scale"].astype(jnp.float32)
        unit_entropy, market_entropy = joint_entropy_components(outputs, batch["unit_mask"])
        normalized_entropy, unit_normalized_entropy, market_normalized_entropy = normalized_joint_entropy(
            outputs,
            batch["unit_mask"],
        )
        entropy = masked_mean(unit_entropy + market_entropy)
        full_normalized, full_unit_normalized, full_market_normalized = normalized_joint_entropy(
            outputs, batch["unit_mask"], legal=False
        )
        value_loss_weighted = ppo_config.value_coefficient * value_loss
        teacher_divergence_loss = ppo_config.kl_coefficient * reference_kl_scale * teacher_divergence
        entropy_coefficient = batch.get(
            "entropy_coefficient",
            jnp.asarray(ppo_config.entropy_coefficient, dtype=jnp.float32),
        ).astype(jnp.float32)
        unit_entropy_coefficient = batch.get("unit_entropy_coefficient", entropy_coefficient)
        market_entropy_coefficient = batch.get("market_entropy_coefficient", entropy_coefficient)
        if ppo_config.opening_entropy_multiplier != 1.0 and "episode_step" not in batch:
            raise ValueError("opening entropy weighting requires exact episode steps")
        entropy_scale = (
            entropy_weights(
                batch["episode_step"], ppo_config.opening_entropy_steps, ppo_config.opening_entropy_multiplier
            )
            if "episode_step" in batch
            else jnp.ones_like(unit_entropy)
        )
        unit_entropy_loss = -unit_entropy_coefficient * masked_mean(unit_entropy * entropy_scale)
        market_entropy_loss = -market_entropy_coefficient * masked_mean(market_entropy * entropy_scale)
        entropy_loss = unit_entropy_loss + market_entropy_loss
        purchase_metrics = {}
        purchase_loss = jnp.float32(0.0)
        if (
            ppo_config.purchase_entropy_coefficient
            or ppo_config.purchase_entropy_metrics
            or "purchase_entropy_coefficient" in batch
        ):
            if "episode_step" not in batch:
                raise ValueError("purchase entropy requires exact episode steps")
            per_state_purchase_loss, purchase_metrics = purchase_entropy_terms(
                outputs["market_action"],
                batch["episode_step"],
                batch.get("purchase_entropy_coefficient", ppo_config.purchase_entropy_coefficient),
                ppo_config.purchase_entropy_steps,
            )
            purchase_loss = masked_mean(per_state_purchase_loss)
        tomato_loss = jnp.float32(0.0)
        if ppo_config.tomato_floor_target > 0 and (
            ppo_config.tomato_floor_coefficient or "tomato_floor_coefficient" in batch
        ):
            tomato_coefficient = batch.get("tomato_floor_coefficient", ppo_config.tomato_floor_coefficient)

            def tomato_enabled(_: None):
                return tomato_floor_terms(outputs["market_action"], tomato_coefficient, ppo_config.tomato_floor_target)

            def tomato_disabled(_: None):
                zeros = jnp.zeros_like(batch["episode_step"], dtype=jnp.float32)
                return zeros, {
                    "tomato_floor_loss": zeros,
                    "tomato_floor_active_fraction": zeros,
                    "tomato_conditional_probability_slot_mean": zeros,
                    "tomato_floor_target": zeros,
                    "tomato_floor_coefficient": zeros,
                }

            per_state_tomato_loss, tomato_metrics = jax.lax.cond(
                tomato_coefficient != 0, tomato_enabled, tomato_disabled, None
            )
            tomato_loss = masked_mean(per_state_tomato_loss)
            purchase_metrics.update(tomato_metrics)
        tomato_shop_loss = jnp.float32(0.0)
        tomato_shop_metrics = {}
        if ppo_config.tomato_shop_bonus_coefficient or "tomato_shop_bonus_coefficient" in batch:
            tomato_shop_coefficient = batch.get(
                "tomato_shop_bonus_coefficient", ppo_config.tomato_shop_bonus_coefficient
            )

            def tomato_shop_enabled(_: None):
                return tomato_shop_bonus_terms(
                    outputs["unit_action"],
                    outputs["market_action"],
                    batch["features"],
                    batch["unit_mask"],
                    tomato_shop_coefficient,
                    absolute_sell=model_config.absolute_sell,
                )

            def tomato_shop_disabled(_: None):
                zeros = jnp.zeros_like(batch["episode_step"], dtype=jnp.float32)
                return zeros, {
                    "tomato_shop_bonus_loss": zeros,
                    "tomato_shop_eligible": zeros,
                    "tomato_shop_sell_inventory_eligible": zeros,
                    "tomato_shop_buy_probability": zeros,
                    "tomato_shop_sell_probability": zeros,
                    "tomato_shop_plant_probability": zeros,
                    "tomato_shop_bonus_coefficient": zeros,
                }

            per_state_tomato_shop_loss, tomato_shop_metrics = jax.lax.cond(
                tomato_shop_coefficient != 0, tomato_shop_enabled, tomato_shop_disabled, None
            )
            tomato_shop_loss = masked_mean(per_state_tomato_shop_loss)
        land_loss = jnp.float32(0.0)
        land_metrics = {}
        if "land4_probability_bonus_coefficient" in batch or "land4_day_entropy_coefficient" in batch:
            required = ("episode_step", "land_owned_count", "land_affordable")
            if any(name not in batch for name in required):
                raise ValueError("fourth-land objective requires rollout land state")
            land_loss, land_metrics = land4_objective_terms(
                outputs["market_action"],
                batch["episode_step"],
                batch["land_owned_count"],
                batch["land_affordable"],
                sample_mask,
                batch.get("land4_probability_bonus_coefficient", ppo_config.land4_probability_bonus_coefficient),
                batch.get("land4_day_entropy_coefficient", ppo_config.land4_day_entropy_coefficient),
                absolute=model_config.absolute_sell,
            )
        regularization_loss = (
            teacher_divergence_loss + entropy_loss + purchase_loss + tomato_loss + tomato_shop_loss + land_loss
        )
        log_ratio = log_prob - batch["old_log_prob"]
        loss = policy_loss + value_loss_weighted + regularization_loss
        metrics = {
            "loss": loss,
            "policy_loss": policy_loss,
            "policy_loss_weighted": policy_loss,
            "policy_advantage_mean": masked_mean(policy_advantage),
            "policy_advantage_standard_deviation": jnp.sqrt(
                masked_mean(jnp.square(policy_advantage - masked_mean(policy_advantage)))
            ),
            "value_loss": value_loss,
            "value_loss_weighted": value_loss_weighted,
            "teacher_divergence": teacher_divergence,
            "teacher_divergence_loss": teacher_divergence_loss,
            "unit_teacher_divergence": reference_mean(unit_divergence),
            "unit_teacher_divergence_per_factor": unit_teacher_divergence_per_factor,
            "market_teacher_divergence": reference_mean(market_divergence),
            "market_teacher_divergence_per_slot": reference_mean(market_divergence) / outputs["market_action"].shape[1],
            # Retain legacy metric keys so existing monitors can compare KL-mode runs byte-for-byte.
            "teacher_kl": teacher_divergence,
            "teacher_kl_loss": teacher_divergence_loss,
            "teacher_kl_loss_scale": reference_kl_scale,
            "unit_teacher_kl": reference_mean(unit_divergence),
            "unit_teacher_kl_per_factor": unit_teacher_divergence_per_factor,
            "unit_teacher_kl_numerator": unit_factor_numerator,
            "unit_teacher_kl_denominator": unit_factor_denominator,
            "market_teacher_kl": reference_mean(market_divergence),
            "market_teacher_kl_per_slot": reference_mean(market_divergence) / outputs["market_action"].shape[1],
            "active_units_mean": masked_mean(active_unit_factors),
            "entropy": entropy,
            "entropy_loss": entropy_loss,
            "entropy_coefficient": entropy_coefficient,
            "unit_entropy_coefficient": unit_entropy_coefficient,
            "market_entropy_coefficient": market_entropy_coefficient,
            "unit_entropy_loss": unit_entropy_loss,
            "market_entropy_loss": market_entropy_loss,
            "regularization_loss": regularization_loss,
            "land4_objective_loss": land_loss,
            "tomato_shop_objective_loss": tomato_shop_loss,
            "unit_entropy": masked_mean(unit_entropy),
            "market_entropy": masked_mean(market_entropy),
            "normalized_entropy": masked_mean(normalized_entropy),
            "unit_normalized_entropy": masked_mean(unit_normalized_entropy),
            "market_normalized_entropy": masked_mean(market_normalized_entropy),
            "full_catalog_normalized_entropy": masked_mean(full_normalized),
            "unit_full_catalog_normalized_entropy": masked_mean(full_unit_normalized),
            "market_full_catalog_normalized_entropy": masked_mean(full_market_normalized),
            "approx_kl": masked_mean((ratio - 1.0) - log_ratio),
            "approx_old_kl": masked_mean(-log_ratio),
            "ratio_mean": masked_mean(ratio),
            "clip_fraction": masked_mean(jnp.abs(ratio - 1.0) > ppo_config.clip),
            "value_mean": masked_mean(value),
            "learning_rate": learning_rate_schedule(ppo_config)(batch["optimizer_step"]),
            "sample_count": jnp.sum(sample_mask),
            **{name: masked_mean(value) for name, value in purchase_metrics.items()},
            **{name: masked_mean(value) for name, value in tomato_shop_metrics.items()},
            **land_metrics,
        }
        if tomato_shop_metrics:
            eligible_fraction = metrics.pop("tomato_shop_eligible")
            metrics["tomato_shop_eligible_fraction"] = eligible_fraction
            eligible_denominator = jnp.maximum(eligible_fraction, 1e-8)
            for name in (
                "tomato_shop_sell_inventory_eligible",
                "tomato_shop_buy_probability",
                "tomato_shop_sell_probability",
                "tomato_shop_plant_probability",
            ):
                metrics[name] /= eligible_denominator
        if "episode_step" in batch:
            metrics.update(
                phase_sums(
                    batch["episode_step"],
                    sample_mask,
                    unit_entropy,
                    market_entropy,
                    unit_normalized_entropy,
                    market_normalized_entropy,
                    unit_entropy_coefficient,
                    market_entropy_coefficient,
                    entropy_scale,
                    purchase_metrics,
                )
            )
        gradient_loss_scale = batch.get("gradient_loss_scale", jnp.asarray(1.0, dtype=jnp.float32))
        if "purchase_temperature" in batch:
            metrics.update(opening_purchase_sums(raw_market_logits, outputs["market_action"], batch))
        if "unit_entropy_coefficient" in batch:
            del metrics["entropy_coefficient"]
        return loss * gradient_loss_scale, metrics

    value_and_gradient = jax.value_and_grad(loss_and_metrics, has_aux=True)

    if heterogeneous_local_backward:
        from kaggriculture.training.heterogeneous_update import GradientSum, make_heterogeneous_update

        if (
            len(selected_devices) != 1
            or static_accumulation_steps is None
            or (collective_devices is None and external_gradient_sum is None)
        ):
            raise ValueError("heterogeneous updates require one GPU/rank and explicit accumulation")
        return make_heterogeneous_update(
            value_and_gradient,
            make_optimizer(ppo_config),
            lambda params: cast_dense_params(params, compute_dtype),
            static_accumulation_steps,
            external_gradient_sum if external_gradient_sum is not None else GradientSum(collective_devices),
            external_processes if external_gradient_sum is not None else len(collective_devices),
        )

    def update_step_precast(
        params: Params,
        inference_params: Params,
        inference_reference_params: Params,
        optimizer_state: Any,
        batch: dict[str, Array],
        apply_optimizer: bool,
    ):
        (_, metrics), gradients = value_and_gradient(inference_params, inference_reference_params, batch)
        gradients = jax.tree.map(lambda gradient, parameter: gradient.astype(parameter.dtype), gradients, params)
        metrics = {**metrics, "gradient_norm": optax.tree.norm(gradients)}
        if not apply_optimizer:
            assert accumulate is not None
            return params, inference_params, accumulate(gradients, optimizer_state), metrics
        updates, optimizer_state = optimizer.update(gradients, optimizer_state, params)
        params = optax.apply_updates(params, updates)
        next_inference_params = cast_dense_params(params, compute_dtype)
        return params, next_inference_params, optimizer_state, metrics

    compiled_update_step = (
        jax.pmap(
            update_step_precast,
            axis_name="data",
            devices=selected_devices if collective_devices is None else tuple(collective_devices),
            static_broadcasted_argnums=(5,),
        )
        if is_data_parallel
        else jax.jit(update_step_precast, static_argnums=(5,))
    )

    global_execution = None
    if global_update_arrays:
        from kaggriculture.training.global_update import GlobalUpdate

        global_execution = GlobalUpdate(
            update_step_precast, selected_devices if collective_devices is None else tuple(collective_devices)
        )
        compiled_update_step = global_execution

    if memory_budget_fraction is not None:
        from kaggriculture.training.memory_budget import guarded_dispatch

        compiled_update_step = guarded_dispatch(compiled_update_step, selected_devices, memory_budget_fraction)

    if not is_data_parallel:
        cached_master_params: Params | None = None
        cached_inference_params: Params | None = None
        cached_reference_source: Params | None = None
        cached_reference_params: Params | None = None

        def update_step(
            params: Params,
            reference_params: Params,
            optimizer_state: Any,
            batch: dict[str, Array],
        ):
            nonlocal cached_master_params, cached_inference_params
            nonlocal cached_reference_source, cached_reference_params
            if cached_reference_source is not reference_params:
                cached_reference_params = cast_dense_params(reference_params, compute_dtype)
                cached_reference_source = reference_params
            assert cached_reference_params is not None
            if cached_master_params is not params:
                cached_inference_params = cast_dense_params(params, compute_dtype)
                cached_master_params = params
            assert cached_inference_params is not None
            params, next_inference_params, optimizer_state, metrics = compiled_update_step(
                params,
                cached_inference_params,
                cached_reference_params,
                optimizer_state,
                batch,
                True if schedule is None else schedule.should_emit(optimizer_state),
            )
            if schedule is not None:
                schedule.advance(optimizer_state)
            cached_master_params = params
            cached_inference_params = next_inference_params
            return params, optimizer_state, metrics

        update_step.data_parallel_device_count = 1
        return update_step

    cached_master_source: Params | None = None
    cached_master_params: Params | None = None
    cached_inference_params: Params | None = None
    cached_reference_source: Params | None = None
    cached_reference_params: Params | None = None
    cached_optimizer_source: Any = None
    cached_optimizer_state: Any = None

    batch_sharding = NamedSharding(
        Mesh(np.asarray(selected_devices, dtype=object), ("batch_replicas",)), PartitionSpec("batch_replicas")
    )

    def prepare_batch(batch: dict[str, Array]) -> PreparedUpdateBatch:
        sharded = shard_batch(
            batch,
            selected_devices,
            balance_sample_mask=True,
            reference_samples=ppo_config.reference_kl_samples,
            allow_uneven_pairs=allow_uneven_pairs,
        )
        arrays = jax.device_put(sharded, batch_sharding)
        if global_execution is not None:
            arrays = global_execution.to_global(arrays)
        return PreparedUpdateBatch(arrays)

    def update_step(
        params: Params,
        reference_params: Params,
        optimizer_state: Any,
        batch: dict[str, Array] | PreparedUpdateBatch,
    ):
        nonlocal cached_master_source, cached_master_params, cached_inference_params
        nonlocal cached_reference_source, cached_reference_params
        nonlocal cached_optimizer_source, cached_optimizer_state
        if cached_reference_source is not reference_params:
            cached_reference_params = put_replicated(
                cast_dense_params(reference_params, compute_dtype),
                selected_devices,
            )
            cached_reference_source = reference_params
            if global_execution is not None:
                cached_reference_params = global_execution.to_global(cached_reference_params)
        assert cached_reference_params is not None
        if cached_master_source is not params:
            cached_master_params = put_replicated(params, selected_devices)
            cached_inference_params = put_replicated(
                cast_dense_params(params, compute_dtype),
                selected_devices,
            )
            cached_master_source = params
            if global_execution is not None:
                cached_master_params = global_execution.to_global(cached_master_params)
                cached_inference_params = global_execution.to_global(cached_inference_params)
        assert cached_master_params is not None and cached_inference_params is not None
        if cached_optimizer_source is not optimizer_state:
            cached_optimizer_state = put_replicated(optimizer_state, selected_devices)
            cached_optimizer_source = optimizer_state
            if global_execution is not None:
                cached_optimizer_state = global_execution.to_global(cached_optimizer_state)
        if global_execution is not None and not isinstance(batch, PreparedUpdateBatch):
            batch = prepare_batch(batch)
        sharded_batch = (
            batch.arrays
            if isinstance(batch, PreparedUpdateBatch)
            else shard_batch(
                batch,
                selected_devices,
                balance_sample_mask=True,
                reference_samples=ppo_config.reference_kl_samples,
                allow_uneven_pairs=allow_uneven_pairs,
            )
        )
        replicated_params, next_inference_params, replicated_optimizer_state, replicated_metrics = compiled_update_step(
            cached_master_params,
            cached_inference_params,
            cached_reference_params,
            cached_optimizer_state,
            sharded_batch,
            True if schedule is None else schedule.should_emit(optimizer_state),
        )
        if schedule is not None:
            schedule.advance(replicated_optimizer_state)
        cached_master_source = replicated_params
        cached_master_params = replicated_params
        cached_inference_params = next_inference_params
        cached_optimizer_source = replicated_optimizer_state
        cached_optimizer_state = replicated_optimizer_state
        if global_execution is not None:
            replicated_metrics = global_execution.to_local(replicated_metrics)
        return replicated_params, replicated_optimizer_state, replicated_metrics

    def finalize(params: Params, optimizer_state: Any) -> tuple[Params, Any]:
        nonlocal cached_master_source, cached_master_params
        nonlocal cached_optimizer_source, cached_optimizer_state
        extract = unreplicate if global_execution is None else global_execution.first_local_replica
        logical_params = extract(params)
        logical_optimizer_state = extract(optimizer_state)
        cached_master_source = logical_params
        cached_master_params = params
        cached_optimizer_source = logical_optimizer_state
        cached_optimizer_state = optimizer_state
        return logical_params, logical_optimizer_state

    update_step.data_parallel_device_count = len(selected_devices)
    update_step.finalize = finalize
    update_step.prepare_batch = prepare_batch
    update_step.reduce_metrics = unreplicate
    return update_step


def make_policy_diagnostics_evaluator(
    model_config: JaxModelConfig,
    compute_dtype: jnp.dtype,
    devices: Sequence[jax.Device] | None = None,
    *,
    collective_devices: Sequence[jax.Device] | None = None,
    partition_kernel: Callable | None = None,
    selected_partition_kernel: Callable | None = None,
    prune_final_queries: bool = False,
    remat_ffn_activation: bool = False,
):
    """Compile full-rollout post-update policy and value diagnostics."""

    def evaluate_precast(inference_params: Params, batch: dict[str, Array]) -> dict[str, Array]:
        outputs = policy_forward(
            inference_params,
            batch,
            model_config,
            dtype=compute_dtype,
            training=False,
            partition_kernel=partition_kernel,
            selected_partition_kernel=selected_partition_kernel,
            prune_final_queries=prune_final_queries,
            remat_ffn_activation=remat_ffn_activation,
        )
        outputs = behavior_outputs(outputs, batch)
        unit_entropy, market_entropy = joint_entropy_components(outputs, batch["unit_mask"])
        normalized_entropy, unit_normalized_entropy, market_normalized_entropy = normalized_joint_entropy(
            outputs,
            batch["unit_mask"],
        )
        return {
            "log_prob": joint_log_prob(
                outputs,
                batch["unit_action"],
                batch["market_action"],
                batch["unit_mask"],
                batch.get("unit_policy_mask"),
                batch.get("market_policy_mask"),
            ),
            "value": paired_zero_sum_values(outputs["value"]),
            "entropy": unit_entropy + market_entropy,
            "unit_entropy": unit_entropy,
            "market_entropy": market_entropy,
            "normalized_entropy": normalized_entropy,
            "unit_normalized_entropy": unit_normalized_entropy,
            "market_normalized_entropy": market_normalized_entropy,
        }

    selected_devices = tuple(jax.local_devices()[:1] if devices is None else devices)
    is_data_parallel = len(selected_devices) > 1 or collective_devices is not None
    compiled_evaluator = (
        jax.pmap(
            evaluate_precast, devices=selected_devices if collective_devices is None else tuple(collective_devices)
        )
        if is_data_parallel
        else jax.jit(evaluate_precast)
    )
    cached_params_source: Params | None = None
    cached_params: Params | None = None

    def evaluate(params: Params, batch: dict[str, Array]) -> dict[str, Array]:
        nonlocal cached_params_source, cached_params
        if cached_params_source is not params:
            cached_params = cast_dense_params(params, compute_dtype)
            if is_data_parallel:
                cached_params = put_replicated(cached_params, selected_devices)
            cached_params_source = params
        assert cached_params is not None
        if not is_data_parallel:
            return compiled_evaluator(cached_params, batch)
        outputs = compiled_evaluator(cached_params, shard_batch(batch, selected_devices))
        return {name: flatten_pmap_batch(values) for name, values in outputs.items()}

    return evaluate
