"""P0 shed-access and market-order regressions."""

from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

from kgenv.arena import SUBMISSION_MAIN
from kgenv.engine import run_episode


spec = importlib.util.spec_from_file_location("main_p0", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def _tiles(quads=("NW",)):
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    for y in range(10):
        for x in range(10):
            quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            if quad in quads:
                tiles[y][x] = None
    return tiles


def _farm(quads=("NW",), money=5000.0, farmer=(4, 4), hands=()):
    return {"money": money, "tiles": _tiles(quads), "farmer": list(farmer),
            "hands": [list(h) for h in hands], "unlocked_quadrants": list(quads),
            "hires_today": 0}


def _obs(day, hour, farm, private, player=0):
    other = _farm()
    return {"player": player, "day": day, "hour": hour,
            "farms": [farm, other] if player == 0 else [other, farm],
            "private": private, "market": {"prices": dict(main.BASE_PRICE)}}


def _private(**shed):
    values = {item: 0 for item in (*main.CROPS, *main.BASE_PRICE, *main.ANIMALS)}
    values.update(shed)
    return {"shed": values, "seeds": {}, "inventories": [{}]}


def test_shed_access_always_contains_all_official_center_tiles():
    expected = ((4, 4), (5, 4), (4, 5), (5, 5))
    assert main._shed_access(10, ("NW",)) == expected
    assert main._shed_access(10, ("NW", "NE")) == expected
    assert main._shed_access(10, ("NW", "NE", "SW")) == expected
    assert main._shed_access(10, ("NW", "NE", "SW", "SE")) == expected


def test_last_day_return_may_use_locked_official_shed_access():
    farm = _farm(("NW",), farmer=(9, 9), hands=((8, 8),))
    private = _private(WHEAT=2)
    private["inventories"] = [{"WHEAT": 1}, {"WHEAT": 1}]
    tasks, *_ = main._build_tasks(_obs(29, 10, farm, private), farm, private, 29)
    assert {tuple((task["x"], task["y"])) for task in tasks} == {(5, 5)}


def test_locked_shed_pickup_and_drop_remain_executable():
    farm = _farm(("NW",), farmer=(5, 4))
    private = _private(WHEAT=4)
    tasks = [
        {"x": 5, "y": 4, "act": ["PICKUP", "WHEAT", 1],
         "key": ("pickup",), "w": 2, "v": 2, "need": None},
        {"x": 5, "y": 4, "act": ["DROP"], "key": ("drop",),
         "w": 1, "v": 1, "need": None},
    ]
    actions = main._schedule_units(_obs(1, 0, farm, private), farm, private, 1, tasks)
    assert actions == [["PICKUP", "WHEAT", 1]]


def test_official_engine_pickup_works_from_every_locked_center_access():
    from kaggle_environments.envs.kaggriculture import kaggriculture as official

    for access in ((5, 4), (4, 5), (5, 5)):
        farm = official._new_farm(10, 3000)
        private = official._new_private()
        farm["farmer"] = list(access)
        private["shed"]["WHEAT"] = 1
        assert farm["tiles"][access[1]][access[0]] == "LOCKED"
        official._apply_unit_action(
            farm, private, 0, ["PICKUP", "WHEAT", 1], 10, 0, 24)
        assert private["shed"]["WHEAT"] == 0
        assert private["inventories"][0]["WHEAT"] == 1

        official._apply_unit_action(farm, private, 0, ["DROP"], 10, 0, 24)
        assert private["shed"]["WHEAT"] == 1
        assert private["inventories"][0] == {}


def test_official_engine_nw_only_pickup_is_a_real_state_change():
    from kaggle_environments import make

    def active(obs):
        if obs["day"] == 0 and obs["hour"] == 0:
            return {"farmer": ["PASS"], "hands": [],
                    "market": [["BUY_PRODUCT", "WHEAT", 1]]}
        if obs["day"] == 0 and obs["hour"] == 1:
            return {"farmer": ["PICKUP", "WHEAT", 1], "hands": [],
                    "market": []}
        return {"farmer": ["PASS"], "hands": [], "market": []}

    env = make("kaggriculture", configuration={"episodeSteps": 4, "seed": 101})
    env.run([active, "pass"])
    assert [state["status"] for state in env.steps[-1]] == ["DONE", "DONE"]
    after_buy = env.steps[1][0]["observation"]["private"]
    after_pickup = env.steps[2][0]["observation"]["private"]
    assert after_buy["shed"]["WHEAT"] == 1
    assert after_pickup["shed"]["WHEAT"] == 0
    assert after_pickup["inventories"][0]["WHEAT"] == 1


def test_market_planner_exposes_single_budgeted_queue():
    private = _private(WHEAT=1)
    private["seeds"] = {"WHEAT": 1, "STRAWBERRY": 0, "MELON": 0, "CARROT": 0,
                         "TOMATO": 0}
    private["inventories"] = [{"WHEAT": 2, "COW": 1}]
    farm = _farm(("NW", "NE"), money=3000.0)
    obs = _obs(0, 0, farm, private)
    orders = main._market_orders(obs, farm, private, 0, 5, 5)
    assert len(orders) <= 10
    assert orders
    assert all(order[0] in {"BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL", "HIRE", "BUY_LAND"}
               for order in orders)
    assert all(len(order) < 3 or order[2] > 0 for order in orders)
