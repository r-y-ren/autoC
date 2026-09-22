"""Kaggriculture submission agent -- "dairy engine" strategy (m2, v2).

Self-contained: standard library only, no imports from the local kgenv
package, so the file uploads as-is to
    kaggle competitions submit kaggriculture -f main.py
and lives at /kaggle_simulations/agent/main.py (official kit convention).
The last callable defined in this file is the entry point (that is how
kaggle_environments picks the agent from a file).

Failure-mode-driven redesign (evidence: exports/failure_modes.md, m1 wave 2):

  FM-1 (cow_baron's dairy out-earns the goose engine) -> the animal engine
      is COWS, not geese.  Unit economics per structure tile (official
      constants): a cared cow pays 3 milk / 2 days = 1.5/day vs a cared
      goose's 2 eggs/day; at the observed gated milk prices (>=130, base
      160) a cow earns 195-375/day vs a goose's ~100/day, on the same
      feed (1 wheat/day) and the same daily labour slots.  The herd ramps
      early (money-gated), is capped by feed capacity, and pastures hug
      the shed ring in every unlocked quadrant so FEED/CARE walking stays
      cheap.  Land purchases (NE/SW/SE) add ring pastures + wheat.
  FM-2 (second melon wave locked out by an opponent's day-15 dump) ->
      NO melon replant branch exists any more: mid-/late-season tile
      allocation is exclusively wheat (feed for cows) because wheat sits
      on a glut-tolerant log curve and cannot be strategically crashed,
      while MELON has zero shop consumption and a quadratic glut curve.
      Premium exposure lives in MILK, which three shop types + the town
      center consume daily, sold through explicit gates (below).
  FM-3 (capital-heavy opening) -> wheat goes in FIRST (day 0) so the
      feed pipeline exists before animals scale; cow purchases are staged
      by a money gate that always keeps a cash reserve for seeds/feed;
      shed wheat shortfalls trigger bounded BUY_PRODUCT top-ups.
  FM-4 (shared fertilizer decay) -> fertilizer is partly self-consumed
      (fertilizing wheat at age 2 turns 4-unit tiles into 6-unit tiles,
      i.e. converts a decaying commodity into feed capacity) and partly
      sold through a price gate with a stock cap (hoard bounded so the
      higher-value milk hoard keeps the shed's 100 slots).

Selective-intervention sell gates (methodology transfer of
arxiv-2608.15291: decide explicitly WHEN to hoard, WHEN to release and
WHEN to defend the price, instead of dumping on a fixed schedule):
see _market_gates() -- every rule is commented with its curve rationale.

An OPTIONAL pluggable LLM consultant hook (LLM_PROVIDER, default None) is
provided for local A/B experiments only. Per the competition rules
(captured 2026-08-28): external models are permitted ("The use of external
data and models is acceptable unless specifically prohibited by the Host")
and modest LLM subscription costs pass the Reasonableness Standard. The
hook is disabled by default and never blocks: any provider failure falls
back to the heuristic gate.
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

# ---- strategy knobs (all values trace to curve/economy analysis in the
# module docstring; tuning changes are logged in the iteration gate log) ----
HERD_CAP = 10            # H10 VARIANT: labour ceiling probe
COW_BUY_RESERVE = 380    # cash kept besides a cow purchase (seeds+feed+hires)
COW_BUY_LAST_DAY = 20    # later cows never reach a production day in time
PASTURE_RING = 2         # pastures within manhattan dist <= 2 of shed access
WHEAT_FEED_RESERVE = 4   # days of feed kept in the shed before selling wheat
WHEAT_BUY_MAX_PRICE = 65 # feed top-ups while wheat is not ruinous
FERT_GATE = 50           # fertilizer: hold below, release above
FERT_STOCK_CAP = 6       # hoard bound: shed slots belong to milk first
FERT_FIELD_RESERVE = 4   # keep some fertilizer for the wheat fields
LLM_PROVIDER = None      # optional consultant, default off; local A/B only

# Module-level state keyed by player id (the framework may exec one copy of
# this file for both seats in self-play validation episodes).  Tracks the
# per-day cow purchase pace so the cash reserve never races to zero during
# the pre-wheat/pre-milk opening (FM-3).
_STATE = {}


def _buy_pace(player, day, hour):
    """Cows bought today so far (resets on day rollover / new episode).

    Observation clock is strictly increasing within an episode, so a
    non-increasing (day, hour) read means a fresh episode started in the
    same process (local eval runs many games on one module instance).
    """
    st = _STATE.get(player)
    if st is None or st["day"] != day:
        return 0
    if hour <= st.get("hour", -1):
        _STATE.pop(player, None)
        return 0
    return st.get("cows_bought", 0)


def _note_buys(player, day, hour, n):
    st = _STATE.get(player)
    if st is None or st["day"] != day or hour <= st.get("hour", -1):
        st = {"day": day, "hour": hour, "cows_bought": 0}
        _STATE[player] = st
    st["hour"] = hour
    st["cows_bought"] = st.get("cows_bought", 0) + n


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


def _shed_access(board_size):
    half = board_size // 2
    return ((half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half))


def _shed_adjacent(x, y, board_size):
    return (x, y) in _shed_access(board_size)


def _quadrant_shed_tile(x, y, board_size):
    """The shed-access tile of the quadrant (x, y) sits in."""
    half = board_size // 2
    qx = half - 1 if x < half else half
    qy = half - 1 if y < half else half
    return (qx, qy)


def _window(crop):
    cd = CROPS[crop]
    return (cd["max_yield_day"] + 1) // 2, cd["max_yield_day"]


def _wheat_cap(day, wheat_price=25):
    """Field-size plan: the labour budget (farmer + <=5 hands, 24 turns)
    sustains roughly herd*3.5 + wheat*1.2 unit-actions/day; planting every
    unlocked tile starves FEED/CARE of walkers and cows escape (measured,
    iteration log).  16 tiles fund the opening, 18 the full herd (18 fertilized
tiles = 21.6 wheat/day vs 12 cows eating 12).
    """
    cap = 16 if day <= 2 else 18
    if day > 2 and wheat_price >= 35:
        cap += 4          # dear wheat: farm more of it (feed margin + cash)
    return min(cap, 24)


def _herd_target(day, feed_capacity):
    """Cow-count plan: ramp early, cap by feed capacity and labour.

    4 + day grows the plan one head per day (money gate paces the real
    purchases); feed_capacity = wheat tiles x 1.2 (fertilized wheat yields
    6 units / 5-day cycle) bounds it so feeding never outruns the fields.
    """
    return min(HERD_CAP, 4 + day, max(4, feed_capacity))


def _hands_target(day, herd, wheat_tiles):
    """Labour plan: farmer + hands; each cow costs ~3.5 unit-actions/day
    (FEED+CARE+COLLECT+harvest/2), each wheat tile ~1.2; 24 turns/day per
    unit; movement overhead ~35%."""
    load = herd * 3.5 + wheat_tiles * 1.2
    if day == 0:
        return 2
    return max(2, min(5, int(load / 13) + 1))


def _milk_gate(day):
    """Milk hold-threshold by day (selective intervention, see _market_gates).

    Base 105: in a joint-dairy market (both players milking ~20+/day vs
    town consumption of ~5/day, measured mirror prices 97-135) holding for
    higher bands just deferred sales into eventual pressure dumps (measured
    realized ~60/unit).  Clearing daily at >= 105 dominates: our engine
    out-produces cow_baron +22..32k solo, and the only way that edge
    survives the shared milk curve is never dumping below the band.
    Decay late-season: the day-29 liquidation floor is coming for everyone,
    so clearing inventory at a lower-but-positive gate beats holding into
    the joint dump.
    """
    if day >= 28:
        return 80
    if day >= 26:
        return 90
    if day >= 24:
        return 100
    return 105


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


def _market_gates(day, prices, shed, herd):
    """Selective-intervention sell decisions: what to SELL this turn, with
    the hoard / release / defend rule per item made explicit.

    Curve rationale (official MARKET_PARAMS, kaggriculture.py):
      * MILK base 160: above-target glut is LINEAR (~2.1 coins lost per
        unit dumped above I0) and three shop types + the town center
        consume milk daily -> holding is safe, dumping is punished
        moderately, and price recovers through town consumption.
          - HOARD while price < gate (_milk_gate by day; LLM may advise).
          - RELEASE in bounded tranches at/above the gate; tranche size is
            elastic to observed scarcity (deep scarcity -> bigger tranche).
          - DEFEND: in the band [gate, gate+12) our own dump is what would
            break the gate, so the tranche is halved there.
          - shed-pressure override: at >= 80 shed items the 100-slot
            discard cliff dominates any price consideration (gate -> 20).
      * FERTILIZER base 100: NO town consumption and a linear glut both
        sides (0.2 coins/unit) -> the joint daily dump decays it all
        season (measured 94 -> 41 vs cow_baron).
          - HOARD below FERT_GATE but only up to FERT_STOCK_CAP slots
            (the milk hoard owns the shed); RELEASE all above the gate;
            from day 25 RELEASE unconditionally (decay beats waiting).
      * WHEAT base 25: log above-curve (glut-tolerant) -> no gating beyond
        the feed reserve; sell the daily surplus.
    Returns a list of ["SELL", item, qty] market orders.
    """
    orders = []
    last_day = day >= SEASON_DAYS - 1
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))

    if last_day:
        # day 29: only bank money counts; everything liquidates regardless
        for item in ("MILK", "FERTILIZER", "WHEAT"):
            if shed.get(item, 0) > 0:
                orders.append(["SELL", item, shed[item]])
        return orders

    # ---- MILK: hoard / release / defend --------------------------------
    milk = shed.get("MILK", 0)
    if milk > 0:
        gate = _llm_sell_gate("MILK", prices.get("MILK", BASE_PRICE["MILK"]),
                              _milk_gate(day), {"day": day, "shed": milk,
                                                "herd": herd})
        p = prices.get("MILK", BASE_PRICE["MILK"])
        # milk lands in the shed in lumpy every-other-day harvests, so the
        # buffer scales with tomorrow's production (herd * 1.5) and the
        # tranche cap grows with stock -- never let lumpiness turn into a
        # pressure dump at the floor
        if shed_count >= 70 and p >= 30:
            # discard-cliff guard: drain to a working buffer rather than
            # let the 100-slot shed discard milk for free
            orders.append(["SELL", "MILK", max(0, milk - 15)])
        elif p >= 145:
            # recovery peak / early scarcity (d8-11 measured 172-186):
            # the first batches must clear NOW, in size
            orders.append(["SELL", "MILK", min(milk, 24)])
        elif p >= gate:
            # sell-through, no buffer: yesterday's production clears every
            # day at the band price; the lumpy every-other-day harvests
            # ride the same band two days out of two
            orders.append(["SELL", "MILK", min(milk, 20)])

    # ---- FERTILIZER: bounded hoard, gated release ----------------------
    fert = shed.get("FERTILIZER", 0)
    if fert > 0:
        if day >= 25:
            orders.append(["SELL", "FERTILIZER", fert])
        elif fert > FERT_STOCK_CAP:
            # hoard bound: keep the shed's slots for milk (measured: a 36
            # hoard forces milk pressure-dumps in the dairy mirror)
            orders.append(["SELL", "FERTILIZER", max(0, fert - FERT_FIELD_RESERVE)])
        elif prices.get("FERTILIZER", BASE_PRICE["FERTILIZER"]) >= FERT_GATE:
            sell = max(0, fert - FERT_FIELD_RESERVE)
            if sell > 0:
                orders.append(["SELL", "FERTILIZER", sell])
    return orders


def _plan_tiles(farm, day, wheat_price=25):
    """Deterministic tile allocation.

    Pastures: the manhattan ring (dist <= PASTURE_RING) around the shed
    access tile of every unlocked quadrant, capped at HERD_CAP + 2 built
    ahead.  Everything else is wheat (FM-2: no premium-crop branch
    mid-season; wheat is crash-proof feed).

    Returns (pasture_set, wheat_set, n_animals, wheat_capacity).
    """
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    quads = _get(farm, "unlocked_quadrants", ["NW"]) or ["NW"]

    pasture_set, wheat_set = set(), set()
    empty_ring, empty_field = [], []
    n_animals = 0
    n_pastures = 0
    n_wheat = 0
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if any(_dist(x, y, *q) <= PASTURE_RING for q in _shed_access(board)
                       if _quadrant_of(x, y, board) in quads) \
                        and not _shed_adjacent(x, y, board):
                    empty_ring.append(pos)
                else:
                    empty_field.append(pos)
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                continue
            if kind == "PASTURE":
                n_pastures += 1
                pasture_set.add(pos)
                if "animal" in tile:
                    n_animals += 1
            elif kind == "PLANT":
                wheat_set.add(pos)
                n_wheat += 1

    # grow the ring toward the herd plan (build-ahead of at most 2)
    ring_target = min(HERD_CAP + 2, n_pastures + 2, _herd_target(day, 99) + 2)
    empty_ring.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in _shed_access(board)), p[1], p[0]))
    for pos in empty_ring:
        if n_pastures < ring_target:
            pasture_set.add(pos)
            n_pastures += 1
        else:
            wheat_set.add(pos)
    # field tiles: nearest-first, capped by the labour budget (see _wheat_cap)
    empty_field.sort(key=lambda p: (min(_dist(p[0], p[1], *q) for q in _shed_access(board)), p[1], p[0]))
    wheat_room = _wheat_cap(day, wheat_price) - len(wheat_set)
    for pos in empty_field:
        if wheat_room > 0:
            wheat_set.add(pos)
            wheat_room -= 1

    # fertilized wheat yields 6 units per 5-day cycle => 1.2 units/day/tile
    capacity = int(len(wheat_set) * 1.2)
    return pasture_set, wheat_set, n_animals, capacity


def _quadrant_of(x, y, board_size):
    half = board_size // 2
    return ("N" if y < half else "S") + ("W" if x < half else "E")


def _build_tasks(obs, farm, private, day):
    """Return (tasks, animals_to_feed, herd_total, wheat_tiles, capacity)."""
    tiles = _get(farm, "tiles", [])
    board = len(tiles)
    wheat_px = _get(_get(obs, "market", {}) or {}, "prices", {}).get("WHEAT", 25)
    pasture_set, wheat_set, n_animals, capacity = _plan_tiles(farm, day, wheat_px)
    seeds = _get(private, "seeds", {}) or {}
    shed = _get(private, "shed", {}) or {}
    inventories = _get(private, "inventories", []) or []
    wheat_on_units = sum(_get(inv, "WHEAT", 0) for inv in inventories if inv)
    cows_on_units = sum(_get(inv, "COW", 0) for inv in inventories if inv)
    fert_on_units = sum(_get(inv, "FERTILIZER", 0) for inv in inventories if inv)
    animals_to_feed = 0

    tasks = []

    def add(w, x, y, act, key, need=None):
        tasks.append({"w": w, "x": x, "y": y, "act": act, "key": key, "need": need})

    last_day = day >= SEASON_DAYS - 1
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            if tile == "LOCKED":
                continue
            pos = (x, y)
            if tile is None:
                if pos in pasture_set:
                    add(46, x, y, ["BUILD_PASTURE"], ("bpast", x, y))
                elif pos in wheat_set and seeds.get("WHEAT", 0) > 0 \
                        and day <= SEASON_DAYS - 6:
                    add(30, x, y, ["PLANT", "WHEAT"], ("plant", x, y))
                continue
            if not isinstance(tile, dict):
                continue
            kind = _get(tile, "kind", "")
            if kind == "WEED":
                if pos in pasture_set or pos in wheat_set:
                    add(22, x, y, ["DIG"], ("dig", x, y))
                continue
            if kind == "PLANT":
                # wheat only in this engine; handle any crop defensively
                crop = _get(tile, "crop", "WHEAT")
                cd = CROPS.get(crop)
                if not cd:
                    continue
                age = day - _get(tile, "planted_day", day)
                yu = _get(tile, "yield_units", 0)
                ws, we = _window(crop)
                in_window = ws <= age <= we
                if not _get(tile, "watered_today", False):
                    if _get(tile, "consecutive_unwatered", 0) >= 1:
                        add(98, x, y, ["WATER"], ("water", x, y))   # dies tonight
                    elif in_window and pos in wheat_set:
                        add(42, x, y, ["WATER"], ("water", x, y))
                    elif age % 2 == 1:
                        add(24, x, y, ["WATER"], ("water", x, y))   # survival
                # FM-4: fertilizer -> 6-unit wheat instead of 4-unit.
                # Fertilize at age 2 so the +2 window waters (ages 2-4)
                # all land inside the 3-day fertilizer window.
                if crop == "WHEAT" and age == 2 and pos in wheat_set \
                        and _get(tile, "fertilized_until_day", -1) < day:
                    add(34, x, y, ["FERTILIZE"], ("fert", x, y), need="FERTILIZER")
                if yu > 0:
                    if age >= cd["max_yield_day"] + 1 or last_day:
                        # rot emergency: one-time crops decay to a weed from
                        # hour 0 of this day, ~1 unit per 2 turns
                        add(95, x, y, ["HARVEST"], ("harvest", x, y))
                    elif age >= cd["max_yield_day"] and (
                            _get(tile, "watered_today", False) or
                            _get(obs, "hour", 0) >= 18):
                        add(80, x, y, ["HARVEST"], ("harvest", x, y))
            elif "animal" in tile:
                if not _get(tile, "fed_today", False):
                    animals_to_feed += 1
                    # escape risk outranks everything: escalate by streak/hour
                    if _get(tile, "consecutive_unfed", 0) >= 1 or \
                            _get(obs, "hour", 0) >= 16:
                        w = 100
                    else:
                        w = 88
                    add(w, x, y, ["FEED"], ("feed", x, y), need="WHEAT")
                if day <= SEASON_DAYS - 3 and not _get(tile, "cared_today", False) \
                        and _get(tile, "fed_today", False):
                    add(56, x, y, ["CARE"], ("care", x, y))
                yu = _get(tile, "yield_units", 0)
                if yu >= 5:
                    add(92, x, y, ["HARVEST"], ("harvest", x, y))   # about to cap
                elif yu >= 3 or (yu > 0 and last_day):
                    add(70, x, y, ["HARVEST"], ("harvest", x, y))
                if _get(tile, "fertilizer_available", False):
                    add(32, x, y, ["COLLECT_FERTILIZER"], ("cfert", x, y))
            elif kind == "PASTURE" and "animal" not in tile:
                if shed.get("COW", 0) + cows_on_units > 0                         and _get(obs, "hour", 0) <= 18:
                    # urgent: an unplaced cow produces nothing and squats
                    # in the shed (a 100-slot shared resource)
                    add(82, x, y, ["PLACE", "COW"], ("place", x, y), need="COW")

    board_half = board // 2
    shed_tile = (board_half - 1, board_half - 1)
    # ---- feed logistics: distribute the wheat across several carriers ----
    # (one carrier cannot FEED a 10+-cow ring within 24 turns; chunks of 5
    # are grabbed by different units because a loaded carrier is barred
    # from picking up another chunk -- see executable() below.  Chunks are
    # raised whenever carried wheat falls short of the mouths, so multiple
    # carriers restock throughout the day.)
    if animals_to_feed > 0 and shed.get("WHEAT", 0) > 0:
        shortfall = animals_to_feed + 2 - wheat_on_units
        i = 0
        while shortfall > 0 and i < 4:
            n = min(5, shortfall, shed.get("WHEAT", 0))
            if n <= 0:
                break
            add(96 - 8 * i, shed_tile[0], shed_tile[1], ["PICKUP", "WHEAT", n],
                ("pickup_w", i))
            shortfall -= n
            i += 1
    # ---- cow logistics: carry bought cows onto empty pastures ----------
    if shed.get("COW", 0) > 0 and cows_on_units < 2 and \
            any(t["key"][0] == "place" for t in tasks):
        add(94, shed_tile[0], shed_tile[1], ["PICKUP", "COW", min(2, shed.get("COW", 0))],
            ("pickup_c", 0))
    # ---- fertilizer logistics for the age-2 wheat fertilize tasks -------
    if any(t["key"][0] == "fert" for t in tasks) and shed.get("FERTILIZER", 0) > 0 \
            and fert_on_units == 0:
        add(40, shed_tile[0], shed_tile[1], ["PICKUP", "FERTILIZER", 3],
            ("pickup_f", 0))
    herd_total = n_animals + shed.get("COW", 0) + cows_on_units
    return tasks, animals_to_feed, herd_total, len(wheat_set), capacity


def _market_orders(obs, farm, private, day, animals_to_feed, herd_total):
    money = _get(farm, "money", 0.0)
    shed = _get(private, "shed", {}) or {}
    seeds = _get(private, "seeds", {}) or {}
    prices = _get(_get(obs, "market", {}) or {}, "prices", {}) or {}
    quads = len(_get(farm, "unlocked_quadrants", ["NW"]) or ["NW"])
    shed_count = sum(v for v in shed.values() if isinstance(v, (int, float)))
    last_day = day >= SEASON_DAYS - 1

    orders = []

    # ---- buying: survival purchases FIRST (per-unit lockstep commits in
    # order, and an unaffordable later order must never eat feed money) ---
    # feed security (FM-3): never let the herd run short of wheat, counting
    # what carriers already hold (a shed-only check sees the morning pickup
    # as a shortfall and re-buys what we just sold -- measured -8k/season).
    # Starvation guard: dear wheat is still cheaper than a lost cow.
    wheat_carried = sum(_get(inv, "WHEAT", 0)
                        for inv in (_get(private, "inventories", []) or []) if inv)
    sys_wheat = shed.get("WHEAT", 0) + wheat_carried
    if animals_to_feed > 0 and not last_day \
            and sys_wheat < animals_to_feed + 3:
        cap = 85 if sys_wheat < animals_to_feed else WHEAT_BUY_MAX_PRICE
        if prices.get("WHEAT", 25) <= cap:
            want = min(16, animals_to_feed + 8 - sys_wheat)
            if want > 0:
                orders.append(["BUY_PRODUCT", "WHEAT", want])
    # seeds
    if seeds.get("WHEAT", 0) < 6 and day <= SEASON_DAYS - 7 and money >= 150:
        orders.append(["BUY_SEED", "WHEAT", 12])
    # cows: staged by money gate AND a daily pace cap (FM-3: the reserve
    # covers seeds + feed + hires, and <=2 head/day through the pre-wheat
    # opening stops the cash racing to zero before the first harvest)
    reserve = 800 if day <= 3 else (550 if day <= 7 else COW_BUY_RESERVE)
    pace = 2 if day <= 3 else 3
    target = _herd_target(day, _plan_tiles(farm, day, prices.get("WHEAT", 25))[3])
    if day > 10 and prices.get("MILK", 160) < 90:
        # demand drought (measured crash seeds: joint flow runs to the
        # floor, milk realized 29-37): freeze scaling -- the marginal cow
        # cannot pay for itself at distressed prices
        target = min(target, max(6, herd_total))
    bought = _buy_pace(_get(obs, "player", 0), day, _get(obs, "hour", 0))
    if herd_total < target and day <= COW_BUY_LAST_DAY \
            and money >= 400 + reserve and shed_count < 88 and bought < pace:
        n = min(pace - bought, target - herd_total,
                int((money - reserve) // 400))
        if n > 0:
            orders.append(["BUY_ANIMAL", "COW", n])
            _note_buys(_get(obs, "player", 0), day, _get(obs, "hour", 0), n)
    # land: NE adds a shed ring + field; SW/SE follow when flush (FM-1 scale)
    if quads < 2 and money >= 1800 and day >= 4:
        orders.append(["BUY_LAND"])

    # ---- selling: selective-intervention gates --------------------------
    orders.extend(_market_gates(day, prices, shed, herd_total))
    # wheat: glut-tolerant curve; sell the surplus above the feed reserve
    if not last_day:
        reserve_w = animals_to_feed + WHEAT_FEED_RESERVE
        surplus = shed.get("WHEAT", 0) - reserve_w
        if surplus > 0 and (prices.get("WHEAT", 25) >= 12 or shed_count >= 70
                            or day >= 26):
            orders.append(["SELL", "WHEAT", surplus])
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
        op = task["act"][0]
        if op in ("WATER", "FERTILIZE"):
            return kind == "PLANT"
        if op == "HARVEST":
            return kind == "PLANT" or (isinstance(tile, dict) and "animal" in tile)
        if op in ("FEED", "CARE", "COLLECT_FERTILIZER"):
            return isinstance(tile, dict) and "animal" in tile
        if op == "PLANT":
            return tile is None
        if op == "DIG":
            return kind == "WEED"
        if op == "BUILD_PASTURE":
            return tile is None
        if op == "PLACE":
            return isinstance(tile, dict) and _get(tile, "kind", "") == "PASTURE" \
                and "animal" not in tile
        if op == "PICKUP":
            if not _shed_adjacent(units[ui][0], units[ui][1], board):
                return False
            # a carrier holding a full chunk moves out to feed instead of
            # chain-grabbing every chunk at the shed (multi-carrier FEED)
            if task["act"][1:2] == ["WHEAT"] and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                return False
            return True
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
            # 2) walk toward the best unclaimed task; prefer tasks whose
            # carried-item requirement this unit already satisfies
            best = None
            for t in tasks:
                if t["key"] in claimed:
                    continue
                score = t["w"] / (1.0 + _dist(ux, uy, t["x"], t["y"]))
                need = t.get("need")
                if need:
                    if _get(unit_inv(ui), need, 0) > 0:
                        score *= 1.8   # carriers converge on consumer tasks
                    else:
                        score *= 0.35  # wheatless units do not chase FEED tasks
                if t["act"][0] == "PICKUP" and t["act"][1:2] == ["WHEAT"] \
                        and _get(unit_inv(ui), "WHEAT", 0) >= 5:
                    score *= 0.35     # loaded carriers leave the shed to feed
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
        day = _get(obs, "day", 0)
        hour = _get(obs, "hour", 0)
        tiles = _get(farm, "tiles", [])
        if not tiles:
            return {"farmer": ["PASS"], "hands": [], "market": []}

        tasks, animals_to_feed, herd_total, wheat_tiles, capacity = \
            _build_tasks(obs, farm, private=_get(obs, "private", {}) or {}, day=day)
        actions = _schedule_units(obs, farm, _get(obs, "private", {}) or {},
                                  day, tasks)
        orders = _market_orders(obs, farm, _get(obs, "private", {}) or {},
                                day, animals_to_feed, herd_total)

        # HIRE up to the labour plan at dawn. Hands reset every morning and
        # only hour <= 2 can hire, so ALL hires must go out in the first
        # turn's order list (one HIRE per turn leaves us stuck at 3 hands
        # against a plan of 5 -- measured in the crash seeds). Cost is fib:
        # 1,1,2,3,5 per day, trivial vs a rotting harvest.
        orders = [o for o in orders if o[0] != "HIRE"]
        hands = _get(farm, "hands", []) or []
        hands_t = _hands_target(day, herd_total, wheat_tiles)
        money = _get(farm, "money", 0.0)
        if hour <= 2 and len(hands) < hands_t and money >= 40:
            for _ in range(min(3, hands_t - len(hands))):
                orders.append(["HIRE"])

        farmer = actions[0] if actions else ["PASS"]
        hands_actions = actions[1:]
        return {"farmer": farmer, "hands": hands_actions, "market": orders[:10]}
    except Exception:
        # a submission must never crash: fall back to a safe legal action
        return {"farmer": ["PASS"], "hands": [], "market": []}
