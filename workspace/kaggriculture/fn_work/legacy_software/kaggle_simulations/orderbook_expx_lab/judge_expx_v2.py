# -*- coding: utf-8 -*-
"""judge_expx_v2：expx 胜位守卫版再验（判决先行·不发射不提交）。

责任口径（任务 expx-v2）：
- 形态=expx_v2（v1 精确模型 + 胜位守卫 ①窗收缩 step144-648 生效、648 后全
  基线语义 ②滞留保险 MR 持有时模型窗内峰值容量清不掉该件→基线出货）。
- 语料=v1 全块 + 第二中性块 673000+i*119（n=16 双席）：26 败局前 8 fold +
  672000+i*117×8 + 673000+i*119×8 = 24 fold 双席 = 48 格/臂；重点复核
  963182245 类格（v1 唯一翻负种子，双席 vs r37）是否再现。
- 判据不变：净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（Δratio_fill 三品∧全品
  均值≥0）∧ d14-27 窗收入差转正（fill 总窗配对 Δ>0）。
- 足迹审计门沿轨道 2 范式；sim_bridge 认证 30/30 先行；workers=2；预算
  ≤250 局次。
证据并入 fn_docs/hybrid/results/2026-09-29-expx-model.json（v2 节）；账本
落 orderbook_expx_lab/evidence/。复用 judge_expx 机件（不改写 v1 判决件）。
只写 orderbook_expx_lab/ 与该 evidence JSON。
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import statistics
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
for _p in (str(MODULE_DIR),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_expx as je  # noqa: E402  （v1 机件复用；含 jm 窗口径热替换）

RECORD_VERSION = "expx-model-v2/1.0"
UNKNOWN = "UNKNOWN"

LOSS_FOLDS = je.LOSS_FOLDS
NEUTRAL1 = je.NEUTRAL_FOLDS                    # 672000+i*117（v1 块）
NEUTRAL2 = [673000 + i * 119 for i in range(8)]  # 第二中性块（任务给定）
FOLDS = LOSS_FOLDS + NEUTRAL1 + NEUTRAL2       # n=24 双席 fold
RECHECK_SEED = 963182245

EXPX_V2_MAIN = str(MODULE_DIR / "build" / "expx_v2" / "main.py")
ARMS = {"oc_c3": je.OC_C3_MAIN, "expx_v2": EXPX_V2_MAIN}
RUN_FORMS = ("oc_c3", "expx_v2")
je.RUN_FORMS = RUN_FORMS                      # per_item_table 口径对齐

WORKERS = 2
BUDGET_CAP_GAMES = 250
REUSE_AUTH = True      # 首跑已过 sim_bridge 30/30（record 在盘）；崩溃重跑不
                       # 重认证不冒烟，直接 engine=sim 复用同日认证件
RAW_ROWS_PATH = MODULE_DIR / "evidence" / "raw_rows_v2.json.gz"
EVID_PATH = je.EVID_PATH                      # 同一 evidence JSON（v2 节）
LEDGER_PATH = MODULE_DIR / "evidence" / "expx_v2_ab_ledger.json"

EV2 = {}
ANOMALIES = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_v2():
    """并入主 evidence JSON（v2 节；v1 节原样保留）。"""
    EV2["anomaly"] = list(ANOMALIES)
    EV2["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    try:
        doc = json.loads(EVID_PATH.read_text(encoding="utf-8"))
    except Exception:
        doc = {}
    doc["v2"] = EV2
    EVID_PATH.write_text(json.dumps(doc, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def save_raw(rows_by_arm):
    """逐臂落 raw 账本（gzip；崩溃不重损）。"""
    with gzip.open(RAW_ROWS_PATH, "wt", encoding="utf-8") as fh:
        json.dump(rows_by_arm, fh, default=str)


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(je.KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        if seed in set(LOSS_FOLDS):
            stratum = "loss_replay"
        elif seed in set(NEUTRAL1):
            stratum = "neutral_672000_i117"
        else:
            stratum = "neutral_673000_i119"
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
            "game_id": "expx2-%s-%d-s%d" % (arm, int(r["seed"]), int(r["seat"])),
            "seed": int(r["seed"]), "arm": arm, "our_seat": int(r["seat"]),
            "trace": True, "opponent": r.get("opponent"),
            "stratum": r.get("stratum"), "agents": agents})
    return specs


def _row_fill_total(row, in_window):
    sw = row.get("shadow") or {}
    if in_window:
        acc = 0.0
        for _day, items in ((row.get("window") or {}).get("fill") or {}).items():
            for _it, r in (items or {}).items():
                acc += float((r or {}).get("value") or 0)
        return acc
    by = (sw.get("per_item_by_seat") or {}).get(int(row.get("seat", 0))) or {}
    return sum(float((r or {}).get("value") or 0) for r in by.values())


def outside_window_paired(ctl, var, units):
    """窗外（step<336 ∪ ≥672）fill 口径配对 Δ——v1 败因归因（早局/末局侧）。"""
    deltas, rows = [], []
    for u in units:
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        if not rc or not rv:
            continue
        vc = _row_fill_total(rc, False) - _row_fill_total(rc, True)
        vv = _row_fill_total(rv, False) - _row_fill_total(rv, True)
        d = vv - vc
        deltas.append(d)
        if u["seed"] == RECHECK_SEED or len(rows) < 10:
            rows.append({"seed": u["seed"], "seat": u["seat"],
                         "outside_control": round(vc, 1),
                         "outside_variant": round(vv, 1),
                         "delta": round(d, 1)})
    return {"n": len(deltas),
            "mean_delta": round(sum(deltas) / len(deltas), 2) if deltas
            else UNKNOWN,
            "median_delta": round(statistics.median(deltas), 2) if deltas
            else UNKNOWN,
            "n_pos": sum(1 for d in deltas if d > 0),
            "rows_lite": rows}


def recheck_rows(ctl, var, units, wp):
    """963182245 复核格（v1 翻负种子；双席）。"""
    out = []
    for u in units:
        if u["seed"] != RECHECK_SEED:
            continue
        key = (u["seed"], u["seat"])
        rc, rv = ctl.get(key), var.get(key)
        if not rc or not rv:
            continue
        wr = next((r for r in (wp.get("rows_lite") or [])
                   if r.get("seed") == u["seed"] and r.get("seat") == u["seat"]),
                  {})
        out.append({
            "seat": u["seat"], "opponent": u.get("opponent"),
            "margin_control": rc.get("margin"), "margin_variant": rv.get("margin"),
            "delta": round(float(rv["margin"]) - float(rc["margin"]), 1),
            "d_window_fill_total": wr.get("d_fill_total"),
            "d_window_fill_milk": wr.get("d_fill_milk"),
            "outside_fill_delta": round(
                _row_fill_total(rv, False) - _row_fill_total(rv, True)
                - (_row_fill_total(rc, False) - _row_fill_total(rc, True)), 1),
            "expx_fires": (rv.get("expx") or {}).get("fires"),
            "expx_units": (rv.get("expx") or {}).get("units"),
            "stranding_insured": (rv.get("expx") or {}).get("stranding_insured"),
            "post_win_base": (rv.get("expx") or {}).get("post_win_base"),
        })
    return out


def main():
    os.chdir(je.KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(je.OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != je.OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    man = json.loads((MODULE_DIR / "build" / "expx_v2" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    v2_sha = hashlib.sha256(Path(EXPX_V2_MAIN).read_bytes()).hexdigest()
    if v2_sha != man.get("main_sha256"):
        raise RuntimeError("expx_v2 main sha 漂移")
    prev_v2 = {}
    try:
        prev_v2 = json.loads(EVID_PATH.read_text(encoding="utf-8")).get("v2") \
            or {}
    except Exception:
        prev_v2 = {}

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES, "smoke_局次": 1, "auth_局次": 0,
              "judgment_局次": 0}

    EV2.update({
        "version": RECORD_VERSION,
        "experiment": ("expx 胜位守卫版再验（expx-v2）：v1 方向获支持（窗差 "
                       "+144/均差 +85/实现价升/零足迹）败因=尾部守卫（2 翻负"
                       "=同种子双席、回退点窗外早局/末局滞留侧）→ ①窗收缩 "
                       "144-648 ②滞留保险 组合守卫 + 第二中性块 673000+i*119"
                       " 复核"),
        "guard": man.get("guard"),
        "source": {
            "commands": ["python3 orderbook_expx_lab/build_expx_v2.py",
                         "python3 orderbook_expx_lab/judge_expx_v2.py"],
            "base_main": je.OC_C3_MAIN, "base_sha256": base_sha,
            "expx_v2_main": EXPX_V2_MAIN, "expx_v2_sha256": v2_sha,
            "build_manifest": {k: man.get(k) for k in
                               ("subs_roundtrip_identity_ok",
                                "gate_literal_untouched", "horizon_k",
                                "win_end", "term", "entry_last_callable",
                                "host_entry")},
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds_1": NEUTRAL1,
                       "neutral_folds_2": NEUTRAL2,
                       "neutral_2_spec": "673000+i*119（任务给定第二中性块 "
                                         "n=8×双席=16 格）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局前 8 + 672000+i*117×8 + 673000+i*119×8"
                                 "；双席 fold n=24/臂=48 格/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": je.EV.get("source", {}).get("caliber") or {
                "unit": "配对单元=(seed,seat)",
                "window": "d14-27 窗 step 336-672 fill 口径主/submit 对照",
                "realized_px": "Σ(filled×成交价)/Σ(filled×base)（膝点表口径）",
                "terminal_money": "farms[obs.player].money（干净口径）"},
            "criterion": ("净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（配对 "
                          "Δratio_fill 三品∧全品均值≥0）∧ d14-27 窗收入差转正"
                          "（fill 口径总窗配对 Δ>0，对照 oc_c3）"),
        },
        "pairs": {}, "window_stats": {}, "per_item_realized": {},
        "per_item_table": {}, "realized_px_paired": {}, "terminal_money": {},
        "gates_footprint": {}, "criteria": {}, "verdict": {},
        "recheck_963182245": {}, "outside_window_fill": {},
        "budget": budget,
    })
    flush_v2()

    # ---- 1) sim_bridge 对照认证 30/30（首跑已过；崩溃重跑复用不重认证） ----
    if REUSE_AUTH and (prev_v2.get("source") or {}).get("sim_auth", {}).get(
            "consistency_ok"):
        EV2["source"]["sim_auth"] = dict(
            prev_v2["source"]["sim_auth"],
            reused_from_first_run=True,
            record="evidence/sim_auth_record_v2.json（首跑 30/30）")
        budget["auth_局次"] = 60       # 首跑记账（未重跑）
        budget["smoke_局次"] = 1        # 首跑记账（未重跑）
        budget["judgment_局次_崩溃首跑"] = 96
        run_cfg = {"engine": "sim", "workers": WORKERS}
        print("sim auth: REUSED (first run 30/30)", flush=True)
    else:
        auth_corpus = list(je.jm.REPLAY_26) + [2026092901, 2026092902,
                                               2026092903, 2026092904]
        auth = sb.sim_bridge(
            {"n_games": 30, "min_checked": 30,
             "record_path": str(MODULE_DIR / "evidence"
                                / "sim_auth_record_v2.json")},
            auth_corpus)
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "wall_speedup",
                      "consistency_ok", "degraded", "degraded_reason",
                      "engine", "timing", "version")}
        EV2["source"]["sim_auth"] = auth_lite
        budget["auth_局次"] = 60
        print("sim auth:", auth_lite.get("consistency_ok"),
              auth_lite.get("consistency"), flush=True)
        if not auth_lite.get("consistency_ok"):
            EV2["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
            flush_v2()
            return EV2
        run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 2) 冒烟（崩溃重跑跳过；首跑已冒烟） ----
    if not (prev_v2.get("expx_v2_telemetry") is not None
            or prev_v2.get("gates_footprint")):
        smoke_units = [{"seed": 2026092999, "seat": 0,
                        "opp_path": opp_paths[0], "opponent": "r37",
                        "stratum": "smoke"}]
        smoke_rows, _e0 = je._play(
            make_specs("smoke", ARMS["expx_v2"], smoke_units), run_cfg)
        print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
              flush=True)
        if smoke_rows[0].get("error"):
            ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
        budget["smoke_局次"] = 1
    # 首跑（崩溃）已刷出的聚合留作确定性交叉核对
    if prev_v2:
        EV2["crashed_run_crosscheck"] = {
            "note": "首跑（后处理 bug 崩溃）已刷出的聚合；本次确定性重跑应逐值"
                    "相等（同种子同件）",
            "terminal_money": {a: (prev_v2.get("terminal_money") or {}).get(a)
                               for a in ("oc_c3", "expx_v2")},
            "window_mean_fill_total": {
                a: ((prev_v2.get("window_stats") or {}).get(a) or {}).get(
                    "mean_fill_total") for a in ("oc_c3", "expx_v2")},
            "footprint": {k: (prev_v2.get("gates_footprint") or {}).get(k)
                          for k in ("n_cells", "n_passed", "gate_passed")},
            "expx_v2_telemetry": prev_v2.get("expx_v2_telemetry")}
    flush_v2()

    # ---- 3) 双臂实跑 ----
    rows_by_arm = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = je._play(specs, run_cfg)
        rows_by_arm[arm] = rows
        save_raw(rows_by_arm)
        budget["judgment_局次"] += len(rows)
        EV2["per_item_realized"][arm] = je.jm.realized_agg(rows)
        EV2["terminal_money"][arm] = je.jm.end_agg(rows)
        EV2["window_stats"][arm] = je.jm.window_agg(rows)
        EV2["window_stats"][arm]["window"] = "d14-27（step 336-672）"
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d" % (arm, n_err, len(rows)))
        mism = EV2["per_item_realized"][arm]["aggregate"].get(
            "shadow_mismatch_steps")
        if mism:
            ANOMALIES.append("%s 影子引擎不一致步 %s" % (arm, mism))
        if arm == "expx_v2":
            te = {"fires": 0, "units": 0, "errors": 0, "censored_lo": 0,
                  "decision_diffs": 0, "mr_limited": 0, "cap_limited": 0,
                  "stranding_insured": 0, "post_win_base": 0}
            for r in rows:
                x = r.get("expx") or {}
                for k in ("fires", "units", "errors", "censored_lo",
                          "mr_limited", "cap_limited", "stranding_insured",
                          "post_win_base"):
                    te[k] += int(x.get(k) or 0)
                te["decision_diffs"] += len(x.get("decision_diff_steps") or [])
            EV2["expx_v2_telemetry"] = te
        print(arm, "games", len(rows), "err", n_err,
              "tm", EV2["terminal_money"][arm]["terminal_money_mean"],
              "win_fill_total", EV2["window_stats"][arm]["mean_fill_total"],
              "shadow_mism", mism, round(time.perf_counter() - t2, 1), "s",
              flush=True)
        EV2["budget"] = budget
        flush_v2()

    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    var = {(r["seed"], r["seat"]): r for r in rows_by_arm["expx_v2"]}

    # ---- 4) 足迹审计门（轨道 2 范式） ----
    fp = je.footprint_audit(ctl, var, units)
    EV2["gates_footprint"] = fp
    if not fp["gate_passed"]:
        ANOMALIES.append("足迹审计门未全过：%d/%d 格过"
                         % (fp["n_passed"], fp["n_cells"]))
    print("footprint:", fp["n_passed"], "/", fp["n_cells"], flush=True)
    flush_v2()

    # ---- 5) 配对判决 + 窗外归因 + 963182245 复核 ----
    ps = je.jm.pair_stats(ctl, var, units)
    wp = je.jm.window_paired(ctl, var, units)
    rp = je.realized_paired3(ctl, var, units)
    EV2["pairs"]["expx_v2_vs_oc_c3"] = ps
    EV2["window_stats"]["paired_expx_v2_vs_oc_c3"] = wp
    EV2["realized_px_paired"]["expx_v2_vs_oc_c3"] = rp
    EV2["per_item_table"] = je.per_item_table(EV2["per_item_realized"])
    EV2["outside_window_fill"] = outside_window_paired(ctl, var, units)
    EV2["recheck_963182245"] = {
        "note": "v1 唯一翻负种子（双席 vs r37，margin 119→−156，Δ−275×2）"
                "在 v2 语料（含第二中性块）复核",
        "cells": recheck_rows(ctl, var, units, wp)}
    win_d = wp["fill_total"]["mean_delta"]
    crit = {
        "净翻胜>0": ps["net_flip_wins"] > 0,
        "flips_neg==0": ps["flips_neg"] == 0,
        "实现价非负（Δratio_fill 三品∧全品均值≥0）": rp["nonneg_all_three"],
        "d14-27窗收入差转正（fill 总窗配对 mean Δ>0）": is_num(win_d)
        and float(win_d) > 0,
    }
    EV2["criteria"] = {
        "checks": crit,
        "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
        "W_L_T": "%s/%s/%s" % (ps["W"], ps["L"], ps["T"]),
        "mean_delta": ps["mean_delta"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
        "outside_window_fill_mean_delta":
            EV2["outside_window_fill"]["mean_delta"],
        "realized_px_nonneg_all_three": rp["nonneg_all_three"],
        "footprint_gate_passed": fp["gate_passed"],
        "positive_arm": all(crit.values())}
    print("expx_v2 vs oc_c3:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
          "dM", ps["mean_delta"], "netflip", ps["net_flip_wins"],
          "flips_neg", ps["flips_neg"], "dWin", win_d,
          "dOutside", EV2["outside_window_fill"]["mean_delta"],
          "px_nonneg", rp["nonneg_all_three"], "crit", crit, flush=True)

    # ---- 6) verdict ----
    budget["total_局次"] = (budget["auth_局次"] + budget["judgment_局次"]
                           + budget["smoke_局次"]
                           + int(budget.get("judgment_局次_崩溃首跑") or 0))
    budget["total_对局口径"] = (30 + int(budget["smoke_局次"])
                               + int(budget["judgment_局次"])
                               + int(budget.get("judgment_局次_崩溃首跑") or 0))
    budget["within_cap_对局口径"] = budget["total_对局口径"] <= BUDGET_CAP_GAMES
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES
    budget["note"] = ("预算逐项=认证 60(30 局×2 引擎)+冒烟 1+判决 96/跑；"
                      "崩溃首跑整批计入 judgment_局次_崩溃首跑；REUSE_AUTH "
                      "生效时认证/冒烟沿首跑记账不重跑，否则按实际跑次累加")
    ok_all = all(crit.values())
    recheck_flip = any((c.get("margin_control") or 0) > 0
                       and (c.get("margin_variant") or 0) <= 0
                       for c in EV2["recheck_963182245"]["cells"])
    EV2["verdict"] = {
        "criterion": EV2["source"]["criterion"],
        "criteria_passed": ok_all,
        "footprint_gate_passed": fp["gate_passed"],
        "recheck_963182245_flip_recurred": bool(recheck_flip),
        "per_item_ratio_fill_delta": {
            it: (EV2["per_item_table"].get(it) or {}).get("d_ratio_fill")
            for it in je.MX_ITEMS},
        "verdict": ("EXPX_V2_POSITIVE: 胜位守卫版四判据全过（足迹审计门%s，"
                    "963182245 翻负%s）"
                    % ("过" if fp["gate_passed"] else "未过",
                       "再现" if recheck_flip else "未再现") if ok_all else
                    "NOT_CONFIRMED（详见 criteria）"),
        "form": "expx_v2",
        "note": "判据与 v1 同（预登记）；不发射不提交",
    }
    EV2["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV2["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行；"
                     "kaggle_environments 可选环境加载告警")
    ANOMALIES.append("守卫口径备忘：①窗收缩后 fire_x=fire_base（648+ 零足迹）；"
                     "②滞留保险容量=模型窗内峰值拍×基线帽逐拍扣减（上限口径，"
                     "保险仅在清不掉投射仓存量时触发）；投影不含自家未来销售、"
                     "不含未来商店解锁")
    LEDGER_PATH.write_text(json.dumps(
        {"pairs": {"expx_v2_vs_oc_c3": {k: ps[k] for k in
                                        ("n", "W", "L", "T", "mean_delta",
                                         "net_flip_wins", "flips_neg")}},
         "window": {"fill_total_mean_delta": wp["fill_total"]["mean_delta"],
                    "fill_milk_mean_delta": wp["fill_milk"]["mean_delta"]},
         "outside_window_fill_mean_delta":
             EV2["outside_window_fill"]["mean_delta"],
         "recheck_963182245": EV2["recheck_963182245"],
         "criteria": EV2["criteria"], "budget": budget},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_v2()
    print("DONE", EV2["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV2["verdict"]["verdict"], flush=True)
    return EV2


if __name__ == "__main__":
    main()
