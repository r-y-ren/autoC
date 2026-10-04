"""Global PPO statistics without averaging independently normalized rank losses."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

import numpy as np


def moments(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=np.float64).reshape(-1)
    if not np.isfinite(values).all():
        raise ValueError("statistics require finite samples")
    if not values.size:
        return np.zeros(3, dtype=np.float64)
    mean = values.mean()
    return np.asarray([values.size, mean, np.sum(np.square(values - mean))])


def merge_moments(rows: np.ndarray) -> tuple[float, float]:
    rows = np.asarray(rows, dtype=np.float64).reshape(-1, 3)
    if not np.isfinite(rows).all() or np.any(rows[:, 0] < 0) or np.any(rows[:, 2] < 0) or rows[:, 0].sum() <= 0:
        raise ValueError("invalid moments")
    counts, means, squared_deviations = rows.T
    count = counts.sum()
    mean = np.dot(counts, means) / count
    variance = np.sum(squared_deviations + counts * np.square(means - mean)) / count
    return float(mean), float(np.sqrt(max(variance, 0.0)))


class PPOCollectives:
    def __init__(self, processes: int, gather: Callable[[np.ndarray], np.ndarray]) -> None:
        if processes < 1:
            raise ValueError("process count must be positive")
        self.processes = processes
        self.gather = gather

    def arrays(self, values: np.ndarray) -> np.ndarray:
        # Transport bytes so JAX's x64 setting cannot silently truncate host statistics.
        values = np.ascontiguousarray(values)
        packed = np.asarray(self.gather(values.view(np.uint8).reshape(-1)), dtype=np.uint8)
        return packed.reshape(-1).view(values.dtype).reshape(self.processes, *values.shape)

    def statistics(self, values: np.ndarray) -> tuple[np.float32, np.float32]:
        return self.statistics_batch([values])[0]

    def statistics_batch(self, groups: list[np.ndarray]) -> list[tuple[np.float32, np.float32]]:
        """Merge every group's moments through one gather; identical to per-group statistics."""
        if not groups:
            return []
        gathered = self.arrays(np.asarray([moments(values) for values in groups], dtype=np.float64))
        return [
            tuple(np.float32(value) for value in merge_moments(gathered[:, index, :])) for index in range(len(groups))
        ]

    def all_true(self, value: bool) -> bool:
        return bool(self.arrays(np.asarray([value])).all())

    def maximum(self, value: float) -> float:
        return float(self.arrays(np.asarray([value], dtype=np.float64)).max())

    def metric_rows(
        self, rows: list[dict[str, Any]], counts: list[int]
    ) -> tuple[list[dict[str, np.ndarray]], list[int]]:
        names = sorted(rows[0])
        if isinstance(rows[0][names[0]], np.ndarray):
            packed = np.asarray([[row[name] for name in names] for row in rows])
        else:
            import jax
            import jax.numpy as jnp

            # One packed transfer replaces tens of thousands of individually synchronized scalar reads.
            device_metrics = jnp.stack([jnp.stack([row[name] for row in rows]) for name in names])
            packed = np.swapaxes(np.asarray(jax.device_get(device_metrics)), 0, 1)
        lengths = self.arrays(np.asarray([len(rows)], dtype=np.int64)).reshape(-1)
        maximum = int(lengths.max())
        packed = np.pad(packed, [(0, maximum - len(rows))] + [(0, 0)] * (packed.ndim - 1))
        counts_array = self.arrays(np.pad(np.asarray(counts, dtype=np.int64), (0, maximum - len(rows))))
        gathered = self.arrays(packed)
        merged = [
            {name: gathered[rank, step, index].reshape(-1) for index, name in enumerate(names)}
            for rank in range(self.processes)
            for step in range(maximum)
        ]
        return merged, counts_array.reshape(-1).tolist()
