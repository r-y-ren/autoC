# -*- coding: utf-8 -*-
"""judge_d27：d27 实验室判决（judgment_r27_v2/analysis32 同口径；判决先行·不发射）。

语料：26 败局回放种子（replays-r30-26 info.seed，judgment_r27_v2 同序）
    + 660000 起补种子 n=24（局组 660000+i*19 错开）→ 双席折叠 n=50。
主判=形态 vs r40（orderbook_r40/build/main.py）与 vs A（orderbook_r44_a/main.py）；
基线=A vs r40 同语料（同局配对锚+安慰剂恒等参照）。
仪器四件套（R26 沿用）：安慰剂=纯注入恒等（placebo 件 + 逐拍回放恒等）/
单件消融（x1、x2 单出）/ 同局配对（同一语料同种子逐局 Δ）/ 翻胜主语
（margin=形态席钱−对席钱，双席折叠）。
sim_bridge 快线先对照认证 30/30（不过即停）；workers=2。
读数：h2h/终局钱/实现价中位（judge_r26.realized_price_stats 复用）/
d27 窗挂单数与单均量前后对照（墙核心信号）/逐局 Δ。
复用（不改写）：judge_r23._load_entry/_build_agents、judge_r26.realized_price_stats、
sim_bridge.run_games/sim_bridge。行为分解+墙读数为本驱动新增。

只写 orderbook_d27_lab/（evidence/）与 /tmp。
"""
from __future__ import annotations

import json
import multiprocessing
import os
import statistics
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
KSIM = os.path.dirname(ROOT)
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

RECORD_VERSION = "judge-d27-lab/1.0"
UNKNOWN = "UNKNOWN"

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]                                   # 26 败局回放种子
FILL_24 = [660000 + i * 19 for i in range(24)]  # 补种子（局组 660000+i*19）
SEEDS = REPLAY_26 + FILL_24

A_MAIN = os.path.join(KSIM, "orderbook_r44_a", "main.py")
R40_MAIN = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
FORM_MAINS = {
    "placebo": os.path.join(ROOT, "build", "placebo", "main.py"),
    "x1": os.path.join(ROOT, "build", "x1", "main.py"),
    "x2": os.path.join(ROOT, "build", "x2", "main.py"),
    "x12": os.path.join(ROOT, "build", "x12", "main.py"),
}
MATRIX_FORMS = ("x1", "x2", "x12")
OPPONENTS = {"r40": R40_MAIN, "A_r44a": A_MAIN}
WORKERS = 2
PLACEBO_SLICE_SEEDS = [REPLAY_26[0], REPLAY_26[26 - 1], FILL_24[0], FILL_24[23]]
IDENTITY_TRACE_SEED = REPLAY_26[0]


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ------------------------------------------------------------ 墙/行为读数 --
def behavior_stats(sink):
    """我席 traced sink [(step, obs_dict, act)] → 卖单行为+按日挂量墙读数。"""
    sells = []            # (step, day, item, qty)
    for entry in (sink or []):
        step, obs, act = entry[0], entry[1], entry[2]
        step = int(step)
        if isinstance(act, dict):
            for cmd in (act.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                        and str(cmd[0]) == "SELL":
                    try:
                        qty = float(cmd[2])
                    except (TypeError, ValueError):
                        continue
                    sells.append((step, step // 24, str(cmd[1]), qty))
    by_day = {}
    for step, day, item, qty in sells:
        d = by_day.setdefault(day, {"orders": 0, "qty": 0.0})
        d["orders"] += 1
        d["qty"] += qty
    for d in by_day.values():
        d["qty"] = round(d["qty"], 1)
        d["avg_qty_per_order"] = (round(d["qty"] / d["orders"], 2)
                                  if d["orders"] else UNKNOWN)
    n = len(sells)
    qty_total = sum(s[3] for s in sells)
    d27 = by_day.get(27, {"orders": 0, "qty": 0.0})
    d28 = by_day.get(28, {"orders": 0, "qty": 0.0})
    return {
        "n_sell_orders": n,
        "sell_qty_total": round(qty_total, 1),
        "sell_qty_mean_per_order": round(qty_total / n, 2) if n else UNKNOWN,
        "by_day": by_day,
        "d27_orders": d27["orders"], "d27_qty": d27["qty"],
        "d27_avg_qty_per_order": d27.get("avg_qty_per_order", UNKNOWN),
        "d28_orders": d28["orders"], "d28_qty": d28["qty"],
        "d28_avg_qty_per_order": d28.get("avg_qty_per_order", UNKNOWN),
    }


def wall_aggregate(bs_list):
    """逐局墙读数→聚合（d27/d28 窗口：挂单数/请求量/单均量 + 全期）。"""
    def _sum(key):
        return sum(b.get(key, 0) or 0 for b in bs_list)

    out = {"n_games_traced": len(bs_list)}
    for tag, ok, qk in (("d27", "d27_orders", "d27_qty"),
                        ("d28", "d28_orders", "d28_qty")):
        orders, qty = _sum(ok), round(_sum(qk), 1)
        out[tag] = {
            "orders_total": orders,
            "orders_mean_per_game": round(orders / len(bs_list), 2) if bs_list else UNKNOWN,
            "qty_total": qty,
            "qty_mean_per_game": round(qty / len(bs_list), 1) if bs_list else UNKNOWN,
            "avg_qty_per_order": round(qty / orders, 2) if orders else UNKNOWN,
        }
    n_orders = _sum("n_sell_orders")
    qty_all = round(_sum("sell_qty_total"), 1)
    out["all_days"] = {
        "orders_total": n_orders,
        "qty_total": qty_all,
        "avg_qty_per_order": round(qty_all / n_orders, 2) if n_orders else UNKNOWN,
    }
    return out


# ------------------------------------------------------------ 局跑口 --
def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    from orderbook_r43 import judge_r26 as j26  # noqa: WPS433
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
               "margin": None, "reads": {}, "opp_reads": {}, "behavior": {}}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - \
                float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    row["reads"] = j26.realized_price_stats(sink)
                    row["behavior"] = behavior_stats(sink)
                other = sinks.get(1 - row["seat"])
                if other is not None:
                    row["opp_reads"] = j26.realized_price_stats(other)
                save = cfg.get("trace_save")
                if save == (int(spec["seed"]), int(spec.get("our_seat", 0))) \
                        and sink is not None:
                    row["_trace"] = [(int(s), o, a) for s, o, a in sink]
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


def fold_arm(rows):
    """judge_r44._fold_arm 同口径：同 seed 双席折叠独立局，缺/红记负。"""
    pairs = {}
    for r in rows or []:
        pairs.setdefault(r.get("seed"), []).append(r)
    wins = losses = ties = 0
    margins = []
    for seed in sorted(pairs):
        rs = pairs[seed]
        ms = [float(r["margin"]) for r in rs if is_num(r.get("margin"))]
        if len(rs) != 2 or len(ms) != 2:
            losses += 1
            margins.extend(ms)
            continue
        score = sum(1.0 if m > 0 else 0.5 if m == 0 else 0.0 for m in ms) / 2.0
        margins.append(sum(ms) / 2.0)
        if score >= 1.0:
            wins += 1
        elif score <= 0.0:
            losses += 1
        else:
            ties += 1
    n = len(pairs)
    return {"n": n, "wins": wins, "losses": losses, "ties": ties,
            "h2h": round((wins + 0.5 * ties) / n, 4) if n else UNKNOWN,
            "mean_margin": round(sum(margins) / len(margins), 1) if margins else UNKNOWN,
            "fold_margins": [round(m, 1) for m in margins]}


def _reads_agg(rows, key):
    pxs = [float(r[key]["realized_px"]) for r in rows
           if isinstance(r.get(key), dict) and is_num(r[key].get("realized_px"))]
    tms = [float(r[key]["terminal_money"]) for r in rows
           if isinstance(r.get(key), dict) and is_num(r[key].get("terminal_money"))]
    sts = [float(r[key]["stranding"]) for r in rows
           if isinstance(r.get(key), dict) and is_num(r[key].get("stranding"))]
    return {
        "realized_px_median": round(statistics.median(pxs), 4) if pxs else UNKNOWN,
        "realized_px_mean": round(sum(pxs) / len(pxs), 4) if pxs else UNKNOWN,
        "terminal_money_median": round(statistics.median(tms), 1) if tms else UNKNOWN,
        "terminal_money_mean": round(sum(tms) / len(tms), 1) if tms else UNKNOWN,
        "stranding_median": round(statistics.median(sts), 2) if sts else UNKNOWN,
    }


def aggregate(rows, engines):
    fold = fold_arm(rows)
    margins = [float(r["margin"]) for r in rows if is_num(r.get("margin"))]
    bs = [r["behavior"] for r in rows if isinstance(r.get("behavior"), dict)
          and "n_sell_orders" in r["behavior"]]
    out = {
        "n_games": len(rows),
        "wins": fold["wins"], "losses": fold["losses"], "ties": fold["ties"],
        "h2h": fold["h2h"], "mean_margin": fold["mean_margin"],
        "fold_margins": fold["fold_margins"],
        "margin_per_game": {
            "mean": round(sum(margins) / len(margins), 1) if margins else UNKNOWN,
            "median": round(statistics.median(margins), 1) if margins else UNKNOWN,
            "min": round(min(margins), 1) if margins else UNKNOWN,
            "max": round(max(margins), 1) if margins else UNKNOWN},
        "ours": _reads_agg(rows, "reads"),
        "opp_side": _reads_agg(rows, "opp_reads"),
        "wall": wall_aggregate(bs),
        "engines": engines,
        "n_error_games": sum(1 for r in rows if r.get("error")),
    }
    return out


def rows_lite(rows):
    return [{"game_id": r["game_id"], "seed": r["seed"], "seat": r["seat"],
             "group": r["group"], "margin": r["margin"],
             "realized_px": (r.get("reads") or {}).get("realized_px"),
             "terminal_money": (r.get("reads") or {}).get("terminal_money"),
             "opp_realized_px": (r.get("opp_reads") or {}).get("realized_px"),
             "d27_orders": (r.get("behavior") or {}).get("d27_orders"),
             "d27_qty": (r.get("behavior") or {}).get("d27_qty"),
             "d27_avg": (r.get("behavior") or {}).get("d27_avg_qty_per_order"),
             "error": r["error"]} for r in rows]


def group_slice(rows, group):
    return [r for r in rows if r.get("group") == group]


def make_specs(arm_main, opp_main, arm, opp, seeds=None):
    seeds = list(SEEDS if seeds is None else seeds)
    specs = []
    for seed in seeds:
        group = ("fill_660000_i19" if seed in set(FILL_24)
                 else "replay_r30_26")
        for seat in (0, 1):
            a = {"type": "python", "path": arm_main}
            b = {"type": "python", "path": opp_main}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "d27-%s-vs%s-%d-s%d" % (arm, opp, seed, seat),
                "seed": seed, "kind": "pair", "arm": arm, "opp": opp,
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


# ------------------------------------------------------------ 恒等门 --
def load_entry(path):
    ns = {}
    src = open(path, "r", encoding="utf-8").read()
    exec(compile(src, path, "exec"), ns)
    entries = [v for v in ns.values() if callable(v)]
    return entries[-1], ns


def identity_gate(trace_rows):
    """逐拍回放恒等：同 obs 序列喂 A 件与各形态件，逐拍动作对比。

    判定：placebo 须全拍恒等；x1/x2/x12 差异拍 ⊆ 实验层触发改动拍（回放
    输入相同→基座状态演化相同→差异当且仅当后处理改写；差异数=改动数）。
    """
    a_agent, _ = load_entry(A_MAIN)
    a_actions, fidelity = [], 0
    for i, row in enumerate(trace_rows):
        step, obs, act = row[0], row[1], row[2]
        got = a_agent(obs)
        a_actions.append(got)
        if got == act:
            fidelity += 1
    out = {
        "n_steps": len(trace_rows),
        "a_replay_vs_recorded_match": fidelity,
        "a_replay_fidelity_ok": fidelity == len(trace_rows),
        "forms": {},
    }
    for form, path in FORM_MAINS.items():
        f_agent, ns = load_entry(path)
        diffs = []
        for i, row in enumerate(trace_rows):
            got = f_agent(row[1])
            if got != a_actions[i]:
                diffs.append(int(row[0]))
        entry = {
            "n_diff_steps": len(diffs),
            "diff_steps_head": diffs[:20],
            "identity": len(diffs) == 0,
        }
        if form in ("x1", "x2"):
            rep = ns.get("_X1_REPORT") or ns.get("_X2_REPORT") or {}
            entry["layer_report"] = dict(rep)
        if form == "x12":
            entry["layer_report"] = {"x1": dict(ns.get("_X1_REPORT") or {}),
                                     "x2": dict(ns.get("_X2_REPORT") or {})}
        out["forms"][form] = entry
    return out


# ------------------------------------------------------------ 主跑口 --
def main():
    os.chdir(ROOT)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    budget = {"cap_局次": 400, "auth_games": 0, "judgment_局次_folds": 0,
              "judgment_games": 0, "gate_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_d27_lab/build_d27.py",
                         "python3 orderbook_d27_lab/judge_d27.py"],
            "seed_base": 660000,
            "seed_stagger": "660000+i*19（局组错开；补种子 n=24）",
            "replay_seeds_26": list(REPLAY_26),
            "fill_seeds_24": list(FILL_24),
            "corpus_total_folds": len(SEEDS),
            "r40_main": R40_MAIN, "a_main": A_MAIN,
            "form_mains": dict(FORM_MAINS),
            "workers": WORKERS,
        },
        "arms": {},
        "budget": budget,
        "elapsed_s": 0.0,
    }
    t0 = time.perf_counter()

    # ---- sim_bridge 快线先对照认证（30/30；不过即停） ----
    auth_corpus = list(REPLAY_26) + [2026092901, 2026092902, 2026092903,
                                     2026092904]
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": os.path.join(ROOT, "evidence", "sim_auth_record.json")},
        auth_corpus)
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    open(os.path.join(ROOT, "evidence", "sim_auth.json"), "w").write(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str) + "\n")
    budget["auth_games"] = 60
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["source"]["sim_auth"] = auth_lite
        out["elapsed_s"] = round(time.perf_counter() - t0, 1)
        open(os.path.join(ROOT, "evidence", "judgment.json"), "w").write(
            json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
        print("ABORT", out["aborted"], flush=True)
        return out
    out["source"]["sim_auth"] = auth_lite

    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS,
               "trace_save": (IDENTITY_TRACE_SEED, 0)}

    # ---- 基线：A vs r40（同语料同种子；墙"前"读数+安慰剂恒等参照） ----
    t1 = time.perf_counter()
    specs = make_specs(A_MAIN, R40_MAIN, "A_r44a", "r40")
    rows_base, engines = _play(specs, run_cfg)
    base = aggregate(rows_base, engines)
    base["replay_r30_26"] = aggregate(group_slice(rows_base, "replay_r30_26"), engines)
    base["fill_660000_i19"] = aggregate(group_slice(rows_base, "fill_660000_i19"), engines)
    base["rows_lite"] = rows_lite(rows_base)
    base["elapsed_s"] = round(time.perf_counter() - t1, 1)
    out["arms"]["A_vs_r40_baseline"] = base
    budget["judgment_局次_folds"] += 50
    budget["judgment_games"] += len(rows_base)
    print("baseline A vs r40:", base["h2h"], base["wins"], base["losses"],
          base["ties"], base["mean_margin"], base["elapsed_s"], "s",
          flush=True)

    # ---- 恒等门（用基线首局同席 trace 逐拍回放） ----
    trace_rows = None
    for r in rows_base:
        if r.get("seed") == IDENTITY_TRACE_SEED and r.get("seat") == 0 \
                and not r.get("error"):
            trace_rows = r.get("_trace")
            break
    gate = {"skipped": True}
    if trace_rows:
        gate = identity_gate(trace_rows)
        gate["skipped"] = False
        gate["trace_seed"] = IDENTITY_TRACE_SEED
        open(os.path.join(ROOT, "evidence", "identity_trace_acts.json"),
             "w").write(json.dumps(
                 [{"step": r[0], "act": r[2]} for r in trace_rows],
                 ensure_ascii=False, default=str) + "\n")
    for r in rows_base:
        r.pop("_trace", None)  # 释放回放内存
    out["identity_gate"] = gate
    print("identity gate:", json.dumps(
        {k: (v if not isinstance(v, dict) else {kk: vv.get("n_diff_steps")
                                                for kk, vv in v.items()})
         for k, v in gate.items() if k in ("n_steps", "forms")},
        ensure_ascii=False), flush=True)

    # ---- 安慰剂恒等抽样（placebo vs r40 同种子逐局 banks 对基线精确相等） ----
    specs = make_specs(FORM_MAINS["placebo"], R40_MAIN, "placebo", "r40",
                       seeds=PLACEBO_SLICE_SEEDS)
    rows_pb, engines_pb = _play(specs, run_cfg)
    budget["gate_games"] += len(rows_pb)
    base_by_key = {(r["seed"], r["seat"]): r for r in rows_base}
    pb_cmp = []
    for r in rows_pb:
        b = base_by_key.get((r["seed"], r["seat"]))
        pb_cmp.append({"seed": r["seed"], "seat": r["seat"],
                       "banks_match": bool(b is not None
                                           and r.get("banks") == b.get("banks")),
                       "margin": r.get("margin"),
                       "baseline_margin": (b or {}).get("margin")})
    placebo = {"n_checked": len(pb_cmp),
               "n_match": sum(1 for c in pb_cmp if c["banks_match"]),
               "detail": pb_cmp}
    out["placebo_identity"] = placebo
    print("placebo identity:", placebo["n_match"], "/", placebo["n_checked"],
          flush=True)

    # ---- 消融矩阵：x1/x2/x12 × vs r40 / vs A ----
    for form in MATRIX_FORMS:
        for opp, opp_path in OPPONENTS.items():
            specs = make_specs(FORM_MAINS[form], opp_path, form, opp)
            t2 = time.perf_counter()
            rows, engines = _play(specs, run_cfg)
            agg = aggregate(rows, engines)
            agg["replay_r30_26"] = aggregate(
                group_slice(rows, "replay_r30_26"), engines)
            agg["fill_660000_i19"] = aggregate(
                group_slice(rows, "fill_660000_i19"), engines)
            agg["rows_lite"] = rows_lite(rows)
            agg["elapsed_s"] = round(time.perf_counter() - t2, 1)
            out["arms"]["%s_vs_%s" % (form, opp)] = agg
            budget["judgment_局次_folds"] += 50
            budget["judgment_games"] += len(rows)
            print(form, "vs", opp, agg["h2h"], agg["wins"], agg["losses"],
                  agg["ties"], agg["mean_margin"], agg["elapsed_s"], "s",
                  flush=True)
            open(os.path.join(ROOT, "evidence",
                              "judgment_%s_vs_%s.json" % (form, opp)),
                 "w").write(json.dumps(agg, ensure_ascii=False, indent=1,
                                       default=str) + "\n")

    budget["total_局次_folds"] = (budget["judgment_局次_folds"]
                                 + budget["gate_games"] // 2)
    budget["total_games"] = (budget["auth_games"] + budget["judgment_games"]
                             + budget["gate_games"])
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    open(os.path.join(ROOT, "evidence", "judgment.json"), "w").write(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
    print("DONE", out["elapsed_s"], "s", "budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    main()
