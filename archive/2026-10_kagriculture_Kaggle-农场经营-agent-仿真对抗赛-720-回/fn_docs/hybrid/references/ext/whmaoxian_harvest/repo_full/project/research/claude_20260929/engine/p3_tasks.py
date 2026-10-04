

# ----------------------------------------------------------------------------- tasks
def plant_subtasks(w, st, t):
    cfg = st["cfg"]
    c = t["crop"]
    cd = CROPS[c]
    age = w.day - t["planted_day"]
    subs = []
    urgent = t["consecutive_unwatered"] >= 1
    watered = t["watered_today"]
    yu = t.get("yield_units", 0)
    endgame = w.step >= LAST - st["cfg"]["endgame_steps"]
    hour_mult = 1.0 + w.hour / cfg["urgency_hours"]
    urg = cfg["urgent_pr"] * hour_mult
    if not cd["ongoing"]:
        ws = (cd["maxd"] + 1) // 2
        in_window = ws <= age <= cd["maxd"]
        ready_age = cd["maxd"] if c != "MELON" else 10
        if c == "WHEAT" and t["fertilized_until_day"] >= w.day and cfg["wheat_fast"]:
            ready_age = 3
        at_ready = age >= ready_age
        if c == "WHEAT" and cfg["fert_wheat"] and age == ws and t["fertilized_until_day"] < w.day and not watered:
            subs.append(("FERTILIZE", cfg["wheat_fert_pr"]))
        if not watered and not (endgame and age >= cd["first"]):
            if urgent:
                subs.append(("WATER", urg))
            elif at_ready:
                subs.append(("WATER", cfg["ready_pr"] * hour_mult))
            elif in_window:
                subs.append(("WATER", cfg["window_pr"]))
        if yu > 0 and age >= cd["first"]:
            decaying = w.step >= t["max_lifespan_step"] >= 0
            if decaying or endgame:
                subs.append(("HARVEST", cfg["decay_pr"]))
            elif at_ready and (watered or yu >= cd["cap"] or (c == "WHEAT" and yu >= 5)):
                subs.append(("HARVEST", cfg["ready_pr"] * hour_mult))
    else:
        first, interval = cd["first"], cd["interval"]
        k = w.day + 1 - t["planted_day"] - first
        prod_today = k >= 0 and k % interval == 0 and k // interval + 1 <= 4
        fert_on = t["fertilized_until_day"] >= w.day
        want_fert = (c == "STRAWBERRY" and cfg["fert_straw"]) or (c == "TOMATO" and cfg["fert_tomato"])
        if prod_today and want_fert and not fert_on and w.hour < 22:
            subs.append(("FERTILIZE", cfg["fert_pr"]))
        if not watered:
            if urgent:
                subs.append(("WATER", urg))
            elif prod_today and (fert_on or want_fert):
                subs.append(("WATER", 6))
            else:
                subs.append(("WATER", cfg["spare_water_pr"]))
        last_prod_day = t["planted_day"] + first - 1 + 3 * interval
        done = w.day > last_prod_day
        inc = 2 if (fert_on or want_fert) else 1
        decaying = t.get("max_lifespan_step", -1) >= 0 and w.step >= t["max_lifespan_step"] - 2
        if yu > 0 and (done or decaying):
            subs.append(("HARVEST", cfg["decay_pr"]))
        elif yu >= cfg["ongoing_harvest_at"] or (yu > 0 and (endgame or (prod_today and yu + inc > cd["cap"]))):
            subs.append(("HARVEST", 8))
        if done and yu == 0:
            subs.append(("DIG", cfg["dig_pr"]))
    return subs


def animal_subtasks(w, st, t):
    a = t["animal"]
    ad = ANIMALS[a]
    subs = []
    cfg = st["cfg"]
    worth = w.prices.get(ad["product"], 0) >= cfg["feed_value_ratio"] * (w.prices.get("WHEAT", 30) + cfg["feed_labor"])
    must = t.get("consecutive_unfed", 0) >= 1
    feed_today = (not t["fed_today"]) and (must or worth or not cfg["skip_feed"])
    if cfg["end_animal"]:
        k0 = w.day + 1 - t["placed_day"] - ad["first"]
        prod_tonight = k0 >= 0 and k0 % ad["interval"] == 0
        if w.day >= 29 or (w.day == 28 and not prod_tonight):
            feed_today = False
    if feed_today:
        subs.append(("FEED", 20))
    if not t["cared_today"] and (t["fed_today"] or feed_today) and not (cfg["end_animal"] and w.day >= 28):
        subs.append(("CARE", 5))
    if t.get("fertilizer_available"):
        subs.append(("COLLECT_FERTILIZER", 4))
    yu = t.get("yield_units", 0)
    if yu > 0:
        k = w.day + 1 - t["placed_day"] - ad["first"]
        prod_today = k >= 0 and k % ad["interval"] == 0
        nxt = 1 + t.get("pending_care_bonus", 0) + 1 if prod_today else 0
        if yu + nxt > ad["held"] or w.step >= LAST - 30 or yu >= ad["held"] - 1:
            subs.append(("HARVEST", 7))
    return subs


def gen_tasks(w, st):
    tasks = {}
    roles = st["roles"]
    crop_now = None
    melons = sum(1 for yy in range(10) for xx in range(10)
                 if isinstance(w.tiles[yy][xx], dict) and w.tiles[yy][xx].get("crop") == "MELON")
    st["melons"] = max(st["melons"], melons)
    melon_left = max(0, st["cfg"]["melon_max"] - st["melons"])
    idle = st.setdefault("idle_since", {})
    se_used = sum(1 for yy in range(5, 10) for xx in range(5, 10)
                  if isinstance(w.tiles[yy][xx], dict) and w.tiles[yy][xx].get("kind") in ("PLANT", "COOP", "PASTURE"))
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if t == "LOCKED":
                continue
            p = (x, y)
            role = roles.get(p)
            subs = []
            if t is None or (isinstance(t, dict) and t.get("kind") == "WEED"):
                since = idle.setdefault(p, w.step)
            else:
                idle.pop(p, None)
                since = w.step
            boost = st["cfg"]["idle_boost"] * (w.step - since) / 24.0
            if t is None:
                if role in ANIMALS:
                    subs.append(("BUILD_" + ANIMALS[role]["struct"], 6))
                elif w.step < LAST - st["cfg"]["plant_stop_steps"] and not (x >= 5 and y >= 5 and se_used >= st["cfg"]["se_max_tiles"]):
                    if x >= 5 and y >= 5:
                        se_used += 1
                    use_bp = st["cfg"]["use_blueprint"] or w.day >= st["cfg"]["bp_from_day"]
                    bpc = blueprint_crop(w, st, p) if use_bp else None
                    if bpc:
                        subs.append(("PLANT:" + bpc, 5 + boost))
                    elif bpc == "" and (not st["cfg"]["bp_fallback"] or w.day >= st["cfg"]["bp_fallback_until"]):
                        pass
                    else:
                        if crop_now is None or (crop_now == "MELON" and melon_left <= 0):
                            crop_now = crop_choice(w, st, melon_left) or ""
                        if crop_now:
                            if crop_now == "MELON":
                                melon_left -= 1
                            subs.append(("PLANT:" + crop_now, 5 + boost))
            elif t.get("kind") == "WEED":
                if role in ANIMALS or w.step < LAST - 3 * TPD:
                    subs.append(("DIG", st["cfg"]["dig_pr"] + boost))
            elif t.get("kind") == "PLANT":
                subs = plant_subtasks(w, st, t)
            elif t.get("kind") in ("COOP", "PASTURE"):
                if t.get("animal"):
                    subs = animal_subtasks(w, st, t)
                elif role in ANIMALS and ANIMALS[role]["struct"] == t["kind"] and st.get("want_more", {}).get(role, True):
                    subs.append(("PLACE:" + role, 9))
                elif w.step < LAST - 3 * TPD:
                    subs.append(("DIG", st["cfg"]["dig_pr"]))
            if subs:
                seen = set()
                out = []
                for s in subs:
                    if s[0] not in seen:
                        seen.add(s[0])
                        out.append(s)
                tasks[p] = out
    return tasks


# ----------------------------------------------------------------------------- execution
def needs_item(op):
    if op == "FEED": return "WHEAT"
    if op == "FERTILIZE": return "FERTILIZER"
    if op.startswith("PLACE:"): return op.split(":")[1]
    return None


def doable(op, inv, seeds_left, buyable=None):
    item = needs_item(op)
    if item and inv.get(item, 0) <= 0:
        return False
    if op.startswith("PLANT:") and seeds_left.get(op.split(":")[1], 0) <= 0:
        c = op.split(":")[1]
        if not buyable or buyable.get(c, 0) <= 0:
            return False
    return True


def act_on_tile(inv, subs, seeds_left, st):
    for op, pr in subs:
        if not doable(op, inv, seeds_left):
            continue
        if op.startswith("PLANT:"):
            c = op.split(":")[1]
            seeds_left[c] -= 1
            return ["PLANT", c]
        if op.startswith("PLACE:"):
            a = op.split(":")[1]
            inv[a] -= 1
            return ["PLACE", a]
        if op == "FEED":
            inv["WHEAT"] -= 1
        if op == "FERTILIZE":
            inv["FERTILIZER"] -= 1
        return [op]
    return None
