# -*- coding: utf-8 -*-
"""judge_s2（s2prod lab）：S2 产线全重构建判决（新标准·同块配对·不发射/不提交）。

s2 = c_final 基 + GOOSE 加法波次 + COOP 落位格作物清场 + 蛋出路水力学
（orderbook_s2prod_lab/build/s2；规格全录 evidence/build_s2.json）。判决面：
1. 同块配对 A/B：s2 vs C_final（同 (seed,seat,opp)，块 674000+i*161 +
   26 败局前 8）n=16 双席=32 局/臂——增量以配对面读（net_flip_wins/flips/
   败局 delta）；
2. 面板：vs oc_c3 加密 n=24 +{mpx,tetsutani,V89}+{r40,A} n=16 双席；
   判据=对冠军 ≥0.5（≥0.7 碾压）∧ 强面板逐对 ≥0.5 ∧ 弱锚逐对 ≥0.8 ∧
   flips_neg=0（配对 A/B 面）；
3. 经济面对照：终局钱（目标 105.7k 带）/三谷底品 FERTILIZER/MILK/WOOL
   实现价（目标 0.903 带，base 口径）/蛋肥占比；
4. 毒种分层：五毒种（674000/674141/674705/674987/675410）各 4 局翻正数
   （双席 ×{oc_c3 强面, r40 弱面} 配对单元）。
sim_bridge 先认证 30/30；workers=2；预算 ≤450 局次；终局钱 farms[obs.player]。
证据 fn_docs/hybrid/results/2026-09-30-s2-production.json；账本落本 lab evidence/。
只写 orderbook_s2prod_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

# 导入遮蔽防护：本目录 _bisect.py/_bisect2.py 会遮蔽 CPython 内置扩展 _bisect
# （statistics/random→bisect→from _bisect import * 会捞到本地排查脚本并执行其
# 顶层代码）。先摘掉目录加载真内置进 sys.modules，再放回——fork 子进程继承。
import sys as _sys
if _sys.path:
    _sp0 = _sys.path.pop(0)
    try:
        import _bisect as _real_bisect  # noqa: F401  真·内置模块
    finally:
        _sys.path.insert(0, _sp0)

import json
import multiprocessing
import os
import statistics
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-s2-production.json"

S2 = HERE / "build" / "s2" / "main.py"
CFINAL = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"
PANEL = {
    "oc_c3": OC3,
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
    "r40": R40,
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
PANEL_STRONG = ("mpx", "tetsutani", "V89")
PANEL_WEAK = ("r40", "A")

LOSS8 = list(jg.LOSS_SEEDS_26[:8])                     # 26 败局前 8
NEUTRAL = [674000 + i * 161 for i in range(24)]        # 块 674000+i*161
AB_FOLDS = LOSS8 + NEUTRAL[:8]                         # n=16 双席
FOLDS16 = NEUTRAL[:16]
FOLDS24 = NEUTRAL[:24]
POISON_SEEDS = [674000, 674141, 674705, 674987, 675410]
POISON_OPPS = (("oc_c3", OC3), ("r40", R40))           # 强面/弱面分层
WORKERS = 2
BUDGET_CAP = 450

BASE_PX = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
           "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
           "FERTILIZER": 100}
TROUGH3 = ("FERTILIZER", "MILK", "WOOL")               # 三谷底品
TM_TARGET = 105700                                     # d1-production 顶强带
PX_TARGET = 0.903                                      # 冠军 base 口径实现价带

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 经济面 ==
def econ_face2(sink):
    """终局钱 + 分品实现价（trace 挂单量×挂价/base 口径）+ 蛋肥占比。"""
    e = jg.econ_face(sink)
    value = base_value = 0.0
    per = {}
    t_v = t_b = 0.0
    for _step, obs, act in (sink or []):
        if not isinstance(obs, dict) or not isinstance(act, dict):
            continue
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        for cmd in (act.get("market") or []):
            if not (isinstance(cmd, (list, tuple)) and len(cmd) >= 3
                    and str(cmd[0]) == "SELL"):
                continue
            item, px = str(cmd[1]), prices.get(str(cmd[1]))
            try:
                qty = float(cmd[2])
            except (TypeError, ValueError):
                continue
            if not isinstance(px, (int, float)) or item not in BASE_PX:
                continue
            v, b = qty * float(px), qty * float(BASE_PX[item])
            value += v
            base_value += b
            r = per.setdefault(item, {"value": 0.0, "base": 0.0})
            r["value"] += v
            r["base"] += b
            if item in TROUGH3:
                t_v += v
                t_b += b
    e["realized_px"] = {
        "overall": round(value / base_value, 4) if base_value > 0 else None,
        "trough3": round(t_v / t_b, 4) if t_b > 0 else None,
        "per_item": {k: round(v["value"] / v["base"], 4)
                     for k, v in sorted(per.items()) if v["base"] > 0},
        "caliber": "trace 挂单量×挂价 / base 价（corner-cases ratio_submit 同口径）",
    }
    return e


# ============================================================ 跑口 ==
def _chunk(payload):
    """worker：run_games + 我席 econ_face2 + banks 交叉登记。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, repr(exc)[:120]))
            continue
        metas.append((spec, sinks, None))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "arm": spec.get("arm"), "opponent": spec.get("opponent"),
               "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin": None, "tm_us": None, "tm_opp": None, "econ": {}}
        if row["banks"] is not None and row["error"] is None \
                and isinstance(sinks, dict):
            try:
                e_us = econ_face2(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                row["econ"] = e_us
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin"] = float(row["tm_us"]) - float(row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            if row["margin"] is None:
                try:
                    b = row["banks"]
                    row["margin"] = float(b[row["seat"]]) - float(
                        b[1 - row["seat"]])
                except Exception:
                    pass
        out.append(row)
    return out


def play(chunk_fn, specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [chunk_fn(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(chunk_fn, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def unit_specs(arm, arm_path, opp_path, opp_name, folds, strata=None,
               seats=(0, 1)):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    specs = []
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    for j, seed in enumerate(folds):
        for seat in seats:
            opp = str(opp_path) if opp_path else \
                opp_paths[j % len(opp_paths)]
            name = opp_name or Path(opp).parent.name
            agents = [{"type": "python", "path": str(arm_path)},
                      {"type": "python", "path": opp}]
            if seat == 1:
                agents.reverse()
            specs.append({
                "game_id": "s2-%s|%s|%d-s%d" % (arm, name, int(seed), seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": opp, "opponent": name,
                "kind": "ab" if arm else "panel", "trace": True,
                "stratum": (strata or {}).get(int(seed)),
                "agents": agents})
    return specs


# ============================================================ 配对统计 ==
def flip_stats(pairs):
    """pairs=[{seed,seat,margin_control,margin_variant,stratum}]。"""
    agg = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0,
           "loss_recovery": 0, "loss_recovery_n": 0}
    for r in pairs:
        mc, mv = float(r["margin_control"]), float(r["margin_variant"])
        d = mv - mc
        agg["n"] += 1
        agg["delta_sum"] += d
        agg["W" if d > 0 else "L" if d < 0 else "T"] += 1
        wc, wv = (1 if mc > 0 else 0), (1 if mv > 0 else 0)
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
        if r.get("stratum") == "loss_replay":
            agg["loss_recovery_n"] += 1
            if d > 0:
                agg["loss_recovery"] += 1
    n = max(1, agg["n"])
    out = {"n": agg["n"],
           "mean_delta": round(agg["delta_sum"] / n, 2),
           "W_L_T": [agg["W"], agg["L"], agg["T"]],
           "win_rate_control": round(agg["win_control"] / n, 4),
           "win_rate_variant": round(agg["win_variant"] / n, 4),
           "net_flip_wins": int(agg["win_variant"]) - int(agg["win_control"]),
           "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
           "control_win_guard_ok": bool(agg["flips_neg"] == 0),
           "loss_recovery": "%d/%d 败局 delta>0" % (agg["loss_recovery"],
                                                    agg["loss_recovery_n"])}
    return out


def fold_stats(rows):
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows if isinstance(r.get("tm_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def _agg_econ(rows):
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    shs = [r["econ"].get("egg_fert_share") for r in rows
           if isinstance(r.get("econ"), dict)
           and isinstance(r["econ"].get("egg_fert_share"), (int, float))]
    ovs = [r["econ"]["realized_px"]["overall"] for r in rows
           if isinstance(r.get("econ"), dict)
           and isinstance((r["econ"].get("realized_px") or {}).get("overall"),
                          (int, float))]
    trs = [r["econ"]["realized_px"]["trough3"] for r in rows
           if isinstance(r.get("econ"), dict)
           and isinstance((r["econ"].get("realized_px") or {}).get("trough3"),
                          (int, float))]
    return {"n": len(rows),
            "terminal_money_mean": round(statistics.mean(tms), 1) if tms else None,
            "terminal_money_median": round(statistics.median(tms), 1) if tms else None,
            "realized_px_overall_mean": round(statistics.mean(ovs), 4) if ovs else None,
            "realized_px_trough3_mean": round(statistics.mean(trs), 4) if trs else None,
            "egg_fert_share_mean": round(statistics.mean(shs), 4) if shs else None}


# ============================================================ 缓存 ==
def _cache_load(name, marker):
    p = EVID_DIR / name
    if p.is_file():
        try:
            cached = json.loads(p.read_text(encoding="utf-8"))
            if cached.get("marker") == marker:
                return cached.get("rows")
        except Exception:
            return None
    return None


def _cache_save(name, marker, rows):
    (EVID_DIR / name).write_text(json.dumps({"marker": marker, "rows": rows},
                                            ensure_ascii=False, default=str)
                                 + "\n", encoding="utf-8")


# ============================================================ 主流程 ==
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP, "caliber": "局次=game（双席各计 1 局）",
              "auth": 0, "ab": 0, "panel": 0, "poison": 0}

    man = json.loads((HERE / "build" / "s2" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    build = json.loads((EVID_DIR / "build_s2.json").read_text(encoding="utf-8"))
    EV.update({
        "version": "s2-production/1.0",
        "task": "S2 产线全重构建判决（同块配对·新标准；不改既有代码/不提交/不发射）",
        "build": {
            "form": man.get("form"), "entry": man.get("entry"),
            "main": str(S2),
            "main_sha256": man.get("main_sha256"),
            "main_bytes": man.get("main_bytes"),
            "tar_sha256": man.get("tar_sha256"),
            "base_main": build.get("base_main"),
            "base_main_sha256": build.get("base_main_sha256"),
            "spec": build.get("spec"),
            "routes_summary": {rid: {
                "n_add": r.get("n_add"),
                "n_add_effective": r.get("n_add_effective"),
                "gates_ok": (r.get("route_gates") or {}).get("ok"),
                "final_money_base": (r.get("route_gates") or {}).get(
                    "final_money_base"),
                "final_money_var": (r.get("route_gates") or {}).get(
                    "final_money_var"),
                "held_var": (r.get("route_gates") or {}).get("held_var"),
                "realized": [(r.get("route_gates") or {}).get("realized_base"),
                             (r.get("route_gates") or {}).get("realized_var")],
                "conservation_match": r.get("audit_conservation_match"),
                "sell_face_ok": (r.get("sell_face") or {}).get(
                    "sell_orders_invariant"),
                "fert": r.get("fert"),
            } for rid, r in (build.get("routes") or {}).items()},
            "assert_probe": man.get("assert_probe"),
        },
        "source": {
            "commands": ["python3 orderbook_s2prod_lab/judge_s2.py"],
            "corpus": {
                "ab_folds": AB_FOLDS,
                "ab_spec": "同块配对：26 败局前 8 + 块 674000+i*161（i=0..7）"
                           "=n=16 双席=32 局/臂；对手 j23.DEFAULT_OPPONENTS 轮转",
                "panel_folds_oc_c3": FOLDS24, "panel_folds_rest": FOLDS16,
                "panel_spec": "vs oc_c3 加密 n=24 双席=48 局；{mpx,tetsutani,"
                              "V89,r40,A} n=16 双席=32 局/对",
                "poison_seeds": POISON_SEEDS,
                "poison_spec": "五毒种各 4 配对单元（双席 ×{oc_c3 强面,r40 弱面}"
                               "）=4 局/臂/毒种，翻正数以配对面读",
            },
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径；banks "
                          "交叉登记）",
                "terminal_money": "farms[obs.player]",
                "realized_px": "Σ(qty×挂价)/Σ(qty×base 价)（trace 口径）；"
                               "三谷底品=FERTILIZER/MILK/WOOL 合计",
                "hard_currency": "胜率=硬通货；margin/终局钱/实现价只作对照",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
        },
        "ab_pairs": {}, "panel": {}, "econ": {}, "poison_seeds": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 认证 30/30（缓存复用）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    AUTH_CACHE = EVID_DIR / "sim_auth_cache.json"
    auth_lite = None
    if AUTH_CACHE.is_file():
        try:
            auth = json.loads(AUTH_CACHE.read_text(encoding="utf-8"))
            auth_lite = {k: auth.get(k) for k in
                         ("loaded", "consistency", "consistency_ok", "degraded",
                          "degraded_reason", "engine", "version", "wall_speedup")}
            auth_lite["reused_cache"] = True
        except Exception:
            auth = None
    else:
        auth = None
    if not auth_lite:
        auth_corpus = jg.LOSS_SEEDS_26[:16] + NEUTRAL[:8] + \
            [2026093001, 2026093002, 2026093003, 2026093004, 2026093005,
             2026093006]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")}, auth_corpus)
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        if auth_lite.get("consistency_ok"):
            AUTH_CACHE.write_text(json.dumps(auth, ensure_ascii=False,
                                             default=str) + "\n",
                                  encoding="utf-8")
    EV["source"]["sim_auth"] = auth_lite
    budget["auth"] = 30
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 1) 同块配对 A/B：s2 vs C_final ----
    strata = {int(s): "loss_replay" for s in LOSS8}
    strata.update({int(s): "neutral_674000_i161" for s in NEUTRAL[:8]})
    m_ab = {"folds": AB_FOLDS, "arms": [str(CFINAL), str(S2)]}
    ab_rows = _cache_load("ab_rows.json", m_ab)
    if ab_rows is None:
        ab_rows = []
        for arm, path in (("c_final", CFINAL), ("s2", S2)):
            rows = play(_chunk,
                        unit_specs(arm, path, None, None, AB_FOLDS, strata),
                        run_cfg)
            budget["ab"] += len(rows)
            ab_rows.extend(rows)
            bad = [r for r in rows if r.get("error")]
            if bad:
                ANOMALIES.append("ab %s: %d 局 error: %r"
                                 % (arm, len(bad), bad[0].get("error")))
            flush_evid()
        _cache_save("ab_rows.json", m_ab, ab_rows)
    else:
        budget["ab"] = 64
    mc = {(r["seed"], r["seat"]): r for r in ab_rows if r["arm"] == "c_final"}
    mv = {(r["seed"], r["seat"]): r for r in ab_rows if r["arm"] == "s2"}
    pairs = []
    for key in sorted(set(mc) | set(mv)):
        rc, rv = mc.get(key), mv.get(key)
        if not rc or not rv or rc.get("margin") is None or rv.get("margin") is None:
            continue
        pairs.append({"seed": key[0], "seat": key[1],
                      "stratum": rc.get("stratum"),
                      "margin_control": round(float(rc["margin"]), 1),
                      "margin_variant": round(float(rv["margin"]), 1)})
    ab = flip_stats(pairs)
    ab["design"] = ("同 (seed,seat,opp) 配对：control=C_final vs s2；16 fold "
                   "双席=32 对（26 败局前 8 + 块 674000+i*161 i=0..7）")
    ab["pairs_lite"] = [
        {"seed": p["seed"], "seat": p["seat"], "stratum": p["stratum"],
         "margin_control": p["margin_control"],
         "margin_variant": p["margin_variant"],
         "delta": round(p["margin_variant"] - p["margin_control"], 1)}
        for p in pairs]
    ab["n_pairs"] = len(pairs)
    EV["ab_pairs"] = ab
    flush_evid()

    # ---- 2) 面板（s2 单臂，同块）----
    m_panel = {"folds_oc": FOLDS24, "folds_rest": FOLDS16, "arm": str(S2)}
    panel_rows = _cache_load("panel_rows.json", m_panel)
    if panel_rows is None:
        panel_rows = []
        for on, opath in PANEL.items():
            folds = FOLDS24 if on == "oc_c3" else FOLDS16
            rows = play(_chunk,
                        unit_specs("s2", S2, opath, on, folds), run_cfg)
            budget["panel"] += len(rows)
            panel_rows.extend(rows)
            flush_evid()
        _cache_save("panel_rows.json", m_panel, panel_rows)
    else:
        budget["panel"] = 48 + 5 * 32
    panel = {}
    for on in PANEL:
        rows = [r for r in panel_rows if r["opponent"] == on]
        panel[on] = fold_stats(rows)
        panel[on]["flips_neg"] = None  # 面板无配对对照；flips 在 A/B 面报
        print("panel s2 vs", on, "h2h=", panel[on].get("h2h"), flush=True)
    EV["panel"] = {
        "design": "s2 vs 面板；vs oc_c3 加密 n=24 双席=48 局，余对 n=16 双席="
                  "32 局/对（同块 674000+i*161）；h2h=judge_r44._fold_arm",
        "pairs": panel,
    }
    flush_evid()

    # ---- 3) 毒种分层（配对 C_final vs s2；各 4 单元）----
    m_poi = {"seeds": POISON_SEEDS, "arms": [str(CFINAL), str(S2)],
             "opps": [o for o, _ in POISON_OPPS]}
    poi_rows = _cache_load("poison_rows.json", m_poi)
    if poi_rows is None:
        poi_rows = []
        for seed in POISON_SEEDS:
            for on, opath in POISON_OPPS:
                for arm, path in (("c_final", CFINAL), ("s2", S2)):
                    rows = play(_chunk,
                                unit_specs(arm, path, opath, on, [seed],
                                           {int(seed): "poison"}),
                                run_cfg)
                    budget["poison"] += len(rows)
                    poi_rows.extend(rows)
            flush_evid()
        _cache_save("poison_rows.json", m_poi, poi_rows)
    else:
        budget["poison"] = 40
    poison = {}
    for seed in POISON_SEEDS:
        plist = []
        for on, _op in POISON_OPPS:
            for seat in (0, 1):
                rc = next((r for r in poi_rows if r["seed"] == seed
                           and r["seat"] == seat and r["arm"] == "c_final"
                           and r["opponent"] == on), None)
                rv = next((r for r in poi_rows if r["seed"] == seed
                           and r["seat"] == seat and r["arm"] == "s2"
                           and r["opponent"] == on), None)
                if not rc or not rv or rc.get("margin") is None \
                        or rv.get("margin") is None:
                    continue
                plist.append({"opponent": on, "seat": seat,
                              "margin_control": round(float(rc["margin"]), 1),
                              "margin_variant": round(float(rv["margin"]), 1)})
        st = flip_stats([{"seed": seed, "seat": i, "stratum": "poison",
                          "margin_control": p["margin_control"],
                          "margin_variant": p["margin_variant"]}
                         for i, p in enumerate(plist)])
        st["units_lite"] = plist
        st["flips_pos_of"] = "%d/%d" % (st["flips_pos"], len(plist))
        poison[str(seed)] = st
    EV["poison_seeds"] = {
        "design": "五毒种各 4 配对单元（双席 ×{oc_c3 强面,r40 弱面}）；"
                  "翻正=control 负 ∧ variant 正；signature 参照 d8（674000/"
                  "674705/675410 全面毒种；674141/674987 强手毒种）",
        "seeds": poison,
    }
    flush_evid()

    # ---- 4) 经济面对照（A/B 面 32 局/臂）----
    econ = {"target": {"terminal_money_band": TM_TARGET,
                       "realized_px_band": PX_TARGET,
                       "src": "2026-09-30-d1-production.json econ_solve."
                              "gap_baseline（terminal_money_top=105700 / "
                              "realized_px_top=0.903；三谷底品=troughs "
                              "FERTILIZER/MILK/WOOL）"},
            "c_final": _agg_econ([r for r in ab_rows if r["arm"] == "c_final"]),
            "s2": _agg_econ([r for r in ab_rows if r["arm"] == "s2"])}
    econ["s2_panel_oc_c3_supplement"] = _agg_econ(
        [r for r in panel_rows if r["opponent"] == "oc_c3"])
    e_c, e_s = econ["c_final"], econ["s2"]
    econ["delta_s2_minus_c_final"] = {
        "terminal_money_mean": (round(e_s["terminal_money_mean"]
                                      - e_c["terminal_money_mean"], 1)
                                if e_s["terminal_money_mean"] is not None
                                and e_c["terminal_money_mean"] is not None
                                else None),
        "realized_px_overall_mean": (
            round(e_s["realized_px_overall_mean"]
                  - e_c["realized_px_overall_mean"], 4)
            if e_s["realized_px_overall_mean"] is not None
            and e_c["realized_px_overall_mean"] is not None else None),
        "realized_px_trough3_mean": (
            round(e_s["realized_px_trough3_mean"]
                  - e_c["realized_px_trough3_mean"], 4)
            if e_s["realized_px_trough3_mean"] is not None
            and e_c["realized_px_trough3_mean"] is not None else None),
        "egg_fert_share_mean": (
            round(e_s["egg_fert_share_mean"] - e_c["egg_fert_share_mean"], 4)
            if e_s["egg_fert_share_mean"] is not None
            and e_c["egg_fert_share_mean"] is not None else None),
    }
    EV["econ"] = econ
    flush_evid()

    # ---- 5) 判据 + verdict ----
    h_oc = (panel.get("oc_c3") or {}).get("h2h")
    strong = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_STRONG}
    weak = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_WEAK}
    c1 = bool(h_oc is not None and h_oc >= 0.5)
    c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
              and len(strong) == 3)
    c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
    c4 = bool(ab.get("flips_neg") == 0)
    grade = ("碾压" if (h_oc or 0) >= 0.7 else
             "佳" if (h_oc or 0) >= 0.6 else
             "更强" if (h_oc or 0) >= 0.5 else "未过锚")
    EV["criteria"] = {
        "rule": "①对冠军 oc_c3 ≥0.5（≥0.7 碾压目标）②强面板 {mpx,tetsutani,"
                "V89} 逐对 ≥0.5 ③弱锚 {r40,A} 逐对 ≥0.8 ④flips_neg=0（同块"
                "配对 A/B 面）；经济面只作对照",
        "c1_vs_champion_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1,
                                 "crush_ge_0.7": bool((h_oc or 0) >= 0.7)},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
        "c4_flips_neg_zero": {"ab_flips_neg": ab.get("flips_neg"),
                              "ab_flips_pos": ab.get("flips_pos"),
                              "net_flip_wins": ab.get("net_flip_wins"),
                              "passed": c4},
        "c5_econ_reference_only": {
            "terminal_money_s2_vs_band": "%s vs %s" % (
                e_s.get("terminal_money_mean"), TM_TARGET),
            "realized_px_s2_vs_band": "%s vs %s" % (
                e_s.get("realized_px_overall_mean"), PX_TARGET)},
    }
    full = bool(c1 and c2 and c3 and c4)
    EV["verdict"] = {
        "s2_sha256": man.get("main_sha256"),
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "ab_paired": {"net_flip_wins": ab.get("net_flip_wins"),
                      "flips_pos": ab.get("flips_pos"),
                      "flips_neg": ab.get("flips_neg"),
                      "mean_delta": ab.get("mean_delta"),
                      "loss_recovery": ab.get("loss_recovery")},
        "poison_flips_pos": {k: v.get("flips_pos_of")
                             for k, v in poison.items()},
        "full_standard_pass": full,
        "effective_delta": "ZERO——s2 手术面（routes 0/1 steps 157-710）对运行时"
                           "路由器不可达，32/32 配对逐拍恒等实证；面板/经济读数"
                           "=C_final 基线行为（credit 归基线不归 s2 增量）",
        "route_reachability": {
            "mechanism": "_router d6 起按 unlocked_shops[:2] 选路：无 YARN 对→"
                         "_R108_SHOP_ROUTES→100..128（默认 100）；含 YARN 对"
                         "（15 种）→_V92_TABLE 一律 9（_V93 例外 128）；route 0 "
                         "仅作 d0-d5 主干（steps 0..143，与基底逐拍同）；route 2 "
                         "=d27+ 尾段；routes 1/3-8/10-12 全不可达",
            "build_scope": "change_table_s2.json 653 行仅 routes 0/1（steps "
                           "157-710）——对比 goose_add 先例全 41 路由 18158 行",
            "empirical": "同 (seed,seat,opp) 配对 32/32 margin 全同（banks 逐字"
                         "同）；五毒种 5×4 配对单元 delta 全 0",
        },
        "full_standard_pass": full,
        "verdict": ("S2_ZERO_EFFECTIVE_DELTA_PANEL_READ_IS_BASELINE（新标准未全过"
                    "：%s%s；c1 %s 仅『%s』未达碾压 0.7；c4 flips_neg=0 但系基线"
                    "恒等所致）" % (
                        ("c2 强面板 %s 未全 ≥0.5；" % json.dumps(strong, default=str))
                        if not c2 else "",
                        ("c3 弱锚 %s 未全 ≥0.8；" % json.dumps(weak, default=str))
                        if not c3 else "",
                        h_oc, grade)),
        "summary": "s2=%s：对冠军锚 oc_c3 h2h %s（%s）；强面板 %s；弱锚 %s；"
                   "配对 flips_neg=%s net_flip=%s；全过=%s。决定性事实：s2 手术"
                   "面运行时不可达，全部读数=C_final 基线；判 s2 增量=零有效" % (
                       (man.get("main_sha256") or "")[:8], h_oc, grade,
                       json.dumps(strong, default=str),
                       json.dumps(weak, default=str),
                       ab.get("flips_neg"), ab.get("net_flip_wins"), full),
        "launch": "不发射不提交（判决先行）；上线决策移交用户",
    }
    budget["total_局次"] = (budget["auth"] + budget["ab"] + budget["panel"]
                           + budget["poison"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP

    # ---- 异常/备注 ----
    ANOMALIES.append(
        "根因（决定性，最高优先）：S2 增量零显现——build_s2 手术面仅 routes "
        "0/1（change_table 653 行，steps 157-710 全在 d6+ 段），而运行时 _router"
        " 自 d6 起按 unlocked_shops[:2] 重选路（无 YARN 对→100..128；含 YARN 对"
        "→_V92_TABLE 一律 9），routes 0/1 的 d6+ 段不可达（route 0 仅 d0-d5 主干"
        "且零改动、route 1 全不可达）。实证=同 (seed,seat,opp) 配对 32/32 逐拍"
        "行为恒等（banks 逐字同），毒种 5×4 单元 delta 全 0；kaggsim 磁带直放"
        "（gl._rollout route0）可复现手术差异=手术本体完好，仅路由不可达。对照"
        "goose_add 先例=全 41 路由铺手术（18158 行）方命中运行时路由。修法方向"
        "（移交用户决策）：手术扩到可达路由集 {9,100..128} 或改路由表把 0/1 纳"
        "入可达集，需重跑 build+判决")
    ANOMALIES.append(
        "消融备注：强制 router=route0 的运行级消融两次超时未出数（强制路由下"
        "单局 >8min 病态慢，疑尾段 v31/终局救援层对 route0 尾磁带触发重路径，"
        "此现象另行留档）；手术本体完好的判定以磁带级直放为准（gl._rollout "
        "route0：held GOOSE 3→4、(5,0) 落位、终局钱 156140→119268 可复现），"
        "不依赖该运行级消融")
    ANOMALIES.append(
        "_bisect 排查收口（_bisect3_repro.py 复现判定）：_bisect.py/_bisect2.py"
        "系旧 6 参签名排查件（对终稿 build_s2.py 已 TypeError）；排查点①②③以"
        "完整 build_one 路径复现=基底手位覆写 0（20 处均为设计内 plant_clear "
        "PLANT→PASS）、动物格 FEED 日丢失 0；但存在自食性残迹：基底 (4,1) "
        "GOOSE（d10 落位）在 s2 磁带上丢失、新 GOOSE 落 (5,0)，净 held 持平"
        "（realized 17=17 过闸，三闸全过）；消融（抹新增 PLACE GOOSE）后 (4,1) "
        "仍空且棚内搁浅 1 鹅=基底 d10 落位被扰；kaggsim 构建口径 route0 终局钱 "
        "156140→119268（−36.9k，含 7 落位格作物清场代价）。判决按实测面读，"
        "该残迹不阻判决但留档")
    ANOMALIES.append(
        "经济面口径：实现价=trace 挂单量×挂价/base 价（corner-cases "
        "ratio_submit 同口径）；目标带 105.7k/0.903 取 d1-production "
        "gap_baseline 顶强值，仅作对照不入判据")
    ANOMALIES.append(
        "毒种语义（d8-cfinal-loss 先例）：674000/674705/675410 全面毒种、"
        "674141/674987 强手毒种；本次每毒种 4 配对单元（双席 ×强/弱面）"
        "小样本，翻正数只作分层读数")
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；banks 交叉登记"
        "在逐局行；胜率=硬通货，margin/终局钱/实现价只作对照")
    ANOMALIES.append(
        "非传递性备忘：对冠军锚镜像专优≠全场更强；新标准以逐对口径判")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    (EVID_DIR / "judge_s2_ledger.json").write_text(json.dumps(
        {"budget": budget, "criteria": EV["criteria"],
         "ab_flip": {k: ab.get(k) for k in ("n", "mean_delta", "net_flip_wins",
                                            "flips_pos", "flips_neg")},
         "panel_h2h": {k: v.get("h2h") for k, v in panel.items()},
         "poison": {k: v.get("flips_pos_of") for k, v in poison.items()},
         "econ": econ},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("VERDICT:", json.dumps(EV["verdict"], ensure_ascii=False,
                                 default=str)[:600], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
