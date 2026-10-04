"""`plan.SAME_DAY_FERT_ON`: sell the day's own fertilizer on the day.

The defect, measured on the real engine (seed 54306694 seat 0 vs tape
105077847). `COLLECT_FERTILIZER` puts one unit per animal per day into the
*hand's* inventory and nothing empties that hand until `_end_of_day`, which
runs after the last market turn -- so day 1's six fertilizer sell on day 2's
opening row. Day 1 dawn is 32 coins, day 2 dawn is 2, day 2 hires nobody and
day 2 is the farmer alone watering: no FEED, no CARE, no COLLECT.

The switch is `MIDDAY_PLACE_V2`'s excursion with fertilizer in it: the COLLECT
ranks take a route tier of their own, a mid-block excursion PLACEs what they
collected into the shed, and those units are added to the day's LAST lot --
`SELL.allocate` runs once at dawn against a shed that has no fertilizer in it
yet, so without the row the deposit has nothing to be sold on.

The one thing melon did not need is the quantity. Melon is never a PICKUP
item, so `PLACE MELON 100` can only bank what the block harvested; a block
that picked fertilizer up at the route base to spread it later is carrying
units the shed must not take, so the deposit asks for exactly the COLLECT
ranks the block has worked since its own first.

The `test_off_*` half is the identity half, pinned on `test_route_early`'s
digests -- the planner at `a838700`, the same pin `test_midday_place.py` and
`test_open_pump.py` use.
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
from test_route_early import BASE_PRICE, PIN, PIN_SEEDS, _digest, _plan, _row, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: The stack `test_route_early`'s digests were taken before -- the planner at
#: `a838700`. None of these five answers anything about a mid-day deposit, and
#: pinning them off is what makes the identity claim this switch's own.
_PINNED_OFF = ("ROUTE_SPLIT_ON", "SURVIVAL_WATER_ON", "TAIL_CARE_ON",
               "FEED_MANDATORY_ON", "EARLY_SELL_ON")


def _view(n_animal=6, day=1, money=600, wheat=12, fert=0, n_ripe=0, yld=4,
          favail=1, nquad=1):
    """`n_animal` geese that have stood overnight -- unfed, and with the
    engine's fertilizer flag up, which is the board `COLLECT_FERTILIZER`
    exists on -- plus `n_ripe` ripe tomatoes as the day's other work."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    t_favail = z.copy()
    kind[:n_animal] = spec.KIND_COOP
    occ[:n_animal] = 0                                  # geese, unfed yesterday
    t_cons[:n_animal] = 1
    t_favail[:n_animal] = favail
    hi = n_animal + n_ripe
    kind[n_animal:hi] = spec.KIND_PLANT
    occ[n_animal:hi] = spec.I_TOMATO
    t_yield[n_animal:hi] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=t_favail, shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _day(view=None, crew=4, **kw):
    return _plan(view if view is not None else _view(**kw),
                 _macro(crew_target=np.int32(crew)))


def _deposits(plan):
    """[(unit, turn, qty)] of every mid-day fertilizer deposit the route emits.

    `OP_PLACE` of `I_FERT` and nothing else: the shipped planner's only other
    PLACE is the animal placement, whose arg is an animal index (`>= I_GOOSE`,
    the very test `sim/units.py` makes), and `OP_DROP` is the day's return leg,
    which lands after the last row by construction.
    """
    uop, ua, uq = (np.asarray(a) for a in plan[:3])
    out = []
    for u in range(spec.MAX_UNITS):
        for t in np.flatnonzero((uop[u] == O.OP_PLACE) & (ua[u] == spec.I_FERT)):
            out.append((u, int(t), int(uq[u, t])))
    return sorted(out)


def _collects(plan):
    """Turns on which the day's route collects fertilizer, per unit."""
    uop = np.asarray(plan[0])
    return {u: list(np.flatnonzero(uop[u] == O.OP_COLLECT_FERT))
            for u in range(spec.MAX_UNITS)
            if (uop[u] == O.OP_COLLECT_FERT).any()}


def _sell_row(plan, turn, item):
    return sum(q for op, a, q in _row(plan, turn)
               if op == O.MO_SELL and a == item)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "SAME_DAY_FERT_ON", True)


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte. Pinned on
    `test_route_early`'s digests, the same ones `test_midday_place.py` and
    `test_open_pump.py` hold their own switches to."""
    monkeypatch.setattr(P, "SAME_DAY_FERT_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_banks_nothing_mid_day_on_a_collecting_board(monkeypatch):
    """OFF there is no excursion at all: the day collects its fertilizer and
    carries it home, which is the defect."""
    monkeypatch.setattr(P, "SAME_DAY_FERT_ON", False)
    plan = _day()
    assert _collects(plan), "the fixture board collected nothing"
    assert not _deposits(plan)
    assert _sell_row(plan, P.early_lot_turns()[-1], spec.I_FERT) == 0


# =========================================================================
# ON: the deposit, the quantity and the row
# =========================================================================

def test_on_deposits_are_a_place_of_fertilizer(on):
    """The op is the engine's selective shed deposit, named and quantified: it
    banks fertilizer and leaves whatever else the block still carries -- the
    feed wheat, the fertilizer picked up to spread -- alone."""
    plan = _day()
    dep = _deposits(plan)
    assert dep, "the day banked nothing"
    uop, ua = np.asarray(plan[0]), np.asarray(plan[1])
    assert not ((uop == O.OP_DROP).any())
    assert all(q > 0 for *_, q in dep), dep
    assert set(int(a) for a in ua[uop == O.OP_PLACE]) == {spec.I_FERT}


def test_on_asks_for_no_more_than_the_block_collected(on):
    """The quantity is the count melon never needed. A deposit that asked for
    `MIDDAY_PLACE_QTY` would hand the shed the fertilizer the block is still
    carrying to spread, so it asks for the COLLECT ranks it has worked."""
    plan = _day()
    dep = _deposits(plan)
    assert dep
    by_unit = _collects(plan)
    assert sum(q for *_, q in dep) <= sum(len(v) for v in by_unit.values())
    for u, _t, q in dep:
        assert 0 < q <= len(by_unit[u]), (u, q, by_unit)
    assert max(q for *_, q in dep) < P.MIDDAY_PLACE_QTY


def test_on_every_deposit_makes_the_row_that_sells_it(on):
    """The time rule: a rank whose deposit cannot reach the day's last selling
    row is not a candidate, so no excursion is ever spent on one."""
    last = P.early_lot_turns()[-1]
    for crew in (2, 4, 6, 8):
        dep = _deposits(_day(crew=crew))
        assert dep, f"crew {crew} banked nothing"
        assert all(t <= last for _u, t, _q in dep), (crew, dep)


def test_on_the_deposit_follows_the_collect_it_banks(on):
    """A PLACE is only worth its turn if the units are on the unit when it
    fires: every deposit stands after that unit's first COLLECT."""
    plan = _day()
    coll = _collects(plan)
    for u, t, _q in _deposits(plan):
        assert u in coll and t > min(coll[u]), (u, t, coll)


def test_on_gives_the_day_a_row_to_sell_the_deposit_on(on):
    """The other half. `SELL.allocate` runs at dawn against a shed with no
    fertilizer in it, so without this the deposit sits until `_end_of_day`."""
    plan = _day()
    banked = sum(q for *_, q in _deposits(plan))
    assert banked > 0
    assert _sell_row(plan, P.early_lot_turns()[-1], spec.I_FERT) >= banked


def test_on_leaves_a_day_with_nothing_to_collect_alone(on):
    """The trigger is the flag, not the day: no fertilizer available, no
    excursion and no row."""
    plan = _day(favail=0)
    assert not _collects(plan)
    assert not _deposits(plan)
    assert _sell_row(plan, P.early_lot_turns()[-1], spec.I_FERT) == 0


def test_on_leaves_day_0_and_the_days_past_the_knob_alone(on, monkeypatch):
    """Days 1..`SAME_DAY_FERT_LAST_DAY`: day 0 has no animal that has stood
    overnight, and past the knob the switch is inert by construction."""
    assert not _deposits(_day(day=0))
    monkeypatch.setattr(P, "SAME_DAY_FERT_LAST_DAY", 5)
    assert _deposits(_day(day=5))
    assert not _deposits(_day(day=6))


def test_on_leaves_the_terminal_day_alone(on):
    """Past `LAST_SHED_DAY` the whole shed liquidates on the day's own rows and
    the route is a PASS override, so there is nothing for an excursion to do."""
    assert not _deposits(_day(day=O.LAST_SHED_DAY + 1))


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
