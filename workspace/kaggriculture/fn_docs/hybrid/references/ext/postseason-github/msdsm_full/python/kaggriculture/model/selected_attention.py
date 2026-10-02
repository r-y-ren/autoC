"""Final-layer attention for policy/value queries, retaining all key/value gradients."""

from __future__ import annotations

import jax
import jax.numpy as jnp

from kaggriculture.model.partition_attention import merge_attention_partitions


def selected_partition_attention(
    raw_query: jax.Array,
    rotated_query: jax.Array,
    raw_key: jax.Array,
    rotated_key: jax.Array,
    value: jax.Array,
    token_mask: jax.Array,
    scale: float,
    *,
    group: int = 120,
    units: int = 20,
    nonspatial: int = 24,
) -> jax.Array:
    batch = raw_query.shape[0]
    lengths = jnp.stack(
        (jnp.sum(token_mask[:, :group], axis=-1), jnp.sum(token_mask[:, group : 2 * group], axis=-1)),
    ).astype(jnp.int32)
    nonspatial_key = jnp.pad(raw_key[:, :, 2 * group :], ((0, 0), (0, 0), (0, group - nonspatial), (0, 0)))
    nonspatial_value = jnp.pad(value[:, :, 2 * group :], ((0, 0), (0, 0), (0, group - nonspatial), (0, 0)))
    key_lengths = jnp.concatenate((lengths[0], lengths[1], jnp.full(batch, nonspatial, jnp.int32)))
    values = jnp.concatenate((value[:, :, :group], value[:, :, group : 2 * group], nonspatial_value))

    def attend(queries: jax.Array, keys: jax.Array, query_lengths: jax.Array) -> jax.Array:
        return merge_attention_partitions(
            queries.transpose(0, 2, 1, 3),
            keys.transpose(0, 2, 1, 3),
            values.transpose(0, 2, 1, 3),
            jnp.tile(query_lengths, 3),
            key_lengths,
            scale,
            3,
        ).astype(value.dtype)

    unit_queries = jnp.concatenate((rotated_query[:, :, :units], raw_query[:, :, :units], raw_query[:, :, :units]))
    unit_keys = jnp.concatenate((rotated_key[:, :, :group], raw_key[:, :, group : 2 * group], nonspatial_key))
    own_counts = lengths[0] - (group - units)
    unit_output = attend(unit_queries, unit_keys, own_counts)
    nonspatial_queries = jnp.tile(raw_query[:, :, units:], (3, 1, 1, 1))
    nonspatial_keys = jnp.concatenate((raw_key[:, :, :group], raw_key[:, :, group : 2 * group], nonspatial_key))
    # The final dummy query keeps the cuDNN sequence extent even without entering any head.
    query_count = raw_query.shape[2] - units - 1
    other_output = attend(nonspatial_queries, nonspatial_keys, jnp.full(batch, query_count, jnp.int32))
    return jnp.concatenate((unit_output, other_output), axis=1)
