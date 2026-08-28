"""Economy model unit tests.

The expected price triples come from the OFFICIAL How-to-Play price table
(captured 2026-08-28): columns P(I0-T), P(I0+T), P(I0+2T).  Verifying our
pricing wrappers against the published table pins the whole economy model
to the engine's actual constants.
"""

import pytest

from kgenv.economy import (
    ANIMALS, CROPS, MARKET_I0, MARKET_PARAMS, PRODUCTS,
    animal_model, crop_cycle_model, glut_sensitivity_report, hire_costs,
    latest_planting_day, land_cost, price, price_after_selling,
)

# item: (P(I0-T), P(I0+T), P(I0+2T)) from the official How-to-Play table
OFFICIAL_PRICE_TABLE = {
    "WHEAT": (45, 20, 19),
    "CARROT": (70, 10, 1),
    "TOMATO": (84, 24, 9),
    "STRAWBERRY": (204, 1, 1),
    "MELON": (300, 1, 1),
    "EGG": (70, 40, 39),
    "MILK": (256, 1, 1),
    "WOOL": (240, 1, 1),
    "FERTILIZER": (140, 60, 20),
}


@pytest.mark.parametrize("item,expected", sorted(OFFICIAL_PRICE_TABLE.items()))
def test_price_matches_official_table(item, expected):
    T = MARKET_PARAMS[item]["T"]
    assert price(item, MARKET_I0) == MARKET_PARAMS[item]["base"]
    assert price(item, MARKET_I0 - T) == expected[0]
    assert price(item, MARKET_I0 + T) == expected[1]
    assert price(item, MARKET_I0 + 2 * T) == expected[2]


def test_price_floor_is_one():
    # dumping a huge glut of a premium good bottoms out at $1
    assert price("MELON", MARKET_I0 + 10_000) == 1
    assert price_after_selling("MELON", 400)["final_price"] == 1


def test_one_time_crop_yields():
    # unfertilized max yields: wheat 4, carrot 3, melon 6 (official table)
    assert crop_cycle_model("WHEAT").yield_units == 4
    assert crop_cycle_model("CARROT").yield_units == 3
    assert crop_cycle_model("MELON").yield_units == 6
    # fertilized: wheat 6 (cap), carrot 4 (cap), melon 6 (cap, reached earlier)
    assert crop_cycle_model("WHEAT", fertilized=True).yield_units == 6
    assert crop_cycle_model("CARROT", fertilized=True).yield_units == 4
    assert crop_cycle_model("MELON", fertilized=True).yield_units == 6


def test_ongoing_crop_yields():
    # tomato: 4 productions x 1 = 4 units; fertilized doubles to 8
    assert crop_cycle_model("TOMATO").yield_units == 4
    assert crop_cycle_model("TOMATO", fertilized=True).yield_units == 8
    assert crop_cycle_model("STRAWBERRY").yield_units == 4


def test_crop_cycle_shapes():
    m = crop_cycle_model("WHEAT")
    assert m.cycle_days == 5            # plant day 0, harvest day 4
    assert m.seed_cost == CROPS["WHEAT"]["seed"]
    assert m.revenue_at_base == 4 * 25  # 4 units x $25 base
    assert m.profit_at_base == m.revenue_at_base - 10
    melon = crop_cycle_model("MELON")
    assert melon.cycle_days == 13       # harvest on day 12
    assert melon.per_tile_day_base > crop_cycle_model("WHEAT").per_tile_day_base


def test_latest_planting_day():
    assert latest_planting_day("WHEAT") == 25       # 29 - 4
    assert latest_planting_day("CARROT") == 26      # 29 - 3
    assert latest_planting_day("MELON") == 17       # 29 - 12
    assert latest_planting_day("TOMATO") == 17      # 29 - (8 + 3*1 + 1)
    assert latest_planting_day("STRAWBERRY") == 12  # 29 - (10 + 3*2 + 1)


def test_animal_care_doubles_goose_output():
    plain = animal_model("GOOSE", cared=False)
    cared = animal_model("GOOSE", cared=True)
    assert cared.gross_per_day == pytest.approx(2 * plain.gross_per_day)
    assert plain.first_yield_day == ANIMALS["GOOSE"]["first_yield_day"]
    # fertilizer adds a flat 1/day per animal regardless of care
    assert cared.fertilizer_per_day == plain.fertilizer_per_day == 1


def test_glut_sensitivity_ordering():
    report = glut_sensitivity_report(units=60)
    by_item = {r["item"]: r for r in report}
    # wheat absorbs gluts far better than strawberry (official curve shapes)
    assert by_item["WHEAT"]["retention"] > by_item["STRAWBERRY"]["retention"]
    assert by_item["EGG"]["retention"] > by_item["MILK"]["retention"]
    # the steepest crashers are the premium above_target>1 products
    worst = report[0]["item"]
    assert worst in ("STRAWBERRY", "MELON", "MILK", "WOOL")


def test_hire_costs_fibonacci():
    assert hire_costs(6) == [1, 1, 2, 3, 5, 8]
    assert sum(hire_costs(4)) == 7


def test_land_costs():
    assert land_cost(1) == 1000
    assert land_cost(2) == 2000
    assert land_cost(3) == 4000
    assert land_cost(4) is None  # fully unlocked


def test_sell_revenue_is_sequential():
    # selling 60 wheat from equilibrium yields slightly less than 60 x base
    r = price_after_selling("WHEAT", 60)
    assert r["avg_price"] < 25
    assert r["avg_price"] > 20
    # revenue grows monotonically with units
    assert price_after_selling("WHEAT", 10)["revenue"] < \
        price_after_selling("WHEAT", 20)["revenue"]
