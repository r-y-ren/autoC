"""W2 branch-plan completion tests (phase_branch_plan.md v1.3).

Covers: d1 classification freeze, d10 SE-window readiness, d14 structure
freeze + BP-8.1 widening guard, BP-8.2 fuse fallback (money floor /
escape detection / per-stage counting), the dawn-invariant lower bound
(capacity backfill, wheat fallback line) and the LINE_CAPS per-line
envelope in _field_alloc; mission peak-day check + telemetry fields.
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


def _obs(farm, opp=None, day=8):
    return {"player": 0, "day": day, "hour": 0,
            "farms": [farm, opp if opp is not None else _farm(_rows10())],
            "market": {"prices": {"STRAWBERRY": 110, "WHEAT": 30}},
            "town": {"unlocked_shops": []}}


def _reset():
    main._STAGE_MEM.clear()
    main._MISSION_SHADOW.clear()


# --------------------------------------------------------------------------
# §9.1 checkpoints: d1 freeze / d10 SE window / d14 freeze snapshot
# --------------------------------------------------------------------------

def test_d1_checkpoint_freezes_classification():
    _reset()
    opp_burst = _farm([[_tile_animal("COW", 0) for _ in range(4)]])
    plan = main._stage_plan(0, _obs(_farm(_rows10()), opp_burst, day=1),
                            1, dict(main._DEFENSIVE_PLAN))
    assert plan["opp_class"] == "burst"
    # later P1 days keep the d1 verdict even after the opponent shrinks
    # (classification is frozen at the d1 checkpoint)
    opp_small = _farm([[None]])
    plan = main._stage_plan(0, _obs(_farm(_rows10()), opp_small, day=3),
                            3, dict(main._DEFENSIVE_PLAN))
    assert plan["opp_class"] == "burst"


def test_d10_checkpoint_se_ready():
    _reset()
    rich = main._stage_plan(0, _obs(_farm(_rows10(), money=5000.0)), 10,
                            dict(main._DEFENSIVE_PLAN))
    st = main._STAGE_MEM[0]
    assert st["d10"]["se_ready"] is True
    _reset()
    main._stage_plan(0, _obs(_farm(_rows10(), money=4000.0)), 10,
                     dict(main._DEFENSIVE_PLAN))
    assert main._STAGE_MEM[0]["d10"]["se_ready"] is False


def test_d14_freeze_guard_blocks_widening():
    _reset()
    # d14 under DEFENSIVE freezes the narrow class
    main._stage_plan(0, _obs(_farm(_rows10()), day=14), 14,
                     dict(main._DEFENSIVE_PLAN))
    assert main._STAGE_MEM[0]["frozen"]["mode"] == "DEFENSIVE"
    wide = dict(main._VOLUME_PLAN)
    out = main._stage_plan(0, _obs(_farm(_rows10()), day=15), 15, wide)
    assert out["mode"] == "DEFENSIVE"          # BP-8.1: no widening back
    assert out.get("freeze_guard") is True
    # a farm already wide at d14 is NOT restricted (exits stay free)
    _reset()
    main._STAGE_MEM[0] = {"day": 14, "decided_day": 6,
                          "c_branch": "C1", "questions": {}}
    main._stage_plan(0, _obs(_farm(_rows10()), day=14), 14,
                     dict(main._VOLUME_PLAN))
    out = main._stage_plan(0, _obs(_farm(_rows10()), day=15), 15,
                           dict(main._VOLUME_PLAN))
    assert out["mode"] == "VOLUME_CROP"
    assert "freeze_guard" not in out


# --------------------------------------------------------------------------
# §8.2 fuse: money floor / escape detection / per-stage counting
# --------------------------------------------------------------------------

def test_fuse_money_floor_fallback_and_counting():
    _reset()
    broke = _obs(_farm(_rows10(), money=250.0), day=8)
    out = main._stage_plan(0, broke, 8, dict(main._VOLUME_PLAN))
    assert out["fused"] is True and out["mode"] == "DEFENSIVE"
    snap = main.stage_state_snapshot(0)
    assert snap["fused"] is True and snap["fuse_events"] == 1
    # recovery within the same stage remains defensive until the stage ends
    main._stage_plan(0, _obs(_farm(_rows10(), money=3000.0), day=9), 9,
                     dict(main._VOLUME_PLAN))
    snap = main.stage_state_snapshot(0)
    assert snap["fused"] is True and snap["fuse_events"] == 1
    # a new stage trip counts again
    main._stage_plan(0, _obs(_farm(_rows10(), money=3000.0), day=15), 15,
                     dict(main._VOLUME_PLAN))
    assert main.stage_state_snapshot(0)["fused"] is False
    main._stage_plan(0, _obs(_farm(_rows10(), money=200.0), day=16), 16,
                     dict(main._VOLUME_PLAN))
    assert main.stage_state_snapshot(0)["fuse_events"] == 2


def test_fuse_escape_detection():
    _reset()
    rows = _rows10()
    for i in range(5):
        rows[0][i] = _tile_animal("COW", 2)
    main._stage_plan(0, _obs(_farm(rows), day=8), 8,
                     dict(main._DEFENSIVE_PLAN))
    # overnight escapes: herd 5 -> 3 (engine has no animal sales)
    rows2 = _rows10()
    for i in range(3):
        rows2[0][i] = _tile_animal("COW", 2)
    out = main._stage_plan(0, _obs(_farm(rows2), day=9), 9,
                           dict(main._DEFENSIVE_PLAN))
    assert out.get("fused") is True


# --------------------------------------------------------------------------
# §5.3 dawn-invariant lower bound + per-line caps envelope
# --------------------------------------------------------------------------

def test_backfill_attaches_under_slack():
    _reset()
    out = main._stage_plan(0, _obs(_farm(_rows10()), day=16), 16,
                           dict(main._DEFENSIVE_PLAN))
    bf = out.get("capacity_backfill")
    assert bf is not None and bf["line"] == "WHEAT"
    assert bf["room_units"] > 0
    assert bf["candidates"][-1] == "WHEAT"      # fallback line is last
    assert main.stage_state_snapshot(0)["backfill"]["room_units"] == \
        bf["room_units"]
    # a loaded farm (util > CAP_USE_MIN) attaches nothing; round-19 tpu
    # 2.0 doubled the law's capacity, so "loaded" now takes a full board
    # across all four quadrants
    rows = _rows10()
    for y in range(10):
        for x in range(10):
            rows[y][x] = _tile_plant("STRAWBERRY", 8)
    out = main._stage_plan(0, _obs(_farm(rows, quads=["NW", "NE", "SW",
                                                    "SE"]), day=16), 16,
                           dict(main._DEFENSIVE_PLAN))
    assert "capacity_backfill" not in out


def test_field_alloc_backfill_expands_wheat_only_leftovers():
    prices = {"WHEAT": 25, "STRAWBERRY": 110, "MELON": 200, "CARROT": 40}
    base = dict(main._DEFENSIVE_PLAN)
    farm = _farm(_rows10(), quads=["NW", "NE", "SW", "SE"])
    _b, crops0, _n, _c = main._field_alloc(farm, 16, prices, base)
    plan = dict(base)
    plan["capacity_backfill"] = {"line": "WHEAT", "room_units": 5}
    _b, crops1, _n, _c = main._field_alloc(farm, 16, prices, plan)
    assert len(crops1["WHEAT"]) == len(crops0["WHEAT"]) + 5


def test_line_caps_envelope_binds():
    prices = {"WHEAT": 25, "STRAWBERRY": 110, "MELON": 200, "CARROT": 40}
    quads = ["NW", "NE", "SW", "SE"]
    plan = dict(main._DEFENSIVE_PLAN)
    plan["straw_quad_cap"] = 99
    plan["straw_total_cap"] = 99
    farm = _farm(_rows10(), quads=quads)
    _b, crops, _n, _c = main._field_alloc(farm, 8, prices, plan)
    assert len(crops["STRAWBERRY"]) <= main.LINE_CAPS["STRAWBERRY"]
    # the envelope truly binds (monkeypatch a tight cap)
    saved = main.LINE_CAPS["STRAWBERRY"]
    main.LINE_CAPS["STRAWBERRY"] = 6
    try:
        _b, crops, _n, _c = main._field_alloc(farm, 8, prices, plan)
        assert len(crops["STRAWBERRY"]) == 6
    finally:
        main.LINE_CAPS["STRAWBERRY"] = saved
    # carrot envelope (endgame window open)
    rows = _rows10()
    saved_c = main.LINE_CAPS["CARROT"]
    main.LINE_CAPS["CARROT"] = 4
    try:
        _b, crops, _n, _c = main._field_alloc(
            _farm(rows, quads=quads), 23, prices,
            dict(main._DEFENSIVE_PLAN))
        assert len(crops["CARROT"]) == 4
    finally:
        main.LINE_CAPS["CARROT"] = saved_c


# --------------------------------------------------------------------------
# §2.6 peak-day check (mission shadow) + telemetry plumbing
# --------------------------------------------------------------------------

def test_mission_peak_day_field():
    rows = _rows10()
    farm = _farm(rows)
    tasks = [{"w": 98, "x": 1, "y": 1, "act": ["WATER"], "key": ("w", 1, 1),
              "v": 98, "red": True} for _ in range(20)]   # 20 D1 duties
    mission = main._build_mission({"hour": 0}, farm, {}, 8, None, tasks)
    assert mission["peak"]["load"] == 40        # ~2 turns per duty
    assert mission["peak"]["ok"] is False       # 1 worker cannot cover 40
    light = tasks[:3]
    mission = main._build_mission({"hour": 0}, farm, {}, 8, None, light)
    assert mission["peak"]["ok"] is True


def test_telemetry_stage_fields():
    _reset()
    main.reset_telemetry()
    obs = _obs(_farm(_rows10(), money=250.0), day=8)
    obs["private"] = {}
    main._stage_plan(0, obs, 8, dict(main._DEFENSIVE_PLAN))
    main._telemetry_record_turn(obs, _farm(_rows10(), money=250.0), {},
                                [["PASS"]], [], {}, [])
    day = main.telemetry_snapshot()["players"]["0"]["days"]["8"]
    assert day["fused"] is True
    assert day["fuse_events"] == 1
    main.reset_telemetry()
    _reset()


# --------------------------------------------------------------------------
# Branch decisions must reach executable plans and market orders
# --------------------------------------------------------------------------

def _healthy_d6_farm(straw_price=110):
    rows = _rows10()
    for i in range(10):
        rows[i // 5][i % 5] = _tile_animal(
            "COW" if i % 2 else "SHEEP", 0)
    for i in range(6):
        rows[2 + i // 5][i % 5] = _tile_plant("STRAWBERRY", 0)
    farm = _farm(rows, money=5000.0, quads=["NW", "NE", "SW"])
    obs = _obs(farm, day=6)
    obs["market"]["prices"].update({
        "STRAWBERRY": straw_price, "MILK": 160, "WOOL": 160})
    obs["town"]["unlocked_shops"] = [
        "SMOOTHIE_SHOP", "BRUNCH_SPOT", "ICE_CREAM_SHOP", "YARN_STORE"]
    return obs


def test_c_branches_drive_distinct_plans():
    _reset()
    c1 = main._stage_plan(0, _healthy_d6_farm(), 6,
                          dict(main._VOLUME_PLAN))
    assert c1["c_branch"] == "C1" and c1["mode"] == "VOLUME_CROP"

    _reset()
    c2 = main._stage_plan(0, _healthy_d6_farm(60), 6,
                          dict(main._DEFENSIVE_PLAN))
    assert c2["c_branch"] == "C2" and c2["mode"] == "MIXED"

    _reset()
    poor = _obs(_farm(_rows10(), money=700.0), day=6)
    c3 = main._stage_plan(0, poor, 6, dict(main._VOLUME_PLAN))
    assert c3["c_branch"] == "C3" and c3["mode"] == "DEFENSIVE"


def test_missing_d6_checkpoint_is_recomputed():
    _reset()
    obs = _healthy_d6_farm()
    obs["day"] = 9
    out = main._stage_plan(0, obs, 9, dict(main._VOLUME_PLAN))
    snap = main.stage_state_snapshot(0)
    assert out["c_branch"] == "C1"
    assert main._STAGE_MEM[0]["decided_day"] == 9
    assert snap["questions"] and all(snap["questions"].values())


def test_b_branches_are_explicit_and_b3_is_bounded():
    _reset()
    standard = _obs(_farm(_rows10()), _farm([[None]]), day=1)
    out = main._stage_plan(0, standard, 1, dict(main._DEFENSIVE_PLAN))
    assert out["b_branch"] == "B2"

    _reset()
    opp = _farm([[_tile_plant("MELON", 1) for _ in range(6)]])
    day1 = main._stage_plan(0, _obs(_farm(_rows10()), opp, day=1), 1,
                            dict(main._DEFENSIVE_PLAN))
    obs3 = _obs(_farm(_rows10(), quads=["NW", "NE"]), opp, day=3)
    day3 = main._stage_plan(0, obs3, 3, dict(main._DEFENSIVE_PLAN))
    day6 = main._stage_plan(0, _obs(_farm(_rows10()), opp, day=6), 6,
                            dict(main._DEFENSIVE_PLAN))
    assert day1["b_branch"] == "B3" and day1["melon_total_cap"] == 0
    assert day3["melon_total_cap"] == 2
    private = {"shed": {}, "seeds": {}, "inventories": []}
    orders = main._market_orders(obs3, obs3["farms"][0], private, 3,
                                  0, 0, day3)
    melon_buys = [o for o in orders if o[:2] == ["BUY_SEED", "MELON"]]
    assert melon_buys and 0 < melon_buys[0][2] <= 2
    assert day6["c_branch"] == "C3"
    assert "melon_total_cap" not in day6


def test_macro_plan_rechecks_same_day_fuse():
    _reset()
    main._PLAN_MEM.clear()
    healthy = _obs(_farm(_rows10(), money=3000.0), day=8)
    first = main._macro_plan(0, healthy, 8)
    broke = _obs(_farm(_rows10(), money=200.0), day=8)
    second = main._macro_plan(0, broke, 8)
    assert not first.get("fused", False)
    assert second["fused"] is True and second["mode"] == "DEFENSIVE"


def test_d10_readiness_and_d22_tier_are_consumed():
    _reset()
    main._STAGE_MEM[0] = {"day": 10, "decided_day": 6,
                          "c_branch": "C1", "questions": {}}
    rich = _farm(_rows10(), money=5000.0,
                 quads=["NW", "NE", "SW"])
    plan = main._stage_plan(0, _obs(rich, day=10), 10,
                            dict(main._VOLUME_PLAN))
    private = {"shed": {}, "seeds": {}, "inventories": []}
    assert plan["se_ready"] is True
    orders = main._market_orders(_obs(rich, day=10), rich, private, 10,
                                  0, 0, plan)
    assert ["BUY_LAND"] in orders

    blocked = dict(plan)
    blocked["se_ready"] = False
    orders = main._market_orders(_obs(rich, day=10), rich, private, 10,
                                  0, 0, blocked)
    assert ["BUY_LAND"] not in orders

    p4 = {"p4_snapshot": {"tiers": {"MILK": "heavy"}}}
    assert main._p4_should_clear("MILK", 25, 0, p4)
    assert not main._p4_should_clear("MILK", 24, 0, p4)
    p4_mid = {"p4_snapshot": {"tiers": {"MILK": "mid"}}}
    assert not main._p4_should_clear("MILK", 25, 0, p4_mid)
    assert main._p4_should_clear("MILK", 26, 0, p4_mid)


def test_market_capex_queue_stays_within_capacity():
    rows = _rows10()
    for i in range(48):
        rows[i // 10][i % 10] = _tile_plant("WHEAT", 1)
    farm = _farm(rows, money=10000.0, hands=[(0, 0)] * 8,
                 quads=["NW", "NE", "SW"])
    obs = _obs(farm, day=8)
    obs["market"]["prices"].update({"MILK": 160, "WOOL": 160})
    private = {"shed": {}, "seeds": {}, "inventories": []}
    plan = dict(main._DEFENSIVE_PLAN)
    orders = main._market_orders(obs, farm, private, 8, 0, 0, plan)
    delta = 0.0
    for order in orders:
        if order[0] == "BUY_LAND":
            delta += 25.0
        elif order[0] == "BUY_SEED":
            delta += float(order[2])
        elif order[0] == "BUY_ANIMAL":
            delta += 2.0 * order[2]
    assert main._capacity_gate(farm, None, delta, 8, plan)[0]


def test_b1_catchup_and_b2_probe_flags_aggressive():
    # aggressive wave C: B1 carries the declared catch-up stride, B2 the
    # d1 strawberry probe + NE land pull-forward.
    main._INTERFERENCE_LOG.clear()
    st = {"opp_class_frozen": "burst"}
    plan = main._b_branch_adjust({}, {}, 1, st)
    assert plan["b_branch"] == "B1"
    assert plan["opening_seq_override"] == {1: {"SHEEP": 5}, 2: {"COW": 4}}
    st2 = {"opp_class_frozen": "reduced"}
    plan2 = main._b_branch_adjust({}, {"player": 0}, 1, st2)
    assert plan2["b_branch"] == "B2"
    assert plan2["straw_d1_probe"] == 3
    assert plan2["land_plan_override"] == {1: (1, 1700)}
    main._INTERFERENCE_LOG.clear()


def test_vehicle_arming_on_confirmed_trigger():
    # V2 arms once on a 2-day confirmed streak and pins its target day in
    # the stage register (cross-day state); V4 mirrors the opponent's
    # dominant public crop inside d4-6.
    main._INTERFERENCE_LOG.clear()
    for d in (2, 3, 4):
        main._INTERFERENCE_LOG.append({"player": 0, "day": d,
                                       "confirmed": True})
    st = {"opp_class_frozen": "reduced", "b_branch": "B2"}
    obs = {"player": 0, "farms": [
        {},
        {"tiles": [[{"kind": "PLANT", "crop": "STRAWBERRY"}] * 4]}]}
    plan = main._b_branch_adjust({}, obs, 5, st)
    assert plan["iv2_target_day"] == 15
    assert plan["iv2_carrot"] == 8
    assert st["iv_state"]["v2_armed_day"] == 5
    plan4 = main._b_branch_adjust({}, obs, 4, st)
    assert plan4["iv4_mirror"]["crop"] == "STRAWBERRY"
    assert plan4["iv4_mirror"]["tiles"] == 4
    # re-arming does not drift the pinned target day
    plan6 = main._b_branch_adjust({}, obs, 6, st)
    assert plan6["iv2_target_day"] == 15
    main._INTERFERENCE_LOG.clear()
