"""`plan.ADMIT_SLACK_ON`: the admit stage's step budget against the real day.

`docs/strategy/2026-09-17-admitslack.md`.  ADMITSLACK's instrument
(`S/admitslack/probe.py`) hooks `_plan_and_stats` and reads the admission
stage's own numbers -- `n_tasks`, `cum_est`, `labour`, `n_admit` -- on the very
games ROUTEEFF's engine-side step ledger measures, so a day carries both its
ESTIMATED step bill and its REALISED one.  Measured on ENG22, d20-29: the
per-unit overhead (`max(_pickup_kinds, land_lead) + EST_LEAD` = 6.08) is
charged against a realised 3.20, and the day ends with 16.0 tail-idle steps on
the 50.9 % of days that DECLINED a ranked task on that budget.

ON hands `ADMIT_SLACK_TURNS` back to each unit.  It is a constant, not a
mechanism, so OFF must be the shipped planner byte for byte -- which is what
the identity pin below asserts against a pristine `git archive` of the branch
base.
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

#: The branch base: `master` 0e66a6e, the shipped FT2 planner plus EVESTOCK,
#: which has no `ADMIT_SLACK_ON` at all.  A SHA and not `HEAD`, so the pin
#: keeps its meaning once this branch is committed.
BASE = "0e66a6e"


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
    was = P.ADMIT_SLACK_ON
    P.ADMIT_SLACK_ON = on
    try:
        return _digests()
    finally:
        P.ADMIT_SLACK_ON = was


def _tree_digests(ref=BASE):
    """The same plans, built by a pristine `git archive <ref> src` tree in a
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
# the identity pin
# =========================================================================

def test_the_switch_ships_off():
    assert P.ADMIT_SLACK_ON is False
    assert P.ADMIT_SLACK_TURNS == 1


def test_the_base_tree_has_no_such_switch():
    """The pin's other end, named: `BASE` is the shipped FT2 + EVESTOCK tree."""
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {BASE}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    assert "ADMIT_SLACK" not in src
    assert "\nADMIT_ROUNDS = 3\n" in src


def test_off_plan_is_byte_identical_to_the_shipped_planner():
    """THE IDENTITY PIN: OFF is the FT2 program, whole-plan sha256, against a
    pristine `git archive BASE src` tree."""
    assert _own_digests() == _tree_digests()
    assert _own_digests(on=False) == _tree_digests()


def test_zero_turns_is_the_shipped_plan(monkeypatch):
    """`ADMIT_SLACK_TURNS == 0` is the shipped plan even with the switch ON."""
    monkeypatch.setattr(P, "ADMIT_SLACK_TURNS", 0)
    assert _own_digests(on=True) == _tree_digests()


# =========================================================================
# what ON does
# =========================================================================

def _n_admit(labour_extra, n_units=6, turn_budget=21, cum=None, n_tasks=40):
    """The admission count the day would take, as `plan.py:9327-9334` takes
    it: the longest prefix of `cum_est` inside the budget, capped at the task
    count."""
    cum = np.cumsum(np.full(spec.N_TILES, 4, np.int32), dtype=np.int32) \
        if cum is None else cum
    labour = n_units * (turn_budget - 6) + labour_extra
    return int(min(int(P._count_le(np, cum, np.int32(labour))), n_tasks))


def test_on_admits_more_on_a_budget_bound_day():
    """The mechanism, on a fixed budget-bound state: six units, a 21-turn
    budget, a 6-step per-unit overhead and 4-step tasks -- 22 admitted OFF,
    and the returned turn a unit admits the next ranked tasks instead of
    leaving them declined."""
    off = _n_admit(0)
    on = _n_admit(6 * P.ADMIT_SLACK_TURNS)
    assert off == 22 and on > off, (off, on)
    # and it is bounded by the task count, never past it
    assert _n_admit(6 * 99, n_tasks=30) == 30


def test_a_task_bound_day_cannot_move():
    """A day whose whole task set already fits admits the same set ON."""
    assert _n_admit(0, n_tasks=5) == _n_admit(6 * P.ADMIT_SLACK_TURNS, n_tasks=5) == 5


def test_on_admits_more_on_a_loaded_board_end_to_end():
    """End to end, through `build_day` itself: on a budget-bound board the
    first `_routes` round is handed a LARGER admitted set ON.  (The digest
    need not move: `ADMIT_ROUNDS` may drop the extra tile again -- which is
    the repairable error the switch is built on, and exactly what the ENG22
    leg prices.)"""
    view = _view(day=20, n_wh=100, nquad=4, money=400, age=6, yld=8)
    seen = []
    real = P._routes

    def spy(xp, *a, **kw):
        seen.append(int(a[5]))                     # the round's `n_admit`
        return real(xp, *a, **kw)

    P._routes = spy
    try:
        seen.clear(); P.ADMIT_SLACK_ON = False
        _plan(view); off = list(seen)
        seen.clear(); P.ADMIT_SLACK_ON = True
        _plan(view); on = list(seen)
    finally:
        P._routes = real
        P.ADMIT_SLACK_ON = False
    assert on[0] > off[0], (off, on)


def test_the_switch_traces_under_jit():
    """`labour + n_units * <int>` with a traced `n_units`: caught here rather
    than ten minutes into a leg."""
    jax = __import__("jax")
    jnp = __import__("jax.numpy", fromlist=["numpy"])
    was = P.ADMIT_SLACK_ON
    P.ADMIT_SLACK_ON = True
    try:
        v = _view(day=20, n_wh=8, shed_wh=30, shed_to=10, nquad=3)
        jv = P.DayView(**{k: (jnp.asarray(x) if isinstance(x, np.ndarray)
                             else jnp.asarray(x)) for k, x in v._asdict().items()})
        m = _macro()
        jm = type(m)(**{k: jnp.asarray(x) for k, x in m._asdict().items()})
        out = jax.jit(lambda vv, mm: P.build_day(jnp, vv, mm))(jv, jm)
        assert out is not None
    finally:
        P.ADMIT_SLACK_ON = was


if __name__ == "__main__":
    for n, d in _own_digests().items():
        print(n, d)
