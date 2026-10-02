"""Bound inference memory without splitting a game's trajectory or changing PPO batches."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import jax
import numpy as np


class ChunkedSampler:
    requires_host_batch = True

    def __init__(self, sampler: Callable, *, rows: int, batch_size: int) -> None:
        devices = getattr(sampler, "data_parallel_device_count", 1)
        if rows < 2 or rows % (2 * devices) or batch_size < 2 or batch_size % (2 * devices):
            raise ValueError("rollout chunks must preserve complete device-local seat pairs")
        if batch_size >= rows:
            raise ValueError("unchunked rollouts must use the original sampler")
        self.sampler = sampler
        self.data_parallel_device_count = devices
        self.rows = rows
        self.chunks = [slice(start, min(start + batch_size, rows)) for start in range(0, rows, batch_size)]
        self.padding = [
            None if part.stop - part.start == batch_size else np.resize(np.arange(part.stop - part.start), batch_size)
            for part in self.chunks
        ]
        self.outputs: list[np.ndarray] | None = None

    def prepare_keys(self, key: jax.Array, steps: int) -> list[tuple] | None:
        prepare = getattr(self.sampler, "prepare_keys", None)
        if prepare is None:
            return None
        count = len(self.chunks)
        keys = prepare(key, steps * count)
        return [tuple(keys[start : start + count]) for start in range(0, len(keys), count)]

    def __call__(self, params: Any, batch: dict[str, np.ndarray], key: Any) -> tuple:
        if batch["features"].shape[0] != self.rows:
            raise ValueError("chunked sampler row count differs from its reusable buffers")
        prepared = isinstance(key, tuple)
        for index, (part, padding) in enumerate(zip(self.chunks, self.padding, strict=True)):
            view = {name: values[part] for name, values in batch.items()}
            if padding is not None:
                view = {name: values[padding] for name, values in view.items()}
            with jax.profiler.TraceAnnotation("rollout_inference_chunk"):
                next_key, *sampled = self.sampler(params, view, key[index] if prepared else key)
                # Finish each chunk before dispatching another to bound live GPU activations.
                host_outputs = jax.device_get(sampled)
            if self.outputs is None:
                self.outputs = [np.empty((self.rows, *value.shape[1:]), dtype=value.dtype) for value in host_outputs]
            count = part.stop - part.start
            for destination, values in zip(self.outputs, host_outputs, strict=True):
                destination[part] = values[:count]
            if not prepared:
                key = next_key
        return next_key, *self.outputs
