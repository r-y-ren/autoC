"""`FORWARD_ADMIT_ON`: the hire scan prices the crew against the work coming.

Hire enumeration (`plan` 1.5) scores every candidate `h` against the task set
`_derive` emits *today*.  A field of one-time crops outside their bonus window
emits nothing -- `spec.CROP_WINDOW_START[I_MELON]` is 6, so the twelve melon
tiles of the recorded top-tier opening are silent through day 5 -- and the
argmax reads an empty board and hires nobody.  ON, and only for the scan, the
window and the harvest age are widened by `FORWARD_ADMIT_DAYS`, so a tile that
will emit a WATER or a HARVEST inside the horizon carries it now.

The switch is inert OFF and at a zero horizon (`test_off_*`, `test_days_zero_*`)
and never touches the day the route actually walks (`test_route_*`).
"""
from __future__ import annotations

import os
import sys

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

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


@pytest.fixture(autouse=True)
def _restore():
    """Every test leaves the module knobs where it found them."""
    on, days = P.FORWARD_ADMIT_ON, P.FORWARD_ADMIT_DAYS
    yield
    P.FORWARD_ADMIT_ON, P.FORWARD_ADMIT_DAYS = on, days


def _melon_open(day=1, money=3000, n=P.MELON_OPEN_TILES, nquad=1):
    """The forced opening's board on `day`: `n` melon tiles planted on day 0.

    Their window opens at age 6, so on days 1-5 not one of them emits an op --
    which is the whole failure this switch is about.
    """
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:n] = spec.KIND_PLANT
    occ[:n] = spec.I_MELON
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(nquad), price=BASE.copy())


def _ripe(day=13, money=3000):
    """A board with work today: 30 thirsty tomatoes, in and past their window."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    kind[:30] = spec.KIND_PLANT
    occ[:30] = spec.I_TOMATO
    t_yield = z.copy(); t_yield[:30] = 2
    t_cons = z.copy(); t_cons[:30] = 1
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4), price=BASE.copy())


def _plan(view):
    return [np.asarray(x) for x in P.build_day(np, view, _macro(), TABLE)]


def _hires(view):
    op = _plan(view)[3]
    return int((op == O.MO_HIRE).sum())


def _boards():
    return ([_melon_open(day=d) for d in range(1, 8)]
            + [_melon_open(day=1, money=222), _melon_open(day=10, money=9000),
               _ripe(), _ripe(day=4, money=500)])


def test_off_is_byte_identical_whatever_the_horizon_says():
    """OFF the second `_derive` is never built, so `FORWARD_ADMIT_DAYS` is dead
    weight -- the shipped plan is the one it always was."""
    P.FORWARD_ADMIT_ON = False
    P.FORWARD_ADMIT_DAYS = 3
    ref = [_plan(v) for v in _boards()]
    for days in (0, 1, 5, 9, 30):
        P.FORWARD_ADMIT_DAYS = days
        for a, v in zip(ref, _boards()):
            for x, y in zip(a, _plan(v)):
                assert np.array_equal(x, y), f"OFF moved at FORWARD_ADMIT_DAYS={days}"


def test_days_zero_equals_off():
    """A zero horizon is the identity: `age + 0 >= c_ws` is `age >= c_ws`, and
    the scan skips the extra pass outright rather than deriving a copy."""
    P.FORWARD_ADMIT_ON = False
    ref = [_plan(v) for v in _boards()]
    P.FORWARD_ADMIT_ON = True
    P.FORWARD_ADMIT_DAYS = 0
    for a, v in zip(ref, _boards()):
        for x, y in zip(a, _plan(v)):
            assert np.array_equal(x, y)


def test_the_silent_melon_field_hires_nobody_until_the_horizon_reaches_it():
    """Day 1 of the forced opening: twelve melon tiles, window at age 6.

    OFF the day hires nobody -- there is no task on the board to pay for a
    hand.  ON, the crew appears exactly when the horizon reaches the window
    (age 1 + 5 = 6), and grows with it.  Monotone in the horizon, because the
    projected task set is a superset of the day's own.
    """
    view = _melon_open(day=1)
    P.FORWARD_ADMIT_ON = False
    assert _hires(view) == 0
    seen = []
    for days in (2, 3, 5, 6, 9):
        P.FORWARD_ADMIT_ON = True
        P.FORWARD_ADMIT_DAYS = days
        seen.append(_hires(view))
    assert seen == sorted(seen), seen                     # monotone in the horizon
    assert seen[0] == 0                                   # 1 + 2 < 6: still silent
    assert seen[2] > 0                                    # 1 + 5 == 6: the window
    assert seen[-1] > seen[2]                             # and the harvest too


def test_the_horizon_reaches_the_window_a_day_at_a_time():
    """Day 3 with a three-day horizon is the same board as day 1 with a five-day
    one: what the scan sees is `age + FORWARD_ADMIT_DAYS`, nothing else."""
    P.FORWARD_ADMIT_ON = True
    P.FORWARD_ADMIT_DAYS = 3
    assert _hires(_melon_open(day=2)) == 0                # 2 + 3 = 5 < 6
    assert _hires(_melon_open(day=3)) > 0                 # 3 + 3 = 6


def test_the_route_still_walks_only_todays_work():
    """The projection buys hands, never ops: on day 1 the melon window is shut,
    so whatever the crew size, not one WATER or HARVEST is emitted."""
    view = _melon_open(day=1)
    P.FORWARD_ADMIT_ON = True
    P.FORWARD_ADMIT_DAYS = 9
    assert _hires(view) > 0
    ops = _plan(view)[0]
    for banned in (O.OP_WATER, O.OP_HARVEST):
        assert int((ops == banned).sum()) == 0, O.OP_NAMES[banned]


def test_enumeration_agrees_across_backends():
    import jax
    import jax.numpy as jnp
    P.FORWARD_ADMIT_ON = True
    P.FORWARD_ADMIT_DAYS = 5
    view, macro = _melon_open(day=1), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        assert np.array_equal(np.asarray(x), np.asarray(y))
