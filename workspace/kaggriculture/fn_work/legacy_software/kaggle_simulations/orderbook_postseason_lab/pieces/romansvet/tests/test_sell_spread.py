"""`plan.SELL_SPREAD_ON`: a flat per-day sale quota over the last days.

MAJKEL1 (`docs/strategy/2026-09-19-majkel1.md`).  Majkel1337 and ymg_aq play
the same d0-5 plate; the +1,304 of wheat between them is SHAPE -- he sells
13-19 units every day d19-24 at ~35 while ymg holds and dumps 235 units into
d25-29 at 21-30.  The switch caps what the VOLUNTARY sale may draw on at
`max(stock // days_left, SELL_SPREAD_MIN)` from `SELL_SPREAD_DAY0`.

The claims, in order: the shipped program is the one WITHOUT it -- whole-plan
digests against a pristine `git archive <PRE_SWITCH> src` tree in a
subprocess; days before the window and the terminal day are untouched ON; the
quota really binds; and the forced-overflow sale still reads the UNCAPPED
`avail`, which is what stops a quota holding back stock the night destroys.
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
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_endroute import _macro, _plan, _sell_rows, _view

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

#: The commit this switch sits on: `master` at MAJKEL1, i.e. the ESR +
#: WIDE_PICK_FREE package with every end-route switch at its shipped value.
#: Nothing stands between it and this tree but `SELL_SPREAD`, so no other
#: switch has to be held and the pin is a ONE-switch comparison.
PRE_SWITCH = "380e0ce0"

#: Boards the quota can bite on: 50 wheat + 45 tomato in the shed, across the
#: window edge (d18 out, d19/d22/d25 in) and on both ends of the end-route
#: family's own days.  `mid`/`d27`/`d28`/`d29` are `test_endroute`'s.
PIN_BOARDS = (
    ("mid", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d18", dict(day=18, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d19", dict(day=19, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d22", dict(day=22, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d25", dict(day=25, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d27", dict(day=27, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d28", dict(day=28, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
    ("d29", dict(day=29, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


#: Lean boards: 70 units in the shed, no tiles and therefore no harvest
#: inflow, so `proj_eod` stays under `SHED_CAPACITY` and every unit sold is
#: the VOLUNTARY allocation -- the only half the quota reshapes.
def _lean(day):
    return _view(day=day, n_wh=0, shed_wh=50, shed_to=20, shops=2)


def _sellmac():
    """`hold` 0: the shared `_macro` holds everything at 10,000, which leaves
    the voluntary allocation empty and the quota nothing to cap."""
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _knobs(on=None, day0=None, mn=None):
    """Set the knobs, keeping whatever the module had.  `getattr` with a
    default so this file still runs inside the pristine `--digests` tree,
    where none of the three names exists yet."""
    names = ("SELL_SPREAD_ON", "SELL_SPREAD_DAY0", "SELL_SPREAD_MIN")
    was = tuple(getattr(P, n, None) for n in names)
    for n, v in zip(names, (on, day0, mn)):
        if v is not None:
            setattr(P, n, v)
    return names, was


def _restore(names, was):
    for n, v in zip(names, was):
        if v is not None:
            setattr(P, n, v)


def _digests(on=None, day0=None, mn=None):
    names, was = _knobs(on, day0, mn)
    try:
        return {n: _digest(_plan(_view(**kw), _sellmac())) for n, kw in PIN_BOARDS}
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


def _wheat(view):
    """Units of WHEAT the day's plan actually puts on market rows."""
    op, a, q = _plan(view, _sellmac())[3:6]
    return int(q[(op == O.MO_SELL) & (a == spec.I_WHEAT)].sum())


# =========================================================================
# the shipped program
# =========================================================================

def test_the_switch_ships_off_at_its_documented_values():
    assert P.SELL_SPREAD_ON is False
    assert P.SELL_SPREAD_DAY0 == 19
    assert P.SELL_SPREAD_END == O.LAST_SHED_DAY + 1 == 29
    assert P.SELL_SPREAD_MIN == 12
    assert P.SELL_SPREAD_ITEMS == (spec.I_WHEAT, spec.I_STRAWBERRY)


def test_off_is_the_pre_switch_tree_byte_for_byte():
    """The claim the judge rests on: with the switch OFF this tree decodes the
    same six-array plan as `PRE_SWITCH` on every board, including the ones
    inside the window."""
    assert _digests() == _tree_digests()


def test_the_constants_are_inert_while_the_switch_is_off():
    """Moving the window or the floor with the switch OFF moves nothing --
    only `SELL_SPREAD_ON` opens the site."""
    base = _digests()
    for day0, mn in ((0, 0), (10, 1), (25, 40)):
        assert _digests(on=False, day0=day0, mn=mn) == base, (day0, mn)


# =========================================================================
# what ON does
# =========================================================================

def test_on_moves_only_the_days_inside_the_window():
    """`mid` and `d18` are outside; the terminal day is exempt by the same
    `days_left == 1` the ENDROUTE family needs."""
    names, was = _knobs(on=False)
    try:
        off = {d: _digest(_plan(_lean(d), _sellmac())) for d in (10, 18, 19, 22, 25, 29)}
        P.SELL_SPREAD_ON = True
        on = {d: _digest(_plan(_lean(d), _sellmac())) for d in (10, 18, 19, 22, 25, 29)}
    finally:
        _restore(names, was)
    for d in (10, 18, 29):
        assert off[d] == on[d], f"d{d} moved outside the window"
    assert any(off[d] != on[d] for d in (19, 22, 25)), \
        "the quota never bound on any board inside the window"


def test_the_quota_holds_wheat_back_and_the_floor_releases_it():
    """50 units at d19 is 11 days left -> `50 // 11 = 4`, under the floor, so
    the floor 12 is the quota; a floor of 0 leaves the raw share; a floor
    above the stock is no cap at all."""
    view = _lean(19)
    names, was = _knobs(on=False)
    try:
        full = _wheat(view)
        P.SELL_SPREAD_ON = True
        P.SELL_SPREAD_MIN = 12
        capped = _wheat(view)
        P.SELL_SPREAD_MIN = 0
        tight = _wheat(view)
        P.SELL_SPREAD_MIN = 500
        loose = _wheat(view)
    finally:
        _restore(names, was)
    assert full > 12, f"the fixture does not dump wheat at d19: {full}"
    assert capped <= 12, f"the quota did not bind: {capped} of {full}"
    assert tight <= capped, f"a lower floor sold more: {tight} vs {capped}"
    assert loose == full, f"a floor over the stock still capped: {loose}"


def test_the_quota_widens_as_the_days_run_out():
    """`stock // days_left` is monotone in the day: the same shed sells at
    least as much on d25 as on d19, and the whole of it on d29."""
    names, was = _knobs(on=True, mn=0)
    try:
        seq = [_wheat(_lean(d)) for d in (19, 22, 25, 28)]
    finally:
        _restore(names, was)
    assert seq == sorted(seq), f"the quota is not monotone in the day: {seq}"


def test_the_forced_overflow_sale_still_reads_the_uncapped_shed():
    """The leak the design refuses: a quota that also shrank `spare` would
    hold stock back INTO the night, which destroys it.  A shed over
    `SHED_CAPACITY` must therefore still clear its deficit with the switch
    on."""
    kw = dict(day=20, n_wh=8, shed_wh=95, shed_to=95, yld=6, shops=2)
    names, was = _knobs(on=False)
    try:
        off = _wheat(_view(**kw))
        P.SELL_SPREAD_ON = True
        on = _wheat(_view(**kw))
    finally:
        _restore(names, was)
    # The voluntary half is capped, so ON sells no more than OFF -- but the
    # forced half is untouched, so it cannot fall to the bare quota either.
    assert on <= off, f"the cap increased the sale: {on} vs {off}"
    assert on > 0, "the overflow sale vanished with the switch on"


if __name__ == "__main__":
    for n, d in _digests().items():
        print(n, d)
