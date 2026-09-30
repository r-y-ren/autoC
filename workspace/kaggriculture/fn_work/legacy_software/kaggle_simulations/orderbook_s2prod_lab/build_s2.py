# -*- coding: utf-8 -*-
"""build_s2（s2prod lab）：S2 整套产线全形重生成（不改既有代码/不提交/不发射）。

产线全形（D5 蓝图参数 + D1 经济解 + D6 刚弹面情报）：
1. 畜群：COW d0-1 抢建 + SHEEP 两波（d3-6/d9-15）+ GOOSE 波次 d6-9 主波/
   d8-9 次波/d10-11 收尾（D5 buy_goose_first_day 形制）入 COOP（象限 0-1）
   ——26 头级全计划供养。goose_add 四教训全上：加法不换种（COW/SHEEP 链零
   触碰）、劳动链合成（合成手放养/巡游）、蛋出路水力学（日产日卖清棚、lot 3=
   D6 刚性 2-4）、日补麦防断粮（晚间补麦，供次日 FEED）。
   畜群构成 ±1 档逐路由自适应（顶强逐局摆动形制）。
2. 麦重配方：WHEAT ~169 / CARROT ~31.5 植种事件（base 163/31 已在带）。COOP
   落位格作物面重生成（D6 弹性面：CARROT/STRAWBERRY 带内摆动；WHEAT 地毯
   133-205 刚性——选择器 WHEAT 罚分保护）。
3. 肥配比：fert60 形态已在基底 c_final（自用 0.428≈43%/卖 57%）——并入不动。
4. 节奏：d6 首剪/d8 奶起（基底已具）+ d12-14 蛋起（新 GOOSE placed+4）/d29
   清仓（基底）；奶毛蛋平台 3-4 日一波 20-45u 核验登记。
5. 外壳断言协同（_GP_PLAN 计划表字面量重算；断言块零触碰）+ 三闸（现金/劳动/
   棚容，回滚≤3）+ 守恒 + 逐事件审计（change_table）。

现金安全（D1 死因复盘：加法系现金曲线死）：我方买单仅花「安全余量」——
日初现金 − 隔夜储备（base 次日无背书晨购 ≈1500）；同拍追加（列表尾）= 后结算
不阻基单；晚间补麦；放养溢出次日续（棚内过夜安全）。

手术面：GOOSE 加法（市场单/hands 表仅追加）+ Q0-1 落位格 d5 起 PLANT 清场
（HARVEST 保留；逐事件登记）。fert 层/M13 层/既有卖单零触碰（仅追加 SELL EGG
lot 3）。基底买畜时序 d0 抢建+d8-9 两波 ≈ D5 形制（±1 档自由度覆盖），沿用。

CLI：python build_s2.py [--routes 0,1] [--n-add 8]。只写 orderbook_s2prod_lab/。
"""
from __future__ import annotations

import argparse
import collections
import copy
import hashlib
import io
import json
import os
import re
import sys
import tarfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
for p in (KSIM_DIR, KSIM_DIR / "orderbook_goose_lab",
          KSIM_DIR / "orderbook_goose_fullplan_lab",
          KSIM_DIR / "orderbook_goose_add_lab"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
_KAGGSIM = KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src" / "src-python"
if str(_KAGGSIM) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM))

from orderbook_r37 import retape_sheep as rs  # noqa: E402
import goose_line as gl  # noqa: E402
import goose_fullplan as gf  # noqa: E402
import goose_additive as ga  # noqa: E402

BASE_MAIN = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
BUILD_DIR = HERE / "build"
EVID_DIR = HERE / "evidence"
RECORD_VERSION = "s2-production/1.0"

TRUNK = 144
TAIL = 648
N_STEPS = 719
MAX_ROLLBACK = 3
WAVE_DAYS = (6, 8, 9, 10, 11)   # D5：d6 主波 / d8-9 次波 / d10-11 收尾
# （任务口径 GOOSE d6-9 + D5 d10-11 收尾；现金门自然落波）
EGG_FLOW_OFFSET = 4             # GOOSE first_yield_day=4 → 蛋流 placed+4
EGG_SELL_LOT = 3                # D6 刚性 lot 2-4
EGG_SELL_SLOTS_PER_DAY = 2
MORNING_RESERVE = 200           # 上午预算余量（价差容错）
CONVERT_FROM_DAY = 5            # 落位格作物清场起点
BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250}
AN_PX = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
WHEAT_EVENT_PENALTY = 25        # 选择器：WHEAT 地毯刚性保护


# ============================================================ 作物清场 ==
_POS = {}


def _load_pos(pkg, rids):
    for rid in rids:
        tr = gl.Track(pkg, rid)
        for (s, u), p in tr.pos_at.items():
            _POS[(rid, s, u)] = p


def pick_coop_tiles(pkg, rid, n):
    """Q0-1（y<5）非结构格按损失评分取 n 格：损失=未来植种价值+WHEAT 罚分
    +d6 站桩作物。WHEAT 地毯刚性由罚分保护（D6：133-205 带）。"""
    tr = gl.Track(pkg, rid)
    struct = {tuple(t) for t in tr.placements()}
    for tile, bs in tr.builds().items():
        if bs:
            struct.add(tuple(tile))
    struct |= set(ga.SHED_TILES)
    score = collections.Counter()
    detail = {}
    for s, u, op, p, args in tr.events:
        t = tuple(p)
        if t[1] >= 5 or t in struct or op != "PLANT":
            continue
        crop = args[0] if args else "WHEAT"
        d = s // 24
        val = BASE_PX.get(crop, 50) * 4
        if d >= CONVERT_FROM_DAY:
            score[t] += val + (WHEAT_EVENT_PENALTY if crop == "WHEAT" else 0)
        else:
            score[t] += val // 2
        detail.setdefault(t, {"crops": collections.Counter(), "first": 99})
        detail[t]["crops"][crop] += 1
        detail[t]["first"] = min(detail[t]["first"], d)
    def shed_d(t):
        return min(abs(t[0] - s[0]) + abs(t[1] - s[1]) for s in ga.SHED_TILES)
    ranked = sorted(score, key=lambda t: (score[t], shed_d(t),
                                          detail[t]["first"], t))
    picked = ranked[:n]
    if len(picked) < n:
        allq = [(x, y) for y in range(5) for x in range(10)]
        allq = [t for t in allq if t not in struct and t not in picked]
        allq.sort(key=lambda t: (score.get(t, 0), t))
        picked += allq[:n - len(picked)]
    rep = {}
    for t in picked:
        dd = detail.get(t, {"crops": {}, "first": None})
        rep["%d,%d" % t] = {"score": score.get(t, 0), "first": dd["first"],
                            "crops": dict(dd["crops"])}
    return picked, rep


def clear_tile_plants(pkg, rid, tiles, table):
    """落位格 d5 起 PLANT → PASS（HARVEST 保留=存量收割不丢；逐事件登记）。"""
    want = {tuple(t) for t in tiles}
    cleared = collections.Counter()
    for s in range(CONVERT_FROM_DAY * 24, N_STEPS):
        idxs, _i, act = gl._cow(pkg, rid, s)
        touched = False
        for u, op in gl.units_of(act):
            if not (isinstance(op, list) and len(op) > 1 and op[0] == "PLANT"):
                continue
            tr_pos = _POS.get((rid, s, u))
            if tr_pos is not None and tuple(tr_pos) in want:
                old = list(op)
                rs._set_unit(act, u, ["PASS"])
                table.append({"route": rid, "step": s, "kind": "plant_clear",
                              "unit": u, "tile": list(tr_pos), "from": old,
                              "to": ["PASS"]})
                cleared[old[1] if len(old) > 1 else "?"] += 1
                touched = True
        if touched:
            gl._commit(pkg, idxs, s, act, table, rid, "plant_clear_flush", {})
    return dict(cleared)


# ============================================================ 加法手术 ==
def _route_plan(pkg_base, rid, n_add, coop_tiles):
    waves = []
    left = n_add
    ti = 0
    wave_tiles = []
    sizes = [3, 3, 2, 2, 2]
    for d, sz in zip(WAVE_DAYS, sizes):
        if left <= 0:
            break
        take = min(sz, left)
        waves.append([d, take])
        wave_tiles.append([list(t) for t in coop_tiles[ti:ti + take]])
        ti += take
        left -= take
    return {"route": rid, "n_add": n_add, "waves": waves,
            "wave_tiles": wave_tiles,
            "tiles": [list(t) for t in coop_tiles[:n_add]],
            "hire_gaps": [], "buy_dropped": [], "trip_overflow": [],
            "care_trim": [], "sell_gap_days": [], "spawn_fallback": (5, 5)}


def base_post_need(pkg_base, rid, safe):
    """base 在我方插入步之后的 BUY 成本合计（预算让渡，防基单静默拒单）。"""
    idxs = pkg_base["routes"][rid]
    out = {}
    for d in range(30):
        c = 0
        for s in range(safe.get(d, d * 24), min(d * 24 + 24, N_STEPS)):
            for o in (pkg_base["actions"][idxs[s]].get("market") or []):
                if not isinstance(o, list) or not o:
                    continue
                if o[0] == "BUY_ANIMAL":
                    c += AN_PX.get(o[1], 400) * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_PRODUCT":
                    c += BASE_PX.get(o[1], 30) * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_SEED":
                    c += {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                          "STRAWBERRY": 80, "MELON": 100}.get(o[1], 20) \
                        * (int(o[2]) if len(o) > 2 else 1)
        out[d] = c
    return out


def my_safe_step(pkg_base, rid):
    """我方插入窗 = base 当日最后一个『大额』BUY（≥300）之后的首步（同拍列表尾
    = 后结算）。避开基单大额结算点，杜绝基单静默拒单（D1 现金死因）。"""
    idxs = pkg_base["routes"][rid]
    out = {}
    for d in range(30):
        last = None
        for s in range(d * 24, min(d * 24 + 24, N_STEPS)):
            for o in (pkg_base["actions"][idxs[s]].get("market") or []):
                if not isinstance(o, list) or not o:
                    continue
                if o[0] == "BUY_ANIMAL":
                    c = AN_PX.get(o[1], 400) * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_LAND":
                    c = 2000
                elif o[0] == "BUY_PRODUCT":
                    c = BASE_PX.get(o[1], 30) * (int(o[2]) if len(o) > 2 else 1)
                else:
                    c = 0
                if o[0] == "HIRE":
                    last = max(last or 0, s)
                elif c >= 300:
                    last = s
        out[d] = (last + 1) if last is not None else d * 24
    return out


def morning_hire_step(pkg_base, rid, day):
    """当日基线 HIRE 最后一步 +1（我方 HIRE 其后=手位零劫持）。"""
    idxs = pkg_base["routes"][rid]
    last = day * 24
    for s in range(day * 24, min(day * 24 + 24, N_STEPS)):
        for o in (pkg_base["actions"][idxs[s]].get("market") or []):
            if isinstance(o, list) and o and o[0] == "HIRE":
                last = s
    return min(last + 1, min(day * 24 + 24, N_STEPS) - 1)


def late_step(pkg_base, rid, day):
    """我方晚间买步 = max(基线当日最后订单步+1, 日末-2)。"""
    idxs = pkg_base["routes"][rid]
    last = day * 24
    for s in range(day * 24, min(day * 24 + 24, N_STEPS)):
        if (pkg_base["actions"][idxs[s]].get("market") or []):
            last = s
    return min(max(last + 1, day * 24 + 21), min(day * 24 + 24, N_STEPS) - 1)


def apply_route_s2(pkg_base, work, rid, plan, table, need, safe):
    """加法扩栏：**晚间买（基线订单后）→ 晨间放养（基线 HIRE 后）**两段式。

    现金安全（D1 现金死因）：晚间买预算=end 日现金−累计−次日无背书需求−余量；
    晨间 HIRE 预算=同式（早窗让渡 need+post_need）→ 基单零静默拒单。
    手位安全（错位死因）：HIRE 恒在基线当日全部 HIRE 之后=手位下标零劫持。
    麦等价（断粮死因）：买麦=次日我手取麦量（FEED 1/格+备用），零净抽取；
    巡游只覆盖**已放养**格（幽灵巡游=偷麦死因复盘）。"""
    ed = ga.RouteEditor(work, rid, table, base_pkg=pkg_base)
    waves = {}
    for w_i, (d, n) in enumerate(plan["waves"]):
        waves.setdefault(int(d), [0, []])
        waves[int(d)][0] += int(n)
        waves[int(d)][1] += [tuple(t) for t in plan["wave_tiles"][w_i]]
    tiles = [tuple(t) for t in plan["tiles"]]
    placed = {}
    pending = []
    spent_log = []
    RESERVE = 120
    cum_spent = 0.0
    post_need = base_post_need(pkg_base, rid, safe)
    if not waves:
        ed.flush_all()
        plan["placed"] = {}
        return ed.stats
    first_day = min(waves)
    idxs = work["routes"][rid]
    mb = plan["mb"]

    def shed_dist(t):
        return min(abs(t[0] - s[0]) + abs(t[1] - s[1]) for s in ga.SHED_TILES)

    def end_budget(d):
        """晚间可花=end 日现金 − 累计 − 次日晨购让渡 − 余量。"""
        end_cash = mb[d] if 0 <= d < len(mb) else 0.0
        nxt = need.get(d + 1, 0) + post_need.get(d + 1, 0)
        return max(0.0, end_cash - cum_spent - nxt - RESERVE)

    # ---- 晚间买段：放置日 d 的鹅/麦在 d-1 日末结算（不阻基单）----
    for day in range(first_day - 1, 29):
        wave = waves.get(day + 1)
        n_wave = wave[0] if wave else 0
        wave_tiles = list(wave[1]) if wave else []
        if n_wave <= 0:
            continue
        est_care = min(8, len([t for t in tiles if t in placed]) + 2)
        wheat_qty = min(2 * n_wave + est_care + 2, 26)
        budget = end_budget(day)
        afford = min(n_wave, max(0, int(budget) - wheat_qty * 26) // 300)
        if afford < n_wave:
            plan.setdefault("wave_trim", []).append(
                {"day": day + 1, "want": n_wave, "afford": afford,
                 "budget": budget})
            wave_tiles = wave_tiles[:afford]
            n_wave = afford
        if n_wave <= 0:
            plan.setdefault("bought", []).append({"day": day + 1, "n": 0})
            continue
        evening = [["BUY_ANIMAL", "GOOSE", n_wave],
                   ["BUY_PRODUCT", "WHEAT", wheat_qty]]
        est = n_wave * 300 + wheat_qty * 26
        if est > budget:
            plan.setdefault("buy_skipped", []).append(
                {"day": day, "est": est, "budget": budget})
            continue
        step0 = late_step(pkg_base, rid, day)
        ok = False
        for s in range(step0, min(day * 24 + 24, N_STEPS)):
            if ed.slots_free(s, len(evening)):
                ed.add_market(s, evening)
                ok = True
                break
        if not ok:
            plan.setdefault("buy_dropped", []).append(
                {"day": day, "evening": evening})
            continue
        cum_spent += est
        spent_log.append({"day": day, "phase": "evening_buy", "spent": est,
                          "budget": budget, "step": step0})
        pending.extend(wave_tiles[:n_wave])
        plan.setdefault("bought", []).append(
            {"day": day + 1, "n": n_wave, "buy_day": day,
             "tiles": [list(t) for t in wave_tiles[:n_wave]]})

    # ---- 晨间段：HIRE（基线 HIRE 后）→ 放养/巡游/蛋卖 ----
    for day in range(first_day, 30):
        day_end = min(day * 24 + 24, N_STEPS)
        trip_tiles = [t for t in pending if t not in placed]
        care_tiles = sorted([t for t in tiles if t in placed],
                            key=lambda t: shed_dist(t))
        n_care = min(3, max(1, (len(care_tiles) + 3) // 4)) if care_tiles else 0
        n_trip = len(trip_tiles) if trip_tiles else 0
        n_hands = n_trip + n_care
        if not n_hands:
            continue
        hire_cost = sum(1 << min(i, 9) for i in range(min(n_hands, 10)))
        m_budget = max(0.0, (mb[day - 1] if 1 <= day < len(mb) else 3000.0)
                       - cum_spent - need.get(day, 0) - post_need.get(day, 0)
                       - RESERVE)
        if hire_cost > m_budget:
            plan.setdefault("hire_skipped", []).append(
                {"day": day, "cost": hire_cost, "budget": m_budget})
            continue
        step_m = morning_hire_step(pkg_base, rid, day)
        morning = [["HIRE"]] * n_hands
        hs = None
        for s in range(step_m, day_end):
            if ed.slots_free(s, len(morning)):
                ed.add_market(s, morning)
                hs = [s]
                break
        if hs is None:
            plan["hire_gaps"].append(day)
            continue
        cum_spent += hire_cost
        spent_log.append({"day": day, "phase": "morning_hire",
                          "spent": hire_cost, "budget": m_budget,
                          "step": hs[0]})
        first = len(ed.base_hires(day))
        spawns = ga.discover_spawns(ed, work, rid, day, hs[0], first, n_hands,
                                    plan["spawn_fallback"])
        if trip_tiles and n_trip:
            for g, tile in enumerate(trip_tiles[:n_trip]):
                hand = first + g
                hstep = hs[0] + 1
                cur = spawns[hand]
                ops = [["PICKUP", "WHEAT", 2], ["PICKUP", "GOOSE"]] \
                    + [[m] for m in ga._walk_path(cur, tile)] \
                    + [["DIG"], ["BUILD_COOP"], ["PLACE", "GOOSE"],
                       ["FEED"], ["CARE"]]
                ok2 = True
                for op in ops:
                    if hstep >= day_end:
                        plan["trip_overflow"].append(
                            {"day": day, "hand": hand, "tile": list(tile)})
                        ok2 = False
                        break
                    ed.set_op(hstep, hand, op)
                    hstep += 1
                if ok2:
                    placed[tile] = day
            pending = [t for t in trip_tiles if t not in placed]
        if care_tiles:
            per = max(1, (len(care_tiles) + n_care - 1) // n_care)
            halves = [care_tiles[i * per:(i + 1) * per]
                      for i in range(n_care)]
            for h_i, ts in enumerate(halves[:n_care]):
                if not ts:
                    continue
                hand = first + n_trip + h_i
                hstep = hs[0] + 1
                cur = spawns[hand]
                n_feed = sum(1 for _ in ts)
                ops = [["PICKUP", "WHEAT", min(9, n_feed + 1)]]
                for tile in ts:
                    ops += [[m] for m in ga._walk_path(cur, tile)]
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
        # ---- 蛋出路水力学：日产日卖清棚 lot3（D6 刚性）----
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
                    ed.add_market(s, [["SELL", "EGG", EGG_SELL_LOT]])
                    n_placed_orders += 1
            if n_placed_orders < EGG_SELL_SLOTS_PER_DAY:
                plan["sell_gap_days"].append(day)
    ed.flush_all()
    plan["placed"] = {("%d,%d" % k): v for k, v in placed.items()}
    plan["spent_log"] = spent_log
    plan["spent"] = sum(x["spent"] for x in spent_log)
    return ed.stats


# ============================================================ 审计面 ==
def sell_face_audit(pkg_base, pkg_var):
    """卖面：既有 SELL 单逐拍逐槽逐字不变；仅允许追加 SELL EGG（lot≤4）。"""
    ok = True
    appended = collections.Counter()
    violations = []
    cap_ok = prefix_ok = True
    for rid in pkg_base["routes"]:
        ib, iw = pkg_base["routes"][rid], pkg_var["routes"][rid]
        for s in range(N_STEPS):
            mb = pkg_base["actions"][ib[s]].get("market") or []
            mw = pkg_var["actions"][iw[s]].get("market") or []
            bs = [o for o in mb if isinstance(o, list) and o and o[0] == "SELL"]
            vs = [o for o in mw if isinstance(o, list) and o and o[0] == "SELL"]
            if vs[:len(bs)] != bs:
                ok = False
                violations.append((rid, s, "sell_rewritten"))
            for o in vs[len(bs):]:
                if not (len(o) >= 3 and o[1] == "EGG" and int(o[2]) <= 4):
                    ok = False
                    violations.append((rid, s, "sell_appended:%s" % (o,)))
            for o in mw[len(mb):]:
                key = "%s:%s" % (o[0], o[1] if len(o) > 1 else "")
                appended[key] += 1
            if len(mw) > 10:
                cap_ok = False
            if len(mw) < len(mb):
                prefix_ok = False
    return {"sell_orders_invariant": ok, "n_sell_violations": len(violations),
            "violations_sample": violations[:5],
            "appended_orders": dict(appended),
            "additive_slot_caliber": {"orders_append_only": bool(prefix_ok),
                                      "market_cap_10": bool(cap_ok)},
            "sell_appended_only_egg_lot_le_4": bool(ok)}


def mw_release_rhythm(pkg, rid):
    """奶毛蛋平台投放核验（3-4 日一波 20-45u 对照）。"""
    idxs = pkg["routes"][rid]
    by_day = collections.Counter()
    lots = []
    for s in range(N_STEPS):
        for o in (pkg["actions"][idxs[s]].get("market") or []):
            if isinstance(o, list) and len(o) >= 3 and o[0] == "SELL" \
                    and o[1] in ("MILK", "WOOL", "EGG"):
                by_day[s // 24] += int(o[2])
                lots.append(int(o[2]))
    days = sorted(by_day)
    waves3 = {str(d): sum(by_day[x] for x in days[i:i + 4])
              for i, d in enumerate(days)}
    in_band = sum(1 for v in waves3.values() if 20 <= v <= 45) \
        / max(1, len(waves3))
    return {"qty_by_day": {str(d): by_day[d] for d in days},
            "lot_med": sorted(lots)[len(lots) // 2] if lots else None,
            "wave4_share_20_45u": round(in_band, 3),
            "wave_note": "3-4 日滚动窗合计对照 20-45u 带（不囤不脉冲）"}


def base_pre_sell_need(pkg_base, rid):
    """base 逐日『无背书需求』=首个 SELL 之前的 BUY/HIRE 累计成本（同拍按列表序）。
    我方上午支出必须让出该额度，否则基单静默拒单→基畜缺位/错位。"""
    idxs = pkg_base["routes"][rid]
    need = {}
    for d in range(30):
        cost = 0
        done = False
        for s in range(d * 24, min(d * 24 + 24, N_STEPS)):
            if done:
                break
            for o in (pkg_base["actions"][idxs[s]].get("market") or []):
                if not isinstance(o, list) or not o:
                    continue
                if o[0] == "SELL":
                    done = True
                    break
                c = 0
                if o[0] == "BUY_ANIMAL":
                    c = AN_PX.get(o[1], 400) * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_PRODUCT":
                    c = BASE_PX.get(o[1], 30) * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_SEED":
                    c = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
                         "STRAWBERRY": 80, "MELON": 100}.get(o[1], 20) \
                        * (int(o[2]) if len(o) > 2 else 1)
                elif o[0] == "BUY_LAND":
                    c = 2000
                elif o[0] == "HIRE":
                    c = 60
                cost += c
        need[d] = cost
    return need


# ============================================================ 三闸 ==
def build_one(work, table, stats, rid, n_add, pkg_base, base_roll, srv):
    """单路由手术（就地写 work；回滚≤3 减档；隔离 sub 成功才并表）。"""
    t0 = time.perf_counter()
    route_rows = []
    rollback_rows = []
    need = base_pre_sell_need(pkg_base, rid)
    n_rb = 0
    while True:
        work["routes"][rid] = list(pkg_base["routes"][rid])
        sub = []
        st = collections.Counter()
        n_eff = max(0, n_add - n_rb)
        coop_tiles, tile_loss = pick_coop_tiles(pkg_base, rid, max(1, n_eff))
        coop_tiles = coop_tiles[:n_eff]
        st.update(collections.Counter(
            clear_tile_plants(work, rid, coop_tiles, sub)))
        plan = _route_plan(pkg_base, rid, n_eff, coop_tiles)
        plan["mb"] = base_roll["money_by_day"]
        safe = my_safe_step(pkg_base, rid)
        st.update(apply_route_s2(pkg_base, work, rid, plan, sub, need, safe))
        st["plant_cleared"] = sum(1 for r in sub
                                  if r.get("kind") == "plant_clear")
        gf.goose_rhythm(work, rid, plan["tiles"], sub, st)
        v = gl._rollout(work, rid, 780010, srv=srv)
        row = gf.gate_route(base_roll, v)
        row.update({"route": rid, "n_rollbacks": n_rb, "n_add": n_eff,
                    "tile_loss": tile_loss, "stats": dict(st),
                    "cash_guard": {"pre_sell_need": need},
                    "spent": plan.get("spent"),
                    "spent_log": plan.get("spent_log"),
                    "plan_issues": {k: plan.get(k) for k in
                                    ("hire_gaps", "buy_dropped",
                                     "trip_overflow", "care_trim",
                                     "sell_gap_days", "wave_trim",
                                     "bought", "placed")}})
        if row["ok"] or n_rb >= MAX_ROLLBACK:
            table.extend(sub)
            stats.update(st)
            route_rows.append(row)
            break
        n_rb += 1
        rollback_rows.append(
            {"route": rid, "iter": n_rb,
             "why": {"cash_ok": row["cash_ok"], "labor_ok": row["labor_ok"],
                     "cap_ok": row["cap_ok"],
                     "min_money": [row["min_money_base"], row["min_money_var"]],
                     "realized": [row["realized_base"], row["realized_var"]]}})
    rows = [{"route": rid,
             "target": dict(collections.Counter(
                 c["species"] for c in gl.route_chains(work, rid)))}]
    audit = gl.audit_variant(pkg_base, work, table, rows)
    audit["sell_face"] = sell_face_audit(pkg_base, work)
    n_collect = n_fert = 0
    tr = gl.Track(work, rid)
    for _t, vs in tr.tile_visits().items():
        n_collect += sum(1 for _s, _u, op in vs if op == "COLLECT_FERTILIZER")
    for _s, _u, op, _p, _a in tr.events:
        if op == "FERTILIZE":
            n_fert += 1
    fert = {"fert_ops": n_fert, "collect_slots": n_collect,
            "achieved_rate": round(n_fert / max(1, n_collect), 3),
            "form": "fert60（基底 c_final 并入；自用~43%/卖~57%）"}
    out = {
        "route": rid, "n_add": n_add,
        "n_add_effective": route_rows[0]["n_add"],
        "route_gates": route_rows[0],
        "rollbacks": rollback_rows,
        "audit": {k: audit[k] for k in ("conservation", "slot_ok", "shared_seg")
                  if k in audit},
        "audit_conservation_match": sum(1 for c in audit.get("conservation", [])
                                        if c.get("match")),
        "sell_face": audit["sell_face"],
        "fert": fert,
        "mw_rhythm": mw_release_rhythm(work, rid),
        "change_rows": len(sub),
        "elapsed_s": round(time.perf_counter() - t0, 1),
    }
    return out


def regen_gp_plan(new_text, pkg):
    """外壳断言协同：基底已 _GP_PLAN 驱动 → 仅重算计划表字面量（断言块零触碰）。"""
    plan = gf.build_plan_table(pkg)
    pat = re.compile(r"^_GP_PLAN = \{.*\}\n", re.M)
    m = pat.search(new_text)
    if not m:
        raise RuntimeError("_GP_PLAN 字面量缺失")
    new_text = new_text[:m.start()] + "_GP_PLAN = %r\n" % (plan,) \
        + new_text[m.end():]
    record = {"regenerated": True,
              "values_source": "重建后 route-0 磁带导出（build_plan_table）",
              "assert_block": "基底已 _GP_PLAN 驱动，零触碰",
              "plan_table": {k: (v if not isinstance(v, dict)
                                 else {str(a): b for a, b in v.items()})
                             for k, v in plan.items()},
              "new_invariants": [
                  "mid(%d..%d) PLACE GOOSE 数 == goose_places=%d"
                  % (TRUNK, TAIL, plan["goose_places"])],
              "semantics": "磁带必须符合计划表才许开局改写"}
    return new_text, record


def main(route_sel=None, n_add=8):
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    t0 = time.perf_counter()
    base_text = BASE_MAIN.read_text(encoding="utf-8")
    pkg_base = rs._decode_routes(base_text)
    rids = sorted(pkg_base["routes"], key=lambda k: int(k))
    if route_sel:
        rids = [r for r in rids if r in set(route_sel)]
    from kaggsim.serve import Serve  # noqa: WPS433
    srv = Serve()
    try:
        base_rolls = {rid: gl._rollout(pkg_base, rid, 780010, srv=srv)
                      for rid in rids}
    finally:
        srv.close()
    _load_pos(pkg_base, rids)
    out = {"version": RECORD_VERSION,
           "written_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "base_main_sha256": hashlib.sha256(
               base_text.encode("utf-8")).hexdigest(),
           "base_main": str(BASE_MAIN),
           "spec": {
               "herd": "GOOSE 加法波次 d6/d8-9/d10-11（现金门）COOP 入 Q0-1"
                       "（不买地）；COW/SHEEP 链零触碰（加法不换种）；±1 档逐"
                       "路由自适应",
               "crop": "WHEAT ~169 / CARROT ~31.5 事件配方；COOP 落位格 d5 起"
                       " PLANT 清场（HARVEST 保留；WHEAT 刚性罚分保护）",
               "fert": "fert60 形态并入（基底已含；自用~43%/卖~57%）",
               "rhythm": "d6 首剪 / d8 奶起 / d12-14 蛋起 / d29 清仓；MWEGG"
                         " 3-4 日一波 20-45u 核验",
               "shell": "_GP_PLAN 重生成 + 三闸 + 守恒 + 逐事件审计",
               "d6_rigid": "lot 2-4（蛋 lot3）/ crew≤12 / 日补麦 / 搁浅金 0",
               "cash_safety": "日支出≤日初现金−隔夜储备1500；同拍尾追加；"
                              "晚间补麦；放养溢出棚内过夜次日续",
           },
           "routes": {}}
    work = copy.deepcopy(pkg_base)
    table = []
    stats = collections.Counter()
    srv = Serve()
    try:
        for rid in rids:
            n_r = n_add + (int(rid) % 3) - 1      # ±1 档自适应自由度
            rec = build_one(work, table, stats, rid, n_r, pkg_base,
                            base_rolls[rid], srv)
            out["routes"][rid] = rec
            g = rec["route_gates"]
            print("route", rid, "n_add", n_r, "->", rec["n_add_effective"],
                  "ok", g.get("ok"), "cash", g.get("cash_ok"),
                  "labor", g.get("labor_ok"), "cap", g.get("cap_ok"),
                  "held", g.get("held_var"), "spent", g.get("spent"),
                  flush=True)
    finally:
        srv.close()
    rs._pool_residue_sweep(work)
    new_text = rs._encode_routes(base_text, work)
    new_text, assert_regen = regen_gp_plan(new_text, work)
    vid = "s2"
    d = BUILD_DIR / vid
    d.mkdir(parents=True, exist_ok=True)
    (d / "main.py").write_text(new_text, encoding="utf-8")
    main_bytes = new_text.encode("utf-8")
    tar_buf = io.BytesIO()
    with tarfile.open(fileobj=tar_buf, mode="w:gz") as tar:
        info = tarfile.TarInfo("main.py")
        info.size = len(main_bytes)
        tar.addfile(info, io.BytesIO(main_bytes))
    tar_bytes = tar_buf.getvalue()
    (d / "submission.tar.gz").write_bytes(tar_bytes)
    probe = gf.assertion_probe(d / "main.py")
    man = {"form": vid, "entry": "_hs_agent",
           "base_main_sha256": out["base_main_sha256"],
           "main_sha256": hashlib.sha256(main_bytes).hexdigest(),
           "main_bytes": len(main_bytes),
           "tar_sha256": hashlib.sha256(tar_bytes).hexdigest(),
           "n_change_rows": len(table),
           "assert_regen": assert_regen,
           "assert_probe": probe}
    (d / "build_manifest.json").write_text(
        json.dumps(man, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    out["manifest"] = man
    out["assert_probe"] = probe
    out["stats_total"] = dict(stats)
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    (EVID_DIR / "build_s2.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    (EVID_DIR / "change_table_s2.json").write_text(
        json.dumps(table[:20000], ensure_ascii=False, default=str) + "\n",
        encoding="utf-8")
    print("probe:", probe, "elapsed:", out["elapsed_s"], flush=True)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--routes", default="")
    ap.add_argument("--n-add", type=int, default=8)
    a = ap.parse_args()
    sel = [r for r in a.routes.split(",") if r] or None
    main(sel, a.n_add)
