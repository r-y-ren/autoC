# -*- coding: utf-8 -*-
"""judge_racegap2：slot 臂 v2 增量判决（对齐保序+越非卖单抢先；不发射不提交）。

v1（碰撞项节拍重排）经单局诊断破序致负（同拍同序 38/51 被重排打破：赢小单
失大单）；v2 改弱支配形态：SELL 相对序不动（对齐=对手稳态单序先验）+自由 SELL
越非卖单冒泡前置（抢先=我单插其单前）。增量口径：
- 复跑 drop_half 主判 32 局（配对/足迹/实现价需 base 行）+ slot v2 主判 32 局
  + slot v2 同族 24 局；同族基线=run1 记录（引擎确定性，重证零增益）。
- slot v2 门禁四门；预算 4+32+32+24=92 局次（累计 236+92=328 ≤350）。
证据并入 fn_docs/hybrid/results/2026-09-30-race-gap.json（v1 移 iterations 节）。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
sys.path.insert(0, str(MODULE_DIR))

import build_racegap as B  # noqa: E402
import judge_racegap as J1  # noqa: E402

JM = J1.JM
EVID_PATH = J1.EVID_PATH

os.chdir(KSIM_DIR)
from orderbook_r40 import sim_bridge as sb  # noqa: E402

ev = json.loads(EVID_PATH.read_text(encoding="utf-8"))
budget = ev["budget"]
budget["run2"] = {"cap_note": "slot v2 增量 92 局次（gates 4 + 主判 32+32 + 同族 24）",
                  "run2_局次": 0}

t0 = time.perf_counter()
auth = sb.sim_bridge({"n_games": 3, "min_checked": 3,
                      "record_path": str(MODULE_DIR / "evidence"
                                         / "sim_auth_record.json")},
                     [2026093101, 2026093102, 2026093103])
if not auth.get("consistency_ok"):
    ev["verdict"] = {"aborted": "run2 sim_bridge 认证未过"}
    EVID_PATH.write_text(json.dumps(ev, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")
    raise SystemExit("ABORT auth")
run_cfg = {"engine": "auto", "bridge": auth, "workers": J1.WORKERS}

# ---- 1) slot v2 门禁四门 ----
g2 = J1.run_gates(B.OUT_DIR / "slot", "slot")
ev.setdefault("gates_run2", {})["slot_v2"] = g2
budget["run2"]["gates_局次"] = 4
budget["run2"]["run2_局次"] += 4
print("gates slot v2:", g2.get("overall"), flush=True)

# ---- 2) 主判：drop_half 32 + slot v2 32 ----
units_main = J1.make_units(J1.FOLDS_MAIN, "main")
base_rows = J1.play_arm("drop_half", J1.DROP_HALF_MAIN, units_main, run_cfg,
                        budget, "run2_局次")
slot_rows = J1.play_arm("slot_v2", J1.ARM_MAIN["slot"], units_main, run_cfg,
                        budget, "run2_局次")
base_map = J1.rows_by_key(base_rows)
slot_map = J1.rows_by_key(slot_rows)

# ---- 3) 足迹审计（slot v2 vs drop_half） ----
fp2 = J1.footprint_audit(base_map, {"slot": slot_map}, units_main)
ev["footprint_audit"]["slot_v2"] = fp2["slot"]
ev["footprint_audit"]["passed_v2"] = all(
    v.get("passed") for k, v in ev["footprint_audit"].items()
    if isinstance(v, dict) and "passed" in v)

# ---- 4) 配对 + 实现价 + 窗 ----
ps = JM.pair_stats(base_map, slot_map, units_main)
rp = JM.realized_paired(base_map, slot_map, units_main)
win = JM.window_paired(base_map, slot_map, units_main)
ev["pairs"]["arms"]["slot_v2"] = {
    "n_units": len(slot_rows),
    "margin_mean": round(sum(r["margin"] for r in slot_rows
                             if r.get("margin") is not None)
                         / max(1, len(slot_rows)), 2),
    "terminal_money_mean": JM.end_agg(slot_rows)["terminal_money_mean"]}
ev["pairs"]["main_slot_v2_vs_drop_half"] = dict(
    J1.lite_pair(ps), rows_lite=ps.get("rows_lite"))
ev["pairs"]["realized_slot"] = {
    "nonneg_both": rp.get("nonneg_both"),
    "all_mean_delta": rp.get("all", {}).get("mean_delta"),
    "milk_mean_delta": rp.get("milk", {}).get("mean_delta")}
ev["pairs"]["window_slot"] = {
    "d14_27_fill_total_delta": win.get("fill_total", {}).get("mean_delta")}

# ---- 5) 同族专组（slot v2 24 局；基线=run1 记录） ----
units_family = J1.make_family_units()
fam_slot_rows = J1.play_arm("slot_v2#fam", J1.ARM_MAIN["slot"], units_family,
                            run_cfg, budget, "run2_局次")
fam_slot_map = J1.rows_by_key(fam_slot_rows)
fam_base_rates = ev["family_group"]["rates"]["drop_half"]
fam_gap_rates = ev["family_group"]["rates"]["gap"]
rates = {"drop_half": fam_base_rates, "gap": fam_gap_rates}
per = {}
for mirror in J1.MIRRORS:
    rows, deltas = [], []
    for u in units_family:
        if u["opponent"] != mirror:
            continue
        r = fam_slot_map.get((u["seed"], u["seat"]))
        if r and r.get("margin") is not None:
            rows.append(float(r["margin"]))
    w = sum(1 for m in rows if m > 0)
    t = sum(1 for m in rows if m == 0)
    n = max(1, len(rows))
    per[mirror] = {"n": len(rows), "W": w, "T": t, "L": len(rows) - w - t,
                   "h2h": round((w + 0.5 * t) / n, 4),
                   "margin_mean": round(sum(rows) / n, 2) if rows else None}
n = sum(per[m]["n"] for m in J1.MIRRORS)
w = sum(per[m]["W"] for m in J1.MIRRORS)
t = sum(per[m]["T"] for m in J1.MIRRORS)
rates["slot"] = {"per_mirror": per,
                 "aggregate": {"n": n, "W": w, "T": t, "L": n - w - t,
                               "h2h": round((w + 0.5 * t) / max(1, n), 4)}}
ev["family_group"]["rates"] = rates
ev["family_group"]["run2_note"] = ("slot v2 重跑；drop_half/gap 基线沿 run1 "
                                   "记录（引擎确定性）")

# ---- 6) v1 迁 iterations + 判据重算 ----
v1_fam = ev["family_group"]["rates"].get("slot")
ev.setdefault("iterations", {})["slot_v1_beat_reorder"] = {
    "mechanism": ("碰撞项节拍重排（v1）：非洗仓可购品 SELL 前置+预测同拍碰撞项"
                  "先行（正流出拍间隔中位数整除=其强拍；强度降序=其单序）"),
    "diagnosis": (
        "单局诊断（seed 1825501814 vs tetsutani）：全部差异拍均为 SELL-SELL "
        "换序（基底卖单已居列表最前、越非卖单无空间）；同拍双多卖 51 拍中 38 拍"
        "我方单序与对手逐字同（同族 tape 同序=稳定可预测），v1 重排打破对齐→"
        "赢小单失大单（CARROT −406/FERT −172/STRAW 逆向换序）；对手列序不可见、"
        "节拍强度代理误排其先行品。结论：同拍槽位杠杆在基底已饱和（X1 并最早槽+"
        "同族同序），序内重排为近零和且预测误差为负期望"),
    "pairs_main": ev["pairs"].get("main_slot_vs_drop_half"),
    "family": v1_fam,
    "criteria_run1": ev.get("criteria", {}).get("slot"),
    "footprint_run1": ev["footprint_audit"].get("slot"),
}
ev["pairs"].pop("main_slot_vs_drop_half", None)
ev["footprint_audit"].pop("slot", None)

fam_arm = rates["slot"]["aggregate"]
fam_base = rates["drop_half"]["aggregate"]
c_flip = (ps.get("net_flip_wins") or 0) > 0
c_neg = ps.get("flips_neg") == 0
c_fam = (fam_arm.get("h2h") or 0) >= (fam_base.get("h2h") or 0)
c_real = bool(rp.get("nonneg_both"))
ev["criteria"]["slot"] = {
    "净翻胜>0": {"net_flip_wins": ps.get("net_flip_wins"), "passed": c_flip},
    "flips_neg==0": {"flips_neg": ps.get("flips_neg"), "passed": c_neg},
    "同族胜率≥drop_half": {"arm_h2h": fam_arm.get("h2h"),
                           "base_h2h": fam_base.get("h2h"), "passed": c_fam},
    "实现价非负": {"nonneg_both": rp.get("nonneg_both"),
                   "all_mean_delta": rp.get("all", {}).get("mean_delta"),
                   "milk_mean_delta": rp.get("milk", {}).get("mean_delta"),
                   "passed": c_real},
    "criteria_passed": bool(c_flip and c_neg and c_fam and c_real)}

gap_c = ev["criteria"]["gap"]
ev["verdict"] = {
    "positive_arms": [a for a in ("gap", "slot")
                      if ev["criteria"][a]["criteria_passed"]],
    "criteria_by_arm": {"gap": gap_c["criteria_passed"],
                        "slot": ev["criteria"]["slot"]["criteria_passed"]},
    "gates_passed": bool(ev["gates"].get("gap", {}).get("overall")
                         and g2.get("overall")),
    "footprint_gate_passed": bool(ev["footprint_audit"].get("passed_v2")),
    "note": ("判决先行·不发射不提交；slot=保序 v2（v1 重排见 iterations）；"
             "同族胜率口径=游戏级 (W+0.5T)/n"),
}
budget["judgment_局次"] = budget.get("judgment_局次", 0) + 0
budget["run2"]["run2_局次"] += len(base_rows) + len(slot_rows) + len(fam_slot_rows)
budget["run2"]["elapsed_s"] = round(time.perf_counter() - t0, 1)
budget["total_局次"] = 236 + budget["run2"]["run2_局次"]
ev["anomaly"] = list(J1.ANOMALIES)
ev["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
EVID_PATH.write_text(json.dumps(ev, ensure_ascii=False, indent=1,
                                default=str) + "\n", encoding="utf-8")
print(json.dumps(ev["verdict"], ensure_ascii=False), flush=True)
print("slot v2 criteria:", json.dumps(ev["criteria"]["slot"],
                                      ensure_ascii=False), flush=True)
