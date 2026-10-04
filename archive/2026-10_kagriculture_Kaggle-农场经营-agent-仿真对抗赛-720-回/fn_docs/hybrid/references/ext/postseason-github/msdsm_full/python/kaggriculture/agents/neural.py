"""Fixed-shape JAX inference for the competition policy."""

from __future__ import annotations

import pickle
from copy import deepcopy
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.actions.masks import MASK_STEM_SIZE, observation_mask_stems
from kaggriculture.actions.quantities import (
    decode_sell_quantity,
    shed_after_unit_actions,
)
from kaggriculture.actions.catalog import (
    BOARD_SIZE,
    ITEMS,
    MARKET_ACTIONS,
    MARKET_SLOTS,
    UNIT_ACTIONS,
)
from kaggriculture.model.execution import forward_options
from kaggriculture.observations.features import (
    FEATURE_DIM,
    MEMORY_FEATURE_NAMES,
    EncodedObservation,
    encode_observation,
    observation_step,
)
from kaggriculture.actions.final_turn import final_turn_action
from kaggriculture.observations.inventory_tracker import (
    InventoryEstimate,
    OpponentInventoryTracker,
)
from kaggriculture.model.policy import (
    JaxModelConfig,
    cast_dense_params,
    policy_forward,
)
from kaggriculture.actions.sell_quantity import ABSOLUTE_ACTION_COUNT, decode_engine_market_order, engine_market_ids


MAX_TOTAL_UNITS = 40
MAX_OWN_UNITS = 20
FIXED_TOKEN_COUNT = 1 + 2 * BOARD_SIZE**2 + MAX_TOTAL_UNITS + len(ITEMS) + 1 + MARKET_SLOTS
CELL_REGION_END = 1 + 2 * BOARD_SIZE**2
__all__ = ["MARKET_ACTIONS", "decode_sell_quantity"]


@dataclass(frozen=True)
class FixedBatch:
    arrays: dict[str, np.ndarray]
    actual_own_units: int
    encoded_own_units: int


def _numpy(tensor: Any) -> np.ndarray:
    if hasattr(tensor, "detach"):
        return tensor.detach().cpu().numpy()
    return np.asarray(tensor)


def prepare_fixed_batch(encoded: EncodedObservation, observation: dict[str, Any]) -> FixedBatch:
    """Pad once and truncate Units only outside the observed-data safety envelope."""
    player = int(observation.get("player", 0))
    farms = observation.get("farms", [])
    if player not in (0, 1) or len(farms) != 2:
        raise ValueError("observation must contain two farms and player 0 or 1")

    actual_own_units = 1 + len(farms[player].get("hands", []))
    actual_opponent_units = 1 + len(farms[1 - player].get("hands", []))
    encoded_own_units = min(actual_own_units, MAX_OWN_UNITS)
    encoded_opponent_units = min(actual_opponent_units, MAX_TOTAL_UNITS - encoded_own_units)

    own_start = CELL_REGION_END
    opponent_start = own_start + actual_own_units
    tail_start = opponent_start + actual_opponent_units
    selected_indices = [
        *range(CELL_REGION_END),
        *range(own_start, own_start + encoded_own_units),
        *range(opponent_start, opponent_start + encoded_opponent_units),
        *range(tail_start, int(encoded.features.shape[0])),
    ]
    selected_count = len(selected_indices)
    if selected_count > FIXED_TOKEN_COUNT:
        raise RuntimeError(f"selected token count {selected_count} exceeds fixed capacity {FIXED_TOKEN_COUNT}")

    old_to_new = {old: new for new, old in enumerate(selected_indices)}
    features = np.zeros((1, FIXED_TOKEN_COUNT, FEATURE_DIM), dtype=np.float32)
    coordinates = np.zeros((1, FIXED_TOKEN_COUNT, 2), dtype=np.float32)
    spatial_mask = np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.bool_)
    rope_groups = np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.int32)
    token_mask = np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.bool_)
    features[0, :selected_count] = _numpy(encoded.features)[selected_indices]
    coordinates[0, :selected_count] = _numpy(encoded.coordinates)[selected_indices]
    spatial_mask[0, :selected_count] = _numpy(encoded.spatial_mask)[selected_indices]
    rope_groups[0, :selected_count] = _numpy(encoded.rope_groups)[selected_indices]
    token_mask[0, :selected_count] = True

    unit_indices = np.zeros((1, MAX_OWN_UNITS), dtype=np.int32)
    old_unit_indices = _numpy(encoded.own_unit_indices).astype(np.int64, copy=False)
    for output_index, old_index in enumerate(old_unit_indices[:encoded_own_units]):
        unit_indices[0, output_index] = old_to_new[int(old_index)]
    market_indices = np.asarray(
        [[old_to_new[int(old_index)] for old_index in _numpy(encoded.market_slot_indices)]],
        dtype=np.int32,
    )
    return FixedBatch(
        arrays={
            "features": features,
            "memory_features": _numpy(encoded.memory_features).astype(np.float32, copy=False)[None],
            "coordinates": coordinates,
            "spatial_mask": spatial_mask,
            "rope_groups": rope_groups,
            "token_mask": token_mask,
            "unit_indices": unit_indices,
            "market_indices": market_indices,
        },
        actual_own_units=actual_own_units,
        encoded_own_units=encoded_own_units,
    )


def dummy_fixed_batch(*, legal_mask: bool = False) -> dict[str, np.ndarray]:
    result = {
        "features": np.zeros((1, FIXED_TOKEN_COUNT, FEATURE_DIM), dtype=np.float32),
        "memory_features": np.zeros((1, len(MEMORY_FEATURE_NAMES)), dtype=np.float32),
        "coordinates": np.zeros((1, FIXED_TOKEN_COUNT, 2), dtype=np.float32),
        "spatial_mask": np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.bool_),
        "rope_groups": np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.int32),
        "token_mask": np.zeros((1, FIXED_TOKEN_COUNT), dtype=np.bool_),
        "unit_indices": np.zeros((1, MAX_OWN_UNITS), dtype=np.int32),
        "market_indices": np.zeros((1, MARKET_SLOTS), dtype=np.int32),
    }
    if legal_mask:
        result["legal_mask_stems"] = np.ones((1, MASK_STEM_SIZE), dtype=np.bool_)
    return result


def decode_unit_action(logits: np.ndarray) -> list[Any]:
    return list(UNIT_ACTIONS[int(np.argmax(logits))])


def decode_market_order(logits: np.ndarray, sellable_shed: dict[str, int]) -> list[Any] | None:
    selected = engine_market_ids(int(np.argmax(logits)), absolute=logits.shape[-1] == ABSOLUTE_ACTION_COUNT)
    return decode_engine_market_order(int(selected), sellable_shed)


class GreedyJaxPolicy:
    def __init__(self, payload: dict[str, Any], *, warm: bool = True) -> None:
        self.config = JaxModelConfig(**payload["model_config"])
        if jax.default_backend() == "cpu":
            self.config = replace(self.config, attention_backend="manual")
        self.config.validate()
        self.execution_variant = payload.get("execution_variant", "baseline")
        self.forward_options = forward_options(self.execution_variant, platform=jax.default_backend())
        self.params = jax.tree_util.tree_map(
            lambda value: jnp.asarray(value, dtype=jnp.float32)
            if jnp.issubdtype(jnp.asarray(value).dtype, jnp.floating)
            else jnp.asarray(value),
            payload["params"],
        )
        self.tracker: OpponentInventoryTracker | None = None
        self.previous_observation: dict[str, Any] | None = None
        self.previous_action: dict[str, Any] | None = None
        self.compute_dtype = (
            jnp.bfloat16 if self.config.attention_backend == "cudnn" and jax.default_backend() == "gpu" else jnp.float32
        )
        if self.compute_dtype == jnp.bfloat16:
            self.params = cast_dense_params(self.params, self.compute_dtype)

        def forward(params: dict[str, Any], batch: dict[str, jax.Array]) -> dict[str, jax.Array]:
            return policy_forward(
                params, batch, self.config, dtype=self.compute_dtype, training=False, **self.forward_options
            )

        self.forward = jax.jit(forward)
        if warm:
            warmed = self.forward(
                self.params,
                {
                    name: jnp.asarray(value)
                    for name, value in dummy_fixed_batch(
                        legal_mask=self.config.legal_mask or self.config.sequential_patch
                    ).items()
                },
            )
            jax.tree_util.tree_map(lambda value: value.block_until_ready(), warmed)

    def _inventory_estimate(self, observation: dict[str, Any]) -> InventoryEstimate:
        player = int(observation.get("player", 0))
        step = observation_step(observation)
        previous_step = observation_step(self.previous_observation) if self.previous_observation is not None else None
        reset = (
            self.tracker is None
            or self.tracker.observer_player != player
            or previous_step is None
            or step < previous_step
            or step > previous_step + 1
        )
        if reset:
            self.tracker = OpponentInventoryTracker(observer_player=player)
            return self.tracker.estimate()
        elif step == previous_step + 1:
            assert self.previous_observation is not None
            return self.tracker.update(self.previous_observation, observation, self.previous_action)
        return self.tracker.estimate()

    def __call__(self, observation: dict[str, Any]) -> dict[str, Any]:
        final_action = self.final_turn_action(observation)
        if final_action is not None:
            self.previous_observation = deepcopy(observation)
            self.previous_action = deepcopy(final_action)
            return final_action

        estimate = self._inventory_estimate(observation)
        fixed = prepare_fixed_batch(encode_observation(observation, estimate), observation)
        if self.config.legal_mask:
            fixed.arrays["legal_mask_stems"] = observation_mask_stems(observation)
        if self.config.sequential_patch:
            from kaggriculture.actions.patch_inputs import observation_patch_inputs

            fixed.arrays.update(observation_patch_inputs(observation))
        outputs = jax.device_get(
            self.forward(self.params, {name: jnp.asarray(value) for name, value in fixed.arrays.items()})
        )
        unit_actions = [
            decode_unit_action(outputs["unit_action"][0, index]) for index in range(fixed.encoded_own_units)
        ]
        if self.config.sequential_patch:
            from kaggriculture.actions.sequential import sequential_units

            unit_ids, _, _ = sequential_units(
                jnp.asarray(outputs["unit_action"]),
                jnp.asarray(fixed.arrays["legal_mask_stems"]),
                jnp.asarray(fixed.arrays["patch_context"]),
                None,
            )
            unit_actions = [
                list(UNIT_ACTIONS[int(index)]) for index in np.asarray(unit_ids)[0, : fixed.encoded_own_units]
            ]
        unit_actions.extend([["PASS"] for _ in range(fixed.actual_own_units - fixed.encoded_own_units)])
        sellable_shed = shed_after_unit_actions(observation, unit_actions)
        market = []
        for logits in outputs["market_action"][0]:
            order = decode_market_order(logits, sellable_shed)
            if order is None:
                continue
            market.append(order)
            if order[0] == "SELL":
                item = str(order[1])
                sellable_shed[item] = max(0, sellable_shed.get(item, 0) - int(order[2]))
        action = {
            "farmer": unit_actions[0],
            "hands": unit_actions[1:],
            "market": market,
        }
        if self.config.sequential_patch:
            from kaggriculture.heuristics.shed_patch import patch_action

            action = patch_action(observation, action)
        self.previous_observation = deepcopy(observation)
        self.previous_action = deepcopy(action)
        return action

    def final_turn_action(self, observation: dict[str, Any]) -> dict[str, Any] | None:
        return None if self.config.sequential_patch else final_turn_action(observation)


def load_policy(payload_path: str | Path, *, warm: bool = True) -> GreedyJaxPolicy:
    with Path(payload_path).open("rb") as source:
        payload = pickle.load(source)
    return GreedyJaxPolicy(payload, warm=warm)
