"""Static game constants, transcribed from kaggriculture.py (sha256 bc8a548...).

Everything here is an array or plain scalar so both the numpy submission and the
JAX simulator can consume it without a translation layer.
"""

from __future__ import annotations

import math

import numpy as np

# ---------------------------------------------------------------- item indexing

# Items that can sit in a shed or a unit inventory.
ITEMS = [
    "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
    "EGG", "MILK", "WOOL", "FERTILIZER",
    "GOOSE", "COW", "SHEEP",
]
N_ITEMS = len(ITEMS)
ITEM_IX = {name: i for i, name in enumerate(ITEMS)}

# Market products are exactly ITEMS[:9] and in the engine's PRODUCTS order.
PRODUCTS = ITEMS[:9]
N_PRODUCTS = len(PRODUCTS)

I_WHEAT, I_CARROT, I_TOMATO, I_STRAWBERRY, I_MELON = 0, 1, 2, 3, 4
I_EGG, I_MILK, I_WOOL, I_FERT = 5, 6, 7, 8
I_GOOSE, I_COW, I_SHEEP = 9, 10, 11

# Plantable crops, in engine CROPS order; crop index c -> item index c.
CROPS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"]
N_CROPS = len(CROPS)

ANIMALS = ["GOOSE", "COW", "SHEEP"]
N_ANIMALS = len(ANIMALS)

# ---------------------------------------------------------------- crop table

#                     seed  first  maxday  interval  maxyield  ongoing
_CROP_ROWS = [
    ("WHEAT",           10,     2,      4,        0,        6,      0),
    ("CARROT",          20,     2,      3,        0,        4,      0),
    ("TOMATO",          50,     8,      8,        1,        4,      1),
    ("STRAWBERRY",     100,    10,     10,        2,        4,      1),
    ("MELON",           80,    10,     12,        0,        6,      0),
]
CROP_SEED_COST = np.array([r[1] for r in _CROP_ROWS], dtype=np.int32)
CROP_FIRST_YIELD_DAY = np.array([r[2] for r in _CROP_ROWS], dtype=np.int32)
CROP_MAX_YIELD_DAY = np.array([r[3] for r in _CROP_ROWS], dtype=np.int32)
CROP_INTERVAL = np.array([r[4] for r in _CROP_ROWS], dtype=np.int32)
CROP_MAX_YIELD = np.array([r[5] for r in _CROP_ROWS], dtype=np.int32)
CROP_ONGOING = np.array([r[6] for r in _CROP_ROWS], dtype=np.int32)
# Watering bonus window is [ (max_yield_day+1)//2 , max_yield_day ] in age-days.
CROP_WINDOW_START = (CROP_MAX_YIELD_DAY + 1) // 2

# Age at which a one-time crop watered on every in-window day already holds
# CROP_MAX_YIELD, so that waiting longer buys nothing.
#
# `_new_plant` seeds a non-ongoing crop with one unit and WATER adds one more
# per in-window day, so the yield at age `a` is
# `min(mxy, 1 + (a - window_start + 1))`, which reaches `mxy` at
# `window_start + mxy - 2`. HARVEST also needs `age >= first_yield_day`, hence
# the lower clamp; the upper clamp is the age past which the engine stops
# paying for water at all.
#
# Only MELON differs from CROP_MAX_YIELD_DAY (10 vs 12): it saturates two days
# before its window closes, and those two days are the whole melon race -- the
# opponent harvests at age 10 and reaches the fresh curve on day 10 while a
# max-yield-day harvest reaches it on day 13 at the same 6 units a tile
# (measured 2026-08-26, 32 games: 6.00 units/tile on both schedules).
CROP_SATURATE_AGE = np.minimum(
    CROP_MAX_YIELD_DAY,
    np.maximum(CROP_FIRST_YIELD_DAY, CROP_WINDOW_START + CROP_MAX_YIELD - 2),
).astype(np.int32)

# ---------------------------------------------------------------- animal table

#                     cost  structure  first  interval  max_held  product
_ANIMAL_ROWS = [
    ("GOOSE",          300,        4,      4,        1,        4,   I_EGG),
    ("COW",            400,        5,      8,        2,        6,   I_MILK),
    ("SHEEP",          500,        5,      6,        3,        6,   I_WOOL),
]
ANIMAL_COST = np.array([r[1] for r in _ANIMAL_ROWS], dtype=np.int32)
ANIMAL_STRUCT = np.array([r[2] for r in _ANIMAL_ROWS], dtype=np.int32)  # KIND_COOP / KIND_PASTURE
ANIMAL_FIRST_YIELD_DAY = np.array([r[3] for r in _ANIMAL_ROWS], dtype=np.int32)
ANIMAL_INTERVAL = np.array([r[4] for r in _ANIMAL_ROWS], dtype=np.int32)
ANIMAL_MAX_HELD = np.array([r[5] for r in _ANIMAL_ROWS], dtype=np.int32)
ANIMAL_PRODUCT = np.array([r[6] for r in _ANIMAL_ROWS], dtype=np.int32)

# ---------------------------------------------------------------- tile kinds

KIND_EMPTY = 0
KIND_LOCKED = 1
KIND_WEED = 2
KIND_PLANT = 3
KIND_COOP = 4
KIND_PASTURE = 5

# ---------------------------------------------------------------- market params

MARKET_I0 = 10000
PRICE_FLOOR = 1
HINGE_GAIN = 8.0

_SHAPES = ["linear", "sq", "sqrt", "log", "log10", "hinge"]

#                    base    T   below_func below_target above_func above_target
_MARKET_ROWS = [
    ("WHEAT",         25,  400,  "sqrt",  0.80, "log",    0.20),
    ("CARROT",        35,  450,  "hinge", 1.00, "sqrt",   0.70),
    ("TOMATO",        60,  200,  "hinge", 0.40, "sqrt",   0.60),
    ("STRAWBERRY",   120,  100,  "sqrt",  0.70, "linear", 1.60),
    ("MELON",        250,  300,  "log",   0.20, "sq",     3.60),
    ("EGG",           50,  332,  "hinge", 0.40, "log",    0.20),
    ("MILK",         160,  122,  "sqrt",  0.60, "linear", 1.60),
    ("WOOL",         200,  105,  "log",   0.20, "sq",     3.20),
    ("FERTILIZER",   100,  200,  "linear",0.40, "linear", 0.40),
]

DEFAULT_MARKET_PARAMS = {
    row[0]: {
        "base": row[1], "I0": MARKET_I0, "T": row[2],
        "below_func": row[3], "below_target": row[4],
        "above_func": row[5], "above_target": row[6],
    }
    for row in _MARKET_ROWS
}


def shape(func: str, x: float, T: float | None = None) -> float:
    """Exact transcription of kaggriculture._shape (float64, as CPython runs it)."""
    x = max(0.0, x)
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return math.sqrt(x)
    if func == "log":
        return math.log(1.0 + x)
    if func == "log10":
        return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


def market_price(item: str, inventory: int, params: dict | None = None) -> int:
    """Exact transcription of kaggriculture.market_price."""
    p = (params or DEFAULT_MARKET_PARAMS)[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / shape(f, T, T)
        price = base + amp * shape(f, I0 - inventory, T)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / shape(f, T, T)
        price = base - amp * shape(f, inventory - I0, T)
    # `int(round(...))` is redundant in Python 3, but this line is a character-for
    # -character transcription of the engine's, and keeping it that way is what
    # makes the port auditable against kaggriculture.py.
    return max(PRICE_FLOOR, int(round(price)))  # noqa: RUF046


# ---------------------------------------------------------------- shops

SHOP_NAMES = sorted([
    "BAKERY", "PIZZA_SHOP", "BRUNCH_SPOT", "YARN_STORE",
    "ICE_CREAM_SHOP", "PET_CAFE", "SMOOTHIE_SHOP", "FARMERS_MARKET",
])
N_SHOPS = len(SHOP_NAMES)
MAX_SHOP_INSTANCES = 8

_SHOP_DEMAND = {
    "BAKERY": ["EGG", "WHEAT"],
    "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}

# SHOP_CONSUME[shop, product] = units removed per shop tick by one instance.
# Single-product shops consume double.
SHOP_CONSUME = np.zeros((N_SHOPS, N_PRODUCTS), dtype=np.int32)
for _si, _name in enumerate(SHOP_NAMES):
    _prods = _SHOP_DEMAND[_name]
    _mult = 2 if len(_prods) == 1 else 1
    for _p in _prods:
        SHOP_CONSUME[_si, ITEM_IX[_p]] = _mult

# Town center consumes one of every product except fertilizer, once per
# townCenterSellInterval turns.
TOWN_CENTER_CONSUME = np.ones(N_PRODUCTS, dtype=np.int32)
TOWN_CENTER_CONSUME[I_FERT] = 0

# ---------------------------------------------------------------- board / misc

BOARD = 10
N_TILES = BOARD * BOARD
HALF = BOARD // 2
STARTING_MONEY = 3000
TURNS_PER_DAY = 24
N_DAYS = 30
EPISODE_STEPS = TURNS_PER_DAY * N_DAYS
SHED_CAPACITY = 100
MAX_MARKET_ORDERS = 10

#: The planner's coin ceiling: every value estimate in coins is clipped to
#: `[0, COIN_CAP - 1]` before it enters ratio, packing or sentinel arithmetic
#: (PLANNER_V3_1 section 2, "< 2**20"). One constant so the reservation decode,
#: the budget's value cap, the task-value clip and `sell.LIQUIDATE` cannot drift
#: apart -- `LIQUIDATE = -COIN_CAP` is then below every decodable reservation by
#: construction (see `core/sell.py`).
COIN_CAP = 1 << 20
WEED_SPAWN_CHANCE = 0.005
SHOP_UNLOCK_INTERVAL = 3
SHOP_SELL_INTERVAL = 4
TOWN_CENTER_SELL_INTERVAL = 24

LAND_PRICES = np.array([1000, 2000, 4000], dtype=np.int32)
# Quadrant ids: 0=NW 1=NE 2=SW 3=SE.  LAND_ORDER is NE, SW, SE.
LAND_ORDER = np.array([1, 2, 3], dtype=np.int32)

# The engine caps nothing: `_do_hire` charges `_fib(hires_today)`, appends a
# hand and returns, and `hires_today` resets nightly. The only limit is the
# 10-order market queue *per turn* (`maxMarketOrdersPerTurn`), so the ceiling is
# a planner choice about how many turns of that queue a day is willing to spend
# on HIRE -- `core/ops.py` spends two of them (turn 0 and turn 2), which is 20
# slots. 16 is where the fib bill stops being a rounding error: 143 coins buys
# ten hands, 376 twelve, 986 fourteen and 2,583 sixteen, against a season the
# immutable kagg2 opponent grosses six figures on twelve. Past sixteen the bill
# doubles every two hands (4,180 for eighteen) and eats the starting purse.
MAX_HANDS = 16
MAX_UNITS = MAX_HANDS + 1

FARM_HAND_COST_MULT = 1


def _fib(n: int) -> int:
    """_fib(0)=1, _fib(1)=1, _fib(2)=2, ..."""
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


# HIRE_COST[n] = cost of the (n+1)-th hire of the day.
HIRE_COST = np.array([_fib(n) for n in range(MAX_HANDS + 1)], dtype=np.int32)

# ---------------------------------------------------------------- tile geometry

_ys, _xs = np.divmod(np.arange(N_TILES), BOARD)
TILE_X = _xs.astype(np.int32)
TILE_Y = _ys.astype(np.int32)
# quadrant of each tile: 0=NW 1=NE 2=SW 3=SE
TILE_QUAD = ((TILE_Y >= HALF).astype(np.int32) * 2 + (TILE_X >= HALF).astype(np.int32))

# Shed-access tiles in the engine's NWSE order: (half-1,half-1), (half,half-1),
# (half-1,half), (half,half)  as (x, y).
SHED_ACCESS_XY = np.array(
    [(HALF - 1, HALF - 1), (HALF, HALF - 1), (HALF - 1, HALF), (HALF, HALF)],
    dtype=np.int32,
)
SHED_ACCESS_TILE = SHED_ACCESS_XY[:, 1] * BOARD + SHED_ACCESS_XY[:, 0]
# Main farmer spawns on the first shed-access tile inside NW.
DEFAULT_SPAWN_TILE = int(SHED_ACCESS_TILE[0])
IS_SHED_ADJACENT = np.zeros(N_TILES, dtype=bool)
IS_SHED_ADJACENT[SHED_ACCESS_TILE] = True


# ---------------------------------------------------------------- price tables

# Inventory offsets we tabulate, relative to I0. Town drain over a season is at
# most ~3k; player sells can add tens of thousands.
# Reachable inventory band. Town drain over a season is at most ~3k below I0;
# two players selling everything they can grow tops out near I0 + 36k.
PRICE_TABLE_LO = -5000
PRICE_TABLE_HI = 80000
PRICE_TABLE_N = PRICE_TABLE_HI - PRICE_TABLE_LO + 1


def _shape_vec(func: str, x: np.ndarray, T: float | None = None) -> np.ndarray:
    """Vectorised `shape`, float64. Must agree with `shape` bit for bit."""
    x = np.maximum(0.0, x.astype(np.float64))
    if func == "linear":
        return x
    if func == "sq":
        return x * x
    if func == "sqrt":
        return np.sqrt(x)
    if func == "log":
        return np.log(1.0 + x)
    if func == "log10":
        return np.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / float(T)
        return u + HINGE_GAIN * np.maximum(0.0, u - 1.0) ** 2
    return x


def build_price_table(params: dict | None = None) -> np.ndarray:
    """int32 [N_PRODUCTS, PRICE_TABLE_N]: market_price at each absolute inventory.

    Computed in float64 on the host so `int(round(...))` matches CPython, then
    every entry whose float lands suspiciously close to a .5 tie is recomputed
    through the scalar `math`-based path. The device only ever gathers from this
    table, so no on-device float can perturb a price.
    """
    params = params or DEFAULT_MARKET_PARAMS
    invs = np.arange(PRICE_TABLE_LO, PRICE_TABLE_HI + 1, dtype=np.int64)
    out = np.empty((N_PRODUCTS, PRICE_TABLE_N), dtype=np.int32)
    for pi, name in enumerate(PRODUCTS):
        p = params[name]
        base, I0, T = float(p["base"]), int(p["I0"]), float(p["T"])
        amp_below = p["below_target"] * base / shape(p["below_func"], T, T)
        amp_above = p["above_target"] * base / shape(p["above_func"], T, T)
        below = invs < I0
        price = np.where(
            below,
            base + amp_below * _shape_vec(p["below_func"], np.where(below, I0 - invs, 0), T),
            base - amp_above * _shape_vec(p["above_func"], np.where(below, 0, invs - I0), T),
        )
        col = np.maximum(PRICE_FLOOR, np.rint(price).astype(np.int64))

        # Recompute anything within 1e-6 of a rounding tie through the scalar path.
        frac = np.abs(price - np.floor(price) - 0.5)
        for k in np.flatnonzero(frac < 1e-6):
            col[k] = market_price(name, int(invs[k]), params)
        out[pi] = col.astype(np.int32)
    return out


def price_index(inventory):
    """Absolute market inventory -> index into a price table row."""
    return inventory - PRICE_TABLE_LO


# ---------------------------------------------------------------- randomisation

_SHAPE_POOL = ["linear", "sq", "sqrt", "log", "log10", "hinge"]


def sample_market_params(rng: np.random.Generator, strength: float = 1.0) -> dict:
    """A perturbed market table for domain randomisation.

    GOAL.md wants the policy to *read* the price curve off its inputs rather than
    memorise the default table. Training on a market whose base prices, anchor
    throughputs and curve shapes move between generations is what forces that.

    The agent is **not** told the perturbed values. `marketParams` is not in the
    observation, and the competition runs the defaults, so training a policy that
    conditions on the true parameters would train a capability it cannot use at
    inference. The randomisation is therefore a regulariser: it penalises any
    strategy that leans on exact price levels instead of on the price and
    inventory the market actually reports.

    `strength = 0` returns the defaults unchanged.
    """
    out = {name: dict(p) for name, p in DEFAULT_MARKET_PARAMS.items()}
    if strength <= 0:
        return out
    for p in out.values():
        p["base"] = max(2, round(p["base"] * _jit(rng, 0.75, 1.35, strength)))
        p["T"] = max(20, round(p["T"] * _jit(rng, 0.70, 1.45, strength)))
        p["below_target"] = float(p["below_target"] * _jit(rng, 0.70, 1.45, strength))
        p["above_target"] = float(p["above_target"] * _jit(rng, 0.70, 1.45, strength))
        # Occasionally reshape a side of the curve outright, so the net cannot
        # assume "this product always crashes" or "this one always absorbs".
        if rng.random() < 0.15 * strength:
            p["above_func"] = str(rng.choice(_SHAPE_POOL))
        if rng.random() < 0.15 * strength:
            p["below_func"] = str(rng.choice(_SHAPE_POOL))
    return out


def _jit(rng, lo, hi, strength):
    """Multiplier in [lo, hi], pulled toward 1.0 as strength falls."""
    m = rng.uniform(lo, hi)
    return 1.0 + (m - 1.0) * float(np.clip(strength, 0.0, 1.0))
