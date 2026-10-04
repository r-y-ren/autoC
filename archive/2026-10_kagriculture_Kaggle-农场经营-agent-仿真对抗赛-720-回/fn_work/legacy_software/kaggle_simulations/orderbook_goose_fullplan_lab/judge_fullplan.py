# -*- coding: utf-8 -*-
"""judge_fullplan（fullplan lab）：goose_full vs oc_c3 配对判决 + H1 参照（不发射）。

配对口径（ab_r41/K2 净翻胜）：control=oc_c3 vs 对手 O，arm=goose_full vs 同 O，
同 seed+seat；margin=run_games banks（farms[obs.player] 干净口径）。语料=26 败局
前 8 fold + 新中性块 672000+i*101（i=0..7），fold 口径 n=16 双席。另跑 H1 参照列
（同 units），报 goose_full-vs-H1 对照。判据：净翻胜>0 ∧ flips_neg==0 ∧ 终局钱
不降 ∧ 蛋肥收入占比报告 + 头部配方对照（G/麦田/终局钱 vs 105.7k）。
sim_bridge 先认证 30/30（不过即停）；workers=2；预算 ≤400 局次。复用（不改写）
orderbook_goose_lab/judge_goose 的 econ_face/_agg_econ/ab_stats/_play 与
orderbook_r40/{judge_r23,ab_r41}。只写 orderbook_goose_fullplan_lab/。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KSIM_DIR = HERE.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))
if str(KSIM_DIR / "orderbook_goose_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_lab"))

import judge_goose as jg  # noqa: E402
import goose_fullplan as gf  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = EVID_DIR / "judge_fullplan.json"
OC3_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
GOOSE_FULL = HERE / "build" / "goose_full" / "main.py"

LOSS_SEEDS_26 = jg.LOSS_SEEDS_26
NEUTRAL_SEEDS = [672000 + i * 101 for i in range(8)]
FOLDS = ([(int(s), "loss_replay") for s in LOSS_SEEDS_26[:8]]
         + [(int(s), "neutral_672k101") for s in NEUTRAL_SEEDS])
WORKERS = 2
BUDGET_CAP_GAMES = 400


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(rel) if Path(rel).is_file() else str(KSIM_DIR / rel)
                 for rel in j23.DEFAULT_OPPONENTS]
    for p in opp_paths:
        if not Path(p).is_file():
            raise FileNotFoundError("对局件缺失: %s" % p)
    units = []
    for j, (seed, stratum) in enumerate(FOLDS):
        opp_path = opp_paths[j % len(opp_paths)]
        for seat in (0, 1):
            units.append({"seed": seed, "seat": seat, "opp_path": opp_path,
                          "opponent": Path(opp_path).parent.name + "/" + Path(opp_path).name,
                          "stratum": stratum})
    return units, opp_paths


def specs_for(rows_src, arm, cand_path):
    from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
    specs = ab._specs_for(rows_src, arm, cand_path, True)
    for spec, src in zip(specs, rows_src):
        spec["stratum"] = src["stratum"]
        spec["game_id"] = "gp-%s-%d-s%d" % (arm, int(src["seed"]), int(src["seat"]))
    return specs


def ensure_auth():
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    corpus = LOSS_SEEDS_26 + [2026092901, 2026092902, 672000, 672101]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, corpus)
    lite = {k: auth.get(k) for k in
            ("loaded", "consistency", "wall_speedup", "consistency_ok",
             "degraded", "degraded_reason", "engine", "timing", "version")}
    (EVID_DIR / "sim_auth.json").write_text(
        json.dumps(lite, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return auth


def pair_stats(ledger, var_key, ctl_key="margin_control"):
    """ab_r41/K2 净翻胜口径（成对 delta/翻胜/胜局对照）。"""
    agg = {"n": 0, "delta_sum": 0.0, "margin_control_sum": 0.0,
           "margin_var_sum": 0.0, "win_control": 0, "win_var": 0,
           "flips_pos": 0, "flips_neg": 0, "loss_recovery": 0, "loss_recovery_n": 0}
    for lu in ledger:
        v = lu.get(var_key)
        if v is None:
            continue
        mc = lu[ctl_key]
        mv = v["margin"]
        agg["n"] += 1
        agg["delta_sum"] += mv - mc
        agg["margin_control_sum"] += mc
        agg["margin_var_sum"] += mv
        wc = 1 if mc > 0 else 0
        wv = 1 if mv > 0 else 0
        agg["win_control"] += wc
        agg["win_var"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
        if lu["stratum"] == "loss_replay":
            agg["loss_recovery_n"] += 1
            if mv - mc > 0:
                agg["loss_recovery"] += 1
    n = max(1, agg["n"])
    out = {"n": agg["n"],
           "mean_delta": round(agg["delta_sum"] / n, 2),
           "mean_margin_control": round(agg["margin_control_sum"] / n, 2),
           "mean_margin_var": round(agg["margin_var_sum"] / n, 2),
           "win_rate_control": round(agg["win_control"] / n, 4),
           "win_rate_var": round(agg["win_var"] / n, 4),
           "net_flip_wins": int(agg["win_var"]) - int(agg["win_control"]),
           "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
           "loss_recovery": "%d/%d 败局 delta>0" % (agg["loss_recovery"], agg["loss_recovery_n"])}
    out["positive_arm"] = bool(out["net_flip_wins"] > 0 and out["flips_neg"] == 0)
    return out


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP_GAMES, "auth_games": 0, "control_games": 0,
              "variant_games": 0, "h1_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "judge-fullplan/1.0",
        "corpus": {"loss_folds": LOSS_SEEDS_26[:8], "neutral_folds": NEUTRAL_SEEDS,
                   "strata": "26 败局前 8 fold + 新中性 672000+i*101（i=0..7）；n=16 双席"},
        "pairs_caliber": "control=oc_c3 vs O / arm=goose_full vs 同 O（同 seed+seat）"
                         "+ H1 参照列；margin=banks[farms[obs.player]]",
    }

    auth = ensure_auth()
    budget["auth_games"] = 30
    ok = auth.get("consistency_ok")
    print("sim auth:", ok, auth.get("consistency"), flush=True)
    if not ok:
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
                               encoding="utf-8")
        return out
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    units, opp_paths = make_units()
    out["opponents"] = opp_paths
    p_ctl = jg._play(specs_for(units, "control", str(OC3_MAIN)), run_cfg)
    budget["control_games"] = len(units)
    p_var = jg._play(specs_for(units, "goose_full", str(GOOSE_FULL)), run_cfg)
    budget["variant_games"] = len(units)
    p_h1 = jg._play(specs_for(units, "h1_ref", str(H1_MAIN)), run_cfg)
    budget["h1_games"] = len(units)
    budget["total_games"] = sum(v for k, v in budget.items() if k.endswith("_games"))
    budget["within_cap"] = budget["total_games"] <= BUDGET_CAP_GAMES

    by = {}
    for tag, rows in (("ctl", p_ctl), ("var", p_var), ("h1", p_h1)):
        for r in rows:
            by.setdefault((int(r["seed"]), int(r["seat"])), {})[tag] = r
    ledger = []
    for u in units:
        k = (u["seed"], u["seat"])
        rec = by.get(k) or {}
        c, v, h = rec.get("ctl"), rec.get("var"), rec.get("h1")
        if not (c and v and h):
            continue
        if any(r.get("error") is not None or r.get("margin") is None for r in (c, v, h)):
            continue
        ledger.append({"seed": u["seed"], "seat": u["seat"], "opponent": u["opponent"],
                       "stratum": u["stratum"], "margin_control": c["margin"],
                       "var": {"margin": v["margin"], "econ": v.get("econ")},
                       "h1": {"margin": h["margin"], "econ": h.get("econ")},
                       "econ_control": c.get("econ")})
    pairs = {
        "goose_full_vs_oc_c3": pair_stats(ledger, "var"),
    }
    # goose_full vs H1：以 h1 margin 为对照
    h1_ledger = []
    for lu in ledger:
        h1_ledger.append({"seed": lu["seed"], "seat": lu["seat"], "stratum": lu["stratum"],
                          "margin_control": lu["h1"]["margin"],
                          "var": {"margin": lu["var"]["margin"]}})
    pairs["goose_full_vs_h1"] = pair_stats(h1_ledger, "var")
    oc3_vs_h1 = []
    for lu in ledger:
        oc3_vs_h1.append({"seed": lu["seed"], "seat": lu["seat"], "stratum": lu["stratum"],
                          "margin_control": lu["h1"]["margin"],
                          "var": {"margin": lu["margin_control"]}})
    pairs["oc_c3_vs_h1"] = pair_stats(oc3_vs_h1, "var")
    out["pairs"] = pairs

    var_econ = jg._agg_econ([{"econ": lu["var"]["econ"]} for lu in ledger])
    ctl_econ = jg._agg_econ([{"econ": lu["econ_control"]} for lu in ledger])
    h1_econ = jg._agg_econ([{"econ": lu["h1"]["econ"]} for lu in ledger])
    out["econ_stats"] = {
        "oc_c3": ctl_econ, "goose_full": var_econ, "h1": h1_econ,
        "terminal_money_delta_mean": (round(var_econ["terminal_money_mean"]
                                            - ctl_econ["terminal_money_mean"], 1)
                                      if var_econ["terminal_money_mean"] is not None
                                      and ctl_econ["terminal_money_mean"] is not None else None),
        "egg_fert_share": {"oc_c3": ctl_econ["egg_fert_share_mean"],
                           "goose_full": var_econ["egg_fert_share_mean"],
                           "h1": h1_econ["egg_fert_share_mean"]},
    }

    p = pairs["goose_full_vs_oc_c3"]
    e = out["econ_stats"]
    crit = {
        "net_flip_pos": bool(p["net_flip_wins"] > 0),
        "flips_neg_zero": bool(p["flips_neg"] == 0),
        "terminal_money_not_down": bool(
            e["terminal_money_delta_mean"] is not None and e["terminal_money_delta_mean"] >= 0),
        "egg_fert_share_reported": True,
    }
    out["criteria"] = {
        "rule": "净翻胜>0 ∧ flips_neg==0 ∧ 终局钱不降（goose_full vs oc_c3）∧ 蛋肥收入占比报告",
        "checks": crit,
        "all_pass": bool(all(crit.values())),
    }
    out["head_compare"] = {
        "head": {"G": "9-11（中位 10）", "WHEAT": "169（涨队配方）", "money_end": "105.7k",
                 "sample": gf.HEAD_PARAMS["sample"]},
        "goose_full_target": {"G": 10, "C": 4, "S": 2,
                              "WHEAT_plants": "163（基线不变，≈头部 169 带内）",
                              "note": "C7/G9-11/S6-8 型按 16-17 链劳动预算裁剪"},
    }
    out["verdict"] = {
        "verdict": ("PROD_ARM_CANDIDATE" if out["criteria"]["all_pass"]
                    else "NO_POSITIVE_GOOSE_ARM"),
        "positive": bool(out["criteria"]["all_pass"]),
        "budget_compliance": "局次 %d/%d（cap 合规）" % (budget["total_games"], BUDGET_CAP_GAMES),
    }
    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声不修不管（任务边界）；终局钱 farms[obs.player] 口径",
        "孪生口径为 solo gengame（对手 PASS）：牛奶/羊毛价不饱和，变体 solo 钱可低于"
        "基线；判据以配对实测（真实对手）为准——蛋吸收（log 支）在对饱和市场下占优是"
        "头部鹅漂移的经济解释（econ_model 镜像世界）",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
                           encoding="utf-8")
    (EVID_DIR / "judge_ledger.json").write_text(
        json.dumps({"units": ledger, "pairs": pairs}, ensure_ascii=False, indent=1,
                   default=str) + "\n", encoding="utf-8")
    print("verdict:", out["verdict"], flush=True)
    for k, s in pairs.items():
        print(" %s: n=%d delta=%.1f netflip=%+d flips_neg=%d" %
              (k, s["n"], s["mean_delta"], s["net_flip_wins"], s["flips_neg"]), flush=True)
    return out


if __name__ == "__main__":
    main()
