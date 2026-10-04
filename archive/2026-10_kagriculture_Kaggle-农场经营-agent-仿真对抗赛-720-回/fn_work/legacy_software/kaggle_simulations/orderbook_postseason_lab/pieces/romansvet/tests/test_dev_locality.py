"""`compact`: *where* the day develops (R3, a gene inert at zero theta).

`slot_rank` and the per-structure placement ranks choose which free tiles get
planted and built on, and they used to choose in sweep order -- so development
scattered over the whole board and the next 12-17 tile-days of watering and
harvesting inherited that scatter. `compact` orders the same free tiles by
their Manhattan distance from the shed-access block instead, in
`compact + 1` bands, so ES can trade "develop wherever" against "develop where
the crew already is" against the pool rather than having a constant picked
here. Measured saturated on top of the one-crossing route, 16 paired games per
matchup: +8,391 +- 7,490 coins against `starter`, +8,700 +- 12,873 against
`kagg2`, and +14,062 +- 5,062 on the `kagg2` **margin** -- the only
intervention in the sweep that is significantly positive on margin in both
matchups.

The inertness guarantee is what lets every incumbent checkpoint keep its plan:
`_rank_near(mask, 0)` must be `_rank(mask)` bit for bit, or the archetype
ladder moves and the appended-block promise of `policy.SHAPES` is void.
"""
from __future__ import annotations

import itertools
import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
from test_admit_route import TABLE, _farm
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO


def _plant_positions(view, macro):
    """Sweep positions whose chain starts with PLANT, straight off `_derive`."""
    d = P._derive(np, view, macro, TABLE, np.int32(0), False, np.int32(0))
    return np.flatnonzero(np.asarray(d.chain_op[:, 0]) == O.OP_PLANT).tolist()


def _empty(money=50_000):
    return _farm({})._replace(money=np.int32(money))


# ---- inertness ---------------------------------------------------------


def test_compact_zero_reproduces_the_sweep_rank():
    """`_rank_near(mask, zeros) == _rank(mask)` on 500 random masks, on both
    backends. If this fails the gene is not inert, the ladder moves, and no
    incumbent theta decodes to the plan it was trained for."""
    import jax.numpy as jnp
    rng = np.random.default_rng(20260826)
    zero = np.zeros(P.N_T, np.int32)
    for i in range(500):
        mask = rng.random(P.N_T) < rng.random()
        want = np.asarray(P._rank(np, mask))
        np.testing.assert_array_equal(np.asarray(P._rank_near(np, mask, zero)), want,
                                      err_msg=f"numpy, mask {i}")
        got = np.asarray(P._rank_near(jnp, jnp.asarray(mask), jnp.asarray(zero)))
        np.testing.assert_array_equal(got, want, err_msg=f"jax, mask {i}")


def test_compact_zero_leaves_the_planted_tiles_where_they_were():
    """The same guarantee one level up: at `compact = 0` the day develops the
    first free sweep positions, which is what every pre-R3 theta asked for."""
    assert _plant_positions(_empty(), _macro(
        plant_target=np.array([6, 0, 0, 0, 0], np.int32))) == [0, 1, 2, 3, 4, 5]


def test_compact_decodes_to_zero_at_theta_zero():
    from test_genome_retype import _obs_sell
    m = brain.decide(np, np.zeros(PO.N_PARAMS, np.float32), _obs_sell())
    assert int(m.compact) == 0
    assert int(m.dev_weight) == brain.GROW_ONE


def test_a_shorter_theta_is_inert():
    """Every layout ever shipped decodes `compact = 0`: the block is appended,
    so a shorter theta zero-pads into it (`policy.unpack`)."""
    from test_genome_retype import SHIPPED_LAYOUTS, _obs_sell
    rng = np.random.default_rng(4)
    for n in SHIPPED_LAYOUTS:
        m = brain.decide(np, (rng.normal(size=n) * 0.4).astype(np.float32), _obs_sell())
        assert int(m.compact) == 0, n
        assert int(m.dev_weight) == brain.GROW_ONE, n


# ---- the gene, on ------------------------------------------------------


def test_compact_saturated_develops_the_nearest_free_tile_first():
    """Saturated, the bucket key is `DIST_SHED` itself: the four shed-access
    tiles (distance 0) go first, then the distance-1 ring, ties by sweep
    position. On an empty board that is 44, 45, 54, 55 and then 34, 35 --
    against 0..5, the far north-west corner, at `compact = 0`."""
    got = _plant_positions(_empty(), _macro(
        plant_target=np.array([6, 0, 0, 0, 0], np.int32), compact=np.int32(P.DIST_MAX)))
    assert sorted(got) == [34, 35, 44, 45, 54, 55]
    assert [int(P.DIST_SHED[p]) for p in sorted(got)] == [1, 1, 0, 0, 0, 0]


def test_compact_is_a_scale_and_not_a_flag():
    """Intermediate values band the distance rather than switching it on: the
    key is `(DIST_SHED * compact) // DIST_MAX`, so raising the gene resolves
    finer bands and the tile the day picks walks in towards the shed. That
    monotone ramp is the gradient ES needs -- a 0/1 gate would have none."""
    one = np.array([1, 0, 0, 0, 0], np.int32)
    dists = [int(P.DIST_SHED[_plant_positions(_empty(), _macro(
        plant_target=one, compact=np.int32(c)))[0]]) for c in range(P.DIST_MAX + 1)]
    assert dists[0] == P.DIST_MAX and dists[-1] == 0
    assert all(a >= b for a, b in itertools.pairwise(dists)), dists


def test_ties_break_to_the_lower_serpentine_index():
    """Inside a band the sweep still orders, and `_rank_near` gets that for
    free because `cumsum` is already in index order."""
    mask = np.zeros(P.N_T, bool)
    mask[[7, 3, 91, 44]] = True
    key = np.zeros(P.N_T, np.int32)
    key[[3, 7]] = 2                      # one band ...
    key[[44, 91]] = 1                    # ... ahead of the other
    rank = np.asarray(P._rank_near(np, mask, key))
    assert [int(rank[p]) for p in (44, 91, 3, 7)] == [0, 1, 2, 3]


def test_compact_moves_the_placements_too():
    """Structures are development as much as plantings are, and the animals
    that stand on them are fed and harvested every day for the rest of the
    season -- so the same rank decides where a coop is built."""
    macro = _macro(animal_want=np.array([4, 0, 0], np.int32))
    far = P._derive(np, _empty(), macro, TABLE, np.int32(0), False, np.int32(0))
    near = P._derive(np, _empty(), macro._replace(compact=np.int32(P.DIST_MAX)),
                     TABLE, np.int32(0), False, np.int32(0))
    f = np.flatnonzero(np.asarray(far.m_place)).tolist()
    n = np.flatnonzero(np.asarray(near.m_place)).tolist()
    assert f and n and f != n
    assert max(int(P.DIST_SHED[p]) for p in n) < min(int(P.DIST_SHED[p]) for p in f)


def test_the_dev_key_stays_inside_the_unrolled_bucket_range():
    """`_rank_near` unrolls `DIST_MAX + 1` buckets; a key outside them would
    silently rank everything at zero. Pinned over the whole gene range."""
    for c in range(P.DIST_MAX + 1):
        key = np.asarray(P._dev_key(np, np.int32(c)))
        assert key.dtype == np.int32
        assert int(key.min()) >= 0 and int(key.max()) <= P.DIST_MAX, c


def test_dev_ranks_agree_across_backends():
    import jax
    import jax.numpy as jnp
    view = _empty()
    macro = _macro(plant_target=np.array([5, 0, 0, 0, 0], np.int32),
                   animal_want=np.array([2, 1, 1], np.int32),
                   compact=np.int32(5))
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        np.testing.assert_array_equal(np.asarray(x), np.asarray(y))


def test_dist_shed_is_the_distance_to_the_shed_access_block():
    """Not a proxy for it: the crew respawns on those four tiles every
    morning, so this is the walk every unit really pays."""
    assert P.DIST_SHED.dtype == np.int32 and P.DIST_SHED.shape == (P.N_T,)
    assert sorted(np.flatnonzero(P.DIST_SHED == 0).tolist()) == [44, 45, 54, 55]
    assert int(P.DIST_SHED.max()) == P.DIST_MAX == 8
    for p in (0, 17, 63, 99):
        want = min(abs(int(P.SERP_X[p]) - int(sx)) + abs(int(P.SERP_Y[p]) - int(sy))
                   for sx, sy in spec.SHED_ACCESS_XY)
        assert int(P.DIST_SHED[p]) == want
