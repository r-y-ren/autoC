# -*- coding: utf-8 -*-
"""judge_v89full_arena（v89 lab）：v89_full 遗留候选紧急池快筛（判决先行·不发射/不提交）。

背景：analysis40 判决 V89 基底升级 H1_HOLD（v89_pure vs H1 0.2174）时注记
"v89_full 预案留档未判"。本 harness 就地补判 v89_full（V89 基座+X1 卫生+
画像器+C3 羊毛相位，build/v89_full/main.py，SHA f6362e3d…，构建校验+G793
零冲突审计已绿）——零修改直跑。

面板（每对 n=12 fold 双席=24 局，中性块 674000+i*131）：
  v89_full vs {H1 王座锚（H1/oc_c3 行为孪生，BT 527.8），mpx, r40, A}
判定重点：G793 门在面板是否会触发（逐局 _G793_REPORT/_G793_STATE 经 entry
__globals__ 采集，judge_v89 同口径）；触发局 vs H1 是否翻盘（触发 fold 子集
W/L/T 拆分）。
口径：h2h=judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；缺席/红局
→该 seed 记负 fail-closed）；margin=farms[obs.player] 终局钱差（干净口径，
banks 交叉登记）；realized_px=Σ(qty×卖时价)/Σ(qty×base)（BASE_PX milkwin 表）。
判决三档：BEATS_CEILING（vs 王座 H1 ≥0.5）/ COMPETITIVE（0.35-0.5）/
WEAK（<0.35）/ UNRUNNABLE。
证据 orderbook_v89_lab/evidence/v89full_arena.json。只写本 lab 与本 evidence。
不改既有代码；不提交；不发射。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_goose_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
EV_PATH = EVID_DIR / "v89full_arena.json"

ARM = HERE / "build" / "v89_full" / "main.py"
H1 = KSIM_DIR / "orderbook_topform_lab" / "build" / "h1" / "main.py"
MPX = (KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
       / "main.py")
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
A = KSIM_DIR / "orderbook_r44_a" / "main.py"

PANEL = {"H1": H1, "mpx": MPX, "r40": R40, "A": A}
SHA = {
    "v89_full": "f6362e3d500e18666f2b5585413a30fd9a10285462770b8eb8af9ad8672b81a8",
    "H1": "76b5f842249efa4c89ef841e51212d7cefc886223655683eeb6764974b22f337",
    "mpx": "f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72c3d84e44f",
    "r40": "4ce951f088740e0b3d4366dbf95f8bb225817b0417bbb2fcea6292a559ee9ea8",
    "A": "b387307fc12e26107c58ee604146fc621099ce88124fa0876fdd7cef28300bd9",
}
N_FOLDS = int(os.environ.get("V89F_FOLDS", "12"))
PANEL_FOLDS = [674000 + i * 131 for i in range(N_FOLDS)]
WORKERS = 2

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    EV_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                  default=str) + "\n", encoding="utf-8")


# ==================================================== 层台账（G793 门） ==
def _layer_stats(entry):
    """经 entry.__globals__ 采该局层台账（G793 门/画像/C3/X1；judge_v89 同口径）。"""
    g = getattr(entry, "__globals__", None)
    out = {}
    if not isinstance(g, dict):
        return out
    rep = g.get("_G793_REPORT")
    if isinstance(rep, dict):
        out["g793"] = {k: int(rep.get(k, 0) or 0)
                       for k in ("calls", "classified", "bypassed", "errors")}
    st = g.get("_G793_STATE")
    if isinstance(st, dict):
        out["g793_state"] = {
            str(s): {"disable": bool(v.get("disable")),
                     "decided": bool(v.get("decided"))}
            for s, v in st.items() if isinstance(v, dict)}
    oc = g.get("_OC_STATE")
    if isinstance(oc, dict):
        out["oc_classes"] = {str(k): (d.get("cls") or "unknown")
                             for k, d in oc.items() if isinstance(d, dict)}
        sw = g.get("_OC_C3_SWAPPED")
        if isinstance(sw, list) and sw:
            out["oc_c3_swapped"] = bool(sw[0])
    x1 = g.get("_X1_REPORT")
    if isinstance(x1, dict):
        out["x1"] = {k: int(v) for k, v in x1.items()
                     if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return out


def wool_probe(sink):
    """羊毛供给读数：卖出笔数/总量/实现价/首末步（C3 相位观察）。"""
    qty = 0.0
    val = 0.0
    n = 0
    steps = []
    for step, obs, act in (sink or []):
        if not isinstance(act, dict):
            continue
        prices = ((obs.get('market') or {}) if isinstance(obs.get('market'),
                  dict) else {}).get('prices') or {}
        for cmd in (act.get('market') or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL" and str(cmd[1]) == "WOOL":
                px = prices.get("WOOL")
                try:
                    q = float(cmd[2])
                except Exception:
                    continue
                if q > 0 and isinstance(px, (int, float)):
                    qty += q
                    val += q * float(px)
                    n += 1
                    steps.append(int(step))
    return {"n_sells": n, "qty": round(qty, 1),
            "rpx": round(val / qty, 4) if qty > 0 else None,
            "first_step": min(steps) if steps else None,
            "last_step": max(steps) if steps else None}


def realized_px(sink):
    """提交口径实现价：Σ(qty×卖时市价)/Σ(qty×base)（BASE_PX milkwin 表）。"""
    val = 0.0
    base = 0.0
    for _step, obs, act in (sink or []):
        if not isinstance(act, dict):
            continue
        prices = ((obs.get('market') or {}) if isinstance(obs.get('market'),
                  dict) else {}).get('prices') or {}
        for cmd in (act.get('market') or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                item = str(cmd[1])
                px = prices.get(item)
                try:
                    q = float(cmd[2])
                except Exception:
                    continue
                b = float(BASE_PX.get(item, 0) or 0)
                if isinstance(px, (int, float)) and q > 0 and b > 0:
                    val += q * float(px)
                    base += q * b
    return round(val / base, 4) if base > 0 else None


# ============================================================ 跑口 ==
def _chunk(payload):
    """worker：双席 trace 局；干净口径 margin + G793 层台账 + 羊毛读数。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = [], ({0: [], 1: []} if spec.get("trace") else None)
            entries = []
            for seat, a in enumerate(spec["agents"]):
                inner = j23._load_entry(a.get("path"))
                entries.append(inner)
                if sinks is not None:
                    agents.append(j23._Tracer(inner, seat, sinks[seat]))
                else:
                    agents.append(inner)
            games.append({"seed": int(spec["seed"]), "agents": agents})
            metas.append((spec, sinks, entries, None))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, [], repr(exc)[:120]))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, entries, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "opponent": spec.get("opponent"), "group": spec.get("group"),
               "engine": res.get("engine"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None,
               "rpx_us": None, "rpx_opp": None,
               "wool_us": None, "wool_opp": None, "layer": {}}
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
                row["rpx_us"] = realized_px(sinks[row["seat"]])
                row["rpx_opp"] = realized_px(sinks[1 - row["seat"]])
                row["wool_us"] = wool_probe(sinks[row["seat"]])
                row["wool_opp"] = wool_probe(sinks[1 - row["seat"]])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(
                    b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
        if len(entries) > row["seat"] and row["error"] is None:
            try:
                row["layer"] = _layer_stats(entries[row["seat"]])
            except Exception as exc:
                row["layer_error"] = repr(exc)[:100]
        out.append(row)
    return out


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(group, opp_name, opp_path, folds):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            specs.append({
                "game_id": "v89f|%s|%s|%d-s%d" % (group, opp_name, seed, seat),
                "seed": int(seed), "arm": "v89_full", "arm_path": str(ARM),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "group": group, "kind": "ab",
                "trace": True,
                "agents": [{"type": "python", "path": str(ARM)},
                           {"type": "python", "path": str(opp_path)}]})
    for s in specs:
        if s["our_seat"] == 1:
            s["agents"].reverse()
    return specs


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows
           if isinstance(r.get("tm_opp"), (int, float))]
    rpx_u = [r["rpx_us"] for r in rows
             if isinstance(r.get("rpx_us"), (int, float))]
    rpx_o = [r["rpx_opp"] for r in rows
             if isinstance(r.get("rpx_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin"] = round(sum(r["margin_clean"] for r in rows
                                 if r["margin_clean"] is not None)
                             / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["realized_px_us"] = round(sum(rpx_u) / len(rpx_u), 4) if rpx_u else None
    f["realized_px_opp"] = round(sum(rpx_o) / len(rpx_o), 4) if rpx_o else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def g793_agg(rows):
    """G793 门触发面聚合 + 触发 fold 子集拆分（翻盘判定用）。"""
    agg = {"n_units": len(rows),
           "sum_calls": 0, "sum_classified": 0, "sum_bypassed": 0,
           "sum_errors": 0,
           "n_games_bypassed": 0, "n_games_classified": 0}
    for r in rows:
        g = (r.get("layer") or {}).get("g793") or {}
        agg["sum_calls"] += int(g.get("calls", 0) or 0)
        agg["sum_classified"] += int(g.get("classified", 0) or 0)
        agg["sum_bypassed"] += int(g.get("bypassed", 0) or 0)
        agg["sum_errors"] += int(g.get("errors", 0) or 0)
        if int(g.get("classified", 0) or 0) > 0:
            agg["n_games_classified"] += 1
        if int(g.get("bypassed", 0) or 0) > 0:
            agg["n_games_bypassed"] += 1
    # fold 子集：任一席该局 bypassed>0 → 该 fold 记"触发"
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    seeds = {}
    for r in rows:
        seeds.setdefault(r["seed"], []).append(r)
    trig_rows, nontrig_rows = [], []
    for seed, rs in seeds.items():
        trig = any(int(((x.get("layer") or {}).get("g793") or {}).get(
            "bypassed", 0) or 0) > 0 for x in rs)
        (trig_rows if trig else nontrig_rows).extend(rs)
    agg["n_folds_trigger"] = len({r["seed"] for r in trig_rows})
    agg["n_folds_no_trigger"] = len({r["seed"] for r in nontrig_rows})
    if trig_rows:
        agg["folds_trigger"] = j44._fold_arm(
            [{"seed": r["seed"], "margin": r["margin_clean"]}
             for r in trig_rows])
    if nontrig_rows:
        agg["folds_no_trigger"] = j44._fold_arm(
            [{"seed": r["seed"], "margin": r["margin_clean"]}
             for r in nontrig_rows])
    return agg


def wool_agg(rows):
    def _sum(side):
        qty = 0.0
        val = 0.0
        n = 0
        firsts = []
        for r in rows:
            w = r.get(side) or {}
            q = float(w.get("qty", 0) or 0)
            if q > 0 and w.get("rpx") is not None:
                qty += q
                val += q * float(w["rpx"])
                n += int(w.get("n_sells", 0) or 0)
                if w.get("first_step") is not None:
                    firsts.append(int(w["first_step"]))
        return {"qty_total": round(qty, 1), "n_sells_total": n,
                "rpx_wavg": round(val / qty, 4) if qty > 0 else None,
                "first_step_mean": round(sum(firsts) / len(firsts), 1)
                if firsts else None}
    return {"us": _sum("wool_us"), "opp": _sum("wool_opp")}


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"auth": 0, "panel": 0}

    EV.update({
        "version": "v89full-arena/1.0",
        "task": "v89_full（V89 基座+X1+画像器+C3，analysis40 注记'预案留档未判'）"
                "紧急池快筛：找比王座（H1/oc_c3，BT 527.8）更好的版本"
                "（判决先行·只测不发·不提交）",
        "piece": {
            "arm": "v89_full", "main": str(ARM), "sha256": SHA["v89_full"],
            "entry_last_callable": "_hs_agent",
            "layers": ["x1_hygiene", "profiler", "c3_wool_phase"],
            "g793_mechanism": "step96-119 镜像谱判门（结构镜像∧现金差≥20=cha22 "
                              "谱特征→跳过投机置换）；触发读数=_G793_REPORT/"
                              "_G793_STATE 经 entry __globals__ 采集",
            "provenance": "haodou092/kaggriculture-harvest-ledger V89 基底"
                          "（2026-09-29 拉取）+我方 X1/画像器/C3 层合成；"
                          "构建记录 orderbook_v89_lab/evidence/build_v89.json",
        },
        "source": {
            "commands": ["python3 orderbook_v89_lab/judge_v89full_arena.py"],
            "corpus": {
                "panel_folds": PANEL_FOLDS,
                "panel_spec": "中性块 674000+i*131（i=0..%d）；每对 n=%d fold "
                              "双席=%d 局" % (N_FOLDS - 1, N_FOLDS, 2 * N_FOLDS),
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/"
                       "余平；缺席/红局→该 seed 记负 fail-closed）",
                "margin": "farms[obs.player] 终局钱差（干净口径；banks 交叉"
                          "登记 margin_banks）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×base)（提交口径；"
                               "BASE_PX=milkwin 表）",
                "g793": "逐局 _G793_REPORT/_G793_STATE（entry __globals__）",
                "hard_currency": "胜率=硬通货；margin/realized_px 只作参考",
                "zero_modification": "对手件与本体 j23._load_entry 直跑（全新"
                                     "命名空间+末 callable）；适配仅本 harness 层",
            },
            "panel": {k: {"path": str(v), "sha": SHA.get(k)}
                      for k, v in PANEL.items()},
        },
        "panel": {}, "g793": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 认证（复用 composite lab 09-30 认证缓存；同机同二进制）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = (KSIM_DIR / "orderbook_composite_lab" / "evidence"
                  / "sim_auth_cache.json")
    auth = None
    if AUTH_CACHE.is_file():
        try:
            auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
        except Exception:
            auth = None
    if isinstance(auth, dict) and auth.get("loaded") and \
            auth.get("consistency_ok"):
        EV["source"]["sim_auth"] = {
            "reused_cache": True, "cache_path": str(AUTH_CACHE),
            "loaded": auth.get("loaded"),
            "consistency": auth.get("consistency"),
            "consistency_ok": auth.get("consistency_ok"),
            "engine": auth.get("engine"), "version": auth.get("version"),
            "wall_speedup": auth.get("wall_speedup")}
        budget["auth"] = 30
    else:
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")},
            [674000 + i * 131 for i in range(8)] + [2026100101])
        EV["source"]["sim_auth"] = {k: auth.get(k) for k in
                                    ("loaded", "consistency",
                                     "consistency_ok", "engine", "version",
                                     "wall_speedup")}
        EV["source"]["sim_auth"]["reused_cache"] = False
        budget["auth"] = 30
    if not (auth.get("loaded") and auth.get("consistency_ok")):
        EV["verdict"] = {"aborted": "sim_bridge 未过 30/30 认证",
                         "verdict": "UNRUNNABLE"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS,
               "record_path": str(EVID_DIR / "sim_bridge_degraded.json")}
    flush_evid()

    # ---- 面板：v89_full vs {H1, mpx, r40, A} ----
    panel = {}
    for on, opath in PANEL.items():
        rows = play(unit_specs("panel", on, opath, PANEL_FOLDS), run_cfg)
        budget["panel"] += len(rows)
        panel[on] = fold_stats(rows)
        panel[on]["g793"] = g793_agg(rows)
        panel[on]["wool"] = wool_agg(rows)
        print("panel v89_full vs", on, "h2h=", panel[on]["h2h"],
              "W/L/T=", panel[on]["wins"], panel[on]["losses"],
              panel[on]["ties"], "g793_bypassed=",
              panel[on]["g793"]["sum_bypassed"], flush=True)
        flush_evid()
    EV["panel"] = {
        "design": "v89_full 对 4 件面板：每对 n=%d fold 双席=%d 局（中性块 "
                  "674000+i*131）；h2h=judge_r44._fold_arm；margin=farms"
                  "[obs.player]；胜率=硬通货" % (N_FOLDS, 2 * N_FOLDS),
        "pairs": panel}

    # ---- G793 触发读数 ----
    EV["g793"] = {
        "caliber": "逐局 _G793_REPORT（calls/classified/bypassed/errors）经 "
                   "entry __globals__；触发 fold=任一席 bypassed>0 的 seed",
        "per_pair": {o: panel[o]["g793"] for o in PANEL},
        "vs_H1_trigger_split": (panel.get("H1") or {}).get("g793"),
        "finding_note": "触发后 vs H1 是否翻盘：看 vs_H1_trigger_split 的 "
                        "folds_trigger（W/L/T）对 folds_no_trigger",
    }

    # ---- 判决三档（vs 王座 H1）----
    h_h1 = (panel.get("H1") or {}).get("h2h")
    n_err = sum((panel.get(o) or {}).get("n_errors", 0) for o in PANEL)
    n_tot = sum((panel.get(o) or {}).get("n_games", 0) for o in PANEL)
    if h_h1 is None or (n_tot and n_err / n_tot > 0.2):
        verdict = "UNRUNNABLE"
    elif h_h1 >= 0.5:
        verdict = "BEATS_CEILING"
    elif h_h1 >= 0.35:
        verdict = "COMPETITIVE"
    else:
        verdict = "WEAK"
    EV["verdict"] = {
        "verdict": verdict,
        "rule": "BEATS_CEILING=vs 王座 H1 h2h≥0.5 / COMPETITIVE=0.35-0.5 / "
                "WEAK=<0.35 / UNRUNNABLE=装载失败或红局>20%",
        "vs_H1_h2h": h_h1,
        "panel_h2h": {o: (panel.get(o) or {}).get("h2h") for o in PANEL},
        "panel_WLT": {o: [panel[o]["wins"], panel[o]["losses"],
                          panel[o]["ties"]] for o in PANEL},
        "g793_trigger_counts": {o: {
            "classified": panel[o]["g793"]["sum_classified"],
            "bypassed": panel[o]["g793"]["sum_bypassed"],
            "errors": panel[o]["g793"]["sum_errors"]} for o in PANEL},
        "mean_margin_vs_H1": (panel.get("H1") or {}).get("mean_margin"),
        "realized_px_vs_H1": {
            "us": (panel.get("H1") or {}).get("realized_px_us"),
            "opp": (panel.get("H1") or {}).get("realized_px_opp")},
        "n_games": n_tot, "n_errors": n_err,
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = budget["auth"] + budget["panel"]
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货，margin/realized_px/"
                     "G793 触发率只作参考；Never quote the peak")
    ANOMALIES.append("自报≠可迁移（六连败教训）：v89_full 无自报战绩（我方合成"
                     "件）；V89 基底自述 G793 机制以本池实测触发读数为准")
    ANOMALIES.append("面板口径与 v94_arena 同构（674000+i*131、_fold_arm、干净"
                     " margin）；H1=oc_c3 行为孪生（BT 527.8 并列王座），选 H1 "
                     "为代表席")
    flush_evid()
    print("VERDICT:", verdict, "vs_H1 h2h=", h_h1, flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
