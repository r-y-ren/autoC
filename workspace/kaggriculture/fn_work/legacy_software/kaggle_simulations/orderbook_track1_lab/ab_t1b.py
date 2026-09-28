# -*- coding: utf-8 -*-
"""ab_t1b（track1 B）：产线 mix 变体 vs H1 原版 配对因果 A/B（不发射）。

责任口径（任务 track1-B）：H1 优势=产出维度（组 J 定向）假设检验——产线结构
（畜群配比/作物配比）变体有无正翻胜。判据：**变体 vs H1 原版配对**（26 败局+
新中性块 672000+i*41，n=16 双席/变体）：
- 配对口径（ab_r41/K2 净翻胜定义）：control=H1 原版 vs 对手 O，arm=变体 vs
  同一 O，同 seed+seat 配对；margin=farms[our].money−farms[opp].money（终局
  钱 farms[obs.player] 干净口径，run_games banks 同源）；
- 净翻胜>0 的变体为正臂（net_flip_wins=win_variant−win_control）；
- **胜局对照不翻负**：control 胜局（margin_control>0）单元中 variant margin<0
  的翻负数（guard，记数并报）。

预算口径：≤300 局次（game 口径；fold 口径=games/2 同报）。语料配对=16 双席
fold/变体（8 败局回放 fold + 8 新中性 fold 672000+i*41 i=0..7；fold 口径 n=16
双席/变体）；对手 j23.DEFAULT_OPPONENTS 轮转。control 32 局共享；每变体 32 局。
复用（不改写）：ab_r41._ab_play_batch/_specs_for/_agg + judge_r23 +
sim_bridge + tape_variants（变体构建件）。只写 orderbook_track1_lab/。
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

from orderbook_r40 import ab_r41 as ab  # noqa: E402
from orderbook_r40 import judge_r23 as j23  # noqa: E402
from orderbook_iterk_lab import ab_k2 as k2  # noqa: E402
import tape_variants as tv  # noqa: E402

RECORD_VERSION = "ab-t1b/1.0"
H1_MAIN = k2.H1_MAIN
EVID_DIR = MODULE_DIR / "evidence"
LEDGER_PATH = EVID_DIR / "ab_t1b_ledger_realrun.json"
WORKERS = 2
BUDGET_CAP_GAMES = 300

# 语料：26 败局回放（前 8 fold，canonical 序）+ 新中性块 672000+i*41（n=8）
LOSS_SEEDS_26 = [
    1825501814, 2013941152, 786146079, 1883261866,
    963182245, 240876256, 1705553586, 2009279466,
    161402123, 435866961, 841473039, 1388158282,
    1647385154, 671940665, 219073637, 1439493993,
    1360429471, 671494671, 1900972921, 973657130,
    1911990026, 1918725083, 176568822, 427304807,
    720683523, 906608145,
]
NEUTRAL_N = 8
NEUTRAL_SEEDS = [672000 + i * 41 for i in range(NEUTRAL_N)]


def run_prod_ab_t1b(config: dict = None) -> dict:
    """B 编排：control 共享 + 各变体配对（同 seed+seat）。"""
    cfg = dict(config) if isinstance(config, dict) else {}
    workers = int(cfg.get("workers", WORKERS))
    opponents = list(cfg.get("opponents") or j23.DEFAULT_OPPONENTS)
    opp_paths = [str(rel) if Path(rel).is_file()
                 else str(KSIM_DIR / rel) for rel in opponents]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)

    main_text = H1_MAIN.read_text(encoding="utf-8")
    pkg_base = tv.rs._decode_routes(main_text)

    # 变体构建（tape_variants）+ feasibility 孪生（审计件已有则复用口径）
    audit_path = EVID_DIR / "tape_variants_audit.json"
    audit = json.loads(audit_path.read_text(encoding="utf-8")) \
        if audit_path.is_file() else {}
    # 时点变体方向=预筛择向（tape_variants.main 会写；此处复原）
    for op, vid in (("BUY_LAND", "land_shift"), ("HIRE", "hire_shift")):
        d, _rows = tv._pick_delta(audit.get("timing_prescreen") or [], op)
        if d is not None:
            tv.VARIANTS[vid]["delta"] = int(d)
    kept = [vid for vid, v in (audit.get("variants") or {}).items()
            if v.get("kept")]
    if not kept:
        raise RuntimeError("无 feasibility 通过的变体（违规全弃）")
    # 预算：32 control + 32×k ≤ cap → k ≤ (cap−32)//32
    k_max = max(0, (BUDGET_CAP_GAMES - 32) // 32)
    kept = kept[:k_max]
    built = {}
    for vid in kept:
        b = tv.build_variant(vid, pkg_base, main_text)
        p = tv.BUILD_DIR / ("variant_%s_main.py" % vid)
        built[vid] = {"path": str(p), "main_text": b["main_text"],
                      "stats": b["stats"]}

    # 单元计划：16 fold × 双席；对手按 fold 序轮转
    folds = ([(int(s), "loss_replay") for s in LOSS_SEEDS_26[:8]] +
             [(int(s), "neutral_672k41") for s in NEUTRAL_SEEDS])
    units = []
    for j, (seed, stratum) in enumerate(folds):
        opp_path = opp_paths[j % len(opp_paths)]
        for seat in (0, 1):
            units.append({"seed": seed, "seat": seat,
                          "opp_path": opp_path,
                          "opponent": Path(opp_path).parent.name,
                          "stratum": stratum})
    run_cfg = {"engine": cfg.get("engine", "auto"), "workers": workers}
    if cfg.get("bridge") is not None:
        run_cfg["bridge"] = cfg["bridge"]
    t0 = time.perf_counter()

    # control+trace（face/pair/基线）
    p1 = ab._ab_play_batch(
        ab._specs_for(units, "control", str(H1_MAIN), True), run_cfg)
    by_key = {(int(r["seed"]), int(r["seat"])): r for r in p1}

    # 各变体配对
    var_rows = {}
    var_games = 0
    for vid in kept:
        rows = ab._ab_play_batch(
            ab._specs_for(units, vid, built[vid]["path"], False), run_cfg)
        var_games += len(units)
        var_rows[vid] = {(int(r["seed"]), int(r["seat"])): r for r in rows}

    # 账本+聚合
    ledger_units = []
    for u in units:
        r1 = by_key.get((u["seed"], u["seat"]))
        if r1 is None or r1.get("error") is not None or \
                r1.get("margin") is None:
            continue
        rec = {"seed": u["seed"], "seat": u["seat"],
               "opponent": u["opponent"], "stratum": u["stratum"],
               "face": r1.get("face"), "pair": r1.get("pair"),
               "margin_control": r1["margin"], "variants": {}}
        for vid in kept:
            r2 = var_rows[vid].get((u["seed"], u["seat"]))
            if r2 is None or r2.get("error") is not None or \
                    r2.get("margin") is None:
                continue
            rec["variants"][vid] = {"margin_variant": r2["margin"],
                                    "delta": r2["margin"] - r1["margin"]}
        if rec["variants"]:
            ledger_units.append(rec)

    stats = {}
    for vid in kept:
        agg = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
               "margin_variant_sum": 0.0, "win_control": 0,
               "win_variant": 0, "flips_pos": 0, "flips_neg": 0,
               "loss_recovery": 0, "loss_recovery_n": 0}
        for lu in ledger_units:
            v = lu["variants"].get(vid)
            if v is None:
                continue
            agg["n"] += 1
            agg["delta_sum"] += v["delta"]
            agg["margin_control_sum"] += lu["margin_control"]
            agg["margin_variant_sum"] += v["margin_variant"]
            wc = 1 if lu["margin_control"] > 0 else 0
            wv = 1 if v["margin_variant"] > 0 else 0
            agg["win_control"] += wc
            agg["win_variant"] += wv
            if wv and not wc:
                agg["flips_pos"] += 1
            if wc and not wv:
                agg["flips_neg"] += 1
            if lu["stratum"] == "loss_replay":
                agg["loss_recovery_n"] += 1
                if v["delta"] > 0:
                    agg["loss_recovery"] += 1
        out = ab._agg(agg)
        out["net_flip_wins"] = int(agg["win_variant"]) - int(agg["win_control"])
        out["flips_pos"] = agg["flips_pos"]
        out["flips_neg"] = agg["flips_neg"]          # 胜局对照不翻负 记数
        out["control_win_guard_ok"] = agg["flips_neg"] == 0
        out["loss_recovery"] = "%d/%d 败局 delta>0" % (
            agg["loss_recovery"], agg["loss_recovery_n"])
        out["positive_arm"] = bool(out["net_flip_wins"] > 0
                                   and out["control_win_guard_ok"])
        out["spec"] = (audit.get("variants") or {}).get(vid, {}).get("spec")
        stats[vid] = out

    positive = [vid for vid, s in stats.items() if s["positive_arm"]]
    verdict = {
        "criterion": "净翻胜>0 的变体为正臂；胜局对照不翻负（flips_neg==0）",
        "positive_variants": positive,
        "verdict": ("PROD_ARM_CANDIDATE: %s" % positive) if positive
        else "NO_POSITIVE_PROD_ARM（无正翻胜产线变体）",
    }
    games = {"control": len(units), "variants": var_games,
             "total": len(units) + var_games, "cap": BUDGET_CAP_GAMES}
    ledger = {
        "version": RECORD_VERSION,
        "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        "config": {"workers": workers, "opponents": opp_paths,
                   "corpus": {"loss_folds": LOSS_SEEDS_26[:8],
                              "neutral_folds": NEUTRAL_SEEDS,
                              "strata": "26 败局回放（前 8 fold）+ 新中性块 "
                                        "672000+i*41（n=8）；双席/变体 n=16 fold"},
                   "variants": kept,
                   "main_sha": k2._sha(main_text),
                   "terminal_money_caliber":
                       "farms[obs.player].money（run_games banks）"},
        "games": games,
        "games_folds": {"folds_total": games["total"] // 2,
                        "per_variant_folds": 16},
        "n_units_planned": len(units),
        "n_units_paired": len(ledger_units),
        "units": ledger_units,
        "variant_stats": stats,
        "verdict": verdict,
        "elapsed_s": round(time.perf_counter() - t0, 2),
    }
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1)
                           + "\n", encoding="utf-8")
    ledger["ledger_path"] = str(LEDGER_PATH)
    return {"ledger": ledger, "variant_stats": stats, "verdict": verdict,
            "games": games}


def main():
    os.chdir(KSIM_DIR)
    from orderbook_track1_lab import ab_t1a as t1a  # noqa: WPS433
    auth = t1a.ensure_auth()
    print("auth:", auth.get("consistency"), auth.get("consistency_ok"),
          flush=True)
    if not auth.get("consistency_ok"):
        print("ABORT: sim_bridge 对照认证未过 30/30", flush=True)
        return {"aborted": "sim_bridge 对照认证未过 30/30"}
    res = run_prod_ab_t1b({"workers": WORKERS, "engine": "auto",
                           "bridge": auth})
    print("B verdict:", res["verdict"], flush=True)
    print("B games:", res["games"], flush=True)
    for vid, s in res["variant_stats"].items():
        print("  %s: n=%d delta=%.1f netflip=%+d flips_neg=%d %s"
              % (vid, s["n"], s["mean_delta"], s["net_flip_wins"],
                 s["flips_neg"], s["loss_recovery"]), flush=True)
    return res


if __name__ == "__main__":
    main()
