"""Kaggriculture submission agent -- "goose engine + melon wave" strategy.

Self-contained: standard library only, no imports from the local kgenv
package, so the file uploads as-is to
    kaggle competitions submit kaggriculture -f main.py
and lives at /kaggle_simulations/agent/main.py (official kit convention).
The last callable defined in this file is the entry point (that is how
kaggle_environments picks the agent from a file).

Strategy summary (every mechanic from the official How-to-Play / engine):
  1. Goose engine: geese close to the shed; FEED daily (wheat), CARE daily
     (banks +1 egg per fed-and-cared day -> doubles daily output), collect
     the 1 fertilizer every animal produces per day, harvest eggs at >=3
     unharvested units. Eggs and fertilizer sit on glut-tolerant price
     curves (log above-target 0.2), so they can be sold daily.
  2. Melon wave: 6 melon tiles seeded on days 0-2, watered through the
     bonus window (ages 6-12), harvested day 12-13 and sold in gated
     tranches (premium curve crashes to $1 on glut). Optional second wave
     days 13-16 only while the melon price is still >= 180.
  3. Wheat base: remaining tiles grow wheat (feed + cash); harvest at
     max_yield_day; sell only the surplus above the feed reserve.
  4. Labour: hire hands each morning while marginal cost < plan load;
     buy NE land early (more wheat), SW/SE when rich.
  5. Endgame: from day 28 stop CARE (bank pays next production), day 29
     liquidate everything -- only bank money counts.

An OPTIONAL pluggable LLM consultant hook (LLM_PROVIDER, default None) is
provided for local A/B experiments only. Per the competition rules
(captured 2026-08-28): external models are permitted ("The use of external
data and models is acceptable unless specifically prohibited by the Host")
and modest LLM subscription costs pass the Reasonableness Standard. The
hook is disabled by default and never blocks: any provider failure falls
back to the heuristic decision.
"""

# --------------------------------------------------------------------------
# Embedded game constants (mirror of kaggle-environments 1.32.7 kaggriculture)
# --------------------------------------------------------------------------
CROPS = {
    "WHEAT":      {"seed": 10, "first_yield_day": 2, "max_yield_day": 4, "interval": 0, "max_yield": 6, "ongoing": False},
    "CARROT":     {"seed": 20, "first_yield_day": 2, "max_yield_day": 3, "interval": 0, "max_yield": 4, "ongoing": False},
    "TOMATO":     {"seed": 50, "first_yield_day": 8, "max_yield_day": 8, "interval": 1, "max_yield": 4, "ongoing": True},
    "STRAWBERRY": {"seed": 100, "first_yield_day": 10, "max_yield_day": 10, "interval": 2, "max_yield": 4, "ongoing": True},
    "MELON":      {"seed": 80, "first_yield_day": 10, "max_yield_day": 12, "interval": 0, "max_yield": 6, "ongoing": False},
}
ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP", "first_yield_day": 4, "interval": 1, "max_held": 4, "product": "EGG"},
    "COW":   {"cost": 400, "structure": "PASTURE", "first_yield_day": 8, "interval": 2, "max_held": 6, "product": "MILK"},
    "SHEEP": {"cost": 500, "structure": "PASTURE", "first_yield_day": 6, "interval": 3, "max_held": 6, "product": "WOOL"},
}
BASE_PRICE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
              "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}

MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
SEASON_DAYS = 30
GEESE_CAP = 8
MELON_WAVE_TILES = 6
PREMIUM_GATE = {"MELON": 150, "STRAWBERRY": 78, "MILK": 104, "WOOL": 130}  # ~0.6x base
LLM_PROVIDER = None  # optional consultant, default off; local experiments only

# Module-level state keyed by player id (the framework may exec one copy of
# this file for both seats in self-play validation episodes).
_STATE = {}


def _get(obj, key, default):
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _dist(ax, ay, bx, by):
    return abs(ax - bx) + abs(ay - by)


def _step_towards(fx, fy, tx, ty):
    dx, dy = tx - fx, ty - fy
    if dx == 0 and dy == 0:
        return ["PASS"]
    if abs(dx) >= abs(dy) and dx != 0:
        return ["EAST"] if dx > 0 else ["WEST"]
    return ["SOUTH"] if dy > 0 else ["NORTH"]


def _shed_adjacent(x, y, board_size):
    half = board_size // 2
    return (x, y) in ((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half))


def _window(crop):
    cd = CROPS[crop]
    return (cd["max_yield_day"] + 1) // 2, cd["max_yield_day"]


def _geese_target(day):
    return min(GEESE_CAP, day + 2) if day <= GEESE_CAP - 2 else GEESE_CAP


def _hands_target(day, load_tiles):
    if day == 0:
        return 1
    if load_tiles <= 18:
        return 2
    if load_tiles <= 26:
        return 3
    return 4


def _llm_sell_gate(item, price, base_gate, context):
    """Optional LLM consultation for premium sell timing; default heuristic.

    The provider (if any) must answer with {"gate": int}. Any failure or
    absurd answer falls back to the heuristic gate. Never blocks the turn:
    providers are expected to enforce their own call budget/timeout
    (Reasonableness Standard).
    """
    if LLM_PROVIDER is None:
        return base_gate
    try:
        ans = LLM_PROVIDER.suggest(
            f"Item {item} trades at {price} (base {BASE_PRICE[item]}). "
            f"Return the minimum price we should accept for selling into a "
            f"glut-crashing market, as JSON {{\"gate\": int}}.", context)
        gate = int(_get(ans or {}, "gate", base_gate))
        if 1 <= gate <= BASE_PRICE[item] * 2:
            return gate
    except Exception:
        pass
    return base_gate


def _plan_tiles(farm, day, melon_price):
    """Deterministic tile allocation: goose zone nearest the shed, then
    melon wave tiles, then wheat on the rest.

    Returns (goose_set, melon_set, wheat_set, n_animals, load).  goose_set
    includes existing structures plus the empty tiles where new coops are
    still wanted (so BUILD_COOP tasks can be raised on them).
    """
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    half = board // 2
    cx = cy = half - 1  # main spawn / shed corner of NW quadrant

    unlocked = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile != "LOCKED":
                unlocked.append((x, y, tile))
    unlocked.sort(key=lambda t: (_dist(cx, cy, t[0], t[1]), t[1], t[0]))

    goose_set, melon_set, wheat_set = set(), set(), set()
    empty = []
    n_structures = 0      # coops/pastures on the ground (occupied or not)
    n_animals = 0         # living placed animals
    n_melon_planted = 0
    for x, y, tile in unlocked:
        if tile is None:
            empty.append((x, y))
            continue
        if not isinstance(tile, dict):
            continue
        k = _get(tile, "kind", "")
        if k == "WEED":
            continue  # handled as tasks when they sit in an allocated zone
        if k in ("COOP", "PASTURE"):
            n_structures += 1
            goose_set.add((x, y))
            if "animal" in tile:
                n_animals += 1
        elif k == "PLANT":
            if _get(tile, "crop", "") == "MELON":
                melon_set.add((x, y))
                n_melon_planted += 1
            else:
                wheat_set.add((x, y))

    geese_t = _geese_target(day)
    melon_t = n_melon_planted
    if day <= 2:
        melon_t = MELON_WAVE_TILES
    elif 13 <= day <= 16 and melon_price >= 180 and n_melon_planted < MELON_WAVE_TILES:
        melon_t = n_melon_planted + MELON_WAVE_TILES  # second wave while price holds
    for x, y in empty:
        if len(goose_set) < geese_t:
            goose_set.add((x, y))       # coop still wanted here
        elif len(melon_set) < melon_t:
            melon_set.add((x, y))
        else:
            wheat_set.add((x, y))
    load = len(goose_set) + len(melon_set) + min(len(wheat_set), 16)
    return goose_set, melon_set, wheat_set, n_animals, load


def _build_tasks(obs, farm, private, day):
    """Return list of dicts: {w, x, y, act, key} for unit scheduling."""
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    melon_price = _get(_get(obs, "market", {}) or {}, "prices", {}).get("MELON", 250)
    goose_set, melon_set, wheat_set, n_animals, load = _plan_tiles(farm, day, melon_price)
    seeds = _get(private, "seeds", {}) or {}
    shed = _get(private, "shed", {}) or {}
    inventories = _get(private, "inventories", []) or []
    wheat_on_units = sum(_get(inv, "WHEAT", 0) for inv in inventories if inv)
    geese_on_units = sum(_get(inv, "GOOSE", 0) for inv in inventories if inv)
    fert_on_units = sum(_get(inv, "FERTILIZER", 0) for inv in inventories if inv)
    animals_to_feed = 0

    tasks = []

    def add(w, x, y, act, key, need=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key, "need": need})

    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if pos in goose_set and day <= GEESE_CAP + 1:
                    add(42, x, y, ["BUILD_COOP"], ("build", x, y))
                elif pos in melon_set and seeds.get("MELON", 0) > 0 and day <= 16:
                    add(30, x, y, ["PLANT", "MELON"], ("plantm", x, y))
                elif pos in wheat_set and seeds.get("WHEAT", 0) > 0 and day <= 25:
                    add(26, x, y, ["PLANT", "WHEAT"], ("plant", x, y))
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                if pos in melon_set or pos in wheat_set or pos in goose_set:
                    add(22, x, y, ["DIG"], ("dig", x, y))
                continue
            if kind == "PLANT":
                crop = _get(tile, "crop", "")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                age = day - _get(tile, "planted_day", day)
                yu = _get(tile, "yield_units", 0)
                ws, we = _window(crop)
                in_window = ws <= age <= we
                if not _get(tile, "watered_today", False):
                    if _get(tile, "consecutive_unwatered", 0) >= 1:
                        add(100, x, y, ["WATER"], ("water", x, y))          # dies tonight
                    elif cd["ongoing"] or (in_window and yu < cd["max_yield"]) or age % 2 == 1:
                        add(34 if in_window else 24, x, y, ["WATER"], ("water", x, y))
                if yu > 0:
                    if not cd["ongoing"] and age >= cd["max_yield_day"]:
                        add(72, x, y, ["HARVEST"], ("harvest", x, y))
                    elif cd["ongoing"] and (yu >= 3 or day >= SEASON_DAYS - 1):
                        add(70, x, y, ["HARVEST"], ("harvest", x, y))
                if crop == "MELON" and 3 <= age <= 6 and _get(tile, "fertilized_until_day", -1) < day:
                    add(28, x, y, ["FERTILIZE"], ("fert", x, y), need="FERTILIZER")
            elif "animal" in tile:
                animal = _get(tile, "animal", "")
                a = ANIMALS.get(animal)
                if not a:
                    continue
                if not _get(tile, "fed_today", False):
                    animals_to_feed += 1
                    w = 98 if _get(tile, "consecutive_unfed", 0) >= 1 else 88
                    add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
                if day <= SEASON_DAYS - 2 and not _get(tile, "cared_today", False) \
                        and _get(tile, "fed_today", False):
                    add(46, x, y, ["CARE"], ("care", x, y))
                yu = _get(tile, "yield_units", 0)
                if yu >= 3 or (yu > 0 and day >= SEASON_DAYS - 1):
                    add(66, x, y, ["HARVEST"], ("harvest", x, y))
                if _get(tile, "fertilizer_available", False):
                    add(36, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))
            elif kind in ("COOP", "PASTURE") and "animal" not in tile:
                if shed.get("GOOSE", 0) + geese_on_units > 0:
                    add(54, x, y, ["PLACE", "GOOSE"], ("place", x, y), need="GOOSE")

    board_half = board // 2
    shed_tile = (board_half - 1, board_half - 1)
    # feed logistics: someone must carry wheat from the shed
    if animals_to_feed > 0 and wheat_on_units == 0 and shed.get("WHEAT", 0) > 0:
        n = min(animals_to_feed + 1, shed.get("WHEAT", 0))
        add(96, shed_tile[0], shed_tile[1], ["PICKUP", "WHEAT", n], ("pickup_w", 0))
    # goose logistics: carry bought geese onto empty coops
    if shed.get("GOOSE", 0) > 0 and geese_on_units < 3 and \
            any(t["key"][0] == "place" for t in tasks):
        add(94, shed_tile[0], shed_tile[1], ["PICKUP", "GOOSE", min(3, shed.get("GOOSE", 0))],
            ("pickup_g", 0))
    # fertilizer logistics for the melon fertilize task
    if any(t["key"][0] == "fert" for t in tasks) and shed.get("FERTILIZER", 0) > 0 \
            and fert_on_units == 0:
        add(38, shed_tile[0], shed_tile[1], ["PICKUP", "FERTILIZER", 2], ("pickup_f", 0))
    # mid-day drop when carrying a lot (protects against end-of-day discard)
    return tasks, animals_to_feed, load


def _market_orders(obs, farm, private, day, animals_to_feed):
    money = _get(farm, "money", 0.0)
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    quads = len(_get(farm, "unlocked_quadrants", []) or ["NW"])
    geese_structures = 0
    living_animals = 0
    tiles = _get(farm, "tiles", [])
    for row in tiles:
        for tile in row:
            if isinstance(tile, dict):
                k = _get(tile, "kind", "")
                if k in ("COOP", "PASTURE"):
                    geese_structures += 1
                    if "animal" in tile:
                        living_animals += 1
    orders = []

    # ---------------- selling ----------------
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    last_day = day >= SEASON_DAYS - 1
    geese_in_transit = shed.get("GOOSE", 0) + sum(
        _get(inv, "GOOSE", 0) for inv in (_get(private, "inventories", []) or []) if inv)
    wheat_reserve = 0 if last_day else (living_animals + min(2, geese_in_transit) + 1)
    wheat_surplus = shed.get("WHEAT", 0) - wheat_reserve
    if wheat_surplus > 0 and (last_day or prices.get("WHEAT", 25) >= 12):
        orders.append(["SELL", "WHEAT", wheat_surplus])
    for item in ("EGG", "FERTILIZER"):
        if shed.get(item, 0) > 0:
            orders.append(["SELL", item, shed[item]])
    if not last_day:
        for item, base_gate in PREMIUM_GATE.items():
            n = shed.get(item, 0)
            if n <= 0:
                continue
            gate = _llm_sell_gate(item, prices.get(item, BASE_PRICE[item]), base_gate,
                                  {"day": day, "shed": n})
            if shed_count >= 85:
                gate = min(gate, 20)  # protect against the 100-item discard cliff
            if prices.get(item, BASE_PRICE[item]) >= gate:
                orders.append(["SELL", item, min(n, 14)])
    else:
        for item in ("MELON", "STRAWBERRY", "MILK", "WOOL", "CARROT", "TOMATO"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])

    # ---------------- buying ----------------
    # feed deficit: buy wheat at the market when our own stock comes short
    if animals_to_feed > shed.get("WHEAT", 0) and not last_day \
            and prices.get("WHEAT", 25) <= 45:
        orders.append(["BUY_PRODUCT", "WHEAT", animals_to_feed - shed.get("WHEAT", 0) + 2])
    # seeds
    if seeds.get("WHEAT", 0) < 6 and day <= SEASON_DAYS - 6 and money >= 120:
        orders.append(["BUY_SEED", "WHEAT", 8])
    if day <= 2 and seeds.get("MELON", 0) < MELON_WAVE_TILES and money >= 480:
        orders.append(["BUY_SEED", "MELON", MELON_WAVE_TILES - seeds.get("MELON", 0)])
    elif 13 <= day <= 15 and seeds.get("MELON", 0) == 0 and \
            prices.get("MELON", 250) >= 180 and money >= 900:
        orders.append(["BUY_SEED", "MELON", MELON_WAVE_TILES])
    # geese
    geese_t = _geese_target(day)
    geese_have = geese_structures  # structures ~= geese managed (empty ones refill)
    if geese_have + shed.get("GOOSE", 0) < geese_t and money >= 300 + 500 and not last_day:
        orders.append(["BUY_ANIMAL", "GOOSE", 1])
    # labour: HIRE is decided at the call site against the hands plan
    # land: NE early, SW mid, SE late
    if quads < 2 and money >= 2600 and day >= 3:
        orders.append(["BUY_LAND"])
    elif quads < 3 and money >= 5000 and day >= 10:
        orders.append(["BUY_LAND"])
    elif quads < 4 and money >= 8500 and day >= 16:
        orders.append(["BUY_LAND"])
    return orders


def _schedule_units(obs, farm, private, day, tasks):
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    units = [tuple(_get(farm, "farmer", [board // 2 - 1, board // 2 - 1]))]
    for h in _get(farm, "hands", []) or []:
        units.append(tuple(h))
    inventories = _get(private, "inventories", []) or []

    def unit_inv(i):
        while len(inventories) <= i:
            inventories.append({})
        return inventories[i]

    claimed = set()
    actions = []

    def executable(task, ui):
        need = task.get("need")
        if need and _get(unit_inv(ui), need, 0) <= 0:
            return False
        x, y = task["x"], task["y"]
        tile = tiles[y][x]
        kind = _get(tile, "kind", "") if isinstance(tile, dict) else None
        act = task["act"]
        op = act[0]
        if op in ("WATER", "FERTILIZE"):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op == "FEED":
            return isinstance(tile, dict) and "animal" in tile
        if op == "CARE":
            return isinstance(tile, dict) and "animal" in tile
        if op == "COLLECT_FERTILIZER":
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op == "BUILD_COOP":
            return tile is None
        if op == "PLACE":
            return isinstance(tile, dict) and _get(tile, "kind", "") == "COOP" \
                and "animal" not in tile
        if op == "PICKUP":
            return _shed_adjacent(units[ui][0], units[ui][1], board)
        return True

    for ui, (ux, uy) in enumerate(units):
        chosen = None
        # 1) act on the current tile (highest weight executable here)
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
            # 2) walk toward the best unclaimed task this unit can eventually do
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
                # standing on it but missing the carried item -> fetch at shed
                half = board // 2
                sx, sy = half - 1, half - 1
                actions.append(_step_towards(ux, uy, sx, sy))
        else:
            actions.append(_step_towards(ux, uy, cx, cy))

    # R6 guard: never request more PLANTs of a crop than seeds held
    seeds = _get(private, "seeds", {}) or {}
    demand = {}
    for a in actions:
        if a and a[0] == "PLANT":
            demand[a[1]] = demand.get(a[1], 0) + 1
    for crop, n in demand.items():
        if n > seeds.get(crop, 0):
            # keep only the first `seeds` plant orders, demote the rest
            keep = seeds.get(crop, 0)
            for i, a in enumerate(actions):
                if a and a[0] == "PLANT" and a[1] == crop:
                    if keep > 0:
                        keep -= 1
                    else:
                        actions[i] = ["PASS"]
    return actions


def agent(obs):
    """Entry point: one action dict per turn (official Quick-Start signature)."""
    try:
        player = _get(obs, "player", 0)
        farms = _get(obs, "farms", [])
        if not farms or player >= len(farms):
            return {"farmer": ["PASS"], "hands": [], "market": []}
        farm = farms[player]
        private = _get(obs, "private", {}) or {}
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        tiles = _get(farm, "tiles", [])
        if not tiles:
            return {"farmer": ["PASS"], "hands": [], "market": []}

        tasks, animals_to_feed, load = _build_tasks(obs, farm, private, day)
        actions = _schedule_units(obs, farm, private, day, tasks)
        orders = _market_orders(obs, farm, private, day, animals_to_feed)

        # HIRE only while below the plan's hand count (strip the placeholder)
        orders = [o for o in orders if o[0] != "HIRE"]
        hands = _get(farm, "hands", []) or []
        hands_t = _hands_target(day, load)
        money = _get(farm, "money", 0.0)
        if hour <= 2 and len(hands) < hands_t and money >= 40:
            orders.append(["HIRE"])

        farmer = actions[0] if actions else ["PASS"]
        hands_actions = actions[1:]
        return {"farmer": farmer, "hands": hands_actions, "market": orders[:10]}
    except Exception:
        # a submission must never crash: fall back to a safe legal action
        return {"farmer": ["PASS"], "hands": [], "market": []}
