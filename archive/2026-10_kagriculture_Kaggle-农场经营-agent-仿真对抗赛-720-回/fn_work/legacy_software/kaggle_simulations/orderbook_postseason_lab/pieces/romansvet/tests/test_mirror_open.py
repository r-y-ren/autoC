"""`plan.MIRROR_OPEN_ON`: the engine class's opening as ONE package.

Every PIECE of the top-10 opening lost alone on our planner (the day-0 melon
plate `MELON_OPEN_ON` -16,224 with their purse +15,547,
`docs/strategy/2026-09-16-meloneng.md`; the forced top opening 94 -> 26 %,
`2026-09-09-forced-opening*.md`; tiles and hands together -4,835,
`2026-09-16-jointlift.md`).  This switch is the three of them as one package
over days 0-`MIRROR_LAST_DAY`: the melon plate through the existing
`_melon_open` machinery, a `crew_target` FLOOR so the plate does not vacate the
output the shared pot pays us for, and a bought-wheat leg so the feed the plate
displaces is bought back.

The pin is the OFF half: with the switch at its module default this tree's
plans are byte for byte the SHIPPED tree's (`_pin.SHIPPED`).  The ON half is
read in the engine, not here; the three behaviour tests below only prove that
each leg of the package actually reaches the plan it is supposed to reach.
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

from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0):
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
        mkt_inv=np.full(spec.N_PRODUCTS, int(spec.MARKET_I0), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


#: Day 0 is the opening board this switch rewrites; the rest are the ordinary
#: mid-game boards every pin in this suite uses, so the OFF identity covers the
#: days the switch is silent on as well as the day it is not.
PIN_BOARDS = (
    ("open", dict(day=0, n_wh=0, money=10_000, nquad=1)),
    ("open_rich", dict(day=0, n_wh=0, money=60_000, nquad=2)),
    ("early", dict(day=5, n_wh=8, shed_wh=20)),
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("late", dict(day=20, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)


def _digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _own_digests():
    return _digests()


def _tree_digests(ref=_pin.SHIPPED):
    """The same five plans, built by a pristine `git archive <ref> src` tree in
    a subprocess -- the pin is a committed tree, not this file's own output."""
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
# OFF: the shipped program, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.MIRROR_OPEN_ON is False
    assert P.open_board() is False
    assert P.open_tiles() == P.MELON_OPEN_TILES
    assert (P.MIRROR_MELON_TILES, P.MIRROR_HANDS_D0_9, P.MIRROR_WHEAT_BUY,
            P.MIRROR_LAST_DAY) == (12, 7, 9, 9)


def test_off_is_the_shipped_tree_byte_for_byte():
    assert _own_digests() == _tree_digests()


# =========================================================================
# ON: each leg reaches the plan
# =========================================================================

def _knob(**kw):
    was = {k: getattr(P, k) for k in kw}
    for k, v in kw.items():
        setattr(P, k, v)
    return was


def _restore(was):
    for k, v in was.items():
        setattr(P, k, v)


def test_on_the_melon_plate_claims_the_opening_day():
    """Leg (a): day 0's plant mix hands MELON `MIRROR_MELON_TILES`, paid for in
    `_MELON_PAY_RANK` order (wheat last), with `sum(plant_target)` preserved."""
    was = _knob(MIRROR_OPEN_ON=True)
    try:
        tgt = np.full(spec.N_CROPS, 4, np.int32)
        m = P._melon_open(np, _view(day=0, n_wh=0),
                          _macro()._replace(plant_target=tgt))
        got = np.asarray(m.plant_target)
        assert int(got[spec.I_MELON]) == min(P.MIRROR_MELON_TILES, int(tgt.sum()))
        assert int(got.sum()) == int(tgt.sum())
        assert int(got[spec.I_WHEAT]) >= int(
            np.delete(got, [spec.I_MELON, spec.I_WHEAT]).max())
    finally:
        _restore(was)


def test_on_the_crew_floor_is_a_floor_inside_the_window_only():
    """Leg (b): `crew_target` is raised to the floor on d0-9 and never lowered,
    and day 10 keeps the decode's own number."""
    was = _knob(MIRROR_OPEN_ON=True)
    try:
        for day, have, want in ((0, 2, P.MIRROR_HANDS_D0_9),
                                (9, 11, 11),
                                (10, 2, 2)):
            m = P._mirror_crew(np, _view(day=day),
                               _macro()._replace(crew_target=np.int32(have)))
            assert int(np.asarray(m.crew_target)) == want, (day, have)
    finally:
        _restore(was)


def test_on_the_wheat_leg_asks_inside_the_window_only():
    """Leg (c): the extra BUY units are asked for on d0-9 and nowhere else."""
    assert int(P._mirror_wheat_ask(np, np.int32(0))) == P.MIRROR_WHEAT_BUY
    assert int(P._mirror_wheat_ask(np, np.int32(9))) == P.MIRROR_WHEAT_BUY
    assert int(P._mirror_wheat_ask(np, np.int32(10))) == 0


def test_on_changes_the_opening_board():
    """The package is not inert: with it on, day 0's plan differs."""
    off = _digests()["open"]
    was = _knob(MIRROR_OPEN_ON=True)
    try:
        assert _digests()["open"] != off
    finally:
        _restore(was)


if __name__ == "__main__":
    for n, d in _own_digests().items():
        print(n, d)
