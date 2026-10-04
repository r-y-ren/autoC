"""Offline, stateless crop scheduling baseline for Kaggriculture."""
import math

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
    market = [["SELL", item, n] for item, n in private["shed"].items() if n > 0]
    budget = farm["money"]
    # Six cheap hands cost 20 coins/day and provide enough labor for the first field.
    if hour < 3 and remaining > 10 and budget > 100:
        count = farm["hires_today"]
        costs = [1, 1, 2, 3, 5, 8]
        for i in range(count, 6):
            if len(market) >= cfg.get("maxMarketOrdersPerTurn", 10):
                break
            cost = costs[i] * cfg.get("farmHandCostMult", 1)
            if budget - cost < 80:
                break
            market.append(["HIRE"])
            budget -= cost

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

    options = []
    for crop, (cost, first, age, yield_n) in CROPS.items():
        if remaining < age * turns + 10:
            continue
        future_inventory = obs["market"]["inventory"][crop] + pending[crop] + yield_n
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
    for i, pos in enumerate(units):
        inventory = private["inventories"][i] if i < len(private["inventories"]) else {}
        carried = sum(inventory.values())
        near_shed = min(shed_tiles, key=lambda p: distance(pos, p))
        home_distance = distance(pos, near_shed)
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
