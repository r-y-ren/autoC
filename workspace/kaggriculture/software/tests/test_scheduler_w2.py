"""W2 scheduler full-spec tests (worker_route_scheduler_design.md v1.3 §2-§4).

Covers: D1-D4 tiering, feed precondition, EOD budget inequality, capacity
feed-forward (deficit/slack), mission golden hash, shadow registry; solver
LPT partition + overflow (D1 pinned), 2-opt segment polish, feed-leg
chunking, ETA drop/D1-infeasibility, determinism; executor F4 skip, EOD
projection assertion, idempotent REPLAN gate, d29 DROP->SELL template.
All shadows: ROUTE_EXECUTOR_ENABLED stays False and nothing here may
change the merged artifact's behaviour.
"""
import importlib
import os
import sys

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE, "kaggle_simulations", "agent"))

main = importlib.import_module("main")


def _tile_plant(crop, planted_day, yield_units=0, streak=0, watered=True):
    return {"kind": "PLANT", "crop": crop, "planted_day": planted_day,
            "yield_units": yield_units, "consecutive_unwatered": streak,
            "watered_today": watered}


def _tile_animal(animal, placed_day, yield_units=0, unfed=0):
    return {"kind": "PASTURE", "animal": animal, "placed_day": placed_day,
            "yield_units": yield_units, "consecutive_unfed": unfed,
            "fed_today": False, "cared_today": False,
            "fertilizer_available": False}


def _farm(tiles_rows, money=3000.0, hands=None, quads=None, farmer=(4, 4)):
    return {"tiles": tiles_rows, "money": money,
            "hands": [list(h) for h in (hands or [])],
            "farmer": list(farmer),
            "unlocked_quadrants": quads or ["NW"]}


def _rows10():
    return [[None] * 10 for _ in range(10)]


def _task(w, x, y, act, key, v=None, red=False, deadline=None):
    return {"w": w, "x": x, "y": y, "act": act, "key": key,
            "need": None, "units": None, "v": w if v is None else v,
            "red": red, "deadline": deadline}


# --------------------------------------------------------------------------
# mission §2: tiers / feed precondition / EOD budget / capacity feed-forward
# --------------------------------------------------------------------------

def test_mission_tiers_d1_d2_d3_d4():
    ws, we = main._window("WHEAT")
    day = 10
    rows = _rows10()
    rows[1][1] = _tile_plant("WHEAT", day - ws, streak=0)     # in window
    rows[2][2] = _tile_plant("STRAWBERRY", day - 3, streak=0)  # ongoing
    rows[3][3] = _tile_animal("COW", 2, unfed=1)               # escapes
    rows[4][4] = _tile_animal("COW", 2, unfed=0)
    farm = _farm(rows)
    tasks = [
        _task(98, 0, 0, ["WATER"], ("water", 0, 0), red=True),   # red -> D1
        _task(40, 1, 1, ["WATER"], ("water", 1, 1)),             # window -> D3
        _task(40, 2, 2, ["WATER"], ("water", 2, 2)),             # ongoing -> D2
        _task(80, 5, 5, ["HARVEST"], ("harv", 5, 5)),            # -> D4
        _task(100, 3, 3, ["FEED"], ("feed", 3, 3)),              # unfed -> D1
        _task(88, 4, 4, ["FEED"], ("feed", 4, 4)),               # grace -> D2
    ]
    obs = {"hour": 0, "player": 0}
    mission = main._build_mission(obs, farm, {}, day, None, tasks)
    tiers = {str(t["key"]): t["tier"] for t in mission["tasks"]}
    assert tiers["('water', 0, 0)"] == "D1"
    assert tiers["('water', 1, 1)"] == "D3"
    assert tiers["('water', 2, 2)"] == "D2"
    assert tiers["('harv', 5, 5)"] == "D4"
    assert tiers["('feed', 3, 3)"] == "D1"
    assert tiers["('feed', 4, 4)"] == "D2"
    assert mission["d1"] == [("water", 0, 0), ("feed", 3, 3)]
    assert mission["tier_counts"] == {"D1": 2, "D2": 2, "D3": 1, "D4": 1}


def test_mission_feed_precondition_event():
    rows = _rows10()
    rows[3][3] = _tile_animal("COW", 2, unfed=1)
    farm = _farm(rows)
    tasks = [_task(100, 3, 3, ["FEED"], ("feed", 3, 3), red=True)]
    # 1 D1 mouth vs 0 wheat in stock -> buy the gap at h0, priority 95
    mission = main._build_mission({"hour": 0}, farm,
                                  {"shed": {"WHEAT": 0}}, 5, None, tasks)
    assert mission["events"] == [{"h": 0, "op": "BUY_PRODUCT",
                                  "item": "WHEAT", "qty": 1,
                                  "priority": 95, "why": "feed_precondition"}]
    # covered -> no event
    mission = main._build_mission({"hour": 0}, farm,
                                  {"shed": {"WHEAT": 4}}, 5, None, tasks)
    assert not [e for e in mission["events"] if e["why"] == "feed_precondition"]


def test_mission_eod_budget_event():
    rows = _rows10()
    rows[2][2] = _tile_plant("STRAWBERRY", 5, yield_units=10)
    farm = _farm(rows)
    tasks = [_task(85, 2, 2, ["HARVEST"], ("harv", 2, 2))]
    private = {"shed": {"WHEAT": 95}}
    mission = main._build_mission({"hour": 0}, farm, private, 8, None, tasks)
    assert mission["eod"]["harvest_in"] == 10
    assert mission["eod"]["projected"] == 105
    assert mission["eod"]["overflow"] == 5
    # log-curve wheat goes first, capped by what the shed holds
    assert {"h": 6, "op": "SELL", "item": "WHEAT", "qty": 5,
            "why": "eod_budget"} in mission["events"]
    # planned_sell is honoured when supplied
    mission = main._build_mission({"hour": 0}, farm, private, 8, None,
                                  tasks, planned_sell=10)
    assert mission["eod"]["overflow"] == 0


def test_mission_capacity_deficit_and_slack():
    # over the law at dawn d0: 40 strawberry tiles vs the crew-5 law (45)
    rows = _rows10()
    for y in range(8):
        for x in range(5):
            rows[y][x] = _tile_plant("STRAWBERRY", 0)
    farm = _farm(rows)
    mission = main._build_mission({"hour": 0}, farm, {}, 0, None, [])
    assert mission["capacity_deficit"] is not None
    assert mission["capacity_deficit"]["type"] == "over"
    assert mission["capacity"]["util"] > main.CAP_USE_MAX
    # slack: an empty farm reports the backfill room
    mission = main._build_mission({"hour": 0}, _farm(_rows10()), {}, 8,
                                  None, [])
    assert mission["capacity_deficit"] is None
    assert mission["capacity_slack"] is not None
    assert mission["capacity_slack"]["room_units"] > 0


def test_mission_hash_golden_determinism():
    rows = _rows10()
    rows[3][3] = _tile_animal("COW", 2, unfed=1)
    farm = _farm(rows)
    tasks = [_task(100, 3, 3, ["FEED"], ("feed", 3, 3), red=True),
             _task(80, 5, 5, ["HARVEST"], ("harv", 5, 5))]
    m1 = main._build_mission({"hour": 0}, farm, {"shed": {"WHEAT": 2}},
                              6, None, tasks)
    m2 = main._build_mission({"hour": 0}, farm, {"shed": {"WHEAT": 2}},
                              6, None, tasks)
    assert m1["mission_hash"] == m2["mission_hash"]
    m3 = main._build_mission({"hour": 0}, farm, {"shed": {"WHEAT": 0}},
                              6, None, tasks)      # event appears -> hash moves
    assert m3["mission_hash"] != m1["mission_hash"]


def test_mission_shadow_registry_once_per_day():
    main._MISSION_SHADOW.clear()
    rows = _rows10()
    farm = _farm(rows, hands=[(2, 2)])
    obs = {"hour": 0, "player": 0, "day": 4}
    m1 = main._mission_shadow_update(0, 4, 0, obs, farm, {}, None, [])
    m2 = main._mission_shadow_update(0, 4, 7, obs, farm, {}, None, [])
    assert m1 is m2                       # cached within the day
    m3 = main._mission_shadow_update(0, 3, 0, obs, farm, {}, None, [])
    assert m3 is not None and m3["day"] == 3   # rollback -> rebuild
    assert main.mission_shadow(0)["day"] == 3


# --------------------------------------------------------------------------
# solver §3: partition / overflow / 2-opt / feed legs / ETA / determinism
# --------------------------------------------------------------------------

def _n_dd_tasks(n, tier="D4", deadline=None, red=False):
    out = []
    for i in range(n):
        out.append(_task(30, i % 4, i // 4, ["CARE"], ("c", i),
                         v=30, red=red, deadline=deadline))
        out[-1]["tier"] = tier
    return out


def test_solve_edf_covers_d1_and_fills_balanced():
    # M3 v2: EDF deadline-first allocation -- D1 coverage is the guarantee,
    # the fill phase balances the remaining budget across workers.
    care_spots = [(6, 6), (6, 7), (6, 8), (7, 6), (7, 7), (7, 8),
                  (8, 6), (8, 7), (5, 6), (5, 7), (6, 5), (7, 5)]
    tasks = []
    for i, (x, y) in enumerate(care_spots):      # SE cluster near the D1s
        tt = _task(30, x, y, ["CARE"], ("c", i), v=30)
        tt["tier"] = "D4"
        tasks.append(tt)
    d1 = [_task(100, 8, 8, ["WATER"], ("d1a", 8, 8), red=True, deadline=23),
          _task(100, 9, 9, ["WATER"], ("d1b", 9, 9), red=True, deadline=23)]
    for t in d1:
        t["tier"] = "D1"
    farm = _farm(_rows10(), hands=[(4, 4)])
    res = main._solve_routes(farm, {"inventories": [{}, {}]}, 5,
                             tasks + d1, planned_hands=0)
    sizes = [len(r["tasks"]) for r in res["routes"]]
    # 48 total turn-budget holds ~10 of the 14 spread-out tasks; the rest
    # are refused by BUDGET (reason eta), never silently kept-over-budget
    assert sum(sizes) >= 10
    assert len(res["dropped"]) + sum(sizes) == 14
    assert res["drop_reasons"]["eta"] == len(res["dropped"])
    assert abs(sizes[0] - sizes[1]) <= 2          # budget fill balances
    assert res["feasible"] is True
    # every D1 sits in a route with an ETA inside its deadline
    d1_covered = 0
    for r in res["routes"]:
        for t, eta in zip(r["tasks"], r["etas"]):
            if t.get("tier") == "D1":
                assert eta <= t["deadline"]
                d1_covered += 1
    assert d1_covered == 2


def test_two_opt_segment_improves_crossing():
    def seg_at(x, y, i):
        return {"key": ("p", i), "x": x, "y": y, "act": ["CARE"],
                "w": 1, "v": 1, "tier": "D4", "deadline": None}
    bad = [seg_at(0, 1, 1), seg_at(5, 1, 2), seg_at(0, 2, 3),
           seg_at(5, 2, 4)]
    before = main._seg_len(bad, (0, 0))
    after = main._two_opt_segment(bad, (0, 0))
    assert main._seg_len(after, (0, 0)) < before
    assert sorted(str(t["key"]) for t in after) == \
        sorted(str(t["key"]) for t in bad)   # permutation only


def test_solve_feed_legs_chunking():
    # all mouths in one quadrant so a single cluster/worker owns the chain
    # M3 v2: single worker (planned_hands=0) so the chunk math is exact
    spots = [(4, 4), (4, 3), (3, 4), (3, 3), (2, 4), (4, 2), (2, 3)]
    tasks = [_task(88, x, y, ["FEED"], ("feed", x, y), v=88)
             for x, y in spots]
    farm = _farm(_rows10())
    res = main._solve_routes(farm, {"inventories": [{}]}, 6, tasks,
                             planned_hands=0)
    assert res["feed_legs"] == 2              # ceil(7 / FEED_LEG_CHUNK)
    pickups = [t for r in res["routes"] for t in r["tasks"]
               if t.get("synthetic")]
    assert sorted(t["act"][2] for t in pickups) == [5, 5]  # two legs on the
    # single worker's chain: 5 then 2... chunks are per-leg FEED_LEG_CHUNK
    assert all(t["act"][:2] == ["PICKUP", "WHEAT"] for t in pickups)
    kept = {t["key"] for r in res["routes"] for t in r["tasks"]}
    assert all(("feed", x, y) in kept for x, y in spots)
    # an existing wheat pickup that covers the load suppresses synthesis
    tasks.append(_task(96, 4, 3, ["PICKUP", "WHEAT", 7], ("pk", 0)))
    res = main._solve_routes(farm, {"inventories": [{}]}, 6, tasks,
                             planned_hands=0)
    assert res["feed_legs"] == 0


def test_solve_eta_drop_and_d1_infeasible():
    late_harvest = _task(85, 9, 9, ["HARVEST"], ("h", 9, 9),
                         deadline=3)          # unreachable in time
    late_harvest["tier"] = "D4"
    d1_late = _task(100, 9, 9, ["WATER"], ("w", 9, 9), red=True,
                    deadline=2)
    d1_late["tier"] = "D1"
    farm = _farm(_rows10(), hands=[(4, 4)])
    res = main._solve_routes(farm, {}, 5, [late_harvest], planned_hands=0)
    assert ("h", 9, 9) in res["dropped"]
    assert res["drop_reasons"]["eta"] == 1
    assert res["feasible"] is True
    res = main._solve_routes(farm, {}, 5, [d1_late], planned_hands=0)
    assert res["feasible"] is False           # never drop an obligation
    assert res["drop_reasons"]["no_fit"] == 1


def test_solve_determinism_extended():
    tasks = _n_dd_tasks(9)
    tasks += [_task(100, 8, 8, ["FEED"], ("feed", 8, 8), v=100, deadline=16),
              _task(85, 9, 8, ["HARVEST"], ("harv", 9, 8), deadline=21)]
    tasks[-2]["tier"] = "D2"
    tasks[-1]["tier"] = "D4"
    farm = _farm(_rows10(), hands=[(4, 4), (0, 0)])
    r1 = main._solve_routes(farm, {"inventories": [{}, {}]}, 6, tasks,
                            planned_hands=0)
    r2 = main._solve_routes(farm, {"inventories": [{}, {}]}, 6, tasks,
                            planned_hands=0)
    assert r1 == r2
    # every selection is key-lexicographic: repeated solves are stable
    assert r1["feed_legs"] >= 0


# --------------------------------------------------------------------------
# executor §4: F4 skip / EOD projection / idempotent gate / d29 template
# --------------------------------------------------------------------------

def test_executor_f4_skips_finished_tile():
    rows = _rows10()
    rows[2][2] = _tile_plant("WHEAT", 5, watered=True)   # already watered
    farm = _farm(rows, farmer=(2, 2))
    stops = [{"key": ("water", 2, 2), "x": 2, "y": 2, "act": ["WATER"],
              "deadline": None, "tier": "D1"},
             {"key": ("care", 4, 2), "x": 4, "y": 2, "act": ["CARE"],
              "deadline": None, "tier": "D4"}]
    routes = [{"worker": 0, "sector": None, "stops": stops,
               "tasks": stops, "etas": [1, 3]}]
    actions, replan = main._execute_routes({"hour": 1, "player": 0},
                                            farm, {}, 5, routes)
    assert actions[0] == ["EAST"]            # skipped the finished stop
    assert replan is False


def test_executor_eod_projection_and_idempotent_gate():
    main._REPLAN_MEM.clear()
    rows = _rows10()
    farm = _farm(rows, farmer=(4, 4))
    stops = [{"key": ("care", 8, 8), "x": 8, "y": 8, "act": ["CARE"],
              "deadline": None, "tier": "D4"}]
    routes = [{"worker": 0, "sector": None, "stops": stops,
               "tasks": stops, "etas": [9]}]
    private = {"shed": {"WHEAT": 96}, "inventories": [{"MILK": 8}]}
    obs = {"hour": 1, "player": 0}
    _a1, replan1 = main._execute_routes(obs, farm, private, 5, routes)
    assert replan1 is True                   # 104 > 100 projected overflow
    _a2, replan2 = main._execute_routes(obs, farm, private, 5, routes)
    assert replan2 is False                  # same plan -> gate stops it
    healthy = {"shed": {"WHEAT": 50}, "inventories": [{}]}
    _a3, replan3 = main._execute_routes(obs, farm, healthy, 5, routes)
    assert replan3 is False


def test_executor_d29_drop_then_sell_template():
    main._D29_SELL_QUEUE.clear()
    rows = _rows10()
    ax, ay = sorted(main._shed_access(10, ["NW"]))[0]
    farm = _farm(rows, farmer=(ax, ay))
    private = {"shed": {"WHEAT": 50}, "inventories": [{"MILK": 10}]}
    actions, replan = main._execute_routes({"hour": 1, "player": 0},
                                           farm, private, 29, [])
    assert replan is False
    # canonical engine form: bare DROP drops everything carried
    assert actions[0] == ["DROP"]
    assert main._D29_SELL_QUEUE[0] == {"MILK": 10}
    # # full shed: bare DROP still fires (engine destroys overflow) but
    # NOTHING enters the sell queue
    main._D29_SELL_QUEUE.clear()
    private = {"shed": {"WHEAT": 100}, "inventories": [{"MILK": 10}]}
    actions, _ = main._execute_routes({"hour": 1, "player": 0}, farm,
                                      private, 29, [])
    assert actions[0] == ["DROP"]
    assert 0 not in main._D29_SELL_QUEUE


# --------------------------------------------------------------------------
# M1/M2 scorecard plumbing: telemetry pulls the dawn mission shadow
# --------------------------------------------------------------------------

def test_telemetry_records_mission_shadow_fields():
    main._MISSION_SHADOW.clear()
    main.reset_telemetry()
    rows = _rows10()
    rows[3][3] = _tile_animal("COW", 2, unfed=1)
    farm = _farm(rows, hands=[(2, 2)])
    obs = {"player": 0, "day": 4, "hour": 0}
    main._mission_shadow_update(0, 4, 0, obs, farm, {}, None,
                                [_task(100, 3, 3, ["FEED"],
                                       ("feed", 3, 3), red=True)])
    main._telemetry_record_turn(obs, farm, {}, [["PASS"]], [], {}, [])
    snap = main.telemetry_snapshot()
    day = snap["players"]["0"]["days"]["4"]
    assert day["mission_hash"] is not None
    assert day["d1_count"] == 1
    assert day["tier_counts"].get("D1") == 1
    assert day["cap_util"] is not None
    assert day["cap_deficit"] is False
    main.reset_telemetry()
    main._MISSION_SHADOW.clear()


# --------------------------------------------------------------------------
# harness/calibration scripts (pure aggregation only; engine runs are the
# scripts' own CLI business, not unit-test business)
# --------------------------------------------------------------------------

def _load_script(name):
    path = os.path.join(SOFTWARE, "scripts", name)
    spec = importlib.util.spec_from_file_location(name[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_capacity_calibration_pure_aggregation():
    cc = _load_script("capacity_calibration.py")
    turn_rows = [
        {"source": "s", "episode": 1, "seat": 0, "day": 0,
         "hands": 2, "labor": 4, "units": 0.0},
        {"source": "s", "episode": 1, "seat": 0, "day": 0,
         "hands": 2, "labor": 2, "units": 0.0},   # same day -> summed
        {"source": "s", "episode": 1, "seat": 0, "day": 1,
         "hands": 2, "labor": 6, "units": 2.0},
        {"source": "s", "episode": 1, "seat": 0, "day": 2,
         "hands": 4, "labor": 12, "units": 4.0},
    ]
    days = cc.day_rows(turn_rows)
    assert len(days) == 3
    assert days[0]["labor"] == 6
    cal = cc.calibrate(days)
    assert cal["n_days"] == 3
    assert cal["all_days"]["turns_per_unit"]["median"] == 3.0
    assert cal["n_high_load"] == 0     # eff 6/72 and 12/120 < 0.5


def test_solver_shadow_stats_summarize():
    ss = _load_script("solver_shadow_stats.py")
    episodes = [{"seed": 1, "turns": 10, "passes": 4, "workers": 2,
                 "days": [
                     {"day": 0, "d1_total": 2, "d1_covered": 2,
                      "feasible": True, "dropped": 0, "feed_legs": 1,
                      "mission_hash": "a", "workers_empty": 0,
                      "workers": 2},
                     {"day": 1, "d1_total": 2, "d1_covered": 1,
                      "feasible": False, "dropped": 1, "feed_legs": 0,
                      "mission_hash": "b", "workers_empty": 1,
                      "workers": 2}]}]
    summary = ss.summarize(episodes)
    assert summary["d1_total"] == 4
    assert summary["d1_covered"] == 3
    assert summary["d1_coverage_rate"] == 0.75
    assert summary["infeasible_days"] == 1
    assert summary["mission_hash_stable"] is True
