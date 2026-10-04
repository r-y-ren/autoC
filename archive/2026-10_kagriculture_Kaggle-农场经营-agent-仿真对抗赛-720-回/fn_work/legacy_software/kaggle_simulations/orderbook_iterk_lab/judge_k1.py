# -*- coding: utf-8 -*-
"""judge_k1（iterk K1 判决）：H1+毛期错峰防御 重访判决（判决先行·不发射）。

责任口径（任务 K1）：
- 语料：26 败局回放种子（replays-r30-26 同序）+ 新中性块 672000+i*37 n=20
  （换新块防过拟合）→ 双席折叠 n=46；
- 反制臂专组：Wool Front-Runner（取材重建件 opponents/counter_wool_front_runner.py）
  10 seeds（中性块前 10，双席）；
- 三对：k1_vs_h1（常规语料零代价判据：h2h ≥ 0.5）/ k1_vs_wfr、h1_vs_wfr
  （反制臂判据：K1 胜率 ≥ H1 基线）；
- sim_bridge 先对照认证 30/30（不过即停）；workers=2；预算 ≤400 局次。
读数：W/L/T/margin/实现价/终局钱（farms[obs.player].money 干净口径）+
K1 剪毛相位对照表（错开前后逐日刀次：实跑追踪口径 + 磁带口径）。
复用（不改写）：orderbook_strongest_lab.judge_strongest（clean_reads/
fold_arm/aggregate/rows_lite/group_slice）+ orderbook_r40.judge_r23._build_agents
+ orderbook_r40.sim_bridge.run_games/sim_bridge。
只写 orderbook_iterk_lab/。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import sys
import time

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(MODULE_DIR)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

from orderbook_iterk_lab import layer_k1 as k1  # noqa: E402
from orderbook_strongest_lab import judge_strongest as js  # noqa: E402

RECORD_VERSION = "judge-k1/1.0"
REPLAY_26 = list(js.REPLAY_26)
NEUTRAL_20 = [672000 + i * 37 for i in range(20)]
SEEDS = REPLAY_26 + NEUTRAL_20
COUNTER_SEEDS = NEUTRAL_20[:10]          # 反制臂专组 10 seeds
WORKERS = 2

H1_MAIN = os.path.join(KSIM, "orderbook_iterk_lab", "build", "h1_base", "main.py")
K1_MAIN = os.path.join(KSIM, "orderbook_iterk_lab", "build", "k1", "main.py")
WFR_MAIN = os.path.join(KSIM, "orderbook_iterk_lab", "opponents",
                        "counter_wool_front_runner.py")
BUDGET_CAP = 400


def make_specs_k1(our_main, opp_main, arm, opp, seeds):
    specs = []
    for seed in seeds:
        group = ("neutral_672000_i37" if seed in set(NEUTRAL_20)
                 else "replay_r30_26")
        for seat in (0, 1):
            a = {"type": "python", "path": our_main}
            b = {"type": "python", "path": opp_main}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "k1-%s-vs%s-%d-s%d" % (arm, opp, seed, seat),
                "seed": seed, "kind": "pair", "arm": arm, "opp": opp,
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


# --------------------------------------------------------------- 跑口 --
def _chunk_k1(payload):
    """js._chunk 同构 + 逐日剪毛数（实跑追踪口径，双席）。"""
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
               "opp": spec.get("opp"), "group": spec.get("group"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "opp_reads": {}, "wall": {},
               "shear_days": {}, "opp_shear_days": {}}
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
                    row["shear_days"] = k1.shear_day_counts_from_sink(sink)
                other = sinks.get(1 - row["seat"])
                if other is not None:
                    row["opp_reads"] = js.clean_reads(other)
                    row["opp_shear_days"] = k1.shear_day_counts_from_sink(other)
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play_k1(specs, cfg):
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n = max(1, min(workers * 2, max(1, len(specs))))
    tasks = [{"specs": specs[i::n], "cfg": dict(cfg or {})} for i in range(n)]
    tasks = [t for t in tasks if t["specs"]]
    if workers <= 1 or len(tasks) <= 1:
        parts = [_chunk_k1(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            parts = pool.map(_chunk_k1, tasks)
    rows, engines = [], []
    for part in parts:
        rows.extend(part["rows"])
        engines.append({"engine": part.get("engine"),
                        "fallback_reason": part.get("fallback_reason")})
    return rows, engines


def shear_phase_agg(rows):
    """实跑剪毛相位对照：{arm: {day: n}}（我席逐日剪毛合计）。"""
    agg = {}
    for r in rows or []:
        d = agg.setdefault(str(r.get("arm")), {})
        for day, n in (r.get("shear_days") or {}).items():
            d[str(day)] = d.get(str(day), 0) + int(n)
    for arm in agg:
        agg[arm] = dict(sorted(agg[arm].items(), key=lambda kv: int(kv[0])))
    return agg


def main():
    os.chdir(KSIM)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    budget = {"cap_局次": BUDGET_CAP, "auth_games": 0, "judgment_games": 0,
              "counter_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_iterk_lab/build_k1.py",
                         "python3 orderbook_iterk_lab/judge_k1.py"],
            "base_main": H1_MAIN, "k1_main": K1_MAIN, "wfr_main": WFR_MAIN,
            "seed_base": 672000,
            "seed_stagger": "672000+i*37（新中性块 n=20 防过拟合）",
            "replay_seeds_26": list(REPLAY_26),
            "neutral_seeds_20": list(NEUTRAL_20),
            "counter_seeds_10": list(COUNTER_SEEDS),
            "corpus_total_folds": len(SEEDS),
            "workers": WORKERS,
            "terminal_money_caliber": "farms[obs.player].money（干净口径）",
            "k1_treatment": ("layer_k1.retape_phase_offset：剪毛刀 d17/20/23/26 "
                             "→ d+1/d+2（d29 保留）；量守恒零跨拍"),
            "counter_rebuild": {
                "material": "orderbook_r45/evidence/counter_wool_front_runner.py",
                "deltas": ["真毛供给=4 羊自足农场（原件幻影单零效果）",
                           "倒毛量=min(48, 棚存 WOOL)",
                           "集毛阈值 dump_min=12（集中倒毛口径）",
                           "季末清仓 step>=714"],
                "kept": "嗅探/dump_at=sniff+2/Anti-Shock 语义原件保持"},
        },
        "pairs": {},
        "budget": budget,
        "elapsed_s": 0.0,
    }
    t0 = time.perf_counter()

    # ---- sim_bridge 对照认证 30/30（不过即停）----
    auth_corpus = list(REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                     2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": os.path.join(MODULE_DIR, "evidence",
                                     "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    open(os.path.join(MODULE_DIR, "evidence", "sim_auth.json"), "w").write(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n")
    budget["auth_games"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["source"]["sim_auth"] = auth_lite
        out["elapsed_s"] = round(time.perf_counter() - t0, 1)
        open(os.path.join(MODULE_DIR, "evidence", "judge_k1_realrun.json"),
             "w").write(json.dumps(out, ensure_ascii=False, indent=1,
                                   default=str) + "\n")
        print("ABORT", out["aborted"], flush=True)
        return out
    out["source"]["sim_auth"] = auth_lite
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 三对判决 ----
    pair_plan = [
        ("k1_vs_h1", K1_MAIN, H1_MAIN, "k1", "h1", SEEDS, "judgment_games"),
        ("k1_vs_wfr", K1_MAIN, WFR_MAIN, "k1", "wfr", COUNTER_SEEDS,
         "counter_games"),
        ("h1_vs_wfr", H1_MAIN, WFR_MAIN, "h1", "wfr", COUNTER_SEEDS,
         "counter_games"),
    ]
    phase_rows = {}
    for name, our_main, opp_main, arm, opp, seeds, bkey in pair_plan:
        specs = make_specs_k1(our_main, opp_main, arm, opp, seeds)
        t2 = time.perf_counter()
        rows, engines = _play_k1(specs, run_cfg)
        agg = js.aggregate(rows, engines)
        agg["replay_r30_26"] = js.aggregate(js.group_slice(rows, "replay_r30_26"),
                                            engines)
        agg["neutral_672000_i37"] = js.aggregate(
            js.group_slice(rows, "neutral_672000_i37"), engines)
        agg["rows_lite"] = js.rows_lite(rows)
        agg["shear_phase_ingame"] = shear_phase_agg(rows)
        agg["elapsed_s"] = round(time.perf_counter() - t2, 1)
        out["pairs"][name] = agg
        budget[bkey] += len(rows)
        phase_rows[name] = rows
        print(name, agg["h2h"], agg["wins"], agg["losses"], agg["ties"],
              agg["mean_margin"], "px", agg["ours"]["realized_px_median"],
              "tm", agg["ours"]["terminal_money_median"], agg["elapsed_s"], "s",
              flush=True)
        open(os.path.join(MODULE_DIR, "evidence", "pair_%s.json" % name),
             "w").write(json.dumps(agg, ensure_ascii=False, indent=1,
                                   default=str) + "\n")

    # ---- K1 剪毛相位对照表（实跑追踪口径 + 磁带口径）----
    h1_side = [{"arm": "h1", "shear_days": r.get("opp_shear_days")}
               for r in phase_rows["k1_vs_h1"]]
    phase = {
        "caliber_ingame": ("实跑追踪口径逐日剪毛数（HARVEST 取 WOOL；"
                           "k1_vs_h1 同局双席：k1 席 vs h1 席）"),
        "ingame_before_h1_side": shear_phase_agg(h1_side),
        "ingame_after_k1_side": shear_phase_agg(phase_rows["k1_vs_h1"]),
        "caliber_static_tape": "磁带口径逐日刀次（41 路由合计，_shear_cells）",
        "static_before": k1.static_shear_day_counts(
            k1._rs._decode_routes(open(H1_MAIN, encoding="utf-8").read())),
        "static_after": k1.static_shear_day_counts(
            k1._rs._decode_routes(open(K1_MAIN, encoding="utf-8").read())),
        "public_phase": list(k1.PUBLIC_PHASE),
    }
    out["shear_phase_table"] = phase

    budget["total_games"] = (budget["auth_games"] + budget["judgment_games"]
                             + budget["counter_games"])
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    open(os.path.join(MODULE_DIR, "evidence", "judge_k1_realrun.json"),
         "w").write(json.dumps(out, ensure_ascii=False, indent=1,
                               default=str) + "\n")
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    main()
