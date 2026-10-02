"""Labour is admitted by (tier, value) and routed by serpentine stripe
(PLANNER_V3_1 section 1.6): the most valuable work is done, and done in a
spatial sweep rather than in value order. The sweep runs in **two** route
groups -- priced-or-mandatory work, then work that is worth nothing -- so
zero-value work can never spend the turns a priced tile needs, and the crew
crosses the worked span once instead of up to four times.

The turn arithmetic every board below pins moved with that on 2026-08-26. A
tile is admitted at `n_ops + EST_MOVES = n_ops + 1` turns, because one
serpentine crossing really does cost one inter-tile move per visit (measured
0.97 over 32 real-engine games), and each unit's admit budget loses a further
`EST_LEAD = 5` for the walk out of the shed it pays every morning -- so the
farmer's own budget is 22 - pickups - 5, while its *route* still has all 22
turns. Admission got tighter on the lead and looser on the moves; both halves
are the same correction and neither is safe alone.
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
from kagg3.core import valuation as V

TABLE = spec.build_price_table()
BASE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)


@pytest.fixture
def pre_split(monkeypatch):
    """`ROUTE_SPLIT_ON` off, for the boards whose numbers *are* the budget.

    On by default since 2026-09-03, it starts a block the turn-1 BUY row does
    not feed at `TURN_BUY`, so the farmer routes 23 turns instead of 22. The
    sweep order and the admit loop are the same program either way -- the tests
    below that pin an order simply moved a turn earlier -- but a board built so
    that the exact route misses by exactly one turn has no undershoot left in
    it, and a worked example of `ADMIT_ROUNDS` has to be arithmetic on one
    budget. Those pin the budget they were computed for."""
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)


def _farm(tiles, day=13):
    """`tiles`: position -> {kind:, occ:, t_yield:, t_cons:, t_day:}.

    The purse is 0, so 1.5's enumeration can never afford a bill and every
    board below is a **one-unit day**: the farmer's own 22 route turns, less
    whatever pickup kinds the day wants [0.12]. Tests that need a hand set
    `money` themselves."""
    z = np.zeros(100, np.int32)
    kind = np.full(100, spec.KIND_EMPTY, np.int32)
    occ, t_yield, t_cons, t_day = z - 1, z.copy(), z.copy(), z.copy()
    for pos, t in tiles.items():
        kind[pos] = t["kind"]
        occ[pos] = t.get("occ", -1)
        t_yield[pos] = t.get("t_yield", 0)
        t_cons[pos] = t.get("t_cons", 0)
        t_day[pos] = t.get("t_day", 0)
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(), t_cons=t_cons,
        t_yield=t_yield, t_fert=z - 1, t_cared=z.copy(), t_favail=z.copy(),
        shed=np.zeros(spec.N_ITEMS, np.int32), seeds=np.zeros(spec.N_CROPS, np.int32),
        money=np.int32(0), nquad=np.int32(4), price=BASE.copy())


def _ripe(crop, units):
    return {"kind": spec.KIND_PLANT, "occ": crop, "t_yield": units}


def _thirsty(crop):
    """A crop that weeds tonight unless watered, planted late enough that it
    still has fires left -- so the watering is mandatory [0.5] *and* worth
    something. `crop_remaining_value` prices a day-0 tomato seen on day 13 at
    zero: its four fires (days 8..11) are spent."""
    return {"kind": spec.KIND_PLANT, "occ": crop, "t_day": 8, "t_cons": 1}


def test_admission_is_by_value_not_by_position():
    # Ten weeds at the head of the sweep -- worth nothing, no planting today
    # needs the ground -- and five ripe strawberries behind them (720 coins
    # each, and optional: an ongoing crop's harvest keeps). The fixed sweep dug
    # weeds for its whole budget and never harvested; admission by value plus a
    # route that sweeps priced work before worthless work takes all five.
    #
    # The route arithmetic, one unit and 22 route turns: the spawn is (4, 4),
    # tile 10 is (9, 1), so the first harvest costs 5 + 3 = 8 moves + 1 op = 9
    # turns. Tiles 11..14 walk one step west each, 2 turns apiece = 8 more, so
    # the five harvests take 17. The nearest weed is tile 0 at (0, 0), 5 + 1 = 6
    # moves + 1 dig = 7 more turns, and 17 + 7 = 24 does not fit in 22 -- so
    # five harvests and not one dig. (Admission lets three of the weeds in:
    # 8 tiles at 2 estimated turns fit the farmer's 22 - 0 - 5 = 17. They are
    # in the second route group and the sweep never reaches them.)
    tiles = {p: {"kind": spec.KIND_WEED} for p in range(10)}
    tiles.update({p: _ripe(spec.I_STRAWBERRY, 6) for p in range(10, 15)})
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    assert int((unit_op == O.OP_HARVEST).sum()) == 5
    assert int((unit_op == O.OP_DIG).sum()) == 0


def test_admitted_tiles_are_routed_in_serpentine_order():
    # values descend 55 > 53 > 46 = 45 > 44, but the route is the sweep
    # 44 (4,4: the spawn) -> 45 -> 46 -> 53 (6,5) -> 55 (4,5). The wheat on 44
    # is a deadline harvest, so it heads the order on the tier as well.
    # The turns are one earlier than they were before `ROUTE_SPLIT_ON`: this
    # block owes no PICKUP and opens with a HARVEST on the spawn tile, which
    # the turn-1 BUY row does not feed, so it starts at `TURN_BUY`. What the
    # test is about -- the *order* and the one-move gaps -- is unchanged.
    tiles = {55: _ripe(spec.I_TOMATO, 4), 53: _ripe(spec.I_TOMATO, 3), 46: _ripe(spec.I_TOMATO, 2),
             45: _ripe(spec.I_STRAWBERRY, 1), 44: _ripe(spec.I_WHEAT, 1)}
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    harvest_turns = [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_HARVEST)]
    assert harvest_turns == [1, 3, 5, 7, 10]


def test_mandatory_work_heads_the_admission_order_whatever_it_is_worth():
    """0.5's LAW lives in *admission* since the one-crossing route [1.6].

    Sixty ripe strawberries -- an ongoing crop's harvest keeps until tomorrow,
    so every one of them is optional -- and one thirsty tomato at the tail.
    The tomato leads `order_v` ahead of all sixty whatever the values say,
    which is what makes it a tile re-admission can never drop: `n_admit` only
    ever shrinks, and it shrinks from the value tail.

    What it no longer gets is a route crossing of its own. The route sweeps
    the priced group in serpentine order, the tomato sits at sweep position 99
    and the farmer's 22 turns run out around position 6, so on *this* board the
    watering is admitted and not walked. That is the deliberate trade of the
    one-crossing route, measured across 32 real-engine games: paying a whole
    board traversal to put mandatory work first cost 11,000-16,000 coins a
    season, while the work it protects is a fraction of that. The cost shows up
    where it should -- in `value_dropped` (`test_day_stats.py`) -- and the
    season-wide figure *fell* 75% under this change, because one crossing
    reaches 23% more tiles.
    """
    tiles = {p: _ripe(spec.I_STRAWBERRY, 6) for p in range(60)}
    tiles[99] = _thirsty(spec.I_TOMATO)
    view = _farm(tiles)
    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    # Tier 2, not 1: `SURVIVAL_WATER_ON` (default since 2026-09-03) ranks a
    # survival watering whose crop can still sell one tier above the rest of
    # the mandatory work. The tomato is exactly that tile, so the LAW this
    # test is about -- mandatory work heads admission whatever it is worth --
    # holds a rung higher than it did.
    assert int(d.tier[99]) == 2 and int(d.tier[:60].max()) == 0
    assert int(P.task_order(np, d.task, d.tile_value, d.tier)[0]) == 99
    unit_op = P.build_day(np, view, _macro(), TABLE)[0]
    assert int((unit_op == O.OP_HARVEST).sum()) > 0


def test_the_route_crosses_the_priced_group_once():
    # 45 and 46 hold ripe tomatoes and come first in the sweep; 99 is the
    # thirsty tile, and its watering is mandatory. All three are priced, so
    # all three share one route group and the sweep takes them in serpentine
    # order rather than crossing the board for the mandatory one first:
    # spawn (4, 4) -> 45 at (5, 4) is 1 move + 1 harvest (turn 2), -> 46 at
    # (6, 4) is 1 + 1 (turn 4), -> 99 at (0, 9) is 6 + 5 = 11 moves + 1 water
    # (turn 16). Every tile is still worked, in 16 route turns rather than the
    # 22 the mandatory-first crossing spent on the same three. The block owes
    # the BUY row nothing and walks first, so under `ROUTE_SPLIT_ON` it starts
    # at `TURN_BUY` and every turn here is one earlier than it was.
    tiles = {45: _ripe(spec.I_TOMATO, 4), 46: _ripe(spec.I_TOMATO, 4), 99: _thirsty(spec.I_TOMATO)}
    unit_op = P.build_day(np, _farm(tiles), _macro(), TABLE)[0]
    assert [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_WATER)] == [16]
    assert [int(t) for t in np.flatnonzero(unit_op[0] == O.OP_HARVEST)] == [2, 4]


def undershoot_board():
    """Three ripe strawberries on the far row (90..92) and a thirsty tomato at
    99. The estimate admits all four (4 x 2 = 8 <= 22 - 0 - 5), the exact route
    90 -> 91 -> 92 -> 99 needs 11 + 2 + 2 + 8 = 23 > 22 turns, and
    re-admission drops one strawberry from the value tail -- never the
    watering [0.5] -- after which 90 -> 91 -> 99 fits in exactly 22.

    Public (no leading underscore) because `test_day_stats.py` reads its
    metrics off this very board and a second copy would drift."""
    tiles = {p: _ripe(spec.I_STRAWBERRY, 6) for p in (90, 91, 92)}
    tiles[99] = _thirsty(spec.I_TOMATO)
    return _farm(tiles)


def test_a_mandatory_tile_survives_when_the_estimate_undershoots(pre_split):
    # Re-admission drops from the value tail -- a strawberry, never the
    # watering [0.5]. The purse is 0, so 1.5 hires nobody and this is the
    # farmer's own 22 turns.
    unit_op = P.build_day(np, undershoot_board(), _macro(), TABLE)[0]
    assert int((unit_op[0] == O.OP_WATER).sum()) == 1
    assert int((unit_op[0] == O.OP_HARVEST).sum()) == 2


def _tile_value(view, pos):
    """The admit stage's coin value of one tile, straight off `_derive`."""
    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    return int(d.tile_value[pos])


def test_a_survival_watering_past_the_bonus_window_banks_no_extra_unit():
    """`bonus_today` is `bonus_water`'s unit, not any watering's [0.11/1.6].

    Wheat (one-time, window start 2, max yield day 4) planted on day 0 and
    seen on day 6 is four days past its window: `harvest_age = clip(28, 2, 4)
    = 4`, so it harvests today, and the engine adds no yield for a watering
    outside the window. The tile is thirsty, so it *is* watered -- for
    survival -- and the three units it holds are worth 3 x 25 = 75. Gating the
    bonus on `c_ongoing == 0` alone booked a fourth, phantom unit (100).
    """
    tile = {"kind": spec.KIND_PLANT, "occ": spec.I_WHEAT, "t_yield": 3, "t_cons": 1, "t_day": 0}
    assert _tile_value(_farm({44: tile}, day=6), 44) == 3 * int(BASE[spec.I_WHEAT])


def test_a_survival_watering_on_a_harvest_tile_carries_the_fires_it_saves():
    """A tile that harvests *and* must be watered is worth both [1.6].

    Tomato (ongoing, first yield 8, interval 1, max yield 4) planted on day 17
    and seen on day 25: age 8, so it fires today and holds one unit, and it is
    thirsty. Its remaining fires are days 26, 27 and 28 -- all inside the
    horizon -- so `crop_remaining_value` is (1 + 3) x 60 = 240, of which the
    harvest already books 1 x 60. The watering therefore carries 3 x 60 = 180
    and the tile is worth 240.

    Pricing that watering at 0 (because the tile harvests) made three fires
    invisible to admission, so the tile could be dropped for work worth less
    than what it was protecting.
    """
    tile = {"kind": spec.KIND_PLANT, "occ": spec.I_TOMATO, "t_yield": 1, "t_cons": 1, "t_day": 17}
    view = _farm({44: tile}, day=25)
    assert _tile_value(view, 44) == 4 * int(BASE[spec.I_TOMATO])
    # both ops are queued, in the engine's order (WATER before HARVEST)
    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    assert d.chain_op[44][:2].tolist() == [O.OP_WATER, O.OP_HARVEST]
    # ... and a tile that only harvests is worth its units alone
    dry = {"kind": spec.KIND_PLANT, "occ": spec.I_TOMATO, "t_yield": 1, "t_day": 17}
    assert _tile_value(_farm({44: dry}, day=25), 44) == 1 * int(BASE[spec.I_TOMATO])


def test_the_pickup_allowance_is_charged_to_every_unit_not_once_to_the_day():
    """`_routes` charges a unit's pickup turns inside its own block [LAW,
    0.12], so the admit stage must deduct them from *each* unit's budget.

    The board: one hungry goose on the spawn tile (serpentine 44) and six ripe
    strawberries on 45..50, one op each, so every tile is estimated at
    1 + EST_MOVES = 2 turns and the seven of them come to 14. Feed wheat is the
    only pickup kind the day wants, so the farmer's admit budget is
    22 - 1 - EST_LEAD = 16 and all seven are admitted. Charging `MAX_PICKUPS`
    instead of the kinds the day actually wants gives 22 - 5 - EST_LEAD = 12
    and admits six -- the feed (mandatory) plus five of the six harvests.

    The route reaches all of them: one PICKUP turn, then FEED on the spawn and
    six adjacent steps-and-harvests, 1 + 6 x 2 = 13 route turns.
    """
    tiles = {p: _ripe(spec.I_STRAWBERRY, 6) for p in range(45, 51)}
    tiles[44] = {"kind": spec.KIND_COOP, "occ": 0, "t_cons": 1}
    price = BASE.copy()
    price[spec.I_EGG] = 1                      # below the wheat, so no CARE joins the chain
    shed = np.zeros(spec.N_ITEMS, np.int32)
    shed[spec.I_WHEAT] = 1
    view = _farm(tiles)._replace(price=price, shed=shed)

    d = P._derive(np, view, _macro(), TABLE, np.int32(0), False, np.int32(0))
    assert int(P._pickup_kinds(np, d)) == 1
    assert int(d.task.sum()) == 7 and d.n_ops[44:51].tolist() == [1] * 7

    unit_op = P.build_day(np, view, _macro(), TABLE)[0]
    assert int((unit_op == O.OP_PICKUP).sum()) == 1
    assert int((unit_op == O.OP_FEED).sum()) == 1
    assert int((unit_op == O.OP_HARVEST).sum()) == 6      # five under the per-day allowance


def test_the_third_admit_round_is_the_one_that_converges(pre_split):
    """`ADMIT_ROUNDS = 3` is not a round number: this board needs all three.

    Four ripe strawberries at 120 a unit, all optional and all priced, so they
    share one route group and sweep in serpentine order. Serpentine position ->
    (x, y) and value: 37 -> (2, 3), 240; 57 -> (2, 5), 480; 71 -> (8, 7), 600;
    98 -> (1, 9), 600. The farmer spawns on (4, 4) with 22 route turns and no
    pickup to pay for; its *admit* budget is 22 - 0 - EST_LEAD = 17 and every
    tile is estimated at 1 op + EST_MOVES = 2.

      round 1  4 x 2 = 8 <= 17 admits all four. Exact route: -> 37 is 3 moves
               + 1 op = 4, -> 57 is 2 + 1 = 3 (7), -> 71 is 8 + 1 = 9 (16),
               -> 98 needs 9 + 1 = 10 more (26). 98 is uncovered; n_admit -> 3.
      round 2  the 240-coin tile 37 is the value tail and goes. Route: -> 57 is
               3 + 1 = 4, -> 71 is 8 + 1 = 9 (13), -> 98 needs 10 more (23).
               Still one over; n_admit -> 2. Walked: 57 + 71 = 1,080.
      round 3  the 480-coin tile 57 goes (600 ties fall to the lower index, so
               71 and 98 stay). Route: -> 71 is 7 + 1 = 8, -> 98 is 9 + 1 = 10
               (18 <= 22). Both covered. Walked: 71 + 98 = 1,200.

    Total queued value is 1,920, so the metric is 840 dropped after two rounds
    and 720 after three -- and a fourth round changes nothing, because round 3
    already leaves no admitted tile uncovered.
    """
    tiles = {37: _ripe(spec.I_STRAWBERRY, 2), 57: _ripe(spec.I_STRAWBERRY, 4),
             71: _ripe(spec.I_STRAWBERRY, 5), 98: _ripe(spec.I_STRAWBERRY, 5)}
    view = _farm(tiles)

    def dropped(rounds):
        saved = P.ADMIT_ROUNDS
        P.ADMIT_ROUNDS = rounds
        try:
            return int(P.build_day_stats(view, _macro(), TABLE).value_dropped)
        finally:
            P.ADMIT_ROUNDS = saved

    assert P.ADMIT_ROUNDS == 3
    assert dropped(2) == 840
    assert dropped(3) == 720 == dropped(4)


def test_crop_remaining_value_at_the_spec_numbers():
    I = np.int32
    ha = lambda c, t: I(int(np.clip(O.LAST_SHED_DAY - t, spec.CROP_FIRST_YIELD_DAY[c], spec.CROP_MAX_YIELD_DAY[c])))
    # wheat planted day 0, seen day 2 holding 1: three in-window waterings
    # left (today, tomorrow, the harvest day) -> 4 units
    assert int(V.crop_remaining_value(np, BASE, I(0), I(1), I(spec.I_WHEAT), I(2), ha(0, 0))) == 4 * 25
    # tomato planted day 0, seen day 9 holding 1: fires 10, 11 left -> 3 units
    assert int(V.crop_remaining_value(np, BASE, I(0), I(1), I(spec.I_TOMATO), I(9), ha(2, 0))) == 3 * 60
    # wheat planted day 27, seen day 28 holding 1: the pay day is
    # `valuation.pay_day()`, which `plan.HORIZON_DROP_ON` (5b0fcc4) moved from
    # 28 to 29 -- today's watering fires at eod 28 and sells on 29, so the
    # banked unit and that one are both money. Without the switch the harvest
    # lands after the last shed day and the planting is worth nothing.
    assert int(V.crop_remaining_value(np, BASE, I(27), I(1), I(spec.I_WHEAT), I(28), ha(0, 27))) == \
        (2 * 25 if P.HORIZON_DROP_ON else 0)


def test_prio_is_gone():
    assert "prio" not in P.Macro._fields


def test_admit_route_agrees_across_backends():
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
        assert np.array_equal(np.asarray(x), np.asarray(y))
