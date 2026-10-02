"""`plan.FERT_RESERVE_ON`: fertilizer is an INPUT, so the lots sell the surplus.

`docs/strategy/2026-09-16-v45-notebook.md` sect.2.7 (`_r85_fertilizer`) and
`2026-09-16-nbintel2.md` sect.6 item 3, re-derived here from the board rather
than from their tape.  OFF the day reserves `n_fert_eff` -- TODAY's
applications -- and hands every other shed unit to the lot greedy.  ON a
backward recurrence over `day+1 .. day+FERT_RESERVE_DAYS` adds the applications
the days ahead will want and the herd will not make, and only the surplus over
that is sellable.

THE SWITCH SHIPS OFF: `docs/strategy/2026-09-16-fertreserve.md` -- the
instrument prices the whole surface at 4 starved applications and 8 bought units
a game against 218 units sold on a quote that only ever walks down, and the
ENG22 kill gate reads the increment over the shipped pair.
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, sys.argv[sys.argv.index("--digests") + 1]
                if "--digests" in sys.argv else "src")

import contextlib

import numpy as np

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

# `kagg3` FIRST, and only then `test_budget_order` -- which does its own
# `sys.path.insert(0, "src")` and imports `kagg3` on the way in, so imported
# above it the `--digests` subprocess would load THIS tree's planner and the
# pins would compare the tree with itself (`tests/test_lot4.py`, 2026-09-16).
from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


def _view(day=10, money=20_000, n_to=6, n_wh=4, age=4, n_an=0, shed_fert=0,
          shed_wh=0, t_fert=-1, yld=2, nquad=2, shops=0,
          mkt_inv=spec.MARKET_I0):
    """A board with a fertilizer-hungry crop, a herd and shed fertilizer -- the
    three things the reserve reads.  Tomato is `CROP_ONGOING`, so its tiles want
    an application every three days all season."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_day, t_yield = z.copy(), z.copy()
    kind[:n_to] = spec.KIND_PLANT
    occ[:n_to] = spec.I_TOMATO
    kind[n_to:n_to + n_wh] = spec.KIND_PLANT
    occ[n_to:n_to + n_wh] = spec.I_WHEAT
    t_day[:n_to + n_wh] = day - age
    t_yield[:n_to + n_wh] = yld
    a0 = n_to + n_wh
    kind[a0:a0 + n_an] = spec.KIND_PASTURE
    occ[a0:a0 + n_an] = spec.I_MILK - spec.N_PRODUCTS  # placeholder, reset below
    occ[a0:a0 + n_an] = 0                              # animal index 0
    tf = z - 1
    tf[:n_to + n_wh] = t_fert
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_FERT] = shed_fert
    shed[spec.I_WHEAT] = shed_wh
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=tf, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, int(mkt_inv), np.int32),
        shops=np.full(spec.N_SHOPS, int(shops), np.int32))


def _sell_macro():
    """A zero reservation price, so the lot greedy will actually sell -- the
    reserve is a QUANTITY, and a board whose `hold` blocks the sale outright
    cannot show it."""
    return _macro(hold=np.zeros(spec.N_PRODUCTS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _sell_macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


PIN_BOARDS = (
    ("bind", dict(day=10, n_to=6, n_wh=4, n_an=0, shed_fert=20)),
    ("herd", dict(day=10, n_to=6, n_wh=4, n_an=6, shed_fert=20)),
    ("covered", dict(day=10, n_to=6, n_wh=4, n_an=0, shed_fert=20, t_fert=14)),
    ("empty", dict(day=10, n_to=0, n_wh=8, n_an=0, shed_fert=20)),
    ("terminal", dict(day=29, n_to=6, n_wh=4, n_an=0, shed_fert=20)),
)

#: The commit this branch sits on: master's shipped pair, whose planner has no
#: `FERT_RESERVE_ON` at all.  A SHA and not `HEAD~1`, so the pin keeps its
#: meaning after the branch is merged and master moves on.
PRE_SWITCH = "4054968"


@contextlib.contextmanager
def _knob(on=True, days=None, num=None, den=None):
    """Set after import, exactly how every runner (`S/drainpin/on2b.py`'s comma
    list, `S/combo2/run_all.sh`) sets it for the measured legs."""
    was = (P.FERT_RESERVE_ON, P.FERT_RESERVE_DAYS,
           P.FERT_RESERVE_SUPPLY_NUM, P.FERT_RESERVE_SUPPLY_DEN)
    P.FERT_RESERVE_ON = on
    if days is not None:
        P.FERT_RESERVE_DAYS = days
    if num is not None:
        P.FERT_RESERVE_SUPPLY_NUM = num
    if den is not None:
        P.FERT_RESERVE_SUPPLY_DEN = den
    try:
        yield
    finally:
        (P.FERT_RESERVE_ON, P.FERT_RESERVE_DAYS,
         P.FERT_RESERVE_SUPPLY_NUM, P.FERT_RESERVE_SUPPLY_DEN) = was


def _digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _tree_digests(ref=PRE_SWITCH):
    """The same five plans built by a pristine `git archive <ref> src` tree in a
    subprocess -- the pin is a committed tree, not this file's own output."""
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
# OFF is master, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.FERT_RESERVE_ON is False


def test_off_plan_is_byte_identical_to_master():
    """The whole-plan digest of five boards against a pristine master tree."""
    assert _digests() == _tree_digests()


def test_off_builds_no_reserve_at_all():
    """OFF the call site is the bare `d.n_fert_eff` -- the helper is never
    entered, so no array the switch owns exists on the OFF path."""
    calls = []
    orig = P._fert_future_reserve
    P._fert_future_reserve = lambda *a, **k: calls.append(1) or orig(*a, **k)
    try:
        for _n, kw in PIN_BOARDS:
            _plan(_view(**kw))
    finally:
        P._fert_future_reserve = orig
    assert calls == []


# =========================================================================
# THE RECURRENCE
# =========================================================================

def _reserve(view, mask=None, **knob):
    m = np.zeros(spec.N_TILES, bool) if mask is None else mask
    with _knob(**knob):
        return int(P._fert_future_reserve(np, view, m))


def test_uncovered_tiles_want_one_application_each_inside_the_window():
    """Six standing tomato tiles, no herd, nothing covered: every tile wants an
    application tomorrow and the three-day cycle puts none on the next two.
    The four wheat tiles are past `t_day + harvest_age` on day 10 and are not
    demand at all -- which is the `last` clamp, tested on its own below."""
    v = _view(day=10, n_to=6, n_wh=4, n_an=0)
    assert _reserve(v) == 6


def test_the_herd_is_netted_off_day_by_day():
    """Six animals make six units a day, so ten applications on one day of the
    window leave four."""
    v = _view(day=10, n_to=6, n_wh=4, n_an=2)
    assert _reserve(v) == 4
    assert _reserve(_view(day=10, n_to=6, n_wh=4, n_an=6)) == 0


def test_the_supply_discount_turns_the_herd_off():
    """`NUM = 0` is the literal V45 form: demand against stock alone."""
    v = _view(day=10, n_to=6, n_wh=4, n_an=6)
    assert _reserve(v, num=0) == 6


def test_a_covered_tile_is_not_demand_until_its_coverage_lapses():
    """`t_fert = 14` covers through day 14, so a three-day walk from day 10
    reaches nothing."""
    assert _reserve(_view(day=10, n_to=6, n_wh=4, t_fert=14)) == 0
    assert _reserve(_view(day=10, n_to=6, n_wh=4, t_fert=11)) == 6


def test_the_mask_moves_a_tile_out_of_the_window():
    """Tiles the day itself fertilizes are covered to `day + 2`, so a two-day
    walk stops seeing them and a three-day walk finds them again on `day + 3`."""
    v = _view(day=10, n_to=6, n_wh=4)
    m = np.zeros(spec.N_TILES, bool)
    m[:6] = True                                  # the six tomato tiles
    assert _reserve(v, days=2) == 6
    assert _reserve(v, mask=m, days=2) == 0
    assert _reserve(v, mask=m, days=3) == 6


def test_the_walk_is_backward_so_a_later_shortfall_carries_forward():
    """A window whose demand all lands on the LAST day still reserves it on the
    first: coverage to day 12 with a four-day walk puts ten applications on day
    13, and the recurrence carries them back to day 11."""
    v = _view(day=10, n_to=6, n_wh=4, t_fert=12)
    assert _reserve(v, days=2) == 0
    assert _reserve(v, days=3) == 6


def test_a_crop_past_its_last_standing_day_is_not_demand():
    """A one-time crop is harvested at `t_day + harvest_age`; past that the tile
    is bare ground and an application on it is worth nothing."""
    assert _reserve(_view(day=27, n_to=0, n_wh=8, age=6)) == 0
    assert _reserve(_view(day=27, n_to=6, n_wh=0)) == 6


# =========================================================================
# THE SWITCH AT THE CALL SITE
# =========================================================================

def _sold(plan, product):
    """Units of one product the day's market rows SELL (`plan` is
    `(unit_op, unit_a, unit_q, mkt_op, mkt_arg, mkt_qty)`)."""
    op, arg, qty = plan[3], plan[4], plan[5]
    return int(np.asarray(qty)[(np.asarray(op) == O.MO_SELL)
                               & (np.asarray(arg) == product)].sum())


def test_on_holds_shed_fertilizer_back_from_the_lots():
    """The one thing the switch is for: fewer fertilizer units on the day's
    lots, and not one unit of any other product moved."""
    v = _view(day=10, n_to=6, n_wh=4, n_an=0, shed_fert=20)
    off = _plan(v)
    with _knob():
        on = _plan(v)
    assert _sold(off, spec.I_FERT) > _sold(on, spec.I_FERT)
    for p in range(spec.N_PRODUCTS):
        if p != spec.I_FERT:
            assert _sold(off, p) == _sold(on, p), spec.PRODUCTS[p]


def test_a_herd_that_covers_the_demand_leaves_the_plan_alone():
    """Supply at or above demand on every day of the window reserves nothing,
    so the whole plan is the OFF plan -- which is why the ENG22 leg needs the
    `FERT_RESERVE_SUPPLY_NUM = 0` arm as well."""
    v = _view(day=10, n_to=6, n_wh=4, n_an=10, shed_fert=20)
    off = _digest(_plan(v))
    with _knob():
        assert _digest(_plan(v)) == off


def test_the_terminal_day_voids_the_reserve():
    """Day 29 sells whatever the reservation says [LAW, 0.4]."""
    v = _view(day=29, n_to=6, n_wh=4, n_an=0, shed_fert=20)
    off = _digest(_plan(v))
    with _knob():
        assert _digest(_plan(v)) == off


def test_the_whole_switch_traces_under_jit_and_agrees_with_numpy():
    import jax
    import jax.numpy as jnp
    v = _view(day=10, n_to=6, n_wh=4, n_an=3, shed_fert=20)
    with _knob():
        want = _plan(v)
        jv = P.DayView(**{k: (jnp.asarray(x) if hasattr(x, "shape")
                             else jnp.asarray(x))
                          for k, x in v._asdict().items()})
        m = _sell_macro()
        jm = type(m)(**{k: (jnp.asarray(x) if isinstance(x, np.ndarray)
                            else x) for k, x in m._asdict().items()})
        got = jax.jit(lambda w: P.build_day(jnp, w, jm))(jv)
    for a, b in zip(want, got):
        assert (np.asarray(a) == np.asarray(b)).all()


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _digests().items():
        print(_n, _d)
