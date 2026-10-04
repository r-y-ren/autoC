"""Selective-attention merging with the complete Q/K/V backward on pinned cuDNN."""

from __future__ import annotations

from functools import partial
from typing import Any

import jax
import jax.numpy as jnp

Array = jax.Array
SUPPORTED_JAX_VERSION = "0.11.1"


def combine_partition_attention(outputs: Array, residuals: Array, query_mask: Array | None = None) -> Array:
    residuals = residuals.astype(jnp.float32)
    if query_mask is not None:
        residuals = jnp.where(query_mask[None, :, :, None], residuals, -jnp.inf)
    maximum = jnp.max(residuals, axis=0)
    valid = jnp.isfinite(maximum)
    safe_maximum = jnp.where(valid, maximum, 0.0)
    weights = jnp.where(valid[None, ...], jnp.exp(residuals - safe_maximum[None, ...]), 0.0)
    denominator = jnp.sum(weights, axis=0)
    safe_outputs = jnp.where(valid[None, ..., None], outputs.astype(jnp.float32), 0.0)
    return jnp.sum(safe_outputs * weights[..., None], axis=0) / jnp.maximum(denominator[..., None], 1.0)


def _cudnn() -> Any:
    # Backward consumes cuDNN's FP32 softmax statistics, not the public BF16 copy.
    if jax.__version__ != SUPPORTED_JAX_VERSION:
        raise RuntimeError(f"partition attention backward requires audited JAX {SUPPORTED_JAX_VERSION}")
    from jax._src.cudnn import fused_attention_stablehlo

    return fused_attention_stablehlo


def _merge_forward(
    query: Array,
    key: Array,
    value: Array,
    query_lengths: Array,
    key_lengths: Array,
    scale: float,
    partitions: int,
    *,
    preserve_residual_precision: bool = False,
) -> tuple[Array, tuple]:
    if partitions <= 0 or query.shape[0] % partitions:
        raise ValueError("batch must contain a positive number of equal attention partitions")
    fused = _cudnn()
    outputs, statistics = fused.dot_product_attention(
        query,
        key,
        value,
        q_seqlen=query_lengths,
        kv_seqlen=key_lengths,
        scale=scale,
        mask_type=fused.MaskType.PADDING,
        return_residual=True,
    )
    batch = query.shape[0] // partitions
    length = query.shape[1]
    # Preserve the existing forward's public-JAX residual quantization exactly.
    residuals = statistics.transpose(0, 2, 1)
    if not preserve_residual_precision:
        residuals = residuals.astype(outputs.dtype)
    residuals = residuals.reshape(partitions, batch, length, query.shape[2])
    query_mask = jnp.arange(length)[None, :] < query_lengths[:batch, None]
    combined = combine_partition_attention(
        outputs.reshape(partitions, batch, *outputs.shape[1:]), residuals, query_mask
    )
    weights = jax.nn.softmax(residuals.astype(jnp.float32), axis=0)
    weights = jnp.where(query_mask[None, :, :, None], weights, 0.0)
    return combined, (query, key, value, query_lengths, key_lengths, statistics, combined, weights)


@partial(jax.custom_vjp, nondiff_argnums=(5, 6))
def merge_attention_partitions(
    query: Array,
    key: Array,
    value: Array,
    query_lengths: Array,
    key_lengths: Array,
    scale: float,
    partitions: int,
) -> Array:
    """Merge partition-major BTNH attention; corresponding queries share lengths."""
    return _merge_forward(query, key, value, query_lengths, key_lengths, scale, partitions)[0]


def _merge_backward(scale: float, partitions: int, residuals: tuple, cotangent: Array) -> tuple:
    query, key, value, query_lengths, key_lengths, statistics, combined, weights = residuals
    fused = _cudnn()
    local_cotangent = (weights[..., None] * cotangent[None]).reshape(query.shape).astype(query.dtype)
    global_output = jnp.broadcast_to(combined[None], (partitions, *combined.shape))
    global_output = global_output.reshape(query.shape).astype(query.dtype)
    unused = jnp.zeros((0,), dtype=query.dtype)
    # cuDNN computes dS=P*(dO.V - dO.O). Using the merged O with alpha*dO
    # adds alpha*P*dO.(O_local-O_merged), exactly the missing LSE-gradient term.
    gradients = fused._dot_product_attention_bwd_p_wrapper.bind(
        query,
        key,
        value,
        unused,
        query_lengths,
        key_lengths,
        unused,
        unused,
        unused,
        unused,
        statistics,
        global_output,
        local_cotangent,
        scale=scale,
        seed=42,
        dropout_rate=0.0,
        variadic_args=(False, False),
        mask_type=fused.MaskType.PADDING,
        layout=fused.AttentionLayout.BTNH.value,
        sliding_window_length=None,
    )
    return (*gradients, None, None)


merge_attention_partitions.defvjp(_merge_forward, _merge_backward)
