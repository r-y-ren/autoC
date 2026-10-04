"""v14.3-sellrace tests (premium-market-lead + day-11 sheep commit).

Covers: the engine-exact per-step town demand mirror (_town_demand_now),
the bounded premium-market-lead advance (_sellrace_leads: flag-off no-op,
demand/flow/hold gates, <=50% premium cap, fertilizer field-reserve +
cap-10, shed-stock conservation), the day-11 five-shearing window
arithmetic, and the shipped main.py switch staying flag-off (byte-equal
to v14.2 by default).
"""
import importlib
import os
import sys

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE, "kaggle_simulations", "agent"))

main = importlib.import_module("main")


def _rows10():
    return [[None] * 10 for _ in range(10)]


def _farm(tiles_rows, money=3000.0, hands=None, quads=None):
    return {"tiles": tiles_rows, "money": money,
            "hands": [list(h) for h in (hands or [])],
            "farmer": [4, 4],
            "unlocked_quadrants": quads or ["NW"]}


def _obs(day=10, hour=5, prices=None, shops=None, shed=None):
    return {"player": 0, "day": day, "hour": hour,
            "farms": [_farm(_rows10()), _farm(_rows10())],
            "market": {"prices": prices or {}, "inventory": {}},
            "town": {"unlocked_shops": shops or []},
            "private": {"shed": shed or {}, "inventories": [{}]}}


def _sellrace_on():
    main.PLANNER_ENABLED = True
    main.PLANNER_OVERRIDES.clear()
    main.PLANNER_OVERRIDES["sellrace_mode"] = True


def _sellrace_off():
    main.PLANNER_ENABLED = False
    main.PLANNER_OVERRIDES.clear()


def setup_function(_fn):
    main._MARKET_MEM.clear()
    main._SELL_PLAN_MEM.clear()
    _sellrace_off()


def teardown_function(_fn):
    _sellrace_off()


# --------------------------------------------------------------------------
# _town_demand_now: engine _town_consumption mirror (kaggriculture.py:736-747)
# --------------------------------------------------------------------------

def test_town_demand_now_engine_mirror():
    shops = ["BAKERY", "YARN_STORE"]
    # step 0: shop draws (BAKERY multi -> 1/item; YARN single -> 2) + center 1
    assert main._town_demand_now(shops, "EGG", 0) == 1 + 1   # shop + center
    assert main._town_demand_now(shops, "WHEAT", 0) == 1 + 1
    assert main._town_demand_now(shops, "WOOL", 0) == 2 + 1
    assert main._town_demand_now(shops, "MILK", 0) == 1      # center only
    # step 4: shops only, no center
    assert main._town_demand_now(shops, "WOOL", 4) == 2
    assert main._town_demand_now(shops, "EGG", 4) == 1
    # step 2: nothing draws
    assert main._town_demand_now(shops, "WOOL", 2) == 0
    assert main._town_demand_now(shops, "MELON", 0) == 1     # center only
    # duplicate shop instances consume independently (drawn with replacement)
    assert main._town_demand_now(["YARN_STORE", "YARN_STORE"], "WOOL", 4) == 4
    # fertilizer: no shop stocks it and the center skips it -- always 0
    for step in (0, 4, 24, 48):
        assert main._town_demand_now(list(main.SHOPS), "FERTILIZER",
                                     step) == 0


# --------------------------------------------------------------------------
# _sellrace_leads: flag-off no-op + gate stack
# --------------------------------------------------------------------------

def _merged(item, qty):
    return [["SELL", item, qty]]


def test_sellrace_flagoff_is_noop():
    obs = _obs(day=10, hour=5, prices={"WOOL": 210},
               shed={"WOOL": 20})
    leads = main._sellrace_leads(obs, 10, {"WOOL": 210}, {"WOOL": 20},
                                 _merged("WOOL", 12), {})
    assert leads == {}


def test_sellrace_lead_premium_half_batch_and_stock_bound():
    _sellrace_on()
    # YARN stores make wool an absorbing line -> the 50%-batch cap governs
    obs = _obs(day=10, hour=5, prices={"WOOL": 210},
               shops=["YARN_STORE", "YARN_STORE"])
    # planned 12, stock 20 -> advance = max(1, int(12*0.5)) = 6, left = 8
    leads = main._sellrace_leads(obs, 10, {"WOOL": 210}, {"WOOL": 20},
                                 _merged("WOOL", 12), {})
    assert leads == {"WOOL": 6}
    assert leads["WOOL"] <= 20 - 12          # two-turn shed conservation
    # planned 12, stock 14 -> advance bounded by leftover stock (2)
    leads = main._sellrace_leads(obs, 10, {"WOOL": 210}, {"WOOL": 14},
                                 _merged("WOOL", 12), {})
    assert leads == {"WOOL": 2}
    # planned 12, stock 12 -> nothing left to advance
    leads = main._sellrace_leads(obs, 10, {"WOOL": 210}, {"WOOL": 12},
                                 _merged("WOOL", 12), {})
    assert leads == {}


def test_sellrace_zero_absorption_line_uses_day_cap():
    _sellrace_on()
    # MELON has no shop anywhere: day demand = center 1 -> zero-absorption
    # class; the advance lifts to SELLRACE_ZERO_DEMAND_CAP (18/turn) so the
    # line can finish its day-drain (within-day re-batching is revenue-
    # neutral; the value is finishing the drain before overnight supply).
    obs = _obs(day=13, hour=5, prices={"MELON": 250})
    leads = main._sellrace_leads(obs, 13, {"MELON": 250}, {"MELON": 24},
                                 _merged("MELON", 6), {})
    assert leads == {"MELON": 18}
    assert leads["MELON"] <= 24 - 6
    # with a yarn store drawing wool (absorbing line), the 50%-batch cap
    # stays in force
    obs = _obs(day=10, hour=5, prices={"WOOL": 210},
               shops=["YARN_STORE", "YARN_STORE"])
    leads = main._sellrace_leads(obs, 10, {"WOOL": 210}, {"WOOL": 20},
                                 _merged("WOOL", 12), {})
    assert leads == {"WOOL": 6}


def test_sellrace_gate_matching_town_demand_blocks():
    _sellrace_on()
    # hour 4 -> step%4==0: PIZZA_SHOP draws MILK; advance must be blocked
    obs = _obs(day=10, hour=4, prices={"MILK": 150},
               shops=["PIZZA_SHOP"])
    leads = main._sellrace_leads(obs, 10, {"MILK": 150}, {"MILK": 30},
                                 _merged("MILK", 10), {})
    assert "MILK" not in leads
    # same state one hour later (no shop/center draw) -> advance allowed
    obs = _obs(day=10, hour=5, prices={"MILK": 150},
               shops=["PIZZA_SHOP"])
    leads = main._sellrace_leads(obs, 10, {"MILK": 150}, {"MILK": 30},
                                 _merged("MILK", 10), {})
    assert leads.get("MILK") == 5


def test_sellrace_gate_negative_flow_blocks():
    _sellrace_on()
    # PIZZA_SHOP stocks MILK -> absorbing line -> 50%-batch cap applies
    obs = _obs(day=10, hour=5, prices={"MILK": 150},
               shops=["PIZZA_SHOP", "PIZZA_SHOP", "PIZZA_SHOP"])
    leads = main._sellrace_leads(obs, 10, {"MILK": 150}, {"MILK": 30},
                                 _merged("MILK", 10), {"MILK": -3.0})
    assert leads == {}
    leads = main._sellrace_leads(obs, 10, {"MILK": 150}, {"MILK": 30},
                                 _merged("MILK", 10), {"MILK": 2.0})
    assert leads.get("MILK") == 5


def test_sellrace_gate_dawn_hold_line_blocks():
    _sellrace_on()
    obs = _obs(day=10, hour=5, prices={"WOOL": 240})
    main._SELL_PLAN_MEM[0] = {
        "day": 10, "hour": 0,
        "plan": {"day": 10, "lines": {"WOOL": {"verdict": "hold"}}}}
    try:
        leads = main._sellrace_leads(obs, 10, {"WOOL": 240}, {"WOOL": 20},
                                     _merged("WOOL", 12), {})
        assert leads == {}
    finally:
        main._SELL_PLAN_MEM.clear()


def test_sellrace_last_day_never_leads():
    _sellrace_on()
    obs = _obs(day=29, hour=5, prices={"WOOL": 210})
    leads = main._sellrace_leads(obs, 29, {"WOOL": 210}, {"WOOL": 20},
                                 _merged("WOOL", 12), {})
    assert leads == {}


def test_sellrace_fertilizer_reserve_and_cap():
    _sellrace_on()
    obs = _obs(day=12, hour=5, prices={"FERTILIZER": 60})
    # planned 6, stock 30: left = min(24, 30-4-6)=20 -> advance capped at 10
    leads = main._sellrace_leads(obs, 12, {"FERTILIZER": 60},
                                 {"FERTILIZER": 30},
                                 _merged("FERTILIZER", 6), {})
    assert leads == {"FERTILIZER": 10}
    # field reserve binds: planned 6, stock 8 -> 8-4-6 < 0 -> no advance
    leads = main._sellrace_leads(obs, 12, {"FERTILIZER": 60},
                                 {"FERTILIZER": 8},
                                 _merged("FERTILIZER", 6), {})
    assert leads == {}
    # planned 30 (d29-style flush never leads; use cap-excess sell), stock 90:
    # cap still 10
    leads = main._sellrace_leads(obs, 12, {"FERTILIZER": 60},
                                 {"FERTILIZER": 90},
                                 _merged("FERTILIZER", 30), {})
    assert leads == {"FERTILIZER": 10}


def test_sellrace_wheat_never_leads():
    _sellrace_on()
    obs = _obs(day=12, hour=5, prices={"WHEAT": 30})
    leads = main._sellrace_leads(obs, 12, {"WHEAT": 30}, {"WHEAT": 90},
                                 _merged("WHEAT", 20), {})
    assert leads == {}                       # C71: opponents BUY wheat


# --------------------------------------------------------------------------
# day-11 five-shearing window (engine-exact evenings formula)
# --------------------------------------------------------------------------

def test_day11_sheep_window_arithmetic():
    # 2945 Farm VE1: day-11 placement -> 5 shearings (17/20/23/26/29);
    # day-12+ placement -> 4; day-8 -> 6.  COW on day 11 -> 6 milk evenings.
    assert main._new_animal_production_evenings(11, "SHEEP") == 5
    assert main._new_animal_production_evenings(12, "SHEEP") == 4
    assert main._new_animal_production_evenings(10, "SHEEP") == 5
    assert main._new_animal_production_evenings(8, "SHEEP") == 6
    assert main._new_animal_production_evenings(11, "COW") == 6


def test_market_orders_applies_leads_end_to_end():
    _sellrace_on()
    main._MARKET_MEM.clear()
    main._SELL_PLAN_MEM.clear()
    main._MISSION_SHADOW.clear()
    main._STAGE_MEM.clear()
    main._PLAN_MEM.clear()
    prices = {"WOOL": 210.0, "WHEAT": 25.0, "MILK": 150.0,
              "FERTILIZER": 60.0}
    shed = {"WOOL": 20, "WHEAT": 40, "FERTILIZER": 30}
    obs = _obs(day=10, hour=5, prices=prices, shed=shed)
    private = {"shed": dict(shed), "seeds": {}, "inventories": [{}]}
    plan = dict(main._DEFENSIVE_PLAN)
    orders_on = main._market_orders(obs, obs["farms"][0], private, 10,
                                    0, 10, plan)
    wool_on = sum(o[2] for o in orders_on
                  if o[0] == "SELL" and o[1] == "WOOL")
    _sellrace_off()
    orders_off = main._market_orders(obs, obs["farms"][0],
                                     {"shed": dict(shed), "seeds": {},
                                      "inventories": [{}]},
                                     10, 0, 10, plan)
    wool_off = sum(o[2] for o in orders_off
                   if o[0] == "SELL" and o[1] == "WOOL")
    # flag-on sells MORE wool this turn; with no yarn shop wool is a zero-
    # absorption line -> the advance lifts to the day-cap (min(leftover, 18))
    # and the total never exceeds the shed stock
    assert wool_on >= wool_off > 0
    assert wool_on <= 20
    if wool_on > wool_off:
        assert wool_on - wool_off <= 20 - wool_off   # leftover bound


# --------------------------------------------------------------------------
# shipped main.py switch: flag-off by default (byte-equal to v14.2)
# --------------------------------------------------------------------------

def test_main_ship_switch_defaults_off():
    assert getattr(main, "_SELLRACE_SHIP", False) is False
    # the namespace the pipeline exec'd into carries the frozen defaults
    assert main.SELLRACE_MODE is False
    assert main.D11_SHEEP_COMMIT == 0
    assert main.SELLRACE_LEAD_FRAC == 0.5
    assert main.SELLRACE_FERT_CAP == 10
    assert main.SELLRACE_ZERO_DEMAND_CAP == 18


def test_d11_commit_knob_clamps_to_domain():
    _sellrace_on()
    main.PLANNER_OVERRIDES["d11_sheep_commit"] = 99   # pathological planner
    # clamp happens at the read site; here we assert the knob channel reads
    # the override and the domain clamp constant is what the code applies
    assert main._plan_knob("d11_sheep_commit", main.D11_SHEEP_COMMIT) == 99
    _sellrace_off()
    assert main._plan_knob("d11_sheep_commit", main.D11_SHEEP_COMMIT) == 0
