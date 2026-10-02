"""Same-turn shed hand-offs: a unit's DROP is visible to a *later* unit's PICKUP.

The engine walks `[farmer, *hands]` in list order and mutates `private["shed"]`
inside each unit's DROP / PICKUP / PLACE-to-shed branch
(`kaggriculture.py:343`, `:358`, `:377`), so within one turn

  * unit 5 DROP, unit 6 PICKUP  -> unit 6 leaves the turn holding the item, and
  * unit 6 DROP, unit 5 PICKUP  -> unit 5's pickup finds nothing; the item lands
    in the shed and stays there,

and the same asymmetry decides who gets the last free slot when the shed is at
`shedCapacity`. `sim/units.py` used to resolve *every* pickup against the
hour-start shed before *every* drop, which made the first case impossible: the
receiving unit got nothing and the item was stranded for the rest of the season
(docs/strategy/2026-09-09-sim-tape-seat-bug.md -- four recorded opponent tapes
hand a COW between hands on day 7 and lost it).

Every scenario is played in `kaggle_environments` and in the simulator from one
installed board and compared field by field, through the harness in
`tests/test_drop_op.py`; the explicit assertions underneath say what the engine
is expected to have done, so a harness that agreed on the *wrong* answer would
still fail.
"""
from __future__ import annotations

import os
import sys

os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from kagg3 import spec
from kagg3.core import ops as O
from test_drop_op import Scenario, _assert_agrees, _run

# Shed-access tiles on a 10x10 board: (4,4) (5,4) (4,5) (5,5) -> 44 45 54 55.
# Units 5 and 6 are the pair the recorded tapes hand a cow between; units 0-4 are
# parked far from the shed so only the two under test can touch it.
U5_TILE, U6_TILE = 45, 54
FAR = [7, 8, 9, 17, 18]
UPOS = FAR + [U5_TILE, U6_TILE]
N_UNITS = len(UPOS)
U5, U6 = 5, 6

PASS, DROP, PICKUP, HARV = O.OP_PASS, O.OP_DROP, O.OP_PICKUP, O.OP_HARVEST
NORTH, SOUTH, EAST, WEST = O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST


def _row(**acts):
    """`_row(u5=(DROP, 0, 0))` -> one script row over all seven units."""
    row = [(PASS, 0, 0)] * N_UNITS
    for name, act in acts.items():
        row[int(name[1:])] = act
    return row


def _play(script, shed):
    sc = Scenario({}, UPOS, shed=shed)
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    return engine[-1]


# --- animal hand-off -------------------------------------------------------

def test_a_lower_unit_s_drop_is_picked_up_by_a_higher_unit_the_same_turn():
    """The exact day-7 turn the four `S/loss12` tapes play: unit 5 banks the cow
    it is carrying and unit 6 takes it straight back out of an empty shed."""
    last = _play([
        _row(u5=(PICKUP, spec.I_COW, 1)),          # 0: unit 5 takes the only cow
        _row(u5=(DROP, 0, 0), u6=(PICKUP, spec.I_COW, 1)),
    ], shed={"COW": 1})
    assert last["inv"][U6][spec.I_COW] == 1, "unit 6 must leave the turn with the cow"
    assert last["inv"][U5].sum() == 0, "unit 5 dropped everything it had"
    assert last["shed"].sum() == 0, "the cow passed through the shed, it did not stay"


def test_a_higher_unit_s_drop_is_not_seen_by_a_lower_unit_s_pickup():
    """The mirror image, which is what makes the order load-bearing: unit 5 acts
    first, finds the shed empty and takes nothing; unit 6's cow lands after it."""
    last = _play([
        _row(u6=(PICKUP, spec.I_COW, 1)),          # 0: unit 6 takes the only cow
        _row(u5=(PICKUP, spec.I_COW, 1), u6=(DROP, 0, 0)),
    ], shed={"COW": 1})
    assert last["inv"][U5].sum() == 0, "unit 5's pickup ran against an empty shed"
    assert last["inv"][U6].sum() == 0, "unit 6 dropped the cow"
    assert last["shed"][spec.I_COW] == 1, "the cow is in the shed, not on a unit"


# --- the capacity edge -----------------------------------------------------
# A plant one step off each unit's shed tile, so the unit can harvest a load and
# walk back with it: a DROP needs an inventory the shed did not hand out.
_U5_PLANT = 46      # (6,4), one step EAST of unit 5's (5,4)
_U6_PLANT = 64      # (4,6), one step SOUTH of unit 6's (4,5)


def _harvest_then(walk_out, walk_back, unit, plant, final_row, shed):
    sc = Scenario({plant: ("WHEAT", 4)}, UPOS, shed=shed)
    u = f"u{unit}"
    script = [
        _row(**{u: (walk_out, 0, 0)}),
        _row(**{u: (HARV, 0, 0)}),
        _row(**{u: (walk_back, 0, 0)}),
        final_row,
    ]
    engine, sim = _run(sc, script, {}, len(script))
    _assert_agrees(engine, sim)
    return engine[-1]


def test_an_earlier_pickup_makes_room_for_a_later_drop():
    """Shed at `shedCapacity`; unit 5 lifts four melons out of it, and unit 6's
    four wheat fit into the room unit 5 just made, in the same turn."""
    last = _harvest_then(
        SOUTH, NORTH, U6, _U6_PLANT,
        _row(u5=(PICKUP, spec.I_MELON, 4), u6=(DROP, 0, 0)),
        shed={"MELON": spec.SHED_CAPACITY})
    assert last["shed"][spec.I_MELON] == spec.SHED_CAPACITY - 4
    assert last["shed"][spec.I_WHEAT] == 4, "the whole load fit behind the pickup"
    assert last["shed"].sum() == spec.SHED_CAPACITY
    assert last["inv"][U6].sum() == 0
    assert last["inv"][U5][spec.I_MELON] == 4


def test_a_later_pickup_does_not_make_room_for_an_earlier_drop():
    """The same board with the roles swapped. Unit 5 drops into a shed that is
    still full, so the engine destroys the load; unit 6's pickup comes after and
    cannot save it."""
    last = _harvest_then(
        EAST, WEST, U5, _U5_PLANT,
        _row(u5=(DROP, 0, 0), u6=(PICKUP, spec.I_MELON, 4)),
        shed={"MELON": spec.SHED_CAPACITY})
    assert last["shed"][spec.I_WHEAT] == 0, "the drop hit a full shed and was destroyed"
    assert last["shed"][spec.I_MELON] == spec.SHED_CAPACITY - 4
    assert last["inv"][U5].sum() == 0, "DROP empties the unit even when it overflows"
    assert last["inv"][U6][spec.I_MELON] == 4
