"""`plan.ROUTE_ORDER_ON`: sweep a block's own tiles, not the day's rank order.

`docs/strategy/2026-09-16-routeorder.md`.  ROUTEEFF closed the development-order
lever and named what was left of `mid_move` -- the walk BETWEEN a unit-day's ops,
the largest term of the d20-29 volume gap -- as the intra-block VISITING order.
ROUTEORDER measured it directly (`S/routeorder/probe.py`, the ordered op path of
every unit of every day on 22 ENG22 boards): 10.18 moves a unit-day where the
walk-minimal order of the SAME tiles, every shed interaction pinned where it is,
spends 8.79.  A block-local boustrophedon recovers 90 % of that gap and is a
static per-rank sort key, which is what the traced route compiler can express.

OFF must be the branch base byte for byte -- the identity pin below asserts it
against a pristine `git archive` of that commit -- and ON must never move an op
in front of the PICKUP that loads it, which the ON test asserts directly off
`_routes` on a fixed state.
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

from test_budget_order import _macro

if "--digests" in sys.argv:                 # the pristine-tree subprocess
    import kagg3
    _want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    assert os.path.abspath(kagg3.__file__).startswith(_want + os.sep), \
        f"the pin loaded {kagg3.__file__}, not the tree under {_want}"

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)

#: The branch base: master `bb695a2` (the shipped FT2 planner plus ROUTEEFF),
#: which has no `ROUTE_ORDER_ON` at all.  A SHA and not `HEAD`, so the pin keeps
#: its meaning once this branch is committed.
BASE = "bb695a23fea47db2c0978749ca9785806970b450"


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
    ("develop", dict(day=8, n_wh=4, seed=12, nquad=1)),
    ("develop_wide", dict(day=18, n_wh=20, seed=12, nquad=3)),
)


def _digests():
    return {n: _digest(_plan(_view(**kw))) for n, kw in PIN_BOARDS}


def _own_digests(on=None):
    if on is None:
        return _digests()
    was = P.ROUTE_ORDER_ON
    P.ROUTE_ORDER_ON = on
    try:
        return _digests()
    finally:
        P.ROUTE_ORDER_ON = was


def _tree_digests(ref=BASE):
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
    assert P.ROUTE_ORDER_ON is False
    assert P.ROUTE_ORDER_SHED_GATE is True


def test_the_base_tree_has_no_such_switch():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ROUTE_ORDER_ON" not in src
    assert "\nROUTE_EFF_ON = False\n" in src


def test_off_plan_is_byte_identical_to_the_shipped_planner():
    """THE IDENTITY PIN: OFF is the branch-base program, whole-plan sha256,
    against a pristine `git archive BASE src` tree."""
    assert _own_digests() == _tree_digests()
    assert _own_digests(on=False) == _tree_digests()


# =========================================================================
# ON: the reorder, and the constraint it must not break
# =========================================================================

def _routes_case(route_order):
    """One fixed state: eight tiles that all consume a PICKUP kind, laid out so
    the day's rank order and every boustrophedon sweep of them differ, one unit
    with the whole day."""
    z = np.zeros((spec.N_TILES, P.CHAIN_MAX), np.int32)
    chain_op = np.full((spec.N_TILES, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain_op[:8, 0] = O.OP_FEED           # every rank consumes the feed pickup
    n_ops = np.zeros(spec.N_TILES, np.int32)
    n_ops[:8] = 1
    picks = np.zeros((3, spec.N_TILES), bool)
    picks[0, :8] = True
    order = np.arange(spec.N_TILES, dtype=np.int32)
    return P._routes(np, chain_op, z, z, n_ops, order, np.int32(8), picks,
                     np.int32(1), np.int32(24), np.int32(0),
                     route_order=route_order)


def test_on_never_moves_an_op_in_front_of_its_pickup():
    """The block's PICKUPs are its *lead*, charged before its first rank, so no
    permutation of the ranks can move an op in front of the pickup that loads
    it -- asserted on the route the switch actually emits."""
    for ro in (None, True):
        op = np.asarray(_routes_case(ro)[0])
        for u in range(op.shape[0]):
            turns = op[u]
            work = [t for t, o in enumerate(turns)
                    if o not in (O.OP_PASS, O.OP_PICKUP, O.OP_NORTH, O.OP_SOUTH,
                                 O.OP_EAST, O.OP_WEST)]
            picks = [t for t, o in enumerate(turns) if o == O.OP_PICKUP]
            if work and picks:
                assert max(picks) < min(work), (ro, u, turns.tolist())


def test_on_works_the_same_tiles_and_no_more_turns():
    """The sweep is a permutation of a block, never a bigger day: every unit's
    route is still `TURNS_PER_DAY` wide and the day still reaches at least the
    tiles it reached off the rank order."""
    off = _routes_case(None)
    on = _routes_case(True)
    assert np.asarray(on[0]).shape == np.asarray(off[0]).shape
    assert np.asarray(on[0]).shape[1] == spec.TURNS_PER_DAY
    assert int(np.asarray(on[4]).sum()) >= int(np.asarray(off[4]).sum())


def test_on_never_crashes_and_keeps_the_shape(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_ORDER_ON", True)
    for _n, kw in PIN_BOARDS:
        plan = _plan(_view(**kw))
        op = np.asarray(plan[0])
        assert op.min() >= 0 and op.max() < O.N_OPS
        assert op.shape[1] == spec.TURNS_PER_DAY


def test_the_two_reorders_never_compile_together(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_ORDER_ON", True)
    monkeypatch.setattr(P, "HARVEST_FIRST_ON", True)
    try:
        _plan(_view(**PIN_BOARDS[0][1]))
    except AssertionError:
        return
    raise AssertionError("both reorders compiled at once")


def test_the_switch_traces_under_jit():
    """`argsort` and the four keys under `jax.jit`: caught here rather than ten
    minutes into a leg.  The helper is the whole of the new traced code."""
    import jax
    import jax.numpy as jnp
    n = spec.N_TILES
    idx = jnp.arange(n, dtype=jnp.int32)
    tx = jnp.asarray(P.SERP_X)
    ty = jnp.asarray(P.SERP_Y)
    tn = jnp.ones(n, jnp.int32)
    key = (ty * spec.BOARD + jnp.where(ty % 2 == 0, tx, spec.BOARD - 1 - tx)
           ).astype(jnp.int32)

    def f(k):
        inb = idx < k
        return P._ro_block(jnp, jnp.int32, idx, key, inb,
                           jnp.sum(inb.astype(jnp.int32)), tx, ty, tn,
                           jnp.int32(0), jnp.int32(0))
    rank_at, move2, seg2, cum2, total2, e_final = jax.jit(f)(jnp.int32(6))
    rank_at = np.asarray(rank_at)
    # a permutation, the block first, and its walk no worse than the rank order
    assert sorted(rank_at.tolist()) == list(range(n))
    assert sorted(rank_at[:6].tolist()) == list(range(6))
    assert int(np.asarray(total2)) <= int(
        np.abs(np.diff(np.asarray(P.SERP_X)[:6])).sum()
        + np.abs(np.diff(np.asarray(P.SERP_Y)[:6])).sum()) + 6 + int(
        np.asarray(P.SERP_X)[0] + np.asarray(P.SERP_Y)[0])


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
