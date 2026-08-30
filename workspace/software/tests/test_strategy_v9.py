"""First-wave v9 strategy tests.

The v9 module is loaded independently from the frozen submission path.  These
checks pin the new seams without changing any legacy strategy expectations.
"""

import copy
import importlib.util
import sys
from pathlib import Path


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
AGENT_V9 = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v9" / "main.py"


def _load(tag="v9"):
    name = f"{tag}_{id(object())}_{len(sys.modules)}"
    spec = importlib.util.spec_from_file_location(name, AGENT_V9)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def _tiles(quads=("NW", "NE")):
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    for y in range(10):
        for x in range(10):
            quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            if quad in quads:
                tiles[y][x] = None
    return tiles


def _farm(quads=("NW", "NE"), farmer=(1, 1), hands=(), money=5000.0):
    return {
        "money": money,
        "tiles": _tiles(quads),
        "farmer": list(farmer),
        "hands": [list(h) for h in hands],
        "unlocked_quadrants": list(quads),
        "hires_today": 0,
    }


def _obs(mod, day=6, hour=6, player=0, private=None, farm=None):
    mine = farm or _farm()
    other = _farm(quads=("NW",), farmer=(4, 4), money=3000.0)
    farms = [mine, other] if player == 0 else [other, mine]
    return {
        "player": player,
        "day": day,
        "hour": hour,
        "farms": farms,
        "market": {"prices": dict(mod.BASE_PRICE)},
        "private": private or {"shed": {}, "seeds": {}, "inventories": [{}]},
    }


def _task(x, y, act, value=100, red=False, need=None, key=None):
    return {
        "w": value,
        "v": value,
        "x": x,
        "y": y,
        "act": list(act),
        "key": key or (act[0].lower(), x, y),
        "red": red,
        "need": need,
    }


def test_agent_v9_loads_as_independent_callable():
    mod = _load("load")
    assert callable(mod.agent)
    assert mod.__file__.replace("\\", "/").endswith("agent_v9/main.py")
    assert mod.TELEMETRY_ENABLED is True
    assert hasattr(mod, "telemetry_snapshot")


def test_telemetry_is_action_transparent_and_can_be_disabled():
    obs = _obs(_load("fixture"))
    off_mod = _load("telemetry_off")
    on_mod = _load("telemetry_on")
    off_mod.set_telemetry_enabled(False)
    off_action = off_mod.agent(copy.deepcopy(obs))
    events = []
    on_mod.set_telemetry_sink(events.append)
    on_action = on_mod.agent(copy.deepcopy(obs))
    assert on_action == off_action
    assert events and events[-1]["kind"] == "turn"

    count = len(events)
    on_mod.set_telemetry_enabled(False)
    disabled_action = on_mod.agent(copy.deepcopy(obs))
    assert disabled_action == on_action
    assert len(events) == count


def test_sector_router_prefers_same_sector_adjacent_task():
    mod = _load("sector")
    farm = _farm(quads=("NW", "NE"), farmer=(1, 1), hands=((2, 1),))
    obs = _obs(mod, farm=farm)
    local = _task(2, 1, ["WATER"], value=100, key=("local", 2, 1))
    remote = _task(8, 1, ["HARVEST"], value=110, key=("remote", 8, 1))
    mod._schedule_units(obs, farm, obs["private"], 6, [local, remote])
    trace = mod.scheduler_trace()[0]
    assert trace["assign"][1] == ("local", 2, 1)
    assert trace["cross_quadrant"] <= 1


def test_same_sector_eligibility_does_not_strand_other_hands():
    mod = _load("multi_sector")
    farm = _farm(quads=("NW",), farmer=(1, 1), hands=((2, 1),))
    obs = _obs(mod, farm=farm)
    tasks = [
        _task(3, 1, ["WATER"], value=100, key=("a", 3, 1)),
        _task(1, 2, ["WATER"], value=90, key=("b", 1, 2)),
    ]
    routed, _ = mod._route_tasks(obs, farm, obs["private"], 6, tasks)
    assert all(set(task["units"]) == {0, 1} for task in routed)


def test_redline_task_still_preempts_local_value_task():
    mod = _load("red")
    farm = _farm(quads=("NW", "SE"), farmer=(1, 1))
    private = {"shed": {}, "seeds": {}, "inventories": [{"WHEAT": 5}]}
    obs = _obs(mod, farm=farm, private=private)
    local = _task(2, 1, ["HARVEST"], value=900, key=("local", 2, 1))
    red = _task(8, 8, ["FEED"], value=100, red=True, need="WHEAT",
                 key=("feed", 8, 8))
    mod._schedule_units(obs, farm, private, 6, [local, red])
    trace = mod.scheduler_trace()[0]
    assert trace["assign"][0] == ("feed", 8, 8)
    assert trace["red_assignments"] == 1


def test_telemetry_and_routes_are_isolated_by_player_and_day():
    mod = _load("isolation")
    mod.reset_telemetry()
    mod._ROUTE_STATE.clear()
    for player, day in ((0, 1), (1, 1), (0, 2)):
        farm = _farm(quads=("NW",), farmer=(1, 1))
        obs = _obs(mod, day=day, player=player, farm=farm)
        mod.agent(copy.deepcopy(obs))
    snapshot = mod.telemetry_snapshot()
    assert set(snapshot["players"]) == {"0", "1"}
    assert set(snapshot["players"]["0"]["days"]) == {"1", "2"}
    assert set(snapshot["players"]["1"]["days"]) == {"1"}
    assert set(mod._ROUTE_STATE) >= {0, 1}
    assert mod._ROUTE_STATE[0]["day"] == 2
    assert mod._ROUTE_STATE[1]["day"] == 1


def test_telemetry_records_requested_shadow_dimensions():
    mod = _load("dimensions")
    mod.reset_telemetry()
    events = []
    mod.set_telemetry_sink(events.append)
    farm = _farm(quads=("NW",), farmer=(1, 1), money=42.0)
    farm["tiles"][1][2] = {
        "kind": "PLANT", "crop": "WHEAT", "planted_day": 4,
        "yield_units": 2, "watered_today": False,
        "consecutive_unwatered": 1, "fertilized_until_day": -1,
    }
    private = {"shed": {"WHEAT": 5}, "seeds": {},
               "inventories": [{"WHEAT": 2}]}
    obs = _obs(mod, day=29, hour=6, farm=farm, private=private)
    action = mod.agent(copy.deepcopy(obs))
    assert action["farmer"]
    event = events[-1]
    assert event["kind"] == "turn"
    assert set(event["metrics"]) >= {
        "moving_turns", "effective_ops", "movement_to_effective_ratio",
        "pass_count", "repeated_tasks", "cross_quadrant_switches",
        "overdue", "zone_tasks_completed", "wheat_alive", "wheat_harvested",
        "external_feed_bought", "minimum_cash", "shed_overflow",
        "terminal_clearout",
    }
    assert event["metrics"]["minimum_cash"] == 42.0
    assert event["metrics"]["wheat_alive"] == 1
    assert event["metrics"]["terminal_clearout"] is False
