"""`plan.PLANT_FILL_LATE_ON`: the v2 board fill, refused until the herd is bought.

`PLANT_FILL_ON` (v2) fills every surplus idle tile with wheat from day 0 and
costs 5.6-6.9k of our own purse on every traced board; its autopsy prices the
loss entirely in the herd (WOOL 152 units to 136, FERTILIZER 191 to 144, EGG
50.6 to 20.9).  The channel is `n_free`: a tile the fill plants today is not
free tomorrow, and `brain.decide` sizes `n_dev` and `animal_count` off exactly
that count.  Traced over three pinned held-out boards
(`docs/strategy/2026-09-09-board-fill.md` sect.3-4), `macro.animal_want` is
zero and `n_build` is 0 on every day after 12, so `_fill_cap`'s reserve is
already 0 there and v2 was spending its herd bill on the *ramp*.  This switch
is v2 with the ramp excluded.

OFF, `if PLANT_FILL_ON or PLANT_FILL_LATE_ON` is the `if PLANT_FILL_ON` it was
and the whole block is dead, so the champion theta decodes byte for byte:
pinned below against a pristine `git archive c5f68ac src` tree, whole-plan digests
on five boards, exactly as `tests/test_crewpush.py` pins its own.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

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

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0):
    """`tests/test_crewpush.py`'s fixture, unchanged, so the two switches this
    report measures together are pinned on one board family."""
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


def _n_plant(plan):
    return int((np.asarray(plan[0]) == O.OP_PLANT).sum())


#: The same five boards `test_crewpush.py` pins, which between them reach the
#: budget walk with a full purse, an empty one, a big board and a small one --
#: every path into the second (fill) grant.
PIN_BOARDS = (
    ("rich", dict(day=12, money=40_000, n_wh=20, shed_wh=20), dict(crew_target=8)),
    ("poor", dict(day=8, money=900, n_wh=8), dict(crew_target=12)),
    ("deep", dict(day=15, money=25_000, n_wh=24, shed_wh=40, shops=2),
     dict(crew_target=16)),
    ("noramp", dict(day=10, money=20_000, n_wh=8, shed_wh=50, shed_to=45), {}),
    ("taxed", dict(day=13, money=30_000, n_wh=16, shed_wh=10),
     dict(crew_target=13, hire_bias=np.int32(-350))),
)


def _own_digests():
    return {n: _digest(_plan(_view(**kw), _macro(**mk))) for n, kw, mk in PIN_BOARDS}


def _head_digests():
    """The same five plans, built by a pristine `git archive c5f68ac src` tree in a
    subprocess -- the pin is the tree this switch was added to, not this file's
    own output."""
    return _pin.tree_digests(__file__, ref=_pin.SHIPPED)


# =========================================================================
# OFF: the shipped program, character for character
# =========================================================================

def test_off_is_the_default():
    assert P.PLANT_FILL_LATE_ON is False
    assert P.PLANT_FILL_ON is False
    assert int(P.PLANT_FILL_FROM_DAY) == 12


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


# =========================================================================
# ON: the day gate, and nothing but the day gate
# =========================================================================

def _fill_case(day):
    """A big board whose macro asks for far fewer tiles than it has and a purse
    that can buy every seed -- the surplus-idle-tile case the fill exists for."""
    view = _view(day=day, money=40_000, nquad=4, yld=4)
    tgt = np.zeros(spec.N_CROPS, np.int32)
    tgt[spec.I_WHEAT] = 3                       # wheat live, far below the board
    return view, _macro(plant_target=tgt)


@pytest.mark.parametrize("day", (0, 5, 8, 11))
def test_on_is_identical_before_the_first_day(monkeypatch, day):
    """A day before `PLANT_FILL_FROM_DAY` plans exactly the OFF plan: `w_fill`
    is zero, `grant` over an all-zero want returns zeros and every maximum
    merges nothing."""
    view, macro = _fill_case(day)
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", False)
    want = _digest(_plan(view, macro))
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", True)
    assert _digest(_plan(view, macro)) == want


def test_on_plants_more_from_the_first_day(monkeypatch):
    """From `PLANT_FILL_FROM_DAY` the fill is live and takes idle tiles."""
    view, macro = _fill_case(int(P.PLANT_FILL_FROM_DAY))
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", False)
    base = _n_plant(_plan(view, macro))
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", True)
    assert _n_plant(_plan(view, macro)) > base


def test_on_matches_v2_from_the_first_day(monkeypatch):
    """On a live day this switch *is* `PLANT_FILL_ON`: the day gate is the only
    thing between them, so the two plans agree byte for byte."""
    view, macro = _fill_case(int(P.PLANT_FILL_FROM_DAY) + 3)
    monkeypatch.setattr(P, "PLANT_FILL_ON", True)
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", False)
    v2 = _digest(_plan(view, macro))
    monkeypatch.setattr(P, "PLANT_FILL_ON", False)
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", True)
    assert _digest(_plan(view, macro)) == v2


def test_the_day_constant_moves_the_gate_and_only_the_gate(monkeypatch):
    """`PLANT_FILL_FROM_DAY` is a day constant: at 8 the day-8 plan becomes the
    v2 plan and the day-7 plan is still the OFF plan."""
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", False)
    off8 = _digest(_plan(*_fill_case(8)))
    monkeypatch.setattr(P, "PLANT_FILL_ON", True)
    v2_8 = _digest(_plan(*_fill_case(8)))
    monkeypatch.setattr(P, "PLANT_FILL_ON", False)
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", True)
    monkeypatch.setattr(P, "PLANT_FILL_FROM_DAY", np.int32(8))
    assert _digest(_plan(*_fill_case(8))) == v2_8 != off8
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", False)
    off7 = _digest(_plan(*_fill_case(7)))
    monkeypatch.setattr(P, "PLANT_FILL_LATE_ON", True)
    assert _digest(_plan(*_fill_case(7))) == off7


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
