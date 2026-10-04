# -*- coding: utf-8 -*-
"""judge_v89：V89 基底升级判决（judgment_r27_v2/strongest 同口径；判决先行·不发射）。

语料：26 败局回放种子（replays-r30-26 info.seed 同序）+ 新中性块 672000+i*79
n=20（换新块防过拟合）→ 双席折叠 n=46。
主判：v89_pure vs H1（判据 h2h>=0.55 才算"基底更强"）+ v89_pure vs r40 参照。
若更强：四门 + v89_full vs H1（全语料）+ v89_full vs v89_pure（26 败局组；
预算裁剪——cap 400 局次）。
仪器：sim_bridge 先对照认证 30/30（不过即停）；同局配对；翻胜主语（margin=
我席钱−对席钱，双席折叠）；终局钱=farms[obs.player].money 干净口径。
读数：W/L/T/margin/实现价中位/终局钱 + G793 门触发面（逐局 _G793_REPORT/
_G793_STATE 经 entry __globals__ 采集）+ v89_full 的画像类/C3 换表/X1 台账。
复用（不改写）：judge_r23._build_agents 语义（自建 chunk 以采层台账）、
judge_strongest.clean_reads/wall_stats/fold_arm/aggregate、sim_bridge。
只写 orderbook_v89_lab/evidence/ 与 fn_docs/hybrid/results/（最终证据）。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
for p in (KSIM, ROOT, os.path.join(KSIM, "orderbook_strongest_lab")):
    if p not in sys.path:
        sys.path.insert(0, p)

import judge_strongest as js  # noqa: E402  纯函数复用（零改动引用）

RECORD_VERSION = "judge-v89/1.0"
UNKNOWN = "UNKNOWN"

REPLAY_26 = list(js.REPLAY_26)
NEUTRAL_20 = [672000 + i * 79 for i in range(20)]
SEEDS = REPLAY_26 + NEUTRAL_20
CAP_局次 = 400

H1_MAIN = os.path.join(KSIM, "orderbook_strongest_lab", "build", "h1",
                       "main.py")
R40_MAIN = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
V89_PURE = os.path.join(ROOT, "build", "v89_pure", "main.py")
V89_FULL = os.path.join(ROOT, "build", "v89_full", "main.py")
EVID = os.path.join(ROOT, "evidence")
WORKERS = 2
STRONGER_H2H = 0.55


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ------------------------------------------------------------ 层台账采集 --
def _layer_stats(entry):
    """经 entry.__globals__ 采该局层台账（G793 门/画像/C3/X1）。"""
    g = getattr(entry, "__globals__", None)
    out = {}
    if not isinstance(g, dict):
        return out
    rep = g.get("_G793_REPORT")
    if isinstance(rep, dict):
        out["g793"] = {k: int(rep.get(k, 0) or 0)
                       for k in ("calls", "classified", "bypassed", "errors")}
    st = g.get("_G793_STATE")
    if isinstance(st, dict):
        out["g793_state"] = {
            str(s): {"disable": bool(v.get("disable")),
                     "decided": bool(v.get("decided"))}
            for s, v in st.items() if isinstance(v, dict)}
    oc = g.get("_OC_STATE")
    if isinstance(oc, dict):
        out["oc_classes"] = {str(k): (d.get("cls") or "unknown")
                             for k, d in oc.items() if isinstance(d, dict)}
        sw = g.get("_OC_C3_SWAPPED")
        if isinstance(sw, list) and sw:
            out["oc_c3_swapped"] = bool(sw[0])
    x1 = g.get("_X1_REPORT")
    if isinstance(x1, dict):
        out["x1"] = {k: int(v) for k, v in x1.items()
                     if isinstance(v, (int, float)) and not isinstance(v, bool)}
    return out


def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            agents, sinks = [], ({0: [], 1: []} if spec.get("trace") else None)
            entries = []
            for seat, a in enumerate(spec["agents"]):
                inner = j23._load_entry(a.get("path"))
                entries.append(inner)
                if sinks is not None:
                    agents.append(j23._Tracer(inner, seat, sinks[seat]))
                else:
                    agents.append(inner)
            games.append({"seed": int(spec["seed"]), "agents": agents})
            metas.append((spec, sinks, entries))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, []))
            metas[-1] = (spec, {"build_error": repr(exc)[:120]}, [])
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, entries) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opp": spec.get("opp"), "group": spec.get("group"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "opp_reads": {}, "wall": {},
               "layer": {}}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    row["reads"] = js.clean_reads(sink)
                    row["wall"] = js.wall_stats(sink)
                other = sinks.get(1 - row["seat"])
                if other is not None:
                    row["opp_reads"] = js.clean_reads(other)
            if len(entries) > row["seat"]:
                row["layer"] = _layer_stats(entries[row["seat"]])
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


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
    rows, engines = [], []
    for part in parts:
        rows.extend(part["rows"])
        engines.append({"engine": part.get("engine"),
                        "fallback_reason": part.get("fallback_reason")})
    return rows, engines


def make_specs(arm_main, opp_main, arm, opp, seeds=None):
    seeds = list(SEEDS if seeds is None else seeds)
    neutral = set(NEUTRAL_20)
    specs = []
    for seed in seeds:
        group = ("neutral_672000_i79" if seed in neutral else "replay_r30_26")
        for seat in (0, 1):
            a = {"type": "python", "path": arm_main}
            b = {"type": "python", "path": opp_main}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "v89-%s-vs%s-%d-s%d" % (arm, opp, seed, seat),
                "seed": seed, "kind": "pair", "arm": arm, "opp": opp,
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


def layer_agg(rows):
    """G793 门触发面 + 画像/C3/X1 汇总（逐局台账）。"""
    layers = [r.get("layer") or {} for r in rows if not r.get("error")]
    g = [L.get("g793") or {} for L in layers if L.get("g793")]
    out = {"n_games_with_layer": len(layers)}
    if g:
        out["g793"] = {
            "n_games": len(g),
            "n_classified": sum(1 for x in g if x.get("classified", 0) > 0),
            "n_bypassed": sum(1 for x in g if x.get("bypassed", 0) > 0),
            "sum_classified": sum(x.get("classified", 0) for x in g),
            "sum_bypassed": sum(x.get("bypassed", 0) for x in g),
            "sum_errors": sum(x.get("errors", 0) for x in g),
            "bypassed_per_game_mean": round(
                sum(x.get("bypassed", 0) for x in g) / len(g), 2),
        }
    states = [L.get("g793_state") or {} for L in layers if L.get("g793_state")]
    if states:
        dis = [any(v.get("disable") for v in s.values()) for s in states]
        out["g793"]["n_gate_disabled_games"] = sum(1 for d in dis if d)
    oc = [L.get("oc_classes") or {} for L in layers if L.get("oc_classes")]
    if oc:
        agg = {}
        for d in oc:
            for v in d.values():
                agg[v] = agg.get(v, 0) + 1
        out["oc_class_seat_counts"] = dict(sorted(agg.items()))
        out["oc_c3_swapped_games"] = sum(
            1 for L in layers if L.get("oc_c3_swapped"))
    x1 = [L.get("x1") or {} for L in layers if L.get("x1")]
    if x1:
        out["x1"] = {
            "changed_turns_sum": sum(x.get("changed_turns", 0) for x in x1),
            "dropped_dead_sum": sum(x.get("dropped_dead", 0) for x in x1),
            "clamped_orders_sum": sum(x.get("clamped_orders", 0) for x in x1),
            "merged_fragments_sum": sum(x.get("merged_fragments", 0) for x in x1),
            "errors_sum": sum(x.get("errors", 0) for x in x1),
        }
    return out


def run_pair(cfg, arm_main, opp_main, arm, opp, seeds, budget, out_pairs):
    specs = make_specs(arm_main, opp_main, arm, opp, seeds=seeds)
    t2 = time.perf_counter()
    rows, engines = _play(specs, cfg)
    agg = js.aggregate(rows, engines)
    agg["replay_r30_26"] = js.aggregate(js.group_slice(rows, "replay_r30_26"),
                                        engines)
    agg["neutral_672000_i79"] = js.aggregate(
        js.group_slice(rows, "neutral_672000_i79"), engines)
    agg["layer_stats"] = layer_agg(rows)
    agg["rows_lite"] = js.rows_lite(rows)
    agg["elapsed_s"] = round(time.perf_counter() - t2, 1)
    key = "%s_vs_%s" % (arm, opp)
    out_pairs[key] = agg
    budget["judgment_games"] += len(rows)
    budget["judgment_folds"] += len(set(r["seed"] for r in rows))
    print(arm, "vs", opp, agg["h2h"], agg["wins"], agg["losses"], agg["ties"],
          agg["mean_margin"], "px", agg["ours"]["realized_px_median"],
          "tm", agg["ours"]["terminal_money_median"], agg["elapsed_s"], "s",
          flush=True)
    os.makedirs(EVID, exist_ok=True)
    open(os.path.join(EVID, "pair_%s.json" % key), "w").write(
        json.dumps(agg, ensure_ascii=False, indent=1, default=str) + "\n")
    return agg


def run_gates(form):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "gates_v89.py"),
                        form], capture_output=True, text=True)
    print(r.stdout[-600:], flush=True)
    if r.returncode != 0:
        print(r.stderr[-600:], flush=True)
    return json.loads(open(os.path.join(EVID, "gates_v89.json")).read())


def main():
    os.chdir(ROOT)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    t0 = time.perf_counter()
    budget = {"cap_局次": CAP_局次, "auth_局次": 0, "gate_局次": 4,
              "judgment_games": 0, "judgment_folds": 0,
              "gate_note": "v89_pure 四门 4 局次（judgment 前已跑）；"
                           "v89_full 四门计入 stage2"}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_v89_lab/build_v89.py",
                         "python3 orderbook_v89_lab/gates_v89.py",
                         "python3 orderbook_v89_lab/judge_v89.py"],
            "seed_base": 672000,
            "seed_stagger": "672000+i*79（局组错开；新中性块 n=20 防过拟合）",
            "replay_seeds_26": REPLAY_26,
            "neutral_seeds_20": NEUTRAL_20,
            "corpus_total_folds": len(SEEDS),
            "h1_main": H1_MAIN, "r40_main": R40_MAIN,
            "v89_pure": V89_PURE, "v89_full": V89_FULL,
            "workers": WORKERS,
            "terminal_money_caliber": "farms[obs.player].money（干净口径）",
        },
        "pairs": {},
        "budget": budget,
    }

    # ---- sim_bridge 对照认证 30/30（不过即停） ----
    auth_corpus = list(REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                     2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": os.path.join(EVID, "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    os.makedirs(EVID, exist_ok=True)
    open(os.path.join(EVID, "sim_auth.json"), "w").write(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n")
    budget["auth_局次"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"), auth_lite.get("consistency"),
          flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["source"]["sim_auth"] = auth_lite
        open(os.path.join(EVID, "judgment.json"), "w").write(
            json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
        print("ABORT", out["aborted"], flush=True)
        return out
    out["source"]["sim_auth"] = auth_lite
    cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 主判：v89_pure vs H1 / vs r40 ----
    a_h1 = run_pair(cfg, V89_PURE, H1_MAIN, "v89p", "H1", SEEDS, budget,
                    out["pairs"])
    run_pair(cfg, V89_PURE, R40_MAIN, "v89p", "r40", SEEDS, budget,
             out["pairs"])

    criteria = [{
        "criterion": "h2h vs H1 >= %.2f（26 败局+新中性块 n=20 双席折叠）"
                     % STRONGER_H2H,
        "value": a_h1.get("h2h"), "passed": is_num(a_h1.get("h2h"))
        and float(a_h1["h2h"]) >= STRONGER_H2H}]
    stronger = bool(criteria[0]["passed"])
    out["criteria_stage1"] = criteria

    # ---- 若更强：v89_full 门禁 + 对照 ----
    if stronger:
        gates_full = run_gates("v89_full")
        budget["gate_局次"] += 4
        run_pair(cfg, V89_FULL, H1_MAIN, "v89full", "H1", SEEDS, budget,
                 out["pairs"])
        # 预算裁剪：v89_full vs v89_pure 用 26 败局组（52 局次；cap 400 内）
        run_pair(cfg, V89_FULL, V89_PURE, "v89full", "v89p", REPLAY_26,
                 budget, out["pairs"])
        out["stage2"] = {"gates": {k: v for k, v in gates_full.items()
                                   if k in ("overall_passed", "forms",
                                            "budget")},
                         "subset_note": "v89_full vs v89_pure 预算裁剪至 26 "
                                        "败局组（52 局次；总预算 cap 400）"}
    else:
        out["stage2"] = {"skipped": "h2h vs H1 < %.2f（基底不更强）→ 不合成"
                                    % STRONGER_H2H}

    budget["total_局次"] = (budget["auth_局次"] + budget["gate_局次"]
                        + budget["judgment_games"])
    budget["within_cap"] = budget["total_局次"] <= CAP_局次
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    open(os.path.join(EVID, "judgment.json"), "w").write(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    main()
