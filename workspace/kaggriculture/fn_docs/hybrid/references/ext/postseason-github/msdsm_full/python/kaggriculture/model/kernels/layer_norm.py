"""Matched LayerNorm forward with an explicitly grouped backward candidate."""

from __future__ import annotations

import jax
import jax.numpy as jnp


def forward(values: jax.Array, scale: jax.Array, bias: jax.Array) -> tuple[jax.Array, tuple]:
    centered = values - jnp.mean(values, axis=-1, keepdims=True)
    reciprocal = jax.lax.rsqrt(jnp.mean(jnp.square(centered), axis=-1, keepdims=True) + 1e-5)
    normalized = centered * reciprocal
    return normalized * scale + bias, (normalized, reciprocal, scale)


@jax.custom_vjp
def compact_layer_norm(values: jax.Array, scale: jax.Array, bias: jax.Array) -> jax.Array:
    return forward(values, scale, bias)[0]


def backward(residuals: tuple, cotangent: jax.Array) -> tuple[jax.Array, jax.Array, jax.Array]:
    normalized, reciprocal, scale = residuals
    weighted = cotangent * scale
    projected = jnp.mean(weighted * normalized, axis=-1, keepdims=True)
    centered = weighted - normalized * projected
    # Center the final derivative too: the FP32 normalized mean need not be exactly zero.
    inputs = reciprocal * (centered - jnp.mean(centered, axis=-1, keepdims=True))
    axes = tuple(range(cotangent.ndim - 1))
    return inputs, jnp.sum(cotangent * normalized, axis=axes), jnp.sum(cotangent, axis=axes)


compact_layer_norm.defvjp(forward, backward)
