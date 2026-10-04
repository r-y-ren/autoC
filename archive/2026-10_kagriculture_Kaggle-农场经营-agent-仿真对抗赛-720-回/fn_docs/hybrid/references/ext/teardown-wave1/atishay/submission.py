"""Kaggriculture competition submission -- a single self-contained file.

This is a generated/assembled artifact mirroring the modular project at
github.com/atishay-kasliwal/kaggriculture (sim/, planner/, my_agents/,
developed and tested across 10 phases there). Assembled into one flat file
on purpose: Kaggle's grading sandbox is a black box that can't be tested
against directly, and a single file with no internal package imports
eliminates an entire class of "worked locally, broke on Kaggle" risk --
there's no way for an import path to be wrong if there's nothing to import.

Renames applied during assembly (each of the five agent modules below
independently defined a function literally called `make_agent`; flattened
into one namespace, only the last definition would survive, silently
breaking the other four):
    single_crop_loop.make_agent    -> make_crop_agent
    quadrant_crop.make_agent       -> make_quadrant_agent
    multi_worker_crop.make_agent   -> make_multi_agent
    animal_loop.make_agent         -> make_animal_agent
    dual_worker_animal.make_agent  -> make_dual_animal_agent
(matching the aliases the original planner/candidates.py and
planner/opponent_model.py already imported them as). `TILE` (single_crop_
loop.py and animal_loop.py both defined the same (4,4) constant) and
PASS_ACTION (sim/value.py and planner/opponent_model.py both defined the
same value) are each defined once here instead of twice.

Entry point: `agent(obs, configuration)` at the bottom, the file's last
top-level def, matching Kaggle's "python file with the last def accepting
an observation and returning an action" requirement.
"""
import copy
import math
import random
from collections import Counter


# ============================================================================
# sim/mechanics.py -- faithful port of the real environment's turn mechanics
# (kaggle_environments/envs/kaggriculture/kaggriculture.py). Validated exactly
# (every turn) against the real engine in the source repo's
# tests/test_sim_matches_env.py.
# ============================================================================

CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}

ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP",    "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}

PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]

MARKET_I0 = 10000
PRICE_FLOOR = 1

MARKET_PARAMS = {
    "WHEAT":      {"base":  25, "I0": MARKET_I0, "T": 400, "below_func": "sqrt",   "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":     {"base":  35, "I0": MARKET_I0, "T": 450, "below_func": "log",    "below_target": 0.20, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":     {"base":  60, "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": MARKET_I0, "T": 100, "below_func": "sqrt",   "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "I0": MARKET_I0, "T": 300, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":        {"base":  50, "I0": MARKET_I0, "T": 332, "below_func": "linear", "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":       {"base": 160, "I0": MARKET_I0, "T": 122, "below_func": "sqrt",   "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "I0": MARKET_I0, "T": 105, "below_func": "log",    "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": MARKET_I0, "T": 200, "below_func": "linear", "below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}

FARMER_MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}

LAND_ORDER = ["NE", "SW", "SE"]
LAND_PRICES = [1000, 2000, 4000]
FARM_HAND_COST_MULT = 1

SHOPS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}

TOWN_CENTER_PRODUCTS = [p for p in PRODUCTS if p != "FERTILIZER"]
TOWN_CENTER_DEMAND_SCHEDULE = [(20, 4), (10, 2), (0, 1)]


def _shape(func, x):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    return x


def _resolve_market_params(overrides):
    resolved = {item: dict(p) for item, p in MARKET_PARAMS.items()}
    if not overrides:
        return resolved
    for item, patch in overrides.items():
        if item in resolved and isinstance(patch, dict):
            resolved[item].update(patch)
    return resolved


def _quadrant_of(x, y, board_size):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _shed_access_tiles(board_size):
    half = board_size // 2
    return [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]


def _is_shed_adjacent(pos, board_size):
    return tuple(pos) in {(x, y) for (x, y) in _shed_access_tiles(board_size)}


def _new_farm(board_size, starting_money):
    return {
        "money": float(starting_money),
        "tiles": [[_initial_tile(x, y, board_size) for x in range(board_size)] for y in range(board_size)],
        "farmer": list(_default_spawn(board_size)),
        "hands": [],
        "unlocked_quadrants": ["NW"],
        "hires_today": 0,
    }


def _initial_tile(x, y, board_size):
    return None if _quadrant_of(x, y, board_size) == "NW" else "LOCKED"


def _default_spawn(board_size):
    for tile in _shed_access_tiles(board_size):
        if _quadrant_of(tile[0], tile[1], board_size) == "NW":
            return tile
    return (0, 0)


def _new_private():
    return {
        "shed": {item: 0 for item in PRODUCTS + list(ANIMALS)},
        "seeds": {crop: 0 for crop in CROPS},
        "inventories": [{}],
    }


def _new_market(params=None):
    params = params or MARKET_PARAMS
    inv = {item: params[item]["I0"] for item in PRODUCTS}
    prices = {item: params[item]["base"] for item in PRODUCTS}
    market = {"inventory": inv, "prices": prices}
    if params is not MARKET_PARAMS:
        market["params"] = params
    return market


def _new_town():
    return {"unlocked_shops": []}


def market_price(item, inventory, params=None):
    p = (params or MARKET_PARAMS)[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        f = p["below_func"]
        amp = p["below_target"] * base / _shape(f, T)
        price = base + amp * _shape(f, I0 - inventory)
    else:
        f = p["above_func"]
        amp = p["above_target"] * base / _shape(f, T)
        price = base - amp * _shape(f, inventory - I0)
    return max(PRICE_FLOOR, int(round(price)))


def _refresh_prices(market):
    params = market.get("params")
    for item in PRODUCTS:
        market["prices"][item] = market_price(item, market["inventory"][item], params)


def _new_plant(crop, day, turns_per_day):
    cd = CROPS[crop]
    return {
        "kind": "PLANT",
        "crop": crop,
        "planted_day": day,
        "watered_today": False,
        "consecutive_unwatered": 1,
        "yield_units": 0 if cd["ongoing"] else 1,
        "max_lifespan_step": (-1 if cd["ongoing"] else (day + cd["max_yield_day"] + 1) * turns_per_day),
        "fertilized_until_day": -1,
    }


def _new_animal(animal, day):
    a = ANIMALS[animal]
    return {
        "kind": a["structure"],
        "animal": animal,
        "placed_day": day,
        "yield_units": 0,
        "consecutive_unfed": 0,
        "fed_today": False,
        "cared_today": False,
        "fertilizer_available": False,
        "pending_care_bonus": 0,
    }


def _farmer_position(farm, idx):
    if idx == 0:
        return farm["farmer"]
    return farm["hands"][idx - 1] if idx - 1 < len(farm["hands"]) else None


def _set_farmer_position(farm, idx, pos):
    if idx == 0:
        farm["farmer"] = list(pos)
    else:
        farm["hands"][idx - 1] = list(pos)


def _farmer_inventory(private, idx):
    while len(private["inventories"]) <= idx:
        private["inventories"].append({})
    return private["inventories"][idx]


def _inv_add(inv, item, n=1):
    inv[item] = inv.get(item, 0) + n


def _inv_take(inv, item, n=1):
    if inv.get(item, 0) < n:
        return False
    inv[item] -= n
    if inv[item] == 0:
        del inv[item]
    return True


def apply_unit_action(farm, private, idx, action, board_size, day, turns_per_day, shed_capacity=100):
    """Process one farmer/hand's action. Invalid / illegal actions are silent no-ops."""
    if not isinstance(action, list) or not action:
        return
    op = action[0]
    pos = _farmer_position(farm, idx)
    if pos is None:
        return
    fx, fy = pos[0], pos[1]
    inv = _farmer_inventory(private, idx)

    if op in FARMER_MOVES:
        dx, dy = FARMER_MOVES[op]
        nx, ny = fx + dx, fy + dy
        if not (0 <= nx < board_size and 0 <= ny < board_size):
            return
        _set_farmer_position(farm, idx, (nx, ny))
        return

    if op == "PASS":
        return

    tile = farm["tiles"][fy][fx]

    if op == "DROP":
        if not _is_shed_adjacent((fx, fy), board_size):
            return
        shed = private["shed"]
        for item, n in list(inv.items()):
            if n <= 0:
                del inv[item]
                continue
            room = max(0, shed_capacity - sum(shed.values()))
            take = min(n, room)
            if take > 0:
                shed[item] = shed.get(item, 0) + take
            del inv[item]
        return

    if op == "PICKUP":
        if not _is_shed_adjacent((fx, fy), board_size):
            return
        if len(action) < 2:
            return
        item = action[1]
        n = int(action[2]) if len(action) >= 3 else 1
        if n <= 0:
            return
        available = private["shed"].get(item, 0)
        n = min(n, available)
        if n <= 0:
            return
        private["shed"][item] -= n
        _inv_add(inv, item, n)
        return

    if op == "PLACE":
        if len(action) < 2:
            return
        item = action[1]
        if (
            item in ANIMALS
            and isinstance(tile, dict)
            and tile.get("kind") == ANIMALS[item]["structure"]
            and "animal" not in tile
        ):
            if _inv_take(inv, item, 1):
                farm["tiles"][fy][fx] = _new_animal(item, day)
            return
        if _is_shed_adjacent((fx, fy), board_size):
            n = int(action[2]) if len(action) >= 3 else 1
            if n <= 0:
                return
            n = min(n, inv.get(item, 0))
            if n <= 0:
                return
            current = sum(private["shed"].values())
            room = max(0, shed_capacity - current)
            n = min(n, room)
            if n <= 0:
                return
            inv[item] -= n
            if inv[item] == 0:
                del inv[item]
            private["shed"][item] = private["shed"].get(item, 0) + n
        return

    if tile == "LOCKED":
        return

    if op == "PLANT":
        if len(action) < 2:
            return
        crop = action[1]
        if crop not in CROPS:
            return
        if tile is not None:
            return
        if private["seeds"].get(crop, 0) <= 0:
            return
        private["seeds"][crop] -= 1
        farm["tiles"][fy][fx] = _new_plant(crop, day, turns_per_day)
        return

    if op == "WATER":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            return
        if tile["watered_today"]:
            return
        tile["watered_today"] = True
        crop_data = CROPS[tile["crop"]]
        if not crop_data["ongoing"]:
            age_days = day - tile["planted_day"]
            window_start = (crop_data["max_yield_day"] + 1) // 2
            if window_start <= age_days <= crop_data["max_yield_day"]:
                bonus = 2 if tile["fertilized_until_day"] >= day else 1
                tile["yield_units"] = min(crop_data["max_yield"], tile["yield_units"] + bonus)
        return

    if op == "HARVEST":
        if not isinstance(tile, dict):
            return
        if tile.get("yield_units", 0) <= 0:
            return
        if tile.get("kind") == "PLANT":
            crop_data = CROPS[tile["crop"]]
            if day - tile["planted_day"] < crop_data["first_yield_day"]:
                return
            units = tile["yield_units"]
            tile["yield_units"] = 0
            _inv_add(inv, tile["crop"], units)
            if not crop_data["ongoing"]:
                farm["tiles"][fy][fx] = None
        elif "animal" in tile:
            units = tile["yield_units"]
            tile["yield_units"] = 0
            _inv_add(inv, ANIMALS[tile["animal"]]["product"], units)
        return

    if op == "FERTILIZE":
        if not (isinstance(tile, dict) and tile.get("kind") == "PLANT"):
            return
        if not _inv_take(inv, "FERTILIZER", 1):
            return
        tile["fertilized_until_day"] = max(tile.get("fertilized_until_day", -1), day + 2)
        return

    if op == "DIG":
        if tile is None:
            return
        if isinstance(tile, dict) and "animal" in tile:
            return
        farm["tiles"][fy][fx] = None
        return

    if op == "BUILD_COOP":
        if tile is not None:
            return
        farm["tiles"][fy][fx] = {"kind": "COOP"}
        return

    if op == "BUILD_PASTURE":
        if tile is not None:
            return
        farm["tiles"][fy][fx] = {"kind": "PASTURE"}
        return

    if op == "FEED":
        if not (isinstance(tile, dict) and "animal" in tile):
            return
        if tile["fed_today"]:
            return
        if not _inv_take(inv, "WHEAT", 1):
            return
        tile["fed_today"] = True
        return

    if op == "COLLECT_FERTILIZER":
        if not (isinstance(tile, dict) and "animal" in tile):
            return
        if not tile["fertilizer_available"]:
            return
        tile["fertilizer_available"] = False
        _inv_add(inv, "FERTILIZER", 1)
        return

    if op == "CARE":
        if not (isinstance(tile, dict) and "animal" in tile):
            return
        if tile["cared_today"]:
            return
        tile["cared_today"] = True
        return


def _spawn_hand(farm, board_size):
    occupants = {tile: 0 for tile in _shed_access_tiles(board_size)}
    all_pos = [tuple(farm["farmer"])] + [tuple(p) for p in farm["hands"]]
    for pos in all_pos:
        if pos in occupants:
            occupants[pos] += 1
    best = sorted(occupants.items(), key=lambda kv: (kv[1], _shed_access_tiles(board_size).index(kv[0])))
    return list(best[0][0])


def _parse_order(order):
    if not isinstance(order, list) or not order:
        return None
    op = order[0]
    if op == "HIRE":
        return {"type": "HIRE"}
    if op == "BUY_LAND":
        return {"type": "BUY_LAND"}
    if op in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"):
        if len(order) < 3:
            return None
        try:
            n = int(order[2])
        except (TypeError, ValueError):
            return None
        if n <= 0:
            return None
        return {"type": op, "item": order[1], "remaining": n}
    return None


def _commit_unit(op, item, price, farm, private, market, shed_capacity=100):
    if op == "SELL":
        if private["shed"].get(item, 0) <= 0:
            return False
        private["shed"][item] -= 1
        farm["money"] += price
        if price > 1:
            market["inventory"][item] += 1
        return True
    if op == "BUY_PRODUCT":
        if farm["money"] < price:
            return False
        if sum(private["shed"].values()) >= shed_capacity:
            return False
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        market["inventory"][item] -= 1
        return True
    if op == "BUY_SEED":
        if farm["money"] < price:
            return False
        farm["money"] -= price
        private["seeds"][item] = private["seeds"].get(item, 0) + 1
        return True
    if op == "BUY_ANIMAL":
        if farm["money"] < price:
            return False
        if sum(private["shed"].values()) >= shed_capacity:
            return False
        farm["money"] -= price
        private["shed"][item] = private["shed"].get(item, 0) + 1
        return True
    return False


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


def _hire_cost(n_already_today, mult=FARM_HAND_COST_MULT):
    return mult * _fib(n_already_today)


def do_hire(farm, private, board_size, mult=FARM_HAND_COST_MULT):
    cost = _hire_cost(farm["hires_today"], mult)
    if farm["money"] < cost:
        return
    farm["money"] -= cost
    farm["hires_today"] += 1
    farm["hands"].append(_spawn_hand(farm, board_size))
    private["inventories"].append({})


def do_buy_land(farm, board_size):
    n_unlocked_extra = len(farm["unlocked_quadrants"]) - 1
    if n_unlocked_extra >= len(LAND_ORDER):
        return
    cost = LAND_PRICES[n_unlocked_extra]
    if farm["money"] < cost:
        return
    farm["money"] -= cost
    quadrant = LAND_ORDER[n_unlocked_extra]
    farm["unlocked_quadrants"].append(quadrant)
    for y in range(board_size):
        for x in range(board_size):
            if _quadrant_of(x, y, board_size) == quadrant and farm["tiles"][y][x] == "LOCKED":
                farm["tiles"][y][x] = None


def decay_plants(farm, step_num):
    board_size = len(farm["tiles"])
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            mls = tile["max_lifespan_step"]
            if mls < 0 or step_num < mls:
                continue
            if (step_num - mls) % 2 != 0:
                continue
            tile["yield_units"] -= 1
            if tile["yield_units"] <= 0:
                farm["tiles"][y][x] = {"kind": "WEED"}


def daily_refresh_plants(farm, current_day, turns_per_day):
    board_size = len(farm["tiles"])
    next_day = current_day + 1
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            was_watered = tile["watered_today"]
            if was_watered:
                tile["consecutive_unwatered"] = 0
            else:
                tile["consecutive_unwatered"] += 1
            tile["watered_today"] = False
            if tile["consecutive_unwatered"] >= 2:
                farm["tiles"][y][x] = {"kind": "WEED"}
                continue
            cd = CROPS[tile["crop"]]
            if not cd["ongoing"]:
                continue
            days_since_first = next_day - tile["planted_day"] - cd["first_yield_day"]
            if days_since_first < 0:
                continue
            interval = cd["interval"]
            if days_since_first % interval != 0:
                continue
            production_count = days_since_first // interval + 1
            if production_count > cd["max_yield"]:
                continue
            fertilized = was_watered and tile.get("fertilized_until_day", -1) >= current_day
            tile["yield_units"] = min(cd["max_yield"], tile["yield_units"] + (2 if fertilized else 1))
            if production_count == cd["max_yield"]:
                tile["max_lifespan_step"] = (next_day + 1) * turns_per_day


def daily_refresh_animals(farm, day):
    board_size = len(farm["tiles"])
    next_day = day + 1
    for y in range(board_size):
        for x in range(board_size):
            tile = farm["tiles"][y][x]
            if not (isinstance(tile, dict) and "animal" in tile):
                continue
            if tile["fed_today"]:
                tile["consecutive_unfed"] = 0
            else:
                tile["consecutive_unfed"] += 1
            if tile["consecutive_unfed"] >= 2:
                farm["tiles"][y][x] = {"kind": ANIMALS[tile["animal"]]["structure"]}
                continue
            a = ANIMALS[tile["animal"]]
            days_since_first = next_day - tile["placed_day"] - a["first_yield_day"]
            if days_since_first >= 0 and days_since_first % a["interval"] == 0:
                base = 1
                bonus = tile.pop("pending_care_bonus", 0) if tile["fed_today"] else 0
                tile["yield_units"] = min(a["max_held"], tile["yield_units"] + base + bonus)
                tile["pending_care_bonus"] = 0
            if tile["cared_today"] and tile["fed_today"]:
                tile["pending_care_bonus"] = tile.get("pending_care_bonus", 0) + 1
            tile["fertilizer_available"] = True
            tile["fed_today"] = False
            tile["cared_today"] = False


def spawn_weeds(farm, board_size, weed_chance, rng):
    for y in range(board_size):
        for x in range(board_size):
            if farm["tiles"][y][x] is None and rng.random() < weed_chance:
                farm["tiles"][y][x] = {"kind": "WEED"}


def drop_inventories_to_shed(private, capacity):
    shed = private["shed"]
    for inv in private["inventories"]:
        for item, n in list(inv.items()):
            if n <= 0:
                del inv[item]
                continue
            current = sum(v for k, v in shed.items())
            room = max(0, capacity - current)
            take = min(n, room)
            if take > 0:
                shed[item] = shed.get(item, 0) + take
            del inv[item]


# ============================================================================
# sim/engine.py -- standalone turn orchestration on plain dicts + config.
# ============================================================================

def _cfg_get(cfg, key, default):
    if isinstance(cfg, dict):
        return cfg.get(key, default)
    return getattr(cfg, key, default)


def new_game(config):
    board_size = int(_cfg_get(config, "boardSize", 10))
    starting_money = int(_cfg_get(config, "startingMoney", 3000))
    market_overrides = _cfg_get(config, "marketParams", None)
    resolved_params = _resolve_market_params(market_overrides) if market_overrides else None
    return {
        "step": 0, "day": 0, "hour": 0,
        "farms": [_new_farm(board_size, starting_money) for _ in range(2)],
        "privates": [_new_private() for _ in range(2)],
        "market": _new_market(resolved_params),
        "town": _new_town(),
    }


def _process_market(game_state, actions, config):
    market = game_state["market"]
    farms = game_state["farms"]
    privates = game_state["privates"]
    board_size = int(_cfg_get(config, "boardSize", 10))
    max_orders = max(1, int(_cfg_get(config, "maxMarketOrdersPerTurn", 10)))
    hire_mult = int(_cfg_get(config, "farmHandCostMult", FARM_HAND_COST_MULT))
    shed_capacity = int(_cfg_get(config, "shedCapacity", 100))

    queues = []
    for action in actions:
        m = action.get("market", []) if isinstance(action, dict) else []
        q = list(m) if isinstance(m, list) else []
        queues.append(q[:max_orders])

    max_len = max((len(q) for q in queues), default=0)
    for i in range(max_len):
        order_states = [_parse_order(q[i]) if i < len(q) else None for q in queues]

        for player_id, ostate in enumerate(order_states):
            if ostate is None:
                continue
            op = ostate["type"]
            if op == "HIRE":
                do_hire(farms[player_id], privates[player_id], board_size, hire_mult)
                order_states[player_id] = None
            elif op == "BUY_LAND":
                do_buy_land(farms[player_id], board_size)
                order_states[player_id] = None

        idx_esc = 0
        while True:
            idx_esc += 1
            if idx_esc >= 100_000:
                break
            quoted = [None, None]
            for player_id, ostate in enumerate(order_states):
                if ostate is None or ostate["remaining"] <= 0:
                    continue
                op, item = ostate["type"], ostate["item"]
                if op == "SELL" and item in PRODUCTS:
                    quoted[player_id] = ("SELL", item, market_price(item, market["inventory"][item], market.get("params")), ostate)
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    quoted[player_id] = ("BUY_PRODUCT", item, market_price(item, market["inventory"][item] - 1, market.get("params")), ostate)
                elif op == "BUY_SEED" and item in CROPS:
                    quoted[player_id] = ("BUY_SEED", item, CROPS[item]["seed"], ostate)
                elif op == "BUY_ANIMAL" and item in ANIMALS:
                    quoted[player_id] = ("BUY_ANIMAL", item, ANIMALS[item]["cost"], ostate)
                else:
                    order_states[player_id] = None

            if all(q is None for q in quoted):
                break

            committed_any = False
            for player_id, q in enumerate(quoted):
                if q is None:
                    continue
                op, item, price, ostate = q
                if _commit_unit(op, item, price, farms[player_id], privates[player_id], market, shed_capacity):
                    ostate["remaining"] -= 1
                    committed_any = True
                else:
                    order_states[player_id] = None

            if not committed_any:
                break

        _refresh_prices(market)


def _town_consume(game_state, config, step_num):
    market, town = game_state["market"], game_state["town"]
    shop_interval = max(1, int(_cfg_get(config, "townShopSellInterval", 4)))
    center_interval = max(1, int(_cfg_get(config, "townCenterSellInterval", 12)))
    turns_per_day = max(1, int(_cfg_get(config, "turnsPerDay", 24)))
    day = step_num // turns_per_day

    if step_num % shop_interval == 0:
        for shop_name in town.get("unlocked_shops", []):
            products = SHOPS[shop_name]
            multiplier = 2 if len(products) == 1 else 1
            for item in products:
                market["inventory"][item] -= multiplier

    if step_num % center_interval == 0:
        center_mult = next(m for threshold, m in TOWN_CENTER_DEMAND_SCHEDULE if day >= threshold)
        for item in TOWN_CENTER_PRODUCTS:
            market["inventory"][item] -= center_mult

    _refresh_prices(market)


def _end_of_day(game_state, config, day, seed):
    board_size = int(_cfg_get(config, "boardSize", 10))
    turns_per_day = max(1, int(_cfg_get(config, "turnsPerDay", 24)))
    weed_chance = float(_cfg_get(config, "weedSpawnChance", 0.005))
    shed_cap = int(_cfg_get(config, "shedCapacity", 100))
    shop_interval = max(1, int(_cfg_get(config, "townShopUnlockInterval", 3)))

    rng = random.Random((seed * 1_000_003) ^ day)

    for player_id, farm in enumerate(game_state["farms"]):
        private = game_state["privates"][player_id]
        daily_refresh_plants(farm, day, turns_per_day)
        daily_refresh_animals(farm, day)
        spawn_weeds(farm, board_size, weed_chance, rng)
        drop_inventories_to_shed(private, shed_cap)
        farm["farmer"] = list(_default_spawn(board_size))
        farm["hands"] = []
        farm["hires_today"] = 0
        private["inventories"] = [{}]

    next_day = day + 1
    town = game_state["town"]
    if next_day > 0 and next_day % shop_interval == 0:
        remaining = [s for s in SHOPS if s not in town["unlocked_shops"]]
        if remaining:
            choice = rng.choice(sorted(remaining))
            town["unlocked_shops"].append(choice)


def sim_step(game_state, actions, config):
    """actions: [action_p0, action_p1]. Mutates and returns game_state."""
    turns_per_day = max(1, int(_cfg_get(config, "turnsPerDay", 24)))
    board_size = int(_cfg_get(config, "boardSize", 10))
    shed_capacity = int(_cfg_get(config, "shedCapacity", 100))
    seed = int(_cfg_get(config, "seed", 0))

    step_num = game_state["step"]
    day = step_num // turns_per_day

    for i, action in enumerate(actions):
        farmer_action = action.get("farmer", ["PASS"]) if isinstance(action, dict) else ["PASS"]
        hands_actions = action.get("hands", []) if isinstance(action, dict) else []
        if not isinstance(hands_actions, list):
            hands_actions = []

        unit_actions = [farmer_action, *hands_actions]
        plant_demand = {}
        for a in unit_actions:
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT":
                plant_demand[a[1]] = plant_demand.get(a[1], 0) + 1
        seeds = game_state["privates"][i].get("seeds", {})
        blocked = {crop for crop, n in plant_demand.items() if n > seeds.get(crop, 0)}

        def _allowed(a):
            if isinstance(a, list) and len(a) >= 2 and a[0] == "PLANT" and a[1] in blocked:
                return ["PASS"]
            return a

        apply_unit_action(game_state["farms"][i], game_state["privates"][i], 0,
                           _allowed(farmer_action), board_size, day, turns_per_day, shed_capacity)
        for h_idx, hand_action in enumerate(hands_actions):
            apply_unit_action(game_state["farms"][i], game_state["privates"][i], h_idx + 1,
                               _allowed(hand_action), board_size, day, turns_per_day, shed_capacity)

    _process_market(game_state, actions, config)
    _town_consume(game_state, config, step_num)
    for farm in game_state["farms"]:
        decay_plants(farm, step_num)
    if (step_num + 1) % turns_per_day == 0:
        _end_of_day(game_state, config, day, seed)

    next_step = step_num + 1
    game_state["step"] = next_step
    game_state["day"] = next_step // turns_per_day
    game_state["hour"] = next_step % turns_per_day
    return game_state


# ============================================================================
# sim/obs_adapter.py -- game_state <-> real observation shape, both ways.
# ============================================================================

def to_obs(game_state, player):
    return {
        "step": game_state["step"],
        "player": player,
        "day": game_state["day"],
        "hour": game_state["hour"],
        "farms": game_state["farms"],
        "market": game_state["market"],
        "town": game_state["town"],
        "private": game_state["privates"][player],
    }


def from_obs(obs):
    me = obs["player"]
    other = 1 - me
    privates = [None, None]
    privates[me] = copy.deepcopy(dict(obs["private"]))
    privates[other] = _new_private()
    return {
        "step": obs["step"],
        "day": obs["day"],
        "hour": obs["hour"],
        "farms": copy.deepcopy([dict(f) for f in obs["farms"]]),
        "privates": privates,
        "market": copy.deepcopy(dict(obs["market"])),
        "town": copy.deepcopy(dict(obs["town"])),
    }


# ============================================================================
# sim/value.py -- rollout scorer aligned with win margin, not just own bank.
# ============================================================================

PASS_ACTION = {"farmer": ["PASS"], "hands": [], "market": []}


def _idle_policy(obs):
    return PASS_ACTION


def _money_margin(game_state):
    farms = game_state["farms"]
    return farms[0]["money"] - farms[1]["money"]


def run_policy(game_state, config, policy_fn, turns, opponent_policy_fn=None):
    gs = copy.deepcopy(game_state)
    opponent_fn = opponent_policy_fn or _idle_policy
    for _ in range(turns):
        action0 = policy_fn(to_obs(gs, 0))
        action1 = opponent_fn(to_obs(gs, 1))
        gs = sim_step(gs, [action0, action1], config)
    return gs


def expected_value(game_state, config, candidate_policy_fn, horizon_days,
                    baseline_policy_fn=None, opponent_policy_fn=None, turns_per_day=24):
    turns = horizon_days * turns_per_day
    baseline_fn = baseline_policy_fn or _idle_policy
    candidate_final = run_policy(game_state, config, candidate_policy_fn, turns, opponent_policy_fn)
    baseline_final = run_policy(game_state, config, baseline_fn, turns, opponent_policy_fn)
    return _money_margin(candidate_final) - _money_margin(baseline_final)


def turns_per_day_default(config):
    return int(_cfg_get(config, "turnsPerDay", 24))


def rank_policies(game_state, config, named_policies, horizon_days,
                   baseline_policy_fn=None, opponent_policy_fn=None):
    turns = horizon_days * turns_per_day_default(config)
    results = []
    for label, policy_fn in named_policies.items():
        candidate_final = run_policy(game_state, config, policy_fn, turns, opponent_policy_fn)
        value = _money_margin(candidate_final)
        results.append((label, value))
    return sorted(results, key=lambda kv: -kv[1])


# ============================================================================
# my_agents/path_planner.py -- shared greedy nearest-tile-need movement.
# ============================================================================

def crop_tile_need(tile, day, crop, harvest_wait):
    if tile is None:
        return 2
    if isinstance(tile, dict) and tile.get("kind") == "PLANT" and tile.get("crop") == crop:
        age = day - tile["planted_day"]
        if not tile["watered_today"]:
            return 0
        if tile["yield_units"] > 0 and age >= harvest_wait:
            return 1
    return None


# Measured empirically (tools/measure_land_roi.py in the source repo): one
# worker with greedy nearest-need movement sustains ~10 tiles/day of
# watering out of a 25-tile quadrant.
MEASURED_TILES_PER_WORKER_PER_DAY_RATIO = 10 / 25


def data_driven_seed_cap(managed_tiles):
    return max(1, round(len(managed_tiles) * MEASURED_TILES_PER_WORKER_PER_DAY_RATIO))


def next_op_for_crop(me, tiles, pos, day, crop, harvest_wait, seeds_available):
    fx, fy = pos
    candidates = []
    for (x, y) in tiles:
        need = crop_tile_need(me["tiles"][y][x], day, crop, harvest_wait)
        if need is not None and not (need == 2 and seeds_available == 0):
            dist = abs(x - fx) + abs(y - fy)
            candidates.append((need, dist, x, y))
    if not candidates:
        return ["PASS"]
    candidates.sort()
    _, _, tx, ty = candidates[0]
    if (tx, ty) == (fx, fy):
        tile = me["tiles"][fy][fx]
        if tile is None:
            return ["PLANT", crop]
        if not tile["watered_today"]:
            return ["WATER"]
        return ["HARVEST"]
    if tx != fx:
        return ["EAST"] if tx > fx else ["WEST"]
    return ["SOUTH"] if ty > fy else ["NORTH"]


# ============================================================================
# my_agents/single_crop_loop.py -- single-tile crop agent.
# ============================================================================

CROP_INFO = {
    "WHEAT":      {"seed_cost": 10,  "first_yield_day": 2,  "max_yield_day": 4,  "bonus_start": 2,  "ongoing": False},
    "CARROT":     {"seed_cost": 20,  "first_yield_day": 2,  "max_yield_day": 3,  "bonus_start": 2,  "ongoing": False},
    "TOMATO":     {"seed_cost": 50,  "first_yield_day": 8,  "max_yield_day": 11, "bonus_start": None, "ongoing": True},
    "STRAWBERRY": {"seed_cost": 100, "first_yield_day": 10, "max_yield_day": 16, "bonus_start": None, "ongoing": True},
    "MELON":      {"seed_cost": 80,  "first_yield_day": 10, "max_yield_day": 12, "bonus_start": 6,  "ongoing": False},
}

FERTILIZER_COST = 100
TILE = (4, 4)


def make_crop_agent(crop, track=None, wait_days=None, fertilize=False):
    info = CROP_INFO[crop]
    seed_cost = info["seed_cost"]
    first_yield_day = info["first_yield_day"]
    ongoing = info["ongoing"]
    harvest_wait = wait_days if wait_days is not None else first_yield_day

    if track is None:
        track = {}
    track.setdefault("spent", 0.0)
    track.setdefault("seeds_bought", 0)
    track.setdefault("units_sold", 0)
    track.setdefault("fertilizer_bought", 0)
    track.setdefault("money_by_day", {})

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]

        track["money_by_day"][day] = me["money"]

        x, y = TILE
        tile = me["tiles"][y][x]
        farmer_inv = private["inventories"][0] if private["inventories"] else {}

        market = []
        seeds = private["seeds"].get(crop, 0)
        if seeds == 0 and tile is None and me["money"] >= seed_cost:
            market.append(["BUY_SEED", crop, 1])
            track["spent"] += seed_cost
            track["seeds_bought"] += 1

        shed_qty = private["shed"].get(crop, 0)
        if shed_qty > 0:
            market.append(["SELL", crop, shed_qty])
            track["units_sold"] += shed_qty

        farmer_op = ["PASS"]

        if tile is None and seeds > 0:
            farmer_op = ["PLANT", crop]

        elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
            age = day - tile["planted_day"]

            wants_fertilize = (
                fertilize
                and tile["yield_units"] < 90
                and tile.get("fertilized_until_day", -1) < day
                and (
                    (info["bonus_start"] is not None and age >= info["bonus_start"])
                    if not ongoing else True
                )
            )

            if not tile["watered_today"]:
                farmer_op = ["WATER"]
            elif wants_fertilize and farmer_inv.get("FERTILIZER", 0) > 0:
                farmer_op = ["FERTILIZE"]
            elif wants_fertilize and private["shed"].get("FERTILIZER", 0) > 0:
                farmer_op = ["PICKUP", "FERTILIZER", 1]
            elif wants_fertilize and me["money"] >= obs["market"]["prices"].get("FERTILIZER", FERTILIZER_COST):
                live_price = obs["market"]["prices"].get("FERTILIZER", FERTILIZER_COST)
                market.append(["BUY_PRODUCT", "FERTILIZER", 1])
                track["spent"] += live_price
                track["fertilizer_bought"] += 1
            elif tile["yield_units"] > 0 and (ongoing or age >= harvest_wait):
                farmer_op = ["HARVEST"]

        return {"farmer": farmer_op, "hands": [], "market": market}

    agent.track = track
    return agent


# ============================================================================
# my_agents/quadrant_crop.py -- multi-tile crop agent, one farmer, one quadrant.
# ============================================================================

QUADRANT_TILES = [(x, y) for x in range(5) for y in range(5)]  # NW quadrant
NE_TILES = [(x, y) for x in range(5, 10) for y in range(5)]


def make_quadrant_agent(crop, wait_days=None, track=None, max_seed_stock=None,
                         tiles=None, buy_land_on_turn0=0):
    info = CROP_INFO[crop]
    seed_cost = info["seed_cost"]
    harvest_wait = wait_days if wait_days is not None else info["max_yield_day"]
    managed_tiles = tiles if tiles is not None else QUADRANT_TILES
    if max_seed_stock is None:
        max_seed_stock = data_driven_seed_cap(managed_tiles)

    if track is None:
        track = {}
    track.setdefault("spent", 0.0)
    track.setdefault("seeds_bought", 0)
    track.setdefault("units_sold", 0)
    track.setdefault("money_by_day", {})
    track.setdefault("tiles_watered_today", 0)
    track.setdefault("water_actions_by_day", {})

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]

        track["money_by_day"][day] = me["money"]
        track["water_actions_by_day"].setdefault(day, 0)

        fx, fy = me["farmer"]
        seeds = private["seeds"].get(crop, 0)

        market = []
        n_extra_unlocked = len(me["unlocked_quadrants"]) - 1
        for _ in range(max(0, buy_land_on_turn0 - n_extra_unlocked)):
            market.append(["BUY_LAND"])

        empty_tiles = sum(1 for (x, y) in managed_tiles if me["tiles"][y][x] is None)
        room = max_seed_stock - seeds
        if room > 0 and empty_tiles > 0 and me["money"] >= seed_cost:
            n = min(room, empty_tiles, 3)
            market.append(["BUY_SEED", crop, n])
            track["spent"] += seed_cost * n
            track["seeds_bought"] += n

        shed_qty = private["shed"].get(crop, 0)
        if shed_qty > 0:
            market.append(["SELL", crop, shed_qty])
            track["units_sold"] += shed_qty

        farmer_op = next_op_for_crop(me, managed_tiles, (fx, fy), day, crop, harvest_wait, seeds)
        if farmer_op[0] == "WATER":
            track["water_actions_by_day"][day] += 1

        return {"farmer": farmer_op, "hands": [], "market": market}

    agent.track = track
    return agent


# ============================================================================
# my_agents/multi_worker_crop.py -- farmer on NW, hired hand on NE.
# ============================================================================

SW_TILES = [(x, y) for x in range(5) for y in range(5, 10)]
SE_TILES = [(x, y) for x in range(5, 10) for y in range(5, 10)]
QUADRANT_POOLS = [QUADRANT_TILES, NE_TILES, SW_TILES, SE_TILES]


def make_multi_agent(crop, wait_days=None, track=None, max_seed_stock=None,
                     target_quadrants=2, operating_reserve=800):
    info = CROP_INFO[crop]
    seed_cost = info["seed_cost"]
    harvest_wait = wait_days if wait_days is not None else info["max_yield_day"]
    target_quadrants = max(1, min(4, target_quadrants))
    managed_pools = QUADRANT_POOLS[:target_quadrants]
    all_tiles = [tile for pool in managed_pools for tile in pool]
    if max_seed_stock is None:
        max_seed_stock = data_driven_seed_cap(all_tiles)

    if track is None:
        track = {}
    track.setdefault("spent", 0.0)
    track.setdefault("seeds_bought", 0)
    track.setdefault("units_sold", 0)
    track.setdefault("hire_spent", 0.0)
    track.setdefault("money_by_day", {})

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]
        track["money_by_day"][day] = me["money"]

        market = []
        unlocked_count = len(me["unlocked_quadrants"])
        will_unlock = 0
        if unlocked_count < target_quadrants:
            next_land_cost = LAND_PRICES[unlocked_count - 1]
            if me["money"] >= next_land_cost + operating_reserve:
                market.append(["BUY_LAND"])
                will_unlock = 1

        desired_hands = min(target_quadrants - 1, unlocked_count - 1 + will_unlock)
        hires_needed = max(0, desired_hands - len(me["hands"]))
        for _ in range(hires_needed):
            market.append(["HIRE"])
        track["hire_spent"] += hires_needed

        seeds = private["seeds"].get(crop, 0)
        active_pools = managed_pools[:unlocked_count + will_unlock]
        active_tiles = [tile for pool in active_pools for tile in pool]
        empty_tiles = sum(1 for (x, y) in active_tiles if me["tiles"][y][x] is None)
        room = max_seed_stock - seeds
        if room > 0 and empty_tiles > 0 and me["money"] >= seed_cost:
            n = min(room, empty_tiles, 4)
            market.append(["BUY_SEED", crop, n])
            track["spent"] += seed_cost * n
            track["seeds_bought"] += n

        shed_qty = private["shed"].get(crop, 0)
        if shed_qty > 0:
            market.append(["SELL", crop, shed_qty])
            track["units_sold"] += shed_qty

        farmer_op = next_op_for_crop(me, QUADRANT_TILES, me["farmer"], day, crop, harvest_wait, seeds)

        hands_ops = [
            next_op_for_crop(me, managed_pools[i + 1], pos, day, crop, harvest_wait, seeds)
            for i, pos in enumerate(me["hands"][:target_quadrants - 1])
        ]

        return {"farmer": farmer_op, "hands": hands_ops, "market": market}

    agent.track = track
    return agent


# ============================================================================
# my_agents/animal_loop.py -- single-tile animal agent.
# ============================================================================

ANIMAL_INFO = {
    "GOOSE": {"buy_cost": 300, "product": "EGG",  "structure": "COOP"},
    "COW":   {"buy_cost": 400, "product": "MILK", "structure": "PASTURE"},
    "SHEEP": {"buy_cost": 500, "product": "WOOL", "structure": "PASTURE"},
}

WHEAT_STOCK_BATCH = 10


def make_animal_agent(animal, track=None, care=True):
    info = ANIMAL_INFO[animal]
    structure = info["structure"]
    product = info["product"]
    build_op = "BUILD_COOP" if structure == "COOP" else "BUILD_PASTURE"

    if track is None:
        track = {}
    track.setdefault("spent_animal", 0.0)
    track.setdefault("spent_wheat", 0.0)
    track.setdefault("units_sold", 0)
    track.setdefault("fertilizer_sold", 0)
    track.setdefault("money_by_day", {})

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]

        track["money_by_day"][day] = me["money"]

        x, y = TILE
        tile = me["tiles"][y][x]
        farmer_inv = private["inventories"][0] if private["inventories"] else {}
        shed = private["shed"]

        market = []

        product_qty = shed.get(product, 0)
        if product_qty > 0:
            market.append(["SELL", product, product_qty])
            track["units_sold"] += product_qty

        fert_qty = shed.get("FERTILIZER", 0)
        if fert_qty > 0:
            market.append(["SELL", "FERTILIZER", fert_qty])
            track["fertilizer_sold"] += fert_qty

        farmer_op = ["PASS"]

        if tile is None:
            farmer_op = [build_op]
        elif isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") is None:
            animal_in_farmer_inv = farmer_inv.get(animal, 0) > 0
            animal_in_shed = shed.get(animal, 0) > 0
            if animal_in_farmer_inv:
                farmer_op = ["PLACE", animal]
            elif animal_in_shed:
                farmer_op = ["PICKUP", animal, 1]
            elif me["money"] >= info["buy_cost"]:
                market.append(["BUY_ANIMAL", animal, 1])
                track["spent_animal"] += info["buy_cost"]

        elif isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") == animal:
            wheat_in_farmer_inv = farmer_inv.get("WHEAT", 0)
            if not tile["fed_today"]:
                if wheat_in_farmer_inv > 0:
                    farmer_op = ["FEED"]
                elif shed.get("WHEAT", 0) > 0:
                    farmer_op = ["PICKUP", "WHEAT", WHEAT_STOCK_BATCH]
                else:
                    wheat_price = obs["market"]["prices"].get("WHEAT", 25)
                    cost = wheat_price * WHEAT_STOCK_BATCH
                    if me["money"] >= cost:
                        market.append(["BUY_PRODUCT", "WHEAT", WHEAT_STOCK_BATCH])
                        track["spent_wheat"] += cost
            elif care and not tile["cared_today"]:
                farmer_op = ["CARE"]
            elif tile.get("fertilizer_available"):
                farmer_op = ["COLLECT_FERTILIZER"]
            elif tile["yield_units"] > 0:
                farmer_op = ["HARVEST"]

        return {"farmer": farmer_op, "hands": [], "market": market}

    agent.track = track
    return agent


# ============================================================================
# my_agents/dual_worker_animal.py -- farmer + hired hand, each own animal.
# ============================================================================

DUAL_FARMER_TILE = (4, 4)
DUAL_HAND_TILE = (3, 4)
DUAL_EXTRA_HAND_TILES = [(3, 4), (2, 4), (1, 4)]
DUAL_SHED_WAYPOINT = (4, 4)


def _dual_shed_adjacent(pos, board_size=10):
    half = board_size // 2
    return tuple(pos) in {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def _dual_step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ["EAST"] if tx > x else ["WEST"]
    if y != ty:
        return ["SOUTH"] if ty > y else ["NORTH"]
    return ["PASS"]


def _dual_farmer_op(me, inv, shed, animal, market, track):
    info = ANIMAL_INFO[animal]
    structure = info["structure"]
    build_op = "BUILD_COOP" if structure == "COOP" else "BUILD_PASTURE"
    x, y = DUAL_FARMER_TILE
    tile = me["tiles"][y][x]

    if tile is None:
        return [build_op]
    if isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") is None:
        if inv.get(animal, 0) > 0:
            return ["PLACE", animal]
        if shed.get(animal, 0) > 0:
            return ["PICKUP", animal, 1]
        if me["money"] >= info["buy_cost"]:
            market.append(["BUY_ANIMAL", animal, 1])
            track["spent_animal"] += info["buy_cost"]
        return ["PASS"]
    if isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") == animal:
        if not tile["fed_today"]:
            if inv.get("WHEAT", 0) > 0:
                return ["FEED"]
            if shed.get("WHEAT", 0) > 0:
                return ["PICKUP", "WHEAT", WHEAT_STOCK_BATCH]
            wheat_price = 25
            cost = wheat_price * WHEAT_STOCK_BATCH
            if me["money"] >= cost:
                market.append(["BUY_PRODUCT", "WHEAT", WHEAT_STOCK_BATCH])
                track["spent_wheat"] += cost
            return ["PASS"]
        if not tile["cared_today"]:
            return ["CARE"]
        if tile.get("fertilizer_available"):
            return ["COLLECT_FERTILIZER"]
        if tile["yield_units"] > 0:
            return ["HARVEST"]
    return ["PASS"]


def _dual_hand_op(me, inv, shed, hand_pos, animal, market, track, target=DUAL_HAND_TILE):
    info = ANIMAL_INFO[animal]
    structure = info["structure"]
    build_op = "BUILD_COOP" if structure == "COOP" else "BUILD_PASTURE"
    tx, ty = target
    tile = me["tiles"][ty][tx]
    at_target = tuple(hand_pos) == target
    at_shed = _dual_shed_adjacent(hand_pos)

    if tile is None:
        return [build_op] if at_target else _dual_step_toward(hand_pos, target)

    if isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") is None:
        if inv.get(animal, 0) > 0:
            return ["PLACE", animal] if at_target else _dual_step_toward(hand_pos, target)
        if shed.get(animal, 0) > 0:
            return ["PICKUP", animal, 1] if at_shed else _dual_step_toward(hand_pos, DUAL_SHED_WAYPOINT)
        if me["money"] >= info["buy_cost"]:
            market.append(["BUY_ANIMAL", animal, 1])
            track["spent_animal"] += info["buy_cost"]
        return ["PASS"]

    if isinstance(tile, dict) and tile.get("kind") == structure and tile.get("animal") == animal:
        if not tile["fed_today"]:
            if inv.get("WHEAT", 0) > 0:
                return ["FEED"] if at_target else _dual_step_toward(hand_pos, target)
            if shed.get("WHEAT", 0) > 0:
                return ["PICKUP", "WHEAT", WHEAT_STOCK_BATCH] if at_shed else _dual_step_toward(hand_pos, DUAL_SHED_WAYPOINT)
            wheat_price = 25
            cost = wheat_price * WHEAT_STOCK_BATCH
            if me["money"] >= cost:
                market.append(["BUY_PRODUCT", "WHEAT", WHEAT_STOCK_BATCH])
                track["spent_wheat"] += cost
            return _dual_step_toward(hand_pos, DUAL_SHED_WAYPOINT) if not at_shed else ["PASS"]
        if not tile["cared_today"]:
            return ["CARE"] if at_target else _dual_step_toward(hand_pos, target)
        if tile.get("fertilizer_available"):
            return ["COLLECT_FERTILIZER"] if at_target else _dual_step_toward(hand_pos, target)
        if tile["yield_units"] > 0:
            return ["HARVEST"] if at_target else _dual_step_toward(hand_pos, target)
    return ["PASS"]


def make_dual_animal_agent(animal_a, animal_b=None, track=None, extra_animals=None):
    animal_b = animal_b or animal_a
    hand_animals = ([animal_b] + list(extra_animals or []))[:len(DUAL_EXTRA_HAND_TILES)]

    if track is None:
        track = {}
    track.setdefault("spent_animal", 0.0)
    track.setdefault("spent_wheat", 0.0)
    track.setdefault("units_sold", 0)
    track.setdefault("fertilizer_sold", 0)
    track.setdefault("hire_spent", 0.0)
    track.setdefault("money_by_day", {})

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]
        track["money_by_day"][day] = me["money"]

        shed = private["shed"]
        farmer_inv = private["inventories"][0] if private["inventories"] else {}

        market = []
        hires_needed = max(0, len(hand_animals) - len(me["hands"]))
        for _ in range(hires_needed):
            market.append(["HIRE"])
        track["hire_spent"] += hires_needed

        for prod in {ANIMAL_INFO[a]["product"] for a in [animal_a] + hand_animals}:
            qty = shed.get(prod, 0)
            if qty > 0:
                market.append(["SELL", prod, qty])
                track["units_sold"] += qty
        fert_qty = shed.get("FERTILIZER", 0)
        if fert_qty > 0:
            market.append(["SELL", "FERTILIZER", fert_qty])
            track["fertilizer_sold"] += fert_qty

        farmer_op = _dual_farmer_op(me, farmer_inv, shed, animal_a, market, track)

        hands_ops = []
        for i, (hand_pos, animal, target) in enumerate(
            zip(me["hands"], hand_animals, DUAL_EXTRA_HAND_TILES), start=1
        ):
            hand_inv = private["inventories"][i] if len(private["inventories"]) > i else {}
            hands_ops.append(_dual_hand_op(me, hand_inv, shed, hand_pos, animal, market, track, target))

        return {"farmer": farmer_op, "hands": hands_ops, "market": market}

    agent.track = track
    return agent


# ============================================================================
# my_agents/bugmaker_melon_recycle.py -- Bugmaker-inspired melon recycle line.
# ============================================================================

BUGMAKER_EARLY_MELON_STOCK = 25
BUGMAKER_EARLY_HANDS = 2
BUGMAKER_LATE_HANDS = 1
BUGMAKER_HARVEST_WAIT = {
    "MELON": 10,
    "WHEAT": 2,
    "CARROT": 2,
}
BUGMAKER_NW_WORKER_POOLS = [
    [(x, y) for x in (3, 4) for y in range(5)],
    [(x, y) for x in (0, 1) for y in range(5)],
    [(2, y) for y in range(5)],
]


def _bugmaker_step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ["EAST"] if tx > x else ["WEST"]
    if y != ty:
        return ["SOUTH"] if ty > y else ["NORTH"]
    return ["PASS"]


def _bugmaker_crop_wait(crop):
    return BUGMAKER_HARVEST_WAIT.get(crop, CROP_INFO[crop]["max_yield_day"])


def _bugmaker_tile_need(tile, day, planting_crop, seeds):
    if tile is None:
        return 3 if seeds.get(planting_crop, 0) > 0 else None
    if tile == "LOCKED":
        return None
    if isinstance(tile, dict) and tile.get("kind") == "WEED":
        return 2
    if isinstance(tile, dict) and tile.get("kind") == "PLANT":
        crop = tile.get("crop")
        if not tile.get("watered_today"):
            return 0
        if crop in CROP_INFO:
            age = day - tile["planted_day"]
            if tile.get("yield_units", 0) > 0 and age >= _bugmaker_crop_wait(crop):
                return 1
    return None


def _bugmaker_next_rotation_op(me, tiles, pos, day, planting_crop, seeds):
    candidates = []
    fx, fy = pos
    for x, y in tiles:
        need = _bugmaker_tile_need(me["tiles"][y][x], day, planting_crop, seeds)
        if need is None:
            continue
        candidates.append((need, abs(x - fx) + abs(y - fy), x, y))
    if not candidates:
        return ["PASS"]
    candidates.sort()
    _need, _dist, tx, ty = candidates[0]
    if (fx, fy) != (tx, ty):
        return _bugmaker_step_toward((fx, fy), (tx, ty))

    tile = me["tiles"][fy][fx]
    if tile is None:
        return ["PLANT", planting_crop]
    if isinstance(tile, dict) and tile.get("kind") == "WEED":
        return ["DIG"]
    if isinstance(tile, dict) and tile.get("kind") == "PLANT":
        if not tile.get("watered_today"):
            return ["WATER"]
        return ["HARVEST"]
    return ["PASS"]


def _bugmaker_sell_products(shed, market, track):
    for product in ("MELON", "WHEAT", "CARROT"):
        qty = shed.get(product, 0)
        if qty > 0:
            market.append(["SELL", product, qty])
            sold = track["units_sold_by_product"]
            sold[product] = sold.get(product, 0) + qty


def _bugmaker_land_orders(me, day, target_quadrants):
    if day < 12:
        return []
    orders = []
    money_after_orders = me["money"]
    unlocked_count = len(me["unlocked_quadrants"])
    while unlocked_count < target_quadrants:
        cost = LAND_PRICES[unlocked_count - 1]
        if money_after_orders < cost:
            break
        orders.append(["BUY_LAND"])
        money_after_orders -= cost
        unlocked_count += 1
    return orders


def _bugmaker_planting_crop(day):
    return "WHEAT" if day >= 16 else "MELON"


def _bugmaker_worker_pools(active_quadrants):
    if active_quadrants <= 1:
        return BUGMAKER_NW_WORKER_POOLS
    return QUADRANT_POOLS[:max(1, min(3, active_quadrants))]


def make_bugmaker_melon_recycle_agent(track=None, target_quadrants=4):
    if track is None:
        track = {}
    track.setdefault("money_by_day", {})
    track.setdefault("seeds_bought_by_crop", {})
    track.setdefault("units_sold_by_product", {})
    track.setdefault("hire_orders", 0)
    track.setdefault("land_orders", 0)

    def agent(obs):
        player = obs["player"]
        me = obs["farms"][player]
        private = obs["private"]
        day = obs["day"]
        hour = obs["hour"]
        track["money_by_day"][day] = me["money"]

        planting_crop = _bugmaker_planting_crop(day)
        market = []
        _bugmaker_sell_products(private["shed"], market, track)

        desired_hands = BUGMAKER_EARLY_HANDS if day <= 24 else BUGMAKER_LATE_HANDS
        hires_needed = max(0, desired_hands - len(me["hands"]))
        for _ in range(hires_needed):
            market.append(["HIRE"])
            track["hire_orders"] += 1

        land_orders = _bugmaker_land_orders(me, day, target_quadrants)
        market.extend(land_orders)
        track["land_orders"] += len(land_orders)

        seeds = private["seeds"]
        active_quadrants = min(target_quadrants, len(me["unlocked_quadrants"]) + len(land_orders))
        active_tiles = [
            tile for pool in QUADRANT_POOLS[:active_quadrants] for tile in pool
        ]
        empty_tiles = sum(1 for x, y in active_tiles if me["tiles"][y][x] is None)

        if planting_crop == "MELON":
            seed_cost = CROP_INFO["MELON"]["seed_cost"]
            desired_stock = BUGMAKER_EARLY_MELON_STOCK if day <= 4 else min(8, empty_tiles)
            needed = max(0, min(empty_tiles, desired_stock - seeds.get("MELON", 0)))
            if needed > 0 and day <= 14 and me["money"] >= seed_cost:
                qty = min(needed, me["money"] // seed_cost)
                if qty > 0:
                    market.append(["BUY_SEED", "MELON", qty])
                    bought = track["seeds_bought_by_crop"]
                    bought["MELON"] = bought.get("MELON", 0) + qty
        else:
            seed_cost = CROP_INFO[planting_crop]["seed_cost"]
            desired_stock = min(8, empty_tiles)
            needed = max(0, min(empty_tiles, desired_stock - seeds.get(planting_crop, 0)))
            if needed > 0 and me["money"] >= seed_cost:
                qty = min(needed, me["money"] // seed_cost)
                if qty > 0:
                    market.append(["BUY_SEED", planting_crop, qty])
                    bought = track["seeds_bought_by_crop"]
                    bought[planting_crop] = bought.get(planting_crop, 0) + qty

        pools_for_workers = _bugmaker_worker_pools(active_quadrants)
        farmer_op = _bugmaker_next_rotation_op(
            me, pools_for_workers[0], me["farmer"], day, planting_crop, seeds
        )
        hands_ops = []
        for index, pos in enumerate(me["hands"]):
            pool = pools_for_workers[min(index + 1, len(pools_for_workers) - 1)]
            hands_ops.append(_bugmaker_next_rotation_op(me, pool, pos, day, planting_crop, seeds))

        return {"farmer": farmer_op, "hands": hands_ops, "market": market}

    agent.track = track
    return agent


# ============================================================================
# planner/opponent_model.py -- infer + mimic the opponent's visible strategy.
# ============================================================================

def _tiles_for_quadrants(unlocked_quadrants):
    tiles = list(QUADRANT_TILES)
    if "NE" in unlocked_quadrants:
        tiles = tiles + NE_TILES
    return tiles


def infer_opponent_focus(opponent_farm):
    crop_counts = Counter()
    animal_counts = Counter()
    for row in opponent_farm["tiles"]:
        for tile in row:
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "PLANT" and tile.get("crop") in CROPS:
                crop_counts[tile["crop"]] += 1
            elif tile.get("animal") in ANIMALS:
                animal_counts[tile["animal"]] += 1
            elif tile.get("kind") == "COOP":
                animal_counts["GOOSE"] += 0.5
            elif tile.get("kind") == "PASTURE":
                animal_counts["COW"] += 0.5

    best_crop = crop_counts.most_common(1)[0] if crop_counts else (None, 0)
    best_animal = animal_counts.most_common(1)[0] if animal_counts else (None, 0)
    if best_animal[1] == 0 and best_crop[1] == 0:
        return None
    if best_crop[1] > 0 and best_animal[1] > 0:
        if best_crop[1] >= best_animal[1] or best_animal[0] == "GOOSE":
            return ("CROP", best_crop[0])
    if best_animal[1] >= best_crop[1] and best_animal[0] is not None:
        return ("ANIMAL", best_animal[0])
    return ("CROP", best_crop[0])


def mimic_opponent_policy(opponent_farm):
    focus = infer_opponent_focus(opponent_farm)
    if focus is None:
        return lambda obs: PASS_ACTION
    kind, name = focus
    if kind == "ANIMAL":
        visible_workers = len(opponent_farm.get("hands", []))
        if visible_workers > 0:
            extra_animals = [name] * max(0, visible_workers - 1)
            return make_dual_animal_agent(name, animal_b=name, extra_animals=extra_animals)
        return make_animal_agent(name)
    wait = CROPS[name]["max_yield_day"]
    unlocked_quadrants = opponent_farm.get("unlocked_quadrants", ["NW"])
    visible_workers = len(opponent_farm.get("hands", []))
    if len(unlocked_quadrants) > 1 or visible_workers > 0:
        target_quadrants = max(2, min(4, max(len(unlocked_quadrants), visible_workers + 1)))
        return make_multi_agent(name, wait_days=wait, target_quadrants=target_quadrants)
    tiles = _tiles_for_quadrants(unlocked_quadrants)
    return make_quadrant_agent(name, wait_days=wait, tiles=tiles)


# ============================================================================
# planner/candidates.py -- the strategy pool search chooses between.
# ============================================================================

def default_candidates():
    candidates = {}

    for quadrants in (2, 3, 4):
        candidates[f"multi_worker_MELON_{quadrants}q"] = (
            lambda quadrants=quadrants: make_multi_agent(
                "MELON", wait_days=CROP_INFO["MELON"]["max_yield_day"],
                target_quadrants=quadrants,
            )
        )

    for a, b in [("COW", "COW"), ("COW", "SHEEP")]:
        candidates[f"dual_{a}_{b}"] = (
            lambda a=a, b=b: make_dual_animal_agent(a, animal_b=b)
        )

    candidates["triple_COW_SHEEP_GOOSE"] = (
        lambda: make_dual_animal_agent("COW", animal_b="SHEEP", extra_animals=["GOOSE"])
    )
    candidates["triple_COW_COW_SHEEP"] = (
        lambda: make_dual_animal_agent("COW", animal_b="COW", extra_animals=["SHEEP"])
    )
    candidates["quad_COW_COW_COW_SHEEP"] = (
        lambda: make_dual_animal_agent("COW", animal_b="COW", extra_animals=["COW", "SHEEP"])
    )
    candidates["quad_COW_COW_SHEEP_SHEEP"] = (
        lambda: make_dual_animal_agent("COW", animal_b="COW", extra_animals=["SHEEP", "SHEEP"])
    )
    candidates["bugmaker_melon_recycle"] = make_bugmaker_melon_recycle_agent

    return candidates


# ============================================================================
# planner/search.py -- score every candidate via a simulated rollout.
# ============================================================================

def _filtered_candidates(obs, candidates):
    focus = infer_opponent_focus(obs["farms"][1 - obs["player"]])
    crop_tempo_counters = {
        "bugmaker_melon_recycle",
        "multi_worker_MELON_2q",
        "dual_COW_COW",
    }
    if obs["day"] <= 2 and focus is None:
        representative = {
            *crop_tempo_counters,
            "quad_COW_COW_COW_SHEEP",
            "quad_COW_COW_SHEEP_SHEEP",
        }
        reduced = {
            label: factory
            for label, factory in candidates.items()
            if label in representative
        }
        if reduced:
            return reduced
    if obs["day"] <= 5 and focus and focus[0] == "CROP":
        reduced = {
            label: factory
            for label, factory in candidates.items()
            if label in crop_tempo_counters
        }
        if reduced:
            return reduced
    return candidates


def choose_strategy(obs, config, horizon_days, candidates=None, model_opponent=True):
    game_state = from_obs(obs)
    cands = candidates or default_candidates()
    cands = _filtered_candidates(obs, cands)

    opponent_policy_fn = None
    if model_opponent:
        opponent_id = 1 - obs["player"]
        opponent_policy_fn = mimic_opponent_policy(game_state["farms"][opponent_id])

    named_policies = {label: factory() for label, factory in cands.items()}
    results = rank_policies(game_state, config, named_policies, horizon_days,
                             opponent_policy_fn=opponent_policy_fn)

    best_label = results[0][0]
    best_agent = cands[best_label]()
    return best_label, best_agent, results


# ============================================================================
# planner/emergency_handler.py -- rescue an at-risk orphaned tile.
# ============================================================================

def _needs_rescue(tile):
    if not isinstance(tile, dict):
        return None
    if tile.get("kind") == "PLANT" and tile.get("consecutive_unwatered", 0) >= 1 and not tile.get("watered_today", False):
        return "WATER"
    if "animal" in tile and tile.get("consecutive_unfed", 0) >= 1 and not tile.get("fed_today", False):
        return "FEED"
    return None


def _rescue_op(me, pos):
    x, y = pos
    op = _needs_rescue(me["tiles"][y][x])
    return [op] if op else None


def apply_emergency_override(action, me):
    farmer_op = list(action.get("farmer", ["PASS"]))
    rescue = _rescue_op(me, me["farmer"])
    if rescue and farmer_op[0] not in ("WATER", "FEED"):
        farmer_op = rescue

    policy_hands_ops = action.get("hands", [])
    hands_ops = []
    for i, hand_pos in enumerate(me.get("hands", [])):
        op = list(policy_hands_ops[i]) if i < len(policy_hands_ops) and policy_hands_ops[i] else ["PASS"]
        rescue = _rescue_op(me, hand_pos)
        if rescue and op[0] not in ("WATER", "FEED"):
            op = rescue
        hands_ops.append(op)

    new_action = dict(action)
    new_action["farmer"] = farmer_op
    new_action["hands"] = hands_ops
    return new_action


# ============================================================================
# planner/executor.py -- replan cadence + safety nets -> live agent(obs).
# ============================================================================

def _suppress_wasted_purchases(action, days_remaining):
    market = action.get("market", []) if isinstance(action, dict) else []
    if not market:
        return action

    filtered = []
    for order in market:
        if not (isinstance(order, list) and order):
            continue
        op = order[0]
        if op == "BUY_SEED" and len(order) >= 2 and order[1] in CROPS:
            first_yield = CROPS[order[1]]["first_yield_day"]
            if days_remaining < first_yield + 1:
                continue
        elif op == "BUY_ANIMAL" and len(order) >= 2 and order[1] in ANIMALS:
            first_yield = ANIMALS[order[1]]["first_yield_day"]
            if days_remaining < first_yield + 1:
                continue
        filtered.append(order)

    if filtered == market:
        return action
    new_action = dict(action)
    new_action["market"] = filtered
    return new_action


def make_planner_agent(config, horizon_days="remaining", replan_interval_days=5,
                        season_days=None, candidates=None, verbose=False,
                        early_replan_turns=6, early_replan_days=3):
    if season_days is None:
        turns_per_day = _cfg_get(config, "turnsPerDay", 24)
        episode_steps = _cfg_get(config, "episodeSteps", 720)
        season_days = episode_steps // turns_per_day
    else:
        turns_per_day = _cfg_get(config, "turnsPerDay", 24)
    state = {
        "active_label": None,
        "active_agent": None,
        "last_replan_day": -1,
        "last_replan_step": -10**9,
        "last_opponent_focus": None,
        "history": [],
    }

    def agent(obs):
        day = obs["day"]
        step = obs.get("step", day * turns_per_day + obs.get("hour", 0))
        opponent_focus = infer_opponent_focus(obs["farms"][1 - obs["player"]])
        focus_changed = opponent_focus is not None and opponent_focus != state["last_opponent_focus"]
        opening_refresh_due = (
            early_replan_turns is not None
            and early_replan_turns > 0
            and day < early_replan_days
            and step - state["last_replan_step"] >= early_replan_turns
        )
        should_replan = (
            state["active_agent"] is None
            or focus_changed
            or opening_refresh_due
            or day - state["last_replan_day"] >= replan_interval_days
        )
        if should_replan:
            effective_horizon = (
                max(1, season_days - day) if horizon_days == "remaining" else horizon_days
            )
            label, active_agent, ranked = choose_strategy(obs, config, effective_horizon, candidates)
            state["active_label"] = label
            state["active_agent"] = active_agent
            state["last_replan_day"] = day
            state["last_replan_step"] = step
            state["last_opponent_focus"] = opponent_focus
            state["history"].append((day, label, ranked[:3]))
            if verbose:
                print(f"[planner] day {day}: replanned -> {label}  top3={ranked[:3]}")
        action = state["active_agent"](obs)
        action = _suppress_wasted_purchases(action, season_days - day)
        me = obs["farms"][obs["player"]]
        return apply_emergency_override(action, me)

    agent.state = state
    return agent


# ============================================================================
# Competition entry point.
# ============================================================================

# The real episode seed is deliberately hidden from agents by the framework
# (kaggle_environments.utils.resolve_episode_seed clears configuration["seed"]
# after resolving it), so the simulator's own internal RNG -- used only to
# predict weed-spawn/shop-unlock TIMING during lookahead, at a 0.5%/tile/day
# rate, low-stakes -- can never match the true hidden seed. This is a fixed,
# arbitrary placeholder for that internal simulation only, not a guess at
# the real one.
_FALLBACK_SIM_SEED = 20260807

_SUBMISSION_STATE = {}


def agent(obs, configuration=None):
    """Kaggle entry point. Lazily builds and caches the planner on first
    call using the real configuration (module-level state persists across
    turns within one episode, since kaggle_environments loads this module
    once per episode, not once per turn). Never lets an unexpected
    exception crash the episode -- falls back to PASS, which is always a
    legal, safe action, and retries building/using the planner on
    subsequent turns."""
    if "planner" not in _SUBMISSION_STATE:
        try:
            config = dict(configuration) if configuration is not None else {}
        except (TypeError, ValueError):
            config = {}
        if config.get("seed") is None:
            config["seed"] = _FALLBACK_SIM_SEED
        try:
            _SUBMISSION_STATE["planner"] = make_planner_agent(config)
        except Exception:
            _SUBMISSION_STATE["planner"] = None

    planner = _SUBMISSION_STATE.get("planner")
    if planner is not None:
        try:
            return planner(obs)
        except Exception:
            pass
    return {"farmer": ["PASS"], "hands": [], "market": []}


# ============================================================================
# V6 submission override: Barathan Aslan melon -> land -> wheat replay copy.
# This final `agent` definition intentionally shadows the planner entry point
# above. It keeps the submitted file single-file/self-contained while removing
# the v5 selector risk that chose cattle in the latest Barathan loss.
# ============================================================================

_V6_MAX_MARKET_ORDERS = 10
_V6_EARLY_HANDS = 5
_V6_LATE_HANDS = 11
_V6_MELON_STOCK = 25
_V6_HARVEST_WAIT = {"MELON": 10, "WHEAT": 2}
_V6_NW_ANCHORS = [(4, 4), (3, 4), (1, 4), (4, 1), (1, 1), (2, 2)]
_V6_FULL_FARM_ANCHORS = [
    (4, 4), (3, 4), (1, 4), (4, 1), (1, 1), (2, 2),
    (7, 4), (9, 4), (7, 1), (9, 1), (2, 7), (7, 7),
]


def _v6_step_toward(pos, target):
    x, y = pos
    tx, ty = target
    if x != tx:
        return ["EAST"] if tx > x else ["WEST"]
    if y != ty:
        return ["SOUTH"] if ty > y else ["NORTH"]
    return ["PASS"]


def _v6_shed_adjacent(pos, board_size=10):
    half = board_size // 2
    return tuple(pos) in {(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)}


def _v6_crop_wait(crop):
    return _V6_HARVEST_WAIT.get(crop, CROP_INFO[crop]["max_yield_day"])


def _v6_partition_tiles(tiles, anchors, unit_count):
    anchors = anchors[:unit_count]
    pools = [[] for _ in anchors]
    for tile in tiles:
        tx, ty = tile
        best = min(
            range(len(anchors)),
            key=lambda idx: (abs(tx - anchors[idx][0]) + abs(ty - anchors[idx][1]), idx),
        )
        pools[best].append(tile)
    return [pool or list(tiles) for pool in pools]


def _v6_active_tiles(me, active_quadrants):
    tiles = []
    for pool in QUADRANT_POOLS[:active_quadrants]:
        for x, y in pool:
            if me["tiles"][y][x] != "LOCKED":
                tiles.append((x, y))
    return tiles


def _v6_worker_pools(me, active_quadrants, unit_count):
    tiles = _v6_active_tiles(me, active_quadrants)
    anchors = _V6_NW_ANCHORS if active_quadrants <= 1 else _V6_FULL_FARM_ANCHORS
    return _v6_partition_tiles(tiles, anchors, unit_count)


def _v6_tile_need(tile, day, planting_crop, seeds):
    if tile is None:
        return 3 if seeds.get(planting_crop, 0) > 0 else None
    if tile == "LOCKED":
        return None
    if isinstance(tile, dict) and tile.get("kind") == "WEED":
        return 2
    if isinstance(tile, dict) and tile.get("kind") == "PLANT":
        crop = tile.get("crop")
        if not tile.get("watered_today"):
            return 0
        if crop in CROP_INFO:
            age = day - tile["planted_day"]
            if tile.get("yield_units", 0) > 0 and age >= _v6_crop_wait(crop):
                return 1
    return None


def _v6_next_crop_op(me, tiles, pos, day, planting_crop, seeds, inventory):
    if any(inventory.get(item, 0) > 0 for item in ("MELON", "WHEAT", "CARROT")):
        if _v6_shed_adjacent(pos):
            return ["DROP"]
        return _v6_step_toward(pos, (4, 4))

    candidates = []
    fx, fy = pos
    for x, y in tiles:
        need = _v6_tile_need(me["tiles"][y][x], day, planting_crop, seeds)
        if need is not None:
            candidates.append((need, abs(x - fx) + abs(y - fy), x, y))
    if not candidates:
        return ["PASS"]
    candidates.sort()
    _need, _dist, tx, ty = candidates[0]
    if (fx, fy) != (tx, ty):
        return _v6_step_toward((fx, fy), (tx, ty))

    tile = me["tiles"][fy][fx]
    if tile is None:
        return ["PLANT", planting_crop]
    if isinstance(tile, dict) and tile.get("kind") == "WEED":
        return ["DIG"]
    if isinstance(tile, dict) and tile.get("kind") == "PLANT":
        if not tile.get("watered_today"):
            return ["WATER"]
        return ["HARVEST"]
    return ["PASS"]


def _v6_append_order(market, order):
    if len(market) < _V6_MAX_MARKET_ORDERS:
        market.append(order)


def _v6_sell_shed(shed, market):
    for product in ("MELON", "WHEAT", "CARROT"):
        qty = shed.get(product, 0)
        if qty > 0:
            _v6_append_order(market, ["SELL", product, qty])


def _v6_estimated_sell_value(shed, prices):
    return sum(shed.get(product, 0) * prices.get(product, 1) for product in ("MELON", "WHEAT", "CARROT"))


def _v6_land_orders(me, day, prices, shed):
    if day < 10:
        return []
    orders = []
    available = me["money"] + _v6_estimated_sell_value(shed, prices)
    unlocked_count = len(me["unlocked_quadrants"])
    while unlocked_count < 4:
        cost = LAND_PRICES[unlocked_count - 1]
        if available < cost:
            break
        orders.append(["BUY_LAND"])
        available -= cost
        unlocked_count += 1
    return orders


def _v6_planting_crop(day):
    return "WHEAT" if day >= 10 else "MELON"


def _v6_seed_order(me, seeds, day, crop, active_tiles):
    empty_tiles = sum(1 for x, y in active_tiles if me["tiles"][y][x] is None)
    if empty_tiles <= 0:
        return None

    if crop == "MELON":
        if day > 1:
            return None
        planted = sum(
            1
            for x, y in active_tiles
            if isinstance(me["tiles"][y][x], dict)
            and me["tiles"][y][x].get("kind") == "PLANT"
            and me["tiles"][y][x].get("crop") == "MELON"
        )
        desired_stock = max(0, _V6_MELON_STOCK - planted)
    else:
        if day > 27:
            return None
        desired_stock = min(80, empty_tiles)

    needed = max(0, min(empty_tiles, desired_stock - seeds.get(crop, 0)))
    seed_cost = CROP_INFO[crop]["seed_cost"]
    if needed <= 0 or me["money"] < seed_cost:
        return None
    qty = int(min(needed, me["money"] // seed_cost))
    return ["BUY_SEED", crop, qty] if qty > 0 else None


def _v6_action(obs):
    player = obs["player"]
    me = obs["farms"][player]
    private = obs["private"]
    day = obs["day"]
    planting_crop = _v6_planting_crop(day)
    market = []

    _v6_sell_shed(private["shed"], market)
    land_orders = _v6_land_orders(me, day, obs["market"]["prices"], private["shed"])
    for order in land_orders:
        _v6_append_order(market, order)

    active_quadrants = min(4, len(me["unlocked_quadrants"]) + len(land_orders))
    active_tiles = _v6_active_tiles(me, active_quadrants)
    seed_order = _v6_seed_order(me, private["seeds"], day, planting_crop, active_tiles)
    if seed_order is not None:
        _v6_append_order(market, seed_order)

    desired_hands = _V6_EARLY_HANDS if day < 10 else _V6_LATE_HANDS
    for _ in range(max(0, desired_hands - len(me["hands"]))):
        _v6_append_order(market, ["HIRE"])

    unit_count = 1 + len(me["hands"])
    pools = _v6_worker_pools(me, active_quadrants, max(1, unit_count))
    inventories = private["inventories"]
    farmer_inv = inventories[0] if inventories else {}
    farmer_op = _v6_next_crop_op(me, pools[0], me["farmer"], day, planting_crop, private["seeds"], farmer_inv)

    hands_ops = []
    for index, pos in enumerate(me["hands"]):
        inv = inventories[index + 1] if len(inventories) > index + 1 else {}
        pool = pools[min(index + 1, len(pools) - 1)]
        hands_ops.append(_v6_next_crop_op(me, pool, pos, day, planting_crop, private["seeds"], inv))

    return {"farmer": farmer_op, "hands": hands_ops, "market": market}


def agent(obs, configuration=None):
    try:
        return _v6_action(obs)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}


# ============================================================================
# Current submission override: champion all-11 labor schedule.
# V7-A remains in my_agents/v7_melon_dynamic.py as a controlled challenger,
# but the first sweep favored all-11 for final cash, so the Kaggle-ready file
# should not default to the reduced-labor experiment.
# ============================================================================

_V7_LATE_HANDS = 11
_V7_DAY24_HANDS = 11
_V7_DAY28_HANDS = 11
_V7_DAY29_HANDS = 11


def _v7_desired_hands(day):
    if day < 10:
        return _V6_EARLY_HANDS
    if day < 24:
        return _V7_LATE_HANDS
    if day < 28:
        return _V7_DAY24_HANDS
    if day == 28:
        return _V7_DAY28_HANDS
    return _V7_DAY29_HANDS


def _v7_action(obs):
    player = obs["player"]
    me = obs["farms"][player]
    private = obs["private"]
    day = obs["day"]
    planting_crop = _v6_planting_crop(day)
    market = []

    _v6_sell_shed(private["shed"], market)
    land_orders = _v6_land_orders(me, day, obs["market"]["prices"], private["shed"])
    for order in land_orders:
        _v6_append_order(market, order)

    active_quadrants = min(4, len(me["unlocked_quadrants"]) + len(land_orders))
    active_tiles = _v6_active_tiles(me, active_quadrants)
    seed_order = _v6_seed_order(me, private["seeds"], day, planting_crop, active_tiles)
    if seed_order is not None:
        _v6_append_order(market, seed_order)

    for _ in range(max(0, _v7_desired_hands(day) - len(me["hands"]))):
        _v6_append_order(market, ["HIRE"])

    unit_count = 1 + len(me["hands"])
    pools = _v6_worker_pools(me, active_quadrants, max(1, unit_count))
    inventories = private["inventories"]
    farmer_inv = inventories[0] if inventories else {}
    farmer_op = _v6_next_crop_op(me, pools[0], me["farmer"], day, planting_crop, private["seeds"], farmer_inv)

    hands_ops = []
    for index, pos in enumerate(me["hands"]):
        inv = inventories[index + 1] if len(inventories) > index + 1 else {}
        pool = pools[min(index + 1, len(pools) - 1)]
        hands_ops.append(_v6_next_crop_op(me, pool, pos, day, planting_crop, private["seeds"], inv))

    return {"farmer": farmer_op, "hands": hands_ops, "market": market}


def agent(obs, configuration=None):
    try:
        return _v7_action(obs)
    except Exception:
        return {"farmer": ["PASS"], "hands": [], "market": []}
