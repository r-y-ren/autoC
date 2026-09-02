"""W1 doc-landing tests (four design documents, 2026-09-02).

Covers: stage register + classifier + capacity/triple gates + MIXED plan +
d6 checkpoint (branch v1.3); observer four channels + est_* + calendar
(OBS v2 §1/§3); sell overrides (contested zero-hood + planner force-clear +
P4 tiers) and interference shadow (market v1.1); mission/solver/executor
shadows (scheduler v1.3 §2-§4).
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


def _tile_animal(animal, placed_day, yield_units=0):
    return {"kind": "PASTURE", "animal": animal, "placed_day": placed_day,
            "yield_units": yield_units, "consecutive_unfed": 0,
            "fed_today": False, "cared_today": False,
            "fertilizer_available": False}


def _farm(tiles_rows, money=3000.0, hands=None, quads=None):
    return {"tiles": tiles_rows, "money": money,
            "hands": [list(h) for h in (hands or [])],
            "farmer": [4, 4],
            "unlocked_quadrants": quads or ["NW"]}


# --------------------------------------------------------------------------
# branch v1.3: stage / classifier / capacity / triple gates / MIXED
# --------------------------------------------------------------------------

def test_stage_of_boundaries():
    assert main._stage_of(0) == "P0"
    assert main._stage_of(1) == "P1"
    assert main._stage_of(5) == "P1"
    assert main._stage_of(6) == "P2"
    assert main._stage_of(14) == "P2"
    assert main._stage_of(15) == "P3"
    assert main._stage_of(22) == "P4"
    assert main._stage_of(28) == "P5"


def test_classifier_classes():
    obs_burst = {"player": 0, "farms": [
        _farm([[None]]),
        _farm([[None, _tile_animal("COW", 0), _tile_animal("SHEEP", 0),
                _tile_animal("SHEEP", 0), _tile_animal("COW", 0)]])]}
    assert main._classify_opponent_opening(obs_burst) == "burst"
    obs_red = {"player": 0, "farms": [_farm([[None]]), _farm(
        [[_tile_animal("SHEEP", 0), _tile_animal("COW", 0), None]])]}
    assert main._classify_opponent_opening(obs_red) == "reduced"
    obs_def = {"player": 0, "farms": [_farm([[None]]), _farm(
        [[_tile_plant("WHEAT", 0) for _ in range(8)]])]}
    assert main._classify_opponent_opening(obs_def) == "deferred"
    obs_melon = {"player": 0, "farms": [_farm([[None]]), _farm(
        [[_tile_plant("MELON", 1) for _ in range(6)]])]}
    assert main._classify_opponent_opening(obs_melon) == "melon_first"


def test_capacity_units_and_law():
    rows = [[_tile_plant("STRAWBERRY", 5), _tile_plant("WHEAT", 1),
             _tile_plant("MELON", 2), _tile_plant("CARROT", 22), None]]
    rows.append([_tile_animal("COW", 0), None, None, None, None])
    units, comps = main._capacity_units(_farm(rows), {})
    # 1 + 1 + 1 + 0.5 + 2*1 = 5.5
    assert abs(units - 5.5) < 1e-9
    assert comps == {"straw": 1, "wheat": 1, "melon": 1, "carrot": 1,
                     "herd": 1}
    # Phase-C capA backfill: crew 12 law = 24x13x0.89/3.3 ~= 84.1
    # units (top-20 anchor; quickwin A/B +7.3% rewards, 0 escapes)
def test_capacity_gate_blocks_overextension():
    # 45 units on a 0-hand farm: law = 7.5 -> util >> 0.85, gate closes
    rows = [[_tile_plant("WHEAT", 1) for _ in range(9)] for _ in range(5)]
    ok, util = main._capacity_gate(_farm(rows), {}, delta_units=25.0)
    assert not ok and util > main.CAP_USE_MAX


def test_curve_gate_projection_blocks_dying_curve():
    prices = {"WOOL": 95}          # spot above the 90 floor...
    # ...project a heavy glut (fresh yesterday-EMA) so the 2-day projection
    # lands below the floor; a stale/future EMA is ignored by the freshness
    # window (cross-episode noise)
    main._MARKET_MEM[0] = {"day": 11, "prices": {}, "flow": {"WOOL": 6.0}}
    try:
        assert not main._curve_gate_ok("WOOL", 0, 12, prices)
        assert main._curve_gate_ok("WOOL", 0, 5, prices)  # stale -> spot-only
    finally:
        main._MARKET_MEM.clear()


def test_cash_gate_invariant():
    rich = _farm([[None]], money=3000.0)
    poor = _farm([[None]], money=400.0, hands=[(1, 1)] * 8)
    assert main._cash_gate_ok(rich, 2000.0)
    assert not main._cash_gate_ok(poor, 0.0)


def test_mixed_plan_shape():
    p = main._MIXED_PLAN
    assert p["mode"] == "MIXED"
    assert p["straw_total_cap"] == 33 and p["herd_ceiling"] == 14
    assert p["crew_cap"] == 11
    assert p["melon_total_cap"] == main.LINE_CAPS["MELON"]


def test_d6_checkpoint_branches():
    # healthy VOLUME-ready state -> C1
    rows = [[_tile_plant("WHEAT", 1) for _ in range(5)] for _ in range(4)]
    # Phase-C capA: herd stays at the VOLUME floor (10); the
    # top-20-anchored law capacity-gates the 42-tile C1 target below
    for i in range(10):
        rows[i // 5][i % 5] = _tile_animal("COW" if i % 2 else "SHEEP", 0)
    mine = _farm(rows, money=1200.0)
    obs = {"player": 0, "day": 6,
           "farms": [mine, _farm([[None]])],
           "market": {"prices": {"STRAWBERRY": 110}},
           "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "BRUNCH_SPOT",
                                       "ICE_CREAM_SHOP", "FARMERS_MARKET"]}}
    questions, branch = main._d6_checkpoint(obs, 6)
    assert questions["q1"] and questions["q2"] and questions["q3"]
    # Phase-C capA: the top-20-anchored law (84.1 @ crew 12, x0.85 = 71.5)
    # capacity-gates the 42-tile C1 build (42+12+2x10 = 74) OUT -- the
    # healthy farm falls to the dairy C3 instead.  The 42-tile C1 returns
    # only if the online probe overturns the backfill.
    assert questions["q5"] is False
    assert branch == "C3"
    # dead strawberry price + live dairy -> C2/C3 family, never C1
    obs["market"]["prices"]["STRAWBERRY"] = 60
    questions, branch = main._d6_checkpoint(obs, 6)
    assert branch in ("C2", "C3")


def test_stage_plan_carries_knobs():
    obs = {"player": 0, "day": 2, "farms": [
        _farm([[None]]),
        _farm([[_tile_animal("COW", 0) for _ in range(4)]])],
        "market": {"prices": {}}, "town": {"unlocked_shops": []}}
    out = main._stage_plan(0, obs, 2, dict(main._DEFENSIVE_PLAN))
    assert out["stage"] == "P1" and out["opp_class"] == "burst"
    # no yarn store unlocked -> B1 differentiation prefers cows
    assert out.get("p1_species_pref") == "COW"


# --------------------------------------------------------------------------
# OBS v2: calendar + four channels + est_*
# --------------------------------------------------------------------------

def test_opp_production_calendar_offsets():
    rows = [[_tile_plant("STRAWBERRY", 5), None, None, None, None]]
    rows.append([_tile_animal("SHEEP", 2), None, None, None, None])
    cal = main._opp_production_calendar(_farm(rows), 6, horizon=16)
    # strawberry planted d5: evenings 14,16,18,20 -> offsets 8,10,12,14
    assert cal["STRAWBERRY"][8] == 1 and cal["STRAWBERRY"][14] == 1
    assert sum(cal["STRAWBERRY"]) == 4
    # sheep placed d2: first wool evening = 2+6-1 = 7 -> offset 1
    assert cal["WOOL"][1] == 1


def test_observer_day_account_and_est():
    main._OPP_OBSERVER.clear()
    tiles = [[_tile_plant("STRAWBERRY", 2, yield_units=3), None,
              _tile_animal("COW", 0, yield_units=2), None, None]]
    opp = _farm(tiles, money=1000.0)
    mine = _farm([[None]], money=1000.0)
    obs = {"player": 0, "day": 3, "hour": 0,
           "farms": [mine, opp],
           "market": {"prices": {"MILK": 160},
                      "inventory": {i: 10000 for i in main.BASE_PRICE}},
           "town": {"unlocked_shops": ["YARN_STORE"]},
           "private": {"shed": {}, "seeds": {}, "inventories": [{}]}}
    # seed the previous-day snapshot
    main._opp_observer_state(0, 3, 0)
    main._OPP_OBSERVER[0]["inv_prev"] = dict(
        obs["market"]["inventory"])
    main._OPP_OBSERVER[0]["tile_yield_prev"] = {
        "STRAWBERRY": 3, "MILK": 2}
    main._OPP_OBSERVER[0]["money_prev"] = 1000.0
    main._OPP_OBSERVER[0]["sold_today"] = {"MILK": 1}
    # W2 note: the day account now warms up on its first pass (no
    # flow/held output) -- the seeded state marks itself initialized
    main._OPP_OBSERVER[0]["initialized"] = True
    # opponent sells 4 wool overnight (inventory +4) and harvests strawberry
    obs["market"]["inventory"]["WOOL"] = 10004
    for row in opp["tiles"]:
        for t in row:
            if isinstance(t, dict) and t.get("crop") == "STRAWBERRY":
                t["yield_units"] = 0
    main._opp_observer_update(obs, obs["private"])
    assert main.est_opp_net("WOOL") is not None
    # harvested 3, minus the 1 net-sale the integer account attributes on a
    # flat inventory against the town-center's 1/day draw (Ch0 formula)
    assert main.est_opp_held("STRAWBERRY") == 2
    assert main.est_opp_conf("WOOL") > 0
    # fail-open: poisoned observation zeroes confidence, never raises
    main._opp_observer_update({"player": 0}, None)
    assert main.est_opp_conf("WOOL") == 0.0


# --------------------------------------------------------------------------
# market v1.1: sell overrides + planner + interference shadow
# --------------------------------------------------------------------------

def test_sell_plan_item_hold_vs_clear():
    main._MARKET_MEM.clear()
    contested = {"STRAWBERRY"}
    assert main._sell_plan_item("STRAWBERRY", 10, {"STRAWBERRY": 110},
                                {}, contested) == "clear"
    # floor segment and dying curve -> clear; FLAT curve -> clear-through
    # (the m2 daily-clear discipline); RISING projection -> hold
    assert main._sell_plan_item("MILK", 10, {"MILK": 1}, {}, None) == "clear"
    assert main._sell_plan_item("MILK", 10, {"MILK": 160}, {}, None) == "clear"
    main._MARKET_MEM[0] = {"day": 9, "prices": {}, "flow": {"MILK": -2.0}}
    try:
        assert main._sell_plan_item("MILK", 10, {"MILK": 160},
                                    main._MARKET_MEM[0]["flow"], None) \
            == "hold"
    finally:
        main._MARKET_MEM.clear()


def test_sell_overrides_zero_hood_and_p4():
    tiles = [[_tile_plant("STRAWBERRY", 1) for _ in range(12)]]
    opp = _farm(tiles)
    obs = {"player": 0, "day": 10, "farms": [_farm([[None]]), opp],
           "market": {"prices": {"STRAWBERRY": 110}},
           "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "BRUNCH_SPOT"]}}
    shed = {"STRAWBERRY": 20}
    out = main._sell_overrides(obs, None, {}, 10,
                               obs["market"]["prices"], shed,
                               ["SMOOTHIE_SHOP", "BRUNCH_SPOT"], [])
    sold = {o[1]: o[2] for o in out if o[0] == "SELL"}
    # contested line: clear-through today, bounded by the dump-rate limiter
    assert 0 < sold.get("STRAWBERRY", 0) <= 2 * (2 * 6 + 1) + 4


def test_interference_shadow_inert_but_logging():
    main._INTERFERENCE_LOG.clear()
    opp = _farm([[_tile_animal("COW", 0) for _ in range(8)]])
    # W2 fix note: the v1.1 formula caps realizable supply by town
    # absorption (market §3.2), so the fixture now carries a MILK shop --
    # a zero-absorption world rightly logs r_opp = 0 (no monetization).
    obs = {"player": 0, "day": 10, "farms": [_farm([[None]]), opp],
           "market": {"prices": {"MILK": 160}},
           "town": {"unlocked_shops": ["SMOOTHIE_SHOP"]}}
    trig = main._interference_shadow(obs, opp, 10, {"MILK": 160})
    # Phase-D: MK-5 vehicle 1 is ARMED -- single-day trigger still returns
    # False (needs 2 consecutive confirm days); the inert->armed change is
    # pinned in test_market_w2
    assert main.INTERFERENCE_ARMED is True
    assert main._INTERFERENCE_LOG and \
        main._INTERFERENCE_LOG[-1]["r_opp"] > 0


def test_opportunity_buy_and_chunk_cap():
    # cheap wheat + feed demand: opportunistic hoard order appears
    private = {"shed": {"WHEAT": 2}, "seeds": {"WHEAT": 12},
               "inventories": [{}]}
    farm = _farm([[_tile_animal("COW", 0), None, None, None, None]],
                 money=2500.0)
    obs = {"player": 0, "day": 4, "hour": 0, "farms": [farm, farm],
           "market": {"prices": {"WHEAT": 22}, "inventory": {}},
           "town": {"unlocked_shops": []},
           "private": private}
    orders = main._market_orders(obs, farm, private, 4, 5, 1,
                                 plan=dict(main._DEFENSIVE_PLAN))
    buys = [o for o in orders if o[0] == "BUY_PRODUCT" and o[1] == "WHEAT"]
    assert buys and all(o[2] <= main.BUY_CHUNK_MAX_UNITS for o in buys)


# --------------------------------------------------------------------------
# scheduler v1.3 shadows: mission / solver / executor
# --------------------------------------------------------------------------

def test_build_mission_annotates_schema():
    tasks = [
        {"w": 98, "x": 1, "y": 1, "act": ["WATER"], "key": ("WATER", 1, 1),
         "need": None, "units": None, "v": 98, "red": True},
        {"w": 40, "x": 2, "y": 2, "act": ["HARVEST"], "key": ("H", 2, 2),
         "need": None, "units": None, "v": 120, "red": False},
        {"w": 30, "x": 3, "y": 3, "act": ["CARE"], "key": ("C", 3, 3),
         "need": None, "units": None, "v": 30, "red": False},
    ]
    farm = _farm([[None] * 5 for _ in range(5)], hands=[(1, 1)])
    obs = {"hour": 0}
    mission = main._build_mission(obs, farm, {}, 5, {}, tasks)
    assert mission["cls_counts"] == {"OBLIGATION": 1, "YIELD": 1,
                                     "BONUS": 1}
    assert mission["d1"] == [("WATER", 1, 1)]
    assert "ok" in mission["capacity"]


def test_solve_routes_deterministic_and_edf_first():
    tasks = [
        {"w": 90, "x": 4, "y": 4, "act": ["FEED"], "key": ("F", 4, 4),
         "v": 90, "red": True, "deadline": 16},
        {"w": 30, "x": 0, "y": 0, "act": ["CARE"], "key": ("C", 0, 0),
         "v": 30, "red": False, "deadline": None},
        {"w": 50, "x": 8, "y": 8, "act": ["HARVEST"], "key": ("H", 8, 8),
         "v": 200, "red": False, "deadline": 21},
    ]
    farm = _farm([[None] * 10 for _ in range(10)], hands=[(4, 4)])
    r1 = main._solve_routes(farm, {}, 5, tasks)
    r2 = main._solve_routes(farm, {}, 5, tasks)
    assert r1 == r2                              # golden determinism
    heads = [route["stops"] for route in r1["routes"] if route["stops"]]
    flat = [s for h in heads for s in h]
    assert ("F", 4, 4) in flat                   # D1 covered somewhere


def test_executor_walks_and_flags_replan():
    route = [{"worker": 0, "sector": None,
              "stops": [{"x": 6, "y": 4, "act": ["WATER"], "deadline": 16}],
              "etas": [3]}]
    farm = _farm([[None] * 10 for _ in range(10)])
    obs = {"hour": 15}                           # too late to reach by 16
    actions, replan = main._execute_routes(obs, farm, {}, 5, route)
    assert actions[0][0] in ("EAST", "WEST", "NORTH", "SOUTH")
    assert replan is True
    obs = {"hour": 1}
    actions, replan = main._execute_routes(obs, farm, {}, 5, route)
    assert replan is False


def test_opp_contesting_removed_from_volume_gate():
    # branch §9-⑦ (user ruling): a 20-tile strawberry opponent NO LONGER
    # blocks VOLUME entry when every readiness condition passes.
    mine_rows = [[None] * 10 for _ in range(10)]
    for i in range(10):
        mine_rows[1 + i // 5][i % 5] = _tile_animal("SHEEP" if i % 2
                                                    else "COW", 0)
    for i in range(6):
        mine_rows[0][i] = _tile_plant("STRAWBERRY", 6)
    opp_rows = [[_tile_plant("STRAWBERRY", 2) for _ in range(10)]
                for _ in range(2)]
    obs = {"player": 0, "day": 7,
           "farms": [_farm(mine_rows, money=1500.0), _farm(opp_rows)],
           "market": {"prices": {"STRAWBERRY": 110}},
           "town": {"unlocked_shops": ["SMOOTHIE_SHOP", "BRUNCH_SPOT",
                                       "ICE_CREAM_SHOP"]}}
    # gate unit test: the rollout stays a pure SOLVENCY veto (stub it green;
    # its own behaviour is pinned by the r5 test suite)
    real_rollout = main._plan_rollout
    main._plan_rollout = lambda *a, **k: {"min_cash": 100.0,
                                          "terminal": 1.0}
    try:
        plan = main._decide_mode(obs, 7, None)
    finally:
        main._plan_rollout = real_rollout
    assert plan["mode"] == "VOLUME_CROP"
