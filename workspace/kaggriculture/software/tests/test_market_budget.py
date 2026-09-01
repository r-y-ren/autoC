"""P0-C market queue budget regressions."""

from __future__ import annotations

import hashlib
import importlib.util
import inspect
from pathlib import Path
import zipfile

import pytest

from kgenv.arena import SUBMISSION_MAIN

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("main_market_budget", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)

OFFICIAL = pytest.importorskip(
    "kaggle_environments.envs.kaggriculture.kaggriculture")


@pytest.fixture(scope="module", autouse=True)
def installed_engine_must_be_the_vendored_reference():
    wheel = SOFTWARE_ROOT / "vendor" / \
        "kaggle_environments-1.32.7+nodeps-py3-none-any.whl"
    with zipfile.ZipFile(wheel) as archive:
        reference = archive.read(
            "kaggle_environments/envs/kaggriculture/kaggriculture.py")
    installed = Path(inspect.getsourcefile(OFFICIAL)).read_bytes()
    assert hashlib.sha256(installed).digest() == hashlib.sha256(reference).digest(), \
        "installed kaggriculture engine differs from the vendored 1.32.7 reference"


def _official_market_out(money, orders, shed_wheat=0):
    """Run one queue through the VENDORED official engine and report state."""
    from types import SimpleNamespace

    farm = OFFICIAL._new_farm(10, 3000)
    farm["money"] = float(money)
    opp = OFFICIAL._new_farm(10, 3000)
    priv = OFFICIAL._new_private()
    priv["shed"]["WHEAT"] = shed_wheat
    market = OFFICIAL._new_market()

    def seat(farms, private, action):
        return SimpleNamespace(
            observation=SimpleNamespace(farms=farms, market=market,
                                        private=private),
            action=action)

    state = [seat([farm], priv, {"market": orders}),
             seat([opp], OFFICIAL._new_private(), {})]
    OFFICIAL._process_market(state, SimpleNamespace(configuration={}))
    return {"money": float(farm["money"]),
            "wheat_inventory": int(market["inventory"]["WHEAT"]),
            "shed_wheat": int(priv["shed"]["WHEAT"]),
            "bought": 10000 - int(market["inventory"]["WHEAT"])}


def _official_market_state(money, orders, *, shed_stock=None, hires_today=0,
                           quadrants_owned=1):
    from types import SimpleNamespace

    farm = OFFICIAL._new_farm(10, 3000)
    farm["money"] = float(money)
    farm["hires_today"] = hires_today
    for _ in range(max(0, quadrants_owned - 1)):
        farm["money"] += 10000
        OFFICIAL._do_buy_land(farm, 10)
    farm["money"] = float(money)
    private = OFFICIAL._new_private()
    private["shed"].update(shed_stock or {})
    market = OFFICIAL._new_market()
    opponent = OFFICIAL._new_farm(10, 3000)

    def seat(farms, private_state, action):
        return SimpleNamespace(observation=SimpleNamespace(
            farms=farms, market=market, private=private_state), action=action)

    state = [seat([farm, opponent], private, {"market": orders}),
             seat([farm, opponent], OFFICIAL._new_private(), {})]
    OFFICIAL._process_market(state, SimpleNamespace(configuration={}))
    return {
        "money": farm["money"],
        "shed": dict(private["shed"]),
        "seeds": dict(private["seeds"]),
        "market_inventory": dict(market["inventory"]),
        "hands": len(farm["hands"]),
        "quadrants": len(farm["unlocked_quadrants"]),
        "remaining_capacity": 100 - sum(private["shed"].values()),
    }


def test_mixed_queue_dry_run_matches_vendored_engine_final_state():
    orders = [["HIRE"]] * 5 + [["BUY_LAND"],
              ["SELL", "MILK", 3],
              ["BUY_SEED", "STRAWBERRY", 2],
              ["BUY_PRODUCT", "WHEAT", 5],
              ["BUY_ANIMAL", "SHEEP", 1]]
    initial_shed = {"MILK": 3}
    official = _official_market_state(3000, orders, shed_stock=initial_shed)
    report = main.plan_market_orders(
        orders, money=3000, shed_count=3, shed_stock=initial_shed,
        market_inventory={item: 10000 for item in main.BASE_PRICE}, max_orders=10)

    assert report["remaining_money"] == official["money"]
    assert report["shed_stock"] == official["shed"]
    assert report["seed_stock"] == official["seeds"]
    assert report["market_inventory"] == official["market_inventory"]
    assert report["hands_count"] == official["hands"]
    assert report["quadrants_owned"] == official["quadrants"]
    assert report["remaining_capacity"] == official["remaining_capacity"]


def test_planner_matches_official_engine_buy20_with_balance_500():
    official = _official_market_out(500.0, [["BUY_PRODUCT", "WHEAT", 20]])
    report = main.plan_market_orders(
        [["BUY_PRODUCT", "WHEAT", 20]], money=500, shed_count=0,
        market_inventory={"WHEAT": 10000})
    assert report["orders"][0]["filled"] == official["bought"]
    assert report["remaining_money"] == official["money"]
    assert report["market_inventory"]["WHEAT"] == official["wheat_inventory"]
    assert report["shed_count"] == official["shed_wheat"]


def test_planner_matches_official_engine_sell30_per_unit_state():
    official = _official_market_out(3000.0, [["SELL", "WHEAT", 30]],
                                    shed_wheat=30)
    report = main.plan_market_orders(
        [["SELL", "WHEAT", 30]], money=3000, shed_count=30,
        shed_stock={"WHEAT": 30}, market_inventory={"WHEAT": 10000})
    assert report["accepted"] == [["SELL", "WHEAT", 30]]
    assert report["remaining_money"] == official["money"]
    assert report["market_inventory"]["WHEAT"] == official["wheat_inventory"]
    assert report["shed_count"] == official["shed_wheat"] == 0


def test_planner_reprices_buy_product_units_like_engine():
    # 5 wheat from I0: engine quotes 26+26+27+27+27 = 133 (post-buy inventory
    # pricing), not 5 x 25.  Differential: planner total must equal engine.
    official = _official_market_out(3000.0, [["BUY_PRODUCT", "WHEAT", 5]])
    report = main.plan_market_orders(
        [["BUY_PRODUCT", "WHEAT", 5]], money=3000, shed_count=0,
        market_inventory={"WHEAT": 10000})
    assert report["committed_spend"] == 3000.0 - official["money"]
    assert report["committed_spend"] == 133


def test_budget_planner_accounts_for_hires_land_rotation_feed_and_animals():
    orders = [["HIRE"], ["HIRE"], ["BUY_LAND"],
              ["BUY_SEED", "STRAWBERRY", 1],
              ["BUY_PRODUCT", "WHEAT", 5], ["BUY_ANIMAL", "COW", 1]]
    report = main.plan_market_orders(orders, money=3000, shed_count=0,
                                     land_costs=[1000], max_orders=10)
    assert report["accepted"] == orders
    assert report["committed_spend"] == 1 + 1 + 1000 + 100 + 133 + 400
    assert report["remaining_money"] == 1365


def test_budget_planner_accounts_for_five_hires_land_rotation_feed_and_animals():
    orders = [["HIRE"]] * 5 + [["BUY_LAND"],
              ["BUY_SEED", "STRAWBERRY", 1],
              ["BUY_PRODUCT", "WHEAT", 5], ["BUY_ANIMAL", "COW", 1]]
    report = main.plan_market_orders(orders, money=3000, shed_count=0,
                                     land_costs=[1000], max_orders=10)
    assert report["accepted"] == orders
    assert report["committed_spend"] == 1 + 1 + 2 + 3 + 5 + 1000 + 100 + 133 + 400
    assert report["remaining_money"] == 1355

def test_budget_planner_day0_opening_herd_is_not_displaced_by_seed_or_feed():
    orders = [["BUY_ANIMAL", "COW", 2], ["BUY_ANIMAL", "SHEEP", 2],
              ["BUY_SEED", "WHEAT", 12], ["BUY_PRODUCT", "WHEAT", 8]]
    report = main.plan_market_orders(orders, money=3000, shed_count=0,
                                     max_orders=10)
    assert report["accepted"][:2] == orders[:2]
    assert report["remaining_money"] >= 0


def test_budget_planner_stops_current_order_on_first_unit_insufficient():
    # Engine repricing: 26+26=52 of 60 spent, the 3rd unit (27) aborts the
    # order; the seed column still runs but 8 < 10 cannot afford one seed.
    report = main.plan_market_orders(
        [["BUY_PRODUCT", "WHEAT", 5], ["BUY_SEED", "WHEAT", 1]],
        money=60, shed_count=0, max_orders=10)
    assert report["accepted"] == [["BUY_PRODUCT", "WHEAT", 2]]
    assert report["orders"][0]["filled"] == 2
    assert report["orders"][0]["abort"] == "no_money"
    assert report["orders"][1]["filled"] == 0
    assert report["orders"][1]["abort"] == "no_money"


def test_budget_planner_capacity_rejects_buy_product_without_spending():
    report = main.plan_market_orders(
        [["BUY_PRODUCT", "WHEAT", 1], ["BUY_ANIMAL", "COW", 1]],
        money=2000, shed_count=100, shed_capacity=100, max_orders=10)
    assert report["accepted"] == []
    assert all(item["abort"] == "shed_full" for item in report["orders"])
    assert report["committed_spend"] == 0


def test_budget_planner_max_ten_keeps_feed_and_day29_recovery_in_order():
    orders = [["HIRE"]] * 5 + [["BUY_SEED", "MELON", 1]] * 4 + \
             [["BUY_PRODUCT", "WHEAT", 10]] + \
             [["SELL", "MILK", 20], ["SELL", "WOOL", 20]]
    report = main.plan_market_orders(orders, money=10000, shed_count=50,
                                     day=29, max_orders=10)
    assert len(report["accepted"]) <= 10
    assert any(order[:2] == ["SELL", "MILK"] for order in report["accepted"])
    assert any(order[:2] == ["SELL", "WOOL"] for order in report["accepted"])
    assert report["accepted"] == [order for order in orders
                                   if order in report["accepted"]]


def test_agent_market_contract_stays_positive_and_at_most_ten():
    from tests.test_p0_wave import _farm, _private, _obs
    private = _private(WHEAT=12)
    private["seeds"] = {"WHEAT": 10, "STRAWBERRY": 4, "MELON": 4,
                         "CARROT": 0, "TOMATO": 0}
    action = main.agent(_obs(8, 0, _farm(("NW", "NE"), money=5000), private))
    assert len(action["market"]) <= 10
    assert all(len(order) < 3 or order[2] > 0 for order in action["market"])
