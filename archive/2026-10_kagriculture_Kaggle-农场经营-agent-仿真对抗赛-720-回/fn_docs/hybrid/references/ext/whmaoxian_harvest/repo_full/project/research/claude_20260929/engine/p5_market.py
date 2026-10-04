

# ----------------------------------------------------------------------------- market
def desired_hands(w, st):
    cfg = st["cfg"]
    plants = animals = empty = 0
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if t is None:
                empty += 1
            elif isinstance(t, dict):
                if t.get("kind") == "PLANT":
                    plants += 1
                elif t.get("animal"):
                    animals += 1
                else:
                    empty += 1
    if "SE" in w.quads and cfg["se_max_tiles"] < 25:
        empty = max(0, empty - (25 - cfg["se_max_tiles"]))
    daily = plants * 2.2 + animals * 4.6 + empty * 2.0 + 8
    hands = int(math.ceil(daily / cfg["hand_turns"])) - 1
    if w.day == 0:
        hands = max(hands, cfg["day0_hands"])
    return max(1, min(cfg["max_hands"], hands))


def projected_shed(w, cmds):
    shed = dict(w.shed)
    for u, c in enumerate(cmds):
        inv = w.invs[u] if u < len(w.invs) else {}
        pos = w.units[u]
        if c[0] == "PLACE" and len(c) >= 3 and pos in SHED_ADJ and c[1] in PRODUCTS:
            shed[c[1]] = shed.get(c[1], 0) + min(int(c[2]), inv.get(c[1], 0))
        elif c[0] == "DROP" and pos in SHED_ADJ:
            for k, v in inv.items():
                shed[k] = shed.get(k, 0) + v
        elif c[0] == "PICKUP" and len(c) >= 3:
            shed[c[1]] = max(0, shed.get(c[1], 0) - int(c[2]))
    return shed


def market_orders(w, st, tasks, cmds):
    cfg = st["cfg"]
    shed = projected_shed(w, cmds)
    animals = animal_count(w)
    feed_tasks = sum(1 for s in tasks.values() if any(o == "FEED" for o, _ in s))
    carried_w = sum(i.get("WHEAT", 0) for i in w.invs)
    wheat_keep = int(math.ceil(animals * cfg["wheat_keep_days"])) + max(0, feed_tasks - carried_w)
    fdem = fert_demand(w, st, cfg["fert_days"])
    carried_f = sum(i.get("FERTILIZER", 0) for i in w.invs)
    fert_keep = max(0, fdem - carried_f)
    last = w.step >= LAST
    sells = []
    proceeds = 0.0
    for item in PRODUCTS:
        q = shed.get(item, 0)
        if q <= 0:
            continue
        final_day = cfg["end_animal"] and (w.day >= 29 or (w.day == 28 and w.hour >= cfg["end_keep_hour"]))
        if item == "WHEAT" and not last and not final_day:
            q = max(0, q - wheat_keep)
        if item == "FERTILIZER" and not last and not final_day:
            q = max(0, q - fert_keep - cfg["fert_sell_margin"])
        if q > 0 and cfg["smart_sell"] and item in cfg["hold_items"] and not last:
            q = smart_quantity(w, st, item, q, shed)
        if q > 0:
            sells.append(["SELL", item, q])
            p = w.prices.get(item, 1)
            proceeds += sum(max(1, price_at(item, w.minv.get(item, 10000) + j)) for j in range(min(q, 30))) + max(0, q - 30) * 1
    sells.sort(key=lambda o: -w.prices.get(o[1], 0) * o[2])
    sells = sells[: cfg["sell_lots"]]
    money = w.money + proceeds * 0.9
    reserve = cfg["cash_buffer"]
    buys = []
    room = 100 - sum(shed.values())
    # 1. feed wheat
    wheat_have = shed.get("WHEAT", 0) + carried_w
    pending_animals = sum(w.shed.get(a, 0) for a in ANIMALS) + sum(i.get(a, 0) for i in w.invs for a in ANIMALS)
    wheat_need = feed_tasks + ((animals + pending_animals) if w.hour >= cfg["wheat_prebuy_hour"] else 0)
    if wheat_have < wheat_need and room > 0:
        pr = w.prices.get("WHEAT", 30) + 2
        k = min(wheat_need - wheat_have, int(max(0, money - 5) // pr), room)
        if k > 0:
            buys.append(["BUY_PRODUCT", "WHEAT", k])
            money -= k * pr
            room -= k
    fr = feed_reserve(w)
    # 2. hires (morning)
    if w.hour <= 2 and w.step < LAST - 6:
        want = desired_hands(w, st)
        have = len(w.units) - 1
        k = 0
        while have + k < want:
            cost = fib(w.hires_today + k)
            if money - fr < cost + reserve:
                break
            buys.append(["HIRE"])
            money -= cost
            k += 1
    # 3. animals for prepared structures
    roles = st["roles"]
    for a in ("SHEEP", "COW", "GOOSE"):
        slots = 0
        for (x, y), r in roles.items():
            if r != a:
                continue
            t = w.tiles[y][x]
            if not (isinstance(t, dict) and t.get("animal")):
                slots += 1
        pend = w.shed.get(a, 0) + sum(i.get(a, 0) for i in w.invs)
        k = slots - pend
        cost = ANIMALS[a]["cost"]
        while k > 0 and money - fr >= cost + reserve and room > 1:
            buys.append(["BUY_ANIMAL", a, 1])
            money -= cost
            fr += 2 * (w.prices.get("WHEAT", 25) + 3)
            room -= 1
            k -= 1
    # 4. land
    nq = len(w.quads)
    if nq < 4 and w.step < LAST - 5 * TPD:
        k = nq - 1
        tomato_world = sum(x in ("PIZZA_SHOP", "FARMERS_MARKET") for x in w.shops) >= cfg["se_tomato_shops"]
        se_ok = (k == 2 and tomato_world and cfg["se_tomato_from"] <= w.day <= cfg["se_tomato_to"]
                 and money - fr >= cfg["se_tomato_money"] and w.hour <= 2)
        if (w.day >= cfg["land_days"][k] and money - fr >= LAND_PRICE[k] + cfg["land_reserve"][k]) or se_ok:
            buys.append(["BUY_LAND"])
            money -= LAND_PRICE[k]
    # 4b. fertilizer when we will need more than we hold
    fshort = fert_keep - shed.get("FERTILIZER", 0)
    if any(o[1] == "FERTILIZER" for o in sells):
        fshort = 0
    fp = w.prices.get("FERTILIZER", 100)
    if fshort > 0 and fp <= cfg["fert_buy_max_price"] and room > fshort:
        k = min(fshort, int(max(0, money - fr - reserve) // (fp + 2)))
        if k > 0:
            buys.append(["BUY_PRODUCT", "FERTILIZER", k])
            money -= k * (fp + 2)
            room -= k
    # 5. seeds for planned plantings
    want_seeds = dict(st.get("seed_intent") or {})
    for c in ("WHEAT", "CARROT"):
        if any(op == "PLANT:" + c for s in tasks.values() for op, _ in s):
            want_seeds[c] = max(want_seeds.get(c, 0), cfg["seed_buffer"])
    bp = BLUEPRINT.get(w.seat) if cfg["use_blueprint"] else None
    if bp and cfg["bp_seed_ahead"] > 0:
        upcoming = {}
        for pp, ev in bp.items():
            for t, c in ev:
                if c in CROPS and w.step <= t <= w.step + cfg["bp_seed_ahead"]:
                    upcoming[c] = upcoming.get(c, 0) + 1
        for c, k in upcoming.items():
            if CROPS[c]["seed"] <= 20:
                want_seeds[c] = max(want_seeds.get(c, 0), min(k, cfg["bp_seed_cap"]))
    after = st.get("seeds_after") or w.seeds
    for c in sorted(want_seeds, key=lambda c: -CROPS[c]["seed"]):
        n = want_seeds[c]
        cost = CROPS[c]["seed"]
        k = min(n - after.get(c, 0), int(max(0, money - fr - reserve) // cost))
        if k > 0:
            buys.append(["BUY_SEED", c, k])
            money -= k * cost
    return (sells + buys)[:10]


# ----------------------------------------------------------------------------- entry
def act(obs, config=None):
    seat = int(obs.get("player", 0) or 0)
    step = int(obs.get("step", 0) or 0)
    st = STATE.get(seat)
    if st is None or step == 0 or step <= st["last"]:
        st = new_state()
        st["cfg"].update(OVERRIDES)
        STATE[seat] = st
    st["last"] = step
    w = World(obs)
    if "opp_clone" not in st:
        st["opp_clone"] = farm_similarity(w.tiles, w.opp["tiles"]) >= st["cfg"]["clone_sim"]
    if w.hour == 0:
        st["target"] = {}
    assign_animal_roles(w, st)
    if st["cfg"]["use_blueprint"]:
        blueprint_mark(w, st)
    tasks = gen_tasks(w, st)
    cmds = run_units(w, st, tasks)
    for i, c in enumerate(cmds):
        if not c or c[0] is None:
            cmds[i] = ["PASS"]
    market = market_orders(w, st, tasks, cmds)
    return {"farmer": cmds[0], "hands": cmds[1:], "market": market}


OVERRIDES = {}


def farm_agent(observation, configuration=None):
    return act(observation, configuration)


def smart_quantity(w, st, item, q, shed):
    """Sell only while the unit price stays above a fraction of the recent price peak."""
    cfg = st["cfg"]
    pm = st.setdefault("pmax", {})
    cur = w.prices.get(item, 1)
    old = pm.get(item)
    if old is None or old[1] < w.step - cfg["peak_window"]:
        pm[item] = (cur, w.step)
    elif cur >= old[0]:
        pm[item] = (cur, w.step)
    peak = pm[item][0]
    remaining = LAST - w.step
    if w.day >= cfg["no_hold_day"] and w.hour >= cfg["no_hold_hour"]:
        return q
    if cfg["front_run"] and opp_front_run(w, st, item) > 0:
        return q
    if remaining <= cfg["liquidate_steps"]:
        ticks = max(1, remaining // 4)
        return min(q, max(1, -(-q // ticks)))
    inv = w.minv.get(item, 10000)
    thr = cfg["hold_theta"] * peak
    k = 0
    while k < q and price_at(item, inv + k) >= thr:
        k += 1
    # capacity valve: keep room for tonight
    held = sum(shed.values())
    if w.hour >= cfg["hold_valve_hour"]:
        carried = sum(sum(i.values()) for i in w.invs)
        over = held + carried - k - cfg["hold_cap"]
        if over > 0:
            k = min(q, k + over)
    return k
