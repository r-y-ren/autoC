# -*- coding: utf-8 -*-
"""retape_sell_lots（R23 L2）：卖单批量化手术。

责任契约（fn_docs/hybrid/responsibility.md【R23 增补】retape_sell_lots）：
d21-28 晚季窗磁带 SELL 单合并放大（少而大，目标批量化率对标 ~337 单级）；
只动卖单量/槽、不动物品总量（卖出守恒）；越窗/守恒破→抛；变更表 kind=sell_lots。

证据口径（分析24，勿搞反）：败局对手（赢我们的）卖单**更少更大**（中位
337 单 vs 赢局对手 405）——目标=向"少而大"靠拢（单数下探至 ~337 量级、
单均量升）；d21-28 是失血段（12 败中 9 败 worst_seg=d21-28）。

手术语义（歧义处理决定留档）：
- 合并域：每路由 step∈window 的 SELL 单（['SELL',item,qty]，qty 为 ≥0 int；
  真磁带含 qty=0 占坑单，照并守恒），**同品合并**。不动 BUY_*/HIRE 与
  farmer/hands 单元指令（FEED/CARE/HARVEST/移动）；窗外步零触碰。
- ①同拍并单（无条件）：同拍同品多单并一单，落点=该拍组内最早槽。
- ②跨拍批量化（目标驱动）：同品单按 (step,slot) 升序切连续 run（"临近"=
  序相邻；run 内同拍重复已由①吸收），每 run 并一单，落点=run 首单的
  (step,slot)。**歧义留档（落点方向）**：取"合并到更早的批次步点或同拍并
  单"口径（只提前不推后）；不取"较大批次步点"的晚拍变体——卖单后移会把
  供资卖单挪到依赖消费之后（V57 资金序先例），只提前是安全向。
- 卖出守恒：合并前后每（路由,品）卖出总量不变（全磁带口径），术后全量对
  账不过即抛 RuntimeError；越窗（变更行步点出窗/窗外步被改动/窗外槽被扰）
  →抛 RuntimeError；参数越界（window 越出磁带步界等）→抛 ValueError。
- 空槽位次语义（742943 先例）：合并后空出的槽置 [] 不删，market 槽位数与
  非卖单槽内容逐槽保持；目标槽只写 ['SELL',item,合计]。
- 动作池共享写时复制（复用 retape_sheep._cow_action/_commit_action/
  _pool_residue_sweep）：同池件可被多路由引用，手术只深拷贝改写+append 入
  池+改路由指针，输入零改动；编解码底座复用 orderbook_r37.retape_sheep
  的 _decode_routes/_encode_routes（blob=base85(zlib(json))，R15 自检链），
  本函数只吃磁带路由包 {actions,routes,shops}，包形态由 _check_package 把关。

目标口径（params={"max_orders_target", "window"}）：
- max_orders_target 缺省 337 =分析24 败局对手卖单中位 337 单级——**每路由
  整条磁带** SELL 单数的目标量级（对标而非过拟合；真 r37 磁带窗内单数中位
  139、全带中位 435，窗内单数中位下探即全带向 ~337 收敛）。
- 实现=只在窗内合并：窗内允许留存单数 budget=max_orders_target−窗外单数
  （钳位 [每品 ≥1 单, 窗内现单数]），按品比例分批（最大余数法，确定性），
  连续 run 切批落地；已 ≤ 目标（或 budget=窗内现单数）的路由只做①。
  真跑实测见 evidence/retape_lots_realrun.json（窗内单数/单均量/守恒摘要）。
- window 缺省 (504,672)=d21-28 窗（day=step//24，[d21*24, d28*24)）。

输出 {"routes": 手术后磁带路由包（写时复制，输入零改动）, "change_table":
逐变更行 {route, kind:"sell_lots", item, from_steps, to_step, qty, reason}}
（from_steps=合并各单所在步，按单计，同拍并单呈重复步；to_step=落点步；
qty=合并总量）。
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Tuple

try:
    from orderbook_r37 import retape_sheep as _rs
except ImportError:                      # 脚本态兜底（retape_tail 同款）
    import retape_sheep as _rs           # type: ignore

#: 批量化参数缺省（max_orders_target=分析24 败局对手中位 337 单级；window=
#: d21-28 窗 [504,672)）。
DEFAULT_PARAMS: Dict[str, Any] = {
    "max_orders_target": 337,
    "window": (504, 672),
}


def _resolve_params(params: Any) -> Tuple[int, Tuple[int, int]]:
    """params → (max_orders_target, (w0, w1))；缺省补齐，越型/未知键即抛。"""
    p = dict(DEFAULT_PARAMS)
    if params is not None:
        if not isinstance(params, dict):
            raise ValueError("params 须为 dict 或 None，得到 %s"
                             % type(params).__name__)
        unknown = sorted(k for k in params if k not in DEFAULT_PARAMS)
        if unknown:
            raise ValueError("params 未知键 %r（仅 %r）"
                             % (unknown, sorted(DEFAULT_PARAMS)))
        p.update(params)
    target = p["max_orders_target"]
    if isinstance(target, bool) or not isinstance(target, int) or target < 1:
        raise ValueError("max_orders_target 须为 ≥1 int，得到 %r" % (target,))
    win = p["window"]
    if not isinstance(win, (list, tuple)) or len(win) != 2:
        raise ValueError("window 须为 (w0, w1) 两元组，得到 %r" % (win,))
    for w in win:
        if isinstance(w, bool) or not isinstance(w, int):
            raise ValueError("window 边界须为 int，得到 %r" % (win,))
    w0, w1 = int(win[0]), int(win[1])
    if not (0 <= w0 < w1):
        raise ValueError("window 须 0<=w0<w1，得到 %r" % (win,))
    return int(target), (w0, w1)


def _route_order(routes: Dict[Any, Any]) -> List[Any]:
    """路由键确定性序（数字串按数值，其余按字典序）。"""
    return sorted(routes, key=lambda k: (0, int(k)) if str(k).isdigit()
                  else (1, str(k)))


def _seq(pkg: Dict[str, Any], rid: Any) -> List[Dict[str, Any]]:
    return [pkg["actions"][i] for i in pkg["routes"][rid]]


def _sell_qty(o: Any) -> Tuple[str, int]:
    """SELL 单形态校验 → (item, qty)；qty 为 ≥0 int（真磁带含 qty=0 占坑单）。"""
    if not (isinstance(o, list) and o and o[0] == "SELL"):
        raise ValueError("非 SELL 单进入卖单核算: %r" % (o,))
    if len(o) != 3 or not isinstance(o[1], str):
        raise ValueError("SELL 单形态须为 ['SELL',item,qty]，得到 %r" % (o,))
    qty = o[2]
    if isinstance(qty, bool) or not isinstance(qty, int) or qty < 0:
        raise ValueError("SELL qty 须为 ≥0 int，得到 %r" % (o,))
    return o[1], qty


def _sell_scan(seq: List[Dict[str, Any]], lo: int, hi: int
               ) -> List[Tuple[int, int, str, int]]:
    """[lo,hi) 窗内 SELL 清单 [(step, slot, item, qty)]（(step,slot) 升序）。"""
    out: List[Tuple[int, int, str, int]] = []
    for s in range(lo, min(hi, len(seq))):
        for j, o in enumerate(seq[s].get("market") or []):
            if isinstance(o, list) and o and o[0] == "SELL":
                item, qty = _sell_qty(o)
                out.append((s, j, item, qty))
    return out


def _sell_totals(seq: List[Dict[str, Any]]) -> Dict[str, int]:
    """全磁带每品卖出总量 {item: qty}（守恒核算基线；形态校验 fail-closed）。"""
    tot: Dict[str, int] = {}
    for a in seq:
        for o in a.get("market") or []:
            if isinstance(o, list) and o and o[0] == "SELL":
                item, qty = _sell_qty(o)
                tot[item] = tot.get(item, 0) + qty
    return tot


def _sell_count(seq: List[Dict[str, Any]]) -> int:
    """全磁带 SELL 单数（批量化率口径）。"""
    return sum(1 for a in seq for o in (a.get("market") or [])
               if isinstance(o, list) and o and o[0] == "SELL")


def _write_lot(mkt: List[Any], slot: int, item: str, qty: int) -> None:
    """目标槽写入合并后 SELL 单（守恒破测试的故障注入缝）。"""
    mkt[slot] = ["SELL", item, qty]


def _apply_group(pkg: Dict[str, Any], rid: Any, item: str,
                 members: List[Tuple[int, int, int]],
                 change_table: List[Dict[str, Any]], reason: str) -> None:
    """一组合并落地（写时复制）：落点=最早 (step,slot)，其余源槽置 []。

    members=[(step, slot, qty)] 按 (step,slot) 升序且 ≥2；只提前不推后由
    落点=首单保证（审计另行核算）。
    """
    land_step, land_slot, _ = members[0]
    total = sum(q for _, _, q in members)
    for s in sorted({m[0] for m in members}):
        idxs, _, act = _rs._cow_action(pkg, rid, s)
        mkt = act["market"]
        for ms, slot, _q in members:
            if ms != s:
                continue
            if slot == land_slot and ms == land_step:
                _write_lot(mkt, slot, item, total)
            else:
                mkt[slot] = []
        _rs._commit_action(pkg, idxs, s, act)
    change_table.append({
        "route": rid, "kind": "sell_lots", "item": item,
        "from_steps": [m[0] for m in members], "to_step": land_step,
        "qty": total, "reason": reason,
    })


def _allocate(counts: List[Tuple[str, int]], total: int) -> Dict[str, int]:
    """每品批数分配（确定性最大余数法）：Σb_i=total 钳位 [品数, Σn_i]。

    counts=[(item, n_i)]（输入序任意，内部按 (-n_i, item) 定序）；b_i≥1。
    """
    order = sorted(counts, key=lambda kv: (-kv[1], kv[0]))
    n_items = len(order)
    cap_total = sum(n for _, n in order)
    total = max(n_items, min(cap_total, total))
    out = {item: 1 for item, _ in order}
    remaining = total - n_items
    if remaining <= 0:
        return out
    caps = [(item, n - 1) for item, n in order]
    free = sum(c for _, c in caps)
    if free <= 0:
        return out
    shares = []
    for item, cap in caps:
        exact = remaining * cap / free
        give = int(exact)            # 向下取整份额
        out[item] += give
        shares.append((exact - give, cap, item))
    left = total - sum(out.values())
    shares.sort(key=lambda t: (-t[0], -t[1], t[2]))
    for _, _, item in shares[:left]:
        out[item] += 1
    return out


def _split_runs(lots: List[Tuple[int, int, int]], b: int
                ) -> List[List[Tuple[int, int, int]]]:
    """同品单 (step,slot) 升序 → b 个连续 run（前段不小于后段，确定性）。"""
    n = len(lots)
    b = max(1, min(n, b))
    q, r = divmod(n, b)
    runs: List[List[Tuple[int, int, int]]] = []
    pos = 0
    for i in range(b):
        size = q + (1 if i < r else 0)
        runs.append(lots[pos:pos + size])
        pos += size
    return runs


def _post_check(pkg: Dict[str, Any], src: Dict[str, Any],
                window: Tuple[int, int],
                change_table: List[Dict[str, Any]]) -> None:
    """术后全量对账（破即抛）：卖出守恒/越窗/窗外不动/非卖单不动/只提前。"""
    w0, w1 = window
    for rid in _route_order(pkg["routes"]):
        pre_tot = _sell_totals(_seq(src, rid))
        post_tot = _sell_totals(_seq(pkg, rid))
        if pre_tot != post_tot:
            raise RuntimeError("卖出守恒破（route=%r）：前 %r 后 %r"
                               % (rid, pre_tot, post_tot))
        oidxs, nidxs = src["routes"][rid], pkg["routes"][rid]
        if len(oidxs) != len(nidxs):
            raise RuntimeError("越窗：路由步数被改动（route=%r）" % (rid,))
        for s in range(len(nidxs)):
            oact, nact = src["actions"][oidxs[s]], pkg["actions"][nidxs[s]]
            if not w0 <= s < w1:
                if nact != oact:
                    raise RuntimeError("越窗：窗外步被改动（route=%r step=%d）"
                                       % (rid, s))
                continue
            omkt = oact.get("market") or []
            nmkt = nact.get("market") or []
            if len(omkt) != len(nmkt):
                raise RuntimeError("槽位数被改动（route=%r step=%d）" % (rid, s))
            for j, (oo, no) in enumerate(zip(omkt, nmkt)):
                if isinstance(oo, list) and oo and oo[0] == "SELL":
                    if not (no == [] or (isinstance(no, list) and no
                            and no[0] == "SELL" and no[1] == oo[1])):
                        raise RuntimeError(
                            "卖单槽改写异常（route=%r step=%d slot=%d）"
                            % (rid, s, j))
                elif no != oo:
                    raise RuntimeError(
                        "非卖单槽被改动（route=%r step=%d slot=%d）" % (rid, s, j))
            for key in set(oact) | set(nact):
                if key != "market" and oact.get(key) != nact.get(key):
                    raise RuntimeError(
                        "单元指令被改动（route=%r step=%d key=%r）" % (rid, s, key))
    for row in change_table:
        if row.get("kind") != "sell_lots":
            raise RuntimeError("变更行 kind 非 sell_lots：%r" % (row,))
        steps = list(row.get("from_steps") or []) + [row.get("to_step")]
        if any(not (w0 <= t < w1) for t in steps):
            raise RuntimeError("越窗：变更行步点出窗：%r" % (row,))
        if row["to_step"] > min(row["from_steps"]):
            raise RuntimeError("推后合并（只提前不推后破）：%r" % (row,))


def retape_sell_lots(tape_routes: Dict[str, Any],
                     params: Any = None) -> Dict[str, Any]:
    """卖单批量化手术+卖出守恒核算。

    签名意图：输入: 磁带路由表+批量化参数 / 输出: {routes, change_table} /
    错误: 卖出守恒破即抛。

    输入形态（=_decode_routes 产物，磁带路由包 {actions, routes, shops}）；
    params=None 用 DEFAULT_PARAMS，dict 时按缺省补齐（仅
    {"max_orders_target", "window"}）。手术语义/歧义决定/目标口径见模块
    docstring；返回 routes 为写时复制新包（输入零改动），change_table 逐行
    {route, kind:"sell_lots", item, from_steps, to_step, qty, reason}。
    错误：参数越型/越界（window 越出磁带步界）→ValueError；术后对账破
    （卖出守恒/越窗/误动非卖单或单元指令）→RuntimeError。
    """
    target, (w0, w1) = _resolve_params(params)
    _rs._check_package(tape_routes)
    min_len = min(len(ids) for ids in tape_routes["routes"].values())
    if w1 > min_len:
        raise ValueError("window 越出磁带步界：%r > %d" % ((w0, w1), min_len))
    pkg = copy.deepcopy(tape_routes)      # 写时复制：输入零改动
    change_table: List[Dict[str, Any]] = []
    for rid in _route_order(pkg["routes"]):
        seq = _seq(pkg, rid)
        # ①同拍并单（无条件）：同拍同品多单并一单，落点=该拍组内最早槽。
        by_step: Dict[Tuple[int, str], List[Tuple[int, int, int]]] = {}
        for s, slot, item, qty in _sell_scan(seq, w0, w1):
            by_step.setdefault((s, item), []).append((s, slot, qty))
        for (s, item), members in sorted(by_step.items()):
            if len(members) < 2:
                continue
            members.sort(key=lambda m: (m[0], m[1]))
            _apply_group(pkg, rid, item, members, change_table,
                         "同拍并单 k=%d→1（d21-28 窗内，只提前不推后）"
                         % len(members))
        # ②跨拍批量化（目标驱动）：窗内留存 budget=目标−窗外单数（钳位）。
        seq = _seq(pkg, rid)
        lots = _sell_scan(seq, w0, w1)
        n_win = len(lots)
        n_out = _sell_count(seq) - n_win
        need = n_out + n_win - target
        if need <= 0 or n_win == 0:
            continue
        per_item: Dict[str, List[Tuple[int, int, int]]] = {}
        for s, slot, item, qty in lots:
            per_item.setdefault(item, []).append((s, slot, qty))
        n_items = len(per_item)
        budget = max(n_items, min(n_win, target - n_out))
        alloc = _allocate([(it, len(v)) for it, v in per_item.items()], budget)
        for item in sorted(per_item):
            runs = _split_runs(per_item[item], alloc[item])
            for run in runs:
                if len(run) < 2:
                    continue
                _apply_group(pkg, rid, item, run, change_table,
                             "跨拍批量化 run k=%d→1（落点=更早批次步点）"
                             % len(run))
    _rs._pool_residue_sweep(pkg)          # 无主池件归一（池闭合，池件口径沿 R15）
    _post_check(pkg, tape_routes, (w0, w1), change_table)
    _rs._check_package(pkg)
    return {"routes": pkg, "change_table": change_table}
