"""`plan.EARLY_SELL_ON`: the same lots, earlier in the day.

The 2026-09-03 strategy study's largest single lever, read straight out of
`_process_market`: each *seat's* queue is truncated to ten orders a turn (HIRE
and BUY_LAND are queue entries and count against the ten), the two seats'
SELL/BUY orders inside one turn are quoted off one pre-commit inventory and
committed in per-unit lockstep -- so a shared turn splits the curve evenly and
the only way to be first is to sell in an earlier turn -- and yesterday's
harvest is already in the shed at hour 0. Every recorded opponent's flow lands
at hours 10-17; ours left at hours 4, 11 and 19.

The switch moves **when**, never what or how much. `test_on_daily_total_*` is
the half that says so: the nine per-product day totals are identical ON and
OFF on every fixture board, mode A and mode B alike.

The `test_off_*` half is the identity half: off, `early_fits` is `None`, the
three lots go out on `O.SELL_TURNS` and the BUY row is the row it always was.
The digests are the whole six-array plan on `test_route_early`'s seeded boards,
taken off the tree at `73c5b8a` -- the commit this switch was cut into, with
the promoted stack (DROP, HORIZON_DROP, ROUTE_SPLIT, SURVIVAL_WATER, TAIL_CARE,
FEED_MANDATORY) at its shipped default, which is what this file's fixtures
leave alone.
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
from test_route_early import (PIN_SEEDS, _acting_units, _digest, _plan, _row,
                              _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import projector as PJ
from kagg3.core import plan as P


@pytest.fixture(autouse=True)
def _three_lots(monkeypatch):
    """Every mode in this file lays out THREE lots, which is what its cases
    count and where its `PIN` was taken.

    `LOT4_ON` has shipped `True` at `LOT4_TURN = 17` since master `d3716e6`
    (`docs/strategy/2026-09-16-judge-baseline-rule.md`), so
    `early_lot_turns()` carries a fourth turn by default and a case that says
    "its three lots" would be read against a four-lot day. Lot 4 is pinned on
    its own by `tests/test_lot4.py`, which is where the four-lot layout
    belongs; here the three-lot layout is STATED in both arms instead of
    assumed from a default that has since moved.
    """
    monkeypatch.setattr(P, "LOT4_ON", False)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


@pytest.fixture
def mode_a(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "A")


@pytest.fixture
def mode_b(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", "B")


#: Every variant the switch admits. The two invariants that hold for all of
#: them -- the day's totals and the engine's ten-order cap -- are parametrised
#: over this list, so a new mode is tested the day it is written.
MODES = ("A", "A1", "A0", "A21", "B", "Z", "Z1")


@pytest.fixture(params=MODES)
def any_mode(request, monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", request.param)
    return request.param


def _on(monkeypatch, mode):
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", mode)


def _n_hire(plan, turn=O.TURN_HIRE):
    """Hands asked for on a turn -- the row lot 1 has to fit behind in "A0"."""
    return len([1 for op, _, _ in _row(plan, turn) if op == O.MO_HIRE])


def _kinds(plan, turn):
    """The op codes of one market turn's live orders, in slot order."""
    return [op for op, _, _ in _row(plan, turn)]


def _z_hire_turn(plan):
    """Which turn a mode "Z" plan hired on: turn 1 on a Z day, turn 0 on the
    wide day Z hands back to mode A."""
    return (O.EARLY_SELL_Z_HIRE_TURN
            if _n_hire(plan, O.EARLY_SELL_Z_HIRE_TURN) else O.TURN_HIRE)


#: A board with stock in the shed on every product, so the lots are wide and
#: the fit against the BUY row's ten slots is a real question and not a
#: formality.
def _stocked_view(day=12, money=20_000, per=8, **kw):
    view = _view(day=day, money=money, **kw)
    shed = np.array(view.shed, np.int32)
    shed[:spec.N_PRODUCTS] = per
    return view._replace(shed=shed)


def _sell_rows(plan):
    """{turn: {product: units}} over every turn that carries a SELL."""
    op, arg, qty = plan[3:6]
    out = {}
    for t in range(spec.TURNS_PER_DAY):
        row = {int(arg[t, s]): int(qty[t, s])
               for s in range(spec.MAX_MARKET_ORDERS)
               if int(op[t, s]) == O.MO_SELL}
        if row:
            out[t] = row
    return out


def _day_total(plan):
    """product -> units the day offers, summed over every turn."""
    tot = {}
    for row in _sell_rows(plan).values():
        for item, n in row.items():
            tot[item] = tot.get(item, 0) + n
    return tot


def _cases():
    """The seeded boards, plus stocked ones that force wide lots."""
    for s in PIN_SEEDS:
        yield _seeded_case(s)
    for per in (2, 8, 20):
        for wheat in (0, 12):
            yield (_stocked_view(per=per, wheat=wheat, n_ripe=12, n_coop=4),
                   _macro(crew_target=np.int32(6),
                          plant_target=np.asarray((3, 3, 2, 2, 0), np.int32),
                          hold=np.zeros(spec.N_PRODUCTS, np.int32)))


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Digests of the whole six-array plan on `test_route_early.PIN_SEEDS`, taken
#: off the tree at `73c5b8a` -- the commit before this switch -- so they pin
#: the pre-switch planner and not this file's own output. Regenerate only with
#: a measured reason to move the plan.
PIN = ("d4e7ca576cf7637f", "0b627c03c8178ccd", "5702eea5c8c6dee5", "ab85fff4377b3226",
       "46fecb48d2b8dd89", "9561fdea3e750fe6", "0b353de010dd650e", "b6ae535acf30126a",
       "2983c0382f4ce20a", "27dc7659bfa8076b", "7936ac26399f166e", "c01dd4d7169c0098")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_sells_only_on_the_shipped_turns(off):
    """Three lots, on `O.SELL_TURNS`, and nothing on the BUY row."""
    for view, macro in _cases():
        turns = set(_sell_rows(_plan(view, macro)))
        assert turns <= set(O.SELL_TURNS), turns


# =========================================================================
# ON: the lots leave earlier
# =========================================================================

def test_on_emits_the_first_lot_on_the_buy_row(mode_a):
    """Lot 1 leaves turn 3 for `O.EARLY_SELL_LOT1_TURN` -- turn 1, recorded
    hour 2 -- on every board whose purchases leave it room."""
    moved = 0
    for view, macro in _cases():
        rows = _sell_rows(_plan(view, macro))
        assert min(rows, default=O.EARLY_SELL_LOT1_TURN) >= O.EARLY_SELL_LOT1_TURN
        if O.EARLY_SELL_LOT1_TURN in rows:
            moved += 1
            # And it really is the first lot: nothing sells before it.
            assert min(rows) == O.EARLY_SELL_LOT1_TURN
    assert moved, "no board moved its first lot"


def test_on_mode_b_finishes_the_day_before_hour_seven(mode_b):
    """Mode B's whole flow is out by `O.EARLY_SELL_LATE_TURNS[-1]` -- recorded
    hour 6 -- which is in front of every recorded opponent's hour-10-to-17
    window."""
    allowed = ({O.EARLY_SELL_LOT1_TURN, O.SELL_TURNS[0]}
               | set(O.EARLY_SELL_LATE_TURNS))
    for view, macro in _cases():
        turns = set(_sell_rows(_plan(view, macro)))
        assert turns <= allowed, turns
        assert max(turns, default=0) + 1 <= 6


@pytest.mark.parametrize("mode", MODES)
def test_on_daily_total_sold_is_unchanged(monkeypatch, mode):
    """The one thing the switch may not do. Same nine products, same units, on
    every fixture board -- only the turn they go out on moves."""
    cases = list(_cases())
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)
    before = [_day_total(_plan(v, m)) for v, m in cases]
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", mode)
    after = [_day_total(_plan(v, m)) for v, m in cases]
    for i, (b, a) in enumerate(zip(before, after)):
        assert b == a, (i, b, a)


@pytest.mark.parametrize("mode", MODES)
def test_on_never_asks_for_more_than_the_engine_takes(monkeypatch, mode):
    """`_process_market` truncates each seat's queue to ten orders a turn and
    says nothing about it. The merged BUY-plus-lot row is the one place in the
    schedule where two variable-width rows share a turn, so the cap is checked
    on every board rather than argued from the layout."""
    monkeypatch.setattr(P, "EARLY_SELL_ON", True)
    monkeypatch.setattr(P, "EARLY_SELL_MODE", mode)
    for view, macro in _cases():
        plan = _plan(view, macro)
        for t in range(spec.TURNS_PER_DAY):
            n = len(_row(plan, t))
            assert n <= spec.MAX_MARKET_ORDERS, (t, n)


def test_on_keeps_the_purchases_in_front_of_the_lot(mode_a):
    """Order inside the merged row: every buy, then every sell. A sell in
    front of a `BUY_PRODUCT` would move the inventory the buy quotes against,
    and the day's purchases were budgeted at the price they always met."""
    for view, macro in _cases():
        row = _row(_plan(view, macro), O.EARLY_SELL_LOT1_TURN)
        kinds = [op for op, _, _ in row]
        if O.MO_SELL not in kinds:
            continue
        first_sell = kinds.index(O.MO_SELL)
        assert all(k == O.MO_SELL for k in kinds[first_sell:]), kinds
        assert all(k != O.MO_SELL for k in kinds[:first_sell]), kinds


def test_on_falls_back_to_the_shipped_turn_when_the_row_is_full(mode_a):
    """A day whose BUY row is busy cannot also carry a nine-wide lot, and the
    engine would eat the overflow in silence. The lot stays on
    `O.SELL_TURNS[0]` then -- checked by construction, on a board built to buy
    every seed, both products and every animal kind."""
    view = _stocked_view(day=6, money=200_000, per=20, n_coop=2, n_ripe=6)
    macro = _macro(crew_target=np.int32(6),
                   hold=np.zeros(spec.N_PRODUCTS, np.int32),
                   plant_target=np.asarray((4, 4, 4, 4, 4), np.int32),
                   animal_want=np.asarray((3, 3, 3), np.int32))
    plan = _plan(view, macro)
    rows = _sell_rows(plan)
    n_buy = len([1 for op, _, _ in _row(plan, O.TURN_BUY)
                 if op not in (O.MO_NONE, O.MO_SELL)])
    if n_buy + spec.N_PRODUCTS > spec.MAX_MARKET_ORDERS:
        assert O.SELL_TURNS[0] in rows or not rows, rows
    # Whatever the board did, the cap holds and the day total is the day total.
    assert all(len(_row(plan, t)) <= spec.MAX_MARKET_ORDERS
               for t in range(spec.TURNS_PER_DAY))


# =========================================================================
# The later variants: where lot 1 goes, and where lot 2 follows it
# =========================================================================

def test_on_every_mode_sells_no_earlier_than_its_first_lot_turn(any_mode):
    """No lot ever lands in front of the turn the mode reserves for lot 1, and
    no mode invents a SELL turn the schedule does not know about."""
    firstt = (O.TURN_HIRE
              if any_mode in (P.EARLY_SELL_MODES_HIRE_ROW
                              + P.EARLY_SELL_MODES_ZERO_ROW)
              else O.EARLY_SELL_LOT1_TURN)
    allowed = ({O.TURN_HIRE, O.EARLY_SELL_LOT1_TURN} | set(O.SELL_TURNS)
               | set(O.EARLY_SELL_LATE_TURNS))
    for view, macro in _cases():
        turns = set(_sell_rows(_plan(view, macro)))
        assert turns <= allowed, (any_mode, turns)
        assert min(turns, default=firstt) >= firstt, (any_mode, turns)


def test_on_mode_a1_puts_the_lot_in_front_of_the_purchases(monkeypatch):
    """A1 is A with the two halves of the merged row swapped: the lot
    compacted to the front, the day's buys behind it. Mode A's own
    `test_on_keeps_the_purchases_in_front_of_the_lot` is the mirror of this,
    and between them they pin that the order is a choice and not an accident."""
    _on(monkeypatch, "A1")
    seen = 0
    for view, macro in _cases():
        row = _row(_plan(view, macro), O.EARLY_SELL_LOT1_TURN)
        kinds = [op for op, _, _ in row]
        if O.MO_SELL not in kinds or set(kinds) == {O.MO_SELL}:
            continue
        seen += 1
        last_sell = len(kinds) - 1 - kinds[::-1].index(O.MO_SELL)
        assert all(k == O.MO_SELL for k in kinds[:last_sell + 1]), kinds
        assert all(k != O.MO_SELL for k in kinds[last_sell + 1:]), kinds
    assert seen, "no board merged a lot with a live purchase"


def test_on_mode_a1_carries_the_same_orders_as_mode_a(monkeypatch):
    """Swapping the halves may not change what the row asks for -- same buys,
    same sells, same quantities, only the slot sequence differs."""
    cases = list(_cases())
    _on(monkeypatch, "A")
    a = [sorted(_row(_plan(v, m), O.EARLY_SELL_LOT1_TURN)) for v, m in cases]
    _on(monkeypatch, "A1")
    a1 = [sorted(_row(_plan(v, m), O.EARLY_SELL_LOT1_TURN)) for v, m in cases]
    assert a == a1


def test_on_mode_a0_rides_the_hire_row_when_the_hires_leave_room(monkeypatch):
    """A0's rule, checked board by board against the engine's ten: the lot is
    on turn 0 exactly when `n_hire + n_sell <= 10`, on the merged BUY row when
    it is not but the purchases leave room, and on the shipped `SELL_TURNS[0]`
    when neither can hold it."""
    cases = list(_cases())
    _on(monkeypatch, "A")
    n_sell = [len(_sell_rows(_plan(v, m)).get(O.EARLY_SELL_LOT1_TURN, {}))
              or len(_sell_rows(_plan(v, m)).get(O.SELL_TURNS[0], {}))
              for v, m in cases]
    _on(monkeypatch, "A0")
    on_hire = 0
    for (view, macro), n_s in zip(cases, n_sell):
        plan = _plan(view, macro)
        rows = _sell_rows(plan)
        if not rows:
            continue
        n_h = _n_hire(plan)
        if n_h + n_s <= spec.MAX_MARKET_ORDERS:
            assert O.TURN_HIRE in rows, (n_h, n_s, sorted(rows))
            assert min(rows) == O.TURN_HIRE
            on_hire += 1
        else:
            assert O.TURN_HIRE not in rows, (n_h, n_s, sorted(rows))
    assert on_hire, "no board put its lot on the hire row"


def test_on_mode_a0_keeps_the_hires_in_front_of_the_lot(monkeypatch):
    """HIRE is atomic and resolves at the head of its slot round, but the row
    is still walked in slot order and a hand hired behind a sale is a hand
    hired late. Hires first, the lot compacted directly behind them."""
    _on(monkeypatch, "A0")
    seen = 0
    for view, macro in _cases():
        row = _row(_plan(view, macro), O.TURN_HIRE)
        kinds = [op for op, _, _ in row]
        assert set(kinds) <= {O.MO_HIRE, O.MO_SELL}, kinds
        if O.MO_HIRE in kinds and O.MO_SELL in kinds:
            seen += 1
        first_sell = kinds.index(O.MO_SELL) if O.MO_SELL in kinds else len(kinds)
        assert all(k == O.MO_HIRE for k in kinds[:first_sell]), kinds
    assert seen, "no board hired and sold on the same turn"


def test_on_mode_a21_moves_lot_two_and_leaves_lot_three(monkeypatch):
    """A21 = A's lot 1, lot 2 up to `O.EARLY_SELL_LATE_TURNS[0]`, lot 3 left on
    the shipped last turn. B's turn 5 is never used."""
    _on(monkeypatch, "A21")
    assert P.early_lot_turns() == (O.SELL_TURNS[0], O.EARLY_SELL_LATE_TURNS[0],
                                   O.SELL_TURNS[-1])
    allowed = {O.EARLY_SELL_LOT1_TURN, O.SELL_TURNS[0],
               O.EARLY_SELL_LATE_TURNS[0], O.SELL_TURNS[-1]}
    for view, macro in _cases():
        turns = set(_sell_rows(_plan(view, macro)))
        assert turns <= allowed, turns
        assert O.SELL_TURNS[1] not in turns


#: Where each mode is meant to put three live lots, straight at `_market`.
#: `core.sell` gives the fixture boards a single live lot, so the board-level
#: tests above cannot see lots 2 and 3 move at all; this one hands the row
#: builder three lots and reads the turns off the answer.
_WHERE = {
    "A":   (O.EARLY_SELL_LOT1_TURN, O.SELL_TURNS[1], O.SELL_TURNS[2]),
    "A1":  (O.EARLY_SELL_LOT1_TURN, O.SELL_TURNS[1], O.SELL_TURNS[2]),
    "A0":  (O.TURN_HIRE, O.SELL_TURNS[1], O.SELL_TURNS[2]),
    "A21": (O.EARLY_SELL_LOT1_TURN, O.EARLY_SELL_LATE_TURNS[0], O.SELL_TURNS[2]),
    "B":   (O.EARLY_SELL_LOT1_TURN, O.EARLY_SELL_LATE_TURNS[0],
            O.EARLY_SELL_LATE_TURNS[1]),
    "Z":   (O.EARLY_SELL_Z_LOT_TURN, O.SELL_TURNS[1], O.SELL_TURNS[2]),
    # `_market` is called here without the `z_heavy` the caller derives, so Z1
    # reads as an ungated Z -- which is the contract: the DAY owns the gate,
    # because it is the thing that fixed `route_base` on it.
    "Z1":  (O.EARLY_SELL_Z_LOT_TURN, O.SELL_TURNS[1], O.SELL_TURNS[2]),
}


def test_on_each_mode_puts_its_three_lots_where_it_says(any_mode):
    """Three live lots, an empty day otherwise (no hires, no purchases), so
    every lot has a whole row to itself and the turn it lands on is the mode's
    rule and nothing else. Quantities travel with the turn: lot k's units are
    lot k's wherever it goes."""
    z5, z3 = np.zeros(spec.N_CROPS, np.int32), np.zeros(spec.N_ANIMALS, np.int32)
    lots = np.zeros((3, spec.N_PRODUCTS), np.int32)
    lots[0, 0], lots[1, 1], lots[2, 2] = 5, 6, 7
    op, arg, qty = P._market(np, np.int32(0), np.int32(0), z5, z3, np.int32(0),
                             lots, np.int32(0))
    rows = _sell_rows((None, None, None, op, arg, qty))
    assert sorted(rows) == sorted(_WHERE[any_mode]), (any_mode, sorted(rows))
    for k, turn in enumerate(_WHERE[any_mode]):
        assert rows[turn] == {k: int(lots[k, k])}, (any_mode, turn, rows[turn])


def test_off_puts_its_three_lots_on_the_shipped_turns(off):
    """The same probe with the switch off: `O.SELL_TURNS`, as always."""
    z5, z3 = np.zeros(spec.N_CROPS, np.int32), np.zeros(spec.N_ANIMALS, np.int32)
    lots = np.zeros((3, spec.N_PRODUCTS), np.int32)
    lots[0, 0], lots[1, 1], lots[2, 2] = 5, 6, 7
    op, arg, qty = P._market(np, np.int32(0), np.int32(0), z5, z3, np.int32(0),
                             lots, np.int32(0))
    assert sorted(_sell_rows((None, None, None, op, arg, qty))) == list(O.SELL_TURNS)


def test_on_every_mode_falls_back_when_no_early_row_has_room(any_mode):
    """A day that buys every seed, both products and every animal kind fills
    the BUY row on its own, and one that also hires a full crew fills turn 0.
    The lot then keeps `O.SELL_TURNS[0]`, and the day's totals still hold."""
    view = _stocked_view(day=6, money=200_000, per=20, n_coop=2, n_ripe=6)
    macro = _macro(crew_target=np.int32(10),
                   hold=np.zeros(spec.N_PRODUCTS, np.int32),
                   plant_target=np.asarray((4, 4, 4, 4, 4), np.int32),
                   animal_want=np.asarray((3, 3, 3), np.int32))
    plan = _plan(view, macro)
    rows = _sell_rows(plan)
    n_buy = len([1 for op, _, _ in _row(plan, O.TURN_BUY)
                 if op not in (O.MO_NONE, O.MO_SELL)])
    n_lot = len(next(iter(rows.values()), ()))
    # Mode Z is the one variant with nothing to fall back *to* on a narrow day:
    # the lot owns turn 0 outright and nine products always fit ten slots. Its
    # own fallback is the WIDE day, which
    # `test_on_mode_z_hands_a_wide_day_back_to_mode_a` holds it to.
    if (any_mode not in P.EARLY_SELL_MODES_ZERO_ROW
            and n_buy + n_lot > spec.MAX_MARKET_ORDERS
            and _n_hire(plan) + n_lot > spec.MAX_MARKET_ORDERS):
        assert O.SELL_TURNS[0] in rows or not rows, rows
    assert all(len(_row(plan, t)) <= spec.MAX_MARKET_ORDERS
               for t in range(spec.TURNS_PER_DAY))


# =========================================================================
# Mode "Z": the lot takes turn 0 and the morning moves behind it
# =========================================================================

def _z_case(view, macro):
    """`(plan, hire turn, buy turn, wide)` of one board under mode Z."""
    plan = _plan(view, macro)
    ht = _z_hire_turn(plan)
    wide = ht == O.TURN_HIRE
    bt = next((t for t in (O.EARLY_SELL_Z_HIRE_TURN, O.EARLY_SELL_Z_HIRE_WIDE_TURN,
                           O.TURN_BUY)
               if any(k not in (O.MO_HIRE, O.MO_SELL) for k in _kinds(plan, t))), None)
    return plan, ht, bt, wide


def test_on_mode_z_gives_the_first_lot_turn_zero(monkeypatch):
    """The whole of mode Z in one assertion: on a day the crew fits one hire
    row, the lot goes out at turn 0 with no predicate in front of it -- nine
    products always fit ten slots -- and the hires move to turn 1. Turn 0
    carries nothing but SELL then, so nothing shares the curve with it but the
    other seat."""
    _on(monkeypatch, "Z")
    seen = 0
    for view, macro in _cases():
        plan, ht, _, wide = _z_case(view, macro)
        if wide:
            continue
        rows = _sell_rows(plan)
        assert set(_kinds(plan, O.EARLY_SELL_Z_LOT_TURN)) <= {O.MO_SELL}
        if rows:
            assert min(rows) == O.EARLY_SELL_Z_LOT_TURN, rows
            assert O.SELL_TURNS[0] not in rows, rows
            seen += 1
        assert ht == O.EARLY_SELL_Z_HIRE_TURN
    assert seen, "no narrow board had a lot to sell"


def test_on_mode_z_hires_in_front_of_the_purchases_it_shares_a_turn_with(monkeypatch):
    """HIRE is atomic -- the engine resolves a slot round's atomic orders in
    player order, ahead of the round's SELL/BUY lockstep -- so the crew is
    hired before the row behind it spends a coin, exactly as it was on turn 0.
    Written as slot order because that is what `_process_market` walks."""
    _on(monkeypatch, "Z")
    for view, macro in _cases():
        plan, ht, _, wide = _z_case(view, macro)
        if wide:
            continue
        kinds = _kinds(plan, O.EARLY_SELL_Z_HIRE_TURN)
        if O.MO_HIRE not in kinds:
            continue
        last_hire = len(kinds) - 1 - kinds[::-1].index(O.MO_HIRE)
        assert all(k == O.MO_HIRE for k in kinds[:last_hire + 1]), kinds


def test_on_mode_z_buys_on_the_first_turn_behind_the_hires_with_room(monkeypatch):
    """`n_hire + n_buy <= 10` puts the BUY row on turn 1 behind the hires; a
    day past the cap sends it to turn 2 alone. Read off the emitted rows and
    compared against the engine's own arithmetic, so the predicate is checked
    and not restated."""
    _on(monkeypatch, "Z")
    both = set()
    for view, macro in _cases():
        plan, ht, bt, wide = _z_case(view, macro)
        if wide or bt is None:
            continue
        n_hire = _n_hire(plan, O.EARLY_SELL_Z_HIRE_TURN)
        n_buy = len([1 for k in _kinds(plan, bt) if k != O.MO_HIRE])
        want = (O.EARLY_SELL_Z_BUY_TURNS[0]
                if n_hire + n_buy <= spec.MAX_MARKET_ORDERS
                else O.EARLY_SELL_Z_BUY_TURNS[1])
        assert bt == want, (bt, want, n_hire, n_buy)
        if bt == O.EARLY_SELL_Z_BUY_TURNS[1]:
            assert O.MO_HIRE not in _kinds(plan, bt), "a Z day's overflow row is empty"
        both.add(bt)
    assert both == set(O.EARLY_SELL_Z_BUY_TURNS), both


def test_on_mode_z_hands_a_wide_day_back_to_mode_a(monkeypatch):
    """More than ten hires need turn 2 for the overflow row, which leaves the
    purchases nowhere to stand -- so a wide day is not a Z day: it emits mode
    A's layout, order for order."""
    _on(monkeypatch, "Z")
    z = {}
    wides = []
    for i, (view, macro) in enumerate(_cases()):
        plan, ht, _, wide = _z_case(view, macro)
        if wide:
            wides.append(i)
        z[i] = plan
    assert wides, "no fixture board hires past the first row"
    _on(monkeypatch, "A")
    for i, (view, macro) in enumerate(_cases()):
        if i in wides:
            a = _plan(view, macro)
            for k in range(len(a)):
                assert np.array_equal(a[k], z[i][k]), (i, k)


def test_on_mode_z_keeps_every_unit_behind_its_own_hire_row(monkeypatch):
    """The law mode Z pays for [LAW, ops.ROUTE_BASE_WIDE]: a hand hired in
    turn t is appended in that turn's market phase, which runs after the unit
    phase, and `market._hire` places it on the least occupied shed-access
    tile -- so one unit that has stepped before the hire row resolves moves
    every later hand's spawn. Z hires at turn 1, so turn 1 is idle for the
    whole crew and `ops.ROUTE_BASE_Z` is 2."""
    _on(monkeypatch, "Z")
    for view, macro in _cases():
        plan, ht, _, wide = _z_case(view, macro)
        if wide:
            continue
        for t in range(O.ROUTE_BASE_Z):
            assert not _acting_units(plan, t), (t, _acting_units(plan, t))


def test_on_mode_z_never_works_a_purchase_before_the_row_that_buys_it(monkeypatch):
    """The other law: an order queued on turn t is credited after turn t's unit
    phase, so nothing a Z day buys can be PICKED UP or PLANTed before turn
    `bt + 1`. This is what `ops.ROUTE_BASE_Z_LATE` and `ROUTE_SPLIT_ON`'s
    `free_first` are between them for."""
    _on(monkeypatch, "Z")
    for view, macro in _cases():
        plan, ht, bt, wide = _z_case(view, macro)
        if wide or bt is None:
            continue
        unit_op = plan[0]
        for t in range(bt + 1):
            for u in range(spec.MAX_UNITS):
                assert int(unit_op[u, t]) not in (O.OP_PICKUP, O.OP_PLANT), (t, u)


def test_on_mode_z1_takes_turn_zero_only_on_a_day_worth_the_tick(monkeypatch):
    """`ticks_before` gives turn 0 (0 shop ticks, 0 centre ticks) and turn 1
    (1, 1): between the two market phases the town centre takes its once-a-day
    bite and the first shop tick fires, and both drain the shelf, so turn 0
    quotes off a market a full day-tick FULLER -- a per-unit discount that
    scales with the lot. Z1 pays it only where the shed is heavy enough for
    the lockstep to be worth it, and every other day keeps mode A's row."""
    assert PJ.ticks_before(O.EARLY_SELL_Z_LOT_TURN) == (0, 0)
    assert PJ.ticks_before(O.EARLY_SELL_Z_HIRE_TURN) == PJ.ticks_before(O.SELL_TURNS[0])
    light = _stocked_view(per=0, day=12)
    heavy = _stocked_view(per=O.EARLY_SELL_Z_MIN_SHED, day=12)
    macro = _macro(crew_target=np.int32(6),
                   plant_target=np.asarray((3, 3, 2, 2, 0), np.int32),
                   hold=np.zeros(spec.N_PRODUCTS, np.int32))
    _on(monkeypatch, "Z1")
    assert not _sell_rows(_plan(light, macro)).get(O.EARLY_SELL_Z_LOT_TURN)
    z1_heavy = _plan(heavy, macro)
    _on(monkeypatch, "Z")
    for k in range(len(z1_heavy)):
        assert np.array_equal(_plan(heavy, macro)[k], z1_heavy[k]), k
    _on(monkeypatch, "A")
    a_light = _plan(light, macro)
    _on(monkeypatch, "Z1")
    for k in range(len(a_light)):
        assert np.array_equal(a_light[k], _plan(light, macro)[k]), k


def test_on_the_lot_turns_agree_with_the_rollouts(any_mode):
    """`sim/rollout` compiles its market turns off `plan.early_lot_turns()` at
    import; `_market` reads the same function at call time. One reader, so the
    simulator cannot resolve a turn the planner does not write."""
    turns = set(P.early_lot_turns())
    for view, macro in _cases():
        rows = set(_sell_rows(_plan(view, macro)))
        early = {O.TURN_HIRE, O.EARLY_SELL_LOT1_TURN}
        assert rows <= turns | early, (any_mode, sorted(rows))
    assert set(range(O.FULL_MARKET_TURNS)) >= (
        {O.TURN_HIRE, O.EARLY_SELL_LOT1_TURN}), "the early rows must be full-row turns"


#: `plan.OPEN_PUMP_ON` went on by default on 2026-09-04: on day 0 the plan buys
#: `OPEN_PUMP_UNITS` wheat behind the hire row and sells it back from the BUY
#: row's head slot, to quote the class-A opening's own wheat off a drained pot.
#: It is pinned off for this file the way `0772ed3` pinned `EARLY_SELL_ON` off
#: for the modules it moved under: modes A0, A1, Z and Z1 move turn 0 or
#: turn 1, which `plan` asserts the pump owns on day 0, so their ON halves
#: cannot run with the new default live. What this file is about -- which turn
#: the day's first lot rides -- the pump does not answer.
#: `tests/test_open_pump.py` owns both halves of the switch.
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


#: `plan.HIRE_ROW_ON` (`b1bde4f`) and `plan.SELL_SLOT_PRIORITY_ON`
#: (`docs/strategy/2026-09-16-slotprio.md`, +459 t 7.31 on the lot-4 combo,
#: sub 56277270) both shipped `True` after the `73c5b8a` digests above were
#: taken, and both move the row this file reads:
#:
#: * the trim cuts the emitted HIRE row down to the hands `_routes` loaded, so
#:   no fixture board here reaches `spec.MAX_MARKET_ORDERS` hires any more and
#:   the wide-day half of mode Z has no board to run on;
#: * slot priority re-orders the merged row, which is the very order
#:   `test_on_keeps_the_purchases_in_front_of_the_lot` was written to assert --
#:   the lot's *place* among the day's turns is this file's subject, its place
#:   inside the row is the later switch's.
#:
#: Both are STATED off here, the way `LOT4_ON` is above and `OPEN_PUMP_ON` and
#: the tail pair are below, rather than left to a default that has since moved;
#: measured TESTFIX3 2026-09-17, with the two off this tree reproduces the
#: `73c5b8a` digests byte for byte. `tests/test_hire_row.py` and
#: `tests/test_slotprio.py` own the two.
@pytest.fixture(autouse=True)
def _later_market_ships_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
