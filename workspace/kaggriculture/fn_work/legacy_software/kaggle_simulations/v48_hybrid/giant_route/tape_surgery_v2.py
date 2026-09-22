# -*- coding: utf-8 -*-
# 【中文】tape_surgery_v2.py —— R9-G2b 计划层三面一致重生成 + 手术 v2
# ===========================================================================
# 契约（fn_docs/responsibility.md R9 增补【修订版】perform_tape_surgery 块）：
#   * allocate_labor_plan [L1]：op 容量（24/人/日×雇工曲线）分配 CARE/FEED/
#     收割/种植；畜群规模受照护容量回传修订（超容→升雇工或降畜群，登记取舍）。
#   * derive_sell_schedule [L1]：M1 吸收节律最优（卖速≈日吸收，羊毛/奶/麦/
#     西瓜各线；末日 d29 清仓残值 0；峰日对在 d14-17 内确定性寻优）。
#   * map_events_to_tape [L1|修订]：排程+卖序+劳动 → 磁带三面（产线/卖/
#     移动）全事件差分集。
#   * rebuild_tape_routes [L1]：六路由 trunk/branch 前缀恒等（切换点
#     88/120/153/216/160 前逐字节同 default）；产线/移动面六路由恒等，
#     仅切换点后卖面按分支重排；事件点切换结构与反应层模块在 blob 外，
#     逐字节保留。
# G2 教训修正：
#   (a) 冻结卖序/移动 → 收入仅投影 24% → v2 三面全部重生成；
#   (b) G2 六路由自 step~4 发散，切换即跳到畜群状态不匹配的续段 → v2 产线
#       面以保守（default 卖参数）现金轨迹冻结，六路由产线/移动逐字节恒等；
#   (c) twin 低估照护产出（引擎实算：fed+cared 同日 pending+1，产出日
#       yield += 1+pending → 全照护羊 1 毛/日、牛 1 奶/日）。
# 引擎语义（vendored kaggle_environments 1.32.7 实读）：
#   * 植物当日必浇（plant 日 unwatered=1，EOD 不浇即 2→杂草）；
#   * 麦窗口龄 2-4，浇一日 +1，初始 1；西瓜窗口龄 6-12（cap 6）；
#   * SELL/BUY 市单与站位无关；FEED 需当日 PICKUP 自带 WHEAT；
#   * EOD：farmer 归 (4,4)、hands 清空、库存落棚（容量 100，溢出丢弃）；
#   * 雇工当日 fib 计价，hands 不跨日；HIRE t0 市单 → 手 t1 起行动；
#   * 市单处理在单步动作之后：t0 买入的货 t1 才可 PICKUP；
#   * 镇吸收：每 4 步每铺拉 1（单品铺 ×2）→ 每铺日 6/12；镇中心日 1。
# 确定性：纯函数 + 固定序；CLI 双跑自证。
# CLI：python tape_surgery_v2.py
#   → giant_route/{target_schedule_v2.json, routes_v2.json,
#                  surgery_v2_diff.json, surgery_v2_report.json}
# ===========================================================================
from __future__ import annotations

import collections
import copy
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HYBRID = os.path.dirname(HERE)
KSIM = os.path.dirname(HYBRID)
BASE_MAIN = os.path.join(KSIM, "v48_derivative", "main.py")

DAYS = 30
N_STEPS = 719
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
SHED_ACCESS = [(4, 4), (5, 4), (4, 5), (5, 5)]
ROUTE_ORDER = ("default", "yarn_fast", "farm_fast", "yarn_second",
               "yarn_third", "bakery_capital")
SWITCH = {"yarn_fast": 88, "farm_fast": 120, "yarn_second": 153,
          "yarn_third": 216, "bakery_capital": 160}

CROPS_CFG = {
    "WHEAT": {"seed": 10, "win": (2, 4), "max_yield": 6},
    "MELON": {"seed": 80, "win": (6, 12), "max_yield": 6},
}
ANIM_CFG = {
    "SHEEP": {"cost": 500, "first": 6, "interval": 3, "cap": 6, "prod": "WOOL"},
    "COW": {"cost": 400, "first": 8, "interval": 2, "cap": 6, "prod": "MILK"},
}
LAND_PRICES = [("NE", 1000), ("SW", 2000), ("SE", 4000)]
MP = {
    "WHEAT":      {"base": 25, "T": 400, "below": ("sqrt", 0.80), "above": ("log", 0.20)},
    "MELON":      {"base": 250, "T": 300, "below": ("log", 0.20), "above": ("sq", 3.60)},
    "MILK":       {"base": 160, "T": 122, "below": ("sqrt", 0.60), "above": ("linear", 1.60)},
    "WOOL":       {"base": 200, "T": 105, "below": ("log", 0.20), "above": ("sq", 3.20)},
    "FERTILIZER": {"base": 100, "T": 200, "below": ("linear", 0.40), "above": ("linear", 0.40)},
}
SHOPS = {
    "BAKERY": ["EGG", "WHEAT"], "PIZZA_SHOP": ["MILK", "TOMATO", "WHEAT"],
    "BRUNCH_SPOT": ["EGG", "WHEAT", "STRAWBERRY"], "YARN_STORE": ["WOOL"],
    "ICE_CREAM_SHOP": ["STRAWBERRY", "MILK", "WHEAT"], "PET_CAFE": ["CARROT"],
    "SMOOTHIE_SHOP": ["STRAWBERRY", "MILK"],
    "FARMERS_MARKET": ["WHEAT", "CARROT", "TOMATO", "STRAWBERRY"],
}
I0 = 10000.0
STOP = {"SHEEP": 14, "COW": 6, "MELON": 17, "WHEAT": 25, "SE": 22}
SELL_FLOOR = {"WOOL": 150.0, "MILK": 120.0, "WHEAT": 20.0,
              "MELON": 150.0, "FERTILIZER": 40.0}
SPIKE_FLOOR = {"WOOL": 110.0, "MILK": 90.0, "MELON": 130.0,
               "FERTILIZER": 40.0, "WHEAT": 20.0}
PRI_FEED, PRI_PLACE, PRI_WATER, PRI_CARE = 0, 1, 2, 3
PRI_HARV_AN, PRI_HARV_CROP, PRI_FERT, PRI_PLANT = 4, 5, 6, 7
MANDATORY = (PRI_FEED, PRI_PLACE, PRI_WATER, PRI_CARE)


def _shape(func, x, T):
    if func == "linear":
        return x / T
    if func == "sq":
        return (x / T) ** 2
    if func == "sqrt":
        return (x / T) ** 0.5
    if func == "log":
        return math.log1p(x) / math.log1p(T)
    raise ValueError(func)


def market_price(item, inv):
    p = MP[item]
    base, T = p["base"], p["T"]
    if inv < I0:
        fn, tgt = p["below"]
        return max(1.0, base + tgt * base * _shape(fn, I0 - inv, T))
    fn, tgt = p["above"]
    return max(1.0, base - tgt * base * _shape(fn, inv - I0, T))


def hire_cost(k):
    total, a, b = 0, 1, 1
    for _ in range(k):
        total += a
        a, b = b, a + b
    return total


def quad(tile):
    x, y = tile
    return ("N" if y < 5 else "S") + ("W" if x < 5 else "E")


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def walk_path(src, dst):
    out = []
    x0, y0 = src
    x1, y1 = dst
    while x0 != x1:
        if x1 > x0:
            out.append(["EAST"])
            x0 += 1
        else:
            out.append(["WEST"])
            x0 -= 1
    while y0 != y1:
        if y1 > y0:
            out.append(["SOUTH"])
            y0 += 1
        else:
            out.append(["NORTH"])
            y0 -= 1
    return out


def _ring(q):
    tiles = [(x, y) for y in range(10) for x in range(10)
             if quad((x, y)) == q and (x, y) not in SHED_ACCESS]
    tiles.sort(key=lambda t: (manhattan(t, (4, 4)), t))
    return tiles


NW_RING, NE_RING, SW_RING = _ring("NW"), _ring("NE"), _ring("SW")
PASTURE_POOL = (NW_RING[:15] + [(5, 4), (4, 5), (5, 3), (3, 5), (6, 4), (4, 6),
                                (6, 3), (3, 6), (5, 2), (2, 5), (7, 4), (4, 7)])
_PASTURE_SET = set(PASTURE_POOL)
WHEAT_NW = NW_RING[15:24]
WHEAT_NE = [t for t in NE_RING if t not in _PASTURE_SET][:9]
MELON_POOL = ([t for t in NE_RING if t not in _PASTURE_SET
               and t not in WHEAT_NE]
              + [t for t in SW_RING if t not in _PASTURE_SET])
MELON_NW_D0 = NW_RING[6:12]

BRANCH_SHOPS = {
    "default": [], "yarn_fast": ["YARN_STORE"], "farm_fast": ["FARMERS_MARKET"],
    "yarn_second": ["YARN_STORE"], "yarn_third": ["YARN_STORE"],
    "bakery_capital": ["BAKERY"],
}
STEADY = {
    "default":        {"WOOL": 4, "MILK": 3, "WHEAT": 6, "MELON": 6, "FERTILIZER": 15},
    "yarn_fast":      {"WOOL": 2, "MILK": 3, "WHEAT": 6, "MELON": 6, "FERTILIZER": 15},
    "farm_fast":      {"WOOL": 4, "MILK": 3, "WHEAT": 10, "MELON": 6, "FERTILIZER": 15},
    "yarn_second":    {"WOOL": 2, "MILK": 3, "WHEAT": 6, "MELON": 6, "FERTILIZER": 15},
    "yarn_third":     {"WOOL": 2, "MILK": 3, "WHEAT": 6, "MELON": 6, "FERTILIZER": 15},
    "bakery_capital": {"WOOL": 4, "MILK": 3, "WHEAT": 10, "MELON": 6, "FERTILIZER": 15},
}
SPIKE_CANDIDATES = ((None,), (14,), (15,), (16,), (14, 15), (15, 16),
                    (16, 17), (14, 15, 16), (15, 16, 17))
SHED_ROOM_TRIGGER = 88          # 棚存超此线即越过稳态上限卖（防 EOD 溢出丢弃）
FERT_COLLECT_MAX_LOAD = 80      # 棚存超此线当日跳过肥料收集（省工+防溢出）


# ============================================================================
# 逐日状态
# ============================================================================
class CropTile:
    __slots__ = ("crop", "planted", "yield_u", "watered", "unwatered",
                 "win_waters")

    def __init__(self, crop, day):
        self.crop = crop
        self.planted = day
        self.yield_u = 1
        self.watered = False
        self.unwatered = 1
        self.win_waters = 0


class AnimalTile:
    __slots__ = ("animal", "placed", "yield_u", "pending", "fed", "cared",
                 "fert_avail", "unfed")

    def __init__(self, animal, day):
        self.animal = animal
        self.placed = day
        self.yield_u = 0
        self.pending = 0
        self.fed = False
        self.cared = False
        self.fert_avail = False
        self.unfed = 0


class DayPlan:
    def __init__(self, day):
        self.day = day
        self.crew = 0
        self.land = None
        self.buys = {}
        self.buy_wheat = 0
        self.buy_seeds = {}
        self.plants = {}
        self.places = []
        self.sell = {}
        self.income = 0.0
        self.groups = []            # (pri, tile, [verbs]) —— tile 组任务
        self.executed = {}          # tile -> [verbs] 实际发射
        self.dropped = []
        self.acts = None            # {who: [24 actions]}
        self.market = None          # [24][orders]


# ============================================================================
# Planner：单次 30 日推演（sim == tape：状态推演只读实际发射的动词）
# ============================================================================
class Planner:
    def __init__(self, herd_wish, hires_wish, policy, mirror=2.0,
                 freeze=None):
        self.herd_wish = copy.deepcopy(herd_wish)
        self.hires_wish = copy.deepcopy(hires_wish)
        self.policy = policy
        self.mirror = mirror
        self.freeze = freeze
        self.cash = 3000.0
        self.animals = {}
        self.crops = {}
        self.shed = collections.Counter()
        self.seeds = collections.Counter()
        self.quads = ["NW"]
        self.book = {k: I0 for k in MP}
        self.crew = {}
        self.sold = collections.Counter()
        self.prod_cum = collections.Counter()
        self.fed_miss = 0
        self.escapes = 0
        self.miss_log = []
        self.push_log = []
        self.days = []
        self.income_hist = []

    # ---------------- 产线辅助 ----------------
    def _pasture_sites(self):
        used = set(self.animals) | set(self.crops)
        return [t for t in PASTURE_POOL
                if (quad(t) in self.quads or t in SHED_ACCESS)
                and t not in used]

    def _harvest_all(self, day):
        return day in (13, 14, 15, 27, 28)

    def _crop_needs_water(self, ct, age):
        if ct.watered:
            return False
        if age == 0 or ct.unwatered >= 1:
            return True
        w0, w1 = CROPS_CFG[ct.crop]["win"]
        if ct.crop == "WHEAT" and w0 <= age <= w1:
            return True
        if ct.crop == "MELON" and w0 <= age <= 10 and ct.win_waters < 5:
            return True
        return False

    def _crop_due_harvest(self, ct, age):
        if ct.crop == "WHEAT":
            return age >= 4
        if ct.crop == "MELON":
            return (age >= 10 and ct.win_waters >= 5) or age >= 12
        return False

    def _desired_plants(self, day):
        used = set(self.animals) | set(self.crops)
        out = []
        if day == 0:
            out.append(("MELON", [t for t in MELON_NW_D0
                                  if t not in used][:5]))
            out.append(("WHEAT", [t for t in WHEAT_NW if t not in used][:6]))
        elif day in (1, 2, 3):
            nw_free = [t for t in NW_RING
                       if t not in used and t not in WHEAT_NW]
            out.append(("MELON", nw_free[:3]))
        elif day in (5, 6):
            out.append(("MELON", [t for t in MELON_POOL
                                  if quad(t) in self.quads
                                  and t not in used][:5]))
        elif day in (10, 11):
            out.append(("MELON", [t for t in MELON_POOL
                                  if quad(t) in self.quads
                                  and t not in used][:4]))
        elif day == 7:
            out.append(("WHEAT", [t for t in WHEAT_NE + WHEAT_NW
                                  if quad(t) in self.quads
                                  and t not in used][:9]))
        if 1 <= day <= STOP["WHEAT"] and day not in (0, 7):
            free = [t for t in WHEAT_NW + WHEAT_NE
                    if quad(t) in self.quads and t not in used]
            if free:
                out.append(("WHEAT", free[:6]))
        return [(c, ts) for c, ts in out if ts]

    def _crew_cap(self, day, wish):
        """现金门雇工上限：雇工费 ≤ 近 5 日均收入 25%+8 或现金 35%。"""
        hist = [x for x in self.income_hist[-5:] if x > 0] or [300.0]
        allow = max(0.25 * sum(hist) / len(hist) + 8, 0.35 * max(0, self.cash))
        crew = min(wish, 14)
        while crew > 3 and hire_cost(crew) > allow:
            crew -= 1
        return crew

    # ---------------- 单日 ----------------
    def plan_day(self, day):
        dp = DayPlan(day)
        frozen = self.freeze[day] if self.freeze is not None else None

        # ---- (b) 卖面（先卖后买：晨单读昨 EOD 棚存，先清仓腾棚容） ----
        self._sell_face(day, dp)
        self.income_hist.append(dp.income)

        # ---- (a) 劳动面：容量回传 ----
        est = self._labor_estimate(day)
        wish = self.hires_wish.get(day, 0)
        if frozen is not None:
            crew = frozen.crew
        else:
            crew = self._crew_cap(day, wish)
            while est > 24 * (1 + crew) and crew < 14:
                crew += 1
                self.push_log.append(f"d{day}: crew -> {crew} "
                                     f"(labor est {est})")
        dp.crew = crew
        self.crew[day] = crew
        reserve = hire_cost(crew) + 25

        # ---- (c) 产线面 ----
        budget = self.cash - reserve
        spend = hire_cost(crew)
        if frozen is not None:
            dp.land = frozen.land
            dp.buys = dict(frozen.buys)
            dp.buy_wheat = frozen.buy_wheat
            plants = dict(frozen.plants)
            spend += sum(ANIM_CFG[k]["cost"] * n for k, n in dp.buys.items())
            spend += sum(CROPS_CFG[c]["seed"] for c in plants.values())
            if dp.land:
                spend += dict(LAND_PRICES)[dp.land]
        else:
            land_day = {"NE": 3, "SW": 10, "SE": 13}
            for q, price in LAND_PRICES:
                if q in self.quads:
                    continue
                if day >= land_day[q] and budget - spend >= price:
                    self.quads.append(q)
                    self.cash -= price
                    spend += price
                    dp.land = q
                break
            buys = {}
            wish_herd = dict(self.herd_wish.get(day, {}))
            # 喂养优先：既有畜群+当日意向头数的饲料成本先占预算
            wish_total = sum(wish_herd.values())
            feed_reserve = (len(self.animals) + wish_total) * 27
            for kind in ("COW", "SHEEP"):
                n = wish_herd.get(kind, 0)
                while n > 0:
                    if day > STOP[kind]:
                        self.miss_log.append(
                            f"d{day}: {kind} x{n} past stop dropped")
                        n = 0
                        break
                    if budget - spend - feed_reserve < ANIM_CFG[kind]["cost"]:
                        self.herd_wish.setdefault(day + 1, {})
                        self.herd_wish[day + 1][kind] = \
                            self.herd_wish[day + 1].get(kind, 0) + n
                        self.push_log.append(
                            f"d{day}: {kind} x{n} -> d{day + 1} "
                            f"(cash/feed-first)")
                        n = 0
                        break
                    spend += ANIM_CFG[kind]["cost"]
                    buys[kind] = buys.get(kind, 0) + 1
                    n -= 1
            dp.buys = buys
            plants = {}
            for crop, tiles in self._desired_plants(day):
                ok = []
                for t in tiles:
                    if budget - spend - feed_reserve < \
                            CROPS_CFG[crop]["seed"]:
                        self.push_log.append(
                            f"d{day}: {crop} seeds cash-short "
                            f"({len(ok)}/{len(tiles)})")
                        break
                    spend += CROPS_CFG[crop]["seed"]
                    ok.append(t)
                plants.update({t: crop for t in ok})
            n_an = len(self.animals) + sum(buys.values())
            must = max(0, n_an - self.shed.get("WHEAT", 0))
            buy_w = max(must, n_an + 4 - self.shed.get("WHEAT", 0))
            shed_room = 100 - sum(self.shed.values())
            buy_w = min(buy_w, max(0, shed_room - sum(buys.values())))
            # 饲料是生存项：must 部分允许吃掉预备金（只求非负）；缓冲部分走预算门
            if buy_w > 0:
                uprice = market_price("WHEAT",
                                      self.book["WHEAT"]
                                      - buy_w * self.mirror)
                room = self.cash - spend - buy_w * uprice
                if room > 0:
                    dp.buy_wheat = buy_w
                elif must > 0:
                    afford = max(0, int((self.cash - spend) / uprice))
                    dp.buy_wheat = min(must, afford)
        dp.plants = plants
        for k, n in dp.buys.items():
            self.shed[k] += n
            self.cash -= ANIM_CFG[k]["cost"] * n
        seed_buy = collections.Counter(plants.values())
        dp.buy_seeds = dict(seed_buy)
        for crop, n in seed_buy.items():
            self.seeds[crop] += n
            self.cash -= CROPS_CFG[crop]["seed"] * n
        if dp.land and dp.land not in self.quads:
            self.quads.append(dp.land)
            self.cash -= dict(LAND_PRICES)[dp.land]
        if dp.buy_wheat:
            uprice = market_price("WHEAT", self.book["WHEAT"])
            self.cash -= dp.buy_wheat * uprice
            self.book["WHEAT"] -= dp.buy_wheat * self.mirror
            self.shed["WHEAT"] += dp.buy_wheat

        # ---- (d) tile 组任务 + (e) 精确分派发射 ----
        self._schedule(day, dp)

        # ---- (f) 状态推演（只认实际发射的动词） ----
        self._advance(day, dp)
        self.days.append(dp)
        self.cash -= hire_cost(dp.crew)
        return dp

    def _labor_estimate(self, day):
        verbs = 0
        tiles = set()
        for t, at in self.animals.items():
            verbs += 2
            tiles.add(t)
            if at.fert_avail:
                verbs += 1
            if at.yield_u >= 5 or (self._harvest_all(day) and at.yield_u):
                verbs += 1
        for t, ct in self.crops.items():
            age = day - ct.planted
            if self._crop_needs_water(ct, age):
                verbs += 1
                tiles.add(t)
            if self._crop_due_harvest(ct, age):
                verbs += 1
                tiles.add(t)
        return verbs + int(1.2 * len(tiles)) + 4

    # ---------------- tile 组任务构造 + 精确分派 ----------------
    def _build_groups(self, day, dp):
        groups = []          # (pri, tile, verbs)
        for kind in ("SHEEP", "COW"):
            while self.shed.get(kind, 0) > 0:
                pool = self._pasture_sites()
                if not pool:
                    self.miss_log.append(
                        f"d{day}: {kind} x{self.shed[kind]} no pasture site")
                    break
                t = pool[0]
                self.shed[kind] -= 1
                self.animals[t] = AnimalTile(kind, day)
                dp.places.append((t, kind))
                groups.append((PRI_PLACE, t,
                               [["BUILD_PASTURE"], ["PLACE", kind],
                                ["FEED"], ["CARE"]]))
        fert_ok = sum(self.shed.values()) <= FERT_COLLECT_MAX_LOAD
        for t, at in sorted(self.animals.items()):
            verbs = [["FEED"], ["CARE"]]
            if at.fert_avail and fert_ok:
                verbs.append(["COLLECT_FERTILIZER"])
            if at.yield_u >= 5 or (self._harvest_all(day) and at.yield_u):
                verbs.append(["HARVEST"])
            groups.append((PRI_FEED, t, verbs))
        for t, crop in sorted(dp.plants.items()):
            groups.append((PRI_WATER, t, [["PLANT", crop], ["WATER"]]))
            self.crops[t] = CropTile(crop, day)
        for t, ct in sorted(self.crops.items()):
            if t in dp.plants:
                continue
            age = day - ct.planted
            verbs = []
            if self._crop_needs_water(ct, age):
                verbs.append(["WATER"])
            if self._crop_due_harvest(ct, age):
                verbs.append(["HARVEST"])
            if verbs:
                groups.append((PRI_WATER, t, verbs))
        groups.sort(key=lambda g: (g[0], manhattan((4, 4), g[1]), g[1]))
        return groups

    def _schedule(self, day, dp):
        groups = self._build_groups(day, dp)
        crew = dp.crew
        acts = {0: [], **{i + 1: [] for i in range(crew)}}
        spawn = {0: (4, 4)}
        occ = collections.Counter({(4, 4): 1})
        for i in range(crew):
            best = min(SHED_ACCESS,
                       key=lambda t: (occ[t], SHED_ACCESS.index(t)))
            spawn[i + 1] = best
            occ[best] += 1
        cur = dict(spawn)
        pickups_needed = collections.defaultdict(collections.Counter)
        assigned = collections.defaultdict(list)
        proj = collections.Counter()          # 每实体精确投影步数

        def limit_of(who):
            return 24 if who == 0 else 23

        def pickup_overhead(who, verbs):
            """该实体首次携带取货任务的棚口绕行开销。"""
            if pickups_needed[who]:
                return 0
            if not any(v[0] in ("FEED", "PLACE") for v in verbs):
                return 0
            shed_t = min(SHED_ACCESS, key=lambda t: manhattan(spawn[who], t))
            n_pk = (1 if any(v[0] == "FEED" for v in verbs) else 0) + \
                len({v[1] for v in verbs if v[0] == "PLACE"})
            detour = manhattan(spawn[who], shed_t)
            if detour == 0:
                detour = 1                     # t0 相位等待 PASS
            return detour + n_pk

        dropped = []
        for (pri, tile, verbs) in groups:
            cands = []
            for who in sorted(acts):
                extra = pickup_overhead(who, verbs)
                need = extra + manhattan(cur[who], tile) + len(verbs)
                if proj[who] + need <= limit_of(who):
                    cands.append((manhattan(cur[who], tile) + extra,
                                  proj[who], who))
            if not cands:
                dropped.append((pri, tile, [v[0] for v in verbs]))
                continue
            who = min(cands)[2]
            proj[who] += pickup_overhead(who, verbs) + \
                manhattan(cur[who], tile) + len(verbs)
            assigned[who].append((pri, tile, verbs))
            cur[who] = tile
            if any(v[0] == "FEED" for v in verbs):
                pickups_needed[who]["WHEAT"] += sum(
                    1 for v in verbs if v[0] == "FEED")
            for v in verbs:
                if v[0] == "PLACE":
                    pickups_needed[who][v[1]] += 1

        # 发射（分派序 = 发射序，精确计步）
        for who in sorted(assigned):
            p = spawn[who]
            if who != 0:
                acts[who].append(["PASS"])   # hand t0 死步（市单后才出生）
            pk = pickups_needed.get(who)
            if pk:
                shed_t = min(SHED_ACCESS, key=lambda t: manhattan(p, t))
                if shed_t == p:
                    # 起点即棚口：垫 PASS 至 t3（t2 市单买入后才可取）
                    pad_to = 3 - (len(acts[who]) - 1 if who != 0
                                  else len(acts[who]))
                    acts[who] += [["PASS"]] * max(0, pad_to)
                else:
                    acts[who] += walk_path(p, shed_t)
                for item, n in sorted(pk.items()):
                    acts[who].append(["PICKUP", item, n])
                p = shed_t
            for (pri, tile, verbs) in assigned[who]:
                if p != tile:
                    acts[who] += walk_path(p, tile)
                acts[who] += [list(v) for v in verbs]
                dp.executed.setdefault(tile, [])
                dp.executed[tile] += [v[0] for v in verbs]
                p = tile
        for who in sorted(acts):
            limit = limit_of(who)
            # PICKUP 相位保护：首 PICKUP 早于 t3（买入未入棚）则垫 PASS
            pickup_ts = [i for i, a in enumerate(acts[who])
                         if a[0] == "PICKUP"]
            if pickup_ts:
                first_pk = pickup_ts[0]
                pad = max(0, 3 - first_pk)
                if pad:
                    acts[who] = (acts[who][:first_pk] + [["PASS"]] * pad +
                                 acts[who][first_pk:])
            # 归一化：farmer 24 槽 / hand 24 槽（index0=死步 PASS，实动 23）
            hard = 24 if who == 0 else 24
            if len(acts[who]) > hard:
                dp.dropped.append(("overflow", who, len(acts[who]) - hard))
                del acts[who][hard:]
            while len(acts[who]) < 24:
                acts[who].append(["PASS"])
            if who != 0:
                acts[who][0] = ["PASS"]
            # hand 实动上限 23（t1..t23）：超限截断尾部
            if who != 0:
                real = [i for i in range(1, 24)
                        if acts[who][i] != ["PASS"]]
                if len(real) > 23:
                    dp.dropped.append(("overflow", who,
                                       len(real) - 23))
        for (pri, tile, vs) in dropped:
            dp.dropped.append(("task", pri, str(tile), vs))
        # 落位对账：被丢弃的 BUILD_PLACE 组 → 撤销已登账的 AnimalTile
        for (pri, tile, vs) in dropped:
            if "PLACE" in vs and tile in self.animals:
                kind = self.animals[tile].animal
                del self.animals[tile]
                self.shed[kind] += 1
                dp.places = [(t2, k) for (t2, k) in dp.places
                             if t2 != tile]
                self.miss_log.append(
                    f"d{dp.day}: {kind} placement dropped {tile} "
                    f"(labor) -> back to shed")
        dp.groups = [(pri, tile, [v[0] for v in verbs])
                     for (pri, tile, verbs) in groups]
        dp.acts = acts

        # 市单相位（订单每步 ≤10；HIRE 先于一切——hands t1 即在岗）：
        #   t0 = HIRE×crew（hands t1 起行动）
        #   t1 = SELL（先卖腾棚容）
        #   t2 = BUY_*（t3 起 PICKUP 可读）
        market = [[] for _ in range(24)]
        market[0] = [["HIRE"]] * min(crew, 10)
        sells = [["SELL", item, n] for item, n in sorted(dp.sell.items())]
        market[1] = sells[:10]
        buys = []
        if dp.land:
            buys.append(["BUY_LAND"])
        for kind, n in sorted(dp.buys.items()):
            buys.append(["BUY_ANIMAL", kind, n])
        for crop, n in sorted(dp.buy_seeds.items()):
            buys.append(["BUY_SEED", crop, n])
        if dp.buy_wheat:
            buys.append(["BUY_PRODUCT", "WHEAT", dp.buy_wheat])
        slot = 2
        for order in buys:
            if len(market[slot]) >= 10:
                slot += 1
            market[slot].append(order)
        dp.market = market

    # ---------------- 卖面 ----------------
    def _sell_face(self, day, dp):
        steady = self.policy["steady"]
        spike = day in (self.policy.get("spike_days") or ())
        for shop in self.policy.get("shops", []):
            for item in SHOPS[shop]:
                if item not in self.book:
                    continue
                mult = 2 if len(SHOPS[shop]) == 1 else 1
                self.book[item] -= 6 * mult
        for item in MP:
            if item != "FERTILIZER":
                self.book[item] -= 1
        floors = SPIKE_FLOOR if spike else SELL_FLOOR
        inc = 0.0
        for item in ("WOOL", "MILK", "MELON", "FERTILIZER", "WHEAT"):
            stock = self.shed.get(item, 0)
            if stock <= 0:
                continue
            load = sum(self.shed.values())
            room_push = load > SHED_ROOM_TRIGGER
            emergency = load > 95
            if day >= 29:
                want = stock
            elif spike and item in ("WOOL", "MILK", "MELON", "FERTILIZER"):
                want = stock
            elif room_push:
                want = stock
            else:
                want = min(stock, steady.get(item, 0))
            eff_floor = {k: max(1.0, v * 0.4) for k, v in floors.items()} \
                if emergency else floors
            sold = 0
            gain = 0.0
            for _ in range(int(want)):
                p_me = market_price(item, self.book[item] + self.mirror)
                if p_me < eff_floor[item]:
                    break
                self.book[item] += self.mirror
                gain += p_me
                sold += 1
            if sold:
                self.shed[item] -= sold
                self.sold[item] += sold
                dp.sell[item] = sold
                inc += gain
        dp.income = inc
        self.cash += inc

    # ---------------- 状态推演 ----------------
    def _advance(self, day, dp):
        for tile, verbs in dp.executed.items():
            at = self.animals.get(tile)
            ct = self.crops.get(tile)
            for v in verbs:
                if at is not None:
                    if v == "FEED":
                        if self.shed.get("WHEAT", 0) > 0:
                            at.fed = True
                            self.shed["WHEAT"] -= 1
                        else:
                            self.fed_miss += 1
                    elif v == "CARE":
                        at.cared = True
                    elif v == "COLLECT_FERTILIZER":
                        if at.fert_avail:
                            at.fert_avail = False
                            self.shed["FERTILIZER"] += 1
                    elif v == "HARVEST":
                        if at.yield_u:
                            self.shed[ANIM_CFG[at.animal]["prod"]] += at.yield_u
                            self.prod_cum[ANIM_CFG[at.animal]["prod"]] += \
                                at.yield_u
                            at.yield_u = 0
                if ct is not None:
                    if v == "WATER" and not ct.watered:
                        ct.watered = True
                        w0, w1 = CROPS_CFG[ct.crop]["win"]
                        age = day - ct.planted
                        if w0 <= age <= w1 and ct.win_waters < 5:
                            ct.win_waters += 1
                            ct.yield_u = min(CROPS_CFG[ct.crop]["max_yield"],
                                             ct.yield_u + 1)
                    elif v == "HARVEST" and ct.yield_u:
                        self.shed[ct.crop] += ct.yield_u
                        self.prod_cum[ct.crop] += ct.yield_u
                        del self.crops[tile]
                        ct = None
        # PLANT 消种子（executed 记动词名，种子账在买面已计）
        for tile, verbs in dp.executed.items():
            if "PLANT" in verbs and tile in self.crops:
                crop = self.crops[tile].crop
                if self.seeds.get(crop, 0) > 0:
                    self.seeds[crop] -= 1
        over = sum(self.shed.values()) - 100
        if over > 0:
            # 饲料 WHEAT 永远最后丢（保命）
            for item in ("FERTILIZER", "MELON", "MILK", "WOOL",
                         "SHEEP", "COW", "WHEAT"):
                take = min(over, self.shed.get(item, 0))
                if take:
                    self.shed[item] -= take
                    over -= take
                    self.miss_log.append(
                        f"d{day}: shed overflow drop {item} x{take}")
                if over <= 0:
                    break
        nxt = day + 1
        for t in list(self.crops):
            ct = self.crops[t]
            ct.unwatered = 0 if ct.watered else ct.unwatered + 1
            ct.watered = False
            if ct.unwatered >= 2:
                del self.crops[t]
                self.miss_log.append(f"d{day}: crop died {t} {ct.crop}")
        for t in list(self.animals):
            at = self.animals[t]
            if at.fed:
                at.unfed = 0
            else:
                at.unfed += 1
            if at.unfed >= 2:
                del self.animals[t]
                self.escapes += 1
                self.miss_log.append(f"d{day}: {at.animal} escaped {t}")
                continue
            cfg = ANIM_CFG[at.animal]
            dsf = nxt - at.placed - cfg["first"]
            if dsf >= 0 and dsf % cfg["interval"] == 0:
                bonus = at.pending if at.fed else 0
                at.yield_u = min(cfg["cap"], at.yield_u + 1 + bonus)
                at.pending = 0
            if at.cared and at.fed:
                at.pending += 1
            at.fert_avail = True
            at.fed = False
            at.cared = False

    def run(self):
        for d in range(DAYS):
            self.plan_day(d)
        return self


# ============================================================================
# 路由合成（从 DayPlan.acts/market 直接拼装；分支仅换卖单）
# ============================================================================
def synth_routes(base_days, branch_sells):
    trunk = []
    for dp in base_days:
        for t in range(24):
            trunk.append({"farmer": dp.acts[0][t],
                          "hands": [dp.acts[i + 1][t]
                                    for i in range(dp.crew)],
                          "market": dp.market[t]})
    trunk = trunk[:N_STEPS]
    routes = {"default": trunk}
    for branch in ROUTE_ORDER[1:]:
        sw = SWITCH[branch]
        sells = branch_sells[branch]
        r = [dict(s) for s in trunk[:sw]]
        day = sw // 24
        skip_t = sw % 24            # 切换日：前缀已含 [0, sw)，只补尾部
        while day * 24 < N_STEPS:
            sells_today = sells.get(day, {})
            day_steps = []
            for t in range(skip_t, 24):
                idx = day * 24 + t
                if idx >= N_STEPS:
                    break
                day_steps.append(dict(trunk[idx]))
            if sells_today and day_steps:
                # 卖单槽 = 日内 t1（与 trunk 卖单相位一致；切换日落在首个步）
                slot = 1 - skip_t if skip_t <= 1 else 0
                slot = max(0, min(slot, len(day_steps) - 1))
                non_sell = [o for o in day_steps[slot]["market"]
                            if o[0] != "SELL"]
                sell_orders = [["SELL", item, n]
                               for item, n in sorted(sells_today.items())]
                day_steps[slot]["market"] = (sell_orders + non_sell)[:10]
            r.extend(day_steps)
            day += 1
            skip_t = 0
        routes[branch] = r[:N_STEPS]
    return routes

# ============================================================================
# 三面差分
# ============================================================================
def extract_events(route):
    ev = []
    for day in range(30):
        lo, hi = day * 24, min(day * 24 + 24, N_STEPS)
        rec = {"day": day, "hires": 0, "buys": collections.Counter(),
               "land": 0, "seeds": collections.Counter(),
               "plants": collections.Counter(), "sells": collections.Counter(),
               "verbs": collections.Counter(), "moves": 0}
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
                elif o[0] == "SELL":
                    rec["sells"][o[1]] += o[2]
                elif o[0] == "BUY_PRODUCT":
                    rec["seeds"][o[1] + "*feed"] += o[2]
            for who in range(0, 16):
                a = route[t]["farmer"] if who == 0 else (
                    route[t]["hands"][who - 1]
                    if who - 1 < len(route[t]["hands"]) else None)
                if a is None:
                    continue
                if a[0] in MOVES:
                    rec["moves"] += 1
                else:
                    rec["verbs"][a[0]] += 1
                    if a[0] == "PLANT":
                        rec["plants"][a[1]] += 1
        for k in ("buys", "seeds", "plants", "sells"):
            rec[k] = dict(rec[k])
        ev.append(rec)
    return ev


def three_face_diff(base_routes, new_routes):
    out = {"production": [], "sell": [], "movement": []}
    for name in ROUTE_ORDER:
        be = extract_events(base_routes[name])
        ne = extract_events(new_routes[name])
        for b, n in zip(be, ne):
            d = b["day"]
            for key in ("hires", "land"):
                if b[key] != n[key]:
                    out["production"].append(
                        {"route": name, "day": d, "kind": key,
                         "original": b[key], "target": n[key]})
            for kind in ("buys", "plants", "seeds"):
                for k in set(b[kind]) | set(n[kind]):
                    if b[kind].get(k, 0) != n[kind].get(k, 0):
                        out["production"].append(
                            {"route": name, "day": d, "kind": kind, "item": k,
                             "original": b[kind].get(k, 0),
                             "target": n[kind].get(k, 0)})
            for k in set(b["sells"]) | set(n["sells"]):
                if b["sells"].get(k, 0) != n["sells"].get(k, 0):
                    out["sell"].append(
                        {"route": name, "day": d, "item": k,
                         "original": b["sells"].get(k, 0),
                         "target": n["sells"].get(k, 0)})
            if (sum(b["verbs"].values()) != sum(n["verbs"].values())
                    or b["verbs"] != n["verbs"] or b["moves"] != n["moves"]):
                out["movement"].append(
                    {"route": name, "day": d,
                     "original_verbs": sum(b["verbs"].values()),
                     "target_verbs": sum(n["verbs"].values()),
                     "original_moves": b["moves"], "target_moves": n["moves"],
                     "target_verb_mix": dict(n["verbs"])})
    return out


# ============================================================================
# 解码/编码
# ============================================================================
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
    routes = json.loads(__import__("zlib").decompress(
        __import__("base64").b85decode(blob)).decode("utf-8"))
    if any(len(v) != N_STEPS for v in routes.values()) or len(routes) != 6:
        raise SystemExit("unexpected route shape")
    return routes, base_text, m.span(1)


def encode_routes(routes):
    import base64
    payload = json.dumps(routes, ensure_ascii=True,
                         separators=(",", ":")).encode("ascii")
    text = base64.b85encode(__import__("zlib").compress(payload, 9)).decode(
        "ascii")
    return "\n".join(f"    '{text[i:i + 78]}'"
                     for i in range(0, len(text), 78)), payload


# ============================================================================
# 主流程
# ============================================================================
def herd_wish_v0():
    return {
        0: {"SHEEP": 3, "COW": 1},
        1: {"SHEEP": 1, "COW": 1},
        2: {"COW": 2},
        4: {"COW": 2},
        5: {"SHEEP": 2}, 6: {"SHEEP": 2}, 7: {"SHEEP": 2},
        8: {"SHEEP": 2}, 9: {"SHEEP": 2}, 10: {"SHEEP": 1},
        11: {"SHEEP": 1},
    }


def hires_wish_v0():
    return {0: 3, 1: 3, 2: 4, 3: 4, 4: 5, 5: 5, 6: 6, 7: 6, 8: 7, 9: 7,
            10: 8, 11: 8, 12: 8, 13: 9, 14: 9, 15: 9, 16: 9, 17: 9,
            18: 8, 19: 8, 20: 8, 21: 7, 22: 7, 23: 7, 24: 7, 25: 6,
            26: 6, 27: 6, 28: 5, 29: 4}


def run_pipeline(herd, hires):
    """迭代 ≤3 轮：计划 → 合成 → 强制动词掉落回传（升雇工→裁羊）。"""
    log = []
    best = None
    for it in range(1, 4):
        pl = Planner(copy.deepcopy(herd), copy.deepcopy(hires),
                     {"steady": dict(STEADY["default"]), "spike_days": None,
                      "shops": []}).run()
        synthed = None
        mand_drop = sum(1 for dp in pl.days for d in dp.dropped
                        if d[0] == "task" and d[1] in MANDATORY)
        task_drop = sum(1 for dp in pl.days for d in dp.dropped
                        if d[0] == "task")
        overflows = sum(1 for dp in pl.days for d in dp.dropped
                        if d[0] == "overflow")
        log.append({"iteration": it,
                    "mandatory_drops": mand_drop,
                    "task_drops": task_drop,
                    "overflow_workers": overflows,
                    "fed_miss": pl.fed_miss,
                    "escapes": pl.escapes,
                    "animals": sum(n for dp in pl.days
                                   for n in dp.buys.values()),
                    "final_cash": round(pl.cash)})
        score = (pl.escapes, mand_drop, pl.fed_miss, -round(pl.cash))
        if best is None or score < best[0]:
            best = (score, pl)
        if (mand_drop == 0 and pl.fed_miss == 0 and overflows == 0
                and pl.escapes == 0):
            break
        # 回传 1：有掉落/溢出的日子 +1 雇工（cap 14）
        changed = False
        for dp in pl.days:
            if dp.dropped:
                if dp.crew < 14:
                    hires[dp.day] = min(14, dp.crew + 1)
                    changed = True
        if changed:
            log[-1]["feedback"] = "hires +1 on drop days"
            continue
        # 回传 2：裁末期羊
        for d in sorted(herd, reverse=True):
            if herd[d].get("SHEEP"):
                herd[d]["SHEEP"] -= 1
                log[-1]["feedback"] = f"herd trim d{d} SHEEP -1"
                break
        else:
            break
    return best[1], None, log


def main() -> int:
    herd, hires = herd_wish_v0(), hires_wish_v0()
    plan, synthed, iter_log = run_pipeline(copy.deepcopy(herd),
                                           copy.deepcopy(hires))
    herd_final = copy.deepcopy(plan.herd_wish)
    hires_final = dict(plan.crew)

    # ---------- 分支卖面（产线冻结重排 + spike 寻优） ----------
    freeze = plan.days
    branch_sells = {}
    branch_stats = {}
    for branch in ROUTE_ORDER:
        best = None
        for spike_days in SPIKE_CANDIDATES:
            pl = Planner(copy.deepcopy(herd_final), copy.deepcopy(hires_final),
                         {"steady": dict(STEADY[branch]),
                          "spike_days": spike_days,
                          "shops": BRANCH_SHOPS[branch]},
                         freeze=freeze).run()
            curve = [dp.income for dp in pl.days]
            peak = max(curve[14:18])
            key = (peak, pl.cash)
            if best is None or key > best[0]:
                best = (key, pl, spike_days, curve)
        _, pl, spike_days, curve = best
        branch_sells[branch] = {dp.day: dict(dp.sell)
                                for dp in pl.days if dp.sell}
        branch_stats[branch] = {
            "spike_days": list(spike_days) if spike_days else [],
            "peak_d14_17": round(max(curve[14:18])),
            "peak_day": 14 + curve[14:18].index(max(curve[14:18])),
            "final_cash": round(pl.cash),
            "wool_sold": pl.sold.get("WOOL", 0),
            "wool_prod": pl.prod_cum.get("WOOL", 0),
            "income_curve": [round(x) for x in curve],
        }

    # ---------- 路由合成（双跑确定性） ----------
    routes = synth_routes(plan.days, branch_sells)
    if json.dumps(synth_routes(plan.days, branch_sells),
                  sort_keys=True) != json.dumps(routes, sort_keys=True):
        raise SystemExit("route synthesis is not deterministic")

    # ---------- 结构不变量 ----------
    assert list(routes) == ["default"] + [b for b in ROUTE_ORDER
                                          if b != "default"]
    for name, r in routes.items():
        assert len(r) == N_STEPS, f"{name} len {len(r)}"
    for branch, sw in SWITCH.items():
        assert routes[branch][:sw] == routes["default"][:sw], \
            f"{branch} prefix diverges before switch {sw}"
    for r in routes.values():
        for step in r:
            assert isinstance(step["farmer"], list) and step["farmer"]
            for h in step["hands"]:
                assert isinstance(h, list) and h
            assert len(step["market"]) <= 10

    # ---------- 三面差分 ----------
    base_routes, _, _ = decode_routes()
    diff = three_face_diff(base_routes, routes)

    # ---------- 落盘 ----------
    with open(os.path.join(HERE, "routes_v2.json"), "w", encoding="utf-8") as h:
        json.dump(routes, h, ensure_ascii=False, separators=(",", ":"))

    schedule = {
        "meta": {
            "task": "R9-G2b plan-layer three-face consistent regeneration",
            "generated": "2026-09-23",
            "faces": ["allocate_labor_plan (herd by care capacity)",
                      "derive_sell_schedule (M1 absorption + spike opt)",
                      "cash-gated production (push-forward, no no-op)"],
            "engine_notes": [
                "care bonus: fed+cared -> pending+1; yield 1+pending",
                "plants watered on plant day or die at EOD",
                "wheat window ages 2-4; melon window 6-12 (cap 6)",
                "EOD shed cap 100; daily fib hires; hands t0 dead step",
            ],
            "invariants": [
                "six routes byte-identical in production+movement faces",
                "branch prefixes identical to default up to switch points",
            ],
        },
        "herd_wish_final": {str(d): v for d, v in herd_final.items()},
        "hires_final": {str(d): v for d, v in hires_final.items()},
        "iterations": iter_log,
        "branches": branch_stats,
        "daily_plan": [{
            "day": dp.day, "crew": dp.crew, "land": dp.land, "buys": dp.buys,
            "plants": {str(t): c for t, c in dp.plants.items()},
            "places": [[str(t), k] for t, k in dp.places],
            "sell": dp.sell, "income": round(dp.income),
            "buy_wheat": dp.buy_wheat, "dropped": [list(x) for x in dp.dropped],
        } for dp in plan.days],
        "miss_log": plan.miss_log,
        "push_log": plan.push_log,
    }
    with open(os.path.join(HERE, "target_schedule_v2.json"), "w",
              encoding="utf-8") as h:
        json.dump(schedule, h, ensure_ascii=False, indent=1)
    with open(os.path.join(HERE, "surgery_v2_diff.json"), "w",
              encoding="utf-8") as h:
        json.dump(diff, h, ensure_ascii=False, indent=1)

    prod_kinds = collections.Counter(e["kind"] for e in diff["production"])
    report = {
        "base_sha256": sha256_bytes(open(BASE_MAIN, "rb").read()),
        "three_face_diff_scale": {
            "production_entries": len(diff["production"]),
            "production_kinds": dict(prod_kinds),
            "sell_entries": len(diff["sell"]),
            "sell_routes": sorted({e["route"] for e in diff["sell"]}),
            "movement_changed_days": len(diff["movement"]),
        },
        "prefix_identity": {b: f"byte-identical to default [:{sw}]"
                            for b, sw in SWITCH.items()},
        "movement_face_regenerated": True,
        "sell_face_regenerated": True,
        "preserved": [
            "route switch structure 88/120/153/216 + router config "
            "(blob-external, byte-identical)",
            "reaction layers (anti-clone preemptive sell / sell-slot "
            "reorder / terminal liquidation / weed repair) — modules "
            "outside blob, byte-identical",
        ],
        "determinism_double_run": True,
        "plan_iterations": iter_log,
        "branch_peaks": {b: branch_stats[b]["peak_d14_17"]
                         for b in branch_stats},
    }
    with open(os.path.join(HERE, "surgery_v2_report.json"), "w",
              encoding="utf-8") as h:
        json.dump(report, h, ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
