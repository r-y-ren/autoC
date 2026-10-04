"""`plan.ENDROUTE2_ON`: the terminal day's turn budget, re-cut to ENDROUTE's row.

`S/endroute2/measure2.py` (the 24 TOPLEG2 engine-class boards, shipped FT2 +
`ENDROUTE_ON`, real engine) prices what is left at the end of the game at 141
coins a board, and ALL of it stands on tiles -- 103 in ripe PLANT units, 38 in
uncollected EGG/MILK/WOOL.  The shed and the crew's hands both end at exactly
0.0, so ENDROUTE's row already banks everything that reaches it.  Day 29 also
idles 53.4 PASS unit-turns, because `drop_turns` / `turn_budget` end the
terminal day at `O.SELL_TURNS[-1] + 1`: before the row existed a DROP later than
turn 18 had nothing to sell into.  This switch moves that cut to
`ENDROUTE_TURN + 1` -- +4 turns for every unit, on day 29 only.

Pinned here:

* OFF the planner is the pre-switch tree byte for byte (whole-plan digests
  against a pristine `git archive <PRE_SWITCH> src` subprocess);
* the two budgets differ by exactly `ENDROUTE_TURN - O.SELL_TURNS[-1]`, and the
  later DROP still lands on a turn whose market phase runs after it;
* ON, no day before the terminal one moves, and a day-29 board whose admission
  binds does;
* without `ENDROUTE_ON` the switch falls back to the OFF program -- since
  2026-09-18 the dependency rides `plan._sw_all` on the vector rather than an
  in-function assert, because a gene block cannot raise at a draw the ES makes.
"""
from __future__ import annotations

import contextlib
import hashlib
import os
import subprocess
import sys
import tempfile

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: The commit this switch sits on: `dropharv`'s head, ENDROUTE and no ENDROUTE2.
PRE_SWITCH = "516e6dc"


def _view(day=29, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """The `tests/test_endroute.py` board family, so the two halves of the
    terminal-day arm are measured on one set of boards."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    kind[:n_wh] = spec.KIND_PLANT
    occ[:n_wh] = spec.I_WHEAT
    t_day[:n_wh] = day - age
    t_yield[:n_wh] = yld
    t_wat[:n_wh] = t_water
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = shed_wh
    shed[spec.I_TOMATO] = shed_to
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=t_wat,
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("mid", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d27", dict(day=27, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d28", dict(day=28, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d29", dict(day=29, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d29bare", dict(day=29, n_wh=0, shed_wh=60, shed_to=38, shops=2)),
    # A terminal day whose admission BINDS: four quadrants of ripe wheat is far
    # more work than 17 turns a unit buys, so the extra four turns must move it.
    ("d29full", dict(day=29, n_wh=40, nquad=4, shed_wh=10, shed_to=0, shops=2)),
)


@contextlib.contextmanager
def _knobs(endroute, endroute2, split=False, **override):
    # `ENDROUTE2_SPLIT_ON` is pinned here too, and by name: it shipped ON on
    # 2026-09-18 with PES, so an arm that only said "ENDROUTE2 off" would be
    # asking `PRE_SWITCH` -- a tree that has no SPLIT at all -- to match a
    # planner that still runs day 29's first shed trip. `setattr` with a
    # default read keeps this file runnable as the archived tree's own
    # `--digests` subprocess, where the name does not exist.
    # PUMPCLIP shipped on 2026-09-18 and `PRE_SWITCH` predates it, so the
    # opening pump and the shed cap are pinned on BOTH ends of this comparison
    # too -- otherwise the pin reads three switches and calls the answer
    # ENDROUTE2 (`tests/test_endroute2_split.py:OTHER_SHIPPED`).
    # 2026-09-18, ESR: the pump went back ON and the cap back OFF -- which is
    # what `PRE_SWITCH` already had -- and `ENDROUTE_ROW2_ON` shipped ON, so it
    # joins the pinned list for the reason SPLIT is on it.
    names = ("ENDROUTE_ON", "ENDROUTE2_ON", "ENDROUTE2_SPLIT_ON",
             "OPEN_PUMP_ON", "CLIP_CAP_ON", "ENDROUTE_ROW2_ON")
    was = [getattr(P, n, None) for n in names]
    for n, v in zip(names, (endroute, endroute2, split, True, False, False)):
        setattr(P, n, override.get(n, v))
    try:
        yield
    finally:
        for n, v in zip(names, was):
            setattr(P, n, v)


def _own_digests(endroute=None, endroute2=None, split=False, **override):
    if endroute is None:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    with _knobs(endroute, endroute2, split, **override):
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _tree_digests(ref=PRE_SWITCH):
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {ref} src | tar -x -C {td}", shell=True,
                       cwd=root, check=True)
        out = subprocess.run(
            [sys.executable, os.path.abspath(__file__), "--digests",
             os.path.join(td, "src")],
            cwd=root, capture_output=True, text=True, check=True)
    return dict(line.split(None, 1) for line in out.stdout.strip().splitlines())


# =========================================================================
# the budget: four turns, and they all still have a market behind them
# =========================================================================

def test_the_two_budgets_differ_by_the_row_it_sells_into():
    gain = P.ENDROUTE_TURN - O.SELL_TURNS[-1]
    for h in range(spec.MAX_HANDS + 1):
        assert P.end_drop_turns(h) - P.drop_turns(h) == gain
        # the DROP lands at or before `ENDROUTE_TURN`, and a unit acts before
        # its own turn's market phase, so the row still sees the deposit.
        base = O.ROUTE_BASE if h <= spec.MAX_MARKET_ORDERS else O.ROUTE_BASE_WIDE
        assert base + P.end_drop_turns(h) - 1 == P.ENDROUTE_TURN
    assert gain == 4


# =========================================================================
# OFF: the switch changes nothing
# =========================================================================

def test_default_is_on():
    """SHIPPED 2026-09-18 inside PES [docs/strategy/2026-09-18-stack3.md]."""
    assert P.ENDROUTE2_ON is True


def test_the_pre_switch_tree_has_no_endroute2():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ENDROUTE2_ON" not in src and "ENDROUTE_ON" in src


def test_off_is_the_pre_switch_tree_byte_for_byte():
    assert _own_digests(endroute=False, endroute2=False) == _tree_digests()


def test_shipped_defaults_are_the_on_program():
    """The defaults moved on 2026-09-18: the shipped program is the ON one, and
    the OFF claim above is made by naming the arm out loud.

    Asked with `ENDROUTE_ROW2_ON` set to what it SHIPS (ESR, 2026-09-18), not
    to the value `_knobs` pins it at for the byte-exact comparisons: this line
    is the one claim in the file about the whole terminal day rather than about
    this switch, so it is the one place the pin must not hold the other row
    away."""
    assert _own_digests() == _own_digests(endroute=True, endroute2=True,
                                          split=True,
                                          ENDROUTE_ROW2_ON=P.ENDROUTE_ROW2_ON)


def test_endroute_alone_is_unchanged_by_this_commit():
    """ENDROUTE ON / ENDROUTE2 OFF is still exactly the arm dropharv judged."""
    on = _own_digests(endroute=True, endroute2=False)
    off = _own_digests(endroute=False, endroute2=False)
    for name in ("mid", "d27", "d28"):
        assert on[name] == off[name], name


# =========================================================================
# ON: the terminal day only
# =========================================================================

def test_no_day_before_the_terminal_one_moves():
    base = _own_digests(endroute=True, endroute2=False)
    on = _own_digests(endroute=True, endroute2=True)
    for name in ("mid", "d27", "d28"):
        assert on[name] == base[name], name


def test_a_binding_terminal_day_does_move():
    base = _own_digests(endroute=True, endroute2=False)
    on = _own_digests(endroute=True, endroute2=True)
    assert on["d29full"] != base["d29full"]


def test_the_market_rows_are_untouched_by_the_budget():
    """ENDROUTE2 spends TURNS; it writes no row of its own. Every SELL turn the
    longer route puts stock behind is a lot the day's layout already owned --
    the extra load reaches turn 18's lot as well as the terminal one, which is
    the mechanism and not a new row."""
    board = dict(PIN_BOARDS)["d29full"]
    def rows(e2):
        with _knobs(True, e2):
            op, _a, _q = _plan(_view(**board))[3:6]
        return {t for t in range(op.shape[0]) if bool((op[t] == O.MO_SELL).any())}
    legal = set(O.SELL_TURNS) | set(P.spread_rows_turns() or ()) | {P.ENDROUTE_TURN}
    assert rows(False) <= rows(True) <= legal
    assert P.ENDROUTE_TURN in rows(True)


def test_it_falls_back_to_the_off_program_without_the_row():
    """The refusal moved from an assert to the VECTOR when this switch became a
    gene (`plan._sw_all`, 2026-09-18).  ENDROUTE2 spends turns into ENDROUTE's
    row and buys a walk that sells nothing without it, and the module-level
    assert still refuses that tree -- but a gene block cannot raise: the ES
    draws all four columns independently, so a draw that takes the row away has
    to take its dependants with it.  What the planner does with the combination
    is therefore the ENDROUTE-off program, exactly, and not an exception."""
    board = dict(PIN_BOARDS)["d29full"]
    with _knobs(False, True):
        got = _digest(_plan(_view(**board)))
    with _knobs(False, False):
        want = _digest(_plan(_view(**board)))
    assert got == want


if __name__ == "__main__":                  # the pristine-tree subprocess
    if "--digests" in sys.argv:
        for name, digest in _own_digests().items():
            print(name, digest)
