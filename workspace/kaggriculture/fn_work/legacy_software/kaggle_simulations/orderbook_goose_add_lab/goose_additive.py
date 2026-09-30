# -*- coding: utf-8 -*-
"""goose_additive（goose_add lab）：鹅线**加法扩栏版**重建（B4d；不发射/不提交/不改既有代码）。

背景（2026-09-29 goose-fullplan 判负复盘）：全计划鹅线败因=**以鹅换牛羊**
（撤 MILK/WOOL 供给让对手价差受益 +11.8k）。头部实拍=26 头大群**加鹅不减牛羊**
（C7-8/S3-8 保留、G10-12、畜线 18-19%/总 7.0-7.7k ops、终局钱中位 105.7k）。

本件=加法不换种（26 头级）：**保留基线 COW/SHEEP 链逐字不动**（牛奶/羊毛供给
零回撤），+10 GOOSE 新链（G10-12 新增口径），劳动链合成扩出（16-17 链→26 头级，
新链 FEED/CARE/收蛋工时由物流余量/新增雇工挤出——头部 7.0-7.7k ops 口径）。

引擎事实（kaggriculture env 源码逐条核验，fn_docs/docs/worker_route_scheduler_
design.md §1）：F1 移动无阻挡；F3 连续 2 日不喂逃走（放置 streak=0）；F4 FEED=
牲畜格+随身 1 小麦；F6 随身无上限+EOD 自动归棚（棚+随身≤100 溢出销毁）；F8 非法
动作=静默 no-op；F9 先单位动作后市场单。棚仓卖面必须**日产日卖清棚**（蛋出路
水力学件=上轮修复沿用：EGG 卖单按日产扩量清棚，否则棚满毁麦→FEED 断粮→逃逸）。

实证口径（本 lab 探针实测）：①SE 象限（x5-9/y5-9）为 LOCKED 未购地——+10 COOP
须 BUY_LAND（4000，第 3 次购地解锁 SE）；②BUY_LAND/BUY_ANIMAL 不足额=静默拒单
（须当日可用现金≥价）；③新雇工=当日基线雇工之后追加 HIRE（下标=基线日雇数+序，
基线手位零扰动）；④合成手从棚格出发 PICKUP WHEAT→PICKUP GOOSE→曼哈顿走线→
BUILD_COOP→PLACE→FEED→CARE 实测落位成活；⑤FEED 必须**日日不缺**（隔日喂实测
逃逸——streak 口径下隔日=1 日缺口叠加丢访即 2；日日喂+单日漏访自愈）。

手术面（纯加法）：市场单仅**追加**（BUY_LAND/BUY_ANIMAL/HIRE/SELL EGG），
hands 表仅**追加**（新雇工位），零既有单/零既有指令改写 → MILK/WOOL 供给
零回撤**构造性成立**（逐品供给量逐路由审计验证）。trunk d0-d3（0..143）零扰动。

三件协同（复用 goose_fullplan_lab）：排程（econ_model+头部参数+回本门控波次）/
劳动重推导（劳动链合成+逐日照护巡游）/外壳断言重生成（_GP_PLAN 计划表驱动，
常数由新磁带导出；只读探针直调 _alt_install）。孪生三闸（现金 min≥0/劳动
realized≥基线/棚容 held≤结构格）+守恒审计先行，回滚换档 ≤3 次（R9 口径）。
确定性：纯函数+固定序。CLI：python goose_additive.py --build [--routes 0,1]。
只写 orderbook_goose_add_lab/。
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import io
import json
import os
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))
if str(KSIM_DIR / "orderbook_goose_fullplan_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_fullplan_lab"))
_KAGGSIM = KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src" / "src-python"
if str(_KAGGSIM) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM))

from orderbook_r37 import retape_sheep as rs  # noqa: E402
import goose_line as gl  # noqa: E402  （Track/route_chains/_commit/audit/_rollout）
import goose_fullplan as gf  # noqa: E402  （labor_table/regen_assertions/assertion_probe/gate_route）

BASE_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
BUILD_DIR = HERE / "build"
EVID_DIR = HERE / "evidence"
RECORD_VERSION = "goose-additive/1.0"

TRUNK = 144           # branch 阈值（trunk 0..143 零扰动红线）
TAIL = 648
N_STEPS = 719
N_ADD = 10            # G10-12 新增口径：+10 GOOSE/路由（26 头级）
LAND_PRICE = 4000     # 第 3 次 BUY_LAND（SE 象限）
GOOSE_PRICE = 300
WAVE_SIZES = (4, 4, 2)          # 买鹅波次（头部 d6 主波/d8-9 次波/d10-11 收尾形制）
WAVE_SEARCH = range(6, 17)      # 波次起点搜索窗（回本门控：当日可用现金≥门槛）
WAVE_MONEY_GATE = 6000          # 首波门槛=购地 4000+4 鹅 1200+雇工余量
EGG_SELL_SLOTS_PER_DAY = 2
EGG_SELL_QTY = 10               # 2 槽×10=20/日≈10 鹅×2 枚（清棚供养）
EGG_FLOW_OFFSET = 4             # 首产 EOD pd+3 → 蛋流/卖点 pd+4
WHEAT_BUFFER_QTY = 12           # 日补麦（+10 头 FEED 日耗 10 麦；棚仓晨窗缓冲）

# 新鹅落位簇（SE 象限 x5-9/y5-9 近棚紧凑簇；头部中央簇 x2-6/y2-7 形制的近棚移植）。
# 序：近棚相邻对=同手两鹅（回棚取鹅腿最短）；远格（≥4 步）成波末=单鹅单手。
GOOSE_TILES = [(6, 5), (7, 5), (7, 6), (6, 6), (5, 6), (5, 7), (6, 7), (5, 8),
               (7, 7), (6, 8)]
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]   # 棚仓出入格（PICKUP/PLACE 均可）

HEAD_PARAMS = {
    "sample": "12 局 19 席（MMPQ 5/DSM 4/DECEM 6/VICTOR 4；2026-09-28~29 PUBLIC 回放）",
    "herd": "26 头大群加鹅不减牛羊：C7-8/S3-8 保留 + G10-12",
    "buy_goose": "d6 主波（12/19 席）/d8-9 次波（7/19）/d10-11 收尾——我方按回本门控平移",
    "coop_pattern": "中央簇紧凑块（x2-6/y2-7）——我方 SE 近棚簇（x5-8/y5-8）",
    "egg_harvest": "鹅格 HARVEST 最大间隙 2 日（19/19 席一致）",
    "egg_sell": "日产日卖；成交价/日均价 中位 1.00；qty 8/日（G10）",
    "labor_split": "畜线 18-19% / 作物线 28-31% / 物流 46-47%（总 7.0k-7.7k ops）",
    "money_end": "头部中位 105.7k",
    "econ": "GOOSE 300/首产 4 日/日产 1+pending（fed+cared）/max_held 4；EGG 价 hinge T=332",
}


# ============================================================ 排程（回本门控）==
def gen_schedule(pkg, avail, plans):
    """产线排程记录：econ_model 网格 top + 头部参数 + 逐路由波次/落位/劳动预算。"""
    import econ_model as em  # noqa: WPS433
    grid = em.enumerate_grid()
    top = grid[0]
    return {
        "version": "goose-additive-schedule/1.0",
        "econ_top": {"spec": top.get("spec"), "net": top.get("net"),
                     "income": top.get("income"), "min_cash": top.get("min_cash"),
                     "grid_src": "orderbook_goose_lab/econ_model.py"},
        "target_spec": {"GOOSE_ADD": N_ADD, "COW": "基线全保", "SHEEP": "基线全保",
                        "note": "26 头级加法扩栏：G10-12 新增、牛羊零回撤（上轮教训）"},
        "buy_waves": {"rule": "回本门控：波次起点=首日可用现金≥%d（购地+首波鹅+雇工）；"
                              "波次 %s；trunk d0-d3 零扰动" % (WAVE_MONEY_GATE, WAVE_SIZES),
                      "waves_by_route": {k: v["waves"] for k, v in plans.items()}},
        "coop_placement": {"rule": "BUY_LAND（%d，SE 象限）+ 近棚簇 %s（近棚=走线短=物流"
                                   "余量挤照护工时）" % (LAND_PRICE, GOOSE_TILES),
                           "head_pattern": HEAD_PARAMS["coop_pattern"]},
        "egg_rhythm": {"rule": "新鹅格 FEED 日日不缺（F3 逃逸红线）+ CARE/HARVEST 隔日交替"
                               "（HARVEST 间隙 ≤2 日，cap4×2 枚/日；CARE 0.5/日/头=头部口径）",
                       "head_max_gap": 2},
        "egg_sell": {"rule": "日产日卖清棚（水力学件沿用）：蛋流日（pd+%d）起每日 %d 槽×qty=%d"
                             " 追加 SELL EGG（零既有单改写）" % (EGG_FLOW_OFFSET, EGG_SELL_SLOTS_PER_DAY,
                                                        EGG_SELL_QTY),
                     "head": HEAD_PARAMS["egg_sell"]},
        "labor_budget": {"rule": "劳动链合成扩出：新链照护=合成雇工（基线日雇后追加 HIRE，"
                                 "基线手位零扰动）；走线从棚格近簇曼哈顿直达（物流余量挤出）",
                         "head_split": HEAD_PARAMS["labor_split"]},
        "head_params": HEAD_PARAMS,
    }


# ============================================================ 手术内部件 ==
def _walk_path(a, b):
    moves = []
    x, y = a
    X, Y = b
    while x < X:
        moves.append("EAST")
        x += 1
    while x > X:
        moves.append("WEST")
        x -= 1
    while y < Y:
        moves.append("SOUTH")
        y += 1
    while y > Y:
        moves.append("NORTH")
        y -= 1
    return moves


class RouteEditor:
    """单路由加法编辑器：市场单/hands 表仅追加；按步聚合提交（池增量最小）。

    base_pkg=基线包（只读；日雇工/槽位基准=基线序恒定），pkg=工作包（可写）。"""

    def __init__(self, pkg, rid, table, base_pkg=None):
        self.pkg = pkg
        self.base_pkg = base_pkg or pkg
        self.rid = rid
        self.table = table
        self._buf = {}       # step -> {"market": [orders], "ops": {hand: op}}
        self._hired = collections.Counter()   # day -> 本编辑器已追加 HIRE 数
        self.stats = collections.Counter()

    def _flush(self, step):
        buf = self._buf.pop(step, None)
        if not buf:
            return
        idxs, _i, act = gl._cow(self.pkg, self.rid, step)
        detail = {}
        if buf["market"]:
            act.setdefault("market", []).extend(buf["market"])
            detail["market_appended"] = buf["market"]
            self.stats["market_appended"] += len(buf["market"])
        if buf["ops"]:
            hands = act.setdefault("hands", [])
            for k in sorted(buf["ops"]):
                while len(hands) <= k:
                    hands.append(["PASS"])
                hands[k] = buf["ops"][k]
            detail["ops"] = {str(k): buf["ops"][k] for k in sorted(buf["ops"])}
            self.stats["hand_ops"] += len(buf["ops"])
        gl._commit(self.pkg, idxs, step, act, self.table, self.rid, "additive_edit", detail)

    def add_market(self, step, orders):
        self._buf.setdefault(step, {"market": [], "ops": {}})["market"].extend(orders)

    def set_op(self, step, hand, op):
        self._buf.setdefault(step, {"market": [], "ops": {}})["ops"][int(hand)] = list(op)

    def flush_all(self):
        for step in sorted(self._buf):
            self._flush(step)

    # ---- 基线日雇工/槽位查询（自基线包；编辑器只追加→基线序恒定）----
    def base_hires(self, day):
        out = []
        idxs = self.base_pkg["routes"][self.rid]
        for s in range(day * 24, min(day * 24 + 24, N_STEPS)):
            for o in (self.base_pkg["actions"][idxs[s]].get("market") or []):
                if isinstance(o, list) and o and o[0] == "HIRE":
                    out.append(s)
        return out

    def slots_free(self, step, pending=0):
        idxs = self.pkg["routes"][self.rid]
        a = self.pkg["actions"][idxs[step]]
        cur = len(a.get("market") or []) + len(self._buf.get(step, {}).get("market", []))
        return cur + pending <= 10

    def plan_hires(self, day, n):
        """当日追加 n 个 HIRE：**同一市场步**（同拍结算=同批出生=手位时序对齐；
        步≥基线最后雇工步→手位=基线日雇数+序，基线手位零扰动）。
        该步须一次有 n 空槽；放不下=当日雇工缺口（None,None，登记跳过）。"""
        base = self.base_hires(day)
        last = max(base) if base else day * 24 - 1
        first = len(base) + self._hired[day]
        for s in range(max(last, day * 24), min(day * 24 + 24, N_STEPS)):
            if self.slots_free(s, n):
                self.add_market(s, [["HIRE"]] * n)
                self._hired[day] += n
                return [s], first
        return None, None


def buy_order_slots(ed, day, from_step, orders, max_step=None):
    """把市场单分散到当日有槽位的步（from_step..max_step）；放不下=登记丢弃。
    max_step 默认=from_step+1：买单须先于合成手 PICKUP GOOSE 结算（F9）。"""
    hi = min(max_step if max_step is not None else from_step + 1,
             min(day * 24 + 24, N_STEPS) - 1)
    dropped = []
    for o in orders:
        placed = False
        for s in range(max(from_step, day * 24), hi + 1):
            if ed.slots_free(s, 1):
                ed.add_market(s, [list(o)])
                placed = True
                break
        if not placed:
            dropped.append(o)
    return dropped


def discover_spawns(ed, work, rid, day, hs, first, n_hands, fallback=(5, 5)):
    """新雇工出生格发现：先置 PASS（PASS 不动位）→flush→Track 读 (hs+1,hN)。"""
    for k in range(n_hands):
        ed.set_op(hs + 1, first + k, ["PASS"])
    ed.flush_all()
    tr = gl.Track(work, rid)
    out = {}
    for k in range(n_hands):
        p = tr.pos_at.get((hs + 1, "h%d" % (first + k)))
        out[first + k] = tuple(p) if p else tuple(fallback)
    return out


# ============================================================ 单路由手术 ==
def apply_route(pkg_base, work, rid, plan, table):
    """加法扩栏手术（纯追加）：BUY_LAND+买鹅波次+合成手放养巡游+蛋卖面+补麦供养。

    逐日处理（同日全部 HIRE 同拍结算→出生格一次发现→放养/巡游排程一致）。"""
    ed = RouteEditor(work, rid, table, base_pkg=pkg_base)
    waves = {int(d): (int(n), [tuple(t) for t in plan["wave_tiles"][w_i]])
             for w_i, (d, n) in enumerate(plan["waves"])}
    tiles = [tuple(t) for t in plan["tiles"]]
    placed = {}                     # tile -> day
    if not waves:
        ed.flush_all()
        plan["placed"] = {}
        return ed.stats
    first_day = min(waves)
    idxs = work["routes"][rid]

    def shed_dist(t):
        return min(abs(t[0] - s[0]) + abs(t[1] - s[1]) for s in SHED_TILES)

    for day in range(first_day, 30):
        day_end = min(day * 24 + 24, N_STEPS)
        # ---- 当日任务面：波次放养 + 已放养格照护 ----
        wave = waves.get(day)
        wave_tiles = wave[1] if wave else []
        n_wave = wave[0] if wave else 0
        far = any(shed_dist(t) >= 4 for t in wave_tiles)
        n_trip = (n_wave if far else (n_wave + 1) // 2) if wave else 0
        care_tiles = [t for t in tiles if placed.get(t, 99) < day]
        ordered = sorted(care_tiles, key=lambda t: (t[1], t[0]))
        n_care = min(2, max(1, (len(ordered) + 3) // 4)) if ordered else 0
        # ---- 补麦供养（棚仓晨窗缓冲；先占槽）----
        if placed or wave:
            dropped = buy_order_slots(ed, day, day * 24,
                                      [["BUY_PRODUCT", "WHEAT", WHEAT_BUFFER_QTY]],
                                      max_step=min(day * 24 + 6, N_STEPS - 1))
            if dropped:
                plan["buy_dropped"].append({"day": day, "orders": dropped})
        # ---- 同日全部 HIRE（同拍=同批出生；手位=基线日雇数+序）----
        n_hands = n_trip + n_care
        hs, first = (None, None)
        if n_hands:
            hs, first = ed.plan_hires(day, n_hands)
            if hs is None:
                plan["hire_gaps"].append(day)
                n_hands = 0
        # ---- 波次买单（≥PICKUP GOOSE 前结算；无合成手=不买防滞留）----
        if wave and hs:
            orders = [["BUY_ANIMAL", "GOOSE", n_wave]]
            if day == first_day:
                orders.insert(0, ["BUY_LAND"])
            dropped = buy_order_slots(ed, day, hs[0], orders)
            if dropped:
                plan["buy_dropped"].append({"day": day, "orders": dropped})
        if not n_hands:
            continue
        spawns = discover_spawns(ed, work, rid, day, hs[0], first, n_hands,
                                 plan["spawn_fallback"])
        # ---- 放养巡游（trip 手）----
        if wave and n_trip:
            seq_by_hand = collections.defaultdict(list)
            if far:
                for g, tile in enumerate(wave_tiles):
                    seq_by_hand[first + g].append(tile)
            else:
                for g, tile in enumerate(wave_tiles):
                    seq_by_hand[first + g // 2].append(tile)
            for hand, ts in sorted(seq_by_hand.items()):
                hstep = hs[0] + 1
                cur = spawns[hand]
                for j, tile in enumerate(ts):
                    placed[tile] = day
                    ops = []
                    if j > 0:
                        shed = min(SHED_TILES,
                                   key=lambda t: abs(t[0] - cur[0]) + abs(t[1] - cur[1]))
                        ops += [[m] for m in _walk_path(cur, shed)]
                        cur = shed
                    ops += [["PICKUP", "WHEAT", 3], ["PICKUP", "GOOSE"]] \
                        + [[m] for m in _walk_path(cur, tile)] \
                        + [["BUILD_COOP"], ["PLACE", "GOOSE"], ["FEED"], ["CARE"]]
                    for op in ops:
                        if hstep >= day_end:
                            plan["trip_overflow"].append({"day": day, "hand": hand,
                                                          "tile": list(tile)})
                            break
                        ed.set_op(hstep, hand, op)
                        hstep += 1
                    cur = tile
        # ---- 逐日照护（FEED 日日不缺；CARE/HARVEST 隔日交替；F4 随身麦）----
        if ordered:
            half = (len(ordered) + 1) // 2
            halves = [ordered[:half], ordered[half:]] if n_care == 2 else [ordered]
            for h_i, ts in enumerate(halves[:n_care]):
                if not ts:
                    continue
                hand = first + n_trip + h_i
                hstep = hs[0] + 1
                cur = spawns[hand]
                ops = [["PICKUP", "WHEAT", min(9, len(ts) + 1)]]
                for tile in ts:
                    ops += [[m] for m in _walk_path(cur, tile)]
                    harvest_day = ((day - placed[tile]) % 2 == 0
                                   and day >= placed[tile] + EGG_FLOW_OFFSET)
                    ops += [["FEED"], ["HARVEST"] if harvest_day else ["CARE"]]
                    cur = tile
                for op in ops:
                    if hstep >= day_end:
                        plan["care_trim"].append({"day": day, "hand": hand,
                                                  "dropped": op})
                        continue
                    ed.set_op(hstep, hand, op)
                    hstep += 1
        # ---- 蛋卖面（日产日卖清棚；零既有单改写）----
        if placed and day >= first_day + EGG_FLOW_OFFSET:
            cand = []
            for s in range(day * 24, day_end):
                a = work["actions"][idxs[s]]
                base_has_sell = any(isinstance(o, list) and o and o[0] == "SELL"
                                    for o in (a.get("market") or []))
                cand.append((0 if base_has_sell else 1, s))
            cand.sort()
            n_placed_orders = 0
            for _pri, s in cand:
                if n_placed_orders >= EGG_SELL_SLOTS_PER_DAY:
                    break
                if ed.slots_free(s, 1):
                    ed.add_market(s, [["SELL", "EGG", EGG_SELL_QTY]])
                    n_placed_orders += 1
            if n_placed_orders < EGG_SELL_SLOTS_PER_DAY:
                plan["sell_gap_days"].append(day)

    ed.flush_all()
    plan["placed"] = {("%d,%d" % k): v for k, v in placed.items()}
    return ed.stats


# ============================================================ 逐路由计划 ==
def route_plan(pkg_base, rid, n_add):
    """逐路由计划：回本门控波次 + 落位簇切片 + 记录器。"""
    return {"route": rid, "n_add": n_add, "waves": [], "wave_tiles": [],
            "tiles": [], "hire_gaps": [], "buy_dropped": [], "trip_overflow": [],
            "care_trim": [], "sell_gap_days": [], "spawn_fallback": (5, 5)}


def build_plans(pkg_base, rids, base_rolls, n_add):
    plans = {}
    for rid in rids:
        plan = route_plan(pkg_base, rid, n_add)
        mb = base_rolls[rid]["money_by_day"]
        # 当日可用现金=前一日终值（money_by_day[d]=d+1 日初）
        def avail(d):
            return mb[d - 1] if 1 <= d < len(mb) else (3000.0 if d == 0 else 0.0)
        w1 = None
        for d in WAVE_SEARCH:
            if avail(d) >= WAVE_MONEY_GATE:
                w1 = d
                break
        if w1 is None:
            plan["waves"] = []
            plans[rid] = plan
            continue
        left = n_add
        waves = []
        for i, sz in enumerate(WAVE_SIZES):
            if left <= 0:
                break
            take = min(sz, left)
            waves.append((w1 + i, take))
            left -= take
        if left > 0:
            waves.append((w1 + len(WAVE_SIZES), left))
        plan["waves"] = waves
        ti = 0
        for _day, n in waves:
            plan["wave_tiles"].append([list(t) for t in GOOSE_TILES[ti:ti + n]])
            ti += n
        plan["tiles"] = [list(t) for t in GOOSE_TILES[:n_add]]
        plans[rid] = plan
    return plans


# ============================================================ 主构建 ==
def main_build(route_sel=None, n_add=N_ADD):
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    base_text = BASE_MAIN.read_text(encoding="utf-8")
    pkg_base = rs._decode_routes(base_text)
    rids = sorted(pkg_base["routes"], key=lambda k: int(k))
    if route_sel:
        want = set(str(r) for r in route_sel)
        rids = [r for r in rids if r in want]

    from kaggsim.serve import Serve  # noqa: WPS433
    srv = Serve()
    try:
        base_rolls = {rid: gl._rollout(pkg_base, rid, 780010, srv=srv) for rid in rids}
    finally:
        srv.close()

    plans = build_plans(pkg_base, rids, base_rolls, n_add)
    schedule = gen_schedule(pkg_base, {r: base_rolls[r]["money_by_day"] for r in rids}, plans)

    work = copy.deepcopy(pkg_base)
    table = []
    route_rows = []
    rollback_rows = []
    srv = Serve()
    try:
        for rid in rids:
            n_rb = 0
            while True:
                work["routes"][rid] = list(pkg_base["routes"][rid])
                table[:] = [r for r in table if r["route"] != rid]
                sub = []
                plan = plans[rid]
                # 回滚=减档（重算波次/落位切片）
                cur_add = max(0, n_add - 2 * n_rb)
                p2 = build_plans(pkg_base, [rid], base_rolls, cur_add)[rid]
                p2["hire_gaps"] = plan["hire_gaps"]
                plans[rid] = p2
                plan = p2
                stats = collections.Counter()
                if plan["waves"]:
                    stats.update(apply_route(pkg_base, work, rid, plan, sub))
                table.extend(sub)
                v = gl._rollout(work, rid, 780010, srv=srv)
                row = gf.gate_route(base_rolls[rid], v)
                row["route"] = rid
                row["n_add"] = cur_add if plan["waves"] else 0
                row["n_rollbacks"] = n_rb
                row["waves"] = plan["waves"]
                row["herd_target_goose"] = (collections.Counter(
                    c["species"] for c in gl.route_chains(pkg_base, rid)).get("GOOSE", 0)
                    + (cur_add if plan["waves"] else 0))
                row["herd_realized_goose"] = int(v["held"].get("GOOSE", 0))
                row["stats"] = dict(stats)
                ok_extra = row["herd_realized_goose"] >= row["herd_target_goose"]
                row["ok"] = bool(row["ok"] and ok_extra)
                if row["ok"] or n_rb >= 3 or cur_add <= 0:
                    route_rows.append(row)
                    break
                n_rb += 1
                rollback_rows.append(
                    {"route": rid, "iter": n_rb, "why": {
                        "cash_ok": row["cash_ok"], "labor_ok": row["labor_ok"],
                        "cap_ok": row["cap_ok"], "herd_ok": ok_extra,
                        "min_money": [row["min_money_base"], row["min_money_var"]],
                        "realized": [row["realized_base"], row["realized_var"]],
                        "held_var": row["held_var"]}})
        rs._pool_residue_sweep(work)

        # ---- 守恒+供给审计 ----
        rows = []
        supply = {}
        for rid in rids:
            arch = collections.Counter(c["species"] for c in gl.route_chains(work, rid))
            base_arch = collections.Counter(c["species"] for c in gl.route_chains(pkg_base, rid))
            rows.append({"route": rid, "target": dict(arch)})
            # 逐品供给（挂单量）：仅追加 → 每品 ≥ 基线（构造性零回撤）
            per = {"base": collections.Counter(), "var": collections.Counter()}
            for tag, pkg in (("base", pkg_base), ("var", work)):
                idxs = pkg["routes"][rid]
                for s in range(N_STEPS):
                    for o in (pkg["actions"][idxs[s]].get("market") or []):
                        if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL":
                            per[tag][str(o[1])] += int(o[2])
            items = sorted(set(per["base"]) | set(per["var"]))
            supply[rid] = {"base": dict(per["base"]), "var": dict(per["var"]),
                           "zero_withdrawal": all(per["var"][it] >= per["base"][it]
                                                  for it in items),
                           "milk_wool_ok": all(per["var"][it] >= per["base"][it]
                                               for it in ("MILK", "WOOL")),
                           "base_arch": dict(base_arch), "var_arch": dict(arch)}
        audit = gl.audit_variant(pkg_base, work, table, rows)
        # 加法口径槽审计：市场单仅追加（基线单=前缀保全）且 ≤10 帽；hands 表仅追加
        slot_add_ok = True
        prefix_ok = True
        for rid in rids:
            ib, iw = pkg_base["routes"][rid], work["routes"][rid]
            for s in range(N_STEPS):
                mb = pkg_base["actions"][ib[s]].get("market") or []
                mw = work["actions"][iw[s]].get("market") or []
                if len(mw) > 10 or len(mw) < len(mb):
                    slot_add_ok = False
                elif mw[:len(mb)] != mb:
                    prefix_ok = False
                hb = pkg_base["actions"][ib[s]].get("hands") or []
                hw = work["actions"][iw[s]].get("hands") or []
                if hw[:len(hb)] != hb:
                    prefix_ok = False
        audit["slot_ok_legacy_caliber"] = audit.get("slot_ok")
        audit["slot_ok"] = bool(slot_add_ok and prefix_ok)
        audit["slot_additive"] = {"orders_append_only": bool(slot_add_ok),
                                  "base_orders_prefix_preserved": bool(prefix_ok)}
    finally:
        srv.close()

    # ---- 外壳断言协同重生成（_GP_PLAN 计划表驱动）----
    new_blob_text = rs._encode_routes(base_text, work)
    final_text, assert_regen = gf.regen_assertions(new_blob_text, work)
    pkg_dir, man = write_package(final_text, base_text, table)
    probe = gf.assertion_probe(pkg_dir / "main.py")

    out = {
        "version": RECORD_VERSION,
        "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "schedule": schedule,
        "n_table_rows": len(table),
        "route_gates": route_rows,
        "rollbacks": rollback_rows,
        "n_bad_routes": sum(1 for r in route_rows if not r["ok"]),
        "audit": {"conservation_n": len(audit.get("conservation", [])),
                  "conservation_match": sum(1 for c in audit.get("conservation", [])
                                            if c.get("match")),
                  "slot_ok": audit.get("slot_ok"),
                  "shared_seg": audit.get("shared_seg"),
                  "n_table_rows": audit.get("n_table_rows")},
        "supply_check": supply,
        "assert_regen": assert_regen,
        "assert_probe": probe,
        "manifest": man,
        "pkg_dir": str(pkg_dir),
        "labor_tables": {rid: gf.labor_table(work, rid) for rid in rids[:6]},
        "plans": {k: v for k, v in plans.items()},
        "twin_money_sample": [{"route": r["route"], "final_base": r["final_money_base"],
                               "final_var": r["final_money_var"],
                               "min_var": r["min_money_var"],
                               "herd_target_g": r["herd_target_goose"],
                               "herd_realized_g": r["herd_realized_goose"]}
                              for r in route_rows],
    }
    (EVID_DIR / "goose_add_build.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    (EVID_DIR / "change_table_goose_add.json").write_text(
        json.dumps(table[:20000], ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("bad_routes:", out["n_bad_routes"], "assert_probe:", probe.get("passed"),
          "n_table_rows:", out["n_table_rows"],
          "elapsed:", round(time.perf_counter() - t0, 1), flush=True)
    return out


def write_package(main_text, base_text, table):
    d = BUILD_DIR / "goose_add"
    d.mkdir(parents=True, exist_ok=True)
    (d / "main.py").write_text(main_text, encoding="utf-8")
    main_bytes = main_text.encode("utf-8")
    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w:gz") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    tar_bytes = tar_buf.getvalue()
    (d / "submission.tar.gz").write_bytes(tar_bytes)
    man = {
        "form": "goose_add", "entry": "_hs_agent",
        "base_main": str(BASE_MAIN),
        "base_main_sha256": hashlib.sha256(base_text.encode("utf-8")).hexdigest(),
        "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes),
        "diff_scope": "_R108_DATA blob + 外壳断言重生成块（_GP_PLAN）——纯加法（市场单/"
                      "hands 表仅追加，零既有行改写）",
        "n_change_rows": len(table),
    }
    (d / "build_manifest.json").write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    return d, man


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--routes", type=str, default="")
    ap.add_argument("--n-add", type=int, default=N_ADD)
    args = ap.parse_args()
    if args.build:
        sel = [r for r in args.routes.split(",") if r.strip()] if args.routes else None
        main_build(route_sel=sel, n_add=args.n_add)
    else:
        ap.print_help()
