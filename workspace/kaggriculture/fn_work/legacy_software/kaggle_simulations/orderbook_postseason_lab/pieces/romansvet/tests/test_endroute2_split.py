"""`plan.ENDROUTE2_SPLIT_ON`: day 29's two shed trips, the first one on time.

`2026-09-17-endroute2.md` sect.5 traced ENDROUTE2's rival gift to the coin and it
is not produce: `ENDROUTE_ON` alone lands the terminal day's one DROP by turn 18,
so the whole load sells on lot 3 (engine hour 19) and CRUSHES the quote under the
rival's own h21/h22 sells; `ENDROUTE2_ON`'s four extra turns push that DROP to
turn 22-23, the h19 quote barely moves and the rival banks +155 a board.

This switch keeps both halves by splitting the terminal route into TWO trips: the
`BANK_BEFORE_LOT_ON` mid-block excursion (walk to the nearest shed access, DROP,
walk back), fired on day 29 with its deadline re-cut to `ENDROUTE2_SPLIT_TURN`
(the day's LAST lot), and then the block's ordinary return leg, whose DROP lands
on `ENDROUTE_TURN` -- `ENDROUTE_ON`'s row, a second sell of the late harvest.

Pinned here:

* OFF the planner is the pre-switch tree byte for byte (whole-plan digests
  against a pristine `git archive <PRE_SWITCH> src` subprocess), and that holds
  for every combination of `ENDROUTE_ON` / `ENDROUTE2_ON`;
* ON, no day before the terminal one moves;
* ON, a terminal day whose blocks can reach a shed access in time takes the
  excursion: a unit DROPs twice, the first DROP at or before
  `ENDROUTE2_SPLIT_TURN` and the last at or before `ENDROUTE_TURN`;
* the day's last lot already offers whatever the first DROP banks (`DROP_ON`'s
  `gain` row), and `BANK_LOT`'s row is NOT widened on the terminal day;
* without the turns or the row it spends them into the switch falls back to
  the OFF program -- since 2026-09-18 the dependency rides `plan._sw_all` on
  the vector rather than an in-function assert, because a gene block cannot
  raise at a draw the ES is free to make.
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

#: The commit this switch sits on: `endroute2`'s head, ENDROUTE + ENDROUTE2.
PRE_SWITCH = "76e81f0"


def _view(day=29, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, near=False,
          mkt_inv=spec.MARKET_I0):
    """`tests/test_endroute2.py`'s board family, plus `near`: the same ripe
    wheat laid on the tiles CLOSEST to a shed access rather than on the first
    `n_wh` serpentine ranks, which is what an excursion needs to be affordable
    (`BANK_MAX_TURNS` is a round trip, the return leg is one way)."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_wat, t_yield = z.copy(), z.copy(), z.copy()
    if near:
        tiles = np.argsort(np.asarray(P.DIST_SHED, np.int32),
                           kind="stable")[:n_wh]
    else:
        tiles = np.arange(n_wh)
    kind[tiles] = spec.KIND_PLANT
    occ[tiles] = spec.I_WHEAT
    t_day[tiles] = day - age
    t_yield[tiles] = yld
    t_wat[tiles] = t_water
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
    ("d29full", dict(day=29, n_wh=40, nquad=4, shed_wh=10, shed_to=0, shops=2)),
    # The board the excursion can actually afford: ripe wheat on the tiles
    # nearest a shed access, so a round trip fits `BANK_MAX_TURNS`.
    ("d29near", dict(day=29, n_wh=24, nquad=4, shed_wh=10, shed_to=0, shops=2,
                     near=True)),
)


#: Every OTHER switch this pin's two ends disagree about, held at the value the
#: planner ships with today. `PRE_SWITCH` predates PUMPCLIP (2026-09-18,
#: `docs/strategy/2026-09-17-stack1.md`), so the archived tree opens day 0 with
#: the wheat pump and carries an uncapped haul; without this the pin would be
#: reading three switches at once and `d29near` -- the only board here whose
#: haul overflows the shed -- would differ for a reason that is not SPLIT.
#: Pinned on BOTH ends, so the comparison is a ONE-switch comparison again.
#: 2026-09-18, ESR: the pump went back ON and the cap back OFF, which is what
#: `PRE_SWITCH` already had, so those two entries are now no-ops on both ends
#: and are kept only so the pin stays explicit.  `ENDROUTE_ROW2_ON` shipped ON
#: at the same merge and does NOT exist at `PRE_SWITCH`, so it joins the dict
#: for the original reason.
OTHER_SHIPPED = dict(OPEN_PUMP_ON=True, CLIP_CAP_ON=False,
                     ENDROUTE_ROW2_ON=False)


@contextlib.contextmanager
def _knobs(endroute, endroute2, split=False, **kw):
    kw = dict(OTHER_SHIPPED, **kw)
    names = ("ENDROUTE_ON", "ENDROUTE2_ON", "ENDROUTE2_SPLIT_ON") + tuple(kw)
    vals = (endroute, endroute2, split) + tuple(kw.values())
    was = [getattr(P, n, None) for n in names]
    for n, v in zip(names, vals):
        setattr(P, n, v)
    try:
        yield
    finally:
        for n, v in zip(names, was):
            setattr(P, n, v)


def _own_digests(endroute=None, endroute2=None, split=False, **kw):
    if endroute is None:
        return {n: _digest(_plan(_view(**b))) for n, b in PIN_BOARDS}
    with _knobs(endroute, endroute2, split, **kw):
        return {n: _digest(_plan(_view(**b))) for n, b in PIN_BOARDS}


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


def _drop_turns(board, **kw):
    """{unit: [turns it DROPs on]} for the units that DROP at all."""
    with _knobs(**kw):
        op = _plan(_view(**board))[0]
    return {u: [t for t in range(op.shape[1]) if int(op[u, t]) == O.OP_DROP]
            for u in range(op.shape[0])
            if bool((op[u] == O.OP_DROP).any())}


# =========================================================================
# OFF: the switch changes nothing, on any combination of the other two
# =========================================================================

def test_default_is_on():
    """SHIPPED 2026-09-18 inside PES [docs/strategy/2026-09-18-stack3.md]."""
    assert P.ENDROUTE2_SPLIT_ON is True


def test_the_pre_switch_tree_has_no_split():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ENDROUTE2_SPLIT_ON" not in src
    assert "ENDROUTE2_ON" in src and "ENDROUTE_ON" in src


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


def test_off_changes_no_arm_of_the_family():
    """The two arms this branch already judged are untouched by this commit:
    with `ENDROUTE2_SPLIT_ON` False, ENDROUTE alone and E + E2 are exactly the
    programs `dropharv` and `endroute2` measured."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(f"git archive {PRE_SWITCH} src | tar -x -C {td}",
                       shell=True, cwd=root, check=True)
        for e, e2 in ((True, False), (True, True)):
            out = subprocess.run(
                [sys.executable, os.path.abspath(__file__), "--digests",
                 os.path.join(td, "src"), "--arm", str(e), str(e2)],
                cwd=root, capture_output=True, text=True, check=True)
            want = dict(line.split(None, 1)
                        for line in out.stdout.strip().splitlines())
            assert _own_digests(endroute=e, endroute2=e2, split=False) == want, \
                (e, e2)


# =========================================================================
# ON: the terminal day only, and two trips on it
# =========================================================================

def test_no_day_before_the_terminal_one_moves():
    base = _own_digests(endroute=True, endroute2=True, split=False)
    on = _own_digests(endroute=True, endroute2=True, split=True)
    for name in ("mid", "d27", "d28"):
        assert on[name] == base[name], name


def test_the_terminal_day_does_move():
    base = _own_digests(endroute=True, endroute2=True, split=False)
    on = _own_digests(endroute=True, endroute2=True, split=True)
    assert on["d29near"] != base["d29near"]


def test_e_plus_e2_drops_once_and_late():
    """The arm this switch is an answer to: one DROP a unit, all of it after
    the day's last lot, which is the price denial the trace says we lose."""
    board = dict(PIN_BOARDS)["d29near"]
    drops = _drop_turns(board, endroute=True, endroute2=True, split=False)
    assert drops, "the board has to work at all"
    for u, ts in drops.items():
        assert len(ts) == 1, (u, ts)
        assert ts[0] <= P.ENDROUTE_TURN, (u, ts)
    # and the crew's LAST DROP lands past the day's last lot -- that is the
    # h19 price denial ENDROUTE alone had and ENDROUTE2 spends.
    assert max(ts[0] for ts in drops.values()) > O.SELL_TURNS[-1]


def test_split_drops_twice_the_first_one_in_front_of_the_last_lot():
    board = dict(PIN_BOARDS)["d29near"]
    drops = _drop_turns(board, endroute=True, endroute2=True, split=True)
    two = {u: ts for u, ts in drops.items() if len(ts) > 1}
    assert two, f"no unit split its day: {drops}"
    for u, ts in two.items():
        assert len(ts) == 2, (u, ts)
        # trip 1 sells on the day's last lot -- a unit acts before its turn's
        # market phase, so a DROP on `ENDROUTE2_SPLIT_TURN` itself still fills
        assert ts[0] <= P.ENDROUTE2_SPLIT_TURN, (u, ts)
        # trip 2 sells on ENDROUTE's row and nowhere later
        assert ts[0] < ts[1] <= P.ENDROUTE_TURN, (u, ts)
    # and at least one of them really is the late row
    assert max(ts[1] for ts in two.values()) > O.SELL_TURNS[-1]


def test_the_first_trip_is_what_endroute_alone_would_have_dropped_or_less():
    """The excursion pays a round trip where the return leg pays one way, so
    the prefix in front of the last lot can only be the same or shorter than
    ENDROUTE alone's -- never later, which is the one direction that would
    hand the denial back."""
    board = dict(PIN_BOARDS)["d29near"]
    e = _drop_turns(board, endroute=True, endroute2=False, split=False)
    s = _drop_turns(board, endroute=True, endroute2=True, split=True)
    for u, ts in s.items():
        if u in e and len(ts) > 1:
            assert ts[0] <= max(e[u]), (u, ts, e[u])


def test_the_deadline_knob_moves_the_first_drop():
    board = dict(PIN_BOARDS)["d29near"]
    late = _drop_turns(board, endroute=True, endroute2=True, split=True)
    early = _drop_turns(board, endroute=True, endroute2=True, split=True,
                        ENDROUTE2_SPLIT_TURN=O.SELL_TURNS[1])
    for u, ts in early.items():
        if len(ts) > 1:
            assert ts[0] <= O.SELL_TURNS[1], (u, ts)
    assert late != early


def test_the_terminal_day_does_not_widen_the_bank_lot_row():
    """`DROP_ON`'s `gain` already offers the block's whole banked yield on the
    day's LAST lot, which is the row the first trip lands in front of. Widening
    `BANK_LOT`'s row as well would only pull day 29's dawn shed onto turn 10,
    which is `ENDSELL`'s measured -68, so it is gated off."""
    board = dict(PIN_BOARDS)["d29near"]

    t = O.SELL_TURNS[P.BANK_LOT]

    def lot_rows(split):
        with _knobs(True, True, split):
            op, a, q = _plan(_view(**board))[3:6]
        sel = op[t] == O.MO_SELL
        return tuple(sorted(zip(a[t][sel].tolist(), q[t][sel].tolist())))

    assert lot_rows(True) == lot_rows(False)


# =========================================================================
# the asserts
# =========================================================================

@pytest.mark.parametrize("e,e2", [(False, False), (True, False), (False, True)])
def test_it_falls_back_to_the_off_program_without_both_halves(e, e2):
    """The refusal moved from an assert to the VECTOR when these switches became
    genes (`plan._sw_all`, 2026-09-18): SPLIT stands on ENDROUTE2's turns and
    ENDROUTE2 stands on ENDROUTE's row, and a gene block cannot raise at a draw
    the ES is free to make.  Without either half the day is the SPLIT-off day,
    byte for byte -- the module-level assert still refuses the TREE."""
    board = dict(PIN_BOARDS)["d29near"]
    with _knobs(e, e2, True):
        got = _digest(_plan(_view(**board)))
    with _knobs(e, e2, False):
        want = _digest(_plan(_view(**board)))
    assert got == want


def test_the_module_asserts_agree_with_the_defaults():
    assert (P.O.SELL_TURNS[0] <= P.ENDROUTE2_SPLIT_TURN
            <= P.O.SELL_TURNS[-1])
    assert P.ENDROUTE2_SPLIT_MIN_VALUE >= 0
    assert P.ENDROUTE2_SPLIT_MAX_TURNS >= 1


if __name__ == "__main__":                  # the pristine-tree subprocess
    if "--digests" in sys.argv:
        if "--arm" in sys.argv:
            i = sys.argv.index("--arm")
            e = sys.argv[i + 1] == "True"
            e2 = sys.argv[i + 2] == "True"
            got = _own_digests(endroute=e, endroute2=e2)
        else:
            # The archived tree's own ENDROUTE arm, but through `_knobs` so
            # `OTHER_SHIPPED` is pinned on this end of the comparison too --
            # `PRE_SWITCH` predates PUMPCLIP and both names exist there, so
            # the pin stays a ONE-switch pin.
            got = _own_digests(endroute=P.ENDROUTE_ON,
                               endroute2=getattr(P, "ENDROUTE2_ON", False))
        for name, digest in got.items():
            print(name, digest)
