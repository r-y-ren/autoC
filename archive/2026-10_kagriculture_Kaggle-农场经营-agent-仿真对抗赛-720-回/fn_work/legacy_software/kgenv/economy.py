"""Quantified economy models for Kaggriculture.

All constants and the price function are taken from the OFFICIAL engine
(kaggle_environments.envs.kaggriculture.kaggriculture, PyPI 1.32.7), which
itself matches the How-to-Play page captured 2026-08-28. Nothing here is
invented; every number traces to the engine source or the official tables.

Key engine facts this module quantifies (source: kaggriculture.py):
  * one-time crops: yield_units starts at 1; each WATER on a day whose age is
    inside [ceil(max_yield_day/2), max_yield_day] adds +1 (+2 if fertilized),
    capped at max_yield
  * ongoing crops: +1 (+2 if fertilized AND watered) per scheduled production,
    capped at max_yield productions, then the plant decays to a weed
  * animals: +1 per scheduled production (+ banked care bonus, +1 per
    fed-and-cared day), capped by max_held *unharvested* units
  * sell price moves per unit sold: price(inv) = base +- amp * f(|inv - I0|)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

# The official engine module is the single source of truth for constants.
from kaggle_environments.envs.kaggriculture.kaggriculture import (
    ANIMALS,
    CROPS,
    MARKET_I0,
    MARKET_PARAMS,
    PRODUCTS,
    market_price,
)

PRICE_FLOOR = 1
SEASON_DAYS = 30  # 720 turns / 24 turns-per-day (official defaults)

# Resources whose price crashes hard on glut (above_target > 1).  From the
# How-to-Play price table: strawberry, melon, milk, wool.
PREMIUM_PRODUCTS = {"STRAWBERRY", "MELON", "MILK", "WOOL"}

# Resources that absorb gluts well (log/sqrt above-curves): safe to dump.
GLUT_TOLERANT = {"WHEAT", "EGG", "FERTILIZER"}


def price(item: str, inventory: int) -> int:
    """Official sell price of `item` at the given market inventory."""
    return market_price(item, inventory)


def price_after_selling(item: str, units: int, start_inventory: int = MARKET_I0) -> Dict[str, float]:
    """Simulate selling `units` one unit at a time into the market.

    Mirrors the engine's per-unit lockstep commit (each sold unit raises
    inventory by 1 and is re-priced; units sold at the $1 floor do not add
    supply).  Returns total revenue, final price and final inventory.
    """
    inv = start_inventory
    revenue = 0.0
    for _ in range(int(units)):
        p = market_price(item, inv)
        revenue += p
        if p > PRICE_FLOOR:
            inv += 1
    return {
        "revenue": revenue,
        "avg_price": revenue / max(1, int(units)),
        "final_price": market_price(item, inv),
        "final_inventory": inv,
    }


def sell_revenue(item: str, units: int) -> float:
    return price_after_selling(item, units)["revenue"]


@dataclass
class CropCycleModel:
    """Per-tile, per-cycle economics of one crop planted on day 0."""

    crop: str
    fertilized: bool = False
    prices: Optional[Dict[str, int]] = None  # current observable prices; None -> base

    cycle_days: int = 0
    unit_actions: int = 0
    yield_units: int = 0
    seed_cost: int = 0
    revenue_at_base: float = 0.0
    revenue_at_prices: float = 0.0
    profit_at_base: float = 0.0
    per_tile_day_base: float = 0.0
    per_action_base: float = 0.0

    def as_dict(self) -> Dict[str, object]:
        return {
            "crop": self.crop,
            "fertilized": self.fertilized,
            "cycle_days": self.cycle_days,
            "unit_actions": self.unit_actions,
            "yield_units": self.yield_units,
            "seed_cost": self.seed_cost,
            "revenue_at_base": self.revenue_at_base,
            "revenue_at_prices": self.revenue_at_prices,
            "profit_at_base": self.profit_at_base,
            "per_tile_day_base": self.per_tile_day_base,
            "per_action_base": self.per_action_base,
        }


def crop_cycle_model(crop: str, fertilized: bool = False,
                     prices: Optional[Dict[str, int]] = None) -> CropCycleModel:
    """Model one optimal-attendance cycle of `crop` on a single tile.

    Follows the engine's WATER bonus window exactly:
    window_start = (max_yield_day + 1) // 2, ages in [window_start, max_yield_day]
    each watered window-day adds +1 (+2 fertilized), yield capped at max_yield.
    Plants must be watered at least every other day to survive, so survival
    watering on non-window days is counted in unit_actions.
    """
    cd = CROPS[crop]
    max_day = cd["max_yield_day"]
    window_start = (max_day + 1) // 2

    if not cd["ongoing"]:
        yield_units = 1
        for age in range(window_start, max_day + 1):
            if yield_units >= cd["max_yield"]:
                break
            yield_units = min(cd["max_yield"], yield_units + (2 if fertilized else 1))
        cycle_days = max_day + 1  # plant day 0, harvest on day max_day
        # waters: survival (every other day before window) + every window day
        # until cap; +1 PLANT +1 HARVEST
        water_days = 0
        y = 1
        for age in range(0, max_day + 1):
            in_window = window_start <= age <= max_day
            if in_window and y < cd["max_yield"]:
                y = min(cd["max_yield"], y + (2 if fertilized else 1))
                water_days += 1
            elif age % 2 == 1:  # minimal survival watering on off-window days
                water_days += 1
        unit_actions = water_days + 2
    else:
        # ongoing: productions at first_yield_day + k*interval, k = 0..max-1
        n_prod = cd["max_yield"]
        per_prod = 2 if fertilized else 1
        yield_units = n_prod * per_prod
        last_day = cd["first_yield_day"] + (n_prod - 1) * cd["interval"]
        cycle_days = last_day + 2  # harvest the morning after the last production
        water_days = cycle_days  # water every day (fertilizer bonus needs it)
        unit_actions = water_days + 1  # single harvest sweep at the end

    m = CropCycleModel(crop=crop, fertilized=fertilized, prices=prices)
    m.cycle_days = cycle_days
    m.unit_actions = unit_actions
    m.yield_units = yield_units
    m.seed_cost = cd["seed"]
    base_price = MARKET_PARAMS[crop]["base"]
    m.revenue_at_base = yield_units * base_price
    px = (prices or {}).get(crop, base_price)
    m.revenue_at_prices = yield_units * px
    m.profit_at_base = m.revenue_at_base - m.seed_cost
    m.per_tile_day_base = m.profit_at_base / max(1, cycle_days)
    m.per_action_base = m.profit_at_base / max(1, unit_actions)
    return m


@dataclass
class AnimalModel:
    animal: str
    cared: bool = False
    feed_cost_per_day: int = 0  # cost of the wheat fed daily (seed-cost basis)

    cost: int = 0
    product: str = ""
    product_base: int = 0
    units_per_production: int = 1
    productions_per_day: float = 0.0
    gross_per_day: float = 0.0
    net_per_day: float = 0.0
    fertilizer_per_day: int = 1
    fertilizer_value_per_day: float = 0.0
    payback_days: float = 0.0
    first_yield_day: int = 0


def animal_model(animal: str, cared: bool = False,
                 wheat_unit_cost: Optional[int] = None,
                 fertilizer_price: Optional[int] = None) -> AnimalModel:
    """Daily steady-state economics of one animal, post first_yield_day.

    CARE banks +1 unit per fed-and-cared day, paid on the next production;
    with interval=1 (goose) that converts to +1 unit every day, i.e. doubles
    output.  Every surviving animal yields 1 collectable fertilizer per day.
    """
    a = ANIMALS[animal]
    if wheat_unit_cost is None:
        wheat_unit_cost = CROPS["WHEAT"]["seed"]  # grow-your-own feed basis
    if fertilizer_price is None:
        fertilizer_price = MARKET_PARAMS["FERTILIZER"]["base"]

    prod_base = MARKET_PARAMS[a["product"]]["base"]
    bonus = 1 if cared else 0
    m = AnimalModel(animal=animal, cared=cared, feed_cost_per_day=wheat_unit_cost)
    m.cost = a["cost"]
    m.product = a["product"]
    m.product_base = prod_base
    m.units_per_production = 1 + bonus
    m.productions_per_day = 1.0 / a["interval"]
    m.gross_per_day = m.units_per_production * m.productions_per_day * prod_base
    # feed is exactly 1 wheat per day (engine FEED takes 1 wheat, once per day)
    m.net_per_day = m.gross_per_day - wheat_unit_cost
    m.fertilizer_per_day = 1
    m.fertilizer_value_per_day = fertilizer_price
    m.payback_days = a["cost"] / max(0.01, m.net_per_day + m.fertilizer_value_per_day)
    m.first_yield_day = a["first_yield_day"]
    return m


def latest_planting_day(crop: str, season_days: int = SEASON_DAYS) -> int:
    """Last day a crop can be planted and still reach its full window.

    One-time crops are harvested on planted_day + max_yield_day, which must
    be <= season_days - 1.  Ongoing crops finish their last production on
    planted_day + first_yield + (max-1)*interval and are harvested the next
    day, so the same bound applies to last_day + 1.
    """
    cd = CROPS[crop]
    if not cd["ongoing"]:
        last_harvest_day = cd["max_yield_day"]
    else:
        last_harvest_day = cd["first_yield_day"] + (cd["max_yield"] - 1) * cd["interval"] + 1
    return max(0, season_days - 1 - last_harvest_day)


def last_production_day(planted_day: int, crop: str) -> int:
    cd = CROPS[crop]
    if not cd["ongoing"]:
        return planted_day + cd["max_yield_day"]
    return planted_day + cd["first_yield_day"] + (cd["max_yield"] - 1) * cd["interval"]


def glut_sensitivity_report(units: int = 60) -> List[Dict[str, object]]:
    """How far each product's price falls after selling `units` from I0.

    Useful for the premium-goods sell-timing policy; numbers come from the
    official price curve via price_after_selling.
    """
    rows = []
    for item in PRODUCTS:
        r = price_after_selling(item, units)
        base = MARKET_PARAMS[item]["base"]
        rows.append({
            "item": item,
            "base": base,
            "units_sold": units,
            "avg_price": round(r["avg_price"], 2),
            "final_price": r["final_price"],
            "retention": round(r["final_price"] / base, 3),
        })
    rows.sort(key=lambda x: x["retention"])
    return rows


def hire_costs(n_hires: int) -> List[int]:
    """Per-hire costs for hires 1..n on one day (fibonacci, resets daily)."""
    costs, a, b = [], 1, 1
    for _ in range(n_hires):
        costs.append(a)
        a, b = b, a + b
    return costs


LAND_PRICES = [1000, 2000, 4000]  # NE, SW, SE (official LAND_PRICES)


def land_cost(quadrants_owned: int) -> Optional[int]:
    """Cost of the next land purchase (quadrants_owned counts NW + bought)."""
    extra = quadrants_owned - 1
    if 0 <= extra < len(LAND_PRICES):
        return LAND_PRICES[extra]
    return None
