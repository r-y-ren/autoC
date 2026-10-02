"""The three planner-side operational metrics of PLANNER_V3_1 section 7:
units the shed destroys, coins the purse could not grant, task value dropped
at the labour boundary.

`build_day_stats` runs the very code `build_day` runs -- both call
`_plan_and_stats` -- so these numbers describe the plan that is actually
walked, and `build_day`'s return tuple (which the simulator consumes) does
not change to carry them.
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
from test_admit_route import BASE, TABLE, _farm, _ripe, undershoot_board
from test_budget_order import _macro
from test_budget_order import _view as _blank
from test_sell_side import _overflow_view

from kagg3 import spec
from kagg3.core import plan as P


def _more_harvests_than_the_route_can_reach():
    """Four ripe strawberries the estimate admits and the exact route cannot
    reach, spread so that ADMIT_ROUNDS re-admissions never converge: tile 4 at
    (4, 0) holding 1 unit (120 coins), tile 9 at (9, 0) holding 5 (600), tile
    91 at (8, 9) holding 5 (600) and tile 99 at (0, 9) holding 6 (720). All
    four are optional (an ongoing crop's harvest keeps) and all four are
    priced, so they share one route group and sweep in serpentine order."""
    tiles = {4: _ripe(spec.I_STRAWBERRY, 1), 9: _ripe(spec.I_STRAWBERRY, 5),
             91: _ripe(spec.I_STRAWBERRY, 5), 99: _ripe(spec.I_STRAWBERRY, 6)}
    return _farm(tiles)


# ---- the metrics -------------------------------------------------------


def test_a_forced_sale_that_absorbs_the_overshoot_destroys_nothing():
    # 95 in the shed, 20 units ripening: the 15-unit overshoot is force-sold
    # out of the 95 units of sellable stock, so end-of-day destroys nothing.
    stats = P.build_day_stats(_overflow_view(), _macro(), TABLE)
    assert int(stats.overflow_destroyed) == 0


def test_a_deeper_overshoot_is_still_absorbed_while_stock_remains():
    # 30 ripening instead of 20: the overshoot grows to 25 and the 95 units of
    # sellable stock still cover it, so nothing is destroyed.
    stats = P.build_day_stats(_overflow_view(harvest_tonight=30), _macro(), TABLE)
    assert int(stats.overflow_destroyed) == 0


def test_the_shed_destroys_what_the_forced_sale_cannot_reach():
    # The forced sale draws on the hour-0 *product* stock alone [0.9], so a
    # shed full of livestock cannot absorb tonight's harvest: all 25 units of
    # the overshoot are destroyed.
    view = _overflow_view(harvest_tonight=30, shed={spec.I_GOOSE: 95})
    stats = P.build_day_stats(view, _macro(), TABLE)
    assert int(stats.overflow_destroyed) == 25


def test_value_dropped_is_the_task_value_admission_turned_away(monkeypatch):
    # The board's four tasks are worth 720, 720, 720 (six strawberries each at
    # the fixture's price of 120) and 240 (the mandatory watering). The route
    # reaches three, and re-admission drops from the value tail -- never the
    # mandatory tier [0.5] -- so exactly one strawberry goes.
    #
    # `ROUTE_SPLIT_ON` off, like `test_admit_route`'s own users of this board:
    # it is built to miss by exactly one turn (23 needed against 22) and the
    # split start hands the farmer that turn, after which nothing is dropped
    # and the metric has no subject.
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    stats = P.build_day_stats(undershoot_board(), _macro(), TABLE)
    assert int(stats.value_dropped) == 6 * int(BASE[spec.I_STRAWBERRY])


def test_value_dropped_counts_work_the_route_never_reaches():
    # The metric is task value *not done today*, not task value not admitted.
    # The estimate is ops + EST_MOVES = 2 a tile, against the farmer's admit
    # budget of 22 - 0 - EST_LEAD = 17 (no pickup kind has any demand on this
    # board [0.12]), so all four tiles are admitted. The exact route
    # reaches far fewer, and because the re-admission drops from the *value*
    # tail while the route drops from its own tail, the loop never converges
    # within ADMIT_ROUNDS = 3:
    #
    #   round 1  admitted {4, 9, 91, 99}; route (4, 4) -> 4 = 4 + 1 = 5 turns,
    #            -> 9 = 5 + 1 = 11, -> 91 = 10 + 1 = 22 (exactly), -> 99 needs
    #            8 + 1 = 9 more. 99 (720) is left uncovered, n_admit -> 3.
    #   round 2  admitted {99, 9, 91} (the 120-coin tile 4 is the value tail);
    #            route -> 9 = 10, -> 91 = 21, -> 99 needs 9 more. n_admit -> 2.
    #   round 3  admitted {99, 9} (600 ties fall to the lower index, so 91
    #            goes); route -> 9 = 10, -> 99 needs 18 + 1 = 19 more. 99 is
    #            *still* admitted and *still* unreached.
    #
    # So one harvest is walked (tile 9) and 120 + 600 + 720 = 1,440 coins of
    # queued work is dropped. The old definition `task & ~admitted` sees only
    # the two tiles admission turned away, 120 + 600 = 720, and misses the
    # 720-coin route residue that is the whole point of the metric.
    stats = P.build_day_stats(_more_harvests_than_the_route_can_reach(), _macro(), TABLE)
    assert int(stats.value_dropped) == 1_440


def test_a_day_whose_work_all_fits_drops_no_value():
    stats = P.build_day_stats(_farm({45: _ripe(spec.I_TOMATO, 4)}), _macro(), TABLE)
    assert int(stats.value_dropped) == 0


def test_a_purse_that_covers_the_plan_has_no_purchase_shortfall():
    macro = _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))
    assert int(P.build_day_stats(_blank(10_000), macro).purchase_shortfall) == 0


def test_purchase_shortfall_counts_the_coins_the_greedy_could_not_grant():
    macro = _macro(plant_target=np.array([4, 0, 0, 0, 0], np.int32))
    cost = int(spec.CROP_SEED_COST[spec.I_WHEAT])
    broke = int(P.build_day_stats(_blank(0), macro).purchase_shortfall)
    half = int(P.build_day_stats(_blank(2 * cost), macro).purchase_shortfall)
    assert broke > half > 0


# ---- the contract ------------------------------------------------------


def test_build_day_still_returns_the_six_plan_arrays():
    view, macro = undershoot_board(), _macro()
    plan = P.build_day(np, view, macro, TABLE)
    assert len(plan) == 6
    assert [np.asarray(a).shape for a in plan[:3]] == [(spec.MAX_UNITS, spec.TURNS_PER_DAY)] * 3


def test_the_stats_are_int32_scalars():
    stats = P.build_day_stats(undershoot_board(), _macro(), TABLE)
    assert stats._fields == ("overflow_destroyed", "purchase_shortfall", "value_dropped")
    for v in stats:
        assert np.asarray(v).dtype == np.int32 and np.asarray(v).shape == ()
