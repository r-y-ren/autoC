"""One-time crops harvest at the age their yield saturates -- or on the last
shed day when the season ends first (PLANNER_V3_1 section 0.1). HARVEST needs
only age >= first_yield_day and yield > 0, so a deadline harvest is legal, and
selling k >= 1 units strictly dominates the 0 an unsold crop is worth once
day 29 has no end-of-day to bank it.

Saturation, not max_yield_day, is the upper clamp: a one-time crop is born
with one unit and each in-window watering adds one, so a crop whose cap is
already full gains nothing by standing another two days. Melon is the only
crop where the two ages differ (10 vs 12) and the only product with no shop
demand, so those two days are the whole melon race.
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
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as V

WHEAT, MELON = spec.I_WHEAT, spec.I_MELON
_MOVES = (O.OP_PASS, O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _view(day, crop, planted_day, t_yield=1, pos=0):
    """One one-time crop on serpentine position `pos`, everything else empty.

    `pos` matters on a DROP day and nowhere else: day 29's route ends at
    `SELL_TURNS[-1]` and every unit owes the walk to a shed-access tile on top
    (`plan.drop_turns`), so a tile the crew cannot get home from is dropped
    unworked. Serpentine 0 is the far corner (`plan.DIST_SHED` = 8) and cannot
    be reached and banked; position 1 can.
    """
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[pos] = spec.KIND_PLANT
    occ = z - 1
    occ[pos] = crop
    t_day = z.copy()
    t_day[pos] = planted_day
    ty = z.copy()
    ty[pos] = t_yield
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day,
        t_water=z.copy(), t_cons=z.copy(), t_yield=ty,
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _tile_ops(view):
    """The farmer's non-movement ops, in order. Only one tile has work."""
    unit_op = P.build_day(np, view, _macro())[0]
    return [int(o) for o in unit_op[0] if int(o) not in _MOVES]


def test_horizon_constant_is_the_last_shed_day():
    assert O.LAST_SHED_DAY == 28


def test_wheat_planted_day_25_harvests_on_the_last_payable_day():
    # The clamp is `valuation.pay_day() - t_day`, and `plan.HORIZON_DROP_ON`
    # (5b0fcc4) moved that day from 28 to 29: what used to be the deadline
    # harvest is now only the in-window watering, and the harvest waits a day
    # for the age its yield saturates. The pay day itself waters and harvests --
    # and on a DROP day banks the load with `OP_DROP`, which is what makes the
    # harvest sellable at all.
    H = V.pay_day()
    assert _tile_ops(_view(day=H - 1, crop=WHEAT, planted_day=25)) == [O.OP_WATER]
    assert _tile_ops(_view(day=H, crop=WHEAT, planted_day=25, pos=1)) == (
        [O.OP_WATER, O.OP_HARVEST] + ([O.OP_DROP] if H > O.LAST_SHED_DAY else []))


def test_wheat_planted_day_25_still_waits_on_day_27():
    # age 2: the clamp age is 3, so no premature harvest -- day 28's watering
    # is worth one more unit.
    ops = _tile_ops(_view(day=27, crop=WHEAT, planted_day=25))
    assert O.OP_HARVEST not in ops
    assert O.OP_WATER in ops


def test_melon_harvests_at_its_saturation_age_not_its_max_yield_day():
    # Age 10 is where melon's yield saturates: `_new_plant` seeds one unit and
    # the waterings at ages 6..10 add five more, which is CROP_MAX_YIELD. Ages
    # 11 and 12 are inside the bonus window but add nothing, so the harvest
    # does not wait for them -- it is two days of melon market position for
    # zero units (measured 2026-08-26: 6.00 units a tile on both schedules).
    assert int(spec.CROP_SATURATE_AGE[MELON]) == 10
    assert int(spec.CROP_MAX_YIELD_DAY[MELON]) == 12
    assert O.OP_HARVEST in _tile_ops(_view(day=10, crop=MELON, planted_day=0, t_yield=6))
    assert O.OP_HARVEST not in _tile_ops(_view(day=9, crop=MELON, planted_day=0, t_yield=5))


def test_melon_planted_day_17_harvests_on_day_27_at_age_10():
    assert _tile_ops(_view(day=27, crop=MELON, planted_day=17, t_yield=6)) == [O.OP_WATER, O.OP_HARVEST]
    assert O.OP_HARVEST not in _tile_ops(_view(day=26, crop=MELON, planted_day=17))


def test_saturation_age_only_moves_melon():
    # Every other crop's window closes before daily watering can saturate it,
    # so the clamp is still its max-yield day and no schedule but melon's moves.
    for c in range(spec.N_CROPS):
        expect = 10 if c == MELON else int(spec.CROP_MAX_YIELD_DAY[c])
        assert int(spec.CROP_SATURATE_AGE[c]) == expect, spec.CROPS[c]


def test_early_season_harvest_day_is_unchanged():
    # planted day 0: max_yield_day 4 is reachable, so the harvest waits for it
    assert O.OP_HARVEST not in _tile_ops(_view(day=3, crop=WHEAT, planted_day=0))
    assert O.OP_HARVEST in _tile_ops(_view(day=4, crop=WHEAT, planted_day=0))


def _obs(view):
    return brain.PolicyObs(
        day=view.day, money=np.int32(0), opp_money=np.int32(0),
        kind=view.kind, occ=view.occ, opp_kind=view.kind, opp_occ=view.occ,
        t_day=view.t_day, t_yield=view.t_yield, shed=view.shed, seeds=view.seeds,
        nquad=np.int32(1), opp_nquad=np.int32(1),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        price=view.price, shops=np.zeros(spec.N_SHOPS, np.int32))


def test_brain_free_slots_count_the_deadline_tile():
    # brain.n_free_slots and the planner read the same clamp, so the tile frees
    # on `valuation.pay_day()` and not a day earlier.
    H = V.pay_day()
    assert int(brain.n_free_slots(np, _obs(_view(day=H, crop=WHEAT, planted_day=25)))) == 100
    assert int(brain.n_free_slots(np, _obs(_view(day=H - 1, crop=WHEAT, planted_day=25)))) == 99


def test_plant_gate_reads_the_horizon():
    # `day + first_yield_day <= valuation.pay_day()` is the gate: wheat (2)
    # plants on `pay_day - 2` and not on the day after it -- day 27 and 28 with
    # `plan.HORIZON_DROP_ON`, 26 and 27 without. Decoded through brain.decide
    # with a zero theta so the crop split is uniform.
    from kagg3.core import policy as PO
    H = V.pay_day()
    theta = np.zeros(PO.N_PARAMS, np.float32)
    free = _view(day=H - 2, crop=WHEAT, planted_day=0)
    free = free._replace(kind=np.full(100, spec.KIND_EMPTY, np.int32),
                         occ=np.full(100, -1, np.int32), money=np.int32(3000))
    m_in = brain.decide(np, theta, _obs(free)._replace(money=np.int32(3000)))
    m_out = brain.decide(np, theta,
                         _obs(free._replace(day=np.int32(H - 1)))._replace(money=np.int32(3000)))
    assert int(m_in.plant_target[WHEAT]) > 0
    assert int(m_out.plant_target[WHEAT]) == 0
