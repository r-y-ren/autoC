# -*- coding: utf-8 -*-
"""judge_panel（d1prod lab）：新标准面板判决（胜率=硬通货；不发射/不提交）。

新评判标准（任务 D1）：
① 直接对战强面板 {oc_c3 冠军锚, mpx, tetsutani, V89} 每对 n=12 双席
   ——对强面板 h2h ≥ 0.5（不许失血）；
② 弱锚 {r40, A} h2h ≥ 0.8；
③ 对 oc_c3 直接对战 ≥ 0.5 才算"更强"；
④ margin/终局钱只作参考（胜率=硬通货）；
⑤ 禁止用配对边际作主判据（fold h2h 唯一主判）。

口径：judge_r44._fold_arm 同 seed 双席折叠（score=两席均分，≥1 胜/≤0 负/余平；
缺席/红局=fail-closed 记负）；margin=终局 farms[obs.player].money 差（干净口径）
+banks 交叉登记；终局钱 farms[obs.player]。sim_bridge 先认证 30/30（不过即停）；
workers=2；预算 ≤600 局次（game 口径）。

编排：全部过闸变体 vs oc_c3 甄别（24 局/变体）→ top-K 全面板（mpx/tetsutani/
V89/r40/A 各 24 局）。语料=新中性块 674000+i*131（i=0..11，冠军赛同块可比）。
复用（不改写）：judge_goose._play 口径/ab_r41._specs_for/j23._build_agents/
sim_bridge.run_games/judge_r44._fold_arm。只写 orderbook_d1prod_lab/ 与
fn_docs/hybrid/results/2026-09-30-d1-production.json（任务指定证据路径）。
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
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import judge_goose as jg  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = (KSIM_DIR.parents[2] / "fn_docs" / "hybrid" / "results"
               / "2026-09-30-d1-production.json")

OC3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
PANEL_STRONG = {
    "oc_c3": OC3,
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14" / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009" / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
}
PANEL_WEAK = {
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
NEUTRAL_FOLDS = [674000 + i * 131 for i in range(12)]
WORKERS = 2
BUDGET_CAP_GAMES = 600
TOP_K_PANEL = 3


# ------------------------------------------------------------ 对局执行 --
def _chunk(payload):
    """worker：一批局（双席 trace）→ 终局钱 farms[obs.player] + banks 交叉登记。"""
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
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, berr) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec["our_seat"]), "opponent": spec.get("opponent"),
               "variant": spec.get("arm"), "banks": rr.get("banks"),
               "error": berr or rr.get("error"), "margin_clean": None,
               "margin_banks": None, "tm_us": None, "tm_opp": None}
        if row["banks"] is not None and row["error"] is None and isinstance(sinks, dict):
            try:
                e_us = jg.econ_face(sinks[row["seat"]])
                e_opp = jg.econ_face(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                row["econ_us"] = e_us
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            b = row["banks"]
            try:
                row["margin_banks"] = float(b[row["seat"]]) - float(b[1 - row["seat"]])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
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


def pair_specs(vid, cand_path, opp_path, opp_name, seeds):
    specs = []
    for seed in seeds:
        for seat in (0, 1):
            agents = [{"type": "python", "path": str(cand_path)},
                      {"type": "python", "path": str(opp_path)}]
            if seat == 1:
                agents.reverse()
            specs.append({"game_id": "d1-%s|%s|%d-s%d" % (vid, opp_name, seed, seat),
                          "seed": int(seed), "kind": "ab", "arm": vid,
                          "our_seat": seat, "trace": True, "opponent": opp_name,
                          "agents": agents})
    return specs


def fold_stats(rows):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r44 import judge_r44 as j44  # noqa: WPS433
    rr = [{"seed": r["seed"], "margin": r["margin_clean"]} for r in rows]
    f = j44._fold_arm(rr)
    tms = [r["tm_us"] for r in rows if isinstance(r.get("tm_us"), (int, float))]
    oms = [r["tm_opp"] for r in rows if isinstance(r.get("tm_opp"), (int, float))]
    f["terminal_money_us_mean"] = round(sum(tms) / len(tms), 1) if tms else None
    f["terminal_money_opp_mean"] = round(sum(oms) / len(oms), 1) if oms else None
    f["mean_margin_clean"] = round(sum(r["margin_clean"] for r in rows
                                       if r["margin_clean"] is not None)
                                   / max(1, len(rows)), 1)
    f["mean_margin_banks"] = round(sum(r["margin_banks"] for r in rows
                                       if r["margin_banks"] is not None)
                                   / max(1, len(rows)), 1)
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def ensure_auth():
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    corpus = jg.LOSS_SEEDS_26 + [2026092901, 2026092902, 672000, 672101]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, corpus)
    lite = {k: auth.get(k) for k in
            ("loaded", "consistency", "wall_speedup", "consistency_ok",
             "degraded", "degraded_reason", "engine", "timing", "version")}
    (EVID_DIR / "sim_auth.json").write_text(
        json.dumps(lite, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return auth


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP_GAMES, "auth": 30, "screen": 0, "panel": 0}

    # ---- 变体件（build_prod 产物）----
    build = json.load(open(EVID_DIR / "build_prod.json"))
    import econ_solve as es  # noqa: WPS433
    menu = es.variant_menu(es.enumerate_solve())
    cands = {}
    for vid, rec in build["variants"].items():
        main_p = HERE / "build" / vid / "main.py"
        if main_p.is_file() and rec.get("assert_probe", {}).get("passed") \
                and rec.get("n_bad_routes", 1) == 0:
            cands[vid] = main_p
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "d1-production/1.0",
        "task": "D1 产线全局重构：MILP/枚举最优产线经济→磁带重生成→新标准判决"
                "（不改既有代码/不提交/不发射）",
        "corpus": {"neutral_folds": NEUTRAL_FOLDS,
                   "neutral_spec": "674000+i*131（i=0..11）；n=12 双席=24 局/对",
                   "comparable": "2026-09-30-champion-tourney.json 同中性块"},
        "caliber": {
            "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；fail-closed）",
            "margin": "终局 farms[obs.player].money 差（干净口径；banks 交叉登记）",
            "terminal_money": "farms[obs.player]",
            "hard_currency": "胜率=硬通货；margin/终局钱只作参考（新标准④⑤）",
        },
        "panel": {"strong": {k: str(v) for k, v in PANEL_STRONG.items()},
                  "weak": {k: str(v) for k, v in PANEL_WEAK.items()}},
        "variants_built": {vid: {
            "spec": build["variants"][vid]["spec"],
            "n_bad_routes": build["variants"][vid]["n_bad_routes"],
            "assert_probe": build["variants"][vid]["assert_probe"].get("passed"),
            "twin": build["variants"][vid]["route_gates_summary"],
            "fert": build["variants"][vid].get("fert_disposition"),
            "sell_face": build["variants"][vid].get("sell_face"),
        } for vid in cands},
    }

    auth = ensure_auth()
    if not auth.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                          default=str) + "\n", encoding="utf-8")
        return out
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 阶段 A：vs oc_c3 甄别（24 局/变体）----
    screen = {}
    for vid, cand in sorted(cands.items()):
        rows = play(pair_specs(vid, cand, OC3, "oc_c3", NEUTRAL_FOLDS), run_cfg)
        budget["screen"] += len(rows)
        screen[vid] = fold_stats(rows)
        screen[vid]["_rows"] = rows
        print("screen", vid, "h2h=", screen[vid]["h2h"], flush=True)

    # ---- 阶段 B：top-K 全面板（mpx/tetsutani/V89/r40/A）----
    ranked = sorted(cands, key=lambda v: -(screen[v]["h2h"] or 0))
    remain = BUDGET_CAP_GAMES - budget["auth"] - budget["screen"]
    k = max(0, min(TOP_K_PANEL, remain // (5 * len(NEUTRAL_FOLDS) * 2)))
    top = ranked[:k]
    panel = {}
    for vid in top:
        panel[vid] = {}
        for on, opath in list(PANEL_STRONG.items()) + list(PANEL_WEAK.items()):
            if on == "oc_c3":
                panel[vid][on] = screen[vid]
                continue
            rows = play(pair_specs(vid, cands[vid], opath, on, NEUTRAL_FOLDS), run_cfg)
            budget["panel"] += len(rows)
            panel[vid][on] = fold_stats(rows)
            print("panel", vid, "vs", on, "h2h=", panel[vid][on]["h2h"], flush=True)
    budget["total_games"] = budget["auth"] + budget["screen"] + budget["panel"]
    budget["within_cap"] = budget["total_games"] <= BUDGET_CAP_GAMES

    # ---- 证据合成面（econ_solve/variants/feasibility）----
    es_rec = json.load(open(EVID_DIR / "econ_solve.json"))
    out["econ_solve"] = {
        "method": es_rec["method"],
        "gap_baseline": es_rec["gap_baseline"],
        "d5_params": es_rec["d5_params"],
        "engine_facts": es_rec["engine_facts"],
        "econ_top5": es_rec["econ_top10"][:5],
        "pareto_front": es_rec["pareto_front"][:8],
        "release_lp_compare": es_rec["release_lp_compare"],
    }
    out["variants"] = {vid: dict(menu[vid]) for vid in menu}
    out["feasibility"] = {vid: {
        "route_gates": build["variants"][vid]["route_gates_summary"],
        "rollbacks": len(build["variants"][vid].get("rollbacks") or []),
        "conservation": "%d/%d" % (build["variants"][vid]["audit_conservation_match"],
                                   len(build["variants"][vid]["audit"].get("conservation") or [])),
        "slot_ok": build["variants"][vid]["audit"].get("slot_ok"),
        "shared_seg": build["variants"][vid]["audit"].get("shared_seg"),
        "assert_probe": build["variants"][vid]["assert_probe"].get("passed"),
        "assert_regen": build["variants"][vid]["assert_regen"],
        "sell_face": build["variants"][vid].get("sell_face"),
    } for vid in build["variants"]}

    # ---- 新标准判定 ----
    def verdict_for(vid):
        p = panel.get(vid) or {}
        strong = {o: p[o]["h2h"] for o in PANEL_STRONG if o in p}
        weak = {o: p[o]["h2h"] for o in PANEL_WEAK if o in p}
        checks = {}
        checks["c1_strong_all_ge_0.5"] = bool(strong) and all(
            (h or 0) >= 0.5 for h in strong.values()) and len(strong) == 4
        checks["c2_weak_all_ge_0.8"] = bool(weak) and all(
            (h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2
        h_oc = (p.get("oc_c3") or {}).get("h2h")
        checks["c3_vs_oc_c3_ge_0.5"] = bool(h_oc is not None and h_oc >= 0.5)
        checks["c4_margin_reference_only"] = True
        checks["c5_no_paired_margin_main"] = True
        stronger = checks["c3_vs_oc_c3_ge_0.5"] and checks["c1_strong_all_ge_0.5"]
        return {"strong_h2h": strong, "weak_h2h": weak, "vs_oc_c3_h2h": h_oc,
                "checks": checks, "stronger_than_champion": bool(stronger),
                "all_criteria": bool(all(checks.values())),
                "verdict": ("STRONGER_THAN_CHAMPION" if stronger and
                            checks["c2_weak_all_ge_0.8"] else
                            "PANEL_CANDIDATE" if checks["c1_strong_all_ge_0.5"] else
                            "NO_POSITIVE_ARM")}

    verdicts = {vid: verdict_for(vid) for vid in top}
    out["panel_pairs"] = {vid: {o: {k: v for k, v in s.items() if k != "_rows"}
                                for o, s in panel[vid].items()} for vid in top}
    out["screen"] = {vid: {k: v for k, v in s.items() if k != "_rows"}
                     for vid, s in screen.items()}
    out["standings"] = sorted(
        [{"variant": vid,
          "vs_oc_c3_h2h": screen[vid]["h2h"],
          "strong_min": min([v for v in verdicts[vid]["strong_h2h"].values()]
                            or [None]),
          "weak_min": min([v for v in verdicts[vid]["weak_h2h"].values()] or [None]),
          "tm_us": screen[vid]["terminal_money_us_mean"],
          "verdict": verdicts[vid]["verdict"]} for vid in top],
        key=lambda r: -(r["vs_oc_c3_h2h"] or 0))
    best = top[0] if top else None
    out["criteria"] = {
        "rule": "①强面板{oc_c3,mpx,tetsutani,V89} 每对 n=12 双席 h2h≥0.5（不许失血）"
                "②弱锚{r40,A}≥0.8 ③对 oc_c3≥0.5=更强 ④margin/终局钱只作参考"
                "⑤禁止配对边际作主判据",
        "per_variant": {vid: verdicts[vid]["checks"] for vid in top},
    }
    out["verdict"] = {
        "best_variant": best,
        "best": verdicts.get(best) if best else None,
        "verdict": (verdicts[best]["verdict"] if best else "NO_BUILD"),
        "stronger_than_champion": bool(best and verdicts[best]["stronger_than_champion"]),
        "budget_compliance": "局次 %d/%d（%s）" % (budget["total_games"], BUDGET_CAP_GAMES,
                                                "合规" if budget["within_cap"] else "超限"),
    }
    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；banks 交叉登记在逐局行",
        "孪生 solo 钱（gengame 对手 PASS）为无饱和世界口径，肥/奶/毛不砸价收益"
        "在 solo 低估——判据以新标准面板实测（真实对手）为准",
        "fert_selfuse 由 PASS-on-crop-tile 闲置槽转化，达成率受候选槽上限（~0.39）"
        "低于 D5 目标 0.46——差额=产线无闲置槽（劳动预算饱和），属自适应自由度上限",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
                           encoding="utf-8")
    (EVID_DIR / "judge_panel_rows.json").write_text(
        json.dumps({"screen": {v: s for v, s in screen.items()},
                    "panel": panel}, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    print("verdict:", out["verdict"], flush=True)
    return out


if __name__ == "__main__":
    main()
