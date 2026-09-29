# -*- coding: utf-8 -*-
"""judge_modelpx_grid：MODELPX 预测器内部参数网格判决（grid-search；判决先行
·不发射不提交）。

责任口径（任务 modelpx-grid）：
- 机制=oc_c3 基座 MODELPX 预测器内部 4 轴（预测窗 win=滑窗 12/{6,24}、
  planned 常数 6/{2,12}、品项集 三品/{+CARROT,+EGG}、时段 h0=2/{10,14}）；
  量帽钉死 3/6/10、阈 0.5、均值窗 4 不参改（预登记：帽/阈=已判死门旋钮）。
- 粗扫：L9 双阵列+贪心正交抽样 18 配置（含基线 placebo）× 小判 n=8 双席
  （26 败局前 8 fold × 双席=16 局/配置）；判据 Δmargin>0 ∧ flips_neg==0。
- 细化：top-3 各取单轴最优邻域 1 件（贪心边际）复跑小判；赢家复验 n=16
  （+新中性 672000+i*113×8 双席=16 局），配对语料=败局 8 + 中性 8 =16 fold。
- 读数：终局钱 farms[obs.player]；margin=banks[our]−banks[opp]；附 d14-27
  窗（step 336-648）收入差对照（fill 口径影子引擎逐拍归因 + submit 口径）。
- 复用（不改写）：orderbook_milkwin_lab/judge_milkwin 的跑口/聚合/影子口径、
  orderbook_r40.sim_bridge.run_games、judge_r23.DEFAULT_OPPONENTS。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；判决预算 ≤400 局次。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-modelpx-grid.json；账本落
orderbook_modelpx_lab/evidence/。只写 orderbook_modelpx_lab/ 与该证据文件。
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

import build_modelpx as BMP  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    "judge_milkwin", KSIM_DIR / "orderbook_milkwin_lab" / "judge_milkwin.py")
JM = importlib.util.module_from_spec(_spec)
sys.modules["judge_milkwin"] = JM          # fork/pickle 需按名可解析
_spec.loader.exec_module(JM)

# d14-27 窗（任务口径：day14 起 step 336 → day27 止 step 648，右开）
JM.WINDOW = (336, 648)
JM.WIN_DAYS = tuple(range(14, 27))

RECORD_VERSION = "modelpx-grid/1.0"
LOSS_FOLDS = JM.REPLAY_26[:8]                      # 26 败局前 8 fold
NEUTRAL_FOLDS = [672000 + i * 113 for i in range(8)]
FOLDS_ALL = LOSS_FOLDS + NEUTRAL_FOLDS             # 复验 n=16 fold
OC_C3_MAIN = str(KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
                 / "main.py")
WORKERS = 2
BUDGET_CAP = 400
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-modelpx-grid.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "judge_grid_ledger.json"

EV = {}
ANOMALIES = []


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


def make_units(folds, tag):
    from orderbook_r40 import judge_r23 as j23
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(folds):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS)
                   else "neutral_672000_i113")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name,
                          "stratum": stratum, "tag": tag})
    return units


def play_arm(arm, cand_path, units, run_cfg, budget, key):
    specs = JM.make_specs(arm, cand_path, units)
    rows, engines = JM._play(specs, run_cfg)
    budget[key] = budget.get(key, 0) + len(rows)
    budget["judgment_局次"] = budget.get("judgment_局次", 0) + len(rows)
    bad = [r for r in rows if r.get("error")]
    if bad:
        ANOMALIES.append("%s: %d 局 error: %r" % (arm, len(bad),
                                                  bad[0].get("error")))
    return rows


def rows_by_key(rows):
    return {(int(r["seed"]), int(r["seat"])): r for r in rows}


def lite_pair(ps):
    keys = ("n", "W", "L", "T", "mean_delta", "win_control", "win_variant",
            "flips_pos", "flips_neg", "net_flip_wins", "loss_recovery",
            "control_win_guard_ok", "positive_arm")
    return {k: ps.get(k) for k in keys}


def win_lite(wp):
    return {k: (wp.get(k) or {}).get("mean_delta") for k in
            ("fill_total", "fill_milk", "submit_total", "submit_milk")}


def marginals(levels_rows):
    """各轴各水平的粗扫 mean_delta 边际（用于邻域贪心）。"""
    out = {}
    for ai, name in enumerate(("win", "planned", "items", "h0")):
        buckets = {}
        for levels, row in levels_rows:
            buckets.setdefault(levels[ai], []).append(row.get("mean_delta") or 0.0)
        out[name] = {lv: round(sum(v) / len(v), 2) for lv, v in buckets.items()}
    return out


def neighbor_of(levels, marg):
    """单轴最优邻域：挑边际最大轴改到其最优水平（不同当前才生效）。"""
    best = None
    for ai, name in enumerate(("win", "planned", "items", "h0")):
        m = marg.get(name) or {}
        if not m:
            continue
        best_lv = max(m, key=lambda lv: m[lv])
        if best_lv == levels[ai]:
            continue
        spread = max(m.values()) - min(m.values())
        cand = list(levels)
        cand[ai] = best_lv
        if best is None or spread > best[0]:
            best = (spread, tuple(cand), name)
    return best


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import sim_bridge as sb
    t0 = time.perf_counter()
    base_sha = hashlib.sha256(Path(OC_C3_MAIN).read_bytes()).hexdigest()
    if base_sha != BMP.BASE_SHA_EXPECTED:
        raise RuntimeError("基底 oc_c3 sha 漂移：%s" % base_sha)

    budget = {"cap_局次": BUDGET_CAP, "auth_局次": 0, "judgment_局次": 0,
              "control_局次": 0, "coarse_局次": 0, "refine_局次": 0,
              "verify_局次": 0,
              "cap_scope": "判决局（对照+粗扫+细化+复验）≤400；sim_bridge 认证"
                           "为先决条件另计"}
    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("MODELPX 预测器内部参数网格（窗内变现 d14-27 三连负后"
                       "定位：门旋钮不绑定，绑定的是预测器内部）——预测窗/"
                       "planned/品项集/时段 4 轴正交粗扫 18 配置 + top-3 邻域"
                       "细化 + 赢家复验 n=16，变体 vs oc_c3 配对"),
        "source": {
            "commands": ["python3 orderbook_modelpx_lab/build_modelpx.py",
                         "python3 orderbook_modelpx_lab/judge_modelpx_grid.py"],
            "base_main": OC_C3_MAIN, "base_sha256": base_sha,
            "corpus": {"loss_folds": LOSS_FOLDS, "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*113（i=0..7）",
                       "coarse_folds": "26 败局前 8 fold（n=8 双席=16 局/配置）",
                       "verify_folds": "败局 8 + 中性 8 =16 fold（n=16 双席=32 局）"},
            "workers": WORKERS,
            "caliber": {
                "margin": "banks[our]−banks[opp]（run_games banks）",
                "terminal_money": "farms[obs.player].money（干净口径）",
                "window": "d14-27 窗 step 336-648 逐日=step//24（14..26）；fill"
                          " 口径=影子引擎逐拍归因；submit 口径=挂单 qty×卖时市价",
            },
            "criteria": "初筛 Δmargin>0 ∧ flips_neg==0（n=8 配对）；top-3 单轴"
                        "邻域细化；赢家复验 n=16 同判据 + d14-27 窗收入差对照",
        },
        "grid": {"configs": [], "results": {}},
        "top_refine": {},
        "pairs": {},
        "window_stats": {},
        "criteria": {},
        "verdict": {},
        "budget": budget,
    })

    # ---- 0) 构建入账 ----
    man_all = json.loads((MODULE_DIR / "evidence" / "build_manifest.json")
                         .read_text(encoding="utf-8"))
    coarse_levels = [tuple(r["levels"]) for r in man_all["grid"]]
    for form, man in man_all["forms"].items():
        EV["grid"]["configs"].append({
            "form": form, "levels": man["levels"], "params": man["params"],
            "main_sha256": man["main_sha256"],
            "roundtrip_identity_ok": man["roundtrip_identity_ok"],
            "subs": [{"old": s["old"][:60], "count": s["count"]}
                     for s in man["subs"]]})
    flush_evid()

    # ---- 1) sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(JM.REPLAY_26[:8]) + NEUTRAL_FOLDS + \
        [2026092901, 2026092902, 2026092903, 2026092904, 2026092905,
         2026092906, 2026092907, 2026092908, 2026092909, 2026092910,
         2026092911, 2026092912, 2026092913, 2026092914]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "consistency_ok", "degraded",
                  "degraded_reason", "engine", "version")}
    EV["source"]["sim_auth"] = auth_lite
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 对照认证未过 30/30"}
        flush_evid()
        print("ABORT", EV["verdict"], flush=True)
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 2) 对照臂 oc_c3（16 fold 双席=32 局，全配对复用） ----
    units_all = make_units(FOLDS_ALL, "all")
    units_loss = [u for u in units_all if u["seed"] in set(LOSS_FOLDS)]
    units_neu = [u for u in units_all if u["seed"] in set(NEUTRAL_FOLDS)]
    ctl_rows = play_arm("oc_c3", OC_C3_MAIN, units_all, run_cfg, budget,
                        "control_局次")
    ctl = rows_by_key(ctl_rows)
    EV["pairs"]["control"] = {"arm": "oc_c3", "n_units": len(ctl_rows),
                              "margin_mean": round(
                                  sum(r["margin"] for r in ctl_rows
                                      if r.get("margin") is not None)
                                  / max(1, len(ctl_rows)), 2),
                              "terminal_money_mean":
                                  JM.end_agg(ctl_rows)["terminal_money_mean"]}
    flush_evid()

    # ---- 3) 粗扫 18 配置 × 16 局 ----
    coarse = {}
    levels_rows = []
    arm_rows = {}
    for levels in coarse_levels:
        form = BMP.cfg_id(levels)
        path = str(MODULE_DIR / "build" / form / "main.py")
        rows = play_arm(form, path, units_loss, run_cfg, budget, "coarse_局次")
        var = rows_by_key(rows)
        arm_rows[form] = var
        ps = JM.pair_stats(ctl, var, units_loss)
        dwin = JM.window_paired(ctl, var, units_loss)
        coarse[form] = {"levels": list(levels), "pair": lite_pair(ps),
                        "dWin_fill_total": win_lite(dwin)["fill_total"],
                        "dWin_fill_milk": win_lite(dwin)["fill_milk"]}
        levels_rows.append((levels, coarse[form]["pair"]))
        EV["grid"]["results"][form] = coarse[form]
        print("coarse", form, "dM", coarse[form]["pair"]["mean_delta"],
              "flips_neg", coarse[form]["pair"]["flips_neg"],
              "dWin", coarse[form]["dWin_fill_total"], flush=True)
        if budget["judgment_局次"] > BUDGET_CAP:
            ANOMALIES.append("判决预算触顶于粗扫 %s" % form)
            break
    flush_evid()

    # ---- 3b) placebo：基线配置 vs oc_c3 动作流逐字节（运行时封印，复用粗扫行） ----
    base_form = BMP.cfg_id((0, 0, 0, 0))
    seal = JM.seal_check(ctl, arm_rows.get(base_form) or {}, units_loss)
    EV["pairs"]["placebo_seal"] = seal
    if not seal.get("passed"):
        ANOMALIES.append("placebo 封印未过：%r" % (seal.get("violations"),))
    flush_evid()

    # ---- 4) top-3 邻域细化 ----
    def passed(item):
        p = item["pair"]
        return (p.get("mean_delta") or 0) > 0 and p.get("flips_neg") == 0

    ranked = sorted(coarse.items(), key=lambda kv: -(kv[1]["pair"].get(
        "mean_delta") or 0))
    top3 = [kv[0] for kv in ranked[:3]]
    marg = marginals(levels_rows)
    done_forms = set(coarse)
    refine = {}
    for form in top3:
        levels = tuple(coarse[form]["levels"])
        nb = neighbor_of(levels, marg)
        if nb is None:
            continue
        _, cand_levels, axis = nb
        cand_form = BMP.cfg_id(cand_levels)
        if cand_form in done_forms:
            continue
        done_forms.add(cand_form)
        BMP.build_one(cand_levels)
        path = str(MODULE_DIR / "build" / cand_form / "main.py")
        rows = play_arm(cand_form, path, units_loss, run_cfg, budget,
                        "refine_局次")
        var = rows_by_key(rows)
        arm_rows[cand_form] = var
        ps = JM.pair_stats(ctl, var, units_loss)
        dwin = JM.window_paired(ctl, var, units_loss)
        refine[cand_form] = {
            "levels": list(cand_levels), "from_top": form, "axis": axis,
            "pair": lite_pair(ps),
            "dWin_fill_total": win_lite(dwin)["fill_total"],
            "dWin_fill_milk": win_lite(dwin)["fill_milk"]}
        print("refine", cand_form, "dM", refine[cand_form]["pair"]["mean_delta"],
              flush=True)
    allc = dict(coarse)
    allc.update(refine)
    passed_forms = [f for f, it in allc.items() if passed(it)]
    winner = max(passed_forms or [f for f in allc if f != base_form],
                 key=lambda f: allc[f]["pair"].get("mean_delta") or 0)
    EV["top_refine"] = {
        "marginals": marg, "top3": top3,
        "top3_pairs": {f: coarse[f]["pair"] for f in top3},
        "refine": refine, "winner": winner,
        "winner_levels": allc[winner]["levels"],
        "passed_initial_screen": passed_forms,
        "screen_rule": "Δmargin>0 ∧ flips_neg==0（n=8 配对）"}
    flush_evid()

    # ---- 5) 赢家复验 n=16（中性 8 fold 双席16 局 + 复用其败局粗扫行） ----
    w_levels = tuple(allc[winner]["levels"])
    w_form = BMP.cfg_id(w_levels)
    w_path = str(MODULE_DIR / "build" / w_form / "main.py")
    neu_rows = play_arm(w_form, w_path, units_neu, run_cfg, budget,
                        "verify_局次")
    var_all = dict(arm_rows.get(w_form) or {})
    var_all.update(rows_by_key(neu_rows))
    ps16 = JM.pair_stats(ctl, var_all, units_all)
    dwin16 = JM.window_paired(ctl, var_all, units_all)
    win16 = {arm: JM.window_agg([r for r in rows if r.get("window")])
             for arm, rows in (("oc_c3", ctl_rows),
                               (w_form, list(var_all.values())))}
    EV["pairs"]["verify"] = {
        "arm": w_form, "levels": list(w_levels),
        "design": "变体 vs oc_c3 同 (seed,seat) 双席配对；16 fold=26 败局前 8 "
                  "+ 新中性 672000+i*113×8",
        "n16": lite_pair(ps16), "rows_lite": ps16.get("rows_lite"),
        "realized_paired": JM.realized_paired(ctl, var_all, units_all).get(
            "nonneg_both")}
    EV["window_stats"] = {
        "window": "d14-27（step 336-648）",
        "paired_delta": win_lite(dwin16),
        "per_day_fill_total_delta_mean": {
            str(d): (dwin16.get("per_day_fill_total_delta", {}).get(d) or {})
            .get("mean_delta")
            for d in sorted(dwin16.get("per_day_fill_total_delta", {}))},
        "agg_by_arm": win16,
        "submit_delta": win_lite(dwin16)}
    EV["criteria"] = {
        "初筛（n=8）": "Δmargin>0 ∧ flips_neg==0",
        "初筛结果": {f: (allc[f]["pair"]["mean_delta"],
                          allc[f]["pair"]["flips_neg"], passed(allc[f]))
                     for f in allc},
        "复验（n=16）": "同判据 + d14-27 窗收入差对照（fill 总窗配对 Δ）",
        "复验结果": {
            "Δmargin>0": (ps16.get("mean_delta") or 0) > 0,
            "flips_neg==0": ps16.get("flips_neg") == 0,
            "d14-27窗收入差>0": (dwin16.get("fill_total", {})
                                 .get("mean_delta") or 0) > 0,
            "净翻胜": ps16.get("net_flip_wins")}}
    ok = ((ps16.get("mean_delta") or 0) > 0 and ps16.get("flips_neg") == 0)
    EV["verdict"] = {
        "positive_arm": bool(ok),
        "winner": w_form, "winner_levels": list(w_levels),
        "n16_mean_delta": ps16.get("mean_delta"),
        "n16_flips_neg": ps16.get("flips_neg"),
        "n16_net_flip_wins": ps16.get("net_flip_wins"),
        "d14_27_fill_total_delta": (dwin16.get("fill_total", {})
                                    .get("mean_delta")),
        "terminal_money_mean": {arm: JM.end_agg(
            list(rows.values()))["terminal_money_mean"]
            for arm, rows in (("oc_c3", ctl), (w_form, var_all))},
        "launch": "不发射（判决先行）；上线决策移交用户"}
    budget["within_cap"] = budget["judgment_局次"] <= BUDGET_CAP
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    LEDGER_PATH.write_text(json.dumps(
        {"budget": budget, "winner": w_form,
         "coarse": {f: it["pair"] for f, it in coarse.items()},
         "refine": {f: it["pair"] for f, it in refine.items()}},
        ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("VERDICT:", EV["verdict"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", budget, flush=True)
    return EV


if __name__ == "__main__":
    main()
