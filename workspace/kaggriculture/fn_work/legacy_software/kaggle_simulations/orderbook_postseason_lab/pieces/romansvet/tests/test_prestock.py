"""`plan.PRESTOCK_ON`: buy tomorrow's shed inputs tonight.

Measured on 39 real-engine replays: 34% of our units' PASS turns are the whole
crew standing on its spawn tiles at hours 0-2 waiting for the BUY row -- 390
unit-turns a game against a strong opponent's 34. The cause is the schedule and
not a valuation miss: a unit acts *before* its turn's market, so while the
morning's PICKUPs depend on a row that resolves at `O.TURN_BUY` = 1, no unit may
walk before turn 2.

The switch moves that row a day earlier. `sim/eod` banks the shed and never
touches `seeds`, so anything bought at `O.TURN_PRESTOCK` = 20 is on hand at
hour 0; day d+1's turn-1 row then carries only the residual, and on a day whose
residual is *empty* the overflow hire row moves into turn 1 and the whole crew
starts a turn earlier (`ops.ROUTE_BASE_PRE` / `ROUTE_BASE_WIDE_PRE`).

The `test_off_*` half is the identity half: off, nothing is emitted at
`TURN_PRESTOCK`, the hire rows are turns 0 and 2 and the plan is byte for byte
the one the champion theta decodes today -- pinned below by a digest of the
whole six-array plan on three fixed boards.
"""
from __future__ import annotations

import hashlib
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
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "PRESTOCK_ON", False)
    # The pin is the pre-split morning: `ROUTE_SPLIT_ON` (on by default since
    # 2026-09-03) starts a block the BUY row does not feed at `TURN_BUY`, which
    # is a turn this file's digests and its "no unit before ROUTE_BASE" both
    # predate. PRESTOCK's own subject -- which turn the *rows* sit on -- is
    # untouched by it either way.
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "PRESTOCK_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


def _view(day=10, money=20_000, n_coop=0, n_ripe=0, wheat=0, fert=0, seeds=None,
          yld=4, nquad=1):
    """A board with `n_coop` hungry geese, then `n_ripe` ripe tomatoes, then
    empty tiles for whatever the macro wants planted."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    kind[:n_coop] = spec.KIND_COOP
    occ[:n_coop] = 0                                   # geese, unfed yesterday
    t_cons[:n_coop] = 1
    hi = n_coop + n_ripe
    kind[n_coop:hi] = spec.KIND_PLANT
    occ[n_coop:hi] = spec.I_TOMATO
    t_yield[n_coop:hi] = yld
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32) if seeds is None
        else np.asarray(seeds, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _row(plan, turn):
    """[(op, arg, qty)] of the live orders on one market turn."""
    op, arg, qty = plan[3:6]
    return [(int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s]))
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) != O.MO_NONE]


def _first_unit_turn(plan):
    """The earliest turn on which any unit does something other than PASS."""
    unit_op = plan[0]
    acting = np.argwhere(unit_op != O.OP_PASS)
    return int(acting[:, 1].min()) if len(acting) else None


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


#: Three boards the OFF plan is pinned on: a planting day, a feeding day, and a
#: day that does both against a shed with room to spare.
PIN_BOARDS = (
    ("plant", dict(day=10, money=20_000), dict(plant_target=[4, 0, 0, 0, 0])),
    ("feed", dict(day=10, money=20_000, n_coop=12, wheat=4), {}),
    ("mixed", dict(day=14, money=20_000, n_coop=6, n_ripe=4, wheat=2, fert=3),
     dict(plant_target=[2, 1, 0, 0, 0])),
)


def _pin_case(cfg):
    board, kw = cfg[1], dict(cfg[2])
    if "plant_target" in kw:
        kw["plant_target"] = np.asarray(kw["plant_target"], np.int32)
    return _view(**board), _macro(**kw)


# =========================================================================
# OFF: the plan the champion theta decodes today
# =========================================================================

def test_off_emits_nothing_at_the_prestock_turn(off):
    for cfg in PIN_BOARDS:
        view, macro = _pin_case(cfg)
        assert _row(_plan(view, macro), O.TURN_PRESTOCK) == [], cfg[0]


def test_off_keeps_the_morning_schedule(off):
    """Hires at turns 0 and 2, the BUY row at turn 1, no unit before
    `ROUTE_BASE`."""
    for cfg in PIN_BOARDS:
        view, macro = _pin_case(cfg)
        plan = _plan(view, macro)
        assert all(o == O.MO_HIRE for o, _, _ in _row(plan, O.TURN_HIRE)), cfg[0]
        assert all(o != O.MO_HIRE for o, _, _ in _row(plan, O.TURN_BUY)), cfg[0]
        first = _first_unit_turn(plan)
        assert first is None or first >= O.ROUTE_BASE, cfg[0]


def test_off_plan_is_byte_identical_to_the_pin(off):
    """The whole six-array plan, hashed. This is the switch's contract: OFF
    every expression re-evaluates to the one it replaced, so a theta trained
    before it decodes byte for byte. Regenerate a digest only with a measured
    reason to move the plan."""
    # Taken off the tree at `d3140c1` -- the commit before this switch -- with
    # `scripts`-free arithmetic, so they pin the pre-switch planner and not
    # this file's own output.
    want = {"plant": "86b370135df44a09", "feed": "8a82257527f7ccd3",
            "mixed": "b2eae287b936ba0d"}
    got = {}
    for cfg in PIN_BOARDS:
        view, macro = _pin_case(cfg)
        got[cfg[0]] = _digest(_plan(view, macro))
    assert got == want


# =========================================================================
# ON: tonight's row, tomorrow's schedule
# =========================================================================

def test_seeds_stay_out_of_the_row_and_come_back_with_the_inner_switch(on, monkeypatch):
    """`PRESTOCK_SEEDS` is off and rejected: planting fills free land once, so
    "tomorrow plants what today planted" is exactly wrong on the day the land
    fills, and it spends the purse that early compounding needs (-90,863 mean
    margin, 0/24 games). The row still carries the five slots, so turning it
    back on is one constant."""
    view = _view(day=10)
    macro = _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))
    row = _row(_plan(view, macro), O.TURN_PRESTOCK)
    assert all(op != O.MO_BUY_SEED for op, _, _ in row), row

    monkeypatch.setattr(P, "PRESTOCK_SEEDS", True)
    row = _row(_plan(view, macro), O.TURN_PRESTOCK)
    seeds = {arg: qty for op, arg, qty in row if op == O.MO_BUY_SEED}
    assert seeds.get(spec.I_WHEAT, 0) > 0, row


def test_on_buys_tomorrows_feed_wheat_tonight(on):
    """A herd the shed cannot feed twice prestocks the difference, as
    BUY_PRODUCT on the wheat slot of the same row."""
    view = _view(day=10, n_coop=8, wheat=8)
    row = _row(_plan(view, _macro()), O.TURN_PRESTOCK)
    bought = {arg: qty for op, arg, qty in row if op == O.MO_BUY_PRODUCT}
    assert bought.get(spec.I_WHEAT, 0) > 0, row


def test_on_never_prestocks_an_animal(on):
    """The herd mix is a same-day policy output today cannot forecast, and an
    animal held overnight is shed room the eod dump wants."""
    view = _view(day=10, n_coop=4, wheat=8)
    macro = _macro(animal_want=np.array([2, 0, 0], np.int32),
                   plant_target=np.array([2, 0, 0, 0, 0], np.int32))
    row = _row(_plan(view, macro), O.TURN_PRESTOCK)
    assert all(op != O.MO_BUY_ANIMAL for op, _, _ in row), row


def test_tomorrows_buy_row_is_empty_and_the_crew_walks_at_turn_one(on):
    """The whole point. Run day d, hand day d+1 the stock tonight's row bought,
    and its own turn-1 row has nothing left to ask for -- so every unit starts
    at `ROUTE_BASE_PRE` instead of `ROUTE_BASE`."""
    macro = _macro()
    today = _view(day=10, n_coop=8, wheat=8)
    row = _row(_plan(today, macro), O.TURN_PRESTOCK)
    bought = 0
    for op, arg, qty in row:
        assert (op, arg) == (O.MO_BUY_PRODUCT, spec.I_WHEAT), row   # this board's only want
        bought += qty
    assert bought > 0

    # Tomorrow opens on the wheat tonight bought (the day's own eight are eaten
    # by the day's own feeds), so its BUY row asks for nothing.
    tomorrow = _view(day=11, n_coop=8, wheat=bought)
    plan = _plan(tomorrow, macro)
    assert _row(plan, O.TURN_BUY) == []
    assert _first_unit_turn(plan) == O.ROUTE_BASE_PRE


def test_a_live_buy_row_keeps_todays_law(on):
    """The switch never moves a unit in front of a row it depends on: a day
    that still has to buy at turn 1 walks from `ROUTE_BASE`, exactly as it
    does off."""
    view = _view(day=10, n_coop=10, wheat=0)     # every feed has to be bought
    plan = _plan(view, _macro())
    assert _row(plan, O.TURN_BUY) != []
    assert _first_unit_turn(plan) >= O.ROUTE_BASE


def test_a_wide_crew_hires_into_turn_one_and_walks_at_turn_two(on):
    """Past `MAX_MARKET_ORDERS` hands the overflow hire row is turn 2 today.
    With the BUY row empty it moves into turn 1 -- which is the only reason
    `ROUTE_BASE_WIDE_PRE` may be 2, the law being "a hand hired in turn t first
    acts in turn t+1"."""
    macro = _macro(hire_bias=np.int32(3_000))    # buy a crew past the first row
    view = _view(day=10, n_ripe=60, yld=6, money=200_000)
    plan = _plan(view, macro)
    n_hire = sum(1 for turn in O.HIRE_TURNS for op, _, _ in _row(plan, turn)
                 if op == O.MO_HIRE)
    n_hire += sum(1 for op, _, _ in _row(plan, O.TURN_BUY) if op == O.MO_HIRE)
    if n_hire <= spec.MAX_MARKET_ORDERS:
        pytest.skip(f"board hired {n_hire} hands, not a wide crew")
    assert _row(plan, O.TURN_HIRE_WIDE) == []
    assert all(op == O.MO_HIRE for op, _, _ in _row(plan, O.TURN_BUY))
    assert _first_unit_turn(plan) == O.ROUTE_BASE_WIDE_PRE


def test_the_prestock_never_breaches_the_cash_reserve(on):
    """It spends `Prefix.purse_left` and nothing else -- the coins the day's own
    greedy left in a purse already net of the hire bill and `cash_reserve`. So
    the row's cost can never reach past what the day could have spent anyway."""
    table = np.asarray(P.default_price_table())
    quotes = P.PJ.buy_quotes(np, table, P.PJ.projected_inv(
        np, np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        np.zeros(spec.N_SHOPS, np.int32), O.TURN_PRESTOCK))
    for money in (0, 3, 40, 400, 4_000):
        view = _view(day=10, n_coop=6, wheat=0, money=money)
        macro = _macro(plant_target=np.array([5, 3, 0, 0, 0], np.int32))
        plan = _plan(view, macro)
        cost = 0
        for op, arg, qty in _row(plan, O.TURN_PRESTOCK):
            if op == O.MO_BUY_PRODUCT:
                cost += int(quotes[arg, :qty].sum())
            else:
                cost += qty * int(spec.CROP_SEED_COST[arg])
        assert cost <= money, (money, cost)
        assert cost <= int(view.money) - int(P.cash_reserve(np, 0, 10)) or cost == 0


def test_the_prestock_respects_shed_room(on):
    """Wheat and fertilizer sit in the shed all night and compete with the eod
    dump for `SHED_CAPACITY`; a day whose own projection already fills it
    prestocks no product at all (seeds are not shed-bound and are unaffected)."""
    full = _view(day=10, n_coop=20, n_ripe=30, wheat=40, yld=8)
    row = _row(_plan(full, _macro()), O.TURN_PRESTOCK)
    assert all(op != O.MO_BUY_PRODUCT for op, _, _ in row), row


def test_a_terminal_tomorrow_prestocks_nothing(on):
    """`terminal` is `day > O.LAST_SHED_DAY`, so from `LAST_SHED_DAY` on there
    is no tomorrow that shops -- and day 29 buys nothing at all [LAW, 0.4]."""
    macro = _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))
    for day in (O.LAST_SHED_DAY, O.LAST_SHED_DAY + 1):
        view = _view(day=day, n_coop=6, wheat=6)
        assert _row(_plan(view, macro), O.TURN_PRESTOCK) == [], day
    # ... and the day before still does, so the bound is pinned from both sides.
    view = _view(day=O.LAST_SHED_DAY - 1, n_coop=6, wheat=6)
    assert _row(_plan(view, macro), O.TURN_PRESTOCK) != []


def test_the_prestock_plan_agrees_across_backends(on):
    """The switch is a Python constant and folds into the trace as a literal,
    but the rows it opens -- a market turn past `FULL_MARKET_TURNS`, a hire row
    selected between two turns, a route base of 1 -- are shapes the numpy path
    had no reason to build before, and the equivalence surface is the plan."""
    import jax
    import jax.numpy as jnp
    cases = [
        (_view(day=10), _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))),
        (_view(day=10, n_coop=8, wheat=8), _macro()),
        (_view(day=11, seeds=np.array([6, 0, 0, 0, 0], np.int32)),
         _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))),
        (_view(day=O.LAST_SHED_DAY, n_coop=6, wheat=6), _macro()),
    ]
    for view, macro in cases:
        a = P.build_day(np, view, macro)
        b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                        jax.tree_util.tree_map(jnp.asarray, macro),
                        jnp.asarray(spec.build_price_table()))
        for x, y in zip(a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {int(view.day)}"


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (buying tomorrow's feed tonight) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04: on day 0 the plan buys
#: `OPEN_PUMP_UNITS` wheat behind the hire row and sells it back from the BUY
#: row's head slot, to quote the class-A opening's own wheat off a drained pot.
#: It is pinned off for this file the way `0772ed3` pinned `EARLY_SELL_ON` off
#: for the modules it moved under: `plan` asserts OPEN_PUMP and PRESTOCK's
#: overflow hire row are mutually exclusive (both own turn 1), so the ON half
#: here cannot run with the new default live.
#: `tests/test_open_pump.py` owns both halves of the switch.
@pytest.fixture(autouse=True)
def _open_pump_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)
