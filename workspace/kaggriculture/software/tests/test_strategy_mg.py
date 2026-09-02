"""M-G species-level herd NPV and structure-capacity regressions."""

from __future__ import annotations

import importlib.util

from kgenv.arena import SUBMISSION_MAIN


spec = importlib.util.spec_from_file_location("main_mg", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def _tiles(quadrants=("NW", "NE", "SW")):
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    for y in range(10):
        for x in range(10):
            quadrant = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            if quadrant in quadrants:
                tiles[y][x] = None
    return tiles


def _farm(*, money=8000.0, animals=()):
    tiles = _tiles()
    pending = list(animals)
    for row in tiles:
        for x, tile in enumerate(row):
            if tile is None and pending:
                animal = pending.pop(0)
                row[x] = {"kind": "PASTURE", "animal": animal,
                          "placed_day": 0, "yield_units": 0,
                          "consecutive_unfed": 0, "fed_today": False,
                          "cared_today": False,
                          "fertilizer_available": False}
    return {"money": money, "tiles": tiles, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": ["NW", "NE", "SW"], "hires_today": 0}


def _private(**shed):
    stock = {item: 0 for item in (*main.CROPS, *main.BASE_PRICE, *main.ANIMALS)}
    stock.update(shed)
    return {"shed": stock, "seeds": {"WHEAT": 20}, "inventories": [{}]}


def _prices(**overrides):
    prices = dict(main.BASE_PRICE)
    prices.update(overrides)
    return prices


def test_new_animal_production_evenings_include_first_yield_delay():
    assert main._new_animal_production_evenings(12, "COW") == 5
    assert main._new_animal_production_evenings(12, "SHEEP") == 4
    assert main._new_animal_production_evenings(16, "COW") == 3
    assert main._new_animal_production_evenings(16, "SHEEP") == 3
    assert main._new_animal_production_evenings(21, "COW") == 1
    assert main._new_animal_production_evenings(22, "COW") == 0


def test_npv_decision_returns_the_best_profitable_species():
    counts = {"COW": 8, "SHEEP": 6, "GOOSE": 0}
    demand = {"MILK": 20, "WOOL": 20}

    cow = main._npv_herd_decision(
        12, _prices(MILK=300, WOOL=100), 14, counts, demand, 40)
    sheep = main._npv_herd_decision(
        12, _prices(MILK=100, WOOL=300), 14, counts, demand, 40)

    assert cow == (main.HERD_CAP_NPV, "COW")
    assert sheep == (main.HERD_CAP_NPV, "SHEEP")


def test_legacy_ceiling_interface_stays_integer_and_fail_closed():
    counts = {"COW": 8, "SHEEP": 6, "GOOSE": 0}
    demand = {"MILK": 20, "WOOL": 20}

    assert main._npv_herd_ceiling(
        12, _prices(MILK=300), 14, counts, demand, 40) == main.HERD_CAP_NPV
    assert main._npv_herd_decision(
        12, _prices(MILK=300), 14, counts, demand, 10) == (main.HERD_CAP, None)


def test_scale_plan_builds_to_its_eighteen_head_structure_ceiling():
    farm = _farm()
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}

    scale_builds, scale_crops, *_ = main._field_alloc(farm, 12, _prices(), scale)
    defensive_builds, *_ = main._field_alloc(
        farm, 12, _prices(), dict(main._DEFENSIVE_PLAN))
    opening_builds, *_ = main._field_alloc(
        farm, 0, _prices(), dict(main._DEFENSIVE_PLAN))

    assert sum(kind == "PASTURE" for kind in scale_builds.values()) == \
        main.MODE_HERD_CAP_SCALE
    assert sum(kind == "PASTURE" for kind in defensive_builds.values()) == \
        main.HERD_CAP + 1
    assert sum(kind == "PASTURE" for kind in opening_builds.values()) == 5
    # V-T8: build lead tightened to one ahead of the herd plan (tetsuya
    # builds batch-by-batch), so the day-0 plan wants 5, not 6
    assert not set(scale_builds).intersection(
        set().union(*scale_crops.values()))


def test_scale_structure_extension_uses_real_empty_before_weed():
    tiles = _tiles()
    accesses = main._shed_access(10, ("NW", "NE", "SW"))
    field_positions = [
        (x, y) for y, row in enumerate(tiles) for x, tile in enumerate(row)
        if tile is None
        and not any(main._dist(x, y, *access) <= main.PASTURE_RING
                    for access in accesses)
    ]
    nearest_field = min(
        field_positions,
        key=lambda pos: min(main._dist(*pos, *access) for access in accesses))
    tiles[nearest_field[1]][nearest_field[0]] = {"kind": "WEED"}
    farm = _farm()
    farm["tiles"] = tiles
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}

    builds, *_ = main._field_alloc(farm, 12, _prices(), scale)

    assert nearest_field not in builds
    assert sum(kind == "PASTURE" for kind in builds.values()) == \
        main.MODE_HERD_CAP_SCALE


def test_scale_structure_extension_uses_field_empty_before_ring_weed():
    tiles = _tiles()
    accesses = main._shed_access(10, ("NW", "NE", "SW"))
    ring_positions = [
        (x, y) for y, row in enumerate(tiles) for x, tile in enumerate(row)
        if tile is None
        and any(main._dist(x, y, *access) <= main.PASTURE_RING
                for access in accesses)
        and not main._shed_adjacent(x, y, 10, ("NW", "NE", "SW"))
    ]
    ring_weed = ring_positions[0]
    tiles[ring_weed[1]][ring_weed[0]] = {"kind": "WEED"}
    farm = _farm()
    farm["tiles"] = tiles
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}

    builds, *_ = main._field_alloc(farm, 12, _prices(), scale)

    assert ring_weed not in builds
    assert sum(kind == "PASTURE" for kind in builds.values()) == \
        main.MODE_HERD_CAP_SCALE


def test_npv_extension_purchase_uses_selected_species():
    animals = ["COW"] * 8 + ["SHEEP"] * 6
    farm = _farm(animals=animals)
    private = _private(WHEAT=40)
    obs = {"player": 0, "day": 12, "hour": 0, "farms": [farm, _farm()],
           "private": private,
           "market": {"prices": _prices(MILK=300, WOOL=100)},
           "town": {"unlocked_shops": ["PIZZA_SHOP", "PIZZA_SHOP",
                                           "YARN_STORE", "YARN_STORE"]}}
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}
    main._STATE.clear()

    orders = main._market_orders(obs, farm, private, 12, 14, 14, scale)
    animal_orders = [order for order in orders if order[0] == "BUY_ANIMAL"]

    assert animal_orders
    assert animal_orders[0][1] == "COW"


def test_npv_selected_species_survives_skewed_existing_composition():
    animals = ["COW"] * 12 + ["SHEEP"] * 3
    farm = _farm(animals=animals)
    private = _private(WHEAT=40)
    obs = {"player": 0, "day": 12, "hour": 0, "farms": [farm, _farm()],
           "private": private,
           "market": {"prices": _prices(MILK=300, WOOL=100)},
           "town": {"unlocked_shops": ["PIZZA_SHOP"] * 4}}
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}
    main._STATE.clear()

    orders = main._market_orders(obs, farm, private, 12, 15, 15, scale)

    assert any(order[:2] == ["BUY_ANIMAL", "COW"] for order in orders)


def test_npv_purchase_quantity_respects_market_absorption():
    animals = ["COW"] * 12 + ["SHEEP"] * 2
    farm = _farm(animals=animals)
    private = _private(WHEAT=40)
    obs = {"player": 0, "day": 12, "hour": 0, "farms": [farm, _farm()],
           "private": private,
           "market": {"prices": _prices(MILK=300, WOOL=100)},
           "town": {"unlocked_shops": ["PIZZA_SHOP", "PIZZA_SHOP"]}}
    scale = {**main._DEFENSIVE_PLAN, "mode": "SCALE_RANCH", "scale": True,
             "herd_ceiling": main.MODE_HERD_CAP_SCALE}
    main._STATE.clear()

    orders = main._market_orders(obs, farm, private, 12, 14, 14, scale)
    animal_orders = [order for order in orders if order[0] == "BUY_ANIMAL"]

    assert animal_orders == [["BUY_ANIMAL", "COW", 1]]


def test_defensive_frame_uses_corrected_production_calendar():
    counts = {"COW": 8, "SHEEP": 6, "GOOSE": 0}
    decision = main._npv_herd_decision(
        16, _prices(MILK=161, WOOL=100), 14, counts,
        {"MILK": 20, "WOOL": 20}, 40, dict(main._DEFENSIVE_PLAN))

    assert main._new_animal_production_evenings(16, "COW") == 3
    assert decision == (main.HERD_CAP, None)
