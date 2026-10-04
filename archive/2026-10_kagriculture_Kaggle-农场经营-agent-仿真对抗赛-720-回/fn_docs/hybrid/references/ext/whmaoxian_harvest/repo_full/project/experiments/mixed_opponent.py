"""Offline receding-horizon farm planner for Kaggriculture."""
import math

MAX_QUADRANTS = 2
FORECAST_DEMAND = 0.0
OPPONENT_SUPPLY = 0.8
ANIMAL_PLAN = ("GOOSE", "GOOSE", "COW", "SHEEP")
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
SHOPS = {
    "BAKERY": ("EGG", "WHEAT"), "PIZZA_SHOP": ("MILK", "TOMATO", "WHEAT"),
    "BRUNCH_SPOT": ("EGG", "WHEAT", "STRAWBERRY"), "YARN_STORE": ("WOOL", "WOOL"),
    "ICE_CREAM_SHOP": ("STRAWBERRY", "MILK", "WHEAT"), "PET_CAFE": ("CARROT", "CARROT"),
    "SMOOTHIE_SHOP": ("STRAWBERRY", "MILK"),
    "FARMERS_MARKET": ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY"),
}

# cost, first harvest age, target harvest age, unfertilized yield
CROPS = {"WHEAT": (10, 2, 4, 4), "CARROT": (20, 2, 3, 3), "MELON": (80, 10, 10, 6)}


def distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def move(a, b):
    if a[0] != b[0]:
        return ["EAST" if b[0] > a[0] else "WEST"]
    if a[1] != b[1]:
        return ["SOUTH" if b[1] > a[1] else "NORTH"]
    return ["PASS"]


def projected_price(crop, inventory):
    base, throughput, down, up = {
        "WHEAT": (25, 400, 0.2, 0.8),
        "CARROT": (35, 450, 0.7, 1.0),
        "MELON": (250, 300, 3.6, 0.2),
    }[crop]
    delta = inventory - 10000
    u = abs(delta) / throughput
    if delta >= 0:
        shape = {"WHEAT": math.log1p(abs(delta)) / math.log1p(throughput),
                 "CARROT": math.sqrt(u), "MELON": u * u}[crop]
        return max(1, base * (1 - down * shape))
    shape = {"WHEAT": math.sqrt(u), "CARROT": u + 8 * max(0, u - 1) ** 2,
             "MELON": math.log1p(abs(delta)) / math.log1p(throughput)}[crop]
    return base * (1 + up * shape)


def agent(obs, configuration=None):
    cfg = configuration or {}
    day, hour = obs["day"], obs["hour"]
    step = obs.get("step", day * 24 + hour)
    last_step = cfg.get("episodeSteps", 720) - 2
    turns = cfg.get("turnsPerDay", 24)
    remaining = last_step - step
    farm = obs["farms"][obs["player"]]
    private = obs["private"]
    tiles = farm["tiles"]
    half = len(tiles) // 2
    shed_tiles = [(half - 1, half - 1), (half, half - 1), (half - 1, half), (half, half)]
    units = [farm["farmer"]] + list(farm["hands"])
    seeds = dict(private["seeds"])
    animal_positions = [(half - 1, half - 1), (half - 2, half - 1),
                        (half - 1, half - 2), (half - 2, half - 2)][:len(ANIMAL_PLAN)]
    feed_reserve = len(ANIMAL_PLAN) if remaining >= turns else 0
    market = [["SELL", item, n - (feed_reserve if item == "WHEAT" else 0)]
              for item, n in private["shed"].items()
              if item not in ANIMAL_COST and n > (feed_reserve if item == "WHEAT" else 0)]
    budget = farm["money"]
    quadrants = len(farm["unlocked_quadrants"])
    desired_hands = 8 + 2 * (quadrants - 1)
    if hour < 3 and remaining > 10 and budget > 100:
        count = farm["hires_today"]
        costs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]
        for i in range(count, min(desired_hands, len(costs))):
            if len(market) >= cfg.get("maxMarketOrdersPerTurn", 10):
                break
            cost = costs[i] * cfg.get("farmHandCostMult", 1)
            if budget - cost < 80:
                break
            market.append(["HIRE"])
            budget -= cost

    if day < 10:
        for animal in dict.fromkeys(ANIMAL_PLAN):
            placed = sum(isinstance(t, dict) and t.get("animal") == animal for row in tiles for t in row)
            carried_n = sum(inv.get(animal, 0) for inv in private["inventories"])
            needed = ANIMAL_PLAN.count(animal) - placed - carried_n - private["shed"].get(animal, 0)
            if needed > 0 and budget > needed * ANIMAL_COST[animal] + 200 and len(market) < 10:
                market.append(["BUY_ANIMAL", animal, needed])
                budget -= needed * ANIMAL_COST[animal]
    if remaining >= turns and private["shed"].get("WHEAT", 0) < feed_reserve:
        needed = feed_reserve - private["shed"].get("WHEAT", 0)
        if budget > needed * obs["market"].get("prices", {}).get("WHEAT", 50) + 50:
            market.append(["BUY_PRODUCT", "WHEAT", needed])
            budget -= needed * obs["market"].get("prices", {}).get("WHEAT", 50)

    # Expansion has an explicit season cutoff and retains operating cash.
    land_cost = (1000, 2000, 4000)[min(quadrants - 1, 2)]
    occupied = sum(isinstance(t, dict) and t.get("kind") == "PLANT" for row in tiles for t in row)
    if (quadrants < MAX_QUADRANTS and day >= 2 and remaining > 16 * turns
            and occupied >= quadrants * half * half * 0.65 and budget > land_cost + 1200):
        market.append(["BUY_LAND"])
        budget -= land_cost

    pending = {crop: 0 for crop in CROPS}
    for row in tiles:
        for tile in row:
            if isinstance(tile, dict) and tile.get("crop") in CROPS:
                pending[tile["crop"]] += CROPS[tile["crop"]][3]
    # Include carried goods and seeds already paid for in anticipated supply.
    for crop in CROPS:
        pending[crop] += seeds.get(crop, 0) * CROPS[crop][3]
        pending[crop] += private["shed"].get(crop, 0)
        pending[crop] += sum(inv.get(crop, 0) for inv in private["inventories"])

    opponent_pending = {crop: 0 for crop in CROPS}
    for row in obs["farms"][1 - obs["player"]]["tiles"]:
        for tile in row:
            if isinstance(tile, dict) and tile.get("crop") in CROPS:
                opponent_pending[tile["crop"]] += CROPS[tile["crop"]][3]
    demand = {crop: turns / cfg.get("townCenterSellInterval", 24) for crop in CROPS}
    for shop in obs.get("town", {}).get("unlocked_shops", []):
        for item in SHOPS.get(shop, ()):
            if item in demand:
                demand[item] += turns / cfg.get("townShopSellInterval", 4)

    options = []
    for crop, (cost, first, age, yield_n) in CROPS.items():
        if remaining < age * turns + 10:
            continue
        future_inventory = (obs["market"]["inventory"][crop] + pending[crop] + yield_n
                            + OPPONENT_SUPPLY * opponent_pending[crop]
                            - FORECAST_DEMAND * demand[crop] * age)
        price = projected_price(crop, future_inventory)
        profit = (yield_n * price - cost) / (age + 0.5)
        if profit > 4:
            options.append((profit, crop))
    crop_choice = max(options)[1] if options else None

    # Buy a small batch one turn before planting (unit actions precede market orders).
    empties = sum(tile is None for row in tiles for tile in row)
    if crop_choice and empties and seeds.get(crop_choice, 0) < 3:
        n = min(3 - seeds.get(crop_choice, 0), empties,
                max(0, int((budget - 50) // CROPS[crop_choice][0])))
        if n:
            market.append(["BUY_SEED", crop_choice, n])

    tasks = []
    for y, row in enumerate(tiles):
        for x, tile in enumerate(row):
            pos = (x, y)
            if pos in animal_positions:
                continue
            if isinstance(tile, dict) and tile.get("kind") == "PLANT":
                crop = tile["crop"]
                if crop not in CROPS:
                    continue
                _, first, age, _ = CROPS[crop]
                crop_age = day - tile["planted_day"]
                mature = crop_age >= first
                ripe = crop_age >= age
                # The last day needs time to carry products back and sell them.
                if mature and (ripe or remaining < turns) and tile.get("yield_units", 0):
                    if not tile["watered_today"] and crop_age <= age and remaining >= 12:
                        tasks.append((pos, ["WATER"], 180))
                    else:
                        tasks.append((pos, ["HARVEST"], 200))
                elif not tile["watered_today"] and remaining >= turns:
                    tasks.append((pos, ["WATER"], 100 + 10 * hour))
            elif tile is None and crop_choice and hour < turns - 3:
                available = [c for _, c in sorted(options, reverse=True) if seeds.get(c, 0) > 0]
                if available:
                    tasks.append((pos, ["PLANT", available[0]], 35))
            elif isinstance(tile, dict) and tile.get("kind") == "WEED" and crop_choice:
                tasks.append((pos, ["DIG"], 20))

    actions = []
    reserved = set()
    available_shed = dict(private["shed"])
    for i, pos in enumerate(units):
        inventory = private["inventories"][i] if i < len(private["inventories"]) else {}
        carried = sum(inventory.values())
        near_shed = min(shed_tiles, key=lambda p: distance(pos, p))
        home_distance = distance(pos, near_shed)
        # Dedicated animal care first, then these workers can help with crops.
        # Pickup budgets are shared, so two workers cannot reserve the same item.
        special = None
        if i < len(ANIMAL_PLAN) and remaining > home_distance + 5:
            target = animal_positions[i]
            animal = ANIMAL_PLAN[i]
            animal_tile = tiles[target[1]][target[0]]
            if not isinstance(animal_tile, dict) or not animal_tile.get("animal"):
                if day < 10:
                    if inventory.get(animal, 0):
                        if distance(pos, target):
                            special = move(pos, target)
                        elif animal_tile is None:
                            special = ["BUILD_COOP" if animal == "GOOSE" else "BUILD_PASTURE"]
                        elif animal_tile.get("kind") == "WEED":
                            special = ["DIG"]
                        else:
                            special = ["PLACE", animal]
                    elif available_shed.get(animal, 0):
                        special = move(pos, near_shed) if home_distance else ["PICKUP", animal, 1]
                        if home_distance == 0:
                            available_shed[animal] -= 1
            else:
                needs_feed = not animal_tile["fed_today"] and remaining >= turns
                if needs_feed and not inventory.get("WHEAT", 0):
                    if available_shed.get("WHEAT", 0):
                        special = move(pos, near_shed) if home_distance else ["PICKUP", "WHEAT", 1]
                        if home_distance == 0:
                            available_shed["WHEAT"] -= 1
                else:
                    op = None
                    if needs_feed:
                        op = "FEED"
                    elif animal_tile.get("yield_units", 0):
                        op = "HARVEST"
                    elif animal_tile.get("fertilizer_available"):
                        op = "COLLECT_FERTILIZER"
                    elif not animal_tile["cared_today"] and remaining >= turns:
                        op = "CARE"
                    if op:
                        special = move(pos, target) if distance(pos, target) else [op]
        if special is not None:
            actions.append(special)
            continue
        # Sell from shed only. Return before the final action, since the last daily
        # auto-deposit would occur after the final opportunity to sell.
        if carried and (remaining <= home_distance + 3 or carried >= 15 or
                        (home_distance == 0 and hour > 0)):
            actions.append(["DROP"] if home_distance == 0 else move(pos, near_shed))
            # Include same-turn DROP because unit actions execute before SELL.
            if home_distance == 0:
                for item, n in inventory.items():
                    order = next((o for o in market if o[:2] == ["SELL", item]), None)
                    if order is not None:
                        order[2] += n
                    else:
                        market.append(["SELL", item, n])
            continue
        candidates = []
        for target, action, priority in tasks:
            if target in reserved:
                continue
            dist = distance(pos, target)
            if action[0] == "PLANT" and (seeds.get(action[1], 0) <= 0 or hour + dist + 2 >= turns):
                continue
            if action[0] == "HARVEST":
                return_dist = min(distance(target, p) for p in shed_tiles)
                if dist + return_dist + 1 > remaining:
                    continue
            if dist >= min(turns - hour, remaining + 1):
                continue
            candidates.append((priority / (dist + 1), target, action))
        if candidates:
            _, target, action = max(candidates)
            reserved.add(target)
            actions.append(action if distance(pos, target) == 0 else move(pos, target))
            if distance(pos, target) == 0 and action[0] == "PLANT":
                seeds[action[1]] -= 1
        elif carried and remaining < turns:
            actions.append(["DROP"] if home_distance == 0 else move(pos, near_shed))
        else:
            actions.append(["PASS"])
    return {"farmer": actions[0], "hands": actions[1:],
            "market": market[:cfg.get("maxMarketOrdersPerTurn", 10)]}
