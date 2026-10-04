# -*- coding: utf-8 -*-
"""judge_s3buy5（s3buy5 lab）：BUY5 开局复刻+洗价层+中盘自适应 终验（判决先行）。

终验面（新标准；n=16 双席/对，vs oc_c3 加密 n=24；块 674000+i*147 新块）：
 ①vs 冠军锚 oc_c3 ≥0.5（≥0.7 碾压目标）②强面板 {mpx,tetsutani,V89} 逐对 ≥0.5
 ③弱锚 {r40,A} ≥0.8 ④flips_neg=0 ⑤附开局对照表（逐拍动作 vs D5/D6/洗价形吻合率）。
附：行为方差对照（同对手重复局 SHEEP/GOOSE 构成摆动 vs D6 蓝图 SHEEP CV
0.56-0.94 / GOOSE 刚性）+ 三臂消融（c_final / s3_open / s3_buy5，配对 flips）。
sim_bridge 先认证 30/30；workers=2；预算 ≤500 局次；胜率=硬通货。
证据 fn_docs/hybrid/results/2026-09-30-s3-buy5.json；账本落本 lab evidence/。
只写 orderbook_s3buy5_lab/ 与上述证据路径。不改既有代码；不提交；不发射。
"""
from __future__ import annotations

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
RESULT_PATH = REPO / "fn_docs" / "hybrid" / "results" / "2026-09-30-s3-buy5.json"

CFINAL = KSIM_DIR / "orderbook_composite_lab" / "build" / "c_final" / "main.py"
S3_FULL = HERE / "build" / "s3_buy5" / "main.py"
S3_OPEN = HERE / "build" / "s3_open" / "main.py"
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py",
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "V89": KSIM_DIR / "orderbook_v89_lab" / "build" / "v89_pure" / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
PANEL_STRONG = ("mpx", "tetsutani", "V89")
PANEL_WEAK = ("r40", "A")
FOLDS16 = [674000 + i * 147 for i in range(16)]
FOLDS24 = [674000 + i * 147 for i in range(24)]
ABL_FOLDS = FOLDS16[:8]
ABL_OPPS = ("oc_c3", "tetsutani")
S3_WASH = HERE / "build" / "s3_wash" / "main.py"
S3_ADAPT0 = HERE / "build" / "s3_adapt0" / "main.py"
ABL_ARMS = (("c_final", CFINAL), ("s3_open", S3_OPEN),
            ("s3_buy5", S3_FULL), ("s3_adapt0", S3_ADAPT0),
            ("s3_wash", S3_WASH))
WORKERS = 2
BUDGET_CAP = 500

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")


# ============================================================ 抽取 ==
S3_T0 = [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", 5],
         ["BUY_PRODUCT", "WHEAT", 4], ["SELL", "WHEAT", 3],
         ["BUY_SEED", "WHEAT", 1]]
S3_T1 = [["SELL", "WHEAT", 1], ["HIRE"], ["HIRE"], ["HIRE"], ["HIRE"],
         ["HIRE"], ["BUY_ANIMAL", "COW", 1], ["BUY_ANIMAL", "SHEEP", 2]]
SPEC_T4 = []  # turn3-4 冻结基准（首局捕获后逐局比对）


def _extract(sink):
    """我席逐拍流→开局/畜群摘要（lite；不回传原始 obs）。"""
    turns = {}
    frozen = []
    buys = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    places = {"COW": 0, "SHEEP": 0, "GOOSE": 0}
    for row in (sink or []):
        step, obs, act = row[0], row[1], row[2]
        if not isinstance(act, dict):
            continue
        step = int(step)
        if step in (0, 1):
            turns[str(step)] = [list(o) for o in (act.get("market") or [])]
        if step <= 3:
            frozen.append(json.dumps(act, sort_keys=True, default=str))
        for o in (act.get("market") or []):
            if isinstance(o, (list, tuple)) and o and o[0] == "BUY_ANIMAL" \
                    and len(o) > 1 and o[1] in buys:
                buys[o[1]] += int(o[2]) if len(o) > 2 else 1
        for u in [act.get("farmer")] + list(act.get("hands") or []):
            if isinstance(u, list) and len(u) > 1 and u[0] == "PLACE" \
                    and u[1] in places:
                places[u[1]] += 1
    return {"turns": turns, "frozen_sig": "|".join(frozen),
            "buys": buys, "places": places}


def _chunk_s3(payload):
    """面板/消融 worker：trace 我席逐拍 + telemetry + 终局钱 + banks。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows = []
    games, metas = [], []
    for spec in payload["specs"]:
        try:
            inner = j23._load_entry(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            sinks = {0: [], 1: []}
            a_us = j23._Tracer(inner, int(spec["our_seat"]),
                               sinks[int(spec["our_seat"])])
            a_opp = j23._Tracer(opp, 1 - int(spec["our_seat"]),
                                sinks[1 - int(spec["our_seat"])])
            agents = [a_us, a_opp] if spec["our_seat"] == 0 else [a_opp, a_us]
            games.append({"seed": int(spec["seed"]), "agents": agents})
            metas.append((spec, inner, sinks, None))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, None, repr(exc)[:120]))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rrs = list(res.get("games") or [])
    for i, (spec, inner, sinks, berr) in enumerate(metas):
        rr = rrs[i] if i < len(rrs) else {}
        seat = int(spec["our_seat"])
        row = {"seed": int(spec["seed"]), "seat": seat,
               "opponent": spec.get("opponent"), "arm": spec.get("arm"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "margin_banks": None,
               "tm_us": None, "tm_opp": None}
        if sinks is not None and row["error"] is None:
            try:
                e_us = jg.econ_face(sinks[seat])
                e_opp = jg.econ_face(sinks[1 - seat])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
            row["opening"] = _extract(sinks[seat])
            try:
                row["telemetry"] = dict(getattr(inner, "telemetry", {}) or {})
            except Exception:
                row["telemetry"] = {}
        b = row["banks"]
        if b is not None and row["error"] is None:
            try:
                row["margin_banks"] = float(b[seat]) - float(b[1 - seat])
            except Exception:
                pass
            if row["margin_clean"] is None:
                row["margin_clean"] = row["margin_banks"]
        rows.append(row)
    return rows


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


def unit_specs(arm, arm_path, opp_path, opp_name, folds, tag):
    specs = []
    for seed in folds:
        for seat in (0, 1):
            specs.append({
                "game_id": "%s-%s|%s|%d-s%d" % (tag, arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "trace": True})
    return specs


def fold_stats(rows):
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
    f["n_games"] = len(rows)
    f["n_errors"] = sum(1 for r in rows if r.get("error"))
    return f


def flip_stats(pairs):
    """配对 flips（胜负口径）：control/variant=两臂 margin。"""
    agg = {"n": 0, "W": 0, "L": 0, "T": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0,
           "flips_pos": 0, "flips_neg": 0}
    for mc, mv in pairs:
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
    n = max(1, agg["n"])
    agg["mean_delta"] = round(agg["delta_sum"] / n, 2)
    agg["net_flip_wins"] = agg["win_variant"] - agg["win_control"]
    return agg


def _cv(xs):
    xs = [float(x) for x in xs]
    if not xs:
        return None
    m = statistics.mean(xs)
    return round(statistics.pstdev(xs) / m, 4) if m else None


def opening_table(rows):
    """逐拍动作 vs 开局指纹吻合率（执行流口径）。"""
    n = len(rows)
    m1 = m2 = frozen = 0
    bad = []
    for r in rows:
        op = r.get("opening") or {}
        t1 = [list(o) for o in (op.get("turns") or {}).get("0", [])]
        t2 = [list(o) for o in (op.get("turns") or {}).get("1", [])]
        ok1, ok2 = t1 == S3_T0, t2 == S3_T1
        m1 += int(ok1)
        m2 += int(ok2)
        sig = op.get("frozen_sig") or ""
        frozen += int(sig == (SPEC_T4[0] if SPEC_T4 else sig))
        if SPEC_T4 and sig != SPEC_T4[0] and len(bad) < 3:
            bad.append({"seed": r["seed"], "seat": r["seat"]})
        if not SPEC_T4 and sig:
            SPEC_T4.append(sig)
    return {
        "design": "执行流逐拍动作 vs 开局指纹（每局 turn1/turn2 市场单 + "
                  "turn1-4 冻结签名）",
        "n_games": n,
        "turn1_match": "%d/%d" % (m1, n),
        "turn2_match": "%d/%d" % (m2, n),
        "turn1_4_frozen": "%d/%d" % (frozen, n),
        "mismatch_samples": bad,
    }


def herd_variance(rows, label):
    """同对手重复局畜群构成摆动（行为方差对照；D6 蓝图 SHEEP CV 0.56-0.94）。"""
    sp, sc, gp, gc, tb, cb = [], [], [], [], [], []
    tiers = {}
    for r in rows:
        op = r.get("opening") or {}
        pl = op.get("places") or {}
        bu = op.get("buys") or {}
        sc.append(pl.get("SHEEP", 0))
        gp.append(pl.get("GOOSE", 0))
        sp.append(bu.get("SHEEP", 0))
        tb.append(r.get("telemetry", {}).get("tier"))
        cb.append(r.get("telemetry", {}).get("cells"))
        t = r.get("telemetry", {}).get("tier")
        tiers[str(t)] = tiers.get(str(t), 0) + 1
    return {
        "label": label, "n_games": len(rows),
        "sheep_placed": {"min": min(sc) if sc else None,
                         "max": max(sc) if sc else None,
                         "mean": round(statistics.mean(sc), 2) if sc else None,
                         "cv": _cv(sc)},
        "sheep_bought_cv": _cv(sp),
        "goose_placed": {"min": min(gp) if gp else None,
                         "max": max(gp) if gp else None,
                         "cv": _cv(gp)},
        "tier_distribution": tiers,
        "cells_mean": round(statistics.mean([c for c in cb
                                             if isinstance(c, int)]), 1)
        if any(isinstance(c, int) for c in cb) else None,
    }


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP, "auth": 0, "ablation": 0, "panel": 0}

    build = json.load(open(HERE / "build" / "s3_buy5" / "build_manifest.json"))
    probe = json.load(open(EVID_DIR / "probe_s3buy5.json"))
    EV.update({
        "version": "s3-buy5/1.0",
        "task": "BUY5 开局复刻+洗价层+中盘畜群自适应（SHEEP 弹性面）到 C_final 基，"
                "冲碾压（不改既有代码/不提交/不发射）",
        "replic": {
            "formula": "S3 = C_final(a37c0d34… 全层保留) + BUY5 开局替换"
                       "（D6 verbatim 族起手 + mooman 洗价形 13/30/30）"
                       "+ 中盘畜群自适应（SHEEP 数弹性档 ±1）",
            "s3_buy5_main": str(S3_FULL),
            "s3_buy5_sha256": build["main_sha256"],
            "s3_open_main": str(S3_OPEN),
            "base_main_sha256": build["base_main_sha256"],
            "entry": build["entry"],
            "opening": build["opening"],
            "adaptive": {k: v for k, v in build["adaptive"].items()
                         if k != "chain_counts"},
            "adaptive_chain_counts": build["adaptive"]["chain_counts"],
            "diff_audit": build["diff_audit"],
            "probes": [{"probe": p["probe"], "verdict": p["verdict"]}
                       for p in probe["probes"]],
            "seal": "尾块追加形态（tail_is_append_only）；反替换回程逐字节="
                    "c_final 基底；磁带 blob 零触碰；卖面/肥/M13 零引用",
        },
        "source": {
            "commands": ["python3 orderbook_s3buy5_lab/build_s3buy5.py",
                         "python3 orderbook_s3buy5_lab/probe_s3buy5.py",
                         "python3 orderbook_s3buy5_lab/judge_s3buy5.py"],
            "corpus": {"neutral_spec": "674000+i*147 新块；每对 n=16 双席=32 局/对"
                                       "（vs oc_c3 加密 n=24=48 局）",
                       "folds16": FOLDS16, "folds24": FOLDS24,
                       "abl_folds": ABL_FOLDS},
            "workers": WORKERS,
            "caliber": {
                "h2h": "judge_r44._fold_arm 同 seed 双席折叠（≥1 胜/≤0 负/余平；"
                       "fail-closed）",
                "margin": "终局 farms[obs.player].money 差（干净口径；banks 交叉登记）",
                "hard_currency": "胜率=硬通货；margin/终局钱只作参考",
                "flips": "消融配对 flips_neg 报数（④）",
            },
            "panel": {k: str(v) for k, v in PANEL.items()},
        },
        "opening_diff": {}, "adaptive": {}, "panel": {},
        "criteria": {}, "verdict": {}, "budget": budget,
    })
    flush_evid()

    # ---- sim_bridge 认证 30/30（缓存复用不重扣局次）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth = None
    for cache in (EVID_DIR / "sim_auth_cache.json",
                  KSIM_DIR / "orderbook_composite_lab" / "evidence"
                  / "sim_auth_cache.json"):
        if cache.is_file():
            auth = json.loads(cache.read_text(encoding="utf-8"))
            EV["source"]["sim_auth"] = {
                k: auth.get(k) for k in
                ("loaded", "consistency", "consistency_ok", "degraded",
                 "degraded_reason", "engine", "version", "wall_speedup")}
            EV["source"]["sim_auth"]["reused_cache"] = str(cache)
            budget["auth"] = 30
            break
    if auth is None:
        auth_corpus = [674000 + i * 147 for i in range(8)] + \
            [2026093011 + i for i in range(22)]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(EVID_DIR / "sim_auth_record.json")}, auth_corpus)
        EV["source"]["sim_auth"] = {
            k: auth.get(k) for k in
            ("loaded", "consistency", "consistency_ok", "degraded",
             "degraded_reason", "engine", "version", "wall_speedup")}
        budget["auth"] = 30
        if (EV["source"]["sim_auth"].get("consistency_ok")):
            (EVID_DIR / "sim_auth_cache.json").write_text(
                json.dumps(auth, ensure_ascii=False, default=str) + "\n",
                encoding="utf-8")
    if not EV["source"]["sim_auth"].get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 1) 三臂消融（c_final / s3_open / s3_buy5，配对 flips）----
    abl_rows = {}
    for arm, apath in ABL_ARMS:
        rows = play(_chunk_s3,
                    unit_specs(arm, apath, PANEL["oc_c3"], "oc_c3",
                               ABL_FOLDS, "abl") +
                    unit_specs(arm, apath, PANEL["tetsutani"], "tetsutani",
                               ABL_FOLDS, "abl"),
                    run_cfg)
        budget["ablation"] += len(rows)
        abl_rows[arm] = rows
        flush_evid()
    keyed = {}
    for arm, rows in abl_rows.items():
        for r in rows:
            keyed[(arm, r["seed"], r["seat"], r["opponent"])] = r

    def pairs_for(a, b):
        out = []
        for (arm, seed, seat, opp), r in keyed.items():
            if arm != a:
                continue
            r2 = keyed.get((b, seed, seat, opp))
            if r2 and r.get("margin_clean") is not None \
                    and r2.get("margin_clean") is not None:
                out.append((r["margin_clean"], r2["margin_clean"]))
        return out

    open_pairs = pairs_for("c_final", "s3_open")
    adapt_pairs = pairs_for("s3_open", "s3_buy5")
    full_pairs = pairs_for("c_final", "s3_buy5")
    EV["adaptive"] = {
        "design": "画像族→SHEEP 档位预设（+1 档=全计划护栏；wfr 钉零畜群触碰）"
                  "+ ±1 档摆动；档位=中盘晚波羊链抑制阶梯 {+1:0, 0:≤2, −1:≤4}"
                  "（减法手术）；s3_buy5=safe 档（armed 钉 +1），s3_adapt0=作动形态"
                  "（消融计量作动代价）",
        "elastic_face": "SHEEP 数（GOOSE/COW/班组/单量/卖法=刚性面零触碰；"
                        "D6：SHEEP CV 0.66 3-19 只 / CARROT 地 CV 0.41 为辅）",
        "ablation": {
            "opening_effect_c_final_to_s3_open": flip_stats(open_pairs),
            "adaptive_effect_s3_open_to_s3_buy5": flip_stats(adapt_pairs),
            "total_effect_c_final_to_s3_buy5": flip_stats(full_pairs),
            "wash_literal_effect_s3_open_to_s3_wash": flip_stats(
                pairs_for("s3_open", "s3_wash")),
            "adapt_actuation_cost_s3_open_to_s3_adapt0": flip_stats(
                pairs_for("s3_open", "s3_adapt0")),
            "caliber": "配对 (seed,seat,opp) 两臂 margin_clean 差；flips=胜负翻转",
        },
    }
    flush_evid()

    # ---- 2) 新标准面板（n=16 双席；vs oc_c3 n=24）----
    panel = {}
    panel_rows = {}
    for on, opath in PANEL.items():
        folds = FOLDS24 if on == "oc_c3" else FOLDS16
        rows = play(_chunk_s3,
                    unit_specs("s3_buy5", S3_FULL, opath, on, folds, "panel"),
                    run_cfg)
        budget["panel"] += len(rows)
        panel[on] = fold_stats(rows)
        panel[on]["flips_neg"] = None
        panel_rows[on] = rows
        print("panel s3_buy5 vs", on, "h2h=", panel[on]["h2h"], flush=True)
        flush_evid()
    EV["panel"] = {
        "design": "新标准面板：每对 n=16 双席=32 局（vs oc_c3 加密 n=24=48 局）；"
                  "块 674000+i*147；h2h=judge_r44._fold_arm；margin 只作参考",
        "pairs": panel,
    }

    # ---- 3) 开局对照表 + 行为方差对照 ----
    all_rows = [r for rows in panel_rows.values() for r in rows]
    EV["opening_diff"] = opening_table(all_rows)
    EV["opening_diff"]["static_table"] = next(
        (p.get("table") for p in probe["probes"]
         if p["probe"].startswith("P2")), None)
    EV["adaptive"]["behavior_variance"] = [
        herd_variance(panel_rows["oc_c3"], "vs oc_c3（同对手重复 n=24 双席）"),
        herd_variance(panel_rows.get("tetsutani", []),
                      "vs tetsutani（同对手重复 n=16 双席）"),
    ]
    EV["adaptive"]["behavior_variance_blueprint"] = {
        "sheep_cv_topband": "0.56-0.94（D6 全顶带同构）；#1 实测 CV 0.66 "
                           "（3-19 只）",
        "goose": "刚性面（S3 零触碰=摆动只落 SHEEP 抑制阶梯）",
        "carrot_secondary": "CV 0.41（12-96 格）——辅面参数口留档未作动器",
    }
    flush_evid()

    # ---- 4) 判据 + verdict ----
    h_oc = (panel.get("oc_c3") or {}).get("h2h")
    strong = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_STRONG}
    weak = {o: (panel.get(o) or {}).get("h2h") for o in PANEL_WEAK}
    c1 = bool(h_oc is not None and h_oc >= 0.5)
    c2 = bool(all((h or 0) >= 0.5 for h in strong.values())
              and len(strong) == 3)
    c3 = bool(all((h or 0) >= 0.8 for h in weak.values()) and len(weak) == 2)
    flip_neg_total = (EV["adaptive"]["ablation"]
                      ["adaptive_effect_s3_open_to_s3_buy5"]["flips_neg"]) + \
        (EV["adaptive"]["ablation"]
         ["opening_effect_c_final_to_s3_open"]["flips_neg"])
    ot = EV["opening_diff"]
    c5 = bool(ot["turn1_match"] == ot["turn2_match"] == "%d/%d"
              % (ot["n_games"], ot["n_games"]))
    grade = ("碾压" if (h_oc or 0) >= 0.7 else
             "佳" if (h_oc or 0) >= 0.6 else
             "更强" if (h_oc or 0) >= 0.5 else "未过锚")
    EV["criteria"] = {
        "rule": "①vs oc_c3 ≥0.5（≥0.7 碾压）②强面板逐对 ≥0.5 ③弱锚 ≥0.8 "
                "④flips_neg=0 ⑤开局对照表吻合",
        "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1,
                               "crush_ge_0.7": bool((h_oc or 0) >= 0.7)},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3},
        "c4_flips_neg_zero": {"flips_neg_total": flip_neg_total,
                              "passed": flip_neg_total == 0},
        "c5_opening_table": {"turn1": ot["turn1_match"],
                             "turn2": ot["turn2_match"],
                             "frozen_t1_4": ot["turn1_4_frozen"],
                             "passed": c5},
        "margin_reference_only": True,
    }
    passed = bool(c1 and c2 and c3 and (flip_neg_total == 0) and c5)
    EV["verdict"] = {
        "s3_buy5_sha256": build["main_sha256"],
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "flips_neg_total": flip_neg_total,
        "full_standard_pass": passed,
        "verdict": "FULL_STANDARD_PASS" if passed else "STANDARD_FAIL",
        "summary": "s3_buy5=%s：对冠军锚 oc_c3 h2h %s（%s）；强面板 %s；弱锚 %s；"
                   "开局吻合 t1 %s/t2 %s（冻结 %s）；flips_neg %d；新标准全过=%s"
                   % (build["main_sha256"][:16], h_oc, grade, strong, weak,
                      ot["turn1_match"], ot["turn2_match"],
                      ot["turn1_4_frozen"], flip_neg_total, passed),
        "launch": "不发射不提交（判决先行）；发射候用户令",
    }

    budget["total_局次"] = budget["auth"] + budget["ablation"] + budget["panel"]
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP
    ANOMALIES.extend([
        "胜率=硬通货；margin/终局钱只作参考；harness 噪声不修不管",
        "D6 实测 verbatim 覆盖 D5 粗读：turn2 卖腿=SELL WHEAT 1（洗价卖腿 30 "
        "落 turn1 洗价形原位 tape[0]）；任务括注『SELL WHEAT 洗价腿』按 D6 实测"
        "口径校正；±SHEEP 腿未取（非冻结指纹，D5 turn1 无羊腿）",
        "自适应=减法阶梯（SHEEP 晚波链抑制）：GOOSE 加法线两连败先例（goose_add "
        "−14k/fullplan −10k，loss_replay 块）已避开；D6 弹性面修正（GOOSE 刚性）",
        "CARROT 地弹性辅面（D6 CV 0.41）留参数口未作动器——产线深埋，留焦窗协同",
        "块 674000+i*147 与 c_final 的 i*139 不同块：对 c_final 历史 0.6562 的比较"
        "仅供参考（跨块口径），本程判据只按本块逐对",
        "画像 preset 取 h1_mirror/r37→0 中档（无家族级归因证据，D5 自注未控 seed）；"
        "unknown/wfr 钉 +1 零足迹（C3 域独占）",
    ])
    flush_evid()
    EV["_elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("verdict:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
