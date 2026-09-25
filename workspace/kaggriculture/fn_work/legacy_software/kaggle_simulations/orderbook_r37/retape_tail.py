# -*- coding: utf-8 -*-
"""retape_tail_savings（R20 L2）：磁带手术·尾盘负空间。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
d28（step 672）起删除 CARE 指令、d29（step 696）起删除 FEED 与闲置 HIRE
指令（省人工/饲料）；动物格 HARVEST（剪毛/收奶/收蛋）与卖单照旧（存量资产
变现不砍）；输出删除清单入变更表。

引擎事实（exports/probes/twin_fidelity/engine_cache/kaggriculture.py 实读）：
- 一季 d0..d29（turnsPerDay=24，步 0..718）；日结 _end_of_day 只在步
  23,47,…,695 发生（(step+1)%24==0 且 step≤718），最后一次=step 695
  （d28→d29），d29→d30 转换不发生（游戏结束）→ d29 起 FEED 纯浪费
  （fed_today 无人消费）、d28 起 CARE 纯浪费（cared_today 只把加成打进
  pending_care_bonus，落在永不发生的下次产日）。
- consecutive_unfed 只在日结自增（≥2 牲畜逃走）；删除域（步 ≥672）之后
  无任何日结，删除不可能让任何牲畜在游戏结束前达到 2（d29 停喂最多累计 1
  不触发）——d28 的 FEED（672..695）必须保留（喂养 d28→d29 日结）。
- **hands 日结归零**（_end_of_day: farm["hands"]=[]、hires_today=0）：手只
  活当日；_do_hire 按成功序 append → 当日第 m 张 HIRE 新雇的手=当日
  hands[m]；hands[i]=第 i 手单元指令（缺失/["PASS"]/垃圾=无指派，引擎
  静默 no-op）。单元动作先于市场执行 → 雇佣步当步 hands[m] 指令落不到新
  手上。
- 市场槽位次语义（742943）：删槽改撮合配对 → HIRE 删除=原位换 []（cash_guard
  顺延置 [] 先例）；HIRE 为原子单，与 [] 同样不进锁步撮合，位次语义不变。

删除判据（术后全量对账，破即抛）：
- CARE：步 ≥672 的单元指令（farmer/hands，op[0]=='CARE'）→ ["PASS"]。
- FEED：步 ≥696 的单元指令（op[0]=='FEED'）→ ["PASS"]。
- HIRE：步 ≥696 的市场单（o[0]=='HIRE'）且「闲置」→ 槽换 []。闲置=该 HIRE
  新雇的手（当日 HIRE 市场序 m → 当日 hands[m]）在其雇佣步之后至当日晚步的
  hands 槽中无任何动作指派；判定基于原磁带（写时复制前视图）。保守：拿不准
  就不删——同日雇佣步**及其之前** slot m 已有指派（登记不一致，手尚未诞生）
  → 记 uncertain 保留。
- 不动清单：动物格 HARVEST 与一切 market 单（SELL/BUY_*）、PLANT/WATER/移动
  等一律不动；d28 前的 FEED/CARE、d28 的 FEED（672..695）不动。误删任一
  → RuntimeError（契约「误删…即抛」）。

手术形态（写时复制）：动作池共享（同池件可被多路由/多步引用）——删除某路由
某步指令=该路由该步动作深拷贝改写（新件 append 入池、路由指针改指），池内
共享件零扰动、输入零改动；decode→surgery→encode 往返由 retape_sheep
._encode_routes 自检链兜底（blob 区间外字节等价/回路一致/可编译/确定性双跑）。

输出 {"routes": 手术后磁带路由包, "removed": 删除清单}；清单行
{route, step, kind, slot, unit, item, qty, reason}（kind∈{CARE,FEED,HIRE}；
slot=市场槽 int（HIRE）与 unit=单元 'F'|'hN'（CARE/FEED）互斥恰一非空；
item/qty=所省资源：FEED→WHEAT 1、HIRE→HAND 1、CARE→null），供 build 内嵌
「# R37_TAIL_REMOVAL_LIST: <json>」与 pack 记 sha。
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

try:
    from orderbook_r37 import retape_sheep as _rs
except ImportError:                      # 脚本态兜底（build_r37 同款）
    import retape_sheep as _rs           # type: ignore

#: turnsPerDay=24：d28 起点步、d29 起点步（删除窗）。
TURNS_PER_DAY = 24
CARE_FROM_STEP = 28 * TURNS_PER_DAY     # 672
FEED_FROM_STEP = 29 * TURNS_PER_DAY     # 696

_REMOVAL_KINDS = ("CARE", "FEED", "HIRE")


# ---------------------------------------------------------------------------
# 闲置 HIRE 判定（当日登记表：hands 日结归零，第 m 张当日 HIRE=当日 hands[m]）
# ---------------------------------------------------------------------------
def _is_assign(op: Any) -> bool:
    """非 PASS 的合法单元指令才算「动作指派」（其余=无指派，引擎静默 no-op）。"""
    return (isinstance(op, list) and bool(op) and isinstance(op[0], str)
            and op[0] != "PASS")


def _day_ordinals(seq: List[Dict[str, Any]]) -> Dict[Tuple[int, int], int]:
    """HIRE 市场位序 (step, slot) → 当日手号 m（市场序=步升序、槽升序）。"""
    out: Dict[Tuple[int, int], int] = {}
    per_day: Dict[int, int] = {}
    for s, a in enumerate(seq):
        for j, o in enumerate(a.get("market") or []):
            if isinstance(o, list) and o and o[0] == "HIRE":
                d = s // TURNS_PER_DAY
                m = per_day.get(d, 0)
                per_day[d] = m + 1
                out[(s, j)] = m
    return out


def _slot_op(a: Dict[str, Any], m: int) -> Any:
    hands = a.get("hands") or []
    return hands[m] if m < len(hands) else None


def _hire_verdict(seq: List[Dict[str, Any]], step: int, slot: int, m: int) -> str:
    """HIRE (step,slot) 新雇手（当日 hands[m]）判定：idle/employed/uncertain。

    窗口：employed=雇佣步之后至当日晚步（hands 日结归零，晚日 hands[m] 属
    别的手；删除域=末日 d29，恰=契约「其后所有步」）；uncertain=同日雇佣步
    及其之前 slot m 已有指派（手尚未诞生，登记不一致→保守保留）。
    """
    day_start = (step // TURNS_PER_DAY) * TURNS_PER_DAY
    day_end = min(day_start + TURNS_PER_DAY - 1, len(seq) - 1)
    if any(_is_assign(_slot_op(seq[x], m)) for x in range(day_start, step + 1)):
        return "uncertain"
    if any(_is_assign(_slot_op(seq[x], m)) for x in range(step + 1, day_end + 1)):
        return "employed"
    return "idle"


# ---------------------------------------------------------------------------
# 术后全量对账（fail-closed；契约「误删 HARVEST/卖单/d28 前 FEED-CARE 即抛」）
# ---------------------------------------------------------------------------
def _audit_removals(before: Dict[str, Any], after: Dict[str, Any],
                    removed: List[Dict[str, Any]]) -> None:
    """输入/输出逐槽对账：差异恰=删除清单且逐条合法，破即 RuntimeError。

    校验面：①清单行形态与窗口（CARE≥672、FEED/HIRE≥696）、kind 与被删形态
    一致；②HIRE 逐条重算闲置判定（非 idle 即误删）；③逐路由逐步逐槽 diff
    与清单双向恰好对应（多删/少删/误改 HARVEST·卖单·窗口外 FEED-CARE 皆红）；
    ④结构不变量：步数、hands 长度、market 槽位数与 shops 不动。
    """
    if (set(after) != set(before)
            or not {"actions", "routes", "shops"} <= set(after)
            or after["shops"] != before["shops"]):
        raise RuntimeError("误删红：磁带包结构/shops 被改动")
    if set(after["routes"]) != set(before["routes"]):
        raise RuntimeError("误删红：路由集合被改动")
    entries: Dict[Tuple[str, int, Tuple[str, Any]], Dict[str, Any]] = {}
    for e in removed:
        if not isinstance(e, dict) or set(e) != {"route", "step", "kind", "slot",
                                                 "unit", "item", "qty", "reason"}:
            raise RuntimeError("误删红：删除清单行形态非法 %r" % (e,))
        rid, s, kind = e["route"], e["step"], e["kind"]
        if kind == "CARE":
            ok = (s >= CARE_FROM_STEP and isinstance(e["unit"], str)
                  and e["slot"] is None and e["item"] is None and e["qty"] is None)
            tgt = ("unit", e["unit"])
        elif kind == "FEED":
            ok = (s >= FEED_FROM_STEP and isinstance(e["unit"], str)
                  and e["slot"] is None and e["item"] == "WHEAT" and e["qty"] == 1)
            tgt = ("unit", e["unit"])
        elif kind == "HIRE":
            ok = (s >= FEED_FROM_STEP and isinstance(e["slot"], int)
                  and e["unit"] is None and e["item"] == "HAND" and e["qty"] == 1)
            tgt = ("market", e["slot"])
        else:
            ok = False
            tgt = ("?", None)
        if not ok:
            raise RuntimeError("误删红：删除清单行越窗/字段不合法 %r" % (e,))
        key = (rid, s, tgt)
        if key in entries:
            raise RuntimeError("误删红：删除清单重复行 %r" % (key,))
        entries[key] = e

    seen = set()
    for rid in sorted(before["routes"], key=lambda k: int(k)):
        ids_b, ids_a = before["routes"][rid], after["routes"][rid]
        if len(ids_b) != len(ids_a):
            raise RuntimeError("误删红：路由 %s 步数被改动 %d->%d"
                               % (rid, len(ids_b), len(ids_a)))
        seq_b = [before["actions"][i] for i in ids_b]
        seq_a = [after["actions"][i] for i in ids_a]
        ord_map = _day_ordinals(seq_b)
        for s, (ab, aa) in enumerate(zip(seq_b, seq_a)):
            fb, fa = ab.get("farmer"), aa.get("farmer")
            if fb != fa:
                key = (rid, s, ("unit", "F"))
                e = entries.get(key)
                if e is None or not (isinstance(fb, list) and fb and fb[0] == e["kind"]
                                     and e["kind"] in ("CARE", "FEED") and fa == ["PASS"]):
                    raise RuntimeError("误删红：farmer 指令被误改 %s@%d %r->%r"
                                       % (rid, s, fb, fa))
                seen.add(key)
            hb = ab.get("hands") or []
            ha = aa.get("hands") or []
            if len(hb) != len(ha):
                raise RuntimeError("误删红：hands 槽数被改动 %s@%d" % (rid, s))
            for i in range(len(hb)):
                if hb[i] != ha[i]:
                    key = (rid, s, ("unit", "h%d" % i))
                    e = entries.get(key)
                    if e is None or not (isinstance(hb[i], list) and hb[i]
                                         and hb[i][0] == e["kind"]
                                         and e["kind"] in ("CARE", "FEED")
                                         and ha[i] == ["PASS"]):
                        raise RuntimeError("误删红：hands[%d] 指令被误改 %s@%d %r->%r"
                                           % (i, rid, s, hb[i], ha[i]))
                    seen.add(key)
            mb = ab.get("market") or []
            ma = aa.get("market") or []
            if len(mb) != len(ma):
                raise RuntimeError("误删红：market 槽位数被改动 %s@%d" % (rid, s))
            for j in range(len(mb)):
                if mb[j] != ma[j]:
                    key = (rid, s, ("market", j))
                    e = entries.get(key)
                    if e is None or not (isinstance(mb[j], list) and mb[j]
                                         and mb[j][0] == "HIRE"
                                         and e["kind"] == "HIRE" and ma[j] == []):
                        raise RuntimeError("误删红：market 槽被误改 %s@%d slot%d %r->%r"
                                           % (rid, s, j, mb[j], ma[j]))
                    seen.add(key)
        for (erid, es, tgt), e in entries.items():
            if erid != rid or tgt[0] != "market":
                continue
            m = ord_map.get((es, tgt[1]))
            if m is None:
                raise RuntimeError("误删红：删除清单 HIRE 位不存在 %r" % ((rid, es, tgt),))
            if _hire_verdict(seq_b, es, tgt[1], m) != "idle":
                raise RuntimeError("误删红：非闲置 HIRE 被删 %r（拿不准就不删）"
                                   % ((rid, es, tgt),))
    if seen != set(entries):
        missing = set(entries) - seen
        raise RuntimeError("误删红：删除清单与实际差异不对应（无实体删除）%r"
                           % sorted(missing, key=str)[:5])


# ---------------------------------------------------------------------------
# 主契约函数
# ---------------------------------------------------------------------------
def retape_tail_savings(tape_routes: Dict[str, Any]) -> Dict[str, Any]:
    """尾盘 CARE/FEED/闲置 HIRE 修剪+删除清单输出。

    签名意图：输入: 磁带 / 输出: {routes, removed}（修剪后磁带+删除清单） /
    错误: 误删 HARVEST/卖单/d28 前 FEED-CARE 指令即抛。

    输入形态（=_decode_routes 产物，磁带路由包）：{"actions": [动作...],
    "routes": {路由id: [动作池下标×719]}, "shops": [...]}；动作={"farmer":
    单元指令, "hands": [单元指令...], "market": [订单槽...]}。
    输出 {"routes": 手术后同形路由包（写时复制，输入零改动）, "removed":
    删除清单行 {route, step, kind, slot, unit, item, qty, reason}}。
    判据与不动清单见模块 docstring；术后全量对账（_audit_removals）任一
    破绽即 RuntimeError。
    """
    if not isinstance(tape_routes, dict):
        raise TypeError("tape_routes must be dict, got %s"
                        % type(tape_routes).__name__)
    _rs._check_package(tape_routes)
    pkg = copy.deepcopy(tape_routes)      # 输入零改动（写时复制手术）
    removed: List[Dict[str, Any]] = []

    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [tape_routes["actions"][i] for i in idxs]   # 判定基于原磁带
        ord_map = _day_ordinals(seq)
        for s in range(len(idxs)):
            edits: List[Tuple[Tuple[str, Any], str, Optional[str], Optional[int],
                              str]] = []
            for u, op in _rs._units(seq[s]):
                if not (isinstance(op, list) and op and isinstance(op[0], str)):
                    continue
                if op[0] == "CARE" and s >= CARE_FROM_STEP:
                    edits.append((("unit", u), "CARE", None, None,
                                  "tail_care_waste: d%d CARE 加成落在永不发生的"
                                  "下次产日（d29→d30 转换不发生），删除省照顾"
                                  % (s // TURNS_PER_DAY)))
                elif op[0] == "FEED" and s >= FEED_FROM_STEP:
                    edits.append((("unit", u), "FEED", "WHEAT", 1,
                                  "tail_feed_waste: d%d FEED 无日结消费（fed_today"
                                  " 落空），删除省 1 WHEAT 饲料"
                                  % (s // TURNS_PER_DAY)))
            if s >= FEED_FROM_STEP:
                for j, o in enumerate(seq[s].get("market") or []):
                    if not (isinstance(o, list) and o and o[0] == "HIRE"):
                        continue
                    m = ord_map[(s, j)]
                    if _hire_verdict(seq, s, j, m) != "idle":
                        continue      # 有役/拿不准：保守不删
                    edits.append((("market", j), "HIRE", "HAND", 1,
                                  "tail_idle_hire: 新雇手（d%d hands[%d]）雇佣后"
                                  "至日末无任何动作指派，删除省 1 手人工"
                                  % (s // TURNS_PER_DAY, m)))
            if not edits:
                continue
            # 写时复制：深拷贝池件改写，append 入池，路由指针改指（共享件零扰动）
            act = copy.deepcopy(pkg["actions"][idxs[s]])
            for tgt, kind, item, qty, reason in edits:
                if tgt[0] == "unit":
                    _rs._set_unit(act, tgt[1], ["PASS"])
                    removed.append({"route": rid, "step": s, "kind": kind,
                                    "slot": None, "unit": tgt[1],
                                    "item": item, "qty": qty, "reason": reason})
                else:
                    act["market"][tgt[1]] = []    # 位次语义：原位换 [] 不删槽
                    removed.append({"route": rid, "step": s, "kind": kind,
                                    "slot": tgt[1], "unit": None,
                                    "item": item, "qty": qty, "reason": reason})
            pkg["actions"].append(act)
            idxs[s] = len(pkg["actions"]) - 1

    _audit_removals(tape_routes, pkg, removed)
    return {"routes": pkg, "removed": removed}
