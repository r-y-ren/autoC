# -*- coding: utf-8 -*-
"""resume_s3buy5：断点续跑收口（首跑 post-process 缺陷后证据装配）。

首跑（judge_s3buy5.py）已实耗 398 局次（auth30+消融160+面板208；面板逐对 h2h
已落 judge_run.log，消融 flips 已落结果文件）；post-process 在 opening_table
解析缺陷处中断（已修）。本续跑只补：
  A. s3_buy5 vs oc_c3 8fold×双席=16 局 trace（开局对照表+行为方差对照）；
  B. c_final/s3_buy5 vs r40 8fold×双席×2臂=32 局（弱锚 0.4375 归因配对）；
累计 398+48=446 ≤500。然后全量装配证据
fn_docs/hybrid/results/2026-09-30-s3-buy5.json。
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import judge_s3buy5 as js

HERE = Path(__file__).resolve().parent
LOG = HERE / "evidence" / "judge_run.log"
RES = js.RESULT_PATH

PANEL_H2H = {"oc_c3": 0.5, "mpx": 0.5, "tetsutani": 0.5625,
             "V89": 0.5625, "r40": 0.4375, "A": 0.8125}


def parse_log():
    out = {}
    for line in LOG.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.search(r"panel s3_buy5 vs (\S+) h2h= ([0-9.]+)", line)
        if m:
            out[m.group(1)] = float(m.group(2))
    return out


def main():
    t0 = time.perf_counter()
    logged = parse_log()
    for k, v in PANEL_H2H.items():
        if logged.get(k) != v:
            raise RuntimeError("log h2h 漂移 %s: %r vs %r" % (k, logged.get(k), v))
    ev = json.loads(RES.read_text(encoding="utf-8"))
    budget = ev.get("budget") or {}
    budget.update({"run1_局次": 398, "run2_局次": 0, "cap_局次": 500,
                   "note": "首跑 auth30+消融160+面板208=398（post-process 缺陷"
                           "不耗局次）；续跑 48 补 trace/归因"})

    cache = HERE / "evidence" / "sim_auth_cache.json"
    if not cache.is_file():
        cache = (js.KSIM_DIR / "orderbook_composite_lab" / "evidence"
                 / "sim_auth_cache.json")
    cfg = {"engine": "auto",
           "bridge": json.loads(cache.read_text(encoding="utf-8")),
           "workers": js.WORKERS}
    folds = js.FOLDS16[:8]
    rows_oc = js.play(js._chunk_s3,
                      js.unit_specs("s3_buy5", js.S3_FULL, js.PANEL["oc_c3"],
                                    "oc_c3", folds, "resume"),
                      cfg)
    budget["run2_局次"] += len(rows_oc)
    rows_r40 = []
    for arm, path in (("c_final", js.CFINAL), ("s3_buy5", js.S3_FULL)):
        rows_r40 += js.play(js._chunk_s3,
                            js.unit_specs(arm, path, js.PANEL["r40"], "r40",
                                          folds, "resume"),
                            cfg)
    budget["run2_局次"] = len(rows_oc) + len(rows_r40)
    budget["total_局次"] = 398 + budget["run2_局次"]
    budget["within_cap"] = budget["total_局次"] <= 500

    # ---- 开局对照表（执行流 trace）----
    ot = js.opening_table(rows_oc + [r for r in rows_r40 if r["arm"] == "s3_buy5"])
    probe = json.loads((HERE / "evidence" / "probe_s3buy5.json")
                       .read_text(encoding="utf-8"))
    ot["static_table"] = next((p.get("table") for p in probe["probes"]
                               if p["probe"].startswith("P2")), None)
    ot["verdict_note"] = ("逐拍动作=D5 指纹 6/6 + D6 族腿 6/6；洗价形=现金安全"
                          "骨架（13/30/30 全量=证伪件见 s3_wash 消融）")
    ev["opening_diff"] = ot

    # ---- 行为方差对照 ----
    var = [
        js.herd_variance(rows_oc, "vs oc_c3（同对手重复 8fold 双席 n=16）"),
        js.herd_variance([r for r in rows_r40 if r["arm"] == "s3_buy5"],
                         "vs r40（同对手重复 8fold 双席 n=16）"),
    ]
    ev.setdefault("adaptive", {})
    ev["adaptive"]["behavior_variance"] = var
    ev["adaptive"]["behavior_variance_blueprint"] = {
        "sheep_cv_topband": "0.56-0.94（D6 全顶带）；#1 实测 CV 0.66（3-19 只）",
        "goose": "刚性面（S3 零触碰）",
        "carrot_secondary": "CV 0.41（12-96 格）——辅面参数口留档未作动器",
        "our_source": "我方羊摆动=世界自适应路由（羊 4-14/局，route 系）+ "
                      "晚波抑制阶梯（safe 档钉 +1）",
        "swing_signal": "市场态 WOOL/EGG 库存比 @d6=死信号（12 fold 实测 "
                        "inv 9995 恒定）——摆动参数口留档，作动臂见 s3_adapt0",
    }
    ev["adaptive"]["actuation_note"] = (
        "s3_buy5=safe 档（armed 钉 +1，32/32 与 s3_open 逐拍恒等=0.0 配对差）；"
        "s3_adapt0=作动形态消融（n=32 配对 mean_delta −5966.56、flips_neg 20）"
        "——SHEEP 抑制阶梯在本方案链实测负期望，主件护栏钉 +1")

    # ---- r40 归因配对 ----
    keyed = {}
    for r in rows_r40:
        keyed[(r["arm"], r["seed"], r["seat"])] = r
    pairs = []
    for (arm, seed, seat), r in keyed.items():
        if arm != "c_final":
            continue
        r2 = keyed.get(("s3_buy5", seed, seat))
        if r2 and r.get("margin_clean") is not None \
                and r2.get("margin_clean") is not None:
            pairs.append((r["margin_clean"], r2["margin_clean"]))
    control = js.flip_stats(pairs)
    fold_c = js.fold_stats([r for r in rows_r40 if r["arm"] == "c_final"])
    fold_s = js.fold_stats([r for r in rows_r40 if r["arm"] == "s3_buy5"])
    ev["panel"] = {
        "design": "新标准面板：每对 n=16 双席=32 局（vs oc_c3 加密 n=24=48 局）；"
                  "块 674000+i*147；h2h=judge_r44._fold_arm；margin 只作参考",
        "pairs_h2h": PANEL_H2H,
        "pairs_h2h_note": "首跑 fold 折叠 h2h（judge_run.log 实录）；W/L/均值明细"
                          "因 post-process 缺陷失录（h2h=fold 硬通货）",
        "r40_block_control": {
            "c_final_h2h_this_block": fold_c.get("h2h"),
            "s3_buy5_h2h_this_block": fold_s.get("h2h"),
            "paired": control,
            "note": "弱锚 r40 面板 0.4375 归因：同块 c_final 对照（8fold 双席）"
                    "——若对照同弱=块/对手强度效应，非 S3 手术之过",
        },
    }

    # ---- 判据 + verdict ----
    h_oc = PANEL_H2H["oc_c3"]
    strong = {o: PANEL_H2H[o] for o in js.PANEL_STRONG}
    weak = {o: PANEL_H2H[o] for o in js.PANEL_WEAK}
    abl = ev["adaptive"]["ablation"]
    c1 = bool(h_oc >= 0.5)
    c2 = bool(all(h >= 0.5 for h in strong.values()))
    c3 = bool(all(h >= 0.8 for h in weak.values()))
    flips_shipped = (abl["opening_effect_c_final_to_s3_open"]["flips_neg"]
                     + abl["adaptive_effect_s3_open_to_s3_buy5"]["flips_neg"])
    c4 = flips_shipped == 0
    c5 = (ot["turn1_match"].split("/")[0] == ot["turn1_match"].split("/")[1]
          and ot["turn2_match"].split("/")[0] == ot["turn2_match"].split("/")[1])
    grade = ("碾压" if h_oc >= 0.7 else "佳" if h_oc >= 0.6 else
             "更强" if h_oc >= 0.5 else "未过锚")
    ev["criteria"] = {
        "rule": "①vs oc_c3 ≥0.5（≥0.7 碾压）②强面板逐对 ≥0.5 ③弱锚 ≥0.8 "
                "④flips_neg=0 ⑤开局对照表吻合",
        "c1_vs_oc_c3_ge_0.5": {"h2h": h_oc, "grade": grade, "passed": c1,
                               "crush_ge_0.7": bool(h_oc >= 0.7)},
        "c2_strong_all_ge_0.5": {"h2h": strong, "passed": c2},
        "c3_weak_all_ge_0.8": {"h2h": weak, "passed": c3,
                               "r40_block_control_h2h":
                                   fold_c.get("h2h")},
        "c4_flips_neg_zero_shipped_pairs": {"flips_neg": flips_shipped,
                                            "passed": c4},
        "c5_opening_table": {"turn1": ot["turn1_match"],
                             "turn2": ot["turn2_match"],
                             "frozen_t1_4": ot["turn1_4_frozen"], "passed": c5},
        "margin_reference_only": True,
    }
    passed = bool(c1 and c2 and c3 and c4 and c5)
    ev["verdict"] = {
        "s3_buy5_sha256": json.loads(
            (HERE / "build" / "s3_buy5" / "build_manifest.json")
            .read_text(encoding="utf-8"))["main_sha256"],
        "vs_champion_anchor": {"h2h": h_oc, "grade": grade},
        "strong_panel_h2h": strong, "weak_anchor_h2h": weak,
        "flips_neg_shipped": flips_shipped,
        "full_standard_pass": passed,
        "verdict": "FULL_STANDARD_PASS" if passed else "STANDARD_FAIL",
        "summary": "s3_buy5：对冠军锚 oc_c3 h2h %s（%s）；强面板 %s；弱锚 %s"
                   "（r40 同块 c_final 对照 %s）；开局吻合 t1 %s/t2 %s；"
                   "flips_neg %d；新标准全过=%s"
                   % (h_oc, grade, strong, weak, fold_c.get("h2h"),
                      ot["turn1_match"], ot["turn2_match"], flips_shipped,
                      passed),
        "launch": "不发射不提交（判决先行）；发射候用户令",
    }
    an = ev.setdefault("anomaly", [])
    an.append("首跑 post-process 缺陷（opening_table 解析）中断收口；面板 208 局"
              "已跑完（h2h 实录 judge_run.log），续跑 48 局补 trace/归因，累计 "
              "446/500 局次如实计")
    an.append("开局手术恒量代价 −8.0/局（32/32 配对恒定，非级联；groove=净麦 −5 "
              "节奏包络保真）")
    an.append("洗价形 13/30/30 全量移植=−46407 均差/20 flips_neg（n=32 配对）——"
              "对 dump 型开局卖腿被割；主件改现金安全洗价骨架 9买/3卖")
    an.append("SHEEP 抑制阶梯作动（s3_adapt0）=−5966 均差/20 flips_neg（n=32）；"
              "主件 safe 档钉 +1 护栏——herd 手术在本方案链三连负（goose_add "
              "−14k/fullplan −10k/本程 −6k）")
    an.append("市场态摆动信号 d6 死信号（WOOL/EGG 库存 12 fold 恒 9995）；摆动"
              "参数口留档，方差主源=世界自适应路由（羊 4-14）")
    ev["budget"] = budget
    ev["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ev["_elapsed_s"] = round(time.perf_counter() - t0, 1)
    RES.write_text(json.dumps(ev, ensure_ascii=False, indent=1, default=str)
                   + "\n", encoding="utf-8")
    print("verdict:", ev["verdict"]["verdict"], flush=True)
    print("c3 weak:", weak, "control:", fold_c.get("h2h"), flush=True)
    return ev


if __name__ == "__main__":
    main()
