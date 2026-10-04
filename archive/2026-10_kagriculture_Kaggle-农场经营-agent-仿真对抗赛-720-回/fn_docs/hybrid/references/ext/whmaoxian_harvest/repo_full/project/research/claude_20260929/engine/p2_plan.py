

# ----------------------------------------------------------------------------- config
DEFAULT = dict(
    open_cows=2, open_sheep=2,
    land_days=(6, 10, 12), land_reserve=(300, 1500, 3000),
    straw_last_day=12, tomato_last_day=19, melon_last_day=0, melon_max=12,
    max_cows=8, max_geese=10, max_sheep_yarn=12,
    goose_from_day=5, goose_last_day=22, cow_last_day=14, sheep_last_day=17,
    max_hands=14, hand_turns=20.0,
    fert_straw=True, fert_tomato=True, fert_wheat=True,
    straw_price_cap=150.0, wheat_keep_days=1.0, sell_lots=5, cash_buffer=20,
    straw_first_day=5, tomato_first_day=6, deliver_value=400.0, zone_bonus=3.0,
    wheat_prebuy_hour=23, day0_hands=4, dig_pr=8, urgent_pr=15,
    milk_min_price=110, wool_min_price=120, cow_base=3, ongoing_harvest_at=2,
    urgency_hours=8.0, tier0=12, tier1=4, zone_pull=1.5, deliver_count=6, evening_hour=19, night_cap=85,
    fert_pr=14, wheat_fert_pr=5, wheat_fast=False, idle_boost=6.0, forward_price=True, supply_weight=0.7, partial_crops=True, plant_stop_steps=40, guard_hour=16, night_target=88, fert_days=3, fert_sell_margin=4, use_blueprint=True, endgame_steps=22, bp_fallback_until=99, keepers=False, keeper_cap=12, zone_first=0, bp_seed_ahead=24, bp_seed_cap=12, bp_seq=True, bp_stale=96, carry_slack=4, pickup_min=2, pickup_extra=2, otw=True, otw_min=3.0, sticky=False, help_deficit=4, fert_pick_min=2, fert_pick_extra=2, soft_tiers=False, tier_bonus=(8, 4, 0), bp_from_day=99, smart_sell=False, hold_items=('WOOL','MILK','STRAWBERRY','MELON','TOMATO','CARROT','EGG'), hold_theta=0.9, peak_window=72, liquidate_steps=24, hold_cap=85, hold_valve_hour=18, front_run=False, fr_horizon=2, clone_sim=0.8, crop_bias={}, harvest_guard=False, night_harvest_cap=80, no_hold_day=28, no_hold_hour=16, end_animal=False, end_keep_hour=12, keeper_pull=3.0, bp_fallback=True, use_drop=True, skip_feed=True, se_tomato_shops=3, se_tomato_from=16, se_tomato_to=18, se_tomato_money=12000, se_max_tiles=25, feed_value_ratio=1.0, feed_labor=10, bp_back=36, bp_ahead=48, fert_buy_max_price=70, seed_buffer=4, ready_pr=12, window_pr=5, decay_pr=20, spare_water_pr=1.5,
)

STATE = {}


def new_state():
    return dict(last=-1, target={}, roles={}, cfg=dict(DEFAULT), melons=0)


# ----------------------------------------------------------------------------- world view
class World:
    def __init__(self, obs):
        self.seat = int(obs.get("player", 0) or 0)
        self.step = int(obs.get("step", 0) or 0)
        self.day = self.step // TPD
        self.hour = self.step % TPD
        farms = obs["farms"]
        self.me = farms[self.seat]
        self.opp = farms[1 - self.seat]
        self.tiles = self.me["tiles"]
        self.money = float(self.me["money"])
        priv = obs.get("private") or {}
        self.shed = {k: int(v) for k, v in (priv.get("shed") or {}).items() if v}
        self.seeds = {k: int(v) for k, v in (priv.get("seeds") or {}).items() if v}
        self.invs = [dict(i or {}) for i in (priv.get("inventories") or [{}])]
        self.units = [tuple(self.me["farmer"])] + [tuple(h) for h in (self.me.get("hands") or [])]
        while len(self.invs) < len(self.units):
            self.invs.append({})
        m = obs.get("market") or {}
        self.prices = {k: int(v) for k, v in (m.get("prices") or {}).items()}
        self.minv = {k: int(v) for k, v in (m.get("inventory") or {}).items()}
        self.shops = list((obs.get("town") or {}).get("unlocked_shops") or [])
        self.quads = list(self.me.get("unlocked_quadrants") or ["NW"])
        self.hires_today = int(self.me.get("hires_today", 0) or 0)

    def owned(self, x, y):
        return self.tiles[y][x] != "LOCKED"

    def demand(self, item):
        d = 1.0 if item != "FERTILIZER" else 0.0
        for s in self.shops:
            p = SHOPS.get(s, ())
            if item in p:
                d += (12.0 if len(p) == 1 else 6.0)
        return d  # units per day


# ----------------------------------------------------------------------------- planning
def _animal_order():
    tiles = [(x, y) for y in range(10) for x in range(10)]
    return sorted(tiles, key=lambda p: (min(dist(p, s) for s in SHED_ADJ), abs(p[0] - 4.5) + abs(p[1] - 4.5), p))


ANIMAL_ORDER = _animal_order()


def herd_counts(w):
    c = {"GOOSE": 0, "COW": 0, "SHEEP": 0}
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if isinstance(t, dict) and t.get("animal") in c:
                c[t["animal"]] += 1
    for a in c:
        c[a] += w.shed.get(a, 0) + sum(inv.get(a, 0) for inv in w.invs)
    return c


def herd_targets(w, st):
    cfg = st["cfg"]
    d = w.day
    shops = w.shops
    yarn = shops.count("YARN_STORE")
    milk_shops = sum(s in ("PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP") for s in shops)
    egg_shops = sum(s in ("BAKERY", "BRUNCH_SPOT") for s in shops)
    cows = cfg["open_cows"]
    if d >= 2:
        cows = min(cfg["max_cows"], cfg["open_cows"] + (d - 1), cfg["cow_base"] + 2 * milk_shops)
        if w.prices.get("MILK", 160) < cfg["milk_min_price"]:
            cows = 0
    sheep = cfg["open_sheep"]
    if yarn and w.prices.get("WOOL", 200) >= cfg["wool_min_price"]:
        sheep = min(cfg["max_sheep_yarn"], cfg["open_sheep"] + 5 * yarn)
    elif d >= 1:
        sheep = 0
    geese = 0
    if d >= cfg["goose_from_day"]:
        geese = min(cfg["max_geese"], 3 + 2 * (d - cfg["goose_from_day"]), 4 + 4 * egg_shops)
    return {"COW": cows if d <= cfg["cow_last_day"] else 0,
            "SHEEP": sheep if d <= cfg["sheep_last_day"] else 0,
            "GOOSE": geese if d <= cfg["goose_last_day"] else 0}


def animal_count(w):
    return sum(1 for y in range(10) for x in range(10)
               if isinstance(w.tiles[y][x], dict) and w.tiles[y][x].get("animal"))


def feed_reserve(w):
    n = animal_count(w) + sum(w.shed.get(a, 0) for a in ANIMALS) + sum(i.get(a, 0) for i in w.invs for a in ANIMALS)
    have = w.shed.get("WHEAT", 0) + sum(i.get("WHEAT", 0) for i in w.invs)
    need = max(0, 2 * n - have)
    return need * (w.prices.get("WHEAT", 25) + 3)


def spendable(w, st):
    return w.money - feed_reserve(w) - st["cfg"]["cash_buffer"]


def assign_animal_roles(w, st):
    roles = st["roles"]
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if isinstance(t, dict) and t.get("kind") in ("COOP", "PASTURE"):
                a = t.get("animal")
                if a:
                    roles[(x, y)] = a
                elif roles.get((x, y)) not in ANIMALS or ANIMALS[roles[(x, y)]]["struct"] != t["kind"]:
                    roles[(x, y)] = "GOOSE" if t["kind"] == "COOP" else "COW"
    counts = {"GOOSE": 0, "COW": 0, "SHEEP": 0}
    for (x, y), r in list(roles.items()):
        if r in ANIMALS:
            t = w.tiles[y][x]
            if t is None or (isinstance(t, dict) and t.get("kind") in ("COOP", "PASTURE", "WEED")):
                counts[r] += 1
            else:
                del roles[(x, y)]
    targets = herd_targets(w, st)
    held = herd_counts(w)
    st["want_more"] = {a: targets[a] > held[a] or w.shed.get(a, 0) + sum(i.get(a, 0) for i in w.invs) > 0 for a in ANIMALS}
    for (x, y), r in list(roles.items()):
        t = w.tiles[y][x]
        if r in ANIMALS and not st["want_more"][r] and not (isinstance(t, dict) and t.get("animal")):
            del roles[(x, y)]
    budget = spendable(w, st)
    for a in ("SHEEP", "COW", "GOOSE"):
        want = max(targets[a], held[a])
        while counts[a] < want:
            if counts[a] >= held[a]:
                # a new animal is needed for this role: only reserve land we can pay for
                if budget < ANIMALS[a]["cost"]:
                    break
                budget -= ANIMALS[a]["cost"] + 2 * (w.prices.get("WHEAT", 25) + 3)
            spot = None
            for p in ANIMAL_ORDER:
                x, y = p
                if not w.owned(x, y) or p in roles:
                    continue
                t = w.tiles[y][x]
                if t is None or (isinstance(t, dict) and t.get("kind") == "WEED"):
                    spot = p
                    break
            if spot is None:
                break
            roles[spot] = a
            counts[a] += 1


def crop_choice(w, st, melon_left=99):
    cfg = st["cfg"]
    d = w.day
    best, bestv = None, 0.0
    budget = spendable(w, st) + sum(CROPS[c]["seed"] * n for c, n in w.seeds.items())
    for c, cd in CROPS.items():
        if cd["seed"] > budget and w.seeds.get(c, 0) <= 0:
            continue
        if c == "MELON" and (d > cfg["melon_last_day"] or melon_left <= 0):
            continue
        if c == "STRAWBERRY" and (d > cfg["straw_last_day"] or d < cfg["straw_first_day"]):
            continue
        if c == "TOMATO" and (d > cfg["tomato_last_day"] or d < cfg["tomato_first_day"]):
            continue
        if d < cfg["straw_first_day"] and c not in ("WHEAT", "MELON"):
            continue
        if c == "WHEAT":
            span, units = (3, 5) if (cfg["fert_wheat"] and cfg["wheat_fast"]) else (4, 6 if cfg["fert_wheat"] else 4)
        elif c == "CARROT":
            span, units = 3, 3
        elif c == "MELON":
            span, units = 10, 6
        elif c == "TOMATO":
            span, units = 11, 8 if cfg["fert_tomato"] else 4
        else:
            span, units = 16, 8 if cfg["fert_straw"] else 4
        if (d + span) * TPD + 18 > LAST:
            if c in ("WHEAT", "CARROT") and cfg["partial_crops"]:
                # latest harvest age that still leaves time to deliver
                a = min(cd["maxd"], (LAST - 8) // TPD - d)
                if a < cd["first"]:
                    continue
                ws = (cd["maxd"] + 1) // 2
                wdays = max(0, a - ws + 1)
                units = min(cd["cap"], 1 + wdays * (2 if (c == "WHEAT" and cfg["fert_wheat"] and a >= 3) else 1))
                span = a
            elif c in ("TOMATO", "STRAWBERRY"):
                first = cd["first"]
                nprod = 0
                for k in range(4):
                    pday = d + first - 1 + k * cd.get("interval", 1)
                    if (pday + 1) * TPD + 16 <= LAST:
                        nprod += 1
                if nprod == 0:
                    continue
                units = units * nprod / 4.0
                span = max(1.0, (LAST - w.step) / TPD)
            else:
                continue
        p = future_price(w, st, c, span * 0.8)
        if c == "STRAWBERRY":
            p = min(p, cfg["straw_price_cap"])
        v = (units * p * cfg["crop_bias"].get(c, 1.0) - cd["seed"]) / (span + 1.0)
        if v > bestv:
            best, bestv = c, v
    return best


def fert_demand(w, st, days=2):
    cfg = st["cfg"]
    need = 0
    for y in range(10):
        for x in range(10):
            t = w.tiles[y][x]
            if not (isinstance(t, dict) and t.get("kind") == "PLANT"):
                continue
            c = t["crop"]
            cd = CROPS[c]
            if cd["ongoing"]:
                if not ((c == "STRAWBERRY" and cfg["fert_straw"]) or (c == "TOMATO" and cfg["fert_tomato"])):
                    continue
                for dd in range(days):
                    day = w.day + dd
                    k = day + 1 - t["planted_day"] - cd["first"]
                    if k >= 0 and k % cd["interval"] == 0 and k // cd["interval"] + 1 <= 4 and t["fertilized_until_day"] < day:
                        need += 1
                        break
            elif c == "WHEAT" and cfg["fert_wheat"]:
                age = w.day - t["planted_day"]
                if age in (1, 2) and t["fertilized_until_day"] < w.day + 1:
                    need += 1
    return need


def pipeline_supply(w, crop, days):
    """Units of crop expected to reach the market within `days` from both farms' visible plants."""
    cd = CROPS[crop]
    tot = 0.0
    for farm in (w.me, w.opp):
        for row in farm["tiles"]:
            for t in row:
                if not (isinstance(t, dict) and t.get("kind") == "PLANT" and t.get("crop") == crop):
                    continue
                age = w.day - t["planted_day"]
                if cd["ongoing"]:
                    for k in range(4):
                        pa = cd["first"] - 1 + k * cd["interval"]
                        if age <= pa <= age + days:
                            tot += 1.6
                    tot += t.get("yield_units", 0)
                else:
                    ready = 10 if crop == "MELON" else cd["maxd"]
                    if ready - age <= days:
                        tot += max(t.get("yield_units", 1), 3 if crop != "MELON" else 6)
    return tot


def future_price(w, st, crop, days):
    cfg = st["cfg"]
    if not cfg["forward_price"]:
        return w.prices.get(crop, MP[crop][0])
    inv = w.minv.get(crop, 10000)
    drain = w.demand(crop) * days
    supply = pipeline_supply(w, crop, days)
    return price_at(crop, inv - drain + supply * cfg["supply_weight"])
