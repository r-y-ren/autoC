# -*- coding: utf-8 -*-
"""retape_sheep_timing（R20 L2）：磁带手术·羊时序前移。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】）：
把各路由磁带 BUY_ANIMAL SHEEP 各批步点前移至判决标定的 d11 窗，使每只羊
首产剪毛后一季刀次 ≥5（d17/20/23/26/29 型）；保持购买总量与 route 9 结构
（6牛+11羊目标）不变、订单槽位与资金序不变量（HIRE/BUY 不得挪到供资卖单
前，V57 先例）；步点参数=判决实验输出（judge_sheep_league 标定）。

静态解剖结论（2026-09-25，实跑 r34a 基座 orderbook_2965_adopt/a/main.py）：
- 磁带=_R108_DATA blob（base85(zlib(json))，字面量在 main.py 单行内）：
  {actions: 3982 条动作池, routes: 41 条路由→719 步动作池下标, shops: 64}。
  动作={farmer: 单元指令列表, hands: [单元指令列表...], market: 订单槽位列表}；
  订单形态 SELL/HIRE/BUY_SEED/BUY_PRODUCT/BUY_ANIMAL/BUY_LAND 与空槽 []。
- 引擎产毛口径（exports/probes/twin_fidelity/engine_cache/kaggriculture.py）：
  ANIMALS.SHEEP={first_yield_day:6, interval:3, max_held:6, product:WOOL}；
  日结 _daily_refresh_animals(day) 以 next_day=day+1 判
  next_day-placed_day-6 ≡0 (mod 3) 产 1 单位（CARE 银行另计）；一季=d0..d29
  （turnsPerDay=24，episodeSteps=720）。买点日 b=step//24 起潜在刀次
  = #{k≥0 : b+6+3k ≤ 29}（b=11→5 刀 d17/20/23/26/29；b=12→4 刀）。
- 剪毛 HARVEST 静态识别（链式口径）：同单元同日内，其后首个未认领
  PLACE 'WOOL'（入棚投放）回溯认领最近一次 HARVEST=一次剪毛；剪毛轮次=
  剪毛日集合（刀=剪毛 HARVEST 轮）。r34a 实测 41 路由轮次 9~13 轮全达标；
  羊买点仅 route 12/115 的 step 265 批越 d11 窗上界（step 264）一格。

手术语义定形（歧义处理决定见各段 docstring）：
- 判据（术后静态核算）：①每羊买点起潜在刀次 ≥5；②羊群剪毛轮次 ≥5；
  ③羊买点全部 ≤ window_end（缺省 264=d11 窗上界）。①②不达标即抛；
  ③残差仅当该批已「记 skip」（被不变量锁死、无可行落点）时入变更表不抛
  ——不变量高于目标判据，且契约明文「换步或记 skip」要求 skip 存活进输出。
- 移动算子（只提前不推后）：源槽订单原位换 []（cash_guard 顺延置 [] 先例，
  742943 空槽位次语义：删槽改撮合配对，故不可删/移/填既有槽位），目标步
  market 列表**尾部追加**（新下标不扰动既有锁步配对；cap=maxMarketOrders
  PerTurn=10，满则换步）；无可行步记 skip。
- 资金序不变量（V57 扩步）：供资卖单=原市场位序（步,槽）之前最近一张 SELL；
  落点 (t, 追加位) 必须 ≥ 供资卖单位序（挪到供资卖单成交前=该步现金更紧
  的因果洞→换步或记 skip）。
- 剪毛轮次 <5 时剪毛 HARVEST 轮对齐五轮型（17/20/23/26/29）：只提前不推后、
  只改动物格 HARVEST 指令不动市场单；落点单元指令须为 ['PASS']（不覆盖
  别的指令）；跟随的 PICKUP/PLACE 配套不随行→change_table 标注断链风险。

编解码私有助手（leading-underscore 内部件，供 retape_tail_savings/build_r37
复用）：_decode_routes(main_text) → 磁带路由包 {actions, routes, shops}（=
_R108_DATA 原形）；_encode_routes(main_text, routes) → 手术后 main 文本。
编码参数与原 blob 逐字节同构（json separators=(",",":") ensure_ascii=False +
zlib level 9 + base85；r34a 实测无编辑往返逐字节恒等）。自检链随编码器
（R15 三件套+确定性双跑，任一不过即抛 RuntimeError）：①blob 区间外逐字节
一致；②解码回路一致（decode(encode(x))==x）；③compile() 可编译；④确定性
双跑（同输入两次编码逐字节一致）。
"""
from __future__ import annotations

import copy
import re
from typing import Any, Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# 可配置步点参数（判决实验输出 judge_sheep_league 标定，B20）；缺省值=
# 满足判据原位/最早可行位语义（见模块 docstring 手术段）。
# ---------------------------------------------------------------------------
TARGET_WINDOW: Dict[str, Any] = {
    "window_end": 264,          # d11 窗上界（d11*24；买点须 ≤ 此步）
    "target_step": None,        # 判决标定的精确目标步；None=缺省（最早可行位）
    "min_cuts": 5,              # 每羊买点起一季潜在刀次下限
    "min_rounds": 5,            # 羊群剪毛轮次下限
    "shear_round_days": (17, 20, 23, 26, 29),   # 五轮型（d11 买点节奏）
    "first_yield_day": 6,       # SHEEP 首产（引擎 ANIMALS）
    "interval": 3,              # SHEEP 产距（引擎 ANIMALS）
    "last_day": 29,             # 一季末日（episodeSteps 720 / turnsPerDay 24）
}

#: 每步市场单槽上限（引擎 maxMarketOrdersPerTurn=10，超出静默丢）。
MARKET_SLOTS = 10

_BLOB_RE = re.compile(
    r"_R108_DATA=json\.loads\(zlib\.decompress\(base64\.b85decode\('([^']+)'\)\)\)")


# ---------------------------------------------------------------------------
# 刀次核算（引擎产毛节奏；买点日 b=step//24，产毛日 b+6+3k ≤ last_day）
# ---------------------------------------------------------------------------
def _potential_shears(buy_step: int, window: Optional[Dict[str, Any]] = None) -> int:
    """买点起一季潜在刀次 = #{k≥0 : b+first+interval*k ≤ last_day}。

    构造用例口径（契约锁定）：d11 买点（b=11）=5 刀（d17/20/23/26/29 型）、
    d12 买点（b=12）=4 刀不达标。b=step//24（引擎 day=step//turnsPerDay）。
    """
    w = TARGET_WINDOW if window is None else window
    day = int(buy_step) // 24
    first = int(w["first_yield_day"])
    interval = int(w["interval"])
    last = int(w["last_day"])
    if interval <= 0:
        raise ValueError("interval must be positive")
    n = 0
    k = 0
    while True:
        d = day + first + interval * k
        if d > last:
            return n
        n += 1
        k += 1


def _sheep_batches(seq: List[Dict[str, Any]]) -> List[Tuple[int, int, int]]:
    """路由磁带 → 羊批清单 [(step, slot, qty)]（BUY_ANIMAL SHEEP 市场单）。"""
    out = []
    for s, a in enumerate(seq):
        for j, o in enumerate(a.get("market") or []):
            if isinstance(o, list) and o and o[0] == "BUY_ANIMAL" and o[1] == "SHEEP":
                out.append((s, j, int(o[2]) if len(o) > 2 else 1))
    return out


def _animal_totals(seq: List[Dict[str, Any]]) -> Dict[str, int]:
    """路由磁带 → 畜购买总量 {SHEEP/COW/GOOSE: qty}（不变量核算用）。"""
    tot: Dict[str, int] = {}
    for a in seq:
        for o in a.get("market") or []:
            if isinstance(o, list) and o and o[0] == "BUY_ANIMAL":
                tot[o[1]] = tot.get(o[1], 0) + (int(o[2]) if len(o) > 2 else 1)
    return tot


# ---------------------------------------------------------------------------
# 剪毛 HARVEST 静态识别（链式口径：同单元同日 HARVEST→PLACE 'WOOL' 认领）
# ---------------------------------------------------------------------------
def _units(a: Dict[str, Any]):
    """动作 → [(unit_id, 指令)]；unit_id='F'（farmer）或 'hN'（hands 下标）。"""
    fu = a.get("farmer")
    if isinstance(fu, list) and fu and isinstance(fu[0], str):
        yield "F", fu
    for i, h in enumerate(a.get("hands") or []):
        if isinstance(h, list) and h and isinstance(h[0], str):
            yield "h%d" % i, h


def _shear_events(seq: List[Dict[str, Any]]) -> List[Tuple[int, str]]:
    """链式剪毛事件 [(step, unit)]：PLACE 'WOOL' 同单元同日回溯认领 HARVEST。

    口径：单元库存里的 WOOL 只能来自其自身 HARVEST（PICKUP WOOL 为棚→身
    反向流，r34a 各路由实测为零）；认领=最近未认领 HARVEST，逐 PLACE 一认。
    确定性：步升序、单元序稳定，同输入同输出。
    """
    claimed = set()
    out: List[Tuple[int, str]] = []
    for s, a in enumerate(seq):
        for u, op in _units(a):
            if not (isinstance(op, list) and len(op) > 1 and op[0] == "PLACE"
                    and op[1] == "WOOL"):
                continue
            for h in range(s - 1, (s // 24) * 24 - 1, -1):
                if (h, u) in claimed:
                    break
                hop = dict(_units(seq[h])).get(u)
                if isinstance(hop, list) and hop and hop[0] == "HARVEST":
                    claimed.add((h, u))
                    out.append((h, u))
                    break
    return out


def _shear_rounds(seq: List[Dict[str, Any]]) -> List[int]:
    """剪毛轮次清单（升序去重日；刀=剪毛 HARVEST 轮）。"""
    return sorted({h // 24 for h, _ in _shear_events(seq)})


# ---------------------------------------------------------------------------
# 磁带路由包编解码（R15 自检链；leading-underscore 内部件，不入函数大表）
# ---------------------------------------------------------------------------
def _decode_routes(main_text: str) -> Dict[str, Any]:
    """r34a main 文本 → 磁带路由包 {actions, routes, shops}（=解码 _R108_DATA）。

    span 定位 blob 字面量（引号内）；编码参数与原 blob 逐字节同构（实测
    r34a 无编辑往返恒等）。形态校验 fail-closed。
    """
    import base64
    import json
    import zlib
    if not isinstance(main_text, str):
        raise TypeError("main_text must be str, got %s" % type(main_text).__name__)
    m = _BLOB_RE.search(main_text)
    if not m:
        raise ValueError("main_text 无 _R108_DATA blob")
    try:
        data = json.loads(zlib.decompress(base64.b85decode(m.group(1))))
    except Exception as exc:
        raise ValueError("_R108_DATA blob 解码失败: %r" % exc) from exc
    _check_package(data)
    return data


def _check_package(data: Any) -> None:
    """磁带路由包形态校验（fail-closed）。"""
    if not isinstance(data, dict):
        raise ValueError("磁带路由包须为 dict，得到 %s" % type(data).__name__)
    for key in ("actions", "routes", "shops"):
        if key not in data:
            raise ValueError("磁带路由包缺键 %r" % key)
    if not isinstance(data["actions"], list) or not data["actions"]:
        raise ValueError("actions 须为非空 list")
    for i, a in enumerate(data["actions"]):
        if not isinstance(a, dict) or not isinstance(a.get("market"), list):
            raise ValueError("actions[%d] 须为含 market list 的 dict" % i)
    if not isinstance(data["routes"], dict) or not data["routes"]:
        raise ValueError("routes 须为非空 dict")
    n = len(data["actions"])
    for k, ids in data["routes"].items():
        if not isinstance(ids, list) or not ids:
            raise ValueError("routes[%r] 须为非空 list" % k)
        for i in ids:
            if not isinstance(i, int) or not 0 <= i < n:
                raise ValueError("routes[%r] 含非法动作下标 %r" % (k, i))
    if not isinstance(data["shops"], list):
        raise ValueError("shops 须为 list")


def _encode_routes(main_text: str, routes: Dict[str, Any]) -> str:
    """手术后路由包 → main 文本（blob 内替换，R15 自检链，任一不过即抛）。

    自检链（校验N红 定罪位）：①blob 区间外逐字节一致（前缀/后缀 utf-8 字节
    恒等）；②解码回路一致（_decode_routes(新文本)==routes 深等）；③compile()
    内存编译新文本；④确定性双跑（再次编码逐字节一致）。
    """
    import base64
    import json
    import zlib
    if not isinstance(main_text, str):
        raise TypeError("main_text must be str, got %s" % type(main_text).__name__)
    _check_package(routes)
    m = _BLOB_RE.search(main_text)
    if not m:
        raise ValueError("main_text 无 _R108_DATA blob")
    lo, hi = m.span(1)
    raw = json.dumps(routes, separators=(",", ":"), ensure_ascii=False)
    body = base64.b85encode(zlib.compress(raw.encode("utf-8"), 9)).decode("ascii")
    new_text = main_text[:lo] + body + main_text[hi:]

    # 自检①：blob 区间外逐字节一致
    pre_old = main_text[:lo].encode("utf-8")
    pre_new = new_text[:lo].encode("utf-8")
    suf_old = main_text[hi:].encode("utf-8")
    suf_new = new_text[lo + len(body):].encode("utf-8")
    if pre_old != pre_new or suf_old != suf_new:
        raise RuntimeError("自检①红：手术泄漏到 blob 区间外（前后缀不逐字节一致）")

    # 自检②：解码回路一致
    if _decode_routes(new_text) != routes:
        raise RuntimeError("自检②红：解码回路不一致（decode(encode(x)) != x）")

    # 自检③：可编译
    try:
        compile(new_text, "<_encode_routes>", "exec")
    except Exception as exc:
        raise RuntimeError("自检③红：新 main 文本 compile() 未通过: %r" % exc) from exc

    # 自检④：确定性双跑
    raw2 = json.dumps(routes, separators=(",", ":"), ensure_ascii=False)
    body2 = base64.b85encode(zlib.compress(raw2.encode("utf-8"), 9)).decode("ascii")
    if body2 != body:
        raise RuntimeError("自检④红：确定性双跑不一致（同输入两次编码不同）")
    return new_text


# ---------------------------------------------------------------------------
# 手术内部件
# ---------------------------------------------------------------------------
def _funding_sell(seq: List[Dict[str, Any]], step: int, slot: int
                  ) -> Optional[Tuple[int, int]]:
    """供资卖单位序（V57）：市场位序（步,槽）严格早于 (step,slot) 的最近 SELL。"""
    for t in range(step, -1, -1):
        mkt = seq[t].get("market") or []
        hi = (slot - 1) if t == step else (len(mkt) - 1)
        for j in range(hi, -1, -1):
            o = mkt[j]
            if isinstance(o, list) and o and o[0] == "SELL":
                return t, j
    return None


def _pick_target(seq: List[Dict[str, Any]], from_step: int,
                 fund: Optional[Tuple[int, int]],
                 window: Dict[str, Any]) -> Optional[int]:
    """落点步（只提前不推后）：缺省=窗内最早可行步；target_step 标定优先。

    可行=t≤window_end 且 t<from_step 且该步订单数 < MARKET_SLOTS（尾部追加
    不扰动既有锁步配对）且追加位序 ≥ 供资卖单位序（资金序不变量）。
    """
    end = min(int(window["window_end"]), from_step - 1)
    order: List[int] = []
    ts = window.get("target_step")
    if ts is not None:
        ts = int(ts)
        if ts <= end:
            order.append(ts)
    order.extend(t for t in range(0, end + 1) if t != (ts if ts is not None else -1))

    def _feasible(t: int) -> bool:
        if t < 0 or t > end:
            return False
        mkt = seq[t].get("market") or []
        if len(mkt) >= MARKET_SLOTS:
            return False
        if fund is not None and (t, len(mkt)) < fund:
            return False
        return True

    for t in order:
        if _feasible(t):
            return t
    return None


def _cow_action(pkg: Dict[str, Any], rid: str, step: int) -> Tuple[List[int], int, Dict[str, Any]]:
    """(rid, step) → 写时复制准备：(路由下标表, 步动作池下标, 步动作深拷贝)。"""
    idxs = pkg["routes"][rid]
    idx = idxs[step]
    return idxs, idx, copy.deepcopy(pkg["actions"][idx])


def _commit_action(pkg: Dict[str, Any], idxs: List[int], step: int,
                   action: Dict[str, Any]) -> None:
    """深拷贝动作入池（append），路由下标指针改指新件（池内共享件零扰动）。"""
    pkg["actions"].append(action)
    idxs[step] = len(pkg["actions"]) - 1


def _align_shear_rounds(pkg: Dict[str, Any], rid: str,
                        window: Dict[str, Any],
                        change_table: List[Dict[str, Any]]) -> None:
    """剪毛轮次 <5 时对齐五轮型（只提前；只动动物格 HARVEST；挪 HARVEST
    不动市场单，跟随的 PICKUP/PLACE 配套不随行→reason 标注断链风险）。

    拆并轮机制：同日多剪把一轮并成一轮；将其一 HARVEST 提到空缺的更早
    五轮型日（目标单元指令须 ['PASS'] 不覆盖别的指令）即拆出新轮。
    """
    idxs = pkg["routes"][rid]
    days = tuple(int(d) for d in window["shear_round_days"])
    min_rounds = int(window["min_rounds"])
    guard = 0
    while True:
        guard += 1
        if guard > 64:
            break
        seq = [pkg["actions"][i] for i in idxs]
        events = _shear_events(seq)
        rounds = sorted({h // 24 for h, _ in events})
        if len(rounds) >= min_rounds:
            break
        by_day: Dict[int, List[Tuple[int, str]]] = {}
        for h, u in events:
            by_day.setdefault(h // 24, []).append((h, u))
        moved = False
        # 拆并轮优先（同日多剪），其次挪离型轮；目标=空缺的更早五轮型日。
        candidates = sorted(by_day.items(), key=lambda kv: (-len(kv[1]), kv[0]))
        for day, evs in candidates:
            targets = [d for d in days if d < day and d not in rounds]
            if not targets:
                continue
            tday = max(targets)
            for h, u in sorted(evs):
                tstep = tday * 24 + (h % 24)
                if tstep >= len(idxs):
                    continue
                _, _, act = _cow_action(pkg, rid, tstep)
                cur = dict(_units(act)).get(u)
                if cur != ["PASS"]:
                    continue     # 落点单元有别的指令：不覆盖（一切指令不动）
                _, _, src = _cow_action(pkg, rid, h)
                _set_unit(src, u, ["PASS"])
                _commit_action(pkg, idxs, h, src)
                _set_unit(act, u, ["HARVEST"])
                _commit_action(pkg, idxs, tstep, act)
                change_table.append({
                    "route": rid, "kind": "harvest_move",
                    "from_step": h, "to_step": tstep, "item": "WOOL", "qty": 1,
                    "reason": ("shear_round_align d%d->d%d unit=%s（只提前；"
                               "跟随的 PICKUP/PLACE 配套不随行，断链风险待"
                               "judge_sheep_league 实证）" % (day, tday, u)),
                })
                moved = True
                break
            if moved:
                break
        if not moved:
            break


def _set_unit(action: Dict[str, Any], u: str, op: List[str]) -> None:
    """动作内单元指令改写（u='F' 或 'hN'）。"""
    if u == "F":
        action["farmer"] = list(op)
        return
    i = int(u[1:])
    hands = action.setdefault("hands", [])
    while len(hands) <= i:
        hands.append(["PASS"])
    hands[i] = list(op)


# ---------------------------------------------------------------------------
# 主契约函数
# ---------------------------------------------------------------------------
def retape_sheep_timing(tape_routes: Dict[str, Any]) -> Dict[str, Any]:
    """羊购买步点前移手术+静态刀次核算。

    签名意图：输入: 磁带路由表 / 输出: {routes, change_table}（手术后磁带+
    步点变更表） / 错误: 手术后静态刀次核算不达标即抛。

    输入形态（=_decode_routes 产物，磁带路由包）：
    {"actions": [动作...], "routes": {路由id: [动作池下标×719]}, "shops": [...]}；
    动作={"farmer": 单元指令, "hands": [单元指令...], "market": 订单槽位列表}。
    输出 {"routes": 手术后同形路由包（写时复制，输入零改动）, "change_table":
    逐变更行 {route, kind, from_step, to_step, item, qty, reason}}；kind∈
    {buy_move, harvest_move, no-op, skip}，达标批记 no-op、被不变量锁死批记
    skip（存活进输出供审计，见模块 docstring 歧义处理）。

    步点参数=TARGET_WINDOW（可配置；B20 judge_sheep_league 标定 target_step）。
    不变量（术后核算，破即抛）：羊/牛/鹅购买总量逐路由不变；订单槽位数
    （订单计数）守恒——移动=源槽换 [] + 目标步市场列表尾部追加（742943 空槽
    位次语义：既有槽位含故意空槽不删不移不填，删槽/填槽改撮合配对；尾部新
    下标不扰动既有锁步配对）；资金序不变量——BUY 不得挪到供资卖单成交前。

    错误：①每羊潜在刀次 <5、②羊群剪毛轮次 <5 → RuntimeError（刀次核算不
    达标，无论是否 skip）；③买点越窗 → RuntimeError 除非该批已记 skip（被
    不变量锁死，契约明文「换步或记 skip」）；不变量破 → RuntimeError。
    """
    # ---- 0. 输入预检（fail-closed）----
    if not isinstance(tape_routes, dict):
        raise TypeError("tape_routes must be dict, got %s"
                        % type(tape_routes).__name__)
    _check_package(tape_routes)
    window = dict(TARGET_WINDOW)
    pkg = copy.deepcopy(tape_routes)      # 输入零改动（写时复制手术）
    change_table: List[Dict[str, Any]] = []

    # 术前留底（不变量核算基线；按路由逐步计，池级共享件不入账）
    totals_before = {rid: _animal_totals([pkg["actions"][i] for i in ids])
                     for rid, ids in pkg["routes"].items()}
    market_before = {rid: [list(pkg["actions"][i].get("market") or []) for i in ids]
                     for rid, ids in pkg["routes"].items()}

    # ---- 1. 羊批步点手术（只提前不推后）----
    skip_keys = set()
    moves: List[Tuple[str, int, int, int, int]] = []   # (rid, from, slot, to, qty)
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        batches = _sheep_batches([pkg["actions"][i] for i in idxs])
        for step, slot, qty in batches:
            seq = [pkg["actions"][i] for i in idxs]   # 每批重取（防陈旧视图）
            cuts = _potential_shears(step, window)
            compliant = (step <= int(window["window_end"])
                         and cuts >= int(window["min_cuts"]))
            if compliant:
                change_table.append({
                    "route": rid, "kind": "no-op", "from_step": step,
                    "to_step": step, "item": "SHEEP", "qty": qty,
                    "reason": ("compliant: step<=window_end(%d) and "
                               "potential_cuts=%d>=%d"
                               % (int(window["window_end"]), cuts,
                                  int(window["min_cuts"]))),
                })
                continue
            fund = _funding_sell(seq, step, slot)
            target = _pick_target(seq, step, fund, window)
            if target is None:
                change_table.append({
                    "route": rid, "kind": "skip", "from_step": step,
                    "to_step": step, "item": "SHEEP", "qty": qty,
                    "reason": ("no feasible earlier step: window_end=%d "
                               "funding_sell=%s（资金序不变量/槽位上限锁死，"
                               "换步无果记 skip）"
                               % (int(window["window_end"]),
                                  ("%d,%d" % fund) if fund else "none")),
                })
                skip_keys.add((rid, step, slot))
                continue
            # 手术：源槽换 []（cash_guard 顺延置 [] 先例）+ 目标步尾部追加
            idxs_s, _, src = _cow_action(pkg, rid, step)
            mkt = src["market"]
            mkt[slot] = []
            _commit_action(pkg, idxs_s, step, src)
            idxs_t, _, tgt = _cow_action(pkg, rid, target)
            tgt["market"].append(["BUY_ANIMAL", "SHEEP", qty])
            _commit_action(pkg, idxs_t, target, tgt)
            moves.append((rid, step, slot, target, qty))
            change_table.append({
                "route": rid, "kind": "buy_move", "from_step": step,
                "to_step": target, "item": "SHEEP", "qty": qty,
                "reason": ("d11 window retape: cuts=%d window_end=%d "
                           "funding_sell=%s（只提前；源槽换 [] 尾部追加，"
                           "订单槽位数守恒+空槽位次语义不变）"
                           % (cuts, int(window["window_end"]),
                              ("%d,%d" % fund) if fund else "none")),
            })

    # ---- 2. 剪毛轮次对齐（<5 才动；只提前；只动动物格 HARVEST）----
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [pkg["actions"][i] for i in idxs]
        if len(_shear_rounds(seq)) < int(window["min_rounds"]):
            _align_shear_rounds(pkg, rid, window, change_table)

    # ---- 3. 不变量核算（破即抛；逐步对照术前基线）----
    totals_after = {rid: _animal_totals([pkg["actions"][i] for i in ids])
                    for rid, ids in pkg["routes"].items()}
    if totals_after != totals_before:
        raise RuntimeError("不变量红：购买总量被改动 %r -> %r"
                           % (totals_before, totals_after))
    out_slots = {(r, s, j) for r, s, j, _, _ in moves}
    in_slots: Dict[Tuple[str, int], List[List[Any]]] = {}
    for r, s, j, t, q in moves:
        in_slots.setdefault((r, t), []).append(["BUY_ANIMAL", "SHEEP", q])
    for rid, ids in pkg["routes"].items():
        base = market_before[rid]
        for s, i in enumerate(ids):
            old_m = base[s]
            new_m = pkg["actions"][i].get("market") or []
            appended = in_slots.get((rid, s), [])
            if len(new_m) != len(old_m) + len(appended):
                raise RuntimeError("不变量红：订单槽位数不守恒 %s@%d %d->%d"
                                   % (rid, s, len(old_m), len(new_m)))
            for j, o in enumerate(old_m):
                cur = new_m[j] if j < len(new_m) else None
                if (rid, s, j) in out_slots:
                    if cur != []:
                        raise RuntimeError("不变量红：移出槽未留 [] 占位 %s@%d slot%d"
                                           % (rid, s, j))
                elif isinstance(o, list) and o:
                    if cur != o:
                        raise RuntimeError("不变量红：既有订单槽位被改/移 %s@%d slot%d"
                                           % (rid, s, j))
                else:
                    if cur != o:
                        raise RuntimeError("不变量红：空槽位次被删/移/填 %s@%d slot%d"
                                           % (rid, s, j))
            if list(new_m[len(old_m):]) != appended:
                raise RuntimeError("不变量红：尾部追加单与移动单不匹配 %s@%d"
                                   % (rid, s))

    # ---- 4. 术后静态刀次核算（①②必抛；③仅 skip 残差豁免）----
    problems = []
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [pkg["actions"][i] for i in idxs]
        for step, slot, qty in _sheep_batches(seq):
            cuts = _potential_shears(step, window)
            if cuts < int(window["min_cuts"]):
                problems.append("①刀次红：%s 羊批 step=%d 潜在刀次=%d<%d"
                                % (rid, step, cuts, int(window["min_cuts"])))
            if step > int(window["window_end"]) and (rid, step, slot) not in skip_keys:
                problems.append("③窗界红：%s 羊批 step=%d>window_end=%d 且未记 skip"
                                % (rid, step, int(window["window_end"])))
        rounds = _shear_rounds(seq)
        if len(rounds) < int(window["min_rounds"]):
            problems.append("②轮次红：%s 剪毛轮次=%s<%d 轮"
                            % (rid, rounds, int(window["min_rounds"])))
    if problems:
        raise RuntimeError("手术后静态刀次核算不达标：%s；change_table=%r"
                           % ("；".join(problems), change_table))

    return {"routes": pkg, "change_table": change_table}


# ---------------------------------------------------------------------------
# 静态解剖（一次性产物生成件；测试只断言可复算）
# ---------------------------------------------------------------------------
def _dissection_snapshot(main_text: str, source: str) -> Dict[str, Any]:
    """真 r34a 磁带解剖快照：各路由羊买点+剪毛轮次清单（确定性、可复算）。"""
    import hashlib
    pkg = _decode_routes(main_text)
    window = dict(TARGET_WINDOW)
    routes_out: Dict[str, Any] = {}
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [pkg["actions"][i] for i in idxs]
        events = _shear_events(seq)
        rounds = sorted({h // 24 for h, _ in events})
        batches = []
        for step, slot, qty in _sheep_batches(seq):
            day = step // 24
            rhythm = []
            k = 0
            while True:
                d = day + int(window["first_yield_day"]) + int(window["interval"]) * k
                if d > int(window["last_day"]):
                    break
                rhythm.append(d)
                k += 1
            batches.append({
                "from_step": step, "slot": slot, "qty": qty, "day": day,
                "potential_cuts": _potential_shears(step, window),
                "rhythm_days": rhythm,
                "scheduled_cuts": len([d for d in rhythm if d in rounds]),
            })
        routes_out[rid] = {
            "sheep_batches": batches,
            "sheep_total": sum(b["qty"] for b in batches),
            "animal_totals": _animal_totals(seq),
            "shear_steps": [h for h, _ in events],
            "shear_rounds": rounds,
        }
    return {
        "source": source,
        "source_sha256": hashlib.sha256(main_text.encode("utf-8")).hexdigest(),
        "generated_by": "orderbook_r37/retape_sheep.py::_dissection_snapshot",
        "engine_basis": {
            "animal": "SHEEP",
            "first_yield_day": window["first_yield_day"],
            "interval": window["interval"],
            "last_day": window["last_day"],
            "turns_per_day": 24,
            "window_end": window["window_end"],
            "shear_round_days": list(window["shear_round_days"]),
            "cuts_formula": "#{k>=0: buy_day+6+3k <= 29}",
            "shear_id": "same-unit same-day HARVEST linked to later PLACE WOOL",
        },
        "routes": routes_out,
    }
