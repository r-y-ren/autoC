"""Prepare the unchanged pmap PRNG chain with a single host transfer per rollout."""

from __future__ import annotations

from dataclasses import dataclass
from functools import partial

import jax
import numpy as np


@dataclass(frozen=True)
class PreparedSamplerKey:
    next_key: np.ndarray
    replica_keys: np.ndarray


@partial(jax.jit, static_argnames=("steps", "replicas"))
def _key_chain(key: jax.Array, *, steps: int, replicas: int) -> tuple[jax.Array, jax.Array]:
    def advance(current: jax.Array, unused: None) -> tuple[jax.Array, tuple[jax.Array, jax.Array]]:
        next_key, parallel_key = jax.random.split(current)
        return next_key, (next_key, jax.random.split(parallel_key, replicas))

    _, keys = jax.lax.scan(advance, key, None, length=steps)
    return keys


def prepare_sampler_keys(key: jax.Array, *, steps: int, replicas: int) -> list[PreparedSamplerKey]:
    if steps < 1 or replicas < 1:
        raise ValueError("steps and replicas must be positive")
    if key.shape != (2,) or key.dtype != np.uint32 or str(jax.random.key_impl(key)) != "threefry2x32":
        raise ValueError("parallel rollout requires a legacy Threefry PRNGKey")
    next_keys, replica_keys = _key_chain(key, steps=steps, replicas=replicas)
    host_next, host_replicas = jax.device_get((jax.random.key_data(next_keys), jax.random.key_data(replica_keys)))
    return [PreparedSamplerKey(first, second) for first, second in zip(host_next, host_replicas, strict=True)]
