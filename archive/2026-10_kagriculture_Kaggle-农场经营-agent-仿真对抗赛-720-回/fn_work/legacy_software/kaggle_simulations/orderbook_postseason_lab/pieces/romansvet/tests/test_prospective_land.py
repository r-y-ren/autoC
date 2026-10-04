"""A quadrant bought this morning is developed this afternoon (PLANNER_V3_1
section 0.3 / M1): the decision head counts its 25 tiles as free when it
predicts the grant, and task derivation plants and builds on them.

Both halves are needed and neither does anything alone. `brain.decide` caps
development at `n_free_slots`, so a head that cannot see the new tiles never
asks for enough plantings to fill them; `_derive` reads the hour-0 `kind`,
where the bought quadrant is still LOCKED, so a planner that cannot see them
plants nothing there whatever the head asks for.
"""
from __future__ import annotations

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
from test_budget_order import _macro, geese

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import policy as PO

BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
NE, SW, SE = 1, 2, 3                               # spec.LAND_ORDER

#: A land bias no valuation can outweigh either way. These tests are about M1's
#: mechanics -- whose tiles open, when, and what is bought for them -- so the
#: gene is pinned out of the way at each end rather than left to argue with the
#: quadrant's computed value, which `test_land_value.py` is for. `WANT` is what
#: a saturated-positive gene really decodes to; `VETO` is past what any decode
#: can produce, so it stands for "refuse, whatever the tiles are worth".
WANT = np.int32(spec.LAND_PRICES[0])
VETO = np.int32(-spec.COIN_CAP)


def _board(locked_quads, nquad=1, money=3000, seeds=0, day=3):
    """NW planted with strawberries (an ongoing crop: no free tile, no task),
    every quadrant in `locked_quads` LOCKED, the rest planted the same way."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_PLANT, np.int32)
    occ = np.full(100, spec.I_STRAWBERRY, np.int32)
    for q in locked_quads:
        kind[P.SERP_QUAD == q] = spec.KIND_LOCKED
        occ[P.SERP_QUAD == q] = -1
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.full(spec.N_CROPS, seeds, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE.copy())


def _view(money=3000, seeds=0):
    return _board((NE, SW, SE), money=money, seeds=seeds)


def _worked(plan, op):
    """How many times `op` is executed anywhere in the day's routes."""
    return int((plan[0] == op).sum())


def _wheat(n):
    return np.array([n, 0, 0, 0, 0], np.int32)


def test_plantings_land_on_the_new_quadrant_the_same_day():
    """Nine of the ten the macro asks for, and the tenth is M2's price, not a
    masking failure: a land day's units idle until the quadrant unlocks in the
    market phase of `SELL_TURNS[0]`, so the crew walks 20 turns instead of 22
    and the hire enumeration -- which scores every candidate on the full budget
    -- admits one tile more than the route can reach."""
    view = _view(seeds=10)
    with_land = P.build_day(np, view, _macro(land_bias=WANT, plant_target=_wheat(10)))
    without = P.build_day(np, view, _macro(land_bias=VETO, plant_target=_wheat(10)))
    assert _worked(with_land, O.OP_PLANT) == 9
    assert _worked(without, O.OP_PLANT) == 0


def test_builds_land_on_the_new_quadrant_too():
    plan = P.build_day(np, _view(), _macro(land_bias=WANT, animal_want=geese(2)))
    assert _worked(plan, O.OP_BUILD_COOP) == 2 and _worked(plan, O.OP_PLACE) == 2


def test_nothing_prospective_when_the_purse_cannot_pay():
    view = _view(money=500, seeds=10)
    plan = P.build_day(np, view, _macro(land_bias=WANT, plant_target=_wheat(10)))
    assert _worked(plan, O.OP_PLANT) == 0
    assert int(plan[5][plan[3] == O.MO_BUY_LAND].sum()) == 0


def test_the_prospective_mask_is_exactly_the_next_quadrant_in_land_order():
    """Three quadrants LOCKED, one purchase: only `LAND_ORDER[nquad - 1]` opens.

    24 or 25 of the 25, depending on how the quadrant sits in the serpentine
    sweep: a land day's units idle until the quadrant unlocks in the market
    phase of `SELL_TURNS[0]` (M2), so the crew walks 20 turns instead of 22 and
    the last tile is sometimes out of reach. What this pins is *which*
    quadrant opens, and against the wrong one the count is 0."""
    for nquad, quad in ((1, NE), (2, SW), (3, SE)):
        view = _board((NE, SW, SE), nquad=nquad, money=10_000, seeds=40)
        plan = P.build_day(np, view, _macro(land_bias=WANT, plant_target=_wheat(40)))
        assert _worked(plan, O.OP_PLANT) >= 24, f"nquad={nquad} did not open one quadrant"
        # the tiles that opened are that quadrant's, not the other two's
        opened = _board([q for q in (NE, SW, SE) if q != quad], nquad=nquad,
                        money=10_000, seeds=40)
        assert _worked(P.build_day(np, opened, _macro(land_bias=WANT,
                                                      plant_target=_wheat(40))),
                       O.OP_PLANT) == 0, f"nquad={nquad} opened the wrong quadrant"
    # a farm that owns everything has nothing prospective
    view = _board((), nquad=4, money=10_000, seeds=40)
    assert _worked(P.build_day(np, view, _macro(land_bias=WANT,
                                                plant_target=_wheat(40))),
                   O.OP_PLANT) == 0


def test_seed_purchases_are_clipped_to_the_tiles_that_will_exist():
    """A macro asking for 40 plantings on a board with 25 prospective tiles and
    no owned free tile buys at most 25 seeds, not 40."""
    view = _view(money=10_000, seeds=0)
    op, _, qty = P.build_day(np, view, _macro(land_bias=WANT,
                                              plant_target=_wheat(40)))[3:6]
    assert int(qty[op == O.MO_BUY_SEED].sum()) == 25


def test_the_seed_clip_leaves_room_for_the_builds():
    """25 prospective tiles, 5 of them wanted for coops: 20 seeds, not 25."""
    view = _view(money=10_000, seeds=0)
    macro = _macro(land_bias=WANT, animal_want=geese(5), plant_target=_wheat(40))
    op, _, qty = P.build_day(np, view, macro)[3:6]
    assert int(qty[op == O.MO_BUY_SEED].sum()) == 20


def _obs(nquad=1, money=3000, locked_quads=(NE, SW, SE)):
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_PLANT, np.int32)
    occ = np.full(100, spec.I_STRAWBERRY, np.int32)
    for q in locked_quads:
        kind[spec.TILE_QUAD == q] = spec.KIND_LOCKED
        occ[spec.TILE_QUAD == q] = -1
    return brain.PolicyObs(
        day=np.int32(3), money=np.int32(money), opp_money=np.int32(3000),
        kind=kind, occ=occ, opp_kind=kind.copy(), opp_occ=occ.copy(),
        t_day=z.copy(), t_yield=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), nquad=np.int32(nquad),
        opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32), price=BASE.copy(),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def test_the_decision_head_counts_the_prospective_tiles():
    obs = _obs()
    assert int(brain.n_free_slots(np, obs)) == 0
    assert int(brain.n_free_slots(np, obs, land=np.int32(1))) == 25
    assert int(brain.n_free_slots(np, obs, land=np.int32(0))) == 0
    # nquad 4 has no next quadrant, so `land` cannot conjure one
    assert int(brain.n_free_slots(np, _obs(nquad=4, locked_quads=()),
                                  land=np.int32(1))) == 0
    # a theta whose land logit is high plans development on the prospective tiles
    theta = np.zeros(PO.N_PARAMS, np.float32)
    theta[PO.offset("gb2") + 1] = 10.0
    m = brain.decide(np, theta, obs)
    assert int(m.land_bias) > 0 and int(m.plant_target.sum() + m.animal_want.sum()) > 0
    assert int(brain.decide(np, theta, obs._replace(money=np.int32(500)))
               .plant_target.sum()) == 0


def test_the_feature_vector_is_unchanged_by_the_new_argument():
    """`brain.features` keeps calling `n_free_slots` with owned tiles only."""
    obs = _obs()
    glob = brain.features(np, obs)[1]
    assert float(glob[5]) == 0.0


def test_prospective_land_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    view = _view(seeds=10)
    macro = _macro(land_bias=WANT, plant_target=_wheat(10), animal_want=geese(2))
    a = P.build_day(np, view, macro)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro),
                    jnp.asarray(spec.build_price_table()))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))


def test_the_decision_head_reads_no_tile_order():
    """[LAW] `PolicyObs`'s tile arrays have no canonical order -- the simulator
    passes raw board order and the submission passes serpentine `DayView`
    order -- so every reduction `brain` makes over them must be permutation
    invariant. Masking `kind` with `spec.TILE_QUAD` was not, and cost gate 1:
    the two call sites counted different quadrants and the trained policy and
    the shipped one hired different crews from the same position."""
    rng = np.random.default_rng(0)
    obs = _obs(nquad=2, locked_quads=(SW, SE))
    perm = rng.permutation(spec.N_TILES)
    shuffled = obs._replace(kind=obs.kind[perm], occ=obs.occ[perm],
                            opp_kind=obs.opp_kind[perm], opp_occ=obs.opp_occ[perm],
                            t_day=obs.t_day[perm], t_yield=obs.t_yield[perm])
    for land in (None, np.int32(0), np.int32(1)):
        assert int(brain.n_free_slots(np, obs, land=land)) == \
            int(brain.n_free_slots(np, shuffled, land=land))
    assert int(brain.n_free_slots(np, obs, land=np.int32(1))) == 25
