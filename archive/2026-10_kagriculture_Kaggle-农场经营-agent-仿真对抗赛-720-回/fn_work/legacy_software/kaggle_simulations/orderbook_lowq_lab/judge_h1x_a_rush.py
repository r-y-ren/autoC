# -*- coding: utf-8 -*-
"""judge_h1x_a_rush（极速快测）：h1x_a（d29 申报校准移植件）H1X 侧配对验证。

对象 h1x_a = orderbook_lowq_lab/build/h1x_a/main.py（24adb04f…）
基座 H1X = orderbook_h1x_lab/build/h1x/main.py（9d073fba…）
判据极简：①配对 delta>0 ②flips_neg=0 —— 两门过=PASS（发射由主会话执行）。
面板（全部复用现成 judge 管线 judge_h1x 跑口/sim_bridge 认证缓存）：
  1. 配对 vs H1X 本体：12 seed（lowq_verdict 低报价子集 spike_ticks<900）
     双席（24 unit），同 (seed,seat,opp=oc_c3) 逐 unit delta（h1x_a−h1x），
     报 W-L-T/mean_delta/flips_neg/flips_pos；
  2. 弱锚 r40 6 fold 双席（回归检查：h2h 不低于 H1X 基线 0.8333）。
预算 ≤100 局（配对 48 + r40 12 = 60 实跑，去重缓存）。确定性不重跑（构建件
已双跑）。只测不发，绝不在线提交。证据 evidence/h1x_a_rush.json。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_s1form_lab"),
          str(KSIM_DIR / "orderbook_h1x_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_h1x as jh  # noqa: E402  只读复用（mk_specs/run_specs/fold/pairs）

H1X_A = HERE / "build" / "h1x_a" / "main.py"
H1X = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
OC_C3 = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
R40 = KSIM_DIR / "orderbook_r40" / "build" / "main.py"

# 低报价子集 12 seed（lowq_verdict.json seeds_used，spike_ticks<900）
SEEDS = [519583859, 902308231, 946703857, 964977762, 1027025959, 1073167058,
         84984751, 369579018, 691180001, 869622071, 1072483309, 1423356419]
FOLDS_R40 = [674000 + i * 159 for i in range(6)]   # 弱锚 6 fold 双席
REG_H1X_VS_R40 = 0.8333   # H1X 基线（回归检查下限）
WORKERS = 4
BUDGET_CAP = 100

EV = {}
ANOMALIES = []


def _sha(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (HERE / "evidence").mkdir(parents=True, exist_ok=True)
    (HERE / "evidence" / "h1x_a_rush.json").write_text(
        json.dumps(EV, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EV.update({
        "version": "h1x_a_rush/1.0",
        "task": "h1x_a（d29 申报校准 H1X 移植件）H1X 侧配对验证（极速快测，"
                "只测不发/绝不在线提交）",
        "objects": {
            "h1x_a": {"path": str(H1X_A), "sha256": _sha(H1X_A),
                      "manifest": "orderbook_lowq_lab/build/h1x_a/"
                                  "build_manifest.json"},
            "h1x_base": {"path": str(H1X), "sha256": _sha(H1X)}},
        "design": {
            "paired": "12 lowq seed（spike_ticks<900）双席 vs oc_c3，同 "
                      "(seed,seat,opp) 逐 unit delta=h1x_a−h1x",
            "r40_anchor": "6 fold（674000+i*159, i=0..5）双席 vs r40 弱锚，"
                          "h2h 回归检查 ≥ H1X 基线 0.8333",
            "criteria": "①配对 mean_delta>0 ②flips_neg==0 —— 两门过=PASS",
            "margin": "终局钱 farms[obs.player] 差（tm_us−tm_opp 干净口径）"},
        "registry_baseline": {"H1X_vs_r40_h2h": REG_H1X_VS_R40},
        "arms": {}, "verdict": {},
    })
    flush_evid()

    # ---- sim_bridge 认证（复用 s1form 认证缓存）----
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    auth = json.loads(auth_cache.read_text(encoding="utf-8"))
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "engine", "version")}
    auth_lite["reused_cache"] = True
    EV["gates"] = {"sim_auth": auth_lite}
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- ① 配对 vs H1X 本体（12 seed 双席 vs oc_c3）----
    rows_a = jh.run_specs(
        jh.mk_specs("h1x_a", H1X_A, OC_C3, "oc_c3", SEEDS, "paired"), run_cfg)
    rows_b = jh.run_specs(
        jh.mk_specs("h1x", H1X, OC_C3, "oc_c3", SEEDS, "paired"), run_cfg)
    pairs = jh.pairs_from(rows_b, rows_a)   # control=h1x 本体, variant=h1x_a
    ft = jh.flip_table(pairs)
    EV["arms"]["paired_vs_h1x"] = {
        "design": "同 (seed,seat,opp=oc_c3) 配对，delta=h1x_a−h1x；"
                  "control=h1x 本体",
        "flip_table": {k: v for k, v in ft.items() if k != "pairs_detail"},
        "pairs_detail": ft.get("pairs_detail"),
        "n_units_planned": 24, "n_pairs": ft.get("n"),
        "fold_h1x_a": jh.fold(rows_a), "fold_h1x_base": jh.fold(rows_b),
    }
    print("paired mean_delta=", ft.get("mean_delta"),
          "W/L/T=", ft.get("W"), ft.get("L"), ft.get("T"),
          "flips_neg=", ft.get("flips_neg"), flush=True)
    flush_evid()

    # ---- ② 弱锚 r40 6 fold 双席 ----
    rows_r = jh.run_specs(
        jh.mk_specs("h1x_a", H1X_A, R40, "r40", FOLDS_R40, "r40_anchor"),
        run_cfg)
    f_r = jh.fold(rows_r)
    h_r = f_r.get("h2h")
    EV["arms"]["r40_anchor"] = {
        "design": "6 fold 双席 vs r40 弱锚（回归检查，下限=H1X 基线 0.8333）",
        "fold": f_r, "h2h": h_r, "baseline": REG_H1X_VS_R40,
        "regression_ok": bool(isinstance(h_r, (int, float))
                              and h_r >= REG_H1X_VS_R40),
    }
    print("r40 h2h=", h_r, "baseline=", REG_H1X_VS_R40,
          "regression_ok=", EV["arms"]["r40_anchor"]["regression_ok"],
          flush=True)
    flush_evid()

    # ---- 判据 ----
    md = ft.get("mean_delta")
    fn = ft.get("flips_neg")
    c1 = bool(isinstance(md, (int, float)) and md > 0)
    c2 = bool(fn == 0)
    passed = bool(c1 and c2)
    n_pairs = ft.get("n")
    completeness = "full" if n_pairs == 24 else "partial(%s/24)" % n_pairs
    EV["criteria"] = {
        "rule": "①配对 mean_delta>0 ②flips_neg==0 —— 两门过=PASS",
        "c1_paired_delta_gt_0": {"mean_delta": md, "passed": c1},
        "c2_flips_neg_eq_0": {"flips_neg": fn, "passed": c2},
    }
    EV["verdict"] = {
        "PASS": passed,
        "verdict": "PASS" if passed else "FAIL",
        "mean_delta": md, "flips_neg": fn, "flips_pos": ft.get("flips_pos"),
        "W_L_T": [ft.get("W"), ft.get("L"), ft.get("T")],
        "n_pairs": n_pairs, "completeness": completeness,
        "r40_h2h": h_r,
        "r40_regression_ok": EV["arms"]["r40_anchor"]["regression_ok"],
        "summary": "配对 vs H1X（12 seed 双席 vs oc_c3，%s）：W-L-T=%s/%s/%s "
                   "mean_delta=%s flips_neg=%s flips_pos=%s；弱锚 r40 h2h=%s"
                   "（基线 0.8333，回归%s）；两门①delta>0 ②flips_neg=0 → %s"
                   % (completeness, ft.get("W"), ft.get("L"), ft.get("T"),
                      md, fn, ft.get("flips_pos"), h_r,
                      "OK" if EV["arms"]["r40_anchor"]["regression_ok"]
                      else "DOWN", "PASS" if passed else "FAIL"),
        "launch": "只测不发（在线提交=硬禁令）；发射由主会话执行",
    }
    EV["budget"] = {
        "cap_局次": BUDGET_CAP, "auth_缓存复用计账": 30,
        "paired_实跑": len(rows_a) + len(rows_b),
        "r40_实跑": len(rows_r),
        "unique_games_run": len(jh._ROW_CACHE),
        "total_局次": 30 + len(jh._ROW_CACHE),
    }
    EV["budget"]["within_cap"] = EV["budget"]["total_局次"] <= BUDGET_CAP
    ANOMALIES.append("harness 噪声不修不管；终局钱 farms[obs.player] 口径；"
                     "确定性不重跑（构建件已双跑过）")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", EV["verdict"]["summary"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", EV["budget"], flush=True)
    return EV


if __name__ == "__main__":
    main()
