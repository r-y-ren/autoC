"""`plan.ROUTE_EFF_ON`: a floor under the day's `compact` gene.

`docs/strategy/2026-09-16-routeeff.md`.  ROUTEEFF's per-hand-day STEP ledger
(`S/routeeff/probe.py`) split every unit step into MOVE / PASS / PROD -- market
orders are a separate action channel (`kaggriculture.py:555-612`) and cost no
unit step, so per unit-day `prod = present - move - pass` exactly -- and found
the largest term of the d20-29 ops-per-hand-day gap to be `mid_move`, the walk
between a unit-day's first and last productive op: 8.93 steps to the engine
class's 8.19 (t 6.05) over the SAME number of distinct tiles.

`_dev_key` names the cause: `compact` is `relu(tanh(dev[0]))`, one-sided and 0
at zero theta, and at `compact == 0` `_rank_near` is `_rank` bit for bit, so
the day develops in plain serpentine order and scatters the season's labour.
This switch puts a floor under that gene.  It is a constant, not a mechanism,
so OFF must be the shipped planner byte for byte -- which is what the identity
pin below asserts against a pristine `git archive` of the branch base.
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

#: The branch base: the shipped FT2 planner (`master` f32e919), which has no
#: `ROUTE_EFF_ON` at all.  A SHA and not `HEAD`, so the pin keeps its meaning
#: once this branch is committed.
BASE = "f32e919290b424dea36ede3b7732b329da62987f"


def _view(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
          t_water=0, yld=6, nquad=1, shops=0, mkt_inv=spec.MARKET_I0, seed=0):
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
        seeds=np.full(spec.N_CROPS, int(seed), np.int32), money=np.int32(money),
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
    ("hot", dict(day=10, n_wh=8, shed_wh=50, shed_to=45)),
    ("cool", dict(day=10, n_wh=8, shed_wh=0, shed_to=0)),
    ("wet", dict(day=10, n_wh=8, shed_wh=50, shed_to=45, t_water=1)),
    ("bare", dict(day=12, n_wh=0, shed_wh=60, shed_to=38)),
    ("wide", dict(day=20, n_wh=8, shed_wh=30, shed_to=10, nquad=3)),
    # `slot_rank` only decides anything on a day that DEVELOPS free tiles, so
    # the switch is inert on a seedless board -- two of the pins carry seed.
    ("develop", dict(day=8, n_wh=4, seed=12, nquad=1)),
    ("develop_wide", dict(day=18, n_wh=20, seed=12, nquad=3)),
)


def _digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _own_digests(on=None):
    if on is None:
        return _digests()
    was = P.ROUTE_EFF_ON
    P.ROUTE_EFF_ON = on
    try:
        return _digests()
    finally:
        P.ROUTE_EFF_ON = was


def _tree_digests(ref=BASE):
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
# the identity pin
# =========================================================================

def test_the_switch_ships_off():
    assert P.ROUTE_EFF_ON is False
    assert P.ROUTE_EFF_COMPACT == P.DIST_MAX


def test_the_base_tree_has_no_such_switch():
    """The pin's other end, named: `BASE` is the shipped FT2 planner."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ROUTE_EFF_ON" not in src
    assert "\nFERT_TIMING_ON = True\n" in src


def test_off_plan_is_byte_identical_to_the_shipped_planner():
    """THE IDENTITY PIN: OFF is the FT2 program, whole-plan sha256, against a
    pristine `git archive BASE src` tree."""
    assert _own_digests() == _tree_digests()
    assert _own_digests(on=False) == _tree_digests()


# =========================================================================
# what ON does
# =========================================================================

def test_on_changes_which_free_tiles_the_day_develops():
    """What the switch actually moves: `slot_rank`, the order free tiles are
    built and planted in.  At `compact == 0` it is the plain serpentine rank;
    at the floor it is `DIST_SHED`, so the tiles nearest a shed access come
    first.  (The whole-plan pin boards below cannot show this -- the shared
    test macro wants no plantings -- so the rank is read directly.)"""
    free = np.zeros(spec.N_TILES, bool)
    free[np.asarray(P.SERP_INV)[:40]] = True
    off = np.asarray(P._rank_near(np, free, P._dev_key(np, np.int32(0))))
    on = np.asarray(P._rank_near(
        np, free, P._dev_key(np, np.maximum(np.int32(0),
                                            np.int32(P.ROUTE_EFF_COMPACT)))))
    assert not (off == on).all()
    # the first tile the floor develops is a nearest-the-shed one, and the
    # serpentine's first tile need not be
    d = np.asarray(P.DIST_SHED)
    assert d[free & (on == 0)].min() == d[free].min()
    assert (np.sort(on[free]) == np.arange(int(free.sum()))).all()


def test_the_floor_only_ever_raises_the_gene():
    for gene in (0, 1, P.ROUTE_EFF_COMPACT, P.DIST_MAX):
        eff = int(np.maximum(np.int32(gene), np.int32(P.ROUTE_EFF_COMPACT)))
        assert eff >= gene and eff >= P.ROUTE_EFF_COMPACT


def test_a_zero_floor_is_the_shipped_plan(monkeypatch):
    """`ROUTE_EFF_COMPACT == 0` is the shipped plan even with the switch ON."""
    monkeypatch.setattr(P, "ROUTE_EFF_COMPACT", 0)
    assert _own_digests(on=True) == _tree_digests()


def test_dev_key_at_the_floor_is_dist_shed():
    """What the floor buys: the development rank becomes `DIST_SHED` itself,
    so the tiles nearest a shed access are built and planted first."""
    key = np.asarray(P._dev_key(np, np.int32(P.DIST_MAX)))
    assert (key == P.DIST_SHED).all()
    assert (np.asarray(P._dev_key(np, np.int32(0))) == 0).all()


def test_the_switch_traces_under_jit():
    """`xp.maximum` of a traced gene against a Python int: caught here rather
    than ten minutes into a leg."""
    import jax
    import jax.numpy as jnp
    f = jax.jit(lambda c: P._dev_key(jnp, jnp.maximum(c, jnp.int32(P.ROUTE_EFF_COMPACT))))
    assert (np.asarray(f(jnp.int32(0))) == P.DIST_SHED).all()


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
