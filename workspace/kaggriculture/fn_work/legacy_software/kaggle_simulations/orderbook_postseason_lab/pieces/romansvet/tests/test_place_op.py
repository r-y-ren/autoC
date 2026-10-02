"""PLACE-to-shed in `sim/units.py` against the real engine.

`ef6aaa6` gave `apply_units` the engine's *selective* shed deposit
(`kaggriculture.py:377-408`): a PLACE that is not an animal going onto a
matching free structure banks `min(qty, inv[item])` of the one named item,
obeys `shedCapacity`, and -- unlike DROP -- leaves the remainder on the unit
instead of destroying it. `tests/test_midday_place.py` pins the planner and the
simulator's own five branches; nothing pinned the branch against
kaggle_environments, which is what this file does.

The harness is `test_drop_op`'s, unchanged: one scenario installed into both
backends, one hand-written script, a field-by-field comparison after every turn.
Where a branch is invisible in the compared snapshot -- an animal on a coop
looks exactly like an empty coop there -- the script follows the PLACE with a
DIG, which the engine refuses on an occupied structure and allows on a free one,
so the branch actually taken shows up in `kinds`.
"""
from __future__ import annotations

import numpy as np
import pytest
from test_drop_op import (
    DROP,
    EAST,
    FARMER,
    H1,
    H2,
    HARV,
    NORTH,
    PASS,
    SOUTH,
    WEST,
    Scenario,
    _assert_agrees,
    _run,
)

from kagg3 import spec
from kagg3.core import ops as O

PLACE, PICKUP, DIG = O.OP_PLACE, O.OP_PICKUP, O.OP_DIG
COOP, PASTURE = O.OP_BUILD_COOP, O.OP_BUILD_PASTURE

#: `test_drop_op`'s board: one ripe crop one step off each of the three
#: shed-access tiles the units start on.
PLANTS = {43: ("WHEAT", 4), 46: ("TOMATO", 3), 64: ("CARROT", 5)}


def _rows(script, n):
    return [list(r) + [(PASS, 0, 0)] * (n - len(r)) for r in script]


def _fetch_wheat(place):
    """Farmer walks to 43, harvests 4 wheat, walks back to the shed, then runs
    `place` (one op per turn) standing on the access tile."""
    sc = Scenario(dict(PLANTS), [FARMER])
    script = [[(WEST, 0, 0)], [(HARV, 0, 0)], [(EAST, 0, 0)]] + [[op] for op in place]
    return sc, script


# --- (1) the plain deposit --------------------------------------------------

def test_place_of_a_harvested_crop_banks_exactly_that_many():
    sc, script = _fetch_wheat([(PLACE, spec.I_WHEAT, 3)])
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"][spec.I_WHEAT] == 3
    assert last["inv"][0][spec.I_WHEAT] == 1, "PLACE leaves the remainder carried"


# --- (2) qty larger than what the unit carries ------------------------------

@pytest.mark.parametrize("qty", [5, spec.SHED_CAPACITY, 10_000])
def test_place_clamps_to_the_carried_amount(qty):
    """The planner passes `SHED_CAPACITY` as the argument, so the clamp against
    the unit's own stack is the normal path, not an edge case."""
    sc, script = _fetch_wheat([(PLACE, spec.I_WHEAT, qty)])
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    assert engine[-1]["shed"][spec.I_WHEAT] == 4
    assert engine[-1]["inv"].sum() == 0


# --- (3) the shed at (and near) capacity ------------------------------------

@pytest.mark.parametrize("room", [0, 1, 3, 4, 9])
def test_place_obeys_shed_capacity_and_keeps_the_overflow(room):
    """DROP destroys what does not fit; PLACE hands it back to the unit."""
    sc, script = _fetch_wheat([(PLACE, spec.I_WHEAT, spec.SHED_CAPACITY)])
    sc.shed = {"MELON": spec.SHED_CAPACITY - room}
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    fit = min(4, room)
    assert last["shed"][spec.I_WHEAT] == fit
    assert last["inv"][0][spec.I_WHEAT] == 4 - fit, "the overflow stays carried"
    assert last["shed"].sum() == spec.SHED_CAPACITY - room + fit


# --- (4) an item the unit does not carry ------------------------------------

@pytest.mark.parametrize("item", [spec.I_TOMATO, spec.I_FERT, spec.I_SHEEP])
def test_place_of_an_item_the_unit_does_not_carry_is_a_no_op(item):
    sc, script = _fetch_wheat([(PLACE, item, 5)])
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    assert engine[-1]["shed"].sum() == 0
    assert engine[-1]["inv"][0][spec.I_WHEAT] == 4


def test_place_of_zero_is_a_no_op():
    sc, script = _fetch_wheat([(PLACE, spec.I_WHEAT, 0)])
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    assert engine[-1]["shed"].sum() == 0


def test_place_away_from_the_shed_is_a_no_op():
    """Standing on the crop, not on an access tile: neither branch applies."""
    sc = Scenario(dict(PLANTS), [FARMER])
    script = [[(WEST, 0, 0)], [(HARV, 0, 0)], [(PLACE, spec.I_WHEAT, 4)]]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    assert engine[-1]["shed"].sum() == 0
    assert engine[-1]["inv"][0][spec.I_WHEAT] == 4


# --- (5) the animal branch must not swallow a product PLACE -----------------
# The four ways `kaggriculture.py:381-392` can be reached, each followed by a
# DIG so the branch actually taken is visible: DIG clears a free structure and
# is refused on an occupied one.

def test_place_of_a_product_on_a_free_coop_banks_it_and_spawns_nothing():
    """`item in ANIMALS` is the engine's first guard. Without it a PLACE of
    wheat onto a free coop would hatch a goose there and bank nothing."""
    sc, script = _fetch_wheat([(COOP, 0, 0), (PLACE, spec.I_WHEAT, 4), (DIG, 0, 0)])
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"][spec.I_WHEAT] == 4 and last["inv"].sum() == 0
    assert last["kinds"][FARMER] == ".", "the coop was empty, so the DIG cleared it"


def test_place_of_an_animal_on_a_mismatched_structure_falls_through_to_the_shed():
    """A GOOSE wants a COOP. On a PASTURE the animal branch does not match and
    the shed branch takes it back -- the case the `arg >= I_GOOSE` half of the
    simulator's predicate exists for."""
    sc = Scenario(dict(PLANTS), [FARMER], shed={"GOOSE": 1})
    script = [[(PICKUP, spec.I_GOOSE, 1)], [(PASTURE, 0, 0)],
              [(PLACE, spec.I_GOOSE, 1)], [(DIG, 0, 0)]]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"][spec.I_GOOSE] == 1 and last["inv"].sum() == 0
    assert last["kinds"][FARMER] == ".", "no goose was placed, so the DIG cleared it"


def test_place_of_an_animal_on_its_own_free_structure_takes_the_animal_branch():
    """The complement: the shed must *not* see this one."""
    sc = Scenario(dict(PLANTS), [FARMER], shed={"GOOSE": 1})
    script = [[(PICKUP, spec.I_GOOSE, 1)], [(COOP, 0, 0)],
              [(PLACE, spec.I_GOOSE, 1)], [(DIG, 0, 0)]]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"].sum() == 0 and last["inv"].sum() == 0
    assert last["kinds"][FARMER] == "COOP", "the goose is on the tile, so DIG is refused"


def test_place_of_an_animal_the_unit_does_not_carry_banks_nothing():
    """The engine takes the animal branch on the *structure*, fails `_inv_take`
    and returns -- it never reaches the shed. The simulator gets there the other
    way (the shed branch with nothing to bank); both must end up inert."""
    sc = Scenario(dict(PLANTS), [FARMER], shed={"GOOSE": 1})
    script = [[(COOP, 0, 0)], [(PLACE, spec.I_GOOSE, 1)], [(DIG, 0, 0)]]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    assert last["shed"][spec.I_GOOSE] == 1, "the shed's goose was never touched"
    assert last["kinds"][FARMER] == "."


# --- unit order, shared with DROP -------------------------------------------

@pytest.mark.parametrize("room", [0, 2, 4, 7, 12])
def test_place_and_drop_share_the_room_in_unit_index_order(room):
    """Three units reach the shed on the same turn with one PLACE, one DROP and
    one PLACE. The engine walks them in index order, so which op gets the last
    slot -- and whether its leftover is kept or destroyed -- is order-dependent.
    """
    sc = Scenario(dict(PLANTS), [FARMER, H1, H2],
                  shed={"MELON": spec.SHED_CAPACITY - room})
    script = _rows([
        [(WEST, 0, 0), (EAST, 0, 0), (SOUTH, 0, 0)],
        [(HARV, 0, 0), (HARV, 0, 0), (HARV, 0, 0)],
        [(EAST, 0, 0), (WEST, 0, 0), (NORTH, 0, 0)],
        [(PLACE, spec.I_WHEAT, 2), (DROP, 0, 0), (PLACE, spec.I_CARROT, spec.SHED_CAPACITY)],
    ], 3)
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    last = engine[-1]
    banked = last["shed"].sum() - (spec.SHED_CAPACITY - room)
    assert banked == min(room, 2 + 3 + 5)
    # The DROP's leftover is destroyed, the PLACEs' leftovers are still carried.
    assert last["inv"][0][spec.I_WHEAT] == 4 - last["shed"][spec.I_WHEAT]
    assert last["inv"][1].sum() == 0, "DROP empties its unit however little fit"
    assert last["inv"][2][spec.I_CARROT] == 5 - last["shed"][spec.I_CARROT]


def test_a_second_place_after_the_shed_filled_keeps_the_rest():
    """Two deposits from one unit across turns: the first fills the shed, the
    second finds no room and the unit walks away still loaded."""
    sc = Scenario({43: ("WHEAT", 8)}, [FARMER], shed={"MELON": spec.SHED_CAPACITY - 5})
    script = [[(WEST, 0, 0)], [(HARV, 0, 0)], [(EAST, 0, 0)],
              [(PLACE, spec.I_WHEAT, 3)], [(PLACE, spec.I_WHEAT, 4)],
              [(PLACE, spec.I_WHEAT, 4)]]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    shed = [int(np.asarray(s["shed"])[spec.I_WHEAT]) for s in engine]
    assert shed[3:] == [3, 5, 5]
    assert engine[-1]["inv"][0][spec.I_WHEAT] == 3
    assert engine[-1]["shed"].sum() == spec.SHED_CAPACITY
