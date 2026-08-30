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


def _wheat_farm_obs(mod, day=8, wheat=14, herd=12, money=1200.0,
                    opp_wheat=0, shops=("BAKERY",)):
    mine = _farm(quads=("NW", "NE", "SW"), money=money)
    # Populate observable wheat and animal structures without requiring a full
    # engine episode; the mode gate only consumes public farm geometry.
    placed = 0
    for y, row in enumerate(mine["tiles"]):
        for x, tile in enumerate(row):
            if tile is None and placed < wheat:
                row[x] = {"kind": "PLANT", "crop": "WHEAT",
                          "planted_day": 4, "yield_units": 1}
                placed += 1
    placed = 0
    for y, row in enumerate(mine["tiles"]):
        for x, tile in enumerate(row):
            if tile is None and placed < herd:
                row[x] = {"kind": "PASTURE", "animal": "COW"}
                placed += 1
    opp = _farm(quads=("NW",), money=900.0)
    placed = 0
    for y, row in enumerate(opp["tiles"]):
        for x, tile in enumerate(row):
            if tile is None and placed < opp_wheat:
                row[x] = {"kind": "PLANT", "crop": "WHEAT",
                          "planted_day": 4, "yield_units": 1}
                placed += 1
    return {"player": 0, "day": day, "hour": 6,
            "farms": [mine, opp],
            "market": {"prices": dict(mod.BASE_PRICE)},
            "town": {"unlocked_shops": list(shops)},
            "private": {"shed": {}, "seeds": {"WHEAT": 4},
                        "inventories": [{}]}}


def test_wheat_farm_gate_is_opt_in_and_fail_closed():
    mod = _load("wheat_gate")
    obs = _wheat_farm_obs(mod)
    mod.V9_WHEAT_FARM_ENABLED = False
    assert mod._macro_plan(0, copy.deepcopy(obs), 8)["mode"] != "WHEAT_FARM"
    mod._PLAN_MEM.clear()
    mod.V9_WHEAT_FARM_ENABLED = True
    assert mod._decide_mode(copy.deepcopy(obs), 8, None)["mode"] == "WHEAT_FARM"
    blocked = _wheat_farm_obs(mod, money=700.0)
    assert mod._decide_mode(blocked, 8, None)["mode"] != "WHEAT_FARM"
    contested = _wheat_farm_obs(mod, opp_wheat=11)
    assert mod._decide_mode(contested, 8, None)["mode"] != "WHEAT_FARM"


def test_wheat_farm_entry_matches_actual_build_pace():
    # The champion's placed herd is 4 (the d0 burst) when cash and the wheat
    # line are both alive at d6-7; the 12-head ceiling completes ~d13-14,
    # outside every viable entry window (probe 2026-08-30).  Entry requires
    # the burst to be placed, and the hold branch keeps the same floor so
    # the mode cannot flap off the moment it enters.
    mod = _load("wheat_pace")
    mod.V9_WHEAT_FARM_ENABLED = True
    burst = _wheat_farm_obs(mod, day=7, wheat=13, herd=4, money=900.0)
    assert mod._decide_mode(burst, 7, None)["mode"] == "WHEAT_FARM"
    unplaced = _wheat_farm_obs(mod, day=7, wheat=13, herd=2, money=900.0)
    assert mod._decide_mode(unplaced, 7, None)["mode"] != "WHEAT_FARM"
    hold = _wheat_farm_obs(mod, day=9, wheat=13, herd=4, money=500.0)
    assert mod._decide_mode(hold, 9, "WHEAT_FARM")["mode"] == "WHEAT_FARM"


def test_wheat_farm_field_contains_only_wheat_and_small_straw_line():
    mod = _load("wheat_field")
    farm = _farm(quads=("NW", "NE", "SW"), money=2000.0)
    plan = mod._wheat_farm_plan()
    _, crop_map, _, _ = mod._field_alloc(
        farm, 8, {**mod.BASE_PRICE, "WHEAT": 33}, plan)
    assert not crop_map["MELON"]
    assert not crop_map["CARROT"]
    assert len(crop_map["STRAWBERRY"]) <= mod.WHEAT_FARM_STRAW_CAP
    assert len(crop_map["WHEAT"]) <= mod.WHEAT_FARM_WHEAT_CAP


def test_wheat_farm_seed_orders_follow_plan_cap_and_plant_deadline():
    mod = _load("wheat_seed")
    farm = _farm(quads=("NW", "NE", "SW"), money=2000.0)
    private = {"shed": {}, "seeds": {"WHEAT": 4}, "inventories": [{}]}
    obs = _obs(mod, day=8, farm=farm, private=private)
    plan = {**mod._wheat_farm_plan(), "wheat_total_cap": 28}

    orders = mod._market_orders(obs, farm, private, 8, 0, 12, plan)
    wheat_seed = [order for order in orders
                  if order[:2] == ["BUY_SEED", "WHEAT"]]
    assert wheat_seed == [["BUY_SEED", "WHEAT", 24]]

    late = mod._market_orders(obs, farm, private,
                              mod.PLANT_LAST_DAY["WHEAT"] + 1, 0, 12, plan)
    assert not any(order[:2] == ["BUY_SEED", "WHEAT"] for order in late)


def test_wheat_farm_same_turn_buys_preserve_hold_cash():
    mod = _load("wheat_cash")
    farm = _farm(quads=("NW", "NE", "SW"), money=1200.0)
    private = {"shed": {}, "seeds": {"WHEAT": 4}, "inventories": [{}]}
    obs = _obs(mod, day=8, farm=farm, private=private)
    obs["market"]["prices"]["WHEAT"] = 36
    plan = mod._wheat_farm_plan()

    orders = mod._market_orders(obs, farm, private, 8, 12, 12, plan)
    feed = sum(order[2] for order in orders
               if order[:2] == ["BUY_PRODUCT", "WHEAT"])
    seeds = sum(order[2] for order in orders
                if order[:2] == ["BUY_SEED", "WHEAT"])
    projected = farm["money"] - feed * 86 - seeds * mod.CROPS["WHEAT"]["seed"]
    assert projected >= mod.WHEAT_FARM_HOLD_CASH


def test_wheat_farm_herd_ceiling_disables_npv_extension():
    mod = _load("wheat_herd")
    farm = _farm(quads=("NW", "NE", "SW"), money=5000.0)
    private = {"shed": {"WHEAT": 40}, "seeds": {"WHEAT": 32},
               "inventories": [{}]}
    obs = _obs(mod, day=12, farm=farm, private=private)
    obs["market"]["prices"].update({"MILK": 300, "WOOL": 300})
    obs["town"] = {"unlocked_shops": ["PIZZA_SHOP"] * 8}

    orders = mod._market_orders(
        obs, farm, private, 12, 14, 14, mod._wheat_farm_plan())
    assert not any(order[0] == "BUY_ANIMAL" for order in orders)


def test_wheat_seed_supply_buys_to_replant_cycle():
    # v9-W1 (round-5 online forensics FM-R5-1): the legacy <6->buy-12
    # cadence let the feed floor decay to zero by d20 in every round-5
    # game; seeds now refill to the standing DEFENSIVE cap each cycle.
    mod = _load("wheat_supply")

    def farm_with(wheat, money=5000.0):
        farm = _farm(quads=("NW", "NE", "SW"), money=money)
        placed = 0
        for row in farm["tiles"]:
            for x, tile in enumerate(row):
                if tile is None and placed < wheat:
                    row[x] = {"kind": "PLANT", "crop": "WHEAT",
                              "planted_day": 8, "yield_units": 1}
                    placed += 1
        return farm

    def orders_for(farm, day=10, wheat_price=33, seeds=None):
        obs = {"player": 0, "day": day, "hour": 0,
               "market": {"prices": {**mod.BASE_PRICE, "WHEAT": wheat_price}},
               "town": {"unlocked_shops": []},
               "farms": [farm, farm],
               "private": {"shed": {}, "seeds": seeds or {},
                           "inventories": [{}]}}
        out = mod._market_orders(obs, farm, obs["private"], day,
                                 animals_to_feed=8, herd_total=12,
                                 plan=dict(mod._DEFENSIVE_PLAN))
        return [o for o in out if o[:2] == ["BUY_SEED", "WHEAT"]]

    # cheap wheat (<30): the v7.2 legacy cadence stands byte-identical
    assert orders_for(farm_with(10), wheat_price=25) == [["BUY_SEED", "WHEAT", 12]]
    assert not orders_for(farm_with(10), wheat_price=25, seeds={"WHEAT": 6})
    assert not orders_for(farm_with(10), wheat_price=29, seeds={"WHEAT": 17})
    # the v9.2 maintenance band starts at 30: cap 18, 10 alive, empty
    # pocket -> the 12 floor binds (want 8); stocked pocket sizes to want
    assert orders_for(farm_with(10), wheat_price=30) == [["BUY_SEED", "WHEAT", 12]]
    assert orders_for(farm_with(10), wheat_price=30, seeds={"WHEAT": 6}) == \
        [["BUY_SEED", "WHEAT", 2]]
    # dear wheat 45 -> cap 30; empty field, rich wallet -> batch ceiling 24
    assert orders_for(farm_with(0), wheat_price=45) == [["BUY_SEED", "WHEAT", 24]]
    # the 35-41 ladder bump: cap 22, 10 alive, empty pocket -> 12
    assert orders_for(farm_with(10), wheat_price=36) == [["BUY_SEED", "WHEAT", 12]]
    # the d0-2 budget belongs to the herd: at most 12
    assert orders_for(farm_with(0), day=1, wheat_price=45) == [["BUY_SEED", "WHEAT", 12]]
    # working capital: a 100-coin wallet still buys 8; sub-30 buys nothing
    assert orders_for(farm_with(10, money=100.0), wheat_price=45) == \
        [["BUY_SEED", "WHEAT", 8]]
    assert not orders_for(farm_with(10, money=25.0), wheat_price=45)
    # past the last productive window: no order
    assert not orders_for(farm_with(10), day=24)


def test_agent_v9_loads_as_independent_callable():
    mod = _load("load")
    assert callable(mod.agent)
    assert mod.__file__.replace("\\", "/").endswith("agent_v9/main.py")
    assert mod.TELEMETRY_ENABLED is True
    assert hasattr(mod, "telemetry_snapshot")


def test_reset_telemetry_clears_sink_reference():
    mod = _load("reset_sink")
    events = []
    mod.set_telemetry_sink(events.append)
    mod.reset_telemetry()
    mod.agent(copy.deepcopy(_obs(mod)))
    assert not events


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


def test_tour_bonus_favors_route_head_over_later_same_sector_tasks():
    mod = _load("tour_bonus")
    farm = _farm(quads=("NW",), farmer=(1, 1), hands=((2, 1),))
    obs = _obs(mod, farm=farm)
    head = _task(2, 2, ["WATER"], value=100, key=("t0", 2, 2))
    tail = _task(4, 1, ["WATER"], value=100, key=("t1", 4, 1))
    routed, _ = mod._route_tasks(obs, farm, obs["private"], 6, [head, tail])
    soft = {task["key"]: task["_v9_soft"].get(0, 0.0) for task in routed}
    assert soft[("t0", 2, 2)] == soft[("t1", 4, 1)] + mod.V9_TOUR_DECAY
    red = _task(1, 1, ["FEED"], value=10, red=True, need="WHEAT",
                key=("r", 1, 1))
    routed_red, _ = mod._route_tasks(obs, farm, obs["private"], 7,
                                     [head, tail, red])
    for task in routed_red:
        if task.get("red"):
            assert not task.get("_v9_soft")


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
