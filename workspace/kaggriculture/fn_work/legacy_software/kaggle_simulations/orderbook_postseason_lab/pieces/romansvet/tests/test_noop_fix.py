"""`plan.NOOP_FIX_ON` (NOOPAUDIT 2026-09-23): orders the engine is certain to reject.

Engine: `_decay_plants` (kaggriculture.py:752-766) decays a crop past
`max_lifespan_step` one unit every other step, after that step's unit actions;
a spent ongoing crop gets `max_lifespan_step = (last + 1) * 24` at its final
fire (:801-802). ON: (1) the last-day harvest of a spent ongoing crop joins the
mandatory tier; (2) `parse_view` shows a tile that is WEED before hour
`NOOP_DOA_H` as empty-handed and watered. OFF is the pinned planner.
"""
from __future__ import annotations

import _pin  # noqa: F401
import numpy as np
import pytest
from test_care_fill import _PINNED_OFF
from test_route_early import PIN, PIN_SEEDS, _digest, _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.agent import parse
from kagg3.core import ops as O
from kagg3.core import plan as P


def _obs(day, hour, tile):
    tiles = [[None] * spec.BOARD for _ in range(spec.BOARD)]
    tiles[0][0] = tile
    farm = dict(tiles=tiles, money=1000, unlocked_quadrants=["NW"], hands=[])
    mkt = dict(prices={n: 10 for n in spec.PRODUCTS}, inventory={n: spec.MARKET_I0 for n in spec.PRODUCTS})
    return dict(player=0, day=day, hour=hour, farms=[farm, dict(farm)], market=mkt, town=dict(unlocked_shops=[]),
                private=dict(shed={}, seeds={}, inventories=[{}]))


def _straw(y, mls):
    return dict(kind="PLANT", crop="STRAWBERRY", planted_day=3, watered_today=False,
                consecutive_unwatered=1, yield_units=y, max_lifespan_step=mls, fertilized_until_day=-1)


@pytest.mark.parametrize("y,mls,day,hour,dead", [
    (1, 480, 20, 0, True),     # decays at step 480 -> WEED after hour 0
    (2, 480, 20, 0, True),     # WEED after step 482 (hour 2)
    (3, 480, 20, 0, False),    # lives to hour 4
    (2, 504, 20, 0, False),    # final-fire day itself: decay starts tomorrow
    (1, -1, 20, 0, False),
])
def test_doa_matches_engine_decay(y, mls, day, hour, dead):
    assert parse._doa(_straw(y, mls), _obs(day, hour, None)) is dead
    wheat = dict(_straw(y, mls), crop="WHEAT")
    assert parse._doa(wheat, _obs(day, hour, None)) is False   # one-time crops untouched


def _view_of(on, monkeypatch, tile):
    monkeypatch.setattr(P, "NOOP_FIX_ON", on)
    v = parse.parse_view(_obs(20, 0, tile), 0)
    k = list(P.SERP).index(0)
    return int(v.t_water[k]), int(v.t_cons[k]), int(v.t_yield[k])


def test_parse_off_is_raw_on_masks_dead_tile(monkeypatch):
    assert _view_of(False, monkeypatch, _straw(2, 480)) == (0, 1, 2)
    assert _view_of(True, monkeypatch, _straw(2, 480)) == (1, 0, 0)
    assert _view_of(True, monkeypatch, _straw(2, 504)) == (0, 1, 2)


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(monkeypatch):
    monkeypatch.setattr(P, "NOOP_FIX_ON", False)
    for name in _PINNED_OFF:
        monkeypatch.setattr(P, name, False)
    assert tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS) == PIN


def _harvests(plan):
    return int(np.sum(np.asarray(plan[0]) == O.OP_HARVEST))


def test_on_last_day_harvest_is_never_cut_below_off(monkeypatch):
    # tomatoes planted day 0: final fire lands for day 11 (0 + 8 + 3*1)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    view = _view(day=11, money=500, n_ripe=60, yld=2)
    monkeypatch.setattr(P, "NOOP_FIX_ON", False)
    off = _harvests(_plan(view))
    monkeypatch.setattr(P, "NOOP_FIX_ON", True)
    assert _harvests(_plan(view)) >= off
    # not the last day: ON == OFF
    view = _view(day=10, money=500, n_ripe=60, yld=2)
    a = _digest(_plan(view))
    monkeypatch.setattr(P, "NOOP_FIX_ON", False)
    assert _digest(_plan(view)) == a
