"""`plan.FERT_DUMP_ON`: from `FERT_DUMP_DAY` a fertilizer unit's sale is worth
its quote PLUS what dumping it takes off the rival's remaining fertilizer
revenue, so the application has to clear both.

FERTILIZER is the one product the town never drains, so its market inventory is
a running total of net sells and its quote is exactly linear in it (0.2 coins a
unit).  One extra dumped unit therefore takes 0.2 off every later quote -- the
rival's and OURS -- and the denial term's sign is the difference of the two
remaining schedules.  Measured on 10 real-engine boards in
`docs/strategy/2026-09-16-fertdenial.md` / `S/fertdenial/`.

THE SWITCH SHIPS OFF unless the legs in that document say otherwise.
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


#: `age = 6` is what puts a real application on the board: a tomato planted six
#: days ago has two more fires inside the three-day fertilizer window, so
#: `fert_marginal_value` prices the application at 120 against a 100-coin quote
#: and `fert_cand` admits all six tiles.  `age = 4` leaves the day with nothing
#: to refuse, which is the OFF-identity control.
PIN_BOARDS = (
    ("early", dict(day=10, n_to=6, n_wh=4, n_an=0, age=6, shed_fert=20)),
    ("late", dict(day=22, n_to=6, n_wh=4, n_an=0, age=6, shed_fert=20)),
    ("late-herd", dict(day=22, n_to=6, n_wh=4, n_an=6, age=6, shed_fert=20)),
    ("late-cheap", dict(day=22, n_to=6, n_wh=4, n_an=0, age=6, shed_fert=20,
                        mkt_inv=spec.MARKET_I0 + 400)),
    ("terminal", dict(day=29, n_to=6, n_wh=4, n_an=0, age=6, shed_fert=20)),
)

#: The commit this branch sits on: master's shipped pair, whose planner has no
#: `FERT_DUMP_ON` at all.  A SHA and not `HEAD~1`, so the pin keeps its meaning
#: after the branch is merged and master moves on.
PRE_SWITCH = "4c6565b"


@contextlib.contextmanager
def _knob(on=True, day=None, bonus=None):
    """Set after import, exactly how every runner (`S/drainpin/on2b.py`'s comma
    list, `S/combo2/run_all.sh`) sets it for the measured legs."""
    was = (P.FERT_DUMP_ON, P.FERT_DUMP_DAY, P.FERT_DUMP_BONUS)
    P.FERT_DUMP_ON = on
    if day is not None:
        P.FERT_DUMP_DAY = day
    if bonus is not None:
        P.FERT_DUMP_BONUS = bonus
    try:
        yield
    finally:
        (P.FERT_DUMP_ON, P.FERT_DUMP_DAY, P.FERT_DUMP_BONUS) = was


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


def _reserved(plan):
    """Fertilizer units the day held back from the lot greedy.  The shed holds
    20 on every board here and the reservation is `n_fert_eff`, so this is the
    count of applications the day admitted -- observable from the market rows
    alone, which is what `S/drainpin/on2b.py` sees."""
    return 20 - _sold(plan, spec.I_FERT)


def _sold(plan, product):
    """Units of one product the day's market rows SELL (`plan` is
    `(unit_op, unit_a, unit_q, mkt_op, mkt_arg, mkt_qty)`)."""
    op, arg, qty = plan[3], plan[4], plan[5]
    return int(np.asarray(qty)[(np.asarray(op) == O.MO_SELL)
                               & (np.asarray(arg) == product)].sum())


# =========================================================================
# OFF is master, byte for byte
# =========================================================================

def test_off_is_the_default():
    assert P.FERT_DUMP_ON is False


def test_off_plan_is_byte_identical_to_master():
    """The whole-plan digest of five boards against a pristine master tree."""
    assert _digests() == _tree_digests()


def test_a_zero_bonus_is_the_off_plan_on_every_board():
    """`FERT_DUMP_BONUS = 0` adds a literal zero to the bar, so ON has to
    re-evaluate to OFF -- the property that makes the constant a size and not a
    second mechanism."""
    off = _digests()
    with _knob(bonus=0):
        assert {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS} == off


def test_before_the_start_day_on_is_the_off_plan():
    """The gate is a day predicate, so every day before `FERT_DUMP_DAY` is
    untouched however large the bonus."""
    for d in (0, 10, 19):
        v = _view(day=d, n_to=6, n_wh=4, age=6, shed_fert=20)
        off = _digest(_plan(v))
        with _knob(day=20, bonus=999):
            assert _digest(_plan(v)) == off, d


# =========================================================================
# THE BAR
# =========================================================================

def test_from_the_start_day_the_bar_rises_by_exactly_the_bonus():
    """An application whose value sits between the quote and the quote plus the
    bonus is dropped; one above the raised bar is kept.  Fertilizer's quote is
    100 at the opening inventory and a two-unit tomato application is worth 120,
    so a bonus of 19 keeps it and a bonus of 21 does not."""
    v = _view(day=22, n_to=6, n_wh=4, age=6, shed_fert=20)
    base = _reserved(_plan(v))
    assert base == 6
    with _knob(day=20, bonus=19):
        assert _reserved(_plan(v)) == 6
    with _knob(day=20, bonus=21):
        assert _reserved(_plan(v)) == 0


def test_the_dropped_application_is_sold_instead():
    """The units the bar refuses need no plumbing of their own: `n_fert_want`
    falls, so `fert_reserved` falls, so `avail[I_FERT]` rises and the lot greedy
    puts them on the day's rows -- and no other product moves."""
    v = _view(day=22, n_to=6, n_wh=4, age=6, shed_fert=20)
    off = _plan(v)
    with _knob(day=20, bonus=999):
        on = _plan(v)
    assert _reserved(on) < _reserved(off)
    assert _sold(on, spec.I_FERT) > _sold(off, spec.I_FERT)
    for p in range(spec.N_PRODUCTS):
        if p != spec.I_FERT:
            assert _sold(off, p) == _sold(on, p), spec.PRODUCTS[p]


def test_a_board_with_no_application_to_refuse_is_the_off_plan():
    """Nothing to gate, nothing moved -- the switch cannot touch a day whose
    tiles are all past their last standing day."""
    v = _view(day=22, n_to=0, n_wh=8, age=4, shed_fert=20)
    assert _reserved(_plan(v)) == 0
    off = _digest(_plan(v))
    with _knob(day=20, bonus=999):
        assert _digest(_plan(v)) == off


def test_the_bar_is_the_quote_PLUS_the_bonus_to_the_coin():
    """The bar is an ADDITION and not a multiple -- the defect H3 records for
    `FERT_VOLUME`, whose `NUM/DEN` times a collapsing quote stops binding after
    about day 16.  Swept to the coin: the six 120-coin applications survive
    every bonus up to 19 and none survives 20, because `fert_cand` asks for
    `fert_val > quote + bonus` and `120 > 100 + 20` is false."""
    v = _view(day=22, n_to=6, n_wh=4, age=6, shed_fert=20)
    got = []
    for bonus in range(0, 25):
        with _knob(day=20, bonus=bonus):
            got.append(_reserved(_plan(v)))
    assert got == [6] * 20 + [0] * 5, got


def test_a_multiple_of_the_same_quote_is_a_different_bar():
    """The two switches are independent: `FERT_VOLUME` at 2/1 refuses the same
    six applications by doubling the quote to 200, not by adding denial, and it
    does so on every day rather than from `FERT_DUMP_DAY`."""
    early = _view(day=10, n_to=6, n_wh=4, age=6, shed_fert=20)
    with _knob(day=20, bonus=999):
        assert _reserved(_plan(early)) == 6           # the day gate holds
    was = (P.FERT_VOLUME_ON, P.FERT_VOLUME_NUM, P.FERT_VOLUME_DEN)
    P.FERT_VOLUME_ON, P.FERT_VOLUME_NUM, P.FERT_VOLUME_DEN = True, 2, 1
    try:
        assert _reserved(_plan(early)) == 0           # no day gate at all
    finally:
        (P.FERT_VOLUME_ON, P.FERT_VOLUME_NUM, P.FERT_VOLUME_DEN) = was


def test_the_whole_switch_traces_under_jit_and_agrees_with_numpy():
    import jax
    import jax.numpy as jnp
    v = _view(day=22, n_to=6, n_wh=4, n_an=3, age=6, shed_fert=20)
    with _knob(day=20, bonus=21):
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


def test_the_jit_gate_is_a_real_day_predicate_not_a_python_branch():
    """Under `jit` the day is a tracer, so the gate must be `where` and not an
    `if` -- one traced program must serve both sides of `FERT_DUMP_DAY`."""
    import jax
    import jax.numpy as jnp
    m = _sell_macro()
    jm = type(m)(**{k: (jnp.asarray(x) if isinstance(x, np.ndarray) else x)
                    for k, x in m._asdict().items()})
    f = jax.jit(lambda w: P.build_day(jnp, w, jm))
    with _knob(day=20, bonus=999):
        for d in (10, 22):
            v = _view(day=d, n_to=6, n_wh=4, age=6, shed_fert=20)
            jv = P.DayView(**{k: jnp.asarray(x) for k, x in v._asdict().items()})
            for a, b in zip(_plan(v), f(jv)):
                assert (np.asarray(a) == np.asarray(b)).all(), d


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _digests().items():
        print(_n, _d)
