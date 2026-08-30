"""v7 weed-reclaim pins (campaign r7-W/r7-H).

Two behaviours the v6 submission could not express:

  * WEED->DIG was unreachable (weeds never entered builds/crop_map);
    "planned" mode reserves reclaimable weeds BEHIND real empties and the
    planned-DIG branch fires for exactly those tiles; "all" also DIGs
    unplanned unlocked weeds; "none" reproduces v6 (no DIG ever).
  * PLANT after hour 21 burns the seed (fresh plant starts at streak 1,
    dies at the evening refresh unwatered); the EOD guard suppresses it.

The module under test is the v7 development tree
(kaggle_simulations/agent_v7/main.py), loaded via importlib so module
state stays isolated per test.
"""

import importlib.util
import sys
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
AGENT_V7 = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v7" / "main.py"


def _load(mode=None, guard=None, hour_min=None, rotation=None):
    spec = importlib.util.spec_from_file_location(
        f"v7_{mode}_{guard}_{hour_min}_{rotation}_{id([])}", AGENT_V7)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    if mode is not None:
        mod.WEED_RECLAIM_MODE = mode
    if guard is not None:
        mod.PLANT_EOD_GUARD = guard
    if hour_min is not None:
        mod.WEED_DIG_HOUR_MIN = hour_min
    if rotation is not None:
        mod.ROTATION_DIG = rotation
    return mod


def _farm(tiles, quads=("NW",)):
    return {"tiles": tiles, "unlocked_quadrants": list(quads),
            "farmer": [5, 6], "hands": [], "money": 3000}


def _open_board(weeds=()):
    tiles = [[None] * 12 for _ in range(12)]
    for x, y in weeds:
        tiles[y][x] = {"kind": "WEED"}
    return tiles


def _blocked_board(free=()):
    """Every tile PASTURE except the given free cells (None or WEED)."""
    tiles = [[{"kind": "PASTURE"} for _ in range(12)] for _ in range(12)]
    for x, y, kind in free:
        tiles[y][x] = None if kind == "empty" else {"kind": "WEED"}
    return tiles


def _obs_with(farm, hour=6, day=6):
    return {
        "day": day, "hour": hour, "player": 0,
        "farms": [farm],
        "market": {"prices": {"WHEAT": 25, "STRAWBERRY": 120}},
        "private": {"seeds": {"WHEAT": 20, "STRAWBERRY": 10},
                    "shed": {}, "inventories": [{}]},
    }


# --------------------------------------------------------------------------- #
# _field_alloc weed reservation
# --------------------------------------------------------------------------- #

def test_mode_none_reproduces_v6_skip():
    mod = _load(mode="none")
    farm = _farm(_open_board(weeds=[(0, 0)]))
    builds, crop_map, n_animals, cap = mod._field_alloc(
        farm, 6, {}, mod._DEFENSIVE_PLAN)
    planned = set().union(*crop_map.values()) | set(builds)
    assert (0, 0) not in planned


def test_planned_weed_reserved_only_when_empties_run_short():
    mod = _load(mode="planned")
    # open NW board: 30+ free tiles, caps never reach the appended weeds
    farm = _farm(_open_board(weeds=[(0, 0), (2, 0)]))
    builds, crop_map, n_animals, cap = mod._field_alloc(
        farm, 6, {}, mod._DEFENSIVE_PLAN)
    planned = set().union(*crop_map.values()) | set(builds)
    assert (0, 0) not in planned and (2, 0) not in planned

    # blocked board, the weed is the only free tile -> it IS reserved
    farm2 = _farm(_blocked_board(free=[(5, 2, "weed")]))
    builds2, crop_map2, n2, cap2 = mod._field_alloc(
        farm2, 6, {}, mod._DEFENSIVE_PLAN)
    planned2 = set().union(*crop_map2.values()) | set(builds2)
    assert (5, 2) in planned2


def test_locked_quadrant_weed_never_reserved():
    mod = _load(mode="planned")
    farm = _farm(_blocked_board(free=[(10, 10, "weed")]))  # SE locked
    builds, crop_map, n_animals, cap = mod._field_alloc(
        farm, 6, {}, mod._DEFENSIVE_PLAN)
    planned = set().union(*crop_map.values()) | set(builds)
    assert (10, 10) not in planned


# --------------------------------------------------------------------------- #
# _build_tasks DIG generation (C1 semantics pinned with the all-day window)
# --------------------------------------------------------------------------- #

def test_dig_task_generated_for_planned_weed():
    mod = _load(mode="planned", hour_min=0)
    farm = _farm(_blocked_board(free=[(5, 2, "weed")]))
    obs = _obs_with(farm)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    digs = [t for t in tasks if t["act"] == ["DIG"]]
    assert (5, 2) in [(t["x"], t["y"]) for t in digs]
    assert all(not t["red"] for t in digs)   # never a red-line task


def test_mode_all_digs_unplanned_weed_mode_none_does_not():
    for mode, expect in (("all", True), ("none", False)):
        mod = _load(mode=mode, hour_min=0)
        farm = _farm(_open_board(weeds=[(0, 0)]))  # far corner, unplanned
        obs = _obs_with(farm)
        tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
        digs = [t for t in tasks if t["act"] == ["DIG"]]
        assert bool(digs) is expect, mode


def test_dig_then_plant_chain_on_freed_tile():
    mod = _load(mode="planned", hour_min=0)
    farm = _farm(_blocked_board(free=[(5, 4, "weed")]))  # NW near-shed
    obs = _obs_with(farm)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    assert any(t["act"] == ["DIG"] and (t["x"], t["y"]) == (5, 4)
               for t in tasks)
    # engine semantics: DIG clears the tile -> the PLANT branch is reachable
    farm["tiles"][4][5] = None
    obs = _obs_with(farm)
    tasks2, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    assert any(t["act"][0] == "PLANT" and (t["x"], t["y"]) == (5, 4)
               for t in tasks2)


# --------------------------------------------------------------------------- #
# v7-C2 late-day window: DIG never competes with live production tasks
# --------------------------------------------------------------------------- #

def test_planned_dig_gated_to_late_day_window():
    mod = _load(mode="planned", hour_min=20)
    farm = _farm(_blocked_board(free=[(5, 2, "weed")]))
    obs = _obs_with(farm, hour=19)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    assert not any(t["act"] == ["DIG"] for t in tasks)
    obs = _obs_with(farm, hour=20)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    assert any(t["act"] == ["DIG"] and (t["x"], t["y"]) == (5, 2)
               for t in tasks)


# --------------------------------------------------------------------------- #
# v7-R rotation-DIG: a finished, harvested strawberry is dug out, not
# watered/fertilized to the horizon
# --------------------------------------------------------------------------- #

def _finished_straw(day=21):
    """Strawberry planted d5: production evenings d14/16/18/20, done d21."""
    return {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 5,
            "watered_today": False, "consecutive_unwatered": 0,
            "yield_units": 0, "max_lifespan_step": -1,
            "fertilized_until_day": -1}


def test_rotation_dig_fires_on_finished_strawberry():
    mod = _load(mode="none", rotation=True, hour_min=20)
    tiles = [[{"kind": "PASTURE"} for _ in range(12)] for _ in range(12)]
    tiles[4][5] = _finished_straw()
    farm = _farm(tiles)
    obs = _obs_with(farm, hour=21, day=21)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 21)
    assert any(t["act"] == ["DIG"] and (t["x"], t["y"]) == (5, 4)
               for t in tasks)
    # dead weight pays nothing: no WATER, no FERTILIZE on the finished tile
    assert not any(t["act"][0] in ("WATER", "FERTILIZE")
                   and (t["x"], t["y"]) == (5, 4) for t in tasks)
    # before the window (or with rotation off) v6 semantics return
    obs10 = _obs_with(farm, hour=10, day=21)
    tasks10, *_ = mod._build_tasks(obs10, farm, obs10["private"], 21)
    assert not any(t["act"] == ["DIG"] for t in tasks10)
    assert any(t["act"][0] == "WATER" and (t["x"], t["y"]) == (5, 4)
               for t in tasks10)


def test_rotation_dig_silent_while_productions_remain():
    mod = _load(mode="none", rotation=True, hour_min=20)
    tiles = [[{"kind": "PASTURE"} for _ in range(12)] for _ in range(12)]
    live = _finished_straw()
    tiles[4][5] = live          # still owes d20 this evening
    farm = _farm(tiles)
    obs = _obs_with(farm, hour=21, day=20)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 20)
    assert not any(t["act"] == ["DIG"] and (t["x"], t["y"]) == (5, 4)
                   for t in tasks)
    assert mod._ongoing_evenings_left("STRAWBERRY", live, 20) == 1
    assert mod._ongoing_evenings_left("STRAWBERRY", live, 21) == 0


def test_scheduler_dig_executable_on_weed_and_plant():
    mod = _load(mode="planned", hour_min=0)
    tiles = [[{"kind": "PASTURE"} for _ in range(12)] for _ in range(12)]
    tiles[0][0] = {"kind": "WEED"}
    tiles[0][1] = _finished_straw()
    farm = {"tiles": tiles, "unlocked_quadrants": ["NW"],
            "farmer": [0, 0], "hands": [], "money": 3000}
    obs = _obs_with(farm, hour=21, day=21)
    actions = mod.agent(obs)          # farmer stands on the WEED tile
    assert actions["farmer"] == ["DIG"]


# --------------------------------------------------------------------------- #
# PLANT end-of-day guard
# --------------------------------------------------------------------------- #

def test_plant_suppressed_after_hour_max_with_guard():
    mod = _load(mode="none", guard=True)
    farm = _farm(_blocked_board(free=[(5, 4, "empty")]))
    for hour in (22, 23):
        obs = _obs_with(farm, hour=hour)
        tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
        assert not any(t["act"][0] == "PLANT" for t in tasks), hour
    obs = _obs_with(farm, hour=20)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    assert any(t["act"][0] == "PLANT" for t in tasks)


def test_plant_guard_off_matches_v6_hours():
    mod = _load(mode="none", guard=False)
    farm = _farm(_blocked_board(free=[(5, 4, "empty")]))
    obs = _obs_with(farm, hour=23)
    tasks, *_ = mod._build_tasks(obs, farm, obs["private"], 6)
    # v6 planted at hour 23 too -- exactly the behaviour the guard removes
    assert any(t["act"][0] == "PLANT" for t in tasks)


# --------------------------------------------------------------------------- #
# v7.2-V1: VOLUME entry herd-readiness floor (seed-103 bankruptcy class)
# --------------------------------------------------------------------------- #

def _mk_farm_v72(quads=("NW", "NE", "SW"), money=5000.0, straw=0, herd=0):
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    half = 5
    for y in range(10):
        for x in range(10):
            q = ("N" if y < half else "S") + ("W" if x < half else "E")
            if q in quads:
                tiles[y][x] = None
    for i in range(straw):
        x, y = i % 5, i // 5
        if tiles[y][x] is None:
            tiles[y][x] = {"kind": "PLANT", "crop": "STRAWBERRY",
                           "planted_day": 5, "yield_units": 0}
    placed = 0
    for y in range(10):
        for x in range(10):
            if placed >= herd:
                break
            if tiles[y][x] is None:
                tiles[y][x] = {"kind": "PASTURE", "animal": "COW",
                               "placed_day": 0, "yield_units": 0}
                placed += 1
    return {"tiles": tiles, "money": money,
            "unlocked_quadrants": list(quads), "farmer": [4, 4],
            "hands": [], "hires_today": 0}


def _mk_obs_v72(mine, opp, prices=None, shops=("FARMERS_MARKET",)):
    prices = prices if prices is not None else {
        "WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
        "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
        "FERTILIZER": 100}
    return {"player": 0, "day": 8, "hour": 0,
            "market": {"prices": prices},
            "town": {"unlocked_shops": list(shops)},
            "farms": [mine, opp],
            "private": {"shed": {}, "seeds": {}, "inventories": [{}]}}


def test_volume_entry_requires_herd_floor():
    mod = _load()
    mod._PLAN_MEM.clear()
    # all other conditions met but the ranch floor is a 4-head opening
    # (the seed-103 bankruptcy class): stay DEFENSIVE
    obs = _mk_obs_v72(_mk_farm_v72(money=800, straw=6, herd=4),
                      _mk_farm_v72(straw=0, herd=10))
    assert mod._decide_mode(obs, 8, None)["mode"] == "DEFENSIVE"
    # herd 10 = the floor reached: the entry fires exactly as before
    ok = _mk_obs_v72(_mk_farm_v72(money=800, straw=6, herd=10),
                     _mk_farm_v72(straw=0, herd=10))
    assert mod._decide_mode(ok, 8, None)["mode"] == "VOLUME_CROP"


def test_volume_hold_survives_below_the_floor():
    # a legitimately entered field keeps its hold semantics when the herd
    # later dips (the floor gates ENTRY, not persistence -- liquidating a
    # working 30-tile field over 3 lost head would be its own disaster)
    mod = _load()
    mod._PLAN_MEM.clear()
    obs = _mk_obs_v72(_mk_farm_v72(money=1000, straw=30, herd=7),
                      _mk_farm_v72(straw=0))
    obs["market"]["prices"]["STRAWBERRY"] = 60
    assert mod._decide_mode(obs, 16, "VOLUME_CROP")["mode"] == "VOLUME_CROP"


# --------------------------------------------------------------------------- #
# v7.2-V2 land-after-ranch sequencing: REJECTED (ablation v72_v2_landseq:
# 46W-42L net -349k, all three indicators worse -- deferring SW pushed the
# third-quadrant strawberry payoff out of the phase window).  The SW
# purchase keeps the r4 d7+ rule; no test pins the rejected knob.
# --------------------------------------------------------------------------- #
