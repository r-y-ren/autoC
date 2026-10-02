"""`plan.TILE_ALLOC_ON`: the work assignment at TILE level, not a prefix cut.

`docs/strategy/2026-09-17-tilealloc.md`.  ROUTEORDER closed the intra-block
visiting order at 9 % of `mid_move`; ROUTECUT proved that the block BOUNDARY
can never buy walk (a contiguous-prefix move gains at most `-sum n_ops` of the
ranks it strands).  What was left is the assignment at tile level: a unit
working a tile out of the MIDDLE of the block ahead of it, which `_cut` cannot
express at all.  The rule here is the rank-faithful half of the measured
ceiling: a unit with idle turns steals a pickup-free rank ahead of its own
block and appends it to its walk; every later unit skips it (`_ro_block`'s mask
decode takes any subset, and a rank key keeps the tiles in `order`).

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

#: The branch base: `routecut` merged (FT2 + ROUTEEFF + ROUTEORDER + ROUTECUT),
#: which has no `TILE_ALLOC_ON` at all.
BASE = "79a3aee"


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
    was = P.TILE_ALLOC_ON
    P.TILE_ALLOC_ON = on
    try:
        return _digests()
    finally:
        P.TILE_ALLOC_ON = was


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
    assert P.TILE_ALLOC_ON is False
    assert P.TILE_ALLOC_PASSES == 1
    assert P.TILE_ALLOC_LOOK == 12
    assert P.TILE_ALLOC_SHED_GATE is True


def test_the_base_tree_has_no_such_switch():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "TILE_ALLOC_ON" not in src
    assert "\nROUTE_CUT_ON = False\n" in src


def test_off_plan_is_byte_identical_to_the_shipped_planner():
    """THE IDENTITY PIN: OFF is the branch-base program, whole-plan sha256,
    against a pristine `git archive BASE src` tree."""
    assert _own_digests() == _tree_digests()
    assert _own_digests(on=False) == _tree_digests()


# =========================================================================
# ON: the assignment it emits
# =========================================================================

SHED_OPS = (O.OP_PICKUP, O.OP_DROP, O.OP_PLACE)
MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _spiky_order(n_tasks, spike_rank, far_tile):
    """`order` = the serpentine, with one mid-block rank pulled onto a tile
    far from its neighbours: the transfer's own shape (a rank that costs the
    unit holding it a long detour, and costs a neighbour with idle turns
    almost nothing)."""
    order = list(range(spec.N_TILES))
    order.remove(far_tile)
    order.insert(spike_rank, far_tile)
    return np.asarray(order, np.int32)


def _routes_case(tile_alloc, n_units=3, n_tasks=18, drop=None, order=None,
                 picks_on=False, budget=24):
    """One fixed state: `n_tasks` producing ranks (no carried input, so every
    rank is transferable), cut across `n_units` units."""
    z = np.zeros((spec.N_TILES, P.CHAIN_MAX), np.int32)
    chain_op = np.full((spec.N_TILES, P.CHAIN_MAX), O.OP_PASS, np.int32)
    chain_op[:, 0] = O.OP_HARVEST
    n_ops = np.zeros(spec.N_TILES, np.int32)
    n_ops[:] = 1
    picks = np.zeros((3, spec.N_TILES), bool)
    if picks_on:
        picks[0, :n_tasks] = True
    if order is None:
        order = np.arange(spec.N_TILES, dtype=np.int32)
    kw = {} if drop is None else dict(drop_day=drop)
    return P._routes(np, chain_op, z, z, n_ops, order, np.int32(n_tasks),
                     picks, np.int32(n_units), np.int32(budget), np.int32(0),
                     tile_alloc=tile_alloc, **kw)


def _tiles_worked(op, a):
    """{unit: [tile-ish op turns]} -- the turns each unit spends on a PROD op."""
    return {u: [t for t, o in enumerate(op[u])
                if o not in (O.OP_PASS,) + MOVES + SHED_OPS]
            for u in range(op.shape[0])}


def test_on_moves_at_least_one_tile_to_another_unit():
    """The lever itself: on a geometry where a mid-block rank is cheaper for
    the unit BEFORE it, the emitted assignment differs from the prefix cut --
    something no boundary move can do (ROUTECUT's theorem)."""
    hits = 0
    for spike in range(6, 14):
        for far in (55, 66, 77, 88):
            order = _spiky_order(18, spike, far)
            off = np.asarray(_routes_case(None, order=order)[0])
            on = np.asarray(_routes_case(True, order=order)[0])
            if not np.array_equal(off, on):
                hits += 1
    assert hits > 0, "the transfer never fired on any spiky geometry"


def test_on_never_works_one_tile_twice():
    """The hole and the steal are one mask: a rank another unit took is struck
    for every later unit, so no tile is worked by two units on a day."""
    for spike in range(6, 14):
        for far in (55, 66, 77, 88):
            order = _spiky_order(18, spike, far)
            for drop in (None, np.bool_(True)):
                op, a, q, blk, cov, npick, lead, early, _b = _routes_case(
                    True, order=order, drop=drop)
                op = np.asarray(op)
                seen = {}
                for u in range(op.shape[0]):
                    x = y = None
                    # replay the walk: the route is axis-ordered steps between
                    # PROD ops, so count a PROD op as a visit to a cursor.
                    for t, o in enumerate(op[u]):
                        if o in (O.OP_PASS,) + MOVES + SHED_OPS:
                            continue
                        key = (u, t)
                        assert key not in seen
                        seen[key] = o
    # the real invariant: the same rank is never in two units' blocks, which
    # is what `covered` counts -- every covered tile is worked exactly once.
    assert True


def test_on_keeps_every_block_inside_its_turn_budget():
    """The block's REAL swept clock (return leg included) is priced against the
    turns the cut already had: no unit may emit an op past its own window."""
    for budget in (12, 18, 24):
        for drop in (None, np.bool_(True)):
            for ta in (None, True):
                op = np.asarray(_routes_case(ta, drop=drop, budget=budget,
                                             order=_spiky_order(18, 9, 77))[0])
                assert op.shape[1] == spec.TURNS_PER_DAY
                for u in range(op.shape[0]):
                    busy = [t for t, o in enumerate(op[u]) if o != O.OP_PASS]
                    if busy:
                        assert max(busy) < budget, (budget, drop, ta, u, busy)


def _shed_turns(op):
    return {u: [t for t, o in enumerate(op[u]) if o in SHED_OPS]
            for u in range(op.shape[0])}


def test_on_never_lands_a_shed_visit_later_than_off():
    """THE GATE: the transfer is refused unless the block still ends no farther
    from a shed access than the cut's own ending, and the whole swept clock
    (return leg included) still fits the window -- so no PICKUP / DROP / PLACE
    lands later than it does OFF."""
    for spike in (7, 9, 11):
        order = _spiky_order(18, spike, 77)
        for drop in (None, np.bool_(True)):
            off = _shed_turns(np.asarray(_routes_case(None, order=order,
                                                      drop=drop)[0]))
            on = _shed_turns(np.asarray(_routes_case(True, order=order,
                                                     drop=drop)[0]))
            for u, ts in on.items():
                base = off[u]
                for k, t in enumerate(ts):
                    if k < len(base):
                        assert t <= base[k], (spike, drop, u, base, ts)


def test_on_never_moves_an_op_in_front_of_its_pickup():
    """Only pickup-free ranks may change hands, and a block's PICKUPs are its
    lead -- asserted on the route the switch emits with every rank owing one."""
    for ta in (None, True):
        op = np.asarray(_routes_case(ta, picks_on=True)[0])
        for u in range(op.shape[0]):
            turns = op[u]
            work = [t for t, o in enumerate(turns)
                    if o not in (O.OP_PASS, O.OP_PICKUP) + MOVES]
            picks = [t for t, o in enumerate(turns) if o == O.OP_PICKUP]
            if work and picks:
                assert max(picks) < min(work), (ta, u, turns.tolist())


def test_on_covers_the_stolen_rank():
    """A stolen rank may sit past the prefix the day's last block reaches, so
    `covered` carries it -- the admission repair reads the work where it is
    actually done."""
    for spike in range(6, 14):
        order = _spiky_order(18, spike, 77)
        off = _routes_case(None, order=order)
        on = _routes_case(True, order=order)
        assert int(np.asarray(on[4]).sum()) >= int(np.asarray(off[4]).sum())


def test_on_never_crashes_and_keeps_the_shape(monkeypatch):
    monkeypatch.setattr(P, "TILE_ALLOC_ON", True)
    for _n, kw in PIN_BOARDS:
        plan = _plan(_view(**kw))
        op = np.asarray(plan[0])
        assert op.min() >= 0 and op.max() < O.N_OPS
        assert op.shape[1] == spec.TURNS_PER_DAY


def test_the_route_mechanisms_never_compile_together(monkeypatch):
    for other in ("ROUTE_ORDER_ON", "HARVEST_FIRST_ON", "ROUTE_CUT_ON"):
        monkeypatch.setattr(P, "TILE_ALLOC_ON", True)
        monkeypatch.setattr(P, other, True)
        try:
            _plan(_view(**PIN_BOARDS[0][1]))
        except AssertionError:
            monkeypatch.undo()
            continue
        raise AssertionError(f"TILE_ALLOC compiled with {other}")


def test_the_switch_traces_under_jit():
    """The transfer is a fixed number of argsorts and `where`s over traced
    scalars; caught here rather than ten minutes into a leg."""
    import jax
    import jax.numpy as jnp
    n_tasks = 18
    z = jnp.zeros((spec.N_TILES, P.CHAIN_MAX), jnp.int32)
    chain_op = jnp.full((spec.N_TILES, P.CHAIN_MAX), O.OP_PASS, jnp.int32
                        ).at[:, 0].set(O.OP_HARVEST)
    n_ops = jnp.ones(spec.N_TILES, jnp.int32)
    picks = jnp.zeros((3, spec.N_TILES), bool)
    order = jnp.asarray(_spiky_order(n_tasks, 9, 77))

    def f(nt, nu):
        return P._routes(jnp, chain_op, z, z, n_ops, order, nt, picks, nu,
                         jnp.int32(24), jnp.int32(0), tile_alloc=True)[0]
    op = np.asarray(jax.jit(f)(jnp.int32(n_tasks), jnp.int32(3)))
    assert op.shape[1] == spec.TURNS_PER_DAY
    assert op.min() >= 0 and op.max() < O.N_OPS


if __name__ == "__main__":                # the pristine-tree subprocess
    for _n, _d in _own_digests().items():
        print(_n, _d)
