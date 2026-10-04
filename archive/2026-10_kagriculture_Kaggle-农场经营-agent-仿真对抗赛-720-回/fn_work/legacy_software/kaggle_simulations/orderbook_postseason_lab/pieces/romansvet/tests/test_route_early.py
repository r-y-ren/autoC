"""`plan.ROUTE_EARLY_ON`: start the blocks the BUY row does not hold.

The same 390 idle unit-turns `PRESTOCK` was written for, from the other side.
`route_base` is 2 because a block whose first act is a PICKUP has to wait for
the row that resolves in turn 1's market phase -- but that is a property of the
*block*, not of the day, and a block that picks nothing up owes the row
nothing. Under the switch such a unit steps out of the shed at `O.TURN_BUY`
while the purchase is still pending, and keeps its last turn as well; the
blocks that do owe the row wait exactly as they always did.

Nothing in the market moves. The BUY row, both hire rows and the three SELL
lots are derived before the route is cut and read nothing the switch touches,
so ON and OFF emit the same three market arrays for the same board -- which is
the half `PRESTOCK` could not claim and the half its real-engine rejection was
about.

The `test_off_*` half is the identity half: off, `route_early` is `None`,
`_routes` compiles none of the trial cut and every start and budget is the
expression it always was -- pinned below by a digest of the whole six-array
plan on boards generated from a fixed seed, taken off the tree at `a838700`,
the commit before this switch.
"""
from __future__ import annotations

import hashlib
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

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


#: The commit `PIN` was taken off: the planner this switch was cut into.
PRE_SWITCH = "a838700"

#: Every switch that ships ON today and **did not exist** at `PRE_SWITCH`
#: (`git show a838700:src/kagg3/core/plan.py`), pinned OFF in BOTH halves --
#: `tests/test_route_split.py`'s rule, in the same form. Without it the OFF
#: half asks `PRE_SWITCH` to reproduce a planner built out of a dozen later
#: switches (as of ship `09af88b`: `WIDE_PICK_ON` col 16 and
#: `WIDE_PICK_FREE_ON` col 17, both shipped ON, ride the very route this file
#: cuts and re-order the granted column's market rows), and the ON half prices
#: them too. This file's subject is which *turn* a pickup-free block starts on;
#: each name below is owned, ON and OFF, by its own test file.
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


#: Both fixtures pin `ROUTE_SPLIT_ON` off, and it is not tidiness: this file's
#: digests are the planner at `a838700`, and `ROUTE_SPLIT_ON` -- on by default
#: since 2026-09-03 -- supersedes this switch inside `_routes`, so the ON half
#: below only has a subject with the newer switch out of the way.
@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(P, "ROUTE_EARLY_ON", True)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


def _view(day=10, money=20_000, n_coop=0, n_ripe=0, wheat=0, fert=0, seeds=None,
          yld=4, nquad=1, weeds=0):
    """A board with `n_coop` hungry geese, then `n_ripe` ripe tomatoes, then
    `weeds` dig tiles, then empty land for whatever the macro wants planted."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy()
    t_yield = z.copy()
    kind[:n_coop] = spec.KIND_COOP
    occ[:n_coop] = 0                                   # geese, unfed yesterday
    t_cons[:n_coop] = 1
    hi = n_coop + n_ripe
    kind[n_coop:hi] = spec.KIND_PLANT
    occ[n_coop:hi] = spec.I_TOMATO
    t_yield[n_coop:hi] = yld
    kind[hi:hi + weeds] = spec.KIND_WEED
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = wheat
    shed[spec.I_FERT] = fert
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=z.copy(), t_water=z.copy(),
        t_cons=t_cons, t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32) if seeds is None
        else np.asarray(seeds, np.int32),
        money=np.int32(money), nquad=np.int32(nquad), price=BASE_PRICE,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32))


def _plan(view, macro=None):
    return tuple(np.asarray(a) for a in P.build_day(np, view, macro or _macro()))


def _row(plan, turn):
    """[(op, arg, qty)] of the live orders on one market turn."""
    op, arg, qty = plan[3:6]
    return [(int(op[turn, s]), int(arg[turn, s]), int(qty[turn, s]))
            for s in range(spec.MAX_MARKET_ORDERS) if int(op[turn, s]) != O.MO_NONE]


def _acting_units(plan, turn):
    """Indices of the units that do something other than PASS on `turn`."""
    unit_op = plan[0]
    return [u for u in range(spec.MAX_UNITS) if int(unit_op[u, turn]) != O.OP_PASS]


def _digest(plan):
    h = hashlib.sha256()
    for a in plan:
        h.update(np.ascontiguousarray(np.asarray(a, np.int32)).tobytes())
    return h.hexdigest()[:16]


# =========================================================================
# OFF: byte-identical to the planner this switch was cut into
# =========================================================================

#: Seeded boards the OFF plan is pinned on -- a spread of days, purses, herds,
#: ripe crops and plant targets, so the pin covers days that buy and days that
#: do not, wide crews and narrow ones.
def _seeded_case(seed):
    rng = np.random.default_rng(seed)
    board = dict(
        day=int(rng.integers(0, 30)),
        money=int(rng.integers(500, 40_000)),
        n_coop=int(rng.integers(0, 14)),
        n_ripe=int(rng.integers(0, 30)),
        wheat=int(rng.integers(0, 20)),
        fert=int(rng.integers(0, 10)),
        yld=int(rng.integers(1, 8)),
        weeds=int(rng.integers(0, 12)),
        nquad=int(rng.integers(1, 5)),
        seeds=rng.integers(0, 6, spec.N_CROPS).astype(np.int32),
    )
    # A small hire bias on purpose: at a few thousand coins a hand the
    # enumeration takes the whole of `MAX_HANDS` and every board comes out
    # wide, which is the one shape the switch is off for. The champion runs
    # six hands at day 10, so this is the crew the boards should be mixed
    # around.
    macro = _macro(plant_target=rng.integers(0, 6, spec.N_CROPS).astype(np.int32),
                   hire_bias=np.int32(rng.integers(0, 600)))
    return _view(**board), macro


PIN_SEEDS = tuple(range(12))

#: Digests of the whole six-array plan on `PIN_SEEDS`, taken off the tree at
#: `a838700` -- the commit before this switch -- so they pin the pre-switch
#: planner and not this file's own output. Regenerate only with a measured
#: reason to move the plan.
PIN = ("e086a25a8c18fb6f", "e4969a68e2c39cf7", "54aad3cc4ec6f095", "68dcf63855c995a1",
       "3b57f9afe04bae8b", "9561fdea3e750fe6", "7e4989ef1bdfb4c0", "e7a5b34a78155761",
       "4d5b2f1d9703477a", "3ad7fb5d772365a8", "456c9e7c429998c2", "d0e3e72a0febce2a")


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The switch's contract: OFF every expression re-evaluates to the one it
    replaced, so a theta trained before it decodes byte for byte."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_keeps_the_whole_crew_behind_the_route_base(off):
    """Turns 0 and 1 are the crew's, and off they are PASS for everybody."""
    for s in PIN_SEEDS:
        plan = _plan(*_seeded_case(s))
        assert _acting_units(plan, O.TURN_HIRE) == [], s
        assert _acting_units(plan, O.TURN_BUY) == [], s


# =========================================================================
# ON: the block that owes the row nothing walks; the ones that do, wait
# =========================================================================

def test_on_starts_the_blocks_that_owe_the_buy_row_nothing(on):
    """A day with a live BUY row and both kinds of block in it. The units whose
    blocks own the feeds pick up at `ROUTE_BASE` as always; the ones sweeping
    the ripe crops have nothing to pick up and step out of the shed at
    `TURN_BUY`, one turn into the pending purchase."""
    view = _view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000)
    plan = _plan(view, _macro())

    assert _row(plan, O.TURN_BUY) != [], "the board is meant to still be buying"
    early = _acting_units(plan, O.TURN_BUY)
    assert early, "no unit started early on a board built to have some"

    unit_op = plan[0]
    for u in early:
        # Turn 1 is a step out of the shed and nothing else: a unit that owes
        # a PICKUP, or whose first act is a tile op, is not allowed out here.
        assert int(unit_op[u, O.TURN_BUY]) in (O.OP_NORTH, O.OP_SOUTH,
                                               O.OP_EAST, O.OP_WEST), u
        assert O.OP_PICKUP not in [int(x) for x in unit_op[u]], u


def test_on_leaves_the_pickup_blocks_where_they_were(on):
    """The purchase-dependent half of the same day: every unit that PICKUPs
    does so at `ROUTE_BASE` or later, which is after the BUY row resolved."""
    view = _view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000)
    plan = _plan(view, _macro())
    unit_op = np.asarray(plan[0])
    picks = np.argwhere(unit_op == O.OP_PICKUP)
    assert len(picks), "the board is meant to pick something up"
    assert picks[:, 1].min() >= O.ROUTE_BASE


def test_on_never_moves_a_whole_crew_that_owes_the_row(on):
    """A day where every block owes a feed keeps today's law exactly."""
    view = _view(day=10, n_coop=12, wheat=0)
    plan = _plan(view, _macro())
    assert _row(plan, O.TURN_BUY) != []
    assert _acting_units(plan, O.TURN_BUY) == []


def test_on_never_moves_a_unit_before_the_overflow_hire_row(on):
    """A wide crew's second hire row is turn 2, and `_hire` spawns a hand on
    the least-occupied shed-access tile -- so one unit that walked at turn 1
    re-scatters every hand hired after it [LAW, `ops.ROUTE_BASE_WIDE`]. The
    switch is off for the whole crew on such a day."""
    macro = _macro(hire_bias=np.int32(3_000))
    view = _view(day=10, n_ripe=60, yld=6, money=200_000)
    plan = _plan(view, macro)
    n_hire = sum(1 for turn in O.HIRE_TURNS for op, _, _ in _row(plan, turn)
                 if op == O.MO_HIRE)
    if n_hire <= spec.MAX_MARKET_ORDERS:
        pytest.skip(f"board hired {n_hire} hands, not a wide crew")
    assert _acting_units(plan, O.TURN_BUY) == []
    assert _acting_units(plan, O.TURN_HIRE_WIDE) == []


def test_on_never_moves_a_unit_into_a_locked_quadrant(on):
    """BUY_LAND resolves in `SELL_TURNS[0]`'s market phase, after that turn's
    unit phase, and a tile op on a LOCKED tile silently no-ops [M2]. So a land
    day keeps the lead it always had: nothing but the shed-side PICKUPs happens
    before the quadrant exists."""
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
    """The whole reason this switch exists rather than `PRESTOCK`'s. The BUY
    row, both hire rows and the three SELL lots are derived before the route is
    cut and read nothing the switch touches, so not one order changes turn,
    slot, argument or quantity."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "ROUTE_EARLY_ON", False)
        base = _plan(view, macro)
        monkeypatch.setattr(P, "ROUTE_EARLY_ON", True)
        early = _plan(view, macro)
        for k in (3, 4, 5):                      # mkt_op, mkt_a, mkt_q
            assert np.array_equal(base[k], early[k]), (s, k)


def test_on_never_leaves_more_task_value_unworked(on, monkeypatch):
    """It buys labour and spends none. The metric is section 7's own -- queued
    task value the day's route does not reach -- and not the count of non-PASS
    turns: a crew that starts earlier also *re-cuts* its blocks, so it can do
    all the same work in two fewer walking turns, which is a gain that a turn
    count reads as a loss."""
    for s in PIN_SEEDS:
        view, macro = _seeded_case(s)
        monkeypatch.setattr(P, "ROUTE_EARLY_ON", False)
        base = int(P.build_day_stats(view, macro).value_dropped)
        monkeypatch.setattr(P, "ROUTE_EARLY_ON", True)
        got = int(P.build_day_stats(view, macro).value_dropped)
        assert got <= base, (s, base, got)


def test_on_actually_fires_on_the_seeded_boards(on):
    """The pin boards are the switch's own sample, so at least some of them
    have to reach it -- a spread that never fires would make every ON
    assertion above vacuous."""
    fired = [s for s in PIN_SEEDS if _acting_units(_plan(*_seeded_case(s)), O.TURN_BUY)]
    assert fired, "no seeded board started a unit early"


def test_the_early_start_plan_agrees_across_backends(on):
    """The per-unit start is a `where` over a per-unit vector where there used
    to be a scalar, and the trial cut is a second `_count_le` (a second masked
    `max` on a DROP day). The equivalence surface is the plan."""
    import jax
    import jax.numpy as jnp
    cases = [_seeded_case(s) for s in PIN_SEEDS]
    cases += [(_view(day=12, n_coop=5, n_ripe=22, wheat=0, yld=6, money=12_000),
               _macro()),
              (_view(day=O.LAST_SHED_DAY + 1, n_ripe=20, yld=6), _macro()),
              (_view(day=O.LAST_SHED_DAY, n_coop=6, wheat=6), _macro())]
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
#: *before* it, and what this file is about (which turn a unit's block starts on) is a question the switch does
#: not answer either way. `tests/test_early_sell.py` owns both halves of it.
@pytest.fixture(autouse=True)
def _early_sell_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "EARLY_SELL_ON", False)


#: `plan.TAIL_FILL_ON` and `plan.BANK_BEFORE_LOT_ON` went on by default on
#: 2026-09-09 (the tail pair, `docs/strategy/2026-09-10-ship-pair.md`). The
#: OFF digests in this file were taken before the pair existed and still mean
#: what they meant -- "OFF, this file's switch leaves the planner it was cut
#: into alone" -- so the pair is pinned off here the way `EARLY_SELL_ON` and
#: `OPEN_PUMP_ON` were pinned off before it (`854b86b`).
#: `tests/test_tail_fill.py` and `tests/test_bank_before_lot.py` own the two.
@pytest.fixture(autouse=True)
def _tail_pair_pinned_off(monkeypatch):
    monkeypatch.setattr(P, "TAIL_FILL_ON", False)
    monkeypatch.setattr(P, "BANK_BEFORE_LOT_ON", False)
