"""`plan.ENDROUTE_ROW2_ON`: the terminal day's SECOND late sell row.

`S/endfamily/run_ledger.sh` (the SPLIT cell, 24 TOPLEG2 + 24 TOPLEG3 engine-class
boards, shipped FT2) prices what `ENDROUTE2_SPLIT_ON` leaves behind at **0.0 and
6.0 coins a board** -- the 431-coin DROPHARV ceiling is banked and the value
ledger is empty.  What the same census shows instead is DEPTH: at day 29 turn 22
the crew still CARRIES 1,250-1,565 coins of produce, and every coin of it is sold
through ONE row.  This switch offers the same flat ask one turn earlier as well,
so the deepest lot of the game meets two rows instead of one.

Pinned here:

* the switch is OFF by default, and OFF the planner is the pre-switch tree byte
  for byte -- whole-plan digests against a pristine `git archive <PRE_SWITCH>
  src` subprocess, as `tests/test_endroute.py` pins its own;
* ON (with `ENDROUTE_ON`), day 29 grows exactly one MORE row, on
  `ENDROUTE_ROW2_TURN`, and every earlier day decodes the OFF plan;
* the row is the full nine-slot layout both seats present and the ask is flat
  (`ENDROUTE_ASK` per product) -- an amount the engine clips, not a price;
* `ENDROUTE_ROW2_TURN` stands strictly between the day's last lot and
  `ENDROUTE_TURN`, and on a turn nothing else in the day uses.
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

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_endroute import PIN_BOARDS, _plan, _sell_rows, _view

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

#: The commit this switch sits on: the `e2split` head with no `ENDROUTE_ROW2` in
#: it (the whole end-of-game family, every switch OFF).
PRE_SWITCH = "903bf79"


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


#: The two switches that STAND BETWEEN this row and `PRE_SWITCH`, held at the
#: value the archived tree has.  `903bf79` is the e2split head with the whole
#: end-of-game family OFF; PES shipped `ENDROUTE2_ON` and `ENDROUTE2_SPLIT_ON`
#: ON on 2026-09-18, so without this the pin would be reading three switches
#: and calling the answer ROW2's.  Pinned on BOTH ends -- in the `--digests`
#: subprocess this file runs from the archived tree too -- so every comparison
#: below is a ONE-switch comparison again.  `setattr` on a name read with a
#: default keeps the file runnable where the name does not exist.
#: PUMPCLIP is NOT in this dict: ESR put `OPEN_PUMP_ON` back to True and
#: `CLIP_CAP_ON` back to False, which is what `PRE_SWITCH` already had.
OTHER_SHIPPED = dict(ENDROUTE2_ON=False, ENDROUTE2_SPLIT_ON=False)


@contextlib.contextmanager
def _knobs(end=None, row2=None, turn=None):
    names = ("ENDROUTE_ON", "ENDROUTE_ROW2_ON", "ENDROUTE_ROW2_TURN")
    was = tuple(getattr(P, n) for n in names)
    other = {n: getattr(P, n, None) for n in OTHER_SHIPPED}
    for n, v in OTHER_SHIPPED.items():
        setattr(P, n, v)
    if end is not None:
        P.ENDROUTE_ON = end
    if row2 is not None:
        P.ENDROUTE_ROW2_ON = row2
    if turn is not None:
        P.ENDROUTE_ROW2_TURN = turn
    try:
        yield
    finally:
        for n, v in zip(names, was):
            setattr(P, n, v)
        for n, v in other.items():
            setattr(P, n, v)


def _own_digests(end=None, row2=None):
    if end is None and row2 is None:
        return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    with _knobs(end=end, row2=row2):
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
# the turn
# =========================================================================

def test_the_second_row_is_between_the_last_lot_and_the_last_row():
    assert O.SELL_TURNS[-1] < P.ENDROUTE_ROW2_TURN < P.ENDROUTE_TURN
    assert P.ENDROUTE_ROW2_TURN == 21


def test_the_turn_collides_with_nothing_the_day_already_uses():
    taken = (set(O.SELL_TURNS) | set(O.MELON_LOT_TURNS)
             | set(O.EARLY_SELL_LATE_TURNS)
             | {O.TURN_PRESTOCK, P.SHED_DUMP_ROW_TURN, P.ENDROUTE_TURN})
    assert P.ENDROUTE_ROW2_TURN not in taken
    # 19 and 21 are the only free turns in the window, so the knob has exactly
    # one alternative and the sweep is complete.
    free = [t for t in range(O.SELL_TURNS[-1] + 1, P.ENDROUTE_TURN)
            if t not in taken]
    assert free == [19, 21]


# =========================================================================
# OFF: the switch changes nothing
# =========================================================================

def test_the_second_row_ships():
    """2026-09-18: promoted `False -> True` as the fourth member of the ESR
    cell (`docs/strategy/2026-09-18-stack5.md`), and appended to the gene block
    as column 15 at the same merge."""
    assert P.ENDROUTE_ROW2_ON is True
    assert P.SWITCH_GENE_DEFAULTS["ENDROUTE_ROW2_ON"] is True
    assert "ENDROUTE_ROW2_ON" in P.SWITCH_GENES


def test_the_pre_switch_tree_has_no_row2():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for path in ("src/kagg3/core/plan.py", "src/kagg3/sim/rollout.py"):
        src = subprocess.run(f"git show {PRE_SWITCH}:{path}", shell=True,
                             cwd=root, capture_output=True, text=True,
                             check=True).stdout
        assert "ENDROUTE_ROW2" not in src, path


def test_off_is_the_pre_switch_tree_byte_for_byte():
    assert _own_digests(end=False, row2=False) == _tree_digests()


def test_shipped_defaults_are_the_on_program():
    """Since ESR the shipped terminal day runs BOTH rows, so the byte-exact pin
    above names the PRE-switch tree and this line names what ships.

    Stated on the plan the defaults actually produce -- ENDROUTE2 and its SPLIT
    standing, which `_knobs` pins away everywhere else in this file -- because
    that is the only place the claim "the shipped program has the second row"
    can be made honestly."""
    board = dict(PIN_BOARDS)["d29"]
    assert P.ENDROUTE_ROW2_ON and P.ENDROUTE_ON
    shipped = _sell_rows(_plan(_view(**board)))
    assert P.ENDROUTE_ROW2_TURN in shipped and P.ENDROUTE_TURN in shipped
    was, P.ENDROUTE_ROW2_ON = P.ENDROUTE_ROW2_ON, False
    try:
        without = _sell_rows(_plan(_view(**board)))
    finally:
        P.ENDROUTE_ROW2_ON = was
    assert set(shipped) - set(without) == {P.ENDROUTE_ROW2_TURN}


def test_endroute_alone_is_untouched():
    """The switch OFF, `ENDROUTE_ON` decodes exactly what it decoded before."""
    with _knobs(end=True, row2=False):
        on = {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    with _knobs(end=True, row2=False):
        again = {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}
    assert on == again
    assert on != _own_digests(end=False, row2=False)


def test_every_day_before_the_last_is_untouched_on():
    off = _own_digests(end=True, row2=False)
    on = _own_digests(end=True, row2=True)
    for name in ("mid", "d27", "d28"):
        assert on[name] == off[name], name


# =========================================================================
# ON: one more row, on the terminal day only
# =========================================================================

def test_on_adds_exactly_one_row_on_day_29():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(end=True, row2=False):
        base = _sell_rows(_plan(_view(**board)))
    with _knobs(end=True, row2=True):
        both = _sell_rows(_plan(_view(**board)))
    assert set(both) - set(base) == {P.ENDROUTE_ROW2_TURN}
    for t in base:
        assert both[t] == base[t], t


def test_the_second_row_is_the_flat_ask_over_all_nine_products():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(end=True, row2=True):
        plan = _plan(_view(**board))
    op, arg, qty = plan[3:6]
    row = P.ENDROUTE_ROW2_TURN
    sell = op[row] == O.MO_SELL
    assert int(sell.sum()) == spec.N_PRODUCTS
    assert sorted(int(a) for a in arg[row][sell]) == list(range(spec.N_PRODUCTS))
    assert set(int(q) for q in qty[row][sell]) == {P.ENDROUTE_ASK}
    # ... and it is the same layout the last row presents.
    last = op[P.ENDROUTE_TURN] == O.MO_SELL
    assert list(arg[row][sell]) == list(arg[P.ENDROUTE_TURN][last])


def test_turn_19_is_the_other_free_seat():
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(end=True, row2=True, turn=19):
        rows = _sell_rows(_plan(_view(**board)))
    assert 19 in rows and P.ENDROUTE_TURN in rows


def test_row2_without_endroute_decodes_the_endroute_off_program():
    """The dependency lives in the VALUE, not in an assert.

    Before ESR this raised: the second row splits ENDROUTE's row, so without
    the first there is nothing to split.  A gene block cannot raise -- the ES
    draws all sixteen columns independently -- so the requirement moved into
    `plan._sw_all`, exactly as `ENDROUTE2_ON` and `ENDROUTE2_SPLIT_ON` did when
    they shipped: a draw that takes the first row away takes the second with
    it, and what the planner emits is the ENDROUTE-off program itself."""
    board = dict(PIN_BOARDS)["d29"]
    with _knobs(end=False, row2=True):
        got = _digest(_plan(_view(**board)))
    with _knobs(end=False, row2=False):
        want = _digest(_plan(_view(**board)))
    assert got == want


if __name__ == "__main__":                  # the pristine-tree subprocess
    if "--digests" in sys.argv:
        for name, digest in _own_digests().items():
            print(name, digest)
