# -*- coding: utf-8 -*-
"""judge_sx：合装件判决（mpx 胜者件+expx_v2 层 vs mpx 胜者件；判决先行·不发射
不提交）。

责任口径（任务 sx-composite）：
- 形态=sx 合装件（mpx_w24_p2_3_h14 + expx_v2 层：MODELPX 预测核 p_next 精确化
  + 边际收益定单量 + 胜位守卫[窗收缩 step144-648+滞留保险]；take_long 共享面
  组合 _expx_take(_mx_cap)）。
- 语料=26 败局前 8 fold + 新中性 673000+i*121×8（i=0..7），n=16 双席=32
  (seed,seat) 单元/臂；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转。
- 主判 sx vs mpx 胜者件；参 sx vs oc_c3。
- 判据（预登记）：sx vs mpx h2h≥0.5 ∧ flips_neg==0 ∧ 实现价非负（配对
  Δratio_fill 三品∧全品均值≥0）∧ 窗差不降（d14-27 fill 总窗配对 mean Δ≥0）；
  附 963182245 类格复核。
- 门禁：足迹审计（非触发拍零足迹）=expx 嫁接层 sx vs mpx 逐拍动作流对比（同
  (seed,seat)），非触发拍零足迹、首差异拍=首个决策差异拍、决策差异拍全落
  MODELPX 窗 [144,695]。
- 读数：终局钱 farms[obs.player]；实现价=Σ(filled×成交价)/Σ(filled×base)。
- sim_bridge 认证 30/30 先行；workers=2；预算 ≤250 局次。
证据写 fn_docs/hybrid/results/2026-09-30-sx-composite.json；账本落
orderbook_sx_lab/evidence/。复用 judge_expx 机件（_play/footprint_audit/
realized_paired3/per_item_table）+ judge_milkwin 配对/窗聚合。不改既有代码。
只写 orderbook_sx_lab/ 与该 evidence JSON。
"""
from __future__ import annotations

import gzip
import hashlib
import json
import os
import statistics
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
for _p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_milkwin_lab"),
           str(KSIM_DIR / "orderbook_expx_lab"), str(MODULE_DIR)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import judge_expx as je  # noqa: E402  （机件复用；含 jm 窗口径热替换 d14-27）
import judge_milkwin as jm  # noqa: E402

RECORD_VERSION = "sx-composite/1.0"
UNKNOWN = "UNKNOWN"

LOSS_FOLDS = list(jm.REPLAY_26[:8])                  # 26 败局前 8 fold
NEUTRAL_FOLDS = [673000 + i * 121 for i in range(8)]  # 任务给定新中性块
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS                   # n=16 双席 fold/臂
RECHECK_SEED = 963182245

# jm 窗口径（judge_expx 已置 d14-27 (336,672)）；如漂移则重置
if jm.WINDOW != (336, 672):
    jm.WINDOW = (336, 672)
    jm.WIN_DAYS = tuple(range(14, 28))

SX_MAIN = str(MODULE_DIR / "build" / "sx" / "main.py")
MPX_MAIN = str(KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
               / "main.py")
OC_C3_MAIN = je.OC_C3_MAIN
OC_C3_SHA_EXPECTED = je.OC_C3_SHA_EXPECTED
ARMS = {"oc_c3": OC_C3_MAIN, "mpx": MPX_MAIN, "sx": SX_MAIN}
RUN_FORMS = ("oc_c3", "mpx", "sx")
MX_WINNER_SHA = ("f0101de9b558d1f56334739f9a49a0a0d4bc860a898792a9b69fc72"
                 "c3d84e44f")

WORKERS = 2
BUDGET_CAP_GAMES = 250
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-30-sx-composite.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "sx_ab_ledger.json"
RAW_ROWS_PATH = MODULE_DIR / "evidence" / "raw_rows_sx.json.gz"

EV = {}
ANOMALIES = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def save_raw(rows_by_arm):
    with gzip.open(RAW_ROWS_PATH, "wt", encoding="utf-8") as fh:
        json.dump(rows_by_arm, fh, default=str)


def make_units():
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_673000_i121")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum})
    return units, opp_paths


def make_specs(arm, cand_path, units):
    return je.make_specs(arm, cand_path, units)   # 同机件（game_id 前缀 expx-）


def h2h(ps):
    """head-to-head 胜率（平局计半）=(W+0.5T)/n；判据≥0.5 ⟺ W≥L。"""
    n = ps.get("n") or 0
    if not n:
        return UNKNOWN
    return round((ps["W"] + 0.5 * ps["T"]) / n, 4)


def main():
    os.chdir(je.KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != OC_C3_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)
    mpx_sha = hashlib.sha256(Path(MPX_MAIN).read_bytes()).hexdigest()
    if mpx_sha != MX_WINNER_SHA:
        raise RuntimeError("mpx 胜者件 sha 漂移：%s" % mpx_sha)
    man = json.loads((MODULE_DIR / "build" / "sx" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    sx_sha = hashlib.sha256(Path(SX_MAIN).read_bytes()).hexdigest()
    if sx_sha != man.get("main_sha256"):
        raise RuntimeError("sx main sha 漂移")

    units, opp_paths = make_units()
    budget = {"cap_局次": BUDGET_CAP_GAMES, "smoke_局次": 1, "auth_局次": 0,
              "judgment_局次": 0}

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("合装件判决（sx=mpx 胜者件+expx_v2 层）：mpx 焦窗（h14-22）"
                       "+ expx 引擎模型化领卖+胜位守卫，作用面正交（预测核/窗字面"
                       "量）唯一共享面 take_long 组合 _expx_take(_mx_cap)；主判 "
                       "sx vs mpx，参 sx vs oc_c3"),
        "build": {
            "composite": man.get("composite"),
            "sx_main": SX_MAIN, "sx_sha256": sx_sha,
            "sx_bytes": man.get("main_bytes"),
            "mpx_winner": man.get("mpx_winner"), "mpx_sha256": mpx_sha,
            "expx_layer": man.get("expx_layer"), "params": man.get("params"),
            "chain": man.get("chain"),
            "subs_groups": len(man.get("subs") or []),
            "subs_total_replacements": sum(s.get("count") for s in
                                          (man.get("subs") or [])),
            "subs_roundtrip_identity_ok": man.get("subs_roundtrip_identity_ok"),
            "gate_literal_untouched": man.get("gate_literal_untouched"),
            "diff_audit": man.get("diff_audit"),
        },
        "source": {
            "commands": ["python3 orderbook_sx_lab/build_sx.py",
                         "python3 orderbook_sx_lab/judge_sx.py"],
            "base_main": OC_C3_MAIN, "base_sha256": base_sha,
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "673000+i*121（任务给定新中性块 n=8）",
                       "folds_per_variant": len(FOLDS),
                       "strata": "26 败局前 8 + 新中性 673000+i*121×8；双席 "
                                 "n=16/臂=32 (seed,seat) 单元/臂"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": {"unit": "配对单元=(seed,seat)；每臂 32 局",
                        "margin": "banks[our]−banks[opp]",
                        "terminal_money": "farms[obs.player].money（干净口径）",
                        "window": "d14-27（step 336-672）fill 口径影子引擎逐拍"
                                  "归因",
                        "realized_px": "Σ(filled×成交价)/Σ(filled×base)"},
            "criterion": ("sx vs mpx h2h≥0.5 ∧ flips_neg==0 ∧ 实现价非负（配对 "
                          "Δratio_fill 三品∧全品均值≥0）∧ 窗差不降（d14-27 fill "
                          "总窗配对 mean Δ≥0）；附 963182245 类格复核"),
        },
        "pairs": {}, "window_stats": {}, "per_item_realized": {},
        "per_item_table": {}, "realized_px_paired": {}, "terminal_money": {},
        "gates_footprint": {}, "criteria": {}, "verdict": {},
        "recheck_963182245": {}, "budget": budget,
    })
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(jm.REPLAY_26[:8]) + NEUTRAL_FOLDS + \
        [2026092901, 2026092902, 2026092903, 2026092904, 2026092905,
         2026092906, 2026092907, 2026092908, 2026092909, 2026092910,
         2026092911, 2026092912, 2026092913, 2026092914]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 冒烟 1 局（非 fold 语料，不入配对） ----
    smoke_units = [{"seed": 2026093099, "seat": 0, "opp_path": opp_paths[0],
                    "opponent": "r37", "stratum": "smoke"}]
    smoke_rows, _e0 = je._play(make_specs("smoke", ARMS["sx"], smoke_units),
                               run_cfg)
    print("smoke:", smoke_rows[0].get("margin"), smoke_rows[0].get("error"),
          flush=True)
    if smoke_rows[0].get("error"):
        ANOMALIES.append("管线冒烟局红：%r" % (smoke_rows[0].get("error"),))
    budget["smoke_局次"] = 1
    flush_evid()

    # ---- 3) 三臂实跑（oc_c3 / mpx / sx） ----
    rows_by_arm = {}
    for arm in RUN_FORMS:
        specs = make_specs(arm, ARMS[arm], units)
        t2 = time.perf_counter()
        rows, engines = je._play(specs, run_cfg)
        rows_by_arm[arm] = rows
        save_raw(rows_by_arm)
        budget["judgment_局次"] += len(rows)
        EV["per_item_realized"][arm] = jm.realized_agg(rows)
        EV["terminal_money"][arm] = jm.end_agg(rows)
        EV["window_stats"][arm] = jm.window_agg(rows)
        EV["window_stats"][arm]["window"] = "d14-27（step 336-672）"
        n_err = sum(1 for r in rows if r.get("error"))
        if n_err:
            ANOMALIES.append("%s 局红 %d/%d" % (arm, n_err, len(rows)))
        mism = EV["per_item_realized"][arm]["aggregate"].get(
            "shadow_mismatch_steps")
        if mism:
            ANOMALIES.append("%s 影子引擎不一致步 %s" % (arm, mism))
        if arm == "sx":
            te = {"fires": 0, "units": 0, "errors": 0, "censored_lo": 0,
                  "decision_diffs": 0, "mr_limited": 0, "cap_limited": 0,
                  "stranding_insured": 0, "post_win_base": 0}
            for r in rows:
                x = r.get("expx") or {}
                for k in ("fires", "units", "errors", "censored_lo",
                          "mr_limited", "cap_limited", "stranding_insured",
                          "post_win_base"):
                    te[k] += int(x.get(k) or 0)
                te["decision_diffs"] += len(x.get("decision_diff_steps") or [])
            EV["sx_expx_telemetry"] = te
        print(arm, "games", len(rows), "err", n_err,
              "tm", EV["terminal_money"][arm]["terminal_money_mean"],
              "win_fill_total", EV["window_stats"][arm]["mean_fill_total"],
              "shadow_mism", mism, round(time.perf_counter() - t2, 1), "s",
              flush=True)
        EV["budget"] = budget
        flush_evid()

    ctl_oc = {(r["seed"], r["seat"]): r for r in rows_by_arm["oc_c3"]}
    ctl_mpx = {(r["seed"], r["seat"]): r for r in rows_by_arm["mpx"]}
    var_sx = {(r["seed"], r["seat"]): r for r in rows_by_arm["sx"]}

    # ---- 4) 足迹审计门（expx 嫁接层 sx vs mpx；非触发拍零足迹） ----
    fp = je.footprint_audit(ctl_mpx, var_sx, units)
    EV["gates_footprint"] = fp
    if not fp["gate_passed"]:
        ANOMALIES.append("足迹审计门未全过：%d/%d 格过"
                         % (fp["n_passed"], fp["n_cells"]))
    print("footprint(sx vs mpx):", fp["n_passed"], "/", fp["n_cells"],
          flush=True)
    flush_evid()

    # ---- 5) 配对判决：主判 sx vs mpx；参 sx vs oc_c3 ----
    def cmp_block(ctl, var, tag):
        ps = jm.pair_stats(ctl, var, units)
        wp = jm.window_paired(ctl, var, units)
        rp = je.realized_paired3(ctl, var, units)
        return {
            "pair": {k: ps.get(k) for k in ("n", "W", "L", "T", "mean_delta",
                                            "win_control", "win_variant",
                                            "flips_pos", "flips_neg",
                                            "net_flip_wins")},
            "h2h": h2h(ps),
            "window_fill_total_mean_delta": wp["fill_total"]["mean_delta"],
            "window_fill_milk_mean_delta": wp["fill_milk"]["mean_delta"],
            "window_submit_total_mean_delta":
                wp["submit_total"]["mean_delta"],
            "realized_px_nonneg_all_three": rp["nonneg_all_three"],
            "realized_px_d_ratio_fill": {
                it: (rp.get(it) or {}).get("mean_delta")
                for it in ("all", "MILK", "WOOL", "STRAWBERRY")},
            "rows_lite": ps.get("rows_lite"),
            "_wp": wp, "_rp": rp, "_ps": ps}

    main_cmp = cmp_block(ctl_mpx, var_sx, "sx_vs_mpx")
    ref_cmp = cmp_block(ctl_oc, var_sx, "sx_vs_oc_c3")
    EV["pairs"]["sx_vs_mpx"] = {k: v for k, v in main_cmp.items()
                                if not k.startswith("_")}
    EV["pairs"]["sx_vs_oc_c3"] = {k: v for k, v in ref_cmp.items()
                                  if not k.startswith("_")}
    EV["window_stats"]["paired_sx_vs_mpx"] = {
        k: (main_cmp["_wp"].get(k) or {}).get("mean_delta")
        for k in ("fill_total", "fill_milk", "submit_total", "submit_milk")}
    EV["window_stats"]["paired_sx_vs_oc_c3"] = {
        k: (ref_cmp["_wp"].get(k) or {}).get("mean_delta")
        for k in ("fill_total", "fill_milk", "submit_total", "submit_milk")}
    EV["realized_px_paired"]["sx_vs_mpx"] = {
        it: {"mean_delta": (main_cmp["_rp"].get(it) or {}).get("mean_delta"),
             "nonneg": (main_cmp["_rp"].get(it) or {}).get("nonneg")}
        for it in ("all", "MILK", "WOOL", "STRAWBERRY")}
    EV["realized_px_paired"]["sx_vs_oc_c3"] = {
        it: {"mean_delta": (ref_cmp["_rp"].get(it) or {}).get("mean_delta"),
             "nonneg": (ref_cmp["_rp"].get(it) or {}).get("nonneg")}
        for it in ("all", "MILK", "WOOL", "STRAWBERRY")}
    EV["per_item_table"]["sx_vs_mpx"] = je.per_item_table({
        "mpx": EV["per_item_realized"]["mpx"],
        "sx": EV["per_item_realized"]["sx"]})

    # ---- 6) 判据（sx vs mpx 主判） ----
    ps = main_cmp["_ps"]
    win_d = main_cmp["window_fill_total_mean_delta"]
    hh = main_cmp["h2h"]
    crit = {
        "sx_vs_mpx_h2h>=0.5": is_num(hh) and float(hh) >= 0.5,
        "flips_neg==0": ps["flips_neg"] == 0,
        "实现价非负（Δratio_fill 三品∧全品均值≥0）":
            main_cmp["realized_px_nonneg_all_three"],
        "窗差不降（d14-27 fill 总窗配对 mean Δ≥0）":
            is_num(win_d) and float(win_d) >= 0,
    }
    EV["criteria"] = {
        "checks": crit, "h2h": hh, "W_L_T": "%s/%s/%s" % (ps["W"], ps["L"],
                                                          ps["T"]),
        "mean_delta": ps["mean_delta"], "flips_neg": ps["flips_neg"],
        "net_flip_wins": ps["net_flip_wins"],
        "window_fill_total_mean_delta": win_d,
        "window_fill_milk_mean_delta":
            main_cmp["window_fill_milk_mean_delta"],
        "realized_px_nonneg_all_three":
            main_cmp["realized_px_nonneg_all_three"],
        "footprint_gate_passed": fp["gate_passed"],
        "positive_arm": all(crit.values())}
    print("sx vs mpx:", "W%s/L%s/T%s" % (ps["W"], ps["L"], ps["T"]),
          "h2h", hh, "dM", ps["mean_delta"], "flips_neg", ps["flips_neg"],
          "dWin", win_d,
          "px_nonneg", main_cmp["realized_px_nonneg_all_three"],
          "crit", crit, flush=True)

    # ---- 7) 963182245 类格复核（sx vs mpx + sx vs oc_c3 双席） ----
    def recheck(ctl, var):
        out = []
        for u in units:
            if u["seed"] != RECHECK_SEED:
                continue
            key = (u["seed"], u["seat"])
            rc, rv = ctl.get(key), var.get(key)
            if not rc or not rv:
                continue
            out.append({
                "seat": u["seat"], "opponent": u.get("opponent"),
                "margin_control": rc.get("margin"),
                "margin_variant": rv.get("margin"),
                "delta": round(float(rv["margin"]) - float(rc["margin"]), 1),
                "sx_fires": (rv.get("expx") or {}).get("fires"),
                "sx_units": (rv.get("expx") or {}).get("units"),
                "stranding_insured": (rv.get("expx") or {}).get(
                    "stranding_insured"),
                "post_win_base": (rv.get("expx") or {}).get("post_win_base"),
            })
        return out

    EV["recheck_963182245"] = {
        "note": "963182245=26 败局第 5 位（expx v1 唯一翻负种子）；本语料在列，"
                "双席 vs r37/轮转对手复核 sx vs mpx 与 sx vs oc_c3",
        "sx_vs_mpx": recheck(ctl_mpx, var_sx),
        "sx_vs_oc_c3": recheck(ctl_oc, var_sx)}

    # ---- 8) verdict ----
    budget["total_局次"] = (budget["auth_局次"] + budget["smoke_局次"]
                           + budget["judgment_局次"])
    budget["within_cap"] = budget["total_局次"] <= BUDGET_CAP_GAMES
    budget["note"] = ("预算=认证 60(30 局×2 引擎)+冒烟 1+判决 96（3 臂×32 "
                      "单元）=157≤250")
    ok_all = all(crit.values())
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "criteria_passed": ok_all,
        "footprint_gate_passed": fp["gate_passed"],
        "h2h_sx_vs_mpx": hh,
        "per_item_ratio_fill_delta_sx_vs_mpx": {
            it: (EV["per_item_table"]["sx_vs_mpx"].get(it) or {}).get(
                "d_ratio_fill") for it in je.MX_ITEMS},
        "verdict": ("SX_COMPOSITE_POSITIVE: 合装件四判据全过（足迹审计门%s）"
                    % ("过" if fp["gate_passed"] else "未过") if ok_all else
                    "NOT_CONFIRMED（详见 criteria）"),
        "form": "sx",
        "note": "判据预登记（sx vs mpx h2h≥0.5 ∧ flips_neg=0 ∧ 实现价非负 ∧ "
                "窗差不降）；不发射不提交",
    }
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    EV["budget"] = budget
    if not budget["within_cap"]:
        ANOMALIES.append("预算超限：%s" % budget)
    ANOMALIES.append("harness 噪声不修不管：HP_TELEMETRY stdout 行；"
                     "kaggle_environments 可选环境加载告警")
    ANOMALIES.append("守卫口径备忘：①窗收缩后 fire_x=fire_base（648+ 零足迹）；"
                     "②滞留保险容量=模型窗内峰值拍×基线帽逐拍扣减；投影不含自家"
                     "未来销售、不含未来商店解锁；take_long 共享面 _expx_take("
                     "_mx_cap) 以 mpx 帽 (3,6,10) 为上限")
    LEDGER_PATH.write_text(json.dumps(
        {"pairs": {"sx_vs_mpx": EV["pairs"]["sx_vs_mpx"]["pair"],
                   "sx_vs_oc_c3": EV["pairs"]["sx_vs_oc_c3"]["pair"]},
         "criteria": EV["criteria"], "budget": budget,
         "recheck_963182245": EV["recheck_963182245"]},
        ensure_ascii=False, indent=1, default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    print("VERDICT:", EV["verdict"]["verdict"], flush=True)
    return EV


if __name__ == "__main__":
    main()
