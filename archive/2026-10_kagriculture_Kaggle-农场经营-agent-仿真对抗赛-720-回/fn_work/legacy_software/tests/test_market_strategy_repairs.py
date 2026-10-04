"""Regression tests for market strategy execution repairs."""
import importlib
import os
import sys

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE, "kaggle_simulations", "agent"))
main = importlib.import_module("main")


def _rows(n=10):
    return [[None] * n for _ in range(n)]


def _farm(tiles=None, money=5000.0, hands=None):
    return {"tiles": tiles if tiles is not None else _rows(),
            "money": money, "hands": [list(x) for x in (hands or [])],
            "farmer": [4, 4], "unlocked_quadrants": ["NW"]}


def _reset():
    main._MARKET_MEM.clear()
    main._SELL_PLAN_MEM.clear()
    main._SELL_BATCH_EMITTED.clear()
    main._EOD_SELL_EMITTED.clear()
    main._MISSION_SHADOW.clear()
    main._STATE.clear()
    main._D29_SELL_QUEUE.clear()
    if hasattr(main, "_SELL_BATCH_ORDER_KEYS"):
        main._SELL_BATCH_ORDER_KEYS.clear()
    if hasattr(main, "_EOD_SELL_ORDER_KEYS"):
        main._EOD_SELL_ORDER_KEYS.clear()
    if hasattr(main, "_INTERFERENCE_ORDER_KEYS"):
        main._INTERFERENCE_ORDER_KEYS.clear()
    if hasattr(main, "_LINEAR_PRESSURE_MEM"):
        main._LINEAR_PRESSURE_MEM.clear()
    main._INTERFERENCE_MEM.clear()
    main._INTERFERENCE_LOG.clear()


def _obs(farm, day=8, hour=0, shops=None, prices=None, private=None,
         opponent=None):
    return {"player": 0, "day": day, "hour": hour,
            "farms": [farm, opponent or _farm()],
            "market": {"prices": prices or {}, "inventory": {}},
            "town": {"unlocked_shops": shops or []},
            "private": private or {"shed": {}, "inventories": [{}]}}


def test_sell_plan_batches_preserve_remainder():
    _reset()
    farm = _farm()
    obs = _obs(farm, prices={"MILK": 160},
               shops=["SMOOTHIE_SHOP", "ICE_CREAM_SHOP"])
    private = {"shed": {"MILK": 10}, "inventories": [{}]}
    line = main._sell_plan_dawn(obs, farm, private, 8)["lines"]["MILK"]
    assert line["qty_today"] == sum(line["batches"]) == 10
    assert line["batches"] == [4, 3, 3]


def test_rejected_planner_batch_is_retried_after_budget_pass():
    _reset()
    farm = _farm()
    obs = _obs(farm, day=8, hour=6, shops=["SMOOTHIE_SHOP"],
               prices={"MILK": 160})
    main._SELL_PLAN_MEM[0] = {"day": 8, "hour": 0, "plan": {
        "day": 8, "lines": {"MILK": {
            "verdict": "clear", "qty_today": 5, "batches": [5],
            "hours": (6,), "planned_price": 160, "stock": 5}}}}
    shed = {"MILK": 5}
    first = main._sell_plan_batches_due(obs, 8, 6, shed, [])
    assert first == [["SELL", "MILK", 5]]
    blockers = [["SELL", "WHEAT", 1] for _ in range(10)]
    source = blockers + first
    budget = main.plan_market_orders(
        source, 0, 15, max_orders=10,
        shed_stock={"WHEAT": 10, "MILK": 5},
        market_inventory={"WHEAT": 10000, "MILK": 10000})
    main._finalize_sell_plan_batches(0, 8, source, budget)
    assert (0, 8, "MILK", 0) not in main._SELL_BATCH_EMITTED
    second = main._sell_plan_batches_due(obs, 8, 7, shed, [])
    assert second == [["SELL", "MILK", 5]]


def test_no_shop_still_has_town_center_absorption():
    assert main._town_daily_demand([])["MILK"] == 1
    _reset()
    farm = _farm()
    obs = _obs(farm, prices={"MILK": 160}, shops=[])
    private = {"shed": {"MILK": 5}, "inventories": [{}]}
    line = main._sell_plan_dawn(obs, farm, private, 8)["lines"]["MILK"]
    assert line["qty_today"] <= 1


def test_opportunity_wheat_buy_does_not_require_animals():
    _reset()
    farm = _farm(money=5000.0)
    private = {"shed": {}, "seeds": {}, "inventories": [{}]}
    obs = _obs(farm, day=8, prices={"WHEAT": 22}, private=private)
    orders = main._market_orders(obs, farm, private, 8, 0, 0,
                                 plan=dict(main._DEFENSIVE_PLAN))
    assert any(o[:2] == ["BUY_PRODUCT", "WHEAT"] for o in orders)


def test_interference_streak_is_idempotent_and_budget_is_hard_gate():
    _reset()
    opp_tiles = _rows()
    for i in range(15):
        opp_tiles[i // 10][i % 10] = {
            "kind": "PASTURE", "animal": "COW", "placed_day": 4,
            "yield_units": 0, "consecutive_unfed": 0,
            "fed_today": True, "cared_today": True}
    mine = _farm(hands=[])
    obs10 = _obs(mine, day=10, shops=["SMOOTHIE_SHOP"],
                 prices={"MILK": 160}, private={"shed": {"MILK": 20},
                 "inventories": [{}]}, opponent=_farm(opp_tiles))
    main._interference_shadow(obs10, mine, 10, obs10["market"]["prices"])
    main._interference_shadow(obs10, mine, 10, obs10["market"]["prices"])
    assert main._INTERFERENCE_MEM[0]["streak"] == 1
    assert len(main._INTERFERENCE_LOG) == 1
    rec = main._INTERFERENCE_LOG[-1]
    rec["confirmed"] = True
    rec["gate_exposure"] = True
    rec["gate_budget"] = False
    assert main._interference_orders(obs10, mine, obs10["private"],
                                     10, obs10["market"]["prices"]) == []


def test_sell_plan_does_not_promise_unharvested_tile_yield():
    _reset()
    tiles = _rows()
    tiles[0][0] = {"kind": "PLANT", "crop": "MELON", "planted_day": 0,
                   "yield_units": 6, "watered_today": True}
    farm = _farm(tiles=tiles)
    private = {"shed": {}, "inventories": [{}]}
    obs = _obs(farm, day=12, prices={"MELON": 250}, private=private)
    plan = main._sell_plan_dawn(obs, farm, private, 12)
    assert "MELON" not in plan["lines"]


def test_linear_pressure_gets_one_day_short_hold_then_releases():
    _reset()
    farm = _farm()
    obs = _obs(farm, day=8, prices={"MILK": 120},
               shops=["SMOOTHIE_SHOP"], private={
                   "shed": {"MILK": 10}, "inventories": [{}]})
    main._market_flow(0, 7, {"MILK": 160})
    first = main._sell_plan_shadow_update(
        0, 8, 0, obs, farm, obs["private"], main._DEFENSIVE_PLAN)
    repeated = main._sell_plan_shadow_update(
        0, 8, 12, obs, farm, obs["private"], main._DEFENSIVE_PLAN)
    assert first["lines"]["MILK"]["defense"] == "short_hold"
    assert first["lines"]["MILK"]["verdict"] == "hold"
    assert repeated is first
    assert repeated["lines"]["MILK"]["batches"] == []
    main._SELL_PLAN_MEM.clear()
    obs["day"] = 9
    second = main._sell_plan_dawn(obs, farm, obs["private"], 9)
    assert second["lines"]["MILK"]["verdict"] == "clear"
    assert second["lines"]["MILK"]["batches"]


def test_hold_plan_suppresses_legacy_sells_until_price_crash():
    _reset()
    farm = _farm(money=5000.0)
    private = {"shed": {"MILK": 10}, "seeds": {}, "inventories": [{}]}
    obs = _obs(farm, day=8, hour=6, prices={"MILK": 120}, private=private)
    main._SELL_PLAN_MEM[0] = {"day": 8, "hour": 0, "plan": {
        "day": 8, "lines": {"MILK": {
            "verdict": "hold", "qty_today": 0, "batches": [],
            "hours": (6, 12, 18), "spot_price": 120,
            "planned_price": 130}}}}
    orders = main._market_orders(obs, farm, private, 8, 0, 0,
                                 plan=dict(main._DEFENSIVE_PLAN))
    assert not [o for o in orders if o[:2] == ["SELL", "MILK"]]
    obs["market"]["prices"]["MILK"] = 90
    orders = main._market_orders(obs, farm, private, 8, 0, 0,
                                 plan=dict(main._DEFENSIVE_PLAN))
    assert [o for o in orders if o[:2] == ["SELL", "MILK"]]


def test_opportunity_wheat_with_animals_reaches_four_day_target():
    _reset()
    farm = _farm(money=5000.0)
    private = {"shed": {"WHEAT": 2}, "seeds": {}, "inventories": [{}]}
    obs = _obs(farm, day=8, prices={"WHEAT": 22}, private=private)
    orders = main._market_orders(obs, farm, private, 8, 5, 5,
                                 plan=dict(main._DEFENSIVE_PLAN))
    wheat = [o for o in orders if o[:2] == ["BUY_PRODUCT", "WHEAT"]]
    assert wheat and sum(o[2] for o in wheat) >= 1
    assert all(o[2] <= main.BUY_CHUNK_MAX_UNITS for o in wheat)


def test_eod_sell_retries_when_budget_truncates_merged_order():
    _reset()
    main._EOD_SELL_EMITTED.clear()
    if hasattr(main, "_EOD_SELL_ORDER_KEYS"):
        main._EOD_SELL_ORDER_KEYS.clear()
    farm = _farm()
    private = {"shed": {"MILK": 5}, "seeds": {}, "inventories": [{}]}
    obs = _obs(farm, day=8, hour=6, prices={"MILK": 160}, private=private)
    main._MISSION_SHADOW[0] = {"day": 8, "hour": 0, "mission": {
        "events": [{"h": 6, "op": "SELL", "item": "MILK", "qty": 5,
                    "why": "eod_budget"}]}}
    generated = main._market_orders(obs, farm, private, 8, 0, 0,
                                    plan=dict(main._DEFENSIVE_PLAN))
    blockers = [["SELL", "WHEAT", 1] for _ in range(10)]
    source = blockers + generated
    budget = main.plan_market_orders(
        source, 0, 15, max_orders=10,
        shed_stock={"WHEAT": 10, "MILK": 5},
        market_inventory={"WHEAT": 10000, "MILK": 10000})
    main._finalize_sell_plan_batches(0, 8, source, budget)
    assert not main._EOD_SELL_EMITTED
    retry = main._market_orders(obs, farm, private, 8, 0, 0,
                                plan=dict(main._DEFENSIVE_PLAN))
    assert [o for o in retry if o[:2] == ["SELL", "MILK"]]


def test_sell_merge_preserves_planner_source_for_finalize():
    _reset()
    farm = _farm()
    private = {"shed": {"MILK": 5}, "seeds": {}, "inventories": [{}]}
    obs = _obs(farm, day=8, hour=6, prices={"MILK": 160}, private=private)
    main._SELL_PLAN_MEM[0] = {"day": 8, "hour": 0, "plan": {
        "day": 8, "lines": {"MILK": {
            "verdict": "clear", "qty_today": 5, "batches": [5],
            "hours": (6,), "planned_price": 160, "stock": 5}}}}
    generated = main._market_orders(obs, farm, private, 8, 0, 0,
                                    plan=dict(main._DEFENSIVE_PLAN))
    budget = main.plan_market_orders(
        generated, 5000, 5, shed_stock={"MILK": 5},
        market_inventory={"MILK": 10000})
    main._finalize_sell_plan_batches(0, 8, generated, budget)
    assert main._SELL_BATCH_EMITTED[(0, 8, "MILK", 0)] == "committed"
