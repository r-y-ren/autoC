# -*- coding: utf-8 -*-
"""extend_s3buy5：余量扩展（446 已耗；+32 局=478≤500）。

A. c_final vs r40 补跑 folds[8:16]（弱锚归因对照升 n=16 双席全量）；
B. s3_buy5 vs v48 公开系形态补充对（n=8 双席，降 n 如实注）。
装配进 fn_docs/hybrid/results/2026-09-30-s3-buy5.json。
"""
import json
import time
from pathlib import Path

import judge_s3buy5 as js

HERE = Path(__file__).resolve().parent
RES = js.RESULT_PATH


def main():
    t0 = time.perf_counter()
    cache = HERE / "evidence" / "sim_auth_cache.json"
    if not cache.is_file():
        cache = (js.KSIM_DIR / "orderbook_composite_lab" / "evidence"
                 / "sim_auth_cache.json")
    cfg = {"engine": "auto",
           "bridge": json.loads(cache.read_text(encoding="utf-8")),
           "workers": js.WORKERS}
    ev = json.loads(RES.read_text(encoding="utf-8"))
    budget = ev["budget"]

    rows_ctrl = js.play(js._chunk_s3,
                        js.unit_specs("c_final", js.CFINAL, js.PANEL["r40"],
                                      "r40", js.FOLDS16[8:16], "ext"),
                        cfg)
    rows_v48 = js.play(js._chunk_s3,
                       js.unit_specs("s3_buy5", js.S3_FULL,
                                     js.KSIM_DIR / "opponents" / "v48_main.py",
                                     "v48", js.FOLDS16[:8], "ext"),
                       cfg)
    budget["run3_局次"] = len(rows_ctrl) + len(rows_v48)
    budget["total_局次"] = budget.get("total_局次", 446) + budget["run3_局次"]
    budget["within_cap"] = budget["total_局次"] <= 500

    # r40 对照升 n=16（8+8）
    prev = ev["panel"]["r40_block_control"]
    allc = prev.get("_rows", []) or []
    fold_c16 = js.fold_stats(rows_ctrl)
    fold_s_sup = js.fold_stats(
        [r for r in rows_v48])
    ev["panel"]["r40_block_control"]["c_final_h2h_full16_foldseg"] = \
        {"folds_8_16_h2h": fold_c16.get("h2h"),
         "note": "c_final 对 r40 folds[8:16] 双席；与 folds[0:8] 的 0.75 合读"}
    ev["panel"]["supplementary_v48"] = {
        "opp": "opponents/v48_main.py（公开系形态，D7 补充面）",
        "n": 8, "seats": 2,
        "s3_buy5_h2h": fold_s_sup.get("h2h"),
        "fold": {k: fold_s_sup.get(k) for k in
                 ("n", "wins", "losses", "ties", "mean_margin",
                  "n_games", "n_errors")},
        "note": "降 n=8 双席补充对（非判据项；判据面板六对不变）",
    }
    ev["panel"]["d7_pool_positioning"] = {
        "pool_band_1900_2300": "W20 线 35%/独立系 27%/mass_c14 21%/W8 线 16%（D7）",
        "buy5_facing": "BUY5 顶带几乎不与我方配对（除收敛过 2400）——开局复刻的"
                      "直接对手面窄；价值=指纹通用性+对 BUY5 带的潜在过带能力",
        "adaptive_role": "自适应臂=全带通用主件定位（D7）——本程 SHEEP 抑制实测"
                        "负期望（−5966/局、flips_neg 20）、CARROT 地未作动器；"
                        "弹性落点需产线级重构（转 S2/下一期）",
    }
    an = ev.setdefault("anomaly", [])
    an.append("D7 池面重估：BUY5 复刻直接对手面窄（我带 1900-2300）；自适应臂为"
              "全带主件但本程两种 actuation（羊抑制/未作动 CARROT）均不可用，"
              "弹性面落地=产线级重构议题")
    ev["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    ev["_elapsed_s_total"] = round(time.perf_counter() - t0, 1)
    RES.write_text(json.dumps(ev, ensure_ascii=False, indent=1, default=str)
                   + "\n", encoding="utf-8")
    print("v48 h2h:", fold_s_sup.get("h2h"),
          "r40 ctrl folds8-16:", fold_c16.get("h2h"),
          "total:", budget["total_局次"], flush=True)


if __name__ == "__main__":
    main()
