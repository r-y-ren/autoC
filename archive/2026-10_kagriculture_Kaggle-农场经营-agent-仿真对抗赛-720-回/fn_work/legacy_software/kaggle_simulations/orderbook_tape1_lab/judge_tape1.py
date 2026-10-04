# -*- coding: utf-8 -*-
"""judge_tape1（tape1 lab）：day0 做市单加重磁带变体快筛（只测不发/不在线提交）。

对象：h1x_t_lite/h1x_t_mid/h1x_t_heavy（build_tape1.py 五门产物）挂 H1X
（9d073fba…）基座；胜者同手术移植 S8（a59208fe…）基座（s8_t_*）。
块=674000+i*159；judge_r44._fold_arm 双席折叠；margin=farms[obs.player] 终局钱差。

设计（判据↔面板一一对应；配对增量=h1x_verdict 在册同键控制臂复用+2 局确定性抽查）：
  每档 12 fold 双席 vs {oc_c3（王座/冠军锚）、r40、A（弱锚）} + 8 fold 双席
  vs {tetsutani（稳节奏 step1009 族）、H1（V82 镜像=h1_mirror 画像族）}；
  配对增量读 H1X 本体同 (seed,seat,opp) 控制臂（oc_c3/r40/A=h1x_verdict
  pairs_detail.margin_h1x 在册复用；tetsutani/H1=本程新跑 16+16 局）。
判据（全过→发射候选成立）：
  c1 配对 delta>0 且 flips_neg=0（全对手单元聚合）
  c2 对王座锚 ≥0.5（vs oc_c3 fold h2h）
  c3 弱锚 ≥0.8 不失守（vs r40 与 vs A 各）
  c4 稳节奏面无显著负（tetsutani 配对 flips_neg=0 且 mean_delta≥0）
  c5 镜像面非毒（H1 配对 flips_neg=0 且 mean_delta≥0）
胜者移植（S8 面板精简）：win_s8 vs {S8 本体配对、oc_c3、r40} 8 fold 双席，
  同口径判据 s1/s2/s3。
预算 ≤450 局次（auth 30 + 去重实跑 410 + 确定性双跑抽查 2 = 442）。
sim_bridge 认证缓存复用；证据 evidence/tape1_verdict.json。绝不在线提交。
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
H1X = KSIM_DIR / "orderbook_h1x_lab" / "build" / "h1x" / "main.py"
S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
TIER_ORDER = ["t_lite", "t_mid", "t_heavy"]
ARMS = {t: HERE / "build" / ("h1x_%s" % t) / "main.py" for t in TIER_ORDER}
S8_ARMS = {t: HERE / "build" / ("s8_%s" % t) / "main.py" for t in TIER_ORDER}
PANEL = {
    "oc_c3": KSIM_DIR / "orderbook_oppcond_lab" / "build" / "oc_c3"
    / "main.py",
    "r40": KSIM_DIR / "orderbook_r40" / "build" / "main.py",
    "A": KSIM_DIR / "orderbook_r44_a" / "main.py",
    "tetsutani": KSIM_DIR / "orderbook_racegap_lab" / "opponents" / "tetsu1009"
    / "main.py",
    "H1": KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py",
}
ANCHOR = "oc_c3"            # 王座/冠军锚（任务允许 oc_c3 或 H1；oc_c3=在册主尺）
WEAK = ("r40", "A")
STEADY = "tetsutani"        # 稳节奏代表（S9 教训 step1009 族）
MIRROR = "H1"               # V82 镜像（h1_mirror 画像族基座）
PAIRED_OPPS_12 = ("oc_c3", "r40", "A")
PAIRED_OPPS_8 = ("tetsutani", "H1")
FOLDS_12 = [674000 + i * 159 for i in range(12)]
FOLDS_8 = FOLDS_12[:8]
WORKERS = 4
BUDGET_CAP = 450

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 30,
          "panel_规格": 3 * (3 * 24 + 2 * 16),
          "control_新跑_规格": 32, "spotcheck_规格": 2,
          "s8_移植_规格": 64, "det_双跑抽查": 2,
          "probe_prior": 5,
          "probe_note": "手术实证试跑 5 局（build 定型前：base/lite/heavy×oc_c3 "
                        "674000-s0 + 定型复核 lite/heavy 同键）计入总账"}
_ROW_CACHE = {}


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "tape1_verdict.json").write_text(
        json.dumps(EV, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱 farms[obs.player]（judge_h1x 同源口径）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    rows, metas = [], []
    games = []
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


def run_specs(specs, cfg, use_cache=True):
    """去重跑口：同 (arm_path,seed,seat,opp_path) 只跑一次（use_cache=False 双跑抽查）。"""
    out, todo = [], []
    for spec in specs:
        key = (spec["arm_path"], int(spec["seed"]), int(spec["our_seat"]),
               spec["opp_path"])
        if use_cache and key in _ROW_CACHE:
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
            if use_cache:
                _ROW_CACHE[key] = row
            out.append(row)
    return out


def mk_specs(arm, arm_path, opp_path, opp_name, folds, block, seats=(0, 1)):
    specs = []
    for seed in folds:
        for seat in seats:
            specs.append({
                "game_id": "tape1-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


# ============================================================ 读数 ==
def pairs_from(rows_c, rows_v):
    """同 (seed,seat,opponent) 配对 margin 面（control=H1X 本体, variant=档件）。"""
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
         "margin_base": round(a, 1), "margin_variant": round(b, 1),
         "delta": round(b - a, 1)}
        for a, b, k in pairs]
    return agg


def fold(rows):
    try:
        return jsf.fold_stats(rows)
    except Exception as exc:
        return {"error": repr(exc)[:120]}


def load_reused_controls():
    """h1x_verdict.json 在册控制臂：margin_h1x @ (seed,seat,opp)→H1X 本体行。"""
    path = KSIM_DIR / "orderbook_h1x_lab" / "evidence" / "h1x_verdict.json"
    d = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for on in PAIRED_OPPS_12:
        det = ((d.get("paired_vs_h1") or {}).get("per_opp") or {}).get(on) \
            or {}
        for u in det.get("pairs_detail") or []:
            rows.append({"seed": int(u["seed"]), "seat": int(u["seat"]),
                         "opponent": on, "arm": "h1x",
                         "margin_clean": float(u["margin_h1x"]),
                         "tm_us": None, "tm_opp": None,
                         "tag": "reused_control"})
    return rows


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)

    builds = {}
    for t in TIER_ORDER:
        builds[t] = json.loads((HERE / "build" / ("h1x_%s" % t)
                                / "build_manifest.json").read_text(
            encoding="utf-8"))
    EV.update({
        "version": "tape1/1.0",
        "task": "day0 做市单加重磁带变体（分析50 P1 台阶一）：值不值得在截止前"
                "（09-30 23:59 UTC）发射（只测不发/在线提交=硬禁令）",
        "tape_location": {
            "band_fingerprint": "band-deepcut §4 我方行 s1 [BUY 6-10|SELL 3-5|"
                                "BUY_SEED 1-2]、s2 [HIRE×5|COW|SHEEP]"
                                "= main.py tape step0/1（fingerprint 索引 +1）",
            "generator_chain": "_R108_DATA route0 磁带 → _R42_OPENING（s0="
                               "13/30/30）→ _v9_opening（step0→V9_OPENING_STEP0="
                               "(BUY 8,SELL 3)、step1 剥麦单）→ _alt_install "
                               "'HybridOpening'（+BUY_SEED WHEAT 1）→ "
                               "opening_liquidity_agent 断言 [BUY 8,SELL 3,"
                               "BUY_SEED 1]",
            "surgery_block": "V9_OPENING_STEP0 常量 + opening_liquidity_agent"
                             "（step1 churn 注入）单块替换，其余字节=基座逐字"},
        "design": {
            "variants": {t: {"params": builds[t]["params"],
                             "groove": builds[t]["groove"],
                             "main_sha256": builds[t]["main"]["sha256"],
                             "tar_sha256": builds[t]["tar"]["sha256"]}
                         for t in TIER_ORDER},
            "corpus": "块 674000+i*159：主面板 12 fold 双席 vs {oc_c3(王座/冠军"
                      "锚),r40,A(弱锚)}；稳节奏 tetsutani 与 V82 镜像 H1 各 8 "
                      "fold 双席；配对增量=H1X 本体同 (seed,seat,opp) 控制臂",
            "caliber": {"margin": "终局钱 farms[obs.player] 差（干净口径）",
                        "fold": "judge_r44._fold_arm 双席折叠",
                        "flips": "同 (seed,seat,opp)：H1X 本体胜而档件负记 "
                                 "flips_neg；反之 flips_pos"},
            "control_reuse": "H1X 控制臂 oc_c3/r40/A 单元复用 h1x_verdict.json"
                             " pairs_detail.margin_h1x（同块同口径在册）；"
                             "tetsutani/H1 新跑",
        },
        "criteria": {
            "rule": "c1 配对 delta>0 且 flips_neg=0；c2 对王座锚 ≥0.5；c3 弱锚 "
                    "≥0.8 不失守；c4 稳节奏面无显著负（flips_neg=0）；c5 镜像面"
                    "非毒——全过→发射候选成立"},
        "panel": {}, "paired_vs_h1x": {}, "steady_face": {}, "mirror_face": {},
        "s8_transplant": {}, "verdict": {},
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
                      "engine", "version", "wall_speedup")}
        auth_lite["reused_cache"] = True
    else:
        auth = sb.sim_bridge({"n_games": 30, "min_checked": 30},
                             FOLDS_12[:8])
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine")}
    EV["gates"] = {"sim_auth": auth_lite}
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- 冒烟 2 局（吸收进面板同键去重）----
    smoke = (mk_specs("h1x_t_lite", ARMS["t_lite"], PANEL["oc_c3"], "oc_c3",
                      [FOLDS_12[0]], "smoke", seats=(0,))
             + mk_specs("h1x_t_lite", ARMS["t_lite"], PANEL["H1"], "H1",
                        [FOLDS_12[0]], "smoke", seats=(0,)))
    run_specs(smoke, run_cfg)
    print("smoke done", flush=True)
    flush_evid()

    # ---- 在册控制臂复用 + 2 局确定性抽查 ----
    reused = load_reused_controls()
    EV["gates"]["control_reuse"] = {
        "n_rows": len(reused),
        "source": "orderbook_h1x_lab/evidence/h1x_verdict.json "
                  "paired_vs_h1.per_opp[*].pairs_detail.margin_h1x"}
    spot = mk_specs("h1x", H1X, PANEL["oc_c3"], "oc_c3",
                    [FOLDS_12[0], FOLDS_12[2]], "spotcheck", seats=(0, 1))[:2]
    spot_rows = run_specs(spot, run_cfg)
    spot_pairs = pairs_from(reused, spot_rows)
    spot_ok = len(spot_pairs) == 2 and all(
        abs(a - b) <= 1e-6 for a, b, _ in spot_pairs)
    EV["gates"]["det_spotcheck"] = {
        "units": [{"seed": k[0], "seat": k[1], "opp": k[2],
                   "margin_reused": round(a, 1), "margin_rerun": round(b, 1)}
                  for a, b, k in spot_pairs], "match": spot_ok}
    # 确定性双跑抽查：同 2 局无缓存再跑一遍
    det_rows = run_specs(spot, run_cfg, use_cache=False)
    det_pairs = pairs_from(spot_rows, det_rows)
    det_ok = len(det_pairs) == 2 and all(
        abs(a - b) <= 1e-6 for a, b, _ in det_pairs)
    EV["gates"]["det_double_run"] = {"match": det_ok, "n": len(det_pairs)}
    if not (spot_ok and det_ok):
        ANOMALIES.append("控制臂复用抽查或确定性双跑不一致——配对读数降级为方向性")
    ANOMALIES.append("harness 噪声不修不管；胜率=硬通货，margin 只作参考")
    ANOMALIES.append("块=674000+i*159（可比 S8/H1X 在册行）；同块配对读增量"
                     "（s3 教训）")
    flush_evid()

    # ---- ① 三档面板 + 配对（vs H1X 本体控制臂）----
    ctrl_rows_12 = reused
    ctrl_rows_8 = {}
    for on in PAIRED_OPPS_8:
        ctrl_rows_8[on] = run_specs(
            mk_specs("h1x", H1X, PANEL[on], on, FOLDS_8, "control8"), run_cfg)
    print("shared controls done", flush=True)
    flush_evid()

    panel_rows = {}
    for t in TIER_ORDER:
        arm, apath = "h1x_" + t, ARMS[t]
        panel_rows[t], paired = {}, {"design": "档件 vs H1X 本体同 "
                                               "(seed,seat,opp) 配对增量",
                                     "per_opp": {}}
        for on in PAIRED_OPPS_12:
            rows = run_specs(mk_specs(arm, apath, PANEL[on], on, FOLDS_12,
                                      "panel12"), run_cfg)
            panel_rows[t][on] = rows
            ps = pairs_from(ctrl_rows_12, rows)
            paired["per_opp"][on] = flip_table(ps)
            EV["panel"].setdefault(t, {})[on] = fold(rows)
            print("panel", t, on, EV["panel"][t][on].get("h2h"), flush=True)
        for on in PAIRED_OPPS_8:
            rows = run_specs(mk_specs(arm, apath, PANEL[on], on, FOLDS_8,
                                      "panel8"), run_cfg)
            panel_rows[t][on] = rows
            ps = pairs_from(ctrl_rows_8[on], rows)
            paired["per_opp"][on] = flip_table(ps)
            EV["panel"].setdefault(t, {})[on] = fold(rows)
        pr_all = []
        for on in PAIRED_OPPS_12 + PAIRED_OPPS_8:
            pr_all.extend(pairs_from(
                ctrl_rows_12 if on in PAIRED_OPPS_12 else ctrl_rows_8[on],
                panel_rows[t][on]))
        paired["all"] = flip_table(pr_all)
        EV["paired_vs_h1x"][t] = paired
        EV["steady_face"][t] = {
            "opp": STEADY, "fold": EV["panel"][t][STEADY],
            "paired": paired["per_opp"][STEADY]}
        EV["mirror_face"][t] = {
            "opp": MIRROR, "fold": EV["panel"][t][MIRROR],
            "paired": paired["per_opp"][MIRROR]}
        print("paired", t, paired["all"]["mean_delta"],
              "flips_neg", paired["all"]["flips_neg"], flush=True)
        flush_evid()

    # ---- 判据 + 胜者 ----
    crit = {}
    for t in TIER_ORDER:
        pa = EV["paired_vs_h1x"][t]["all"]
        h_anchor = (EV["panel"][t].get(ANCHOR) or {}).get("h2h")
        h_weak = {w: (EV["panel"][t].get(w) or {}).get("h2h") for w in WEAK}
        st = EV["steady_face"][t]["paired"]
        mi = EV["mirror_face"][t]["paired"]
        c1 = bool((pa.get("mean_delta") or 0) > 0 and pa.get("flips_neg") == 0)
        c2 = bool(h_anchor is not None and h_anchor >= 0.5)
        c3 = bool(all(v is not None and v >= 0.8 for v in h_weak.values()))
        c4 = bool(st.get("flips_neg") == 0 and (st.get("mean_delta") or 0) >= 0)
        c5 = bool(mi.get("flips_neg") == 0 and (mi.get("mean_delta") or 0) >= 0)
        crit[t] = {
            "c1_paired_delta_pos_flips0": {"mean_delta": pa.get("mean_delta"),
                                           "flips_neg": pa.get("flips_neg"),
                                           "W/L/T": [pa.get("W"), pa.get("L"),
                                                     pa.get("T")],
                                           "passed": c1},
            "c2_anchor_h2h_ge_0.5": {"opp": ANCHOR, "h2h": h_anchor,
                                     "passed": c2},
            "c3_weak_h2h_ge_0.8": {"h2h": h_weak, "passed": c3},
            "c4_steady_no_neg": {"opp": STEADY,
                                 "flips_neg": st.get("flips_neg"),
                                 "mean_delta": st.get("mean_delta"),
                                 "passed": c4},
            "c5_mirror_nontoxic": {"opp": MIRROR,
                                   "flips_neg": mi.get("flips_neg"),
                                   "mean_delta": mi.get("mean_delta"),
                                   "h2h": (EV["panel"][t].get(MIRROR)
                                           or {}).get("h2h"),
                                   "passed": c5},
            "all_pass": bool(c1 and c2 and c3 and c4 and c5),
            "groove_flag": builds[t]["groove"]["flag"],
        }
    EV["tier_criteria"] = crit
    winners = [t for t in TIER_ORDER if crit[t]["all_pass"]]
    if winners:
        win = max(winners, key=lambda t: EV["paired_vs_h1x"][t]["all"]
                  ["mean_delta"])
    else:
        win = max(TIER_ORDER, key=lambda t: EV["paired_vs_h1x"][t]["all"]
                  ["mean_delta"])
    EV["winner"] = {"tier": win, "among_pass": winners,
                    "rule": "全判据过者中取配对 mean_delta 最大；无一全过则取"
                            "最大者仅供判读（不构成发射候选）"}
    flush_evid()

    # ---- ② 胜者移植 S8（精简面板：S8 本体配对/王座锚/弱锚 r40，8 fold 双席）----
    s8_rows = {}
    s8_ctrl = {}
    for on in (ANCHOR, "r40"):
        s8_ctrl[on] = run_specs(
            mk_specs("s8", S8, PANEL[on], on, FOLDS_8, "s8_control"), run_cfg)
        s8_rows[on] = run_specs(
            mk_specs("s8_" + win, S8_ARMS[win], PANEL[on], on, FOLDS_8,
                     "s8_panel"), run_cfg)
    sp = {"design": "s8_%s vs S8 本体同 (seed,seat,opp) 配对（8 fold 双席）"
                    % win, "per_opp": {}}
    pr = []
    for on in (ANCHOR, "r40"):
        ps = pairs_from(s8_ctrl[on], s8_rows[on])
        sp["per_opp"][on] = flip_table(ps)
        pr.extend(ps)
        sp.setdefault("fold_h2h", {})[on] = {
            "win_s8": fold(s8_rows[on]), "s8_base": fold(s8_ctrl[on])}
    sp["all"] = flip_table(pr)
    EV["s8_transplant"] = {
        "tier": win, "main_sha256": json.loads(
            (HERE / "build" / ("s8_%s" % win) / "build_manifest.json")
            .read_text(encoding="utf-8"))["main"]["sha256"],
        "paired_vs_s8_base": sp,
        "criteria": {
            "s1_paired_delta_pos_flips0": {
                "mean_delta": sp["all"].get("mean_delta"),
                "flips_neg": sp["all"].get("flips_neg"),
                "passed": bool((sp["all"].get("mean_delta") or 0) > 0
                               and sp["all"].get("flips_neg") == 0)},
            "s2_anchor_h2h_ge_0.5": {
                "h2h": sp["fold_h2h"][ANCHOR]["win_s8"].get("h2h"),
                "passed": bool((sp["fold_h2h"][ANCHOR]["win_s8"].get("h2h")
                                or 0) >= 0.5)},
            "s3_weak_r40_h2h_ge_0.8": {
                "h2h": sp["fold_h2h"]["r40"]["win_s8"].get("h2h"),
                "passed": bool((sp["fold_h2h"]["r40"]["win_s8"].get("h2h")
                                or 0) >= 0.8)},
        },
    }
    EV["s8_transplant"]["all_pass"] = all(
        v["passed"] for v in EV["s8_transplant"]["criteria"].values())
    print("s8 transplant done", EV["s8_transplant"]["criteria"], flush=True)
    flush_evid()

    # ---- 总判读 ----
    full = crit[win]["all_pass"] if win in winners else False
    s8_full = EV["s8_transplant"]["all_pass"]
    EV["verdict"] = {
        "tier_criteria": {t: crit[t]["all_pass"] for t in TIER_ORDER},
        "winner": win,
        "h1x_launch_candidate": bool(full),
        "s8_launch_candidate": bool(s8_full),
        "verdict": ("发射候选成立（档件 %s；%s）" % (
            win, "S8 移植同过" if s8_full else "S8 移植未过"))
            if (full or s8_full) else
            "发射候选不成立（如实报）：H1X 面全过=%s，S8 面全过=%s"
            % (full, s8_full),
        "launch": "只测不发（在线提交=硬禁令）；发射决策移交用户",
        "summary": "tape1[%s]：配对 delta %s（flips +%s/-%s）；王座锚 %s；弱锚 "
                   "%s；稳节奏 %s；镜像 %s；S8 移植配对 %s" % (
                       win, EV["paired_vs_h1x"][win]["all"].get("mean_delta"),
                       EV["paired_vs_h1x"][win]["all"].get("flips_pos"),
                       EV["paired_vs_h1x"][win]["all"].get("flips_neg"),
                       crit[win]["c2_anchor_h2h_ge_0.5"]["h2h"],
                       crit[win]["c3_weak_h2h_ge_0.8"]["h2h"],
                       crit[win]["c4_steady_no_neg"]["mean_delta"],
                       crit[win]["c5_mirror_nontoxic"]["mean_delta"],
                       EV["s8_transplant"]["paired_vs_s8_base"]["all"]
                       .get("mean_delta")),
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE) + 2  # +确定性双跑 2 局
    BUDGET["total_局次"] = 30 + BUDGET["unique_games_run"] + \
        BUDGET.get("probe_prior", 0)
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP
    ANOMALIES.append("t_heavy 破 groove 约束（step2 净麦 0≠−5）已标注，按任务令"
                     "单独测；修回形（买 27/28 或卖 45）留档未取")
    ANOMALIES.append("S8 面板 8 fold 精简（任务允许）；稳节奏/镜像各 8 fold")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", EV["verdict"]["summary"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
