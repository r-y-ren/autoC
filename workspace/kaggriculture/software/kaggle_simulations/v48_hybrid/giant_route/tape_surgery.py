# -*- coding: utf-8 -*-
# 【中文】tape_surgery.py —— R9-G2 perform_tape_surgery（map_events_to_tape +
# rebuild_tape_routes）
# ===========================================================================
# 职责（fn_docs/responsibility.md R9 增补）：
#   perform_tape_surgery：把 giant_route/target_schedule.json 的产线排程映射为
#   v48 磁带产线事件手术——解码基底路由（v48_derivative/main.py 内嵌
#   _V48_ROUTES blob），对 BUY/BUILD/HIRE/种植事件改写；反应层/卖单面不动。
#   - map_events_to_tape [L1]：排程 → 磁带事件差分集（逐条 {route, day, kind,
#     item, original, target}）。
#   - rebuild_tape_routes [L1]：重编码受影响路由段并保一致性（事件点/路由
#     切换结构不变=六路由键序/719 长度/88-120-153-216 切换逻辑全不触碰；
#     SELL 订单逐字节保留；移动动词逐字节保留）。
# 引擎语义要点（vendored kaggle_environments 1.32.7 实读）：
#   * 非法动作静默 no-op；PICKUP 取 min(n, 棚存)；PLACE 动物需站在匹配空置
#     结构上；PLANT 需种子+空地+同步入种子校验（超发整步丢弃）；
#   * 动物 2 个连续未喂日出逃；产出=每间隔 base 1 + care 加成（喂+护同日
#     才积累/消耗）→ 喂养面是收入核心；
#   * FEED 需执行实体当日自带 WHEAT（棚区 PICKUP）；CARE/HARVEST/
#     COLLECT_FERTILIZER 无库存要求；
#   * EOD：farmer 归位 (4,4)、hands 清空、实体库存落棚、shop 每 3 日解锁。
# 手术架构：
#   * 事件面：HIRE 重写（10 单/步上限）/BUY_ANIMAL/BUY_LAND/BUY_SEED+PLANT
#     计数对齐（STRAWBERRY/CARROT 线清零，槽回收进场址池）；
#   * 动物流：傍晚买 → 次日晨 PICKUP → 行走上 (BUILD, PLACE) 相邻对落位；
#     既有 15-16 对复用，缺口用场址池（麦轮 (PLANT,WATER) 对/草莓对/
#     (PASS,PASS) 停留对，按目标土地解锁日校验）；
#   * 喂养面：新场址 tile 上，把原行走动作翻转 FEED/CARE（隔日 HARVEST），
#     执行实体须当日经停棚区（FEED 需带麦）；其棚区槽翻为 PICKUP WHEAT。
# 确定性：纯函数 + 固定序；双跑一致由 CLI 自证。
# CLI：python tape_surgery.py → giant_route/{routes_surgered,surgery_diff,
#   surgery_report}.json
# ===========================================================================
from __future__ import annotations

import argparse
import base64
import collections
import copy
import hashlib
import json
import os
import re
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
KSIM = os.path.dirname(HYBRID)
BASE_MAIN = os.path.join(KSIM, "v48_derivative", "main.py")
SCHEDULE = os.path.join(HERE, "target_schedule.json")

N_STEPS = 719
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]
ANIMAL_KINDS = ("SHEEP", "COW", "GOOSE")
MAX_ORDERS = 10
ROUTE_ORDER = ("default", "yarn_fast", "farm_fast", "yarn_second",
               "yarn_third", "bakery_capital")


# ---------------------------------------------------------------------------
# 解码/编码
# ---------------------------------------------------------------------------
_ROUTES_RE = re.compile(
    r"_V48_ROUTES = json\.loads\(zlib\.decompress\(base64\.b85decode\(\n\(\n"
    r"(.*?)"
    r"\n\)\n\)\)\.decode\(\"utf-8\"\)\)",
    re.S,
)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def decode_routes(base_path: str = BASE_MAIN):
    base_text = open(base_path, "r", encoding="utf-8").read()
    m = _ROUTES_RE.search(base_text)
    if not m:
        raise SystemExit("base _V48_ROUTES blob not found")
    blob = "".join(re.findall(r"'([^']*)'", m.group(1)))
    routes = json.loads(zlib.decompress(base64.b85decode(blob)).decode("utf-8"))
    if any(len(v) != N_STEPS for v in routes.values()) or len(routes) != 6:
        raise SystemExit("unexpected route shape")
    return routes, base_text, m.span(1)


def encode_routes(routes):
    payload = json.dumps(routes, ensure_ascii=True,
                         separators=(",", ":")).encode("ascii")
    text = base64.b85encode(zlib.compress(payload, 9)).decode("ascii")
    return "\n".join(f"    '{text[i:i + 78]}'"
                     for i in range(0, len(text), 78)), payload


# ---------------------------------------------------------------------------
# 行走模拟（引擎语义：EOD 归位/hands 清零/雇佣次步生效/边界夹紧）
# ---------------------------------------------------------------------------
def spawn_hand(pos_list):
    occ = {t: 0 for t in SHED_TILES}
    for p in pos_list:
        p = tuple(p)
        if p in occ:
            occ[p] += 1
    best = sorted(occ.items(),
                  key=lambda kv: (kv[1], SHED_TILES.index(kv[0])))
    return list(best[0][0])


def simulate_positions(route, hires_per_day):
    farmer = [4, 4]
    hands = []
    positions = []
    pending_hires = 0
    for i in range(N_STEPS):
        if i % 24 == 0:
            farmer = [4, 4]
            hands = []
            pending_hires = 0
        while pending_hires > 0 and len(hands) < hires_per_day.get(i // 24, 0):
            hands.append(spawn_hand([farmer] + hands))
            pending_hires -= 1
        f = route[i]["farmer"]
        if isinstance(f, list) and f and f[0] in MOVES:
            dx, dy = MOVES[f[0]]
            nx, ny = farmer[0] + dx, farmer[1] + dy
            if 0 <= nx < 10 and 0 <= ny < 10:
                farmer = [nx, ny]
        for hi, ha in enumerate(route[i]["hands"]):
            if hi >= len(hands):
                break
            if not isinstance(ha, list) or not ha:
                continue
            if ha[0] in MOVES:
                dx, dy = MOVES[ha[0]]
                nx, ny = hands[hi][0] + dx, hands[hi][1] + dy
                if 0 <= nx < 10 and 0 <= ny < 10:
                    hands[hi] = [nx, ny]
        positions.append([tuple(farmer)] + [tuple(h) for h in hands])
        n_hire = sum(1 for o in route[i]["market"] if o[0] == "HIRE")
        room = max(0, hires_per_day.get(i // 24, 0)
                   - len(hands) - pending_hires)
        pending_hires += min(n_hire, room)
    return positions


def action_at(route, step, who):
    if who == 0:
        a = route[step]["farmer"]
    else:
        hs = route[step]["hands"]
        a = hs[who - 1] if who - 1 < len(hs) else None
    return a if isinstance(a, list) and a else None


def unlocked(tile, day, land_days):
    x, y = tile
    q = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
    if q == "NW":
        return True
    idx = {"NE": 0, "SW": 1, "SE": 2}[q]
    return idx < len(land_days) and day >= land_days[idx]


# ---------------------------------------------------------------------------
# 事件提取与差分（map_events_to_tape）
# ---------------------------------------------------------------------------
def extract_events(route):
    ev = []
    for day in range(30):
        lo, hi = day * 24, min(day * 24 + 24, N_STEPS)
        rec = {"day": day, "hires": 0,
               "buys": collections.Counter(), "land": 0,
               "seeds": collections.Counter(),
               "plants": collections.Counter(),
               "builds": 0, "places": collections.Counter(),
               "animal_pickups": collections.Counter()}
        for t in range(lo, hi):
            for o in route[t]["market"]:
                if o[0] == "HIRE":
                    rec["hires"] += 1
                elif o[0] == "BUY_ANIMAL":
                    rec["buys"][o[1]] += o[2]
                elif o[0] == "BUY_LAND":
                    rec["land"] += 1
                elif o[0] == "BUY_SEED":
                    rec["seeds"][o[1]] += o[2]
            for who in range(0, 16):
                a = action_at(route, t, who)
                if a is None:
                    continue
                if a[0] == "PLANT":
                    rec["plants"][a[1]] += 1
                elif a[0] == "BUILD_PASTURE":
                    rec["builds"] += 1
                elif a[0] == "PLACE" and len(a) > 1 and a[1] in ANIMAL_KINDS:
                    rec["places"][a[1]] += 1
                elif a[0] == "PICKUP" and len(a) > 2 and a[1] in ANIMAL_KINDS:
                    rec["animal_pickups"][a[1]] += a[2]
        for k in ("buys", "seeds", "plants", "places", "animal_pickups"):
            rec[k] = dict(rec[k])
        ev.append(rec)
    return ev


def schedule_days(schedule):
    out = []
    for e in schedule["daily_events"]:
        out.append({"day": e["day"], "hires": e.get("hire", 0),
                    "buys": dict(e.get("buy_animals", {})),
                    "land": len(e.get("buy_land", [])),
                    "plants": dict(e.get("plant", {}))})
    return out


def map_events_to_tape(routes, schedule):
    tgt = schedule_days(schedule)
    diffs = []
    for name in ROUTE_ORDER:
        orig = extract_events(routes[name])
        for o, t in zip(orig, tgt):
            d = o["day"]
            for key in ("hires", "land"):
                if o[key] != t[key]:
                    diffs.append({"route": name, "day": d, "kind": key,
                                  "original": o[key], "target": t[key]})
            for kind in ("buys", "plants"):
                item_map = {"MELON_tiles": "MELON", "WHEAT_step_to_add": "WHEAT"}
                keys = set(o[kind]) | set(t[kind])
                for k in keys:
                    ov = o[kind].get(k, 0)
                    nv = t[kind].get(k, 0)
                    item = item_map.get(k, k)
                    if ov != nv:
                        diffs.append({"route": name, "day": d, "kind": kind,
                                      "item": item, "original": ov,
                                      "target": nv})
    return diffs


# ---------------------------------------------------------------------------
# 手术（rebuild_tape_routes）
# ---------------------------------------------------------------------------
class Surgery:
    """单路由产线事件手术；所有落点经位置模拟器验证。"""

    def __init__(self, name, route, schedule, log, site_blacklist=None):
        self.name = name
        self.route = copy.deepcopy(route)
        self.tgt = schedule_days(schedule)
        self.log = log
        self.hires = {t["day"]: t["hires"] for t in self.tgt}
        # 目标土地购买日序（NE→SW→SE 顺序即购买序）
        self.land_days = [t["day"] for t in self.tgt if t["land"] > 0]
        self.positions = simulate_positions(self.route, self.hires)
        self.site_blacklist = site_blacklist or set()

    # -- 基础 -------------------------------------------------------------
    def who_range(self, day):
        return range(0, self.hires[day] + 1)

    def tile_of(self, step, who):
        pos = self.positions[step]
        return pos[who] if who < len(pos) else None

    def day_steps(self, day):
        return range(day * 24, min(day * 24 + 24, N_STEPS))

    def nonmove_slots(self, day):
        out = []
        for t in self.day_steps(day):
            for who in self.who_range(day):
                a = action_at(self.route, t, who)
                if a is None or a[0] in MOVES:
                    continue
                out.append((t, who, a[0], a[1] if len(a) > 1 else None,
                            self.tile_of(t, who)))
        return out

    def set_action(self, step, who, new_action, reason):
        old = action_at(self.route, step, who)
        if new_action is None or (old is not None and list(new_action) == old):
            return
        if who == 0:
            self.route[step]["farmer"] = list(new_action)
        else:
            self.route[step]["hands"][who - 1] = list(new_action)
        self.log.append({"route": self.name, "day": step // 24, "step": step,
                         "who": who, "op": "replace",
                         "original": old, "new": list(new_action),
                         "reason": reason})

    def market_room(self, step):
        return MAX_ORDERS - len(self.route[step]["market"])

    # -- E1 HIRE ----------------------------------------------------------
    def rewrite_hires(self):
        for day in range(30):
            want = self.hires[day]
            for t in self.day_steps(day):
                m = self.route[t]["market"]
                keep = [o for o in m if o[0] != "HIRE"]
                if len(keep) != len(m):
                    self.log.append({"route": self.name, "day": day,
                                     "step": t, "who": None, "op": "hire_reset",
                                     "original": None, "new": None,
                                     "reason": "clear HIRE"})
                self.route[t]["market"] = keep
            inserted = 0
            for t in self.day_steps(day):
                if inserted >= want:
                    break
                n = min(self.market_room(t), want - inserted)
                if n > 0:
                    self.route[t]["market"].extend([["HIRE"]] * n)
                    inserted += n
                    self.log.append({"route": self.name, "day": day,
                                     "step": t, "who": None,
                                     "op": "hire_insert", "original": None,
                                     "new": n, "reason": f"crew={want}"})
            if inserted != want:
                raise SystemExit(f"{self.name} d{day}: hire capacity short")

    # -- E2/E3 市场买单 -----------------------------------------------------
    def edit_buys(self):
        for day in range(30):
            t = self.tgt[day]
            lo, hi = day * 24, min(day * 24 + 24, N_STEPS)
            want = collections.Counter(t["buys"])
            steps = [s for s in range(lo, hi)
                     if any(o[0] == "BUY_ANIMAL"
                            for o in self.route[s]["market"])]
            for s in range(lo, hi):
                m = self.route[s]["market"]
                keep = [o for o in m if o[0] != "BUY_ANIMAL"]
                if len(keep) != len(m):
                    for o in m:
                        if o[0] == "BUY_ANIMAL":
                            self.log.append({"route": self.name, "day": day,
                                             "step": s, "who": None,
                                             "op": "delete", "original": o,
                                             "new": None,
                                             "reason": "animal buy rewrite"})
                self.route[s]["market"] = keep
            slots = list(steps)
            need = sum(want.values())
            if day == 0:
                cand = range(lo, hi)             # d0 兜底升序（晨购）
            else:
                cand = range(hi - 1, lo - 1, -1)  # 其余日兜底降序（傍晚）
            for s in cand:
                if len(slots) >= need:
                    break
                if s not in slots and self.market_room(s) > 0:
                    slots.append(s)
            if day == 0:
                slots.sort()               # d0 晨购晨落（基底同日形态）
                take = lambda: slots.pop(0)
            else:
                slots.sort(reverse=True)   # 傍晚购次日晨落
                take = lambda: slots.pop()
            for kind in ANIMAL_KINDS:
                n = want.get(kind, 0)
                while n > 0 and slots:
                    s = take()
                    order = ["BUY_ANIMAL", kind, n]
                    self.route[s]["market"].append(order)
                    self.log.append({"route": self.name, "day": day,
                                     "step": s, "who": None, "op": "insert",
                                     "original": None, "new": order,
                                     "reason": "animal buy rewrite"})
                    n = 0
                if n > 0:
                    raise SystemExit(f"{self.name} d{day}: buy slot short")
            # BUY_LAND：目标日重排（购买序=land_days 序）
            for s in range(N_STEPS):
                m = self.route[s]["market"]
                keep = [o for o in m if o[0] != "BUY_LAND"]
                if len(keep) != len(m):
                    self.log.append({"route": self.name, "day": s // 24,
                                     "step": s, "who": None, "op": "delete",
                                     "original": ["BUY_LAND"], "new": None,
                                     "reason": "land day rewrite"})
                self.route[s]["market"] = keep
            for d in self.land_days:
                for s in self.day_steps(d):
                    if self.market_room(s) > 0:
                        self.route[s]["market"].append(["BUY_LAND"])
                        self.log.append({"route": self.name, "day": d,
                                         "step": s, "who": None,
                                         "op": "insert", "original": None,
                                         "new": ["BUY_LAND"],
                                         "reason": "land day rewrite"})
                        break

    # -- 种植面 -------------------------------------------------------------
    def edit_plants(self):
        """MELON/WHEAT 排程锚日计数对齐；STRAWBERRY/CARROT 清零。
        返回（strawberry 槽, 全作物 (PLANT,X) 相邻对）场址池。"""
        straw_pool = collections.defaultdict(list)
        pair_pool = collections.defaultdict(list)
        tgt_plants = {}
        for t in self.tgt:
            pl = {}
            if t["plants"].get("MELON_tiles"):
                pl["MELON"] = t["plants"]["MELON_tiles"]
            if t["plants"].get("WHEAT_step_to_add"):
                pl["WHEAT"] = t["plants"]["WHEAT_step_to_add"]
            tgt_plants[t["day"]] = pl
        for day in range(30):
            hi = min(day * 24 + 24, N_STEPS)
            slots = self.nonmove_slots(day)
            plants_now = collections.Counter()
            for (t, who, verb, arg, tile) in slots:
                if verb == "PLANT":
                    plants_now[arg] += 1
            want = tgt_plants.get(day, {})
            # 1) STRAWBERRY/CARROT 清零 + 场址回收
            for (t, who, verb, arg, tile) in slots:
                if verb == "PLANT" and arg in ("STRAWBERRY", "CARROT"):
                    a2 = action_at(self.route, t + 1, who) if t + 1 < hi else None
                    if (a2 is not None and a2[0] not in MOVES
                            and self.tile_of(t + 1, who) == tile
                            and tile is not None):
                        straw_pool[day].append((t, who, tile))
                    else:
                        self.set_action(t, who, ["PASS"],
                                        "crop line removed (schedule)")
            # 2) 排程锚日 MELON/WHEAT 计数对齐
            for crop in ("MELON", "WHEAT"):
                target = want.get(crop)
                if target is None:
                    continue
                have = plants_now.get(crop, 0)
                if have > target:
                    k = have - target
                    for (t, who, verb, arg, tile) in reversed(slots):
                        if k <= 0:
                            break
                        if verb == "PLANT" and arg == crop:
                            self.set_action(t, who, ["PASS"],
                                            f"{crop} day-count trim")
                            k -= 1
                elif have < target:
                    k = target - have
                    used = {tile for (t, who, verb, arg, tile) in slots
                            if verb == "PLANT"}
                    for (t, who, verb, arg, tile) in slots:
                        if k <= 0:
                            break
                        if tile is None or tile in used or not unlocked(
                                tile, day, self.land_days):
                            continue
                        if verb == "PASS" or (verb == "PLANT" and arg in
                                              ("STRAWBERRY", "CARROT")):
                            self.set_action(t, who, ["PLANT", crop],
                                            f"{crop} day-count add")
                            used.add(tile)
                            k -= 1
        # 3) 相邻对场址池（任意 (PLANT@t, 非移动@t+1 同实体同 tile)）
        for day in range(30):
            hi = min(day * 24 + 24, N_STEPS)
            for t in range(day * 24, hi - 1):
                for who in self.who_range(day):
                    a1 = action_at(self.route, t, who)
                    a2 = action_at(self.route, t + 1, who)
                    if not a1 or not a2 or a1[0] != "PLANT":
                        continue
                    if a2[0] in MOVES:
                        continue
                    tile = self.tile_of(t, who)
                    if tile is not None and self.tile_of(t + 1, who) == tile \
                            and unlocked(tile, day, self.land_days) \
                            and tile not in self.site_blacklist:
                        pair_pool[day].append((t, who, tile))
        return straw_pool, pair_pool

    def edit_seeds(self):
        for day in range(30):
            demand = collections.Counter()
            for t in self.day_steps(day):
                for who in range(0, 16):
                    a = action_at(self.route, t, who)
                    if a and a[0] == "PLANT":
                        demand[a[1]] += 1
            for s in self.day_steps(day):
                m = self.route[s]["market"]
                keep = []
                for o in m:
                    if o[0] == "BUY_SEED":
                        self.log.append({"route": self.name, "day": day,
                                         "step": s, "who": None, "op": "delete",
                                         "original": o, "new": None,
                                         "reason": "seed rewrite"})
                    else:
                        keep.append(o)
                self.route[s]["market"] = keep
            for crop in ("WHEAT", "MELON"):
                n = demand.get(crop, 0)
                for s in self.day_steps(day):
                    if n <= 0:
                        break
                    if self.market_room(s) > 0:
                        self.route[s]["market"].append(["BUY_SEED", crop, n])
                        self.log.append({"route": self.name, "day": day,
                                         "step": s, "who": None, "op": "insert",
                                         "original": None,
                                         "new": ["BUY_SEED", crop, n],
                                         "reason": "seed rewrite"})
                        n = 0
                if n > 0:
                    raise SystemExit(f"{self.name} d{day}: seed room short")

    def shed_slot_before(self, day, who, before_step, exclude=(),
                         wheat_ok=False):
        """实体 who 在日内的棚区非移动槽（step < before_step），供 PICKUP。
        默认不占用 PICKUP WHEAT（喂养载麦基础设施）；排除已用 step。"""
        best = wheat = None
        for (t, w, verb, arg, tile) in self.nonmove_slots(day):
            if w != who or t >= before_step or t in exclude:
                continue
            if not (tile in SHED_TILES):
                continue
            if verb in ("PASS", "DROP"):
                best = best or (t, verb, arg)
            elif verb == "PICKUP" and arg in ANIMAL_KINDS:
                return (t, verb, arg)          # 基底动物面槽优先
            elif verb == "PICKUP" and arg == "WHEAT":
                wheat = wheat or (t, verb, arg)
        return best or (wheat if wheat_ok else None)

    # -- 动物流 -------------------------------------------------------------
    def collect_pairs(self):
        pairs = collections.defaultdict(list)
        for t in range(N_STEPS - 1):
            day = t // 24
            for who in self.who_range(day):
                a1 = action_at(self.route, t, who)
                a2 = action_at(self.route, t + 1, who)
                if (a1 and a2 and a1[0] == "BUILD_PASTURE"
                        and a2[0] == "PLACE" and len(a2) > 1
                        and a2[1] in ANIMAL_KINDS
                        and self.tile_of(t, who) == self.tile_of(t + 1, who)):
                    pairs[day].append((t, who))
        return pairs

    def edit_animals(self, straw_pool, pair_pool):
        pairs = self.collect_pairs()
        buys = {}
        for day in range(30):
            c = collections.Counter()
            for s in self.day_steps(day):
                for o in self.route[s]["market"]:
                    if o[0] == "BUY_ANIMAL":
                        c[o[1]] += o[2]
            buys[day] = c
        shed = collections.Counter()
        placed_log = []                     # (day, t, who, kind, tile, src)
        used = set()
        occupied = set()                    # 已落位 tile
        built = {}                          # tile -> 首建日（含未用基底对）
        for d, pl in pairs.items():
            for (t, who) in pl:
                tile = self.tile_of(t + 1, who)
                if tile is not None:
                    built.setdefault(tile, d)
        unplaced = collections.Counter()
        pickups = {}                        # (day, who) -> [kind, n, first_t, slot]
        for day in range(30):
            pending = collections.Counter(shed)
            if day == 0:
                pending += buys[0]
            elif day > 1:
                pending += buys[day - 1]      # d0 买单已当日消化，d1 不重计
            shed = collections.Counter()
            day_pairs = [p for p in pairs.get(day, []) if p not in used]
            straw = [(t, who, tile) for (t, who, tile) in straw_pool.get(day, [])
                     if (t, who) not in used
                     and tile not in self.site_blacklist]
            wheat_pairs = [(t, who, tile)
                           for (t, who, tile) in pair_pool.get(day, [])
                           if (t, who) not in used
                           and tile not in self.site_blacklist]

            def carrier_has(kind, who, t_place, n):
                """实体当日是否有棚区槽先于落位步（载畜可行性；
                畜种分槽，不占喂养载麦槽）。"""
                key = (day, who, kind)
                if key in pickups and pickups[key][2] < t_place:
                    return True
                excl = {v[3] for k, v in pickups.items()
                        if k[0] == day and k[1] == who}
                sl = self.shed_slot_before(day, who, t_place, exclude=excl)
                if sl is None and day <= 1:
                    # d0/d1 兜底：允许占用载麦槽（当日喂养面小，1 日未喂
                    # 不致出逃——引擎 2 连日未喂才逃）
                    sl = self.shed_slot_before(day, who, t_place,
                                               exclude=excl, wheat_ok=True)
                if sl is None:
                    return False
                pickups[key] = [kind, 0, t_place, sl[0]]
                return True

            def place_one(t, who, tile, kind, src):
                key = (day, who, kind)
                if key in pickups:
                    pickups[key][1] += 1
                placed_log.append((day, t, who, kind, tile, src))
                occupied.add(tile)

            for src_name, src in (("base", day_pairs), ("site", straw),
                                  ("site", wheat_pairs)):
                for item in src:
                    kind = next((k for k in ANIMAL_KINDS if pending[k] > 0),
                                None)
                    if kind is None:
                        break
                    if len(item) == 3:
                        t, who, tile = item
                        if tile is None or not unlocked(tile, day,
                                                       self.land_days):
                            continue
                        if tile in occupied:
                            continue
                        if action_at(self.route, t, who)[0] != "PLANT":
                            continue
                        if not carrier_has(kind, who, t + 1, 1):
                            continue
                        self.set_action(t, who, ["BUILD_PASTURE"],
                                        "pasture site (plant pair)")
                        self.set_action(t + 1, who, ["PLACE", kind],
                                        "animal place (site pair)")
                        used.add((t, who))
                        built[tile] = day
                        place_one(t + 1, who, tile, kind, src_name)
                        pending[kind] -= 1
                    else:
                        t, who = item
                        tile = self.tile_of(t + 1, who)
                        if tile in occupied or tile is None:
                            continue
                        if not carrier_has(kind, who, t + 1, 1):
                            continue
                        a2 = action_at(self.route, t + 1, who)
                        if a2 and a2[1] != kind:
                            self.set_action(t + 1, who, ["PLACE", kind],
                                            "animal kind rewrite")
                        used.add((t, who))
                        built[tile] = day
                        place_one(t + 1, who, tile, kind, src_name)
                        pending[kind] -= 1
            # fill：空置已建牧场上的非移动槽 → PLACE（消化剩余 pending）
            if any(pending[k] > 0 for k in ANIMAL_KINDS):
                for (t, who, verb, arg, tile) in self.nonmove_slots(day):
                    kind = next((k for k in ANIMAL_KINDS if pending[k] > 0),
                                None)
                    if kind is None:
                        break
                    if tile in occupied or tile not in built:
                        continue
                    if built[tile] > day:
                        continue
                    if verb not in ("PASS", "WATER", "PLANT", "FEED",
                                    "CARE", "COLLECT_FERTILIZER", "HARVEST"):
                        continue
                    if not carrier_has(kind, who, t, 1):
                        continue
                    self.set_action(t, who, ["PLACE", kind],
                                    "animal place (fill empty pasture)")
                    place_one(t, who, tile, kind, "fill")
                    pending[kind] -= 1
            shed += pending
        unplaced = collections.Counter(shed)
        # 应用 pickup 翻转（载畜）
        for (day, who, kind), (k2, n, first_t, slot_t) in sorted(
                pickups.items()):
            if n <= 0:
                continue
            a = action_at(self.route, slot_t, who)
            if a is None or a[0] in MOVES:
                continue
            self.set_action(slot_t, who, ["PICKUP", kind, n],
                            "animal pickup rewrite")
        # 记录已建未占牧场（供 tending 诊断）
        self.built_pastures = built
        return placed_log, unplaced

    # -- 喂养面 -------------------------------------------------------------
    def edit_tending(self, placed_log):
        new_tiles = {}
        for (day, t, who, kind, tile, src) in placed_log:
            if src != "base" and tile is not None:
                new_tiles[tile] = min(new_tiles.get(tile, 99), day)
        flips = collections.Counter()
        for day in range(30):
            slots = self.nonmove_slots(day)
            per_tile = collections.defaultdict(list)
            for (t, who, verb, arg, tile) in slots:
                if tile in new_tiles and day >= new_tiles[tile] \
                        and tile not in SHED_TILES:
                    if verb in ("WATER", "PASS", "PLANT"):
                        per_tile[tile].append((t, who, verb, arg))
            for tile, ts in per_tile.items():
                if not ts:
                    continue
                plan = ["FEED", "CARE"]
                if day % 3 == (new_tiles[tile] + 1) % 3:
                    plan = ["HARVEST", "FEED"]
                for (t, who, verb, arg), nv in zip(ts, plan):
                    self.set_action(t, who, [nv], f"tend new pasture {tile}")
                    flips[nv] += 1
        # FEED 载麦：翻转执行实体的棚区槽为 PICKUP WHEAT
        for day in range(30):
            slots = self.nonmove_slots(day)
            shed_slots = collections.defaultdict(list)
            for (t, who, verb, arg, tile) in slots:
                if tile in SHED_TILES and verb in ("PICKUP", "DROP", "PASS"):
                    shed_slots[who].append((t, verb, arg))
            feeders = {who for (t, who, verb, arg, tile) in slots
                       if tile in new_tiles and verb == "FEED"
                       and day >= new_tiles.get(tile, 99)}
            for who in sorted(feeders):
                sl = shed_slots.get(who)
                if not sl:
                    continue
                t, verb, arg = sl[0]              # 最早棚区槽（先于 FEED 步）
                if verb == "PICKUP" and arg == "WHEAT":
                    continue                      # 已有载麦（量不足另议）
                self.set_action(t, who, ["PICKUP", "WHEAT", 6],
                                "feeder wheat carriage")
                flips["PICKUP_WHEAT"] += 1
        return new_tiles, flips

    def run(self):
        self.rewrite_hires()
        self.edit_buys()
        straw_pool, pair_pool = self.edit_plants()
        self.edit_seeds()
        placed, unplaced = self.edit_animals(straw_pool, pair_pool)
        new_tiles, flips = self.edit_tending(placed)
        return {"placed": collections.Counter(k for (_, _, _, k, _, _)
                                              in placed),
                "unplaced": dict(unplaced),
                "new_pasture_tiles": {str(k): v for k, v in new_tiles.items()},
                "tend_flips": dict(flips)}


def rebuild_tape_routes(routes, schedule, site_blacklist=None):
    log = []
    new_routes = {}
    stats = {}
    for name in ROUTE_ORDER:
        bl = (site_blacklist or {}).get(name, set())
        s = Surgery(name, routes[name], schedule, log, site_blacklist=bl)
        stats[name] = s.run()
        new_routes[name] = s.route
    return new_routes, log, stats


def main() -> int:
    ap = argparse.ArgumentParser(description="R9-G2 tape surgery")
    args = ap.parse_args()
    routes, base_text, span = decode_routes()
    schedule = json.load(open(SCHEDULE, encoding="utf-8"))

    diffs = map_events_to_tape(routes, schedule)
    new_routes, log, stats = rebuild_tape_routes(routes, schedule)

    new2, _, _ = rebuild_tape_routes(routes, schedule)
    if json.dumps(new2, sort_keys=True) != json.dumps(new_routes,
                                                      sort_keys=True):
        raise SystemExit("surgery is not deterministic")

    assert list(new_routes) == list(routes)
    for name, r in new_routes.items():
        assert len(r) == N_STEPS
        o_sell = [o for s in routes[name] for o in s["market"]
                  if o[0] == "SELL"]
        n_sell = [o for s in r for o in s["market"] if o[0] == "SELL"]
        assert o_sell == n_sell, f"{name}: SELL face changed"
        for t in range(N_STEPS):
            of, nf = routes[name][t]["farmer"], r[t]["farmer"]
            assert (of[0] in MOVES) == (nf[0] in MOVES), \
                f"{name} t{t}: farmer movement changed"
            if of[0] in MOVES:
                assert of == nf
            for hi_ in range(max(len(routes[name][t]["hands"]),
                                 len(r[t]["hands"]))):
                oh = (routes[name][t]["hands"][hi_]
                      if hi_ < len(routes[name][t]["hands"]) else None)
                nh = (r[t]["hands"][hi_] if hi_ < len(r[t]["hands"]) else None)
                om = oh is not None and oh[0] in MOVES
                nm_ = nh is not None and nh[0] in MOVES
                assert om == nm_, f"{name} t{t} h{hi_}: hand movement changed"
                if om:
                    assert oh == nh

    with open(os.path.join(HERE, "routes_surgered.json"), "w",
              encoding="utf-8") as h:
        json.dump(new_routes, h, ensure_ascii=False, separators=(",", ":"))
    with open(os.path.join(HERE, "surgery_diff.json"), "w",
              encoding="utf-8") as h:
        json.dump({"schedule_meta": schedule["meta"], "diffs": diffs,
                   "edit_log": log, "stats": stats}, h, ensure_ascii=False,
                  indent=1)

    ops = collections.Counter(e["op"] for e in log)
    kinds = collections.Counter(d["kind"] for d in diffs)
    report = {
        "base_sha256": sha256_bytes(open(BASE_MAIN, "rb").read()),
        "diff_entries": len(diffs), "diff_kinds": dict(kinds),
        "edits": len(log), "edit_ops": dict(ops),
        "per_route": stats,
        "sell_face_unchanged": True,
        "movement_skeleton_unchanged": True,
        "route_switch_structure_unchanged": True,
    }
    with open(os.path.join(HERE, "surgery_report.json"), "w",
              encoding="utf-8") as h:
        json.dump(report, h, ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
