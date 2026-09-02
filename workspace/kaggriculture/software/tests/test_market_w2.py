"""W2 market-strategy tests (market_strategy_design.md v1.1).

Covers: engine-exact BUY_PRODUCT cost model + generation-side affordability
(MS-1.1 committed-spend merge), the MK-2 dawn sell planner shadow (five
rules: contested zero-hood, hold-edge, batch=min(supply,absorption), EOD
wheat-first forcing, line-quota cap; §4.4 defense postures), the fixed MK-4
interference shadow (calendar x min(supply,absorb) x projection, 2-day
confirmation, gate booleans), and the reconciliation aggregation.
"""
import importlib
import os
import sys

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE, "kaggle_simulations", "agent"))

main = importlib.import_module("main")


def _tile_plant(crop, planted_day, yield_units=0):
    return {"kind": "PLANT", "crop": crop, "planted_day": planted_day,
            "yield_units": yield_units, "consecutive_unwatered": 0,
            "watered_today": True}


def _tile_animal(animal, placed_day):
    return {"kind": "PASTURE", "animal": animal, "placed_day": placed_day,
            "yield_units": 0, "consecutive_unfed": 0, "fed_today": True,
            "cared_today": True, "fertilizer_available": False}


def _farm(tiles_rows, money=3000.0, hands=None, quads=None):
    return {"tiles": tiles_rows, "money": money,
            "hands": [list(h) for h in (hands or [])],
            "farmer": [4, 4],
            "unlocked_quadrants": quads or ["NW"]}


def _rows10():
    return [[None] * 10 for _ in range(10)]


def _obs(farm, opp=None, day=8, prices=None, shops=None):
    return {"player": 0, "day": day, "hour": 0,
            "farms": [farm, opp if opp is not None else _farm(_rows10())],
            "market": {"prices": prices or {}, "inventory": {}},
            "town": {"unlocked_shops": shops or []},
            "private": {"shed": {}, "inventories": [{}]}}


def _reset():
    main._MARKET_MEM.clear()
    main._MISSION_SHADOW.clear()
    main._SELL_PLAN_MEM.clear()
    main._INTERFERENCE_MEM.clear()
    main._INTERFERENCE_LOG.clear()
    main._OPP_OBSERVER.clear()


# --------------------------------------------------------------------------
# MS-1.1: engine-exact BUY_PRODUCT cost + affordability
# --------------------------------------------------------------------------

def test_buy_product_cost_matches_simulator():
    for inv in (9500, 10000, 10800, 12000):
        order = [["BUY_PRODUCT", "WHEAT", 5]]
        budget = main.plan_market_orders(
            order, 10.0 ** 9, 0, market_inventory={"WHEAT": inv})
        exact = main.buy_product_cost("WHEAT", 5, {"WHEAT": inv})
        assert abs(budget["committed_spend"] - exact) < 1e-6, inv


def test_affordable_buy_units_is_tight():
    obs = {"market": {"inventory": {"WHEAT": 10800}}}
    budget = 300.0
    units = main._affordable_buy_units("WHEAT", budget, obs)
    cost_n = main.buy_product_cost("WHEAT", units, obs["market"]["inventory"])
    assert cost_n <= budget
    if units > 0:
        extra = main.buy_product_cost("WHEAT", units + 1,
                                      obs["market"]["inventory"])
        assert extra > budget


# --------------------------------------------------------------------------
# MK-2 dawn sell planner (shadow, five rules + defense postures)
# --------------------------------------------------------------------------

def _plan_with(shed, day=8, opp=None, prices=None, shops=None):
    _reset()
    farm = _farm(_rows10())
    obs = _obs(farm, opp=opp, day=day, prices=prices, shops=shops)
    obs["private"] = {"shed": dict(shed), "inventories": [{}]}
    return main._sell_plan_dawn(obs, farm, obs["private"], day)


def test_sell_plan_contested_clears_and_batches_bounded():
    opp = _farm([[_tile_plant("STRAWBERRY", 2) for _ in range(12)]])
    plan = _plan_with({"STRAWBERRY": 9}, opp=opp,
                      prices={"STRAWBERRY": 130},
                      shops=["SMOOTHIE_SHOP", "BRUNCH_SPOT",
                             "ICE_CREAM_SHOP"])
    line = plan["lines"]["STRAWBERRY"]
    assert line["verdict"] == "clear"          # rule 2: contested zero-hood
    absorb = main._town_daily_demand(
        ["SMOOTHIE_SHOP", "BRUNCH_SPOT", "ICE_CREAM_SHOP"]).get(
            "STRAWBERRY", 1)
    assert line["qty_today"] <= max(absorb, 1)  # rule 3: batch <= absorption
    assert sum(line["batches"]) == line["qty_today"]
    assert len(line["batches"]) <= len(main.SELL_PLAN_HOURS)


def test_sell_plan_hold_on_absorption_lift_and_clear_when_flat():
    # rule 1: hold needs the projection to beat spot by HOLD_EDGE -- that
    # only happens under net absorption (a day-over-day price RISE).
    _reset()
    main._market_flow(0, 7, {"MELON": 100})       # yesterday's baseline
    farm = _farm(_rows10())
    obs = _obs(farm, day=8, prices={"MELON": 130})
    obs["private"] = {"shed": {"MELON": 4}, "inventories": [{}]}
    plan = main._sell_plan_dawn(obs, farm, obs["private"], 8)
    line = plan["lines"]["MELON"]
    assert line["planned_price"] >= line["spot_price"] * \
        main.SELL_PLAN_HOLD_EDGE
    assert line["verdict"] == "hold"
    # zero flow: projection == spot -> the carry risk is unpaid -> clear
    plan = _plan_with({"MELON": 4}, prices={"MELON": 130})
    assert plan["lines"]["MELON"]["verdict"] == "clear"


def test_sell_plan_eod_overflow_forces_wheat():
    _reset()
    farm = _farm(_rows10())
    obs = _obs(farm, day=8, prices={"WHEAT": 30})
    obs["private"] = {"shed": {"WHEAT": 20}, "inventories": [{}]}
    main._MISSION_SHADOW[0] = {
        "day": 8, "hour": 0,
        "mission": {"eod": {"overflow": 12}}}
    plan = main._sell_plan_dawn(obs, farm, obs["private"], 8)
    line = plan["lines"]["WHEAT"]
    assert line["verdict"] == "clear" and line["eod_forced"] is True
    assert line["qty_today"] >= 12             # overflow leaves the shed
    main._MISSION_SHADOW.clear()


def test_sell_plan_line_quota_cap():
    shed = {item: 5 for item in
            ("STRAWBERRY", "MELON", "WOOL", "MILK", "CARROT", "EGG")}
    plan = _plan_with(shed, prices={
        # everything above base: all lines read "clear"
        item: int(main.BASE_PRICE[item] * 1.6) for item in shed})
    with_batches = [k for k, v in plan["lines"].items() if v["batches"]]
    assert len(with_batches) <= main.SELL_PLAN_MAX_LINES   # rule 5


def test_sell_plan_defense_postures_by_shape():
    # price dump day-over-day -> POSITIVE flow (glut) = under attack;
    # sq (WOOL) cuts immediately, log (WHEAT) ignores the pressure.
    main._MARKET_MEM.clear()
    main._market_flow(0, 7, {"WOOL": 150, "WHEAT": 30})
    _reset_seed = dict(main._MARKET_MEM.get(0) or {})
    main._MARKET_MEM.clear()
    main._MARKET_MEM[0] = _reset_seed            # yesterday's baseline
    farm = _farm(_rows10())
    obs = _obs(farm, day=8, prices={"WOOL": 110, "WHEAT": 24})
    obs["private"] = {"shed": {"WOOL": 6, "WHEAT": 10}, "inventories": [{}]}
    plan = main._sell_plan_dawn(obs, farm, obs["private"], 8)
    assert plan["lines"]["WOOL"]["defense"] == "cut"
    assert plan["lines"]["WOOL"]["verdict"] == "clear"
    assert plan["lines"]["WHEAT"]["defense"] == "ignore"
    main._MARKET_MEM.clear()


def test_sell_plan_shadow_registry_once_per_day():
    _reset()
    farm = _farm(_rows10())
    obs = _obs(farm, day=8, prices={"WHEAT": 30})
    p1 = main._sell_plan_shadow_update(0, 8, 0, obs, farm,
                                       {"shed": {"WHEAT": 5}}, None)
    p2 = main._sell_plan_shadow_update(0, 8, 12, obs, farm,
                                       {"shed": {"WHEAT": 5}}, None)
    assert p1 is p2
    assert main.sell_plan_shadow(0)["day"] == 8


# --------------------------------------------------------------------------
# MK-4 interference shadow (v1.1 fixed formula, still inert)
# --------------------------------------------------------------------------

def _opp_calendar_farm(day):
    rows = _rows10()
    for i in range(15):                     # 15 cows, in-window milk flow
        rows[i // 10][i % 10] = _tile_animal("COW", day - 6)
    return _farm(rows)


def test_interference_confirm_days_and_reset():
    _reset()
    shops = ["SMOOTHIE_SHOP", "BRUNCH_SPOT", "ICE_CREAM_SHOP"]
    obs = _obs(_farm(_rows10()), opp=_opp_calendar_farm(10), day=10,
               prices={"MILK": 160, "STRAWBERRY": 120, "WOOL": 150},
               shops=shops)
    assert main._interference_shadow(obs, obs["farms"][0], 10,
                                     obs["market"]["prices"]) is False
    rec1 = main.interference_shadow_log()[-1]
    assert rec1["raw_trigger"] is True and rec1["streak"] == 1
    assert rec1["confirmed"] is False          # needs 2 consecutive days
    obs11 = _obs(_farm(_rows10()), opp=_opp_calendar_farm(11), day=11,
                 prices={"MILK": 160, "STRAWBERRY": 120, "WOOL": 150},
                 shops=shops)
    main._interference_shadow(obs11, obs11["farms"][0], 11,
                              obs11["market"]["prices"])
    rec2 = main.interference_shadow_log()[-1]
    assert rec2["streak"] == 2 and rec2["confirmed"] is True
    # Phase-D: MK-5 vehicle 1 (inventory dump) is ARMED -- the shadow's
    # return now means "confirmed and armed"; the fire/no-fire decision
    # lives in _interference_orders' three gates
    assert rec2["armed"] is True
    # a quiet day resets the streak
    obs12 = _obs(_farm(_rows10()), opp=_farm(_rows10()), day=12,
                 prices={"MILK": 160, "STRAWBERRY": 120, "WOOL": 150},
                 shops=shops)
    main._interference_shadow(obs12, obs12["farms"][0], 12,
                              obs12["market"]["prices"])
    rec3 = main.interference_shadow_log()[-1]
    assert rec3["streak"] == 0 and rec3["confirmed"] is False
    # gates + rollout terminal recorded for calibration
    assert "gate_exposure" in rec2 and "gate_budget" in rec2
    assert "r_us_rollout" in rec2 and "r_us_flow" in rec2


# --------------------------------------------------------------------------
# reconciliation aggregation (MK-2 gate instrument, pure function)
# --------------------------------------------------------------------------

def test_reconciliation_summarize():
    spec = importlib.util.spec_from_file_location(
        "spr",
        os.path.join(SOFTWARE, "scripts", "sell_plan_reconciliation.py"))
    spr = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(spr)
    records = {
        "sales": [
            {"item": "MILK", "deviation_pct": -2.0},
            {"item": "MILK", "deviation_pct": 4.0},
            {"item": "WOOL", "deviation_pct": 10.0},
        ],
        "planned_clear": [{"item": "MILK", "sold": True},
                          {"item": "WOOL", "sold": True},
                          {"item": "EGG", "sold": False}],
        "holds": [{"item": "WHEAT", "move_pct": 6.0},
                  {"item": "WHEAT", "move_pct": -2.0}],
    }
    s = spr.summarize(records)
    assert s["sales"] == 3
    assert s["coverage"] == round(2 / 3, 4)
    assert s["price_deviation_pct"]["n"] == 3
    assert s["by_item_deviation_pct"]["MILK"]["n"] == 2
    assert s["hold_move_pct"]["mean_pct"] == 2.0
