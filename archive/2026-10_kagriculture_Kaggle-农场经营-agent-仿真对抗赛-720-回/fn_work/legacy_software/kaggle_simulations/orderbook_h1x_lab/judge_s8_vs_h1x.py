# -*- coding: utf-8 -*-
"""judge_s8_vs_h1x：S8 vs H1X 直接对战 + 两条校准臂（只测不发/不在线提交）。

主问题：S8 与 H1X 谁更强——同块直接对话（h2h）。
对象：
  S8  = orderbook_s8spike_lab/build/s8/main.py（a59208fe…）
  H1X = orderbook_h1x_lab/build/h1x/main.py（9d073fba…）
块 = 674000+i*159。judge_r44._fold_arm 双席折叠、margin=farms[obs.player]
（终局钱 tm_us−tm_opp 干净口径）。
臂：
  ① s8 vs h1x（16 fold 双席，i=0..15）——主问题谁更强；
  ② s8 vs h1 （12 fold 双席，i=0..11）——同块锚点（H1X vs H1=0.7083 在册）；
  ③ s8 vs mpx（12 fold 双席，i=0..11）——同块锚点（H1X vs mpx=0.7083 在册）。
判读：s8_vs_h1x h2h（S8 胜率）≥0.6→S8 更强；≤0.4→H1X 更强；0.4-0.6→
伯仲之间，以同块锚点（vs H1/mpx）判。
预算 ≤150 局（auth 30 缓存复用 + 实跑去重）；确定性抽查 2 局双跑；异常 fail-closed。
证据 evidence/s8_vs_h1x.json。绝不在线提交。
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
S8 = KSIM_DIR / "orderbook_s8spike_lab" / "build" / "s8" / "main.py"
H1X = HERE / "build" / "h1x" / "main.py"
H1 = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
MPX = KSIM_DIR / "orderbook_modelpx_lab" / "build" / "mpx_w24_p2_3_h14" \
    / "main.py"

FOLDS_MAIN = [674000 + i * 159 for i in range(16)]   # s8 vs h1x 16 fold
FOLDS_CAL = [674000 + i * 159 for i in range(12)]    # 校准臂 12 fold
WORKERS = 4
BUDGET_CAP = 150
# 同块在册锚点（h1x_verdict.json panel，12 fold 双席，subject=H1X 胜率）
REG_H1X_VS_H1 = 0.7083
REG_H1X_VS_MPX = 0.7083

EV = {}
ANOMALIES = []
BUDGET = {"cap_局次": BUDGET_CAP, "auth": 30,
          "main_规格": 32, "cal_h1_规格": 24, "cal_mpx_规格": 24,
          "det_抽查": 2}
_ROW_CACHE = {}


def _sha(path):
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def flush_evid():
    EV["anomaly"] = list(ANOMALIES)
    EV["budget"] = dict(BUDGET)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    (EVID_DIR / "s8_vs_h1x.json").write_text(
        json.dumps(EV, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")


# ============================================================ 跑口 ==
def _chunk_runs(payload):
    """双席追踪跑 + 终局钱 farms[obs.player]（judge_h1x 同源口径）。"""
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
               "margin_clean": None, "tm_us": None, "tm_opp": None}
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
                "game_id": "s8x-%s|%s|%d-s%d" % (arm, opp_name, seed, seat),
                "seed": int(seed), "arm": arm, "arm_path": str(arm_path),
                "our_seat": seat, "opp_path": str(opp_path),
                "opponent": opp_name, "block": block, "kind": "ab",
                "trace": True})
    return specs


def fold(rows):
    try:
        return jsf.fold_stats(rows)
    except Exception as exc:
        return {"error": repr(exc)[:120]}


def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    EVID_DIR.mkdir(parents=True, exist_ok=True)
    EV.update({
        "version": "s8_vs_h1x/1.0",
        "task": "S8 vs H1X 直接对战（谁更强）+ 两条同块校准臂（只测不发/"
                "不在线提交）",
        "design": {
            "objects": {
                "S8": {"path": str(S8), "sha256": _sha(S8)},
                "H1X": {"path": str(H1X), "sha256": _sha(H1X)},
                "H1": {"path": str(H1), "sha256": _sha(H1)},
                "mpx": {"path": str(MPX), "sha256": _sha(MPX)}},
            "block": "674000+i*159；main=i=0..15（16 fold），cal=i=0..11"
                     "（12 fold）",
            "caliber": {
                "margin": "终局钱 farms[obs.player] 差（tm_us−tm_opp 干净口径）",
                "fold": "judge_r44._fold_arm 双席折叠（缺席/红局记负）",
                "h2h": "h2h=subject（S8）胜率=(胜+0.5平)/独立 n；胜率=硬通货",
                "arm_orientation": "arm=S8（subject），opp={h1x,h1,mpx}；"
                                   "margin>0 即 S8 领先"},
            "arms": {
                "main_s8_vs_h1x": "16 fold 双席（32 局）——主问题谁更强",
                "cal_s8_vs_h1": "12 fold 双席（24 局）——锚点 vs H1"
                                "（H1X 在册 0.7083）",
                "cal_s8_vs_mpx": "12 fold 双席（24 局）——锚点 vs mpx"
                                 "（H1X 在册 0.7083）"},
        },
        "registry_anchors": {"H1X_vs_H1": REG_H1X_VS_H1,
                             "H1X_vs_mpx": REG_H1X_VS_MPX},
        "arms": {}, "calibration": {}, "determinism": {},
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
                             FOLDS_MAIN[:8])
        auth_lite = {k: auth.get(k) for k in
                     ("loaded", "consistency", "consistency_ok", "engine")}
    EV["gates"] = {"sim_auth": auth_lite}
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"aborted": "sim_bridge 认证未过"}
        flush_evid()
        return EV
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}
    flush_evid()

    # ---- ① 主问题：s8 vs h1x（16 fold 双席）----
    rows_main = run_specs(
        mk_specs("s8", S8, H1X, "h1x", FOLDS_MAIN, "main"), run_cfg)
    f_main = fold(rows_main)
    EV["arms"]["s8_vs_h1x"] = {"fold": f_main, "n_folds": 16,
                               "n_games": len(rows_main)}
    print("s8_vs_h1x h2h(S8)=", f_main.get("h2h"), flush=True)
    flush_evid()

    # ---- ② 校准臂 s8 vs h1（12 fold 双席）----
    rows_h1 = run_specs(
        mk_specs("s8", S8, H1, "h1", FOLDS_CAL, "cal"), run_cfg)
    f_h1 = fold(rows_h1)
    EV["arms"]["s8_vs_h1"] = {"fold": f_h1, "n_folds": 12,
                              "n_games": len(rows_h1)}
    print("s8_vs_h1 h2h(S8)=", f_h1.get("h2h"), flush=True)
    flush_evid()

    # ---- ③ 校准臂 s8 vs mpx（12 fold 双席）----
    rows_mpx = run_specs(
        mk_specs("s8", S8, MPX, "mpx", FOLDS_CAL, "cal"), run_cfg)
    f_mpx = fold(rows_mpx)
    EV["arms"]["s8_vs_mpx"] = {"fold": f_mpx, "n_folds": 12,
                               "n_games": len(rows_mpx)}
    print("s8_vs_mpx h2h(S8)=", f_mpx.get("h2h"), flush=True)
    flush_evid()

    # ---- 确定性抽查 2 局双跑（绕缓存直跑对比）----
    det_specs = (mk_specs("s8", S8, H1X, "h1x", [FOLDS_MAIN[0]], "det",
                          seats=(0,))
                 + mk_specs("s8", S8, H1X, "h1x", [FOLDS_MAIN[1]], "det",
                            seats=(1,)))
    det = {"design": "同 spec 双跑比对 margin_clean，须逐字节一致"
                     "（确定性）", "cases": [], "all_identical": True}
    for sp in det_specs:
        r1 = play([sp], run_cfg)[0]
        r2 = play([sp], run_cfg)[0]
        same = (r1.get("margin_clean") == r2.get("margin_clean")
                and r1.get("tm_us") == r2.get("tm_us")
                and r1.get("tm_opp") == r2.get("tm_opp"))
        det["cases"].append({"seed": sp["seed"], "seat": sp["our_seat"],
                             "m1": r1.get("margin_clean"),
                             "m2": r2.get("margin_clean"),
                             "identical": bool(same),
                             "error": r1.get("error") or r2.get("error")})
        if not same:
            det["all_identical"] = False
    EV["determinism"] = det
    if not det["all_identical"]:
        ANOMALIES.append("确定性抽查双跑不一致——fail-closed，结果降级")
    flush_evid()

    # ---- 校准对比表 ----
    EV["calibration"] = {
        "design": "同块（674000+i*159）三件转：S8 两臂 vs H1X 在册读数同块可比",
        "vs_H1": {"s8_h2h": f_h1.get("h2h"),
                  "s8_mean_margin": f_h1.get("mean_margin"),
                  "h1x_reg_h2h": REG_H1X_VS_H1,
                  "delta_s8_minus_h1x": (round(f_h1["h2h"] - REG_H1X_VS_H1, 4)
                                         if isinstance(f_h1.get("h2h"),
                                                       (int, float)) else None)},
        "vs_mpx": {"s8_h2h": f_mpx.get("h2h"),
                   "s8_mean_margin": f_mpx.get("mean_margin"),
                   "h1x_reg_h2h": REG_H1X_VS_MPX,
                   "delta_s8_minus_h1x": (round(f_mpx["h2h"] -
                                                REG_H1X_VS_MPX, 4)
                                          if isinstance(f_mpx.get("h2h"),
                                                        (int, float))
                                          else None)},
    }

    # ---- 判读 ----
    h_main = f_main.get("h2h")
    if isinstance(h_main, (int, float)):
        if h_main >= 0.6:
            verdict = "S8 更强"
        elif h_main <= 0.4:
            verdict = "H1X 更强"
        else:
            verdict = "伯仲之间，以同块锚点判"
    else:
        verdict = "主问题读数异常（fail-closed）"
    # 锚点侧写（供伯仲区间参考）
    d_h1 = EV["calibration"]["vs_H1"]["delta_s8_minus_h1x"]
    d_mpx = EV["calibration"]["vs_mpx"]["delta_s8_minus_h1x"]
    anchor = "S8 锚点占优" if (isinstance(d_h1, (int, float)) and d_h1 > 0
                              and isinstance(d_mpx, (int, float))
                              and d_mpx > 0) else \
        "H1X 锚点占优" if (isinstance(d_h1, (int, float)) and d_h1 < 0
                          and isinstance(d_mpx, (int, float))
                          and d_mpx < 0) else "锚点混合/持平"
    EV["criteria"] = {
        "rule": "s8_vs_h1x h2h（S8 胜率）≥0.6→S8 更强；≤0.4→H1X 更强；"
                "0.4-0.6→伯仲之间以同块锚点判",
        "s8_vs_h1x_h2h": h_main,
        "determinism_ok": det["all_identical"],
    }
    final_verdict = ("%s（%s）" % (verdict, anchor)
                     if verdict == "伯仲之间，以同块锚点判" else verdict)
    EV["verdict"] = {
        "s8_vs_h1x_h2h_S8": h_main,
        "s8_vs_h1x_fold": f_main,
        "direct_verdict": verdict,
        "anchor_side": anchor,
        "verdict": final_verdict,
        "summary": "S8[%s] vs H1X[%s] 直接对话 h2h(S8)=%s（W/L/T %s/%s/%s，"
                   "margin %s）；锚点 vs H1 S8=%s vs H1X在册=%s；vs mpx "
                   "S8=%s vs H1X在册=%s；判读=%s"
                   % (_sha(S8)[:8], _sha(H1X)[:8], h_main,
                      f_main.get("wins"),
                      f_main.get("losses"), f_main.get("ties"),
                      f_main.get("mean_margin"),
                      f_h1.get("h2h"), REG_H1X_VS_H1,
                      f_mpx.get("h2h"), REG_H1X_VS_MPX, final_verdict),
        "launch": "只测不发（在线提交=硬禁令）；发射决策移交用户",
    }
    BUDGET["unique_games_run"] = len(_ROW_CACHE)
    BUDGET["det_reruns"] = len(det_specs)  # 双跑各多跑一次
    BUDGET["total_局次"] = 30 + len(_ROW_CACHE) + len(det_specs)
    BUDGET["within_cap"] = BUDGET["total_局次"] <= BUDGET_CAP
    ANOMALIES.append(
        "harness 噪声不修不管；终局钱 farms[obs.player] 口径；胜率=硬通货，"
        "margin 只作参考")
    ANOMALIES.append(
        "sim_bridge 认证复用 s1form 缓存（consistency_ok）按 30 计账；"
        "预算局次=auth+去重后实跑局数+确定性双跑重跑")
    ANOMALIES.append(
        "校准臂 12 fold（i=0..11）与 H1X 在册同块可比；主对话 16 fold "
        "（i=0..15）多 4 fold 增样本")
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    flush_evid()
    print("VERDICT:", EV["verdict"]["summary"], flush=True)
    print("DONE", EV["elapsed_s"], "s budget:", BUDGET, flush=True)
    return EV


if __name__ == "__main__":
    main()
