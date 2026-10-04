# -*- coding: utf-8 -*-
"""goose_line（goose lab）：鹅线产线重生成磁带手术 + feasibility 孪生 + 四门。

责任口径（任务 B4b，不发射/不提交/不动既有代码）：把 econ_model 解出的鹅线
排程**重生成**进 H1 磁带（基底=orderbook_strongest_lab/build/h1/main.py，
sha 76b5f842…）——非抄磁带（R9/G2 教训），产线事件按解出的排程重建：
- BUY_GOOSE：物种换链（BUY_ANIMAL+PICKUP+PLACE 三联）+ 结构翻转
  （PASTURE↔COOP，按落位格 BUILD 事件翻转）；头数守恒按目标谱（量守恒）。
  qty>1 买单拆分=同拍槽内追加（同拍卖零跨拍；10 单帽下），qty 减量删链保槽。
- FEED/CARE：日节奏保留（FEED 日日保命/ CARE=产出翻倍 lever 不动）。
- 收蛋节奏：鹅格 HARVEST 间隙 ≤2 日（cap 4 vs 2 枚/日产出），冗余位
  COLLECT_FERTILIZER→HARVEST 再分配（肥料池价塌 vs 蛋对数吸收=蛋优先，
  econ_model 面登记取舍）。
- 卖单面跟随产线：蛋卖点按吸收节奏（中段 EGG 单量按产比缩放+富余 WOOL/
  MILK 槽改写为 EGG 日产节奏）；WOOL/MILK 单量按余量产比缩放；FERT 早卖
  晚买节奏不动（基线已是该形）。
四护栏：写时复制（retape_sheep 池语义）/量守恒核算/逐事件审计 change_table/
feasibility 孪生三闸（现金≥0·劳动不劣于基线·棚容结构正确）。
确定性：纯函数+固定序。CLI：python goose_line.py --build-all。
只写 orderbook_goose_lab/。
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
_KAGGSIM = KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src" / "src-python"
if str(_KAGGSIM) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM))

from orderbook_r37 import retape_sheep as rs  # noqa: E402

H1_MAIN = (KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
BUILD_DIR = HERE / "build"
EVID_DIR = HERE / "evidence"
RECORD_VERSION = "goose-line/1.0"

N_STEPS = 719
TRUNK_STEPS = 144          # steps 0..143 = d0..d5（route 0 trunk；router step144 换线）
TAIL_STEPS = 648           # steps 648..718 = d27..d29（route 2 tail；router step648 换线）
MOVES = {"NORTH": (0, -1), "SOUTH": (0, 1), "WEST": (-1, 0), "EAST": (1, 0)}
SHED_TILES = [(4, 4), (5, 4), (4, 5), (5, 5)]
ANIMALS = ("GOOSE", "COW", "SHEEP")
MAX_ORDERS = 10            # maxMarketOrdersPerTurn
EGG_FLOW_FIRST_DAY = 5     # 鹅首产 EOD d3 于满照护（pd0）→ 蛋流 d4 起，卖点 d5 起

VARIANT_SPECS = {
    "goose5": {"target": {"GOOSE": 5, "COW": 6, "SHEEP": 6},
               "desc": "纯增量档 5 鹅（6牛6羊5鹅 17 头）"},
    "goose7": {"target": {"GOOSE": 7, "COW": 6, "SHEEP": 4},
               "desc": "纯增量档 7 鹅（6牛4羊7鹅 17 头）"},
    "goose9": {"target": {"GOOSE": 9, "COW": 6, "SHEEP": 2},
               "desc": "纯增量档 9 鹅（6牛2羊9鹅 17 头）"},
    "mix76": {"target": {"GOOSE": 7, "COW": 6, "SHEEP": 0},
              "desc": "混合档 7鹅6牛（13 头菜单口径）"},
    "mix79": {"target": {"GOOSE": 7, "COW": 0, "SHEEP": 9},
              "desc": "混合档 7鹅9羊（16 头菜单口径）"},
    "goose9econ": {"target": {"GOOSE": 9, "COW": 4, "SHEEP": 2},
                   "desc": "经济解最优档 9鹅4牛2羊（网格 top1）"},
}


# ============================================================ 单元位置跟踪 ==
def units_of(a):
    """动作 → [(unit_id, 指令)]；unit_id='F' 或 'hN'。"""
    fu = a.get("farmer")
    if isinstance(fu, list) and fu and isinstance(fu[0], str):
        yield "F", fu
    for i, h in enumerate(a.get("hands") or []):
        if isinstance(h, list) and h and isinstance(h[0], str):
            yield "h%d" % i, h


class Track:
    """路由磁带单元位置跟踪（引擎 _spawn_hand/_end_of_day 语义复刻）。

    校验：route 0/2/101/109 对 gengame 终局落位格 4/4 吻合（goose_line
    开发期实测；route 101 一格引擎 no-op 属基线自身库存缺链，非跟踪误差）。
    """

    def __init__(self, pkg, rid):
        self.rid = rid
        self.events = []      # (step, unit, op, pos, args)
        self.by_step_unit = {}
        self.pos_at = {}      # (step, unit) -> pos（动作执行后）
        self._run(pkg)

    def _run(self, pkg):
        idxs = pkg["routes"][self.rid]
        pos = {"F": (4, 4)}
        hands = []
        for s, i in enumerate(idxs):
            a = pkg["actions"][i]
            for u, op in units_of(a):
                if u != "F":
                    n = int(u[1:])
                    while len(hands) <= n:
                        hands.append("h%d" % len(hands))
                    uid = hands[n]
                else:
                    uid = "F"
                p = pos.get(uid)
                if p is None:
                    continue
                if op[0] in MOVES:
                    dx, dy = MOVES[op[0]]
                    nx, ny = p[0] + dx, p[1] + dy
                    if 0 <= nx < 10 and 0 <= ny < 10:
                        pos[uid] = (nx, ny)
                else:
                    args = tuple(op[1:]) if len(op) > 1 else ()
                    self.events.append((s, uid, op[0], tuple(p), args))
                    self.by_step_unit[(s, uid)] = (op[0], tuple(p), args)
                self.pos_at[(s, uid)] = tuple(pos.get(uid) or (-1, -1))
            for o in (a.get("market") or []):
                if isinstance(o, list) and o and o[0] == "HIRE":
                    occ = {t: 0 for t in SHED_TILES}
                    for q in list(pos.values()):
                        if q in occ:
                            occ[q] += 1
                    best = sorted(occ.items(),
                                  key=lambda kv: (kv[1], SHED_TILES.index(kv[0])))[0][0]
                    hid = "h%d" % len(hands)
                    hands.append(hid)
                    pos[hid] = best
            if (s + 1) % 24 == 0:
                pos = {"F": (4, 4)}
                hands = []

    def placements(self):
        out = {}
        for s, u, op, p, args in self.events:
            if op == "PLACE" and args and args[0] in ANIMALS:
                out.setdefault(tuple(p), (args[0], s, u))
        return out

    def builds(self):
        out = collections.defaultdict(list)
        for s, u, op, p, args in self.events:
            if op in ("BUILD_PASTURE", "BUILD_COOP"):
                out[tuple(p)].append((s, u, op))
        return out

    def tile_visits(self):
        out = collections.defaultdict(list)   # tile -> [(step, unit, op)]
        for s, u, op, p, args in self.events:
            if op in ("FEED", "CARE", "HARVEST", "COLLECT_FERTILIZER"):
                out[tuple(p)].append((s, u, op))
        return out


# ============================================================ 链与画像 ==
def route_chains(pkg, rid):
    """物种放置链（FIFO 扫线精确配对；qty>1 买单摊多链）+ 落位格。"""
    idxs = pkg["routes"][rid]
    tr = Track(pkg, rid)
    pl = tr.positions if False else None  # noqa（占位防误用）
    placements = tr.placements()          # tile -> (species, pl_step, unit)
    pl_by = {}
    for tile, (sp, ps, pu) in placements.items():
        pl_by[(ps, pu)] = tile
    out = []
    for sp in ANIMALS:
        queue = []
        pending = {}
        for s, i in enumerate(idxs):
            a = pkg["actions"][i]
            for j, o in enumerate(a.get("market") or []):
                if isinstance(o, list) and o and o[0] == "BUY_ANIMAL" \
                        and len(o) > 1 and o[1] == sp:
                    q = int(o[2]) if len(o) > 2 else 1
                    for _ in range(int(q)):
                        queue.append((s, j))
            for u, op in units_of(a):
                if not (isinstance(op, list) and len(op) > 1):
                    continue
                if op[0] == "PICKUP" and op[1] == sp:
                    if queue:
                        b = queue.pop(0)
                        pending[u] = {"species": sp, "buy_step": b[0],
                                      "buy_slot": b[1], "pu_step": s,
                                      "pu_unit": u}
                elif op[0] == "PLACE" and op[1] == sp:
                    d = pending.pop(u, None)
                    if d is not None:
                        d["pl_step"] = s
                        d["pl_unit"] = u
                        d["tile"] = pl_by.get((s, u))
                        out.append(d)
    out.sort(key=lambda c: (c["buy_step"], c["buy_slot"], c["pl_step"]))
    return out


def route_profile(pkg, rid):
    """画像：买单量 arch + 链 arch + 作物种植。"""
    idxs = pkg["routes"][rid]
    buy = collections.Counter()
    plant = collections.Counter()
    for s, i in enumerate(idxs):
        a = pkg["actions"][i]
        for o in (a.get("market") or []):
            if isinstance(o, list) and o and o[0] == "BUY_ANIMAL" and len(o) > 2:
                buy[o[1]] += int(o[2])
        for u, op in units_of(a):
            if isinstance(op, list) and len(op) > 1 and op[0] == "PLANT":
                plant[op[1]] += 1
    ch = route_chains(pkg, rid)
    chn = collections.Counter(c["species"] for c in ch)
    return {"buy": dict(buy), "chains": dict(chn), "plant": dict(plant),
            "n_chains": len(ch)}


def largest_remainder(spec, n):
    """目标谱按头数 n 最大余数法缩放（量守恒到该路由链数）。"""
    tot = sum(int(v) for v in spec.values()) or 1
    raw = {k: int(v) * n / tot for k, v in spec.items()}
    base = {k: int(v // 1) for k, v in raw.items()}
    short = n - sum(base.values())
    order = sorted(raw, key=lambda k: (-(raw[k] - base[k]), k))
    for k in order[:max(0, short)]:
        base[k] += 1
    return {k: int(base.get(k, 0)) for k in spec}


def trunk_target(spec):
    return largest_remainder(spec, 6)


# ============================================================ 手术件 ==
def _cow(pkg, rid, step):
    return rs._cow_action(pkg, rid, step)


def _commit(pkg, idxs, step, act, table, rid, kind, detail):
    rs._commit_action(pkg, idxs, step, act)
    row = {"route": rid, "step": step, "kind": kind}
    row.update(detail)
    table.append(row)


def _order_qty(act, slot):
    o = act["market"][slot]
    return int(o[2]) if len(o) > 2 else 1


def convert_chain(pkg, rid, chain, to_sp, table):
    """链物种 A→B：买单（整单改种或同拍拆单）+ PICKUP/PLACE 改种 + 格结构翻转。

    同拍拆单=qty>1 时把 qty 减 1 并同拍末位追加 [BUY_ANIMAL B 1]（同拍卖
    内零跨拍；<10 单帽）。返回 'ok' / 'no_slot'。
    """
    sp = chain["species"]
    if sp == to_sp:
        return "ok"
    # 买单
    idxs, idx, act = _cow(pkg, rid, chain["buy_step"])
    o = act["market"][chain["buy_slot"]]
    q = _order_qty(act, chain["buy_slot"])
    old = list(o)
    if q <= 1:
        o[1] = to_sp
        _commit(pkg, idxs, chain["buy_step"], act, table, rid,
                "buy_species", {"slot": chain["buy_slot"], "from": old,
                                "to": list(o)})
    else:
        if len(act["market"]) >= MAX_ORDERS:
            return "no_slot"
        o[2] = q - 1
        _commit(pkg, idxs, chain["buy_step"], act, table, rid,
                "buy_qty_dec", {"slot": chain["buy_slot"], "from": old,
                                "to": list(o)})
        idxs2, _i2, act2 = _cow(pkg, rid, chain["buy_step"])
        act2["market"].append(["BUY_ANIMAL", to_sp, 1])
        _commit(pkg, idxs2, chain["buy_step"], act2, table, rid,
                "buy_split_append", {"slot": len(act2["market"]) - 1,
                                     "from": None,
                                     "to": ["BUY_ANIMAL", to_sp, 1]})
    # 单元指令
    for key, verb in (("pu_step", "PICKUP"), ("pl_step", "PLACE")):
        step, unit = chain[key], chain["pu_unit"] if verb == "PICKUP" else chain["pl_unit"]
        idxs3, _i3, act3 = _cow(pkg, rid, step)
        old_op = None
        if unit == "F":
            old_op = list(act3.get("farmer") or [])
            act3["farmer"] = [verb, to_sp]
        else:
            k = int(unit[1:])
            hands = act3.setdefault("hands", [])
            while len(hands) <= k:
                hands.append(["PASS"])
            old_op = list(hands[k])
            hands[k] = [verb, to_sp]
        _commit(pkg, idxs3, step, act3, table, rid,
                verb.lower() + "_species", {"unit": unit, "from": old_op,
                                            "to": [verb, to_sp]})
    # 落位格结构翻转（仅 GOOSE↔非 GOOSE 需 PASTURE↔COOP；同结构不翻）
    tile = chain.get("tile")
    if tile is not None and (sp == "GOOSE") != (to_sp == "GOOSE"):
        want = "BUILD_COOP" if to_sp == "GOOSE" else "BUILD_PASTURE"
        other = "BUILD_PASTURE" if to_sp == "GOOSE" else "BUILD_COOP"
        tr = Track(pkg, rid)
        builds = tr.builds().get(tuple(tile), [])
        for bs, bu, bop in builds:
            if bop == other:
                idxs4, _i4, act4 = _cow(pkg, rid, bs)
                old_op = None
                if bu == "F":
                    old_op = list(act4.get("farmer") or [])
                    act4["farmer"] = [want]
                else:
                    k = int(bu[1:])
                    hands = act4.setdefault("hands", [])
                    while len(hands) <= k:
                        hands.append(["PASS"])
                    old_op = list(hands[k])
                    hands[k] = [want]
                _commit(pkg, idxs4, bs, act4, table, rid,
                        "build_flip", {"unit": bu, "tile": list(tile),
                                       "from": old_op, "to": [want]})
                break
    return "ok"


def drop_chain(pkg, rid, chain, table):
    """删链（头数下调）：买单 qty−1（0=占坑保槽）+ PICKUP/PLACE 置 PASS。"""
    idxs, idx, act = _cow(pkg, rid, chain["buy_step"])
    o = act["market"][chain["buy_slot"]]
    old = list(o)
    q = _order_qty(act, chain["buy_slot"])
    o[2] = max(0, q - 1)
    _commit(pkg, idxs, chain["buy_step"], act, table, rid,
            "buy_qty_dec", {"slot": chain["buy_slot"], "from": old, "to": list(o)})
    for key, verb in (("pu_step", "PICKUP"), ("pl_step", "PLACE")):
        step = chain[key]
        unit = chain["pu_unit"] if verb == "PICKUP" else chain["pl_unit"]
        idxs2, _i2, act2 = _cow(pkg, rid, step)
        old_op = None
        if unit == "F":
            old_op = list(act2.get("farmer") or [])
            act2["farmer"] = ["PASS"]
        else:
            k = int(unit[1:])
            hands = act2.setdefault("hands", [])
            while len(hands) <= k:
                hands.append(["PASS"])
            old_op = list(hands[k])
            hands[k] = ["PASS"]
        _commit(pkg, idxs2, step, act2, table, rid,
                verb.lower() + "_drop", {"unit": unit, "from": old_op,
                                         "to": ["PASS"]})
    return "ok"


def _chain_ok_after(chain, done_ids):
    return id(chain) not in done_ids


def apply_target(pkg, rid, chains, target, table, region, stats):
    """把某区（trunk/branch）链换/删到目标谱（贪心：先补 GOOSE 缺口）。"""
    have = collections.Counter(c["species"] for c in chains)
    need = {sp: int(target.get(sp, 0)) - int(have.get(sp, 0)) for sp in ANIMALS}
    used = set()
    # 转换对（to 缺口 from 盈余）：GOOSE 缺口优先（SHEEP→GOOSE > COW→GOOSE）
    pairs = []
    for to_sp in ("GOOSE", "COW", "SHEEP"):
        if need[to_sp] <= 0:
            continue
        for from_sp in ("SHEEP", "COW", "GOOSE"):
            if from_sp == to_sp or need[from_sp] >= 0:
                continue
            pairs.append((from_sp, to_sp))
    for from_sp, to_sp in pairs:
        while need[to_sp] > 0 and need[from_sp] < 0:
            cand = [c for c in chains
                    if c["species"] == from_sp and _chain_ok_after(c, used)]
            if not cand:
                break
            ch = cand[0]
            rc = convert_chain(pkg, rid, ch, to_sp, table)
            if rc != "ok":
                stats["convert_blocked"] += 1
                used.add(id(ch))
                continue
            used.add(id(ch))
            stats["converted"] += 1
            stats["conv_%s_to_%s" % (from_sp, to_sp)] = \
                stats.get("conv_%s_to_%s" % (from_sp, to_sp), 0) + 1
            need[to_sp] -= 1
            need[from_sp] += 1
    # 头数差（链数≠目标和）：删盈余
    for sp in ANIMALS:
        while need[sp] < 0:
            cand = [c for c in chains
                    if c["species"] == sp and _chain_ok_after(c, used)]
            if not cand:
                break
            drop_chain(pkg, rid, cand[-1], table)
            used.add(id(cand[-1]))
            need[sp] += 1
            stats["dropped"] += 1
    return stats


# ============================================================ 收蛋节奏 ==
def egg_rhythm(pkg, rid, goose_tiles, table, stats, all_tiles=None):
    """鹅格收蛋节奏：HARVEST 间隙 ≤2 日（cap4×2 枚/日）。冗余位 COLLECT_
    FERTILIZER→HARVEST 再分配；FEED/CARE 不动（保命/产出双 lever）。

    尾段（d27+）对全部落位格做日域规则（HARVEST 物种无关=零风险；跨 branch
    换线后 tile 集按本路由登记，尾段改动仅 route 2 尾被复用，偏差信息登记）。
    """
    tr = Track(pkg, rid)
    visits = tr.tile_visits()
    tiles = sorted(set(tuple(t) for t in goose_tiles))
    if all_tiles:
        tiles = sorted(set(tiles) | set(tuple(t) for t in all_tiles))
    for tile in tiles:
        vs = visits.get(tuple(tile), [])
        by_day = collections.defaultdict(list)
        for s, u, op in vs:
            by_day[s // 24].append((s, u, op))
        last_h = None
        for d in range(30):
            day_ops = by_day.get(d, [])
            has_h = any(op == "HARVEST" for _, _, op in day_ops)
            if has_h:
                last_h = d
                continue
            # 尾段（d27+）日域规则（跨 branch 无关=共享段安全）；其余带间隙看回
            if d >= TAIL_STEPS // 24:
                need_h = True
            else:
                need_h = (last_h is None and d >= 4) or \
                         (last_h is not None and d - last_h >= 2)
            if not need_h or not day_ops:
                continue
            # 候选：COLLECT_FERTILIZER（后出现的优先）
            cand = [(s, u) for s, u, op in day_ops if op == "COLLECT_FERTILIZER"]
            if not cand:
                stats["rhythm_deficit_days"] += 1
                continue
            s, u = cand[-1]
            idxs, _i, act = _cow(pkg, rid, s)
            old_op = None
            if u == "F":
                old_op = list(act.get("farmer") or [])
                act["farmer"] = ["HARVEST"]
            else:
                k = int(u[1:])
                hands = act.setdefault("hands", [])
                while len(hands) <= k:
                    hands.append(["PASS"])
                old_op = list(hands[k])
                hands[k] = ["HARVEST"]
            _commit(pkg, idxs, s, act, table, rid, "rhythm_x_to_h",
                    {"unit": u, "tile": list(tile), "day": d, "from": old_op,
                     "to": ["HARVEST"]})
            stats["rhythm_converted"] += 1
            last_h = d


# ============================================================ 卖单面 ==
def sell_face(pkg, rid, goose_tiles_all, base_egg, tgt_egg, base_prod, tgt_prod,
              table, stats):
    """卖单面跟随产线：中段（144..647）EGG 按产比缩放+富余 WOOL/MILK 槽
    改写 EGG（吸收节奏）；WOOL/MILK 按余量产比缩放；尾段卖单不动（sell-all
    哨兵自适应）；FERT 不动（早卖晚买基线已成形）。"""
    idxs = pkg["routes"][rid]
    ratio_egg = (tgt_egg / base_egg) if base_egg > 0 else 1.0
    ratios = {}
    for it in ("MILK", "WOOL"):
        b, t = base_prod.get(it, 0.0), tgt_prod.get(it, 0.0)
        ratios[it] = (t / b) if b > 0 else 0.0
    slots = []        # (step, slot, item, qty)
    for s in range(TRUNK_STEPS, TAIL_STEPS):
        a = pkg["actions"][idxs[s]]
        for j, o in enumerate(a.get("market") or []):
            if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL" \
                    and o[1] in ("EGG", "MILK", "WOOL"):
                slots.append((s, j, o[1], int(o[2])))
    egg_slots = [x for x in slots if x[2] == "EGG"]
    surplus = [x for x in slots if x[2] in ("MILK", "WOOL")]
    # 1) EGG 存量槽量按产比缩放（≥1 保节奏）
    for s, j, it, q in egg_slots:
        nq = max(1, int(round(q * ratio_egg))) if q > 0 else 0
        if nq != q:
            idxs2, _i, act = _cow(pkg, rid, s)
            o = act["market"][j]
            old = list(o)
            o[2] = nq
            _commit(pkg, idxs2, s, act, table, rid, "sell_qty_scale",
                    {"slot": j, "item": it, "from": old, "to": list(o)})
            stats["sell_qty_scaled"] += 1
    # 2) 富余 WOOL/MILK 槽（超出余量产比所需）→ 改写 EGG 日产节奏
    keep = {}
    for it in ("MILK", "WOOL"):
        rows = [x for x in surplus if x[2] == it]
        keep[it] = max(0, int(round(len(rows) * ratios[it])))
    retarget = []
    for it in ("MILK", "WOOL"):
        rows = [x for x in surplus if x[2] == it]
        k = keep[it]
        retarget.extend(rows[k:])
        for s, j, it2, q in rows[:k]:
            nq = max(1, int(round(q * ratios[it2]))) if q > 0 else 0
            if nq != q:
                idxs2, _i, act = _cow(pkg, rid, s)
                o = act["market"][j]
                old = list(o)
                o[2] = nq
                _commit(pkg, idxs2, s, act, table, rid, "sell_qty_scale",
                        {"slot": j, "item": it2, "from": old, "to": list(o)})
                stats["sell_qty_scaled"] += 1
    # 改写目标：蛋流日起按日节奏摊（qty=日产 2×G）
    daily = max(1, 2 * int(tgt_egg))
    rt_sorted = sorted(retarget, key=lambda x: x[0])
    day_seen = collections.Counter()
    for s, j, it, q in rt_sorted:
        d = s // 24
        if d < EGG_FLOW_FIRST_DAY:
            continue
        if day_seen[d] >= 2:          # 每日至多 2 个改写点（吸收节奏）
            continue
        day_seen[d] += 1
        idxs2, _i, act = _cow(pkg, rid, s)
        o = act["market"][j]
        old = list(o)
        o[0] = "SELL"
        o[1] = "EGG"
        o[2] = int(daily)
        _commit(pkg, idxs2, s, act, table, rid, "sell_retarget_egg",
                {"slot": j, "day": d, "from": old, "to": list(o)})
        stats["sell_retargeted"] += 1


# ============================================================ 路由手术 ==
def surgery_route(pkg, rid, spec, table):
    """单路由：trunk 波次谱（路由无关=共享段恒等）+ branch 补齐 + 收蛋节奏 + 卖面。"""
    stats = collections.Counter()
    chains = route_chains(pkg, rid)
    trunk = [c for c in chains if c["buy_step"] < TRUNK_STEPS
             and c["pl_step"] < TRUNK_STEPS]
    branch = [c for c in chains if c not in trunk]
    base_arch = collections.Counter(c["species"] for c in chains)
    n = len(chains)
    target = largest_remainder(spec["target"], n)
    t_trunk = trunk_target(spec["target"])
    # trunk 波次（同输入同规则→跨路由共享段逐字等价）
    apply_target(pkg, rid, trunk, t_trunk, table, "trunk", stats)
    # branch 补齐 = 总目标 − trunk 实额（重算链面）
    chains2 = route_chains(pkg, rid)
    trunk2 = [c for c in chains2 if c["buy_step"] < TRUNK_STEPS
              and c["pl_step"] < TRUNK_STEPS]
    branch2 = [c for c in chains2 if c not in trunk2]
    have_t = collections.Counter(c["species"] for c in trunk2)
    tgt_branch = {sp: max(0, int(target.get(sp, 0)) - int(have_t.get(sp, 0)))
                  for sp in ANIMALS}
    apply_target(pkg, rid, branch2, tgt_branch, table, "branch", stats)
    # 收蛋节奏：全部鹅格（含基线既有鹅）；尾段规则覆盖全部落位格
    chains3 = route_chains(pkg, rid)
    goose_tiles = [c["tile"] for c in chains3
                   if c["species"] == "GOOSE" and c.get("tile") is not None]
    all_tiles = [c["tile"] for c in chains3 if c.get("tile") is not None]
    egg_rhythm(pkg, rid, goose_tiles, table, stats, all_tiles=all_tiles)
    # 卖面：按产面（链数）产比
    chains4 = route_chains(pkg, rid)
    tgt_arch = collections.Counter(c["species"] for c in chains4)
    base_prod = {"MILK": float(base_arch.get("COW", 0)),
                 "WOOL": float(base_arch.get("SHEEP", 0))}
    tgt_prod = {"MILK": float(tgt_arch.get("COW", 0)),
                "WOOL": float(tgt_arch.get("SHEEP", 0))}
    sell_face(pkg, rid, goose_tiles,
              base_egg=float(base_arch.get("GOOSE", 0)),
              tgt_egg=float(tgt_arch.get("GOOSE", 0)),
              base_prod=base_prod, tgt_prod=tgt_prod,
              table=table, stats=stats)
    return {"route": rid, "base_arch": dict(base_arch),
            "target": dict(target), "trunk_target": dict(t_trunk),
            "final_arch": dict(tgt_arch), "stats": dict(stats),
            "goose_tiles": [list(t) for t in goose_tiles]}


def surgery_all(pkg, spec, table):
    rows = []
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        rows.append(surgery_route(pkg, rid, spec, table))
    rs._pool_residue_sweep(pkg)
    return rows


# ============================================================ 审计 ==
def audit_variant(pkg_base, pkg_var, table, rows):
    """量守恒+槽守恒+共享段恒等（trunk/tail 跨路由逐字）审计。"""
    out = {"conservation": [], "slot_ok": True, "shared_seg": {}}
    for row in rows:
        rid = row["route"]
        b = route_profile(pkg_base, rid)
        v = route_profile(pkg_var, rid)
        target = row["target"]
        # 量守恒：链 arch==target（注册 rounding）；买单量差登记
        ok = all(int(v["chains"].get(sp, 0)) == int(target.get(sp, 0))
                 for sp in ANIMALS)
        out["conservation"].append({
            "route": rid, "chains_before": b["chains"], "chains_after": v["chains"],
            "target": target, "match": bool(ok),
            "buy_before": b["buy"], "buy_after": v["buy"]})
    # 槽守恒：逐步市场单数（仅同拍拆单允许 +1）
    adds = collections.Counter(r["step"] for r in table
                               if r["kind"] == "buy_split_append")
    for rid in pkg_base["routes"]:
        idxs_b, idxs_v = pkg_base["routes"][rid], pkg_var["routes"][rid]
        for s in range(N_STEPS):
            nb = len(pkg_base["actions"][idxs_b[s]].get("market") or [])
            nv = len(pkg_var["actions"][idxs_v[s]].get("market") or [])
            if nv > nb + int(adds.get(s, 0)) or nv < nb - sum(
                    1 for r in table if r["route"] == rid and r["step"] == s
                    and r["kind"] == "buy_qty_dec"
                    and int(r["to"][2]) == 0):
                out["slot_ok"] = False
                out.setdefault("slot_violations", []).append((rid, s, nb, nv))
    # 共享段恒等：trunk(0..143) 与 tail(648..718) 跨路由值等价（分组=基线共享）
    groups_t = collections.defaultdict(list)
    groups_l = collections.defaultdict(list)
    for rid in pkg_base["routes"]:
        for s in range(0, TRUNK_STEPS):
            groups_t[(s, pkg_base["routes"][rid][s])].append(rid)
        for s in range(TAIL_STEPS, N_STEPS):
            groups_l[(s, pkg_base["routes"][rid][s])].append(rid)
    for name, groups in (("trunk", groups_t), ("tail", groups_l)):
        bad = 0
        for (s, _idx), rids in groups.items():
            vals = {json.dumps(pkg_var["actions"][pkg_var["routes"][r][s]],
                               sort_keys=True, ensure_ascii=False) for r in rids}
            if len(vals) > 1:
                bad += 1
        out["shared_seg"][name] = {"groups": len(groups), "divergent": bad}
    out["n_table_rows"] = len(table)
    return out


# ============================================================ feasibility ==
def _rollout(pkg, rid, seed, srv=None):
    from kaggsim.serve import Serve
    from kaggsim.tape import action_to_line
    own = srv is None
    srv = srv or Serve()
    try:
        idxs = pkg["routes"][rid]
        lines = [action_to_line(pkg["actions"][i]) for i in idxs]
        js = srv.gengame(int(seed), lines, ["PASS"] * len(lines))
        days = js.get("days") or []
        f = js["final"]["farms"][0]
        held = {}
        structures = {"PASTURE": 0, "COOP": 0}
        tiles_with_animal = []
        for y, row in enumerate(f.get("tiles") or []):
            for x, t in enumerate(row):
                if isinstance(t, dict):
                    if t.get("animal"):
                        held[t["animal"]] = held.get(t["animal"], 0) + 1
                        tiles_with_animal.append([x, y, t["animal"]])
                    if t.get("kind") in structures:
                        structures[t["kind"]] += 1
        shed = js["final"]["private"][0].get("shed") or {}
        return {
            "seed": int(seed),
            "money_by_day": [(d.get("money") or [None])[0] for d in days],
            "min_money": min((d.get("money") or [None])[0] or 0 for d in days)
            if days else None,
            "final_money": f.get("money"),
            "held": held, "structures": structures,
            "stranded_animals": sum(int(shed.get(k, 0) or 0) for k in ANIMALS),
            "shed": shed, "tiles_with_animal": tiles_with_animal,
        }
    finally:
        if own:
            srv.close()


def feasibility_twin(pkg_base, pkg_var, rids, srv=None, base_cache=None):
    """三闸（基线相对口径）：现金 min≥0 / 劳动=落位+滞留不劣于基线 / 棚容=动物
    格≤结构格（引擎 1 动物/结构格）。base_cache={rid: rollout} 可跨变体复用。"""
    checks = []
    verdict = "PASS"
    own = srv is None
    srv = srv or Serve()
    base_cache = base_cache if base_cache is not None else {}
    try:
        for rid in rids:
            if rid in base_cache:
                b = base_cache[rid]
            else:
                b = _rollout(pkg_base, rid, 780010, srv=srv)
                base_cache[rid] = b
            v = _rollout(pkg_var, rid, 780010, srv=srv)
            held_total = sum(int(x) for x in v["held"].values())
            base_held = sum(int(x) for x in b["held"].values())
            realized = held_total + int(v["stranded_animals"])
            base_realized = base_held + int(b["stranded_animals"])
            cash_ok = bool(v["min_money"] is not None and v["min_money"] >= 0)
            labor_ok = bool(realized >= base_realized
                            and v["stranded_animals"] <= b["stranded_animals"])
            n_struct = int(v["structures"].get("PASTURE", 0)) + \
                int(v["structures"].get("COOP", 0))
            cap_ok = bool(held_total <= n_struct)
            row = {"route": rid, "seed": 780010,
                   "cash_ok": cash_ok, "min_money_base": b["min_money"],
                   "min_money_var": v["min_money"],
                   "labor_ok": labor_ok,
                   "held_base": b["held"], "held_var": v["held"],
                   "stranded_base": b["stranded_animals"],
                   "stranded_var": v["stranded_animals"],
                   "realized_base": base_realized, "realized_var": realized,
                   "cap_ok": cap_ok, "structures_var": v["structures"],
                   "final_money_base": b["final_money"],
                   "final_money_var": v["final_money"],
                   "tiles_with_animal": v["tiles_with_animal"]}
            row["ok"] = bool(cash_ok and labor_ok and cap_ok)
            if not row["ok"]:
                verdict = "VIOLATION"
            checks.append(row)
    finally:
        if own:
            srv.close()
    return {"verdict": verdict, "checks": checks}


# ============================================================ 构建 ==
def build_variant(vid, pkg_base, main_text):
    spec = VARIANT_SPECS[vid]
    work = copy.deepcopy(pkg_base)
    table = []
    t0 = time.perf_counter()
    rows = surgery_all(work, spec, table)
    aud = audit_variant(pkg_base, work, table, rows)
    new_text = rs._encode_routes(main_text, work)
    return {"variant_id": vid, "spec": spec, "pkg": work, "table": table,
            "rows": rows, "audit": aud, "main_text": new_text,
            "elapsed_s": round(time.perf_counter() - t0, 2)}


def write_package(vid, main_text):
    """变体包：main.py + submission.tar.gz + build_manifest.json（四门喂料）。"""
    d = BUILD_DIR / vid
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
    h1_bytes = H1_MAIN.read_bytes()
    # 恒等口径：blob 区间外与 H1 逐字节一致（写时复制=只动 _R108_DATA blob）
    man = {
        "form": vid, "entry": "_hs_agent",
        "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
        "main_bytes": len(main_bytes),
        "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
        "tar_bytes": len(tar_bytes),
        "base_main_sha256": hashlib.sha256(h1_bytes).hexdigest(),
        "copy_on_write": "仅 _R108_DATA blob 内替换（_encode_routes 四重自检）",
    }
    (d / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return d, man


def main_build_all():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    main_text = H1_MAIN.read_text(encoding="utf-8")
    pkg_base = rs._decode_routes(main_text)
    out = {"version": RECORD_VERSION,
           "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main_sha256": hashlib.sha256(
               main_text.encode("utf-8")).hexdigest(),
           "variants": {}}
    t0 = time.perf_counter()
    base_cache = {}          # rid -> 基线 rollout（跨变体复用）
    base_anchor2 = {}        # rid -> 基线 seed780030 rollout
    from kaggsim.serve import Serve
    srv = Serve()
    rids = sorted(pkg_base["routes"], key=lambda k: int(k))
    try:
        for rid in rids:
            base_cache[rid] = _rollout(pkg_base, rid, 780010, srv=srv)
        for rid in ("0", "101", "109"):
            base_anchor2[rid] = _rollout(pkg_base, rid, 780030, srv=srv)
        for vid in VARIANT_SPECS:
            t1 = time.perf_counter()
            b = build_variant(vid, pkg_base, main_text)
            pkg_dir, man = write_package(vid, b["main_text"])
            twin = feasibility_twin(pkg_base, b["pkg"], rids, srv=srv,
                                    base_cache=base_cache)
            extra = []
            for rid in ("0", "101", "109"):
                rb = base_anchor2[rid]
                rv = _rollout(b["pkg"], rid, 780030, srv=srv)
                extra.append({"route": rid, "seed": 780030,
                              "min_money_base": rb["min_money"],
                              "min_money_var": rv["min_money"],
                              "final_money_base": rb["final_money"],
                              "final_money_var": rv["final_money"],
                              "stranded_base": rb["stranded_animals"],
                              "stranded_var": rv["stranded_animals"]})
            twin["anchor_seed2"] = extra
            n_bad = sum(1 for c in twin["checks"] if not c["ok"])
            out["variants"][vid] = {
                "spec": b["spec"], "stats_rows": b["rows"],
                "audit": b["audit"], "feasibility": twin,
                "n_table_rows": len(b["table"]),
                "table_head": b["table"][:40],
                "table_full_path": str(EVID_DIR / ("change_table_%s.json" % vid)),
                "pkg_dir": str(pkg_dir), "manifest": man,
                "kept": twin["verdict"] == "PASS" and n_bad == 0,
                "n_bad_routes": n_bad,
                "elapsed_s": round(time.perf_counter() - t1, 1)}
            (EVID_DIR / ("change_table_%s.json" % vid)).write_text(
                json.dumps(b["table"], ensure_ascii=False, indent=1) + "\n",
                encoding="utf-8")
            print(vid, "twin:", twin["verdict"], "bad_routes:", n_bad,
                  "kept:", out["variants"][vid]["kept"],
                  out["variants"][vid]["elapsed_s"], "s", flush=True)
    finally:
        srv.close()
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    (EVID_DIR / "goose_build.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build-all", action="store_true")
    args = ap.parse_args()
    if args.build_all:
        main_build_all()
    else:
        ap.print_help()
