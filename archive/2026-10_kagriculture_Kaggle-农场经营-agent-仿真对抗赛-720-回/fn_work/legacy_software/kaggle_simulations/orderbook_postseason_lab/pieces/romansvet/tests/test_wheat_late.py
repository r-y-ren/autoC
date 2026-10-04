"""`plan.WHEAT_LATE_ASK`: a dosed, water-gated wheat-only fill, d10-19.

VOLUMEHI/OPSCENSUS: the d10-19 cap on the 15 hiband ship losses is the ASK
(`n_free` 26-38 against an ask of 0-9, nothing vetoing) and the thing behind
the ask is the UNIT-TURN, not the tile.  The float adds at most
`WHEAT_LATE_ASK * n_free` wheat tiles to the gene's own plant target on days
`WHEAT_LATE_DAY0..DAY1`, and no more than the day's SPARE crew turns can water
at `WHEAT_LATE_TURNS` each (`land_reach`'s own spare-turn numerator).

The claims, in order: the shipped program is the one WITHOUT it -- whole-plan
digests against a pristine `git archive <PRE_SWITCH> src` tree in a subprocess;
the window constants are inert at 0.0; the dose really adds WHEAT and only
wheat; the window edges hold; the turn gate binds and is monotone.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

import _pin

_pin.bootstrap()

import numpy as np

from kagg3 import spec
from kagg3.core import plan as P

from test_endroute import _macro, _view

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

#: The commit this float sits on: `master` at VOLUMEHI/OPSCENSUS, i.e. the ESR
#: + WIDE_PICK_FREE package.  Nothing stands between it and this tree but
#: WHEAT_LATE, so the pin is a ONE-knob comparison.
PRE_SWITCH = "9616aca8"

#: Boards across the window edge, with idle tiles to fill and money to fill
#: them with.  `n_wh` wheat tiles standing means the morning already owes
#: WATER work, which is what the turn gate is charged against.
PIN_BOARDS = (
    ("d9", dict(day=9, n_wh=8, shed_wh=20, shops=2)),
    ("d10", dict(day=10, n_wh=8, shed_wh=20, shops=2)),
    ("d12", dict(day=12, n_wh=8, shed_wh=20, shops=2)),
    ("d16", dict(day=16, n_wh=4, shed_wh=20, shops=2)),
    ("d19", dict(day=19, n_wh=8, shed_wh=20, shops=2)),
    ("d20", dict(day=20, n_wh=8, shed_wh=20, shops=2)),
    ("d29", dict(day=29, n_wh=8, shed_wh=60, shops=2)),
)


def _mac(wheat=6, **kw):
    """A gene that wants wheat today -- `_fill_wheat` only fills in wheat when
    the gene has wheat live (`target[I_WHEAT] > 0`)."""
    t = np.zeros(spec.N_CROPS, np.int32)
    t[spec.I_WHEAT] = wheat
    return _macro(plant_target=t, **kw)


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _mac()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _knobs(ask=None, day0=None, day1=None, turns=None):
    """Set the knobs, keeping whatever the module had.  `getattr` with a
    default so this file still runs inside the pristine `--digests` tree,
    where none of the four names exists yet."""
    names = ("WHEAT_LATE_ASK", "WHEAT_LATE_DAY0", "WHEAT_LATE_DAY1",
             "WHEAT_LATE_TURNS")
    was = tuple(getattr(P, n, None) for n in names)
    for n, v in zip(names, (ask, day0, day1, turns)):
        if v is not None:
            setattr(P, n, v)
    return names, was


def _restore(names, was):
    for n, v in zip(names, was):
        if v is not None:
            setattr(P, n, v)


def _digests(**kw):
    names, was = _knobs(**kw)
    try:
        return {n: _digest(_plan(_view(**b))) for n, b in PIN_BOARDS}
    finally:
        _restore(names, was)


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


def _planted(view, macro=None):
    """Tiles the day's plan actually PLANTs, per crop."""
    from kagg3.core import ops as O
    op, arg = _plan(view, macro)[0:2]
    out = np.zeros(spec.N_CROPS, np.int32)
    for c in range(spec.N_CROPS):
        out[c] = int(((op == O.OP_PLANT) & (arg == c)).sum())
    return out


# =========================================================================
# the shipped program
# =========================================================================

def test_the_float_ships_at_zero_and_its_window_is_the_census_window():
    assert P.WHEAT_LATE_ASK == 0.0
    assert (P.WHEAT_LATE_DAY0, P.WHEAT_LATE_DAY1) == (10, 19)
    assert P.WHEAT_LATE_TURNS == 6


def test_zero_is_the_pre_knob_tree_byte_for_byte():
    """The claim the judge rests on: at 0.0 this tree decodes the same
    six-array plan as `PRE_SWITCH` on every board, inside the window too."""
    assert _digests() == _tree_digests()


def test_the_constants_are_inert_while_the_dose_is_zero():
    base = _digests()
    for d0, d1, tn in ((0, 29, 1), (12, 15, 40), (5, 25, 2)):
        assert _digests(ask=0.0, day0=d0, day1=d1, turns=tn) == base, (d0, d1, tn)


# =========================================================================
# what a dose does
# =========================================================================

def test_the_dose_adds_wheat_inside_the_window_and_nothing_outside_it():
    names, was = _knobs()
    try:
        off = {n: _planted(_view(**b)) for n, b in PIN_BOARDS}
        P.WHEAT_LATE_ASK = 1.0
        on = {n: _planted(_view(**b)) for n, b in PIN_BOARDS}
    finally:
        _restore(names, was)
    for n in ("d9", "d20", "d29"):
        assert (off[n] == on[n]).all(), f"{n} moved outside the window"
    inside = [n for n in ("d10", "d12", "d16", "d19")
              if int(on[n][spec.I_WHEAT]) > int(off[n][spec.I_WHEAT])]
    assert inside, f"the dose never added a tile: {off} -> {on}"
    for n in ("d10", "d12", "d16", "d19"):
        for c in range(spec.N_CROPS):
            if c != spec.I_WHEAT:
                assert int(on[n][c]) == int(off[n][c]), \
                    f"{n} moved crop {c}: the fill is wheat-only"


def test_the_dose_is_monotone_and_the_turn_gate_caps_it():
    """More dose is never fewer tiles; and a turn charge big enough to close
    the gate returns the OFF program on every board."""
    view = _view(day=12, n_wh=8, shed_wh=20, shops=2)
    names, was = _knobs()
    try:
        off = int(_planted(view)[spec.I_WHEAT])
        got = []
        for a in (0.25, 0.5, 1.0):
            P.WHEAT_LATE_ASK = a
            got.append(int(_planted(view)[spec.I_WHEAT]))
        P.WHEAT_LATE_ASK = 1.0
        P.WHEAT_LATE_TURNS = 10_000          # one tile costs the whole crew
        shut = _digest(_plan(view))
        P.WHEAT_LATE_ASK = 0.0
        P.WHEAT_LATE_TURNS = 6
        base = _digest(_plan(view))
    finally:
        _restore(names, was)
    assert got == sorted(got), f"the dose is not monotone: {got}"
    assert got[-1] > off, f"the largest dose added nothing: {off} -> {got}"
    assert shut == base, "a closed turn gate is not the OFF program"


def test_a_closed_gate_buys_no_seed_either():
    """The refusal `_wheat_late_cap` documents: zero extra tiles means the
    second grant never runs, so the day does not buy seed it cannot plant."""
    from kagg3.core import ops as O
    view = _view(day=12, n_wh=8, shed_wh=20, shops=2)
    names, was = _knobs()
    try:
        op, arg, qty = _plan(view)[3:6]
        off = int(qty[(op == O.MO_BUY_SEED)].sum()) if hasattr(O, "MO_BUY_SEED") \
            else _digest(_plan(view))
        P.WHEAT_LATE_ASK = 1.0
        P.WHEAT_LATE_TURNS = 10_000
        op, arg, qty = _plan(view)[3:6]
        shut = int(qty[(op == O.MO_BUY_SEED)].sum()) if hasattr(O, "MO_BUY_SEED") \
            else _digest(_plan(view))
    finally:
        _restore(names, was)
    assert off == shut, f"a closed gate still moved the BUY row: {off} -> {shut}"


if "--digests" in sys.argv:
    for _n, _d in _digests().items():
        print(_n, _d)
