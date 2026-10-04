"""Opt-in profiling variants: checkpoint-compatible accumulation for finite gradients."""

from __future__ import annotations

from typing import Any

import jax
import jax.numpy as jnp
import numpy as np
import optax


def accumulate_only(gradients: Any, state: optax.MultiStepsState) -> optax.MultiStepsState:
    accumulated = jax.tree.map(
        lambda gradient, previous: (previous + (gradient - previous) / (state.mini_step + 1)).astype(jnp.float32),
        gradients,
        state.acc_grads,
    )
    return state._replace(mini_step=optax.safe_increment(state.mini_step), acc_grads=accumulated)


class AccumulationSchedule:
    def __init__(self, steps: int) -> None:
        if steps <= 0:
            raise ValueError("accumulation steps must be positive")
        self.steps = steps
        self.state_source: Any = None
        self.microstep = 0

    def should_emit(self, state: optax.MultiStepsState) -> bool:
        if self.state_source is not state:
            counters = np.asarray(jax.device_get(state.mini_step))
            self.microstep = int(counters.flat[0])
            if not np.all(counters == self.microstep) or not 0 <= self.microstep < self.steps:
                raise ValueError("inconsistent or out-of-range accumulation counters")
        return self.microstep == self.steps - 1

    def advance(self, state: optax.MultiStepsState) -> None:
        self.microstep = (self.microstep + 1) % self.steps
        self.state_source = state


def deferred_multisteps(
    optimizer: optax.GradientTransformation,
    steps: int,
) -> optax.GradientTransformation:
    if steps <= 0:
        raise ValueError("accumulation steps must be positive")
    reference = optax.MultiSteps(optimizer, every_k_schedule=steps, use_grad_mean=True, accumulator_dtype=jnp.float32)

    def update(
        gradients: Any,
        state: optax.MultiStepsState,
        params: Any = None,
    ) -> tuple[Any, optax.MultiStepsState]:
        accumulated = jax.tree.map(
            lambda gradient, previous: previous + (gradient - previous) / (state.mini_step + 1),
            gradients,
            state.acc_grads,
        )
        emit = state.mini_step == steps - 1

        def apply_inner(operands: tuple[Any, Any, Any]) -> tuple[Any, Any]:
            values, inner_state, parameters = operands
            return optimizer.update(optax.tree.cast_like(values, gradients), inner_state, parameters)

        def retain_inner(operands: tuple[Any, Any, Any]) -> tuple[Any, Any]:
            _, inner_state, _ = operands
            update_shapes, _ = jax.eval_shape(apply_inner, operands)
            return optax.tree.zeros_like(update_shapes), inner_state

        updates, inner_state = jax.lax.cond(
            emit,
            apply_inner,
            retain_inner,
            (accumulated, state.inner_opt_state, params),
        )
        next_state = optax.MultiStepsState(
            mini_step=optax.safe_increment(state.mini_step) % steps,
            gradient_step=jnp.where(emit, optax.safe_increment(state.gradient_step), state.gradient_step),
            inner_opt_state=inner_state,
            acc_grads=jax.tree.map(lambda value: ((1 - emit) * value).astype(jnp.float32), accumulated),
            skip_state=state.skip_state,
        )
        return updates, next_state

    return optax.GradientTransformation(reference.init, update)
