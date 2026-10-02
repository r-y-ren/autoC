"""The lots are projected on the turns they are sold on [EARLY_SELL].

`sell.lot_inventories` built the three lots' curves at the constant
`O.SELL_TURNS = (3, 10, 18)` whatever `EARLY_SELL_MODE` said, while `_rows`
emitted them on `plan.early_lot_turns()`. Under mode "B" that priced lot 2
against a shelf drained by seven town ticks it never waits for: the greedy saw
a dearer-looking lot 1, put the day there, and what would not fit fell out of
the day into the hour-19 residue (`scratchpad/blueprint/report.md`, 282 units a
game). The fix threads the mode's own turns through `lot_inventories` and its
one caller in `plan._market`.

Mode "A" -- the shipped default -- has `early_lot_turns() == O.SELL_TURNS`, so
the fix is inert there, and the first half of this file is the pin that says
so: the whole six-array plan is byte-identical to the plan the pre-fix
projection builds, on every one of `test_route_early`'s seeded boards.
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
from test_early_sell import _day_total, _sell_rows, _stocked_view
from test_melon_open import _melon_view
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import projector as PJ
from kagg3.core import sell as S


def _pre_fix(monkeypatch):
    """Put the pre-fix projection back: the three lots at `O.SELL_TURNS`,
    whatever turns the caller asks for."""
    real = S.lot_inventories
    monkeypatch.setattr(S, "lot_inventories",
                        lambda xp, mkt_inv, shops, turns=None, day=None:
                        real(xp, mkt_inv, shops, day=day))
@pytest.fixture(autouse=True)
def _three_lots(monkeypatch):
    """This file's subject is the THREE-turn mode-"A" layout `O.SELL_TURNS`.

    `LOT4_ON` has shipped `True` at `LOT4_TURN = 17` since master `d3716e6`
    (`docs/strategy/2026-09-16-judge-baseline-rule.md`), so
    `early_lot_turns()` is `(3, 10, 17, 18)` by default and every assertion
    below about "the three lots" would be read against a four-lot day. Lot 4
    is pinned on its own by `tests/test_lot4.py`; here it is stated OFF in
    BOTH arms rather than assumed, which is also the honest reading of the
    docstring: with lot 4 shipped the projection fix is no longer inert in
    mode "A" -- it is what puts lot 4's curve on turn 17 -- and that is the
    fix working, not a regression.
    """
    monkeypatch.setattr(P, "LOT4_ON", False)




def _shops():
    """A town whose shops actually drain the shelf, so two projection turns
    are two different curves and not the same one twice. With no shop the
    whole day projects alike: `ticks_before` differs only in the shop tick
    over turns 3..18 (the town centre takes one tick before every one of
    them), so an empty town makes the defect invisible."""
    return np.full(spec.N_SHOPS, 3, np.int32)


def _contested_view():
    """A board on which the lot the greedy picks is a real question: a shelf
    the shops drain, an inventory on the live part of the curve, and stock in
    every product. With `press = 0` every unit goes to the last lot whatever
    the projection says (selling later is weakly better with no pressure), so
    the pressure is the point of the fixture and not decoration."""
    return _stocked_view()._replace(
        shops=_shops(),
        mkt_inv=np.full(spec.N_PRODUCTS, 1_000, np.int32))


def _contested_macro():
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32),
                  press=np.ones(spec.N_PRODUCTS, np.int32))


# =========================================================================
# mode "A": inert, to the byte
# =========================================================================

def test_mode_a_lot_turns_are_the_shipped_constant(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "A")
    assert P.early_lot_turns() == tuple(O.SELL_TURNS)


def test_default_turns_are_the_shipped_constant():
    """The argument's default is the old body, so every caller that does not
    pass turns (the tests, and any future one) reads the old curves."""
    inv = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 37 + 400
    sh = _shops()
    assert np.array_equal(S.lot_inventories(np, inv, sh),
                          S.lot_inventories(np, inv, sh, O.SELL_TURNS))


@pytest.mark.parametrize("seed", PIN_SEEDS)
def test_mode_a_plan_is_byte_identical_to_the_pre_fix_projection(seed, monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "A")
    view, macro = _seeded_case(seed)
    after = _digest(_plan(view, macro))
    _pre_fix(monkeypatch)
    assert _digest(_plan(view, macro)) == after


# =========================================================================
# mode "B": lot 2 is projected on turn 4, the turn it is sold on
# =========================================================================

def test_mode_b_lot2_projects_on_its_own_turn(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "B")
    turns = P.early_lot_turns()
    assert turns == (O.SELL_TURNS[0],) + tuple(O.EARLY_SELL_LATE_TURNS)

    inv = np.arange(spec.N_PRODUCTS, dtype=np.int32) * 37 + 400
    sh = _shops()
    il = S.lot_inventories(np, inv, sh, turns)
    for k, t in enumerate(turns):
        assert np.array_equal(il[k], PJ.projected_inv(np, inv, sh, t))
    # ... and it is a different shelf from the one the pre-fix body used.
    old = S.lot_inventories(np, inv, sh)
    assert np.array_equal(il[0], old[0])            # lot 1 never moved
    assert not np.array_equal(il[1], old[1])        # turn 4 vs turn 10
    assert not np.array_equal(il[2], old[2])        # turn 5 vs turn 18
    assert (il[1] > old[1]).any()                   # fewer ticks, fuller shelf


def test_mode_b_plan_moves_off_the_pre_fix_projection(monkeypatch):
    """The fix bites. On a contested board mode "B"'s plan is not the plan the
    pre-fix projection built -- lot 2 and lot 3 are now priced at turns 4 and
    5, which is a fuller (cheaper) shelf than the turn-10/18 curves the old
    body handed them, so the greedy's lot choice moves. What the truer curve
    is worth is an engine measurement, not something a unit test pins; what
    this pins is that the day still offers the same nine totals on the same
    lot turns -- the switch moves *when*, never what or how much."""
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "B")
    view, macro = _contested_view(), _contested_macro()
    after = _plan(view, macro)
    _pre_fix(monkeypatch)
    before = _plan(view, macro)
    assert _digest(after) != _digest(before)
    assert _day_total(after) == _day_total(before)
    assert set(_sell_rows(after)) <= set(P.early_lot_turns()) | {O.EARLY_SELL_LOT1_TURN}


# =========================================================================
# MELON_LOT_EARLY_ON: the dump day's rows, four turns earlier
# =========================================================================

def test_melon_lot_turns_read_the_switch_at_call_time(monkeypatch):
    """`setattr` after import is how the campaign harness sets a switch, so
    the turns cannot be captured at import."""
    assert P.melon_lot_turns() == tuple(O.MELON_LOT_TURNS)
    monkeypatch.setattr(P, "MELON_LOT_EARLY_ON", True)
    assert P.melon_lot_turns() == (6, 7, 8)
    assert P._midday_place_turn() == 6 + P.MIDDAY_PLACE_LOT


def test_early_melon_turns_keep_the_layout_law(monkeypatch):
    """The same three checks `ops._check_schedule` makes of the shipped tuple,
    against the turns the switch substitutes."""
    monkeypatch.setattr(P, "MELON_LOT_EARLY_ON", True)
    turns = P.melon_lot_turns()
    assert len(turns) == len(O.MELON_LOT_TURNS)
    assert O.FULL_MARKET_TURNS <= min(turns)
    assert max(turns) < O.SELL_TURNS[-1]
    assert not (set(turns) & (set(O.SELL_TURNS) | set(O.EARLY_SELL_LATE_TURNS)
                              | {O.TURN_PRESTOCK}))


def test_melon_rows_move_to_the_early_turns(monkeypatch):
    """The dump day's melon rows come out on the switch's turns, carrying the
    same units the shipped turns carried: hours 7/8/9 instead of 12/14/16."""
    monkeypatch.setattr(P, "MELON_OPEN_ON", True)
    view, macro = _melon_view(), _macro(crew_target=np.int32(6))
    late = _sell_rows(_plan(view, macro))
    monkeypatch.setattr(P, "MELON_LOT_EARLY_ON", True)
    early = _sell_rows(_plan(view, macro))

    def _melon(rows):
        return {t: r[spec.I_MELON] for t, r in rows.items()
                if spec.I_MELON in r and t not in P.early_lot_turns()}

    assert set(_melon(late)) == set(O.MELON_LOT_TURNS)
    assert set(_melon(early)) == set(P.MELON_LOT_EARLY_TURNS)
    assert ([_melon(early)[t] for t in sorted(_melon(early))]
            == [_melon(late)[t] for t in sorted(_melon(late))])
    assert sum(_melon(early).values()) > 0


@pytest.mark.parametrize("seed", PIN_SEEDS)
def test_early_melon_lots_are_inert_without_melon_open(seed, monkeypatch):
    """The switch moves rows that only `MELON_OPEN_ON` emits: `_market` builds
    `melon_lots` inside `if MELON_OPEN_ON`, and with the opening off the
    season's melon is sold through the ordinary three lots like any other
    product. So `MELON_LOT_EARLY_ON` alone is a no-op, to the byte -- it is
    the opening's clock, not a melon clock of its own, and it must be measured
    with `MELON_OPEN_ON=True` or not at all."""
    view, macro = _seeded_case(seed)
    assert not P.MELON_OPEN_ON
    off = _digest(_plan(view, macro))
    monkeypatch.setattr(P, "MELON_LOT_EARLY_ON", True)
    assert _digest(_plan(view, macro)) == off
