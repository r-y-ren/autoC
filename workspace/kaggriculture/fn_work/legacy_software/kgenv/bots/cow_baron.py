"""Strong heuristic opponent: cow_baron_agent -- "dairy baron" (m1 wave 2).

Animal-mix variant of the goose engine family: COWS on pastures hugging the
shed instead of geese.  Fed + cared daily (care banking turns 1 milk / 2 days
into 3), wheat on the remaining tiles for feed self-sufficiency and cash.
Milk sells through a price gate in bounded tranches (the shared market's
linear milk glut punishes dumps); fertilizer sells daily; day 29 liquidates.

Purely a function of the observation (stateless per call), same signature as
the other local bots: f(obs) -> {"farmer": [...], "hands": [[...]],
"market": [[...]]}.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

CROPS_INFO = {
    "WHEAT":  {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT": {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "MELON":  {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS_INFO = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}

COW_CAP = 6                 # cows in play at once (feed labour bound)
WHEAT_TILES = 12            # concurrent wheat tiles (feed + cash)
MILK_GATE = 130             # hold milk below this price (linear glut curve)
MILK_TRANCHE = 10           # bounded tranche per triggered day
HANDS_TARGET = 3            # farmer + 3 hands
SEASON_DAYS = 30
COW_RESERVE = 700           # keep this much cash besides a cow purchase
WHEAT_BUY_MAX_PRICE = 45    # buy feed wheat only while cheap


def _dist(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx: int, fy: int, tx: int, ty: int) -> List[str]:
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _shed_tile(board: int) -> Tuple[int, int]:
    return (board // 2 - 1, board // 2 - 1)


def _shed_adjacent(x: int, y: int, board: int) -> bool:
    h = board // 2
    return (x, y) in ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))


def cow_baron_agent(obs: Dict) -> Dict:
    player = obs.get("player", 0)
    farms = obs.get("farms", [])
    private = obs.get("private", {}) or {}
    if not farms or player >= len(farms):
        return {"farmer": ["PASS"], "hands": [], "market": []}
    farm = farms[player]
    day = obs.get("day", 0)
    hour = obs.get("hour", 0)
    money = farm.get("money", 0.0)
    tiles = farm.get("tiles", [])
    board = len(tiles)
    if not board:
        return {"farmer": ["PASS"], "hands": [], "market": []}
    seeds = private.get("seeds", {}) or {}
    shed = private.get("shed", {}) or {}
    inventories = private.get("inventories", []) or []
    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
    fx, fy = farm.get("farmer", [board // 2 - 1] * 2)
    hands = farm.get("hands", []) or []
    last_day = day >= SEASON_DAYS - 1

    # ---- read the ground ------------------------------------------------
    cows = 0            # living animals
    pastures: List[Tuple[int, int]] = []       # structures (occupied or not)
    wheat_tiles: List[Tuple[int, int]] = []
    empty: List[Tuple[int, int]] = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            if tile is None:
                empty.append((x, y))
            elif isinstance(tile, dict):
                if tile.get("kind") == "PASTURE":
                    pastures.append((x, y))
                    if "animal" in tile:
                        cows += 1
                elif tile.get("kind") == "PLANT":
                    wheat_tiles.append((x, y))

    sx, sy = _shed_tile(board)
    empty.sort(key=lambda p: (_dist(sx, sy, p[0], p[1]), p[1], p[0]))
    shed_cows = shed.get("COW", 0) + sum(
        (inv or {}).get("COW", 0) for inv in inventories if inv)

    # ---- task list ------------------------------------------------------
    tasks: List[Dict] = []

    def add(w, x, y, act, key, need=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key, "need": need})

    animals_to_feed = 0
    for x, y in pastures:
        tile = tiles[y][x]
        if "animal" not in tile:
            if shed_cows > 0:
                add(54, x, y, ["PLACE", "COW"], ("place", x, y), need="COW")
            continue
        if not last_day:
            if not tile.get("fed_today", False):
                animals_to_feed += 1
                w = 100 if tile.get("consecutive_unfed", 0) >= 1 else 90
                add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
            if day <= SEASON_DAYS - 2 and not tile.get("cared_today", False) \
                    and tile.get("fed_today", False):
                add(47, x, y, ["CARE"], ("care", x, y))
        if tile.get("yield_units", 0) >= 3 or (tile.get("yield_units", 0) > 0 and last_day):
            add(66, x, y, ["HARVEST"], ("harvest", x, y))
        if tile.get("fertilizer_available", False):
            add(36, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))

    # pasture ring: BUILD_PASTURE on the empties nearest the shed until cap;
    # wheat field: plant up to cap on the empties beyond the near ring
    if not last_day:
        for x, y in empty:
            if len(pastures) >= COW_CAP:
                break
            if _dist(sx, sy, x, y) <= 2:
                add(44, x, y, ["BUILD_PASTURE"], ("bpast", x, y))
                pastures.append((x, y))  # reserve the ring tile
    wheat_room = WHEAT_TILES - len(wheat_tiles)
    plantable = [p for p in empty if _dist(sx, sy, p[0], p[1]) >= 2]
    for x, y in plantable[:max(0, wheat_room)]:
        if seeds.get("WHEAT", 0) > 0 and day <= SEASON_DAYS - 6 and not last_day:
            add(26, x, y, ["PLANT", "WHEAT"], ("plant", x, y))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict) or tile.get("kind") != "PLANT":
                continue
            if not last_day:
                cd = CROPS_INFO.get(tile.get("crop", ""), None)
                if cd is None:
                    continue
                age = day - tile.get("planted_day", day)
                if not tile.get("watered_today", False):
                    if tile.get("consecutive_unwatered", 0) >= 1:
                        add(98, x, y, ["WATER"], ("water", x, y))
                    elif 2 <= age <= 4:
                        add(34, x, y, ["WATER"], ("water", x, y))
            age_w = day - tile.get("planted_day", day)
            if tile.get("yield_units", 0) > 0 and (
                    age_w >= 5 or (age_w >= 4 and (tile.get("watered_today", False)
                                                   or hour >= 20)) or last_day):
                add(72, x, y, ["HARVEST"], ("harvestw", x, y))
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if isinstance(tile, dict) and tile.get("kind") == "WEED":
                add(20, x, y, ["DIG"], ("dig", x, y))

    # ---- logistics (shed pickups) ----------------------------------------
    wheat_on_units = sum((inv or {}).get("WHEAT", 0) for inv in inventories if inv)
    if animals_to_feed > 0 and wheat_on_units == 0 and shed.get("WHEAT", 0) > 0:
        n = min(animals_to_feed + 1, shed.get("WHEAT", 0))
        add(96, sx, sy, ["PICKUP", "WHEAT", n], ("pickup_w", 0))
    cows_on_units = sum((inv or {}).get("COW", 0) for inv in inventories if inv)
    if shed.get("COW", 0) > 0 and cows_on_units == 0 and \
            any(t["key"][0] == "place" for t in tasks):
        add(94, sx, sy, ["PICKUP", "COW", min(2, shed.get("COW", 0))],
            ("pickup_c", 0))

    # ---- schedule units (claim-based, act-here-first) ---------------------
    claimed = set()

    def unit_inv(i: int) -> Dict:
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    def executable(t: Dict, ui: int) -> bool:
        need = t.get("need")
        if need and (inv := unit_inv(ui)).get(need, 0) <= 0:
            return False
        x, y = t["x"], t["y"]
        tile = tiles[y][x]
        kind = tile.get("kind", "") if isinstance(tile, dict) else None
        op = t["act"][0]
        if op in ("WATER",):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op == "PLACE":
            return isinstance(tile, dict) and kind == "PASTURE" and "animal" not in tile
        if op == "PICKUP":
            return _shed_adjacent(units[ui][0], units[ui][1], board)
        return True

    units = [(fx, fy)] + [tuple(h) for h in hands]
    actions: List[List[str]] = []
    for ui, (ux, uy) in enumerate(units):
        chosen = None
        best_here = None
        for t in tasks:
            if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                continue
            if not executable(t, ui):
                continue
            if best_here is None or t["w"] > best_here["w"]:
                best_here = t
        if best_here is not None:
            chosen = best_here
        else:
            best = None
            for t in tasks:
                if t["key"] in claimed:
                    continue
                score = t["w"] / (1.0 + _dist(ux, uy, t["x"], t["y"]))
                if best is None or score > best[0]:
                    best = (score, t)
            chosen = best[1] if best else None
        if chosen is None:
            actions.append(["PASS"])
            continue
        claimed.add(chosen["key"])
        cx, cy = chosen["x"], chosen["y"]
        if (ux, uy) == (cx, cy):
            if executable(chosen, ui):
                actions.append(list(chosen["act"]))
            else:
                actions.append(_step_towards(ux, uy, sx, sy))
        else:
            actions.append(_step_towards(ux, uy, cx, cy))

    # seed-demote guard (engine blocks ALL plants of a crop on over-demand)
    demand = {}
    for a in actions:
        if a and a[0] == "PLANT":
            demand[a[1]] = demand.get(a[1], 0) + 1
    for crop, n in demand.items():
        if n > seeds.get(crop, 0):
            keep = seeds.get(crop, 0)
            for i, a in enumerate(actions):
                if a and a[0] == "PLANT" and a[1] == crop:
                    if keep > 0:
                        keep -= 1
                    else:
                        actions[i] = ["PASS"]

    # ---- market orders ----------------------------------------------------
    orders: List[list] = []
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    living = cows
    feed_need = 0 if last_day else living + 1
    if last_day:
        for item in ("MILK", "WHEAT", "FERTILIZER", "EGG", "WOOL"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])
    else:
        # milk through the gate (bounded tranche; shed-cap protection)
        if shed.get("MILK", 0) > 0:
            gate = MILK_GATE
            if shed_count >= 80:
                gate = 20
            if prices.get("MILK", 160) >= gate:
                orders.append(["SELL", "MILK", min(shed["MILK"], MILK_TRANCHE)])
        if shed.get("FERTILIZER", 0) > 0:
            orders.append(["SELL", "FERTILIZER", shed["FERTILIZER"]])
        reserve = feed_need + min(2, shed_cows)
        surplus = shed.get("WHEAT", 0) - reserve
        if surplus > 0:
            orders.append(["SELL", "WHEAT", surplus])
    # purchases
    if not last_day:
        if shed.get("WHEAT", 0) < feed_need and prices.get("WHEAT", 25) <= WHEAT_BUY_MAX_PRICE:
            orders.append(["BUY_PRODUCT", "WHEAT", feed_need - shed.get("WHEAT", 0) + 2])
        if seeds.get("WHEAT", 0) < 6 and day <= SEASON_DAYS - 6 and money >= 120:
            orders.append(["BUY_SEED", "WHEAT", 10])
        if cows + shed_cows < COW_CAP and money >= 400 + COW_RESERVE:
            orders.append(["BUY_ANIMAL", "COW", 1])
        if hour <= 2 and len(hands) < HANDS_TARGET and money >= 40:
            orders.append(["HIRE"])

    farmer = actions[0] if actions else ["PASS"]
    return {"farmer": farmer, "hands": actions[1:], "market": orders[:10]}
