"""Keep heterogeneous backward work local; synchronize only complete gradients."""

from collections.abc import Callable, Sequence
from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import optax
from jax.experimental import multihost_utils
from jax.flatten_util import ravel_pytree
from jax.sharding import Mesh
from jax.sharding import PartitionSpec as P


class GradientSum:
    def __init__(self, devices: Sequence[jax.Device]) -> None:
        self.mesh = Mesh(np.asarray(tuple(devices), dtype=object), ("data",))
        self.pack = None
        self.unpack = None
        # No arithmetic/fusion in this heterogeneous executable: GPU-specific
        # fusion autotune results cannot be shared between A100 and A30.
        self.reduce = jax.jit(
            jax.shard_map(
                lambda value: jax.lax.psum(value, "data"),
                mesh=self.mesh,
                in_specs=P("data"),
                out_specs=P("data"),
                check_vma=False,
            )
        )

    def __call__(self, gradients: Any) -> Any:
        if self.pack is None:
            _, unpack = ravel_pytree(gradients)
            self.pack = jax.jit(lambda tree: ravel_pytree(tree)[0])
            self.unpack = jax.jit(unpack)
        arrays = self.pack(gradients)[None]
        arrays = multihost_utils.host_local_array_to_global_array(arrays, self.mesh, P("data"))
        reduced = self.reduce(arrays)
        return self.unpack(reduced.addressable_shards[0].data[0])


def make_heterogeneous_update(
    value_and_gradient: Callable,
    inner_optimizer: optax.GradientTransformation,
    cast_params: Callable,
    steps: int,
    reduce_sum: Callable,
    processes: int,
) -> Callable:
    """Return a one-local-GPU update retaining the existing MultiSteps state tree."""
    from kaggriculture.model.kernels.deferred_optimizer import AccumulationSchedule, accumulate_only

    if steps < 1 or processes < 1:
        raise ValueError("positive steps and processes required")
    schedule = AccumulationSchedule(steps)

    @jax.jit
    def backward(params: Any, reference: Any, state: Any, batch: Any) -> tuple[Any, Any]:
        (_, metrics), gradients = value_and_gradient(params, reference, batch)
        gradients = jax.tree.map(lambda value: value.astype(jnp.float32), gradients)
        return accumulate_only(gradients, state), {**metrics, "gradient_norm": optax.tree.norm(gradients)}

    @jax.jit
    def emit(params: Any, state: Any, summed: Any) -> tuple[Any, Any, Any]:
        gradients = jax.tree.map(lambda value: value / processes, summed)
        updates, inner = inner_optimizer.update(gradients, state.inner_opt_state, params)
        params = optax.apply_updates(params, updates)
        state = state._replace(
            mini_step=jnp.zeros_like(state.mini_step),
            gradient_step=optax.safe_increment(state.gradient_step),
            inner_opt_state=inner,
            acc_grads=jax.tree.map(jnp.zeros_like, state.acc_grads),
        )
        return params, state, cast_params(params)

    cached_params = cached_reference = inference = reference_inference = None

    def update(params: Any, reference: Any, state: Any, batch: Any) -> tuple[Any, Any, Any]:
        nonlocal cached_params, cached_reference, inference, reference_inference
        if cached_params is not params:
            inference = cast_params(params)
            cached_params = params
        if cached_reference is not reference:
            reference_inference = cast_params(reference)
            cached_reference = reference
        should_emit = schedule.should_emit(state)
        with jax.profiler.TraceAnnotation("mixed_local_backward"):
            state, metrics = backward(inference, reference_inference, state, batch)
        if should_emit:
            with jax.profiler.TraceAnnotation("mixed_gradient_sum"):
                summed = reduce_sum(state.acc_grads)
            with jax.profiler.TraceAnnotation("mixed_local_adam"):
                params, state, inference = emit(params, state, summed)
            cached_params = params
        schedule.advance(state)
        return params, state, metrics

    update.data_parallel_device_count = 1
    update.prepare_batch = lambda batch: jax.device_put(batch, jax.local_devices()[0])
    return update
