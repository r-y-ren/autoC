"""`plan.FERT_VOLUME_ON`: the fertilizer unit's opportunity cost.

The 2026-09-03 live study makes FERTILIZER our largest measured revenue gap
(median +7,306 a loss, opponents 321 units a season against our 180 at the same
realised price). The ledger says the leak is not collection and not the shed:
over four real-engine games against kagg2 the herd arms 428.8 animal-days, the
route collects 399.8 of them, the shed ends on 2.5 units -- and **173.8 units a
game go onto our own tiles**, against kagg2's 58.2. The 116-unit difference at
our own realised 54.8 coins is the gap.

ON charges the application for the unit it spends: the `fert_cand` gate asks
for `FERT_VOLUME_NUM/FERT_VOLUME_DEN` times the unit's quote instead of one
times it, and `v_fert` bids the *net* gain over selling into `_admit` instead
of the gross value. Fewer applications means a smaller `fert_reserved`, which
is what puts the units in the day's lots.

The `test_off_*` half is the identity half: off, the bar is the flat quote and
`v_fert` is the gross value, both the expressions this switch was cut into. The
digests are the whole six-array plan on `test_route_early`'s seeded boards,
taken off a clean `git archive 2170352` export -- the commit this switch was
cut into, with the promoted stack at its shipped default, which is what this
file's fixtures leave alone.
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
from test_route_early import (PIN_SEEDS, _digest, _plan, _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "FERT_VOLUME_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)


def _fert_cases():
    """Boards that hold plant tiles worth fertilizing, plus the seeded ones.

    `fert` stocks the shed so `n_fert_eff` is not the binding constraint and
    the gate is what decides; `n_ripe` plants the tiles.
    """
    for s in PIN_SEEDS:
        yield _seeded_case(s)
    for day in (6, 12, 18, 24):
        for fert in (4, 20):
            for n_ripe in (8, 24):
                yield (_view(day=day, money=20_000, fert=fert, n_ripe=n_ripe,
                             yld=3, n_coop=4),
                       _macro(crew_target=np.int32(6),
                              plant_target=np.asarray((3, 3, 2, 2, 0), np.int32),
                              hold=np.zeros(spec.N_PRODUCTS, np.int32)))


def _cheap_fert_cases(quote=30):
    """`_fert_cases`' stocked boards with the fertilizer quote walked down.

    Nothing else moves: only `price[I_FERT]`, which is what both halves of the
    switch read. A fresh market quotes fertilizer at its 100-coin base and the
    real one is at 40-55 by day 13 and 14-30 by day 29 (2026-08-30 profile), so
    the base-price fixtures are the *least* favourable board for an application
    and the mid-season ones are where the day's units are actually spent.
    """
    for day in (6, 12, 18, 24):
        for fert in (4, 20):
            for n_ripe in (8, 24):
                view = _view(day=day, money=20_000, fert=fert, n_ripe=n_ripe,
                             yld=3, n_coop=4)
                price = np.array(view.price, np.int32)
                price[spec.I_FERT] = quote
                yield (view._replace(price=price),
                       _macro(crew_target=np.int32(6),
                              plant_target=np.asarray((3, 3, 2, 2, 0), np.int32),
                              hold=np.zeros(spec.N_PRODUCTS, np.int32)))


def _n_op(plan, op):
    """How many unit-turns of `op` the compiled day walks."""
    unit_op = plan[0]
    return int(np.sum(np.asarray(unit_op) == op))


def _sold(plan):
    """{product: units} the day's lots offer, over every turn."""
    o, arg, qty = plan[3:6]
    out = {}
    for t in range(spec.TURNS_PER_DAY):
        for s in range(spec.MAX_MARKET_ORDERS):
            if int(o[t, s]) == O.MO_SELL:
                out[int(arg[t, s])] = out.get(int(arg[t, s]), 0) + int(qty[t, s])
    return out


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `PIN_SEEDS`, taken off the tree at
#: `2170352` -- the commit before this switch -- so they pin the pre-switch
#: planner and not this file's own output. Regenerate only with a measured
#: reason to move the plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_ignores_the_knobs(off, monkeypatch):
    """OFF the bar is the flat quote and `v_fert` the gross value, so neither
    knob is read: the compiled day is the same at any `NUM/DEN`."""
    cases = list(_cheap_fert_cases())
    base = [_digest(_plan(v, m)) for v, m in cases]
    for num, den in ((1, 1), (5, 1), (1, 7)):
        monkeypatch.setattr(P, "FERT_VOLUME_NUM", num)
        monkeypatch.setattr(P, "FERT_VOLUME_DEN", den)
        assert [_digest(_plan(v, m)) for v, m in cases] == base, (num, den)


def test_shipped_knobs_ask_for_more_than_off():
    """The shipped setting is a *higher* bar; at `NUM == DEN` the gate half of
    the switch would be inert and only the admit half would move."""
    assert P.FERT_VOLUME_NUM > P.FERT_VOLUME_DEN
    assert P.FERT_VOLUME_ON is False


# =========================================================================
# ON: fewer applications, and the freed units go to market
# =========================================================================

def test_on_never_fertilizes_more_than_off(monkeypatch):
    """The gate only ever rises, so no board gains an application."""
    cases = list(_fert_cases())
    monkeypatch.setattr(P, "FERT_VOLUME_ON", False)
    before = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    after = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    assert all(a <= b for a, b in zip(after, before)), list(zip(before, after))
    assert sum(after) < sum(before), (sum(before), sum(after))


def test_on_sells_at_least_as_much_fertilizer(monkeypatch):
    """The point of the switch: an application the gate drops leaves its unit
    unreserved, and `SELL.allocate` is what picks it up."""
    cases = list(_fert_cases())
    monkeypatch.setattr(P, "FERT_VOLUME_ON", False)
    before = [_sold(_plan(v, m)).get(spec.I_FERT, 0) for v, m in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    after = [_sold(_plan(v, m)).get(spec.I_FERT, 0) for v, m in cases]
    assert all(a >= b for a, b in zip(after, before)), list(zip(before, after))
    assert sum(after) > sum(before), (sum(before), sum(after))


def test_on_keeps_the_applications_that_clear_the_higher_bar(on):
    """Not a ban. The fixture boards all quote fertilizer at its 100-coin base,
    where two quotes is more than any tomato's three fires are worth -- which is
    the correct answer there and is why `_fert_cases` alone cannot show it. The
    board this switch is aimed at is the mid-season one, where the quote has
    walked down its own curve; at 30 coins the same tiles clear the higher bar
    and keep their applications."""
    kept = sum(_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in _cheap_fert_cases())
    assert kept > 0


def test_on_drops_fewer_applications_as_the_quote_falls(monkeypatch):
    """The gate is a *price*, not a day rule: the cheaper the unit is to sell,
    the more of the herd's output goes on our own tiles. Monotone in the quote,
    on the boards where OFF fertilizes at all."""
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    counts = [sum(_n_op(_plan(v, m), O.OP_FERTILIZE)
                  for v, m in _cheap_fert_cases(q))
              for q in (100, 60, 30, 10)]
    assert counts == sorted(counts), counts


def test_on_admit_value_is_net_of_the_unit(monkeypatch):
    """The switch's second half, isolated. With the knobs at 1/1 the gate is
    the OFF gate exactly, so every difference left in the compiled day is the
    admit stage bidding `fert_val - price` where it used to bid `fert_val` --
    and a lower bid can only lose a turn contest, never win one it lost."""
    cases = list(_cheap_fert_cases())
    monkeypatch.setattr(P, "FERT_VOLUME_ON", False)
    before = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    monkeypatch.setattr(P, "FERT_VOLUME_NUM", 1)
    monkeypatch.setattr(P, "FERT_VOLUME_DEN", 1)
    after = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    assert all(a <= b for a, b in zip(after, before)), list(zip(before, after))


def test_on_is_inert_when_the_knobs_are_one(monkeypatch):
    """The knobs' own identity: at `NUM == DEN` the gate is the OFF gate, so
    only the admit value moves -- which is what makes the two halves of the
    switch separable in a bisect."""
    cases = list(_fert_cases())
    monkeypatch.setattr(P, "FERT_VOLUME_ON", False)
    before = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    monkeypatch.setattr(P, "FERT_VOLUME_NUM", 1)
    monkeypatch.setattr(P, "FERT_VOLUME_DEN", 1)
    after = [_n_op(_plan(v, m), O.OP_FERTILIZE) for v, m in cases]
    # The gate is identical; any difference left is the admit stage dropping an
    # application for want of a turn, never adding one.
    assert all(a <= b for a, b in zip(after, before)), list(zip(before, after))


# =========================================================================
# MODES: which price the application is charged
# =========================================================================
#
# `FERT_VOLUME_MODE` picks the reference price the gate multiplies and `v_fert`
# subtracts. "spot" is the mode the 48-game table in plan.py measured, so it
# stays the default and ON with it is byte-identical to the switch as first
# cut. The other two exist because fertilizer's quote only ever walks down --
# it is the one product the town never drains -- so any multiple of the spot
# stops binding once the quote collapses.

TABLE = P.default_price_table()


def _ref(view, mode, monkeypatch):
    """`_fert_reference` under one mode, as an int."""
    monkeypatch.setattr(P, "FERT_VOLUME_MODE", mode)
    return int(P._fert_reference(np, view, TABLE))


def _mid_season(fert=0, inv_over=250, day=6):
    """A board whose quote, market inventory and shed agree with each other.

    `_cheap_fert_cases` walks `price[I_FERT]` down on its own and leaves
    `mkt_inv` on a fresh market, which is fine for the two modes that read the
    quote or the base but makes the marginal reference meaningless -- it is
    read off `mkt_inv`. Here the inventory is walked up `inv_over` units and
    the quote is the table entry at that inventory, which is the state the
    engine really presents from about day 13 on.
    """
    view = _view(day=day, money=20_000, fert=fert, n_ripe=24, yld=3, n_coop=4)
    inv = np.array(view.mkt_inv, np.int32)
    inv[spec.I_FERT] = spec.MARKET_I0 + inv_over
    price = np.array(view.price, np.int32)
    price[spec.I_FERT] = TABLE[spec.I_FERT, spec.MARKET_I0 + inv_over
                               - spec.PRICE_TABLE_LO]
    return view._replace(mkt_inv=inv, price=price)


def test_off_ignores_the_mode(off, monkeypatch):
    """The OFF identity, extended: OFF neither the gate nor `v_fert` reads the
    reference at all, so the mode cannot move a single compiled day."""
    cases = list(_cheap_fert_cases()) + [_seeded_case(s) for s in PIN_SEEDS]
    base = [_digest(_plan(v, m)) for v, m in cases]
    for mode in ("base", "marginal", "spot"):
        monkeypatch.setattr(P, "FERT_VOLUME_MODE", mode)
        assert [_digest(_plan(v, m)) for v, m in cases] == base, mode


def test_default_mode_is_the_measured_one():
    """ON at the shipped default is the behaviour plan.py's 48-game table
    documents, so a reader of that table and a reader of this file agree."""
    assert P.FERT_VOLUME_MODE == "spot"


def test_spot_reference_is_the_quote(monkeypatch):
    view = _mid_season()
    assert _ref(view, "spot", monkeypatch) == int(view.price[spec.I_FERT])


def test_base_reference_is_the_sell_floor_base(monkeypatch):
    """`"base"` reads the very number `_sell_hold` reads under FERT_FLOOR_ON:
    the quote at the opening inventory of this game's market draw."""
    got = _ref(_mid_season(), "base", monkeypatch)
    assert got == int(TABLE[spec.I_FERT, P._I0_COL])
    assert got == int(TABLE[spec.I_FERT, spec.MARKET_I0 - spec.PRICE_TABLE_LO])


def test_base_reference_does_not_fall_with_the_quote(monkeypatch):
    """The whole point of the mode. The spot loses more than half its value
    over the same walk; the base does not move at all."""
    spots = [_ref(_mid_season(inv_over=k), "spot", monkeypatch)
             for k in (0, 100, 250, 400)]
    bases = [_ref(_mid_season(inv_over=k), "base", monkeypatch)
             for k in (0, 100, 250, 400)]
    assert spots == sorted(spots, reverse=True) and spots[-1] * 2 < spots[0]
    assert len(set(bases)) == 1


def test_marginal_reference_never_exceeds_the_quote(monkeypatch):
    """It is the quote of the *next* unit, so it can only be at or below the
    quote of the first one -- the honest opportunity cost is the lowest of the
    three bars, which is why this mode fertilizes at least as much as spot."""
    for fert in (0, 5, 20, 60):
        view = _mid_season(fert=fert)
        assert (_ref(view, "marginal", monkeypatch)
                <= _ref(view, "spot", monkeypatch)), fert


def test_marginal_reference_falls_as_the_shed_fills(monkeypatch):
    """Every unit already queued walks the curve down one step, so the unit an
    application would spend is worth less the more of them there are."""
    got = [_ref(_mid_season(fert=f), "marginal", monkeypatch)
           for f in (0, 10, 40, 90)]
    assert got == sorted(got, reverse=True) and got[0] > got[-1]


def test_modes_are_ordered_mid_season(monkeypatch):
    """base >= spot >= marginal, on the board the switch is aimed at."""
    view = _mid_season(fert=20)
    b = _ref(view, "base", monkeypatch)
    s = _ref(view, "spot", monkeypatch)
    m = _ref(view, "marginal", monkeypatch)
    assert b > s > m, (b, s, m)


def test_base_mode_fertilizes_no_more_than_spot(monkeypatch):
    """A higher reference is a higher bar and a lower admit bid, both of which
    only ever drop an application."""
    cases = [_mid_season(fert=f, inv_over=k)
             for f in (4, 20, 60) for k in (0, 150, 200, 300, 450)]
    macro = _macro(crew_target=np.int32(6),
                   plant_target=np.asarray((3, 3, 2, 2, 0), np.int32),
                   hold=np.zeros(spec.N_PRODUCTS, np.int32))
    monkeypatch.setattr(P, "FERT_VOLUME_ON", True)
    monkeypatch.setattr(P, "FERT_VOLUME_MODE", "spot")
    spot = [_n_op(_plan(v, macro), O.OP_FERTILIZE) for v in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_MODE", "base")
    base = [_n_op(_plan(v, macro), O.OP_FERTILIZE) for v in cases]
    monkeypatch.setattr(P, "FERT_VOLUME_MODE", "marginal")
    marg = [_n_op(_plan(v, macro), O.OP_FERTILIZE) for v in cases]
    assert all(b <= s for b, s in zip(base, spot)), list(zip(base, spot))
    assert all(m >= s for m, s in zip(marg, spot)), list(zip(marg, spot))
    # Both inequalities are strict somewhere in this set: at a 100-coin base
    # two bases is more than any tomato's three fires are worth, so `"base"`
    # bans the application outright, while at a 60-unit shed the marginal unit
    # is quoted 12 coins under the first one and the same tiles clear the
    # lower bar the honest opportunity cost sets.
    assert sum(base) < sum(spot) < sum(marg), (sum(base), sum(spot), sum(marg))


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03 (commit 0772ed3): the
#: day's first lot rides turn 1 behind the BUY row instead of standing on
#: `O.SELL_TURNS[0]`. This file's PIN digests were taken before that, so the
#: switch is pinned off here the way `a838700`'s stack was pinned off for the
#: digest fixtures; `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04 (commit ff3fe12): on
#: day 0 the plan buys `OPEN_PUMP_UNITS` wheat behind the hire row and sells it
#: back from the BUY row's head slot. The PIN digests above predate it, so it
#: is pinned off here like `EARLY_SELL_ON`; `tests/test_open_pump.py` owns
#: both halves of the switch.
@pytest.fixture(autouse=True)
def _open_pump_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "OPEN_PUMP_ON", False)


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
