"""Synchronous current-current self-play collection with the Rust engine."""

from __future__ import annotations

import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.actions.masks import ActionMaskWorkspace
from kaggriculture.actions.quantities import shed_after_unit_actions
from kaggriculture.training.checkpointing import policy_hash
from kaggriculture.actions.catalog import MARKET_ACTIONS, MARKET_SLOTS, UNIT_ACTIONS
from kaggriculture.observations.features import FEATURE_DIM, FEATURE_INDEX, encode_memory_estimate, encode_observation
from kaggriculture.actions.final_turn import final_turn_ids
from kaggriculture.training.host_memory import register_host_array
from kaggriculture.observations.inventory_tracker import (
    InventoryEstimate,
    OpponentInventoryTracker,
    PublicFlows,
    infer_public_flows,
)
from kaggriculture.agents.neural import FIXED_TOKEN_COUNT, MAX_OWN_UNITS, FixedBatch, prepare_fixed_batch
from kaggriculture.model.policy import (
    VALUE_COST_DIFFERENCE_REFERENCE,
    VALUE_MONEY_ENCODING_REFERENCE,
    JaxModelConfig,
    Params,
    cast_dense_params,
    own_unit_mask_from_features,
    policy_forward,
)
from kaggriculture.training.sharding import flatten_pmap_batch, put_global_replicated, put_replicated, shard_batch
from kaggriculture.training.land_metrics import LandTrace, hand_counts, land_counts, land_order_probability
from kaggriculture.training.purchase_policy import behavior_outputs
from kaggriculture.training.objectives import paired_zero_sum_values
from kaggriculture.training.rollout_chunks import ChunkedSampler
from kaggriculture.training.sampler_keys import PreparedSamplerKey, prepare_sampler_keys
from kaggriculture.actions.sell_quantity import decode_engine_market_order, engine_market_ids

Array = jax.Array
STATE_ARRAY_NAMES = (
    "features",
    "memory_features",
    "coordinates",
    "spatial_mask",
    "rope_groups",
    "token_mask",
    "unit_indices",
    "market_indices",
)
BF16_STORAGE_NAMES = frozenset(("features", "memory_features"))
PARTITIONED_STATE_ARRAY_NAMES = ("features",)


@dataclass
class SeatHistory:
    observer_player: int
    tracker: OpponentInventoryTracker | None = None
    previous_observation: dict[str, Any] | None = None
    previous_action: dict[str, Any] | None = None

    def encode(
        self,
        observation: dict[str, Any],
        public_flows: dict[int, PublicFlows] | None = None,
    ) -> FixedBatch:
        estimate = self.inventory_estimate(observation, public_flows)
        return prepare_fixed_batch(encode_observation(observation, estimate), observation)

    def inventory_estimate(
        self,
        observation: dict[str, Any],
        public_flows: dict[int, PublicFlows] | None = None,
    ) -> InventoryEstimate:
        if self.tracker is None:
            self.tracker = OpponentInventoryTracker(observer_player=self.observer_player)
            return self.tracker.estimate(copy_maps=False)
        elif self.previous_observation is not None:
            self.tracker.advance(
                self.previous_observation,
                observation,
                self.previous_action,
                public_flows,
            )
        return self.tracker.estimate(copy_maps=False)

    def remember(self, observation: dict[str, Any], action: dict[str, Any]) -> None:
        # RustEnv creates fresh Python objects on every step and only reads actions.
        # Retaining them is therefore safe and avoids recursively copying both farms.
        self.previous_observation = observation
        self.previous_action = action


@dataclass
class RolloutBatch:
    states: dict[str, np.ndarray]
    unit_mask: np.ndarray
    unit_action: np.ndarray
    market_action: np.ndarray
    old_log_prob: np.ndarray
    value: np.ndarray
    returns: np.ndarray
    advantages: np.ndarray
    games: int
    horizon: int
    seed_start: int
    seed_end: int
    money: np.ndarray
    collection_seconds: float
    stage_seconds: dict[str, float]
    advantage_mean: float
    advantage_standard_deviation: float
    behavior_hash: str
    purchase_temperature: float = 1.0
    purchase_temperature_steps: int = 5
    purchase_temperature_enabled: bool = False
    land_trace: LandTrace | None = None
    final_turn_fallback: bool = False

    @property
    def transitions(self) -> int:
        return self.games * 2 * self.horizon

    def minibatch(self, indices: np.ndarray, valid_count: int) -> dict[str, np.ndarray]:
        batch = {name: values[indices] for name, values in self.states.items()}
        batch.update(
            {
                "unit_mask": self.unit_mask[indices],
                "unit_action": self.unit_action[indices],
                "market_action": self.market_action[indices],
                "old_log_prob": self.old_log_prob[indices],
                "advantage": self.advantages[indices],
                "return": self.returns[indices],
                "sample_mask": np.arange(len(indices)) < valid_count,
                "episode_step": (indices // (self.games * 2)).astype(np.int32),
            }
        )
        if self.land_trace is not None:
            batch.update(
                land_owned_count=self.land_trace.counts[:-1].reshape(-1)[indices],
                land_affordable=self.land_trace.affordable.reshape(-1)[indices],
            )
        if self.final_turn_fallback:
            batch["policy_valid"] = batch["episode_step"] != self.horizon - 1
        if self.purchase_temperature_enabled or self.purchase_temperature != 1.0:
            batch["purchase_temperature"] = np.where(
                batch["episode_step"] < self.purchase_temperature_steps, self.purchase_temperature, 1.0
            ).astype(np.float32)
            batch["purchase_temperature_steps"] = np.asarray(self.purchase_temperature_steps, dtype=np.int32)
        return batch


@dataclass
class RolloutWorkspace:
    """Reusable host buffers for identically shaped full-game rollouts."""

    games: int
    horizon: int
    compute_dtype: jnp.dtype
    compact_storage_dtype: np.dtype | jnp.dtype | None
    feature_buffer: np.ndarray
    feature_buffer_registration: Any | None
    unit_mask: np.ndarray
    unit_action: np.ndarray
    market_action: np.ndarray
    log_prob: np.ndarray
    value: np.ndarray
    states: dict[str, np.ndarray] | None = None
    action_masks: ActionMaskWorkspace | None = None

    @classmethod
    def create(
        cls,
        *,
        games: int,
        horizon: int,
        compute_dtype: jnp.dtype,
        compact_storage_dtype: np.dtype | jnp.dtype | None = None,
        pin_features: bool = False,
        legal_mask: bool = False,
    ) -> RolloutWorkspace:
        transitions = games * 2 * horizon
        feature_buffer = np.empty((games * 2, FIXED_TOKEN_COUNT, FEATURE_DIM), dtype=np.float32)
        registration = register_host_array(feature_buffer) if pin_features else None
        return cls(
            games=games,
            horizon=horizon,
            compute_dtype=compute_dtype,
            compact_storage_dtype=compact_storage_dtype,
            feature_buffer=feature_buffer,
            feature_buffer_registration=registration,
            unit_mask=np.empty((transitions, MAX_OWN_UNITS), dtype=np.bool_),
            unit_action=np.empty((transitions, MAX_OWN_UNITS), dtype=np.int32),
            market_action=np.empty((transitions, MARKET_SLOTS), dtype=np.int32),
            log_prob=np.empty((transitions,), dtype=np.float32),
            value=np.empty((transitions,), dtype=np.float32),
            action_masks=ActionMaskWorkspace(games * 2, pin=pin_features) if legal_mask else None,
        )

    def validate(
        self,
        *,
        games: int,
        horizon: int,
        compute_dtype: jnp.dtype,
        compact_storage_dtype: np.dtype | jnp.dtype | None,
    ) -> None:
        expected = (games, horizon, np.dtype(compute_dtype), compact_storage_dtype)
        actual = (self.games, self.horizon, np.dtype(self.compute_dtype), self.compact_storage_dtype)
        if actual != expected:
            raise ValueError(f"rollout workspace mismatch: actual={actual}, expected={expected}")


def stack_fixed_batches(fixed_batches: list[FixedBatch]) -> tuple[dict[str, np.ndarray], np.ndarray]:
    states = {
        name: np.concatenate([fixed.arrays[name] for fixed in fixed_batches], axis=0) for name in STATE_ARRAY_NAMES
    }
    unit_mask = np.zeros((len(fixed_batches), MAX_OWN_UNITS), dtype=np.bool_)
    for index, fixed in enumerate(fixed_batches):
        unit_mask[index, : fixed.encoded_own_units] = True
    return states, unit_mask


def value_context_from_features(features: np.ndarray) -> dict[str, np.ndarray]:
    """Recover public current-money difference before compact BF16 trajectory storage."""
    global_features = features[:, 0].astype(np.float32)
    money_log_scale = np.float32(np.log1p(VALUE_MONEY_ENCODING_REFERENCE))
    self_money = np.expm1(global_features[:, FEATURE_INDEX["self_money"]] * money_log_scale)
    opponent_money = np.expm1(global_features[:, FEATURE_INDEX["opponent_money"]] * money_log_scale)
    return {
        "value_cost_difference": ((self_money - opponent_money) / VALUE_COST_DIFFERENCE_REFERENCE).astype(np.float32),
        "value_time": global_features[:, FEATURE_INDEX["season_progress"]].astype(np.float32),
    }


def sample_categorical_cdf(logits: Array, key: Array) -> tuple[Array, Array]:
    """Sample categorical rows with one uniform variate and return selected log-probabilities."""
    log_probs = jax.nn.log_softmax(logits.astype(jnp.float32), axis=-1)
    thresholds = jax.random.uniform(key, (*logits.shape[:-1], 1), dtype=jnp.float32)
    actions = inverse_cdf_actions(log_probs, thresholds)
    selected = jnp.take_along_axis(log_probs, actions[..., None], axis=-1)[..., 0]
    return actions, selected


def inverse_cdf_actions(log_probs: Array, thresholds: Array) -> Array:
    cumulative = jnp.cumsum(jnp.exp(log_probs), axis=-1)
    # A strict upper bound skips zero-mass plateaus even when uniform() returns zero.
    # Renormalizing the final sum prevents roundoff from selecting a masked trailing bin.
    cumulative /= cumulative[..., -1:]
    return jnp.sum(cumulative <= thresholds, axis=-1).astype(jnp.int32)


def make_sampler(
    model_config: JaxModelConfig,
    compute_dtype: jnp.dtype,
    devices: Sequence[jax.Device] | None = None,
    *,
    collective_devices: Sequence[jax.Device] | None = None,
    cache_global_params: bool = True,
    precompute_keys: bool = True,
    partition_kernel: Callable | None = None,
    selected_partition_kernel: Callable | None = None,
    prune_final_queries: bool = False,
    remat_ffn_activation: bool = False,
    track_land: bool = False,
):
    def sample_precast(params: Params, batch: dict[str, Array], key: Array):
        next_key, sample_key = jax.random.split(key)
        outputs = policy_forward(
            params,
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
        unit_mask = (
            own_unit_mask_from_features(batch["features"])
            if model_config.rope_correction_backend == "partitioned"
            else batch["unit_mask"]
        )
        unit_key, market_key = jax.random.split(sample_key)
        if model_config.sequential_patch:
            from kaggriculture.actions.sequential import sequential_units

            thresholds = jax.random.uniform(unit_key, outputs["unit_action"].shape[:2], dtype=jnp.float32)
            unit_action, unit_log_prob, effective_stems = sequential_units(
                outputs["unit_action"], batch["legal_mask_stems"], batch["patch_context"], thresholds
            )
        else:
            unit_action, unit_log_prob = sample_categorical_cdf(outputs["unit_action"], unit_key)
        if track_land:
            market_log_probs = jax.nn.log_softmax(outputs["market_action"].astype(jnp.float32), axis=-1)
            thresholds = jax.random.uniform(market_key, (*market_log_probs.shape[:-1], 1), dtype=jnp.float32)
            market_action = inverse_cdf_actions(market_log_probs, thresholds)
            market_log_prob = jnp.take_along_axis(market_log_probs, market_action[..., None], axis=-1)[..., 0]
            land_probability = land_order_probability(market_log_probs, absolute=model_config.absolute_sell)
        else:
            market_action, market_log_prob = sample_categorical_cdf(outputs["market_action"], market_key)
        log_prob = jnp.sum(unit_log_prob * unit_mask, axis=-1) + jnp.sum(market_log_prob, axis=-1)
        result = (next_key, unit_action, market_action, log_prob, paired_zero_sum_values(outputs["value"]))
        if track_land:
            result = (*result, land_probability)
        return (*result, unit_log_prob, market_log_prob, effective_stems) if model_config.sequential_patch else result

    selected_devices = tuple(jax.local_devices()[:1] if devices is None else devices)
    if len(selected_devices) == 1 and collective_devices is None:
        return jax.jit(sample_precast)

    use_global_params = collective_devices is not None and cache_global_params
    compiled_sampler = jax.pmap(
        sample_precast,
        devices=selected_devices if collective_devices is None else tuple(collective_devices),
        in_axes=(None if use_global_params else 0, 0, 0),
    )
    cached_params_source: Params | None = None
    cached_params: Params | None = None

    def sample(params: Params, batch: dict[str, Array], key: Array | PreparedSamplerKey):
        nonlocal cached_params_source, cached_params
        if cached_params_source is not params:
            cached_params = (
                put_replicated(params, selected_devices)
                if not use_global_params
                else put_global_replicated(params, collective_devices)
            )
            cached_params_source = params
        assert cached_params is not None
        sharded_batch = shard_batch(batch, selected_devices)
        if isinstance(key, PreparedSamplerKey):
            next_key, sharded_keys = key.next_key, key.replica_keys
        else:
            next_key, parallel_key = jax.random.split(key)
            sharded_keys = np.asarray(jax.device_get(jax.random.split(parallel_key, len(selected_devices))))
        _, *sampled = compiled_sampler(
            cached_params,
            sharded_batch,
            sharded_keys,
        )
        return (next_key, *(flatten_pmap_batch(value) for value in sampled))

    sample.data_parallel_device_count = len(selected_devices)
    # shard_batch already transfers to the devices; a JAX input here would round-trip via the host.
    sample.requires_host_batch = True

    def prepare_keys(key: Array, steps: int) -> list[PreparedSamplerKey]:
        return prepare_sampler_keys(key, steps=steps, replicas=len(selected_devices))

    if precompute_keys:
        sample.prepare_keys = prepare_keys
    return sample


def decode_actions(
    observations: list[dict[str, Any]],
    fixed_batches: list[FixedBatch],
    unit_ids: np.ndarray,
    market_ids: np.ndarray,
) -> list[dict[str, Any]]:
    actions = []
    for observation, fixed, selected_units, selected_market in zip(
        observations,
        fixed_batches,
        unit_ids,
        market_ids,
    ):
        unit_actions = [list(UNIT_ACTIONS[int(selected_units[index])]) for index in range(fixed.encoded_own_units)]
        unit_actions.extend([["PASS"] for _ in range(fixed.actual_own_units - fixed.encoded_own_units)])
        sellable_shed = shed_after_unit_actions(observation, unit_actions)
        market = []
        for action_id in selected_market:
            order = decode_engine_market_order(int(action_id), sellable_shed)
            if order is None:
                continue
            market.append(order)
            if order[0] == "SELL":
                item = str(order[1])
                sellable_shed[item] = max(0, sellable_shed.get(item, 0) - int(order[2]))
        actions.append({"farmer": unit_actions[0], "hands": unit_actions[1:], "market": market})
    return actions


def _allocate_storage(
    first_states: dict[str, np.ndarray],
    transitions: int,
    compute_dtype: jnp.dtype,
    compact_storage_dtype: np.dtype | jnp.dtype | None,
) -> dict[str, np.ndarray]:
    model_storage_dtype = compute_dtype if compact_storage_dtype is None else compact_storage_dtype
    return {
        name: np.empty(
            (transitions, *values.shape[1:]),
            dtype=model_storage_dtype if compute_dtype == jnp.bfloat16 and name in BF16_STORAGE_NAMES else values.dtype,
        )
        for name, values in first_states.items()
    }


def generalized_advantage_estimate(
    values: np.ndarray,
    terminal_rewards: np.ndarray,
    *,
    horizon: int,
    games: int,
    gamma: float,
    gae_lambda: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute full-game GAE backward while retaining time/game/seat layout."""
    paired_values = values.reshape(horizon, games, 2)
    rewards = np.zeros_like(paired_values)
    rewards[-1] = terminal_rewards
    advantages = np.empty_like(paired_values)
    next_advantage = np.zeros((games, 2), dtype=np.float32)

    for step in range(horizon - 1, -1, -1):
        terminal = step == horizon - 1
        next_value = 0.0 if terminal else paired_values[step + 1]
        continuation = 0.0 if terminal else 1.0
        delta = rewards[step] + gamma * continuation * next_value - paired_values[step]
        next_advantage = delta + gamma * gae_lambda * continuation * next_advantage
        advantages[step] = next_advantage

    returns = advantages + paired_values
    return returns.reshape(-1), advantages.reshape(-1)


def collect_self_play(
    params: Params,
    model_config: JaxModelConfig,
    *,
    games: int,
    horizon: int,
    seed_counter: int,
    rng: Array,
    compute_dtype: jnp.dtype,
    gamma: float = 1.0,
    gae_lambda: float = 0.85,
    sampler: Callable[[Params, dict[str, Array], Array], tuple[Array, Array, Array, Array, Array]] | None = None,
    inference_batch_size: int | None = None,
    compact_storage_dtype: np.dtype | jnp.dtype | None = None,
    pinned_feature_buffer: bool = False,
    workspace: RolloutWorkspace | None = None,
    purchase_temperature: float = 1.0,
    purchase_temperature_steps: int = 5,
    purchase_temperature_enabled: bool = False,
    track_land: bool = False,
    final_turn_fallback: bool = False,
) -> tuple[RolloutBatch, Array]:
    if games <= 0 or horizon <= 0:
        raise ValueError("games and horizon must be positive")
    if horizon > 719:
        raise ValueError("the authoritative environment has at most 719 transitions")
    if final_turn_fallback and horizon != 719:
        raise ValueError("final-turn fallback requires a complete 719-transition game")

    import kagg_engine

    started = time.monotonic()
    seeds = list(range(seed_counter, seed_counter + games))
    overrides = {"episodeSteps": horizon + 1}
    rust_batch_environment_supported = (
        model_config.rope_correction_backend == "partitioned"
        and hasattr(kagg_engine, "RustBatchEnv")
        and hasattr(kagg_engine.RustBatchEnv, "write_partitioned_features_both")
        and hasattr(kagg_engine.RustBatchEnv, "step_self_play_ids_batch")
    )
    batch_environment = (
        kagg_engine.RustBatchEnv(seeds, config_overrides=overrides) if rust_batch_environment_supported else None
    )
    environments = (
        []
        if batch_environment is not None
        else [kagg_engine.RustEnv(seed, config_overrides=overrides) for seed in seeds]
    )
    rust_batch_feature_encoder = getattr(kagg_engine, "fixed_features_batch", None)
    rust_partitioned_feature_encoder = getattr(kagg_engine, "partitioned_features_batch", None)
    rust_batch_stepper = getattr(kagg_engine, "step_ids_batch", None)
    rust_bf16_copy = getattr(kagg_engine, "copy_f32_to_bf16_bits", None)
    rust_feature_encoder = bool(environments) and hasattr(environments[0], "fixed_features")
    rust_tracks_history = batch_environment is not None or (
        bool(environments) and hasattr(environments[0], "tracked_memory")
    )
    selected_batch_feature_encoder = (
        rust_partitioned_feature_encoder
        if model_config.rope_correction_backend == "partitioned" and rust_partitioned_feature_encoder is not None
        else rust_batch_feature_encoder
    )
    native_rust_rollout = batch_environment is not None or (
        selected_batch_feature_encoder is not None and rust_batch_stepper is not None and rust_tracks_history
    )
    observations_by_game = (
        [] if native_rust_rollout else [environment.reset(seed) for environment, seed in zip(environments, seeds)]
    )
    if track_land and batch_environment is None:
        raise ValueError("land diagnostics require the native RustBatchEnv rollout")
    land_trace = LandTrace.create(horizon, games * 2) if track_land else None
    histories = [] if native_rust_rollout else [[SeatHistory(0), SeatHistory(1)] for _ in environments]
    agents_per_step = games * 2
    if workspace is not None:
        workspace.validate(
            games=games,
            horizon=horizon,
            compute_dtype=compute_dtype,
            compact_storage_dtype=compact_storage_dtype,
        )
        if batch_environment is None:
            raise ValueError("a reusable rollout workspace requires the RustBatchEnv fast path")
        if pinned_feature_buffer and workspace.feature_buffer_registration is None:
            raise ValueError("the reusable rollout workspace feature buffer is not pinned")
    feature_buffer = (
        workspace.feature_buffer
        if workspace is not None
        else (
            np.empty((agents_per_step, FIXED_TOKEN_COUNT, FEATURE_DIM), dtype=np.float32)
            if batch_environment is not None
            else None
        )
    )
    feature_buffer_registration = (
        register_host_array(feature_buffer)
        if workspace is None and pinned_feature_buffer and feature_buffer is not None
        else None
    )
    action_masks = None
    if model_config.legal_mask:
        if batch_environment is None or not hasattr(batch_environment, "write_action_masks_both"):
            raise ValueError("masked PPO requires the pinned RustBatchEnv mask writer")
        action_masks = (
            workspace.action_masks
            if workspace is not None
            else ActionMaskWorkspace(agents_per_step, pin=pinned_feature_buffer)
        )
        if action_masks is None:
            raise ValueError("masked PPO requires a mask-enabled rollout workspace")
    patch_stems = patch_context = None
    patch_unit_valid = patch_market_valid = None
    if model_config.sequential_patch:
        from kaggriculture.actions.masks import MASK_STEM_SIZE
        from kaggriculture.actions.sequential import PATCH_CONTEXT_SIZE

        if batch_environment is None or not hasattr(batch_environment, "write_patch_inputs"):
            raise ValueError("sequential patch requires the training Rust patch writer")
        patch_stems = np.empty((agents_per_step, MASK_STEM_SIZE), dtype=np.bool_)
        patch_context = np.empty((agents_per_step, PATCH_CONTEXT_SIZE), dtype=np.int32)
        patch_unit_valid = np.ones((agents_per_step, 20), dtype=np.bool_)
        patch_market_valid = np.ones((agents_per_step, 10), dtype=np.bool_)
    inference_batch_size = agents_per_step if inference_batch_size is None else inference_batch_size
    transitions = agents_per_step * horizon
    if sampler is None:
        sampler = make_sampler(model_config, compute_dtype, track_land=track_land)
    if inference_batch_size < agents_per_step:
        sampler = ChunkedSampler(sampler, rows=agents_per_step, batch_size=inference_batch_size)
        inference_batch_size = agents_per_step
    prepare_keys = getattr(sampler, "prepare_keys", None)
    sampler_keys = None if prepare_keys is None else prepare_keys(rng, horizon)
    inference_params = cast_dense_params(params, compute_dtype)
    inference_indices = (
        None if inference_batch_size == agents_per_step else np.resize(np.arange(agents_per_step), inference_batch_size)
    )
    state_array_names = (
        PARTITIONED_STATE_ARRAY_NAMES if model_config.rope_correction_backend == "partitioned" else STATE_ARRAY_NAMES
    )
    states_storage = None if workspace is None else workspace.states
    unit_mask_storage = (
        np.empty((transitions, MAX_OWN_UNITS), dtype=np.bool_) if workspace is None else workspace.unit_mask
    )
    unit_action_storage = (
        np.empty((transitions, MAX_OWN_UNITS), dtype=np.int32) if workspace is None else workspace.unit_action
    )
    market_action_storage = (
        np.empty((transitions, MARKET_SLOTS), dtype=np.int32) if workspace is None else workspace.market_action
    )
    log_prob_storage = np.empty((transitions,), dtype=np.float32) if workspace is None else workspace.log_prob
    value_storage = np.empty((transitions,), dtype=np.float32) if workspace is None else workspace.value
    stage_seconds = {
        "setup": time.monotonic() - started,
        "features": 0.0,
        "storage": 0.0,
        "inference": 0.0,
        "environment": 0.0,
        "legal_masks": 0.0,
        "land_metrics": 0.0,
    }
    temperature_batches = (
        {
            active: np.full(inference_batch_size, purchase_temperature if active else 1.0, dtype=np.float32)
            for active in (False, True)
        }
        if purchase_temperature_enabled or purchase_temperature != 1.0
        else None
    )
    for step in range(horizon):
        stage_started = time.monotonic()
        flat_observations = (
            []
            if native_rust_rollout
            else [observations_by_game[game][seat] for game in range(games) for seat in range(2)]
        )
        flat_histories = (
            [] if native_rust_rollout else [histories[game][seat] for game in range(games) for seat in range(2)]
        )
        public_flows_by_game: list[dict[int, PublicFlows] | None] = []
        if not rust_tracks_history:
            for game in range(games):
                previous = histories[game][0].previous_observation
                current = observations_by_game[game][0]
                if previous is None:
                    public_flows_by_game.append(None)
                    continue
                public_flows_by_game.append(
                    {player: infer_public_flows(previous, current, player) for player in range(2)}
                )
        flat_public_flows = (
            [None] * agents_per_step
            if rust_tracks_history
            else [public_flows_by_game[game] for game in range(games) for _ in range(2)]
        )
        fixed_batches: list[FixedBatch] = []
        if batch_environment is not None:
            with jax.profiler.TraceAnnotation("rust_write_partitioned_features_both"):
                actual_unit_counts, encoded_unit_counts = batch_environment.write_partitioned_features_both(
                    feature_buffer
                )
            state_batch = {"features": feature_buffer}
            unit_mask = np.arange(MAX_OWN_UNITS)[None, :] < np.asarray(encoded_unit_counts)[:, None]
        elif rust_partitioned_feature_encoder is not None and model_config.rope_correction_backend == "partitioned":
            with jax.profiler.TraceAnnotation("rust_partitioned_features_batch"):
                features, actual_unit_counts, encoded_unit_counts = rust_partitioned_feature_encoder(environments)
            state_batch = {"features": np.asarray(features)}
            unit_mask = np.arange(MAX_OWN_UNITS)[None, :] < np.asarray(encoded_unit_counts)[:, None]
        elif rust_batch_feature_encoder is not None and rust_tracks_history:
            with jax.profiler.TraceAnnotation("rust_fixed_features_batch"):
                state_batch, actual_unit_counts, encoded_unit_counts = rust_batch_feature_encoder(environments)
            state_batch = {name: np.asarray(values) for name, values in state_batch.items()}
            unit_mask = np.arange(MAX_OWN_UNITS)[None, :] < np.asarray(encoded_unit_counts)[:, None]
            if not native_rust_rollout:
                fixed_batches = [
                    FixedBatch(arrays={}, actual_own_units=actual, encoded_own_units=encoded)
                    for actual, encoded in zip(actual_unit_counts, encoded_unit_counts)
                ]
        elif rust_batch_feature_encoder is not None:
            estimates = [
                history.inventory_estimate(observation, public_flows)
                for history, observation, public_flows in zip(
                    flat_histories,
                    flat_observations,
                    flat_public_flows,
                )
            ]
            memory_batch = np.stack([encode_memory_estimate(estimate) for estimate in estimates])
            state_batch, actual_unit_counts, encoded_unit_counts = rust_batch_feature_encoder(
                environments,
                memory_batch,
            )
            state_batch = {name: np.asarray(values) for name, values in state_batch.items()}
            unit_mask = np.arange(MAX_OWN_UNITS)[None, :] < np.asarray(encoded_unit_counts)[:, None]
            fixed_batches = [
                FixedBatch(arrays={}, actual_own_units=actual, encoded_own_units=encoded)
                for actual, encoded in zip(actual_unit_counts, encoded_unit_counts)
            ]
        elif rust_feature_encoder:
            estimates = [
                history.inventory_estimate(observation, public_flows)
                for history, observation, public_flows in zip(
                    flat_histories,
                    flat_observations,
                    flat_public_flows,
                )
            ]
            fixed_batches = []
            for game, environment in enumerate(environments):
                for seat in range(2):
                    estimate = estimates[2 * game + seat]
                    arrays, actual_own_units, encoded_own_units = environment.fixed_features(
                        seat,
                        encode_memory_estimate(estimate).tolist(),
                    )
                    fixed_batches.append(
                        FixedBatch(
                            arrays=arrays,
                            actual_own_units=actual_own_units,
                            encoded_own_units=encoded_own_units,
                        )
                    )
        else:
            fixed_batches = [
                history.encode(observation, public_flows)
                for history, observation, public_flows in zip(
                    flat_histories,
                    flat_observations,
                    flat_public_flows,
                )
            ]
        if selected_batch_feature_encoder is None:
            state_batch, unit_mask = stack_fixed_batches(fixed_batches)
        model_state_batch = {name: state_batch[name] for name in state_array_names}
        model_state_batch.update(value_context_from_features(model_state_batch["features"]))
        stage_seconds["features"] += time.monotonic() - stage_started

        if land_trace is not None:
            stage_started = time.monotonic()
            with jax.profiler.TraceAnnotation("land_snapshot"):
                land_trace.observe(step, model_state_batch["features"], np.asarray(batch_environment.rewards()))
            stage_seconds["land_metrics"] += time.monotonic() - stage_started

        if action_masks is not None:
            stage_started = time.monotonic()
            with jax.profiler.TraceAnnotation("rust_action_masks_and_compaction"):
                model_state_batch["legal_mask_stems"] = action_masks.write(batch_environment)
            stage_seconds["legal_masks"] += time.monotonic() - stage_started

        if patch_stems is not None:
            stage_started = time.monotonic()
            batch_environment.write_patch_inputs(patch_stems, patch_context)
            model_state_batch["legal_mask_stems"] = patch_stems
            model_state_batch["unit_policy_mask"] = patch_unit_valid
            model_state_batch["market_policy_mask"] = patch_market_valid
            stage_seconds["legal_masks"] += time.monotonic() - stage_started

        stage_started = time.monotonic()
        if states_storage is None:
            states_storage = _allocate_storage(
                model_state_batch,
                transitions,
                compute_dtype,
                compact_storage_dtype,
            )
            if workspace is not None:
                workspace.states = states_storage
        with jax.profiler.TraceAnnotation("jax_inference_dispatch"):
            use_host_batch = getattr(sampler, "data_parallel_device_count", 1) > 1 or getattr(
                sampler, "requires_host_batch", False
            )
            array = np.asarray if use_host_batch else jnp.asarray
            if inference_indices is None:
                device_batch = {name: array(values) for name, values in model_state_batch.items()}
                if model_config.rope_correction_backend != "partitioned":
                    device_batch["unit_mask"] = array(unit_mask)
            else:
                device_batch = {name: array(values[inference_indices]) for name, values in model_state_batch.items()}
                if model_config.rope_correction_backend != "partitioned":
                    device_batch["unit_mask"] = array(unit_mask[inference_indices])
            if temperature_batches is not None:
                device_batch["purchase_temperature"] = array(temperature_batches[step < purchase_temperature_steps])
            if patch_context is not None:
                device_batch["patch_context"] = array(
                    patch_context if inference_indices is None else patch_context[inference_indices]
                )
            rng, *sampled = sampler(inference_params, device_batch, rng if sampler_keys is None else sampler_keys[step])
        stage_seconds["inference"] += time.monotonic() - stage_started

        stage_started = time.monotonic()
        with jax.profiler.TraceAnnotation("trajectory_storage"):
            start = step * agents_per_step
            end = start + agents_per_step
            for name, values in model_state_batch.items():
                destination = states_storage[name][start:end]
                if name == "features" and destination.dtype == jnp.bfloat16 and rust_bf16_copy is not None:
                    rust_bf16_copy(values, destination.view(np.uint16))
                else:
                    destination[:] = values
            unit_mask_storage[start:end] = unit_mask
        stage_seconds["storage"] += time.monotonic() - stage_started

        stage_started = time.monotonic()
        with jax.profiler.TraceAnnotation("jax_inference_wait"):
            host_sampled = jax.device_get(sampled)
            unit_ids, market_ids, log_prob, values = host_sampled[:4]
            if model_config.sequential_patch:
                states_storage["legal_mask_stems"][start:end] = host_sampled[-1][:agents_per_step]
            if land_trace is not None:
                land_trace.probability[step] = host_sampled[4][:agents_per_step]
        unit_ids = unit_ids[:agents_per_step]
        market_ids = market_ids[:agents_per_step]
        if action_masks is not None:
            unit_legal = np.take_along_axis(action_masks.unit_dense, unit_ids[..., None], axis=-1)
            market_legal = np.take_along_axis(action_masks.market_dense, market_ids, axis=-1)
            if not unit_legal.all() or not market_legal.all():
                raise RuntimeError("sampler selected an action outside its stored legal mask")
        unit_action_storage[start:end] = unit_ids
        market_action_storage[start:end] = market_ids
        log_prob_storage[start:end] = log_prob[:agents_per_step]
        value_storage[start:end] = values[:agents_per_step]
        stage_seconds["inference"] += time.monotonic() - stage_started

        stage_started = time.monotonic()
        expected_done = step == horizon - 1
        executed_unit_ids, executed_market_ids = unit_ids, market_ids
        if final_turn_fallback and expected_done and not model_config.sequential_patch:
            final_observations = (
                [observation for game in batch_environment.observe() for observation in game]
                if batch_environment is not None
                else [observation for game in environments for observation in game.observe()]
                if native_rust_rollout
                else flat_observations
            )
            forced = [
                final_turn_ids(observation, unit_ids.shape[1], absolute_sell=model_config.absolute_sell)
                for observation in final_observations
            ]
            executed_unit_ids = np.stack([actions[0] for actions in forced])
            executed_market_ids = np.stack([actions[1] for actions in forced])
        decoded_market_ids = engine_market_ids(executed_market_ids, absolute=model_config.absolute_sell)
        if model_config.sequential_patch:
            executed_unit_ids = np.array(unit_ids, dtype=np.int32, copy=True)
            decoded_market_ids = np.array(decoded_market_ids, dtype=np.int32, copy=True)
            batch_environment.patch_action_ids(
                executed_unit_ids, decoded_market_ids, patch_unit_valid, patch_market_valid
            )
            states_storage["unit_policy_mask"][start:end] = patch_unit_valid
            states_storage["market_policy_mask"][start:end] = patch_market_valid
            unit_lp, market_lp = host_sampled[-3:-1]
            log_prob_storage[start:end] = (unit_lp[:agents_per_step] * unit_mask * patch_unit_valid).sum(axis=-1) + (
                market_lp[:agents_per_step] * patch_market_valid
            ).sum(axis=-1)
        if native_rust_rollout:
            if batch_environment is not None:
                with jax.profiler.TraceAnnotation("rust_step_self_play_ids_batch"):
                    done_by_game = batch_environment.step_self_play_ids_batch(executed_unit_ids, decoded_market_ids)
            else:
                with jax.profiler.TraceAnnotation("rust_step_ids_batch"):
                    done_by_game = rust_batch_stepper(environments, executed_unit_ids, decoded_market_ids)
            for game, done in enumerate(done_by_game):
                if done != expected_done:
                    raise RuntimeError(f"environment {game} done={done} at step {step}, expected {expected_done}")
        else:
            flat_actions = decode_actions(flat_observations, fixed_batches, executed_unit_ids, decoded_market_ids)
            if not rust_tracks_history:
                for history, observation, action in zip(flat_histories, flat_observations, flat_actions):
                    history.remember(observation, action)

            next_observations = []
            for game, environment in enumerate(environments):
                actions = flat_actions[2 * game : 2 * game + 2]
                observations, done = environment.step(actions)
                if done != expected_done:
                    raise RuntimeError(f"environment {game} done={done} at step {step}, expected {expected_done}")
                next_observations.append(observations)
            observations_by_game = next_observations
        stage_seconds["environment"] += time.monotonic() - stage_started

    finalize_started = time.monotonic()
    assert states_storage is not None
    if land_trace is not None:
        batch_environment.write_partitioned_features_both(feature_buffer)
        land_trace.counts[-1] = land_counts(feature_buffer)
        land_trace.hands[-1] = hand_counts(feature_buffer)
    rewards_by_game = (
        batch_environment.rewards()
        if batch_environment is not None
        else [environment.rewards for environment in environments]
    )
    money = np.asarray(rewards_by_game, dtype=np.float32)
    agent_rewards = np.zeros((games, 2), dtype=np.float32)
    agent_rewards[:, 0] = np.sign(money[:, 0] - money[:, 1])
    agent_rewards[:, 1] = -agent_rewards[:, 0]
    returns, advantages = generalized_advantage_estimate(
        value_storage,
        agent_rewards,
        horizon=horizon,
        games=games,
        gamma=gamma,
        gae_lambda=gae_lambda,
    )
    advantage_mean = float(advantages.mean())
    advantage_standard_deviation = float(advantages.std())
    stage_seconds["finalize"] = time.monotonic() - finalize_started
    collection_seconds = time.monotonic() - started
    stage_seconds["unattributed"] = max(0.0, collection_seconds - sum(stage_seconds.values()))
    rollout = RolloutBatch(
        land_trace=land_trace,
        final_turn_fallback=final_turn_fallback and not model_config.sequential_patch,
        purchase_temperature=purchase_temperature,
        purchase_temperature_steps=purchase_temperature_steps,
        purchase_temperature_enabled=purchase_temperature_enabled,
        states=states_storage,
        unit_mask=unit_mask_storage,
        unit_action=unit_action_storage,
        market_action=market_action_storage,
        old_log_prob=log_prob_storage,
        value=value_storage,
        returns=returns,
        advantages=advantages,
        games=games,
        horizon=horizon,
        seed_start=seed_counter,
        seed_end=seed_counter + games,
        money=money,
        collection_seconds=collection_seconds,
        stage_seconds=stage_seconds,
        advantage_mean=advantage_mean,
        advantage_standard_deviation=advantage_standard_deviation,
        behavior_hash=policy_hash(params),
    )
    if feature_buffer_registration is not None:
        feature_buffer_registration.close()
    return rollout, jnp.asarray(rng)


def action_catalog_sizes() -> tuple[int, int]:
    return len(UNIT_ACTIONS), len(MARKET_ACTIONS)
