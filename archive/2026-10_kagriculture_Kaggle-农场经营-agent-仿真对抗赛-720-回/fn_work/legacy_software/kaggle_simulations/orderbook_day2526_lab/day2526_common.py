# -*- coding: utf-8 -*-
"""day2526_common：d25/26 单日凹陷攻坚共用件（新 lab；不改既有代码）。

职责：件装载（末 callable + 台账 ns 捕获）、逐拍追踪（obs/act/遥测）、
影子引擎逐拍成交归因（kgenv.replay_profile 同 judge_milkwin 口径）、
d25/26 解剖记录。判决口径与 judge_milkwin 一致（fill=影子引擎逐拍归因、
submit=挂单 qty×卖时市价、终局钱 farms[obs.player]）。
只写 orderbook_day2526_lab/ 与 fn_docs/hybrid/results/2026-09-30-day2526.json。
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

DAY = 24
WINDOW = (336, 648)                 # d14-27 窗（step 右开）
WIN_DAYS = tuple(range(14, 27))
FOCUS = (576, 624)                  # d25/26 解剖窗（step 576-624 右开）
FOCUS_DAYS = (25, 26)

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
LOSS_FOLDS = REPLAY_26[:8]

DROP_HALF_MAIN = str(KSIM_DIR / "orderbook_unified_u2_lab" / "build" /
                     "u2v2_drop_half" / "main.py")
DROP_HALF_SHA = ("5d2d12468a5d1ec53c3d3e4726de54e6a5d29eb038fc97ca45c72b2c"
                 "e7992df0")
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
               / "main.py")
MX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
ALL_ITEMS = ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON", "EGG",
             "MILK", "WOOL", "FERTILIZER")

EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-day2526.json"
EVID_DIR = MODULE_DIR / "evidence"

_SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}


# ------------------------------------------------------------ 观测量 --
def to_plain(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): to_plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_plain(v) for v in x]
    return x


def obs_dict(obs: Any) -> Dict[str, Any]:
    if isinstance(obs, dict):
        return obs
    out: Dict[str, Any] = {}
    for key in ("player", "step", "day", "hour", "market", "farms",
                "private", "opponent", "town"):
        try:
            out[key] = to_plain(getattr(obs, key))
        except Exception:
            continue
    return out


def num(v: Any) -> Optional[float]:
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def obs_step(obs: Any) -> int:
    d = obs if isinstance(obs, dict) else obs_dict(obs)
    s = num(d.get("step"))
    if s is not None:
        return int(s)
    return int(num(d.get("day")) or 0) * DAY + int(num(d.get("hour")) or 0)


def call_inner(inner: Any, obs: Any, configuration: Any) -> Any:
    code = getattr(inner, "__code__", None)
    n = code.co_argcount if code is not None else 1
    args = [obs, configuration][:max(1, int(n))]
    return inner(*args)


def load_agent_ns(path: Any) -> Tuple[Any, Dict[str, Any]]:
    """单文件件装载（末 callable 语义）；返回 (entry, ns 全表)。"""
    p = os.path.abspath(str(path))
    if not os.path.isfile(p):
        raise FileNotFoundError("agent 文件不存在: %s" % p)
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
        raise ValueError("%s 装载后无 callable" % p)
    return entries[-1], ns


class Tracer:
    """观察/动作/台账逐拍追踪（不改动作）。"""

    def __init__(self, inner: Any, seat: int, sink: List[Any]):
        self.inner, self.seat, self.sink = inner, seat, sink

    def __call__(self, obs: Any, configuration: Any = None) -> Any:
        act = call_inner(self.inner, obs, configuration)
        self.sink.append((obs_step(obs), obs_dict(obs), act))
        return act


def stream_digest(sink) -> str:
    try:
        acts = [e[2] for e in (sink or [])]
        return hashlib.sha256(
            json.dumps(acts, default=str, sort_keys=True).encode()
        ).hexdigest()[:16]
    except Exception:
        return "err"


def end_reads(sink) -> Dict[str, Any]:
    """终局读数：终局钱 farms[obs.player].money（干净口径）+ 终局滞留。"""
    last_obs = None
    for entry in (sink or []):
        if isinstance(entry[1], dict):
            last_obs = entry[1]
    if not isinstance(last_obs, dict):
        return {"terminal_money": None, "stranding": None}
    try:
        player = int(last_obs.get("player", 0))
    except Exception:
        player = 0
    farms = last_obs.get("farms")
    tm = None
    if isinstance(farms, list) and player < len(farms) \
            and isinstance(farms[player], dict):
        try:
            tm = round(float(farms[player].get("money", 0.0)), 2)
        except (TypeError, ValueError):
            pass
    prices = ((last_obs.get("market") or {}) if isinstance(
        last_obs.get("market"), dict) else {}).get("prices") or {}
    shed = ((last_obs.get("private") or {}) if isinstance(
        last_obs.get("private"), dict) else {}).get("shed") or {}
    total = 0.0
    for item, qty in (shed or {}).items():
        px = prices.get(item, 0)
        try:
            total += float(px) * float(qty)
        except (TypeError, ValueError):
            continue
    return {"terminal_money": tm, "stranding": round(total, 2)}


# ------------------------------------------------------------ 影子引擎 --
def shadow_ticks(sinks, seed, keep=None):
    """影子引擎逐拍成交归因：返回 {step: {pl: [order,...]}} + mismatch 计数。

    order = {type,item,filled,value,remaining}（SELL/BUY 均留）。
    """
    try:
        base = str(KSIM_DIR.parent)
        if base not in sys.path:
            sys.path.insert(0, base)
        from kgenv import replay_profile as rp  # noqa: WPS433
    except Exception as exc:
        return {"error": repr(exc)[:120], "ticks": {}}
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            m[seat][int(entry[0])] = (entry[1], entry[2])
    steps = sorted(set(m[0]) | set(m[1]))
    if not steps:
        return {"error": "empty_traces", "ticks": {}}
    first = steps[0]
    pre0 = m[0].get(first, (None, None))[0] or m[1].get(first, (None, None))[0]
    pre1 = m[1].get(first, (None, None))[0] or pre0
    try:
        state = rp._s_snapshot(pre0, [pre0.get("private"),
                                      pre1.get("private")])
    except Exception as exc:
        return {"error": "snapshot: %r" % exc, "ticks": {}}
    ticks: Dict[int, Any] = {}
    mism = 0
    for s in steps:
        acts = [m[0].get(s, (None, None))[1], m[1].get(s, (None, None))[1]]
        acts = [a if isinstance(a, dict) else
                {"farmer": ["PASS"], "hands": [], "market": []} for a in acts]
        try:
            post, attr = rp._s_step(state, acts, s, _SHADOW_CFG, int(seed))
        except Exception:
            mism += 1
            continue
        rec = {}
        for pl in (0, 1):
            try:
                orders = attr["market"][pl]["orders"]
            except Exception:
                orders = []
            rec[pl] = [{"type": o.get("type"), "item": o.get("item"),
                        "filled": float(o.get("filled") or 0),
                        "value": float(o.get("value") or 0),
                        "remaining": o.get("remaining")}
                       for o in orders]
        ticks[s] = rec
        nxt = s + 1
        n0 = m[0].get(nxt, (None, None))[0]
        n1 = m[1].get(nxt, (None, None))[0]
        if n0 and n1:
            try:
                diff = rp._s_compare(post, n0,
                                     [n0.get("private"), n1.get("private")])
            except Exception:
                diff = ["compare_error"]
            if diff:
                mism += 1
                try:
                    state = rp._s_snapshot(n0, [n0.get("private"),
                                                n1.get("private")])
                except Exception:
                    state = post
            else:
                state = post
        else:
            state = post
    return {"ticks": ticks, "shadow_mismatch_steps": mism}


def submit_rows(act) -> List[Dict[str, Any]]:
    """动作里的市场指令（SELL/BUY）→ 结构行。"""
    out = []
    for cmd in (act.get("market") or []) if isinstance(act, dict) else []:
        if not (isinstance(cmd, (list, tuple)) and len(cmd) >= 3):
            continue
        op = str(cmd[0])
        if op not in ("SELL", "BUY"):
            continue
        try:
            q = float(cmd[2])
        except (TypeError, ValueError):
            continue
        out.append({"op": op, "item": str(cmd[1]), "qty": q})
    return out


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
