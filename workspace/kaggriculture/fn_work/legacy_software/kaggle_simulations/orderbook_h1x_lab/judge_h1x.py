# -*- coding: utf-8 -*-
"""judge_h1x（H1X = H1 王座基座 + S8 尖拍捕获层）：判决（只测不发/不在线提交）。

H1X = orderbook_strongest_lab/build/h1/main.py（76b5f842…）+ 尖拍尾块
（build_h1x.py；机制提取自 s8/main.py a59208fe…），entry _h1x_agent。

判决口径同 S8 判决：judge_r44._fold_arm 双席折叠、margin=farms[obs.player]
（终局钱差，干净口径）、块 674000+i*159（i=0..11，可比 S8 行）：
  1. 面板（每对 12 fold 双席）：h1x vs {H1（关键！同基座对照）、oc_c3、mpx、
     r40、A}——h2h 逐对 fold；
  2. 同块配对增量（vs H1 逐 unit delta）：H1 控制臂 vs {oc_c3,mpx,r40,A} 同
     (seed,seat,opp) 配对——W-L-T+mean+flips_neg/pos；
  3. 毒种五枚（674000/674141/674705/674987/675410）每枚 4 局（{mpx,oc_c3}×
     双席）配对 H1 对照——验证毒种翻正是否随层迁移；
判读：h1x vs H1 h2h ≥0.5 且 flips_neg≤2 且毒种翻正保持 → 超越王座候选成立。
预算 ≤500 局次（auth 30 + smoke 2 + 面板 120 + 控制 96 + 毒种 40，缓存去重）。
sim_bridge 认证缓存复用。证据 evidence/h1x_verdict.json。
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
REPO = KSIM_DIR.parents[2]
for p in (str(KSIM_DIR), str(KSIM_DIR / "orderbook_s1form_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_s_form as jsf  # noqa: E402  只读复用（Tracer/end_reads/flip/fold）

EVID_DIR = HERE / "evidence"
H1X = HERE / "build" / "h1x" / "main.py"
H1 = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
PANEL = {
    "H1": H1,
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
    / "main.py",
    "mpx": KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14"
    / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
}
CONTROL_OPPS = ("oc_c3", "mpx", "r40", "A")     # 同块配对（H1 控制臂）第三方
POISON_SEEDS = [674000, 674141, 674705, 674987, 675410]
POISON_OPPS = ("mpx", "oc_c3")
FOLDS = [674000 + i * 159 for i in range(12)]
WORKERS = 4
BUDGET_CAP = 500

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 30, "smoke": 2,
          "panel_规格": 120, "control_规格": 96, "poison_规格": 40}
_ROW_CACHE = {}


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "h1x_verdict.json").write_text(
        json.dumps(EV, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱 farms[obs.player]（judge_s8 同源口径）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows, games, metas = [], [], []
    for spec in payload["specs"]:
        sinks = {0: [], 1: []}
        try:
            our = j23._load_entry(spec["arm_path"])
            opp = j23._load_entry(spec["opp_path"])
            a_us = jsf._Tracer(our, spec["our_seat"], sinks[spec["our_seat"]])
            a_opp = jsf._Tracer(opp, 1 - spec["our_seat"],
                                sinks[1 - spec["our_seat"]])
            a0, a1 = (a_us, a_opp) if spec["our_seat"] == 0 else (a_opp, a_us)
            games.append({"seed": int(spec["seed"]), "agents": [a0, a1]})
            metas.append((spec, sinks, our, None))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, sinks, None, repr(exc)[:120]))
    res = sb.run_games(games, dict(payload.get("cfg") or {})) if games \
        else {"games": []}
    rrs = list(res.get("games") or [])
    for i, (spec, sinks, our, berr) in enumerate(metas):
        rr = rrs[i] if i < len(rrs) else {}
        row = {"seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
               "arm": spec["arm"], "opponent": spec.get("opponent"),
               "block": spec.get("block"), "tag": spec.get("tag"),
               "banks": rr.get("banks"), "error": berr or rr.get("error"),
               "margin_clean": None, "tm_us": None, "tm_opp": None,
               "telemetry": jsf._snap_telemetry(our) if our is not None
               else None}
        if row["banks"] is not None and row["error"] is None:
            try:
                e_us = jsf.end_reads(sinks[row["seat"]])
                e_opp = jsf.end_reads(sinks[1 - row["seat"]])
                row["tm_us"] = e_us.get("terminal_money")
                row["tm_opp"] = e_opp.get("terminal_money")
                if row["tm_us"] is not None and row["tm_opp"] is not None:
                    row["margin_clean"] = float(row["tm_us"]) - float(
                        row["tm_opp"])
            except Exception as exc:
                row["econ_error"] = repr(exc)[:100]
        rows.append(row)
    return rows


def play(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk_runs(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk_runs, tasks)
    rows = []
    for part in parts:
        rows.extend(part)
    return rows


def run_specs(specs, cfg):
    """去重跑口：同 (arm_path,seed,seat,opp_path) 只跑一次。"""
    out, todo = [], []
    for spec in specs:
        key = (spec["arm_path"], int(spec["seed"]), int(spec["our_seat"]),
               spec["opp_path"])
        if key in _ROW_CACHE:
            out.append(_ROW_CACHE[key])
        else:
            todo.append((key, spec))
    if todo:
        rows = play([s for _, s in todo], cfg)
        by_key = {}
        for row in rows:
            by_key.setdefault((row.get("seed"), row.get("seat"),
                              row.get("opponent")), []).append(row)
        for key, spec in todo:
            cand = by_key.get((int(spec["seed"]), int(spec["our_seat"]),
                              spec.get("opponent"))) or []
            row = cand.pop(0) if cand else {
                "seed": int(spec["seed"]), "seat": int(spec["our_seat"]),
                "arm": spec["arm"], "opponent": spec.get("opponent"),
                "error": "row_missing", "margin_clean": None}
            row.setdefault("block", spec.get("block"))
            row.setdefault("tag", spec.get("tag"))
            _ROW_CACHE[key] = row
            out.append(row)
    return out


def mk_specs(arm, arm_path, opp_path, opp_name, folds, block, seats=(0, 1)):
    specs = []
    for seed in folds:
        for seat in seats:
            specs.append({
                "game_id": "h1x-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


# ============================================================ 读数 ==
def pairs_from(rows_c, rows_v):
    """同 (seed,seat,opponent) 配对 margin 面（control=H1, variant=h1x）。"""
    key = lambda r: (r["seed"], r["seat"], r.get("opponent"))  # noqa: E731
    mc = {key(r): r for r in rows_c if r.get("margin_clean") is not None}
    mv = {key(r): r for r in rows_v if r.get("margin_clean") is not None}
    out = []
    for k in sorted(set(mc) & set(mv)):
        out.append((float(mc[k]["margin_clean"]), float(mv[k]["margin_clean"]),
                    k))
    return out


def flip_table(pairs):
    agg = jsf.flip_stats([(a, b) for a, b, _ in pairs])
    agg["pairs_detail"] = [
        {"seed": k[0], "seat": k[1], "opp": k[2],
         "margin_h1": round(a, 1), "margin_h1x": round(b, 1),
         "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold(rows):
    """judge_r44._fold_arm 双席折叠（jsf.fold_stats 包装）。"""
    try:
        return jsf.fold_stats(rows)
    except Exception as exc:
        return {"error": repr(exc)[:120]}


def h1x_telemetry(rows):
    tot = {}
    for r in rows:
        t = r.get("telemetry") or {}
        for k, v in t.items():
            if isinstance(v, (int, float)):
                tot[k] = tot.get(k, 0) + v
    return tot


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    build = json.load(open(HERE / "build" / "h1x" / "build_manifest.json"))
    EV.update({
        "version": "h1x/1.0",
        "task": "H1X=H1 王座基座+S8 尖拍捕获层：测是否超越王座（只测不发/不"
                "在线提交）",
        "design": {
            "formula": "H1X = H1(76b5f842…)+尖拍尾块（机制自 s8 a59208fe… "
                       "提取）挂 _hs_agent",
            "artifact": {"base": build["base"], "main": build["main"],
                         "tar": build["tar"], "entry": build["entry"],
                         "host": build["host_entry"]},
            "spike_params": build["spike_params"],
            "corpus": {
                "panel": "h1x vs {H1,oc_c3,mpx,r40,A}，12 fold（674000+"
                         "i*159,i=0..11）双席",
                "paired": "H1 控制臂 vs {oc_c3,mpx,r40,A} 同 (seed,seat,opp)"
                          " 配对（逐 unit delta）",
                "poison": "五毒种（674000/674141/674705/674987/675410）各 4 "
                          "局（{mpx,oc_c3}×双席）配对 H1 对照"},
            "caliber": {
                "margin": "终局钱 farms[obs.player] 差（干净口径）",
                "fold": "judge_r44._fold_arm 双席折叠（缺席/红局记负）",
                "flips": "同 (seed,seat,opp) 配对：H1 胜而 h1x 负记 flips_neg"
                         "；H1 负而 h1x 正记 flips_pos",
                "hard_currency": "胜率=硬通货；margin 只作参考"},
        },
        "gates": {"build": build["checks"],
                  "h1x_sha256": build["main"]["sha256"],
                  "tar_sha256": build["tar"]["sha256"]},
        "panel": {}, "paired_vs_h1": {}, "poison_seeds": {},
        "criteria": {}, "verdict": {},
    })
    flush_evid()

    # ---- sim_bridge 认证（复用 s1form 认证缓存）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_cache = KSIM_DIR / "orderbook_s1form_lab" / "evidence" / \
        "sim_auth_cache.json"
    if auth_cache.is_file():
        auth = json.loads(auth_cache.read_text(encoding="utf-8"))
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "degraded",
                      "degraded_reason", "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth = sb.sim_bridge({"n_games": 30, "min_checked": 30},
                             FOLDS[:8] + POISON_SEEDS)
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine")}
    EV["gates"]["sim_auth"] = auth_lite
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 冒烟 2 局 ----
    smoke = (mk_specs("h1x", H1X, PANEL["oc_c3"], "oc_c3", [FOLDS[0]],
                      "smoke", seats=(0,))
             + mk_specs("h1x", H1X, PANEL["H1"], "H1", [FOLDS[0]],
                        "smoke", seats=(0,)))
    run_specs(smoke, run_cfg)
    print("smoke done", flush=True)
    flush_evid()

    # ---- ① 面板：h1x vs 5 对手（12 fold 双席）----
    panel = {"design": "h1x vs {H1,oc_c3,mpx,r40,A}，12 fold（674000+i*159）"
                       "双席；fold=judge_r44._fold_arm",
             "pairs": {}}
    panel_rows = {}
    for on, opath in PANEL.items():
        rows = run_specs(mk_specs("h1x", H1X, opath, on, FOLDS, "panel"),
                         run_cfg)
        panel_rows[on] = rows
        panel["pairs"][on] = fold(rows)
        print("panel", on, panel["pairs"][on].get("h2h"), flush=True)
        flush_evid()
    EV["panel"] = panel

    # ---- ② 同块配对增量（vs H1 逐 unit delta）----
    ctrl_rows, paired = {}, {"design": "H1 控制臂 vs {oc_c3,mpx,r40,A} 同 "
                                       "(seed,seat,opp) 配对（12 fold 双席）；"
                                       "delta=h1x−H1", "per_opp": {}}
    for on in CONTROL_OPPS:
        ctrl_rows[on] = run_specs(
            mk_specs("h1", H1, PANEL[on], on, FOLDS, "control"), run_cfg)
    pr_all = []
    for on in CONTROL_OPPS:
        ps = pairs_from(ctrl_rows[on], panel_rows[on])
        pr_all.extend(ps)
        paired["per_opp"][on] = flip_table(ps)
        paired.setdefault("fold_h2h", {})[on] = {
            "H1": fold(ctrl_rows[on]), "h1x": fold(panel_rows[on])}
        print("paired", on, paired["per_opp"][on]["mean_delta"], flush=True)
    paired["all"] = flip_table(pr_all)
    EV["paired_vs_h1"] = paired
    flush_evid()

    # ---- ③ 毒种五枚（每枚 4 局配对 H1 对照）----
    po_c, po_v = [], []
    for seed in POISON_SEEDS:
        for on in POISON_OPPS:
            po_c += mk_specs("h1", H1, PANEL[on], on, [seed], "poison")
            po_v += mk_specs("h1x", H1X, PANEL[on], on, [seed], "poison")
    rows_poc = run_specs(po_c, run_cfg)
    rows_pov = run_specs(po_v, run_cfg)
    pairs_po = pairs_from(rows_poc, rows_pov)
    po = {"design": "五毒种各 4 局（{mpx,oc_c3}×双席）同 (seed,seat,opp) 配对"
                    " H1 对照；翻正=flips_pos（H1 负→h1x 正）",
          "flips_total": flip_table(pairs_po), "per_seed": {}}
    for seed in POISON_SEEDS:
        ps = [p for p in pairs_po if p[2][0] == seed]
        ft = flip_table(ps)
        po["per_seed"][str(seed)] = {
            "n_pairs": ft["n"], "flips_pos_翻正": ft["flips_pos"],
            "flips_neg_翻负": ft["flips_neg"], "mean_delta": ft["mean_delta"],
            "margins": [{"opp": p[2][2], "seat": p[2][1],
                         "h1": round(p[0], 1), "h1x": round(p[1], 1),
                         "delta": round(p[1] - p[0], 1)} for p in ps]}
    po["fold_h2h"] = {on: {"h1x": fold([r for r in rows_pov
                                        if r.get("opponent") == on]),
                           "H1": fold([r for r in rows_poc
                                       if r.get("opponent") == on])}
                      for on in POISON_OPPS}
    EV["poison_seeds"] = po
    print("poison done", flush=True)
    flush_evid()

    # ---- 尖拍层 telemetry（触发面）----
    all_h1x = [r for rows in panel_rows.values() for r in rows] + rows_pov
    EV["h1x_layer_telemetry"] = {
        "panel_and_poison": h1x_telemetry(all_h1x),
        "note": "spike_item_ticks=尖拍触发品·拍数；append/topup=②③ 收回量；"
                "skip_full_decl=本轮已满申报跳过；errors=异常回退"}

    # ---- 判据 + verdict ----
    h_h1 = (panel["pairs"].get("H1") or {}).get("h2h")
    flips_neg_panel = paired["all"].get("flips_neg", 0)
    flips_neg_poison = po["flips_total"].get("flips_neg", 0)
    flips_neg = flips_neg_panel + flips_neg_poison
    po_keep = bool(flips_neg_poison == 0
                   and po["flips_total"].get("win_variant", 0)
                   >= po["flips_total"].get("win_control", 0)
                   and (po["flips_total"].get("mean_delta") or 0) >= 0)
    c1 = bool(h_h1 is not None and h_h1 >= 0.5)
    c2 = bool(flips_neg <= 2)
    c3 = po_keep
    full = bool(c1 and c2 and c3)
    EV["criteria"] = {
        "rule": "h1x vs H1 h2h ≥0.5 且 flips_neg≤2 且毒种翻正保持 → "
                "超越王座候选成立",
        "c1_h2h_vs_H1_ge_0.5": {"h2h": h_h1,
                                "fold": panel["pairs"].get("H1"),
                                "passed": c1},
        "c2_flips_neg_le_2": {"flips_neg_panel": flips_neg_panel,
                              "flips_neg_poison": flips_neg_poison,
                              "flips_neg_total": flips_neg, "passed": c2},
        "c3_poison_flip_maintained": {
            "operationalization": "毒种配对 flips_neg==0 ∧ h1x 胜局数≥H1 胜局"
                                  "数 ∧ mean_delta≥0（翻正随层迁移且不回退）",
            "flips_pos": po["flips_total"].get("flips_pos"),
            "flips_neg": flips_neg_poison,
            "win_h1": po["flips_total"].get("win_control"),
            "win_h1x": po["flips_total"].get("win_variant"),
            "mean_delta": po["flips_total"].get("mean_delta"),
            "passed": c3},
    }
    EV["verdict"] = {
        "h2h_vs_H1": h_h1,
        "panel_h2h": {k: v.get("h2h") for k, v in panel["pairs"].items()},
        "paired_vs_h1": {"W": paired["all"].get("W"),
                         "L": paired["all"].get("L"),
                         "T": paired["all"].get("T"),
                         "mean_delta": paired["all"].get("mean_delta"),
                         "flips_pos": paired["all"].get("flips_pos"),
                         "flips_neg": flips_neg_panel},
        "poison": {"flips_pos": po["flips_total"].get("flips_pos"),
                   "flips_neg": flips_neg_poison,
                   "mean_delta": po["flips_total"].get("mean_delta"),
                   "per_seed_flips_pos": {k: v["flips_pos_翻正"]
                                          for k, v in po["per_seed"].items()}},
        "criteria_passed": full,
        "verdict": ("超越王座候选成立" if full else
                    "未成立（如实报）：c1=%s c2=%s c3=%s" % (c1, c2, c3)),
        "summary": "H1X[%s]：vs H1 h2h %s；面板 %s；配对增量 W/L/T %s/%s/%s "
                   "mean %s（flips +%s/-%s）；毒种翻正 %s/-%s mean %s；判据 %s"
                   % (build["main"]["sha256"][:8], h_h1,
                      json.dumps({k: v.get("h2h")
                                  for k, v in panel["pairs"].items()},
                                 default=str),
                      paired["all"].get("W"), paired["all"].get("L"),
                      paired["all"].get("T"), paired["all"].get("mean_delta"),
                      paired["all"].get("flips_pos"), flips_neg_panel,
                      po["flips_total"].get("flips_pos"), flips_neg_poison,
                      po["flips_total"].get("mean_delta"), full),
        "launch": "只测不发（在线提交=硬禁令）；发射决策移交用户",
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE)
    BUDGET["total_局次"] = 30 + len(_ROW_CACHE)
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货，"
        "margin 只作参考")
    ANOMALIES.append(
        "同块配对读增量（s3 教训）；块=674000+i*159(i=0..11)（可比 S8 行）；"
        "毒种 674000 与面板块重合单元经缓存去重")
    ANOMALIES.append(
        "毒种翻正保持口径：flips_neg==0 ∧ win_h1x≥win_H1 ∧ mean_delta≥0；"
        "S8 基线=同块 20/20 单元 delta>0、6 个符号翻正（vs s_append）")
    ANOMALIES.append(
        "sim_bridge 认证复用 s1form 缓存（consistency_ok）按 30 计账；"
        "预算局次=auth+去重后实跑局数")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", EV["verdict"]["summary"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
