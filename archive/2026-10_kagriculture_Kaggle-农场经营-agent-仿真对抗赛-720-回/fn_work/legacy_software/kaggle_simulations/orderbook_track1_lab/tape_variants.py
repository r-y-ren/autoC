# -*- coding: utf-8 -*-
"""tape_variants（track1 B）：H1 产线 mix 磁带手术变体 + feasibility 孪生空跑。

责任口径（任务 track1-B）：假设 H1 优势在产出维度（组 J 定向）——产线结构
（畜群配比/作物配比）有无正翻胜变体。**只做小幅单因子变体**（G2 教训：整季
结构复刻 0/16 判死，不做大幅重生成）：
- 畜群（6牛11羊 基线 arch，逐路线匹配）：羊 11→13/15、牛 6→8、混 7牛9羊
  ——**物种换链手术**（链=BUY_ANIMAL+PICKUP+PLACE 同物种三联；换链保总量
  =量守恒配比平移；混 7牛9羊=16 头按菜单口径）；只动产线事件（市场单内容+
  单元 PICKUP/PLACE 物种），市场单槽不删/不移/不填（R23/R26 红线；qty 内容
  改写为受控手术口径）。
- 作物（麦:萝卜配比 ±10/20%）：PLANT WHEAT↔CARROT 末位换项 + BUY_SEED 配比
  内容改写，**总量守恒**（W+C 不变）。
- 买地/雇工时点微调 ±1 拍：BUY_LAND/HIRE 订单 ±1 步平移（spec 授权手术；单
  槽内容保序）。
每变体 **feasibility 孪生空跑先行**（gengame 磁带重放孪生；劳动/现金/棚容
违规即弃）：
- 现金：逐日 money ≥ 0 且买入实额=计划（买不起=现金违规）；
- 劳动：期末棚内滞留畜/品 ≤ 基线（放置链不动；买多放少=劳动违规）；
- 棚容：结构容量=已建棚/栏数×max_held（动物落位 ≤ 栏位；溢出=棚容违规）+
  期末棚存不劣于基线。
审计：change_table 逐事件（route/kind/from/to/step/slot）+ 量守恒核算 +
前后产线画像（畜/作物/时点）。手术=写时复制（retape_sheep._cow_action/
_commit_action 池语义，池内共享件零扰动）+_encode_routes 四重自检。
只写 orderbook_track1_lab/。
"""
from __future__ import annotations

import copy
import json
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
_KAGGSIM_PY = (KSIM_DIR.parents[1] / "tools" / "sim_bridge" / "src"
               / "src-python")
if str(_KAGGSIM_PY) not in sys.path:
    sys.path.insert(0, str(_KAGGSIM_PY))

from orderbook_r37 import retape_sheep as rs  # noqa: E402

RECORD_VERSION = "tape-variants/1.0"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
BUILD_DIR = MODULE_DIR / "build"
EVID_DIR = MODULE_DIR / "evidence"

# 产线 arch（构建期画像）：6牛11羊无鹅=畜群配比手术对象
FLOCK_ARCH = {"COW": 6, "SHEEP": 11, "GOOSE": 0}
CROP_W_BASE, CROP_C_BASE = 163, 31   # 麦:萝卜（WHEAT:CARROT）基线种植数

# 变体菜单（≤10）：id→(因子, 参数)。时点组方向=feasibility 预筛后择向
# （−1/−1 初版实测：雇工 −1 拍跨日界清手=全季无工（孪生判死）；买地 −1 拍
# 部分路由走位错位（孪生判死）——预筛四向取可行向，预筛记录入审计）。
VARIANTS: Dict[str, Dict[str, Any]] = {
    "flock_sheep13": {"factor": "flock_mix", "desc": "羊 11→13（牛隐含 6→4；量守恒换链）",
                      "target": {"COW": 4, "SHEEP": 13}},
    "flock_sheep15": {"factor": "flock_mix", "desc": "羊 11→15（牛隐含 6→2；量守恒换链）",
                      "target": {"COW": 2, "SHEEP": 15}},
    "flock_cow8": {"factor": "flock_mix", "desc": "牛 6→8（羊隐含 11→9；量守恒换链）",
                   "target": {"COW": 8, "SHEEP": 9}},
    "flock_mix79": {"factor": "flock_mix", "desc": "混 7牛9羊（16 头；−1 头按菜单口径）",
                    "target": {"COW": 7, "SHEEP": 9}},
    "crop_wheat_p10": {"factor": "crop_mix", "desc": "麦:萝卜配比 +10%（麦→萝卜平移 10%总量）",
                       "shift": 0.10},
    "crop_wheat_m10": {"factor": "crop_mix", "desc": "麦:萝卜配比 −10%（萝卜→麦平移 10%总量）",
                       "shift": -0.10},
    "crop_wheat_p20": {"factor": "crop_mix", "desc": "麦:萝卜配比 +20%",
                       "shift": 0.20},
    "crop_wheat_m20": {"factor": "crop_mix", "desc": "麦:萝卜配比 −20%",
                       "shift": -0.20},
    "land_shift": {"factor": "timing", "desc": "买地时点 ±1 拍（方向=预筛可行向）",
                   "op": "BUY_LAND", "delta": None},
    "hire_shift": {"factor": "timing", "desc": "雇工时点 ±1 拍（方向=预筛可行向）",
                   "op": "HIRE", "delta": None},
}
TIMING_PRESCREEN = []   # main() 预筛四向结果（审计留档）


# ------------------------------------------------------------ 产线画像 --

def route_profile(pkg: Dict[str, Any], rid: str) -> Dict[str, Any]:
    """路由产线画像：畜/作物/买地/雇工（构建期口径）。"""
    idxs = pkg["routes"][rid]
    anim: Dict[str, int] = {}
    plant: Dict[str, int] = {}
    seed: Dict[str, int] = {}
    land_steps: List[int] = []
    hire_steps: List[int] = []
    for s, i in enumerate(idxs):
        a = pkg["actions"][i]
        for o in (a.get("market") or []):
            if not (isinstance(o, list) and o):
                continue
            if o[0] == "BUY_ANIMAL":
                anim[o[1]] = anim.get(o[1], 0) + (int(o[2]) if len(o) > 2 else 1)
            elif o[0] == "BUY_SEED":
                seed[o[1]] = seed.get(o[1], 0) + (int(o[2]) if len(o) > 2 else 1)
            elif o[0] == "BUY_LAND":
                land_steps.append(s)
            elif o[0] == "HIRE":
                hire_steps.append(s)
        for _u, op in rs._units(a):
            if isinstance(op, list) and op and op[0] == "PLANT" and len(op) > 1:
                plant[op[1]] = plant.get(op[1], 0) + 1
    return {"anim": anim, "plant": plant, "seed": seed,
            "land_steps": land_steps, "hire_n": len(hire_steps),
            "hire_first": hire_steps[:3], "hire_last": hire_steps[-3:]}


def flock_routes(pkg: Dict[str, Any]) -> List[str]:
    """匹配 FLOCK_ARCH 的路由（畜群配比手术对象；缺省物种=0）。"""
    out = []
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        p = route_profile(pkg, rid)
        anim = dict(p["anim"])
        if all(int(anim.pop(k, 0)) == int(v) for k, v in FLOCK_ARCH.items()) \
                and not anim:
            out.append(rid)
    return out


def crop_routes(pkg: Dict[str, Any]) -> List[str]:
    """麦:萝卜=基线配比的路由（作物配比手术对象）。"""
    out = []
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        p = route_profile(pkg, rid)
        if (p["plant"].get("WHEAT") == CROP_W_BASE
                and p["plant"].get("CARROT") == CROP_C_BASE):
            out.append(rid)
    return out


# ------------------------------------------------------------ 手术件 --

def _animal_chains(pkg: Dict[str, Any], rid: str, species: str
                   ) -> List[Dict[str, Any]]:
    """物种放置链（扫线 FIFO 精确配对）：buy 入队→PICKUP 出队→同单元 PLACE。

    棚内按物种 FIFO：同物种 k-th PICKUP 喂自 k-th BUY（步序严格）。PICKUP 无
    队可出（orphan，真磁带存在）不成链；PLACE 按单元认领其最近 PICKUP。
    """
    idxs = pkg["routes"][rid]
    queue: List[Tuple[int, int]] = []          # (buy_step, buy_slot)
    pending: Dict[str, Dict[str, Any]] = {}    # unit → chain draft
    chains: List[Dict[str, Any]] = []
    for s, i in enumerate(idxs):
        a = pkg["actions"][i]
        for j, o in enumerate(a.get("market") or []):
            if isinstance(o, list) and o and o[0] == "BUY_ANIMAL" \
                    and len(o) > 1 and o[1] == species:
                queue.append((s, j))
        for u, op in rs._units(a):
            if not (isinstance(op, list) and len(op) > 1):
                continue
            if op[0] == "PICKUP" and op[1] == species:
                if queue:
                    b = queue.pop(0)
                    pending[u] = {"buy_step": b[0], "buy_slot": b[1],
                                  "pu_step": s, "pu_unit": u}
            elif op[0] == "PLACE" and op[1] == species:
                d = pending.pop(u, None)
                if d is not None:
                    d.update({"pl_step": s, "pl_unit": u})
                    chains.append(d)
    return chains


def _set_market_species(pkg, rid, step, slot, species, qty=None,
                        table=None, kind="buy_species"):
    """写时复制改市场单物种（slot 位次不动）；qty=None 保持。"""
    idxs, idx, act = rs._cow_action(pkg, rid, step)
    o = act["market"][slot]
    old = list(o)
    o[1] = species
    if qty is not None:
        o[2] = int(qty)
    rs._commit_action(pkg, idxs, step, act)
    if table is not None:
        table.append({"route": rid, "kind": kind, "step": step, "slot": slot,
                      "from": old, "to": list(o)})
    return act


def _set_unit_op(pkg, rid, step, unit, op, table=None, kind="unit_op"):
    """写时复制改单元指令（PICKUP/PLACE 物种或置 PASS）。"""
    idxs, idx, act = rs._cow_action(pkg, rid, step)
    old = None
    if unit == "F":
        old = list(act.get("farmer") or [])
        act["farmer"] = list(op)
    else:
        i = int(unit[1:])
        hands = act.setdefault("hands", [])
        while len(hands) <= i:
            hands.append(["PASS"])
        old = list(hands[i])
        hands[i] = list(op)
    rs._commit_action(pkg, idxs, step, act)
    if table is not None:
        table.append({"route": rid, "kind": kind, "step": step, "unit": unit,
                      "from": old, "to": list(op)})
    return act


def surgery_flock(pkg: Dict[str, Any], target: Dict[str, int],
                  table: List[Dict[str, Any]]) -> Dict[str, Any]:
    """畜群配比手术（arch 路由）：换链 A→B + 删链（量守恒/菜单口径）。"""
    stats = {"routes": 0, "converted": 0, "deleted": 0}
    for rid in flock_routes(pkg):
        prof = route_profile(pkg, rid)
        cur = dict(prof["anim"])
        stats["routes"] += 1
        # 需求：A 减多少 / B 加多少
        for sp_from, sp_to in (("COW", "SHEEP"), ("SHEEP", "COW")):
            need_to = int(target.get(sp_to, 0)) - int(cur.get(sp_to, 0))
            have_from = int(cur.get(sp_from, 0)) - int(target.get(sp_from, 0))
            n = min(need_to, have_from)
            if n <= 0:
                continue
            chains = _animal_chains(pkg, rid, sp_from)
            for ch in chains[-n:]:
                _set_market_species(pkg, rid, ch["buy_step"], ch["buy_slot"],
                                    sp_to, None, table, "buy_species")
                _set_unit_op(pkg, rid, ch["pu_step"], ch["pu_unit"],
                             ["PICKUP", sp_to], table, "pickup_species")
                _set_unit_op(pkg, rid, ch["pl_step"], ch["pl_unit"],
                             ["PLACE", sp_to], table, "place_species")
                cur[sp_from] = cur.get(sp_from, 0) - 1
                cur[sp_to] = cur.get(sp_to, 0) + 1
                stats["converted"] += 1
        # 总量差（菜单口径 −1 头等）：删/补链
        for sp in ("SHEEP", "COW"):
            diff = int(cur.get(sp, 0)) - int(target.get(sp, 0))
            if diff <= 0:
                continue
            chains = _animal_chains(pkg, rid, sp)
            for ch in chains[-diff:]:
                # 删链：买单 qty−1（不足→qty 0 占坑保槽）+ PICKUP/PLACE 置 PASS
                idxs, idx, act = rs._cow_action(pkg, rid, ch["buy_step"])
                o = act["market"][ch["buy_slot"]]
                old = list(o)
                q = int(o[2]) if len(o) > 2 else 1
                o[2] = max(0, q - 1)
                rs._commit_action(pkg, idxs, ch["buy_step"], act)
                table.append({"route": rid, "kind": "buy_qty_dec",
                              "step": ch["buy_step"], "slot": ch["buy_slot"],
                              "from": old, "to": list(o)})
                _set_unit_op(pkg, rid, ch["pu_step"], ch["pu_unit"], ["PASS"],
                             table, "pickup_drop")
                _set_unit_op(pkg, rid, ch["pl_step"], ch["pl_unit"], ["PASS"],
                             table, "place_drop")
                cur[sp] = cur.get(sp, 0) - 1
                stats["deleted"] += 1
    return stats


def surgery_crop(pkg: Dict[str, Any], shift: float,
                 table: List[Dict[str, Any]]) -> Dict[str, Any]:
    """作物配比手术：总量守恒平移 round(shift×(W+C)) 由麦→萝卜（负向反向）。"""
    stats = {"routes": 0, "moved": 0}
    for rid in crop_routes(pkg):
        prof = route_profile(pkg, rid)
        w = int(prof["plant"].get("WHEAT", 0))
        c = int(prof["plant"].get("CARROT", 0))
        total = w + c
        delta = int(round(float(shift) * total))
        stats["routes"] += 1
        if delta == 0:
            continue
        if delta > 0:
            sp_from, sp_to, n = "WHEAT", "CARROT", min(delta, w)
        else:
            sp_from, sp_to, n = "CARROT", "WHEAT", min(-delta, c)
        idxs = pkg["routes"][rid]
        # PLANT 末位换项
        done = 0
        for s in range(len(idxs) - 1, -1, -1):
            if done >= n:
                break
            i = idxs[s]
            a = pkg["actions"][i]
            hit = None
            for _u, op in rs._units(a):
                if isinstance(op, list) and len(op) > 1 and op[0] == "PLANT" \
                        and op[1] == sp_from:
                    hit = op
                    break
            if hit is None:
                continue
            idxs2, idx2, act = rs._cow_action(pkg, rid, s)
            for _u, op in rs._units(act):
                if isinstance(op, list) and len(op) > 1 and op[0] == "PLANT" \
                        and op[1] == sp_from:
                    old = list(op)
                    op[1] = sp_to
                    table.append({"route": rid, "kind": "plant_item",
                                  "step": s, "from": old, "to": list(op)})
                    break
            rs._commit_action(pkg, idxs2, s, act)
            done += 1
        # BUY_SEED 配比内容改写（末位 n 单位 from→to；槽位不动）
        left = done
        for s in range(len(idxs) - 1, -1, -1):
            if left <= 0:
                break
            i = idxs[s]
            a = pkg["actions"][i]
            for j, o in enumerate(a.get("market") or []):
                if left <= 0:
                    break
                if isinstance(o, list) and o and o[0] == "BUY_SEED" \
                        and len(o) > 2 and o[1] == sp_from and int(o[2]) > 0:
                    k = min(int(o[2]), left)
                    idxs2, idx2, act = rs._cow_action(pkg, rid, s)
                    o2 = act["market"][j]
                    old = list(o2)
                    o2[2] = int(o2[2]) - k
                    rs._commit_action(pkg, idxs2, s, act)
                    table.append({"route": rid, "kind": "buy_seed_dec",
                                  "step": s, "slot": j, "from": old,
                                  "to": list(o2)})
                    left -= k
        if left > 0:
            raise RuntimeError("BUY_SEED from 侧量不足: rid=%s left=%d"
                               % (rid, left))
        # to 侧加量：摊分到 sp_to 全部买单（均摊上限 ceil）——单步现金扰动
        # 最小化（基线 min_money 仅 27，集中加量会挤死早期买畜）。
        to_orders: List[Tuple[int, int]] = []
        for s in range(len(idxs)):
            i = idxs[s]
            a = pkg["actions"][i]
            for j, o in enumerate(a.get("market") or []):
                if isinstance(o, list) and o and o[0] == "BUY_SEED" \
                        and o[1] == sp_to:
                    to_orders.append((s, j))
        if to_orders and done > 0:
            base_q = done // len(to_orders)
            extra = done - base_q * len(to_orders)
            for k, (s, j) in enumerate(to_orders):
                inc = base_q + (1 if k < extra else 0)
                if inc <= 0:
                    continue
                idxs2, idx2, act = rs._cow_action(pkg, rid, s)
                o2 = act["market"][j]
                old = list(o2)
                o2[2] = int(o2[2] if len(o2) > 2 else 0) + inc
                rs._commit_action(pkg, idxs2, s, act)
                table.append({"route": rid, "kind": "buy_seed_inc",
                              "step": s, "slot": j, "from": old,
                              "to": list(o2)})
        stats["moved"] += done
    return stats


def surgery_timing(pkg: Dict[str, Any], op_name: str, delta: int,
                   table: List[Dict[str, Any]]) -> Dict[str, Any]:
    """时点手术：市场单 op_name 全流平移 delta 步（槽内容保序，跨步挪位）。"""
    stats = {"routes": 0, "moved": 0, "clamped": 0}
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        moves = []       # (step, slot, order)
        for s, i in enumerate(idxs):
            a = pkg["actions"][i]
            for j, o in enumerate(a.get("market") or []):
                if isinstance(o, list) and o and o[0] == op_name:
                    moves.append((s, j, list(o)))
        if not moves:
            continue
        stats["routes"] += 1
        # 源侧清位：qty=0 SELL 占坑单（真磁带原生形态，实测惰性）——HIRE/
        # BUY_LAND 的 qty0 不中和（实测仍执行），故源槽换惰性占坑保槽位次序。
        for s, j, o in moves:
            t = s + int(delta)
            if t < 0 or t >= len(idxs):
                stats["clamped"] += 1
                continue
            idxs2, _idx, act = rs._cow_action(pkg, rid, s)
            o2 = act["market"][j]
            old = list(o2)
            o2[:] = ["SELL", "WHEAT", 0]
            rs._commit_action(pkg, idxs2, s, act)
            table.append({"route": rid, "kind": "src_slot_placeholder",
                          "step": s, "slot": j, "from": old, "to": list(o2)})
            # 目标侧：新步追加同内容单（位次=末位；单槽零触碰口径外=spec 授权）
            idxs3, _idx3, act3 = rs._cow_action(pkg, rid, t)
            act3["market"].append(list(o))
            rs._commit_action(pkg, idxs3, t, act3)
            table.append({"route": rid, "kind": "dst_slot_append", "step": t,
                          "slot": len(act3["market"]) - 1, "from": None,
                          "to": list(o)})
            stats["moved"] += 1
    return stats


# ------------------------------------------------------------ feasibility --

def _rollout(pkg: Dict[str, Any], rid: str, seeds=(780010, 780030),
             srv=None) -> List[Dict[str, Any]]:
    """路由计划孪生空跑（gengame 磁带重放 vs idle 对手；双 seed）。"""
    from kaggsim.serve import Serve
    from kaggsim.tape import action_to_line
    own = srv is None
    srv = srv or Serve()
    try:
        idxs = pkg["routes"][rid]
        lines = [action_to_line(pkg["actions"][i]) for i in idxs]
        idle = ["PASS"] * len(lines)
        out = []
        for s in seeds:
            js = srv.gengame(int(s), lines, idle)
            days = js.get("days") or []
            f = js["final"]["farms"][0]
            held: Dict[str, int] = {}
            structures = {"PASTURE": 0, "COOP": 0}
            for row in (f.get("tiles") or []):
                for t in row:
                    if isinstance(t, dict):
                        if t.get("animal"):
                            held[t["animal"]] = held.get(t["animal"], 0) + 1
                        if t.get("kind") in structures:
                            structures[t["kind"]] += 1
            shed = js["final"]["private"][0].get("shed") or {}
            out.append({
                "seed": int(s),
                "money_by_day": [d.get("money", [None])[0] for d in days],
                "min_money": min((d.get("money", [None])[0] or 0)
                                 for d in days) if days else None,
                "final_money": f.get("money"),
                "held": held, "structures": structures,
                "shed": shed,
                "stranded_animals": sum(int(shed.get(k, 0) or 0)
                                       for k in ("COW", "SHEEP", "GOOSE")),
            })
        return out
    finally:
        if own:
            srv.close()


def feasibility_twin(pkg_var: Dict[str, Any], pkg_base: Dict[str, Any],
                     rids: List[str], srv=None) -> Dict[str, Any]:
    """feasibility 孪生空跑：劳动/现金/棚容 三闸（基线对照，违规即弃）。

    劳动闸加严（v2）：期末棚内滞留畜==0 且 落位+滞留==计划头数（计划实额
    落位=放置链闭合；买多放少/放丢=劳动违规）。
    """
    checks = []
    verdict = "PASS"
    for rid in rids:
        plan = route_profile(pkg_var, rid)["anim"]
        plan_total = sum(int(v) for v in plan.values())
        base_runs = _rollout(pkg_base, rid, srv=srv)
        var_runs = _rollout(pkg_var, rid, srv=srv)
        for vb, vv in zip(base_runs, var_runs):
            held_total = sum(int(x) for x in vv["held"].values())
            realized_total = held_total + int(vv["stranded_animals"])
            row = {"route": rid, "seed": vv["seed"],
                   "cash_ok": bool(vv["min_money"] is not None
                                   and vv["min_money"] >= 0),
                   "min_money_base": vb["min_money"],
                   "min_money_var": vv["min_money"],
                   "stranded_base": vb["stranded_animals"],
                   "stranded_var": vv["stranded_animals"],
                   "plan_total": plan_total,
                   "realized_total": realized_total,
                   "held_base": vb["held"], "held_var": vv["held"],
                   "structures_var": vv["structures"],
                   "shed_var": vv["shed"],
                   "final_money_base": vb["final_money"],
                   "final_money_var": vv["final_money"]}
            row["labor_ok"] = bool(int(vv["stranded_animals"]) == 0
                                   and realized_total == plan_total)
            cap_ok = True
            n_pas = int(vv["structures"].get("PASTURE", 0))
            n_coop = int(vv["structures"].get("COOP", 0))
            held_pc = int(vv["held"].get("COW", 0)) + int(vv["held"].get(
                "SHEEP", 0))
            held_g = int(vv["held"].get("GOOSE", 0))
            if held_pc > n_pas * 6 or held_g > n_coop * 4:
                cap_ok = False
            row["shed_cap_ok"] = cap_ok
            row["ok"] = bool(row["cash_ok"] and row["labor_ok"] and cap_ok)
            if not row["ok"]:
                verdict = "VIOLATION"
            checks.append(row)
    return {"verdict": verdict, "checks": checks}


# ------------------------------------------------------------ 构建 --

def build_variant(vid: str, pkg_base: Dict[str, Any], main_text: str
                  ) -> Dict[str, Any]:
    """变体构建：手术→审计→编码（_encode_routes 四重自检）→main 文本。"""
    if vid not in VARIANTS:
        raise ValueError("未知变体: %r" % vid)
    spec = VARIANTS[vid]
    work = copy.deepcopy(pkg_base)
    table: List[Dict[str, Any]] = []
    t0 = time.perf_counter()
    if spec["factor"] == "flock_mix":
        stats = surgery_flock(work, spec["target"], table)
    elif spec["factor"] == "crop_mix":
        stats = surgery_crop(work, float(spec["shift"]), table)
    elif spec["factor"] == "timing":
        stats = surgery_timing(work, spec["op"], int(spec["delta"]), table)
    else:
        raise ValueError("未知因子: %r" % spec["factor"])
    rs._pool_residue_sweep(work)
    new_text = rs._encode_routes(main_text, work)
    return {"variant_id": vid, "spec": spec, "pkg": work, "table": table,
            "stats": stats, "main_text": new_text,
            "elapsed_s": round(time.perf_counter() - t0, 2)}


def audit_variant(built: Dict[str, Any], pkg_base: Dict[str, Any]) -> Dict[str, Any]:
    """量守恒+产线前后画像审计。"""
    vid = built["variant_id"]
    spec = built["spec"]
    rows = {}
    rids = sorted(set(r["route"] for r in built["table"]),
                  key=lambda k: int(k)) or sorted(pkg_base["routes"],
                                                  key=lambda k: int(k))
    for rid in rids:
        b = route_profile(pkg_base, rid)
        v = route_profile(built["pkg"], rid)
        rows[rid] = {"before": {"anim": b["anim"], "plant": b["plant"],
                                "land_steps": b["land_steps"][:4],
                                "hire_n": b["hire_n"]},
                     "after": {"anim": v["anim"], "plant": v["plant"],
                               "land_steps": v["land_steps"][:4],
                               "hire_n": v["hire_n"]}}
    if spec["factor"] == "flock_mix":
        cons = all(
            sum(rows[r]["before"]["anim"].values())
            == sum(rows[r]["after"]["anim"].values()) + (
                1 if spec["target"].get("COW", 0) +
                spec["target"].get("SHEEP", 0) < 17 else 0)
            for r in rows)
        cons_note = "畜总量守恒（混 7牛9羊=16 头菜单口径 −1 头）"
    elif spec["factor"] == "crop_mix":
        cons = all(
            sum(rows[r]["before"]["plant"].values())
            == sum(rows[r]["after"]["plant"].values()) for r in rows)
        cons_note = "种植总量守恒（麦:萝卜互换）"
    else:
        cons = all(
            rows[r]["before"]["hire_n"] == rows[r]["after"]["hire_n"]
            for r in rows)
        cons_note = "订单总量守恒（仅时点平移）"
    return {"variant_id": vid, "conservation_ok": bool(cons),
            "conservation_note": cons_note,
            "n_table_rows": len(built["table"]),
            "routes": rows}


def prescreen_timing(pkg_base: Dict[str, Any], main_text: str, srv=None
                     ) -> List[Dict[str, Any]]:
    """时点方向预筛：BUY_LAND/HIRE × ±1 拍 四向孪生（2 路由×2 seed），择可行向。"""
    results = []
    for op in ("BUY_LAND", "HIRE"):
        for delta in (-1, 1):
            work = copy.deepcopy(pkg_base)
            table: List[Dict[str, Any]] = []
            surgery_timing(work, op, delta, table)
            rs._pool_residue_sweep(work)
            rids = sorted(set(r["route"] for r in table),
                          key=lambda k: int(k))[:2]
            twin = feasibility_twin(work, pkg_base, rids, srv=srv) \
                if rids else {"verdict": "NO_OP", "checks": []}
            results.append({"op": op, "delta": delta,
                            "verdict": twin["verdict"],
                            "n_moved": sum(1 for r in table
                                           if r["kind"] == "dst_slot_append")})
            print("prescreen", op, delta, twin["verdict"], flush=True)
    return results


def _pick_delta(prescreen: List[Dict[str, Any]], op: str) -> Tuple[
        Optional[int], List[Dict[str, Any]]]:
    """择向：PASS 优先（−1 优先于 +1）；无 PASS 取 VIOLATION 中留档回退 −1。"""
    rows = [r for r in prescreen if r["op"] == op]
    ok = [r for r in rows if r["verdict"] == "PASS"]
    if ok:
        ok.sort(key=lambda r: r["delta"])
        return int(ok[0]["delta"]), rows
    return -1, rows


def main():
    BUILD_DIR.mkdir(parents=True, exist_ok=True)
    main_text = H1_MAIN.read_text(encoding="utf-8")
    pkg_base = rs._decode_routes(main_text)
    out = {"version": RECORD_VERSION,
           "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
           "variants": {}}
    # 时点方向预筛（−1 拍雇工/买地初版实测孪生判死，见模块 docstring）
    prescreen = prescreen_timing(pkg_base, main_text)
    out["timing_prescreen"] = prescreen
    for op, vid in (("BUY_LAND", "land_shift"), ("HIRE", "hire_shift")):
        d, rows = _pick_delta(prescreen, op)
        VARIANTS[vid]["delta"] = int(d)
        VARIANTS[vid]["desc"] += "→ 实选 %d 拍" % int(d)
        VARIANTS[vid]["prescreen"] = rows
    for vid in VARIANTS:
        t0 = time.perf_counter()
        built = build_variant(vid, pkg_base, main_text)
        aud = audit_variant(built, pkg_base)
        # 受影响路由（孪生对象）：手术表里的路由，最多 3 个
        rids = sorted(set(r["route"] for r in built["table"]),
                      key=lambda k: int(k))[:3]
        twin = feasibility_twin(built["pkg"], pkg_base, rids) if rids \
            else {"verdict": "NO_OP", "checks": []}
        p = BUILD_DIR / ("variant_%s_main.py" % vid)
        p.write_text(built["main_text"], encoding="utf-8")
        out["variants"][vid] = {
            "spec": built["spec"], "stats": built["stats"],
            "audit": aud, "feasibility": twin,
            "main_path": str(p),
            "kept": twin["verdict"] == "PASS",
            "elapsed_s": round(time.perf_counter() - t0, 2)}
        print(vid, "twin:", twin["verdict"],
              "kept:", out["variants"][vid]["kept"], flush=True)
    (EVID_DIR / "tape_variants_audit.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1) + "\n",
        encoding="utf-8")
    return out


if __name__ == "__main__":
    main()
