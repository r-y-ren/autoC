"""`plan.MIDDAY_DROP_ON`: run the DROP chain on day 28 as well as day 29.

The premise this switch is *not* built on: "a hired hand's inventory is lost at
nightfall". It is not. `_end_of_day` calls `_drop_inventories_to_shed` for every
seat before it clears `farm["hands"]`, so every unit's load is banked into the
shed for free, wherever the unit stands. What the nightly dump does destroy is
the part that does not fit the 100-unit shed -- and measured in the real engine
(48 games, champion theta vs kagg2) two thirds of the season's destruction lands
on `O.LAST_SHED_DAY`, the day the deadline harvest empties the board.

So the switch moves the day-29 chain -- return leg, `SELL_TURNS[-1]` budget, lot
3's offer of the banked load -- one day back, and nothing else. Day 28 keeps its
purchases, its reservations and its tomorrow: `terminal` does not move, and
neither does `_worth_a_turn`, which reads `terminal` and not `drop_day`.

Measured and **rejected**: 96 seeds x 2 seats against kagg2, paired diff
-1,157 coins, t = -11.3. The return leg costs a day-28 unit about ten of its
twenty-two turns and the overflow it saves is worth at most 675 a game. The
switch stays here because the measurement is the point -- and because OFF,
`drop_day` is `terminal` again and every expression re-evaluates to the one it
replaced (verified against `rep/drop_b28.csv`, all 192 rows identical). These
tests pin the behaviour under both settings so a future second-block routing
attempt has something to build on.
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
from test_day29_endgame import _greedy_macro, _ripe_view, _sold, _view, _walk

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

LAST = O.LAST_SHED_DAY                                   # 28


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "MIDDAY_DROP_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "MIDDAY_DROP_ON", True)
    monkeypatch.setattr(P, "HORIZON_DROP_ON", False)   # the day-28 chain was measured on the 28-horizon


def _plan(view):
    return tuple(np.asarray(a) for a in P.build_day(np, view, _greedy_macro()))


def _plans(monkeypatch, view, midday):
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "MIDDAY_DROP_ON", midday)
    monkeypatch.setattr(P, "HORIZON_DROP_ON", False)   # the day-28 chain was measured on the 28-horizon
    return _plan(view)


def _drop_turns(unit_op, u):
    return [t for t in range(spec.TURNS_PER_DAY) if int(unit_op[u, t]) == O.OP_DROP]


# ---------------------------------------------------------------- switch OFF

def test_off_leaves_day_28_working_to_the_last_turn(off):
    """The day-29 budget cut is what the switch buys; off, day 28 keeps all 24
    turns and banks nothing by hand."""
    unit_op = _plan(_ripe_view(LAST))[0]
    assert not np.any(unit_op == O.OP_DROP), "day 28 must not DROP with the switch off"
    worked = np.any(unit_op != O.OP_PASS, axis=0)
    assert np.any(worked[O.SELL_TURNS[-1] + 1:]), \
        "off, day 28's route must still use the turns after the last lot"


@pytest.mark.parametrize("day", [20, 27, LAST, 29])
def test_off_is_the_plan_it_always_was(monkeypatch, day):
    """The refactor that split `drop_day` from `_worth_a_turn`'s `terminal` is
    a rename off the switch: two builds of the same day must agree, and day 29
    -- where `drop_day` and `terminal` coincide either way -- must not move
    when the switch is thrown."""
    view = _ripe_view(day)
    a = _plans(monkeypatch, view, False)
    b = _plans(monkeypatch, view, False)
    for x, y in zip(a, b):
        assert np.array_equal(x, y)


@pytest.mark.parametrize("day", [20, 27, 29])
def test_the_switch_moves_no_day_but_28(monkeypatch, day):
    """Day 29 is already a DROP day and days before 28 are not; only
    `LAST_SHED_DAY` may change."""
    view = _ripe_view(day)
    a = _plans(monkeypatch, view, False)
    b = _plans(monkeypatch, view, True)
    for i, (x, y) in enumerate(zip(a, b)):
        assert np.array_equal(x, y), f"day {day} plan array {i} moved"


# ---------------------------------------------------------------- switch ON

def test_day_28_harvests_walks_home_and_drops(on):
    """The section-4 chain, one day earlier."""
    view = _ripe_view(LAST)
    unit_op, _, _, op, arg, qty = _plan(view)
    assert int((unit_op == O.OP_HARVEST).sum()) > 0, "day 28 must work its ripe tiles"

    access = {tuple(xy) for xy in spec.SHED_ACCESS_XY}
    dropped = 0
    for u in range(spec.MAX_UNITS):
        turns = _drop_turns(unit_op, u)
        if not turns:
            assert int((unit_op[u] != O.OP_PASS).sum()) == 0, \
                f"unit {u} worked but never banked its load"
            continue
        assert len(turns) == 1, f"unit {u} drops {len(turns)} times"
        t = turns[0]
        # A unit acts before its turn's market, so turn 18 itself still sells.
        assert t <= O.SELL_TURNS[-1], f"unit {u} drops at {t}, past the last lot"
        assert _walk(unit_op, u)[t] in access, f"unit {u} drops away from the shed"
        assert np.all(unit_op[u, t + 1:] == O.OP_PASS)
        dropped += 1
    assert dropped > 0


def test_day_28_last_lot_offers_what_the_route_banks(on):
    """`_view`'s shed holds no tomato at all, so anything sold in lot 3 can
    only have come off the route -- and lots 1 and 2, which resolve before the
    DROP, must not offer it."""
    view = _ripe_view(LAST)
    _, _, _, op, arg, qty = _plan(view)
    assert int(view.shed[spec.I_TOMATO]) == 0
    assert _sold(op, arg, qty, O.SELL_TURNS[-1]).get(spec.I_TOMATO, 0) > 0
    assert _sold(op, arg, qty, O.SELL_TURNS[0]).get(spec.I_TOMATO, 0) == 0
    assert _sold(op, arg, qty, O.SELL_TURNS[1]).get(spec.I_TOMATO, 0) == 0


def test_day_28_still_has_a_tomorrow(on):
    """`terminal` does not move with the switch: day 28 still buys land (M2,
    on the first SELL turn), which the terminal day is forbidden to do."""
    op, arg, qty = _plan(_ripe_view(LAST))[3:6]
    assert int(qty[op == O.MO_BUY_LAND].sum()) == 1


@pytest.mark.parametrize("day,pruned", [(27, False), (LAST, False), (29, True)])
def test_worth_a_turn_stays_keyed_to_the_terminal_day(monkeypatch, day, pruned):
    """The seam itself. `_worth_a_turn` cuts every task the day prices at zero,
    which is only sound where there is no tomorrow -- day 28 has one, so it
    must be called with `terminal` and not with the widened `drop_day`."""
    seen = []
    real = P._worth_a_turn
    monkeypatch.setattr(P, "_worth_a_turn",
                        lambda xp, d, flag: (seen.append(bool(flag)), real(xp, d, flag))[1])
    monkeypatch.setattr(P, "DROP_ON", True)
    monkeypatch.setattr(P, "MIDDAY_DROP_ON", True)
    monkeypatch.setattr(P, "HORIZON_DROP_ON", False)   # the day-28 chain was measured on the 28-horizon
    _plan(_ripe_view(day))
    assert seen and set(seen) == {pruned}, f"day {day}: _worth_a_turn saw {seen}"


def test_day_28_banks_before_the_night_dump_can_destroy_it(on):
    """What the switch is for: the load reaches the shed while a lot can still
    sell it, instead of meeting `SHED_CAPACITY` at end of day.

    A board with far more ripe produce than the shed holds: off the switch the
    day sells nothing (`_view`'s shed is under every reservation and the
    harvest never reaches a lot); on, lot 3 clears the route's load."""
    view = _ripe_view(LAST)
    n_lot3 = sum(_sold(*_plan(view)[3:6], O.SELL_TURNS[-1]).values())
    assert n_lot3 > 0


# ---------------------------------------------------------------- backends

def test_numpy_and_jax_agree_with_the_switch_on(on):
    """The switch must not split the two planner backends: `drop_day` is a
    traced scalar on the JAX side and a numpy bool on the other."""
    import jax.numpy as jnp

    view = _ripe_view(LAST)
    jview = view._replace(**{f: jnp.asarray(getattr(view, f))
                             for f in type(view)._fields})
    macro = _greedy_macro()
    jmacro = macro._replace(**{f: jnp.asarray(getattr(macro, f))
                               for f in type(macro)._fields})
    a = _plan(view)
    b = tuple(np.asarray(x) for x in P.build_day(jnp, jview, jmacro))
    for i, (x, y) in enumerate(zip(a, b)):
        assert np.array_equal(x, y), f"backends disagree on plan array {i}"
