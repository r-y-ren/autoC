# -*- coding: utf-8 -*-
"""judge_strongest：最强版本循环对决（judgment_r27_v2/analysis32 同口径；判决先行·不发射）。

语料：26 败局回放种子（replays-r30-26 info.seed，judgment_r27_v2 同序）
    + 新中性块 671000+i*23 n=20（换新块防过拟合）→ 双席折叠 n=46。
臂集 {h0,h1,h12,A,r40}；7 对：h0-h1、h0-h12、h1-A、h1-r40、h12-A、h0-A、h0-r40。
仪器四件套（R26 沿用）：placebo 恒等（placebo 件=纯注入恒等，逐局 banks 对 h0
精确相等）/ 单件消融（h1/h12）/ 同局配对（同语料同种子逐局 Δ）/ 翻胜主语
（margin=我席钱−对席钱，双席折叠）。
sim_bridge 快线先对照认证 30/30（不过即停）；workers=2。
读数：h2h/终局钱（**farms[obs.player].money 干净口径**，不用 judge_r26 的
farms[0] 污染读数）/实现价中位/逐局 Δ/d27 窗挂单墙前后对照（h0 vs h1）。
复用（不改写）：judge_r23._build_agents、sim_bridge.run_games/sim_bridge。
只写 orderbook_strongest_lab/（evidence/）与 /tmp。
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

RECORD_VERSION = "judge-strongest/1.0"
UNKNOWN = "UNKNOWN"

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
NEUTRAL_20 = [671000 + i * 23 for i in range(20)]
SEEDS = REPLAY_26 + NEUTRAL_20

A_MAIN = os.path.join(KSIM, "orderbook_r44_a", "main.py")
R40_MAIN = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
FORM_MAINS = {
    "h0": os.path.join(ROOT, "build", "h0", "main.py"),
    "h1": os.path.join(ROOT, "build", "h1", "main.py"),
    "h12": os.path.join(ROOT, "build", "h12", "main.py"),
    "placebo": os.path.join(ROOT, "build", "placebo", "main.py"),
}
ARMS = {"h0": FORM_MAINS["h0"], "h1": FORM_MAINS["h1"],
        "h12": FORM_MAINS["h12"], "A": A_MAIN, "r40": R40_MAIN}
PAIRS = [("h0", "h1"), ("h0", "h12"), ("h1", "A"), ("h1", "r40"),
         ("h12", "A"), ("h0", "A"), ("h0", "r40")]
WORKERS = 2


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ------------------------------------------------------------ 干净读数 --
def clean_reads(sink):
    """实现价 + 终局钱（**farms[obs.player].money**，避开 judge_r26 farms[0] 污染）。
    实现价=Σ(qty×卖时市价)/Σ(qty×该局该品日均价)（judge_r26 同式）。"""
    daily = {}
    sells = []          # (day,item,qty,px)
    last_obs = None
    for entry in (sink or []):
        step, obs, act = entry[0], entry[1], entry[2]
        if not isinstance(obs, dict):
            continue
        step = int(step)
        prices = ((obs.get("market") or {}) if isinstance(obs.get("market"),
                  dict) else {}).get("prices") or {}
        day = step // 24
        for item, px in (prices or {}).items():
            if isinstance(px, (int, float)):
                daily.setdefault((day, str(item)), []).append(float(px))
        if isinstance(act, dict):
            for cmd in (act.get("market") or []):
                if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                        and str(cmd[0]) == "SELL":
                    item = str(cmd[1])
                    px = prices.get(item)
                    if isinstance(px, (int, float)):
                        sells.append((day, item, float(cmd[2]), float(px)))
        last_obs = obs
    realized = UNKNOWN
    if sells:
        num = den = 0.0
        for day, item, qty, px in sells:
            pxs = daily.get((day, item)) or []
            avg = (sum(pxs) / len(pxs)) if pxs else px
            num += qty * px
            den += qty * avg
        realized = round(num / den, 4) if den > 0 else UNKNOWN
    terminal = UNKNOWN
    stranding = UNKNOWN
    if isinstance(last_obs, dict):
        # 干净终局钱：farms[obs.player].money（我席），非 farms[0]
        try:
            player = int(last_obs.get("player", 0))
        except Exception:
            player = 0
        farms = last_obs.get("farms")
        if isinstance(farms, list) and player < len(farms) \
                and isinstance(farms[player], dict):
            try:
                terminal = round(float(farms[player].get("money", 0.0)), 2)
            except (TypeError, ValueError):
                pass
        prices = ((last_obs.get("market") or {}) if isinstance(
            last_obs.get("market"), dict) else {}).get("prices") or {}
        shed = ((last_obs.get("private") or {}) if isinstance(
            last_obs.get("private"), dict) else {}).get("shed") or {}
        total = 0.0
        for item, qty in (shed or {}).items():
            try:
                total += float(prices.get(item, 0)) * float(qty)
            except (TypeError, ValueError):
                continue
        stranding = round(total, 2)
    return {"realized_px": realized, "terminal_money": terminal,
            "stranding": stranding}


def wall_stats(sink):
    """d27+ 挂单墙读数：step>=624 请求量/单均量/qty>库存幻影单计数。"""
    rows = []
    for entry in (sink or []):
        step, obs, act = entry[0], entry[1], entry[2]
        step = int(step)
        if not isinstance(act, dict):
            continue
        shed = ((obs or {}).get("private") or {}).get("shed") or {}
        if not isinstance(shed, dict):
            shed = {}
        for cmd in (act.get("market") or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3 \
                    and str(cmd[0]) == "SELL":
                try:
                    qty = float(cmd[2])
                except (TypeError, ValueError):
                    continue
                item = str(cmd[1])
                try:
                    held = float(shed.get(item, 0))
                except (TypeError, ValueError):
                    held = 0.0
                rows.append((step, step // 24, item, qty, held))

    def _agg(sel):
        n = len(sel)
        qty = sum(r[3] for r in sel)
        ph = [r for r in sel if r[3] > r[4]]
        return {"orders": n, "qty_total": round(qty, 1),
                "avg_qty_per_order": round(qty / n, 2) if n else UNKNOWN,
                "max_qty": round(max((r[3] for r in sel), default=0.0), 1),
                "phantom_orders_qty_gt_held": len(ph),
                "phantom_qty_over_held": round(sum(r[3] - r[4] for r in ph), 1),
                "big_orders_qty_ge_500": sum(1 for r in sel if r[3] >= 500)}
    return {"all_days": _agg(rows),
            "step_ge_624": _agg([r for r in rows if r[0] >= 624]),
            "step_670_695": _agg([r for r in rows if 670 <= r[0] <= 695]),
            "d27": _agg([r for r in rows if r[1] == 27])}


# ------------------------------------------------------------ 局跑口 --
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
               "opp": spec.get("opp"), "group": spec.get("group"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "opp_reads": {}, "wall": {}}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    row["reads"] = clean_reads(sink)
                    row["wall"] = wall_stats(sink)
                other = sinks.get(1 - row["seat"])
                if other is not None:
                    row["opp_reads"] = clean_reads(other)
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


def _wall_agg(bs_list):
    def _sum(key, sub):
        return sum((b.get(sub, {}).get(key, 0) or 0) for b in bs_list)
    out = {"n_games_traced": len(bs_list)}
    for sub in ("all_days", "step_ge_624", "step_670_695", "d27"):
        orders = _sum("orders", sub)
        qty = round(_sum("qty_total", sub), 1)
        out[sub] = {
            "orders_total": orders, "qty_total": qty,
            "avg_qty_per_order": round(qty / orders, 2) if orders else UNKNOWN,
            "max_qty": max((b.get(sub, {}).get("max_qty", 0) or 0)
                           for b in bs_list) if bs_list else 0,
            "phantom_orders_qty_gt_held": _sum("phantom_orders_qty_gt_held", sub),
            "phantom_qty_over_held": round(_sum("phantom_qty_over_held", sub), 1),
            "big_orders_qty_ge_500": _sum("big_orders_qty_ge_500", sub),
        }
    return out


def aggregate(rows, engines):
    fold = fold_arm(rows)
    margins = [float(r["margin"]) for r in rows if is_num(r.get("margin"))]
    walls = [r["wall"] for r in rows if isinstance(r.get("wall"), dict)
             and "all_days" in r["wall"]]
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
        "wall": _wall_agg(walls),
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
             "d27_orders": (r.get("wall") or {}).get("d27", {}).get("orders"),
             "d27_avg": (r.get("wall") or {}).get("d27", {}).get("avg_qty_per_order"),
             "error": r["error"]} for r in rows]


def group_slice(rows, group):
    return [r for r in rows if r.get("group") == group]


def make_specs(arm_main, opp_main, arm, opp, seeds=None):
    seeds = list(SEEDS if seeds is None else seeds)
    specs = []
    for seed in seeds:
        group = ("neutral_671000_i23" if seed in set(NEUTRAL_20)
                 else "replay_r30_26")
        for seat in (0, 1):
            a = {"type": "python", "path": arm_main}
            b = {"type": "python", "path": opp_main}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "hs-%s-vs%s-%d-s%d" % (arm, opp, seed, seat),
                "seed": seed, "kind": "pair", "arm": arm, "opp": opp,
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


def main():
    os.chdir(ROOT)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    budget = {"cap_局次": 450, "auth_games": 0, "judgment_局次_folds": 0,
              "judgment_games": 0, "gate_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_strongest_lab/build_strongest.py",
                         "python3 orderbook_strongest_lab/gates_strongest.py",
                         "python3 orderbook_strongest_lab/judge_strongest.py"],
            "seed_base": 671000,
            "seed_stagger": "671000+i*23（局组错开；新中性块 n=20 防过拟合）",
            "replay_seeds_26": list(REPLAY_26),
            "neutral_seeds_20": list(NEUTRAL_20),
            "corpus_total_folds": len(SEEDS),
            "a_main": A_MAIN, "r40_main": R40_MAIN, "form_mains": dict(FORM_MAINS),
            "pairs": [list(p) for p in PAIRS],
            "workers": WORKERS,
            "terminal_money_caliber": "farms[obs.player].money（干净口径，非 judge_r26 farms[0]）",
        },
        "pairs": {},
        "budget": budget,
        "elapsed_s": 0.0,
    }
    t0 = time.perf_counter()

    # ---- sim_bridge 对照认证 30/30（不过即停） ----
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
    print("sim auth:", auth_lite.get("consistency_ok"), auth_lite.get("consistency"),
          flush=True)
    if not auth_lite.get("consistency_ok"):
        out["aborted"] = "sim_bridge 对照认证未过 30/30"
        out["source"]["sim_auth"] = auth_lite
        out["elapsed_s"] = round(time.perf_counter() - t0, 1)
        open(os.path.join(ROOT, "evidence", "judgment.json"), "w").write(
            json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
        print("ABORT", out["aborted"], flush=True)
        return out
    out["source"]["sim_auth"] = auth_lite
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- placebo 恒等（placebo 件=纯注入恒等；对 h0 逐局 banks 精确相等）----
    pb_seeds = [REPLAY_26[0], REPLAY_26[25], NEUTRAL_20[0], NEUTRAL_20[19]]
    specs = make_specs(FORM_MAINS["placebo"], ARMS["h0"], "placebo", "h0",
                       seeds=pb_seeds)
    rows_pb, _ = _play(specs, run_cfg)
    budget["gate_games"] += len(rows_pb)
    h0_by_key = {}
    specs_h0 = make_specs(ARMS["h0"], FORM_MAINS["placebo"], "h0", "placebo",
                          seeds=pb_seeds)
    rows_h0, _ = _play(specs_h0, run_cfg)
    budget["gate_games"] += len(rows_h0)
    h0_by_key = {(r["seed"], r["seat"]): r for r in rows_h0}
    pb_cmp = []
    for r in rows_pb:
        b = h0_by_key.get((r["seed"], r["seat"]))
        pb_cmp.append({"seed": r["seed"], "seat": r["seat"],
                       "banks_match": bool(b is not None and r.get("banks") == b.get("banks")),
                       "margin": r.get("margin"), "h0_margin": (b or {}).get("margin")})
    out["placebo_identity"] = {"n_checked": len(pb_cmp),
                               "n_match": sum(1 for c in pb_cmp if c["banks_match"]),
                               "detail": pb_cmp}
    print("placebo identity:", out["placebo_identity"]["n_match"], "/",
          out["placebo_identity"]["n_checked"], flush=True)

    # ---- 7 对循环对决 ----
    for arm, opp in PAIRS:
        specs = make_specs(ARMS[arm], ARMS[opp], arm, opp)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        agg = aggregate(rows, engines)
        agg["replay_r30_26"] = aggregate(group_slice(rows, "replay_r30_26"), engines)
        agg["neutral_671000_i23"] = aggregate(group_slice(rows, "neutral_671000_i23"), engines)
        agg["rows_lite"] = rows_lite(rows)
        agg["elapsed_s"] = round(time.perf_counter() - t2, 1)
        out["pairs"]["%s_vs_%s" % (arm, opp)] = agg
        budget["judgment_局次_folds"] += len(SEEDS)
        budget["judgment_games"] += len(rows)
        print(arm, "vs", opp, agg["h2h"], agg["wins"], agg["losses"], agg["ties"],
              agg["mean_margin"], "px", agg["ours"]["realized_px_median"],
              "tm", agg["ours"]["terminal_money_median"], agg["elapsed_s"], "s",
              flush=True)
        open(os.path.join(ROOT, "evidence", "pair_%s_vs_%s.json" % (arm, opp)),
             "w").write(json.dumps(agg, ensure_ascii=False, indent=1, default=str) + "\n")

    budget["total_局次_folds"] = budget["judgment_局次_folds"] + budget["gate_games"] // 2
    budget["total_games"] = budget["auth_games"] + budget["judgment_games"] + budget["gate_games"]
    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    open(os.path.join(ROOT, "evidence", "judgment.json"), "w").write(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    main()
