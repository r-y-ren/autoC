"""`plan.LOT_SPLIT_ON`: cap the units one product may put in one sell lot.

LOT-DEPTH (`docs/strategy/2026-09-14-lot-depth.md`). Every product quotes off
a monotone curve in the market inventory (`spec.py:111-169`) and a SELL walks
that quote DOWN unit by unit (`sim/market.py:69-76`), so a lot -- which is one
market order of `lots[l][p]` units -- pays for its own depth. WHEAT-REBUY §2
measured the bill: unit-weighted, ymg_aq clears +0.99/unit above the dawn
quote and we clear -0.51, and our day-29 liquidation alone puts ~64.6 units
through one row at -3.82.

The switch is the counter-experiment to `SELL.allocate`'s `press` term: cap
the units per lot, spread the rest over the day's other lots, keep the day's
total for the product exactly where it was.
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

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import sell as SELL

ND = spec.N_DAYS


def _view(money=9000, nquad=1, day=8, shed=None):
    """A blank board: every tile free, nothing planted, `shed` in the shed."""
    z = np.zeros(100, np.int32)
    sh = np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed
    return P.DayView(
        day=np.int32(day),
        kind=np.full(100, spec.KIND_EMPTY, np.int32), occ=z - 1,
        t_day=z.copy(), t_water=z.copy(), t_cons=z.copy(), t_yield=z.copy(),
        t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=sh, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(money), nquad=np.int32(nquad),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _macro(**kw):
    base = {
        "plant_target": np.zeros(spec.N_CROPS, np.int32),
        "animal_want": np.zeros(spec.N_ANIMALS, np.int32),
        "land_bias": np.int32(0),
        "hold": np.full(spec.N_PRODUCTS, 10_000, np.int32),
        "press": np.zeros(spec.N_PRODUCTS, np.int32),
        "grow_mult": np.full(spec.N_PRODUCTS, brain.GROW_ONE, np.int32),
        "compact": np.int32(0),
        "dev_weight": np.int32(brain.GROW_ONE),
        "hire_bias": np.int32(0),
        "crew_target": np.int32(0),
        "animal_defer": np.int32(0),
        "forward_days": np.int32(0),
    }
    # [g12] Appended after the pins in `tests/test_fertengine.py` were cut, and
    # those run this helper against a pristine PRE-`g12` `src` tree in a
    # subprocess -- so the field is named only when the planner has it.
    if "fert_defer" in P.Macro._fields:
        base["fert_defer"] = np.int32(0)
    base.update(kw)
    return P.Macro(**base)


@pytest.fixture
def off():
    """Restore the module globals whatever a test did to them."""
    was = (P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS)
    yield
    P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = was


def _plan(view, macro):
    return [np.asarray(x) for x in P.build_day(np, view, macro)]


def _sell_view(day=8, money=9000, units=90, product=spec.I_STRAWBERRY):
    """A board with one product in the shed and nothing else to do with it.

    90 units is under `SHED_CAPACITY` (100), so nothing overflows and the
    whole stock is the allocator's VOLUNTARY sale -- which is the only thing
    the switch reshapes.
    """
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[product] = units
    return _view(money=money, day=day, shed=shed)


def _sell_macro(press=0):
    """`hold` 0 sells everything; `press` is the lot-timing term the switch is
    the counter-experiment to -- a large one collapses the day into lot 1."""
    return _macro(plant_target=np.array([8, 0, 0, 0, 0], np.int32),
                  hold=np.zeros(spec.N_PRODUCTS, np.int32),
                  press=np.full(spec.N_PRODUCTS, press, np.int32))


def _sell_turns(view, macro, product):
    """`{turn: units}` for every SELL row of `product` in the day plan."""
    op, a, q = _plan(view, macro)[3:6]
    out = {}
    for t in range(op.shape[0]):
        n = int(q[t][(op[t] == O.MO_SELL) & (a[t] == product)].sum())
        if n:
            out[t] = n
    return out


def test_lot_split_is_off_in_the_shipped_program():
    """The three constants exist and the shipped program is the one without
    them: `LOT_SPLIT_ON` False and a cap that is inert even if it were on."""
    assert P.LOT_SPLIT_ON is False
    assert P.LOT_SPLIT_MAX == 0
    assert P.LOT_SPLIT_DAYS == ()


def test_off_identity_over_the_whole_plan_tuple(off):
    """OFF is character-identical on a fixed board -- and stays identical with
    the SIZE and the DAY window set, because only `LOT_SPLIT_ON` opens the
    site. Pinned over every array of the plan tuple, not only the sell rows."""
    view, macro = _sell_view(), _sell_macro(press=4)
    base = _plan(view, macro)
    for cap, days in ((20, ()), (20, (8,)), (1, ()), (40, (8, 29))):
        P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = cap, days
        P.LOT_SPLIT_ON = False
        got = _plan(view, macro)
        assert len(got) == len(base)
        for k, (b, g) in enumerate(zip(base, got)):
            assert np.array_equal(b, g), f"array {k} moved at cap {cap} {days}"
    # ON with a cap of 0 is the same statement from the other side: the switch
    # is open and the cap refuses to bind.
    P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = True, 0, ()
    for k, (b, g) in enumerate(zip(base, _plan(view, macro))):
        assert np.array_equal(b, g), f"array {k} moved at cap 0"


def test_on_splits_a_one_lot_sale_into_more_lots(off):
    """A `press` large enough to collapse the day into ONE lot is exactly the
    case the switch exists for: the cap puts the sale back on three rows."""
    view, macro = _sell_view(), _sell_macro(press=50)
    base = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert len(base) == 1, f"the fixture no longer sells in one lot: {base}"
    P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = True, 20, ()
    got = _sell_turns(view, macro, spec.I_STRAWBERRY)
    assert len(got) > len(base), f"the cap did not split the lot: {got}"
    assert len(got) == SELL.N_LOTS, f"90 units at cap 20 wants every lot: {got}"


def test_the_cap_is_respected_while_the_lots_have_room(off):
    """No lot stands above `LOT_SPLIT_MAX` while the day's total fits under
    `N_LOTS * LOT_SPLIT_MAX`; past that the residue rides the LAST lot, and
    nothing else does."""
    P.LOT_SPLIT_ON, P.LOT_SPLIT_DAYS = True, ()
    for cap, units in ((20, 50), (40, 90), (10, 25), (35, 90)):
        view, macro = _sell_view(units=units), _sell_macro(press=50)
        P.LOT_SPLIT_MAX = cap
        rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
        assert sum(rows.values()) == units, f"cap {cap}: {rows}"
        turns = sorted(rows)
        for t in turns[:-1]:
            assert rows[t] <= cap, f"cap {cap} broken on turn {t}: {rows}"
        over = max(units - cap * SELL.N_LOTS, 0)
        assert rows[turns[-1]] <= cap + over, \
            f"cap {cap}: the last lot carries more than the residue: {rows}"


def test_no_unit_is_lost_and_no_unit_is_added(off):
    """`s_qty` is what the overflow deficit and every downstream bulk add are
    computed off, so the day's total per product must be identical ON and OFF.
    Checked on a shed that never fills, over every cap and both day forms."""
    for units in (30, 60, 90):
        view, macro = _sell_view(units=units), _sell_macro(press=50)
        base = _sell_turns(view, macro, spec.I_STRAWBERRY)
        total = sum(base.values())
        assert total == units, f"the fixture holds units back: {base}"
        for cap in (1, 5, 20, 31, 40, 100):
            for days in ((), (8,)):
                P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = True, cap, days
                rows = _sell_turns(view, macro, spec.I_STRAWBERRY)
                assert sum(rows.values()) == total, \
                    f"cap {cap} days {days} moved volume: {rows} vs {base}"


def test_the_day_window_is_the_only_day_the_cap_binds(off):
    """`LOT_SPLIT_DAYS` is a day list, not a start day: a day outside it is
    byte-identical to OFF, a day inside it is the capped plan."""
    view, macro = _sell_view(day=8), _sell_macro(press=50)
    base = _plan(view, macro)
    P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX = True, 20
    P.LOT_SPLIT_DAYS = (29,)
    for k, (b, g) in enumerate(zip(base, _plan(view, macro))):
        assert np.array_equal(b, g), f"array {k} moved on a day outside the window"
    P.LOT_SPLIT_DAYS = (8, 29)
    assert len(_sell_turns(view, macro, spec.I_STRAWBERRY)) == SELL.N_LOTS


def test_every_product_walks_its_own_quote_down(off):
    """The structure the switch is aimed at is universal: `market_price` is
    monotone in `I0 - inventory` for all nine products below `I0`, so a SELL
    of n units always clears strictly below n times the first quote -- and the
    cap therefore has something to buy on every one of them."""
    for p, name in enumerate(spec.PRODUCTS):
        first = spec.market_price(name, 9_900)
        last = spec.market_price(name, 9_900 + 40)
        assert last <= first, f"{name} does not walk down"
        assert last < first, f"{name} is flat over 40 units: {first} {last}"
        view = _sell_view(units=90, product=p)
        macro = _sell_macro(press=50)
        base = _sell_turns(view, macro, p)
        P.LOT_SPLIT_ON, P.LOT_SPLIT_MAX, P.LOT_SPLIT_DAYS = True, 20, ()
        got = _sell_turns(view, macro, p)
        P.LOT_SPLIT_ON = False
        assert sum(got.values()) == sum(base.values()), f"{name}: volume moved"
        if sum(base.values()) > 20:
            assert len(got) >= len(base), f"{name}: the cap lost a lot: {got}"
