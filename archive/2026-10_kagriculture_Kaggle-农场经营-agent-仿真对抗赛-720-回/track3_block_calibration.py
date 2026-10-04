# -*- coding: utf-8 -*-
"""track3 跨块读数校准（分析35 P4：±0.06 跨块漂移教训量化）。

同一臂集（h1_base/i1/i2/i12 + r40 自镜像噪声地板）对 r40 在 3 个语料块
各 n=16 双席折叠重读，量化逐块读数漂移：
 ① 26 败局块（REPLAY_26 均匀取 16 seed）
 ② 671000 块（671000+i*23，i<16；分析34 旧中性块同构）
 ③ 672000 块（672000+i*29，i<16；分析35 新中性块同构）

读数口径=judge_iter1.fold_arm（双席折叠 h2h）+ aggregate（实现价/终局钱
farms[obs.player] 干净口径）。复用（不改写）：judge_iter1._play/fold_arm/
aggregate/clean_reads、orderbook_r40.sim_bridge（含 30/30 对照认证，
不过即回落官方引擎并在 source.degraded 留痕）。

产出：fn_docs/hybrid/results/2026-09-29-track3-calibration-raw.json（fix3 原始
数据，最终证据 2026-09-29-track3-ruler-fixes.json 的 fix3 段由此装配）。
"""
from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.join(HERE, "fn_work", "legacy_software", "kaggle_simulations")
LAB = os.path.join(KSIM, "orderbook_iter1_lab")
RESULTS = os.path.join(HERE, "fn_docs", "hybrid", "results")
if LAB not in sys.path:
    sys.path.insert(0, LAB)

import judge_iter1 as j  # noqa: E402  复用（不改写）判尺读数件

ARMS = {
    "h1_base": os.path.join(LAB, "build", "h1_base", "main.py"),
    "i1": os.path.join(LAB, "build", "i1", "main.py"),
    "i2": os.path.join(LAB, "build", "i2", "main.py"),
    "i12": os.path.join(LAB, "build", "i12", "main.py"),
    "r40_self": os.path.join(KSIM, "orderbook_r40", "build", "main.py"),
}
R40 = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
N_PER_BLOCK = 16
WORKERS = 4
REPLAY_26 = list(j.REPLAY_26)


def block_seeds():
    """3 语料块各 n=16：败局块均匀取样；中性块取前 16 个 stagger seed。"""
    return {
        "replay26_b16": [REPLAY_26[i * len(REPLAY_26) // N_PER_BLOCK]
                         for i in range(N_PER_BLOCK)],
        "neutral_671000_i23_b16": [671000 + i * 23 for i in range(N_PER_BLOCK)],
        "neutral_672000_i29_b16": [672000 + i * 29 for i in range(N_PER_BLOCK)],
    }


def make_specs(arm_main, arm, seeds, group):
    specs = []
    for seed in seeds:
        for seat in (0, 1):
            a = {"type": "python", "path": arm_main}
            b = {"type": "python", "path": R40}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "t3cal-%s-%s-%d-s%d" % (arm, group, seed, seat),
                "seed": int(seed), "kind": "pair", "arm": arm, "opp": "r40",
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


def main():
    os.chdir(LAB)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()
    blocks = block_seeds()
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "track3-block-calibration/1.0",
        "source": {
            "purpose": "分析35 P4 跨块读数校准（h1_base 对 r40 旧块 0.837 / "
                       "新中性块 0.772 的 ±0.06 漂移量化）",
            "arms": {k: os.path.relpath(v, HERE) for k, v in ARMS.items()},
            "opponent": os.path.relpath(R40, HERE),
            "blocks": blocks,
            "n_per_block": N_PER_BLOCK,
            "workers": WORKERS,
            "caliber": "双席折叠 h2h（fold_arm）；实现价/终局钱 farms[obs.player]"
                       ".money 干净口径（judge_iter1.clean_reads）",
            "reuse": "judge_iter1._play/fold_arm/aggregate（不改写）",
        },
        "rows": {},
        "drift_table": {},
        "elapsed_s": 0.0,
    }
    # ---- sim_bridge 对照认证 30/30（不过即回落官方引擎，不中止校准） ----
    # 语料=26 败局全量+4 构造 seed=30 恰满 min_checked（少于 30 会误判降级）
    auth_corpus = REPLAY_26 + [2026092901, 2026092902, 2026092903,
                               2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": os.path.join(RESULTS,
                                     "2026-09-29-track3-sim-auth-record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "version")}
    out["source"]["sim_auth"] = auth_lite
    print("sim auth:", auth_lite.get("consistency_ok"), flush=True)
    if auth_lite.get("consistency_ok"):
        run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    else:
        run_cfg = {"engine": "official", "workers": WORKERS}
        out["source"]["degraded"] = "sim_bridge 认证未过，回落官方引擎重读"
    # ---- 5 臂 × 3 块 × n=16 双席重读 ----
    for arm, main_path in ARMS.items():
        for group, seeds in blocks.items():
            specs = make_specs(main_path, arm, seeds, group)
            t2 = time.perf_counter()
            rows, engines = j._play(specs, run_cfg)
            agg = j.aggregate(rows, engines)
            key = "%s__%s" % (arm, group)
            out["rows"][key] = {
                "arm": arm, "block": group, "n_folds": N_PER_BLOCK,
                "n_games": agg["n_games"],
                "wins": agg["wins"], "losses": agg["losses"],
                "ties": agg["ties"], "h2h": agg["h2h"],
                "mean_margin": agg["mean_margin"],
                "realized_px_median": agg["ours"]["realized_px_median"],
                "terminal_money_median": agg["ours"]["terminal_money_median"],
                "stranding_median": agg["ours"]["stranding_median"],
                "fold_margins": agg["fold_margins"],
                "n_error_games": agg["n_error_games"],
                "engines": engines,
                "elapsed_s": round(time.perf_counter() - t2, 1),
            }
            print(key, agg["h2h"], agg["wins"], agg["losses"], agg["ties"],
                  agg["mean_margin"], "px", agg["ours"]["realized_px_median"],
                  "tm", agg["ours"]["terminal_money_median"],
                  out["rows"][key]["elapsed_s"], "s", flush=True)
    # ---- 逐块漂移表 ----
    for arm in ARMS:
        by_block = {}
        for group in blocks:
            r = out["rows"]["%s__%s" % (arm, group)]
            by_block[group] = {"h2h": r["h2h"],
                               "mean_margin": r["mean_margin"],
                               "realized_px_median": r["realized_px_median"],
                               "terminal_money_median":
                                   r["terminal_money_median"]}
        h2hs = [v["h2h"] for v in by_block.values()
                if isinstance(v["h2h"], (int, float))]
        mms = [v["mean_margin"] for v in by_block.values()
               if isinstance(v["mean_margin"], (int, float))]
        out["drift_table"][arm] = {
            "by_block": by_block,
            "h2h_spread": round(max(h2hs) - min(h2hs), 4) if h2hs else None,
            "margin_spread": round(max(mms) - min(mms), 1) if mms else None,
        }
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    out["cross_block_rule"] = {
        "same_block_only": "跨实验/跨臂比较只在同块读数之间做（同块才比）",
        "cross_block_weighted": "跨块必须并报逐块读数+folds 加权合并值"
                                "（Σfold_margin/Σn，不得只报单一 headline）",
        "noise_floor": "r40_self 逐块 h2h≈0.5 为块噪声地板；臂间差须超"
                       "双侧块漂移带才可判机制差",
    }
    path = os.path.join(RESULTS, "2026-09-29-track3-calibration-raw.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1, default=str)
        fh.write("\n")
    print("DONE", out["elapsed_s"], "s ->", path, flush=True)
    return out


if __name__ == "__main__":
    main()
