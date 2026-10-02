"""`plan.ROUTE_CUT_ON`: the block ASSIGNMENT, not the block's visiting order.

`docs/strategy/2026-09-16-routecut.md`.  ROUTEORDER closed the intra-block
sweep at 9 % of `mid_move` and named what was left: `_cut` takes the LARGEST
rank whose block fits the budget, so the boundary between two adjacent units
falls wherever the turn budget runs out.  The crew's whole walk is

    sum_{j<=E} move[j] + sum_u base_move_u - sum_{u>=1} move[s_u]

so for a fixed coverage the boundary owns exactly `base_move_u - move[s_u]`.
`ROUTE_CUT_ON` pulls a block's end back by at most `ROUTE_CUT_LOOK` ranks when
that hands the next unit a strictly cheaper entry, under the strongest form of
the shed gate: the new end is no farther from a shed access and is earlier on
the block's own clock, so every shed interaction lands on the same turn or
sooner -- the invariant this file asserts on an emitted route.

OFF must be the branch base byte for byte (the identity pin below, whole-plan
sha256 against a pristine `git archive` of that commit).
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

#: The branch base: `routeorder` merged (the shipped FT2 planner plus ROUTEEFF
#: plus `ROUTE_ORDER_ON`), which has no `ROUTE_CUT_ON` at all.  A SHA and not
#: `HEAD`, so the pin keeps its meaning once this branch is committed.
BASE = "d131961"

_view = None        # bound below


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


def _mkview(day=10, money=20_000, n_wh=8, age=4, shed_wh=0, shed_to=0,
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


_view = _mkview

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
    was = P.ROUTE_CUT_ON
    P.ROUTE_CUT_ON = on
    try:
        return _digests()
    finally:
        P.ROUTE_CUT_ON = was


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
    assert P.ROUTE_CUT_ON is False
    assert P.ROUTE_CUT_LOOK == 3
    assert P.ROUTE_CUT_SHED_GATE is True


def test_the_base_tree_has_no_such_switch():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ROUTE_CUT_ON" not in src
    assert "\nROUTE_ORDER_ON = False\n" in src


def test_off_plan_is_byte_identical_to_the_shipped_planner():
    """THE IDENTITY PIN: OFF is the branch-base program, whole-plan sha256,
    against a pristine `git archive BASE src` tree."""
    assert _own_digests() == _tree_digests()
    assert _own_digests(on=False) == _tree_digests()


def test_on_is_inert_on_the_pin_boards():
    """ON is OFF: the priced rule never fires.  Not a defect -- the theorem
    below -- and the measured fact on 44 ENG22 games (`d/board +0, sd 0`) at
    look-back 3 and 12 with the shed gate, and 8 without it."""
    assert _own_digests(on=True) == _own_digests(on=False)


def test_the_boundary_term_can_never_pay():
    """THE THEOREM the leg measured.  Pull a block's end back from `e` to `c`:
    the next unit enters at `c + 1` instead of `e + 1`, so the walk changes by

        base(e+1) - base(c+1) - move[e+1] + move[c+1]

    and this block strands `cu[e] - cu[c] = sum_{c<j<=e} (move[j] + n_ops[j])`
    turns it had nothing else to spend.  Along the path c+1 -> ... -> e -> e+1
    the triangle inequality gives
    `base(e+1) <= base(c+1) + sum_{c+1<j<=e+1} move[j]`, so

        gain <= -sum_{c<j<=e} n_ops[j]  <  0

    for every boundary, every geometry, every look-back: a contiguous-prefix
    boundary can never buy walk, because the leg the next unit walks in from
    its spawn is already bounded by the hops it would otherwise have walked.
    Checked here on random geometry, which is what the engine leg confirmed."""
    rng = np.random.default_rng(7065)
    for _ in range(200):
        n = int(rng.integers(6, 20))
        tx = rng.integers(0, spec.BOARD, n)
        ty = rng.integers(0, spec.BOARD, n)
        tn = rng.integers(1, 3, n)
        spx, spy = int(rng.integers(0, spec.BOARD)), int(rng.integers(0, spec.BOARD))
        move = np.concatenate([[0], np.abs(np.diff(tx)) + np.abs(np.diff(ty))])
        base = np.abs(tx - spx) + np.abs(ty - spy)
        cost = base - move
        cum = np.cumsum(move + tn)
        for e in range(1, n - 1):
            for c in range(max(0, e - 12), e):
                gain = cost[e + 1] - cost[c + 1] - (cum[e] - cum[c])
                assert gain <= -int(tn[c + 1:e + 1].sum()), (e, c, gain)


# =========================================================================
# ON: the route it emits
# =========================================================================

SHED_OPS = (O.OP_PICKUP, O.OP_DROP, O.OP_PLACE)
MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _routes_case(route_cut, n_units=3, n_tasks=24, drop=None):
    """One fixed state: `n_tasks` ranks that all consume a PICKUP kind, cut
    across `n_units` units, so every block has a boundary and a lead."""
    z = np.zeros((spec.N_TILES, P.CHAIN_MAX), np.int32)
    chain_op = np.full((spec.N_TILES, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain_op[:n_tasks, 0] = O.OP_FEED     # every rank consumes the feed pickup
    n_ops = np.zeros(spec.N_TILES, np.int32)
    n_ops[:n_tasks] = 1
    picks = np.zeros((3, spec.N_TILES), bool)
    picks[0, :n_tasks] = True
    order = np.arange(spec.N_TILES, dtype=np.int32)
    kw = {} if drop is None else dict(drop_day=drop)
    return P._routes(np, chain_op, z, z, n_ops, order, np.int32(n_tasks),
                     picks, np.int32(n_units), np.int32(24), np.int32(0),
                     route_cut=route_cut, **kw)


def test_on_never_moves_an_op_in_front_of_its_pickup():
    """The block's PICKUPs are its *lead*, charged before its first rank, so no
    recut can move an op in front of the pickup that loads it -- asserted on
    the route the switch actually emits."""
    for rc in (None, True):
        op = np.asarray(_routes_case(rc)[0])
        for u in range(op.shape[0]):
            turns = op[u]
            work = [t for t, o in enumerate(turns)
                    if o not in (O.OP_PASS, O.OP_PICKUP) + MOVES]
            picks = [t for t, o in enumerate(turns) if o == O.OP_PICKUP]
            if work and picks:
                assert max(picks) < min(work), (rc, u, turns.tolist())


def _shed_turns(op):
    """{unit: [turns of its shed interactions]}"""
    return {u: [t for t, o in enumerate(op[u]) if o in SHED_OPS]
            for u in range(op.shape[0])}


def test_on_never_lands_a_shed_visit_later_than_off():
    """THE GATE, on an emitted route: the recut only ever ends a block earlier
    on its own clock and no farther from a shed access, so every PICKUP / DROP
    / PLACE lands on the turn it landed on or sooner -- the one direction that
    cannot be wrong (`MIDDAY_PLACE` / `BANK_BEFORE_LOT` price on it)."""
    for drop in (None, np.bool_(True)):
        off = _shed_turns(np.asarray(_routes_case(None, drop=drop)[0]))
        on = _shed_turns(np.asarray(_routes_case(True, drop=drop)[0]))
        for u, ts in on.items():
            base = off[u]
            for k, t in enumerate(ts):
                if k < len(base):
                    assert t <= base[k], (drop, u, base, ts)


def test_on_keeps_the_day_covered_and_the_shape():
    """The ranks a block gives up are the NEXT unit's first ranks (`start =
    end + 1`), so the day still reaches what it reached; and the route is
    still `TURNS_PER_DAY` wide."""
    off = _routes_case(None)
    on = _routes_case(True)
    assert np.asarray(on[0]).shape == np.asarray(off[0]).shape
    assert np.asarray(on[0]).shape[1] == spec.TURNS_PER_DAY
    assert int(np.asarray(on[4]).sum()) >= int(np.asarray(off[4]).sum()) - 1


def test_on_never_crashes_and_keeps_the_shape(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_CUT_ON", True)
    for _n, kw in PIN_BOARDS:
        plan = _plan(_view(**kw))
        op = np.asarray(plan[0])
        assert op.min() >= 0 and op.max() < O.N_OPS
        assert op.shape[1] == spec.TURNS_PER_DAY


def test_the_two_route_mechanisms_never_compile_together(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_CUT_ON", True)
    monkeypatch.setattr(P, "ROUTE_ORDER_ON", True)
    try:
        _plan(_view(**PIN_BOARDS[0][1]))
    except AssertionError:
        return
    raise AssertionError("both route mechanisms compiled at once")


def test_the_switch_traces_under_jit():
    """The recut is a fixed window of `where`s over traced scalars; caught here
    rather than ten minutes into a leg."""
    import jax
    import jax.numpy as jnp
    n_tasks = 24
    z = jnp.zeros((spec.N_TILES, P.CHAIN_MAX), jnp.int32)
    chain_op = jnp.full((spec.N_TILES, P.CHAIN_MAX), O.OP_PASS, jnp.int32
                        ).at[:n_tasks, 0].set(O.OP_FEED)
    n_ops = jnp.zeros(spec.N_TILES, jnp.int32).at[:n_tasks].set(1)
    picks = jnp.zeros((3, spec.N_TILES), bool).at[0, :n_tasks].set(True)
    order = jnp.arange(spec.N_TILES, dtype=jnp.int32)

    def f(nt, nu):
        return P._routes(jnp, chain_op, z, z, n_ops, order, nt, picks, nu,
                         jnp.int32(24), jnp.int32(0), route_cut=True)[0]
    op = np.asarray(jax.jit(f)(jnp.int32(n_tasks), jnp.int32(3)))
    assert op.shape[1] == spec.TURNS_PER_DAY
    assert op.min() >= 0 and op.max() < O.N_OPS


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
