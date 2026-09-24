# -*- coding: utf-8 -*-
"""phase_b —— R14 Phase B：四臂×双席位 seated 重演。

方法取材（只读复用不改源）：
  - twin 引擎（kaggle_simulations/agent/planner/twin；vendored wheel）；
  - 席位 seated 重演驱动（orderbook_l1_derivative/gate_equivalence_precision
    ._seated_replay 同构：对手席按录像动作开环重放，我席 callable 实驱）；
  - L3 在飞件装载（官方 last-callable 语义：compile+exec_dir+末位 callable；
    gate_launch_l3/v48 先例同款）。

四臂：对照=L3 原行为；A1 卖空率对齐；A2 高价品优先；A3 组合。
双席位：每局每臂在 seat0/seal1 各重演一次（对手席=录像开环重放，两臂共用
同一对手脚本——开环重演口径，对手反应性损失记入 evidence 注记）。

零足迹校验（双层口径，evidence 注记）：
  - 包装层（判据绑定面）：同观测下非 surge 日 wrapped==base 逐字节一致、
    surge 日差异仅限卖单——这是处置的可观察因果属性；
  - 流层：对照臂 vs 处置臂动作流——首 surge 日前必须逐字节一致；首改步
    之后市场态因果发散（我方卖单改变市场库存→价格路径→基座后续行为，含
    surge 日内后续步的非卖单反应），流差异记 first_alien_diff/
    causal_aftermath 报告面（不判红）。
"""
from __future__ import annotations

import copy
import json
import os
import sys
import time

from . import corpus as _corpus

ARMS = ("A1", "A2", "A3")
CONTROL = "control"

# 引擎品项序（kaggle_environments 1.32.7 kaggriculture PRODUCTS 键序镜像）
PRODUCT_ORDER = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
                 "EGG", "MILK", "WOOL")
MAX_MARKET_ORDERS = 10  # 引擎 maxMarketOrdersPerTurn 默认

_HERE = os.path.dirname(os.path.abspath(__file__))
_KSIM = os.path.dirname(_HERE)
_SOFTWARE = os.path.dirname(_KSIM)
sys.dont_write_bytecode = True


# ---------------------------------------------------------------------------
# L3 在飞件装载（官方 last-callable 语义）
# ---------------------------------------------------------------------------
def load_l3_callable(main_path):
    """装载 L3 main.py 末位 callable（官方提交语义；每调用全新装载）。

    复刻 gate_equivalence_precision._load_last_callable：compile(path) →
    exec_dir 进 sys.path → 空 env exec → 取 env 最后一个 callable（刻意不用
    named-`agent` 优先装载——那是层链中途包装器，官方入口是尾部 last-callable）。
    """
    path = os.path.abspath(main_path)
    if not os.path.isfile(path):
        raise FileNotFoundError(f"L3 main 不存在: {path}")
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    env = {}
    exec_dir = os.path.dirname(path)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, path, "exec"), env)
    finally:
        sys.path.remove(exec_dir)
    callables = [v for v in env.values() if callable(v)]
    if not callables:
        raise ValueError(f"{path} 装载后无 callable")
    return callables[-1]


# ---------------------------------------------------------------------------
# 观测/私有态小工具
# ---------------------------------------------------------------------------
def _priv_of(obs):
    """obs → private dict（dict/attr/JSON 串三态兼容）。"""
    priv = None
    if isinstance(obs, dict):
        priv = obs.get("private")
    else:
        priv = getattr(obs, "private", None)
    if isinstance(priv, str):
        priv = json.loads(priv)
    return priv or {}


def _shed_of(obs):
    shed = _priv_of(obs).get("shed") or {}
    if isinstance(shed, str):
        shed = json.loads(shed)
    return {k: int(v) for k, v in dict(shed).items() if int(v) > 0}


def _tot_inv_of(obs):
    """shed + 携带 inventories（Phase A tot_inv 同口径）。"""
    priv = _priv_of(obs)
    s = dict(priv.get("shed") or {})
    for inv in (priv.get("inventories") or []):
        for k, v in (inv or {}).items():
            s[k] = s.get(k, 0) + int(v)
    return {k: v for k, v in s.items() if v > 0}


def _prices_of(obs):
    market = obs.get("market") if isinstance(obs, dict) else getattr(obs, "market", None)
    if isinstance(market, str):
        market = json.loads(market)
    prices = (market or {}).get("prices") or {}
    return {k: float(v) for k, v in dict(prices).items()}


def _day_of(obs):
    if isinstance(obs, dict):
        return obs.get("day")
    return getattr(obs, "day", None)


def _step_of(obs):
    if isinstance(obs, dict):
        return obs.get("step")
    return getattr(obs, "step", None)


# ---------------------------------------------------------------------------
# 卖单改造（单一功能转变）
# ---------------------------------------------------------------------------
def _is_sell(order):
    return (isinstance(order, (list, tuple)) and len(order) >= 3
            and order[0] == "SELL")


def apply_surge_day_sells(action, observation, params, arm, tracker=None):
    """surge 日卖单改造：A1 卖空率对齐 / A2 高价品优先 / A3 组合。

    输入：基座 action、当前 observation、处置参数 params={'rate': r}（A1/A3；
    A2 仅用观测价×库存，不需要参数键）、tracker=包装层日内已执行量估计
    （{'sold_by_item': {item: qty}}，None 则视作零）。
    输出：改造后 action（深拷贝，不动基座对象）。

    语义：
    - A1：当日目标卖出量 = rate × 当日累计可卖（期初+产出，随到货自适应）；
      remaining = rate×(当前持有+已执行) − 已执行 − 基座本步在架可成交量；
      按"我方自然卖序"（基座 SELL 品项序 → 其余有货品项按引擎品项序）逐品项
      放量补单——只增不减，新增单逐品项 ≤ shed 库存（引擎仅 shed 背书成交），
      market 单数 ≤10。
    - A2：卖单按 当日价×shed库存 价值降序重排（非 SELL 单原槽位保留）；
      有空槽时按价值降序为有货未卖品项补单（qty=shed）。
    - A3：先 A1 放量，再 A2 重排+补槽。
    - 硬约束：任何品项新增量不超过 shed 持有（只卖有的）；farmer/hands 与
      非 SELL market 单逐字节原样保留。
    异常上抛（build_treatment_arm 兜底回退原 action）。
    """
    if arm not in ARMS:
        raise ValueError(f"未知处置臂 {arm!r}")
    if not isinstance(action, dict):
        raise TypeError("action 非 dict")
    market = action.get("market")
    if not isinstance(market, list):
        return copy.deepcopy(action)
    out = {k: copy.deepcopy(v) for k, v in action.items()}
    shed = _shed_of(observation)
    prices = _prices_of(observation)
    tot = _tot_inv_of(observation)
    if tracker is None:
        sold = {}
    elif isinstance(tracker, dict):
        sold = tracker.get("sold_by_item") or {}
    else:
        sold = getattr(tracker, "sold_by_item", None) or {}

    sells = [i for i, o in enumerate(market) if _is_sell(o)]
    base_qty = {}
    for i in sells:
        item = market[i][1]
        base_qty[item] = base_qty.get(item, 0) + int(market[i][2])
    room = {i: max(0, shed.get(i, 0) - base_qty.get(i, 0))
            for i in set(shed) | set(base_qty)}

    def _value(item):
        return prices.get(item, 0.0) * shed.get(item, 0)

    add_qty = {}
    if arm in ("A1", "A3"):
        rate = float(params.get("rate", 0.0))
        rate = min(1.0, max(0.0, rate))
        tot_total = sum(tot.values())
        sold_total = sum(sold.values())
        # 当日目标 = rate×(当前持有+已执行)；基座本步已提交且可成交的部分
        # 计入目标额度（pending）——只提至目标，不重复放量。
        pending_base = sum(min(base_qty.get(i, 0), shed.get(i, 0))
                           for i in base_qty)
        remaining = rate * (tot_total + sold_total) - sold_total - pending_base
        if remaining > 0:
            natural = [market[i][1] for i in sells]
            natural += [i for i in PRODUCT_ORDER
                        if i in shed and i not in natural]
            for item in natural:
                if remaining <= 0:
                    break
                take = min(remaining, room.get(item, 0))
                if take > 0:
                    add_qty[item] = add_qty.get(item, 0) + int(take)
                    remaining -= take

    # 组装 market：非 SELL 单原槽位保留；SELL 单按 A2 价值序重排；新增单
    # （A1 放量提量 / A2 补槽追加）合并。
    new_market = []
    sell_orders = []
    for i, order in enumerate(market):
        if _is_sell(order):
            item = order[1]
            qty = int(order[2])
            if item in add_qty:
                qty += add_qty.pop(item)
            sell_orders.append([str(order[0]), item, int(qty)])
        else:
            new_market.append(list(order) if isinstance(order, (list, tuple))
                              else copy.deepcopy(order))
    for item, qty in add_qty.items():  # 基座未卖品项的 A1 追加
        if qty > 0:
            sell_orders.append(["SELL", item, int(qty)])
    if arm in ("A2", "A3"):
        sell_orders.sort(key=lambda o: -_value(o[1]))
        for item in (i for i in PRODUCT_ORDER if i in shed
                     and i not in base_qty and i not in add_qty):
            if len(sell_orders) >= MAX_MARKET_ORDERS:
                break
            if _value(item) <= 0:
                continue
            sell_orders.append(["SELL", item, int(shed[item])])
    # 槽位上限：SELL 单塞进 market，超出 10 单的截尾（引擎同语义截断）
    for order in sell_orders:
        if len(new_market) >= MAX_MARKET_ORDERS:
            break
        new_market.append(order)
    out["market"] = new_market
    return out


# ---------------------------------------------------------------------------
# 处置臂包装
# ---------------------------------------------------------------------------
class _Tracker:
    """包装层日内状态：已执行量估计（库存正差累计）+ 动作对记录。"""

    def __init__(self):
        self.step = None
        self.day = None
        self.sold_by_item = {}
        self.last_tot = None
        self.pairs = []  # (day, step, base_action, out_action)

    def reset(self):
        self.sold_by_item = {}

    def update(self, obs, day):
        tot = _tot_inv_of(obs)
        if self.last_tot is not None and self.day is not None \
                and day == self.day:
            for item, qty in tot.items():
                drop = self.last_tot.get(item, 0) - qty
                if drop > 0:
                    self.sold_by_item[item] = (self.sold_by_item.get(item, 0)
                                               + drop)
            for item, qty in self.last_tot.items():
                if item not in tot:
                    drop = qty
                    if drop > 0:
                        self.sold_by_item[item] = (
                            self.sold_by_item.get(item, 0) + drop)
        self.last_tot = tot


def build_treatment_arm(l3_callable, surge_config, arm):
    """构造处置 callable：包装 L3 agent。

    输入：L3 callable + surge_config（{day:int → params dict，至少
    {'rate': r}}）+ 臂类型。输出：包装 callable。
    - 非 surge 日回合：基座 action 原样透传（同对象）；
    - surge 日回合：apply_surge_day_sells 改造；包装层任何异常→回退原 action
      （fail-safe）；
    - step==0（或观测 step 回退）复位 tracker；跨日重置日内计数。
    wrapped.pairs 供零足迹包装层校验（(day, step, base, out) 列表）。
    """
    if arm not in ARMS:
        raise ValueError(f"未知处置臂 {arm!r}")
    tracker = _Tracker()

    def wrapped(obs):
        step, day = _step_of(obs), _day_of(obs)
        if step == 0 or (tracker.step is not None and step < tracker.step):
            tracker.reset()
            tracker.last_tot = None
        if day != tracker.day:
            if day is not None and tracker.day is not None \
                    and day == tracker.day + 1:
                tracker.update(obs, tracker.day)  # 日界转移的成交归前一日
            tracker.reset()
            tracker.day = day
        tracker.update(obs, day)
        base = l3_callable(obs)
        out_action = base
        if day in surge_config:
            try:
                out_action = apply_surge_day_sells(
                    base, obs, surge_config[day], arm, tracker)
            except Exception:
                out_action = base  # fail-safe：回退原 action
        tracker.pairs.append((day, step, base, out_action))
        tracker.step = step
        return out_action

    wrapped.pairs = tracker.pairs
    wrapped.arm = arm
    return wrapped


# ---------------------------------------------------------------------------
# twin 驱动
# ---------------------------------------------------------------------------
_TWIN = None


def _twin():
    global _TWIN
    if _TWIN is None:
        if _SOFTWARE not in sys.path:
            sys.path.insert(0, _SOFTWARE)
        from kaggle_simulations.agent.planner import twin
        _TWIN = twin
    return _TWIN


def _obs_dict(state, seat):
    """twin 席位观测 → 提交 callable 可读纯 dict（等价面门同款）。"""
    obs0 = state.seats[0].observation
    mine = state.seats[seat].observation
    return {
        "farms": obs0.farms,
        "market": obs0.market,
        "town": obs0.town,
        "day": mine.day,
        "hour": mine.hour,
        "step": obs0.step,
        "player": seat,
        "private": mine.private,
        "remainingOverageTime": 60.0,
    }


def _canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, default=str)


def replay_dual_seat(replay, our_callable, seat, wall_timeout=900.0):
    """单局单臂单席位 seated 重演（对手席=录像开环重放）。

    输入：回放 dict、我方 callable、我方席位。输出：
      {margin, status, steps_n, finals, stream, wall_s}——margin=我席终局
    资金−对席终局资金；status：env.done→'DONE' 否则 'INCOMPLETE'；agent/引擎
    异常向上抛（编排层重跑一次）；wall 超时抛 TimeoutError。
    """
    twin = _twin()
    bundle = twin.load_engine()
    state = twin.build_state_from_replay(replay, 0, bundle)
    recorded = twin.replay_transition_actions(replay)
    if not recorded:
        raise ValueError("replay 无转移动作流")
    stream, taken = [], 0
    t0 = time.perf_counter()
    while not state.env.done and taken < len(recorded):
        if taken % 120 == 0 and time.perf_counter() - t0 > wall_timeout:
            raise TimeoutError(f"replay 超时 {wall_timeout}s @taken={taken}")
        obs = _obs_dict(state, seat)
        mine = our_callable(obs)
        pair = [recorded[taken][1 - seat]] * 2
        pair[seat] = mine
        twin.step(state, pair)
        stream.append(mine)
        taken += 1
    finals = twin.final_money(state)
    return {"margin": finals[seat] - finals[1 - seat],
            "finals": finals,
            "status": "DONE" if state.env.done else "INCOMPLETE",
            "steps_n": taken, "stream": stream,
            "wall_s": round(time.perf_counter() - t0, 2)}


# ---------------------------------------------------------------------------
# 零足迹校验
# ---------------------------------------------------------------------------
def _sell_only_diff(a, b):
    """两动作差异是否仅限卖单（非 market 键逐字节等 + 非 SELL market 多重集等）。"""
    if not isinstance(a, dict) or not isinstance(b, dict):
        return False
    if set(a) != set(b):
        return False
    for key in a:
        if key == "market":
            continue
        if _canonical(a[key]) != _canonical(b[key]):
            return False
    am, bm = a.get("market"), b.get("market")
    if not isinstance(am, list) or not isinstance(bm, list):
        return _canonical(am) == _canonical(bm)
    a_other = [_canonical(o) for o in am if not _is_sell(o)]
    b_other = [_canonical(o) for o in bm if not _is_sell(o)]
    return sorted(a_other) == sorted(b_other)


def compare_action_stream(control_stream, treatment_stream, surge_days):
    """流层零足迹校验（双层口径的流层面，evidence 注记）。

    判据绑定面 binding_ok：
      - 首个差异若存在，必须落在 surge 日内（首 surge 日之前非 surge 日
        逐字节一致；处置从未触发的局全流一致）；
    注记面：首改步之后非 surge 日的流差异 = 市场态因果发散（我方 surge 日
    卖单改变市场库存→价格路径→基座后续行为），n_causal_aftermath 计数，
    不判红；surge 日差异须仅限卖单（first_alien_diff 定位首个异类）。
    step t 的日属 = t//24（agent 在态 t 被调）。
    """
    surge = {int(d) for d in (surge_days or [])}
    control_stream = list(control_stream or [])
    treatment_stream = list(treatment_stream or [])
    first_div = None
    n_after, n_surge_diff, first_alien = 0, 0, None
    for t in range(max(len(control_stream), len(treatment_stream))):
        a = control_stream[t] if t < len(control_stream) else "<missing>"
        b = treatment_stream[t] if t < len(treatment_stream) else "<missing>"
        if _canonical(a) == _canonical(b):
            continue
        if first_div is None:
            first_div = t
        day = t // 24
        if day in surge:
            n_surge_diff += 1
            if not _sell_only_diff(a, b) and first_alien is None:
                first_alien = {"step": t, "day": day, "kind": "surge_alien",
                               "control": _canonical(a)[:200],
                               "treatment": _canonical(b)[:200]}
        elif first_div is not None and t > first_div:
            n_after += 1
    n_off_total = 0
    for t in range(max(len(control_stream), len(treatment_stream))):
        a = control_stream[t] if t < len(control_stream) else "<missing>"
        b = treatment_stream[t] if t < len(treatment_stream) else "<missing>"
        if _canonical(a) != _canonical(b) and (t // 24) not in surge:
            n_off_total += 1
    binding_ok = first_div is None or (first_div // 24) in surge
    return {"identical_off_surge": bool(n_off_total == 0),
            "binding_ok": bool(binding_ok),
            "first_alien_diff": first_alien, "first_divergence": first_div,
            "n_off_surge_diffs": n_off_total, "n_causal_aftermath": n_after,
            "n_surge_diffs": n_surge_diff}


def wrapper_zero_footprint(pairs, surge_days):
    """包装层零足迹校验：非 surge 日 wrapped==base；surge 日差异仅限卖单。"""
    surge = {int(d) for d in (surge_days or [])}
    violations = []
    for idx, (day, step, base, out) in enumerate(pairs or []):
        if _canonical(base) == _canonical(out):
            continue
        if day not in surge:
            violations.append({"step": step, "day": day,
                               "kind": "off_surge_modification"})
        elif not _sell_only_diff(base, out):
            violations.append({"step": step, "day": day,
                               "kind": "surge_alien_diff"})
    return {"ok": not violations, "violations": violations[:20],
            "n_violations": len(violations),
            "n_modified_steps": sum(1 for d, s, b, o in pairs or []
                                    if _canonical(b) != _canonical(o))}


# ---------------------------------------------------------------------------
# 编排
# ---------------------------------------------------------------------------
def _orientation_key(phase_a_game, seat):
    """席位 → Phase A 定向键（'our'=renyxin 原席 / 'other'=对席）。"""
    our = phase_a_game.get("seat")
    if our is None:
        return "our"
    return "our" if seat == our else "other"


def _surge_config_for(phase_a_game, seat):
    orient = phase_a_game.get("orientations", {}).get(
        _orientation_key(phase_a_game, seat)) or {}
    cfg = {}
    for d_str, comp in (orient.get("composition") or {}).items():
        if comp:
            cfg[int(d_str)] = {"rate": comp.get("opp_short_rate", 0.0)}
    return cfg, sorted(int(d) for d in (orient.get("surge_days") or []))


def _run_arm(replay, l3_main, seat, arm, surge_config, retry=1):
    """单臂单席重演（异常→全新装载重跑一次；仍败上抛）。"""
    last_exc = None
    for attempt in range(retry + 1):
        try:
            base = load_l3_callable(l3_main)
            callable_fn = (build_treatment_arm(base, surge_config, arm)
                           if arm in ARMS else base)
            res = replay_dual_seat(replay, callable_fn, seat)
            res["pairs"] = getattr(callable_fn, "pairs", None)
            return res
        except Exception as exc:
            last_exc = exc
    raise last_exc


def phase_b_four_arm_replay(phase_b_corpus, phase_a_report, l3_main,
                            wall_budget_s=7200.0, log=None):
    """四臂×双席位重演编排。

    输入：corpus_select()['phase_b']（losses+wins）、Phase A 报告、L3 main
    路径。输出：{per_game, summary}——逐局逐臂双席 margin/Δ/零足迹校验/
    异常红标。单臂单席 fail 两次=该局该臂红（fail-closed 留痕不中断其余）。
    """
    log = log or (lambda msg: None)
    by_ep = {g.get("episode"): g for g in phase_a_report.get("per_game", [])}
    games = list((phase_b_corpus or {}).get("losses", [])) \
        + list((phase_b_corpus or {}).get("wins", []))
    t_start = time.perf_counter()
    per_game, n_red, n_replays = [], 0, 0
    for entry in games:
        ep = entry.get("episode")
        rec = {"episode": ep, "tag": entry.get("tag"), "res": entry.get("res"),
               "margin": entry.get("margin"), "seat": entry.get("seat"),
               "arms": {}}
        pa_game = by_ep.get(ep) or {}
        try:
            replay = _corpus.load_replay(entry["path"])
        except Exception as exc:
            rec["error"] = f"装载失败: {type(exc).__name__}: {exc}"
            per_game.append(rec)
            n_red += 1
            continue
        for seat in (0, 1):
            surge_cfg, surge_days = _surge_config_for(pa_game, seat)
            seat_key = f"seat{seat}"
            try:
                control = _run_arm(replay, l3_main, seat, CONTROL, surge_cfg)
            except Exception as exc:
                rec["arms"][seat_key] = {"error": f"对照臂: {exc!r}"}
                n_red += 1
                n_replays += 2
                continue
            n_replays += 1
            rec["arms"][seat_key] = {
                "surge_days": surge_days,
                CONTROL: {"margin": round(control["margin"], 1),
                          "status": control["status"],
                          "steps_n": control["steps_n"]},
            }
            for arm in ARMS:
                n_replays += 1
                try:
                    res = _run_arm(replay, l3_main, seat, arm, surge_cfg)
                except Exception as exc:
                    rec["arms"][seat_key][arm] = {
                        "error": f"{type(exc).__name__}: {exc}", "red": True}
                    n_red += 1
                    continue
                zfp_wrapper = wrapper_zero_footprint(res.get("pairs"),
                                                     surge_days)
                zfp_stream = compare_action_stream(
                    control["stream"], res["stream"], surge_days)
                # 红标判据（零足迹双层口径）：
                # - 包装层 ok（同观测非 surge 日不改性、surge 日改造仅限卖单）
                #   ——处置的可观察因果属性，绑定；
                # - 流层 binding_ok（首差异必须落在 surge 日内；无处置局全流
                #   一致）——绑定；
                # - 流层 surge 日非卖单差异与首改步后非 surge 日差异均为基座
                #   对市场态发散的因果反应（first_alien_diff/aftermath 报告
                #   面，不判红）。
                ok = (zfp_wrapper["ok"] and zfp_stream["binding_ok"]
                      and res["status"] == "DONE")
                rec["arms"][seat_key][arm] = {
                    "margin": round(res["margin"], 1),
                    "delta": round(res["margin"] - control["margin"], 1),
                    "status": res["status"], "steps_n": res["steps_n"],
                    "zerofootprint_wrapper": zfp_wrapper,
                    "zerofootprint_stream": {
                        k: v for k, v in zfp_stream.items()},
                    "n_modified_steps": zfp_wrapper["n_modified_steps"],
                    "red": not ok,
                }
                if not ok:
                    n_red += 1
        log(f"[phase_b] ep={ep} "
            + " ".join(
                f"{arm}:[{rec['arms']['seat0'].get(arm, {}).get('delta')},"
                f"{rec['arms']['seat1'].get(arm, {}).get('delta')}]"
                for arm in ARMS)
            + f" ({time.perf_counter() - t_start:.0f}s)")
        if time.perf_counter() - t_start > wall_budget_s:
            rec["budget_stop"] = True
            per_game.append(rec)
            break
        per_game.append(rec)
    summary = {"n_games": len(games), "n_replays": n_replays, "n_red": n_red,
               "wall_s": round(time.perf_counter() - t_start, 1),
               "budget_stopped": bool(per_game and per_game[-1].get("budget_stop"))}
    return {"per_game": per_game, "summary": summary}
