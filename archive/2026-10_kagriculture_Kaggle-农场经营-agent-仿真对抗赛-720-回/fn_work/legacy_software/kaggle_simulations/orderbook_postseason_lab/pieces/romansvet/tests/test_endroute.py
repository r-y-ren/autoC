"""`plan.ENDROUTE_ON`: the terminal day's LAST executed sell row.

`S/dropharv/measure.py` (24 TOPLEG2 engine-class boards, shipped FT2) prices the
d27-29 residue at 431 coins a board: 290 of it is stock still in the shed when the
game ends -- 9.8 units, essentially all FERTILIZER -- because day 29's three lots
are sized off the DAWN shed while the day's own COLLECT_FERTILIZER units are
DROPped in after `SELL_TURNS[-1]`.  Futile planting and futile seed buys are a
measured ZERO (the terminal law already blocks them).

Pinned here:

* the switch SHIPS ON (2026-09-17), and set OFF the planner is the pre-switch
  tree byte for byte -- whole-plan digests against a pristine `git archive
  <PRE_SWITCH> src` subprocess, as `tests/test_endsell.py` and
  `tests/test_lot4.py` pin theirs -- so the shipped program differs from the
  champion's on day 29 and on no other day;
* ON, day 29 grows exactly one extra SELL row, on `ENDROUTE_TURN`, and every
  earlier day decodes the OFF plan;
* the row is the full nine-slot layout both seats present, and the ask is flat
  (`ENDROUTE_ASK` per product) -- it is an amount the engine clips, not a price;
* `ENDROUTE_TURN` is a turn the engine actually EXECUTES (step 718 of 720).
"""
from __future__ import annotations

import contextlib
import hashlib
import os
import subprocess
import sys
import tempfile

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure (the
# `tests/_pin.py` hazard `tests/test_lot4.py` documents).
_pin.bootstrap()

import numpy as np

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

#: The commit this switch sits on: the `master` head with no `ENDROUTE_ON` in it.
PRE_SWITCH = "a7e19c7"


def _view(day=28, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """The `tests/test_endsell.py` / `tests/test_lot4.py` board family, so every
    sell-row switch is measured on one set of boards."""
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


def _sell_rows(plan):
    """{turn: units offered} over every SELL slot the day emits."""
    op, _arg, qty = plan[3:6]
    out = {}
    for t in range(op.shape[0]):
        n = int(qty[t][op[t] == O.MO_SELL].sum())
        if n:
            out[t] = n
    return out


PIN_BOARDS = (
    ("mid", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d27", dict(day=27, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d28", dict(day=28, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d29", dict(day=29, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d29bare", dict(day=29, n_wh=0, shed_wh=60, shed_to=38, shops=2)),
)


@contextlib.contextmanager
def _knobs(on, ask=None):
    # The two switches that STAND ON this row shipped ON on 2026-09-18 with PES
    # (`docs/strategy/2026-09-18-stack3.md`), and both are pinned OFF here --
    # on every arm, not only the OFF one.  This file's subject is ENDROUTE
    # ALONE: `PRE_SWITCH` predates ENDROUTE2 entirely, so the byte-exact pin
    # would be reading three switches, and "exactly one row on day 29" is a
    # claim about the row this switch adds, not about the second trip
    # ENDROUTE2_SPLIT sends after it.  Their own files carry the ON claims
    # (`tests/test_endroute2.py`, `tests/test_endroute2_split.py`).
    # 2026-09-18 ESR adds a third: `ENDROUTE_ROW2_ON`, the SECOND late row,
    # which stands on this one exactly as the other two do.
    was = (P.ENDROUTE_ON, P.ENDROUTE_ASK,
           P.ENDROUTE2_ON, P.ENDROUTE2_SPLIT_ON, P.ENDROUTE_ROW2_ON)
    P.ENDROUTE_ON = on
    P.ENDROUTE2_ON = P.ENDROUTE2_SPLIT_ON = P.ENDROUTE_ROW2_ON = False
    if ask is not None:
        P.ENDROUTE_ASK = ask
    try:
        yield
    finally:
        (P.ENDROUTE_ON, P.ENDROUTE_ASK,
         P.ENDROUTE2_ON, P.ENDROUTE2_SPLIT_ON, P.ENDROUTE_ROW2_ON) = was


def _own_digests(on=None):
    if on is None:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    with _knobs(on):
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
# the turn: it has to be one the engine runs
# =========================================================================

def test_the_row_stands_on_the_last_executed_turn():
    """`episodeSteps` is 720 and step 718 -- day 29 turn 22 -- is the last one
    executed, so turn 23 of the terminal day never resolves."""
    assert P.ENDROUTE_TURN == 22
    assert spec.EPISODE_STEPS == spec.TURNS_PER_DAY * spec.N_DAYS == 720
    assert (spec.N_DAYS - 1) * spec.TURNS_PER_DAY + P.ENDROUTE_TURN \
        == spec.EPISODE_STEPS - 2
    assert O.SELL_TURNS[-1] < P.ENDROUTE_TURN < spec.TURNS_PER_DAY - 1


# =========================================================================
# OFF: the switch changes nothing
# =========================================================================

def test_the_row_ships():
    """2026-09-17: promoted `False -> True` on the POOLED180 read (169 held-out
    boards, +d at t >= 3, THEIR purse flat), under the gift-free ship rule."""
    assert P.ENDROUTE_ON is True
    assert P.ENDROUTE_ASK == int(spec.SHED_CAPACITY)
    assert P.SWITCH_GENE_DEFAULTS["ENDROUTE_ON"] is True
    assert "ENDROUTE_ON" in P.SWITCH_GENES


def test_the_pre_switch_tree_has_no_endroute():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ENDROUTE_ON" not in src


def test_off_is_the_pre_switch_tree_byte_for_byte():
    assert _own_digests(on=False) == _tree_digests()


def test_shipped_defaults_are_the_on_program():
    """The shipped program is the ON one, and it differs from the pre-switch
    tree on the terminal day and NOWHERE else: `mid`/`d27`/`d28` are still that
    tree byte for byte, both day-29 boards are not.

    Since 2026-09-18 the shipped terminal day carries ENDROUTE2 and its SPLIT on
    top of this row, so the equality below is stated where it is still this
    file's to make -- every day BEFORE the last -- and the day-29 difference is
    asserted against the pre-switch tree, which both arms clear.  What the ON
    arm adds to day 29 by itself is `test_on_adds_exactly_one_row_on_day_29`.
    """
    shipped, off = _own_digests(), _tree_digests()
    alone = _own_digests(on=True)
    for name in ("mid", "d27", "d28"):
        assert shipped[name] == alone[name], name
    for name in ("d29", "d29bare"):
        assert alone[name] != off[name], name
    for name in ("mid", "d27", "d28"):
        assert shipped[name] == off[name], name
    for name in ("d29", "d29bare"):
        assert shipped[name] != off[name], name


def test_every_day_before_the_last_is_untouched_on():
    off = _own_digests(on=False)
    on = _own_digests(on=True)
    for name in ("mid", "d27", "d28"):
        assert on[name] == off[name], name


# =========================================================================
# ON: one extra row, on the terminal day only
# =========================================================================

def test_on_adds_exactly_one_row_on_day_29():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(False):
        off = _sell_rows(_plan(_view(**board)))
    with _knobs(True):
        on = _sell_rows(_plan(_view(**board)))
    assert set(on) - set(off) == {P.ENDROUTE_TURN}
    for t in off:
        assert on[t] == off[t], t


def test_the_row_is_the_flat_ask_over_all_nine_products():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(True):
        plan = _plan(_view(**board))
    op, arg, qty = plan[3:6]
    row = P.ENDROUTE_TURN
    sell = op[row] == O.MO_SELL
    assert int(sell.sum()) == spec.N_PRODUCTS
    assert sorted(int(a) for a in arg[row][sell]) == list(range(spec.N_PRODUCTS))
    assert set(int(q) for q in qty[row][sell]) == {P.ENDROUTE_ASK}


def test_the_ask_is_a_knob_and_zero_means_no_row():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(True, ask=0):
        on = _sell_rows(_plan(_view(**board)))
    with _knobs(False):
        off = _sell_rows(_plan(_view(**board)))
    assert on == off


if __name__ == "__main__":                  # the pristine-tree subprocess
    if "--digests" in sys.argv:
        for name, digest in _own_digests().items():
            print(name, digest)
