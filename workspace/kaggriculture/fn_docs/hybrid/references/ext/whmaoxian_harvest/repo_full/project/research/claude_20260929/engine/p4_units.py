

def tile_weight(t):
    if t is None:
        return 1.0
    if isinstance(t, dict):
        if t.get("animal"):
            return 4.5
        if t.get("kind") == "PLANT":
            return 2.0
        return 1.0
    return 0.0


def compute_zones(w, st, n):
    """Split the owned farm into n angular sectors of similar workload."""
    cells = []
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if t == "LOCKED":
                continue
            ang = math.atan2(y - 4.5, x - 4.5)
            cells.append((ang, (x, y), tile_weight(t)))
    cells.sort()
    total = sum(c[2] for c in cells) or 1.0
    zone = {}
    if n <= 0:
        return zone
    acc = 0.0
    for ang, p, wgt in cells:
        k = min(n - 1, int(acc / total * n))
        zone[p] = k
        acc += wgt
    return zone


def run_units(w, st, tasks):
    cfg = st["cfg"]
    n = len(w.units)
    cmds = [None] * n
    if cfg["harvest_guard"] and w.hour >= cfg["guard_hour"] and w.day < 29:
        load0 = sum(sum(i.values()) for i in w.invs) + sum(w.shed.values())
        if load0 > cfg["night_harvest_cap"]:
            filt = {}
            for p, subs in tasks.items():
                ss = [x for x in subs if not (x[0] == "HARVEST" and x[1] < cfg["decay_pr"])]
                if ss:
                    filt[p] = ss
            tasks = filt
            st["harvest_blocked"] = True
    seeds_left = dict(w.seeds)
    invs = [dict(i) for i in w.invs]
    targets = st["target"]
    for u in list(targets):
        if u >= n or targets[u] not in tasks:
            targets.pop(u, None)
    claimed = {p: u for u, p in targets.items()}
    if st.get("zone_n") != n or st.get("zone_day") != w.day:
        st["zone"] = compute_zones(w, st, n)
        st["zone_n"] = n
        st["zone_day"] = w.day
    zone = st["zone"]
    shed = dict(w.shed)
    n_anim = animal_count(w)
    if cfg["keepers"] and n_anim > 0:
        k_count = max(1, min(n, int(math.ceil(n_anim / float(cfg["keeper_cap"])))))
        keepers = set(range(k_count))
    else:
        keepers = None
    animal_tiles = set()
    for (ax, ay) in [(x, y) for y in range(10) for x in range(10)]:
        tt = w.tiles[ay][ax]
        if isinstance(tt, dict) and (tt.get("animal") or tt.get("kind") in ("COOP", "PASTURE")):
            animal_tiles.add((ax, ay))
    # per-zone needs
    feed_need = [0] * n
    fert_need = [0] * n
    place_need = [dict() for _ in range(n)]
    for p, s in tasks.items():
        z = zone.get(p, 0) if zone.get(p, 0) < n else 0
        for o, _ in s:
            if o == "FEED":
                feed_need[z] += 1
            elif o == "FERTILIZE":
                fert_need[z] += 1
            elif o.startswith("PLACE:"):
                a = o.split(":")[1]
                place_need[z][a] = place_need[z].get(a, 0) + 1
    total_feed = sum(feed_need)
    total_fert = sum(fert_need)
    if keepers is not None:
        share = int(math.ceil(total_feed / float(len(keepers))))
        feed_need = [share if u in keepers else 0 for u in range(n)]
    budget = max(0.0, spendable(w, st))
    buyable = {c: int(budget // CROPS[c]["seed"]) for c in CROPS}

    waits = st.setdefault("waits", {})

    def wait_for_seed(u, p):
        if not any(op.startswith("PLANT:") and buyable.get(op.split(":")[1], 0) > 0 for op, _ in tasks.get(p, ())):
            return False
        k = waits.get(u, (None, 0))
        k = (p, k[1] + 1) if k[0] == p else (p, 1)
        waits[u] = k
        return k[1] <= 2

    def carried(item):
        return sum(i.get(item, 0) for i in invs)

    otw_claim = {}

    def on_the_way(u, pos, inv, tgt):
        if not cfg["otw"] or pos == tgt or pos not in tasks:
            return None
        if claimed.get(pos, u) != u or otw_claim.get(pos, u) != u:
            return None
        subs = [(op, pr) for op, pr in tasks[pos] if pr >= cfg["otw_min"]]
        if not subs:
            return None
        c = act_on_tile(inv, subs, seeds_left, st)
        if c:
            otw_claim[pos] = u
        return c

    end_phase = w.step >= LAST - 14
    free = []
    for u in range(n):
        pos = w.units[u]
        inv = invs[u]
        home = nearest_shed(pos)
        cargo = [k for k, v in inv.items() if v > 0 and k in PRODUCTS and k != "WHEAT"]
        if end_phase and any(v > 0 for v in inv.values()) and LAST - w.step <= dist(pos, home) + 1:
            cmds[u] = ["DROP"] if pos == home else [step_toward(pos, home)]
            targets.pop(u, None)
            continue
        my_feed = max(feed_need[u], 0)
        if pos in SHED_ADJ:
            keep_fert = fert_need[u]
            slack = cfg["carry_slack"]
            if cfg["end_animal"] and (w.day >= 29 or (w.day == 28 and w.hour >= cfg["end_keep_hour"])):
                slack = 0
                my_feed = 0
                keep_fert = 0
            sell_cargo = [k for k in cargo if k != "FERTILIZER" or inv[k] > keep_fert + slack]
            if inv.get("WHEAT", 0) > my_feed + slack:
                sell_cargo.append("WHEAT")
            if sell_cargo and cfg["use_drop"] and my_feed <= 0 and keep_fert <= 0 and not any(inv.get(a, 0) for a in ANIMALS):
                cmds[u] = ["DROP"]
                for k in list(inv):
                    inv[k] = 0
                continue
            if sell_cargo:
                k = max(sell_cargo, key=lambda k: inv[k] * w.prices.get(k, 1))
                q = inv[k] - (keep_fert if k == "FERTILIZER" else (my_feed if k == "WHEAT" else 0))
                cmds[u] = ["PLACE", k, q]
                inv[k] -= q
                continue
            # wheat for my zone's animals (or anyone's if others lack)
            if keepers is not None:
                want_w = my_feed - inv.get("WHEAT", 0)
            else:
                want_w = my_feed - inv.get("WHEAT", 0)
                if want_w > 0:
                    want_w += cfg["pickup_extra"]
                elif total_feed > carried("WHEAT") + cfg["help_deficit"]:
                    want_w = min(6, total_feed - carried("WHEAT"))
                if 0 < want_w < cfg["pickup_min"] and inv.get("WHEAT", 0) > 0:
                    want_w = 0
            if want_w > 0 and shed.get("WHEAT", 0) > 0:
                k = min(shed["WHEAT"], want_w)
                cmds[u] = ["PICKUP", "WHEAT", k]
                shed["WHEAT"] -= k
                inv["WHEAT"] = inv.get("WHEAT", 0) + k
                continue
            want_f = fert_need[u] - inv.get("FERTILIZER", 0)
            if want_f > 0 and (want_f >= cfg["fert_pick_min"] or inv.get("FERTILIZER", 0) == 0):
                want_f += cfg["fert_pick_extra"]
            else:
                want_f = 0
            if want_f > 0 and shed.get("FERTILIZER", 0) > 0:
                k = min(shed["FERTILIZER"], want_f)
                cmds[u] = ["PICKUP", "FERTILIZER", k]
                shed["FERTILIZER"] -= k
                inv["FERTILIZER"] = inv.get("FERTILIZER", 0) + k
                continue
            picked = False
            for a in ANIMALS:
                need_a = place_need[u].get(a, 0) - inv.get(a, 0)
                if need_a <= 0:
                    # help: animals nobody in zone carries
                    tot = sum(pn.get(a, 0) for pn in place_need)
                    need_a = min(1, tot - carried(a))
                if need_a > 0 and shed.get(a, 0) > 0:
                    k = min(shed[a], need_a)
                    cmds[u] = ["PICKUP", a, k]
                    shed[a] -= k
                    inv[a] = inv.get(a, 0) + k
                    picked = True
                    break
            if picked:
                continue
        tgt = targets.get(u)
        if tgt is not None and tgt == pos:
            c = act_on_tile(inv, tasks[tgt], seeds_left, st)
            if c:
                cmds[u] = c
                continue
            if wait_for_seed(u, tgt):
                cmds[u] = ["PASS"]
                continue
            targets.pop(u, None)
            claimed.pop(tgt, None)
        free.append(u)
    # ---- global tiered matching for units that are not acting this turn
    keep = set()
    for u in free:
        p = targets.get(u)
        if (cfg["sticky"] and p is not None and p in tasks and p != w.units[u]
                and any(doable(op, invs[u], seeds_left, buyable) for op, _ in tasks[p])):
            keep.add(u)
            continue
        targets.pop(u, None)
        if p is not None and claimed.get(p) == u:
            claimed.pop(p, None)
    free_match = [u for u in free if u not in keep]
    hours_left = 23 - w.hour
    carried_all = sum(sum(v for k, v in i.items()) for i in invs)
    keep_est = int(animal_count(w) * cfg["wheat_keep_days"]) + 5
    night_risk = carried_all + keep_est > cfg["night_cap"]
    st["night_risk"] = night_risk
    pairs = []
    for u in free_match:
        pos = w.units[u]
        inv = invs[u]
        home = nearest_shed(pos)
        for p, subs in tasks.items():
            if p in claimed:
                continue
            d = dist(pos, p)
            if d > hours_left + 1 and w.hour > 0:
                continue
            if w.step >= LAST - 30 and w.step + d + dist(p, nearest_shed(p)) + 2 > LAST:
                continue
            if keepers is not None and p in animal_tiles and u not in keepers:
                continue
            prs = [pr for op, pr in subs if doable(op, inv, seeds_left, buyable)]
            if not prs:
                continue
            top = max(prs)
            tier = 0 if top >= cfg["tier0"] else (1 if top >= cfg["tier1"] else 2)
            if cfg["soft_tiers"]:
                sc = d - cfg["tier_bonus"][tier] - 0.001 * sum(prs)
            else:
                sc = tier * 1000 + d - 0.001 * sum(prs)
            if zone.get(p) == u:
                sc -= cfg["zone_pull"]
            elif cfg["zone_first"]:
                sc += cfg["zone_first"]
            if keepers is not None and u in keepers and p in animal_tiles:
                sc -= cfg["keeper_pull"]
            pairs.append((sc, u, p))
        # supply trips as pseudo tasks at the nearest shed tile
        dh = dist(pos, home)
        if inv.get("WHEAT", 0) <= 0 and total_feed > carried("WHEAT") and shed.get("WHEAT", 0) > 0 and (keepers is None or u in keepers):
            pairs.append((0 * 1000 + dh + 0.5, u, ("SUPPLY", "WHEAT")))
        if inv.get("FERTILIZER", 0) <= 0 and total_fert > carried("FERTILIZER") and shed.get("FERTILIZER", 0) > 0:
            pairs.append((1 * 1000 + dh + 0.5, u, ("SUPPLY", "FERTILIZER")))
        for a in ANIMALS:
            tot = sum(pn.get(a, 0) for pn in place_need)
            if tot > carried(a) and shed.get(a, 0) > 0 and inv.get(a, 0) == 0:
                pairs.append((1 * 1000 + dh + 0.5, u, ("SUPPLY", a)))
        cargo = [k for k, v in inv.items() if v > 0 and k in PRODUCTS and k not in ("WHEAT", "FERTILIZER")]
        cargo_value = sum(inv[k] * w.prices.get(k, 1) for k in cargo)
        cargo_n = sum(inv[k] for k in cargo) + inv.get("FERTILIZER", 0) + max(0, inv.get("WHEAT", 0) - feed_need[u] - 1)
        cargo_value += max(0, inv.get("WHEAT", 0) - feed_need[u] - 1) * w.prices.get("WHEAT", 30)
        if night_risk and cargo_n >= 3 and w.hour >= cfg["evening_hour"] - dh:
            pairs.append((0 * 1000 + dh - cargo_n, u, ("SUPPLY", "DELIVER")))
        elif cargo_value >= cfg["deliver_value"] or cargo_n >= cfg["deliver_count"]:
            pairs.append((1 * 1000 + dh - cargo_n, u, ("SUPPLY", "DELIVER")))
    pairs.sort(key=lambda x: x[0])
    used = set()
    supply_count = {}
    for sc, u, p in pairs:
        if u in used:
            continue
        if isinstance(p, tuple) and len(p) == 2 and p[0] == "SUPPLY":
            item = p[1]
            lim = 1
            if item == "WHEAT":
                lim = max(1, (total_feed - carried("WHEAT") + 9) // 10)
            if supply_count.get(item, 0) >= lim:
                continue
            supply_count[item] = supply_count.get(item, 0) + 1
            used.add(u)
            pos = w.units[u]
            c = None if (item == "DELIVER" and w.hour >= cfg["guard_hour"]) else on_the_way(u, pos, invs[u], nearest_shed(pos))
            cmds[u] = c if c else [step_toward(pos, nearest_shed(pos))]
            continue
        if p in claimed:
            continue
        used.add(u)
        targets[u] = p
        claimed[p] = u
    for u in free:
        if cmds[u] is not None:
            continue
        pos = w.units[u]
        inv = invs[u]
        tgt = targets.get(u)
        if tgt is None:
            cargo = [k for k, v in inv.items() if v > 0 and k in PRODUCTS and k != "WHEAT"]
            home = nearest_shed(pos)
            if w.step >= LAST - 30 and any(v > 0 for v in inv.values()):
                cmds[u] = ["DROP"] if pos == home else [step_toward(pos, home)]
            else:
                cmds[u] = [step_toward(pos, home)] if (cargo and pos != home) else ["PASS"]
        elif tgt == pos:
            c = act_on_tile(inv, tasks[tgt], seeds_left, st)
            cmds[u] = c if c else ["PASS"]
        else:
            c = on_the_way(u, pos, inv, tgt)
            cmds[u] = c if c else [step_toward(pos, tgt)]
    # ---- hard night-capacity guard: force deliveries when tonight's drop would overflow
    if w.hour >= cfg["guard_hour"]:
        keep = int(animal_count(w) * cfg["wheat_keep_days"]) + 4
        loads = []
        for u in range(n):
            inv = invs[u]
            spare = sum(v for k, v in inv.items() if k in PRODUCTS and k not in ("WHEAT",))
            spare += max(0, inv.get("WHEAT", 0) - feed_need[u])
            loads.append((spare, u))
        load = keep + sum(sum(v for v in invs[u].values()) for u in range(n))
        for spare, u in sorted(loads, reverse=True):
            if load <= cfg["night_target"] or spare <= 0:
                break
            pos = w.units[u]
            home = nearest_shed(pos)
            if dist(pos, home) > 23 - w.hour:
                continue
            inv = invs[u]
            if pos == home:
                items = [k for k, v in inv.items() if v > 0 and k in PRODUCTS and (k != "WHEAT" or v > feed_need[u])]
                if items:
                    k = max(items, key=lambda k: inv[k])
                    q = inv[k] - (feed_need[u] if k == "WHEAT" else 0)
                    cmds[u] = ["PLACE", k, q]
            else:
                cmds[u] = [step_toward(pos, home)]
            targets.pop(u, None)
            load -= spare
    # seed intents: units that will stand on a planting tile within two steps
    intent = {}
    for u, p in targets.items():
        if p not in tasks or u >= n:
            continue
        c = cmds[u]
        npos = w.units[u]
        if c and c[0] in ("NORTH", "SOUTH", "EAST", "WEST"):
            dx, dy = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}[c[0]]
            npos = (npos[0] + dx, npos[1] + dy)
        if dist(npos, p) <= 2:
            for op, _ in tasks[p]:
                if op.startswith("PLANT:"):
                    cr = op.split(":")[1]
                    intent[cr] = intent.get(cr, 0) + 1
                    break
    st["seed_intent"] = intent
    st["seeds_after"] = seeds_left
    return cmds
