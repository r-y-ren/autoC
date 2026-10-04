# -*- coding: utf-8 -*-
"""judge_knee：谷底三品价格膝点量门实测（knee-gate；判决先行·不发射不提交）。

责任口径（任务 knee-gate）：
- 机制（knee 层，尾块注入沿 append 先例，基底=h1 件 sha 76b5f842…）：对
  FERTILIZER/MILK/WOOL 三品，本步 SELL 单量按价格膝点截留——膝点=价崩拐点
  （简单可实现口径：该品当前 quote<0.7×base），截留帽=min(沈存 30%, 步帽 X)
  （X=10/20 两变体）；quote>=0.7×base 全量挂卖；截留不是挪卖（只减不挪、
  零跨拍、磁带 blob 零触碰、异常回退原动作），截掉的量留在棚里由磁带后续
  卖单/终局清算（712-718）自然出清（终局清算窗 step>=712 不截留）。
- 判决：门禁四门（load/health/determinism/identity）+ knee 触发面统计
  （逐品截留量/触发步数）；变体 vs H1 配对（26 败局前 8 fold + 新中性
  672000+i*89×8，n=16 双席/变体；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转）；
  判据=净翻胜>0 ∧ flips_neg==0 ∧ 终局滞留不升（截留不能变死货）。
- 读数附分品实现价对照（FERT/MILK/WOOL vs base 口径 变体 vs H1）+ 终局钱
  （farms[obs.player].money 干净口径）。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤300 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-knee-gate.json；账本落
orderbook_knee_lab/evidence/。复用（不改写）：sim_bridge.run_games/sim_bridge、
gate_launch_fourgate_l1._redirect_check、kgenv.replay_profile 影子引擎、
judge_r23._load_entry。只写 orderbook_knee_lab/ 与 fn_docs/hybrid/results/
2026-09-29-knee-gate.json。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
L1_DIR = str(KSIM_DIR / "orderbook_l1_derivative")
if L1_DIR not in sys.path:
    sys.path.insert(0, L1_DIR)

RECORD_VERSION = "knee-gate/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
LOSS_FOLDS = REPLAY_26[:8]                       # 26 败局 canonical 前 8 fold
NEUTRAL_FOLDS = [672000 + i * 89 for i in range(8)]  # 任务给定新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS               # n=16 双席 fold/变体

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}
KNEE_ITEMS = ("FERTILIZER", "MILK", "WOOL")
CORNER_REF = {"FERTILIZER": 0.4518, "MILK": 0.5669, "WOOL": 0.599}  # 参照口径

H1_MAIN = str(KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py")
H1_SHA_EXPECTED = ("76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764"
                   "974b22f337")
FORM_MAINS = {
    "knee_x10": str(MODULE_DIR / "build" / "knee_x10" / "main.py"),
    "knee_x20": str(MODULE_DIR / "build" / "knee_x20" / "main.py"),
}
ARMS = {"h1": H1_MAIN, "knee_x10": FORM_MAINS["knee_x10"],
        "knee_x20": FORM_MAINS["knee_x20"]}
ENTRY_NAME = "_kg_agent"
FORMS = ("knee_x10", "knee_x20")

WORKERS = 2
BUDGET_CAP_GAMES = 300
EPISODE_SEEDS = (101, 102)
STEP_BUDGET_MS = 1000.0
SIZE_CAP_BYTES = 100 * 1024 * 1024
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-knee-gate.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "knee_ab_ledger.json"

_SHADOW_CFG = {
    "boardSize": 10, "turnsPerDay": 24, "shedCapacity": 100,
    "maxMarketOrdersPerTurn": 10, "farmHandCostMult": 1,
    "weedSpawnChance": 0.005, "townShopSellInterval": 4,
    "townCenterSellInterval": 24, "townShopUnlockInterval": 3,
    "startingMoney": 3000, "episodeSteps": 720,
}

EV: Dict[str, Any] = {}
ANOMALIES: List[str] = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_evid():
    """边跑边落盘（每次阶段完成即写）。"""
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------ 观测量 --
def _to_plain(x: Any) -> Any:
    if isinstance(x, dict):
        return {str(k): _to_plain(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_to_plain(v) for v in x]
    return x


def _obs_dict(obs: Any) -> Dict[str, Any]:
    if isinstance(obs, dict):
        return obs
    out: Dict[str, Any] = {}
    for key in ("player", "step", "day", "hour", "market", "farms",
                "private", "opponent"):
        try:
            out[key] = _to_plain(getattr(obs, key))
        except Exception:
            continue
    return out


def _num(v: Any):
    try:
        return float(v)
    except Exception:
        return None


def _obs_step(obs: Any) -> int:
    d = obs if isinstance(obs, dict) else _obs_dict(obs)
    s = _num(d.get("step"))
    if s is not None:
        return int(s)
    return int(_num(d.get("day")) or 0) * DAY + int(_num(d.get("hour")) or 0)


def _call_inner(inner: Any, obs: Any, configuration: Any) -> Any:
    code = getattr(inner, "__code__", None)
    n = code.co_argcount if code is not None else 1
    args = [obs, configuration][:max(1, int(n))]
    return inner(*args)


def _load_agent(path: Any):
    """单文件件装载（末 callable 语义）+ knee 台账报告字典（_KG_REPORT）。"""
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
    reports = {k: ns[k] for k in ("_KG_REPORT",)
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


def _snap_report(rep: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: v for k, v in rep.items() if k != "per_item"}
    per = {}
    for item, row in (rep.get("per_item") or {}).items():
        per[str(item)] = dict(row) if isinstance(row, dict) else row
    out["per_item"] = per
    return out


class _Tracer:
    """观察/动作/knee 台账逐拍追踪（不改动作）。"""

    def __init__(self, inner: Any, seat: int, sink: List[Any],
                 reports: Dict[str, Any]):
        self.inner, self.seat, self.sink, self.reports = inner, seat, sink, \
            reports

    def __call__(self, obs: Any, configuration: Any = None) -> Any:
        act = _call_inner(self.inner, obs, configuration)
        tel = {name: _snap_report(rep) for name, rep in self.reports.items()}
        self.sink.append((_obs_step(obs), _obs_dict(obs), act, tel))
        return act


# ------------------------------------------------------------ 读数 --
def item_reads(sink) -> Dict[str, Any]:
    """提交口径分品：Σ(qty_req×卖时市价) 与 Σ(qty_req×base)。"""
    out: Dict[str, Dict[str, float]] = {}
    for entry in (sink or []):
        obs, act = entry[1], entry[2]
        if not isinstance(obs, dict) or not isinstance(act, dict):
            continue
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        for cmd in (act.get("market") or []):
            if not (isinstance(cmd, (list, tuple)) and len(cmd) >= 3
                    and str(cmd[0]) == "SELL"):
                continue
            item = str(cmd[1])
            px = prices.get(item)
            try:
                q = float(cmd[2])
            except (TypeError, ValueError):
                continue
            if not isinstance(px, (int, float)):
                continue
            row = out.setdefault(item, {"req_qty": 0.0, "sub_value": 0.0})
            row["req_qty"] += q
            row["sub_value"] += q * float(px)
    return out


def shadow_items(sinks, seed) -> Dict[str, Any]:
    """影子引擎逐拍成交归因：分品 Σ(filled×成交价)=Σvalue / Σfilled。"""
    try:
        base = str(KSIM_DIR.parent)
        if base not in sys.path:
            sys.path.insert(0, base)
        from kgenv import replay_profile as rp  # noqa: WPS433
    except Exception as exc:
        return {"error": repr(exc)[:120]}
    m = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            m[seat][int(entry[0])] = (entry[1], entry[2])
    steps = sorted(set(m[0]) | set(m[1]))
    if not steps:
        return {"error": "empty_traces"}
    first = steps[0]
    pre0 = m[0].get(first, (None, None))[0] or m[1].get(first, (None, None))[0]
    pre1 = m[1].get(first, (None, None))[0] or pre0
    try:
        state = rp._s_snapshot(pre0, [pre0.get("private"),
                                      pre1.get("private")])
    except Exception as exc:
        return {"error": "snapshot: %r" % exc}
    acc: Dict[int, Dict[str, Dict[str, float]]] = {0: {}, 1: {}}
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
        for pl in (0, 1):
            try:
                orders = attr["market"][pl]["orders"]
            except Exception:
                continue
            for o in orders:
                if o.get("type") != "SELL":
                    continue
                item = str(o.get("item"))
                filled = float(o.get("filled") or 0)
                value = float(o.get("value") or 0)
                req = float(o.get("requested") or 0)
                row = acc[pl].setdefault(item, {"filled": 0.0, "value": 0.0,
                                                "req": 0.0})
                row["filled"] += filled
                row["value"] += value
                row["req"] += req
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
    return {"per_item_by_seat": acc, "shadow_mismatch_steps": mism}


def end_reads(sink) -> Dict[str, Any]:
    """终局读数：终局钱 farms[obs.player].money + 终局滞留（末拍 shed×quote）
    + 三品 end 棚存。"""
    last_obs = None
    for entry in (sink or []):
        if isinstance(entry[1], dict):
            last_obs = entry[1]
    if not isinstance(last_obs, dict):
        return {"terminal_money": UNKNOWN, "stranding": UNKNOWN,
                "shed_end": {}}
    try:
        player = int(last_obs.get("player", 0))
    except Exception:
        player = 0
    farms = last_obs.get("farms")
    tm = UNKNOWN
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
    shed_end: Dict[str, Any] = {}
    by_item: Dict[str, float] = {}
    for item, qty in (shed or {}).items():
        try:
            q = float(qty)
        except (TypeError, ValueError):
            continue
        px = prices.get(item, 0)
        try:
            v = float(px) * q
        except (TypeError, ValueError):
            v = 0.0
        total += v
        if str(item) in KNEE_ITEMS:
            shed_end[str(item)] = q
            by_item[str(item)] = round(v, 2)
    return {"terminal_money": tm, "stranding": round(total, 2),
            "stranding_knee_items": by_item, "shed_end": shed_end}


def knee_reads(sink) -> Dict[str, Any]:
    """knee 台账末拍累计（逐品截留量/触发步数；step0 复位→末拍=局总量）。"""
    last = None
    for entry in (sink or []):
        tel = entry[3] if len(entry) > 3 else None
        if isinstance(tel, dict) and isinstance(tel.get("_KG_REPORT"), dict):
            last = tel["_KG_REPORT"]
    if not isinstance(last, dict):
        return {"present": False}
    per = {}
    for item, row in (last.get("per_item") or {}).items():
        per[str(item)] = dict(row) if isinstance(row, dict) else row
    out = {k: v for k, v in last.items() if k != "per_item"}
    out["per_item"] = per
    out["present"] = True
    return out


# ------------------------------------------------------------ 局跑口 --
def _build_agents_kg(spec):
    out = []
    sinks = {0: [], 1: []}
    for seat, a in enumerate(spec["agents"]):
        inner, reports = _load_agent(a["path"])
        out.append(_Tracer(inner, seat, sinks[seat], reports))
    return out, sinks


def _run_chunk(payload):
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = _build_agents_kg(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "items": None, "shadow": None,
               "knee": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our, opp = sinks[row["seat"]], sinks[1 - row["seat"]]
            row["reads"] = end_reads(our)
            row["items"] = item_reads(our)
            row["knee"] = knee_reads(our)
            row["shadow"] = shadow_items(sinks, int(spec["seed"]))
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    chunks = [c for c in chunks if c]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_run_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    engines = []
    for part in parts:
        rows.extend(part["rows"])
        engines.append({"engine": part.get("engine"),
                        "fallback_reason": part.get("fallback_reason")})
    return rows, engines


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_672000_i89")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum})
    return units, opp_paths


def make_specs(arm, cand_path, units):
    specs = []
    for r in units:
        agents = [{"type": "python", "path": cand_path},
                  {"type": "python", "path": r["opp_path"]}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "kg-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


# ------------------------------------------------------------ 聚合 --
def pair_stats(ctl: Dict, var: Dict, kept_units: List[Dict]) -> Dict:
    """配对聚合：W-L-T（Δ 口径）/Δ/翻负/净翻胜（corner 同口径）。"""
    agg = {"n": 0, "w": 0, "l": 0, "t": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0,
           "loss_recovery": 0, "loss_recovery_n": 0, "rows_lite": []}
    for u in kept_units:
        key = (u["seed"], u["seat"])
        rc, rvv = ctl.get(key), var.get(key)
        if not rc or not rvv or rc.get("margin") is None \
                or rvv.get("margin") is None:
            continue
        mc, mv = float(rc["margin"]), float(rvv["margin"])
        d = mv - mc
        agg["n"] += 1
        agg["delta_sum"] += d
        agg["w" if d > 0 else "l" if d < 0 else "t"] += 1
        wc, wv = 1 if mc > 0 else 0, 1 if mv > 0 else 0
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
        if u["stratum"] == "loss_replay":
            agg["loss_recovery_n"] += 1
            if d > 0:
                agg["loss_recovery"] += 1
        agg["rows_lite"].append(
            {"seed": u["seed"], "seat": u["seat"], "stratum": u["stratum"],
             "opponent": u.get("opponent"), "margin_control": round(mc, 1),
             "margin_variant": round(mv, 1), "delta": round(d, 1)})
    n = max(1, agg["n"])
    out = {"n": agg["n"], "W": agg["w"], "L": agg["l"], "T": agg["t"],
           "mean_delta": round(agg["delta_sum"] / n, 2),
           "win_control": agg["win_control"], "win_variant": agg["win_variant"],
           "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
           "net_flip_wins": agg["win_variant"] - agg["win_control"],
           "loss_recovery": "%d/%d 败局 Δ>0" % (agg["loss_recovery"],
                                                agg["loss_recovery_n"]),
           "control_win_guard_ok": agg["flips_neg"] == 0,
           "rows_lite": agg["rows_lite"]}
    out["positive_arm"] = bool(out["net_flip_wins"] > 0
                               and out["control_win_guard_ok"])
    return out


def realized_agg(rows: List[Dict]) -> Dict[str, Any]:
    """分品实现价聚合：Σvalue/Σ(filled×base)（成交价口径）+ 提交口径。"""
    per: Dict[str, Dict[str, float]] = {}
    for r in rows:
        for item, row in (r.get("items") or {}).items():
            acc = per.setdefault(item, {"req_qty": 0.0, "sub_value": 0.0})
            acc["req_qty"] += float(row.get("req_qty") or 0)
            acc["sub_value"] += float(row.get("sub_value") or 0)
    sh: Dict[str, Dict[str, float]] = {}
    mism = 0
    for r in rows:
        s = r.get("shadow") or {}
        mism += int(s.get("shadow_mismatch_steps") or 0)
        side = int(r.get("seat", 0))
        by_seat = s.get("per_item_by_seat") or {}
        for item, row in (by_seat.get(side) or by_seat.get(str(side)) or {}
                          ).items():
            acc = sh.setdefault(item, {"filled": 0.0, "value": 0.0,
                                       "req": 0.0})
            acc["filled"] += float(row.get("filled") or 0)
            acc["value"] += float(row.get("value") or 0)
            acc["req"] += float(row.get("req") or 0)
    out_items = {}
    num_f = den_f = num_s = den_s = 0.0
    for item in sorted(set(per) | set(sh)):
        base = float(BASE_PX.get(item, 0) or 0)
        f = sh.get(item) or {}
        p = per.get(item) or {}
        filled = f.get("filled", 0.0)
        value = f.get("value", 0.0)
        req = p.get("req_qty", 0.0)
        sub = p.get("sub_value", 0.0)
        row = {"base_px": base,
               "filled_qty": round(filled, 1), "filled_value": round(value, 1),
               "avg_fill_px": round(value / filled, 2) if filled else UNKNOWN,
               "ratio_fill": round(value / (filled * base), 4)
               if filled and base else UNKNOWN,
               "req_qty": round(req, 1),
               "avg_submit_px": round(sub / req, 2) if req else UNKNOWN,
               "ratio_submit": round(sub / (req * base), 4)
               if req and base else UNKNOWN}
        out_items[item] = row
        if base:
            num_f += value
            den_f += filled * base
            num_s += sub
            den_s += req * base
    agg = {"ratio_fill_all": round(num_f / den_f, 4) if den_f else UNKNOWN,
           "ratio_submit_all": round(num_s / den_s, 4) if den_s else UNKNOWN,
           "n_games": len(rows), "shadow_mismatch_steps": mism}
    return {"per_item": out_items, "aggregate": agg}


def end_agg(rows: List[Dict]) -> Dict[str, Any]:
    """终局钱/终局滞留聚合（farms[obs.player].money；末拍 shed×quote）。"""
    tms = [float(r["reads"]["terminal_money"]) for r in rows
           if isinstance(r.get("reads"), dict)
           and is_num(r["reads"].get("terminal_money"))]
    sts = [float(r["reads"]["stranding"]) for r in rows
           if isinstance(r.get("reads"), dict)
           and is_num(r["reads"].get("stranding"))]
    shed_items: Dict[str, List[float]] = {i: [] for i in KNEE_ITEMS}
    st_items: Dict[str, List[float]] = {i: [] for i in KNEE_ITEMS}
    for r in rows:
        rd = r.get("reads") or {}
        for i in KNEE_ITEMS:
            v = (rd.get("shed_end") or {}).get(i)
            if is_num(v):
                shed_items[i].append(float(v))
            v2 = (rd.get("stranding_knee_items") or {}).get(i)
            if is_num(v2):
                st_items[i].append(float(v2))
    return {
        "terminal_money_mean": round(sum(tms) / len(tms), 1) if tms else UNKNOWN,
        "terminal_money_median": round(statistics.median(tms), 1) if tms
        else UNKNOWN,
        "stranding_mean": round(sum(sts) / len(sts), 1) if sts else UNKNOWN,
        "stranding_median": round(statistics.median(sts), 1) if sts else UNKNOWN,
        "stranding_knee_items_mean": {
            i: round(sum(v) / len(v), 1) if v else UNKNOWN
            for i, v in st_items.items()},
        "shed_end_knee_items_mean": {
            i: round(sum(v) / len(v), 2) if v else UNKNOWN
            for i, v in shed_items.items()},
    }


def knee_agg(rows: List[Dict]) -> Dict[str, Any]:
    """knee 触发面：逐品截留量/触发步数（跨局合计 + 每局均值）。"""
    per: Dict[str, Dict[str, float]] = {}
    games_trunc = 0
    tot_trunc = 0.0
    for r in rows:
        kn = r.get("knee") or {}
        if not kn.get("present"):
            continue
        hit = False
        for item, row in (kn.get("per_item") or {}).items():
            acc = per.setdefault(item, {k: 0.0 for k in (
                "knee_quote_steps", "sell_steps", "trig_steps", "sell_orders",
                "requested_qty", "posted_qty", "truncated_orders",
                "truncated_qty", "dropped_orders")})
            for k in acc:
                v = row.get(k) if isinstance(row, dict) else None
                if is_num(v):
                    acc[k] += float(v)
            if isinstance(row, dict) and float(row.get("truncated_qty") or 0) \
                    > 0:
                hit = True
        t = float(kn.get("truncated_qty") or 0)
        tot_trunc += t
        if hit or t > 0:
            games_trunc += 1
    n = max(1, len(rows))
    per_out = {}
    for item in sorted(per):
        row = dict(per[item])
        row["trig_steps_per_game"] = round(row["trig_steps"] / n, 2)
        row["truncated_qty_per_game"] = round(row["truncated_qty"] / n, 1)
        per_out[item] = {k: (round(v, 1) if isinstance(v, float) else v)
                         for k, v in row.items()}
    return {"n_games": len(rows), "games_with_truncation": games_trunc,
            "truncated_qty_total": round(tot_trunc, 1),
            "per_item": per_out}


def stranding_paired(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """终局滞留配对 Δ（variant−control；判据=均值不升）。"""
    deltas = []
    rows = []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        sc = ((rc or {}).get("reads") or {}).get("stranding")
        sv = ((rv or {}).get("reads") or {}).get("stranding")
        if not is_num(sc) or not is_num(sv):
            continue
        d = float(sv) - float(sc)
        deltas.append(d)
        rows.append({"seed": u["seed"], "seat": u["seat"],
                     "stranding_control": sc, "stranding_variant": sv,
                     "delta": round(d, 1)})
    return {"n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 2) if deltas
            else UNKNOWN,
            "median_delta": round(statistics.median(deltas), 2) if deltas
            else UNKNOWN,
            "max_delta": round(max(deltas), 1) if deltas else UNKNOWN,
            "n_up": sum(1 for d in deltas if d > 0),
            "not_up": bool(deltas and (sum(deltas) / len(deltas)) <= 0),
            "rows_lite": rows}


# ------------------------------------------------------------ 四门门禁 --
def _gate_load(pkg):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(os.path.join(pkg, "main.py"))
    name = getattr(entry, "__name__", "")
    if name != ENTRY_NAME:
        return {"passed": False,
                "error": "末 callable=%r 应为 %r" % (name, ENTRY_NAME)}
    return {"passed": True, "entry": name}


def _run_episode(pkg, seed):
    import gate_launch_fourgate_l1 as l1g  # noqa: WPS433
    check = l1g._redirect_check(pkg)
    return check.run_full_episode(int(seed))


def _gate_health(pkg):
    eps = [_run_episode(pkg, s) for s in EPISODE_SEEDS]
    details = []
    ok = True
    for ep in eps:
        statuses = list(ep.get("statuses") or [])
        rewards = list(ep.get("rewards") or [])
        step_ms = ep.get("max_step_ms")
        turns = ep.get("turns_played")
        good = (statuses == ["DONE", "DONE"] and len(rewards) == 2
                and all(is_num(r) and abs(float(r)) < 1e12 for r in rewards)
                and is_num(step_ms) and float(step_ms) < STEP_BUDGET_MS
                and turns == 720)
        ok = ok and good
        details.append({"seed": ep.get("seed"), "statuses": statuses,
                        "turns_played": turns, "max_step_ms": step_ms,
                        "p99_step_ms": ep.get("p99_step_ms"),
                        "passed": good})
    return {"passed": ok, "step_budget_ms": STEP_BUDGET_MS,
            "episodes": details}


def _gate_determinism(pkg):
    e1 = _run_episode(pkg, EPISODE_SEEDS[0])
    e2 = _run_episode(pkg, EPISODE_SEEDS[0])
    h1, h2 = e1.get("action_stream_sha256"), e2.get("action_stream_sha256")
    ok = bool(h1) and h1 == h2
    return {"passed": ok, "rerun_seed": EPISODE_SEEDS[0],
            "hashes": {"run1": h1, "run2": h2}}


def _gate_identity(pkg, form):
    import tarfile
    main_bytes = open(os.path.join(pkg, "main.py"), "rb").read()
    tar_bytes = open(os.path.join(pkg, "submission.tar.gz"), "rb").read()
    man = json.load(open(os.path.join(pkg, "build_manifest.json")))
    main_sha = hashlib.sha256(main_bytes).hexdigest()
    with tarfile.open(fileobj=__import__("io").BytesIO(tar_bytes),
                      mode="r:gz") as tar:
        members = tar.getnames()
        inner = tar.extractfile("main.py").read()
    base = open(H1_MAIN, "rb").read()
    base_sha = hashlib.sha256(base).hexdigest()
    checks = {
        "size_lt_100mb": len(tar_bytes) < SIZE_CAP_BYTES,
        "tar_members_exact": members == ["main.py"],
        "inner_matches_disk": inner == main_bytes,
        "sha_matches_manifest": main_sha == man.get("main_sha256"),
        "h1_base_sha_ok": base_sha == H1_SHA_EXPECTED,
        "h1_prefix_identical": main_bytes.startswith(base),
        "injected_not_identity": main_bytes != base
        and len(main_bytes) > len(base),
        "entry_manifest_ok": man.get("entry") == ENTRY_NAME,
    }
    return {"passed": all(checks.values()), "checks": checks,
            "main_sha256": main_sha,
            "tar_size_mb": round(len(tar_bytes) / 1e6, 3),
            "tar_members": members,
            "base_main_sha256": base_sha,
            "byte_identical_to_h1": main_bytes == base,
            "injected_tail_bytes": len(main_bytes) - len(base)}


def run_gates(form: str) -> Dict[str, Any]:
    pkg = str(MODULE_DIR / "build" / form)
    os.makedirs(os.path.join(pkg, "evidence"), exist_ok=True)
    res: Dict[str, Any] = {}
    for gname, fn in (("load", lambda p=pkg: _gate_load(p)),
                      ("health", lambda p=pkg: _gate_health(p)),
                      ("determinism", lambda p=pkg: _gate_determinism(p))):
        try:
            res[gname] = fn()
        except Exception as exc:
            res[gname] = {"passed": False, "error": repr(exc)[:200]}
    try:
        res["identity"] = _gate_identity(pkg, form)
    except Exception as exc:
        res["identity"] = {"passed": False, "error": repr(exc)[:200]}
    res["overall"] = all(g.get("passed") for g in res.values())
    return res


# ------------------------------------------------------------ main --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_text = Path(H1_MAIN).read_text(encoding="utf-8")
    base_sha = hashlib.sha256(base_text.encode("utf-8")).hexdigest()
    if base_sha != H1_SHA_EXPECTED:
        raise RuntimeError("基底 h1 sha 漂移：%s" % base_sha)

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES,
              "smoke_局次": 2,   # 跑前管线冒烟 2 局（sim 强制，不入配对语料）
              "aborted_attempt_局次": 64,  # 首跑中断：auth 60 + knee_x10 门 4
              "auth_局次": 0, "gate_局次": 0, "judgment_局次": 0}

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("谷底三品价格膝点量门实测（knee-gate；判决先行·不发射）："
                       "FERTILIZER/MILK/WOOL 本步 SELL 单量按 quote<0.7×base "
                       "截留至 min(沈存30%,步帽X)（X=10/20 两变体），只减不挪、"
                       "截掉的量由磁带后续卖单/终局清算自然出清"),
        "source": {
            "commands": ["python3 orderbook_knee_lab/build_knee.py",
                         "python3 orderbook_knee_lab/judge_knee.py"],
            "base_main": H1_MAIN, "base_sha256": base_sha,
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*89（任务给定新中性块 n=8）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局回放（canonical 前 8 fold）+ 新中性块"
                                 " 672000+i*89（i=0..7）；双席 fold n=16/变体"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": ("margin=终局 banks[our]−banks[opp]；终局钱 "
                        "farms[obs.player].money 干净口径；分品实现价="
                        "Σ(filled×成交价)/Σ(filled×base)（影子引擎逐拍归因 "
                        "value/filled），提交口径 Σ(qty×卖时市价) 对照；"
                        "终局滞留=末拍 shed×quote（judge_strongest 同口径）"),
            "criterion": ("净翻胜>0 ∧ flips_neg==0 ∧ 终局滞留不升（配对 Δ 均值"
                          "≤0；截留不能变死货）"),
            "base_px_table": BASE_PX,
            "corner_ref_ratio_fill": CORNER_REF,
        },
        "mechanism": {
            "layer": "knee（尾块注入沿 append 先例；宿主=h1 件 _hs_agent；"
                     "入口=_kg_agent 末 callable）",
            "items": list(KNEE_ITEMS),
            "knee_rule": "该品当前 quote < 0.7×base 触发截留；quote≥0.7×base "
                         "全量挂卖（膝点=价崩拐点，简单可实现口径）",
            "cap_rule": "本步该品挂卖总量截留至 min(沈存×30%, 步帽 X)（沈存=同拍"
                        "投射仓 _xd7_projected，失败回退裸 shed）",
            "clearing": "截留不是挪卖：截掉的量留在棚里，由磁带后续卖单/终局清算"
                        "（712-718）自然出清；终局清算窗 step≥712 不截留（出清"
                        "路径保真，亦不干扰 E182 终局规划器物理守卫）",
            "constraints": ["只减不挪", "零跨拍挪量（R23/R26）", "磁带 blob 零触碰",
                            "非 SELL/挂量不确定条目原样保留",
                            "异常回退原动作（同对象零足迹）"],
            "variants": {"knee_x10": {"step_cap": 10},
                         "knee_x20": {"step_cap": 20}},
        },
        "params": {},
        "gates": {},
        "knee_trigger_surface": {},
        "pairs": {},
        "per_item_realized": {},
        "stranding": {},
        "terminal_money": {},
        "criteria": {},
        "verdict": {},
        "budget": budget,
    })
    flush_evid()

    # ---- 0) 构建参数入账 ----
    for form in FORMS:
        man = json.load(open(str(MODULE_DIR / "build" / form /
                                 "build_manifest.json")))
        EV["params"][form] = {"manifest_main_sha256": man.get("main_sha256"),
                              "injected_tail_bytes": man.get(
                                  "injected_tail_bytes"),
                              "params": man.get("params")}
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                     2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60        # 30 局×官方/仿真双引擎（judge_strongest 口径）
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 门禁四门（两变体） ----
    for form in FORMS:
        t1 = time.perf_counter()
        res = run_gates(form)
        EV["gates"][form] = res
        budget["gate_局次"] += 4      # health×2 + determinism×2 官方引擎完整局
        print(form, "gates:", {k: v.get("passed") for k, v in res.items()
                               if k != "overall"},
              round(time.perf_counter() - t1, 1), "s", flush=True)
        flush_evid()

    # ---- 3) 三臂实跑（h1 对照 + 两变体；同语料同对手同席配对） ----
    rows_by_arm: Dict[str, List[Dict[str, Any]]] = {}
    for arm in ("h1", "knee_x10", "knee_x20"):
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget["judgment_局次"] += len(rows)
        agg_end = end_agg(rows)
        agg_real = realized_agg(rows)
        EV["per_item_realized"][arm] = agg_real
        EV["stranding"][arm] = agg_end
        EV["terminal_money"][arm] = {
            "mean": agg_end["terminal_money_mean"],
            "median": agg_end["terminal_money_median"]}
        if arm != "h1":
            EV["knee_trigger_surface"][arm] = knee_agg(rows)
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d（见 rows_lite error 字段）"
                             % (arm, n_err, len(rows)))
        mism = agg_real["aggregate"].get("shadow_mismatch_steps")
        print(arm, "games", len(rows), "err", n_err,
              "tm", agg_end["terminal_money_mean"],
              "stranding", agg_end["stranding_mean"],
              "shadow_mism", mism,
              round(time.perf_counter() - t2, 1), "s", flush=True)
        EV["budget"] = budget
        flush_evid()
    budget["total_局次"] = budget["auth_局次"] + budget["gate_局次"] \
        + budget["judgment_局次"] + budget["smoke_局次"] \
        + budget["aborted_attempt_局次"]
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES

    # ---- 4) 配对判决（变体 vs h1） ----
    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["h1"]}
    for form in FORMS:
        var = {(r["seed"], r["seat"]): r for r in rows_by_arm[form]}
        ps = pair_stats(ctl, var, units)
        st = stranding_paired(ctl, var, units)
        EV["pairs"]["%s_vs_h1" % form] = ps
        EV["stranding"]["paired_%s_vs_h1" % form] = st
        crit = {
            "净翻胜>0": ps["net_flip_wins"] > 0,
            "flips_neg==0": ps["flips_neg"] == 0,
            "终局滞留不升": st["not_up"],
        }
        EV["criteria"][form] = {
            "checks": crit,
            "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
            "stranding_mean_delta": st["mean_delta"],
            "positive_arm": all(crit.values())}
        print(form, "vs h1:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
              "dM", ps["mean_delta"], "netflip", ps["net_flip_wins"],
              "flips_neg", ps["flips_neg"], "dStrand", st["mean_delta"],
              "crit", crit, flush=True)
        flush_evid()

    # ---- 5) verdict ----
    positives = [f for f in FORMS if EV["criteria"][f]["positive_arm"]]
    knee_items_readout = {}
    for arm in ("h1", "knee_x10", "knee_x20"):
        per = EV["per_item_realized"][arm].get("per_item") or {}
        knee_items_readout[arm] = {
            i: {"ratio_fill": per.get(i, {}).get("ratio_fill"),
                "ratio_submit": per.get(i, {}).get("ratio_submit"),
                "filled_qty": per.get(i, {}).get("filled_qty")}
            for i in KNEE_ITEMS}
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "positive_variants": positives,
        "per_variant": {
            f: {"net_flip_wins": EV["criteria"][f]["net_flip_wins"],
                "flips_neg": EV["criteria"][f]["flips_neg"],
                "mean_delta": EV["pairs"]["%s_vs_h1" % f]["mean_delta"],
                "stranding_mean_delta":
                    EV["criteria"][f]["stranding_mean_delta"],
                "positive_arm": EV["criteria"][f]["positive_arm"]}
            for f in FORMS},
        "knee_items_ratio_fill": knee_items_readout,
        "verdict": ("价格膝点量门正臂：%s" % (", ".join(positives) if positives
                                          else "无（两变体均未达判据）")),
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    LEDGER_PATH.write_text(json.dumps(
        {"pairs": {k: {"n": v["n"], "W": v["W"], "L": v["L"], "T": v["T"],
                       "mean_delta": v["mean_delta"],
                       "net_flip_wins": v["net_flip_wins"],
                       "flips_neg": v["flips_neg"]}
                   for k, v in EV["pairs"].items()},
         "criteria": EV["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
