# -*- coding: utf-8 -*-
"""judge_milkwin_carpet：窗内地毯臂 mx_carpet 加跑（人工放行）。

背景：前置臂帽/阈均不绑定（旋钮在时机），预登记门本意=参数不行才打时机；
人工放行 d14-20（step 336-480）MILK 日新高追加单（帽 20/步）加跑。
- 对阵：变体 vs oc_c3 配对同语料（26 败局前 8 fold + 新中性 672000+i*107×8，
  n=16 双席=32 (seed,seat) 单元/臂；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转）。
- 引擎：官方（kaggsim.official 认证钉版）——sim_bridge 30/30 已证两引擎终局
  资金等价（见主跑 source.sim_auth），续跑直取官方免 60 认证局；并以确定性
  同语料重跑 oc_c3 对照 32 局（首轮只存聚合、配对需逐单元窗读数），与首轮
  存档 margin_control 逐格交叉核对。
- 判据沿用四条：净翻胜>0 ∧ flips_neg==0 ∧ 实现价非负（Δratio_fill MILK∧全品
  ≥0）∧ d14-20 窗收入差转正（fill 口径总窗配对 mean Δ>0）；附窗逐日对照。
- 预算：64 局（≤放行余量 97）；累计 317/350。
结果补进 fn_docs/hybrid/results/2026-09-29-milk-window.json 的 carpet 节；
账本落 orderbook_milkwin_lab/evidence/。只写 orderbook_milkwin_lab/ 与该
results JSON。不改既有代码、不发射、不提交。
"""
from __future__ import annotations

import json
import os
import time
from pathlib import Path

import judge_milkwin as J

RECORD_ADD = "milk-window/carpet-followup/1.0"
CONTROL = "oc_c3"
CARPET = "mx_carpet"
RUN_ARMS = (CONTROL, CARPET)          # oc_c3 确定性重跑 + 地毯臂
FOLLOWUP_ENVELOPE = 97


def main():
    os.chdir(J.KSIM_DIR)
    t0 = time.perf_counter()
    ev = json.loads(J.EVID_PATH.read_text(encoding="utf-8"))

    units, opp_paths = J.make_units()
    run_cfg = {"engine": "official", "workers": J.WORKERS}
    budget_add = {"envelope_局次": FOLLOWUP_ENVELOPE, "arms": {}}

    rows_by_arm = {}
    for arm in RUN_ARMS:
        specs = J.make_specs(arm, J.ARMS[arm], units)
        t1 = time.perf_counter()
        rows, engines = J._play(specs, run_cfg)
        rows_by_arm[arm] = rows
        budget_add["arms"][arm] = len(rows)
        n_err = sum(1 for r in rows if r.get("error"))
        print(arm, "games", len(rows), "err", n_err,
              "tm", J.end_agg(rows)["terminal_money_mean"],
              "win", J.window_agg(rows)["mean_fill_total"],
              "engines", engines,
              round(time.perf_counter() - t1, 1), "s", flush=True)
        if n_err:
            ev["anomaly"].append("carpet 续跑 %s 局红 %d/%d" % (arm, n_err,
                                                              len(rows)))

    ctl = {(r["seed"], r["seat"]): r for r in rows_by_arm[CONTROL]}
    var = {(r["seed"], r["seat"]): r for r in rows_by_arm[CARPET]}

    # ---- 与首轮 oc_c3 存档逐格交叉核对（确定性 + 引擎等价） ----
    xrows = (ev.get("pairs", {}).get("mx_cap2_vs_oc_c3", {})
             .get("rows_lite") or [])
    xchk = {"design": "确定性同语料重跑 oc_c3（官方）vs 首轮（sim）存档 "
                      "margin_control 逐格相等", "n": 0, "n_match": 0,
            "mismatch": []}
    for row in xrows:
        key = (int(row["seed"]), int(row["seat"]))
        rc = ctl.get(key)
        if not rc or rc.get("margin") is None:
            continue
        xchk["n"] += 1
        ok = abs(float(rc["margin"]) - float(row["margin_control"])) < 1e-6
        if ok:
            xchk["n_match"] += 1
        elif len(xchk["mismatch"]) < 8:
            xchk["mismatch"].append({"seed": key[0], "seat": key[1],
                                     "rerun": rc["margin"],
                                     "stored": row["margin_control"]})
    xchk["passed"] = bool(xchk["n"] and xchk["n_match"] == xchk["n"])
    print("crosscheck:", xchk["n_match"], "/", xchk["n"], flush=True)
    if not xchk["passed"]:
        ev["anomaly"].append("carpet 续跑 oc_c3 重跑与首轮存档 margin 不全等"
                             "（%d/%d）；配对以本轮重跑为准" %
                             (xchk["n_match"], xchk["n"]))

    # ---- 判决（四判据沿用） ----
    ps = J.pair_stats(ctl, var, units)
    wp = J.window_paired(ctl, var, units)
    rp = J.realized_paired(ctl, var, units)
    win_d = wp["fill_total"]["mean_delta"]
    crit = {
        "净翻胜>0": ps["net_flip_wins"] > 0,
        "flips_neg==0": ps["flips_neg"] == 0,
        "实现价非负（Δratio_fill MILK∧全品均值≥0）": rp["nonneg_both"],
        "d14-20窗收入差转正（fill 总窗配对 mean Δ>0）": (J.is_num(win_d)
                                                       and float(win_d) > 0),
    }
    positive = all(crit.values())
    trig = {
        "carpet_steps_total": sum(int((r.get("mx") or {}).get("carpet_steps")
                                      or 0) for r in rows_by_arm[CARPET]),
        "carpet_units_total": sum(int((r.get("mx") or {}).get("carpet_units")
                                      or 0) for r in rows_by_arm[CARPET]),
        "games_with_carpet": sum(1 for r in rows_by_arm[CARPET]
                                 if int((r.get("mx") or {}).get("carpet_steps")
                                        or 0) > 0),
    }

    # ---- 合并进 evidence（carpet 节） ----
    ev.setdefault("pairs", {})["%s_vs_oc_c3" % CARPET] = ps
    ev.setdefault("window_stats", {})[CARPET] = J.window_agg(rows_by_arm[CARPET])
    ev["window_stats"][CONTROL + "_rerun_official"] = J.window_agg(
        rows_by_arm[CONTROL])
    ev["window_stats"]["paired_%s_vs_oc_c3" % CARPET] = wp
    ev.setdefault("per_item_realized", {})[CARPET] = J.realized_agg(
        rows_by_arm[CARPET])
    ev["per_item_realized"][CONTROL + "_rerun_official"] = J.realized_agg(
        rows_by_arm[CONTROL])
    ev.setdefault("realized_px_paired", {})["%s_vs_oc_c3" % CARPET] = rp
    ev.setdefault("terminal_money", {})[CARPET] = J.end_agg(rows_by_arm[CARPET])
    ev["terminal_money"][CONTROL + "_rerun_official"] = J.end_agg(
        rows_by_arm[CONTROL])
    ev.setdefault("criteria", {})[CARPET] = {
        "checks": crit,
        "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
        "realized_px_nonneg_both": rp["nonneg_both"],
        "positive_arm": positive}
    ev["carpet_arm"] = {
        "form": CARPET, "ran": True,
        "reason": "人工放行（前置臂帽/阈均不绑定=旋钮在时机；预登记门本意=参数"
                  "不行才打时机）",
        "mechanism": ("d14-20（step 336-480）MILK 日新高追加单（p_now≥当日窗内"
                     "高点）帽 20/步；只加同拍挂卖、量限投射仓未挂余量、同拍买侧"
                     " MILK 不动、满 10 单不加、异常回退"),
        "params": ev["variants"][CARPET]["params"],
        "trigger_surface": trig,
        "engine": "official（kaggsim.official 认证钉版；sim_bridge 30/30 已证"
                  "两引擎资金等价，续跑免认证局）",
        "control_rerun": ("确定性同语料重跑 oc_c3 32 局（首轮只存聚合，配对需"
                          "逐单元窗读数）"),
        "crosscheck_vs_stage1": xchk,
        "budget_add": budget_add,
    }
    v = ev.setdefault("verdict", {})
    v.setdefault("per_variant", {})[CARPET] = {
        "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
        "mean_delta": ps["mean_delta"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
        "realized_px_nonneg_both": rp["nonneg_both"],
        "positive_arm": positive}
    if positive:
        v["positive_variants"] = list(v.get("positive_variants") or []) + \
            [CARPET]
    v["verdict"] = ("牛奶窗变现正臂：%s" % (", ".join(v["positive_variants"])
                                           if v.get("positive_variants")
                                           else "无（含地毯臂在内受测变体均未"
                                                "全过四判据）"))
    v["carpet_verdict_lite"] = {
        "W/L/T": "%d/%d/%d" % (ps["W"], ps["L"], ps["T"]),
        "mean_delta": ps["mean_delta"],
        "net_flip_wins": ps["net_flip_wins"], "flips_neg": ps["flips_neg"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
        "per_day_fill_milk_delta_mean": {
            k: vv["mean_delta"] for k, vv in
            wp["per_day_fill_milk_delta"].items()},
        "positive_arm": positive}

    b = ev.setdefault("budget", {})
    b["carpet_局次"] = int(b.get("carpet_局次") or 0) + sum(
        budget_add["arms"].values())
    b["total_局次"] = (int(b.get("auth_局次") or 0)
                       + int(b.get("judgment_局次") or 0)
                       + int(b.get("carpet_局次") or 0)
                       + int(b.get("smoke_局次") or 0))
    b["within_cap"] = b["total_局次"] <= int(b.get("cap_局次") or 0)
    b["carpet_followup"] = budget_add
    ev["anomaly"].append(
        "carpet 续跑引擎=官方（kaggsim.official 认证钉版），与首轮 sim 臂口径"
        "差异由 sim_bridge 30/30 等价认证 + oc_c3 逐格交叉核对背书")
    ev["anomaly"].append(
        "carpet 续跑预算 %d 局（oc_c3 重跑 %d + mx_carpet %d）≤放行余量 %d"
        % (sum(budget_add["arms"].values()), budget_add["arms"][CONTROL],
           budget_add["arms"][CARPET], FOLLOWUP_ENVELOPE))
    ev["elapsed_s_carpet_followup"] = round(time.perf_counter() - t0, 1)
    ev["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ev["_record_version"] = RECORD_ADD

    J.EVID_PATH.write_text(json.dumps(ev, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")
    J.LEDGER_PATH.write_text(json.dumps(
        {"carpet_followup": {
            "pair": {k: ps[k] for k in ("n", "W", "L", "T", "mean_delta",
                                        "net_flip_wins", "flips_neg",
                                        "win_control", "win_variant")},
            "window_fill_total_mean_delta": win_d,
            "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
            "criteria": crit, "trigger_surface": trig,
            "crosscheck": xchk, "budget_add": budget_add}},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    print("CARPET:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
          "dM", ps["mean_delta"], "netflip", ps["net_flip_wins"],
          "flips_neg", ps["flips_neg"], "dWin", win_d,
          "dWinMilk", wp["fill_milk"]["mean_delta"],
          "px_nonneg", rp["nonneg_both"], "positive", positive, flush=True)
    print("per_day milk d:", {k: vv["mean_delta"] for k, vv in
                              wp["per_day_fill_milk_delta"].items()},
          flush=True)
    print("trig:", trig, flush=True)
    print("DONE", ev["elapsed_s_carpet_followup"], "s budget:",
          budget_add, flush=True)
    return ev


if __name__ == "__main__":
    main()
