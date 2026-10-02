"""Function-preserving depth growth with optimizer-state preservation."""

from __future__ import annotations

from dataclasses import replace
from typing import Any

import jax
import numpy as np

from kaggriculture.training.checkpointing import policy_hash
from kaggriculture.model.policy import JaxModelConfig, init_dense, init_norm, parameter_count


def identity_block(model: JaxModelConfig, seed: int) -> dict:
    keys = jax.random.split(jax.random.PRNGKey(seed), 4)
    block = {
        "attention_norm": init_norm(model.d_model),
        "qkv": init_dense(keys[0], model.d_model, 3 * model.d_model),
        "attention_output": init_dense(keys[1], model.d_model, model.d_model),
        "ffn_norm": init_norm(model.d_model),
        "ffn_input": init_dense(keys[2], model.d_model, model.ffn_dim),
        "ffn_output": init_dense(keys[3], model.ffn_dim, model.d_model),
    }
    block = jax.tree.map(np.asarray, block)
    for name in ("attention_output", "ffn_output"):
        block[name] = jax.tree.map(np.zeros_like, block[name])
    return block


def block_indices(previous: int, target: int) -> tuple[int, ...]:
    if previous < 1 or target <= previous:
        raise ValueError("target depth must exceed positive source depth")
    return tuple((index + 1) * target // previous - 1 for index in range(previous))


def retained_tree(tree: dict, indices: tuple[int, ...]) -> dict:
    return {**tree, "blocks": tuple(tree["blocks"][index] for index in indices)}


def grow_tree(tree: dict, additions: tuple[dict, ...], indices: tuple[int, ...]) -> dict:
    if len(tree["blocks"]) != len(indices):
        raise ValueError("retained depth mismatch")
    size = len(indices) + len(additions)
    if tuple(sorted(set(indices))) != indices or min(indices) < 0 or max(indices) >= size:
        raise ValueError("invalid retained block indices")
    retained = dict(zip(indices, tree["blocks"], strict=True))
    extra = iter(additions)
    blocks = tuple(retained[index] if index in retained else next(extra) for index in range(size))
    return {**tree, "blocks": blocks}


def grow_payload(payload: dict, model: JaxModelConfig, *, seed: int) -> tuple[dict, dict]:
    previous = JaxModelConfig(**payload["model_config"])
    if (
        previous.layers < 1
        or previous.dropout != 0
        or model.layers <= previous.layers
        or model != replace(previous, layers=model.layers)
    ):
        raise ValueError("growth must only increase depth of a dropout-free model")
    model.validate()
    indices = block_indices(previous.layers, model.layers)
    raw = payload["state"]
    if raw.get("reference_refresh_pending"):
        raise ValueError("finish a pending reference transition before growth")
    adam = raw["optimizer_state"]
    if int(adam.mini_step) != 0 or any(np.any(np.asarray(a) != 0) for a in jax.tree.leaves(adam.acc_grads)):
        raise ValueError("growth requires an empty Adam accumulation boundary")
    additions = tuple(identity_block(model, seed + index) for index in range(model.layers - previous.layers))
    policies = {}
    for role, hash_key in (("params", "policy_sha256"), ("reference_params", "reference_sha256")):
        original = raw[role]
        if len(original["blocks"]) != previous.layers or policy_hash(original) != payload[hash_key]:
            raise ValueError(f"source {role} shape or checksum mismatch")
        if any(not np.isfinite(a).all() for a in jax.tree.leaves(original)):
            raise ValueError("source weights must be finite")
        template = jax.tree.map(lambda a: (a.shape, a.dtype.str), additions[0])
        if any(jax.tree.map(lambda a: (a.shape, a.dtype.str), block) != template for block in original["blocks"]):
            raise ValueError("source block structure differs from the configured architecture")
        policies[role] = grow_tree(original, additions, indices)
        if policy_hash(retained_tree(policies[role], indices)) != payload[hash_key]:
            raise ValueError("growth changed existing weights")

    names = set(raw["params"])

    def parameter_tree(value: Any) -> bool:
        return isinstance(value, dict) and set(value) == names

    count = 0
    zeros = jax.tree.map(np.zeros_like, additions)

    def extend(value: Any) -> Any:
        nonlocal count
        if parameter_tree(value):
            count += 1
            return grow_tree(value, zeros, indices)
        return value

    new_adam = jax.tree.map(extend, adam, is_leaf=parameter_tree)
    if count != 3:
        raise ValueError(f"expected mu, nu and accumulator parameter trees, got {count}")
    restored = jax.tree.map(
        lambda a: retained_tree(a, indices) if parameter_tree(a) else a, new_adam, is_leaf=parameter_tree
    )
    if policy_hash(restored) != policy_hash(adam):
        raise ValueError("growth changed an existing Adam leaf or counter")
    new_state = {**raw, **policies, "optimizer_state": new_adam}
    old_control = {key: value for key, value in raw.items() if key not in {*policies, "optimizer_state"}}
    new_control = {key: value for key, value in new_state.items() if key in old_control}
    if policy_hash(old_control) != policy_hash(new_control):
        raise ValueError("growth changed RNG, counters or other control state")
    updated = {
        **payload,
        "model_config": model.to_dict(),
        "state": new_state,
        "policy_sha256": policy_hash(policies["params"]),
        "reference_sha256": policy_hash(policies["reference_params"]),
    }
    receipt = {
        "source_policy_sha256": payload["policy_sha256"],
        "source_reference_sha256": payload["reference_sha256"],
        "existing_optimizer_sha256": policy_hash(adam),
        "preserved_control_sha256": policy_hash(old_control),
        "new_policy_sha256": updated["policy_sha256"],
        "new_reference_sha256": updated["reference_sha256"],
        "completed_updates": raw["completed_updates"],
        "adam_step": int(adam.gradient_step),
        "seed": seed,
        "layers": [previous.layers, model.layers],
        "parameters": [parameter_count(raw["params"]), parameter_count(policies["params"])],
        "old_block_indices": list(indices),
        "added_block_indices": [i for i in range(model.layers) if i not in indices],
        "new_moments": "zero; existing Adam state and schedule counters retained",
        "production_changed": False,
    }
    return updated, receipt
