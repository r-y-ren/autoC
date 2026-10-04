"""`plan.HIRE_BIAS_ZERO_ON`: the forward horizon as a REPLACE, not an ADD.

`docs/strategy/2026-09-10-forward-admit.md` measured `FORWARD_ADMIT_ON` as an
addition -- the hire scan is handed tomorrow's work while `macro.hire_bias`,
the trained tilt that exists *because* the scan could only see today, is still
on the gain line.  Both channels say "hire earlier", so the board pays twice
(HELD42 -8,676; the quiet-tile discounted shape -2,628).  This switch zeroes
the tilt so the horizon is the only thing arguing for the hand.

OFF is the shipped program byte for byte; ON is a one-term edit of 1.5's gain
line and nothing else.
"""
from __future__ import annotations

import os
import sys

import _pin

_pin.bootstrap()                      # kagg3 FIRST, from the tree under test

import contextlib

import numpy as np

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

from test_budget_order import _macro   # safe: kagg3 is already loaded

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


PIN_BOARDS = (
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("town", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, shops=2)),
)

#: The switch string the shipped FT2 package runs under, applied after import
#: exactly as `S/drainpin/on2b.py` applies it for every measured leg.
SHIPPED_SWITCHES = dict(
    OPEN_PUMP_ON=True, TAIL_FILL_ON=True, BANK_BEFORE_LOT_ON=True,
    HIRE_ROW_ON=True, LOT4_ON=True, LOT4_TURN=17,
    SELL_SLOT_PRIORITY_ON=True, FERT_TIMING_ON=True, FERT_TIMING_DAYS=2)


@contextlib.contextmanager
def _knobs(**kw):
    was = {k: getattr(P, k) for k in kw}
    for k, v in kw.items():
        setattr(P, k, v)
    try:
        yield
    finally:
        for k, v in was.items():
            setattr(P, k, v)


def _digests():
    """Ten plans: five boards x {biased, unbiased} theta, under the shipped
    switch string.  The biased half is the one the switch can move."""
    out = {}
    with _knobs(**SHIPPED_SWITCHES):
        for n, kw in PIN_BOARDS:
            v = _view(**kw)
            out[n] = _pin.digest(P.build_day(np, v, _macro()))
            out[n + "_bias"] = _pin.digest(
                P.build_day(np, v, _macro(hire_bias=np.int32(250))))
    return out


def _own(zero=None):
    if zero is None:
        return _digests()
    with _knobs(HIRE_BIAS_ZERO_ON=zero):
        return _digests()


# ==========================================================================
# OFF identity
# ==========================================================================

def test_default_is_off():
    assert P.HIRE_BIAS_ZERO_ON is False


def test_off_plan_is_byte_identical_to_the_shipped_tree():
    """THE IDENTITY PIN.  Whole plan tuples, hashed, against a pristine
    `git archive c5f68ac src` -- the tree of Kaggle upload 56284867.  Equal
    means this branch added one constant and no behaviour."""
    assert _own(zero=False) == _pin.tree_digests(__file__)


def test_module_default_matches_the_off_pin():
    assert _own() == _own(zero=False)


# ==========================================================================
# ON: one term, the right one
# ==========================================================================

def _hires(view, macro):
    op, _arg, qty = P.build_day(np, view, macro)[3:6]
    return int(qty[op == O.MO_HIRE].sum())


def test_on_is_inert_on_a_theta_whose_bias_is_zero():
    """`x + 0 * h == x`: the switch can only remove a term that is there."""
    with _knobs(**SHIPPED_SWITCHES):
        for _n, kw in PIN_BOARDS:
            v = _view(**kw)
            a = _pin.digest(P.build_day(np, v, _macro()))
            with _knobs(HIRE_BIAS_ZERO_ON=True):
                b = _pin.digest(P.build_day(np, v, _macro()))
            assert a == b, kw


def test_on_makes_a_biased_theta_plan_as_an_unbiased_one():
    """The switch's whole claim: `hire_bias` reaches the program through one
    term of 1.5's gain line, so zeroing it is exactly a theta whose gene is 0.
    Ten plans, whole-tuple digests, on the shipped switch string."""
    biased = {k: v for k, v in _own(zero=False).items() if k.endswith("_bias")}
    zeroed = {k: v for k, v in _own(zero=True).items() if k.endswith("_bias")}
    plain = {k + "_bias": v for k, v in _own(zero=False).items()
             if not k.endswith("_bias")}
    assert zeroed == plain          # ON == the gene at zero
    assert biased != plain          # and the tilt really was doing something


def test_on_cuts_the_crew_a_biased_theta_buys():
    """A +250 tilt is worth 13 hands off `HIRE_BILLS`' fib marginals
    [brain.HIRE_BIAS_MAX]; zeroed, the day is back to arguing from its work.
    Read without `HIRE_ROW_ON`, which clips the emitted row to the hands the
    route loads and hides the enumeration behind it."""
    v = _view(day=10, money=60_000, n_wh=8, shed_wh=50, shed_to=45)
    m = _macro(hire_bias=np.int32(250))
    with _knobs(**{**SHIPPED_SWITCHES, "HIRE_ROW_ON": False}):
        on_bias = _hires(v, m)
        with _knobs(HIRE_BIAS_ZERO_ON=True):
            zeroed = _hires(v, m)
        assert on_bias > zeroed
        assert zeroed == _hires(v, _macro())


def test_on_leaves_the_crew_ramp_alone():
    """`crew_target` (g10) is a different channel and is deliberately not
    ablated: a theta with a ramp and no tilt hires the same crew either way."""
    v = _view(day=10, money=60_000, n_wh=8, shed_wh=50, shed_to=45)
    m = _macro(crew_target=np.int32(11))
    with _knobs(**{**SHIPPED_SWITCHES, "HIRE_ROW_ON": False}):
        a = _hires(v, m)
        with _knobs(HIRE_BIAS_ZERO_ON=True):
            b = _hires(v, m)
        assert a == b and a > 0


def _melon_open(day, n=12, money=3000):
    """The forced opening: `n` melon planted on day 0.  Their bonus window
    opens at age 6 (`spec.CROP_WINDOW_START[I_MELON]`), so on days 1-5 not one
    of them emits an op -- the failure FORWARD_ADMIT exists for."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:n] = spec.KIND_PLANT
    occ[:n] = spec.I_MELON
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(1), price=BASE_PRICE.copy())


def test_forward_admit_override_still_works_as_a_switch():
    """The other half of the arm: `FORWARD_ADMIT_ON` beats `macro.forward_days`,
    a zero horizon is the identity, and a one-day horizon on day 5 admits the
    melon that matures on day 6.  Read with `HIRE_ROW_ON` OFF -- see the test
    below for why."""
    v = _melon_open(day=5, money=9_000)
    m = _macro()
    with _knobs(**{**SHIPPED_SWITCHES, "HIRE_ROW_ON": False}):
        base = _hires(v, m)
        with _knobs(FORWARD_ADMIT_ON=True, FORWARD_ADMIT_DAYS=0):
            assert _hires(v, m) == base
        with _knobs(FORWARD_ADMIT_ON=True, FORWARD_ADMIT_DAYS=1):
            assert _hires(v, m) > base          # the horizon reaches the window
            override = _pin.digest(P.build_day(np, v, m))
        # OFF, the gene rules and decodes to the same program
        gene = _pin.digest(P.build_day(np, v, _macro(forward_days=np.int32(1))))
        assert gene == override


def test_the_shipped_hire_row_clips_the_whole_horizon_on_a_silent_field():
    """MEASURED 2026-09-17, and the reason this arm is not the fix it looks
    like: `HIRE_ROW_ON` (shipped ON) clamps the HIRE row to the hands the
    day's route actually LOADS, and a field whose crops are all outside their
    window gives the route nothing to load.  So on exactly the days
    FORWARD_ADMIT targets, the hands the projected scan buys are clipped
    straight back out and the whole plan tuple is byte-identical."""
    m = _macro()
    with _knobs(**SHIPPED_SWITCHES):                      # HIRE_ROW_ON True
        for d in (1, 3, 5, 7):
            v = _melon_open(day=d, money=9_000)
            off = _pin.digest(P.build_day(np, v, m))
            for days in (1, 2, 3):
                with _knobs(FORWARD_ADMIT_ON=True, FORWARD_ADMIT_DAYS=days):
                    assert _pin.digest(P.build_day(np, v, m)) == off, (d, days)


if __name__ == "__main__":                 # the pristine-tree subprocess
    for _n, _d in _own().items():
        print(_n, _d)
