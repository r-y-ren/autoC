"""Strong heuristic opponent: melon_hoarder_agent -- "melon wave bandit"
(m1 wave 2).

Market-rhythm variant of the melon-wave family: NO animals at all, 12-tile
melon waves (double the submission's 6) plus a small wheat base for cash
flow.  Melons are hoarded and only sold when the shared market price clears
a high gate, in bounded tranches sized for the quadratic melon glut curve;
a second wave goes in on days 13-16 only while the price still holds.
Day 29 liquidates everything.

Stateless per call: f(obs) -> {"farmer": [...], "hands": [[...]],
"market": [[...]]}.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

CROPS_INFO = {
    "WHEAT": {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "MELON": {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}

MELON_TILES = 12          # wave size (the submission plants 6)
WHEAT_TILES = 8           # cash-flow base
MELON_GATE = 190          # hoard below this price (submission gates at 150)
MELON_TRANCHE = 20        # bounded dump per triggered day
WAVE2_GATE = 170          # second wave only while the price still holds
HANDS_TARGET = 3
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


def melon_hoarder_agent(obs: Dict) -> Dict:
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
    prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
    fx, fy = farm.get("farmer", [board // 2 - 1] * 2)
    hands = farm.get("hands", []) or []
    last_day = day >= SEASON_DAYS - 1
    melon_price = prices.get("MELON", 250)

    melons_alive = 0
    wheat_alive = 0
    empty: List[Tuple[int, int]] = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            if tile is None:
                empty.append((x, y))
            elif isinstance(tile, dict) and tile.get("kind") == "PLANT":
                if tile.get("crop") == "MELON":
                    melons_alive += 1
                else:
                    wheat_alive += 1

    h = board // 2
    sx, sy = h - 1, h - 1
    empty.sort(key=lambda p: (_dist(sx, sy, p[0], p[1]), p[1], p[0]))

    # wave plan: wave 1 days 0-2, wave 2 days 13-16 while the price holds
    wave_open = (day <= 2) or (13 <= day <= 16 and melon_price >= WAVE2_GATE)
    melon_room = (MELON_TILES - melons_alive) if wave_open else 0
    wheat_room = WHEAT_TILES - wheat_alive

    tasks: List[Dict] = []

    def add(w, x, y, act, key):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key})

    for x, y in empty:
        if melon_room > 0 and seeds.get("MELON", 0) > 0 and not last_day:
            add(40, x, y, ["PLANT", "MELON"], ("plantm", x, y))
            melon_room -= 1
        elif wheat_room > 0 and seeds.get("WHEAT", 0) > 0 \
                and day <= SEASON_DAYS - 6 and not last_day:
            add(26, x, y, ["PLANT", "WHEAT"], ("plant", x, y))
            wheat_room -= 1

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if not isinstance(tile, dict):
                continue
            if tile.get("kind") == "WEED":
                add(22, x, y, ["DIG"], ("dig", x, y))
                continue
            if tile.get("kind") != "PLANT":
                continue
            crop = tile.get("crop", "")
            if crop not in CROPS_INFO:
                continue
            cd = CROPS_INFO[crop]
            age = day - tile.get("planted_day", day)
            if not last_day and not tile.get("watered_today", False):
                if tile.get("consecutive_unwatered", 0) >= 1:
                    add(98, x, y, ["WATER"], ("water", x, y))
                elif crop == "MELON":
                    if 2 <= age <= 12:
                        add(44, x, y, ["WATER"], ("water", x, y))
                else:  # wheat: yield window ages 2..4
                    if 2 <= age <= 4:
                        add(34, x, y, ["WATER"], ("water", x, y))
            yu = tile.get("yield_units", 0)
            if yu > 0:
                if crop == "MELON":
                    # hold through the whole window, harvest at the end
                    if age >= 12 or last_day:
                        add(76, x, y, ["HARVEST"], ("harvest", x, y))
                else:
                    if age >= 4 or last_day:
                        add(72, x, y, ["HARVEST"], ("harvest", x, y))

    # ---- schedule units ----------------------------------------------------
    claimed = set()
    units = [(fx, fy)] + [tuple(p) for p in hands]

    def executable(t: Dict, ux: int, uy: int) -> bool:
        tile = tiles[t["y"]][t["x"]]
        kind = tile.get("kind", "") if isinstance(tile, dict) else None
        op = t["act"][0]
        if op == "WATER":
            return kind == "PLANT" and not tile.get("watered_today", False)
        if op == "HARVEST":
            return kind == "PLANT" and tile.get("yield_units", 0) > 0
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        return True

    actions: List[List[str]] = []
    for ux, uy in units:
        chosen = None
        best_here = None
        for t in tasks:
            if t["key"] in claimed or (t["x"], t["y"]) != (ux, uy):
                continue
            if not executable(t, ux, uy):
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
        if (ux, uy) == (chosen["x"], chosen["y"]):
            actions.append(list(chosen["act"]))
        else:
            actions.append(_step_towards(ux, uy, chosen["x"], chosen["y"]))

    # seed-demote guard
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

    # ---- market orders ------------------------------------------------------
    orders: List[list] = []
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    if last_day:
        for item in ("MELON", "WHEAT", "FERTILIZER", "EGG"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])
    else:
        # the hoard: sell melons only above the gate, in bounded tranches;
        # force-sell when the shed approaches the 100-item discard cliff
        if shed.get("MELON", 0) > 0:
            gate = MELON_GATE
            if shed_count >= 80:
                gate = 20
            if melon_price >= gate:
                orders.append(["SELL", "MELON", min(shed["MELON"], MELON_TRANCHE)])
        if shed.get("WHEAT", 0) > 2:
            orders.append(["SELL", "WHEAT", shed["WHEAT"] - 2])
    if not last_day:
        if wave_open and seeds.get("MELON", 0) < MELON_TILES - melons_alive \
                and money >= 80 * MELON_TILES:
            orders.append(["BUY_SEED", "MELON",
                           MELON_TILES - melons_alive - seeds.get("MELON", 0)])
        if seeds.get("WHEAT", 0) < 6 and day <= SEASON_DAYS - 6 and money >= 120:
            orders.append(["BUY_SEED", "WHEAT", 10])
        if hour <= 2 and len(hands) < HANDS_TARGET and money >= 40:
            orders.append(["HIRE"])

    farmer = actions[0] if actions else ["PASS"]
    return {"farmer": farmer, "hands": actions[1:], "market": orders[:10]}
