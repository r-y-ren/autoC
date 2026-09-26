# -*- coding: utf-8 -*-
"""retape_cash_reserve（R19/R20 L2·2026-09-26 快速通道结构性增补）：磁带手术·d0 现金留存。

责任契约（fn_docs/hybrid/responsibility.md【R19/R20 增补】retape_cash_reserve）：
把 d0 窗（step 0-23）内一笔**非紧迫种子买点**（其依赖消费[PICKUP/PLANT 供种链]
在足够后方者）的 BUY_SEED 步点后移到其依赖消费之前最近可行位，使 d0 日终
现金 ≥5（考古实证过夜 4-5 金即可满编 d1 三手+首日喂养）；**计划自洽不变量**：
移后买点仍先于其供种消费（种子到达不晚于 PICKUP/PLANT 需要），PICKUP/PLANT/
收成链不移不动、后移不越种植截止线（step 624）；无可行候选（依赖消费过近/
窗内无种子单）→零改动记 no-op 并留档，交运行时守卫兜底。输出变更表
（kind=cash_reserve_buy_move）。错误：移后买点晚于依赖消费（断供种链）或
越种植截止线即抛。

供种链判定（用户裁决口径·保守优先）：
- 某 BUY_SEED 的「依赖消费」= 其后该作物种子被 PICKUP 或 PLANT 消费的最早拍
  （保守：取该作物**后续首次 PICKUP/PLANT 拍**；拿不准[找不到消费拍/形态
  不识]→视为紧迫不可移，试下一笔）。种子在引擎内为易耗通用品
  （private["seeds"]，PLANT 直接扣、buy→plant 一步到胃），故「最早拍」即该
  买点的真实供种消费——保守取最早拍=绝不拆链（宁可不挪）。
- 非紧迫=可挪动：存在落点 t 使 24 ≤ t < 依赖消费拍（种子在消费拍前到达：
  单元动作先于市场结算（kaggriculture interpreter 逐拍复核），t 拍市场结算
  的种子 t+1 拍才可用 → t 严格小于消费拍）、t ≤ 624（种植截止线=仍种得活）
  且 t 落「同日或前一日」（消费拍所在日或其前一日）内可行（market 槽 <10，
  尾部追加不扰动既有锁步配对）。依赖消费拍 ≤24（d0 窗内）即「消费过近」→
  该买点紧迫不可移。

手术算子（沿 retape_sheep_timing 移动算子）：源槽订单原位换 []（cash_guard
顺延置 [] 先例；742943 空槽位次语义：不删/不移/不填既有槽位），目标步 market
列表尾部追加（新下标不扰动既有锁步配对；cap=maxMarketOrdersPerTurn=10，
满则换步/记不可行）。PICKUP/PLANT/收成链零改动（只动 market 单）。

候选优先级（用户裁决）：窗内种子单中取「依赖消费最靠后」的那笔（挪动余量
最大）；MELON 优先（80 金/粒，挪一颗即足额）。逐笔挪动直至推算 d0 日终 ≥5
或候选耗尽；每笔一行变更表。

d0 日终现金核算（沿守卫投影口径·retape 侧静态近似·保守偏严）：
- money 起点 3000（引擎 startingMoney）；d0 逐拍按 market 槽位序 walk——
  HIRE→cash -= fib(当日序)（引擎 _do_hire 口径 1,1,2,3,5…）；BUY_SEED→
  CROPS.seed 精确扣减；BUY_ANIMAL→ANIMALS.cost 精确扣减；BUY_PRODUCT/
  BUY_LAND→引擎 base/地价静态近似扣减（「d0 各拍购买扣减」）；SELL→
  qty×base 静态近似计入（「卖单收入计入」）。
- 保守偏严=买价从高不折（base 不打折）、卖单收入从低取整（向下取整）、
  判据 d0 日终 ≥5 无容差。静态近似不捕捉动态价差（实测对敲 slippage ~20-30
  金），故该口径为「近似即可」的判据面而非精算面。
- 判据=移后计划推算 d0 日终 ≥5（达线即停）；未达线但候选耗尽=尽力留档
  （行内 reason 记推算值），不抛（错误面只限断供种链/越截止线）。

输出 {"routes": 手术后磁带路由包（写时复制，输入零改动）, "change_table":
逐变更行 {route, kind, from_step, to_step, item, qty, reason}}；kind∈
{cash_reserve_buy_move, no-op}——零改动路由记 no-op（from_step=to_step=0、
item=None、qty=0，reason 记候选判定与推算现金），存活进输出供审计。

编解码/手术底座复用 retape_sheep 内部件（_decode_routes/_encode_routes/
_check_package/_cow_action/_commit_action/_units）；retape_cash_reserve
首参与返回形态见函数 docstring。
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Optional, Tuple

try:
    from orderbook_r37 import retape_sheep as _rs
except ImportError:                      # 脚本态兜底（retape_tail 同款）
    import retape_sheep as _rs           # type: ignore

# ---------------------------------------------------------------------------
# 常数（引擎 kaggriculture 实读：CROPS/ANIMALS/MARKET_PARAMS/LAND_PRICES、
# turnsPerDay=24、episodeSteps=720、startingMoney=3000、maxMarketOrders
# PerTurn=10；种植截止线 624=EXP402/layer S 同源，guard 回填种活时限同值）
# ---------------------------------------------------------------------------
TURNS_PER_DAY = 24
D0_WINDOW_END = 23                      # d0 窗 = step 0..23
D0_CASH_FLOOR = 5.0                     # d0 日终现金下限（考古实证 4-5 金）
START_MONEY = 3000.0                    # 引擎 startingMoney
PLANTING_DEADLINE = 624                 # 种植截止线（后移上限=仍种得活）
MARKET_SLOTS = 10                       # 引擎 maxMarketOrdersPerTurn

SEED_PRICE = {"WHEAT": 10, "CARROT": 20, "TOMATO": 50,
              "STRAWBERRY": 100, "MELON": 80}
ANIMAL_COST = {"GOOSE": 300, "COW": 400, "SHEEP": 500}
PRODUCT_BASE = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
                "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
                "FERTILIZER": 100}
LAND_PRICES = (1000, 2000, 4000)


def _hire_cost(n: int) -> int:
    """当日第 n 张 HIRE 价（引擎 _do_hire：mult×fib(n)，fib(0)=1,1,2,3,5…）。"""
    a, b = 1, 1
    for _ in range(int(n)):
        a, b = b, a + b
    return a


# ---------------------------------------------------------------------------
# d0 现金投影（沿守卫投影口径·静态近似·保守偏严）
# ---------------------------------------------------------------------------
def _order_cost(o: Any) -> Optional[Tuple[str, float]]:
    """市场单 → (op, 金额)：HIRE/BUY_* 记支出负额、SELL 记收入正额；不识别 None。"""
    if not (isinstance(o, (list, tuple)) and o and isinstance(o[0], str)):
        return None
    op = o[0]
    if op == "HIRE":
        return ("HIRE", -1.0)            # 金额按 walk 内当日序 fib 结算
    if op in ("BUY_SEED", "BUY_PRODUCT", "BUY_ANIMAL", "SELL"):
        if len(o) < 3 or not isinstance(o[1], str):
            return None
        try:
            qty = int(o[2])
        except (TypeError, ValueError):
            return None
        if isinstance(o[2], bool) or qty <= 0:
            return None
        item = o[1]
        if op == "BUY_SEED":
            if item not in SEED_PRICE:
                return None
            return ("BUY_SEED", -float(int(SEED_PRICE[item] * qty)))
        if op == "BUY_ANIMAL":
            if item not in ANIMAL_COST:
                return None
            return ("BUY_ANIMAL", -float(int(ANIMAL_COST[item] * qty)))
        if op == "BUY_PRODUCT":
            if item not in PRODUCT_BASE:
                return None
            # 保守偏严：买价 base 从高（不打折），浮点向上取整语义=金额取整不减
            return ("BUY_PRODUCT", -float(int(PRODUCT_BASE[item] * qty)))
        # SELL：卖单收入计入（静态近似 base 价），保守偏严=收入从低向下取整
        if item not in PRODUCT_BASE:
            return None
        return ("SELL", float(int(PRODUCT_BASE[item] * qty)))
    if op == "BUY_LAND":
        try:
            qty = int(o[2]) if len(o) > 2 else 1
        except (TypeError, ValueError):
            qty = 1
        if isinstance(o[2] if len(o) > 2 else 1, bool) or qty <= 0:
            return None
        return ("BUY_LAND", -float(int(LAND_PRICES[0] * qty)))
    return None


def _project_d0_end(seq: List[Dict[str, Any]]) -> float:
    """路由磁带 → 推算 d0 日终现金（step 0..23 全部市场单 walk，静态近似）。

    口径：money 起点 3000；逐拍按 market 槽位序（lockstep 结算序）扣购买/
    计卖单收入；HIRE 价=当日 fib 序（_hire_cost）。形态不识的槽位零影响
    （守卫投影 entry=None 同款）。返回 float（保守偏严后仍可能高于实测，
    见模块 docstring）。
    """
    cash = START_MONEY
    hires_today = 0
    end = min(int(D0_WINDOW_END), len(seq) - 1)
    for s in range(0, end + 1):
        for o in (seq[s].get("market") or []):
            got = _order_cost(o)
            if got is None:
                continue
            op, amount = got
            if op == "HIRE":
                cash -= _hire_cost(hires_today)
                hires_today += 1
            else:
                cash += amount
    return cash


# ---------------------------------------------------------------------------
# 供种链判定 + 落点
# ---------------------------------------------------------------------------
def _first_consumption(seq: List[Dict[str, Any]], crop: str,
                       after_step: int) -> Optional[int]:
    """crop 在 after_step 之后的首个 PICKUP/PLANT 消费拍（保守最早拍）。

    单元指令形态 ["PICKUP", crop, …] / ["PLANT", crop] 记消费；找不到/形态
    不识→None（调用方按「拿不准=紧迫」处置）。确定性：步升序、单元序稳定。
    """
    for s in range(after_step + 1, len(seq)):
        for _u, op in _rs._units(seq[s]):
            if (isinstance(op, list) and len(op) > 1 and op[0] in ("PICKUP",
                                                                  "PLANT")
                    and op[1] == crop):
                return s
    return None


def _pick_landing(seq: List[Dict[str, Any]], from_step: int,
                  consumption: int) -> Optional[int]:
    """落点步：依赖消费前最近可行拍（同日或前一日；≤624；>from_step；槽<10）。

    「最近可行」=自消费拍-1 递减搜索取首个可行拍；范围限消费拍所在日或
    其前一日（用户口径「同日或前一日」）且 ≥24（挪出 d0 窗才有现金留存
    效应——落点仍在 d0 内则日终现金不变，核算判据自会挡下）。可行=该步
    market 槽数 < MARKET_SLOTS（尾部追加不扰动既有锁步配对）。无→None。
    """
    c = int(consumption)
    day_start = (c // TURNS_PER_DAY) * TURNS_PER_DAY
    lo = max(day_start - TURNS_PER_DAY, TURNS_PER_DAY, from_step + 1)
    hi = min(c - 1, PLANTING_DEADLINE)
    for t in range(hi, lo - 1, -1):
        mkt = seq[t].get("market") or []
        if len(mkt) < MARKET_SLOTS:
            return t
    return None


def _candidate_rows(seq: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """d0 窗种子单 → 候选清单（含依赖消费拍与可挪判定），优先级已排。"""
    out: List[Dict[str, Any]] = []
    for s in range(0, min(D0_WINDOW_END, len(seq) - 1) + 1):
        for j, o in enumerate(seq[s].get("market") or []):
            if not (isinstance(o, list) and len(o) >= 3 and o[0] == "BUY_SEED"
                    and isinstance(o[1], str)):
                continue
            try:
                qty = int(o[2])
            except (TypeError, ValueError):
                continue
            if isinstance(o[2], bool) or qty <= 0:
                continue
            crop = o[1]
            cons = _first_consumption(seq, crop, s)
            # 非紧迫判定（保守）：消费拍存在且严格晚于 d0 窗（≥25）才可挪；
            # 找不到消费拍=拿不准→紧迫不可移（fail-safe 不拆链）。
            movable = cons is not None and cons > D0_WINDOW_END + 1
            out.append({"from_step": s, "slot": j, "item": crop, "qty": qty,
                        "consumption": cons, "movable": movable})
    out.sort(key=lambda r: (0 if r["item"] == "MELON" else 1,
                            -(r["consumption"] or -1), -r["from_step"],
                            -r["qty"], r["slot"]))
    return out


# ---------------------------------------------------------------------------
# 主契约函数
# ---------------------------------------------------------------------------
def retape_cash_reserve(tape_routes: Dict[str, Any]) -> Dict[str, Any]:
    """d0 现金留存磁带手术：非紧迫种子买点后移至依赖消费前最近可行拍。

    签名意图：输入: 磁带路由表（=_decode_routes 产物同形） / 输出:
    {routes, change_table}（手术后磁带+变更表） / 错误: 移后买点晚于依赖
    消费（断供种链）或越种植截止线即抛。

    输入形态：{"actions": [动作...], "routes": {路由id: [动作池下标×719]},
    "shops": [...]}；动作={"farmer": 单元指令, "hands": [单元指令...],
    "market": 订单槽位列表}。输出 routes=写时复制手术后同形路由包（输入零
    改动），change_table 逐行 {route, kind, from_step, to_step, item, qty,
    reason}；kind∈{cash_reserve_buy_move, no-op}（零改动路由记 no-op 留档）。

    手术语义（详见模块 docstring）：d0 窗种子单按「MELON 优先、依赖消费最
    靠后」取候选；候选的依赖消费=该作物后续首次 PICKUP/PLANT 拍（保守；
    拿不准→紧迫不可移）；落点=依赖消费前最近可行拍（同日或前一日、≤624、
    market 槽<10 尾部追加）；逐笔挪动直至推算 d0 日终 ≥5（守卫投影口径
    静态近似·保守偏严）或候选耗尽。计划自洽不变量：PICKUP/PLANT/收成链
    不移不动（只动 market 单）、移后买点严格先于依赖消费（种子到达不晚于
    需要）、后移 ≤624。

    错误：手术后核算——移后买点 ≥ 依赖消费拍（断供种链）或 > 624（越种植
    截止线）→ RuntimeError（fail-closed；正常路径由落点规则保证不触发，
    保留为手术输出的守卫面）。输入非 dict/包形态坏→TypeError/ValueError
    （_check_package 同款 fail-closed）。
    """
    if not isinstance(tape_routes, dict):
        raise TypeError("tape_routes must be dict, got %s"
                        % type(tape_routes).__name__)
    _rs._check_package(tape_routes)
    pkg = copy.deepcopy(tape_routes)      # 输入零改动（写时复制手术）
    change_table: List[Dict[str, Any]] = []

    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [pkg["actions"][i] for i in idxs]
        before = _project_d0_end(seq)
        cands = _candidate_rows(seq)
        n_movable = sum(1 for c in cands if c["movable"])
        stats = ("窗内种子单 %d 张（可挪 %d/紧迫 %d）" % (
            len(cands), n_movable, len(cands) - n_movable))
        if before >= D0_CASH_FLOOR:
            change_table.append({
                "route": rid, "kind": "no-op", "from_step": 0, "to_step": 0,
                "item": None, "qty": 0,
                "reason": ("already reserved: projected d0 end %.1f >= %g "
                           "（守卫投影口径静态近似）；候选分析：%s"
                           % (before, D0_CASH_FLOOR, stats)),
            })
            continue
        moved = 0
        projected = before
        for cand in cands:
            if projected >= D0_CASH_FLOOR:
                break
            if not cand["movable"]:
                continue
            landing = _pick_landing(seq, cand["from_step"], cand["consumption"])
            if landing is None:
                continue
            # 手术：源槽换 []（cash_guard 顺延置 [] 先例）+ 目标步尾部追加
            idxs_s, _, src = _rs._cow_action(pkg, rid, cand["from_step"])
            src["market"][cand["slot"]] = []
            _rs._commit_action(pkg, idxs_s, cand["from_step"], src)
            idxs_t, _, tgt = _rs._cow_action(pkg, rid, landing)
            tgt["market"].append(["BUY_SEED", cand["item"], cand["qty"]])
            _rs._commit_action(pkg, idxs_t, landing, tgt)
            seq = [pkg["actions"][i] for i in idxs]   # 重取（防陈旧视图）
            projected = _project_d0_end(seq)
            moved += 1
            change_table.append({
                "route": rid, "kind": "cash_reserve_buy_move",
                "from_step": cand["from_step"], "to_step": landing,
                "item": cand["item"], "qty": cand["qty"],
                "reason": ("d0 cash reserve: consumption@%d（保守最早 "
                           "PICKUP/PLANT 拍）→落点依赖消费前最近可行拍"
                           "（同日或前一日）；源槽换 [] 尾部追加；推算 d0 "
                           "日终 %.1f→%.1f" % (cand["consumption"], before,
                                              projected)),
            })
        if moved == 0:
            change_table.append({
                "route": rid, "kind": "no-op", "from_step": 0, "to_step": 0,
                "item": None, "qty": 0,
                "reason": ("no feasible candidate: %s——依赖消费过近/拿不准"
                           "（保守判定紧迫不可移）或无可行落点；推算 d0 日终 "
                           "%.1f<%g → 交运行时守卫兜底"
                           % (stats, projected, D0_CASH_FLOOR)),
            })

    # ---- 术后核算（fail-closed）：移后买点仍先于依赖消费且 ≤624 ----
    for rid in sorted(pkg["routes"], key=lambda k: int(k)):
        idxs = pkg["routes"][rid]
        seq = [pkg["actions"][i] for i in idxs]
        for row in change_table:
            if (row["route"] != rid
                    or row["kind"] != "cash_reserve_buy_move"):
                continue
            cons = _first_consumption(seq, row["item"], row["from_step"])
            # 移后买点=to_step；其依赖消费以「源拍之后该作物首次消费拍」为准
            if row["to_step"] > PLANTING_DEADLINE:
                raise RuntimeError(
                    "越种植截止线：%s %s 移至 step %d>624（仍种得活被破）"
                    % (rid, row["item"], row["to_step"]))
            if cons is not None and row["to_step"] >= cons:
                raise RuntimeError(
                    "断供种链：%s %s 移至 step %d 不早于依赖消费拍 %d"
                    % (rid, row["item"], row["to_step"], cons))

    return {"routes": pkg, "change_table": change_table}
