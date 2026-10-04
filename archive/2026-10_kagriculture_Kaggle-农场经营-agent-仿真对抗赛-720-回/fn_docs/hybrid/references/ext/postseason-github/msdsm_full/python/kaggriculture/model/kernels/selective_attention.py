"""Experimental tiled selective RoPE, including all five input cotangents.

The two 120-token farms are addressed as virtual 128-token groups so each tile
uses either raw or rotated Q/K, without materializing three attention partitions.
This computes the unquantized global softmax, not bitwise cuDNN partition merging.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
from typing import Any

import jax
import jax.numpy as jnp
from jax.experimental import pallas as pl
from jax.experimental.pallas import triton as plt

Array = jax.Array
FARM_TOKENS = 120
NONSPATIAL_TOKENS = 24
FARM_STRIDE = 128
FARM_PADDING = FARM_STRIDE - FARM_TOKENS
TOKENS = 2 * FARM_TOKENS + NONSPATIAL_TOKENS
SPATIAL_VIRTUAL_TOKENS = 2 * FARM_STRIDE
VALID_VIRTUAL_TOKENS = SPATIAL_VIRTUAL_TOKENS + NONSPATIAL_TOKENS
VIRTUAL_TOKENS = SPATIAL_VIRTUAL_TOKENS + 32
SELECTED_UNITS = 20
SELECTED_TOKENS = 32


def _positions(tile: Array, block: int) -> tuple[Array, Array]:
    virtual = tile * block + jnp.arange(block)
    physical = virtual - (virtual // FARM_STRIDE) * FARM_PADDING
    valid = jnp.where(
        virtual < SPATIAL_VIRTUAL_TOKENS, virtual % FARM_STRIDE < FARM_TOKENS, virtual < VALID_VIRTUAL_TOKENS
    )
    return physical, valid


def _query_tiles(block: int, selected: bool) -> int:
    return (
        pl.cdiv(SELECTED_UNITS, block) + pl.cdiv(SELECTED_TOKENS - SELECTED_UNITS, block)
        if selected
        else pl.cdiv(VIRTUAL_TOKENS, block)
    )


def _query_positions(tile: Array, block: int, selected: bool) -> tuple[Array, Array, Array]:
    if not selected:
        rows, valid = _positions(tile, block)
        return rows, valid, tile * block // FARM_STRIDE
    unit_tiles = pl.cdiv(SELECTED_UNITS, block)
    own = tile < unit_tiles
    rows = jnp.where(own, tile * block, SELECTED_UNITS + (tile - unit_tiles) * block) + jnp.arange(block)
    # Pallas 0.11.1 select lowering coerces two weak scalar branches to the predicate dtype.
    limit = jnp.where(own, jnp.int32(SELECTED_UNITS), jnp.int32(SELECTED_TOKENS))
    group = jnp.where(own, jnp.int32(0), jnp.int32(2))
    return rows, rows < limit, group


def _query_valid(mask: Any, rows: Array, physical_valid: Array, selected: bool) -> Array:
    if not selected:
        return physical_valid & plt.load(mask.at[rows], mask=physical_valid, other=False)
    valid = physical_valid & (rows < SELECTED_TOKENS - 1)
    positions = jnp.where(rows < SELECTED_UNITS, 100 + rows, jnp.where(rows == SELECTED_UNITS, 240, 254 + rows - 21))
    return valid & plt.load(mask.at[positions], mask=valid, other=False)


def _load(ref: Any, rows: Array, valid: Array) -> Array:
    return plt.load(ref.at[rows[:, None], jnp.arange(ref.shape[-1])[None, :]], mask=valid[:, None], other=0)


def _store(ref: Any, rows: Array, valid: Array, values: Array) -> None:
    plt.store(ref.at[rows[:, None], jnp.arange(ref.shape[-1])[None, :]], values.astype(ref.dtype), mask=valid[:, None])


def _dot(left: Array, right: Array) -> Array:
    return plt.dot(left, right, precision=jax.lax.Precision.HIGHEST)


def _forward_kernel(
    q: Any, k: Any, v: Any, rq: Any, rk: Any, mask: Any, out: Any, lse: Any, *, scale: float, block: int, selected: bool
) -> None:
    tile = pl.program_id(0)
    rows, physical_valid, query_group = _query_positions(tile, block, selected)
    valid = _query_valid(mask, rows, physical_valid, selected)
    query, rotated_query = _load(q, rows, valid), _load(rq, rows, valid)

    def body(key_tile: Array, carry: tuple) -> tuple:
        maximum, denominator, accumulated = carry
        columns, key_valid = _positions(key_tile, block)
        key_valid &= plt.load(mask.at[columns], mask=key_valid, other=False)
        same = (query_group == key_tile * block // FARM_STRIDE) & (query_group < 2)
        key = _load(k, columns, key_valid & ~same) + _load(rk, columns, key_valid & same)
        scores = _dot(jnp.where(same, rotated_query, query), key.T) * scale
        scores = jnp.where(key_valid[None, :], scores, -jnp.inf)
        next_maximum = jnp.maximum(maximum, jnp.max(scores, axis=1))
        safe_maximum = jnp.where(jnp.isfinite(next_maximum), next_maximum, 0)
        correction = jnp.exp(maximum - safe_maximum)
        probability = jnp.exp(scores - safe_maximum[:, None])
        values = _load(v, columns, key_valid)
        return (
            next_maximum,
            denominator * correction + jnp.sum(probability, axis=1),
            accumulated * correction[:, None] + _dot(probability.astype(v.dtype), values),
        )

    maximum, denominator, accumulated = jax.lax.fori_loop(
        0,
        pl.cdiv(VIRTUAL_TOKENS, block),
        body,
        (
            jnp.full((block,), -jnp.inf, jnp.float32),
            jnp.zeros((block,), jnp.float32),
            jnp.zeros((block, q.shape[-1]), jnp.float32),
        ),
    )
    result = accumulated / jnp.maximum(denominator[:, None], 1)
    # Masked real tokens must be written too; virtual padding must never alias a real token.
    _store(out, rows, physical_valid, jnp.where(valid[:, None], result, 0))
    statistics = jnp.where(valid & (denominator > 0), maximum + jnp.log(denominator), jnp.inf)
    plt.store(lse.at[rows], statistics, mask=physical_valid)


def _dq_kernel(
    q: Any,
    k: Any,
    v: Any,
    rq: Any,
    rk: Any,
    mask: Any,
    out: Any,
    lse: Any,
    dout: Any,
    dq: Any,
    drq: Any,
    *,
    scale: float,
    block: int,
    precompute_delta: bool,
    selected: bool,
) -> None:
    tile = pl.program_id(0)
    rows, physical_valid, query_group = _query_positions(tile, block, selected)
    valid = _query_valid(mask, rows, physical_valid, selected)
    query, rotated_query = _load(q, rows, valid), _load(rq, rows, valid)
    upstream = _load(dout, rows, valid)
    if precompute_delta:
        delta = plt.load(out.at[rows], mask=valid, other=0)
    else:
        delta = jnp.sum(_load(out, rows, valid).astype(jnp.float32) * upstream.astype(jnp.float32), axis=1)
    statistics = plt.load(lse.at[rows], mask=valid, other=jnp.inf)

    def body(key_tile: Array, carry: tuple) -> tuple:
        raw_gradient, rotated_gradient = carry
        columns, key_valid = _positions(key_tile, block)
        key_valid &= plt.load(mask.at[columns], mask=key_valid, other=False)
        same = (query_group == key_tile * block // FARM_STRIDE) & (query_group < 2)
        key = _load(k, columns, key_valid & ~same) + _load(rk, columns, key_valid & same)
        scores = _dot(jnp.where(same, rotated_query, query), key.T) * scale
        probability = jnp.where(key_valid[None, :] & valid[:, None], jnp.exp(scores - statistics[:, None]), 0)
        dp = _dot(upstream.astype(v.dtype), _load(v, columns, key_valid).T)
        ds = (probability * (dp - delta[:, None]) * scale).astype(k.dtype)
        gradient = _dot(ds, key)
        return raw_gradient + jnp.where(same, 0, gradient), rotated_gradient + jnp.where(same, gradient, 0)

    gradients = jax.lax.fori_loop(
        0, pl.cdiv(VIRTUAL_TOKENS, block), body, (jnp.zeros((block, q.shape[-1]), jnp.float32),) * 2
    )
    _store(dq, rows, physical_valid, gradients[0])
    _store(drq, rows, physical_valid, gradients[1])


def _dkv_kernel(
    q: Any,
    k: Any,
    v: Any,
    rq: Any,
    rk: Any,
    mask: Any,
    out: Any,
    lse: Any,
    dout: Any,
    dk: Any,
    drk: Any,
    dv: Any,
    *,
    scale: float,
    block: int,
    precompute_delta: bool,
    selected: bool,
) -> None:
    tile = pl.program_id(0)
    columns, valid = _positions(tile, block)
    valid &= plt.load(mask.at[columns], mask=valid, other=False)
    key, rotated_key, values = _load(k, columns, valid), _load(rk, columns, valid), _load(v, columns, valid)

    def body(query_tile: Array, carry: tuple) -> tuple:
        raw_gradient, rotated_gradient, value_gradient = carry
        rows, physical_valid, query_group = _query_positions(query_tile, block, selected)
        query_valid = _query_valid(mask, rows, physical_valid, selected)
        same = (tile * block // FARM_STRIDE == query_group) & (query_group < 2)
        query = _load(q, rows, query_valid & ~same) + _load(rq, rows, query_valid & same)
        upstream = _load(dout, rows, query_valid)
        if precompute_delta:
            delta = plt.load(out.at[rows], mask=query_valid, other=0)
        else:
            delta = jnp.sum(_load(out, rows, query_valid).astype(jnp.float32) * upstream.astype(jnp.float32), axis=1)
        statistics = plt.load(lse.at[rows], mask=query_valid, other=jnp.inf)
        scores = _dot(query, jnp.where(same, rotated_key, key).T) * scale
        probability = jnp.where(query_valid[:, None] & valid[None, :], jnp.exp(scores - statistics[:, None]), 0)
        dp = _dot(upstream.astype(v.dtype), values.T)
        ds = (probability * (dp - delta[:, None]) * scale).astype(q.dtype)
        gradient = _dot(ds.T, query)
        return (
            raw_gradient + jnp.where(same, 0, gradient),
            rotated_gradient + jnp.where(same, gradient, 0),
            value_gradient + _dot(probability.T.astype(q.dtype), upstream.astype(q.dtype)),
        )

    gradients = jax.lax.fori_loop(
        0, _query_tiles(block, selected), body, (jnp.zeros((block, q.shape[-1]), jnp.float32),) * 3
    )
    _, physical_valid = _positions(tile, block)
    for ref, gradient in zip((dk, drk, dv), gradients, strict=True):
        _store(ref, columns, physical_valid, gradient)


def _specs(shape: tuple[int, ...]) -> tuple[pl.BlockSpec, pl.BlockSpec]:
    tensor = pl.BlockSpec((None, None, shape[2], shape[3]), lambda tile, batch, head: (batch, head, 0, 0))
    mask = pl.BlockSpec((None, TOKENS), lambda tile, batch, head: (batch, 0))
    return tensor, mask


def _forward(
    q: Array,
    k: Array,
    v: Array,
    rq: Array,
    rk: Array,
    mask: Array,
    scale: float,
    block: int,
    interpret: bool,
    precompute_delta: bool,
    compact_upstream: bool,
    backward_warps: int,
    num_stages: int,
    selected: bool,
) -> tuple[Array, tuple]:
    tensor_spec, mask_spec = _specs(q.shape)
    key_spec, _ = _specs(k.shape)
    statistics_spec = pl.BlockSpec((None, None, q.shape[2]), lambda tile, batch, head: (batch, head, 0))
    out, statistics = pl.pallas_call(
        partial(_forward_kernel, scale=scale, block=block, selected=selected),
        out_shape=(jax.ShapeDtypeStruct(q.shape, jnp.float32), jax.ShapeDtypeStruct(q.shape[:-1], jnp.float32)),
        grid=(_query_tiles(block, selected), q.shape[0], q.shape[1]),
        in_specs=(tensor_spec, key_spec, key_spec, tensor_spec, key_spec, mask_spec),
        out_specs=(tensor_spec, statistics_spec),
        compiler_params=plt.CompilerParams(num_warps=8 if block == 128 else 4, num_stages=num_stages),
        interpret=interpret,
        name="selective_rope_forward",
    )(q, k, v, rq, rk, mask)
    return out, (q, k, v, rq, rk, mask, out, statistics)


@partial(jax.custom_vjp, nondiff_argnums=(6, 7, 8, 9, 10, 11, 12, 13))
def _attention(
    q: Array,
    k: Array,
    v: Array,
    rq: Array,
    rk: Array,
    mask: Array,
    scale: float,
    block: int,
    interpret: bool,
    precompute_delta: bool,
    compact_upstream: bool,
    backward_warps: int,
    num_stages: int,
    selected: bool,
) -> Array:
    return _forward(
        q,
        k,
        v,
        rq,
        rk,
        mask,
        scale,
        block,
        interpret,
        precompute_delta,
        compact_upstream,
        backward_warps,
        num_stages,
        selected,
    )[0]


def _backward(
    scale: float,
    block: int,
    interpret: bool,
    precompute_delta: bool,
    compact_upstream: bool,
    backward_warps: int,
    num_stages: int,
    selected: bool,
    residuals: tuple,
    dout: Array,
) -> tuple:
    q, k, v, rq, rk, mask, out, statistics = residuals
    tensor_spec, mask_spec = _specs(q.shape)
    key_spec, _ = _specs(k.shape)
    statistics_spec = pl.BlockSpec((None, None, q.shape[2]), lambda tile, batch, head: (batch, head, 0))
    delta_or_output = jnp.sum(out * dout.astype(jnp.float32), axis=-1) if precompute_delta else out
    # Delta needs full precision; all remaining uses already cast dO for tensor-core dots.
    if compact_upstream:
        dout = dout.astype(q.dtype)
    input_specs = (
        tensor_spec,
        key_spec,
        key_spec,
        tensor_spec,
        key_spec,
        mask_spec,
        statistics_spec if precompute_delta else tensor_spec,
        statistics_spec,
        tensor_spec,
    )
    inputs = (q, k, v, rq, rk, mask, delta_or_output, statistics, dout)

    def launch(kernel: Callable, count: int) -> tuple:
        shape, output_spec = (q.shape, tensor_spec) if count == 2 else (k.shape, key_spec)
        tiles = _query_tiles(block, selected) if count == 2 else pl.cdiv(VIRTUAL_TOKENS, block)
        return pl.pallas_call(
            partial(kernel, scale=scale, block=block, precompute_delta=precompute_delta, selected=selected),
            out_shape=tuple(jax.ShapeDtypeStruct(shape, q.dtype) for _ in range(count)),
            grid=(tiles, q.shape[0], q.shape[1]),
            in_specs=input_specs,
            out_specs=(output_spec,) * count,
            compiler_params=plt.CompilerParams(
                num_warps=backward_warps or (8 if block == 128 else 4), num_stages=num_stages
            ),
            interpret=interpret,
            name=f"selective_rope_{'dq' if count == 2 else 'dkv'}",
        )(*inputs)

    dq, drq = launch(_dq_kernel, 2)
    dk, drk, dv = launch(_dkv_kernel, 3)
    return dq, dk, dv, drq, drk, None


_attention.defvjp(_forward, _backward)


def fused_selective_attention(
    q: Array,
    k: Array,
    v: Array,
    rq: Array,
    rk: Array,
    mask: Array,
    scale: float,
    *,
    block: int = 32,
    interpret: bool = False,
    precompute_delta: bool = False,
    compact_upstream: bool = False,
    backward_warps: int = 0,
    num_stages: int = 2,
    selected_queries: bool = False,
) -> Array:
    query_count = SELECTED_TOKENS if selected_queries else TOKENS
    if block not in (16, 32, 64, 128) or q.shape[2] != query_count or k.shape[2] != TOKENS:
        raise ValueError("selective kernel requires 264 keys, 264 or 32 queries, and a 16/32/64/128 tile")
    if (
        rq.shape != q.shape
        or any(array.shape != k.shape for array in (v, rk))
        or (q.shape[:2], q.shape[-1]) != (k.shape[:2], k.shape[-1])
    ):
        raise ValueError("incompatible Q/K/V and rotated Q/K shapes")
    if any(array.dtype != q.dtype for array in (k, v, rq, rk)):
        raise ValueError("Q/K/V and rotated Q/K must have matching dtypes")
    if q.shape[-1] not in (16, 32, 64) or mask.shape != (q.shape[0], TOKENS):
        raise ValueError("invalid head width or token mask")
    if compact_upstream and not precompute_delta:
        raise ValueError("compute the FP32 delta before compacting the upstream cotangent")
    if backward_warps not in (0, 2, 4, 8):
        raise ValueError("backward warps must be 0 (automatic), 2, 4 or 8")
    if num_stages not in (1, 2, 3, 4):
        raise ValueError("pipeline stages must be 1, 2, 3 or 4")
    return _attention(
        q,
        k,
        v,
        rq,
        rk,
        mask,
        scale,
        block,
        interpret,
        precompute_delta,
        compact_upstream,
        backward_warps,
        num_stages,
        selected_queries,
    ).transpose(0, 2, 1, 3)


def fused_selected_attention(
    q: Array, rq: Array, k: Array, rk: Array, v: Array, mask: Array, scale: float, **options: Any
) -> Array:
    return fused_selective_attention(q, k, v, rq, rk, mask, scale, selected_queries=True, **options)
