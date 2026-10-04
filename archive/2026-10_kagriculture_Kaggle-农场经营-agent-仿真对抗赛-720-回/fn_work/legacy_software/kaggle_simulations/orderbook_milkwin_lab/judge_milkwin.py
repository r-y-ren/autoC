# -*- coding: utf-8 -*-
"""judge_milkwin：MODELPX 参数级实验判决（牛奶窗变现实验；判决先行·不发射
不提交）。

责任口径（任务 milk-window）：
- 机制=oc_c3 基座 MODELPX 预卖层参数级旋钮（MILK/STRAWBERRY/WOOL、
  阈 p_next<p_cur-THR、量帽三档 3/6/10、窗 h2-22 + hour-1 档）：帽位扫描
  {3/6/10 基线, 6/12/20, 10/20/30}（MILK 侧加权=仅 MILK 放大，余二品保基线）
  + 阈扫描 {0.5 基线, 0.2 更敏, 1.0 更钝}；臂 3 窗内地毯（d14-20 step
  336-480 MILK 日新高追加单帽 20/步）按预登记触发条件加跑。
- 判决：变体 vs oc_c3 配对（26 败局前 8 fold + 新中性 672000+i*107×8，
  n=16 双席/变体=32 (seed,seat) 单元/臂；对手 j23.DEFAULT_OPPONENTS 按 fold
  轮转）；附 d14-20 窗逐日收入对照（fill 口径影子引擎逐拍归因 + submit 口径
  挂单 qty×卖时市价）。
- 判据（预登记）：净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（配对 Δratio_fill
  MILK∧全品均值≥0）∧ d14-20 窗收入差转正（fill 口径总窗配对 Δ>0，对照
  oc_c3）。
- 读数：终局钱 farms[obs.player].money 干净口径；实现价=Σ(filled×成交价)/
  Σ(filled×base)（影子引擎逐拍归因）。
- 等价封印：mx_base（全基线参数）vs oc_c3 同 (seed,seat) 双席动作流逐字节等价
  + 终局钱相等——参数级手术行为保真证明。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤350 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-milk-window.json；账本落
orderbook_milkwin_lab/evidence/。复用（不改写）：sim_bridge.run_games/
sim_bridge、judge_r23.DEFAULT_OPPONENTS、kgenv.replay_profile 影子引擎。
只写 orderbook_milkwin_lab/ 与 fn_docs/hybrid/results/2026-09-29-milk-window.json。
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

RECORD_VERSION = "milk-window/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
LOSS_FOLDS = REPLAY_26[:8]                          # 26 败局 canonical 前 8 fold
NEUTRAL_FOLDS = [672000 + i * 107 for i in range(8)]  # 任务给定新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS                   # n=16 双席 fold/变体

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}
MX_ITEMS = ("MILK", "STRAWBERRY", "WOOL")
WINDOW = (336, 480)                                  # d14-20 窗（任务口径）
WIN_DAYS = tuple(range(WINDOW[0] // DAY, WINDOW[1] // DAY))  # 14..19

OC_C3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
                 / "main.py")
OC_C3_SHA_EXPECTED = ("3f8b57fd4d5e7070a40e444c130347bbc3ada58ff183ae163b1f3d"
                      "39ba9bd23d")
FORM_MAINS = {
    form: str(MODULE_DIR / "build" / form / "main.py")
    for form in ("mx_base", "mx_cap2", "mx_cap33", "mx_thr_m02", "mx_thr_m10",
                 "mx_carpet")
}
ARMS = {"oc_c3": OC_C3_MAIN, **FORM_MAINS}
SCAN_FORMS = ("mx_cap2", "mx_cap33", "mx_thr_m02", "mx_thr_m10")
SEAL_FORM = "mx_base"
CARPET_FORM = "mx_carpet"
RUN_FORMS = ("oc_c3", SEAL_FORM) + SCAN_FORMS        # 主跑臂序
ENTRY_NAME = "_mx_agent"

WORKERS = 2
BUDGET_CAP_GAMES = 350
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-milk-window.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "milkwin_ab_ledger.json"

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
    """单文件件装载（末 callable 语义）+ mx 台账报告字典（_MX_REPORT）。"""
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
    reports = {k: ns[k] for k in ("_MX_REPORT",)
               if isinstance(ns.get(k), dict)}
    return entries[-1], reports


def _snap_report(rep: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in rep.items()}


class _Tracer:
    """观察/动作/mx 台账逐拍追踪（不改动作）。"""

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


def shadow_window(sinks, seed) -> Dict[str, Any]:
    """影子引擎逐拍成交归因：全步分品 + d14-20 窗逐日分品（fill 口径
    filled/value）；submit 口径逐日由 sinks 挂单 qty×卖时市价。"""
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
    win: Dict[int, Dict[int, Dict[str, Dict[str, float]]]] = {0: {}, 1: {}}
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
        in_win = WINDOW[0] <= s < WINDOW[1]
        day = s // DAY
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
                row = acc[pl].setdefault(item, {"filled": 0.0, "value": 0.0})
                row["filled"] += filled
                row["value"] += value
                if in_win:
                    wrow = win[pl].setdefault(day, {}).setdefault(
                        item, {"filled": 0.0, "value": 0.0})
                    wrow["filled"] += filled
                    wrow["value"] += value
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
    # submit 口径逐日（我席/对面均取，便于逐日对照）
    sub: Dict[int, Dict[int, Dict[str, Dict[str, float]]]] = {0: {}, 1: {}}
    for seat in (0, 1):
        for entry in (sinks.get(seat) or []):
            s, obs, act = int(entry[0]), entry[1], entry[2]
            if not (WINDOW[0] <= s < WINDOW[1]) or not isinstance(act, dict):
                continue
            prices = ((obs.get("market") or {}) if isinstance(
                obs.get("market"), dict) else {}).get("prices") or {}
            day = s // DAY
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
                row = sub[seat].setdefault(day, {}).setdefault(
                    item, {"qty": 0.0, "value": 0.0})
                row["qty"] += q
                row["value"] += q * float(px)
    return {"per_item_by_seat": acc, "window_fill_by_seat": win,
            "window_submit_by_seat": sub,
            "shadow_mismatch_steps": mism}


def end_reads(sink) -> Dict[str, Any]:
    """终局读数：终局钱 farms[obs.player].money + 终局滞留（末拍 shed×quote）。"""
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
        if str(item) in MX_ITEMS:
            by_item[str(item)] = round(v, 2)
    return {"terminal_money": tm, "stranding": round(total, 2),
            "stranding_mx_items": by_item}


def mx_reads(sink) -> Dict[str, Any]:
    """mx 台账末拍累计（地毯触发面；step0 复位→末拍=局总量）。"""
    last = None
    for entry in (sink or []):
        tel = entry[3] if len(entry) > 3 else None
        if isinstance(tel, dict) and isinstance(tel.get("_MX_REPORT"), dict):
            last = tel["_MX_REPORT"]
    return dict(last) if isinstance(last, dict) else {"present": False}


def _stream_digest(sink):
    """我席动作流 digest（逐拍 act 序列）。"""
    try:
        acts = [entry[2] for entry in (sink or [])]
        return hashlib.sha256(
            json.dumps(acts, default=str, sort_keys=True)
            .encode()).hexdigest()[:16]
    except Exception:
        return "err"


# ------------------------------------------------------------ 局跑口 --
def _build_agents_mx(spec):
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
            agents, sinks = _build_agents_mx(spec)
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
               "window": None, "mx": None, "stream_sha_our": None}
        if berr is not None:
            row["error"] = berr["build_error"]
        if row["banks"] is not None and row["error"] is None and sinks:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            our, opp = sinks[row["seat"]], sinks[1 - row["seat"]]
            row["reads"] = end_reads(our)
            row["items"] = item_reads(our)
            row["mx"] = mx_reads(our)
            row["stream_sha_our"] = _stream_digest(our)
            sw = shadow_window(sinks, int(spec["seed"]))
            row["shadow"] = sw
            if isinstance(sw, dict) and "window_fill_by_seat" in sw:
                row["window"] = {
                    "fill": sw["window_fill_by_seat"].get(row["seat"]) or {},
                    "submit": sw["window_submit_by_seat"].get(row["seat"])
                    or {}}
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
                   else "neutral_672000_i107")
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
            "game_id": "mw-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


# ------------------------------------------------------------ 聚合 --
def pair_stats(ctl: Dict, var: Dict, kept_units: List[Dict]) -> Dict:
    """配对聚合：W-L-T（Δ 口径）/Δ/翻负/净翻胜（knee 同口径）。"""
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
    """分品实现价聚合：Σ(filled×成交价)/Σ(filled×base)（成交价口径）+ 提交口径。"""
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
            acc = sh.setdefault(item, {"filled": 0.0, "value": 0.0})
            acc["filled"] += float(row.get("filled") or 0)
            acc["value"] += float(row.get("value") or 0)
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


def _ratio_row(r, item=None):
    """单局实现价（fill 口径 ratio）：全品或单品。"""
    sw = r.get("shadow") or {}
    by = (sw.get("per_item_by_seat") or {}).get(int(r.get("seat", 0))) or {}
    num = den = 0.0
    items = [item] if item else list(by.keys())
    for it in items:
        row = by.get(it) or by.get(str(it)) or {}
        base = float(BASE_PX.get(it, 0) or 0)
        filled = float(row.get("filled") or 0)
        value = float(row.get("value") or 0)
        if base and filled:
            num += value
            den += filled * base
    return (num / den) if den else None


def realized_paired(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """实现价配对 Δ（变体−对照；判据=均值≥0，MILK∧全品）。"""
    out: Dict[str, Any] = {}
    for tag, item in (("all", None), ("milk", "MILK")):
        deltas, rows = [], []
        for u in units:
            key = (u["seed"], u["seat"])
            rc, rv = ctl.get(key), var.get(key)
            if not rc or not rv:
                continue
            vc, vv = _ratio_row(rc, item), _ratio_row(rv, item)
            if vc is None or vv is None:
                continue
            d = float(vv) - float(vc)
            deltas.append(d)
            rows.append({"seed": u["seed"], "seat": u["seat"],
                         "ratio_control": round(vc, 4),
                         "ratio_variant": round(vv, 4),
                         "delta": round(d, 4)})
        out[tag] = {
            "n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 4) if deltas
            else UNKNOWN,
            "median_delta": round(statistics.median(deltas), 4) if deltas
            else UNKNOWN,
            "n_up": sum(1 for d in deltas if d > 0),
            "nonneg": bool(deltas and (sum(deltas) / len(deltas)) >= 0),
            "rows_lite": rows[:12]}
    out["nonneg_both"] = bool(out["all"]["nonneg"] and out["milk"]["nonneg"])
    return out


def _win_row(w) -> Dict[str, float]:
    """单局窗读数（fill/submit 口径总量 + MILK + 逐日总量）。"""
    out = {"fill_total": 0.0, "fill_milk": 0.0, "submit_total": 0.0,
           "submit_milk": 0.0}
    per_day_fill = {}
    per_day_milk = {}
    for day, items in ((w.get("fill") or {})).items():
        dt = dm = 0.0
        for item, row in (items or {}).items():
            v = float((row or {}).get("value") or 0)
            dt += v
            if item == "MILK":
                dm += v
        out["fill_total"] += dt
        out["fill_milk"] += dm
        per_day_fill[int(day)] = dt
        per_day_milk[int(day)] = dm
    for day, items in ((w.get("submit") or {})).items():
        for item, row in (items or {}).items():
            v = float((row or {}).get("value") or 0)
            out["submit_total"] += v
            if item == "MILK":
                out["submit_milk"] += v
    out["per_day_fill_total"] = per_day_fill
    out["per_day_fill_milk"] = per_day_milk
    return out


def window_agg(rows: List[Dict]) -> Dict[str, Any]:
    """窗收入聚合（d14-20 step 336-480；逐日均值 + 总量均值）。"""
    n = 0
    sums = {"fill_total": 0.0, "fill_milk": 0.0, "submit_total": 0.0,
            "submit_milk": 0.0}
    day_t = {d: 0.0 for d in WIN_DAYS}
    day_m = {d: 0.0 for d in WIN_DAYS}
    for r in rows:
        w = r.get("window")
        if not isinstance(w, dict):
            continue
        wr = _win_row(w)
        n += 1
        for k in sums:
            sums[k] += wr[k]
        for d in WIN_DAYS:
            day_t[d] += wr["per_day_fill_total"].get(d, 0.0)
            day_m[d] += wr["per_day_fill_milk"].get(d, 0.0)
    n = max(1, n)
    return {
        "n_games": n,
        "window": "d14-20（step 336-480）",
        "mean_fill_total": round(sums["fill_total"] / n, 1),
        "mean_fill_milk": round(sums["fill_milk"] / n, 1),
        "mean_submit_total": round(sums["submit_total"] / n, 1),
        "mean_submit_milk": round(sums["submit_milk"] / n, 1),
        "per_day_fill_total_mean": {str(d): round(day_t[d] / n, 1)
                                    for d in WIN_DAYS},
        "per_day_fill_milk_mean": {str(d): round(day_m[d] / n, 1)
                                   for d in WIN_DAYS},
    }


def window_paired(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """窗收入配对 Δ（变体−对照）：总窗 + 逐日（fill 主口径/submit 对照）。"""
    keys = ("fill_total", "fill_milk", "submit_total", "submit_milk")
    deltas = {k: [] for k in keys}
    day_dt = {d: [] for d in WIN_DAYS}
    day_dm = {d: [] for d in WIN_DAYS}
    rows_lite = []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        wc = (rc or {}).get("window")
        wv = (rv or {}).get("window")
        if not isinstance(wc, dict) or not isinstance(wv, dict):
            continue
        vc, vv = _win_row(wc), _win_row(wv)
        row = {"seed": u["seed"], "seat": u["seat"]}
        for k in keys:
            d = vv[k] - vc[k]
            deltas[k].append(d)
            row["d_" + k] = round(d, 1)
        for d in WIN_DAYS:
            dd = (vv["per_day_fill_total"].get(d, 0.0)
                  - vc["per_day_fill_total"].get(d, 0.0))
            dm = (vv["per_day_fill_milk"].get(d, 0.0)
                  - vc["per_day_fill_milk"].get(d, 0.0))
            day_dt[d].append(dd)
            day_dm[d].append(dm)
            row["d_day%d_fill_total" % d] = round(dd, 1)
            row["d_day%d_fill_milk" % d] = round(dm, 1)
        rows_lite.append(row)

    def _agg(vals):
        return {"n": len(vals),
                "mean_delta": round(sum(vals) / len(vals), 2) if vals
                else UNKNOWN,
                "median_delta": round(statistics.median(vals), 2) if vals
                else UNKNOWN,
                "n_pos": sum(1 for v in vals if v > 0),
                "n_neg": sum(1 for v in vals if v < 0)}

    return {k: _agg(deltas[k]) for k in keys} | {
        "per_day_fill_total_delta": {str(d): _agg(day_dt[d])
                                     for d in WIN_DAYS},
        "per_day_fill_milk_delta": {str(d): _agg(day_dm[d])
                                    for d in WIN_DAYS},
        "rows_lite": rows_lite}


def end_agg(rows: List[Dict]) -> Dict[str, Any]:
    """终局钱聚合（farms[obs.player].money）。"""
    tms = [float(r["reads"]["terminal_money"]) for r in rows
           if isinstance(r.get("reads"), dict)
           and is_num(r["reads"].get("terminal_money"))]
    return {
        "terminal_money_mean": round(sum(tms) / len(tms), 1) if tms else UNKNOWN,
        "terminal_money_median": round(statistics.median(tms), 1) if tms
        else UNKNOWN,
    }


def seal_check(ctl: Dict, var: Dict, units: List[Dict]) -> Dict[str, Any]:
    """等价封印：mx_base vs oc_c3 同 (seed,seat) 动作流逐字节等价 + 终局钱相等。"""
    n = n_sha = n_money = 0
    bad = []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        if not rc or not rv:
            continue
        n += 1
        same_sha = (rc.get("stream_sha_our") is not None
                    and rc.get("stream_sha_our") == rv.get("stream_sha_our"))
        mc = ((rc.get("reads") or {}).get("terminal_money"))
        mv = ((rv.get("reads") or {}).get("terminal_money"))
        same_money = is_num(mc) and is_num(mv) and abs(float(mc) - float(mv)) \
            < 1e-6
        if same_sha:
            n_sha += 1
        if same_money:
            n_money += 1
        if not (same_sha and same_money) and len(bad) < 8:
            bad.append({"seed": u["seed"], "seat": u["seat"],
                        "sha_control": rc.get("stream_sha_our"),
                        "sha_variant": rv.get("stream_sha_our"),
                        "money_control": mc, "money_variant": mv})
    return {"design": "mx_base（全基线参数）vs oc_c3 同 (seed,seat) 双席：我席"
                      "逐拍动作流 digest 全等 + 终局钱相等（参数级手术行为保真"
                      "封印）",
            "n_units": n, "n_stream_identical": n_sha,
            "n_money_equal": n_money,
            "passed": bool(n and n_sha == n and n_money == n),
            "violations": bad}


# ------------------------------------------------------------ main --
def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES,
              "smoke_局次": 1,
              "auth_局次": 0, "judgment_局次": 0, "carpet_局次": 0}

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("牛奶窗变现武器实验（milk-window；参数级合法面·判决先行"
                       "不发射）：镜像败局钱差集中 d14-20 窗（step 336-480，"
                       "品类主差 MILK）——MODELPX 预卖层帽位/阈位扫描 + 窗内地毯"
                       "条件臂，变体 vs oc_c3 配对"),
        "source": {
            "commands": ["python3 orderbook_milkwin_lab/build_milkwin.py",
                         "python3 orderbook_milkwin_lab/judge_milkwin.py"],
            "base_main": OC_C3_MAIN, "base_sha256": base_sha,
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*107（任务给定新中性块 n=8）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局回放（canonical 前 8 fold）+ 新中性块"
                                 " 672000+i*107（i=0..7）；双席 fold n=16/变体"
                                 "=32 (seed,seat) 单元/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": {
                "unit": "配对单元=(seed,seat)；每臂 16 fold×双席=32 局",
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-20 窗 step 336-480 逐日=step//24（14..19）；"
                          "fill 口径=影子引擎逐拍归因 Σ(filled×成交价)；"
                          "submit 口径=挂单 qty×卖时市价",
                "realized_px": "Σ(filled×成交价)/Σ(filled×base)（影子引擎）",
            },
            "criterion": ("净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（配对 Δratio_fill "
                          "MILK∧全品均值≥0）∧ d14-20 窗收入差转正（fill 口径总窗"
                          "配对 Δ>0，对照 oc_c3）"),
            "carpet_trigger_rule": ("臂 1/2 有效=任一扫描变体 d14-20 窗 fill 口径"
                                    "总窗配对 mean Δ>0 → 加跑 mx_carpet；否则"
                                    "按预登记条件跳过并留档"),
        },
        "mechanism": {
            "layer": "件 MX（尾块注入沿 append 先例；宿主=oc_c3 件 _hs_agent；"
                     "入口=_mx_agent 末 callable）",
            "surgery": "参数级：基座 MODELPX 3 组字面量同参替换（阈×4/帽位档式"
                       "×1/hour-1 帽×3，计数台账+反替换回程逐字节封印）",
            "items": list(MX_ITEMS),
            "thr_rule": "压力测试 p_next<p_cur-THR（基线 0.5；0.2 更敏/1.0 更钝）",
            "cap_rule": "量帽三档（默认/中/高）基线 3/6/10；MILK 侧加权=仅 MILK"
                        "放大至 6/12/20 或 10/20/30，STRAWBERRY/WOOL 保基线；"
                        "价格模型 planned=6 不参改",
            "carpet_rule": "d14-20（step 336-480）MILK 日新高追加单（p_now≥当日"
                           "窗内高点，帽 20/步）：只加同拍挂卖、量限投射仓未挂"
                           "余量、同拍买侧 MILK 不动、满 10 单不加、异常回退",
            "constraints": ["零跨拍挪量（R23/R26 红线）", "磁带 blob 零触碰",
                            "守恒：只挂卖自己投射仓存量", "异常回退原动作"],
        },
        "variants": {},
        "gates_seal": {},
        "pairs": {},
        "window_stats": {},
        "per_item_realized": {},
        "realized_px_paired": {},
        "terminal_money": {},
        "criteria": {},
        "verdict": {},
        "budget": budget,
    })
    flush_evid()

    # ---- 0) 构建参数入账 ----
    for form in FORM_MAINS:
        man = json.loads((MODULE_DIR / "build" / form /
                          "build_manifest.json").read_text(encoding="utf-8"))
        EV["variants"][form] = {"params": man.get("params"),
                                "main_sha256": man.get("main_sha256"),
                                "injected_tail_bytes": man.get(
                                    "injected_tail_bytes"),
                                "subs": man.get("subs"),
                                "roundtrip_identity_ok":
                                    man.get("roundtrip_identity_ok"),
                                "entry_last_callable":
                                    man.get("entry_last_callable")}
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
    budget["auth_局次"] = 60
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

    # ---- 2) 管线冒烟 1 局（非 fold 语料，不入配对） ----
    smoke_units = [{"seed": 2026092999, "seat": 0,
                    "opp_path": opp_paths[0], "opponent": "r37",
                    "stratum": "smoke"}]
    smoke_rows, _e0 = _play(make_specs("smoke", ARMS["oc_c3"], smoke_units),
                            run_cfg)
    print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
          flush=True)
    if smoke_rows[0].get("error"):
        ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
    flush_evid()

    # ---- 3) 六臂实跑（oc_c3 对照 + mx_base 封印 + 4 扫描变体） ----
    rows_by_arm: Dict[str, List[Dict[str, Any]]] = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget["judgment_局次"] += len(rows)
        EV["per_item_realized"][arm] = realized_agg(rows)
        EV["terminal_money"][arm] = end_agg(rows)
        EV["window_stats"][arm] = window_agg(rows)
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d（见 rows_lite error 字段）"
                             % (arm, n_err, len(rows)))
        mism = EV["per_item_realized"][arm]["aggregate"].get(
            "shadow_mismatch_steps")
        if mism:
            ANOMALIES.append("%s 影子引擎不一致步 %s（窗收入 fill 口径见噪声）"
                             % (arm, mism))
        print(arm, "games", len(rows), "err", n_err,
              "tm", EV["terminal_money"][arm]["terminal_money_mean"],
              "win_fill_total",
              EV["window_stats"][arm]["mean_fill_total"],
              "shadow_mism", mism,
              round(time.perf_counter() - t2, 1), "s", flush=True)
        EV["budget"] = budget
        flush_evid()

    # ---- 4) 等价封印（mx_base vs oc_c3） ----
    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    seal = seal_check(ctl, {(r["seed"], r["seat"]): r
                            for r in rows_by_arm[SEAL_FORM]}, units)
    EV["gates_seal"] = seal
    if not seal["passed"]:
        ANOMALIES.append("等价封印未全过：mx_base 与 oc_c3 动作流/终局钱"
                         "存在差异（参数级手术行为非保真，Δ归因存疑）")
    print("seal:", seal["n_stream_identical"], "/", seal["n_units"],
          "money", seal["n_money_equal"], flush=True)
    flush_evid()

    # ---- 5) 配对判决（4 扫描变体 vs oc_c3） ----
    def _judge_form(form):
        var = {(r["seed"], r["seat"]): r for r in rows_by_arm[form]}
        ps = pair_stats(ctl, var, units)
        wp = window_paired(ctl, var, units)
        rp = realized_paired(ctl, var, units)
        EV["pairs"]["%s_vs_oc_c3" % form] = ps
        EV["window_stats"]["paired_%s_vs_oc_c3" % form] = wp
        EV["realized_px_paired"]["%s_vs_oc_c3" % form] = rp
        win_d = wp["fill_total"]["mean_delta"]
        crit = {
            "净翻胜>0": ps["net_flip_wins"] > 0,
            "flips_neg==0": ps["flips_neg"] == 0,
            "实现价非负（Δratio_fill MILK∧全品均值≥0）": rp["nonneg_both"],
            "d14-20窗收入差转正（fill 总窗配对 mean Δ>0）": is_num(win_d)
            and float(win_d) > 0,
        }
        EV["criteria"][form] = {
            "checks": crit,
            "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
            "window_fill_total_mean_delta": win_d,
            "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
            "realized_px_nonneg_both": rp["nonneg_both"],
            "positive_arm": all(crit.values())}
        print(form, "vs oc_c3:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
              "dM", ps["mean_delta"], "netflip", ps["net_flip_wins"],
              "flips_neg", ps["flips_neg"],
              "dWin", win_d, "dWinMilk", wp["fill_milk"]["mean_delta"],
              "px_nonneg", rp["nonneg_both"],
              "crit", crit, flush=True)
        flush_evid()

    for form in SCAN_FORMS:
        _judge_form(form)

    # ---- 6) 臂 3 窗内地毯（条件加跑） ----
    carpet_reason = None
    any_window_pos = any(
        is_num(EV["criteria"][f]["window_fill_total_mean_delta"])
        and float(EV["criteria"][f]["window_fill_total_mean_delta"]) > 0
        for f in SCAN_FORMS)
    if any_window_pos:
        carpet_reason = ("臂 1/2 有效（≥1 扫描变体 d14-20 窗 fill 总窗配对 "
                         "mean Δ>0）→ 加跑 mx_carpet")
        specs = make_specs(CARPET_FORM, ARMS[CARPET_FORM], units)
        t3 = time.perf_counter()
        rows, _e3 = _play(specs, run_cfg)
        rows_by_arm[CARPET_FORM] = rows
        budget["carpet_局次"] += len(rows)
        EV["per_item_realized"][CARPET_FORM] = realized_agg(rows)
        EV["terminal_money"][CARPET_FORM] = end_agg(rows)
        EV["window_stats"][CARPET_FORM] = window_agg(rows)
        carpet_trig = sum(int((r.get("mx") or {}).get("carpet_steps") or 0)
                          for r in rows)
        carpet_units = sum(int((r.get("mx") or {}).get("carpet_units") or 0)
                           for r in rows)
        EV["variants"][CARPET_FORM]["trigger_surface"] = {
            "carpet_steps_total": carpet_trig,
            "carpet_units_total": carpet_units,
            "games_with_carpet": sum(
                1 for r in rows
                if int((r.get("mx") or {}).get("carpet_steps") or 0) > 0)}
        _judge_form(CARPET_FORM)
        print("carpet done", round(time.perf_counter() - t3, 1), "s trig",
              carpet_trig, "units", carpet_units, flush=True)
    else:
        carpet_reason = ("臂 1/2 均未现窗收入差转正（预登记触发条件不满足）→ "
                         "mx_carpet 未加跑")
    EV["carpet_arm"] = {"form": CARPET_FORM, "ran": any_window_pos,
                        "reason": carpet_reason}
    budget["total_局次"] = (budget["auth_局次"] + budget["judgment_局次"]
                           + budget["carpet_局次"] + budget["smoke_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES

    # ---- 7) verdict ----
    judged = list(SCAN_FORMS) + ([CARPET_FORM] if any_window_pos else [])
    positives = [f for f in judged if EV["criteria"][f]["positive_arm"]]
    milk_px = {}
    for arm in RUN_FORMS + ((CARPET_FORM,) if any_window_pos else ()):
        per = EV["per_item_realized"][arm].get("per_item") or {}
        milk_px[arm] = {i: {"ratio_fill": per.get(i, {}).get("ratio_fill"),
                            "filled_qty": per.get(i, {}).get("filled_qty")}
                        for i in MX_ITEMS}
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "positive_variants": positives,
        "per_variant": {
            f: {"net_flip_wins": EV["criteria"][f]["net_flip_wins"],
                "flips_neg": EV["criteria"][f]["flips_neg"],
                "mean_delta": EV["pairs"]["%s_vs_oc_c3" % f]["mean_delta"],
                "window_fill_total_mean_delta":
                    EV["criteria"][f]["window_fill_total_mean_delta"],
                "window_fill_milk_mean_delta":
                    EV["criteria"][f]["window_fill_milk_mean_delta"],
                "realized_px_nonneg_both":
                    EV["criteria"][f]["realized_px_nonneg_both"],
                "positive_arm": EV["criteria"][f]["positive_arm"]}
            for f in judged},
        "seal_passed": seal["passed"],
        "mx_items_ratio_fill": milk_px,
        "verdict": ("牛奶窗变现正臂：%s" % (", ".join(positives) if positives
                                           else "无（受测变体均未全过四判据）")),
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行（件自报 "
                     "telemetry）；kaggle_environments 可选环境加载告警")
    ANOMALIES.append("窗口径备忘：d14-20 窗=step 336-480（任务给定），逐日桶="
                     "step//24（14..19 共 6 桶）")
    ANOMALIES.append("帽位扫描 MILK 侧加权读法：量帽放大仅施于 MILK，"
                     "STRAWBERRY/WOOL 保持 3/6/10（一臂一旋钮归因）")
    LEDGER_PATH.write_text(json.dumps(
        {"pairs": {k: {"n": v["n"], "W": v["W"], "L": v["L"], "T": v["T"],
                       "mean_delta": v["mean_delta"],
                       "net_flip_wins": v["net_flip_wins"],
                       "flips_neg": v["flips_neg"]}
                   for k, v in EV["pairs"].items()},
         "window": {k: {"fill_total_mean_delta":
                        v["fill_total"]["mean_delta"],
                        "fill_milk_mean_delta": v["fill_milk"]["mean_delta"]}
                    for k, v in EV["window_stats"].items()
                    if k.startswith("paired_")},
         "criteria": EV["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
