"""The day's route crosses the worked span once (PLANNER_V3_1 1.6, R1).

`_plan_and_stats` used to build the route order as
`d.tier * 2 + (d.tile_value > 0)` -- four groups, each swept in serpentine
order and concatenated. A group of *m* scattered tiles still spans the whole
board, so every populated group costs the crew another traversal: measured
over 32 real-engine games, 1.32 inter-tile moves per tile visited against a
single sweep's 1.00, 48.6% of the season's unit-turns spent walking, and an
admit estimate that no longer described the route it was admitting for. 305
plantings were queued over a season and 141 done.

Two groups now -- priced-or-mandatory, then worthless -- and 0.5's LAW moves
to admission, which already orders by the mandatory flag and only ever drops
from the value tail. The one thing the route still owes the LAW is that a
mandatory tile can never be *worth nothing*, or it would fall into the last
group with the weed digs; `_derive` floors `tile_value` at `tier` for that.

Measured on the champion over 16 paired games per matchup: +13,061 +- 7,932
coins against `starter`, +11,212 +- 9,228 against `kagg2`, inter-tile moves
per visit 1.32 -> 1.00, and `value_dropped` 21,302 -> 5,303 a season.
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
from test_admit_route import TABLE, _farm, _ripe, _thirsty
from test_budget_order import _macro
from test_mandatory_tier import _board, _weeds_head

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3.core import valuation as V  # `pay_day()` reads `P`'s horizon switch

MOVES = (O.OP_NORTH, O.OP_SOUTH, O.OP_EAST, O.OP_WEST)


def _visits(unit_op):
    """Sweep positions the farmer works, in the order it works them.

    Read off the route by walking the emitted moves from the spawn tile, so
    this is the route the engine will really execute and not a second model of
    it."""
    x, y = int(spec.SHED_ACCESS_XY[0, 0]), int(spec.SHED_ACCESS_XY[0, 1])
    seen = []
    for op in unit_op.tolist():
        if op == O.OP_NORTH:
            y -= 1
        elif op == O.OP_SOUTH:
            y += 1
        elif op == O.OP_EAST:
            x += 1
        elif op == O.OP_WEST:
            x -= 1
        elif op != O.OP_PASS:
            pos = int(np.flatnonzero((P.SERP_X == x) & (P.SERP_Y == y))[0])
            if not seen or seen[-1] != pos:
                seen.append(pos)
    return seen


def _mixed_board():
    """Three priced tiles and two worthless digs, packed tightly enough that
    the farmer's 22 route turns reach all five.

    44 is the spawn tile itself and 45..48 walk east along row 4. The
    *mandatory* tile is 46 -- the last of the three priced ones -- which is
    exactly the tile the four-group route used to cross the board for first.
    Nothing is planted today, so a dig is worth nothing."""
    tiles = {44: _ripe(spec.I_TOMATO, 4), 45: _ripe(spec.I_TOMATO, 4),
             46: _thirsty(spec.I_TOMATO),
             47: {"kind": spec.KIND_WEED}, 48: {"kind": spec.KIND_WEED}}
    return _farm(tiles)


def test_the_route_has_two_groups_not_four():
    """Every priced-or-mandatory tile is visited before any worthless one, and
    the sweep position is non-decreasing inside each group -- one crossing.

    The exact route, one unit from the spawn (4, 4): harvest 44 in place (turn
    2), one step east and harvest 45 (turn 4), one step east and water 46 (turn
    6), then the two digs on turns 8 and 10. The mandatory watering is walked
    *third*, between two optional harvests, because the route no longer knows
    which tile is mandatory -- only which is priced.
    """
    view = _mixed_board()
    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    priced = {p for p in range(P.N_T) if bool(d.task[p]) and int(d.tile_value[p]) > 0}
    worthless = {p for p in range(P.N_T) if bool(d.task[p]) and int(d.tile_value[p]) == 0}
    assert priced == {44, 45, 46} and worthless == {47, 48}
    # Tier 2 under `SURVIVAL_WATER_ON` (default since 2026-09-03): the tomato
    # can still sell, so its survival watering sits above the rest of the
    # mandatory tier. What this test is about -- that the *route* knows only
    # priced from worthless, and walks the watering third -- is unchanged.
    assert int(d.tier[46]) == 2                      # ... and it is the mandatory one

    order = _visits(P.build_day(np, view, _macro(), TABLE)[0][0])
    assert order == [44, 45, 46, 47, 48]
    # non-decreasing inside each group is the "one crossing" property; the two
    # groups concatenated is the one traversal the LAW's last group still costs
    head = [p for p in order if p in priced]
    tail = [p for p in order if p in worthless]
    assert head == sorted(head) and tail == sorted(tail)
    assert order == head + tail


def test_the_route_order_carries_no_tier():
    """`route_tier` is `(tile_value > 0)` and nothing else.

    Pinned directly, because it is a one-expression change that a later edit
    could quietly widen back to four groups without breaking a board test."""
    d = P._derive(np, _mixed_board(), _macro(), TABLE, np.int32(0), False, np.int32(0))
    route_tier = (d.tile_value > 0).astype(np.int32)
    assert set(np.unique(route_tier).tolist()) <= {0, 1}
    assert route_tier[46] == 1 and route_tier[47] == 0


def _random_view(rng, day):
    """A board of random kinds and tile state -- most of them nonsense, which
    is the point: the floor has to hold on every reachable `_derive` input."""
    z = np.zeros(P.N_T, np.int32)
    kind = rng.integers(0, 5, P.N_T).astype(np.int32)
    occ = rng.integers(-1, 5, P.N_T).astype(np.int32)
    shed = rng.integers(0, 30, spec.N_ITEMS).astype(np.int32)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ,
        t_day=rng.integers(0, day + 1, P.N_T).astype(np.int32),
        t_water=rng.integers(0, 2, P.N_T).astype(np.int32),
        t_cons=rng.integers(0, 2, P.N_T).astype(np.int32),
        t_yield=rng.integers(0, 6, P.N_T).astype(np.int32),
        t_fert=z - 1, t_cared=rng.integers(0, 2, P.N_T).astype(np.int32),
        t_favail=rng.integers(0, 2, P.N_T).astype(np.int32),
        shed=shed, seeds=rng.integers(0, 5, spec.N_CROPS).astype(np.int32),
        money=np.int32(int(rng.integers(0, 20_000))), nquad=np.int32(4),
        price=rng.integers(1, 300, spec.N_PRODUCTS).astype(np.int32))


def test_a_mandatory_tile_is_never_worth_nothing():
    """`d.tile_value >= 1` wherever `d.tier > 0`, over 200 random views.

    This is the whole of what the route still owes 0.5: the last group is the
    work that is worth nothing, and a survival watering on a crop whose stream
    has run out must not fall into it.

    It used to read `tile_value >= tier`, which was the same statement while
    the tier was the 0/1 mandatory flag. `SURVIVAL_WATER_ON` (default since
    2026-09-03) adds a tier 2 for the survival watering that must not be cut,
    and the floor it pays is `min(tier, 1)` -- one coin, deliberately, because
    the floor decides the route *group* and nothing else. So the invariant is
    restated as the group membership it always meant: no tile the mandatory
    tier holds may land in the worthless group."""
    rng = np.random.default_rng(20260826)
    macro = _macro(plant_target=np.array([2, 1, 1, 0, 0], np.int32),
                   animal_want=np.array([1, 1, 0], np.int32))
    for i in range(200):
        view = _random_view(rng, day=int(rng.integers(0, spec.N_DAYS)))
        d = P._derive(np, view, macro, TABLE, np.int32(0), False, np.int32(0))
        tv, tier = np.asarray(d.tile_value), np.asarray(d.tier)
        assert tier.max() > 0, i          # the boards do carry mandatory work
        assert bool(np.all(tv[tier > 0] >= 1)), i


def test_the_floor_is_one_coin_and_only_one(monkeypatch):
    """It decides the group and nothing else: ordering *inside* a group is
    serpentine, so a bigger floor would buy nothing and would start competing
    with real coins in the admission order.

    `SURVIVAL_WATER_ON` off, and the board is why: its subject is a thirsty
    tile whose fires are spent -- the one case where the floor is the only
    thing standing between a mandatory watering and the worthless group. That
    is exactly the tile the switch (default since 2026-09-03) takes out of
    `must_water` altogether, so on the shipped default this board has no
    mandatory tile at all and the floor has no subject. What the floor still
    is -- one coin, `min(tier, 1)` -- is pinned on the shipped default by
    `test_a_mandatory_tile_is_never_worth_nothing` above."""
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    kind = _weeds_head()
    kind[98] = kind[99] = spec.KIND_PLANT
    occ = np.full(P.N_T, -1, np.int32)
    occ[98] = occ[99] = spec.I_TOMATO
    t_cons = np.zeros(P.N_T, np.int32)
    t_cons[98] = 1                          # thirsty, and its fires are spent
    t_yield = np.zeros(P.N_T, np.int32)
    t_yield[99] = 1
    view = _board(kind, day=13, occ=occ, t_cons=t_cons, t_yield=t_yield)
    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    assert int(d.tier[98]) == 1 and int(d.tile_value[98]) == 1


def test_the_forty_weed_boards_still_work_the_mandatory_tile():
    """The three adversarial boards of `test_mandatory_tier.py`, through
    `build_day`: 40 worthless digs at the head of the sweep and the one tile
    that matters at position 99, nine moves from the spawn.

    They pass because the mandatory tile is *priced* -- either by its own
    stream or by the one-coin floor -- and the worthless group still sweeps
    last."""
    for op_code, extra in ((O.OP_WATER, "water"), (O.OP_FEED, "feed"),
                           (O.OP_HARVEST, "harvest")):
        kind = _weeds_head()
        occ = np.full(P.N_T, -1, np.int32)
        t_cons = np.zeros(P.N_T, np.int32)
        t_day = np.zeros(P.N_T, np.int32)
        t_yield = np.zeros(P.N_T, np.int32)
        shed = np.zeros(spec.N_ITEMS, np.int32)
        day = 5
        if extra == "water":
            kind[99], occ[99], t_cons[99] = spec.KIND_PLANT, spec.I_TOMATO, 1
        elif extra == "feed":
            kind[99], occ[99], t_cons[99] = spec.KIND_COOP, 0, 1
            shed[spec.I_WHEAT] = 1
        else:
            # A one-time crop is mandatory on the day it reaches `harvest_age`
            # = `clip(valuation.pay_day() - t_day, first, saturate)`, and
            # `plan.HORIZON_DROP_ON` (5b0fcc4) moved that pay day from 28 to
            # 29: wheat planted on 25 no longer harvests on 28, it waters and
            # waits. Written off the switch instead of re-pinned, and one day
            # *short* of the pay day, because the pay day itself is a DROP day
            # whose route owes the walk home and tile 99 is eight moves from
            # the nearest shed access -- too far to reach and bank, the same
            # reachability `test_deadline_harvest.py` moves its tile for. Aged
            # to saturation (`day - 4`) so the harvest is mandatory on both
            # settings of the switch.
            kind[99], occ[99] = spec.KIND_PLANT, spec.I_WHEAT
            day = int(V.pay_day()) - 1
            t_day[99], t_yield[99] = day - 4, 3
        view = _board(kind, day=day, occ=occ, t_day=t_day, t_cons=t_cons,
                      t_yield=t_yield, shed=shed)
        unit_op = P.build_day(np, view, _macro())[0]
        assert int((unit_op[0] == op_code).sum()) == 1, extra


def test_the_admit_loop_converges_when_the_estimate_over_admits(monkeypatch):
    """On the undershoot board the exact route cannot reach everything the
    estimate admitted, and `ADMIT_ROUNDS` closes the gap: `admitted & ~covered`
    is empty at the end, so `value_dropped` is exactly the tile admission gave
    up and nothing is left standing at the labour boundary.

    (It does not converge on every board -- `test_day_stats.py` pins one where
    it cannot, because the route drops from its own tail while re-admission
    drops from the value tail. That residue is what section 7's metric is
    for.)"""
    # `ROUTE_SPLIT_ON` off: `undershoot_board` is built so the exact route
    # misses by exactly one turn (23 needed against 22), and the split start
    # hands the farmer that turn -- there is no undershoot left to converge on.
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    from test_admit_route import undershoot_board
    stats = P.build_day_stats(undershoot_board(), _macro(), TABLE)
    # one 720-coin strawberry admission gave up, and no route residue on top
    assert int(stats.value_dropped) == 720


def test_route_arrays_agree_across_backends():
    import jax
    import jax.numpy as jnp
    tiles = {p: _ripe(spec.I_MELON, 6) for p in range(0, 60, 3)}
    tiles.update({p: {"kind": spec.KIND_WEED} for p in range(1, 60, 3)})
    tiles[99] = _thirsty(spec.I_TOMATO)
    view, macro = _farm(tiles), _macro()
    a = P.build_day(np, view, macro, TABLE)
    b = P.build_day(jnp, jax.tree_util.tree_map(jnp.asarray, view),
                    jax.tree_util.tree_map(jnp.asarray, macro), jnp.asarray(TABLE))
    for x, y in zip(a, b):
        np.testing.assert_array_equal(np.asarray(x), np.asarray(y))
