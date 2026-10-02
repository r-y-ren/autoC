"""Feeding is survival, cashing a CARE bank on a fire day, and unlocking
today's CARE; CARE is emitted only when its payout is reachable, fed, under
the cap and worth the wheat (PLANNER_V3_1 section 0.11). The third reason is
what makes the cadence daily: the bank increments only on a day that was both
fed and cared, so a feed rule that waits for hunger inherits the engine's
`consecutive_unfed >= 2` and caps CARE at one day in two. Survival work stops
on the pay day (section 0.4): nothing that lives past it can still sell -- and
with it goes the quiet-day feed.

The days are written off `valuation.pay_day()` and not off `O.LAST_SHED_DAY`
= 28: `plan.HORIZON_DROP_ON` (5b0fcc4) moved the pay day to 29, and both
gates this file reads move with it -- `survival_pays = day < VAL.pay_day()`
(`plan.py:3905`) and `care_ok`'s `h_next <= VAL.pay_day()` (`plan.py:4006`).
`pay_day() - 1` is where the two part company: a goose is still fed for
survival there, but tonight's care would pay two days out and is refused.

Three boards pin `TAIL_CARE_ON` off (on by default since 0c8bee8): the tail
hop spends a unit's idle turns on the nearest animal the day fed and left
uncared (`plan.py:5313-5326`) without ever asking `care_ok`, so with it on
every refusal those three are about is written back into the day for free.
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

from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as V

# `plan` is imported at module scope on purpose: `valuation.pay_day()` reads
# the horizon switch off `valuation._PLAN`, which `plan` binds when it is
# imported, and a module that reaches `valuation` without it reads the
# un-switched 28 instead (see `df9013d` on `test_budget_greedy.py`).
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _farm(day, animals=(), plants=(), wheat=10, price=None):
    """`animals`: (position, kind, placed_day, t_cons, t_bank).
    `plants`: (position, crop, planted_day, t_cons)."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_cons, t_bank = z.copy(), z.copy(), z.copy()
    for pos, a, placed, cons, bank in animals:
        kind[pos] = spec.ANIMAL_STRUCT[a]
        occ[pos] = a
        t_day[pos], t_cons[pos], t_bank[pos] = placed, cons, bank
    for pos, c, planted, cons in plants:
        kind[pos] = spec.KIND_PLANT
        occ[pos] = c
        t_day[pos], t_cons[pos] = planted, cons
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1),
        price=BASE.copy() if price is None else price, t_bank=t_bank)


def _ops(view, **macro):
    unit_op = P.build_day(np, view, _macro(**macro))[0]
    return {op: int((unit_op == op).sum()) for op in (O.OP_FEED, O.OP_CARE, O.OP_WATER)}


GOOSE_FED = (0, 0, 0, 0, 0)          # position 0, goose placed day 0, fed yesterday, no bank


@pytest.fixture
def no_tail_care(monkeypatch):
    """`TAIL_CARE_ON` off. On by default since 0c8bee8, it spends a unit's
    idle tail on the nearest animal the day fed and left uncared
    (`plan.py:5313-5326`: `need_care & fed_anyway`, neither of which asks
    `care_ok`). The turn is free, so with the switch on every board below is
    cared whatever the horizon, the price or the headroom decided, and the
    refusal each is about has no visible effect -- the same reason 0c8bee8
    pinned it off in `test_horizon_drop.test_care_pays_only_when_its_fire_is
    _payable` and in all of `test_care_hold`."""
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)


def _tomato_day():
    """Planting day of a tomato whose first fire lands on `pay_day() - 1`, so
    its remaining stream still pays for the survival watering
    `SURVIVAL_WATER_ON` prices (`plan.py:3956`). A day-0 tomato has spent all
    four of its fires long before the horizon and is refused for *that*
    reason, which is why 0c8bee8 re-planted `test_horizon_drop`'s thirsty
    tomatoes on day 20 when it turned the switch on: 20 with the horizon on,
    19 without it."""
    return V.pay_day() - int(spec.CROP_FIRST_YIELD_DAY[spec.I_TOMATO]) - 1


def _care_pays_on(day, kind=0, placed=0):
    """Harvest day the CARE taken on `day` pays on: `next_fire_after`, the
    value `care_ok` tests against `VAL.pay_day()` (`plan.py:4006`). For a
    goose placed on day 0 it is `day + 2` -- the care banks at tonight's eod
    and the fire that pays it is the next one after that."""
    return int(V.next_fire_after(np, np.int32(placed),
                                 np.int32(spec.ANIMAL_FIRST_YIELD_DAY[kind]),
                                 np.int32(spec.ANIMAL_INTERVAL[kind]), np.int32(day)))


def _past_care_horizon_day():
    """The first day whose care is past the horizon while the day still feeds:
    `day + 2 > pay_day()` and `day < pay_day()` leave exactly `pay_day() - 1`.
    28 with the horizon on, 27 without it."""
    return V.pay_day() - 1


def test_no_survival_work_on_the_pay_day():
    # `survival_pays = day < VAL.pay_day()` (plan.py:3905): on the pay day
    # itself nothing that has to live into tomorrow can still sell.
    day = V.pay_day()
    view = _farm(day, animals=[(0, 0, 0, 1, 0)],
                 plants=[(1, spec.I_TOMATO, _tomato_day(), 1)], wheat=0)
    ops = _ops(view)
    assert ops[O.OP_FEED] == 0 and ops[O.OP_WATER] == 0
    op, qty = P.build_day(np, view, _macro())[3], P.build_day(np, view, _macro())[5]
    assert int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_PRODUCT].sum()) == 0   # no feed wheat bought


def test_survival_work_still_runs_the_day_before_the_pay_day():
    # The same board one day earlier: a fire still lands by the pay day, so
    # the watering is priced and the hungry goose is fed.
    day = V.pay_day() - 1
    assert _tomato_day() + int(spec.CROP_FIRST_YIELD_DAY[spec.I_TOMATO]) <= V.pay_day()
    ops = _ops(_farm(day, animals=[(0, 0, 0, 1, 0)],
                     plants=[(1, spec.I_TOMATO, _tomato_day(), 1)]))
    assert ops[O.OP_FEED] == 1 and ops[O.OP_WATER] == 1


def test_a_pending_bank_is_fed_on_its_fire_day():
    # goose fires every night; fed yesterday, so not hungry -- fed for the bank
    assert _ops(_farm(10, animals=[(0, 0, 0, 0, 1)]))[O.OP_FEED] == 1


def test_a_quiet_day_is_fed_for_the_care_it_unlocks():
    # Not hungry, no bank, and (for a cow) no fire tonight: the feed buys
    # nothing but today's CARE, and that is the whole point -- without it the
    # bank can only grow on the days hunger already forced a feed.
    for animal in (GOOSE_FED, (0, 1, 0, 0, 0)):
        ops = _ops(_farm(10, animals=[animal]))
        assert ops[O.OP_FEED] == 1 and ops[O.OP_CARE] == 1


def test_no_quiet_day_feed_when_the_care_cannot_pay():
    # A quiet-day feed is worth exactly the care it unlocks, so every test
    # `care_ok` fails takes the feed with it.
    #   `pay_day() - 1`: today's care would pay a day past the horizon
    late = _past_care_horizon_day()
    assert _care_pays_on(late) > V.pay_day() >= late + 1
    assert _ops(_farm(late, animals=[(0, 0, 0, 0, 0)]))[O.OP_FEED] == 0
    #   the product does not clear the wheat
    cheap = BASE.copy()
    cheap[spec.I_EGG] = 20
    assert _ops(_farm(10, animals=[GOOSE_FED], price=cheap))[O.OP_FEED] == 0
    #   no headroom: a cow holding a bank of 5 against max_held 6
    assert _ops(_farm(10, animals=[(0, 1, 0, 0, 5)]))[O.OP_FEED] == 0


def test_care_is_emitted_when_it_pays():
    # hungry goose on day 10: fed, egg 50 > wheat 25, payout day 12, bank 0 -> CARE
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 1


def test_no_care_when_the_payout_is_past_the_horizon(no_tail_care):
    # `pay_day() - 1`: the care pays one day past the horizon and is refused;
    # the day before, it lands on the pay day itself and is taken.
    late = _past_care_horizon_day()
    assert _care_pays_on(late) > V.pay_day()
    assert _ops(_farm(late, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 0
    assert _care_pays_on(late - 1) <= V.pay_day()
    assert _ops(_farm(late - 1, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 1


def test_no_care_when_the_egg_is_worth_less_than_the_wheat(no_tail_care):
    price = BASE.copy()
    price[spec.I_EGG] = 20
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)]))[O.OP_CARE] == 1
    assert _ops(_farm(10, animals=[(0, 0, 0, 1, 0)], price=price))[O.OP_CARE] == 0


def test_no_care_without_headroom_under_max_held(no_tail_care):
    # cow placed day 0 seen on day 10 (fires on harvest days 8, 10, 12: none
    # tonight, so the bank carries): holds 6, bank 5 + this care + the base
    # unit would exceed it; bank 4 fits exactly
    assert _ops(_farm(10, animals=[(0, 1, 0, 1, 5)]))[O.OP_CARE] == 0
    assert _ops(_farm(10, animals=[(0, 1, 0, 1, 4)]))[O.OP_CARE] == 1


def test_a_fire_tonight_clears_the_bank_before_the_care_counts():
    # goose placed day 0, cared every day since: bank 3 on day 3, fires tonight.
    # The eod consumes that bank before today's care banks toward eod 4, so the
    # care still pays +1 and headroom is judged against 0, not 3.
    assert _ops(_farm(3, animals=[(0, 0, 0, 1, 3)]))[O.OP_CARE] == 1


def test_care_never_outruns_its_feed():
    # `want_care = want_feed & care_ok`, so wherever the feed want is empty the
    # care want is too: on the pay day nothing survival-shaped is emitted
    # however well the care itself would price. (On day 28 this board is now
    # quiet for the *care* horizon instead, so the day moves with `pay_day()`.)
    ops = _ops(_farm(V.pay_day(), animals=[GOOSE_FED]))
    assert ops[O.OP_FEED] == 0 and ops[O.OP_CARE] == 0


def test_pre_maturity_care_is_allowed_within_headroom():
    # cow placed day 8, day 9: first fire day 16 <= 28, bank 0 -> CARE
    assert _ops(_farm(9, animals=[(0, 1, 8, 1, 0)]))[O.OP_CARE] == 1


def test_parse_view_reads_the_pending_bank():
    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    tiles[0][0] = {"kind": "COOP", "animal": "GOOSE", "placed_day": 2, "fed_today": False,
                   "consecutive_unfed": 1, "yield_units": 0, "cared_today": False,
                   "fertilizer_available": True, "pending_care_bonus": 2}
    obs = {"day": 4,
           "farms": [{"tiles": tiles, "money": 100, "unlocked_quadrants": ["NW"], "hands": []}],
           "private": {"shed": {}, "seeds": {}},
           "market": {"prices": {n: 7 for n in spec.PRODUCTS},
                      "inventory": {n: spec.MARKET_I0 for n in spec.PRODUCTS}},
           "town": {"unlocked_shops": []}}
    v = parse.parse_view(obs, 0)
    k = int(np.flatnonzero(P.SERP == 0)[0])         # serpentine position of tile (0, 0)
    assert int(v.t_bank[k]) == 2


def test_sim_day_view_carries_the_bank():
    import jax.numpy as jnp

    from kagg3.sim import rollout
    from kagg3.sim.state import build_tables, initial_state, prices_of
    st = initial_state(jnp)
    st = st._replace(t_bank=st.t_bank.at[0, 0].set(3))
    tables = build_tables(jnp)
    v = rollout.day_view(st, 0, jnp.int32(0), prices_of(jnp, tables, st.mkt_inv))
    assert int(np.asarray(v.t_bank).sum()) == 3
