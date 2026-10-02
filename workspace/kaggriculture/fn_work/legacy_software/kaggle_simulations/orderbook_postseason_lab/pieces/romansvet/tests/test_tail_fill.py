"""`plan.TAIL_FILL_ON`: spend the turns between the block and the end of day.

`_routes` cuts a block at the last tile whose whole chain the budget reaches,
so what is left is the turns the *next* tile did not fit into -- 555 idle
unit-turns a game by the 39-replay census (2026-09-01), 41% of all our idle, a
mean 2.5 turns of day left, and a carry-free task reachable at 81% of them a
median one tile away. The filler walks to the nearest tile that offers one and
takes it, up to `plan.TAIL_HOPS` times.

The one thing it may never do is touch the day's own plan: it only ever fills a
tile at rank >= `n_admit`, which no block can hold (`end` is
`min(jmax, n_tasks - 1)`), and a tile one unit fills is struck off for the
units after it. So ON and OFF agree on every turn OFF does not PASS, on every
market row, and on every DROP day, whose tail is the return leg.
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
from test_route_early import (PIN, PIN_SEEDS, _digest, _plan, _row,
                              _seeded_case, _view)

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)
#: What a filled turn may ever hold: the walk, and the three ops that bank into
#: tile state on the turn they are taken and need nothing carried.
FILL_OPS = MOVES + (O.OP_WATER, O.OP_DIG, O.OP_COLLECT_FERT)


#: Both fixtures pin `ROUTE_SPLIT_ON` off. The digest below is the pre-split
#: planner's, and `_tail_board` is arithmetic on a farmer that starts at
#: `ROUTE_BASE`: with the split start it reaches one tile further and the
#: two-turn tail the board exists to produce closes up.
#: `test_on_leaves_every_turn_the_route_owns_alone_under_route_split` runs the
#: filler's one invariant against the shipped default instead.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


def _worked(unit_op, u):
    """Tiles unit `u` takes a tile op on, walked off its emitted moves from its
    own spawn tile -- so this is the route the engine will really execute."""
    x, y = int(P.SPAWN_X[u]), int(P.SPAWN_Y[u])
    out = []
    for op in np.asarray(unit_op)[u].tolist():
        if op == O.OP_NORTH:
            y -= 1
        elif op == O.OP_SOUTH:
            y += 1
        elif op == O.OP_EAST:
            x += 1
        elif op == O.OP_WEST:
            x -= 1
        elif op not in (O.OP_PASS, O.OP_PICKUP):
            out.append(int(np.flatnonzero((P.SERP_X == x) & (P.SERP_Y == y))[0]))
    return out


def _busy(plan):
    return int((np.asarray(plan[0]) != O.OP_PASS).sum())


#: Twenty-two ripe *and* thirsty tomatoes packed into the serpentine's first
#: tiles, and a purse for a hand or two. Each tile is a three-turn stop (a step,
#: a WATER, a HARVEST), which is what puts a two-turn tail on a block: the cut
#: takes the last stop that fits and the next one is a turn too dear. The tiles
#: past `n_admit` are unwatered plants one step from where a block ends, which
#: is the census's median case (a free task 1.0 tiles away, 2.5 turns of day
#: left).
def _tail_board(n=22, money=3_000, day=10):
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    kind[:n], occ[:n], t_yield[:n] = spec.KIND_PLANT, spec.I_TOMATO, 6
    t_cons[:n] = 1                                   # dry: it weeds tonight
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=np.zeros(spec.N_ITEMS, np.int32),
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(money),
        nquad=np.int32(4),
        price=np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32),
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


# =========================================================================
# OFF: byte-identical to the planner the switch was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """Pinned on `test_route_early`'s digests: OFF this is that planner."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_passes_the_tail(off):
    """The behaviour the switch exists to change: a unit on the board below
    ends its block with turns of day left and spends every one of them on
    PASS."""
    unit_op = np.asarray(_plan(_tail_board(), _macro())[0])
    live = [u for u in range(spec.MAX_UNITS) if (unit_op[u] != O.OP_PASS).any()]
    tails = [P.TPD - 1 - int(np.nonzero(unit_op[u] != O.OP_PASS)[0].max()) for u in live]
    assert max(tails) >= 2, tails


# =========================================================================
# ON: the tail works, and nothing else moves
# =========================================================================

def test_on_fills_the_tail_with_a_reachable_task(on, monkeypatch):
    """The census case: the block ends, an unwatered plant is one tile away,
    and the turn that used to PASS waters it."""
    view, macro = _tail_board(), _macro()
    plan = _plan(view, macro)
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    base = _plan(view, macro)

    on_op = np.asarray(plan[0])
    off_op = np.asarray(base[0])
    filled = np.argwhere((off_op == O.OP_PASS) & (on_op != O.OP_PASS))
    assert len(filled), "the tail was not filled"
    got = [int(on_op[u, t]) for u, t in filled]
    assert O.OP_WATER in got, got
    for op in got:
        assert op in FILL_OPS, op


def test_on_leaves_every_turn_the_route_owns_alone(on, monkeypatch):
    """The filler writes into PASS turns and nowhere else: it changes no
    admission, no block cut and no market row, so every op the day already had
    is on the same turn, for the same unit, with the same argument."""
    for s in PIN_SEEDS + (100, 101):
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "TAIL_FILL_ON", False)
        base = _plan(view, macro)
        monkeypatch.setattr(P, "TAIL_FILL_ON", True)
        got = _plan(view, macro)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):                       # unit_op, unit_a, unit_q
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        for k in (3, 4, 5):                      # mkt_op, mkt_a, mkt_q
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (s, k)


def test_on_leaves_every_turn_the_route_owns_alone_under_route_split(monkeypatch):
    """The same invariant against the shipped default: the two switches share
    `_routes` but not a single expression, so the filler still only ever writes
    into a turn the split-start route left as PASS."""
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", True)
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "TAIL_FILL_ON", False)
        base = _plan(view, macro)
        monkeypatch.setattr(P, "TAIL_FILL_ON", True)
        got = _plan(view, macro)
        keep = np.asarray(base[0]) != O.OP_PASS
        for k in range(3):
            assert np.array_equal(np.asarray(base[k])[keep],
                                  np.asarray(got[k])[keep]), (s, k)
        for k in (3, 4, 5):
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (s, k)


def test_on_only_ever_fills_with_a_carry_free_op(on, monkeypatch):
    """Nothing that needs a purchase, and no HARVEST: a harvest lands in the
    unit's inventory, which the day's sale cannot draw on."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "TAIL_FILL_ON", False)
        base = np.asarray(_plan(view, macro)[0])
        monkeypatch.setattr(P, "TAIL_FILL_ON", True)
        got = np.asarray(_plan(view, macro)[0])
        for u, t in np.argwhere((base == O.OP_PASS) & (got != O.OP_PASS)):
            assert int(got[u, t]) in FILL_OPS, (s, u, t, int(got[u, t]))


def test_on_never_lets_two_units_work_the_same_tile(on):
    """Blocks are disjoint rank ranges and a filled tile is struck off for
    every later unit, so no tile is ever worked by two units -- which is the
    one way a filler could cost the day a turn instead of buying one."""
    for s in PIN_SEEDS + (100, 101):
        plan = _plan(*_seeded_case(s))
        seen = {}
        for u in range(spec.MAX_UNITS):
            for tile in set(_worked(plan[0], u)):
                assert seen.setdefault(tile, u) == u, (s, tile, u, seen[tile])


def test_on_never_fills_a_drop_day(on, monkeypatch):
    """A DROP day's tail is the walk home plus the DROP, measured from the
    block's last tile -- the filler would walk the unit off it."""
    for day in (O.LAST_SHED_DAY, O.LAST_SHED_DAY + 1):
        view, macro = _view(day=day, n_ripe=24, yld=6, money=8_000), _macro()
        monkeypatch.setattr(P, "TAIL_FILL_ON", False)
        base = _plan(view, macro)
        monkeypatch.setattr(P, "TAIL_FILL_ON", True)
        got = _plan(view, macro)
        if not P.DROP_ON:
            pytest.skip("DROP_ON is off")
        for k in range(3):
            assert np.array_equal(np.asarray(base[k]), np.asarray(got[k])), (day, k)


def test_on_actually_buys_turns_on_the_seeded_boards(on, monkeypatch):
    """A filler that never fires would make every assertion above vacuous."""
    gained = 0
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "TAIL_FILL_ON", False)
        base = _busy(_plan(view, macro))
        monkeypatch.setattr(P, "TAIL_FILL_ON", True)
        gained += _busy(_plan(view, macro)) - base
    assert gained > 0, gained


def test_the_filled_plan_agrees_across_backends(on):
    """An argmin over a distance key, a hop loop and a running struck-off mask:
    the equivalence surface is the plan."""
    import jax
    import jax.numpy as jnp
    cases = [_seeded_case(s) for s in PIN_SEEDS]
    cases += [(_tail_board(), _macro()),
              (_view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000),
               _macro()),
              (_view(day=O.LAST_SHED_DAY + 1, n_ripe=20, yld=6), _macro())]
    for view, macro in cases:
        a = P.build_day(np, view, macro)
        b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                        jax.tree_util.tree_map(jnp.asarray, macro),
                        jnp.asarray(spec.build_price_table()))
        for x, y in zip(a, b):
            assert np.array_equal(np.asarray(x), np.asarray(y)), f"day {int(view.day)}"


#: `plan.EARLY_SELL_ON` went on by default on 2026-09-03: the day's first lot
#: rides turn 1 behind the BUY row instead of standing on `O.SELL_TURNS[0]`.
#: It is pinned off for this file the way `a838700`'s stack was pinned off for
#: the digest fixtures -- the pins and worked examples below are the plan
#: *before* it, and what this file is about (the idle tail) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.BANK_BEFORE_LOT_ON` went on by default beside this file's switch on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). It is
#: pinned off here for the same reason the four switches in the `on`/`off`
#: fixtures are, and for one of its own: the PIN digests above predate it, and
#: `_worked` counts `OP_DROP` as working the tile the unit stands on. The
#: excursion banks into the shed from a *farm* tile, which another unit's
#: block may legitimately own -- on seed 1 unit 4 DROPs on tile 44 at turn 10
#: while unit 7 DIGs, PLANTs and WATERs it -- so
#: `test_on_never_lets_two_units_work_the_same_tile` reads a collision that
#: exists with the filler OFF as well and is therefore not the filler's.
#: `tests/test_bank_before_lot.py` owns the excursion.
@pytest.fixture(autouse=True)
def _bank_before_lot_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)


#: Three more switches went on by default AFTER the `a838700` digests above
#: were taken, and all three move the market rows the pin hashes: `HIRE_ROW_ON`
#: (`b1bde4f`), `LOT4_ON` with `LOT4_TURN = 17`
#: (`docs/strategy/2026-09-16-lot4.md`, POOLED180 +791 t 13.19, sub 56276165)
#: and `SELL_SLOT_PRIORITY_ON` (`docs/strategy/2026-09-16-slotprio.md`, +459
#: t 7.31 on the lot-4 combo, sub 56277270). They are pinned off here exactly
#: as `EARLY_SELL_ON` and the tail pair above are: with the three stated off,
#: this tree reproduces the `a838700` digests byte for byte (measured,
#: TESTFIX3 2026-09-17), so the pin keeps its meaning -- "OFF, this file's
#: switch leaves the planner it was cut into alone" -- instead of silently
#: becoming a hash of three later ships. `tests/test_lot4.py` and
#: `tests/test_slotprio.py` own those.
@pytest.fixture(autouse=True)
def _later_market_ships_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "HIRE_ROW_ON", False)
    monkeypatch.setattr(P, "LOT4_ON", False)
    monkeypatch.setattr(P, "SELL_SLOT_PRIORITY_ON", False)
