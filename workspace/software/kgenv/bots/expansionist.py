"""Strong heuristic opponent: expansionist_agent -- "land grabber" (m1 wave 2).

Capital-expansion variant: grab every quadrant early (NE $1000 / SW $2000 /
SE $4000), re-hire a large daily crew (hands are cheap: fib costs 1,1,2,3,5,8
per day), and run an industrial WHEAT estate at labour scale.  A small
"goose court" (up to 6 coops by the shed) turns the estate self-fertilizing
(window waterings pay double -> 6 units per tile instead of 4) and funds
itself with eggs; the estate's own wheat feeds the court.  Wheat's log-shaped
glut curve keeps the price near base under heavy dumping, so it sells daily.

Distinct from the submission (compact 8-goose + melon-wave farm, one land
purchase) by scale, crop mix (no melons at all) and capital plan (all land,
max labour).

Stateless per call: f(obs) -> {"farmer": [...], "hands": [[...]],
"market": [[...]]}.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

CROPS_INFO = {
    "WHEAT": {"seed": 10, "first_yield_day": 2, "max_yield_day": 4,
              "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS_INFO = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4,
              "interval": 1, "max_held": 4, "product": "EGG"},
}

LAND_RESERVE = [2600, 4600, 7000]      # for NE(1000), SW(2000), SE(4000)
HANDS_BY_QUADS = {1: 3, 2: 5, 3: 6, 4: 7}
TILES_PER_UNIT = 3                     # sustainable wheat tiles per labourer
TILES_BASE = 4
GEESE_CAP = 6
GOOSE_RESERVE = 600
HIRE_UNTIL_HOUR = 4
SEASON_DAYS = 30


def _dist(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx: int, fy: int, tx: int, ty: int) -> List[str]:
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def expansionist_agent(obs: Dict) -> Dict:
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
    quads = len(farm.get("unlocked_quadrants", []) or ["NW"])
    last_day = day >= SEASON_DAYS - 1
    units = 1 + len(hands)

    h = board // 2
    sx, sy = h - 1, h - 1  # shed corner

    wheat_alive = 0
    geese = 0
    coops: List[Tuple[int, int]] = []
    empty: List[Tuple[int, int]] = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            if tile is None:
                empty.append((x, y))
            elif isinstance(tile, dict):
                k = tile.get("kind", "")
                if k == "COOP":
                    coops.append((x, y))
                    if "animal" in tile:
                        geese += 1
                elif k == "PLANT":
                    wheat_alive += 1
    empty.sort(key=lambda p: (_dist(sx, sy, p[0], p[1]), p[1], p[0]))

    tile_cap = TILES_BASE + TILES_PER_UNIT * units
    room = max(0, min(tile_cap - wheat_alive, len(empty)))
    shed_geese = shed.get("GOOSE", 0) + sum(
        (inv or {}).get("GOOSE", 0) for inv in inventories if inv)

    tasks: List[Dict] = []

    def add(w, x, y, act, key, need=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key,
                      "need": need})

    # ---- goose court: coops hug the shed ---------------------------------
    if not last_day:
        ring = [p for p in empty if _dist(sx, sy, p[0], p[1]) <= 2]
        for x, y in ring:
            if len(coops) >= GEESE_CAP:
                break
            add(44, x, y, ["BUILD_COOP"], ("bcoop", x, y))
            coops.append((x, y))

    # ---- estate planting (near-first) -------------------------------------
    estate = [p for p in empty if _dist(sx, sy, p[0], p[1]) >= 3]
    for x, y in estate[:room]:
        if seeds.get("WHEAT", 0) > 0 and day <= SEASON_DAYS - 6 and not last_day:
            add(42, x, y, ["PLANT", "WHEAT"], ("plant", x, y))

    # ---- per-tile tasks -----------------------------------------------------
    animals_to_feed = 0
    for x, y in coops:
        tile = tiles[y][x]
        if not isinstance(tile, dict) or "animal" not in tile:
            if shed_geese > 0:
                add(54, x, y, ["PLACE", "GOOSE"], ("place", x, y), need="GOOSE")
            continue
        if not last_day:
            if not tile.get("fed_today", False):
                animals_to_feed += 1
                w = 99 if tile.get("consecutive_unfed", 0) >= 1 else 89
                add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
            if day <= SEASON_DAYS - 2 and not tile.get("cared_today", False) \
                    and tile.get("fed_today", False):
                add(47, x, y, ["CARE"], ("care", x, y))
        if tile.get("yield_units", 0) >= 3 or (tile.get("yield_units", 0) > 0 and last_day):
            add(66, x, y, ["HARVEST"], ("harveste", x, y))
        if tile.get("fertilizer_available", False):
            add(40, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))

    fert_on_units = sum((inv or {}).get("FERTILIZER", 0)
                        for inv in inventories if inv)
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "WEED":
                add(24, x, y, ["DIG"], ("dig", x, y))
                continue
            if tile.get("kind") != "PLANT":
                continue
            age = day - tile.get("planted_day", day)
            if not last_day and not tile.get("watered_today", False):
                if tile.get("consecutive_unwatered", 0) >= 1:
                    add(98, x, y, ["WATER"], ("water", x, y))   # dies tonight
                elif 2 <= age <= 4:
                    add(48, x, y, ["WATER"], ("water", x, y))
            # fertilize the window once per cycle (doubles window waterings)
            if not last_day and 2 <= age <= 3 \
                    and tile.get("fertilized_until_day", -1) < day \
                    and shed.get("FERTILIZER", 0) + fert_on_units > 0:
                add(30, x, y, ["FERTILIZE"], ("fert", x, y), need="FERTILIZER")
            # harvest only after the age-4 window watering had its chance
            if tile.get("yield_units", 0) > 0 and (
                    age >= 5 or (age >= 4 and (tile.get("watered_today", False)
                                               or hour >= 20)) or last_day):
                add(74, x, y, ["HARVEST"], ("harvest", x, y))

    # ---- logistics: shed pickups -------------------------------------------
    wheat_on_units = sum((inv or {}).get("WHEAT", 0)
                         for inv in inventories if inv)
    if animals_to_feed > 0 and wheat_on_units == 0 and shed.get("WHEAT", 0) > 0:
        n = min(animals_to_feed + 1, shed.get("WHEAT", 0))
        add(96, sx, sy, ["PICKUP", "WHEAT", n], ("pickup_w", 0))
    geese_on_units = sum((inv or {}).get("GOOSE", 0)
                         for inv in inventories if inv)
    if shed.get("GOOSE", 0) > 0 and geese_on_units == 0 and \
            any(t["key"][0] == "place" for t in tasks):
        add(94, sx, sy, ["PICKUP", "GOOSE", min(2, shed.get("GOOSE", 0))],
            ("pickup_g", 0))
    if any(t["key"][0] == "fert" for t in tasks) and fert_on_units == 0 \
            and shed.get("FERTILIZER", 0) > 0:
        add(38, sx, sy, ["PICKUP", "FERTILIZER", 2], ("pickup_f", 0))

    # ---- schedule units ------------------------------------------------------
    claimed = set()

    def unit_inv(i: int) -> Dict:
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    def executable(t: Dict, ui: int, ux: int, uy: int) -> bool:
        need = t.get("need")
        if need and unit_inv(ui).get(need, 0) <= 0:
            return False
        tile = tiles[t["y"]][t["x"]]
        kind = tile.get("kind", "") if isinstance(tile, dict) else None
        op = t["act"][0]
        if op == "WATER":
            return kind == "PLANT" and not tile.get("watered_today", False)
        if op == "FERTILIZE":
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" and tile.get("yield_units", 0) > 0 or \
                (isinstance(tile, dict) and "animal" in tile and
                 tile.get("yield_units", 0) > 0)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op == "BUILD_COOP":
            return tile is None
        if op == "PLACE":
            return isinstance(tile, dict) and kind == "COOP" and "animal" not in tile
        if op == "PICKUP":
            return (ux, uy) in ((h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h))
        return True

    unit_list = [(fx, fy)] + [tuple(p) for p in hands]
    actions: List[List[str]] = []
    for ui, (ux, uy) in enumerate(unit_list):
        chosen = None
        best_here = None
        for t in tasks:
            if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                continue
            if not executable(t, ui, ux, uy):
                continue
            if best_here is None or t["w"] > best_here["w"]:
                best_here = t
        if best_here is not None:
            chosen = best_here
        else:
            best: Optional[Tuple[float, Dict]] = None
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
        if (ux, uy) == (chosen["x"], chosen["y"]):
            if executable(chosen, ui, ux, uy):
                actions.append(list(chosen["act"]))
            else:
                # standing on it but missing the carried item -> fetch at shed
                actions.append(_step_towards(ux, uy, sx, sy))
        else:
            actions.append(_step_towards(ux, uy, chosen["x"], chosen["y"]))

    # seed-demote guard (engine blocks ALL plants of a crop on over-demand)
    demand = 0
    for a in actions:
        if a and a[0] == "PLANT":
            demand += 1
    if demand > seeds.get("WHEAT", 0):
        keep = seeds.get("WHEAT", 0)
        for i, a in enumerate(actions):
            if a and a[0] == "PLANT":
                if keep > 0:
                    keep -= 1
                else:
                    actions[i] = ["PASS"]

    # ---- market orders ---------------------------------------------------------
    orders: List[list] = []
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    feed_need = 0 if last_day else geese + 1
    if last_day:
        for item in ("WHEAT", "EGG", "FERTILIZER"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])
    else:
        surplus = shed.get("WHEAT", 0) - feed_need
        if surplus > 0:
            orders.append(["SELL", "WHEAT", surplus])
        if shed.get("EGG", 0) > 0:
            orders.append(["SELL", "EGG", shed["EGG"]])
        fert_floor = 20 if shed_count >= 80 else 60
        if shed.get("FERTILIZER", 0) > 2 and \
                prices.get("FERTILIZER", 100) >= fert_floor:
            orders.append(["SELL", "FERTILIZER", shed["FERTILIZER"] - 2])
    if not last_day:
        # land only when labour-saturated and cash clears price + reserve
        extra = quads - 1
        if extra < 3 and money >= LAND_RESERVE[extra] \
                and wheat_alive + 3 >= tile_cap:
            orders.append(["BUY_LAND"])
        if shed.get("WHEAT", 0) < feed_need and \
                prices.get("WHEAT", 25) <= 40:
            orders.append(["BUY_PRODUCT", "WHEAT",
                           feed_need - shed.get("WHEAT", 0) + 2])
        if seeds.get("WHEAT", 0) < 12 and money >= 200 and day <= SEASON_DAYS - 6:
            orders.append(["BUY_SEED", "WHEAT", 24])
        if geese + shed_geese < GEESE_CAP and day >= 1 \
                and money >= 300 + GOOSE_RESERVE:
            orders.append(["BUY_ANIMAL", "GOOSE", 1])
        hands_target = HANDS_BY_QUADS.get(quads, 7)
        if hour <= HIRE_UNTIL_HOUR and len(hands) < hands_target and money >= 40:
            orders.append(["HIRE"])

    farmer = actions[0] if actions else ["PASS"]
    return {"farmer": farmer, "hands": actions[1:], "market": orders[:10]}
