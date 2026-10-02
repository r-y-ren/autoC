"""Labour ordering is tiered (PLANNER_V3_1 sections 0.5 and 1.6). `build_day`
admits tiles by (mandatory tier, value) and then routes the admitted set in
**two** route groups -- priced-or-mandatory work, then the work that is worth
nothing -- each swept in serpentine order within itself.

The mandatory group went away on 2026-08-26 (the one-crossing route): a group
of scattered tiles spans the whole board however few of them there are, so
every populated group cost the crew another traversal, and four of them cost
1.32 inter-tile moves per visit against a single sweep's 1.00. Work that is
lost for good if skipped today (survival waterings, survival feeds, deadline
harvests) is still admitted ahead of every optional tile and is still never
the tile re-admission drops -- and it still leads the route on every board
below, because `_derive` floors a mandatory tile's value at one coin, which is
enough to put it in the priced group ahead of every worthless dig. What it no
longer gets is a crossing of its own ahead of the priced work.

Every tier is compared lexicographically against the value key, never packed
into the int32 key.
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


@pytest.fixture
def pre_split(monkeypatch):
    """The pre-switch planner the turn arithmetic below is a worked example of.

    `SURVIVAL_WATER_ON` (default since 0c8bee8) is the load-bearing pin: it
    stops watering a crop whose remaining stream prices at zero, and the
    thirsty tomato that board hangs at 98 is exactly that tile -- with the
    switch on it is not mandatory, not priced by the one-coin floor and not
    watered at all, so the board no longer has the mandatory-beside-priced
    pair it was built to show.

    `ROUTE_SPLIT_ON` (default since 1d03376) goes with it because the turns
    themselves are the worked example: the split start opens the block one
    turn earlier, which moves every op below by one *and* buys a second dig
    the 22-turn budget was written to just miss.
    """
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


def _board(kind, day=5, shed=None, **tiles):
    """The purse is 0, so 1.5's enumeration hires nobody: every route below is
    the farmer's own 22 turns, and the turn arithmetic in each comment assumes
    exactly that one unit."""
    z = np.zeros(100, np.int32)
    t = {"occ": z - 1, "t_day": z.copy(), "t_water": z.copy(), "t_cons": z.copy(),
         "t_yield": z.copy(), "t_fert": z - 1, "t_cared": z.copy(), "t_favail": z.copy()}
    t.update(tiles)
    return P.DayView(
        day=np.int32(day), kind=kind, **t,
        shed=np.zeros(spec.N_ITEMS, np.int32) if shed is None else shed,
        seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4),
        price=np.full(spec.N_PRODUCTS, 25, np.int32))


def _weeds_head():
    """40 weeds filling the head of the sweep. Nothing is planted today, so a
    dig is worth nothing and the weeds land in the *last* of the two route
    groups [1.6]: one unit's 22 route turns reach only the two or three nearest
    of them, and only after everything that is worth anything. Every board
    below hangs its one interesting tile at the tail (position 99, tile (0, 9),
    nine moves from the farmer's spawn tile (4, 4)) -- unreachable if the
    worthless digs went first, which is what they used to do.

    Since the one-crossing route the interesting tile leads because it is
    *priced*, not because it is mandatory: `_derive` floors a mandatory tile at
    one coin so a survival watering on a spent crop cannot fall in with the
    digs."""
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    kind[:40] = spec.KIND_WEED
    return kind


def test_a_survival_watering_leads_the_route():
    # The watering is mandatory [0.5] and, on this board, worth nothing: the
    # tomato's fires are spent, so only the tier lifts it over the digs.
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_TOMATO                    # ongoing crop, no harvest yet
    t_cons = np.zeros(100, np.int32)
    t_cons[99] = 1                             # weeds tonight unless watered
    unit_op = P.build_day(np, _board(kind, occ=occ, t_cons=t_cons), _macro())[0]
    assert (unit_op[0] == O.OP_WATER).sum() == 1


def test_a_survival_feed_leads_the_route():
    # A feed that saves an animal is mandatory [0.5], so it is routed before
    # the weeds whatever the two are worth.
    kind = _weeds_head()
    kind[99] = spec.KIND_COOP
    occ = np.full(100, -1, np.int32)
    occ[99] = 0                                # a goose
    t_cons = np.zeros(100, np.int32)
    t_cons[99] = 1                             # unfed yesterday: escapes tonight
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 1
    unit_op = P.build_day(np, _board(kind, occ=occ, t_cons=t_cons, shed=shed),
                          _macro())[0]
    assert (unit_op[0] == O.OP_FEED).sum() == 1


def test_a_deadline_harvest_leads_the_route():
    # Day 28: the harvest is lost for good if skipped, so it is mandatory
    # [0.5] and heads the sweep.
    #
    # The wheat is the one that *saturates* today (age 4 =
    # `CROP_SATURATE_AGE`), not the day-25 one this board used to build:
    # `_derive` harvests a one-time crop at `clip(pay_day() - t_day, first,
    # sat)`, and `HORIZON_DROP_ON` -- default since 5b0fcc4 -- moved
    # `pay_day()` from 28 to 29, so a day-25 wheat now waits for its fourth
    # unit on day 29 and today's board has no harvest on it at all. A
    # saturated wheat is the deadline under either horizon, which is the
    # premise the test was written on.
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_WHEAT
    t_day = np.zeros(100, np.int32)
    t_day[99] = 28 - int(spec.CROP_SATURATE_AGE[spec.I_WHEAT])
    t_yield = np.zeros(100, np.int32)
    t_yield[99] = 3
    unit_op = P.build_day(np, _board(kind, day=28, occ=occ, t_day=t_day, t_yield=t_yield),
                          _macro())[0]
    assert (unit_op[0] == O.OP_HARVEST).sum() == 1


def test_a_plain_harvest_is_optional_and_still_leads_the_weeds():
    # An ongoing crop's harvest on day 13 can wait, so it is *not* mandatory --
    # but it is priced (one tomato unit at the fixture's flat 25 coins), and a
    # priced tile is routed ahead of every worthless dig [1.6]. It used to tie
    # the weeds on (tier, serpentine) and lose the whole budget to them.
    #
    # The route, one unit and 22 turns: spawn (4, 4) -> 99 at (0, 9) is 4 + 5 =
    # 9 moves + 1 harvest = 10 turns; back to weed 0 at (0, 0) is 9 moves + 1
    # dig = 10 more (20); weed 1 at (1, 0) is 1 move + 1 dig = 2 more (22, and
    # it exactly fits); weed 2 would need 2 more and does not.
    kind = _weeds_head()
    kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[99] = spec.I_TOMATO
    t_yield = np.zeros(100, np.int32)
    t_yield[99] = 1
    unit_op = P.build_day(np, _board(kind, day=13, occ=occ, t_yield=t_yield),
                          _macro())[0]
    assert (unit_op[0] == O.OP_HARVEST).sum() == 1
    assert (unit_op[0] == O.OP_DIG).sum() == 2


def test_mandatory_work_still_leads_the_priced_work_it_now_shares_a_board_with(pre_split):
    # 40 worthless weeds, a thirsty tomato at 98 (mandatory, and worth nothing
    # on its own -- its fires are spent, so only `_derive`'s one-coin floor
    # prices it) and a ripe tomato at 99 (optional, worth 25). Both land in
    # route group 1 and sweep in serpentine order; the weeds are group 0.
    # 98 comes first because it is the earlier sweep position, not because it
    # is mandatory -- and that is the point: the floor is what keeps a spent
    # survival watering out of the worthless group.
    #
    # spawn (4, 4) -> 98 at (1, 9) is 3 + 5 = 8 moves + 1 water = 9 turns, so
    # the watering lands on turn 2 + 8 = 10; one step west + 1 harvest puts the
    # harvest on turn 12; the first weed then costs 9 moves + 1 dig and lands
    # on turn 22, and the second does not fit.
    kind = _weeds_head()
    kind[98] = kind[99] = spec.KIND_PLANT
    occ = np.full(100, -1, np.int32)
    occ[98] = occ[99] = spec.I_TOMATO
    t_cons = np.zeros(100, np.int32)
    t_cons[98] = 1                             # weeds tonight unless watered
    t_yield = np.zeros(100, np.int32)
    t_yield[99] = 1
    unit_op = P.build_day(np, _board(kind, day=13, occ=occ, t_cons=t_cons,
                                     t_yield=t_yield), _macro())[0]
    assert [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_WATER)] == [10]
    assert [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_HARVEST)] == [12]
    assert [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_DIG)] == [22]


def test_a_higher_tier_beats_the_score_in_task_order():
    task = np.zeros(100, bool)
    task[[10, 20, 30]] = True
    score = np.zeros(100, np.int32)
    score[10], score[20] = 1000, 500
    tier = np.zeros(100, np.int32)
    tier[30] = 1
    order = P.task_order(np, task, score, tier)
    assert list(order[:3]) == [30, 10, 20]
    assert sorted(order.tolist()) == list(range(100))


def test_score_still_orders_within_a_tier():
    task = np.zeros(100, bool)
    task[[10, 20]] = True
    score = np.zeros(100, np.int32)
    score[20] = 5
    tier = np.ones(100, np.int32)
    assert list(P.task_order(np, task, score, tier)[:2]) == [20, 10]


def test_no_tier_equals_zero_tier():
    # The pre-tier ordering itself is still pinned by test_task_priority.py's
    # task_order tests, which call it without a tier.
    rng = np.random.default_rng(3)
    task = rng.random(100) < 0.6
    score = rng.integers(-5, 6, size=100).astype(np.int32)
    assert P.task_order(np, task, score).tolist() == \
        P.task_order(np, task, score, np.zeros(100, np.int32)).tolist()


def test_task_order_with_tier_agrees_across_backends():
    import jax.numpy as jnp
    rng = np.random.default_rng(1)
    for _ in range(20):
        task = rng.random(100) < 0.6
        score = rng.integers(-5, 6, size=100).astype(np.int32)
        # 0..3: the admit stage and the route stage both pass 0/1 today, and
        # `task_order` packs neither into the key. Swept wider than either
        # caller needs on purpose -- the LAW is that any int32 tier works.
        tier = rng.integers(0, 4, size=100).astype(np.int32)
        a = P.task_order(np, task, score, tier)
        b = np.asarray(P.task_order(jnp, jnp.asarray(task), jnp.asarray(score), jnp.asarray(tier)))
        assert a.tolist() == b.tolist()
