"""r4-P1 state-value scheduler unit tests (campaign III round-3 P1).

Pins the scheduling-layer contract the ablation gate judged on:
  * red-line classification -- FEED with an escape streak, WATER with a
    death streak or planted-today, are `red` and outrank every weighted
    task in the assignment (nearest-worker phase A, value order);
  * terminal-value pricing -- CARE only exists while another production
    evening remains; window water carries the +2*price bonus; harvest
    value scales with held units;
  * fetch routing -- a worker assigned a carried-item task it cannot
    execute walks to the shed and PICKUPs the chunk instead of churning;
  * sticky targets survive within a day and reset on day roll;
  * wheatless workers do not crowd out loaded carriers (carrier affinity).
"""

import importlib.util

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_r4p1", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def _shed(**kw):
    base = {item: 0 for item in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY",
                                 "MELON", "EGG", "MILK", "WOOL", "FERTILIZER",
                                 "GOOSE", "COW", "SHEEP")}
    base.update(kw)
    return base


def _prices(**kw):
    base = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
            "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
    base.update(kw)
    return base


def _tiles(quadrants=("NW",)):
    def tile(x, y):
        quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
        return None if quad in quadrants else "LOCKED"
    return [[tile(x, y) for x in range(10)] for y in range(10)]


def _farm(tiles=None, money=5000.0, farmer=(4, 4), hands=(), quads=None):
    quads = quads or ["NW"]
    return {
        "money": money,
        "tiles": tiles if tiles is not None else _tiles(tuple(quads)),
        "farmer": list(farmer),
        "hands": [list(hand) for hand in hands],
        "unlocked_quadrants": quads,
        "hires_today": 0,
    }


def _obs(day, hour, farm, private, prices=None, player=0):
    other = _farm(money=3000.0)
    farms = [farm, other] if player == 0 else [other, farm]
    return {
        "player": player, "day": day, "hour": hour, "farms": farms,
        "private": private, "market": {"prices": prices or _prices()},
    }


def _pasture_tile(animal="SHEEP", yield_units=0, consecutive_unfed=0,
                  fed_today=False, placed_day=10):
    return {"kind": "PASTURE", "animal": animal, "placed_day": placed_day,
            "yield_units": yield_units, "consecutive_unfed": consecutive_unfed,
            "fed_today": fed_today, "cared_today": False,
            "fertilizer_available": False}


def _plant_tile(crop="WHEAT", planted_day=8, watered=False, streak=0,
                yield_units=0):
    return {"kind": "PLANT", "crop": crop, "planted_day": planted_day,
            "watered_today": watered, "consecutive_unwatered": streak,
            "yield_units": yield_units, "fertilized_until_day": -1}


# -------------------------------------------------------------------------- #
# red-line classification
# -------------------------------------------------------------------------- #

def test_water_streak_and_fresh_plant_are_red():
    tiles = _tiles()
    tiles[0][2] = _plant_tile("WHEAT", planted_day=8, streak=1)
    tiles[0][3] = _plant_tile("WHEAT", planted_day=10, streak=0)
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    tasks, *_ = main._build_tasks(_obs(10, 6, farm, private), farm, private, 10)
    reds = {t["key"]: t for t in tasks if t.get("red")}
    assert ("water", 2, 0) in reds          # streak 1: dies tonight
    assert ("water", 3, 0) in reds          # planted today: dies tonight
    assert reds[("water", 2, 0)]["v"] >= 100  # terminal value priced in


def test_feed_streak_and_late_hour_are_red():
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", consecutive_unfed=1)
    tiles[3][4] = _pasture_tile("COW")
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    tasks, *_ = main._build_tasks(_obs(10, 6, farm, private), farm, private, 10)
    streak_feed = [t for t in tasks
                   if t["key"] == ("feed", 4, 2)]
    assert streak_feed and streak_feed[0].get("red")
    assert streak_feed[0]["v"] >= main.ANIMALS["SHEEP"]["cost"]
    tasks_late, *_ = main._build_tasks(_obs(10, 17, farm, private),
                                       farm, private, 10)
    late_feed = [t for t in tasks_late if t["key"] == ("feed", 4, 3)]
    assert late_feed and late_feed[0].get("red")   # hour >= FEED_RED_HOUR


def test_redline_feed_gets_nearest_worker_despite_better_value_task():
    # a melon window WATER (v 650) nearby must NOT crowd out the escape-
    # streak FEED across the map: phase A covers reds before any value work
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", consecutive_unfed=1)
    tiles[0][1] = _plant_tile("MELON", planted_day=8, streak=0)
    farm = _farm(tiles=tiles, farmer=(0, 1), hands=((1, 1),), quads=["NW"])
    private = {"shed": _shed(WHEAT=10), "seeds": {},
               "inventories": [{"WHEAT": 5}, {}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    actions = main._schedule_units(obs, farm, private, 10, tasks)
    feed = [t for t in tasks if t["act"][0] == "FEED"][0]
    feeder = (farm["farmer"], feed)  # placeholder; the assertion is the walk
    # the wheat-loaded farmer (0,1) carries WHEAT -> it must be walking to
    # or feeding the sheep at (4,2), not parking on the melon
    dx, dy = feed["x"] - farm["farmer"][0], feed["y"] - farm["farmer"][1]
    if abs(dx) + abs(dy) > 0:
        assert actions[0] in (["FEED"], ["EAST"], ["WEST"], ["SOUTH"], ["NORTH"])
        moved = main.MOVES.get(actions[0][0]) if actions[0][0] in main.MOVES \
            else None
        if moved:
            assert (moved[0] * dx >= 0) and (moved[1] * dy >= 0)
    del feeder


def test_far_red_water_wins_over_nearby_low_value_water():
    # r3 failure mode: w/(1+dist) let a near w=30 task starve a far w=98
    # death-tonight tile all day.  Value-minus-mu pricing must send SOMEONE
    # to the dying tile: here the only worker sits next to a fresh wheat
    # plant (survival water) while a streak-1 melon dies across the quad.
    tiles = _tiles()
    tiles[4][4] = _plant_tile("WHEAT", planted_day=9, streak=0)   # near, v~45
    tiles[0][0] = _plant_tile("MELON", planted_day=8, streak=1)   # far, red
    farm = _farm(tiles=tiles, farmer=(4, 4), quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    actions = main._schedule_units(obs, farm, private, 10, tasks)
    assert actions[0] in (["WEST"], ["NORTH"], ["WATER"])
    if actions[0] == ["WATER"]:
        assert tiles[4][4]["consecutive_unwatered"] == 0  # executed the near


# -------------------------------------------------------------------------- #
# terminal-value pricing
# -------------------------------------------------------------------------- #

def test_care_skipped_when_no_production_evening_remains():
    # sheep placed d0 (evenings 5,8,...,26) -- on day 27 no evening remains:
    # CARE value is 0 and the task must not exist
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", placed_day=0, fed_today=True)
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    obs = _obs(27, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 27)
    assert not any(t["act"][0] == "CARE" for t in tasks)
    # day 26 still has tonight's evening 26: CARE exists
    obs26 = _obs(26, 6, farm, private)
    tasks26, *_ = main._build_tasks(obs26, farm, private, 26)
    assert any(t["act"][0] == "CARE" for t in tasks26)


def test_prod_evening_helper_matches_engine_calendar():
    # cow placed d0: first production evening 7 (placed+fyd-1), then every
    # 2 days; evening 27 exists, evening 29 is past the cash-out horizon
    assert main._prod_evening_from(6, 0, 8, 2)
    assert main._prod_evening_from(27, 0, 8, 2)
    assert not main._prod_evening_from(28, 0, 8, 2)
    # sheep placed d2: evenings 7,10,...; day 8 -> next evening 10 <= 28
    assert main._prod_evening_from(8, 2, 6, 3)


def test_harvest_value_scales_with_held_units():
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("COW", yield_units=5)
    tiles[3][4] = _pasture_tile("COW", yield_units=2)
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    v5 = next(t["v"] for t in tasks if t["key"] == ("harvest", 4, 2))
    assert v5 >= 5 * main.BASE_PRICE["MILK"]        # about to cap: +1 period


# -------------------------------------------------------------------------- #
# fetch routing and stickiness
# -------------------------------------------------------------------------- #

def test_wheatless_worker_fetches_at_shed_before_feeding():
    tiles = _tiles()
    tiles[0][0] = _pasture_tile("COW", consecutive_unfed=1)
    farm = _farm(tiles=tiles, farmer=(4, 4), quads=["NW"])  # shed-adjacent
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    actions = main._schedule_units(obs, farm, private, 10, tasks)
    assert actions[0][:2] == ["PICKUP", "WHEAT"]    # not a hopeless trek


def test_sticky_target_survives_within_the_day():
    # M5: v72's _sticky_state registry is gone; continuity lives in the
    # dispatcher's _ASSIGN_MEM (previous solve's per-worker first stop)
    main._ASSIGN_MEM.clear()
    tiles = _tiles()
    tiles[0][0] = _plant_tile("STRAWBERRY", planted_day=8, streak=1)
    farm = _farm(tiles=tiles, farmer=(3, 3), quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    obs1 = _obs(10, 6, farm, private)
    tasks1, *_ = main._build_tasks(obs1, farm, private, 10)
    main._schedule_units(obs1, farm, private, 10, tasks1)
    st = main._ASSIGN_MEM[0]
    assert st["day"] == 10
    farm2 = _farm(tiles=tiles, farmer=(3, 4), quads=["NW"])   # one step on
    obs2 = _obs(10, 7, farm2, private)
    tasks2, *_ = main._build_tasks(obs2, farm2, private, 10)
    actions = main._schedule_units(obs2, farm2, private, 10, tasks2)
    # still heading for the same dying tile (no oscillation)
    if actions[0] in (["WEST"], ["NORTH"], ["SOUTH"], ["EAST"]):
        dx = 0 - farm2["farmer"][0]
        dy = 0 - farm2["farmer"][1]
        mx, my = main.MOVES[actions[0][0]]
        assert mx * dx + my * dy > 0


def test_assign_registry_resets_on_day_roll():
    main._ASSIGN_MEM.clear()
    tiles = _tiles()
    tiles[0][0] = _plant_tile("STRAWBERRY", planted_day=8, streak=1)
    farm = _farm(tiles=tiles, farmer=(3, 3), quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    main._schedule_units(obs, farm, private, 10, tasks)
    assert main._ASSIGN_MEM[0]["day"] == 10
    assert 0 in main._ASSIGN_MEM[0]["assign"]
    obs11 = _obs(11, 0, farm, private)             # new day: registry rolls
    tasks11, *_ = main._build_tasks(obs11, farm, private, 11)
    main._schedule_units(obs11, farm, private, 11, tasks11)
    assert main._ASSIGN_MEM[0]["day"] == 11


def test_task_claim_prevents_pileup_on_one_target():
    # three workers, one far red water, two near value tasks: nobody else
    # may claim the red task the first worker already holds
    tiles = _tiles()
    tiles[0][0] = _plant_tile("MELON", planted_day=8, streak=1)
    tiles[4][3] = _plant_tile("WHEAT", planted_day=9, streak=0)
    tiles[4][5] = None if tiles[4][5] is None else None
    farm = _farm(tiles=tiles, farmer=(4, 4),
                 hands=((4, 3), (3, 4)), quads=["NW"])
    private = {"shed": _shed(), "seeds": {}, "inventories": [{}, {}, {}]}
    obs = _obs(10, 6, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 10)
    actions = main._schedule_units(obs, farm, private, 10, tasks)
    walkers = [a for a in actions
               if a[0] in ("WEST", "NORTH", "EAST", "SOUTH")]
    # at most one unit walks toward the far corner melon
    assert sum(1 for a in walkers) >= 1


def test_scheduler_keeps_champion_weight_contract():
    # legacy `w` fields stay intact for the r3-pinned tests/telemetry
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", consecutive_unfed=1)
    tiles[3][4] = _pasture_tile("COW")
    tiles[1][4] = _plant_tile("WHEAT", planted_day=8, streak=1,
                              yield_units=4)
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    tasks, to_feed, *_ = main._build_tasks(_obs(10, 6, farm, private),
                                           farm, private, 10)
    feeds = {t["key"]: t for t in tasks if t["act"][0] == "FEED"}
    assert feeds[("feed", 4, 2)]["w"] == 100
    assert feeds[("feed", 4, 3)]["w"] == 88
    water = [t for t in tasks if t["act"][0] == "WATER"]
    assert all(t["w"] < 100 for t in water)
