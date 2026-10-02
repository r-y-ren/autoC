"""Fixed-order unit sampling with recorded, prefix-dependent support."""

from __future__ import annotations

import jax
import jax.numpy as jnp
import numpy as np

from kaggriculture.actions.masks import MASKED_LOGIT, MAX_UNITS, UNIT_STEM_INDEX, UNIT_STEM_SIZE, UNIT_STEMS

# Rust supplies (tile id, empty structure kind) per unit, then five seed counts.
PATCH_CONTEXT_SIZE = MAX_UNITS * 2 + 5
GROUPS = {
    "WATER": 0,
    "FERTILIZE": 1,
    "HARVEST": 2,
    "DIG": 3,
    "BUILD_COOP": 4,
    "BUILD_PASTURE": 4,
    "PLANT": 5,
    "CARE": 6,
    "FEED": 7,
    "COLLECT_FERTILIZER": 8,
}
CROPS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON")
STEM_GROUP = np.asarray([GROUPS.get(stem[0], -1) for stem in UNIT_STEMS], np.int32)
STEM_CROP = np.asarray([CROPS.index(s[1]) if s[0] == "PLANT" else -1 for s in UNIT_STEMS], np.int32)
STEM_STRUCTURE = np.asarray(
    [1 if s == ("PLACE", "GOOSE") else 2 if s in (("PLACE", "COW"), ("PLACE", "SHEEP")) else 0 for s in UNIT_STEMS],
    np.int32,
)


@jax.jit
def sequential_units(
    logits: jax.Array,
    stems: jax.Array,
    context: jax.Array,
    thresholds: jax.Array | None,
) -> tuple[jax.Array, jax.Array, jax.Array]:
    """Sample or greedily decode one forward pass, preserving the exact conditional masks.

    thresholds=None selects argmax. Otherwise supply one U[0,1) draw per unit.
    Inactive units never claim a tile or spend seeds. Masked actions have zero mass.
    """
    rows = logits.shape[0]
    base = stems[:, :UNIT_STEM_SIZE].reshape(rows, MAX_UNITS, len(UNIT_STEMS))
    tiles = context[:, :MAX_UNITS]
    structures = context[:, MAX_UNITS : MAX_UNITS * 2]
    seeds = context[:, MAX_UNITS * 2 :]
    mapping = jnp.asarray(UNIT_STEM_INDEX)
    group = jnp.asarray(STEM_GROUP)
    crop = jnp.asarray(STEM_CROP)
    structure = jnp.asarray(STEM_STRUCTURE)
    claimed = jnp.zeros((rows, MAX_UNITS), jnp.int32) - 1
    batch = jnp.arange(rows)

    def step(carry: tuple, unit: jax.Array) -> tuple:
        remaining, claims = carry
        animal_place = (structure[None, :] > 0) & (structure[None, :] == structures[:, unit, None])
        groups = jnp.where(animal_place, 9, group[None, :])
        same_tile = (tiles == tiles[:, unit, None]) & (tiles >= 0)
        prior = jnp.arange(MAX_UNITS)[None, :] < unit
        blocked = jnp.any(
            same_tile[:, :, None]
            & prior[:, :, None]
            & (claims[:, :, None] == groups[:, None, :])
            & (groups[:, None, :] >= 0),
            axis=1,
        )
        has_seed = (crop[None, :] < 0) | (remaining[:, jnp.maximum(crop, 0)] > 0)
        effective = base[:, unit] & ~blocked & has_seed
        effective = effective.at[:, UNIT_STEMS.index(("PASS",))].set(True)
        masked = jnp.where(effective[:, mapping], logits[:, unit].astype(jnp.float32), MASKED_LOGIT)
        log_probs = jax.nn.log_softmax(masked, axis=-1)
        if thresholds is None:
            selected = jnp.argmax(masked, axis=-1)
        else:
            cdf = jnp.cumsum(jnp.exp(log_probs), axis=-1)
            cdf /= cdf[:, -1:]
            selected = jnp.sum(cdf <= thresholds[:, unit, None], axis=-1)
        stem = mapping[selected]
        selected_crop = crop[stem]
        active = tiles[:, unit] >= 0
        remaining = remaining.at[batch, jnp.maximum(selected_crop, 0)].add(
            -((selected_crop >= 0) & active).astype(jnp.int32)
        )
        claims = claims.at[:, unit].set(jnp.where(active, groups[batch, stem], -1))
        return (remaining, claims), (selected, log_probs[batch, selected], effective)

    _, (actions, log_prob, masks) = jax.lax.scan(step, (seeds, claimed), jnp.arange(MAX_UNITS))
    effective_stems = stems.at[:, :UNIT_STEM_SIZE].set(jnp.swapaxes(masks, 0, 1).reshape(rows, UNIT_STEM_SIZE))
    return actions.T, log_prob.T, effective_stems
