"""Red-line checklist tests against synthetic farm snapshots.

Each rule (R1 watering / R2 feeding / R3 production caps / R4 shed / R5
deadlines / R6 supply) is exercised with a crafted state.
"""

from kgenv.redlines import check_farm, summary


def make_farm(tiles, money=3000.0, unlocked=None):
    return {
        "money": money,
        "tiles": tiles,
        "farmer": [4, 4],
        "hands": [],
        "unlocked_quadrants": unlocked or ["NW"],
        "hires_today": 0,
    }


def plant(crop, planted_day, watered=False, unwatered=0, yield_units=0):
    return {"kind": "PLANT", "crop": crop, "planted_day": planted_day,
            "watered_today": watered, "consecutive_unwatered": unwatered,
            "yield_units": yield_units, "max_lifespan_step": -1,
            "fertilized_until_day": -1}


def animal(kind="GOOSE", fed=False, unfed=0, yield_units=0, cared=False,
           fert=True, placed_day=0, pending=0):
    structure = "COOP" if kind == "GOOSE" else "PASTURE"
    return {"kind": structure, "animal": kind, "placed_day": placed_day,
            "yield_units": yield_units, "fed_today": fed,
            "consecutive_unfed": unfed, "cared_today": cared,
            "fertilizer_available": fert, "pending_care_bonus": pending}


def empty_private(shed=None, seeds=None):
    return {"shed": shed or {}, "seeds": seeds or {}, "inventories": [{}]}


def grid_1x1(tile):
    return [[tile]]


def codes(violations):
    return [v.code for v in violations]


def test_r1_plant_dies_tonight():
    farm = make_farm(grid_1x1(plant("WHEAT", 0, watered=False, unwatered=1)))
    v = check_farm(farm, empty_private(), day=2)
    assert "PLANT_DIES_TONIGHT" in codes(v)
    assert v[0].severity == "critical"


def test_r1_healthy_plant_no_violation():
    farm = make_farm(grid_1x1(plant("WHEAT", 0, watered=True, unwatered=0)))
    v = check_farm(farm, empty_private(), day=2)
    assert "PLANT_DIES_TONIGHT" not in codes(v)
    assert "PLANT_UNWATERED_TODAY" not in codes(v)


def test_r2_animal_escapes_tonight():
    farm = make_farm(grid_1x1(animal(fed=False, unfed=1)))
    v = check_farm(farm, empty_private(), day=3)
    assert "ANIMAL_ESCAPES_TONIGHT" in codes(v)
    assert v[0].severity == "critical"


def test_r2_feed_supply_short():
    farm = make_farm(grid_1x1(animal(fed=False, unfed=0)))
    v = check_farm(farm, empty_private(shed={"WHEAT": 0}), day=3)
    assert "FEED_SUPPLY_SHORT" in codes(v)


def test_r3_ongoing_finished_must_harvest():
    # tomato planted day 0, now day 19: last production was day 11
    farm = make_farm(grid_1x1(plant("TOMATO", 0, watered=True, yield_units=4)))
    v = check_farm(farm, empty_private(), day=19)
    assert "ONGOING_HARVEST_NOW" in codes(v)


def test_r3_one_time_past_window():
    farm = make_farm(grid_1x1(plant("WHEAT", 0, watered=True, yield_units=4)))
    v = check_farm(farm, empty_private(), day=9)
    assert "ONE_TIME_PAST_WINDOW" in codes(v)


def test_r4_shed_overflow_risk():
    farm = make_farm(grid_1x1(None))
    shed = {"WHEAT": 96, "EGG": 4}
    v = check_farm(farm, empty_private(shed=shed), day=5)
    assert "SHED_OVERFLOW_RISK" in codes(v)
    assert v[0].severity == "critical"


def test_r5_seed_past_deadline():
    farm = make_farm(grid_1x1(None))
    v = check_farm(farm, empty_private(seeds={"MELON": 3}), day=20)
    assert "SEED_PAST_DEADLINE" in codes(v)
    # wheat is still viable on day 20 (latest day 25)
    v2 = check_farm(farm, empty_private(seeds={"WHEAT": 3}), day=20)
    assert "SEED_PAST_DEADLINE" not in codes(v2)


def test_healthy_farm_no_criticals():
    tiles = [
        [plant("WHEAT", 20, watered=True), None],
        [animal(fed=True, unfed=0, yield_units=1), {"kind": "WEED"}],
    ]
    farm = make_farm(tiles)
    private = empty_private(shed={"WHEAT": 10}, seeds={"WHEAT": 2})
    v = check_farm(farm, private, day=22)
    s = summary(v)
    assert s["critical"] == 0
    assert "WEED_TILE" in codes(v)  # info-level only
