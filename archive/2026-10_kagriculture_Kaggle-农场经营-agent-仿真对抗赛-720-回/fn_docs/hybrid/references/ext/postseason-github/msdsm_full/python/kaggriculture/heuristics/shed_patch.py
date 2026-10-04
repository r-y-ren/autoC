"""Shed post-processing applied to the policy's action: overnight room and the final sale.

The score is money only. Goods are lost to the shed (capacity 100) in two ways, measured on 120
ladder replays (expB24 child_exp00): the end-of-day sweep moves every pocket into the shed and
deletes what does not fit, and whatever the shed holds when the episode ends is never sold.

* Hour 23 before day 29: if the shed after this turn's unit actions and the policy's own sales, plus
  every pocket after those actions, exceeds the capacity, sell shed stock so the sweep fits. Pockets
  cannot be sold, so when they alone exceed the capacity the shed is emptied and the sweep fills it
  to the cap. Tomorrow's feed (a wheat a head, counting the wheat the units carry) is kept, and the
  product priced highest against its base is sold first.
* Steps 717 and 718 (day 29 hours 21 and 22, the last two turns an agent acts on): sell the whole
  shed after this turn's unit actions; on 718 every unit at a shed door holding goods DROPs first,
  and orders that spend money are removed because nothing bought then can be used.

The engine resolves unit actions before the market inside a step, so a DROP and a SELL of the same
goods fit in one turn; quantities are sized from the shed after this turn's unit actions.
"""

from __future__ import annotations

import math
from copy import deepcopy
from typing import Any

SHED_CAPACITY = 100
MARKET_SLOTS = 10
TURNS_PER_DAY = 24
LAST_DAY = 29
OVERNIGHT_HOUR = 23
DELIVER_STEP = 717
FINAL_STEP = 718
FEED_DAYS = 1
PRICE_FLOOR = 1
HINGE_GAIN = 8.0
MARKET_I0 = 10_000
ANIMALS = ("GOOSE", "COW", "SHEEP")
ANIMAL_STRUCTURE = {"GOOSE": "COOP", "COW": "PASTURE", "SHEEP": "PASTURE"}
SPENDING_ORDERS = frozenset({"BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "HIRE", "BUY_LAND"})
# The engine's market curves (kaggriculture 1.32.7+); the market in an observation carries no params.
MARKET_PARAMS = {
    "WHEAT": {"base": 25, "T": 400, "below_func": "sqrt", "below_target": 0.80, "above_func": "log", "above_target": 0.20},
    "CARROT": {"base": 35, "T": 450, "below_func": "hinge", "below_target": 1.00, "above_func": "sqrt", "above_target": 0.70},
    "TOMATO": {"base": 60, "T": 200, "below_func": "hinge", "below_target": 0.40, "above_func": "sqrt", "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "T": 100, "below_func": "sqrt", "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON": {"base": 250, "T": 300, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.60},
    "EGG": {"base": 50, "T": 332, "below_func": "hinge", "below_target": 0.40, "above_func": "log", "above_target": 0.20},
    "MILK": {"base": 160, "T": 122, "below_func": "sqrt", "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL": {"base": 200, "T": 105, "below_func": "log", "below_target": 0.20, "above_func": "sq", "above_target": 3.20},
    "FERTILIZER": {"base": 100, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}  # fmt: skip
PRODUCTS = tuple(MARKET_PARAMS)


def _shape(func: str, x: float, t: float) -> float:
    x = max(0.0, x)
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "hinge":
        u = x / t
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def market_price(item: str, inventory: int) -> int:
    p = MARKET_PARAMS[item]
    base, t = p["base"], p["T"]
    if inventory < MARKET_I0:
        amp = p["below_target"] * base / _shape(p["below_func"], t, t)
        price = base + amp * _shape(p["below_func"], MARKET_I0 - inventory, t)
    else:
        amp = p["above_target"] * base / _shape(p["above_func"], t, t)
        price = base - amp * _shape(p["above_func"], inventory - MARKET_I0, t)
    return max(PRICE_FLOOR, round(price))


def step_of(observation: dict[str, Any]) -> int:
    if observation.get("step") is not None:
        return int(observation["step"])
    return int(observation.get("day", 0)) * TURNS_PER_DAY + int(observation.get("hour", 0))


def shed_doors(board_size: int) -> set[tuple[int, int]]:
    half = board_size // 2
    return {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def unit_orders(action: dict[str, Any], unit_count: int) -> list[list[Any]]:
    orders = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
    orders.extend([["PASS"]] * (unit_count - len(orders)))
    return [order if isinstance(order, list) and order else ["PASS"] for order in orders[:unit_count]]


def _take(bag: dict[str, int], item: str, wanted: int) -> int:
    taken = min(max(0, wanted), bag.get(item, 0))
    bag[item] = bag.get(item, 0) - taken
    return taken


def project_units(observation: dict[str, Any], orders: list[list[Any]]) -> tuple[dict[str, int], int]:
    """The shed and the total pocket count after this turn's unit actions, in the engine's unit order.

    Harvest and fertilizer collection add what the tile shows; FEED, FERTILIZE and animal PLACE
    consume from the pocket. Actions whose success depends on state not modelled here are treated
    as succeeding when their precondition is visible, which errs towards more goods and more room.
    """
    player = int(observation["player"])
    farm = observation["farms"][player]
    private = observation.get("private", {})
    tiles = farm.get("tiles", [])
    doors = shed_doors(len(tiles))
    shed = {str(item): int(count) for item, count in (private.get("shed") or {}).items()}
    inventories = [dict(inventory or {}) for inventory in (private.get("inventories") or [])]
    positions = [tuple(farm.get("farmer", (-1, -1))), *(tuple(hand) for hand in farm.get("hands", []))]
    inventories.extend({} for _ in range(len(positions) - len(inventories)))

    for index, order in enumerate(orders[: len(positions)]):
        x, y = positions[index]
        pocket = inventories[index]
        operation = str(order[0])
        tile = tiles[y][x] if 0 <= y < len(tiles) and 0 <= x < len(tiles[y]) else None
        tile = tile if isinstance(tile, dict) else {}
        if operation == "DROP" and (x, y) in doors:
            for item, held in list(pocket.items()):
                moved = min(int(held), max(0, SHED_CAPACITY - sum(shed.values())))
                shed[item] = shed.get(item, 0) + moved
            pocket.clear()
        elif operation == "PICKUP" and (x, y) in doors and len(order) >= 2:
            item = str(order[1])
            moved = _take(shed, item, int(order[2]) if len(order) >= 3 else 1)
            pocket[item] = pocket.get(item, 0) + moved
        elif operation == "PLACE" and len(order) >= 2:
            item = str(order[1])
            if item in ANIMALS and tile.get("kind") == ANIMAL_STRUCTURE[item] and "animal" not in tile:
                _take(pocket, item, 1)
            elif (x, y) in doors:
                room = max(0, SHED_CAPACITY - sum(shed.values()))
                moved = _take(pocket, item, min(room, int(order[2]) if len(order) >= 3 else 1))
                shed[item] = shed.get(item, 0) + moved
        elif operation == "HARVEST":
            produced = int(tile.get("yield_units", 0) or 0)
            product = tile.get("crop") or {"GOOSE": "EGG", "COW": "MILK", "SHEEP": "WOOL"}.get(tile.get("animal"))
            if product and produced > 0:
                pocket[product] = pocket.get(product, 0) + produced
        elif operation == "COLLECT_FERTILIZER" and tile.get("fertilizer_available"):
            pocket["FERTILIZER"] = pocket.get("FERTILIZER", 0) + 1
        elif operation == "FEED" and tile.get("animal"):
            _take(pocket, "WHEAT", 1)
        elif operation == "FERTILIZE" and tile.get("kind") == "PLANT":
            _take(pocket, "FERTILIZER", 1)
    pockets: dict[str, int] = {}
    for pocket in inventories:
        for item, count in pocket.items():
            pockets[item] = pockets.get(item, 0) + max(0, int(count))
    return shed, pockets


def policy_sales(market: list[list[Any]]) -> dict[str, int]:
    sold: dict[str, int] = {}
    for order in market[:MARKET_SLOTS]:
        if isinstance(order, list) and len(order) >= 3 and order[0] == "SELL":
            sold[str(order[1])] = sold.get(str(order[1]), 0) + max(0, int(order[2]))
    return sold


def add_sales(market: list[list[Any]], extra: dict[str, int], priority: list[str]) -> list[list[Any]]:
    """Raise an existing SELL of the same item, otherwise take a free slot, in `priority` order."""
    market = [list(order) for order in market]
    for item in priority:
        quantity = extra.get(item, 0)
        if quantity <= 0:
            continue
        existing = next(
            (order for order in market[:MARKET_SLOTS] if len(order) >= 3 and order[0] == "SELL" and order[1] == item),
            None,
        )
        if existing is not None:
            existing[2] = int(existing[2]) + quantity
        elif len(market) < MARKET_SLOTS:
            market.append(["SELL", item, quantity])
    return market


def animal_count(farm: dict[str, Any]) -> int:
    return sum(1 for row in farm.get("tiles", []) for cell in row if isinstance(cell, dict) and cell.get("animal"))


def overnight_sales(
    observation: dict[str, Any], stock: dict[str, int], excess: int, pocket_wheat: int
) -> dict[str, int]:
    """Up to `excess` units, one at a time from the product priced highest against its base.

    Each unit sold saves a pocket unit the sweep would delete, so a sale gains unless the product
    sold would have fetched more than the saved unit's worth on top of today's price later; the
    least depressed product is the one least likely to recover, so it goes first. Tomorrow's feed
    (a wheat a head) is kept, counting the wheat the units carry in.
    """
    inventory = {item: int(observation["market"]["inventory"][item]) for item in PRODUCTS}
    held = {item: stock.get(item, 0) for item in PRODUCTS}
    farm = observation["farms"][int(observation["player"])]
    held["WHEAT"] = max(0, held["WHEAT"] - max(0, FEED_DAYS * animal_count(farm) - pocket_wheat))
    sales = {item: 0 for item in PRODUCTS}
    for _ in range(excess):
        candidates = []
        for item in PRODUCTS:
            if held[item] - sales[item] <= 0:
                continue
            price = market_price(item, inventory[item] + sales[item])
            candidates.append((-price / MARKET_PARAMS[item]["base"], -price, item))
        if not candidates:
            break
        sales[min(candidates)[2]] += 1
    return sales


def sale_priority(observation: dict[str, Any], extra: dict[str, int]) -> list[str]:
    prices = observation["market"].get("prices") or {}
    return sorted(extra, key=lambda item: -float(prices.get(item, 0) or 0) * extra[item])


def patch_action(
    observation: dict[str, Any], action: dict[str, Any], night: bool = True, final: bool = True
) -> dict[str, Any]:
    """`night` switches the hour-23 room sale, `final` the sell-out on steps 717 and 718."""
    step = step_of(observation)
    day, hour = divmod(step, TURNS_PER_DAY)
    overnight = night and hour == OVERNIGHT_HOUR and day < LAST_DAY
    if not (overnight or (final and step in (DELIVER_STEP, FINAL_STEP))):
        return action

    player = int(observation["player"])
    farm = observation["farms"][player]
    unit_count = 1 + len(farm.get("hands", []))
    orders = unit_orders(action, unit_count)
    market = [list(order) for order in (action.get("market") or []) if isinstance(order, list) and order]

    if step == FINAL_STEP:
        doors = shed_doors(len(farm.get("tiles", [])))
        positions = [tuple(farm.get("farmer", (-1, -1))), *(tuple(hand) for hand in farm.get("hands", []))]
        inventories = observation.get("private", {}).get("inventories") or []
        for index, position in enumerate(positions):
            carrying = index < len(inventories) and sum((inventories[index] or {}).values()) > 0
            if position in doors and carrying:
                orders[index] = ["DROP"]
    if step in (DELIVER_STEP, FINAL_STEP):
        market = [order for order in market if order[0] not in SPENDING_ORDERS]

    shed, pockets = project_units(observation, orders)
    sold = policy_sales(market)
    stock = {item: max(0, shed.get(item, 0) - sold.get(item, 0)) for item in PRODUCTS}

    if overnight:
        carried = sum(pockets.values())
        excess = sum(max(0, count) for count in shed.values()) - sum(sold.values()) + carried - SHED_CAPACITY
        if excess <= 0:
            return action
        extra = overnight_sales(observation, stock, excess, pockets.get("WHEAT", 0))
    else:
        extra = stock
    extra = {item: quantity for item, quantity in extra.items() if quantity > 0}
    if not extra and step not in (DELIVER_STEP, FINAL_STEP):
        return action
    market = add_sales(market, extra, sale_priority(observation, extra))
    return {"farmer": orders[0], "hands": orders[1:], "market": market}


def patched(policy: Any, observation: dict[str, Any], decide: Any = None) -> dict[str, Any]:
    """Run the policy, patch its action, and record the patched action as the one taken.

    `decide(policy, observation)` replaces the policy's own call when given (unit_rules.decide
    decodes the unit actions with the fertilizer mask and the same-tile duplicate rule).
    The opponent-inventory tracker separates its own market flow from the opponent's using the
    previous action; leaving the unpatched action there would book the patch's sales to the opponent.
    """
    action = decide(policy, observation) if decide is not None else policy(observation)
    action = patch_action(observation, action)
    if hasattr(policy, "previous_action"):
        policy.previous_action = deepcopy(action)
    return action
