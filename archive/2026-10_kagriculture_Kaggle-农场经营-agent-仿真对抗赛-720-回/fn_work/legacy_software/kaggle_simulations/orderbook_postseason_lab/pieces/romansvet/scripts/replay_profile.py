#!/usr/bin/env python3
"""Profile Kaggle kaggriculture replays into one CSV row per (episode, seat).

Dependency-light: stdlib json/csv/argparse plus numpy (only for the summary
percentiles printed at the end).

Replay semantics (verified against kaggle_environments):
  steps[t]["action"] is the action that produced steps[t]["observation"].
  So the pre-state for action t is steps[t-1]["observation"], and the engine's
  internal `step` counter during that transition is t-1 (day = (t-1)//24).

Money only ever changes in the market phase (SELL / BUY_* / HIRE / BUY_LAND);
the town is NOT a sell channel -- town shops consume from the *shared market
inventory*, which pushes prices up.  We therefore reconstruct income by
re-simulating the engine's per-unit lockstep market phase from the observed
pre-state, and cross-check the reconstruction against the true money deltas.
"""

import argparse
import csv
import json
import math
import os
import sys

# ---------------------------------------------------------------- engine consts
CROPS = {
    "WHEAT":      {"seed": 10},
    "CARROT":     {"seed": 20},
    "TOMATO":     {"seed": 50},
    "STRAWBERRY": {"seed": 100},
    "MELON":      {"seed": 80},
}
ANIMALS = {
    "GOOSE": {"cost": 300, "structure": "COOP"},
    "COW":   {"cost": 400, "structure": "PASTURE"},
    "SHEEP": {"cost": 500, "structure": "PASTURE"},
}
PRODUCTS = ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG", "MILK", "WOOL", "FERTILIZER"]
TOWN_CENTER_PRODUCTS = [p for p in PRODUCTS if p != "FERTILIZER"]
SHOPS = {
    "BAKERY":         ["EGG", "WHEAT"],
    "PIZZA_SHOP":     ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT":    ["EGG", "WHEAT", "STRAWBERRY"],
    "YARN_STORE":     ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"],
    "PET_CAFE":       ["CARROT"],
    "SMOOTHIE_SHOP":  ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
MARKET_I0 = 10000
PRICE_FLOOR = 1
HINGE_GAIN = 8.0
MARKET_PARAMS = {
    "WHEAT":      {"base":  25, "I0": MARKET_I0, "T": 400, "below_func": "sqrt",  "below_target": 0.80, "above_func": "log",    "above_target": 0.20},
    "CARROT":     {"base":  35, "I0": MARKET_I0, "T": 450, "below_func": "hinge", "below_target": 1.00, "above_func": "sqrt",   "above_target": 0.70},
    "TOMATO":     {"base":  60, "I0": MARKET_I0, "T": 200, "below_func": "hinge", "below_target": 0.40, "above_func": "sqrt",   "above_target": 0.60},
    "STRAWBERRY": {"base": 120, "I0": MARKET_I0, "T": 100, "below_func": "sqrt",  "below_target": 0.70, "above_func": "linear", "above_target": 1.60},
    "MELON":      {"base": 250, "I0": MARKET_I0, "T": 300, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.60},
    "EGG":        {"base":  50, "I0": MARKET_I0, "T": 332, "below_func": "hinge", "below_target": 0.40, "above_func": "log",    "above_target": 0.20},
    "MILK":       {"base": 160, "I0": MARKET_I0, "T": 122, "below_func": "sqrt",  "below_target": 0.60, "above_func": "linear", "above_target": 1.60},
    "WOOL":       {"base": 200, "I0": MARKET_I0, "T": 105, "below_func": "log",   "below_target": 0.20, "above_func": "sq",     "above_target": 3.20},
    "FERTILIZER": {"base": 100, "I0": MARKET_I0, "T": 200, "below_func": "linear","below_target": 0.40, "above_func": "linear", "above_target": 0.40},
}
LAND_PRICES = [1000, 2000, 4000]
LAND_ORDER = ["NE", "SW", "SE"]
TURNS_PER_DAY = 24
SHED_CAP = 100
MAX_ORDERS = 10
UNIT_OPS = ["NORTH", "SOUTH", "EAST", "WEST", "PASS", "PICKUP", "PLANT", "WATER", "HARVEST",
            "FERTILIZE", "BUILD_COOP", "BUILD_PASTURE", "DIG", "PLACE", "FEED",
            "COLLECT_FERTILIZER", "CARE", "DROP"]
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def _shape(func, x, T=None):
    x = max(0.0, x)
    if func == "linear": return x
    if func == "sq":     return x * x
    if func == "sqrt":   return math.sqrt(x)
    if func == "log":    return math.log(1.0 + x)
    if func == "log10":  return math.log10(1.0 + x)
    if func == "hinge":
        if not T or T <= 0:
            return x
        u = x / T
        return u + HINGE_GAIN * max(0.0, u - 1.0) ** 2
    return x


_PRICE_CACHE = {}


def market_price(item, inventory):
    key = (item, inventory)
    v = _PRICE_CACHE.get(key)
    if v is not None:
        return v
    p = MARKET_PARAMS[item]
    base, I0, T = p["base"], p["I0"], p["T"]
    if inventory < I0:
        amp = p["below_target"] * base / _shape(p["below_func"], T, T)
        price = base + amp * _shape(p["below_func"], I0 - inventory, T)
    else:
        amp = p["above_target"] * base / _shape(p["above_func"], T, T)
        price = base - amp * _shape(p["above_func"], inventory - I0, T)
    v = max(PRICE_FLOOR, int(round(price)))
    if len(_PRICE_CACHE) < 400000:
        _PRICE_CACHE[key] = v
    return v


# ---------------------------------------------------------------- helpers
def _shed_access(board=10):
    h = board // 2
    return {(h - 1, h - 1), (h, h - 1), (h - 1, h), (h, h)}


SHED_TILES = _shed_access(10)


def _parse_order(order):
    if not isinstance(order, list) or not order:
        return None
    op = order[0]
    if op in ("HIRE", "BUY_LAND"):
        return {"type": op}
    if op in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"):
        if len(order) < 3:
            return None
        try:
            n = int(order[2])
        except (TypeError, ValueError):
            return None
        if n <= 0:
            return None
        return {"type": op, "item": order[1], "remaining": n}
    return None


def _fib(n):
    a, b = 1, 1
    for _ in range(n):
        a, b = b, a + b
    return a


class SeatAcc:
    """Accumulators for one seat of one episode."""

    def __init__(self):
        self.money = []            # per recorded step
        self.hands = []
        self.quads = []
        self.plant = {c: 0 for c in CROPS}
        self.place = {a: 0 for a in ANIMALS}
        self.build = {"COOP": 0, "PASTURE": 0}
        self.ops = {o: 0 for o in UNIT_OPS}
        self.unit_actions = 0
        self.sell_req = {p: 0 for p in PRODUCTS}
        self.sell_exec = {p: 0 for p in PRODUCTS}
        self.sell_rev = {p: 0.0 for p in PRODUCTS}
        self.sell_orders = 0
        self.buy_orders = 0
        self.buy_seed = {c: 0 for c in CROPS}
        self.buy_animal = {a: 0 for a in ANIMALS}
        self.buy_prod = {"WHEAT": 0, "FERTILIZER": 0}
        self.spend_seed = 0.0
        self.spend_animal = 0.0
        self.spend_prod = 0.0
        self.spend_hire = 0.0
        self.spend_land = 0.0
        self.rev_by_day = [0.0] * 31
        self.item_rev_day = {p: [0.0] * 31 for p in PRODUCTS}
        self.item_unit_day = {p: [0] * 31 for p in PRODUCTS}
        # BUY_PRODUCT units per product per day, the buy-side twin of
        # `item_unit_day`. No CSV column reads it -- `scripts/replay_flow.py`
        # needs the buy side at day resolution to build a flow table, and
        # counting it here keeps one reconstruction of the market phase.
        self.item_buy_day = {p: [0] * 31 for p in PRODUCTS}
        self.rev_premium = 0.0     # revenue earned above base price
        self.recon_err = 0.0
        self.hires = 0
        self.quad_day = [None, None, None]
        self.first_day = {}        # threshold -> day
        self.tiles_used = []       # occupied non-weed tiles per day sample
        self.weeds = 0


def profile_replay(path, ours_name="OurTeam"):
    with open(path) as fh:
        rep = json.load(fh)
    info = rep.get("info", {}) or {}
    teams = info.get("TeamNames") or [a.get("Name") for a in info.get("Agents", [])]
    eid = info.get("EpisodeId") or rep.get("id")
    if not teams or len(teams) != 2:
        return []
    if teams[0] == teams[1]:
        sys.stderr.write("skip mirror game %s\n" % path)
        return []
    ours_seat = teams.index(ours_name) if ours_name in teams else None
    steps = rep["steps"]
    n = len(steps)
    rewards = rep.get("rewards") or [None, None]

    accs = [SeatAcc(), SeatAcc()]
    # shared market series
    price_series = {p: [] for p in PRODUCTS}
    inv_series = {p: [] for p in PRODUCTS}
    town_consumed = {p: 0 for p in PRODUCTS}
    shops_by_day = []
    inv_pred_err = 0

    prev_obs0 = None
    prev_priv = None
    for t in range(n):
        s = steps[t]
        obs0 = s[0]["observation"]
        farms = obs0["farms"]
        mk = obs0["market"]
        town = obs0.get("town", {}) or {}
        for p in PRODUCTS:
            price_series[p].append(mk["prices"][p])
            inv_series[p].append(mk["inventory"][p])
        if t % TURNS_PER_DAY == 0:
            shops_by_day.append(list(town.get("unlocked_shops", [])))
        privs = [s[0]["observation"].get("private", {}) or {},
                 s[1]["observation"].get("private", {}) or {}]
        for seat in (0, 1):
            a = accs[seat]
            f = farms[seat]
            a.money.append(float(f["money"]))
            a.hands.append(len(f.get("hands") or []))
            a.quads.append(len(f.get("unlocked_quadrants") or ["NW"]))

        if prev_obs0 is not None:
            day = (t - 1) // TURNS_PER_DAY
            eng_step = t - 1
            prev_farms = prev_obs0["farms"]
            prev_mk = prev_obs0["market"]
            # ---- unit-action counting + tile diffs
            for seat in (0, 1):
                a = accs[seat]
                act = s[seat].get("action") or {}
                if not isinstance(act, dict):
                    act = {}
                units = [act.get("farmer") or ["PASS"]]
                hs = act.get("hands") or []
                if isinstance(hs, list):
                    units.extend([h for h in hs if isinstance(h, list) and h])
                for u in units:
                    if not isinstance(u, list) or not u:
                        continue
                    a.unit_actions += 1
                    op = u[0]
                    if op in a.ops:
                        a.ops[op] += 1
                # tile diffs -> exact plants / builds / animal placements
                pt = prev_farms[seat]["tiles"]
                ct = farms[seat]["tiles"]
                for y in range(10):
                    prow, crow = pt[y], ct[y]
                    if prow == crow:
                        continue
                    for x in range(10):
                        pv, cv = prow[x], crow[x]
                        if pv == cv:
                            continue
                        if isinstance(cv, dict):
                            k = cv.get("kind")
                            if k == "PLANT" and not (isinstance(pv, dict) and pv.get("kind") == "PLANT"):
                                a.plant[cv["crop"]] = a.plant.get(cv["crop"], 0) + 1
                            elif "animal" in cv and not (isinstance(pv, dict) and "animal" in pv):
                                a.place[cv["animal"]] = a.place.get(cv["animal"], 0) + 1
                            elif k in ("COOP", "PASTURE") and not (isinstance(pv, dict) and pv.get("kind") == k):
                                a.build[k] += 1
                            elif k == "WEED" and not (isinstance(pv, dict) and pv.get("kind") == "WEED"):
                                a.weeds += 1
            # ---- market phase reconstruction
            _simulate_market(steps, t, prev_obs0, prev_priv, obs0, accs, day)
            # ---- town consumption (exact, from pre-state shop list)
            prev_town = prev_obs0.get("town", {}) or {}
            shops = prev_town.get("unlocked_shops", []) or []
            if eng_step % 4 == 0:
                for sh in shops:
                    prods = SHOPS.get(sh, [])
                    mult = 2 if len(prods) == 1 else 1
                    for it in prods:
                        town_consumed[it] += mult
            if eng_step % 24 == 0:
                for it in TOWN_CENTER_PRODUCTS:
                    town_consumed[it] += 1

        prev_obs0 = obs0
        prev_priv = privs

    rows = []
    for seat in (0, 1):
        a = accs[seat]
        rows.append(_make_row(path, eid, teams, seat, ours_seat, rewards, a, accs[1 - seat],
                              price_series, inv_series, town_consumed, shops_by_day, n))
    return rows


def _simulate_market(steps, t, prev_obs0, prev_priv, obs0, accs, day):
    """Re-run the engine's lockstep market phase for the transition t-1 -> t."""
    prev_farms = prev_obs0["farms"]
    farms = obs0["farms"]
    mk_inv = dict(prev_obs0["market"]["inventory"])
    sheds = []
    money = []
    for seat in (0, 1):
        priv = prev_priv[seat] if prev_priv else {}
        shed = dict(priv.get("shed", {}) or {})
        invs = [dict(i) for i in (priv.get("inventories") or [{}])]
        act = steps[t][seat].get("action") or {}
        if not isinstance(act, dict):
            act = {}
        units = [act.get("farmer") or ["PASS"]]
        hs = act.get("hands") or []
        if isinstance(hs, list):
            units.extend([h if isinstance(h, list) and h else ["PASS"] for h in hs])
        pf = prev_farms[seat]
        positions = [tuple(pf["farmer"])] + [tuple(p) for p in (pf.get("hands") or [])]
        # apply the shed-touching unit ops so SELL sees the right stock
        for idx, u in enumerate(units):
            if idx >= len(positions) or not isinstance(u, list) or not u:
                continue
            op = u[0]
            pos = positions[idx]
            inv = invs[idx] if idx < len(invs) else {}
            if op == "PICKUP" and len(u) >= 2 and pos in SHED_TILES:
                item = u[1]
                k = int(u[2]) if len(u) >= 3 and str(u[2]).lstrip("-").isdigit() else 1
                k = min(k, shed.get(item, 0))
                if k > 0:
                    shed[item] = shed.get(item, 0) - k
                    inv[item] = inv.get(item, 0) + k
            elif op == "DROP" and pos in SHED_TILES:
                for item, k in list(inv.items()):
                    room = max(0, SHED_CAP - sum(shed.values()))
                    take = min(k, room)
                    if take > 0:
                        shed[item] = shed.get(item, 0) + take
                    del inv[item]
            elif op == "PLACE" and len(u) >= 2:
                item = u[1]
                tile = pf["tiles"][pos[1]][pos[0]]
                is_animal_place = (item in ANIMALS and isinstance(tile, dict)
                                   and tile.get("kind") == ANIMALS[item]["structure"]
                                   and "animal" not in tile)
                if not is_animal_place and pos in SHED_TILES:
                    k = int(u[2]) if len(u) >= 3 and str(u[2]).lstrip("-").isdigit() else 1
                    k = min(k, inv.get(item, 0), max(0, SHED_CAP - sum(shed.values())))
                    if k > 0:
                        inv[item] = inv.get(item, 0) - k
                        shed[item] = shed.get(item, 0) + k
        sheds.append(shed)
        money.append(float(pf["money"]))

    queues = []
    for seat in (0, 1):
        act = steps[t][seat].get("action") or {}
        m = act.get("market", []) if isinstance(act, dict) else []
        q = list(m) if isinstance(m, list) else []
        queues.append(q[:MAX_ORDERS])
        a = accs[seat]
        for o in q[:MAX_ORDERS]:
            po = _parse_order(o)
            if po is None:
                continue
            if po["type"] == "SELL" and po["item"] in a.sell_req:
                a.sell_req[po["item"]] += po["remaining"]
                a.sell_orders += 1
            elif po["type"] in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL"):
                a.buy_orders += 1

    start_money = list(money)
    max_len = max((len(q) for q in queues), default=0)
    for i in range(max_len):
        order_states = []
        for pid, q in enumerate(queues):
            order_states.append(_parse_order(q[i]) if i < len(q) else None)
        for pid, ost in enumerate(order_states):
            # HIRE / BUY_LAND are atomic and priced off state we can read
            # exactly from the observed transition, so they are accounted for
            # below rather than inside this lockstep loop.
            if ost is not None and ost["type"] in ("HIRE", "BUY_LAND"):
                order_states[pid] = None
        while True:
            quoted = [None, None]
            for pid, ost in enumerate(order_states):
                if ost is None or ost["remaining"] <= 0:
                    continue
                op, item = ost["type"], ost["item"]
                if op == "SELL" and item in PRODUCTS:
                    quoted[pid] = (op, item, market_price(item, mk_inv[item]), ost)
                elif op == "BUY_PRODUCT" and item in ("WHEAT", "FERTILIZER"):
                    quoted[pid] = (op, item, market_price(item, mk_inv[item] - 1), ost)
                elif op == "BUY_SEED" and item in CROPS:
                    quoted[pid] = (op, item, CROPS[item]["seed"], ost)
                elif op == "BUY_ANIMAL" and item in ANIMALS:
                    quoted[pid] = (op, item, ANIMALS[item]["cost"], ost)
                else:
                    order_states[pid] = None
            if all(q is None for q in quoted):
                break
            committed = False
            for pid, q in enumerate(quoted):
                if q is None:
                    continue
                op, item, price, ost = q
                a = accs[pid]
                ok = False
                if op == "SELL":
                    if sheds[pid].get(item, 0) > 0:
                        sheds[pid][item] -= 1
                        money[pid] += price
                        a.sell_exec[item] += 1
                        a.sell_rev[item] += price
                        a.rev_by_day[min(30, day)] += price
                        a.item_rev_day[item][min(30, day)] += price
                        a.item_unit_day[item][min(30, day)] += 1
                        a.rev_premium += max(0.0, price - MARKET_PARAMS[item]["base"])
                        if price > 1:
                            mk_inv[item] += 1
                        ok = True
                elif op == "BUY_PRODUCT":
                    if money[pid] >= price and sum(sheds[pid].values()) < SHED_CAP:
                        money[pid] -= price
                        sheds[pid][item] = sheds[pid].get(item, 0) + 1
                        mk_inv[item] -= 1
                        a.buy_prod[item] = a.buy_prod.get(item, 0) + 1
                        a.item_buy_day[item][min(30, day)] += 1
                        a.spend_prod += price
                        ok = True
                elif op == "BUY_SEED":
                    if money[pid] >= price:
                        money[pid] -= price
                        a.buy_seed[item] = a.buy_seed.get(item, 0) + 1
                        a.spend_seed += price
                        ok = True
                elif op == "BUY_ANIMAL":
                    if money[pid] >= price and sum(sheds[pid].values()) < SHED_CAP:
                        money[pid] -= price
                        sheds[pid][item] = sheds[pid].get(item, 0) + 1
                        a.buy_animal[item] = a.buy_animal.get(item, 0) + 1
                        a.spend_animal += price
                        ok = True
                if ok:
                    ost["remaining"] -= 1
                    committed = True
                else:
                    order_states[pid] = None
            if not committed:
                break

    # exact hire / land costs from the observed state transition
    for seat in (0, 1):
        a = accs[seat]
        pf, cf = prev_farms[seat], farms[seat]
        dq = len(cf.get("unlocked_quadrants") or []) - len(pf.get("unlocked_quadrants") or [])
        if dq > 0:
            base = len(pf.get("unlocked_quadrants") or []) - 1
            for k in range(dq):
                if 0 <= base + k < len(LAND_PRICES):
                    a.spend_land += LAND_PRICES[base + k]
                    a.quad_day[base + k] = day
        dh = int(cf.get("hires_today", 0)) - int(pf.get("hires_today", 0))
        if dh > 0:
            prevh = int(pf.get("hires_today", 0))
            for k in range(dh):
                a.spend_hire += _fib(prevh + k)
            a.hires += dh
        actual = float(cf["money"]) - float(pf["money"])
        sim = money[seat] - start_money[seat]
        # hire/land are handled outside the sim; add their exact cost back in
        hire_land = 0.0
        if dq > 0:
            base = len(pf.get("unlocked_quadrants") or []) - 1
            for k in range(dq):
                if 0 <= base + k < len(LAND_PRICES):
                    hire_land += LAND_PRICES[base + k]
        if dh > 0:
            prevh = int(pf.get("hires_today", 0))
            for k in range(dh):
                hire_land += _fib(prevh + k)
        a.recon_err += abs(actual - (sim - hire_land))


def _pct(x, y):
    return 0.0 if not y else 100.0 * x / y


def _make_row(path, eid, teams, seat, ours_seat, rewards, a, opp, price_series,
              inv_series, town_consumed, shops_by_day, n):
    def money_at_day(d):
        idx = min(n - 1, TURNS_PER_DAY * (d + 1) - 1)
        return a.money[idx]

    def hands_on_day(d):
        lo, hi = TURNS_PER_DAY * d, min(n, TURNS_PER_DAY * (d + 1))
        seg = a.hands[lo:hi]
        return max(seg) if seg else 0

    first = {}
    for thr in (10000, 50000, 100000):
        fd = -1
        for i, m in enumerate(a.money):
            if m >= thr:
                fd = i // TURNS_PER_DAY
                break
        first[thr] = fd

    total_rev = sum(a.sell_rev.values())
    total_units = sum(a.sell_exec.values())
    row = {
        "file": os.path.basename(path),
        "episode": eid,
        "seat": seat,
        "team": teams[seat],
        "ours": 1 if ours_seat == seat else 0,
        "opp_team": teams[1 - seat],
        "final_money": rewards[seat] if rewards[seat] is not None else a.money[-1],
        "won": 1 if (rewards[seat] or 0) > (rewards[1 - seat] or 0) else 0,
        "margin": (rewards[seat] or 0) - (rewards[1 - seat] or 0),
    }
    for d in (5, 10, 15, 20, 25):
        row["money_d%d" % d] = money_at_day(d)
    row["money_d29"] = a.money[-1]
    row["first_day_10k"] = first[10000]
    row["first_day_50k"] = first[50000]
    row["first_day_100k"] = first[100000]
    for d in (5, 10, 20, 29):
        row["hands_d%d" % d] = hands_on_day(d)
    row["hands_max"] = max(a.hands) if a.hands else 0
    row["hires_total"] = a.hires
    row["spend_hire"] = round(a.spend_hire, 1)
    row["spend_land"] = round(a.spend_land, 1)
    row["quads_end"] = a.quads[-1]
    for i in range(3):
        row["quad%d_day" % (i + 2)] = a.quad_day[i] if a.quad_day[i] is not None else -1
    for c in CROPS:
        row["plant_%s" % c] = a.plant.get(c, 0)
    row["plant_total"] = sum(a.plant.values())
    for an in ANIMALS:
        row["place_%s" % an] = a.place.get(an, 0)
    row["place_total"] = sum(a.place.values())
    row["build_COOP"] = a.build["COOP"]
    row["build_PASTURE"] = a.build["PASTURE"]
    for op in ("WATER", "HARVEST", "FEED", "CARE", "FERTILIZE", "COLLECT_FERTILIZER",
               "DIG", "PICKUP", "PLACE", "DROP", "PASS", "PLANT"):
        row["op_%s" % op] = a.ops.get(op, 0)
    row["op_MOVE"] = sum(a.ops.get(m, 0) for m in MOVES)
    row["unit_actions"] = a.unit_actions
    row["pass_rate"] = round(_pct(a.ops.get("PASS", 0), a.unit_actions), 2)
    row["move_rate"] = round(_pct(row["op_MOVE"], a.unit_actions), 2)
    row["sell_orders"] = a.sell_orders
    row["buy_orders"] = a.buy_orders
    row["sell_units_total"] = total_units
    row["sell_revenue_total"] = round(total_rev, 1)
    row["spend_seed"] = round(a.spend_seed, 1)
    row["spend_animal"] = round(a.spend_animal, 1)
    row["spend_product"] = round(a.spend_prod, 1)
    row["revenue_premium_share"] = round(_pct(a.rev_premium, total_rev), 2)
    row["recon_err"] = round(a.recon_err, 1)
    row["recon_err_pct_of_rev"] = round(_pct(a.recon_err, max(1.0, total_rev)), 2)
    for p in PRODUCTS:
        # revenue-weighted median day of sale, and the early/late unit split
        rv = a.item_rev_day[p]
        tot_p = sum(rv)
        d50 = -1
        if tot_p > 0:
            acc = 0.0
            for d, v in enumerate(rv):
                acc += v
                if acc >= 0.5 * tot_p:
                    d50 = d
                    break
        row["sellday50_%s" % p] = d50
        row["sellu_early_%s" % p] = sum(a.item_unit_day[p][:16])
        row["sellrev_early_%s" % p] = round(sum(rv[:16]), 1)
        row["sellu_%s" % p] = a.sell_exec[p]
        row["sellrev_%s" % p] = round(a.sell_rev[p], 1)
        row["sellreq_%s" % p] = a.sell_req[p]
        row["revshare_%s" % p] = round(_pct(a.sell_rev[p], max(1.0, total_rev)), 2)
    for c in CROPS:
        row["buyseed_%s" % c] = a.buy_seed.get(c, 0)
    for an in ANIMALS:
        row["buyanimal_%s" % an] = a.buy_animal.get(an, 0)
    row["buyprod_WHEAT"] = a.buy_prod.get("WHEAT", 0)
    row["buyprod_FERTILIZER"] = a.buy_prod.get("FERTILIZER", 0)
    for d in (0, 1, 2, 3):
        lo, hi = d * 8, min(31, d * 8 + 8)
        row["rev_days%d_%d" % (lo, hi - 1)] = round(sum(a.rev_by_day[lo:hi]), 1)
    # shared market summary (identical for both seats of an episode)
    for p in PRODUCTS:
        ps = price_series[p]
        row["price_mean_%s" % p] = round(sum(ps) / len(ps), 1)
        row["price_min_%s" % p] = min(ps)
        for d in (5, 10, 15, 20, 29):
            row["price_d%d_%s" % (d, p)] = ps[min(n - 1, TURNS_PER_DAY * (d + 1) - 1)]
        row["invend_%s" % p] = inv_series[p][-1] - MARKET_I0
        row["towncons_%s" % p] = town_consumed[p]
    row["shops_end"] = len(shops_by_day[-1]) if shops_by_day else 0
    row["shops_list"] = "|".join(sorted(shops_by_day[-1])) if shops_by_day else ""
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--ours", default="OurTeam")
    ap.add_argument("-o", "--out", default="-")
    ap.add_argument("--summary", action="store_true",
                    help="print numeric-column medians for ours vs opponents (numpy)")
    args = ap.parse_args()

    rows = []
    for p in args.paths:
        try:
            rows.extend(profile_replay(p, args.ours))
        except Exception as e:  # noqa: BLE001
            sys.stderr.write("FAILED %s: %r\n" % (p, e))
        sys.stderr.write(".")
        sys.stderr.flush()
    sys.stderr.write("\n")
    if not rows:
        return 1
    fields = list(rows[0].keys())
    out = sys.stdout if args.out == "-" else open(args.out, "w", newline="")
    w = csv.DictWriter(out, fieldnames=fields)
    w.writeheader()
    for r in rows:
        w.writerow(r)
    if args.summary:
        import numpy as np
        ours = [r for r in rows if r["ours"] == 1]
        opps = [r for r in rows if r["ours"] == 0]
        sys.stderr.write("%-30s %12s %12s\n" % ("column", "ours(med)", "opp(med)"))
        for k in fields:
            try:
                a = np.array([float(r[k]) for r in ours], dtype=float)
                b = np.array([float(r[k]) for r in opps], dtype=float)
            except (TypeError, ValueError):
                continue
            sys.stderr.write("%-30s %12.1f %12.1f\n" % (k, np.median(a), np.median(b)))
    if out is not sys.stdout:
        out.close()
        sys.stderr.write("wrote %d rows x %d cols -> %s\n" % (len(rows), len(fields), args.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
