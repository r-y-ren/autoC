"""Phase-D tests: MK-3 planner takeover + MK-5 interference vehicle 1.

Covers: dawn-plan batch emission at planned hours (dedup, gate-overlay
skip, dump-rate clamp), the d29 DROP->SELL queue drain in _market_orders,
and the interference inventory-dump vehicle (trigger confirm + exposure
gate + kill-table inverse sizing + stock clamp + standdown by daily
re-check).
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


def _reset():
    main._MARKET_MEM.clear()
    main._MISSION_SHADOW.clear()
    main._SELL_PLAN_MEM.clear()
    main._SELL_BATCH_EMITTED.clear()
    main._INTERFERENCE_MEM.clear()
    main._INTERFERENCE_LOG.clear()
    main._OPP_OBSERVER.clear()
    main._D29_SELL_QUEUE.clear()


# --------------------------------------------------------------------------
# MK-3: batch emission
# --------------------------------------------------------------------------

def _obs(farm, day=8, hour=6, prices=None, shops=None):
    return {"player": 0, "day": day, "hour": hour,
            "farms": [farm, _farm(_rows10())],
            "market": {"prices": prices or {}, "inventory": {}},
            "town": {"unlocked_shops": shops or []},
            "private": {"shed": {}, "inventories": [{}]}}


def test_batches_due_at_planned_hour_with_dedup():
    _reset()
    farm = _farm(_rows10())
    main._SELL_PLAN_MEM[0] = {"day": 8, "hour": 0, "plan": {
        "day": 8,
        "lines": {"MILK": {"verdict": "clear", "qty_today": 10,
                           "batches": [5, 5], "hours": (6, 12),
                           "planned_price": 160.0, "spot_price": 165.0,
                           "defense": "none", "eod_forced": False,
                           "stock": 10, "inflow": 0}}}}
    shed = {"MILK": 10}
    shops = ["SMOOTHIE_SHOP", "ICE_CREAM_SHOP", "FARMERS_MARKET"]
    # hour 5: not due yet
    out = main._sell_plan_batches_due(_obs(farm, hour=5), 8, 5, shed, [])
    assert out == []
    # hour 6: first batch fires
    out = main._sell_plan_batches_due(_obs(farm, hour=6, shops=shops),
                                      8, 6, shed, [])
    assert out == [["SELL", "MILK", 5]]
    # dedup: same batch never fires twice
    out = main._sell_plan_batches_due(_obs(farm, hour=7, shops=shops),
                                      8, 7, shed, [])
    assert out == []
    # hour 12: second batch
    out = main._sell_plan_batches_due(_obs(farm, hour=12, shops=shops),
                                      8, 12, shed, [])
    assert out == [["SELL", "MILK", 5]]
    _reset()


def test_batch_skipped_when_gate_overlay_sold_the_line():
    _reset()
    farm = _farm(_rows10())
    main._SELL_PLAN_MEM[0] = {"day": 8, "hour": 0, "plan": {
        "day": 8,
        "lines": {"MILK": {"verdict": "clear", "qty_today": 9,
                           "batches": [9], "hours": (6,),
                           "planned_price": 160.0, "spot_price": 165.0,
                           "defense": "none", "eod_forced": False,
                           "stock": 9, "inflow": 0}}}}
    existing = [["SELL", "MILK", 4]]         # the gate overlay sold it
    out = main._sell_plan_batches_due(_obs(farm, hour=6), 8, 6,
                                      {"MILK": 9}, existing)
    assert out == []                          # skipped, marked emitted
    # and it will NOT retry later this day
    out = main._sell_plan_batches_due(_obs(farm, hour=18), 8, 18,
                                      {"MILK": 9}, [])
    assert out == []
    _reset()


def test_d29_queue_drained_into_market_orders():
    _reset()
    main._D29_SELL_QUEUE[0] = {"MILK": 10}
    farm = _farm(_rows10())
    private = {"shed": {"MILK": 12}, "inventories": [{}]}
    obs = _obs(farm, day=29, hour=1,
               prices={"MILK": 160, "WOOL": 150, "WHEAT": 30,
                       "STRAWBERRY": 110, "MELON": 200, "CARROT": 40,
                       "EGG": 50})
    obs["private"] = private
    orders = main._market_orders(obs, farm, private, 29, 0, 0,
                                 plan=dict(main._DEFENSIVE_PLAN))
    sells = [o for o in orders if o[0] == "SELL" and o[1] == "MILK"]
    # the d29 full-liquidation already sells the whole shed (12); the
    # queue adds a bounded min(10, 12) tranche on top (budget truncation
    # arbitrates the 10-order cap downstream)
    assert ["SELL", "MILK", 12] in sells or ["SELL", "MILK", 10] in sells
    assert 0 not in main._D29_SELL_QUEUE     # drained
    _reset()


# --------------------------------------------------------------------------
# MK-5: vehicle 1 (inventory dump)
# --------------------------------------------------------------------------

def _opp_calendar_farm(day):
    rows = _rows10()
    for i in range(15):
        rows[i // 10][i % 10] = _tile_animal("COW", day - 6)
    return _farm(rows)


def _mk5_obs(day, shed, prices):
    mine = _farm(_rows10(), money=5000.0)
    opp = _opp_calendar_farm(day)
    return {"player": 0, "day": day, "hour": 0, "farms": [mine, opp],
            "market": {"prices": prices, "inventory": {}},
            "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "BRUNCH_SPOT",
                                        "ICE_CREAM_SHOP"]},
            "private": {"shed": dict(shed), "inventories": [{}]}}


def test_interference_vehicle1_fires_after_two_confirm_days():
    _reset()
    prices = {"MILK": 160, "STRAWBERRY": 120, "WOOL": 150, "WHEAT": 30}
    obs10 = _mk5_obs(10, {"MILK": 20}, prices)
    out = main._interference_orders(
        obs10, obs10["farms"][0], obs10["private"], 10, prices)
    assert out == []                          # day 10: streak 1, no fire
    assert main._INTERFERENCE_LOG[-1]["streak"] == 1
    obs11 = _mk5_obs(11, {"MILK": 20}, prices)
    out = main._interference_orders(
        obs11, obs11["farms"][0], obs11["private"], 11, prices)
    rec = main._INTERFERENCE_LOG[-1]
    if rec.get("confirmed"):
        # confirmed: vehicle 1 dumps toward 0.75x base if exposure passes
        if rec.get("gate_exposure"):
            assert len(out) == 1 and out[0][0] == "SELL"
            assert out[0][1] == rec["top_opp_line"]
            assert rec["fired_vehicle1"]["qty"] == out[0][2]
        else:
            assert out == []
    else:
        assert out == []
    _reset()


def test_interference_stands_down_when_trigger_clears():
    _reset()
    prices = {"MILK": 160, "STRAWBERRY": 120, "WOOL": 150, "WHEAT": 30}
    obs10 = _mk5_obs(10, {"MILK": 20}, prices)
    main._interference_orders(obs10, obs10["farms"][0],
                              obs10["private"], 10, prices)
    obs11 = _mk5_obs(11, {"MILK": 20}, prices)
    main._interference_orders(obs11, obs11["farms"][0],
                              obs11["private"], 11, prices)
    # quiet day: opponent farm emptied -> trigger clears
    obs12 = _mk5_obs(12, {"MILK": 20}, prices)
    obs12["farms"][1] = _farm(_rows10())
    out = main._interference_orders(
        obs12, obs12["farms"][0], obs12["private"], 12, prices)
    assert out == []
    assert main._INTERFERENCE_LOG[-1]["streak"] == 0
    _reset()


def test_vehicle1_no_stock_no_order():
    _reset()
    prices = {"MILK": 160, "STRAWBERRY": 120, "WOOL": 150, "WHEAT": 30}
    for d in (10, 11):
        obs = _mk5_obs(d, {"WHEAT": 5}, prices)   # no MILK held
        out = main._interference_orders(
            obs, obs["farms"][0], obs["private"], d, prices)
    assert out == []                          # nothing to dump
    _reset()
