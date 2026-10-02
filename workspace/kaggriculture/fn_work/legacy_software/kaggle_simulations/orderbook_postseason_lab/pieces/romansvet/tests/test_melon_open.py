"""`plan.MELON_OPEN_ON`: the recorded top-tier opening, played by the planner.

Day 0 buys twelve melon out of the *carrot* (the wheat pays last and only if
the carrot cannot cover the debt), the seed clip sees melon and wheat before
every other crop, the melon goes on the tiles nearest a shed access, and on the
day it saturates each block that holds one walks home after its last melon
tile, DROPs, walks back and **carries on** -- so the crop reaches lots whose
engine hours are still in front of the opponent's hour-17 dump without the day
being turned into the idle DROP day `MIDDAY_DROP_ON` was rejected for.

The `test_off_*` half is the identity half: off, `_melon_open` is never called,
`before` is the cumsum it always was, `plant_crop` is the crop-order boundary
it always was, `_routes` compiles no excursion and `_market` emits no melon
row. The digests are the whole six-array plan on `test_route_early`'s seeded
boards, taken off a clean `git archive aae13e0` export -- the commit this
switch was cut into, with the promoted stack (ROUTE_SPLIT, SURVIVAL_WATER,
TAIL_CARE, FEED_MANDATORY) at its shipped default, which is what this file's
fixtures leave alone.
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
from test_route_early import (BASE_PRICE, PIN_SEEDS, _digest, _plan, _row,
                              _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MELON_OPEN_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "MELON_OPEN_ON", True)


def _mix(target, day=P.MELON_OPEN_DAY):
    """`_melon_open`'s rewritten plant target on `day`."""
    view = _view(day=day)
    macro = _macro(plant_target=np.asarray(target, np.int32))
    return [int(x) for x in P._melon_open(np, view, macro).plant_target]


def _melon_view(n=12, day=P.MELON_OPEN_HARVEST_DAY, money=3_000, yld=6):
    """A board of `n` melon tiles planted on day 0, on the day they saturate."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    kind[:n] = spec.KIND_PLANT
    occ[:n] = spec.I_MELON
    t_yield[:n] = yld
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(1), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _melon_lots(plan):
    """[(engine hour, units)] of the melon-only rows, in turn order."""
    out = []
    for t in O.MELON_LOT_TURNS:
        for op, arg, qty in _row(plan, t):
            if op == O.MO_SELL and arg == spec.I_MELON:
                out.append((t + 1, qty))
    return out


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `test_route_early.PIN_SEEDS`, taken
#: off a clean `git archive aae13e0` export -- the commit before this switch --
#: so they pin the pre-switch planner and not this file's own output.
#: Regenerate only with a measured reason to move the plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_emits_no_melon_row_and_no_excursion(off):
    """The extra lots and the DROP belong to the switch, not to the layout."""
    plan = _plan(_melon_view(), _macro(crew_target=np.int32(6)))
    assert _melon_lots(plan) == []
    assert not (np.asarray(plan[0]) == O.OP_DROP).any()


# =========================================================================
# ON: the day-0 mix
# =========================================================================

def test_on_day_zero_buys_twelve_melon_and_keeps_the_wheat():
    """The shipped day-0 mix is 10 WHEAT + 9 CARROT. The recorded opening's is
    7 WHEAT + 12 MELON: the carrot pays nine of the twelve and the wheat pays
    the last three, because it is last in `_MELON_PAY_RANK`. v2 paid in plain
    crop order, wheat first, and the day came out 0 WHEAT + 7 CARROT."""
    assert _mix((10, 9, 0, 0, 0)) == [7, 0, 0, 0, 12]


def test_on_never_takes_the_last_wheat_while_another_crop_can_pay():
    """Wheat is the animal feed and the four-day rotation: it is the last thing
    the opening spends, on every mix the network can hand it."""
    for target in ((10, 9, 0, 0, 0), (6, 6, 3, 4, 0), (4, 0, 9, 6, 0),
                   (12, 4, 4, 0, 0), (19, 0, 0, 0, 0)):
        mix = _mix(target)
        others = sum(target) - target[0]
        assert mix[spec.I_MELON] == min(P.MELON_OPEN_TILES, sum(target))
        assert sum(mix) == sum(target), (target, mix)
        # Wheat only gives up what the other crops together could not cover.
        assert mix[spec.I_WHEAT] == target[0] - max(
            min(P.MELON_OPEN_TILES, sum(target)) - others, 0), (target, mix)


def test_on_leaves_every_other_day_and_a_bigger_melon_want_alone():
    """Only `MELON_OPEN_DAY` is touched, and the switch can only ever *raise*
    melon: a day the network already wants more melon keeps its own mix."""
    assert _mix((10, 9, 0, 0, 0), day=P.MELON_OPEN_DAY + 1) == [10, 9, 0, 0, 0]
    assert _mix((2, 2, 0, 0, 15)) == [2, 2, 0, 0, 15]


def test_on_day_zero_seed_row_carries_the_melon_and_the_wheat(on):
    """`seed_cap` clips the seed want prefix-wise and the day over-asks, so the
    order the prefix is taken in decides which crop the clip drops. Melon
    first, wheat second."""
    view = _view(day=P.MELON_OPEN_DAY, money=3_000)
    macro = _macro(plant_target=np.asarray((10, 9, 0, 0, 0), np.int32))
    seeds = {arg: qty for op, arg, qty in _row(_plan(view, macro), O.TURN_BUY)
             if op == O.MO_BUY_SEED}
    assert seeds.get(spec.I_MELON, 0) == P.MELON_OPEN_TILES
    assert seeds.get(spec.I_WHEAT, 0) > 0
    assert seeds.get(spec.I_CARROT, 0) == 0


# =========================================================================
# ON: the dump day
# =========================================================================

def test_on_dump_day_offers_its_melon_in_small_lots_before_hour_seventeen(on):
    """Every 2800-tier opponent's first melon lot lands on day 10 hour 17. The
    switch's rows are all in front of it and none of them is larger than the
    recorded opening's largest -- a squared curve is walked, not jumped."""
    plan = _plan(_melon_view(), _macro(crew_target=np.int32(6)))
    lots = _melon_lots(plan)
    assert lots, "the dump day offered nothing"
    assert all(h <= 16 for h, _ in lots), lots
    assert all(0 < q <= P.MELON_OPEN_LOT for _, q in lots), lots


def test_on_dump_day_banks_its_crop_with_a_drop_and_keeps_working(on):
    """The excursion is the whole mechanism: a block that holds a melon walks
    home, DROPs and **carries on**. The day keeps its full `turn_budget`, which
    is what separates this from the `MIDDAY_DROP_ON` route that was rejected
    for idling the crew from `SELL_TURNS[-1]` on."""
    unit_op = np.asarray(_plan(_melon_view(), _macro(crew_target=np.int32(6)))[0])
    assert (unit_op == O.OP_DROP).any(), "nothing was banked mid-day"
    for u in range(spec.MAX_UNITS):
        drops = np.flatnonzero(unit_op[u] == O.OP_DROP)
        if not len(drops):
            continue
        after = unit_op[u, drops[0] + 1:]
        assert (after != O.OP_PASS).any(), f"unit {u} stopped at its DROP"
    late = unit_op[:, O.SELL_TURNS[-1] + 1:]
    assert (late != O.OP_PASS).any(), "the dump day was cut short like a DROP day"


def test_on_leaves_every_other_day_without_a_melon_row(on):
    """The extra rows are the dump day's alone; every other day of the season
    presents the layout it always did."""
    for day in (P.MELON_OPEN_HARVEST_DAY - 1, P.MELON_OPEN_HARVEST_DAY + 1):
        plan = _plan(_melon_view(day=day), _macro(crew_target=np.int32(6)))
        assert _melon_lots(plan) == [], day


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the opening melon lot) is a question the switch does
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
