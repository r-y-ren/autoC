# -*- coding: utf-8 -*-
"""collect_rhythm：rhythm_stats 补采（逐日可售产出量对照摘要 + %4 相位核对）。

judge_rhythm 首跑用 ab_r41 批口丢弃了轨迹 sink（rhythm_stats 空）；本脚本以
judge_rhythm._run_chunk（自批口，保留轨迹）对 **6 fold 子集**（3 败局+3 中性）
× 双席重跑 control + 全部 kept 变体（6 臂 × 12 局=72 局次；预算 30+144+72=246
≤300），把 rhythm_stats 与预算回写 fn_docs/hybrid/results/2026-09-29-prod-
rhythm.json（判据/pairs 不动——同种子确定性，margin 口径不变）。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

import judge_rhythm as jr  # noqa: E402


def main():
    os.chdir(jr.KSIM_DIR)
    t0 = time.perf_counter()
    ev_path = jr.EVID_PATH
    ev = json.loads(Path(ev_path).read_text(encoding="utf-8"))
    kept = [vid for vid, v in (ev.get("variants") or {}).items()
            if v.get("kept")]

    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record2.json")},
        list(jr.REPLAY_26) + [2026092905, 2026092906, 2026092907,
                              2026092908])
    if not auth.get("consistency_ok"):
        print("ABORT: sim auth failed", flush=True)
        return None
    run_cfg = {"engine": "auto", "bridge": auth, "workers": jr.WORKERS}

    folds = jr.LOSS_FOLDS[:3] + jr.NEUTRAL_FOLDS[:3]   # 6 fold 子集
    opp_paths = [str(jr.KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(folds):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(jr.LOSS_FOLDS) else
                   "neutral_672000_i73")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum})

    ev.setdefault("budget", {})["rhythm_局次"] = 0
    arms = {"control": str(jr.rv.H1_MAIN)}
    for vid in kept:
        arms[vid] = ev["variants"][vid]["main_path"]
    out = {"_subset": {"loss_folds": jr.LOSS_FOLDS[:3],
                       "neutral_folds": jr.NEUTRAL_FOLDS[:3],
                       "n_folds": 6, "double_seat_games_per_arm": 12}}
    for arm, path in arms.items():
        rows = jr._play(units, arm, path, run_cfg)
        ev["budget"]["rhythm_局次"] += len(rows)
        agg = jr.rhythm_agg(rows)
        if arm == "control":
            agg["season_sellable_mean_control"] = agg.get("season_sellable_mean")
        else:
            agg["control_season"] = out["control"].get("season_sellable_mean")
        out[arm] = agg
        print(arm, "season", agg.get("season_sellable_mean"),
              "ph4", agg.get("harvest_phase4_share"), flush=True)

    ev["rhythm_stats"] = out
    ev["budget"]["total_局次"] = (ev["budget"].get("auth_局次", 0)
                                 + ev["budget"].get("judgment_局次", 0)
                                 + ev["budget"]["rhythm_局次"])
    ev["budget"]["within_cap"] = bool(ev["budget"]["total_局次"] <= 300)
    ev["rhythm_stats_elapsed_s"] = round(time.perf_counter() - t0, 1)
    ev.setdefault("anomaly", []).append(
        "rhythm_stats=6 fold 子集轨迹补采（首跑批口丢 sink）；判据/pairs 沿首跑")
    Path(ev_path).write_text(json.dumps(ev, ensure_ascii=False, indent=1,
                                        default=str) + "\n", encoding="utf-8")
    print("DONE rhythm", ev["budget"], flush=True)
    return ev


if __name__ == "__main__":
    main()
