# -*- coding: utf-8 -*-
"""judge_iter1：组 I 增量移植判决（judgment_r27_v2/judge_strongest 同口径；判决先行·不发射）。

语料：26 败局回放种子（replays-r30-26 info.seed，judgment_r27_v2 同序）
    + 新中性块 672000+i*29 n=20（换新块防过拟合）→ 双席折叠 n=46。
臂集 {h1_base,i1,i2,i12,r40}；7 对：i1/i2/i12 × h1_base（增量效应）、
i1/i2/i12 × r40（不回退）、h1_base-r40（同语料参照）。
主判=形态 vs h1_base（增量效应）+ 形态 vs r40（不回退）。
sim_bridge 快线先对照认证 30/30（不过即停）；workers=2；预算 ≤450 局次。
判据（预登记）：对 h1_base h2h ≥0.55 ∧ 实现价非负 ∧ 非触发拍零足迹（安慰剂
恒等：层零改动局对 h1_base 逐局 banks 精确相等）∧ 对 r40 h2h 不降（≥0.80）；
I1 触发面统计必附（触发局数/释放量）。
读数：h2h/终局钱（**farms[obs.player].money 干净口径**，不用 farms[0] 污染
读数）/实现价中位/逐局 Δ；触发面=层台账（_I1_REPORT/_I2_REPORT）逐局快照。
复用（不改写）：judge_r23._load_entry/_Tracer、sim_bridge.run_games/sim_bridge。
只写 orderbook_iter1_lab/（evidence/）、fn_docs/hybrid/results/ 与 /tmp。
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
REPO = os.path.dirname(os.path.dirname(os.path.dirname(KSIM)))
if KSIM not in sys.path:
    sys.path.insert(0, KSIM)

RECORD_VERSION = "judge-iter1/1.0"
UNKNOWN = "UNKNOWN"

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
NEUTRAL_20 = [672000 + i * 29 for i in range(20)]
SEEDS = REPLAY_26 + NEUTRAL_20

R40_MAIN = os.path.join(KSIM, "orderbook_r40", "build", "main.py")
FORM_MAINS = {
    "h1_base": os.path.join(ROOT, "build", "h1_base", "main.py"),
    "i1": os.path.join(ROOT, "build", "i1", "main.py"),
    "i2": os.path.join(ROOT, "build", "i2", "main.py"),
    "i12": os.path.join(ROOT, "build", "i12", "main.py"),
}
ARMS = dict(FORM_MAINS)
ARMS["r40"] = R40_MAIN
PAIRS = [("i1", "h1_base"), ("i2", "h1_base"), ("i12", "h1_base"),
         ("i1", "r40"), ("i2", "r40"), ("i12", "r40"),
         ("h1_base", "r40")]
WORKERS = 2

EVID_HYBRID = os.path.join(REPO, "fn_docs", "hybrid", "results",
                           "2026-09-29-iter1-increments.json")


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


# ------------------------------------------------------------ 干净读数 --
def clean_reads(sink):
    """实现价 + 终局钱（**farms[obs.player].money**，避开 farms[0] 污染）。
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


# ------------------------------------------------------------ 局跑口 --
def _load_with_reports(path):
    """装载件并抓层台账引用（同 exec 命名空间，游戏结束后可读）。"""
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    entry = j23._load_entry(path)
    g = getattr(entry, "__globals__", {}) or {}
    reps = {}
    for k in ("_I1_REPORT", "_I2_REPORT"):
        if isinstance(g.get(k), dict):
            reps[k] = g[k]
    return entry, reps


def _chunk(payload):
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    specs = payload["specs"]
    cfg = dict(payload.get("cfg") or {})
    games, metas = [], []
    for spec in specs:
        try:
            sinks = {0: [], 1: []}
            agents = []
            arm_reps = None
            for seat, a in enumerate(spec["agents"]):
                entry, reps = _load_with_reports(a["path"])
                agents.append(j23._Tracer(entry, seat, sinks[seat]))
                if int(spec.get("our_seat", 0)) == seat:
                    arm_reps = reps
            games.append({"seed": int(spec["seed"]), "agents": agents})
            metas.append((spec, sinks, arm_reps))
        except Exception as exc:
            games.append({"seed": int(spec["seed"]), "agents": []})
            metas.append((spec, None, {"build_error": repr(exc)[:120]}))
    res = sb.run_games(games, cfg) if games else {"games": []}
    rows_run = list(res.get("games") or [])
    out = []
    for i, (spec, sinks, arm_reps) in enumerate(metas):
        rr = rows_run[i] if i < len(rows_run) else {}
        row = {"game_id": spec.get("game_id"), "seed": int(spec["seed"]),
               "seat": int(spec.get("our_seat", 0)), "arm": spec.get("arm"),
               "opp": spec.get("opp"), "group": spec.get("group"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "opp_reads": {},
               "arm_reports": {}, "arm_changed_turns": None}
        if isinstance(arm_reps, dict) and "build_error" in arm_reps:
            row["error"] = arm_reps["build_error"]
            sinks = None
        if isinstance(arm_reps, dict):
            snap = {}
            changed = 0
            for k, v in arm_reps.items():
                if isinstance(v, dict) and "build_error" not in v:
                    snap[k] = dict(v)
                    try:
                        changed += int(v.get("changed_turns") or 0)
                    except Exception:
                        pass
            row["arm_reports"] = snap
            row["arm_changed_turns"] = changed
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    row["reads"] = clean_reads(sink)
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
        "realized_px_min": round(min(pxs), 4) if pxs else UNKNOWN,
        "terminal_money_median": round(statistics.median(tms), 1) if tms else UNKNOWN,
        "terminal_money_mean": round(sum(tms) / len(tms), 1) if tms else UNKNOWN,
        "stranding_median": round(statistics.median(sts), 2) if sts else UNKNOWN,
    }


def aggregate(rows, engines):
    fold = fold_arm(rows)
    margins = [float(r["margin"]) for r in rows if is_num(r.get("margin"))]
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
        "engines": engines,
        "n_error_games": sum(1 for r in rows if r.get("error")),
    }
    return out


def rows_lite(rows):
    return [{"game_id": r["game_id"], "seed": r["seed"], "seat": r["seat"],
             "arm": r["arm"], "opp": r["opp"],
             "group": r["group"], "margin": r["margin"],
             "realized_px": (r.get("reads") or {}).get("realized_px"),
             "terminal_money": (r.get("reads") or {}).get("terminal_money"),
             "opp_realized_px": (r.get("opp_reads") or {}).get("realized_px"),
             "arm_changed_turns": r.get("arm_changed_turns"),
             "arm_reports": r.get("arm_reports"),
             "error": r["error"]} for r in rows]


def group_slice(rows, group):
    return [r for r in rows if r.get("group") == group]


def make_specs(arm_main, opp_main, arm, opp, seeds=None):
    seeds = list(SEEDS if seeds is None else seeds)
    specs = []
    for seed in seeds:
        group = ("neutral_672000_i29" if seed in set(NEUTRAL_20)
                 else "replay_r30_26")
        for seat in (0, 1):
            a = {"type": "python", "path": arm_main}
            b = {"type": "python", "path": opp_main}
            agents = [a, b] if seat == 0 else [b, a]
            specs.append({
                "game_id": "i1-%s-vs%s-%d-s%d" % (arm, opp, seed, seat),
                "seed": seed, "kind": "pair", "arm": arm, "opp": opp,
                "group": group, "our_seat": seat, "trace": True,
                "agents": agents})
    return specs


def zero_footprint_check(rows):
    """非触发拍零足迹（安慰剂恒等）：层零改动局（双席）对 h1_base 逐局 banks
    精确相等（两局皆 [P,P] 同种子跑口，确定性下必同）。"""
    by_seed = {}
    for r in rows or []:
        by_seed.setdefault(r.get("seed"), []).append(r)
    checked, matched, fails = 0, 0, []
    for seed in sorted(by_seed):
        rs = by_seed[seed]
        if len(rs) != 2:
            continue
        if any((r.get("arm_changed_turns") or 0) != 0 for r in rs):
            continue          # 有触发（改动）→不属安慰剂面
        checked += 1
        b0, b1 = rs[0].get("banks"), rs[1].get("banks")
        if b0 is not None and b0 == b1:
            matched += 1
        else:
            fails.append({"seed": seed, "banks_a": b0, "banks_b": b1})
    return {"n_checked": checked, "n_match": matched, "fails": fails}


def trigger_stats(rows, form):
    """触发面：逐局层台账快照→汇总（I1 必附 触发局数/释放量）。"""
    games = [r for r in rows if r.get("arm") == form and r.get("arm_reports")]
    acc_i1, acc_i2 = {}, {}
    trigger_games = 0
    trigger_ticks = 0
    for r in games:
        changed = int(r.get("arm_changed_turns") or 0)
        trigger_ticks += changed
        if changed > 0:
            trigger_games += 1
        for key, acc in (("_I1_REPORT", acc_i1), ("_I2_REPORT", acc_i2)):
            rep = (r.get("arm_reports") or {}).get(key) or {}
            for k, v in rep.items():
                if is_num(v):
                    acc[k] = acc.get(k, 0) + v
    out = {
        "form": form,
        "games_traced": len(games),
        "trigger_games": trigger_games,          # 触发局数（≥1 拍改动）
        "trigger_ticks": trigger_ticks,           # 触发拍数（层内改动）
    }
    if acc_i1:
        out["i1"] = {
            "released_units": round(acc_i1.get("released_units", 0), 1),  # 释放量
            "held_units": round(acc_i1.get("held_units", 0), 1),
            "added_units": int(acc_i1.get("added_units", 0)),
            "forced_release_units": round(acc_i1.get("forced_release_units", 0), 1),
            "gate_open_ticks": int(acc_i1.get("gate_open_ticks", 0)),
            "gate_closed_ticks": int(acc_i1.get("gate_closed_ticks", 0)),
            "release_ticks": int(acc_i1.get("release_ticks", 0)),
            "hold_ticks": int(acc_i1.get("hold_ticks", 0)),
            "revenue_checks": int(acc_i1.get("revenue_checks", 0)),
            "pressure_sum": round(acc_i1.get("pressure_sum", 0), 1),
            "day_px_sum": round(acc_i1.get("day_px_sum", 0), 1),
            "window_out": int(acc_i1.get("window_out", 0)),
            "no_tomato": int(acc_i1.get("no_tomato", 0)),
            "errors": int(acc_i1.get("errors", 0)) + int(acc_i1.get("gate_errors", 0)),
        }
    if acc_i2:
        out["i2"] = {
            "herd_gate_open_ticks": int(acc_i2.get("herd_gate_open_ticks", 0)),
            "herd_inserts": int(acc_i2.get("herd_inserts", 0)),
            "herd_insert_units": int(acc_i2.get("herd_insert_units", 0)),
            "herd_no_extra_ticks": int(acc_i2.get("herd_no_extra_ticks", 0)),
            "courier_ticks": int(acc_i2.get("courier_ticks", 0)),
            "courier_boosts": int(acc_i2.get("courier_boosts", 0)),
            "courier_boost_units": int(acc_i2.get("courier_boost_units", 0)),
            "courier_inserts": int(acc_i2.get("courier_inserts", 0)),
            "courier_insert_units": int(acc_i2.get("courier_insert_units", 0)),
            "courier_hoists": int(acc_i2.get("courier_hoists", 0)),
            "errors": int(acc_i2.get("errors", 0)),
        }
    return out


def _finalize(out, budget):
    """触发面/判据/verdict/anomaly 汇总 + judgment.json 与证据落档。

    可被 --recompute 复用（从 evidence/pair_*.json 行重算，不重跑局）。
    """
    # ---- 触发面 ----
    all_rows = []
    for name, agg in out["pairs"].items():
        arm, opp = name.split("_vs_")
        for r in (agg.get("rows_lite") or []):
            all_rows.append(dict(r, arm=r.get("arm") or arm,
                                 opp=r.get("opp") or opp))
    out["trigger_stats"] = {f: trigger_stats(all_rows, f)
                            for f in ("i1", "i2", "i12")}
    print("trigger:", json.dumps(out["trigger_stats"], ensure_ascii=False)[:600],
          flush=True)

    # ---- 判据（预登记）逐条 ----
    criteria = {}
    for form in ("i1", "i2", "i12"):
        vs_base = out["pairs"]["%s_vs_h1_base" % form]
        vs_r40 = out["pairs"]["%s_vs_r40" % form]
        ts = out["trigger_stats"][form]
        pxs = [float(r["realized_px"]) for r in
               (vs_base.get("rows_lite") or []) + (vs_r40.get("rows_lite") or [])
               if is_num(r.get("realized_px"))]
        c = {}
        c["c1_h2h_vs_h1_base_ge_0.55"] = {
            "value": vs_base.get("h2h"),
            "passed": is_num(vs_base.get("h2h")) and float(vs_base["h2h"]) >= 0.55}
        c["c2_realized_px_nonneg"] = {
            "value": {"min": round(min(pxs), 4) if pxs else UNKNOWN,
                      "median": vs_base.get("ours", {}).get("realized_px_median")},
            "passed": bool(pxs) and min(pxs) >= 0}
        zf = vs_base.get("zero_footprint_identity") or {}
        c["c3_zero_footprint_placebo_identity"] = {
            "value": {"n_checked": zf.get("n_checked"), "n_match": zf.get("n_match"),
                      "fails": zf.get("fails")},
            "passed": bool(zf.get("n_checked")) and zf.get("n_match") == zf.get("n_checked")}
        c["c4_h2h_vs_r40_ge_0.80"] = {
            "value": vs_r40.get("h2h"),
            "passed": is_num(vs_r40.get("h2h")) and float(vs_r40["h2h"]) >= 0.80}
        released = (ts.get("i1") or {}).get("released_units")
        if released is None:
            released = ((ts.get("i2") or {}).get("herd_insert_units", 0)
                        + (ts.get("i2") or {}).get("courier_boost_units", 0))
        c["i1_trigger_face_attached"] = {
            "value": {"trigger_games": ts.get("trigger_games"),
                      "released_units": released},
            "passed": True}
        all_pass = all(v.get("passed") for k, v in c.items()
                       if k != "i1_trigger_face_attached")
        criteria[form] = {"criteria": c, "all_passed": all_pass}
    out["criteria"] = criteria

    # ---- verdict ----
    verdict = {}
    for form in ("i1", "i2", "i12"):
        cr = criteria[form]["criteria"]
        failed = [k for k, v in cr.items()
                  if k != "i1_trigger_face_attached" and not v.get("passed")]
        verdict[form] = {
            "verdict": "接受为增量候选" if not failed else "否决（判据未过）",
            "failed_criteria": failed,
            "vs_h1_base_h2h": out["pairs"]["%s_vs_h1_base" % form].get("h2h"),
            "vs_r40_h2h": out["pairs"]["%s_vs_r40" % form].get("h2h"),
        }
    out["verdict"] = {
        "forms": verdict,
        "overall": ("全部形态判据通过→组 I 增量移植成立"
                    if all(v["verdict"].startswith("接受") for v in verdict.values())
                    else "存在否决形态→组 I 增量移植不成立（逐形态见 forms）"),
        "criteria_pre_registered":
            "对 h1_base h2h ≥0.55 ∧ 实现价非负 ∧ 非触发拍零足迹（安慰剂恒等）"
            "∧ 对 r40 h2h 不降（≥0.80）；I1 触发面统计必附（触发局数/释放量）",
    }

    # ---- anomaly / 噪声清单 ----
    ref = out["pairs"].get("h1_base_vs_r40") or {}
    out["anomaly"] = {
        "error_games": sum(a.get("n_error_games", 0) for a in out["pairs"].values()),
        "engine_fallbacks": [e for a in out["pairs"].values()
                             for e in (a.get("engines") or [])
                             if e.get("fallback_reason")],
        "harness_out_of_scope_writes_known_noise": [
            "gate_launch_fourgate_l1/sim_bridge 运行期遥测打印（HP_TELEMETRY 行）",
            "sim_bridge 记录件写入 evidence/sim_auth_record.json（已收口进 lab）",
            "kaggle_environments 装载期 stderr（open_spiel_env/cabt 缺件提示）",
            "judge_r23 装载期 sys.path 临时追加（不落盘）",
        ],
        "notes": [
            "I2 产线换畜种=磁带手术级不可移植（HERD 物种置换指令改写）；"
            "COURIER 走位送货=物理层不可移植；两件均如实报不硬做。",
            "statma ca25 与 H1 基底同源（前 7046 行仅差 3 处+95 个 CR 字节）："
            "H1 内层已含同族 V9_HERD/V9_COURIER 全层，I2 移植面=订单层切片的"
            "外层再实现（触发面实测窄，见 trigger_stats）。",
            "I1 阈值取源件紧档 9000/80=112.5 每单元（e087 放宽档 7500/80 不用），"
            "对应原语料唯一触发局 −741 的教训：触发条件宁紧勿松。",
            "c4 判据为绝对阈值 ≥0.80；同语料参照对 h1_base_vs_r40 h2h=%s"
            "（旧语料 671000+i*23 上 h1 对 r40 为 0.837）——本中性块上基底自身"
            "亦低于 0.80，逐形态对 r40 读数同时给了同语料相对口径（均未高于基底）。"
            % (ref.get("h2h"),),
        ],
    }

    open(os.path.join(ROOT, "evidence", "judgment.json"), "w").write(
        json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n")
    # ---- 证据落档（fn_docs/hybrid/results/）----
    evidence = {
        "_generated_at": out["_generated_at"],
        "source": out["source"],
        "budget": budget,
        "elapsed_s": out.get("elapsed_s"),
        "builds": json.load(open(os.path.join(ROOT, "evidence", "build_manifest.json"))),
        "gates": json.load(open(os.path.join(ROOT, "evidence", "gates.json"))),
        "pairs": {k: {kk: vv for kk, vv in v.items() if kk != "rows_lite"}
                  for k, v in out["pairs"].items()},
        "rows_lite": {k: v.get("rows_lite") for k, v in out["pairs"].items()},
        "trigger_stats": out["trigger_stats"],
        "criteria": out["criteria"],
        "verdict": out["verdict"],
        "anomaly": out["anomaly"],
    }
    zp = os.path.join(ROOT, "evidence", "zero_footprint_probe.json")
    if os.path.isfile(zp):
        evidence["zero_footprint_probe"] = json.load(open(zp))
    os.makedirs(os.path.dirname(EVID_HYBRID), exist_ok=True)
    open(EVID_HYBRID, "w").write(
        json.dumps(evidence, ensure_ascii=False, indent=1, default=str) + "\n")
    print("evidence ->", EVID_HYBRID, flush=True)


def recompute():
    """--recompute：从 evidence/pair_*.json 行重算触发面/判据/verdict（不重跑局）。"""
    out = json.load(open(os.path.join(ROOT, "evidence", "judgment.json")))
    for name in list(out.get("pairs") or {}):
        p = os.path.join(ROOT, "evidence", "pair_%s.json" % name)
        if os.path.isfile(p):
            out["pairs"][name] = json.load(open(p))
    out["_recompute_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    out["anomaly_note_recompute"] = (
        "首跑触发面汇总过滤键缺 arm 字段致 games_traced=0（行内台账快照完好）；"
        "已修 judge_iter1.rows_lite 并以 --recompute 从 pair_*.json 行重算，"
        "未重跑任何局。")
    budget = out.get("budget") or {}
    _finalize(out, budget)
    return out


def main():
    os.chdir(ROOT)
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433

    budget = {"cap_局次": 450, "auth_games": 0, "judgment_局次_folds": 0,
              "judgment_games": 0}
    out = {
        "_generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "version": RECORD_VERSION,
        "source": {
            "commands": ["python3 orderbook_iter1_lab/build_iter1.py",
                         "python3 orderbook_iter1_lab/gates_iter1.py",
                         "python3 orderbook_iter1_lab/judge_iter1.py"],
            "seed_base": 672000,
            "seed_stagger": "672000+i*29（局组错开；新中性块 n=20 防过拟合）",
            "replay_seeds_26": list(REPLAY_26),
            "neutral_seeds_20": list(NEUTRAL_20),
            "corpus_total_folds": len(SEEDS),
            "r40_main": R40_MAIN, "form_mains": dict(FORM_MAINS),
            "pairs": [list(p) for p in PAIRS],
            "workers": WORKERS,
            "terminal_money_caliber": "farms[obs.player].money（干净口径，非 farms[0]）",
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

    # ---- 7 对循环对决 ----
    for arm, opp in PAIRS:
        specs = make_specs(ARMS[arm], ARMS[opp], arm, opp)
        t2 = time.perf_counter()
        rows, engines = _play(specs, run_cfg)
        agg = aggregate(rows, engines)
        agg["replay_r30_26"] = aggregate(group_slice(rows, "replay_r30_26"), engines)
        agg["neutral_672000_i29"] = aggregate(group_slice(rows, "neutral_672000_i29"), engines)
        if opp == "h1_base":
            agg["zero_footprint_identity"] = zero_footprint_check(rows)
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

    budget["total_局次_folds"] = budget["judgment_局次_folds"]
    budget["total_games"] = budget["auth_games"] + budget["judgment_games"]

    out["elapsed_s"] = round(time.perf_counter() - t0, 1)
    _finalize(out, budget)
    print("DONE", out["elapsed_s"], "s budget:", budget, flush=True)
    return out


if __name__ == "__main__":
    if "--recompute" in sys.argv:
        recompute()
    else:
        main()
