"""Pure-JAX policy/value model initialized from the source-free competition policy."""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

import jax
import jax.numpy as jnp

from kaggriculture.actions.masks import apply_action_masks, apply_unit_masks
from kaggriculture.model.partition_attention import merge_attention_partitions
from kaggriculture.actions.sell_quantity import PRODUCT_COUNT, QUANTITY_COUNT, compose_market_logits

from kaggriculture.actions.catalog import (
    MARKET_ACTIONS,
    UNIT_ACTIONS,
)
from kaggriculture.observations.features import (
    FEATURE_INDEX,
    MEMORY_PACK_FEATURE_INDICES,
    TOKEN_ADAPTER_FEATURES,
)


Array = jax.Array
Params = dict[str, Any]
LAYER_NORM_EPSILON = 1e-5
PARTITION_GROUP_TOKENS = 120
PARTITION_NONSPATIAL_TOKENS = 24
PARTITION_FIXED_TOKENS = 2 * PARTITION_GROUP_TOKENS + PARTITION_NONSPATIAL_TOKENS
GRID_MAX_COORDINATE = 9.0
VALUE_COST_DIFFERENCE_REFERENCE = 20_000.0
VALUE_MONEY_ENCODING_REFERENCE = 1_000_000.0
VALUE_HEAD_INIT_SEED = 42_042


@dataclass(frozen=True)
class JaxModelConfig:
    d_model: int = 256
    layers: int = 6
    heads: int = 8
    ffn_dim: int = 1024
    dropout: float = 0.1
    rope_dim: int = 16
    rope_base: float = 100.0
    attention_backend: str = "manual"
    rope_correction_backend: str = "dense"
    legal_mask: bool = False
    absolute_sell: bool = False
    sequential_patch: bool = False

    def validate(self) -> None:
        if self.sequential_patch and not self.absolute_sell:
            raise ValueError("sequential patch shed sales require absolute quantities")
        if self.sequential_patch and self.legal_mask:
            raise ValueError("sequential patch uses its own support, not independent legal masks")
        if self.absolute_sell and self.legal_mask:
            raise ValueError("absolute SELL currently requires the unmasked policy")
        if self.d_model % self.heads:
            raise ValueError("d_model must be divisible by heads")
        head_dim = self.d_model // self.heads
        if self.rope_dim > head_dim or self.rope_dim % 4:
            raise ValueError("rope_dim must fit in one head and be divisible by four")
        if self.rope_base <= 1.0:
            raise ValueError("rope base must be greater than one")
        if not 0.0 <= self.dropout < 1.0:
            raise ValueError("dropout must be in [0, 1)")
        if self.attention_backend not in ("manual", "cudnn"):
            raise ValueError("attention backend must be manual or cudnn")
        if self.rope_correction_backend not in ("dense", "augmented", "partitioned"):
            raise ValueError("RoPE correction backend must be dense, augmented, or partitioned")

    def to_dict(self) -> dict[str, int | float | str]:
        return {
            "d_model": self.d_model,
            "layers": self.layers,
            "heads": self.heads,
            "ffn_dim": self.ffn_dim,
            "dropout": self.dropout,
            "rope_dim": self.rope_dim,
            "rope_base": self.rope_base,
            "attention_backend": self.attention_backend,
            "rope_correction_backend": self.rope_correction_backend,
            "legal_mask": self.legal_mask,
            **({"sequential_patch": True} if self.sequential_patch else {}),
            **({"absolute_sell": True} if self.absolute_sell else {}),
        }


def init_dense(key: Array, input_dim: int, output_dim: int) -> Params:
    limit = 1.0 / math.sqrt(input_dim)
    return {
        "kernel": jax.random.uniform(
            key,
            (input_dim, output_dim),
            minval=-limit,
            maxval=limit,
            dtype=jnp.float32,
        ),
        "bias": jax.random.uniform(
            jax.random.fold_in(key, 1),
            (output_dim,),
            minval=-limit,
            maxval=limit,
            dtype=jnp.float32,
        ),
    }


def init_norm(width: int) -> Params:
    return {
        "scale": jnp.ones((width,), dtype=jnp.float32),
        "bias": jnp.zeros((width,), dtype=jnp.float32),
    }


def initialize_params(key: Array, config: JaxModelConfig) -> Params:
    config.validate()

    def next_key() -> Array:
        nonlocal key
        key, result = jax.random.split(key)
        return result

    adapters = {
        token_type: init_dense(next_key(), len(feature_names), config.d_model)
        for token_type, feature_names in TOKEN_ADAPTER_FEATURES.items()
    }
    blocks = []
    for _ in range(config.layers):
        blocks.append(
            {
                "attention_norm": init_norm(config.d_model),
                "qkv": init_dense(next_key(), config.d_model, config.d_model * 3),
                "attention_output": init_dense(next_key(), config.d_model, config.d_model),
                "ffn_norm": init_norm(config.d_model),
                "ffn_input": init_dense(next_key(), config.d_model, config.ffn_dim),
                "ffn_output": init_dense(next_key(), config.ffn_dim, config.d_model),
            }
        )
    params = {
        "adapters": adapters,
        "input_norm": init_norm(config.d_model),
        "blocks": tuple(blocks),
        "final_norm": init_norm(config.d_model),
        "unit_action": init_dense(next_key(), config.d_model, len(UNIT_ACTIONS)),
        "market_action": init_dense(next_key(), config.d_model, len(MARKET_ACTIONS)),
    }
    if config.absolute_sell:
        params["sell_quantity"] = init_dense(next_key(), config.d_model, PRODUCT_COUNT * QUANTITY_COUNT)
    return params


def add_zero_value_head(params: Params, config: JaxModelConfig) -> Params:
    """Add a GELU critic whose zero output preserves the behavior-cloned policy."""
    if "value" in params:
        return params
    return {
        **params,
        "value": {
            "hidden": init_dense(
                jax.random.PRNGKey(VALUE_HEAD_INIT_SEED),
                config.d_model,
                config.d_model,
            ),
            "output": {
                "kernel": jnp.zeros((config.d_model, 1), dtype=jnp.float32),
                "bias": jnp.zeros((1,), dtype=jnp.float32),
            },
        },
    }


def add_sell_quantity_head(params: Params, config: JaxModelConfig, seed: int) -> Params:
    if "sell_quantity" in params:
        raise ValueError("do not reinitialize an existing SELL quantity head")
    return {
        **params,
        "sell_quantity": init_dense(jax.random.PRNGKey(seed), config.d_model, PRODUCT_COUNT * QUANTITY_COUNT),
    }


def cast_dense_params(params: Params, dtype: jnp.dtype) -> Params:
    """Pre-cast dense weights while preserving FP32 LayerNorm arithmetic."""

    def cast_node(node: Any) -> Any:
        if isinstance(node, dict):
            if set(node) == {"kernel", "bias"}:
                return {name: value.astype(dtype) for name, value in node.items()}
            return {name: cast_node(value) for name, value in node.items()}
        if isinstance(node, tuple):
            return tuple(cast_node(value) for value in node)
        return node

    return cast_node(params)


def dense(inputs: Array, params: Params, dtype: jnp.dtype) -> Array:
    return jnp.matmul(inputs.astype(dtype), params["kernel"].astype(dtype)) + params["bias"].astype(dtype)


def policy_head(inputs: Array, params: Params, dtype: jnp.dtype) -> Array:
    # BF16 GEMM+BIAS fusion otherwise changes rounding between sampling and selected-log-prob graphs.
    logits = jnp.matmul(inputs.astype(dtype), params["kernel"].astype(dtype), preferred_element_type=jnp.float32)
    return logits + params["bias"].astype(jnp.float32)


def layer_norm(inputs: Array, params: Params, dtype: jnp.dtype) -> Array:
    values = inputs.astype(jnp.float32)
    mean = jnp.mean(values, axis=-1, keepdims=True)
    variance = jnp.mean(jnp.square(values - mean), axis=-1, keepdims=True)
    normalized = (values - mean) * jax.lax.rsqrt(variance + LAYER_NORM_EPSILON)
    output = normalized * params["scale"] + params["bias"]
    return output.astype(dtype)


def apply_dropout(inputs: Array, key: Array | None, rate: float, training: bool) -> Array:
    if not training or rate == 0.0:
        return inputs
    if key is None:
        raise ValueError("training with dropout requires a PRNG key")
    keep_probability = 1.0 - rate
    keep = jax.random.bernoulli(key, keep_probability, inputs.shape)
    return jnp.where(keep, inputs / keep_probability, 0.0).astype(inputs.dtype)


def rotate_axis(
    tensor: Array,
    positions: Array,
    spatial_mask: Array,
    start: int,
    width: int,
    base: float,
) -> Array:
    section = tensor[..., start : start + width]
    frequency_index = jnp.arange(0, width, 2, dtype=jnp.float32)
    inverse_frequency = 1.0 / (base ** (frequency_index / width))
    angles = positions.astype(jnp.float32)[:, None, :, None] * inverse_frequency[None, None, None, :]
    cosine = jnp.cos(angles).astype(section.dtype)
    sine = jnp.sin(angles).astype(section.dtype)
    even = section[..., 0::2]
    odd = section[..., 1::2]
    rotated = jnp.stack((even * cosine - odd * sine, even * sine + odd * cosine), axis=-1).reshape(section.shape)
    selected = jnp.where(spatial_mask[:, None, :, None], rotated, section)
    return tensor.at[..., start : start + width].set(selected)


def apply_2d_rope(
    query: Array,
    key: Array,
    coordinates: Array,
    spatial_mask: Array,
    config: JaxModelConfig,
) -> tuple[Array, Array]:
    axis_dim = config.rope_dim // 2
    x = coordinates[..., 0]
    y = coordinates[..., 1]
    query = rotate_axis(query, x, spatial_mask, 0, axis_dim, config.rope_base)
    query = rotate_axis(query, y, spatial_mask, axis_dim, axis_dim, config.rope_base)
    key = rotate_axis(key, x, spatial_mask, 0, axis_dim, config.rope_base)
    key = rotate_axis(key, y, spatial_mask, axis_dim, axis_dim, config.rope_base)
    return query, key


def dense_rope_correction(
    raw_query: Array,
    raw_key: Array,
    rotated_query: Array,
    rotated_key: Array,
    rope_groups: Array,
    rope_dim: int,
    scale: float,
) -> Array:
    raw_rotary = jnp.einsum(
        "bhtd,bhsd->bhts",
        raw_query[..., :rope_dim],
        raw_key[..., :rope_dim],
    ).astype(jnp.float32)
    rotated_rotary = jnp.einsum(
        "bhtd,bhsd->bhts",
        rotated_query[..., :rope_dim],
        rotated_key[..., :rope_dim],
    ).astype(jnp.float32)
    query_group = rope_groups[:, None, :, None]
    key_group = rope_groups[:, None, None, :]
    same_farm_pair = (query_group != 0) & (query_group == key_group)
    return jnp.where(~same_farm_pair, (raw_rotary - rotated_rotary) * scale, 0.0)


def augmented_rope_inputs(
    raw_query: Array,
    raw_key: Array,
    value: Array,
    rotated_query: Array,
    rotated_key: Array,
    rope_groups: Array,
    rope_dim: int,
) -> tuple[Array, Array, Array]:
    query_parts = [raw_query]
    key_parts = [raw_key]
    for group in (1, 2):
        group_mask = (rope_groups == group)[:, None, :, None]
        query_parts.extend(
            (
                jnp.where(group_mask, rotated_query[..., :rope_dim], 0.0),
                jnp.where(group_mask, raw_query[..., :rope_dim], 0.0),
            )
        )
        key_parts.extend(
            (
                jnp.where(group_mask, rotated_key[..., :rope_dim], 0.0),
                jnp.where(group_mask, -raw_key[..., :rope_dim], 0.0),
            )
        )
    augmented_query = jnp.concatenate(query_parts, axis=-1)
    augmented_key = jnp.concatenate(key_parts, axis=-1)
    value_padding = augmented_query.shape[-1] - value.shape[-1]
    augmented_value = jnp.pad(value, ((0, 0), (0, 0), (0, 0), (0, value_padding)))
    return augmented_query, augmented_key, augmented_value


def partitioned_cudnn_attention(
    raw_query: Array,
    raw_key: Array,
    value: Array,
    rotated_query: Array,
    rotated_key: Array,
    token_mask: Array,
    scale: float,
    *,
    merge_kernel: Callable | None = None,
) -> Array:
    """Evaluate exact selective-RoPE attention as disjoint key partitions."""
    batch = raw_query.shape[0]
    merge = merge_attention_partitions if merge_kernel is None else merge_kernel
    group = PARTITION_GROUP_TOKENS
    group_query_rotated = jnp.concatenate(
        (rotated_query[:, :, :group], rotated_query[:, :, group : 2 * group]),
        axis=0,
    )
    group_key_rotated = jnp.concatenate(
        (rotated_key[:, :, :group], rotated_key[:, :, group : 2 * group]),
        axis=0,
    )
    group_query_raw = jnp.concatenate(
        (raw_query[:, :, :group], raw_query[:, :, group : 2 * group]),
        axis=0,
    )
    group_value = jnp.concatenate(
        (value[:, :, :group], value[:, :, group : 2 * group]),
        axis=0,
    )
    opposite_key = jnp.concatenate(
        (raw_key[:, :, group : 2 * group], raw_key[:, :, :group]),
        axis=0,
    )
    opposite_value = jnp.concatenate(
        (value[:, :, group : 2 * group], value[:, :, :group]),
        axis=0,
    )
    nonspatial_key = raw_key[:, :, 2 * group :]
    nonspatial_value = value[:, :, 2 * group :]
    key_padding = group - PARTITION_NONSPATIAL_TOKENS
    nonspatial_key = jnp.pad(nonspatial_key, ((0, 0), (0, 0), (0, key_padding), (0, 0)))
    nonspatial_value = jnp.pad(nonspatial_value, ((0, 0), (0, 0), (0, key_padding), (0, 0)))
    nonspatial_key = jnp.concatenate((nonspatial_key, nonspatial_key), axis=0)
    nonspatial_value = jnp.concatenate((nonspatial_value, nonspatial_value), axis=0)

    group_lengths = jnp.concatenate(
        (
            jnp.sum(token_mask[:, :group], axis=-1, dtype=jnp.int32),
            jnp.sum(token_mask[:, group : 2 * group], axis=-1, dtype=jnp.int32),
        )
    )
    opposite_lengths = jnp.concatenate((group_lengths[batch:], group_lengths[:batch]))
    group_queries = jnp.concatenate((group_query_rotated, group_query_raw, group_query_raw), axis=0)
    group_keys = jnp.concatenate((group_key_rotated, opposite_key, nonspatial_key), axis=0)
    group_values = jnp.concatenate((group_value, opposite_value, nonspatial_value), axis=0)
    query_lengths = jnp.tile(group_lengths, 3)
    key_lengths = jnp.concatenate(
        (
            group_lengths,
            opposite_lengths,
            jnp.full((batch * 2,), PARTITION_NONSPATIAL_TOKENS, dtype=jnp.int32),
        )
    )
    group_outputs = merge(
        jnp.transpose(group_queries, (0, 2, 1, 3)),
        jnp.transpose(group_keys, (0, 2, 1, 3)),
        jnp.transpose(group_values, (0, 2, 1, 3)),
        query_lengths,
        key_lengths,
        scale,
        3,
    ).astype(value.dtype)
    group_outputs = group_outputs.reshape(2, batch, group, *group_outputs.shape[2:])
    group_outputs = jnp.concatenate((group_outputs[0], group_outputs[1]), axis=1)

    nonspatial_query = raw_query[:, :, 2 * group :]
    nonspatial_query = jnp.concatenate((nonspatial_query, nonspatial_query, nonspatial_query), axis=0)
    padded_nonspatial_key = nonspatial_key[:batch]
    padded_nonspatial_value = nonspatial_value[:batch]
    nonspatial_keys = jnp.concatenate(
        (raw_key[:, :, :group], raw_key[:, :, group : 2 * group], padded_nonspatial_key),
        axis=0,
    )
    nonspatial_values = jnp.concatenate(
        (value[:, :, :group], value[:, :, group : 2 * group], padded_nonspatial_value),
        axis=0,
    )
    nonspatial_outputs = merge(
        jnp.transpose(nonspatial_query, (0, 2, 1, 3)),
        jnp.transpose(nonspatial_keys, (0, 2, 1, 3)),
        jnp.transpose(nonspatial_values, (0, 2, 1, 3)),
        jnp.full(
            (batch * 3,),
            PARTITION_NONSPATIAL_TOKENS,
            dtype=jnp.int32,
        ),
        jnp.concatenate(
            (
                group_lengths[:batch],
                group_lengths[batch:],
                jnp.full((batch,), PARTITION_NONSPATIAL_TOKENS, dtype=jnp.int32),
            )
        ),
        scale,
        3,
    ).astype(value.dtype)
    return jnp.concatenate((group_outputs, nonspatial_outputs), axis=1)


def partition_policy_tokens(
    hidden: Array,
    coordinates: Array,
    spatial_mask: Array,
    rope_groups: Array,
    source_token_mask: Array,
) -> tuple[Array, Array, Array, Array, Array, Array, Array, int]:
    """Reorder compact observations into two fixed farm blocks plus global tokens."""
    if hidden.shape[1] != PARTITION_FIXED_TOKENS:
        raise ValueError(f"partitioned attention requires {PARTITION_FIXED_TOKENS} tokens")
    batch_size = hidden.shape[0]
    group = PARTITION_GROUP_TOKENS
    unit_slots = group - 100
    unit_offsets = jnp.arange(unit_slots, dtype=jnp.int32)[None, :]
    own_counts = jnp.sum(rope_groups == 1, axis=-1, dtype=jnp.int32) - 100
    opponent_counts = jnp.sum(rope_groups == 2, axis=-1, dtype=jnp.int32) - 100
    own_units = jnp.where(unit_offsets < own_counts[:, None], 201 + unit_offsets, 0)
    opponent_units = jnp.where(
        unit_offsets < opponent_counts[:, None],
        201 + own_counts[:, None] + unit_offsets,
        0,
    )
    self_cells = jnp.broadcast_to(jnp.arange(1, 101, dtype=jnp.int32), (batch_size, 100))
    opponent_cells = jnp.broadcast_to(jnp.arange(101, 201, dtype=jnp.int32), (batch_size, 100))
    tail_offsets = jnp.arange(PARTITION_NONSPATIAL_TOKENS - 1, dtype=jnp.int32)[None, :]
    tail = 201 + own_counts[:, None] + opponent_counts[:, None] + tail_offsets
    global_token = jnp.zeros((batch_size, 1), dtype=jnp.int32)
    indices = jnp.concatenate(
        (self_cells, own_units, opponent_cells, opponent_units, global_token, tail),
        axis=1,
    )

    def gather(values: Array) -> Array:
        gather_indices = indices.reshape((*indices.shape, *((1,) * (values.ndim - 2))))
        gather_indices = jnp.broadcast_to(gather_indices, (*indices.shape, *values.shape[2:]))
        return jnp.take_along_axis(values, gather_indices, axis=1)

    valid_units = jnp.arange(unit_slots)[None, :]
    token_mask = jnp.concatenate(
        (
            jnp.ones((batch_size, 100), dtype=jnp.bool_),
            valid_units < own_counts[:, None],
            jnp.ones((batch_size, 100), dtype=jnp.bool_),
            valid_units < opponent_counts[:, None],
            jnp.ones((batch_size, PARTITION_NONSPATIAL_TOKENS), dtype=jnp.bool_),
        ),
        axis=1,
    )
    token_mask &= gather(source_token_mask)
    hidden = gather(hidden) * token_mask[..., None].astype(hidden.dtype)
    unit_indices = jnp.where(
        valid_units < own_counts[:, None],
        jnp.arange(100, 120, dtype=jnp.int32)[None, :],
        240,
    )
    market_indices = jnp.broadcast_to(jnp.arange(254, 264, dtype=jnp.int32), (batch_size, 10))
    return (
        hidden,
        gather(coordinates),
        gather(spatial_mask),
        gather(rope_groups),
        token_mask,
        unit_indices,
        market_indices,
        240,
    )


def metadata_from_features(features: Array) -> tuple[Array, Array, Array, Array]:
    """Recover exact spatial metadata already encoded in the dense feature rows."""
    token_columns = jnp.asarray(
        [FEATURE_INDEX[f"token:{token_type}"] for token_type in TOKEN_ADAPTER_FEATURES],
        dtype=jnp.int32,
    )
    token_mask = jnp.any(jnp.take(features, token_columns, axis=-1) > 0.5, axis=-1)
    cell_mask = features[..., FEATURE_INDEX["token:CELL"]] > 0.5
    unit_mask = features[..., FEATURE_INDEX["token:UNIT"]] > 0.5
    spatial_mask = cell_mask | unit_mask
    self_mask = features[..., FEATURE_INDEX["farm:SELF"]] > 0.5
    opponent_mask = features[..., FEATURE_INDEX["farm:OPPONENT"]] > 0.5
    rope_groups = jnp.where(spatial_mask & self_mask, 1, jnp.where(spatial_mask & opponent_mask, 2, 0))
    x = features[..., FEATURE_INDEX["cell_x"]] + features[..., FEATURE_INDEX["unit_x"]]
    y = features[..., FEATURE_INDEX["cell_y"]] + features[..., FEATURE_INDEX["unit_y"]]
    coordinates = jnp.stack((x, y), axis=-1) * GRID_MAX_COORDINATE
    return coordinates, spatial_mask, rope_groups, token_mask


def own_unit_mask_from_features(features: Array) -> Array:
    """Recover the fixed policy-head mask from self Unit feature rows."""
    unit_rows = features[..., FEATURE_INDEX["token:UNIT"]] > 0.5
    self_rows = features[..., FEATURE_INDEX["farm:SELF"]] > 0.5
    unit_counts = jnp.sum(unit_rows & self_rows, axis=-1, dtype=jnp.int32)
    return jnp.arange(PARTITION_GROUP_TOKENS - 100)[None, :] < unit_counts[:, None]


def self_attention(
    hidden: Array,
    coordinates: Array,
    spatial_mask: Array,
    rope_groups: Array,
    token_mask: Array,
    params: Params,
    config: JaxModelConfig,
    dtype: jnp.dtype,
    dropout_key: Array | None,
    training: bool,
    *,
    partition_kernel: Callable | None = None,
) -> Array:
    batch, tokens, _ = hidden.shape
    head_dim = config.d_model // config.heads
    with jax.named_scope("attention_qkv"):
        qkv = dense(hidden, params["qkv"], dtype).reshape(batch, tokens, 3, config.heads, head_dim)
    query, key, value = jnp.moveaxis(qkv, 2, 0)
    query = jnp.transpose(query, (0, 2, 1, 3))
    key = jnp.transpose(key, (0, 2, 1, 3))
    value = jnp.transpose(value, (0, 2, 1, 3))
    raw_query, raw_key = query, key
    with jax.named_scope("attention_rope"):
        query, key = apply_2d_rope(query, key, coordinates, spatial_mask, config)

    scale = 1.0 / math.sqrt(head_dim)
    use_cudnn = config.attention_backend == "cudnn" and not training and jax.default_backend() == "gpu"
    if use_cudnn or partition_kernel is not None:
        if config.rope_correction_backend == "partitioned":
            with jax.named_scope("attention_rope_partitioned"):
                kernel = partitioned_cudnn_attention if partition_kernel is None else partition_kernel
                attended = kernel(
                    raw_query,
                    raw_key,
                    value,
                    query,
                    key,
                    token_mask,
                    scale,
                )
            attended = attended.reshape(batch, tokens, config.d_model)
            output = dense(attended, params["attention_output"], dtype)
            return output * token_mask[..., None].astype(dtype)
        correction = None
        if config.rope_correction_backend == "dense":
            with jax.named_scope("attention_rope_correction_dense"):
                correction = dense_rope_correction(
                    raw_query,
                    raw_key,
                    query,
                    key,
                    rope_groups,
                    config.rope_dim,
                    scale,
                ).astype(dtype)
        elif config.rope_correction_backend == "augmented":
            with jax.named_scope("attention_rope_augmented_inputs"):
                query, key, value = augmented_rope_inputs(
                    raw_query,
                    raw_key,
                    value,
                    query,
                    key,
                    rope_groups,
                    config.rope_dim,
                )
        elif config.rope_correction_backend != "partitioned":
            raise ValueError(f"unknown RoPE correction backend: {config.rope_correction_backend}")
        padding = tokens % 2
        query = jnp.pad(query, ((0, 0), (0, 0), (0, padding), (0, 0)))
        key = jnp.pad(key, ((0, 0), (0, 0), (0, padding), (0, 0)))
        value = jnp.pad(value, ((0, 0), (0, 0), (0, padding), (0, 0)))
        if correction is not None:
            # A float32 bias with BF16 q/k corrupts cuDNN backward on A30.
            correction = jnp.pad(correction, ((0, 0), (0, 0), (0, padding), (0, padding)))
        padded_token_mask = jnp.pad(token_mask, ((0, 0), (0, padding)))
        sequence_lengths = jnp.sum(padded_token_mask, axis=-1, dtype=jnp.int32)
        attention_mask = padded_token_mask[:, None, None, :] if correction is not None else None
        query = jnp.transpose(query, (0, 2, 1, 3))
        key = jnp.transpose(key, (0, 2, 1, 3))
        value = jnp.transpose(value, (0, 2, 1, 3))
        with jax.named_scope("attention_cudnn"):
            attended = jax.nn.dot_product_attention(
                query,
                key,
                value,
                bias=correction,
                mask=attention_mask,
                scale=scale,
                query_seq_lengths=sequence_lengths if correction is None else None,
                key_value_seq_lengths=sequence_lengths if correction is None else None,
                implementation="cudnn",
            )
        attended = attended[:, :tokens, :, :head_dim].reshape(batch, tokens, config.d_model)
    else:
        with jax.named_scope("attention_rope_correction_dense"):
            correction = dense_rope_correction(
                raw_query,
                raw_key,
                query,
                key,
                rope_groups,
                config.rope_dim,
                scale,
            )
        scores = jnp.einsum("bhtd,bhsd->bhts", query, key).astype(jnp.float32) * scale
        scores += correction
        scores = jnp.where(token_mask[:, None, None, :], scores, jnp.finfo(jnp.float32).min)
        attention = jax.nn.softmax(scores, axis=-1).astype(dtype)
        attention = apply_dropout(attention, dropout_key, config.dropout, training)
        attended = jnp.einsum("bhts,bhsd->bhtd", attention, value)
        attended = jnp.transpose(attended, (0, 2, 1, 3)).reshape(batch, tokens, config.d_model)
    output = dense(attended, params["attention_output"], dtype)
    return output * token_mask[..., None].astype(dtype)


def packed_memory_features(features: Array) -> Array:
    memory_rows = jnp.argmax(features[..., FEATURE_INDEX["token:MEMORY"]], axis=1)
    memory_indices = jnp.asarray(MEMORY_PACK_FEATURE_INDICES, dtype=jnp.int32)
    packed = jnp.take(features, memory_indices, axis=-1)
    return jnp.take_along_axis(packed, memory_rows[:, None, None], axis=1)[:, 0]


def typed_input_projection(params: Params, features: Array, memory_features: Array, dtype: jnp.dtype) -> Array:
    projected = jnp.zeros((*features.shape[:2], params["input_norm"]["scale"].shape[0]), dtype=dtype)
    for token_type, feature_names in TOKEN_ADAPTER_FEATURES.items():
        if token_type == "MEMORY":
            token_projection = dense(memory_features, params["adapters"][token_type], dtype)[:, None, :]
        else:
            indices = jnp.asarray([FEATURE_INDEX[name] for name in feature_names], dtype=jnp.int32)
            active_features = jnp.take(features, indices, axis=-1)
            token_projection = dense(active_features, params["adapters"][token_type], dtype)
        type_mask = features[..., FEATURE_INDEX[f"token:{token_type}"]].astype(dtype)[..., None]
        projected += token_projection * type_mask
    return projected


def policy_forward(
    params: Params,
    batch: dict[str, Array],
    config: JaxModelConfig,
    dtype: jnp.dtype = jnp.float32,
    *,
    rng: Array | None = None,
    training: bool = False,
    prune_final_tokens: bool = False,
    prune_final_queries: bool = False,
    compact_norm_backward: bool = False,
    partition_kernel: Callable | None = None,
    remat_ffn_activation: bool = False,
    selected_partition_kernel: Callable | None = None,
    return_market_features: bool = False,
    return_value_inputs: bool = False,
) -> dict[str, Array]:
    if partition_kernel is not None and (training or config.rope_correction_backend != "partitioned"):
        raise ValueError("custom partition kernels require dropout-free partitioned execution")
    if partition_kernel is not None and prune_final_queries and selected_partition_kernel is None:
        raise ValueError("custom partition kernels require a matching selected-query kernel")
    if selected_partition_kernel is not None and not prune_final_queries:
        raise ValueError("a selected-query kernel requires final-query pruning")
    if (prune_final_tokens or prune_final_queries) and training and config.dropout > 0.0:
        raise ValueError("final-token pruning requires dropout-free execution")
    if prune_final_queries and (
        training or config.attention_backend != "cudnn" or config.rope_correction_backend != "partitioned"
    ):
        raise ValueError("selected queries require dropout-free partitioned cuDNN attention")
    partitioned = config.rope_correction_backend == "partitioned"

    def normalize(values: Array, norm_params: Params) -> Array:
        if not compact_norm_backward:
            return layer_norm(values, norm_params, dtype)
        from kaggriculture.model.kernels.layer_norm import compact_layer_norm

        return compact_layer_norm(values.astype(jnp.float32), norm_params["scale"], norm_params["bias"]).astype(dtype)

    memory_features = packed_memory_features(batch["features"]) if partitioned else batch["memory_features"]
    state_projection = typed_input_projection(params, batch["features"], memory_features, dtype)
    hidden = normalize(state_projection, params["input_norm"])
    if partitioned:
        coordinates, spatial_mask, rope_groups, token_mask = metadata_from_features(batch["features"])
    else:
        coordinates = batch["coordinates"]
        spatial_mask = batch["spatial_mask"]
        rope_groups = batch["rope_groups"]
        token_mask = batch["token_mask"]
    hidden *= token_mask[..., None].astype(dtype)
    unit_indices = batch.get("unit_indices")
    market_indices = batch.get("market_indices")
    global_index = 0
    if partitioned:
        (
            hidden,
            coordinates,
            spatial_mask,
            rope_groups,
            token_mask,
            unit_indices,
            market_indices,
            global_index,
        ) = partition_policy_tokens(
            hidden,
            coordinates,
            spatial_mask,
            rope_groups,
            token_mask,
        )
    else:
        assert unit_indices is not None and market_indices is not None

    if training and config.dropout > 0.0:
        if rng is None:
            raise ValueError("training with dropout requires a PRNG key")
        dropout_keys: Array | None = jax.random.split(rng, config.layers * 3)
    else:
        dropout_keys = None

    for block_index, block in enumerate(params["blocks"]):
        attention_dropout_key = dropout_keys[block_index * 3] if dropout_keys is not None else None
        hidden_dropout_key = dropout_keys[block_index * 3 + 1] if dropout_keys is not None else None
        output_dropout_key = dropout_keys[block_index * 3 + 2] if dropout_keys is not None else None
        normalized = normalize(hidden, block["attention_norm"])
        if prune_final_queries and block_index == len(params["blocks"]) - 1:
            from kaggriculture.model.selected_attention import selected_partition_attention

            group = PARTITION_GROUP_TOKENS
            own_units = group - 100
            selected = jnp.concatenate(
                (jnp.arange(100, group), jnp.array([2 * group]), jnp.arange(254, 264), jnp.array([2 * group]))
            )
            q_params = {name: values[..., : config.d_model] for name, values in block["qkv"].items()}
            kv_params = {name: values[..., config.d_model :] for name, values in block["qkv"].items()}
            head_dim = config.d_model // config.heads
            query = (
                dense(normalized[:, selected], q_params, dtype)
                .reshape(hidden.shape[0], selected.size, config.heads, head_dim)
                .transpose(0, 2, 1, 3)
            )
            kv = dense(normalized, kv_params, dtype).reshape(
                hidden.shape[0], hidden.shape[1], 2, config.heads, head_dim
            )
            key, value = jnp.moveaxis(kv, 2, 0)
            key, value = key.transpose(0, 2, 1, 3), value.transpose(0, 2, 1, 3)
            rotated_query, _ = apply_2d_rope(query, query, coordinates[:, selected], spatial_mask[:, selected], config)
            _, rotated_key = apply_2d_rope(key, key, coordinates, spatial_mask, config)
            selected_kernel = (
                selected_partition_attention if selected_partition_kernel is None else selected_partition_kernel
            )
            attended = selected_kernel(
                query, rotated_query, key, rotated_key, value, token_mask, 1 / math.sqrt(head_dim)
            )
            token_mask = token_mask[:, selected].at[:, -1].set(False)
            hidden = hidden[:, selected] + dense(
                attended.reshape(hidden.shape[0], selected.size, config.d_model), block["attention_output"], dtype
            ) * token_mask[..., None].astype(dtype)
            unit_indices = jnp.where(unit_indices < group, jnp.arange(own_units)[None, :], own_units)
            market_indices = jnp.broadcast_to(jnp.arange(own_units + 1, own_units + 11), market_indices.shape)
            global_index = own_units
        else:
            hidden += self_attention(
                normalized,
                coordinates,
                spatial_mask,
                rope_groups,
                token_mask,
                block,
                config,
                dtype,
                attention_dropout_key,
                training,
                partition_kernel=partition_kernel,
            )
        if prune_final_tokens and not prune_final_queries and block_index == len(params["blocks"]) - 1:
            # No later attention can consume unused tokens; only the heads remain.
            selected_indices = jnp.concatenate(
                (jnp.full((hidden.shape[0], 1), global_index, dtype=jnp.int32), unit_indices, market_indices),
                axis=1,
            )
            hidden = jnp.take_along_axis(hidden, selected_indices[..., None], axis=1)
            token_mask = jnp.take_along_axis(token_mask, selected_indices, axis=1)
            unit_count, market_count = unit_indices.shape[1], market_indices.shape[1]
            unit_indices = jnp.broadcast_to(jnp.arange(1, 1 + unit_count), unit_indices.shape)
            market_indices = jnp.broadcast_to(
                jnp.arange(1 + unit_count, 1 + unit_count + market_count), market_indices.shape
            )
            global_index = 0
        with jax.named_scope("ffn"):
            normalized = normalize(hidden, block["ffn_norm"])
            activation = partial(jax.nn.gelu, approximate="none")
            if remat_ffn_activation:
                activation = jax.checkpoint(activation)
            feed_forward = activation(dense(normalized, block["ffn_input"], dtype))
            feed_forward = apply_dropout(feed_forward, hidden_dropout_key, config.dropout, training)
            feed_forward = dense(feed_forward, block["ffn_output"], dtype)
            feed_forward = apply_dropout(feed_forward, output_dropout_key, config.dropout, training)
            hidden += feed_forward * token_mask[..., None].astype(dtype)
    hidden = normalize(hidden, params["final_norm"])

    unit_indices = jnp.broadcast_to(unit_indices[..., None], (*unit_indices.shape, config.d_model))
    market_indices = jnp.broadcast_to(
        market_indices[..., None],
        (*market_indices.shape, config.d_model),
    )
    units = jnp.take_along_axis(hidden, unit_indices, axis=1)
    market = jnp.take_along_axis(hidden, market_indices, axis=1)
    outputs = {
        "unit_action": policy_head(units, params["unit_action"], dtype),
        "market_action": policy_head(market, params["market_action"], dtype),
    }
    if config.absolute_sell:
        quantity = policy_head(market, params["sell_quantity"], dtype).reshape(
            (*market.shape[:-1], PRODUCT_COUNT, QUANTITY_COUNT)
        )
        outputs["market_action"] = compose_market_logits(outputs["market_action"], quantity)
    if return_market_features:
        outputs["market_features"] = market
    if "value" in params:
        value_hidden = dense(hidden[:, global_index], params["value"]["hidden"], dtype)
        value_hidden = jax.nn.gelu(value_hidden.astype(jnp.float32), approximate=False).astype(dtype)
        value_logits = dense(value_hidden, params["value"]["output"], dtype).astype(jnp.float32)
        value_logits = value_logits[..., 0]
        if "linear_cost" in params["value"]:
            global_features = batch["features"][:, 0].astype(jnp.float32)
            money_log_scale = jnp.log1p(jnp.asarray(VALUE_MONEY_ENCODING_REFERENCE, dtype=jnp.float32))
            self_money = jnp.expm1(global_features[:, FEATURE_INDEX["self_money"]] * money_log_scale)
            opponent_money = jnp.expm1(global_features[:, FEATURE_INDEX["opponent_money"]] * money_log_scale)
            default_cost_difference = (self_money - opponent_money) / VALUE_COST_DIFFERENCE_REFERENCE
            cost_difference = batch.get("value_cost_difference", default_cost_difference).astype(jnp.float32)
            time = batch.get(
                "value_time",
                global_features[:, FEATURE_INDEX["season_progress"]],
            ).astype(jnp.float32)
            w0, w1 = params["value"]["linear_cost"].astype(jnp.float32)
            value_logits += (w0 + w1 * time) * cost_difference
            if return_value_inputs:
                outputs["value_features"] = hidden[:, global_index]
                outputs["value_cost_difference"] = cost_difference
                outputs["value_time"] = time
        outputs["value"] = value_logits
    if config.sequential_patch:
        return apply_unit_masks(outputs, batch)
    return apply_action_masks(outputs, batch) if config.legal_mask else outputs


def parameter_count(params: Params) -> int:
    return sum(int(leaf.size) for leaf in jax.tree_util.tree_leaves(params))
