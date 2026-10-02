"""`plan.CREW_PUSH_COST_ON`: the crew-target push sized off the hand's own bill.

`CREW-PUSH` (census direction #5, `2026-09-11-codex-defects.md:64-98`): the ramp
pays a flat `CREW_TARGET_PUSH = 400` for every hand up to `macro.crew_target`
while `bills[h]` charges the Fibonacci price in full, so "every hand up to the
target pays for itself" is true only while the marginal is under 400 -- and the
enumeration's argmax stops short of the target on 46/300 board-days at 18.8k
cash.  ON, `crew_push_cum()` builds the push from `spec.HIRE_COST` instead:
`sum` refunds the bill and keeps the tilt (upward), `max` covers only what 400
cannot (the 15th hand and up), `exact` pays the bill alone (downward).

OFF, `crew_push_cum()` is `CREW_TARGET_PUSH * m` and the site's expression is
the shipped one, so the champion theta decodes byte for byte: pinned below
against a pristine `git archive c5f68ac src` tree, whole-plan digests on five
boards, exactly as `tests/test_lot4.py` and `tests/test_shed_deficit.py` pin
their own.
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
    """The `tests/test_lot4.py` / `tests/test_shed_deficit.py` fixture, so all
    three switches are measured on one board family."""
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


def _hires(plan):
    """Hands the day's HIRE row actually books."""
    op = plan[3]
    return int((op == O.MO_HIRE).sum())


#: Five boards that reach the crew enumeration from both sides: a purse that
#: can field the whole ladder (`rich`), one that cannot (`poor`), a target
#: above what 400 covers (`deep`), one the gene never switched on (`noramp`,
#: where `min(h, 0) == 0` makes the push inert whatever the table says), and a
#: negative `hire_bias` that eats the tilt (`taxed`) -- the shape the census
#: found behind the 46/300 refusals.
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
    assert P.CREW_PUSH_COST_ON is False
    assert P.CREW_PUSH_COST_MODE in P.CREW_PUSH_COST_MODES
    m = np.arange(spec.MAX_HANDS + 1, dtype=np.int64)
    assert (P.crew_push_cum() == P.CREW_TARGET_PUSH * m).all()
    # OFF the mode is not read at all: a runner that set it and forgot to flip
    # the switch ships the shipped program.
    for mode in P.CREW_PUSH_COST_MODES:
        assert (P.crew_push_cum(mode) == P.CREW_TARGET_PUSH * m).all()


def test_off_plan_is_byte_identical_to_head():
    """The whole plan tuple, hashed, against a pristine HEAD tree."""
    assert _own_digests() == _head_digests()


# =========================================================================
# The table: what each mode charges the ramp
# =========================================================================

def test_sum_refunds_the_fib_bill_and_keeps_the_tilt(monkeypatch):
    """`sum` = the shipped push plus `HIRE_BILLS[m]`, so inside the target the
    marginal read is `dvalue + hire_bias + 400` whatever the hand costs."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    cum = P.crew_push_cum("sum")
    m = np.arange(spec.MAX_HANDS + 1)
    assert (cum == P.CREW_TARGET_PUSH * m + P.HIRE_BILLS[:spec.MAX_HANDS + 1]).all()
    marg = np.diff(cum.astype(np.int64))
    assert (marg == P.CREW_TARGET_PUSH + spec.HIRE_COST[:spec.MAX_HANDS]).all()


def test_max_only_covers_what_400_cannot(monkeypatch):
    """`max` is the minimal repair: identical to OFF through the 14th hand
    (fib 377 < 400) and only the 15th (610) and 16th (987) move.  B's
    `crew_target` tops out at 13, so this mode is the falsifier -- it must be
    INERT on every board whose target the gene can decode below 15."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    cum = P.crew_push_cum("max")
    off = P.CREW_TARGET_PUSH * np.arange(spec.MAX_HANDS + 1)
    assert (cum[:15] == off[:15]).all()
    assert (cum[15:] > off[15:]).all()


def test_exact_is_the_bill_alone_and_is_the_downward_sign(monkeypatch):
    """`exact` pays each hand its own fib price and nothing more -- strictly
    below OFF wherever the marginal is under 400, i.e. every hand through the
    14th, which is the opposite sign the census says was never measured in this
    shape."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    cum = P.crew_push_cum("exact")
    assert (cum == P.HIRE_BILLS[:spec.MAX_HANDS + 1]).all()
    off = P.CREW_TARGET_PUSH * np.arange(spec.MAX_HANDS + 1)
    assert (cum[1:15] < off[1:15]).all()


def test_every_mode_is_monotone_and_starts_at_zero(monkeypatch):
    """The table is indexed by `min(h, crew_target)`, so entry 0 has to be the
    zero push a zero target decodes (exact inertness at zero theta) and the
    sequence has to be non-decreasing or a bigger crew could score below a
    smaller one for free."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    for mode in P.CREW_PUSH_COST_MODES:
        cum = P.crew_push_cum(mode)
        assert cum.dtype == np.int32 and cum.shape == (spec.MAX_HANDS + 1,)
        assert cum[0] == 0
        assert (np.diff(cum.astype(np.int64)) > 0).all(), mode


def test_an_unknown_mode_is_refused(monkeypatch):
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", "fib")
    with pytest.raises(ValueError):
        P.crew_push_cum()


# =========================================================================
# ON: what the plan does with it
# =========================================================================

def test_a_zero_target_is_inert_in_every_mode(monkeypatch):
    """`min(h, 0) == 0` indexes entry 0, so a theta that never switched the
    ramp on decodes byte for byte whatever the table holds -- the same
    "exactly inert at zero" property the gene was built with."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    for kw in (dict(day=12, money=40_000, n_wh=20, shed_wh=20),
               dict(day=10, money=20_000, n_wh=8, shed_wh=50, shed_to=45)):
        monkeypatch.setattr(P, "CREW_PUSH_COST_ON", False)
        off = _digest(_plan(_view(**kw), _macro(crew_target=np.int32(0))))
        monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
        for mode in P.CREW_PUSH_COST_MODES:
            monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", mode)
            assert _digest(_plan(_view(**kw), _macro(crew_target=np.int32(0)))) == off


def test_sum_never_books_fewer_hands_than_off(monkeypatch):
    """Inside the target `sum` adds `HIRE_BILLS[m] >= 0` to every candidate's
    score, and the added term is non-decreasing in `h`, so the argmax cannot
    move DOWN -- and `max` (inert below the 15th hand) cannot move at all."""
    for money in (2_000, 8_000, 20_000, 60_000):
        for target in (4, 8, 12, 13, 16):
            for bias in (0, -350):
                view = _view(day=13, money=money, n_wh=20, shed_wh=20)
                mac = _macro(crew_target=np.int32(target),
                             hire_bias=np.int32(bias))
                monkeypatch.setattr(P, "CREW_PUSH_COST_ON", False)
                off = _hires(_plan(view, mac))
                monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
                monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", "sum")
                assert _hires(_plan(view, mac)) >= off, (money, target, bias)
                monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", "max")
                assert _hires(_plan(view, mac)) == off, (money, target, bias)


def test_sum_buys_the_hand_the_flat_push_refused(monkeypatch):
    """The lever itself: a board where a negative `hire_bias` plus the fib
    marginal outruns 400 books fewer hands than the gene asked for, and the
    bill-sized push books more of them."""
    view = _view(day=14, money=50_000, n_wh=30, shed_wh=30, shops=2)
    mac = _macro(crew_target=np.int32(13), hire_bias=np.int32(-350))
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", False)
    off = _hires(_plan(view, mac))
    assert off < 13, off                       # the refusal the census measured
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", "sum")
    assert _hires(_plan(view, mac)) > off


def test_affordability_is_untouched(monkeypatch):
    """The push is a SCORE, not a purse: `bills[h] + cash_reserve <= money` is
    the same test in every mode, so a farm that cannot field the ladder does
    not field it because the table got bigger."""
    for money in (0, 40, 200, 900):
        view = _view(day=9, money=money, n_wh=8)
        mac = _macro(crew_target=np.int32(16), hire_bias=np.int32(0))
        monkeypatch.setattr(P, "CREW_PUSH_COST_ON", False)
        off = _hires(_plan(view, mac))
        for mode in P.CREW_PUSH_COST_MODES:
            monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
            monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", mode)
            on = _hires(_plan(view, mac))
            assert int(P.HIRE_BILLS[on]) <= money, (money, mode, on)
            assert on <= max(off, 0) + spec.MAX_HANDS


def test_past_the_target_the_push_is_flat(monkeypatch):
    """`min(h, crew_target)` caps the table read, so two boards that differ
    only above the target read the same push: a crew bigger than the ramp asked
    for is still argued from the day's work, in every mode."""
    monkeypatch.setattr(P, "CREW_PUSH_COST_ON", True)
    for mode in P.CREW_PUSH_COST_MODES:
        monkeypatch.setattr(P, "CREW_PUSH_COST_MODE", mode)
        cum = P.crew_push_cum()
        for target in (3, 7, 13):
            reads = [int(cum[min(h, target)]) for h in range(1, spec.MAX_HANDS + 1)]
            assert reads[target - 1:] == [int(cum[target])] * (spec.MAX_HANDS - target + 1)


if __name__ == "__main__":                      # the HEAD-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
