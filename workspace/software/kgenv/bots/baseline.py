"""Baseline heuristic agents (two distinct styles) for local evaluation.

baseline_wheat_agent -- "wheat engine": full-tour wheat farming with 2 daily
    hands, NE land purchase, harvest-at-max-yield, dump-sell everything.
    This is the A/B comparator for the enhanced submission bot.

greedy_carrot_agent -- "carrot rush": carrot-only quick cycles with 1 hand,
    no land purchase; a deliberately different style for the opponent pool.

Both are pure functions of the observation (stateless per call) and share a
small tour-scheduling core: stand-on-tile -> act; otherwise walk toward the
highest-urgency unclaimed task.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

CROPS_INFO = {
    "WHEAT":  {"seed": 10, "first_yield_day": 2, "max_yield_day": 4,  "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT": {"seed": 20, "first_yield_day": 2, "max_yield_day": 3,  "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO": {"seed": 50, "first_yield_day": 8, "max_yield_day": 8,  "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":  {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS_INFO = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW": {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}

MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
SEASON_DAYS = 30


def _dist(ax: int, ay: int, bx: int, by: int) -> int:
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx: int, fy: int, tx: int, ty: int, board_size: int) -> List[str]:
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _tour_act(obs: Dict, crop: str, hire_hands: int, buy_land_at: Optional[int],
              max_plant_tiles: int) -> Dict:
    """Shared tour-scheduling core for the baseline styles."""
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
    seeds = private.get("seeds", {}) or {}
    shed = private.get("shed", {}) or {}
    fx, fy = farm.get("farmer", [board // 2 - 1] * 2)
    hands = farm.get("hands", []) or []
    crop_cfg = CROPS_INFO[crop]

    market: List[list] = []

    # ---- market layer -------------------------------------------------
    for item in ("WHEAT", "CARROT", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"):
        n = shed.get(item, 0)
        if n > 0:
            market.append(["SELL", item, n])
    want_tiles = min(max_plant_tiles, 25 if len(farm.get("unlocked_quadrants", [])) < 2 else 40)
    target_seeds = min(want_tiles, seeds.get(crop, 0) + 12)
    if seeds.get(crop, 0) < want_tiles and money >= crop_cfg["seed"] * 4 and \
            day <= SEASON_DAYS - 1 - crop_cfg["max_yield_day"]:
        market.append(["BUY_SEED", crop, min(12, max(1, want_tiles - seeds.get(crop, 0)))])
    if hour <= 1 and len(hands) < hire_hands and money >= 40:
        market.append(["HIRE"])
    if buy_land_at is not None and money >= buy_land_at and \
            len(farm.get("unlocked_quadrants", [])) < 4:
        market.append(["BUY_LAND"])

    # ---- build task list ----------------------------------------------
    tasks = []  # (weight, x, y, action_list, key)
    plants_alive = 0
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile is None:
                if seeds.get(crop, 0) > 0 and day <= SEASON_DAYS - 1 - crop_cfg["max_yield_day"]:
                    tasks.append((8.0, x, y, ["PLANT", crop], ("plant", x, y)))
            elif isinstance(tile, dict):
                if tile.get("kind") == "WEED":
                    tasks.append((12.0, x, y, ["DIG"], ("dig", x, y)))
                elif tile.get("kind") == "PLANT" and tile.get("crop") == crop:
                    plants_alive += 1
                    age = day - tile.get("planted_day", day)
                    if not tile.get("watered_today", False):
                        w = 60.0 if tile.get("consecutive_unwatered", 0) >= 1 else 40.0
                        tasks.append((w, x, y, ["WATER"], ("water", x, y)))
                    if tile.get("yield_units", 0) > 0 and (
                            (not crop_cfg["ongoing"] and age >= crop_cfg["max_yield_day"])
                            or (crop_cfg["ongoing"] and tile["yield_units"] >= 3)
                            or day >= SEASON_DAYS - 1):
                        tasks.append((55.0, x, y, ["HARVEST"], ("harvest", x, y)))
                elif "animal" in tile:
                    if not tile.get("fed_today", False) and shed.get("WHEAT", 0) + sum(
                            i.get("WHEAT", 0) for i in private.get("inventories", [])) > 0:
                        tasks.append((80.0, x, y, ["FEED"], ("feed", x, y)))
                    if tile.get("yield_units", 0) >= 3:
                        tasks.append((50.0, x, y, ["HARVEST"], ("harvest", x, y)))

    # hands need wheat in inventory to FEED; keep baseline simple: animals
    # only get fed if a unit carries wheat (BUY_PRODUCT path omitted here).

    # ---- schedule units -------------------------------------------------
    def schedule(ux: int, uy: int, claimed: set) -> List[str]:
        # act on current tile first
        for w, x, y, act, key in sorted(tasks, key=lambda t: -t[0]):
            if (x, y) == (ux, uy) and key not in claimed:
                claimed.add(key)
                return act
        # otherwise move to the best unclaimed task
        best = None
        for w, x, y, act, key in tasks:
            if key in claimed:
                continue
            score = w / (1.0 + _dist(ux, uy, x, y))
            if best is None or score > best[0]:
                best = (score, x, y, key)
        if best is None:
            return ["PASS"]
        _, tx, ty, key = best
        claimed.add(key)
        return _step_towards(ux, uy, tx, ty, board)

    claimed: set = set()
    farmer_action = schedule(fx, fy, claimed)
    hands_actions = [schedule(hx, hy, claimed) for hx, hy in hands]
    return {"farmer": farmer_action, "hands": hands_actions, "market": market[:10]}


def baseline_wheat_agent(obs: Dict) -> Dict:
    """Wheat engine: farmer + 2 hands, 12 tiles matched to watering capacity."""
    return _tour_act(obs, "WHEAT", hire_hands=2, buy_land_at=None, max_plant_tiles=12)


def greedy_carrot_agent(obs: Dict) -> Dict:
    """Carrot rush: 1 hand, no land, fast 4-day cycles, dump-sell."""
    return _tour_act(obs, "CARROT", hire_hands=1, buy_land_at=None, max_plant_tiles=18)
