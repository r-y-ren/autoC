# -*- coding: utf-8 -*-
"""judge_corner：三改进角实测（corner-cases；诊断+判决先行·不发射不提交）。

责任口径（任务 corner-cases）：
- 任务一（口径缺口·分品实现价体检）：control（H1）实跑 traced 局，逐品
  Σ(qty×成交价)/Σ(qty×base)（base=WHEAT25/CARROT35/TOMATO60/STRAWBERRY120/
  MELON250/EGG50/MILK160/WOOL200/FERT100）。成交价=kgenv 影子引擎逐拍成交
  归因（value/filled；与官方引擎交叉校验过），另记提交口径（qty×卖时市价）
  对照 judge_strongest clean_reads。对照=tetsutani 自报（WOOL 0.65-0.70/
  MILK 0.61-0.67 被自冲 vs 城镇排走品 1.5-2.1×）+ 冠军 0.903（base 口径）。
  诊断不判决。
- 任务二（建模轮首验）：care2（CARE 翻倍）+ fertilize-on（按吸收率定速施肥）
  磁带手术变体 vs H1 配对；任务三（分析40 表#3）：dephase（日新高追加单挂拍
  k%4 轮转全相位——禁区下唯一合法面）同口径。
- 配对口径（prod-rhythm 同）：control=H1 vs 对手 O，arm=变体 vs 同一 O，同
  seed+seat 配对；margin=终局 banks[our]−banks[opp]（farms[obs.player].money
  干净口径交叉核对入 anomaly）；判据=净翻胜>0 ∧ flips_neg==0（胜局不翻负）。
- 语料：26 败局前 8 fold + 新中性块 672000+i*83（i=0..7）→ n=16 双席
  fold/变体；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤350 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-corner-cases.json；账本落
orderbook_corner_lab/evidence/。复用（不改写）：sim_bridge.run_games/
sim_bridge、tape_variants.feasibility_twin、retape_sheep 编解码件。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

import corner_variants as cv  # noqa: E402

RECORD_VERSION = "corner-cases/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
LOSS_FOLDS = REPLAY_26[:8]                      # 26 败局 canonical 前 8 fold
NEUTRAL_FOLDS = [672000 + i * 83 for i in range(8)]   # 新中性 672000+i*83
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS              # n=16 双席 fold/变体

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}
TETSUTANI = {"WOOL": [0.65, 0.70], "MILK": [0.61, 0.67],
             "note": "tetsutani 自报：WOOL/MILK 被自冲谷底；城镇排走品 1.5-2.1×"}
CHAMPION_BASE = 0.903                          # 冠军 base 口径（任务给定对照）

WORKERS = 2
BUDGET_CAP_GAMES = 350
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-corner-cases.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "corner_ab_ledger.json"

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
        f = float(v)
    except Exception:
        return None
    return f


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
    """单文件件装载（末 callable 语义）+ 遥测报告字典（_S928/_DP）。"""
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
    reports = {k: ns[k] for k in ("_S928_REPORT", "_S932_REPORT",
                                  "_S939_REPORT", "_S948_REPORT",
                                  "_DP_REPORT")
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


class _Tracer:
    """观察/动作/遥测逐拍追踪（不改动作）。"""

    def __init__(self, inner: Any, seat: int, sink: List[Any],
                 reports: Dict[str, Any]):
        self.inner, self.seat, self.sink, self.reports = inner, seat, sink, \
            reports
        self.prev: Dict[tuple, float] = {}

    def __call__(self, obs: Any, configuration: Any = None) -> Any:
        act = _call_inner(self.inner, obs, configuration)
        tel: Dict[str, Dict[str, float]] = {}
        for name, rep in self.reports.items():
            d = {}
            for k, v in rep.items():
                if isinstance(v, (int, float)) and not isinstance(v, bool):
                    delta = float(v) - self.prev.get((name, k), 0.0)
                    if delta:
                        d[k] = delta
                    self.prev[(name, k)] = float(v)
            if d:
                tel[name] = d
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


_DH_REPORTS = ("_S928_REPORT", "_S932_REPORT", "_S939_REPORT", "_S948_REPORT")


def sell_phase_reads(sink) -> Dict[str, Any]:
    """实现卖单 %4 相位直方（单数/挂量）+ 日新高追加单簇挂拍（遥测）。"""
    cnt: Counter = Counter()
    qty: Counter = Counter()
    s928: Counter = Counter()      # 追加单挂拍（changed 次数按相位）
    s928_units: Counter = Counter()
    dp_hung: Counter = Counter()
    per_fam: Dict[str, int] = {}
    for entry in (sink or []):
        step, obs, act, tel = entry[0], entry[1], entry[2], (entry[3] or {})
        ph = int(step) % 4
        if isinstance(act, dict):
            for cmd in (act.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                        and str(cmd[0]) == "SELL":
                    try:
                        q = float(cmd[2])
                    except (TypeError, ValueError):
                        q = 0.0
                    cnt[ph] += 1
                    qty[ph] += q
        for fam in _DH_REPORTS:
            d = tel.get(fam) or {}
            if d.get("changed"):
                s928[ph] += int(d["changed"])
                s928_units[ph] += float(d.get("units") or 0)
                per_fam[fam] = per_fam.get(fam, 0) + int(d["changed"])
            if d.get("eligible"):
                per_fam[fam + ":eligible"] = \
                    per_fam.get(fam + ":eligible", 0) + int(d["eligible"])
        dp_d = tel.get("_DP_REPORT") or {}
        if dp_d.get("hung"):
            dp_hung[ph] += int(dp_d["hung"])

    def _share(c: Counter) -> Dict[str, float]:
        tot = sum(c.values()) or 1
        return {str(k): round(v / tot, 4) for k, v in sorted(c.items())}

    tot_c = sum(cnt.values()) or 1
    tot_q = sum(qty.values()) or 1
    return {"orders": dict(sorted(cnt.items())),
            "qty": {str(k): round(v, 1) for k, v in sorted(qty.items())},
            "phase4_count_share": _share(cnt),
            "phase4_qty_share": _share(qty),
            "concentration_count": round(max(cnt.values()) / tot_c, 4)
            if cnt else UNKNOWN,
            "concentration_qty": round(max(qty.values()) / tot_q, 4)
            if qty else UNKNOWN,
            "s928_append_events": dict(sorted(s928.items())),
            "s928_append_units": {str(k): round(v, 1)
                                  for k, v in sorted(s928_units.items())},
            "dh_append_by_family": per_fam,
            "dp_hung_events": dict(sorted(dp_hung.items()))}


def clean_reads(sink) -> Dict[str, Any]:
    """终局钱 farms[obs.player].money 干净口径（交叉核对用）。"""
    last_obs = None
    for entry in (sink or []):
        if isinstance(entry[1], dict):
            last_obs = entry[1]
    if not isinstance(last_obs, dict):
        return {"terminal_money": UNKNOWN}
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
    return {"terminal_money": tm}


# ------------------------------------------------------------ 局跑口 --
def _build_agents_cc(spec):
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
            agents, sinks = _build_agents_cc(spec)
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
               "margin": None, "reads": {}, "items": None, "items_opp": None,
               "shadow": None, "sell_phase": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our, opp = sinks[row["seat"]], sinks[1 - row["seat"]]
            row["reads"] = clean_reads(our)
            row["items"] = item_reads(our)
            row["items_opp"] = item_reads(opp)
            row["sell_phase"] = sell_phase_reads(our)
            if spec.get("shadow"):
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


def _units_all(shadow: bool):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_672000_i83")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name, "stratum": stratum,
                          "shadow": bool(shadow)})
    return units, opp_paths


def _specs_for(units, arm, cand_path, trace: bool):
    specs = []
    for r in units:
        agents = [{"type": "python", "path": cand_path},
                  {"type": "python", "path": r["opp_path"]}]
        if int(r["seat"]) == 1:
            agents.reverse()
        specs.append({
            "game_id": "cc-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": bool(trace), "shadow": bool(r.get("shadow")),
            "opponent": r.get("opponent"), "stratum": r.get("stratum"),
            "agents": agents})
    return specs


# ------------------------------------------------------------ 聚合 --
def pair_stats(ctl: Dict, var: Dict, kept_units: List[Dict]) -> Dict:
    """配对聚合：W-L-T（Δ 口径）/Δ/翻负/净翻胜（prod-rhythm 同口径）。"""
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


def realized_agg(rows: List[Dict], key: str = "items",
                 shadow_side: str = "our") -> Dict[str, Any]:
    """分品实现价聚合：Σvalue/Σ(filled×base)（成交价口径）+ 提交口径。"""
    per: Dict[str, Dict[str, float]] = {}
    for r in rows:
        for item, row in (r.get(key) or {}).items():
            acc = per.setdefault(item, {"req_qty": 0.0, "sub_value": 0.0})
            acc["req_qty"] += float(row.get("req_qty") or 0)
            acc["sub_value"] += float(row.get("sub_value") or 0)
    sh: Dict[str, Dict[str, float]] = {}
    for r in rows:
        side = int(r.get("seat", 0)) if shadow_side == "our" \
            else 1 - int(r.get("seat", 0))
        s = r.get("shadow") or {}
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
           "n_games": len(rows)}
    return {"per_item": out_items, "aggregate": agg}


def sell_phase_agg(rows: List[Dict]) -> Dict[str, Any]:
    cnt: Counter = Counter()
    qty: Counter = Counter()
    s928: Counter = Counter()
    s928_u: Counter = Counter()
    dp: Counter = Counter()
    fam: Counter = Counter()
    for r in rows:
        sp = r.get("sell_phase") or {}
        for k, v in (sp.get("orders") or {}).items():
            cnt[str(k)] += int(v)
        for k, v in (sp.get("qty") or {}).items():
            qty[str(k)] += float(v)
        for k, v in (sp.get("s928_append_events") or {}).items():
            s928[str(k)] += int(v)
        for k, v in (sp.get("s928_append_units") or {}).items():
            s928_u[str(k)] += float(v)
        for k, v in (sp.get("dh_append_by_family") or {}).items():
            fam[str(k)] += int(v)
        for k, v in (sp.get("dp_hung_events") or {}).items():
            dp[str(k)] += int(v)
    tot_c = sum(cnt.values()) or 1
    tot_q = sum(qty.values()) or 1

    def _share(c: Counter, tot: float):
        return {k: round(v / tot, 4) for k, v in sorted(c.items())}

    return {"n_games": len(rows),
            "orders": dict(sorted(cnt.items())),
            "qty": {k: round(v, 1) for k, v in sorted(qty.items())},
            "phase4_count_share": _share(cnt, tot_c),
            "phase4_qty_share": _share(qty, tot_q),
            "concentration_count": round(max(cnt.values()) / tot_c, 4)
            if cnt else UNKNOWN,
            "concentration_qty": round(max(qty.values()) / tot_q, 4)
            if qty else UNKNOWN,
            "s928_append_events": dict(sorted(s928.items())),
            "s928_append_units_total": round(sum(s928_u.values()), 1),
            "s928_append_events_total": sum(s928.values()),
            "dh_append_by_family": dict(sorted(fam.items())),
            "dp_hung_events": dict(sorted(dp.items())),
            "dp_hung_events_total": sum(dp.values())}


# ------------------------------------------------------------ main --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    main_text = cv.H1_MAIN.read_text(encoding="utf-8")
    pkg_base = cv.rs._decode_routes(main_text)
    units, opp_paths = _units_all(shadow=True)
    units_pairs, _ = _units_all(shadow=False)

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("三改进角实测（诊断+判决先行）：任务一 H1 分品实现价 vs "
                       "base 口径体检（对照 tetsutani 自报/冠军 0.903）；任务二 "
                       "care2（CARE 翻倍）+fertilize-on（吸收率定速）建模轮结论"
                       "首验；任务三 dephase 卖相位去集中（禁区下合法面=日新高"
                       "追加单挂拍轮转）"),
        "source": {
            "commands": ["python3 orderbook_corner_lab/judge_corner.py"],
            "base_main": str(cv.H1_MAIN),
            "base_sha256": hashlib.sha256(
                main_text.encode("utf-8")).hexdigest(),
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*83（新中性块 n=8）",
                       "folds_per_variant": 16,
                       "strata": "26 败局回放（canonical 前 8 fold）+ 新中性块"
                                 " 672000+i*83（i=0..7）；双席 fold n=16/变体"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": ("margin=终局 banks[our]−banks[opp]；终局钱 "
                        "farms[obs.player].money 干净口径交叉核对；"
                        "实现价=Σ(qty×成交价)/Σ(qty×base)（成交价=影子引擎"
                        "逐拍归因 value/filled），提交口径 Σ(qty×卖时市价) 对照"),
            "criterion": "净翻胜>0 的变体为正臂；胜局对照不翻负（flips_neg==0）",
            "base_px_table": BASE_PX,
        },
        "realized_base": {}, "care2": {}, "fertilize_on": {}, "dephase": {},
        "sell_phase": {}, "verdict": {}, "budget": {"cap_局次": BUDGET_CAP_GAMES,
                                                    "auth_局次": 0,
                                                    "judgment_局次": 0},
    })
    flush_evid()

    # ---- 1) 磁带手术变体构建 + 审计 + 孪生三闸先行 ----
    built_all: Dict[str, Any] = {}
    for vid in ("care2", "fert_on"):
        tv0 = time.perf_counter()
        b = cv.build_variant(vid, pkg_base, main_text)
        aud = b["audit"]
        by_events = Counter(r["route"] for r in b["table"]
                            if r.get("status") == "inserted")
        twin_rids = [r for r, _ in by_events.most_common(3)] \
            or sorted(pkg_base["routes"], key=lambda k: int(k))[:3]
        twin = cv.twin_check(b, pkg_base, twin_rids) if twin_rids else \
            {"verdict": "NO_OP", "checks": []}
        kept = bool(twin.get("verdict") == "PASS"
                    and aud.get("conservation_ok")
                    and b["stats"]["inserted"] > 0)
        p = cv.BUILD_DIR / ("variant_%s_main.py" % vid)
        p.write_text(b["main_text"], encoding="utf-8")
        EV[vid if vid != "fert_on" else "fertilize_on"]["variant"] = {
            "stats": b["stats"],
            "conservation": {"ok": aud["conservation_ok"],
                             "note": aud["conservation_note"],
                             "n_inserted": aud["n_inserted"],
                             "n_table_rows": aud["n_table_rows"]},
            "twin": {"verdict": twin.get("verdict"), "twin_rids": twin_rids,
                     "n_checks": len(twin.get("checks") or []),
                     "n_violation": sum(1 for c in (twin.get("checks") or [])
                                        if not c.get("ok"))},
            "main_path": str(p), "kept": kept,
            "elapsed_s": round(time.perf_counter() - tv0, 2)}
        built_all[vid] = b
        if not kept:
            ANOMALIES.append("%s 弃（twin=%s cons=%s inserted=%d）" % (
                vid, twin.get("verdict"), aud.get("conservation_ok"),
                b["stats"]["inserted"]))
        print("variant", vid, "twin", twin.get("verdict"), "kept", kept,
              "inserted", b["stats"]["inserted"], flush=True)
        flush_evid()

    kept_tape = [vid for vid in ("care2", "fert_on")
                 if EV[vid if vid != "fert_on" else "fertilize_on"]
                 ["variant"].get("kept")]

    # ---- 2) sim_bridge 对照认证 30/30（不过即停） ----
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        list(REPLAY_26) + [2026092901, 2026092902, 2026092903, 2026092904])
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    (MODULE_DIR / "evidence" / "sim_auth.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str)
        + "\n", encoding="utf-8")
    EV["source"]["sim_auth"] = auth_lite
    EV["budget"]["auth_局次"] = 30
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"verdict": "ABORT：sim_bridge 对照认证未过 30/30"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        return EV
    flush_evid()
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 3) control（H1 traced+影子归因）→ 任务一 realized_base ----
    specs_ctl = _specs_for(units, "control", str(cv.H1_MAIN), True)
    rows_ctl, engines_ctl = _play(specs_ctl, run_cfg)
    EV["budget"]["judgment_局次"] += len(rows_ctl)
    ctl = {(int(r["seed"]), int(r["seat"])): r for r in rows_ctl}
    tm_deltas = []
    for r in rows_ctl:
        if r.get("error"):
            ANOMALIES.append("control 红局 %s s%d: %s" % (
                r["seed"], r["seat"], r["error"]))
            continue
        tm = (r.get("reads") or {}).get("terminal_money")
        if is_num(tm) and isinstance(r.get("banks"), list):
            banks0 = float(r["banks"][int(r["seat"])])
            if abs(float(tm) - banks0) > 0.5:
                tm_deltas.append(round(float(tm) - banks0, 2))
        sh = r.get("shadow") or {}
        if sh.get("error"):
            ANOMALIES.append("影子归因失败 %s s%d: %s" % (
                r["seed"], r["seat"], sh["error"]))
        elif sh.get("shadow_mismatch_steps", 0) > 0:
            ANOMALIES.append("影子归因失配 %s s%d: %d 拍（已重同步）" % (
                r["seed"], r["seat"], sh["shadow_mismatch_steps"]))
    if tm_deltas:
        tm_deltas.sort()
        ANOMALIES.append(
            "终局钱口径注记：trace 末拍=step718（banks=末拍结算后）——%d/%d 局 "
            "tm 与 banks 差额（tm−banks）中位 %s、区间 [%s,%s]；margin 判据用 "
            "banks 口径不受影响" % (
                len(tm_deltas), len(rows_ctl), tm_deltas[len(tm_deltas) // 2],
                tm_deltas[0], tm_deltas[-1]))
    ours = [r for r in rows_ctl if not r.get("error")]
    rb_ours = realized_agg(ours, "items", "our")
    rb_opp = realized_agg(ours, "items_opp", "opp")
    # 影子成交价口径（fill）来自 shadow；提交口径来自 items
    EV["realized_base"] = {
        "per_item": rb_ours["per_item"],
        "aggregate": rb_ours["aggregate"],
        "对照": {
            "tetsutani_self_report": TETSUTANI,
            "champion_base_caliber": CHAMPION_BASE,
            "opp_side_in_same_games": rb_opp["aggregate"],
            "opp_side_per_item": rb_opp["per_item"],
            "note": ("比例=Σ(qty×成交价)/Σ(qty×base)；tetsutani 自报与冠军 "
                     "0.903 为 base 口径同表可比；opp 侧=同局四对手（r37/"
                     "2965a/2965b/v48_derivative）"),
        },
        "n_games_traced": len(ours),
        "caliber_fill": "成交价=影子引擎逐拍归因 value/filled",
        "caliber_submit": "提交口径=Σ(qty_req×卖时市价)/Σ(qty_req×base)"
                          "（judge_strongest clean_reads 同族）",
    }
    # 任务一诊断性结论（不判决）
    per = rb_ours["per_item"]
    wm = {k: per.get(k, {}).get("ratio_fill") for k in ("WOOL", "MILK")}
    hurt = sorted(((v.get("ratio_fill"), it) for it, v in per.items()
                   if is_num(v.get("ratio_fill"))))[:3]
    EV["realized_base"]["task1_answer"] = {
        "wool_milk_valley_self_harm": {
            "WOOL": wm.get("WOOL"), "MILK": wm.get("MILK"),
            "threshold": "对照 tetsutani 自冲带 0.61-0.70；<0.9 视为谷底自伤"},
        "most_hurt_items": [{"item": it, "ratio_fill": r} for r, it in hurt],
    }
    EV["sell_phase"]["control"] = sell_phase_agg(ours)
    print("control played", len(rows_ctl), "games; realized:",
          rb_ours["aggregate"], flush=True)
    flush_evid()

    # ---- 4) dephase 实现面判定（日新高追加单实测触发量） ----
    sp_ctl = EV["sell_phase"]["control"]
    n_appends = int(sp_ctl.get("s928_append_events_total") or 0)
    u_appends = float(sp_ctl.get("s928_append_units_total") or 0)
    dephase_form = {
        "form": "追加单相位去集中：日新高追加单簇（S928/S948/S932/S939 纯追加"
                "支）挂拍 k%4 轮转全相位（同拍单集不动=只追加零改写；跨拍不挪"
                "量=磁带卖单零触碰；跨相位同品同量等价交换=红线未做）",
        "tape_touched": False,
        "surface_measurement": {
            "dh_append_events": n_appends,
            "dh_append_units": u_appends,
            "dh_append_by_family": sp_ctl.get("dh_append_by_family"),
            "append_phase4_events": sp_ctl.get("s928_append_events"),
            "realized_sell_concentration_count":
                sp_ctl.get("concentration_count"),
            "realized_sell_concentration_qty": sp_ctl.get("concentration_qty"),
            "note": ("47% vs 36%（mooman 实测）口径=卖单 %4 相位最大相位占比；"
                     "卖单主体=磁带计划单（跨拍挪量红线封死不可重排），日新高"
                     "追加单=唯一合法去集中面（step928/948 变现簇同拍追加族）"),
        },
    }
    dephase_keep = n_appends > 0
    if not dephase_keep:
        dephase_form["implementable"] = False
        dephase_form["reason"] = ("该发现无法在禁区下实现：日新高追加单实测零触发"
                                  "（无追加单可轮转挂拍），且磁带卖单相位重排全部"
                                  "触跨拍挪量红线")
        EV["dephase"] = {"form": dephase_form, "pairs": {}}
        ANOMALIES.append("dephase 无合法实现面（S928 追加单实测 %d 次）"
                         % n_appends)
        flush_evid()
    else:
        dp_built = cv.build_dephase(main_text)
        if not dp_built.get("ok"):
            dephase_form["implementable"] = False
            dephase_form["reason"] = "壳手术失败: %s" % dp_built.get("error")
            EV["dephase"] = {"form": dephase_form, "pairs": {}}
            ANOMALIES.append("dephase 壳手术失败: %s" % dp_built.get("error"))
            flush_evid()
        else:
            p = cv.BUILD_DIR / "variant_dephase_main.py"
            p.write_text(dp_built["main_text"], encoding="utf-8")
            dephase_form["implementable"] = True
            dephase_form["patch"] = dp_built["patch"]
            dephase_form["main_path"] = str(p)
            EV["dephase"] = {"form": dephase_form, "pairs": {}}
            print("dephase surface: appends=%d units=%s -> built"
                  % (n_appends, u_appends), flush=True)
            flush_evid()

    # ---- 5) 各变体配对（逐变体边跑边写） ----
    ledger = {"version": RECORD_VERSION,
              "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              "units": [], "variant_stats": {}}
    arms = []
    if EV["care2"].get("variant", {}).get("kept"):
        arms.append(("care2", EV["care2"]["variant"]["main_path"], "care2"))
    if EV["fertilize_on"].get("variant", {}).get("kept"):
        arms.append(("fertilize_on",
                     EV["fertilize_on"]["variant"]["main_path"],
                     "fertilize_on"))
    if EV["dephase"].get("form", {}).get("implementable"):
        arms.append(("dephase", EV["dephase"]["form"]["main_path"], "dephase"))
    for vid, path, slot in arms:
        tv1 = time.perf_counter()
        rows_var, _ = _play(_specs_for(units_pairs, vid, path, True), run_cfg)
        EV["budget"]["judgment_局次"] += len(rows_var)
        var = {(int(r["seed"]), int(r["seat"])): r for r in rows_var}
        for r in rows_var:
            if r.get("error"):
                ANOMALIES.append("%s 红局 %s s%d: %s" % (
                    vid, r["seed"], r["seat"], r["error"]))
        stats = pair_stats(ctl, var, units_pairs)
        stats["elapsed_s"] = round(time.perf_counter() - tv1, 2)
        EV[slot]["pairs"] = stats
        EV["sell_phase"][vid] = sell_phase_agg(
            [r for r in rows_var if not r.get("error")])
        ledger["variant_stats"][vid] = {k: v for k, v in stats.items()
                                        if k != "rows_lite"}
        for row in stats["rows_lite"]:
            ledger["units"].append(dict(row, variant=vid))
        print("pair", vid, "W-L-T", stats["W"], stats["L"], stats["T"],
              "d", stats["mean_delta"], "netflip", stats["net_flip_wins"],
              "flips_neg", stats["flips_neg"], "pos", stats["positive_arm"],
              flush=True)
        flush_evid()

    # ---- 6) verdict ----
    per_variant = {}
    for vid, _p, slot in arms:
        ps = EV[slot].get("pairs") or {}
        per_variant[vid] = {"net_flip_wins": ps.get("net_flip_wins"),
                            "flips_neg": ps.get("flips_neg"),
                            "mean_delta": ps.get("mean_delta"),
                            "positive_arm": ps.get("positive_arm")}
    positive = [v for v, d in per_variant.items() if d.get("positive_arm")]
    v2 = [v for v in ("care2", "fertilize_on") if per_variant.get(v, {})
          .get("positive_arm")]
    v3 = "dephase" if per_variant.get("dephase", {}).get("positive_arm") else None
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "task1": ("分品实现价口径缺口已补（realized_base.per_item）；"
                  "谷底自伤判定见 realized_base.task1_answer"),
        "task2_positive_variants": v2,
        "task2_verdict": ("建模轮首验：care2/fertilize-on 均未达净翻胜>0∧不翻负"
                          "——结论否定" if not v2 else
                          "建模轮首验：%s 达判据（正臂候选）" % v2),
        "task3_positive": v3,
        "task3_verdict": (
            "dephase 无合法实现面（禁区下不可实现）"
            if not EV["dephase"].get("form", {}).get("implementable")
            else ("dephase 追加单挂拍轮转 %s"
                  % ("达判据（正臂候选）" if v3 else
                     "未达判据（净翻胜>0∧不翻负不成立）"))),
        "positive_variants": positive,
        "per_variant": per_variant,
    }
    EV["budget"]["total_局次"] = (EV["budget"]["auth_局次"]
                                 + EV["budget"]["judgment_局次"])
    EV["budget"]["within_cap"] = bool(EV["budget"]["total_局次"]
                                      <= BUDGET_CAP_GAMES)
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ledger["verdict"] = EV["verdict"]
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget", EV["budget"], flush=True)
    return EV


if __name__ == "__main__":
    main()
