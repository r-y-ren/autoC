# -*- coding: utf-8 -*-
"""judge_r23 + segment_stats（R23 L1/L2）：判决线。

责任契约（fn_docs/hybrid/responsibility.md【R23 增补】）：
败局 12 局定向重演（分析24 败局谱系）+联赛 300-500 局（含榜前 550 段强手
样本）+分段统计（d21-28 资金差/实现单价/有效挂单率）+仿真器对照（≥30 局
抽样与官方引擎逐局一致）；聚合分项四判据+总判出 evidence。

【判决口径钉】（实现与测试同钉；判据=R23 ②分项+总判原文）
- 语义=活件（pkg_path 的 r40 件）vs 原局对手录像动作（开环，R15/R19/
  judge_predict 先例）逐局双席位各演一遍（候选坐 seat0 一局+seat1 一局，
  排除座位效应）；录像映射=磁带 step X ↔ replay si X+1（parse_states 校准
  口径）：live 观察 step s 时回放 replay action[s+1]。
- 联赛=离线真交易（judge_league 同构）：主对 h2h vs r37（现役最强）+强对手
  件（r34a/r33/v48 等仓内件）+mirror（r40 vs r40）；每独立 seed 双席位各
  一局、席位翻转不双计——统计按独立 seed n 报：胜=两席皆胜、平=席位分歧
  或皆平、负=皆负，rate=(胜+0.5平)/独立局；无决胜 seed（W+L=0）→rate=0.0
  fail-closed。榜前 550 段=强对手件臂（不含 mirror）。
- 分段统计=败局定向重演局（有原局基线）逐局对同席原局实况自比（judge_
  predict「坐哪席就与该席原局实况比」同源）；判据聚合取逐局读数中位
  （实价为逐局配对 up_pct 中位），任一局红/缺读数→该判据 fail-closed
  False（红局计入不短路：计损失、入 errors、不中断全跑）。
- 判决提速=同一批局三次实跑（零外推）：主口径 speedup=official 串行墙钟
  （改4 前判决口径：官方引擎逐局串行）/本判决并行墙钟（仿真器+workers
  并行跑口，缺省 16 workers=调研 16x 并行口径）；辅口径 speedup_parallel
  （同引擎纯并行）、speedup_engine（纯引擎）同录 evidence；仿真器对照=
  sim_bridge 抽样 ≥30 局双引擎逐局终局资金一致率（对照降级→改4 判
  False）。
- 引擎=run_games 判决跑口（config 可强制 engine=sim/official/auto；auto=
  桥证得 loaded+consistency_ok 才走仿真器，否则回退官方引擎留档）。
- evidence 由本函数返回、不落盘（台账/实跑落盘归实跑编排，防测试覆写真
  台账——R19 judge 同则）；六判据=c1..c4 分项（改1..改4）+c5/c6 总判
  （h2h vs r37、联赛总胜率），overall=六判据全真。

【segment_stats 口径】states=逐拍状态行序列（对局状态序列），字段（均可
缺省）：step|day（步标/日标，day 缺省=step//24）、cash|money（我方资金）、
opp_cash|opp_money（对席资金）、turnover（当拍 SELL 成交额）、vol（当拍
SELL 成交量）、filled_orders（当拍 SELL 成交单数）、orders（当拍 SELL
挂单数）、qty（当拍 SELL 挂单量）。四读数均取 d21-28 窗（day∈[21,28]，
day=step//24；成交类字段记「该状态拍挂出并结算的单」）：
  seg_delta    =d21-28 段资金差=窗末（day≤28 末行）margin−段始（day≤20
                 末行，缺则窗首行）margin，margin=cash−opp_cash；
  realized_px  =实现单价=Σturnover/Σvol（成交额/量）；
  fill_rate    =有效挂单占比=Σfilled_orders/Σorders（成交单/挂单）；
  lot_size     =批量化率=Σqty/Σorders（单均量，挂单口径）。
任一所需字段缺/非数（或分母为 0）→该读数 "UNKNOWN"（缺字段→UNKNOWN）。
baseline=原局基线：四读数 Mapping 直用，或状态行序列（内算读数）；verdict
={status, unknown, seg_delta_positive, realized_px_up_pct, fill_rate_delta,
lot_size_up_pct, baseline}。
"""
from __future__ import annotations

import copy
import hashlib
import json
import math
import multiprocessing
import os
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Sequence, Tuple

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
LEGACY_DIR = KSIM_DIR.parent

RECORD_VERSION = "judge-r23/1.0"
UNKNOWN = "UNKNOWN"
REPLAY_GLOB = "episode-*-replay.json"
REPLAY_CACHE_DIRS = ("/tmp/kagr23", "/tmp/kagr24", "/tmp/kagr22",
                     "/tmp/r33audit")
PULL_DIR = "/tmp/kagr24"
KAGGLE_BIN = "/home/renyxin/.local/bin/kaggle"

TURN = 24                       # turnsPerDay
WIN_DAY_LO, WIN_DAY_HI = 21, 28
WIN_STEP_LO = WIN_DAY_LO * TURN      # 504：d21-28 窗（拍）下界（含）
WIN_STEP_HI = (WIN_DAY_HI + 1) * TURN  # 696：上界（不含）
SEG_ANCHOR_DAY = 20                  # 资金差段始=day20 日终

# 判据阈值（R23 ②原文）
T_TOP550_WINRATE = 0.30         # 改1：榜前 550 段胜率 ≥30%（基线 0/5）
T_SEG_POSITIVE = 0.0            # 改1：d21-28 段资金差转正
T_SEG_DELTA_MEDIAN = 3600.0     # 改2：段资金差中位 ≥+3,600（胜局基线半）
T_REALIZED_PX_UP_PCT = 3.0      # 改2：实现单价 +3%
T_FILL_RATE = 0.90              # 改3：有效挂单占比 ≥90%
T_PX_UP_PCT = 2.0               # 改3：单价 +2%
T_SPEEDUP = 10.0                # 改4：判决提速 ≥10x
T_H2H_RATE = 0.55               # 总判：h2h vs r37 ≥0.55
T_LEAGUE_WINRATE = 0.85         # 总判：联赛总胜率 ≥85%

_METRICS = ("seg_delta", "realized_px", "fill_rate", "lot_size")

DEFAULT_OPPONENTS: Tuple[str, ...] = (
    "orderbook_r37/build/main.py",
    "orderbook_2965_adopt/a/main.py",
    "orderbook_2965_adopt/b/main.py",
    "v48_derivative/main.py",
)

DEFAULT_BENCH: Dict[str, Any] = {
    "n_games": 350,             # 联赛总对局数（双席计；每独立 seed 两局）
    "opponents": None,          # None→DEFAULT_OPPONENTS（首个=主对 r37）
    "workers": 16,              # 并行 workers（调研 16x 并行口径）
    "engine": "auto",           # auto/sim/official（run_games 可强制）
    "n_bridge_games": 30,       # 仿真器对照抽样局数（≥30）
    "speed_probe_games": 32,    # 提速实测局数（串行/并行同批）
    "seed_bases": {"h2h": 510000, "strong": 520000, "mirror": 530000,
                   "speed": 540000},
    "bridge_config": {},        # 透传 sim_bridge
    "pull_missing": True,       # 语料缺 replay 时 kaggle 拉取
}


# ============================================================ segment_stats --

def _num(x: Any) -> Optional[float]:
    if isinstance(x, bool):
        return None
    if isinstance(x, (int, float)):
        v = float(x)
        return None if math.isnan(v) else v
    return None


def _row_day(row: Mapping[str, Any]) -> Optional[int]:
    """状态行→日标：day 优先，缺则 step//24（hour 仅在 day+hour 形态下用）。"""
    d = _num(row.get("day"))
    if d is not None:
        return int(d)
    s = _num(row.get("step"))
    if s is not None:
        return int(s) // TURN
    return None


def _row_margin(row: Mapping[str, Any]) -> Optional[float]:
    c = _num(row.get("cash", row.get("money")))
    o = _num(row.get("opp_cash", row.get("opp_money")))
    if c is None or o is None:
        return None
    return c - o


def _readings(states: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """状态行序列→四读数（缺字段→UNKNOWN；窗=d21-28）。"""
    rows = [r for r in states if isinstance(r, Mapping)]
    win = [r for r in rows
           if _row_day(r) is not None
           and WIN_DAY_LO <= _row_day(r) <= WIN_DAY_HI]
    before = [r for r in rows
              if _row_day(r) is not None and _row_day(r) <= SEG_ANCHOR_DAY]

    seg: Any = UNKNOWN
    start = end = None
    for r in reversed(before):
        m = _row_margin(r)
        if m is not None:
            start = m
            break
    if start is None:
        for r in win:
            m = _row_margin(r)
            if m is not None:
                start = m
                break
    for r in reversed(win):
        m = _row_margin(r)
        if m is not None:
            end = m
            break
    if start is not None and end is not None:
        seg = round(end - start, 1)

    def _sum(key: str) -> Optional[float]:
        if not win:
            return None
        total = 0.0
        for r in win:
            v = _num(r.get(key))
            if v is None:
                return None
            total += v
        return total

    turnover, vol = _sum("turnover"), _sum("vol")
    filled, orders = _sum("filled_orders"), _sum("orders")
    qty = _sum("qty")
    realized: Any = UNKNOWN
    if turnover is not None and vol is not None and vol > 0:
        realized = round(turnover / vol, 2)
    fill: Any = UNKNOWN
    if filled is not None and orders is not None and orders > 0:
        fill = round(filled / orders, 4)
    lot: Any = UNKNOWN
    if qty is not None and orders is not None and orders > 0:
        lot = round(qty / orders, 2)
    return {"seg_delta": seg, "realized_px": realized,
            "fill_rate": fill, "lot_size": lot}


def segment_stats(states: Any, baseline: Any = None) -> Dict[str, Any]:
    """分段统计：d21-28 段资金差、实现单价、有效挂单占比、批量化率。

    签名意图：输入: 对局状态序列+原局基线 / 输出: {seg_delta, realized_px,
    fill_rate, lot_size, verdict} / 错误: 缺字段→UNKNOWN。

    口径见模块 docstring【segment_stats 口径】。states 须为状态行序列
    （非 Mapping 行→TypeError）；baseline 为四读数 Mapping 或状态行序列；
    verdict 带基线自比（realized_px_up_pct 等，无基线→None）。
    """
    if states is None or isinstance(states, (str, bytes, Mapping)):
        raise TypeError("states 须为状态行序列")
    try:
        rows = list(states)
    except TypeError as exc:
        raise TypeError("states 须为状态行序列") from exc
    for r in rows:
        if not isinstance(r, Mapping):
            raise TypeError("states 行须为 Mapping")
    reads = _readings(rows)

    base_reads: Optional[Dict[str, Any]] = None
    if baseline is not None:
        if isinstance(baseline, Mapping) and any(
                k in baseline for k in _METRICS):
            base_reads = {k: baseline.get(k, UNKNOWN) for k in _METRICS}
        else:
            if isinstance(baseline, (str, bytes, Mapping)):
                raise TypeError("baseline 须为状态行序列或四读数 Mapping")
            base_rows = list(baseline)
            for r in base_rows:
                if not isinstance(r, Mapping):
                    raise TypeError("baseline 行须为 Mapping")
            base_reads = _readings(base_rows)

    def _up_pct(cur: Any, base: Any) -> Optional[float]:
        c, b = _num(cur), _num(base)
        if c is None or b is None or b == 0:
            return None
        return round((c - b) / abs(b) * 100.0, 2)

    def _delta(cur: Any, base: Any) -> Optional[float]:
        c, b = _num(cur), _num(base)
        if c is None or b is None:
            return None
        return round(c - b, 4)

    unknown = [k for k in _METRICS if reads[k] == UNKNOWN]
    seg_pos: Optional[bool] = None
    if _num(reads["seg_delta"]) is not None:
        seg_pos = bool(_num(reads["seg_delta"]) > T_SEG_POSITIVE)
    verdict = {
        "status": "ok" if not unknown else "UNKNOWN",
        "unknown": unknown,
        "seg_delta_positive": seg_pos,
        "realized_px_up_pct": (
            _up_pct(reads["realized_px"], base_reads["realized_px"])
            if base_reads else None),
        "fill_rate_delta": (
            _delta(reads["fill_rate"], base_reads["fill_rate"])
            if base_reads else None),
        "lot_size_up_pct": (
            _up_pct(reads["lot_size"], base_reads["lot_size"])
            if base_reads else None),
        "baseline": base_reads,
    }
    return {"seg_delta": reads["seg_delta"],
            "realized_px": reads["realized_px"],
            "fill_rate": reads["fill_rate"],
            "lot_size": reads["lot_size"],
            "verdict": verdict}


# ============================================================ 观察/装载面 --

def _to_plain(o: Any) -> Any:
    if isinstance(o, Mapping):
        return {k: _to_plain(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_to_plain(v) for v in o]
    return o


_OBS_KEYS = ("step", "day", "hour", "player", "farms", "market", "town",
             "private", "remainingOverageTime")


def _obs_dict(obs: Any) -> Dict[str, Any]:
    """引擎观察（dict/Struct/attr 对象）→纯 dict 快照。"""
    if isinstance(obs, Mapping):
        return _to_plain(obs)
    out: Dict[str, Any] = {}
    for key in _OBS_KEYS:
        try:
            out[key] = _to_plain(getattr(obs, key))
        except Exception:
            continue
    return out


def _obs_step(obs: Any) -> int:
    d = obs if isinstance(obs, Mapping) else _obs_dict(obs)
    s = _num(d.get("step"))
    if s is not None:
        return int(s)
    day = _num(d.get("day")) or 0
    hour = _num(d.get("hour")) or 0
    return int(day) * TURN + int(hour)


def _load_entry(path: Any) -> Any:
    """单文件件装载：官方 last-callable 语义（全新命名空间、末 callable）。"""
    p = os.path.abspath(str(path))
    if not os.path.isfile(p):
        raise FileNotFoundError(f"agent 文件不存在: {p}")
    with open(p, "r", encoding="utf-8") as fh:
        src = fh.read()
    ns: Dict[str, Any] = {}
    exec_dir = os.path.dirname(p)
    sys.path.append(exec_dir)
    try:
        exec(compile(src, p, "exec"), ns)
    finally:
        sys.path.remove(exec_dir)
    entries = [v for v in ns.values() if callable(v)]
    if not entries:
        raise ValueError(f"{p} 装载后无 callable")
    return entries[-1]


def _call_inner(inner: Any, obs: Any, configuration: Any) -> Any:
    code = getattr(inner, "__code__", None)
    n = code.co_argcount if code is not None and hasattr(code, "co_argcount") \
        else 1
    args = [obs, configuration][:max(1, int(n))]
    return inner(*args)


class _TapeAgent:
    """录像开环对手：按步回放原局动作（磁带 step X ↔ replay si X+1）。"""

    def __init__(self, actions: Sequence[Any]):
        self.actions = list(actions or [])

    def __call__(self, obs: Any, configuration: Any = None) -> Any:
        idx = _obs_step(obs) + 1
        if 0 <= idx < len(self.actions) and self.actions[idx]:
            return copy.deepcopy(self.actions[idx])
        return {"farmer": ["PASS"], "hands": [], "market": []}


class _Tracer:
    """观察/动作逐拍追踪（为分段统计产状态行；不改动作）。"""

    def __init__(self, inner: Any, seat: int, sink: List[Any]):
        self.inner = inner
        self.seat = seat
        self.sink = sink

    def __call__(self, obs: Any, configuration: Any = None) -> Any:
        act = _call_inner(self.inner, obs, configuration)
        self.sink.append((_obs_step(obs), _obs_dict(obs), act))
        return act


# ============================================================ 归因（成交） --

def _shadow_module():
    """kgenv 影子引擎（逐拍成交归因，与官方引擎逐场交叉校验过）；缺→None。"""
    try:
        base = str(LEGACY_DIR)
        if base not in sys.path:
            sys.path.insert(0, base)
        from kgenv import replay_profile as rp  # noqa: WPS433
        return rp
    except Exception:
        return None


_SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": TURN, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}


def _window_states(traces: Mapping[int, List[Any]], our_seat: int,
                   seed: int) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """追踪/录像观察→d21-28 逐拍状态行（含 day20 日终锚行）。

    traces={seat: [(step, obs_dict, action)]}；成交类字段由影子引擎逐拍归因
    （SELL 单）；影子不可得/归因缺口→该拍省略成交字段（读数侧 UNKNOWN）。
    返回 (rows, meta)（meta.attribution_mismatches=影子对账失配拍数）。
    """
    idx: Dict[int, Dict[int, Tuple[Dict[str, Any], Any]]] = {}
    for seat, sink in traces.items():
        m: Dict[int, Tuple[Dict[str, Any], Any]] = {}
        for step, obs, act in sink:
            m[int(step)] = (obs, act)
        idx[int(seat)] = m
    s0, s1 = idx.get(0, {}), idx.get(1, {})
    steps = sorted(set(s0) | set(s1))
    meta: Dict[str, Any] = {"attribution_mismatches": 0,
                            "attribution_used": False, "steps": len(steps)}

    def _money(seat: int, step: int) -> Optional[float]:
        obs = idx.get(seat, {}).get(step, (None, None))[0]
        if not obs:
            return None
        farms = obs.get("farms") or []
        if seat >= len(farms) or not isinstance(farms[seat], Mapping):
            return None
        return _num(farms[seat].get("money"))

    def _sell_rows_from_attr(attr: Any, seat: int) -> Dict[str, Any]:
        out = {"orders": 0, "qty": 0.0, "filled_orders": 0, "vol": 0.0,
               "turnover": 0.0}
        try:
            for o in attr["market"][seat]["orders"]:
                if o.get("type") != "SELL":
                    continue
                out["orders"] += 1
                out["qty"] += float(o.get("requested") or 0)
                filled = float(o.get("filled") or 0)
                out["vol"] += filled
                out["turnover"] += float(o.get("value") or 0)
                if filled > 0:
                    out["filled_orders"] += 1
        except Exception:
            return {}
        return out

    rp = _shadow_module()
    shadow_state = None
    if rp is not None and idx.get(0) and idx.get(1):
        pre0 = idx[0].get(WIN_STEP_LO, (None, None))[0]
        pre1 = idx[1].get(WIN_STEP_LO, (None, None))[0]
        if pre0 and pre1:
            try:
                shadow_state = rp._s_snapshot(
                    pre0, [pre0.get("private"), pre1.get("private")])
                meta["attribution_used"] = True
            except Exception:
                shadow_state = None

    rows: List[Dict[str, Any]] = []
    anchor = WIN_STEP_LO - 1                     # 503=day20 日终
    if anchor >= 0 and (anchor in s0 or anchor in s1):
        rows.append({"step": anchor, "day": anchor // TURN,
                     "cash": _money(our_seat, anchor),
                     "opp_cash": _money(1 - our_seat, anchor)})
    for step in range(WIN_STEP_LO, WIN_STEP_HI):
        if step not in s0 and step not in s1:
            continue
        obs0 = s0.get(step, (None, None))[0]
        obs1 = s1.get(step, (None, None))[0]
        row: Dict[str, Any] = {
            "step": step, "day": step // TURN,
            "cash": _money(our_seat, step),
            "opp_cash": _money(1 - our_seat, step),
        }
        if shadow_state is not None and obs0 and obs1:
            acts = [s0.get(step, (None, None))[1],
                    s1.get(step, (None, None))[1]]
            try:
                post, attr = rp._s_step(shadow_state, acts, step, _SHADOW_CFG,
                                        int(seed))
                nxt0 = s0.get(step + 1, (None, None))[0]
                nxt1 = s1.get(step + 1, (None, None))[0]
                if nxt0 and nxt1:
                    diff = rp._s_compare(
                        post, nxt0,
                        [nxt0.get("private"), nxt1.get("private")])
                    if diff:
                        meta["attribution_mismatches"] += 1
                        shadow_state = rp._s_snapshot(
                            nxt0, [nxt0.get("private"), nxt1.get("private")])
                    else:
                        shadow_state = post
                else:
                    shadow_state = post
                acc = _sell_rows_from_attr(attr, our_seat)
                if acc:
                    row["orders"] = acc["orders"]
                    row["qty"] = acc["qty"]
                    row["filled_orders"] = acc["filled_orders"]
                    row["vol"] = acc["vol"]
                    row["turnover"] = acc["turnover"]
            except Exception:
                meta["attribution_mismatches"] += 1
        rows.append(row)
    return rows, meta


def _states_from_replay(replay: Mapping[str, Any], seat: int,
                        seed: int) -> Tuple[List[Dict[str, Any]],
                                            Dict[str, Any]]:
    """原局 replay→某席 d21-28 状态行（replay si t=state_t；拍动作=si t+1）。"""
    steps = replay.get("steps") or []
    traces: Dict[int, List[Any]] = {0: [], 1: []}
    for s in range(max(0, WIN_STEP_LO - 1), min(len(steps), WIN_STEP_HI + 1)):
        for pl in (0, 1):
            if s >= len(steps) or not isinstance(steps[s], list) \
                    or pl >= len(steps[s]):
                continue
            entry = steps[s][pl] or {}
            obs = _obs_dict(entry.get("observation") or {})
            nxt = s + 1
            act = None
            if nxt < len(steps) and isinstance(steps[nxt], list) \
                    and pl < len(steps[nxt]):
                act = (steps[nxt][pl] or {}).get("action")
            traces[pl].append((s, obs, act))
    return _window_states(traces, seat, seed)


# ============================================================ 语料面 --

def _find_replay(episode: int, pull_missing: bool) -> Optional[Path]:
    for d in REPLAY_CACHE_DIRS:
        p = Path(d) / f"episode-{episode}-replay.json"
        if p.is_file() and p.stat().st_size > 0:
            return p
    if pull_missing and os.path.isfile(KAGGLE_BIN):
        Path(PULL_DIR).mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run([KAGGLE_BIN, "competitions", "replay",
                            str(episode)], cwd=PULL_DIR, timeout=120,
                           capture_output=True)
        except Exception:
            pass
        p = Path(PULL_DIR) / f"episode-{episode}-replay.json"
        if p.is_file() and p.stat().st_size > 0:
            return p
    return None


def _load_items(corpus: Any) -> List[Dict[str, Any]]:
    """语料→败局条目（episode id/replay 路径；缓存查找+可选拉取）。

    条目级预检不合法/文件缺失/重复→ValueError（fail-closed，judge_predict
    同则）；输出 [{episode, path, seed, our_seat, opp_actions, n_steps}]。
    """
    if corpus is None or isinstance(corpus, (str, bytes, Mapping)):
        raise ValueError("corpus 须为条目序列")
    entries = list(corpus)
    if not entries:
        raise ValueError("corpus 为空")
    items: List[Dict[str, Any]] = []
    seen: set = set()
    for entry in entries:
        if isinstance(entry, bool):
            raise ValueError(f"corpus 条目非法（bool）: {entry!r}")
        if isinstance(entry, int):
            ep = int(entry)
            path = _find_replay(ep, DEFAULT_BENCH["pull_missing"])
            if path is None:
                raise ValueError(f"corpus 条目 replay 缺失: {entry!r}")
        elif isinstance(entry, (str, Path)):
            p = Path(str(entry))
            if not p.is_file():
                raise ValueError(f"corpus 条目文件缺失: {entry!r}")
            path = p
        else:
            raise ValueError(f"corpus 条目非法: {entry!r}")
        try:
            replay = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise ValueError(f"corpus 条目解析失败 {path}: {exc}") from exc
        if not isinstance(replay, Mapping) or not isinstance(
                replay.get("steps"), list) or not replay["steps"]:
            raise ValueError(f"corpus 条目缺 steps: {path}")
        info = replay.get("info") or {}
        conf = replay.get("configuration") or {}
        seed = info.get("seed")
        if seed is None:
            seed = conf.get("seed")
        if seed is None:
            raise ValueError(f"corpus 条目缺 seed: {path}")
        ep = info.get("EpisodeId")
        if ep is None:
            stem = path.name.split("-")
            ep = int(stem[1]) if len(stem) > 1 and stem[1].isdigit() else -1
        ep = int(ep)
        if ep in seen:
            raise ValueError(f"corpus 条目重复: {ep}")
        seen.add(ep)
        teams = list(info.get("TeamNames") or [])
        our_seat = teams.index("renyxin") if "renyxin" in teams else 0
        opp_seat = 1 - our_seat
        steps = replay["steps"]
        opp_actions = []
        for s in range(len(steps)):
            act = None
            if isinstance(steps[s], list) and opp_seat < len(steps[s]):
                act = (steps[s][opp_seat] or {}).get("action")
            opp_actions.append(act)
        items.append({"episode": ep, "path": str(path), "seed": int(seed),
                      "our_seat": int(our_seat), "opp_actions": opp_actions,
                      "n_steps": len(steps)})
    return items


# ============================================================ 跑口（并行） --

def _build_agents(spec: Mapping[str, Any]
                  ) -> Tuple[List[Any], Optional[Dict[int, List[Any]]]]:
    """局规格→(agents, traces)。traces 非 None=该局逐拍追踪。"""
    out: List[Any] = []
    sinks: Optional[Dict[int, List[Any]]] = None
    if spec.get("trace"):
        sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        kind = a.get("type")
        if kind == "tape":
            inner: Any = _TapeAgent(a.get("actions") or [])
        elif kind in ("candidate", "python", "path"):
            inner = _load_entry(a.get("path"))
        else:
            raise ValueError(f"agent 规格非法: {a!r}")
        if sinks is not None:
            out.append(_Tracer(inner, seat, sinks[seat]))
        else:
            out.append(inner)
    return out, sinks


def _run_chunk(payload: Mapping[str, Any]) -> Dict[str, Any]:
    """worker：一批局跑 run_games（判决跑口），追踪局补状态行。"""
    specs = payload["specs"]
    cfg = dict(payload["cfg"] or {})
    try:
        from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    except ImportError:
        import sim_bridge as sb  # type: ignore
    games: List[Dict[str, Any]] = []
    metas: List[Tuple[Dict[str, Any], Optional[Dict[int, List[Any]]]]] = []
    build_errors: Dict[str, str] = {}
    for spec in specs:
        try:
            agents, sinks = _build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            agents, sinks = [], None
            games.append({"seed": int(spec["seed"]), "agents": []})
            build_errors[spec["game_id"]] = \
                f"{type(exc).__name__}: {exc}"
        metas.append((spec, sinks))
    t0 = time.perf_counter()
    res = sb.run_games(games, cfg) if games else {"games": [], "engine": None}
    elapsed = time.perf_counter() - t0
    run_rows = list(res.get("games") or [])
    rows: List[Dict[str, Any]] = []
    for i, (spec, sinks) in enumerate(metas):
        rr = run_rows[i] if i < len(run_rows) else {}
        row: Dict[str, Any] = {
            "game_id": spec["game_id"], "seed": int(spec["seed"]),
            "kind": spec.get("kind"), "arm": spec.get("arm"),
            "our_seat": int(spec.get("our_seat", 0)),
            "episode": spec.get("episode"),
            "banks": rr.get("banks"), "error": rr.get("error"),
            "elapsed_s": rr.get("elapsed_s"),
            "states": None, "attribution": None,
        }
        if spec["game_id"] in build_errors:
            row["error"] = build_errors[spec["game_id"]]
        if sinks is not None and row["error"] is None:
            try:
                st, meta = _window_states(sinks, int(spec["our_seat"]),
                                          int(spec["seed"]))
                row["states"] = st
                row["attribution"] = meta
            except Exception as exc:
                row["states"] = None
                row["attribution"] = {
                    "error": f"{type(exc).__name__}: {exc}"}
        rows.append(row)
    return {"rows": rows, "engine": res.get("engine"), "elapsed_s": elapsed,
            "fallback_reason": res.get("fallback_reason")}


def _chunked(specs: Sequence[Dict[str, Any]], n_chunks: int
             ) -> List[List[Dict[str, Any]]]:
    n_chunks = max(1, min(int(n_chunks), max(1, len(specs))))
    out: List[List[Dict[str, Any]]] = [[] for _ in range(n_chunks)]
    for i, spec in enumerate(specs):
        out[i % n_chunks].append(spec)
    return [c for c in out if c]


def _play_batch(specs: Sequence[Dict[str, Any]], cfg: Mapping[str, Any]
                ) -> List[Dict[str, Any]]:
    """并行判决跑口（workers 口径=调研 16x 并行）；红局计入不短路。"""
    specs = list(specs)
    workers = int(cfg.get("workers", 16))
    tasks = [{"specs": chunk, "cfg": dict(cfg)}
             for chunk in _chunked(specs, workers * 2)]
    if workers <= 1 or len(tasks) <= 1:
        results = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            results = pool.map(_run_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    for res in results:
        rows.extend(res["rows"])
    return rows


def _measure_speedup(specs: Sequence[Dict[str, Any]],
                     cfg: Mapping[str, Any]) -> Dict[str, Any]:
    """判决提速实测（同批局三次实跑，零外推）：

    - speedup（主口径=判决提速）=official 串行墙钟（改4 前判决口径：官方引
      擎逐局串行）/本判决并行墙钟（仿真器+workers 并行跑口）；
    - speedup_parallel=同引擎（仿真器）串行/并行（纯并行 workers 口径）；
    - speedup_engine=official/仿真器 同串行（纯引擎口径）。
    """
    specs = list(specs)
    if not specs:
        return {"speedup": None, "speedup_parallel": None,
                "speedup_engine": None, "serial_wall_s": None,
                "parallel_wall_s": None, "n_games": 0, "workers": 0}
    workers = int(cfg.get("workers", 16))
    off_cfg = dict(cfg)
    off_cfg["engine"] = "official"
    off_cfg.pop("bridge", None)
    t0 = time.perf_counter()
    _run_chunk({"specs": specs, "cfg": off_cfg})
    official = time.perf_counter() - t0
    t0 = time.perf_counter()
    _run_chunk({"specs": specs, "cfg": dict(cfg)})
    serial = time.perf_counter() - t0
    t0 = time.perf_counter()
    _play_batch(specs, cfg)
    parallel = time.perf_counter() - t0

    def _ratio(a: float, b: float) -> Optional[float]:
        return round(a / b, 3) if b and b > 0 else None

    return {"speedup": _ratio(official, parallel),
            "speedup_parallel": _ratio(serial, parallel),
            "speedup_engine": _ratio(official, serial),
            "official_wall_s": round(official, 3),
            "serial_wall_s": round(serial, 3),
            "parallel_wall_s": round(parallel, 3),
            "n_games": len(specs), "workers": workers,
            "sec_per_game_official": round(official / len(specs), 4),
            "sec_per_game_serial": round(serial / len(specs), 4),
            "baseline": ("official 串行判决（改4 前口径）→本判决"
                         "（仿真器+workers 并行跑口）")}


def _bridge_crosscheck(cfg: Mapping[str, Any], corpus: Sequence[int]
                       ) -> Dict[str, Any]:
    """仿真器对照：sim_bridge 抽样 ≥30 局双引擎逐局终局资金一致率。"""
    try:
        from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    except ImportError:
        import sim_bridge as sb  # type: ignore
    bcfg = dict(cfg.get("bridge_config") or {})
    bcfg.setdefault("n_games", int(cfg.get("n_bridge_games", 30)))
    bcfg.setdefault("min_checked", int(cfg.get("n_bridge_games", 30)))
    return sb.sim_bridge(config=bcfg, corpus=list(corpus))


# ============================================================ 聚合面 --

def _seed_result(games: Sequence[Mapping[str, Any]]
                 ) -> Tuple[str, bool]:
    """同 seed 双席局→(win/draw/loss, 有决胜)。红局计负（fail-closed）。"""
    won = lost = drawn = 0
    for g in games:
        banks = g.get("banks")
        seat = int(g.get("our_seat", 0))
        if g.get("error") or not isinstance(banks, (list, tuple)) \
                or len(banks) != 2 or any(b is None for b in banks):
            lost += 1
            continue
        mine, theirs = float(banks[seat]), float(banks[1 - seat])
        if mine > theirs:
            won += 1
        elif mine < theirs:
            lost += 1
        else:
            drawn += 1
    if won >= 2:
        return "win", True
    if lost >= 2:
        return "loss", True
    return "draw", (won + lost) > 0


def _arm_rate(games: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    """臂级 seed 口径胜率（judge_league 同构）。"""
    by_seed: Dict[Any, List[Mapping[str, Any]]] = {}
    for g in games:
        by_seed.setdefault(g["seed"], []).append(g)
    n_w = n_d = n_l = 0
    decisive = 0
    for _seed, gs in sorted(by_seed.items()):
        res, dec = _seed_result(gs)
        decisive += 1 if dec else 0
        if res == "win":
            n_w += 1
        elif res == "loss":
            n_l += 1
        else:
            n_d += 1
    n = len(by_seed)
    if n == 0 or decisive == 0:
        rate = 0.0
    else:
        rate = (n_w + 0.5 * n_d) / n
    game_wins = 0
    game_n = 0
    for g in games:
        banks = g.get("banks")
        seat = int(g.get("our_seat", 0))
        if g.get("error") or not isinstance(banks, (list, tuple)) \
                or len(banks) != 2 or any(b is None for b in banks):
            game_n += 1
            continue
        game_n += 1
        if float(banks[seat]) > float(banks[1 - seat]):
            game_wins += 1
    return {"n_seeds": n, "n_games": len(games), "seed_W": n_w,
            "seed_D": n_d, "seed_L": n_l, "decisive_seeds": decisive,
            "rate": round(rate, 4), "game_wins": game_wins,
            "game_win_rate": round(game_wins / game_n, 4) if game_n
            else None}


def _median(vals: Sequence[Any]) -> Optional[float]:
    xs = [v for v in (_num(x) for x in vals) if v is not None]
    return round(float(statistics.median(xs)), 2) if xs else None


def _resolve_pkg(pkg_path: Any) -> Dict[str, Any]:
    p = Path(str(pkg_path))
    if p.is_dir():
        p = p / "main.py"
    if not p.is_file():
        raise FileNotFoundError(f"pkg main.py 不可得: {p}")
    return {"main": str(p), "sha256": hashlib.sha256(
        p.read_bytes()).hexdigest()}


def _resolve_bench(bench: Any) -> Dict[str, Any]:
    if bench is None:
        cfg = copy.deepcopy(DEFAULT_BENCH)
    elif isinstance(bench, Mapping):
        cfg = copy.deepcopy(DEFAULT_BENCH)
        for k, v in bench.items():
            if k not in DEFAULT_BENCH:
                raise ValueError(f"bench 未知键: {k}")
            cfg[k] = v
    else:
        raise ValueError("bench 须为 Mapping 或 None")
    n_games = cfg.get("n_games")
    if isinstance(n_games, bool) or not isinstance(n_games, int) \
            or n_games < 2 or n_games % 2:
        raise ValueError(f"n_games 须为 ≥2 偶数（双席计）: {n_games!r}")
    workers = cfg.get("workers")
    if isinstance(workers, bool) or not isinstance(workers, int) \
            or workers < 1:
        raise ValueError(f"workers 须为 ≥1 整数: {workers!r}")
    if cfg.get("engine") not in ("auto", "sim", "official"):
        raise ValueError(f"engine 非法: {cfg.get('engine')!r}")
    for key in ("speed_probe_games", "n_bridge_games"):
        v = cfg.get(key)
        if isinstance(v, bool) or not isinstance(v, int) or v < 1:
            raise ValueError(f"{key} 须为 ≥1 整数: {v!r}")
    if not isinstance(cfg.get("bridge_config"), Mapping):
        raise ValueError("bridge_config 须为 Mapping")
    if not isinstance(cfg.get("seed_bases"), Mapping):
        raise ValueError("seed_bases 须为 Mapping")
    opps = cfg.get("opponents")
    if opps is None:
        opps = [str(KSIM_DIR / rel) for rel in DEFAULT_OPPONENTS]
    if not isinstance(opps, (list, tuple)) or not opps:
        raise ValueError("opponents 须为非空路径序列")
    resolved = []
    for o in opps:
        po = Path(str(o))
        if not po.is_file():
            raise ValueError(f"opponent 件缺失: {o}")
        resolved.append(str(po))
    cfg["opponents"] = resolved
    return cfg


def _league_specs(pkg: Mapping[str, Any], cfg: Mapping[str, Any]
                  ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """联赛局表：主对 h2h（=opponents[0]=r37）+强对手臂+mirror，独立 seed。"""
    n_seeds_total = int(cfg["n_games"]) // 2
    n_h2h = max(1, round(0.4 * n_seeds_total))
    n_mirror = max(1, round(0.2 * n_seeds_total))
    n_strong = max(0, n_seeds_total - n_h2h - n_mirror)
    strong_paths = list(cfg["opponents"][1:])
    bases = cfg["seed_bases"]
    specs: List[Dict[str, Any]] = []
    arms: Dict[str, Any] = {}

    def _arm(name: str, opp: Mapping[str, Any], base: int, n: int) -> None:
        seeds = [int(base) + i for i in range(n)]
        arms[name] = {"opponent": opp, "seeds": seeds}
        for seed in seeds:
            for seat in (0, 1):
                a_seat = {"type": "candidate", "path": pkg["main"]}
                b_seat = dict(opp)
                agents = [a_seat, b_seat] if seat == 0 else [b_seat, a_seat]
                specs.append({
                    "game_id": f"lg-{name}-{seed}-s{seat}", "seed": seed,
                    "kind": "league", "arm": name, "our_seat": seat,
                    "trace": False, "agents": agents})

    _arm("h2h_r37", {"type": "python", "path": cfg["opponents"][0]},
         int(bases.get("h2h", 510000)), n_h2h)
    if strong_paths:
        per = n_strong // len(strong_paths)
        for j, path in enumerate(strong_paths):
            n = per + (1 if j < n_strong % len(strong_paths) else 0)
            if n <= 0:
                continue
            _arm(f"strong_{Path(path).parent.name}_{j}",
                 {"type": "python", "path": path},
                 int(bases.get("strong", 520000)) + j * 1000, n)
    _arm("mirror", {"type": "candidate", "path": pkg["main"]},
         int(bases.get("mirror", 530000)), n_mirror)
    return specs, arms


# ============================================================ judge_r23 --

def judge_r23(pkg_path: str, corpus: Any, bench: Any = None) -> Dict[str, Any]:
    """判决 v23：败局定向重演+联赛+分段统计+仿真器对照，聚合分项+总判。

    签名意图：输入: r40 包+语料+副证配置 / 输出: evidence JSON /
    错误: 单局红计入不短路。

    口径见模块 docstring；六判据=c1 改1（榜前550段胜率≥30% ∧ 段资金差转正）
    /c2 改2（段资金差中位≥+3,600 ∧ 实现单价+3%）/c3 改3（有效挂单占比≥90%
    ∧ 单价+2%）/c4 改4（判决提速≥10x ∧ 对照一致100%）/c5 总判h2h（vs r37
    ≥0.55）/c6 总判联赛（总胜率≥85%）；overall=六判据全真。evidence 由本
    函数返回不落盘；单局红/异常计入 errors 不短路全跑。
    """
    t_start = time.perf_counter()
    pkg = _resolve_pkg(pkg_path)
    cfg = _resolve_bench(bench)
    items = _load_items(corpus)

    errors: List[Dict[str, Any]] = []
    # ---- 原局基线（逐席自比） ----
    baselines: Dict[Any, Dict[int, Dict[str, Any]]] = {}
    for it in items:
        try:
            replay = json.loads(Path(it["path"]).read_text(encoding="utf-8"))
            per_seat: Dict[int, Dict[str, Any]] = {}
            for seat in (0, 1):
                rows, _meta = _states_from_replay(replay, seat, it["seed"])
                per_seat[seat] = segment_stats(rows)
            baselines[it["episode"]] = per_seat
        except Exception as exc:
            errors.append({"scope": "baseline", "episode": it["episode"],
                           "error": f"{type(exc).__name__}: {exc}"})

    # ---- 局表：败局定向重演（双席位）+联赛 ----
    specs: List[Dict[str, Any]] = []
    for it in items:
        tape = {"type": "tape", "actions": it["opp_actions"]}
        cand = {"type": "candidate", "path": pkg["main"]}
        for seat in (0, 1):
            agents = [cand, tape] if seat == 0 else [tape, cand]
            specs.append({
                "game_id": f"dir-{it['episode']}-s{seat}", "seed": it["seed"],
                "kind": "directed", "arm": "loss_replay", "our_seat": seat,
                "episode": it["episode"], "trace": True, "agents": agents})
    league_specs, arms = _league_specs(pkg, cfg)
    specs.extend(league_specs)

    # ---- 对照（先证桥，判决跑口才可用仿真器）+跑口（并行）+提速 ----
    all_seeds = sorted({int(s["seed"]) for s in specs})
    bridge = _bridge_crosscheck(cfg, all_seeds)
    if bridge.get("degraded"):
        errors.append({"scope": "bridge",
                       "error": bridge.get("degraded_reason") or "degraded"})
    run_cfg = dict(cfg)
    run_cfg["bridge"] = bridge
    rows = _play_batch(specs, run_cfg)
    for r in rows:
        if r.get("error"):
            errors.append({"scope": "game", "game_id": r["game_id"],
                           "seed": r["seed"], "error": r["error"]})
    probe = list(league_specs)[:int(cfg["speed_probe_games"])]
    speed = _measure_speedup(probe, run_cfg)

    # ---- 分段统计（败局定向重演局 vs 同席原局基线） ----
    per_game: List[Dict[str, Any]] = []
    for r in rows:
        if r.get("kind") != "directed":
            continue
        base = (baselines.get(r.get("episode")) or {}).get(
            int(r["our_seat"]))
        try:
            st = segment_stats(r.get("states") or [], baseline=base)
        except Exception as exc:                       # 红计入不短路
            st = None
            errors.append({"scope": "segment", "game_id": r["game_id"],
                           "error": f"{type(exc).__name__}: {exc}"})
        banks = r.get("banks")
        seat = int(r["our_seat"])
        margin = None
        if isinstance(banks, (list, tuple)) and len(banks) == 2 \
                and all(b is not None for b in banks):
            margin = float(banks[seat]) - float(banks[1 - seat])
        per_game.append({
            "game_id": r["game_id"], "seed": r["seed"], "our_seat": seat,
            "red": bool(r.get("error")), "margin": margin,
            "win": (margin is not None and margin > 0),
            "readings": ({k: st[k] for k in _METRICS} if st else
                         {k: UNKNOWN for k in _METRICS}),
            "up_pct": (st or {}).get("verdict", {}).get("realized_px_up_pct"),
            "attribution": r.get("attribution"),
        })

    seg_deltas = [g["readings"]["seg_delta"] for g in per_game]
    fills = [g["readings"]["fill_rate"] for g in per_game]
    lots = [g["readings"]["lot_size"] for g in per_game]
    px_up = [g["up_pct"] for g in per_game]
    seg_median = _median(seg_deltas)
    fill_median = _median(fills)
    lot_median = _median(lots)
    px_up_median = _median(px_up)
    n_dir = len(per_game)
    n_red = sum(1 for g in per_game if g["red"])

    def _complete(vals: Sequence[Any]) -> bool:
        return bool(vals) and all(_num(v) is not None for v in vals)

    seg_ok_data = _complete(seg_deltas) and n_red == 0
    px_ok_data = _complete(px_up) and n_red == 0
    fill_ok_data = _complete(fills) and n_red == 0

    # ---- 胜率（seed 口径） ----
    league_rows = [r for r in rows if r.get("kind") == "league"]
    by_arm: Dict[str, List[Mapping[str, Any]]] = {}
    for r in league_rows:
        by_arm.setdefault(str(r["arm"]), []).append(r)
    arm_rates = {name: _arm_rate(gs) for name, gs in sorted(by_arm.items())}
    strong_names = [n for n in arm_rates if n.startswith("strong_")
                    or n == "h2h_r37"]
    strong_games = [r for r in league_rows if str(r["arm"]) in strong_names]
    top550 = _arm_rate(strong_games) if strong_games else {
        "rate": 0.0, "n_seeds": 0}
    league_rate = _arm_rate(league_rows) if league_rows else {
        "rate": 0.0, "n_seeds": 0}
    h2h = arm_rates.get("h2h_r37", {"rate": 0.0, "n_seeds": 0})

    # ---- 六判据 ----
    c1_readings = {"top550_winrate": top550.get("rate"),
                   "top550_baseline": "0/5（分析24 榜前550对手基线）",
                   "seg_delta_median": seg_median}
    c1_pass = (bool(top550.get("rate") is not None
                    and top550["rate"] >= T_TOP550_WINRATE)
               and seg_ok_data
               and bool(seg_median is not None
                        and seg_median > T_SEG_POSITIVE))
    c2_readings = {"seg_delta_median": seg_median,
                   "realized_px_up_pct": px_up_median,
                   "n_games": n_dir, "n_red": n_red}
    c2_pass = (seg_ok_data and px_ok_data
               and bool(seg_median is not None
                        and seg_median >= T_SEG_DELTA_MEDIAN)
               and bool(px_up_median is not None
                        and px_up_median >= T_REALIZED_PX_UP_PCT))
    c3_readings = {"fill_rate": fill_median,
                   "realized_px_up_pct": px_up_median,
                   "n_games": n_dir, "n_red": n_red}
    c3_pass = (fill_ok_data and px_ok_data
               and bool(fill_median is not None
                        and fill_median >= T_FILL_RATE)
               and bool(px_up_median is not None
                        and px_up_median >= T_PX_UP_PCT))
    speedup = speed.get("speedup")
    consistency = bridge.get("consistency") or {}
    c4_readings = {"speedup": speedup,
                   "speedup_parallel": speed.get("speedup_parallel"),
                   "speedup_engine": speed.get("speedup_engine"),
                   "consistency_rate": consistency.get("rate"),
                   "n_checked": consistency.get("n_checked"),
                   "consistency_ok": bridge.get("consistency_ok"),
                   "bridge_engine": bridge.get("engine")}
    c4_pass = (bool(speedup is not None and speedup >= T_SPEEDUP)
               and bool(bridge.get("consistency_ok"))
               and consistency.get("rate") == 1.0)
    c5_readings = {"h2h_rate": h2h.get("rate"), "n_seeds": h2h.get("n_seeds")}
    c5_pass = bool(h2h.get("rate") is not None
                   and h2h["rate"] >= T_H2H_RATE)
    c6_readings = {"league_winrate": league_rate.get("rate"),
                   "n_seeds": league_rate.get("n_seeds"),
                   "n_games": league_rate.get("n_games")}
    c6_pass = bool(league_rate.get("rate") is not None
                   and league_rate["rate"] >= T_LEAGUE_WINRATE)

    criteria = {
        "c1_rebuild_route": {
            "label": "改1（条件路由/同开拼接）",
            "threshold": "榜前550段胜率≥30%（基线0/5）∧ d21-28段资金差转正",
            "readings": c1_readings, "pass": bool(c1_pass)},
        "c2_sell_exec": {
            "label": "改2（卖货执行/批量化）",
            "threshold": "d21-28段资金差中位≥+3,600（胜局基线半）∧ 实现单价+3%",
            "readings": c2_readings, "pass": bool(c2_pass)},
        "c3_queue_hygiene": {
            "label": "改3（队列补洞）",
            "threshold": "有效挂单占比≥90% ∧ 单价+2%",
            "readings": c3_readings, "pass": bool(c3_pass)},
        "c4_sim_judge": {
            "label": "改4（Rust 仿真器判决基建）",
            "threshold": "判决提速≥10x（official串行判决→本判决并行跑口）"
                         "∧ 仿真器对照一致100%",
            "readings": c4_readings, "pass": bool(c4_pass)},
        "c5_h2h_r37": {
            "label": "总判·h2h vs r37",
            "threshold": "h2h vs r37（独立seed n）≥0.55",
            "readings": c5_readings, "pass": bool(c5_pass)},
        "c6_league_winrate": {
            "label": "总判·联赛总胜率",
            "threshold": "联赛总胜率≥85%",
            "readings": c6_readings, "pass": bool(c6_pass)},
    }
    failed = [k for k, v in criteria.items() if not v["pass"]]
    evidence: Dict[str, Any] = {
        "judge": "judge_r23",
        "version": RECORD_VERSION,
        "generated_at": datetime.now(timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"),
        "pkg": pkg,
        "config": {
            "corpus": [it["episode"] for it in items],
            "corpus_paths": [it["path"] for it in items],
            "bench": {k: v for k, v in cfg.items()},
            "engine": bridge.get("engine"),
            "workers": cfg.get("workers"),
        },
        "counts": {
            "directed_games": n_dir, "directed_red": n_red,
            "league_games": len(league_rows),
            "league_seeds": league_rate.get("n_seeds"),
            "h2h_seeds": h2h.get("n_seeds"),
            "top550_seeds": top550.get("n_seeds"),
            "mirror_seeds": (arm_rates.get("mirror") or {}).get("n_seeds"),
        },
        "readings": {
            "directed": {
                "seg_delta_median": seg_median,
                "seg_delta_values": seg_deltas,
                "realized_px_up_pct_median": px_up_median,
                "fill_rate_median": fill_median,
                "lot_size_median": lot_median,
                "per_game": per_game,
            },
            "league": {
                "arms": arm_rates,
                "top550_winrate": top550.get("rate"),
                "top550_detail": top550,
                "league_winrate": league_rate.get("rate"),
                "league_detail": league_rate,
                "h2h_rate": h2h.get("rate"),
                "h2h_detail": h2h,
            },
            "speed": speed,
            "bridge": {
                "consistency": consistency,
                "consistency_ok": bridge.get("consistency_ok"),
                "engine": bridge.get("engine"),
                "wall_speedup": bridge.get("wall_speedup"),
                "degraded": bridge.get("degraded"),
                "degraded_reason": bridge.get("degraded_reason"),
            },
        },
        "criteria": criteria,
        "overall": {
            "pass": not failed,
            "n_pass": len(criteria) - len(failed),
            "failed": failed,
        },
        "errors": errors,
        "source": {
            "rerun_command": (
                "python3 -c \"from orderbook_r40.judge_r23 import "
                "judge_r23; judge_r23('<pkg>', <corpus>, <bench>)\""),
            "seeds": {"directed": [it["seed"] for it in items],
                      "league": {n: a.get("seeds") for n, a in arms.items()}},
        },
        "elapsed_s": round(time.perf_counter() - t_start, 3),
    }
    return evidence
