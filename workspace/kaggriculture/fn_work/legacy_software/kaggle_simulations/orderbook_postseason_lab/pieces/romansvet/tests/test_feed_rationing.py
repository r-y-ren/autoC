"""When feed wheat runs short, the animals worth most are fed first
(PLANNER_V3_1 section 0.6): remaining sellable production capped at the
animal's cost, plus the care bank the feed cashes, serpentine position as the
final tiebreak. A feed that only cashes a bank is worth that payout alone, so
it never outranks an animal whose life is at stake.
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
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _view(animals, wheat, day=5):
    """`animals`: list of (serpentine position, animal index), hungry with no
    care bank -- or (position, animal index, t_cons, t_bank) to say otherwise.
    All placed on day 0; `wheat` in the shed and no money to buy more."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons, t_bank = z.copy(), z.copy()
    for entry in animals:
        pos, a = entry[0], entry[1]
        cons, bank = (entry + (1, 0))[2:4]
        kind[pos] = spec.ANIMAL_STRUCT[a]
        occ[pos] = a
        t_cons[pos], t_bank[pos] = cons, bank
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4),
        price=np.full(spec.N_PRODUCTS, 25, np.int32), t_bank=t_bank)


def _feed_turns(view, **macro):
    unit_op = P.build_day(np, view, _macro(**macro))[0]
    return [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_FEED)]


def test_the_costlier_animal_is_fed_when_one_wheat_is_left():
    # goose at position 0 (value capped at its 300 cost), sheep at position 50
    # (capped at 500). One unit, one wheat: only the sheep gets a FEED task.
    # Position 50 is tile (9, 5): 6 moves from the spawn at (4, 4), after the
    # wheat pickup at turn 2 -- FEED lands on turn 9. The goose at (0, 0)
    # would have been 8 moves away (turn 11).
    assert _feed_turns(_view([(0, 0), (50, 2)], wheat=1)) == [O.ROUTE_BASE + 1 + 6]


def test_ties_fall_to_the_lower_position():
    # two identical geese: the one at position 3 -- tile (3, 0), 5 moves --
    # is fed; position 7 is tile (7, 0), 7 moves away
    assert _feed_turns(_view([(7, 0), (3, 0)], wheat=1)) == [O.ROUTE_BASE + 1 + 5]


def test_a_bank_only_feed_never_beats_a_hungry_animal():
    # day 10, one wheat: goose A at position 0 is not hungry but banked a CARE
    # bonus and fires tonight, so it wants a feed to cash it; goose B at
    # position 3 is hungry. Both are geese with the same replacement value, so
    # the old rank tied on value and fell to A, the lower position -- trading a
    # 300-coin goose for one 25-coin egg. A bank-only feed is now worth the
    # payout alone, so the wheat goes to B at tile (3, 0), 5 moves out.
    turns = _feed_turns(_view([(0, 0, 0, 1), (3, 0)], wheat=1, day=10))
    assert turns == [O.ROUTE_BASE + 1 + 5]


def test_a_bank_breaks_the_tie_between_two_hungry_animals():
    # both geese are hungry and equally costly to replace, but the one at
    # position 7 also cashes a banked egg tonight, so it outranks the nearer
    # goose at position 3 despite the higher serpentine index. Position 7 is
    # tile (7, 0), 7 moves from the spawn.
    turns = _feed_turns(_view([(3, 0), (7, 0, 1, 1)], wheat=1, day=10))
    assert turns == [O.ROUTE_BASE + 1 + 7]


def test_rank_by_orders_by_value_then_index():
    mask = np.zeros(10, bool)
    mask[[1, 4, 6, 8]] = True
    value = np.array([0, 5, 0, 0, 9, 0, 5, 0, 1, 0], np.int32)
    rank = P._rank_by(np, mask, value)
    assert rank[4] == 0 and rank[1] == 1 and rank[6] == 2 and rank[8] == 3


def test_rank_by_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(2)
    for _ in range(20):
        mask = rng.random(100) < 0.5
        value = rng.integers(0, 4, size=100).astype(np.int32)
        a = P._rank_by(np, mask, value)
        b = np.asarray(P._rank_by(jnp, jnp.asarray(mask), jnp.asarray(value)))
        assert a[mask].tolist() == b[mask].tolist()
