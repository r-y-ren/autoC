"""`plan.SURVIVAL_WATER_ON`: price the survival watering, and rank it above
the rest of the mandatory tier when it is worth taking.

The engine kills a planted tile two ways and only one is a watering
(`kaggle_environments/envs/kaggriculture/kaggriculture.py`):
`_daily_refresh_plants` :782-784 turns a tile with `consecutive_unwatered >= 2`
into WEED at the nightly refresh, and `_decay_plants` :752-766 eats one unit
every other *step* off any crop past its `max_lifespan_step` -- which an
ongoing crop is handed the moment it fires for the `max_yield`-th time
(:801-802). Watering answers the first and is powerless against the second.

Over the 32 McGrain replays the tail is almost entirely the second: 32.6 decay
deaths a game against 0.56 unwatered ones. What that leaves behind is 30.3
tile-days a game of PLANT whose `crop_remaining_value` is 0 and which
`must_water` still promotes into the MANDATORY tier every other day.

ON, the value the day already computes decides both: a survival watering is
mandatory only where the crop's remaining value beats `SURVIVAL_WATER_MIN`,
and the ones that pass sit one tier above the rest of the mandatory work.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests: OFF `must_water` is the expression it always was and `tier` is the
mandatory flag.
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
import pytest
from test_budget_order import _macro
from test_route_early import (PIN, PIN_SEEDS, _digest, _plan, _seeded_case)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

TABLE = spec.build_price_table()
BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


#: Both fixtures pin `ROUTE_SPLIT_ON` off, as `test_tail_care` does: the OFF
#: digests are the pre-split planner's and the boards below are arithmetic on
#: a farmer that starts at `ROUTE_BASE`. `TAIL_CARE_ON` and
#: `FEED_MANDATORY_ON` go with it -- this switch shipped on 2026-09-03 as one
#: of a stack of three, and the other two write into the same day plan, so
#: neither the pre-switch digests nor this file's worked examples are about
#: them.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


def _board(crop, planted_day, day, t_yield, t_cons=1, n=1):
    """`n` thirsty plants of one crop at the head of the serpentine.

    `t_cons = 1` is the tile the engine weeds tonight: one more unwatered
    refresh takes it to 2. `t_water = 0` says today has not watered it yet.
    """
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:n], occ[:n] = spec.KIND_PLANT, crop
    t_cons_a, t_day, t_y = z.copy(), z.copy(), z.copy()
    t_cons_a[:n], t_day[:n], t_y[:n] = t_cons, planted_day, t_yield
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons_a, t_yield=t_y, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0),
        nquad=np.int32(4), price=BASE_PRICE.copy(),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _derive(view):
    return P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))


def _waters(view):
    """Does the day plan a WATER at all?"""
    return bool((np.asarray(_plan(view, _macro())[0]) == O.OP_WATER).any())


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced -- `harvest_age` is hoisted above the water block but reads the
    same inputs, and `min(tier, 1)` is `tier` while the tier is the mandatory
    flag -- so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_waters_a_crop_that_can_never_sell_again(off):
    """The behaviour the switch exists to change. A STRAWBERRY planted on day
    2 has fired all four of its yields by day 18 (`first_yield_day` 10,
    `interval` 2) and holds nothing, so its remaining value is 0 and
    `_decay_plants` is already eating it -- and `must_water` still puts it in
    the mandatory tier and spends a unit-turn on it."""
    view = _board(spec.I_STRAWBERRY, planted_day=2, day=22, t_yield=0)
    d = _derive(view)
    assert P.VAL.crop_remaining_value(
        np, view.price, view.t_day, view.t_yield,
        np.clip(view.occ, 0, spec.N_CROPS - 1), view.day,
        np.clip(P.VAL.pay_day() - view.t_day, 10, 10))[0] == 0
    assert int(np.asarray(d.tier)[0]) == 1, "the spent tile was not mandatory"
    assert _waters(view), "the spent tile was not watered"


# =========================================================================
# ON: the value at the sale day decides, and the ones that pass rank first
# =========================================================================

def test_on_waters_a_tile_that_weeds_tonight_with_a_stream_left(on):
    """A STRAWBERRY planted on day 8 still has fires at days 20, 22 and 24, so
    the watering that keeps it alive tonight buys all of them. It stays
    mandatory -- and goes one tier above the rest of the mandatory work."""
    view = _board(spec.I_STRAWBERRY, planted_day=8, day=19, t_yield=0)
    d = _derive(view)
    assert int(np.asarray(d.tier)[0]) == 2, "the survival water was not promoted"
    assert _waters(view), "the tile that dies tonight was not watered"


def test_on_leaves_a_crop_that_can_never_sell_again(on):
    """The 30.3 tile-days: `test_off_waters_a_crop_that_can_never_sell_again`'s
    board, with the turn given back. The tile leaves `must_water` entirely --
    no water, no tier -- and weeds tonight, which `_decay_plants` was going to
    do to it anyway."""
    view = _board(spec.I_STRAWBERRY, planted_day=2, day=22, t_yield=0)
    assert int(np.asarray(_derive(view).tier)[0]) == 0
    assert not _waters(view), "a crop with no stream left was still watered"


def test_on_leaves_a_tile_whose_harvest_cannot_land_before_pay_day(on, monkeypatch):
    """A MELON planted on day 25 first yields on day 35: there is no day at or
    before `pay_day()` on which it sells, so `crop_remaining_value` is 0 and
    the watering buys nothing. OFF the same board takes the turn."""
    view = _board(spec.I_MELON, planted_day=25, day=26, t_yield=1)
    assert not _waters(view), "a crop that cannot reach pay_day was watered"
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    assert _waters(view), "the OFF board did not water it either"


def test_on_ranks_the_survival_water_above_a_deadline_harvest(on):
    """Why the second tier: everything else in the mandatory tier survives
    being cut -- a ripe WHEAT keeps its units on the tile until tomorrow --
    while the thirsty tile is gone for good. So the harvest stays at tier 1
    and the watering that saves a stream sits above it."""
    view = _board(spec.I_STRAWBERRY, planted_day=8, day=19, t_yield=0, n=1)
    ripe = np.asarray(view.kind).copy()
    occ, t_day, t_y, t_cons = (np.asarray(view.occ).copy(), np.asarray(view.t_day).copy(),
                               np.asarray(view.t_yield).copy(), np.asarray(view.t_cons).copy())
    ripe[1], occ[1], t_day[1], t_y[1], t_cons[1] = spec.KIND_PLANT, spec.I_WHEAT, 15, 6, 0
    view = view._replace(kind=ripe, occ=occ, t_day=t_day, t_yield=t_y, t_cons=t_cons)
    tier = np.asarray(_derive(view).tier)
    assert int(tier[1]) == 1, "the deadline harvest left the mandatory tier"
    assert int(tier[0]) > int(tier[1]), "the survival water did not outrank it"


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the survival watering) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests in this file were taken before the pair existed and still mean
#: what they meant -- "OFF, this file's switch leaves the planner it was cut
#: into alone" -- so the pair is pinned off here the way `EARLY_SELL_ON` and
#: `OPEN_PUMP_ON` were pinned off before it (`854b86b`).
#: `tests/test_tail_fill.py` and `tests/test_bank_before_lot.py` own the two.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
