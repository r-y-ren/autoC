"""Reject oversized GPU executables before dispatching any collective participants."""

from __future__ import annotations

import json
from typing import Any

import jax


def memory_snapshot(devices: tuple) -> list[dict[str, int]]:
    fields = ("bytes_in_use", "peak_bytes_in_use", "bytes_limit", "largest_free_block_bytes")
    return [
        {"device_id": device.id, **{key: value for key, value in device.memory_stats().items() if key in fields}}
        for device in devices
        if device.platform == "gpu"
    ]


def executable_bytes(analysis: Any) -> int:
    return (
        analysis.argument_size_in_bytes
        + analysis.output_size_in_bytes
        + analysis.temp_size_in_bytes
        - analysis.alias_size_in_bytes
    )


def guarded_dispatch(compiled: Any, devices: tuple, fraction: float) -> Any:
    if not 0 < fraction < 1:
        raise ValueError("GPU executable budget must leave a memory reserve")
    limits = [device.memory_stats()["bytes_limit"] for device in devices if device.platform == "gpu"]
    if not limits:
        return compiled
    limit = int(min(limits) * fraction)
    checked = set()

    def dispatch(*inputs: Any) -> Any:
        leaves, tree = jax.tree.flatten(inputs[:-1])
        signature = (
            tree,
            tuple((value.shape, str(value.dtype), getattr(value, "weak_type", False)) for value in leaves),
            inputs[-1],
        )
        if signature not in checked:
            analysis = compiled.lower(*inputs).compile().memory_analysis()
            if analysis is None:
                raise RuntimeError("GPU compiler did not report executable memory usage")
            required = executable_bytes(analysis)
            print(
                json.dumps(
                    {
                        "event": "gpu_memory_budget",
                        "required_bytes": required,
                        "budget_bytes": limit,
                        "temporary_bytes": analysis.temp_size_in_bytes,
                        "local_devices": len(devices),
                    }
                ),
                flush=True,
            )
            if required > limit:
                raise MemoryError(
                    f"compiled PPO requires {required} bytes/GPU, budget is {limit}; "
                    "lower microbatch_per_gpu before dispatch"
                )
            checked.add(signature)
        return compiled(*inputs)

    return dispatch
