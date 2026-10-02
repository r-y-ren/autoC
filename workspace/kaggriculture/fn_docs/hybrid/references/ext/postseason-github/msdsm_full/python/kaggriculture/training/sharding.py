"""Small helpers for explicit single-process JAX data parallelism."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import jax
import numpy as np
from jax.sharding import Mesh, NamedSharding, PartitionSpec


def select_data_parallel_devices(
    requested_count: int,
    available_devices: Sequence[jax.Device] | None = None,
) -> tuple[jax.Device, ...]:
    if requested_count <= 0:
        raise ValueError("data-parallel device count must be positive")
    available = tuple(jax.local_devices() if available_devices is None else available_devices)
    if requested_count > len(available):
        raise ValueError(f"requested {requested_count} data-parallel devices, but only {len(available)} are local")
    return available[:requested_count]


def put_replicated(tree: Any, devices: Sequence[jax.Device]) -> Any:
    selected_devices = tuple(devices)
    device_count = len(selected_devices)
    if device_count <= 0:
        raise ValueError("at least one data-parallel device is required")
    axis_name = "data_replicas"
    mesh = Mesh(np.asarray(selected_devices, dtype=object), (axis_name,))
    sharding = NamedSharding(mesh, PartitionSpec(axis_name))

    def replicate(value: Any) -> jax.Array:
        host = np.asarray(jax.device_get(value))
        replicas = np.broadcast_to(host, (device_count, *host.shape)).copy()
        return jax.device_put(replicas, sharding)

    return jax.tree.map(replicate, tree)


def put_global_replicated(tree: Any, devices: Sequence[jax.Device]) -> Any:
    """Cache unmapped parameters on all inference devices without per-call rewrapping."""
    mesh = Mesh(np.asarray(tuple(devices), dtype=object), ("inference",))
    sharding = NamedSharding(mesh, PartitionSpec())

    def replicate(value: Any) -> jax.Array:
        host = np.asarray(jax.device_get(value))
        buffers = [jax.device_put(host, device) for device in mesh.local_devices]
        return jax.make_array_from_single_device_arrays(host.shape, sharding, buffers)

    return jax.tree.map(replicate, tree)


def _first_replica(value: Any) -> Any:
    # A generic slice gathers all local pmap shards, although shard zero already
    # contains the complete result. Keep generic indexing for tracers/global arrays.
    if (
        isinstance(value, jax.Array)
        and not isinstance(value, jax.core.Tracer)
        and value.ndim > 0
        and value.is_fully_addressable
    ):
        for shard in value.addressable_shards:
            leading = shard.index[0]
            if (
                isinstance(leading, slice)
                and leading.indices(value.shape[0]) == (0, 1, 1)
                and shard.data is not None
                and shard.data.shape == (1, *value.shape[1:])
            ):
                return shard.data.reshape(value.shape[1:])
    return value[0]


def unreplicate(tree: Any) -> Any:
    return jax.tree.map(_first_replica, tree)


def shard_batch(
    batch: dict[str, Any],
    devices: Sequence[jax.Device],
    *,
    balance_sample_mask: bool = False,
    reference_samples: int | None = None,
    allow_uneven_pairs: bool = False,
) -> dict[str, jax.Array]:
    """Place equal, independent batch shards on devices for ``pmap``.

    PPO's final padded microbatch is re-ordered so every replica receives the same
    number of valid seat pairs. This makes the mean of local gradients exactly the
    global masked-mean gradient.
    """
    selected_devices = tuple(devices)
    device_count = len(selected_devices)
    if not selected_devices:
        raise ValueError("at least one data-parallel device is required")
    arrays = {name: np.asarray(value) for name, value in batch.items()}
    non_scalars = [value for value in arrays.values() if value.ndim > 0]
    if not non_scalars:
        raise ValueError("a sharded batch requires at least one non-scalar field")
    batch_size = non_scalars[0].shape[0]
    if any(value.shape[0] != batch_size for value in non_scalars):
        raise ValueError("all non-scalar batch fields must share a leading dimension")
    if batch_size % device_count:
        raise ValueError(f"batch size {batch_size} is not divisible by {device_count} devices")

    order: np.ndarray | None = None
    uneven = False
    if balance_sample_mask:
        sample_mask = arrays.get("sample_mask")
        if sample_mask is None:
            raise ValueError("balanced sharding requires sample_mask")
        valid = np.flatnonzero(sample_mask)
        padding = np.flatnonzero(~sample_mask.astype(np.bool_))
        pair_multiple = 2 * device_count
        uneven = bool(len(valid) % pair_multiple or len(padding) % pair_multiple)
        if uneven and not allow_uneven_pairs:
            raise ValueError("valid and padded rows must each divide into complete seat-pair device shards")
        if batch_size % pair_multiple or not np.all(
            sample_mask.reshape(-1, 2)[:, 0] == sample_mask.reshape(-1, 2)[:, 1]
        ):
            raise ValueError("shards and masks must preserve complete seat pairs")
        valid_chunks = [chunk.reshape(-1) for chunk in np.array_split(valid.reshape(-1, 2), device_count)]
        padding_sizes = [batch_size // device_count - len(chunk) for chunk in valid_chunks]
        padding_chunks = np.split(padding, np.cumsum(padding_sizes)[:-1])
        balanced_order = np.concatenate(
            [
                np.concatenate((valid_chunk, padding_chunk))
                for valid_chunk, padding_chunk in zip(valid_chunks, padding_chunks)
            ]
        )
        if not np.array_equal(balanced_order, np.arange(batch_size)):
            order = balanced_order

    local_batch_size = batch_size // device_count
    sharded = {}
    for name, value in arrays.items():
        if value.ndim == 0:
            sharded[name] = np.broadcast_to(value, (device_count,))
        else:
            ordered = value if order is None else value[order]
            sharded[name] = ordered.reshape(device_count, local_batch_size, *value.shape[1:])

    if reference_samples is not None:
        if reference_samples <= 0:
            raise ValueError("reference samples must be positive")
        maximum_local_samples = (reference_samples + device_count - 1) // device_count
        sample_mask = sharded.get("sample_mask", np.ones((device_count, local_batch_size), dtype=np.bool_))
        valid_per_device = np.sum(sample_mask, axis=1)
        if maximum_local_samples > local_batch_size:
            raise ValueError("reference samples exceed the physical device batch")
        if maximum_local_samples > valid_per_device.min() and not allow_uneven_pairs:
            raise ValueError("reference samples exceed the valid rows available on a device")
        base, remainder = divmod(reference_samples, device_count)
        reference_mask = np.zeros((device_count, maximum_local_samples), dtype=np.bool_)
        for device_index in range(device_count):
            count = min(base + (device_index < remainder), int(valid_per_device[device_index]))
            reference_mask[device_index, :count] = True
        sharded["reference_sample_mask"] = reference_mask
        sharded["reference_mean_scale"] = np.full(
            device_count,
            device_count / max(int(reference_mask.sum()), 1),
            dtype=np.float32,
        )
    if uneven or (balance_sample_mask and allow_uneven_pairs):
        # All ranks must call pmap with identical PyTrees, including all-padding ranks.
        sharded["sample_mean_scale"] = np.full(device_count, device_count / max(len(valid), 1), dtype=np.float32)
    return sharded


def flatten_pmap_batch(array: jax.Array) -> jax.Array:
    return array.reshape((-1, *array.shape[2:]))
