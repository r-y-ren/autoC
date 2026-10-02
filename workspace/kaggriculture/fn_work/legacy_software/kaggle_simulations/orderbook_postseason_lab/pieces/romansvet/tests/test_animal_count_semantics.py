"""`animal_want` is the number of animals acquired today, per kind, full stop
(PLANNER_V3_1 section 0.8): zero restocks nothing, standing structures are
stocked before new ones are built, and stock already in the shed is placed
because placing is not an acquisition.

Per kind, and the kinds are not independent: cow and sheep both live on a
PASTURE, so they are assigned in one pass in list order and cannot claim the
same tile.
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
from test_budget_order import _macro, one_kind

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


def _view(free_coops=2, geese_in_shed=0):
    """`free_coops` empty coops at the head of the sweep, everything else
    empty; 3,000 coins on day 0."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:free_coops] = spec.KIND_COOP
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_GOOSE] = geese_in_shed
    return P.DayView(
        day=np.int32(0), kind=kind, occ=z - 1, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=shed, seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(3000), nquad=np.int32(1),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _counts(view, animal_count):
    plan = P.build_day(np, view, _macro(animal_want=one_kind(0, animal_count)))
    unit_op, op, qty = plan[0], plan[3], plan[5]
    bought = int(qty[O.TURN_BUY][op[O.TURN_BUY] == O.MO_BUY_ANIMAL].sum())
    return bought, int((unit_op == O.OP_PLACE).sum()), int((unit_op == O.OP_BUILD_COOP).sum())


def test_zero_acquires_nothing_even_with_empty_structures():
    assert _counts(_view(free_coops=2), 0) == (0, 0, 0)


def test_one_stocks_a_standing_coop_before_building():
    assert _counts(_view(free_coops=2), 1) == (1, 1, 0)


def test_three_stocks_both_coops_and_builds_one():
    assert _counts(_view(free_coops=2), 3) == (3, 3, 1)


def test_shed_stock_is_placed_without_being_counted():
    # two geese already bought sit in the shed: they go into the coops today
    # although the gene asks for no acquisition
    assert _counts(_view(free_coops=2, geese_in_shed=2), 0) == (0, 2, 0)
