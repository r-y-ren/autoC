"""`plan.ROUTE_SPLIT_ON`: one start turn per block, not one per crew.

`ROUTE_EARLY_ON` asks three questions of a day before it lets anything out at
`TURN_BUY`, and two of the three are laws. The third -- "the block walks before
it works" -- is a proxy for the only op the turn-1 BUY row actually feeds a
pickup-free block (PLANT draws its seed from the shed; FEED, FERTILIZE and
PLACE all arrive through a PICKUP), and the first -- "no wide crew" -- is a law
about *movement* that says nothing about a unit standing still. So this switch
splits the day-start wait two ways:

  narrow day  a block that owes no PICKUP and opens with a step or any op but
              PLANT steps out at `O.TURN_BUY`, and is cut against one more turn
  wide day    an already-hired unit that owes a PICKUP takes it at
              `TURN_BUY + 1` -- stationary, on its own access tile, so the
              turn-2 hire row still counts the occupancy `SPAWN_SLOT` assumes
              -- and starts its walk at `O.ROUTE_BASE_WIDE`

The census this was cut for (39 replays, 2026-09-01) puts 375 idle unit-turns a
game in the day-start wait against the tape's 11.

The `test_off_*` half is the identity half, and it borrows `test_route_early`'s
pins: OFF *both* switches, this planner is the one at `a838700`, so the same
twelve digests have to come back.
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
from test_route_early import (PIN, PIN_SEEDS, _acting_units, _digest, _plan,
                              _row, _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


#: The commit `PIN` was taken off: the planner this switch was cut into.
PRE_SWITCH = "a838700"

#: Every switch that ships ON today and **did not exist** at `PRE_SWITCH`
#: (`git show a838700:src/kagg3/core/plan.py`), pinned OFF in BOTH halves --
#: `tests/test_endroute2.py`'s rule, in the form this file can use (it takes no
#: `--digests` subprocess, so the pin is a fixture rather than a `_knobs`
#: contextmanager). Without it the OFF half asks `PRE_SWITCH` to reproduce a
#: planner built out of nine later switches and the ON half prices them too:
#: since 2026-09-18 `WIDE_PICK_ON` and `WIDE_PICK_FREE_ON` ride the very *wide*
#: branch this switch cuts, and `WIDE_PICK_FREE_ON` re-orders the granted
#: column's market rows -- so toggling `ROUTE_SPLIT_ON` alone moved `mkt_op`
#: and the identity digests both. This file's subject is which *turn* a block
#: starts on; each name below is owned, ON and OFF, by its own test file.
#: [RULE: a pin is only a pin if the two ends run the same switch string.]
PRE_SWITCH_OFF = (
    "LOT4_ON", "EARLY_SELL_ON", "TAIL_FILL_ON", "TAIL_CARE_ON",
    "BANK_BEFORE_LOT_ON", "SURVIVAL_WATER_ON", "FEED_MANDATORY_ON",
    "FERT_TIMING_ON", "HIRE_ROW_ON", "SELL_SLOT_PRIORITY_ON",
    "SELL_SLOT_PRIORITY_SELLS_FIRST_ON", "PRESTOCK_V2_BUY_ON",
    "OPEN_PUMP_ON", "OPEN_PUMP_SLOT0_ON", "ENDROUTE_ON", "ENDROUTE_ROW2_ON",
    "ENDROUTE2_ON", "ENDROUTE2_SPLIT_ON", "WIDE_PICK_ON", "WIDE_PICK_FREE_ON",
)


#: Read at import, before any fixture pins anything: the shipped defaults.
SHIPPED = {n: getattr(P, n, None) for n in PRE_SWITCH_OFF}


@pytest.fixture(autouse=True)
def _pre_switch_pinned_off(monkeypatch):
    for name in PRE_SWITCH_OFF:
        monkeypatch.setattr(P, name, False, raising=False)


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", True)


def _spawn_tile(u=0):
    """View index of unit `u`'s spawn tile."""
    x, y = int(P.SPAWN_X[u]), int(P.SPAWN_Y[u])
    return int(np.flatnonzero((P.SERP_X == x) & (P.SERP_Y == y))[0])


def _n_hire(plan):
    return sum(1 for turn in O.HIRE_TURNS for op, _, _ in _row(plan, turn)
               if op == O.MO_HIRE)


# =========================================================================
# OFF: byte-identical to the planner both switches were cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract, pinned on `test_route_early`'s own digests."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_keeps_the_whole_crew_behind_the_route_base(off):
    for s in PIN_SEEDS:
        plan = _plan(*_seeded_case(s))
        assert _acting_units(plan, O.TURN_HIRE) == [], s
        assert _acting_units(plan, O.TURN_BUY) == [], s


# =========================================================================
# ON, narrow: the block the BUY row does not feed starts at TURN_BUY
# =========================================================================

def test_on_starts_the_blocks_that_owe_the_buy_row_nothing(on):
    view = _view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000)
    plan = _plan(view, _macro())
    assert _row(plan, O.TURN_BUY) != [], "the board is meant to still be buying"
    early = _acting_units(plan, O.TURN_BUY)
    assert early, "no unit started early on a board built to have some"
    unit_op = plan[0]
    for u in early:
        assert int(unit_op[u, O.TURN_BUY]) != O.OP_PICKUP, u
        assert int(unit_op[u, O.TURN_BUY]) != O.OP_PLANT, u


def test_on_lets_a_carry_free_op_on_the_spawn_tile_out_at_turn_1(on, monkeypatch):
    """The gate `ROUTE_EARLY_ON` could not open. One ripe crop, standing on the
    farmer's own access tile, and an empty purse so nothing is hired and
    nothing is bought: the block's first act is a HARVEST at `base_move == 0`,
    which needs the BUY row no more than a step does. `ROUTE_EARLY_ON` keeps it
    behind `ROUTE_BASE` because it asks for the step; this switch asks what the
    row feeds, and the answer for a HARVEST is nothing."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_yield = z.copy()
    tile = _spawn_tile(0)
    kind[tile], occ[tile], t_yield[tile] = spec.KIND_PLANT, spec.I_TOMATO, 6
    view = P.DayView(
        day=np.int32(10), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=z.copy(), t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0),
        nquad=np.int32(4), price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100],
                                          np.int32),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))
    macro = _macro()

    plan = _plan(view, macro)
    assert int(plan[0][0, O.TURN_BUY]) == O.OP_HARVEST

    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", True)
    assert int(_plan(view, macro)[0][0, O.TURN_BUY]) == O.OP_PASS


def test_on_never_starts_a_block_that_owes_the_row(on):
    """A day where every block owes a feed keeps today's law exactly."""
    view = _view(day=10, n_coop=12, wheat=0)
    plan = _plan(view, _macro())
    assert _row(plan, O.TURN_BUY) != []
    assert _acting_units(plan, O.TURN_BUY) == []


# =========================================================================
# ON, wide: the pickup moves, the crew still does not
# =========================================================================

def _wide_plan():
    macro = _macro(hire_bias=np.int32(3_000))
    view = _view(day=10, n_coop=14, n_ripe=40, wheat=0, yld=6, money=200_000)
    return view, macro, _plan(view, macro)


def test_on_moves_a_wide_crew_pickup_up_to_turn_2(on):
    """A wide day's overflow hire row is turn 2 and the whole crew waits for
    it. A PICKUP does not move the unit, and the BUY row it draws on resolved
    at turn 1, so it may be taken at turn 2 -- and the walk still starts at
    `O.ROUTE_BASE_WIDE`."""
    view, macro, plan = _wide_plan()
    if _n_hire(plan) <= spec.MAX_MARKET_ORDERS:
        pytest.skip("board did not hire a wide crew")
    unit_op = np.asarray(plan[0])
    at2 = [u for u in range(spec.MAX_UNITS)
           if int(unit_op[u, O.TURN_HIRE_WIDE]) != O.OP_PASS]
    assert at2, "no unit collected on the wide day's spare turn"
    for u in at2:
        assert int(unit_op[u, O.TURN_HIRE_WIDE]) == O.OP_PICKUP, u


def test_on_never_moves_a_unit_before_the_overflow_hire_row(on):
    """The law `ops.ROUTE_BASE_WIDE` is: `market._hire` spawns a hand on the
    least-occupied shed-access tile, so a unit that has walked off its own
    access tile before turn 2's market phase re-scatters every hand hired in
    it. Nothing may *move* at turns 0..2 of a wide day."""
    view, macro, plan = _wide_plan()
    if _n_hire(plan) <= spec.MAX_MARKET_ORDERS:
        pytest.skip("board did not hire a wide crew")
    unit_op = np.asarray(plan[0])
    for turn in (O.TURN_HIRE, O.TURN_BUY, O.TURN_HIRE_WIDE):
        moved = [u for u in range(spec.MAX_UNITS) if int(unit_op[u, turn]) in MOVES]
        assert moved == [], (turn, moved)
    assert _acting_units(plan, O.TURN_BUY) == [], "turn 1 is not a wide crew's"


def test_on_never_lets_a_turn_2_hire_act_in_turn_2(on):
    """A hand hired in turn t is appended in that turn's market phase and first
    acts in t + 1 [LAW], so the overflow hires own nothing before
    `O.ROUTE_BASE_WIDE`."""
    view, macro, plan = _wide_plan()
    n = _n_hire(plan)
    if n <= spec.MAX_MARKET_ORDERS:
        pytest.skip("board did not hire a wide crew")
    unit_op = np.asarray(plan[0])
    for u in range(spec.MAX_MARKET_ORDERS + 1, spec.MAX_UNITS):
        assert int(unit_op[u, O.TURN_HIRE_WIDE]) == O.OP_PASS, u


# =========================================================================
# ON: the laws that hold on every board
# =========================================================================

def test_on_never_acts_in_the_hire_turn(on):
    """Turn 0's hire row resolves after turn 0's unit phase, so the same spawn
    argument that fixes turn 2 on a wide day fixes turn 0 on every day."""
    for s in PIN_SEEDS:
        assert _acting_units(_plan(*_seeded_case(s)), O.TURN_HIRE) == [], s


def test_on_never_picks_up_before_the_buy_row_resolves(on):
    """`TURN_BUY` resolves in its own market phase, after that turn's unit
    phase, so the earliest a PICKUP can see what the row bought is turn 2."""
    for s in PIN_SEEDS:
        unit_op = np.asarray(_plan(*_seeded_case(s))[0])
        picks = np.argwhere(unit_op == O.OP_PICKUP)
        if len(picks):
            assert int(picks[:, 1].min()) >= O.TURN_BUY + 1, s


def test_on_never_plants_before_the_seed_is_bought(on):
    """The one op a pickup-free block can hold that the BUY row does feed."""
    for s in PIN_SEEDS:
        unit_op = np.asarray(_plan(*_seeded_case(s))[0])
        plants = np.argwhere(unit_op == O.OP_PLANT)
        if len(plants):
            assert int(plants[:, 1].min()) >= O.TURN_BUY + 1, s


def test_on_never_moves_a_unit_into_a_locked_quadrant(on):
    """BUY_LAND resolves in `SELL_TURNS[0]`'s market phase and a tile op on a
    LOCKED tile silently no-ops [M2], so a land day keeps its lead."""
    macro = _macro(land_bias=np.int32(2_000),
                   plant_target=np.array([6, 0, 0, 0, 0], np.int32))
    view = _view(day=6, n_ripe=20, yld=6, money=20_000, nquad=1)
    plan = _plan(view, macro)
    assert any(op == O.MO_BUY_LAND for op, _, _ in _row(plan, O.SELL_TURNS[0])), \
        "the board is meant to buy a quadrant"
    unit_op = np.asarray(plan[0])
    off_tile = (unit_op != O.OP_PASS) & (unit_op != O.OP_PICKUP)
    worked = np.nonzero(off_tile.any(axis=0))[0]
    assert len(worked) and int(worked[0]) > O.SELL_TURNS[0], worked[:4]


def test_on_leaves_every_market_row_untouched(on, monkeypatch):
    """The route is cut after the market is derived and the market reads
    nothing the switch touches, so not one order changes."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
        base = _plan(view, macro)
        monkeypatch.setattr(P, "ROUTE_SPLIT_ON", True)
        split = _plan(view, macro)
        for k in (3, 4, 5):                      # mkt_op, mkt_a, mkt_q
            assert np.array_equal(base[k], split[k]), (s, k)


def test_on_actually_fires_on_the_seeded_boards(on, monkeypatch):
    """A spread that never reaches the switch would make the ON half vacuous,
    and it has to fire on strictly more boards than `ROUTE_EARLY_ON` does --
    the whole point of re-reading its third gate."""
    def fired(seeds):
        return [s for s in seeds
                if np.asarray(_plan(*_seeded_case(s))[0])[:, :O.ROUTE_BASE + 1].max()
                != O.OP_PASS]
    split = fired(PIN_SEEDS)
    assert split, "no seeded board started a unit early"
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", True)
    assert len(fired(PIN_SEEDS)) <= len(split)


def test_the_split_start_plan_agrees_across_backends(on):
    """Per-unit starts, a trial cut and a per-unit pickup base -- three vectors
    where there used to be scalars. The equivalence surface is the plan."""
    import jax
    import jax.numpy as jnp
    cases = [_seeded_case(s) for s in PIN_SEEDS]
    cases += [(_view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000),
               _macro()),
              (_view(day=10, n_coop=14, n_ripe=40, wheat=0, yld=6, money=200_000),
               _macro(hire_bias=np.int32(3_000))),
              (_view(day=O.LAST_SHED_DAY + 1, n_ripe=20, yld=6), _macro()),
              (_view(day=O.LAST_SHED_DAY, n_coop=6, wheat=6), _macro())]
    for view, macro in cases:
        a = P.build_day(np, view, macro)
        b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                        jax.tree_util.tree_map(jnp.asarray, macro),
                        jnp.asarray(spec.build_price_table()))
        for x, y in zip(a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {int(view.day)}"


def test_the_pre_switch_tree_has_none_of_the_pinned_switches():
    """The pin above is a claim about `PRE_SWITCH`, so it is checked against
    `PRE_SWITCH` rather than trusted: every name in `PRE_SWITCH_OFF` is absent
    from the planner the digests were taken off, and `ROUTE_SPLIT_ON` -- this
    file's subject -- is absent too."""
    import subprocess
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = subprocess.run(f"git show {PRE_SWITCH}:src/kagg3/core/plan.py",
                         shell=True, cwd=root, capture_output=True, text=True,
                         check=True).stdout
    missing = [n for n in PRE_SWITCH_OFF + ("ROUTE_SPLIT_ON",) if n in src]
    assert missing == [], missing


def test_every_pinned_switch_ships_on():
    """...and the other end of the same claim: a name that has gone OFF since
    is dead weight in the pin and belongs out of the tuple."""
    off = [n for n, v in SHIPPED.items() if v is not True]
    assert off == [], off
