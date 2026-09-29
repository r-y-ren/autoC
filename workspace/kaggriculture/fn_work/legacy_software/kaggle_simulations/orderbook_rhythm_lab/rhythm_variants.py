# -*- coding: utf-8 -*-
"""rhythm_variants（prod-rhythm）：H1 产线相位磁带手术变体（分析38 诊断④）。

责任口径（任务 prod-rhythm）：检验"残差在生产节奏"——生产事件相位平移是否
翻胜。基底=orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…）。
单因子相位变体（≤6）：
- PLANT 事件全流 ±1/±2 拍（4 变体）：收获可用性节奏平移（种植相位整体挪动
  → 成熟/可收时点同步平移）；
- HARVEST 事件日内 %4 相位 ±1 拍（2 变体）：对齐/错开排水拍（%4∈{2,3}），
  **日内约束**（跨日界不动=纯相位处理，不带可用性跨日混杂）。

手术=合同保持的窗内相位转位（写时复制，retape_sheep._cow_action/
_commit_action 池语义）——**逐 (route,unit) op 多重集精确不变（量守恒）**；
空间零扰动（限同格滞留窗：相邻槽连续且窗内无位移指令的极大段；位移指令=不
动锚点）。引擎合同实据（kagg-engine engine.rs）：①作物定植日必浇水（连续
2 日未浇→枯死；WATER 落空=白浇）；②畜连续 2 日未喂→逃逸（FEED 日合同）；
③产线旋转=WATER→HARVEST→PLANT→WATER（种前收、收后种）。故：
- **PLANT 变体=合同对块平移**：PLANT+同日同格次拍 WATER 配对（磁带实测
  9698/9796 配对），对块整体 ±delta 拍，落点/回填槽须为安全单件（非
  PLANT/WATER/HARVEST 旋转件），否则 clamp——种-水-收序不破（收前种=种失败、
  水落空=枯死）。
- **HARVEST 变体=单事件 ±1 拍（日内 %4 相位）**：链式转位，链尾回填件为
  PLANT/WATER 合同件则 clamp（防种-水逆序）。
- 日界跨拍一律禁止（_end_of_day 清手回出生位：跨日=空间破坏；且浇水合同
  日内互锁）→ 本实验的"节奏"=**日内相位**，跨日可用性平移被合同/空间锁死
  （结构性发现，入 anomaly）。
市场单槽零触碰（R23/R26 红线）。审计=逐事件 change_table（route/unit/kind/
from_step/to_step/op）+ 前后产线画像 + %4 相位直方图。
孪生三闸先行（复用 tape_variants.feasibility_twin：现金/劳动/棚容，违规即弃）。
只写 orderbook_rhythm_lab/。
"""
from __future__ import annotations

import copy
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Tuple

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

try:
    from orderbook_track1_lab import tape_variants as tv  # noqa: E402
except ImportError:  # 目录非包（无 __init__）：直插路径导入
    sys.path.insert(0, str(KSIM_DIR / "orderbook_track1_lab"))
    import tape_variants as tv  # noqa: E402
from orderbook_r37 import retape_sheep as rs  # noqa: E402

RECORD_VERSION = "rhythm-variants/1.0"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
BUILD_DIR = MODULE_DIR / "build"

# 变体菜单（单因子）：id→(事件 kind, delta, 日内约束)
VARIANTS: Dict[str, Dict[str, Any]] = {
    "plant_m2": {"kind": "PLANT", "delta": -2, "same_day": False,
                 "desc": "全部 PLANT 事件 −2 拍（收获可用性节奏平移）"},
    "plant_m1": {"kind": "PLANT", "delta": -1, "same_day": False,
                 "desc": "全部 PLANT 事件 −1 拍"},
    "plant_p1": {"kind": "PLANT", "delta": 1, "same_day": False,
                 "desc": "全部 PLANT 事件 +1 拍"},
    "plant_p2": {"kind": "PLANT", "delta": 2, "same_day": False,
                 "desc": "全部 PLANT 事件 +2 拍"},
    "harvest_m1": {"kind": "HARVEST", "delta": -1, "same_day": True,
                   "desc": "HARVEST 事件日内 %4 相位 −1 拍（错开排水拍）"},
    "harvest_p1": {"kind": "HARVEST", "delta": 1, "same_day": True,
                   "desc": "HARVEST 事件日内 %4 相位 +1 拍（对齐排水拍）"},
}
DAY = 24


# ------------------------------------------------------------ 手术件 --

def _unit_slots(pkg: Dict[str, Any], rid: str) -> Dict[str, Dict[int, List]]:
    """路由 → {unit: {step: op}}（真磁带槽表；日界/雇佣空洞=缺槽）。"""
    idxs = pkg["routes"][rid]
    out: Dict[str, Dict[int, List]] = {}
    for s, i in enumerate(idxs):
        for u, op in rs._units(pkg["actions"][i]):
            out.setdefault(u, {})[s] = list(op)
    return out


def _chains(events: List[int], delta: int, slots: set) -> List[List[int]]:
    """事件步 → delta 链（walk 序 c_{i+1}=c_i+delta，限窗内槽；互斥覆盖）。

    链首=e−delta 非事件的事件（顺序无关划分；否则负 delta 会把别链事件槽
    误当尾槽，写位冲突破量守恒）。
    """
    eset = set(events)
    seen = set()
    out: List[List[int]] = []
    for e in events:
        if (e - delta) in eset or e in seen:
            continue
        chain = [e]
        seen.add(e)
        cur = e + delta
        while cur in eset and cur in slots and cur not in seen:
            chain.append(cur)
            seen.add(cur)
            cur += delta
        out.append(chain)
    return out


_MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}


def _dwell_windows(slots: Dict[int, List]) -> List[List[int]]:
    """同格滞留窗：相邻槽连续且窗内无位移指令的极大段（位移=不动锚点）。"""
    out: List[List[int]] = []
    cur: List[int] = []
    for s in sorted(slots):
        if cur and (s != cur[-1] + 1 or slots[cur[-1]][0] in _MOVES):
            out.append(cur)
            cur = []
        cur.append(s)
    if cur:
        out.append(cur)
    return [w for w in out if not (len(w) == 1 and slots[w[0]][0] in _MOVES)]


def surgery_phase(pkg: Dict[str, Any], kind: str, delta: int,
                  same_day: bool, table: List[Dict[str, Any]]
                  ) -> Dict[str, Any]:
    """合同保持的窗内相位转位手术（量守恒；逐事件审计）。

    kind=PLANT：合同对块 [PLANT,同日同格次拍 WATER] 平移 delta 拍（落点/回填
    槽须为安全单件=非 PLANT/WATER/HARVEST 旋转件）；kind=HARVEST：单事件
    链式转位 ±delta 拍（链尾回填件为 PLANT/WATER 合同件则 clamp）。
    """
    stats = {"routes": 0, "events": 0, "moved": 0, "moved_pairs": 0,
             "clamped": 0, "clamped_reasons": Counter(), "day_cross": 0,
             "displaced_other_kind": Counter()}
    unsafe = {"PLANT", "WATER", "HARVEST"}
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        slots_by_unit = _unit_slots(pkg, rid)
        step_edits: Dict[int, Dict[str, List]] = {}
        for u, slots in slots_by_unit.items():
            for win in _dwell_windows(slots):
                wset = set(win)
                if kind == "PLANT":
                    # 合同对配对（PLANT→次拍同日 WATER）
                    paired = {}
                    for s in win:
                        op = slots[s]
                        if op and op[0] == "PLANT" and s + 1 in wset \
                                and slots[s + 1][0] == "WATER" \
                                and (s + 1) // DAY == s // DAY:
                            paired[s] = s + 1
                    events = [s for s in win if slots[s][0] == "PLANT"]
                    if not events:
                        continue
                    stats["events"] += len(events)
                    order = sorted(paired, reverse=(delta > 0))
                    claimed: set = set()
                    for s in order:
                        w = paired[s]
                        src = {s, w}
                        tgt = {s + delta, s + delta + 1}
                        vac = sorted(src - tgt)
                        occ = sorted(tgt - src)
                        reason = None
                        if (s + delta) // DAY != s // DAY or \
                                (s + delta + 1) // DAY != s // DAY:
                            reason = "day_cross"
                        elif not tgt <= wset:
                            reason = "window_end"
                        elif (src | tgt) & claimed:
                            reason = "slot_claimed"
                        elif any(slots[t][0] in unsafe or slots[t][0] in _MOVES
                                  for t in occ):
                            reason = "contract_tail"   # 含位移锚点（空间零扰动）
                        if reason is not None:
                            stats["clamped"] += 1    # 口径=PLANT 事件数
                            stats["clamped_reasons"][reason] += 1
                            for c in (s, w):
                                table.append({"route": rid, "unit": u,
                                              "kind": kind, "from_step": c,
                                              "to_step": c,
                                              "op": list(slots[c]),
                                              "status": "clamped",
                                              "reason": reason})
                            continue
                        # 对块转位：目标←对块（PLANT→s+delta，WATER→+1）；
                        # 空出槽←落点位移件（序保持：sorted(occ)↔sorted(vac)）
                        tgt_ops = {s + delta: slots[s], s + delta + 1: slots[w]}
                        for t in tgt:
                            step_edits.setdefault(t, {})[u] = \
                                list(tgt_ops[t])
                        for v, o in zip(vac, occ):
                            step_edits.setdefault(v, {})[u] = list(slots[o])
                        claimed |= (src | tgt)
                        for c in (s, w):
                            table.append({"route": rid, "unit": u,
                                          "kind": kind, "from_step": c,
                                          "to_step": c + delta,
                                          "op": list(slots[c]),
                                          "status": "moved"})
                        stats["moved"] += 1    # 口径=PLANT 事件数（对=1）
                        stats["moved_pairs"] += 1
                        for t in occ:
                            stats["displaced_other_kind"][
                                str(slots[t][0])] += 1
                    for s in sorted(events):
                        if s not in paired:
                            stats["clamped"] += 1
                            stats["clamped_reasons"]["unpaired_plant"] += 1
                            table.append({"route": rid, "unit": u,
                                          "kind": kind, "from_step": s,
                                          "to_step": s, "op": list(slots[s]),
                                          "status": "clamped",
                                          "reason": "unpaired_plant"})
                else:
                    events = sorted(s for s in win
                                    if slots[s] and slots[s][0] == kind)
                    if not events:
                        continue
                    stats["events"] += len(events)
                    for chain in _chains(events, delta, wset):
                        tail = chain[-1] + delta
                        reason = None
                        if tail not in wset or slots[tail][0] in _MOVES:
                            reason = "window_end"
                        elif slots[tail][0] in {"PLANT", "WATER"}:
                            reason = "contract_tail"
                        elif any((c + delta) // DAY != c // DAY
                                 for c in chain):
                            reason = "day_cross"
                        if reason is not None:
                            stats["clamped"] += len(chain)
                            stats["clamped_reasons"][reason] += len(chain)
                            for c in chain:
                                table.append({"route": rid, "unit": u,
                                              "kind": kind, "from_step": c,
                                              "to_step": c, "op": list(slots[c]),
                                              "status": "clamped",
                                              "reason": reason})
                            continue
                        moves = [(chain[i + 1], slots[chain[i]]) for i in
                                 range(len(chain) - 1)]
                        moves.append((tail, slots[chain[-1]]))
                        moves.append((chain[0], slots[tail]))
                        for tgt_s, op in moves:
                            d = step_edits.setdefault(tgt_s, {})
                            if u in d:
                                raise RuntimeError(
                                    "写位冲突: rid=%s step=%s unit=%s"
                                    % (rid, tgt_s, u))
                            d[u] = list(op)
                        for c in chain:
                            table.append({"route": rid, "unit": u,
                                          "kind": kind, "from_step": c,
                                          "to_step": c + delta,
                                          "op": list(slots[c]),
                                          "displaced": list(slots[tail]),
                                          "displaced_from": tail,
                                          "status": "moved"})
                            stats["moved"] += 1
                        stats["displaced_other_kind"][str(slots[tail][0])] += 1
        if not step_edits:
            continue
        stats["routes"] += 1
        for s, edits in step_edits.items():
            idxs, _idx, act = rs._cow_action(pkg, rid, s)
            for u2, op in edits.items():
                rs._set_unit(act, u2, op)
            rs._commit_action(pkg, idxs, s, act)
    stats["clamped_reasons"] = dict(stats["clamped_reasons"])
    stats["displaced_other_kind"] = dict(stats["displaced_other_kind"])
    return stats


# ------------------------------------------------------------ 审计 --

def _op_multiset(pkg: Dict[str, Any], rid: str) -> Counter:
    c: Counter = Counter()
    for u, slots in _unit_slots(pkg, rid).items():
        for _s, op in slots.items():
            c[(u, str(op[0]), str(op[1]) if len(op) > 1 else "")] += 1
    return c


def _phase_hist(pkg: Dict[str, Any], rid: str, kind: str) -> Counter:
    h: Counter = Counter()
    for u, slots in _unit_slots(pkg, rid).items():
        for s, op in slots.items():
            if op and op[0] == kind:
                h[s % 4] += 1
    return h


def audit_variant(built: Dict[str, Any], pkg_base: Dict[str, Any]) -> Dict:
    """量守恒（逐单元 op 多重集精确不变）+ 前后画像 + %4 相位直方图。"""
    vid = built["variant_id"]
    spec = built["spec"]
    kind = spec["kind"]
    rids = sorted(set(r["route"] for r in built["table"]),
                  key=lambda k: int(k))
    rows = {}
    cons_ok = True
    for rid in rids:
        b_ms, v_ms = _op_multiset(pkg_base, rid), _op_multiset(built["pkg"], rid)
        b_prof, v_prof = tv.route_profile(pkg_base, rid), \
            tv.route_profile(built["pkg"], rid)
        same = b_ms == v_ms
        cons_ok = cons_ok and same
        rows[rid] = {
            "multiset_identical": bool(same),
            "anim_before": b_prof["anim"], "anim_after": v_prof["anim"],
            "plant_before": b_prof["plant"], "plant_after": v_prof["plant"],
            "phase4_before": dict(_phase_hist(pkg_base, rid, kind)),
            "phase4_after": dict(_phase_hist(built["pkg"], rid, kind)),
        }
    return {"variant_id": vid,
            "conservation_ok": bool(cons_ok),
            "conservation_note": "逐 (route,unit) op 多重集精确不变"
                                 "（链式转位=纯置换；市场单零触碰）",
            "n_table_rows": len(built["table"]), "routes": rows}


# ------------------------------------------------------------ 构建 --

def build_variant(vid: str, pkg_base: Dict[str, Any], main_text: str
                  ) -> Dict[str, Any]:
    """变体构建：链式转位→审计→编码（_encode_routes 四重自检）→main 文本。"""
    if vid not in VARIANTS:
        raise ValueError("未知变体: %r" % vid)
    spec = dict(VARIANTS[vid])
    work = copy.deepcopy(pkg_base)
    table: List[Dict[str, Any]] = []
    t0 = time.perf_counter()
    stats = surgery_phase(work, spec["kind"], int(spec["delta"]),
                          bool(spec["same_day"]), table)
    rs._pool_residue_sweep(work)
    new_text = rs._encode_routes(main_text, work)
    return {"variant_id": vid, "spec": spec, "pkg": work, "table": table,
            "stats": stats, "main_text": new_text,
            "elapsed_s": round(time.perf_counter() - t0, 2)}


def twin_check(built: Dict[str, Any], pkg_base: Dict[str, Any],
               rids: List[str]) -> Dict[str, Any]:
    """孪生三闸（tape_variants.feasibility_twin 原件复用；违规即弃）。"""
    return tv.feasibility_twin(built["pkg"], pkg_base, rids)
