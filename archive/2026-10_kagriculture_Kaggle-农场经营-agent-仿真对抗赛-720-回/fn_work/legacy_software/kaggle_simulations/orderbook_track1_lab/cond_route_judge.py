# -*- coding: utf-8 -*-
"""cond_route_judge：件 C 快速确认判决（条件合装件"永不变差"全局确认；不发射）。

责任口径（任务 cond-route-confirm 快线）：
1. 全局面：C vs H1 全语料（26 败局回放 + 新中性块 672000+i*47 n=20，
   双席折叠 n=46）——判据 h2h≥0.5（永不变差）+ 非触发世界零足迹
   （逐拍差异只许落在 ICE+YARN 世界局）。
   零足迹审计设计：同 seed 同席同对手配对跑 armA=C@0/H1@1、armB=H1@0/C@1、
   ctrl=H1@0/H1@1 三局，逐拍动作流对比（A0vsC0、B1vsC1 主对比；A1vsC1、
   B0vsC0 副对比）——非触发世界四流均须逐拍零差异。
2. 触发切片面：ICE+YARN 世界专组定向挖掘（gengame 重放定向法，mine_worlds
   唯件复用；轨道 1 已验 32/32）n≥12——判据 Δ>0 复现（Δ=margin_arm−
   margin_control 配对口径，轨道 1 mean_delta 同式；h2h 同报）。
3. 读数：W/L/T/margin/实现价/终局钱（farms[obs.player] 干净口径）+触发局数。

复用（不改写）：orderbook_r40.judge_r23._build_agents/_load_entry、
sim_bridge.sim_bridge/run_games（先认证 30/30）、orderbook_track1_lab.mine_worlds
（record_pair/predict_world/pair_key）、orderbook_strongest_lab.judge_strongest
（REPLAY_26/clean_reads/fold_arm/_reads_agg 读数口径）。
预算 ≤250 局次（judgment 口径；auth/挖掘另计）。workers=2。
只写 orderbook_track1_lab/（build_cond/evidence、evidence）与
fn_docs/hybrid/results/2026-09-29-cond-route-confirm.json。不改既有代码。
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import multiprocessing
import os
import sys
import time
from pathlib import Path

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

RECORD_VERSION = "cond-route-confirm/1.0"
H1_MAIN = KSIM_DIR / "orderbook_strongest_lab" / "build" / "h1" / "main.py"
C_MAIN = MODULE_DIR / "build_cond" / "c_main.py"
BUILD_EVID = MODULE_DIR / "build_cond" / "evidence"
EVID_DIR = MODULE_DIR / "evidence"
RAW_PATH = EVID_DIR / "cond_route_judge_raw.json"
FINAL_PATH = (MODULE_DIR.parents[3] / "fn_docs" / "hybrid" / "results"
              / "2026-09-29-cond-route-confirm.json")

TRIGGER_KEY = "ICE_CREAM_SHOP+YARN_STORE"
NEUTRAL_20 = [672000 + i * 47 for i in range(20)]
SLICE_FOLDS_TARGET = 12             # n=24 配对单元（n≥12 双口径均达标）
MINE_SEED_BASE = 691000             # 挖掘专属域（与 556/671/672/780/960k 不撞）
MINE_SEED_STEP = 53
MINE_SCAN_CAP = 20000
REC_SEED = 960001                   # 录制 seed（mine_worlds REC_SEED_BASE 域）
WORKERS = 2
BUDGET_CAP = 250                    # 局次（judgment：global+slice）
REVEAL_STEP = 144


def _load_js():
    """judge_strongest 唯件装载（读数口径复用；不改写）。"""
    p = KSIM_DIR / "orderbook_strongest_lab" / "judge_strongest.py"
    spec = importlib.util.spec_from_file_location("judge_strongest_reuse", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


JS = _load_js()
REPLAY_26 = list(JS.REPLAY_26)
SEEDS = REPLAY_26 + NEUTRAL_20


# ------------------------------------------------------------ 逐拍对比 --
def _canon(a):
    try:
        return json.dumps(a, sort_keys=True, default=str)
    except Exception:
        return repr(a)


def _stream_diff(sa, sb, cap=4):
    """两追踪槽逐拍动作流对比（按拍序；空槽对位缺失记差异）。"""
    na, nb = len(sa or []), len(sb or [])
    diffs = []
    for i in range(max(na, nb)):
        ea = (sa or [])[i] if i < na else None
        eb = (sb or [])[i] if i < nb else None
        ca = _canon(ea[2]) if ea is not None else None
        cb = _canon(eb[2]) if eb is not None else None
        if ca != cb:
            step = (ea or eb)[0]
            diffs.append({"i": i, "step": int(step),
                          "a": (ca or "")[:160], "b": (cb or "")[:160]})
    return {"n_steps_a": na, "n_steps_b": nb, "n_diff": len(diffs),
            "first_diff_step": diffs[0]["step"] if diffs else None,
            "diffs_sample": diffs[:cap]}


def _pair_from_sink(sink):
    from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
    for entry in (sink or []):
        if len(entry) < 2 or not isinstance(entry[1], dict):
            continue
        if int(entry[0]) != REVEAL_STEP:
            continue
        return ab._pair_key(entry[1])
    return None


# ------------------------------------------------------------ 跑局（并行） --
def _run_group_chunk(payload):
    """worker：一组三局（armA/armB/ctrl）建迹跑局→组内读数/Δ/逐拍对比。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    groups = payload["groups"]
    cfg = dict(payload.get("cfg") or {})
    games, meta = [], []
    for g in groups:
        for tag in ("armA", "armB", "ctrl"):
            spec = {"game_id": "cond-%s-%s-%d" % (g["kind"], tag, g["seed"]),
                    "seed": int(g["seed"]), "kind": g["kind"], "trace": True,
                    "our_seat": g["seats"][tag], "agents": g["agents"][tag]}
            ag, sinks = j23._build_agents(spec)
            games.append({"seed": int(g["seed"]), "agents": ag})
            meta.append((g, tag, sinks))
    res = sb.run_games(games, cfg) if games else {"games": [],
                                                  "engine": None}
    rows_run = list(res.get("games") or [])
    by_seed = {}
    for i, (g, tag, sinks) in enumerate(meta):
        rr = rows_run[i] if i < len(rows_run) else {}
        rec = by_seed.setdefault(g["seed"], {"g": g, "tags": {}})
        rec["tags"][tag] = {"banks": rr.get("banks"),
                            "error": rr.get("error"), "sinks": sinks}
    out = []
    for seed in sorted(by_seed):
        out.append(_finish_group(by_seed[seed]))
    return {"groups": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _finish_group(rec):
    """组收尾：margin/实现价/终局钱（farms[obs.player]）/Δ/逐拍足迹对比。"""
    g, t = rec["g"], rec["tags"]

    def _arm_row(tag, seat):
        r = t[tag]
        row = {"seat": seat, "banks": r["banks"], "error": r["error"],
               "margin": None, "reads": None, "opp_reads": None}
        if r["banks"] is not None and r["error"] is None:
            banks = r["banks"]
            row["margin"] = float(banks[seat]) - float(banks[1 - seat])
            sink = (r["sinks"] or {}).get(seat)
            if sink:
                row["reads"] = JS.clean_reads(sink)
            other = (r["sinks"] or {}).get(1 - seat)
            if other:
                row["opp_reads"] = JS.clean_reads(other)
        return row

    arm_a, arm_b = _arm_row("armA", 0), _arm_row("armB", 1)
    c = t["ctrl"]
    ctrl = {"banks": c["banks"], "error": c["error"], "margin_s0": None,
            "margin_s1": None, "reads_s0": None, "reads_s1": None}
    if c["banks"] is not None and c["error"] is None:
        banks = c["banks"]
        ctrl["margin_s0"] = float(banks[0]) - float(banks[1])
        ctrl["margin_s1"] = -ctrl["margin_s0"]
        s0 = (c["sinks"] or {}).get(0)
        s1 = (c["sinks"] or {}).get(1)
        if s0:
            ctrl["reads_s0"] = JS.clean_reads(s0)
        if s1:
            ctrl["reads_s1"] = JS.clean_reads(s1)
    pair = (_pair_from_sink((c["sinks"] or {}).get(0))
            or _pair_from_sink((t["armA"]["sinks"] or {}).get(0)))
    pair_a = _pair_from_sink((t["armA"]["sinks"] or {}).get(0))
    pair_b = _pair_from_sink((t["armB"]["sinks"] or {}).get(1))
    pair_consistent = len({p for p in (pair, pair_a, pair_b) if p}) <= 1
    deltas = {}
    if arm_a["margin"] is not None and ctrl["margin_s0"] is not None:
        deltas["A"] = round(arm_a["margin"] - ctrl["margin_s0"], 2)
    if arm_b["margin"] is not None and ctrl["margin_s1"] is not None:
        deltas["B"] = round(arm_b["margin"] - ctrl["margin_s1"], 2)
    fp = {
        "A0_vs_C0": _stream_diff((t["armA"]["sinks"] or {}).get(0),
                                 (c["sinks"] or {}).get(0)),
        "B1_vs_C1": _stream_diff((t["armB"]["sinks"] or {}).get(1),
                                 (c["sinks"] or {}).get(1)),
        "A1_vs_C1": _stream_diff((t["armA"]["sinks"] or {}).get(1),
                                 (c["sinks"] or {}).get(1)),
        "B0_vs_C0": _stream_diff((t["armB"]["sinks"] or {}).get(0),
                                 (c["sinks"] or {}).get(0)),
    }
    return {"seed": int(g["seed"]), "kind": g["kind"], "pair": pair,
            "trigger": pair == TRIGGER_KEY,
            "cell_pred": g.get("cell_pred"),
            "cell_match": (None if g.get("cell_pred") is None
                           else pair == g.get("cell_pred")),
            "pair_consistent": pair_consistent,
            "arms": {"A": arm_a, "B": arm_b}, "ctrl": ctrl,
            "deltas": deltas, "footprint": fp}


def _play(groups, cfg):
    groups = list(groups)
    n_chunks = max(1, min(WORKERS * 2, len(groups)))
    chunks = [groups[i::n_chunks] for i in range(n_chunks)]
    tasks = [{"groups": c, "cfg": dict(cfg)} for c in chunks if c]
    if WORKERS <= 1 or len(tasks) <= 1:
        parts = [_run_group_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(WORKERS, len(tasks))) as pool:
            parts = pool.map(_run_group_chunk, tasks)
    out = []
    for part in parts:
        out.extend(part["groups"])
    return out, [{"engine": p.get("engine"),
                  "fallback_reason": p.get("fallback_reason")}
                 for p in parts]


# ------------------------------------------------------------ 聚合 --
def _fold(rows):
    """双席折叠 W/L/T/h2h（judge_strongest.fold_arm 同口径）。"""
    return JS.fold_arm(rows)


def _arm_rows(groups):
    rows = []
    for g in groups:
        for tag in ("A", "B"):
            m = g["arms"][tag]["margin"]
            rows.append({"seed": g["seed"], "margin": m})
    return rows


def _reads_agg(groups, ours=True):
    rows = []
    for g in groups:
        for tag in ("A", "B"):
            key = "reads" if ours else "opp_reads"
            v = g["arms"][tag].get(key)
            if isinstance(v, dict):
                rows.append({key: v})
    return JS._reads_agg(rows, "reads" if ours else "opp_reads")


def _group_lite(g):
    return {"seed": g["seed"], "kind": g["kind"], "pair": g["pair"],
            "trigger": g["trigger"], "cell_pred": g.get("cell_pred"),
            "cell_match": g.get("cell_match"),
            "margin_A": g["arms"]["A"]["margin"],
            "margin_B": g["arms"]["B"]["margin"],
            "margin_ctrl_s0": g["ctrl"]["margin_s0"],
            "delta_A": g["deltas"].get("A"), "delta_B": g["deltas"].get("B"),
            "tm_A": (g["arms"]["A"].get("reads") or {}).get("terminal_money"),
            "px_A": (g["arms"]["A"].get("reads") or {}).get("realized_px"),
            "fp_diffs": {k: v["n_diff"] for k, v in g["footprint"].items()},
            "error": (g["arms"]["A"]["error"] or g["arms"]["B"]["error"]
                      or g["ctrl"]["error"])}


# ------------------------------------------------------------ 主编排 --
def main():
    os.chdir(KSIM_DIR)
    t0 = time.perf_counter()
    budget = {"cap_局次": BUDGET_CAP, "auth_games_separate": 0,
              "mining_games_separate": 0, "judgment_games": 0,
              "global_games": 0, "slice_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": [
                "python3 orderbook_track1_lab/cond_route_build.py",
                "python3 orderbook_track1_lab/cond_route_gates.py",
                "python3 orderbook_track1_lab/cond_route_judge.py"],
            "base_main": str(H1_MAIN),
            "base_main_sha256": hashlib.sha256(
                H1_MAIN.read_bytes()).hexdigest(),
            "cond_main": str(C_MAIN),
            "workers": WORKERS,
            "corpus": {"replay_r30_26": REPLAY_26,
                       "neutral_672000_i47": NEUTRAL_20,
                       "n_folds": len(SEEDS), "fold": "双席折叠"},
            "caliber": {
                "margin": "farms[our].money−farms[opp].money（run_games banks 干净口径）",
                "terminal_money": "farms[obs.player].money（judge_strongest.clean_reads）",
                "realized_px": "Σ(qty×卖时市价)/Σ(qty×该局该品日均价)（clean_reads 同式）",
                "delta": "margin_arm−margin_control 同 seed+seat 配对（轨道 1 mean_delta 同式）",
                "footprint": "同 seed 同席同对手 arm vs ctrl 逐拍动作流对比（canon JSON）"},
        },
    }

    # ---- 0. 门禁读入（build_cond/evidence/gates_cond.json）----
    gates_path = BUILD_EVID / "gates_cond.json"
    gates = json.loads(gates_path.read_text(encoding="utf-8")) \
        if gates_path.is_file() else {"overall_passed": False,
                                      "error": "gates_cond.json 缺失"}
    out["gates"] = gates
    man = json.loads((MODULE_DIR / "build_cond" / "build_manifest.json")
                     .read_text(encoding="utf-8"))
    out["source"]["cond_main_sha256"] = man.get("main_sha256")
    out["source"]["cond_tar_sha256"] = man.get("tar_sha256")
    if not gates.get("overall_passed"):
        out["aborted"] = "四门未全过，判决中止"
        FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                         default=str) + "\n", encoding="utf-8")
        print("ABORT", out["aborted"], flush=True)
        return out

    # ---- 1. sim_bridge 对照认证 30/30（不过即停）----
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    auth_corpus = REPLAY_26 + [2026092901, 2026092902, 2026092903, 2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(BUILD_EVID / "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    BUILD_EVID.mkdir(parents=True, exist_ok=True)
    (BUILD_EVID / "sim_auth.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n",
        encoding="utf-8")
    budget["auth_games_separate"] = 60
    out["source"]["sim_auth"] = auth_lite
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["budget"] = budget
        FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
        FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                         default=str) + "\n", encoding="utf-8")
        print("ABORT", out["aborted"], flush=True)
        return out
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 2. 定向挖掘（mine_worlds 唯件；gengame 重放定向法）----
    import mine_worlds as mw  # noqa: WPS433  同 lab 挖掘件
    mine_t0 = time.perf_counter()
    srv = mw.Serve()
    try:
        rec = mw.record_pair("orderbook_strongest_lab/build/h1/main.py",
                             REC_SEED, srv)
    finally:
        pass
    budget["mining_games_separate"] = 2
    lines = rec["tapes"]["order_h1_first"]["lines"]
    lines2 = rec["tapes"]["order_h1_second"]["lines"]
    found, scanned = [], 0
    for i in range(MINE_SCAN_CAP):
        s = MINE_SEED_BASE + i * MINE_SEED_STEP
        wk = mw.predict_world(s, lines[0], lines[1], srv)
        scanned += 1
        if mw.pair_key(wk) == TRIGGER_KEY:
            found.append(s)
            if len(found) >= SLICE_FOLDS_TARGET:
                break
    mine = {"method": "gengame 磁带重放定向（H1/H1 实录磁带预测店对；mine_worlds 唯件）",
            "rec_seed": REC_SEED, "seed_domain": "%d+i*%d" % (MINE_SEED_BASE,
                                                              MINE_SEED_STEP),
            "n_scanned_predictions": scanned,
            "n_found": len(found), "seeds": found,
            "elapsed_s": round(time.perf_counter() - mine_t0, 2)}
    out["source"]["trigger_slice_mining"] = mine
    (BUILD_EVID / "cond_mine_plan.json").write_text(
        json.dumps(mine, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print("mined", len(found), "ICE+YARN seeds in", scanned, "scans",
          mine["elapsed_s"], "s", flush=True)
    srv.close()

    # ---- 3. 全语料 C vs H1（46 folds × 3 局）----
    def _mk_group(seed, kind, cell_pred=None):
        return {"seed": int(seed), "kind": kind, "cell_pred": cell_pred,
                "seats": {"armA": 0, "armB": 1, "ctrl": 0},
                "agents": {
                    "armA": [{"type": "python", "path": str(C_MAIN)},
                             {"type": "python", "path": str(H1_MAIN)}],
                    "armB": [{"type": "python", "path": str(H1_MAIN)},
                             {"type": "python", "path": str(C_MAIN)}],
                    "ctrl": [{"type": "python", "path": str(H1_MAIN)},
                             {"type": "python", "path": str(H1_MAIN)}]}}

    n_global = len(SEEDS) * 3
    n_slice = len(found) * 3
    if n_global + n_slice > BUDGET_CAP:
        found = found[: max(0, (BUDGET_CAP - n_global) // 3)]
        n_slice = len(found) * 3
    mine["seeds_used"] = list(found)
    budget["global_games"] = n_global
    budget["slice_games"] = n_slice
    budget["judgment_games"] = n_global + n_slice
    budget["judgment_局次_folds"] = len(SEEDS) + len(found)
    print("budget:", budget, flush=True)

    global_groups = [_mk_group(s, "global") for s in SEEDS]
    t1 = time.perf_counter()
    g_rows, g_engines = _play(global_groups, run_cfg)
    g_rows.sort(key=lambda r: r["seed"])
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_PATH.write_text(json.dumps(
        {"global": [_group_lite(g) for g in g_rows]}, ensure_ascii=False,
        indent=1, default=str) + "\n", encoding="utf-8")
    print("global done", round(time.perf_counter() - t1, 1), "s", flush=True)

    # ---- 4. 触发切片（mined seeds × 3 局）----
    slice_groups = [_mk_group(s, "slice", cell_pred=TRIGGER_KEY) for s in found]
    t2 = time.perf_counter()
    s_rows, s_engines = _play(slice_groups, run_cfg) if slice_groups else ([], [])
    s_rows.sort(key=lambda r: r["seed"])
    with open(RAW_PATH, "r", encoding="utf-8") as h:
        raw = json.loads(h.read())
    raw["slice"] = [_group_lite(g) for g in s_rows]
    RAW_PATH.write_text(json.dumps(raw, ensure_ascii=False, indent=1,
                                   default=str) + "\n", encoding="utf-8")
    print("slice done", round(time.perf_counter() - t2, 1), "s", flush=True)

    # 预测校验（mine_validate 机制：预测 vs 实测，全语料+切片）
    srv2 = mw.Serve()
    try:
        val_rows = []
        for g in g_rows + s_rows:
            pk_pred = mw.pair_key(
                mw.predict_world(g["seed"], lines[0], lines[1], srv2))
            val_rows.append({"seed": g["seed"], "kind": g["kind"],
                             "pred": pk_pred, "actual": g["pair"],
                             "match": pk_pred == g["pair"]})
        pred_check = {
            "method": "mine_validate 机制：录制磁带 gengame 重放预测 vs 实跑 trace 店对",
            "n": len(val_rows),
            "n_match": sum(1 for r in val_rows if r["match"]),
            "rate": round(sum(1 for r in val_rows if r["match"]) /
                          max(1, len(val_rows)), 4),
            "rows": val_rows}
    finally:
        srv2.close()
    out["source"]["trigger_slice_mining"]["prediction_check"] = pred_check

    # ---- 5. 聚合与判决 ----
    def _face(groups, label):
        rows = _arm_rows(groups)
        fold = _fold(rows)
        return {"pair": "C_vs_H1", "slice": label,
                "n_folds": fold["n"], "wins": fold["wins"],
                "losses": fold["losses"], "ties": fold["ties"],
                "h2h": fold["h2h"], "mean_margin": fold["mean_margin"],
                "fold_margins": fold["fold_margins"],
                "ours": _reads_agg(groups, True),
                "opp_side": _reads_agg(groups, False),
                "engines": g_engines if label == "global" else s_engines,
                "n_error_games": sum(
                    1 for g in groups for t in ("A", "B")
                    if g["arms"][t]["error"]),
                "rows_lite": [_group_lite(g) for g in groups]}

    global_face = _face(g_rows, "global")
    slice_face = _face(s_rows, "slice") if s_rows else {}

    # 触发局数统计
    trg_global = [g["seed"] for g in g_rows if g["trigger"]]
    trg_slice = [g["seed"] for g in s_rows if g["trigger"]]
    out["trigger_stats"] = {
        "n_trigger_folds_global": len(trg_global),
        "trigger_seeds_global": trg_global,
        "n_trigger_folds_slice": len(trg_slice),
        "trigger_seeds_slice": trg_slice,
        "n_trigger_folds_total": len(trg_global) + len(trg_slice),
        "n_trigger_games_total": 3 * (len(trg_global) + len(trg_slice)),
        "cell_match_slice": {
            "n": len(s_rows),
            "n_match": sum(1 for g in s_rows if g.get("cell_match"))}}

    # 零足迹审计（非触发世界逐拍差异只许落在 ICE+YARN 世界局）
    fp_violations, fp_trigger = [], []
    for g in g_rows + s_rows:
        for k, d in g["footprint"].items():
            if g["trigger"]:
                if d["n_diff"]:
                    fp_trigger.append({"seed": g["seed"], "stream": k,
                                       "n_diff": d["n_diff"],
                                       "first_diff_step": d["first_diff_step"]})
            elif d["n_diff"]:
                fp_violations.append({"seed": g["seed"], "kind": g["kind"],
                                      "stream": k, "n_diff": d["n_diff"],
                                      "first_diff_step": d["first_diff_step"],
                                      "sample": d["diffs_sample"][:2]})
    n_non_trigger = sum(1 for g in g_rows + s_rows if not g["trigger"])
    out["footprint_audit"] = {
        "design": "同 seed 同席同对手配对：armA=C@0/H1@1、armB=H1@0/C@1 vs "
                  "ctrl=H1@0/H1@1；逐拍动作流对比 4 流（A0vsC0/B1vsC1 主、"
                  "A1vsC1/B0vsC0 副）",
        "streams": ["A0_vs_C0", "B1_vs_C1", "A1_vs_C1", "B0_vs_C0"],
        "n_groups_total": len(g_rows) + len(s_rows),
        "n_non_trigger_groups": n_non_trigger,
        "n_trigger_groups": (len(g_rows) + len(s_rows)) - n_non_trigger,
        "non_trigger_violations": fp_violations,
        "zero_footprint": len(fp_violations) == 0,
        "trigger_world_diffs": fp_trigger,
        "pair_consistency_all": all(g["pair_consistent"]
                                    for g in g_rows + s_rows)}
    out["global"] = global_face
    out["trigger_slice"] = slice_face

    # 触发切片 Δ（轨道 1 mean_delta 同式：margin_arm−margin_control 配对）
    deltas = []
    for g in s_rows:
        for k in ("A", "B"):
            if g["deltas"].get(k) is not None:
                deltas.append(g["deltas"][k])
    mean_delta = (round(sum(deltas) / len(deltas), 2)
                  if deltas else None)
    win_arm = sum(1 for g in s_rows for t in ("A", "B")
                  if (g["arms"][t]["margin"] or 0) > 0)
    win_ctrl = sum(1 for g in s_rows
                   for t, m in (("A", g["ctrl"]["margin_s0"]),
                                ("B", g["ctrl"]["margin_s1"]))
                   if (m or 0) > 0)
    out["trigger_slice"]["delta_paired"] = {
        "caliber": "margin_arm−margin_control（同 seed+seat 配对；轨道 1 mean_delta 同式）",
        "n_units": len(deltas), "mean_delta": mean_delta,
        "per_unit": deltas, "net_flip_wins": win_arm - win_ctrl,
        "win_arm": win_arm, "win_control": win_ctrl}
    out["trigger_slice"]["n_达标"] = len(deltas) >= 12

    # 判决
    h2h_ok = (global_face.get("h2h") is not None
              and global_face["h2h"] >= 0.5)
    fp_ok = out["footprint_audit"]["zero_footprint"]
    delta_ok = (mean_delta is not None and mean_delta > 0
                and (slice_face.get("mean_margin") or 0) > 0)
    n_ok = out["trigger_slice"]["n_达标"]
    out["verdict"] = {
        "criteria": {
            "全局 h2h≥0.5（永不变差）": h2h_ok,
            "非触发世界零足迹": fp_ok,
            "触发切片 Δ>0 复现（mean_delta>0 且 h2h mean_margin>0）": delta_ok,
            "触发切片 n≥12 配对单元": n_ok},
        "never_worse": h2h_ok and fp_ok,
        "trigger_positive": delta_ok,
        "verdict": ("COND_ROUTE_CONFIRMED: 永不变差+触发正增益"
                    if (h2h_ok and fp_ok and delta_ok and n_ok)
                    else "NOT_CONFIRMED（详见 criteria）"),
    }
    out["budget"] = budget
    out["anomaly"] = [
        "harness 噪声：HP_TELEMETRY stdout 行（H1 件自报 telemetry）——不修不管",
        "harness 噪声：kaggle_environments 可选环境加载告警（open_spiel/cabt）——无关环境忽略",
        "判世界时点=step144 揭示帧（world 第二店 step143 才落定，最早可判时点；"
        "pre-144 件 C 与 H1 逐字节同 → world 实现不受处理影响）",
    ]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    FINAL_PATH.parent.mkdir(parents=True, exist_ok=True)
    FINAL_PATH.write_text(json.dumps(out, ensure_ascii=False, indent=1,
                                     default=str) + "\n", encoding="utf-8")
    print("verdict:", out["verdict"]["verdict"], out["verdict"]["criteria"],
          flush=True)
    print("global h2h:", global_face["h2h"], "fold margins:",
          global_face["fold_margins"][:8], "...", flush=True)
    print("footprint zero:", fp_ok, "violations:", len(fp_violations),
          flush=True)
    print("slice mean_delta:", mean_delta, "n:", len(deltas), flush=True)
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    main()
