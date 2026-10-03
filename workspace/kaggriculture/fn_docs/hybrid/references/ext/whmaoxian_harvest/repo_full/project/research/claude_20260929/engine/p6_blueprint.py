

# ----------------------------------------------------------------------------- blueprint from a tape
BLUEPRINT = {}


def _bp_spawn(farmer, hands):
    occ = {p: 0 for p in SHED_ADJ}
    for pos in [tuple(farmer)] + [tuple(h) for h in hands]:
        if pos in occ:
            occ[pos] += 1
    return list(min(SHED_ADJ, key=lambda p: (occ[p], SHED_ADJ.index(p))))


def tape_plantings(tape, route_switch=None):
    """Replay unit positions of a 719-step action tape; return {(x,y): [(step, crop), ...]}.
    route_switch: optional (step, tape2) to continue from another tape at that step."""
    out = {}
    farmer = [4, 4]
    hands = []
    mv = {"NORTH": (0, -1), "SOUTH": (0, 1), "EAST": (1, 0), "WEST": (-1, 0)}
    for t in range(min(719, len(tape))):
        src = tape
        if route_switch and t >= route_switch[0]:
            src = route_switch[1]
        a = src[t] if t < len(src) and isinstance(src[t], dict) else {}
        if t % TPD == 0:
            farmer = [4, 4]
            hands = []
        cmds = [a.get("farmer")] + list(a.get("hands") or [])
        units = [farmer] + hands
        for i, c in enumerate(cmds):
            if i >= len(units) or not isinstance(c, list) or not c:
                continue
            pos = units[i]
            if c[0] in mv:
                dx, dy = mv[c[0]]
                nx, ny = pos[0] + dx, pos[1] + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    pos[0], pos[1] = nx, ny
            elif c[0] == "PLANT" and len(c) >= 2:
                out.setdefault((pos[0], pos[1]), []).append((t, c[1]))
            elif c[0] in ("BUILD_COOP", "BUILD_PASTURE"):
                out.setdefault((pos[0], pos[1]), []).append((t, c[0]))
        for o in (a.get("market") or []):
            if isinstance(o, list) and o and o[0] == "HIRE":
                hands.append(_bp_spawn(farmer, hands))
    return out


def blueprint_crop(w, st, p):
    bp = BLUEPRINT.get(w.seat)
    if not bp:
        return None
    ev = [(t, c) for t, c in bp.get(p, ()) if c in CROPS]
    if not ev:
        return ""
    cfg = st["cfg"]
    used = st.setdefault("bp_used", {})
    last = used.get(p, -10 ** 9)
    for t, c in ev:
        if t <= last:
            continue
        if t < w.step - cfg["bp_stale"]:
            continue
        if t > w.step + cfg["bp_ahead"]:
            return ""
        if not cfg["bp_seq"] and t < w.step - cfg["bp_back"]:
            continue
        return c
    return ""


def blueprint_mark(w, st):
    """Record which blueprint event each newly planted tile consumed."""
    bp = BLUEPRINT.get(w.seat)
    if not bp:
        return
    cfg = st["cfg"]
    used = st.setdefault("bp_used", {})
    seen = st.setdefault("bp_seen", {})
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            key = (x, y)
            if isinstance(t, dict) and t.get("kind") == "PLANT":
                tag = (t["crop"], t["planted_day"])
                if seen.get(key) != tag:
                    seen[key] = tag
                    last = used.get(key, -10 ** 9)
                    for et, c in bp.get(key, ()):
                        if et > last and c == t["crop"] and et >= w.step - cfg["bp_stale"] - 24:
                            used[key] = et
                            break


OPP_SELLS = {}


def tape_sells(tape, route_switch=None):
    out = {}
    for t in range(min(719, len(tape))):
        src = tape
        if route_switch and route_switch[1] and t >= route_switch[0]:
            src = route_switch[1]
        a = src[t] if t < len(src) and isinstance(src[t], dict) else {}
        for o in (a.get("market") or []):
            if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL":
                out.setdefault(o[1], []).append((t, int(o[2])))
    return out


def farm_similarity(a, b):
    same = tot = 0
    for y in range(10):
        for x in range(10):
            ta, tb = a[y][x], b[y][x]
            if ta == "LOCKED" and tb == "LOCKED":
                continue
            tot += 1
            ka = (ta.get("crop") or ta.get("animal") or ta.get("kind")) if isinstance(ta, dict) else ta
            kb = (tb.get("crop") or tb.get("animal") or tb.get("kind")) if isinstance(tb, dict) else tb
            same += ka == kb
    return same / float(tot or 1)


def opp_front_run(w, st, item):
    """Units the clone opponent is about to sell of `item` within the front-run horizon."""
    sched = OPP_SELLS.get(w.seat)
    if not sched or not st.get("opp_clone"):
        return 0
    h = st["cfg"]["fr_horizon"]
    return sum(q for t, q in sched.get(item, ()) if w.step < t <= w.step + h)
