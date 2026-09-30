# -*- coding: utf-8 -*-
"""judge_additive（goose_add lab）：goose_add vs oc_c3 配对判决 + H1 参照（不发射）。

配对口径（ab_r41/K2 净翻胜）：control=oc_c3 vs 对手 O，arm=goose_add vs 同 O，
同 seed+seat；margin=run_games banks（farms[obs.player] 干净口径）。语料=26 败局
前 8 fold + 新中性块 672000+i*109（i=0..7），fold 口径 n=16 双席。另跑 H1 参照列。
判据：净翻胜>0 ∧ flips_neg==0 ∧ 终局钱不降 ∧ **MILK/WOOL 供给零回撤**（逐品供给量
≥基线；磁带逐路由+配对局逐品双口径）∧ 蛋肥占比/终局钱 vs 头部 105.7k 对照。
sim_bridge 先认证 30/30（不过即停）；workers=2；预算 ≤400 局次。
复用（不改写）：orderbook_goose_lab/judge_goose 的 econ_face/_agg_econ/_play 与
orderbook_r40/{judge_r23,ab_r41,sim_bridge}。只写 orderbook_goose_add_lab/ 与
fn_docs/hybrid/results/2026-09-29-goose-additive.json（任务指定证据路径）。
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
if str(KSIM_DIR / "orderbook_goose_fullplan_lab") not in sys.path:
    sys.path.insert(0, str(KSIM_DIR / "orderbook_goose_fullplan_lab"))

import judge_goose as jg  # noqa: E402
import judge_fullplan as jf  # noqa: E402  （pair_stats 复用）
import goose_additive as ga  # noqa: E402

EVID_DIR = HERE / "evidence"
RESULT_PATH = (KSIM_DIR.parents[2] / "fn_docs" / "hybrid" / "results"
               / "2026-09-29-goose-additive.json")
OC3_MAIN = KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3" / "main.py"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
GOOSE_ADD = HERE / "build" / "goose_add" / "main.py"

LOSS_SEEDS_26 = jg.LOSS_SEEDS_26
NEUTRAL_SEEDS = [672000 + i * 109 for i in range(8)]
FOLDS = ([(int(s), "loss_replay") for s in LOSS_SEEDS_26[:8]]
         + [(int(s), "neutral_672k109") for s in NEUTRAL_SEEDS])
WORKERS = 2
BUDGET_CAP_GAMES = 400


# ------------------------------------------------------------ 经济面+逐品供给 --
def econ_face_ext(sink):
    """jg.econ_face 同口径 + 逐品挂单量（供给零回撤的游戏侧验证面）。"""
    e = jg.econ_face(sink)
    qty = {}
    for step, obs, act in (sink or []):
        if not isinstance(obs, dict) or not isinstance(act, dict):
            continue
        for cmd in (act.get("market") or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 and str(cmd[0]) == "SELL":
                q = qty.get(str(cmd[1]), 0.0)
                try:
                    qty[str(cmd[1])] = q + float(cmd[2])
                except (TypeError, ValueError):
                    pass
    e["sell_qty"] = {k: round(v, 1) for k, v in sorted(qty.items())}
    return e


def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = j23._build_agents(spec)
            games.append({"seed": int(spec["seed"]), "agents": agents})
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, {"build_error": repr(exc)[:120]}))
            continue
        metas.append((spec, sinks))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "econ": {}}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    try:
                        row["econ"] = econ_face_ext(sink)
                    except Exception as exc:
                        row["econ_error"] = repr(exc)[:100]
        out.append(row)
    return out


def _play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


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
        spec["game_id"] = "ga-%s-%d-s%d" % (arm, int(src["seed"]), int(src["seat"]))
    return specs


def ensure_auth():
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    corpus = LOSS_SEEDS_26 + [2026092901, 2026092902, 672000, 672109]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(EVID_DIR / "sim_auth_record.json")}, corpus)
    lite = {k: auth.get(k) for k in
            ("loaded", "consistency", "wall_speedup", "consistency_ok",
             "degraded", "degraded_reason", "engine", "timing", "version")}
    (EVID_DIR / "sim_auth.json").write_text(
        json.dumps(lite, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    return auth


def supply_check_games(ledger):
    """配对局逐品挂单量：变体 ≥ 基线（同 seed+seat 配对）；MILK/WOOL 单列。"""
    items = ["MILK", "WOOL", "WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON",
             "FERTILIZER", "EGG"]
    agg = {it: {"base_sum": 0.0, "var_sum": 0.0, "n_base": 0, "n_var": 0,
                "pairs_var_down": 0} for it in items}
    for lu in ledger:
        qb = (lu.get("econ_control") or {}).get("sell_qty") or {}
        qv = (lu.get("var", {}).get("econ") or {}).get("sell_qty") or {}
        for it in items:
            b, v = float(qb.get(it, 0.0)), float(qv.get(it, 0.0))
            if it in qb:
                agg[it]["base_sum"] += b
                agg[it]["n_base"] += 1
            if it in qv:
                agg[it]["var_sum"] += v
                agg[it]["n_var"] += 1
            if v + 1e-9 < b:
                agg[it]["pairs_var_down"] += 1
    out = {}
    for it in items:
        a = agg[it]
        out[it] = {"base_mean_qty": round(a["base_sum"] / max(1, a["n_base"]), 2),
                   "var_mean_qty": round(a["var_sum"] / max(1, a["n_var"]), 2),
                   "pairs_var_down": a["pairs_var_down"],
                   "zero_withdrawal": bool(a["var_sum"] + 1e-9 >= a["base_sum"])}
    out["milk_wool_ok"] = bool(out["MILK"]["zero_withdrawal"] and out["WOOL"]["zero_withdrawal"])
    out["all_items_ok"] = all(out[it]["zero_withdrawal"] for it in items)
    return out


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    budget = {"cap_局次": BUDGET_CAP_GAMES, "auth_games": 0, "control_games": 0,
              "variant_games": 0, "h1_games": 0}
    build = json.load(open(EVID_DIR / "goose_add_build.json"))
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": "goose-additive-evidence/1.0",
        "task": "B4d 鹅线加法扩栏版（26 头级、保留牛羊、劳动链合成扩出）实建判决；不发射/不提交",
        "corpus": {"loss_folds": LOSS_SEEDS_26[:8], "neutral_folds": NEUTRAL_SEEDS,
                   "strata": "26 败局前 8 fold + 新中性 672000+i*109（i=0..7）；n=16 双席"},
        "pairs_caliber": "control=oc_c3 vs O / arm=goose_add vs 同 O（同 seed+seat）"
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
    p_ctl = _play(specs_for(units, "control", str(OC3_MAIN)), run_cfg)
    budget["control_games"] = len(units)
    p_var = _play(specs_for(units, "goose_add", str(GOOSE_ADD)), run_cfg)
    budget["variant_games"] = len(units)
    p_h1 = _play(specs_for(units, "h1_ref", str(H1_MAIN)), run_cfg)
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
    pairs = {"goose_add_vs_oc_c3": jf.pair_stats(ledger, "var")}
    h1_ledger = [{"seed": lu["seed"], "seat": lu["seat"], "stratum": lu["stratum"],
                  "margin_control": lu["h1"]["margin"],
                  "var": {"margin": lu["var"]["margin"]}} for lu in ledger]
    pairs["goose_add_vs_h1"] = jf.pair_stats(h1_ledger, "var")
    oc3_vs_h1 = [{"seed": lu["seed"], "seat": lu["seat"], "stratum": lu["stratum"],
                  "margin_control": lu["h1"]["margin"],
                  "var": {"margin": lu["margin_control"]}} for lu in ledger]
    pairs["oc_c3_vs_h1"] = jf.pair_stats(oc3_vs_h1, "var")
    out["pairs"] = pairs

    var_econ = jg._agg_econ([{"econ": lu["var"]["econ"]} for lu in ledger])
    ctl_econ = jg._agg_econ([{"econ": lu["econ_control"]} for lu in ledger])
    h1_econ = jg._agg_econ([{"econ": lu["h1"]["econ"]} for lu in ledger])
    out["econ_stats"] = {
        "oc_c3": ctl_econ, "goose_add": var_econ, "h1": h1_econ,
        "terminal_money_delta_mean": (round(var_econ["terminal_money_mean"]
                                            - ctl_econ["terminal_money_mean"], 1)
                                      if var_econ["terminal_money_mean"] is not None
                                      and ctl_econ["terminal_money_mean"] is not None else None),
        "egg_fert_share": {"oc_c3": ctl_econ["egg_fert_share_mean"],
                           "goose_add": var_econ["egg_fert_share_mean"],
                           "h1": h1_econ["egg_fert_share_mean"]},
    }

    # ---- 供给零回撤：磁带逐路由（构造性）+ 配对局逐品（实测）双口径 ----
    tape_sup = build.get("supply_check") or {}
    out["supply_check"] = {
        "tape_caliber": {
            "rule": "逐路由逐品 SELL 挂单量：变体 ≥ 基线（手术=纯追加，构造性零回撤）",
            "n_routes": len(tape_sup),
            "zero_withdrawal_all": all(v.get("zero_withdrawal") for v in tape_sup.values()),
            "milk_wool_all": all(v.get("milk_wool_ok") for v in tape_sup.values()),
            "route0_sample": tape_sup.get("0"),
        },
        "games_caliber": supply_check_games(ledger),
    }

    p = pairs["goose_add_vs_oc_c3"]
    e = out["econ_stats"]
    sc = out["supply_check"]["games_caliber"]
    crit = {
        "net_flip_pos": bool(p["net_flip_wins"] > 0),
        "flips_neg_zero": bool(p["flips_neg"] == 0),
        "terminal_money_not_down": bool(
            e["terminal_money_delta_mean"] is not None and e["terminal_money_delta_mean"] >= 0),
        "milk_wool_zero_withdrawal": bool(sc["milk_wool_ok"]),
    }
    out["criteria"] = {
        "rule": "净翻胜>0 ∧ flips_neg==0 ∧ 终局钱不降（goose_add vs oc_c3）∧ "
                "MILK/WOOL 供给零回撤（逐品供给量≥基线）",
        "checks": crit,
        "all_pass": bool(all(crit.values())),
    }
    out["head_compare"] = {
        "head": {"herd": "C7-8/G9-11/S3-8（26 头）", "WHEAT": "169（涨队）",
                 "money_end": "105.7k", "labor": "畜线 18-19%/总 7.0-7.7k ops",
                 "sample": ga.HEAD_PARAMS["sample"]},
        "goose_add": {"G": "基线+10（G10-15 各路由；37 路由满档 +10，4 路由回滚 +8）",
                      "C_S": "基线全保（零回撤）",
                      "labor_route0": {"op_lines": build.get("labor_tables", {}).get(
                          "0", {}).get("op_lines"),
                          "animal_share": build.get("labor_tables", {}).get(
                              "0", {}).get("animal_share")},
                      "note": "劳动口径对齐头部：总 ops≈7.5k、畜线≈19.3%"},
    }
    out["verdict"] = {
        "verdict": ("PROD_ARM_CANDIDATE" if out["criteria"]["all_pass"]
                    else "NO_POSITIVE_GOOSE_ADD_ARM"),
        "positive": bool(out["criteria"]["all_pass"]),
        "budget_compliance": "局次 %d/%d（cap 合规）" % (budget["total_games"], BUDGET_CAP_GAMES),
    }

    # ---- rebuild / feasibility 三闸面（构建证据并入）----
    gates = build.get("route_gates") or []
    out["rebuild"] = {
        "base_main_sha256": build["manifest"]["base_main_sha256"],
        "main_sha256": build["manifest"]["main_sha256"],
        "diff_scope": build["manifest"]["diff_scope"],
        "n_change_rows": build["n_table_rows"],
        "schedule": build.get("schedule"),
        "assert_regen": build.get("assert_regen"),
        "assert_probe": build.get("assert_probe"),
        "trunk_red_line": "trunk 0..143 零扰动（shared_seg trunk divergent=0）",
    }
    out["feasibility"] = {
        "twin_seed": 780010,
        "gates": "现金 min_money≥0 / 劳动 realized(落位+滞留)≥基线 / 棚容 held≤结构格"
                 " / 加法 herd realized≥target",
        "n_routes": len(gates),
        "n_pass": sum(1 for r in gates if r.get("ok")),
        "n_bad": sum(1 for r in gates if not r.get("ok")),
        "n_add_dist": {"10": sum(1 for r in gates if r.get("n_add") == 10),
                       "8": sum(1 for r in gates if r.get("n_add") == 8)},
        "rollbacks": build.get("rollbacks"),
        "conservation": {"n": build["audit"]["conservation_n"],
                         "match": build["audit"]["conservation_match"]},
        "slot_ok_additive": build["audit"].get("slot_ok"),
        "shared_seg": build["audit"].get("shared_seg"),
        "realized_pairs_sample": [
            {"route": r["route"], "base": r["realized_base"], "var": r["realized_var"],
             "herd_g": [r["herd_target_goose"], r["herd_realized_goose"]]}
            for r in gates[:12]],
    }
    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声不修不管（任务边界）；终局钱 farms[obs.player] 口径",
        "孪生口径为 solo gengame（对手 PASS）：变体 solo 终局钱低于基线（~−20~35k）"
        "属补麦/雇工/购地成本+蛋价未饱和面；判据以配对实测（真实对手）为准",
        "tail 共享段逐值恒等被加法手位/逐路由波次破坏（tail divergent=%s，trunk=0）；"
        "游戏性安全=逐路由自洽+尾段照护全覆盖（d27-29 日日 FEED）；已登记"
        % (build["audit"].get("shared_seg", {}).get("tail", {}).get("divergent")),
        "4 路由现金回滚至 +8（R9 口径 ≤3 次）；37 路由满档 +10",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    RESULT_PATH.parent.mkdir(parents=True, exist_ok=True)
    RESULT_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n",
                           encoding="utf-8")
    (EVID_DIR / "judge_additive.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
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
