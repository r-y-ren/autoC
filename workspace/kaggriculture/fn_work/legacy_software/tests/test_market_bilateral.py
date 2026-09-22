"""Differential coverage for the official bilateral market lockstep engine.

The test imports the vendored kaggle-environments wheel directly into a
per-test temporary directory.  A small independent mirror models only the
market operations used here, then compares every externally visible market
field and a derived fill ledger with the official ``_process_market`` result.
"""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
from pathlib import Path
import importlib
import importlib.util
import sys
import tempfile
import zipfile
from types import SimpleNamespace

import pytest


SOFTWARE = Path(__file__).resolve().parents[1]
WHEEL = SOFTWARE / "vendor" / "kaggle_environments-1.32.7+nodeps-py3-none-any.whl"


class _OfficialEngine:
    """Load the vendored package, even when another copy is installed."""

    def __enter__(self):
        self.tempdir = tempfile.TemporaryDirectory(prefix="kaggriculture-official-")
        with zipfile.ZipFile(WHEEL) as wheel:
            wheel.extractall(self.tempdir.name)
        self.saved = {
            name: module
            for name, module in sys.modules.items()
            if name == "kaggle_environments"
            or name.startswith("kaggle_environments.")
        }
        for name in list(self.saved):
            del sys.modules[name]
        self.old_path = list(sys.path)
        sys.path.insert(0, self.tempdir.name)
        importlib.invalidate_caches()
        self.engine = importlib.import_module(
            "kaggle_environments.envs.kaggriculture.kaggriculture"
        )
        assert Path(self.engine.__file__).resolve().is_relative_to(
            Path(self.tempdir.name).resolve()
        )
        return self.engine

    def __exit__(self, exc_type, exc, tb):
        for name in list(sys.modules):
            if name == "kaggle_environments" or name.startswith("kaggle_environments."):
                del sys.modules[name]
        sys.path[:] = self.old_path
        sys.modules.update(self.saved)
        self.tempdir.cleanup()


def _products(engine):
    return list(engine.PRODUCTS)


def _market(engine, item, inventory):
    values = {name: engine.MARKET_PARAMS[name]["I0"] for name in engine.PRODUCTS}
    values[item] = inventory
    market = {
        "inventory": values,
        "prices": {
            name: engine.market_price(name, values[name])
            for name in engine.PRODUCTS
        },
    }
    return market


def _farm(money):
    return {
        "money": float(money),
        "tiles": [[None] * 4 for _ in range(4)],
        "farmer": [1, 1],
        "hands": [],
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }


def _private(engine, shed):
    return {
        "shed": {item: int(shed.get(item, 0)) for item in _products(engine)},
        "seeds": {crop: 0 for crop in engine.CROPS},
        "inventories": [{}],
    }


def _state(engine, orders, money, shed, inventory, max_orders=10):
    farms = [_farm(money[0]), _farm(money[1])]
    privates = [_private(engine, shed[0]), _private(engine, shed[1])]
    market = _market(engine, inventory[0], inventory[1])
    observations = [
        SimpleNamespace(farms=farms, market=market, private=privates[seat])
        for seat in range(2)
    ]
    states = [
        SimpleNamespace(observation=observations[seat], action={"market": orders[seat]})
        for seat in range(2)
    ]
    env = SimpleNamespace(
        configuration={
            "boardSize": 4,
            "maxMarketOrdersPerTurn": max_orders,
            "farmHandCostMult": 1,
            "shedCapacity": 100,
        }
    )
    return states, env, farms, privates, market


def _snapshot(farms, privates, market):
    return {
        "wallet": [farms[seat]["money"] for seat in range(2)],
        "shed": [deepcopy(privates[seat]["shed"]) for seat in range(2)],
        "market_inventory": deepcopy(market["inventory"]),
        "prices": deepcopy(market["prices"]),
    }


def _mirror(engine, orders, money, shed, inventory, max_orders=10):
    """Independent per-unit bilateral mirror for the covered operations."""
    wallets = [float(money[0]), float(money[1])]
    sheds = [
        defaultdict(
            int,
            {
                item: int(shed[seat].get(item, 0))
                for item in engine.PRODUCTS
            },
        )
        for seat in range(2)
    ]
    market = {item: engine.MARKET_PARAMS[item]["I0"] for item in engine.PRODUCTS}
    market[inventory[0]] = inventory[1]
    fills = [defaultdict(int), defaultdict(int)]
    queues = [list(queue)[:max_orders] for queue in orders]

    for order_index in range(max((len(queue) for queue in queues), default=0)):
        active = []
        for seat, queue in enumerate(queues):
            order = queue[order_index] if order_index < len(queue) else None
            if not isinstance(order, list) or len(order) < 3:
                active.append(None)
                continue
            op, item = order[0], order[1]
            try:
                remaining = int(order[2])
            except (TypeError, ValueError):
                remaining = 0
            active.append({"op": op, "item": item, "remaining": remaining})

        while True:
            quoted = [None, None]
            for seat, state in enumerate(active):
                if state is None or state["remaining"] <= 0:
                    continue
                op, item = state["op"], state["item"]
                if op == "SELL" and item in engine.PRODUCTS:
                    price = engine.market_price(item, market[item])
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    price = engine.market_price(item, market[item] - 1)
                else:
                    active[seat] = None
                    continue
                quoted[seat] = (op, item, price)
            if all(value is None for value in quoted):
                break

            committed = False
            for seat, quote in enumerate(quoted):
                if quote is None:
                    continue
                op, item, price = quote
                if op == "SELL":
                    ok = sheds[seat][item] > 0
                    if ok:
                        sheds[seat][item] -= 1
                        wallets[seat] += price
                        if price > 1:
                            market[item] += 1
                else:
                    ok = wallets[seat] >= price and sum(sheds[seat].values()) < 100
                    if ok:
                        wallets[seat] -= price
                        sheds[seat][item] += 1
                        market[item] -= 1
                if ok:
                    active[seat]["remaining"] -= 1
                    fills[seat][(op, item)] += 1
                    committed = True
                else:
                    active[seat] = None
            if not committed:
                break

    prices = {
        item: engine.market_price(item, market[item]) for item in engine.PRODUCTS
    }
    return {
        "wallet": wallets,
        "shed": [dict(shed_for_seat) for shed_for_seat in sheds],
        "market_inventory": market,
        "prices": prices,
        "fills": [dict(values) for values in fills],
    }


def _actual_fills(orders, before, after):
    fills = [defaultdict(int), defaultdict(int)]
    for seat, queue in enumerate(orders):
        for order in queue:
            op, item = order[0], order[1]
            if op == "SELL":
                count = before["shed"][seat][item] - after["shed"][seat][item]
            elif op == "BUY_PRODUCT":
                count = after["shed"][seat][item] - before["shed"][seat][item]
            else:
                count = 0
            fills[seat][(op, item)] += max(0, count)
    return [dict(values) for values in fills]


def _run_case(engine, case, swap=False):
    orders = deepcopy(case["orders"])
    money = list(case["money"])
    shed = deepcopy(case["shed"])
    if swap:
        orders.reverse()
        money.reverse()
        shed.reverse()
    states, env, farms, privates, market = _state(
        engine,
        orders,
        money,
        shed,
        (case["item"], case["inventory"]),
        case.get("max_orders", 10),
    )
    before = _snapshot(farms, privates, market)
    expected = _mirror(
        engine,
        orders,
        money,
        shed,
        (case["item"], case["inventory"]),
        case.get("max_orders", 10),
    )
    engine._process_market(states, env)
    actual = _snapshot(farms, privates, market)
    actual["fills"] = _actual_fills(orders, before, actual)
    assert actual == expected
    return actual


CASES = {
    "both_sell": {
        "item": "WHEAT",
        "inventory": 10000,
        "money": [3000, 3000],
        "shed": [{"WHEAT": 3}, {"WHEAT": 2}],
        "orders": [[["SELL", "WHEAT", 3]], [["SELL", "WHEAT", 2]]],
    },
    "both_buy": {
        "item": "WHEAT",
        "inventory": 10000,
        "money": [3000, 3000],
        "shed": [{}, {}],
        "orders": [[["BUY_PRODUCT", "WHEAT", 3]], [["BUY_PRODUCT", "WHEAT", 2]]],
    },
    "buy_against_sell": {
        "item": "WHEAT",
        "inventory": 10000,
        "money": [3000, 3000],
        "shed": [{}, {"WHEAT": 4}],
        "orders": [[["BUY_PRODUCT", "WHEAT", 4]], [["SELL", "WHEAT", 4]]],
    },
    "funding_stops_order": {
        "item": "WHEAT",
        "inventory": 10000,
        "money": [51, 3000],
        "shed": [{}, {"WHEAT": 1}],
        "orders": [[["BUY_PRODUCT", "WHEAT", 4]], [["SELL", "WHEAT", 1]]],
    },
    "dollar_floor": {
        "item": "MELON",
        "inventory": 10500,
        "money": [3000, 3000],
        "shed": [{"MELON": 3}, {}],
        "orders": [[["SELL", "MELON", 3]], []],
    },
    "different_queue_lengths": {
        "item": "WHEAT",
        "inventory": 10000,
        "money": [3000, 3000],
        "shed": [{"WHEAT": 2, "CARROT": 1}, {"WHEAT": 1}],
        "orders": [[["SELL", "WHEAT", 2], ["SELL", "CARROT", 1]],
                   [["BUY_PRODUCT", "WHEAT", 1]]],
    },
}


@pytest.fixture(scope="module")
def official_engine():
    with _OfficialEngine() as engine:
        yield engine


@pytest.mark.parametrize("case_name", sorted(CASES))
@pytest.mark.parametrize("swap", [False, True], ids=["seat-order", "seat-order-exchanged"])
def test_bilateral_market_matches_official_mirror(official_engine, case_name, swap):
    _run_case(official_engine, CASES[case_name], swap=swap)


def test_exchange_seat_order_preserves_fieldwise_swapped_result(official_engine):
    for case in CASES.values():
        base = _run_case(official_engine, case, swap=False)
        exchanged = _run_case(official_engine, case, swap=True)
        assert exchanged["wallet"] == list(reversed(base["wallet"]))
        assert exchanged["shed"] == list(reversed(base["shed"]))
        assert exchanged["market_inventory"] == base["market_inventory"]
        assert exchanged["prices"] == base["prices"]
        assert exchanged["fills"] == list(reversed(base["fills"]))


def test_floor_case_explicitly_has_one_dollar_fill(official_engine):
    result = _run_case(official_engine, CASES["dollar_floor"])
    assert result["fills"] == [{("SELL", "MELON"): 3}, {}]
    assert result["wallet"] == [3003.0, 3000.0]
    assert result["market_inventory"]["MELON"] == 10500
    assert result["prices"]["MELON"] == 1
