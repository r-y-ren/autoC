"""Every FERTILIZE the planner emits is backed by fertilizer in the acting
unit's own hands -- the invariant, and the measurement that closes the
"wasted FERTILIZE ops" lever.

**The engine rule.** `kaggriculture.py:475-482`: FERTILIZE returns without
doing anything if the tile is not a PLANT, then calls
`_inv_take(inv, "FERTILIZER", 1)` and returns -- again silently -- if the
*unit's own* inventory (not the shed) holds none. Either way the unit has
still spent its one op for the turn. A no-op FERTILIZE therefore costs a
unit-turn and forgoes an application; over the replays an application is worth
~110 coins (`S/fert_marginal/report.md`: 269 extra crop units for 181
applications). `_drop_inventories_to_shed` (:843, called from `_end_of_day`
:878) empties every unit's hands into the shed each night and :882 resets the
list, so a unit starts every day with nothing and PICKUP is the *only* way it
can be holding fertilizer when its block reaches a FERTILIZE.

**The measurement.** Census of every issued FERTILIZE op in 80 real-engine
games (`S/fert_carry/census.py` over the 32 McGrain replays in
`S/autopsy_mcgrain/replays`, the 16 in `S/autopsy_oceanmix/replays`, and 16
fresh ones off this tree):

| | per game |
|---|---|
| FERTILIZE ops issued | 181.2 / 165.9 / **183.3** |
| of those effective | 181.2 / 165.9 / **183.3** |
| no-op, unit held no fertilizer | **0** |
| no-op, tile not a PLANT | **0** |
| redundant, tile already fertilized | **0** |
| fertilizer PICKUP units asked / received | 181.2 / 181.2 |

Zero no-ops in 11,386 ops. The "~110 no-op FERTILIZE ops a game" that
`S/fert_buy/report.md` and `S/fert_marginal/report.md` both quote is an
artifact of their census rule, `any element of the action list that
startswith("FERTILIZE")`: the *item* string in `["PICKUP", "FERTILIZER", n]`
matches it. Reproduced exactly -- 293.2 under that rule = 181.2 true
FERTILIZE + 112.0 fertilizer PICKUP rows (`S/fert_carry/reprod.py`).

**Why it holds, in the planner.** `plan.py:2625` caps the day's applications
at what the shed can supply (`n_fert_eff = min(n_fert_want, fert_avail)`,
`fert_avail = shed + fert_bought`), :2626 selects exactly that many tiles by
value rank into `want_fert`, `_pick_masks` (:1718) makes `want_fert` pickup
kind 1, `_routes` gives unit *u* `blk[1, u]` = the count of `want_fert` tiles
inside its own block (:3965) and :3405-3409 writes that as its morning PICKUP
quantity. The per-unit counts partition the day's `want_fert` tiles, so they
sum to `n_fert_eff` and no two blocks can draw the same shed unit. :3428-3430
holds that same `n_fert_eff` back from the sale, so the stock is still there
when the pickups fire. And the two tail passes can only emit COLLECT_FERT,
WATER, DIG (:3204-3208) or FEED, CARE -- never FERTILIZE -- so there is no
fallback path that could issue one off-plan.

No switch: there is no defect to gate. These tests pin the invariant so the
phantom cannot come back, and so a future change to the route, the budget or
the sale cannot quietly start ordering applications the crew cannot back.
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
from test_route_early import _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

#: Wider than `test_route_early`'s twelve: the invariant is a property, so the
#: boards are there to falsify it rather than to pin a digest.
SEEDS = tuple(range(40))


def _fert_pickups(plan):
    """int[MAX_UNITS]: fertilizer units unit *u*'s morning PICKUPs ask for."""
    unit_op, unit_a, unit_q = plan[0], plan[1], plan[2]
    hit = (unit_op == O.OP_PICKUP) & (unit_a == spec.I_FERT)
    return np.where(hit, unit_q, 0).sum(axis=1)


def _fert_ops(plan):
    """int[MAX_UNITS]: FERTILIZE ops unit *u* is told to perform."""
    return (plan[0] == O.OP_FERTILIZE).sum(axis=1)


def _fert_bought(plan):
    """Fertilizer units the day's BUY_PRODUCT rows add to the shed."""
    op, arg, qty = plan[3], plan[4], plan[5]
    hit = (op == O.MO_BUY_PRODUCT) & (arg == spec.I_FERT)
    return int(np.where(hit, qty, 0).sum())


def _fert_sold(plan):
    op, arg, qty = plan[3], plan[4], plan[5]
    hit = (op == O.MO_SELL) & (arg == spec.I_FERT)
    return int(np.where(hit, qty, 0).sum())


def _targets(unit_op):
    """[(u, sweep position)] of every FERTILIZE, by walking the emitted route
    from each unit's own spawn tile -- the route the engine will really
    execute, not a second model of it. The walk is in board coordinates and
    `SERP_INV` puts the answer back in the serpentine space a `DayView` is
    indexed by."""
    out = []
    for u in range(spec.MAX_UNITS):
        x, y = int(P.SPAWN_X[u]), int(P.SPAWN_Y[u])
        for op in unit_op[u].tolist():
            if op == O.OP_NORTH:
                y -= 1
            elif op == O.OP_SOUTH:
                y += 1
            elif op == O.OP_EAST:
                x += 1
            elif op == O.OP_WEST:
                x -= 1
            elif op == O.OP_FERTILIZE:
                assert 0 <= x < spec.BOARD and 0 <= y < spec.BOARD, (u, x, y)
                out.append((u, int(P.SERP_INV[y * spec.BOARD + x])))
    return out


def test_every_fertilize_is_backed_by_the_acting_units_own_pickup():
    """The whole lever, as an invariant: a unit is never told to spread more
    fertilizer than it was told to pick up. It starts the day empty
    (`kaggriculture.py:878`), so a shortfall here is a silent engine no-op and
    a unit-turn thrown away."""
    for s in SEEDS:
        plan = _plan(*_seeded_case(s))
        picked, spread = _fert_pickups(plan), _fert_ops(plan)
        for u in range(spec.MAX_UNITS):
            assert int(spread[u]) <= int(picked[u]), (s, u, int(spread[u]), int(picked[u]))


def test_no_unit_picks_up_fertilizer_it_is_not_sent_to_spread():
    """The other side of the same equality: the pickup turn is a turn, so a
    unit that carries a unit home has wasted one. `blk` is the count of
    `want_fert` tiles in the block, so the two are equal by construction."""
    for s in SEEDS:
        plan = _plan(*_seeded_case(s))
        assert _fert_pickups(plan).tolist() == _fert_ops(plan).tolist(), s


def test_the_days_pickups_never_outrun_the_shed():
    """Summed over the crew the pickups cannot exceed hour-0 stock plus the
    BUY row, or the engine's `n = min(n, available)` (`kaggriculture.py:372`)
    silently short-changes whichever unit picks up last."""
    for s in SEEDS:
        view, macro = _seeded_case(s)
        plan = _plan(view, macro)
        avail = int(view.shed[spec.I_FERT]) + _fert_bought(plan)
        assert int(_fert_pickups(plan).sum()) <= avail, (s, avail)


def _contested(fert=6):
    """Sixty fertilizable tomatoes -- far more applications than `fert` can
    cover -- a crew wide enough to split them across blocks, and a shed already
    at capacity so the BUY row cannot top the fertilizer up. Whatever the day
    spreads has to come out of the `fert` units standing in the shed."""
    view = _view(day=8, n_ripe=60, fert=fert, money=8_000, yld=1)
    shed = view.shed.copy()
    shed[spec.I_EGG] = spec.SHED_CAPACITY - fert
    return view._replace(shed=shed)


def test_two_blocks_cannot_draw_the_same_shed_unit():
    """The failure mode the lever assumed: two blocks that both count the same
    shed stock, so whichever unit picks up second finds the shed empty and
    walks its half of the route spreading nothing. `n_fert_eff` caps the day's
    applications at the stock and the per-block counts partition them, so the
    six units in the shed are split three and three, not taken twice."""
    view = _contested(fert=6)
    plan = _plan(view, _macro())

    picked, spread = _fert_pickups(plan), _fert_ops(plan)
    assert _fert_bought(plan) == 0, "the board is meant to be unable to buy"
    carriers = [u for u in range(spec.MAX_UNITS) if picked[u]]
    assert len(carriers) >= 2, "the board is meant to split across blocks"
    assert int(picked.sum()) == int(view.shed[spec.I_FERT])
    assert picked.tolist() == spread.tolist()
    # Supply and not demand is what binds here -- the same board with ten in
    # the shed spreads ten -- so the six above really are the crew rationing
    # one stock between two blocks rather than running out of worthwhile tiles.
    ten = _plan(_contested(fert=10), _macro())
    assert int(_fert_ops(ten).sum()) == 10
    assert _fert_pickups(ten).tolist() == _fert_ops(ten).tolist()


def test_a_fertilize_only_ever_lands_on_a_plantable_unfertilized_tile():
    """The other two no-op branches of `kaggriculture.py:475-482`: a tile that
    is not a PLANT is refused before the fertilizer is even taken, and one
    already fertilized today burns a unit for nothing."""
    seen = 0
    for s in SEEDS:
        view, macro = _seeded_case(s)
        plan = _plan(view, macro)
        hit = _targets(plan[0])
        assert len(hit) == int(_fert_ops(plan).sum()), s   # the walk found them all
        seen += len(hit)
        for u, tile in hit:
            assert int(view.kind[tile]) == spec.KIND_PLANT, (s, u, tile)
            assert int(view.t_fert[tile]) < int(view.day), (s, u, tile)
    assert seen > 0, "no board fertilized anything -- the sweep proves nothing"


def test_the_sale_never_sells_the_fertilizer_the_day_will_spread():
    """The pickups run from the route base, which straddles sell lot 1, so the
    stock they need has to survive the sale (`plan.py:3428-3430`)."""
    for s in SEEDS:
        view, macro = _seeded_case(s)
        plan = _plan(view, macro)
        left = int(view.shed[spec.I_FERT]) - _fert_sold(plan)
        assert int(_fert_pickups(plan).sum()) <= left + _fert_bought(plan), s
