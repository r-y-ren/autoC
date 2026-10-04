# -*- coding: utf-8 -*-
"""retape_shear_phase（R22 L2）：毛周期错峰手术。

责任契约（fn_docs/hybrid/responsibility.md【R22 增补】）：
把 r37 磁带羊格剪毛（HARVEST WOOL）轮次相位偏移出公开相（d17/20/23/26/29
型），错峰参数可配（默认偏移 +2 天型）；保每格刀次 ≥5（沿 R20 核算）、
只动剪毛 HARVEST 排程不动买卖/FEED/CARE；无可行错峰（刀次受损）→no-op
留档。输出变更表（kind=shear_phase）。

手术语义（歧义处理决定见各段 docstring）：
- 目标=把羊格剪毛轮次整体相位偏移 offset 天（默认 +2：公开相 d17/20/23/26/29
  → d19/22/25/28，+31 出季丢弃）。
- 刀次口径（沿 R20/retape_sheep._shear_cells 格位口径）：每格羊产毛窗期
  [buy_day+first_yield, last_day] 内被 HARVEST 认领的造访数；格位归属=
  unit_pos 执行后位置（count_shearings 同款）。
- 可行错峰（每格取可行偏移=产毛窗∩偏移目标日）：一刀从剪毛日 d 挪到
  d+offset，落点日须在产毛窗期 [buy+first, last_day]（不越季 ≤d29）且落点
  可达（retape_sheep harvest_move 走位口径：单元走位曼哈顿 ≤1 验可达，配套
  走位链把空闲单元带到羊格落刀；不可达→换拍/记 skip）。每格干净可挪刀数
  ≥ min_cuts(5) → 整体相位偏移（挪可行刀、丢出季/不可达余刀，「+31 出季
  丢弃」）；<5 → 该格 no-op 留档（刀次受损不抛，保原刀）。
- 只动剪毛 HARVEST 排程：落刀/让刀落在空闲 ['PASS'] 拍（walk+HARVEST），不
  覆盖 FEED/CARE/作物 HARVEST/买卖单/走位；市场单槽零触碰（742943 空槽位次
  语义：空槽不动、订单槽不删不移不填）。
- 保位次语义（空槽不动）+写时复制（_cow_action/_commit_action 池 append，
  路由指针改指新件）+自检链沿先例（_encode_routes 四件套）。
- 术后静态核算：每格刀次 ≥ min_cuts，不达标即抛 RuntimeError「刀次<5」。

输出 {"routes", "change_table"}：逐行 {route, kind:"shear_phase", item:"WOOL",
from_day, to_day, cells, reason}。from_day/to_day=该格剪毛轮次相位锚（首刀日
→ 首刀日+offset；no-op 时相等）；cells=[该格]；reason 记整体轮次平移与刀次
核算摘要；no-op 行 reason 以 "no-op" 起（留档）。
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# 跨包 import retape_sheep 私有编解码/核算件（KSIM 在 sys.path；兜底直连）。
_KSIM = str(Path(__file__).resolve().parent.parent)
if _KSIM not in sys.path:
    sys.path.insert(0, _KSIM)
try:
    from orderbook_r37.retape_sheep import (  # type: ignore
        _chain_ok, _check_package, _cow_action, _commit_action,
        _derive_grid_info, _idle_runs, _set_unit, _shear_cells, _units,
        _walk_path,
    )
except ImportError:  # 兜底：直接以 orderbook_r37/ 为 sys.path 根
    _R37 = str(Path(__file__).resolve().parent.parent / "orderbook_r37")
    if _R37 not in sys.path:
        sys.path.insert(0, _R37)
    from retape_sheep import (  # type: ignore
        _chain_ok, _check_package, _cow_action, _commit_action,
        _derive_grid_info, _idle_runs, _set_unit, _shear_cells, _units,
        _walk_path,
    )

# 刀次核算窗（沿 R20 TARGET_WINDOW 产毛节奏）。
FIRST_YIELD = 6
INTERVAL = 3
LAST_DAY = 29
MIN_CUTS = 5
DEFAULT_OFFSET = 2


def _cut_unit(seq: List[Dict[str, Any]], s: int, cell: Any,
              pos: Dict[Tuple[int, str], Any]) -> Optional[str]:
    """剪毛拍 s（产毛窗内 HARVEST 造访格 cell）的执行单元；非剪毛拍→None。"""
    for u, op in _units(seq[s]):
        if (isinstance(op, list) and op and op[0] == "HARVEST"
                and pos.get((s, u)) == cell):
            return u
    return None


def _place_walk(pkg: Dict[str, Any], idxs: List[int], rid: Any, cell: Any,
                day: int, pos: Dict[Tuple[int, str], Any],
                used: Set[Tuple[int, str]]) -> Optional[Tuple[int, str]]:
    """走位手术（harvest_move 先例）：day 当日把空闲单元走到羊格 cell 落刀。

    候选=单元空闲跑（连续 ['PASS'] 拍段）；round 形（往返）2m+1≤run、trail 形
    （单程驻留，跑到日末忙拍后）m+1≤run 且 t1>last_busy。落点 HARVEST 落在
    ['PASS'] 拍（不覆盖别的指令）；走位指令链 _chain_ok 可达。返回 (落刀拍,
    单元)；不可达→None（换拍/记 skip 由调用方）。写时复制改写走位+落刀。
    """
    D0 = day * 24
    D1 = min((day + 1) * 24, len(idxs))
    if D0 >= D1:
        return None
    seq = [pkg["actions"][i] for i in idxs]
    units = sorted({u for (s, u) in pos if D0 <= s < D1})
    cands: List[Tuple[int, str, int, Any, int, str, int, int]] = []
    for u in units:
        for t0, t1, p0, last_busy, broken in _idle_runs(seq, pos, u, day):
            if broken:
                continue
            if any((t, u) in used for t in range(t0, t1 + 1)):
                continue
            m = abs(int(p0[0]) - int(cell[0])) + abs(int(p0[1]) - int(cell[1]))
            span = t1 - t0 + 1
            forms: List[str] = []
            if 2 * m + 1 <= span:
                forms.append("round")
            if t1 > last_busy and m + 1 <= span and "round" not in forms:
                forms.append("trail")
            for form in forms:
                t_h = t0 + m
                if D0 <= t_h < D1:
                    cands.append((t_h, u, t0, p0, m, form, t1, last_busy))
    cands.sort(key=lambda x: (x[0], x[1]))
    for t_h, u, t0, p0, m, form, t1, last_busy in cands:
        if not _chain_ok(pos, t0, u):
            continue
        for i, (op, p) in enumerate(_walk_path(p0, cell)):
            _, _, act = _cow_action(pkg, rid, t0 + i)
            _set_unit(act, u, [op])
            _commit_action(pkg, idxs, t0 + i, act)
            pos[(t0 + i, u)] = p
            used.add((t0 + i, u))
        _, _, hact = _cow_action(pkg, rid, t_h)
        _set_unit(hact, u, ["HARVEST"])
        _commit_action(pkg, idxs, t_h, hact)
        pos[(t_h, u)] = cell
        used.add((t_h, u))
        if form == "round":
            for i, (op, p) in enumerate(_walk_path(cell, p0)):
                _, _, act = _cow_action(pkg, rid, t_h + 1 + i)
                _set_unit(act, u, [op])
                _commit_action(pkg, idxs, t_h + 1 + i, act)
                pos[(t_h + 1 + i, u)] = p
                used.add((t_h + 1 + i, u))
        else:
            for t in range(t_h + 1, t1 + 1):
                pos[(t, u)] = cell     # trail 跑尾段驻留（日界重生免返）
                used.add((t, u))
        return t_h, u
    return None


def retape_shear_phase(tape_routes: Dict[str, Any],
                       offset: Any = None) -> Dict[str, Any]:
    """毛期错峰手术+每格刀次静态核算（≥5 不达标即抛）。

    签名意图：输入: 磁带路由表+错峰参数 / 输出: {routes, change_table} /
    错误: 刀次 <5 即抛。

    输入形态（=_decode_routes 产物，磁带路由包）：
    {"actions": [动作...], "routes": {路由id: [动作池下标×N]}, "shops": [...]}；
    动作={"farmer": 单元指令, "hands": [单元指令...], "market": 订单槽位列表}。
    输出 {"routes": 手术后同形路由包（写时复制，输入零改动）, "change_table":
    逐格一行 {route, kind, item, from_day, to_day, cells, reason}}；kind=
    "shear_phase"（错峰成功 from_day≠to_day / no-op from_day==to_day 且 reason
    起 "no-op"）。

    offset: 相位偏移天型（缺省 DEFAULT_OFFSET=+2）；int(offset) 可配。

    术后静态核算：每格刀次 < MIN_CUTS → RuntimeError（刀次<5）。no-op 格保
    原刀次（≥5 不触红）；错峰格刀次=干净可挪刀数（≥5 入选）。
    """
    # ---- 0. 输入预检（fail-closed）----
    if not isinstance(tape_routes, dict):
        raise TypeError("tape_routes must be dict, got %s"
                        % type(tape_routes).__name__)
    off = DEFAULT_OFFSET if offset is None else int(offset)
    _check_package(tape_routes)
    pkg = copy.deepcopy(tape_routes)          # 输入零改动（写时复制手术）
    grid = _derive_grid_info(pkg)             # {rid: {cells, unit_pos}}
    change_table: List[Dict[str, Any]] = []

    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        if rid not in grid:
            continue
        idxs = pkg["routes"][rid]
        g = grid[rid]
        pos: Dict[Tuple[int, str], Any] = g["unit_pos"]
        used: Set[Tuple[int, str]] = set()   # 走位落点占用（路由级，防格间走位重叠）
        for c in sorted(g["cells"], key=repr):
            seq = [pkg["actions"][i] for i in idxs]
            info = _shear_cells(seq, g)[c]
            b = int(info["buy_day"])
            cut_list: List[Tuple[int, str]] = []
            for s in sorted(info["cuts"]):
                u = _cut_unit(seq, s, c, pos)
                if u is not None:
                    cut_list.append((s, u))
            orig_days = sorted({s // 24 for s, _ in cut_list})

            # 逐刀走位手术挪到偏移日；快照/回退防半成品（<5 刀即回退 no-op）。
            idxs_snap = list(idxs)
            pos_snap = dict(pos)
            pool_snap = len(pkg["actions"])
            used_snap = set(used)
            moves: List[Tuple[int, str, int, str]] = []
            for s, u in cut_list:
                tday = s // 24 + off
                if not (b + FIRST_YIELD <= tday <= LAST_DAY):
                    continue                    # 出季/越窗 → 丢（+31 出季丢弃）
                r = _place_walk(pkg, idxs, rid, c, tday, pos, used)
                if r is not None:
                    moves.append((s, u, r[0], r[1]))

            if len(moves) >= MIN_CUTS:
                # 整体相位偏移：源剪毛让刀（→PASS）；落刀已由走位手术写回。
                tgt = {(ts, tu) for _, _, ts, tu in moves}
                for s, u in cut_list:
                    if (s, u) not in tgt:
                        _, _, act = _cow_action(pkg, rid, s)
                        _set_unit(act, u, ["PASS"])
                        _commit_action(pkg, idxs, s, act)
                new_days = sorted({ts // 24 for _, _, ts, _ in moves})
                change_table.append({
                    "route": rid, "kind": "shear_phase", "item": "WOOL",
                    "from_day": (orig_days[0] if orig_days else None),
                    "to_day": (new_days[0] if new_days else None),
                    "cells": [c],
                    "reason": ("shear_phase offset=%+d cell=%r rounds %s->%s "
                               "n_cuts %d->%d（整体相位平移；出季/不可达余刀 "
                               "%d 丢弃）"
                               % (off, c, orig_days, new_days, len(cut_list),
                                  len(moves), len(cut_list) - len(moves))),
                })
            else:
                # 无可行错峰（刀次受损）→ no-op 留档（回退半成品，保原刀不抛）。
                idxs[:] = idxs_snap
                del pkg["actions"][pool_snap:]   # 剪走位手术孤儿件（池复原）
                pos.clear()
                pos.update(pos_snap)
                used.clear()
                used.update(used_snap)
                change_table.append({
                    "route": rid, "kind": "shear_phase", "item": "WOOL",
                    "from_day": (orig_days[0] if orig_days else None),
                    "to_day": (orig_days[0] if orig_days else None),
                    "cells": [c],
                    "reason": ("no-op: offset=%+d cell=%r 干净可挪刀 %d<%d "
                               "（刀次受损不抛，保原刀）rounds %s kept"
                               % (off, c, len(moves), MIN_CUTS, orig_days)),
                })

    # ---- 术后静态核算（每格刀次 ≥ MIN_CUTS，不达标即抛）----
    grid2 = _derive_grid_info(pkg)
    bad: List[str] = []
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        if rid not in grid2:
            continue
        g2 = grid2[rid]
        seq2 = [pkg["actions"][i] for i in pkg["routes"][rid]]
        for c, v in sorted(_shear_cells(seq2, g2).items(),
                           key=lambda kv: repr(kv[0])):
            if v["n_cuts"] < MIN_CUTS:
                bad.append("route %s cell %r n_cuts=%d" % (rid, c, v["n_cuts"]))
    if bad:
        raise RuntimeError("刀次<5 术后静态核算红：%s" % "; ".join(bad[:8]))

    return {"routes": pkg, "change_table": change_table}
