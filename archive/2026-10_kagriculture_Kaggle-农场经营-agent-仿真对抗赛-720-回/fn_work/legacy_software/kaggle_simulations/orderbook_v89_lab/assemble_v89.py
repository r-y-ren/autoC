# -*- coding: utf-8 -*-
"""assemble_v89：证据汇聚（build/gates/judgment → fn_docs/hybrid/results/
2026-09-29-v89-upgrade.json）。键集=artifact/gates/pairs/criteria/verdict/
anomaly。只读 orderbook_v89_lab/evidence/ 三件；只写最终证据一份。"""
from __future__ import annotations

import json
import os
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
EVID = os.path.join(ROOT, "evidence")
FINAL = os.path.normpath(os.path.join(
    KSIM, "..", "..", "..", "fn_docs", "hybrid", "results",
    "2026-09-29-v89-upgrade.json"))
STRONGER_H2H = 0.55


def _load(name):
    return json.load(open(os.path.join(EVID, name)))


def _pair_lite(p):
    keys = ("n_games", "wins", "losses", "ties", "h2h", "mean_margin",
            "margin_per_game", "ours", "opp_side", "n_error_games",
            "layer_stats", "elapsed_s")
    out = {k: p.get(k) for k in keys}
    for sub in ("replay_r30_26", "neutral_672000_i79"):
        s = p.get(sub) or {}
        out[sub] = {k: s.get(k) for k in
                    ("n_games", "wins", "losses", "ties", "h2h", "mean_margin")}
    return out


def main():
    build = _load("build_v89.json")
    gates = _load("gates_v89.json")
    jud = _load("judgment.json")
    pairs = jud.get("pairs") or {}
    a_h1 = pairs.get("v89p_vs_H1") or {}
    a_r40 = pairs.get("v89p_vs_r40") or {}
    f_h1 = pairs.get("v89full_vs_H1") or {}
    f_p = pairs.get("v89full_vs_v89p") or {}
    h2h = a_h1.get("h2h")
    stronger = isinstance(h2h, (int, float)) and float(h2h) >= STRONGER_H2H

    criteria = list(jud.get("criteria_stage1") or [])
    if a_r40:
        criteria.append({
            "criterion": "参照：h2h vs r40（V82 系历史对照口径）",
            "value": a_r40.get("h2h"), "passed": None})
    if stronger:
        if f_h1:
            criteria.append({
                "criterion": "v89_full h2h vs H1 >= 0.55（全栈版保持基底优势）",
                "value": f_h1.get("h2h"),
                "passed": isinstance(f_h1.get("h2h"), (int, float))
                and float(f_h1["h2h"]) >= STRONGER_H2H})
        if f_p:
            criteria.append({
                "criterion": "v89_full h2h vs v89_pure >= 0.50（我方层在新基底"
                             "净贡献非负；26 败局组）",
                "value": f_p.get("h2h"),
                "passed": isinstance(f_p.get("h2h"), (int, float))
                and float(f_p["h2h"]) >= 0.50})
        if f_h1 and isinstance(f_h1.get("h2h"), (int, float)):
            criteria.append({
                "criterion": "G793 全程零错误（v89_full 判决局层台账 errors=0）",
                "value": ((f_h1.get("layer_stats") or {}).get("g793") or {}
                          ).get("sum_errors"),
                "passed": ((f_h1.get("layer_stats") or {}).get("g793") or {}
                           ).get("sum_errors") == 0})
    criteria.append({
        "criterion": "预算 <=400 局次",
        "value": jud.get("budget", {}).get("total_局次"),
        "passed": bool(jud.get("budget", {}).get("within_cap"))})

    # ---- verdict ----
    if jud.get("aborted"):
        verdict = "ABORTED: %s" % jud["aborted"]
    elif not stronger:
        verdict = ("H1_HOLD：v89_pure h2h vs H1 = %s < %.2f——V89 非更强基底，"
                   "判据未触发→不合成全栈版、不进对照判决；维持 H1（=V82+X1）"
                   "为最强件。注：lab 内已预案构建 v89_full（build 校验+G793 "
                   "零冲突审计绿，sha 见 artifact.forms），仅留档、不列候选、"
                   "未跑四门未判决" % (h2h, STRONGER_H2H))
    else:
        f_h1_ok = isinstance(f_h1.get("h2h"), (int, float)) \
            and float(f_h1["h2h"]) >= STRONGER_H2H
        f_p_ok = isinstance(f_p.get("h2h"), (int, float)) \
            and float(f_p["h2h"]) >= 0.50
        if f_h1_ok and f_p_ok:
            verdict = ("V89_STRONGER + FULL_ADOPT：v89_pure h2h vs H1 = %s "
                       ">= %.2f（基底更强）；v89_full 再压 H1（h2h=%s）且我方层"
                       "净贡献非负（vs v89_pure h2h=%s）→ 全栈版列为新最强件候选"
                       "（不发射不提交）" % (h2h, STRONGER_H2H, f_h1.get("h2h"),
                                             f_p.get("h2h")))
        elif f_h1_ok and not f_p_ok:
            verdict = ("V89_STRONGER + LAYERS_HURT：基底更强（h2h=%s），但全栈版"
                       "对 v89_pure h2h=%s < 0.50——X1/画像/C3 在 V89 基底净负，"
                       "候选=v89_pure（不发射不提交）" % (h2h, f_p.get("h2h")))
        else:
            verdict = ("V89_STRONGER + FULL_FAIL：基底更强（h2h=%s），但 v89_full"
                       " vs H1 h2h=%s < %.2f——合成未保优势，候选=v89_pure"
                       % (h2h, f_h1.get("h2h"), STRONGER_H2H))

    anomaly = {
        "judgment_abort": jud.get("aborted"),
        "budget_trims": (jud.get("stage2") or {}).get("subset_note"),
        "g793_trigger_surface": {
            k: (v.get("layer_stats") or {}).get("g793")
            for k, v in pairs.items()},
        "g793_trigger_finding": (
            "镜像指纹判定 100% 命中（我方 H1/r40 开局窗农场结构本就同世界"
            "同构），但 cha22 现金劈特征（|Δmoney|≥20）0 命中 → G793 门 "
            "0 旁路 0 错误、对本对局零行为影响；V89 vs 我方系的实质差异="
            "V82 减去 PET_CAFE 倾斜（pet_any_demand_agent 尾包被 V89 移除）"),
        "v89_full_prebuild": (
            "判据未触发；v89_full 已预案合成（build 校验+C3 差量守恒 443/34"
            "+G793 零冲突审计绿），但未跑四门、未进对照判决，不列为候选"),
        "harness_noise": "HP_TELEMETRY 为仿真器/官方引擎 harness 自带遥测"
                         "打印，未修未理（任务口径）",
        "v89_g793_mechanism": build.get("artifact", {}).get("diff_vs_v82"),
        "g793_conflict_audit": (build.get("forms", {}).get("v89_full", {})
                                .get("probes", {}).get("g793_conflict_dynamic")),
    }

    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "v89-upgrade/1.0",
        "experiment": "haodou V89（我方 V82 基底作者后续版）基底升级判决："
                      "V89 本体实测 vs 最强 H1（26 败局+新中性块 672000+i*79 "
                      "n=20 双席折叠）+ vs r40 参照；若更强合成 v89_full="
                      "V89+X1+画像器+C3 并对照。不改既有代码、不提交、不发射。",
        "artifact": dict(build.get("artifact") or {},
                         forms=build.get("forms"),
                         build_record="orderbook_v89_lab/evidence/build_v89.json"),
        "gates": gates,
        "pairs": {k: _pair_lite(v) for k, v in pairs.items()},
        "criteria": criteria,
        "verdict": verdict,
        "anomaly": anomaly,
        "budget": jud.get("budget"),
        "source": jud.get("source"),
        "readings_caliber": {
            "wlt_margin": "margin=我席钱−对席钱；双席折叠（fold_arm）",
            "realized_px": "Σ(qty×卖时市价)/Σ(qty×该局该品日均价) 中位",
            "terminal_money": "farms[obs.player].money（干净口径）",
            "g793": "逐局 _G793_REPORT/_G793_STATE（entry __globals__ 采集）",
        },
    }
    os.makedirs(os.path.dirname(FINAL), exist_ok=True)
    with open(FINAL, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    print("verdict:", verdict)
    print("->", FINAL)
    return out


if __name__ == "__main__":
    main()
