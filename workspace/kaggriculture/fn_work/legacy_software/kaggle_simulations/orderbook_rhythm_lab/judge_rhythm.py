# -*- coding: utf-8 -*-
"""judge_rhythm：产线相位变体 vs H1 配对因果 A/B（prod-rhythm；判决先行·不发射）。

责任口径（任务 prod-rhythm；分析38 诊断④"残差在生产节奏"）：
- 变体=chain 转位相位手术（rhythm_variants；量守恒+逐事件审计+孪生三闸先行，
  违规即弃）；基底=orderbook_strongest_lab/build/h1/main.py（sha 76b5f842…）。
- 配对口径（ab_r41/ab_t1b 净翻胜定义）：control=H1 原版 vs 对手 O，arm=变体
  vs 同一 O，同 seed+seat 配对；margin=终局 banks[our]−banks[opp]（**farms[
  obs.player].money 干净口径同源**，逐局交叉核对入 anomaly）。
- 判据：净翻胜>0（net_flip_wins=win_variant−win_control）∧ 胜局对照不翻负
  （flips_neg==0）= 正臂。
- 语料：26 败局回放（canonical 前 6 fold）+ 新中性块 672000+i*73（i=0..5）
  → n=12 双席 fold/变体；对手 j23.DEFAULT_OPPONENTS 按 fold 轮转。
- sim_bridge 对照认证 30/30 先行（不过即停）；workers=2；预算 ≤300 局次
  （control 24 + 24×变体数）。
- rhythm_stats：逐日可售产出量对照摘要（shed 净变动+实卖请求−买入请求）
  + 实现 %4 相位直方（处理生效核对）。
证据边跑边写 fn_docs/hybrid/results/2026-09-29-prod-rhythm.json；账本落
orderbook_rhythm_lab/evidence/。复用（不改写）：judge_r23._build_agents、
sim_bridge.run_games/sim_bridge、tape_variants.feasibility_twin。
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing
import os
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List

MODULE_DIR = Path(__file__).resolve().parent
KSIM_DIR = MODULE_DIR.parent
REPO = KSIM_DIR.parents[2]
if str(KSIM_DIR) not in sys.path:
    sys.path.insert(0, str(KSIM_DIR))

import rhythm_variants as rv  # noqa: E402

RECORD_VERSION = "prod-rhythm/1.0"
UNKNOWN = "UNKNOWN"
DAY = 24
N_DAYS = 30

REPLAY_26 = [1825501814, 2013941152, 786146079, 1883261866, 963182245,
             240876256, 1705553586, 2009279466, 161402123, 435866961,
             841473039, 1388158282, 1647385154, 671940665, 219073637,
             1439493993, 1360429471, 671494671, 1900972921, 973657130,
             1911990026, 1918725083, 176568822, 427304807, 720683523,
             906608145]
LOSS_FOLDS = REPLAY_26[:6]                    # 26 败局 canonical 前 6 fold
NEUTRAL_FOLDS = [672000 + i * 73 for i in range(6)]   # 新中性块 672000+i*73
FOLDS = LOSS_FOLDS + NEUTRAL_FOLDS            # n=12 双席 fold/变体

WORKERS = 2
BUDGET_CAP_GAMES = 300
EVID_PATH = REPO / "fn_docs" / "hybrid" / "results" / \
    "2026-09-29-prod-rhythm.json"
LEDGER_PATH = MODULE_DIR / "evidence" / "rhythm_ab_ledger.json"

EV: Dict[str, Any] = {}
ANOMALIES: List[str] = []


def is_num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def flush_evid():
    """边跑边落盘（每次阶段完成即写）。"""
    EV["anomaly"] = list(ANOMALIES)
    EV["_generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    EVID_PATH.parent.mkdir(parents=True, exist_ok=True)
    EVID_PATH.write_text(json.dumps(EV, ensure_ascii=False, indent=1,
                                    default=str) + "\n", encoding="utf-8")


# ------------------------------------------------------------ 读数 --
def rhythm_reads(sink):
    """逐日可售产出量（shed 净变动+实卖请求−买入请求）+ 实现 %4 相位直方。"""
    day_first_shed: Dict[int, float] = {}
    sell: Counter = Counter()
    buy: Counter = Counter()
    phase_h: Counter = Counter()
    phase_p: Counter = Counter()
    last_shed = 0.0
    last_day = 0
    for entry in (sink or []):
        step, obs, act = int(entry[0]), entry[1], entry[2]
        if not isinstance(obs, dict):
            continue
        day = step // DAY
        shed = ((obs.get("private") or {}) if isinstance(obs.get("private"),
                dict) else {}).get("shed") or {}
        tot = 0.0
        for v in (shed or {}).values():
            try:
                tot += float(v)
            except (TypeError, ValueError):
                continue
        if day not in day_first_shed:
            day_first_shed[day] = tot
        last_shed, last_day = tot, max(last_day, day)
        if not isinstance(act, dict):
            continue
        for cmd in (act.get("market") or []):
            if isinstance(cmd, (list, tuple)) and len(cmd) >= 3:
                try:
                    q = float(cmd[2])
                except (TypeError, ValueError):
                    continue
                if str(cmd[0]) == "SELL":
                    sell[day] += q
                elif str(cmd[0]) == "BUY_PRODUCT":
                    buy[day] += q
        ops = []
        fu = act.get("farmer")
        if isinstance(fu, list) and fu:
            ops.append(fu)
        for h in (act.get("hands") or []):
            if isinstance(h, list) and h:
                ops.append(h)
        for op in ops:
            if op[0] == "HARVEST":
                phase_h[step % 4] += 1
            elif op[0] == "PLANT":
                phase_p[step % 4] += 1
    daily = []
    for d in range(N_DAYS):
        start = day_first_shed.get(d)
        end = day_first_shed.get(d + 1)
        if end is None and d == last_day:
            end = last_shed
        if start is None or end is None:
            daily.append(None)
            continue
        daily.append(round(end - start + sell[d] - buy[d], 2))
    season = round(sum(x for x in daily if x is not None), 1)
    tot_h = sum(phase_h.values()) or 1
    return {"daily_sellable": daily, "season_sellable": season,
            "sell_req_season": round(sum(sell.values()), 1),
            "buy_req_season": round(sum(buy.values()), 1),
            "harvest_phase4": {str(k): v for k, v in sorted(phase_h.items())},
            "harvest_phase4_share": {str(k): round(v / tot_h, 4)
                                     for k, v in sorted(phase_h.items())},
            "plant_phase4": {str(k): v for k, v in sorted(phase_p.items())}}


def clean_reads(sink):
    """终局钱 farms[obs.player].money 干净口径（交叉核对用）。"""
    last_obs = None
    for entry in (sink or []):
        if isinstance(entry[1], dict):
            last_obs = entry[1]
    if not isinstance(last_obs, dict):
        return {"terminal_money": UNKNOWN}
    try:
        player = int(last_obs.get("player", 0))
    except Exception:
        player = 0
    farms = last_obs.get("farms")
    tm = UNKNOWN
    if isinstance(farms, list) and player < len(farms) \
            and isinstance(farms[player], dict):
        try:
            tm = round(float(farms[player].get("money", 0.0)), 2)
        except (TypeError, ValueError):
            pass
    return {"terminal_money": tm}


# ------------------------------------------------------------ 局跑口 --
def _run_chunk(payload):
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
               "opponent": spec.get("opponent"), "stratum": spec.get("stratum"),
               "banks": rr.get("banks"), "error": rr.get("error"),
               "margin": None, "reads": {}, "rhythm": None}
        if isinstance(sinks, dict) and "build_error" in sinks:
            row["error"] = sinks["build_error"]
            sinks = None
        if row["banks"] is not None and row["error"] is None:
            banks = row["banks"]
            row["margin"] = float(banks[row["seat"]]) - float(
                banks[1 - row["seat"]])
            if isinstance(sinks, dict):
                sink = sinks.get(row["seat"])
                if sink is not None:
                    row["reads"] = clean_reads(sink)
                    row["rhythm"] = rhythm_reads(sink)
        out.append(row)
    return {"rows": out, "engine": res.get("engine"),
            "fallback_reason": res.get("fallback_reason")}


def _play_batch(specs, cfg):
    """并行跑口（fork Pool；自 _run_chunk，保留 reads/rhythm 轨迹读数）。"""
    specs = list(specs)
    workers = int((cfg or {}).get("workers", WORKERS))
    n_chunks = max(1, min(workers * 2, max(1, len(specs))))
    chunks = [specs[i::n_chunks] for i in range(n_chunks)]
    chunks = [c for c in chunks if c]
    tasks = [{"specs": c, "cfg": dict(cfg or {})} for c in chunks]
    if workers <= 1 or len(tasks) <= 1:
        results = [_run_chunk(t) for t in tasks]
    else:
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(processes=min(workers, len(tasks))) as pool:
            results = pool.map(_run_chunk, tasks)
    rows: List[Dict[str, Any]] = []
    for part in results:
        rows.extend(part["rows"])
    return rows


def _play(units, arm, cand_path, cfg):
    from orderbook_r40 import ab_r41 as ab  # noqa: WPS433
    specs = ab._specs_for(units, arm, cand_path, True)
    for sp, u in zip(specs, units):
        sp["stratum"] = u.get("stratum")
    return _play_batch(specs, cfg)


# ------------------------------------------------------------ 聚合 --
def pair_stats(ctl: Dict, var: Dict, kept_units: List[Dict]) -> Dict:
    """配对聚合：W-L-T（Δ 口径）/Δ/翻负数/净翻胜。"""
    agg = {"n": 0, "w": 0, "l": 0, "t": 0, "delta_sum": 0.0,
           "win_control": 0, "win_variant": 0, "flips_pos": 0, "flips_neg": 0,
           "loss_recovery": 0, "loss_recovery_n": 0, "rows_lite": []}
    for u in kept_units:
        key = (u["seed"], u["seat"])
        rc, rvv = ctl.get(key), var.get(key)
        if not rc or not rvv or rc.get("margin") is None \
                or rvv.get("margin") is None:
            continue
        mc, mv = float(rc["margin"]), float(rvv["margin"])
        d = mv - mc
        agg["n"] += 1
        agg["delta_sum"] += d
        agg["w" if d > 0 else "l" if d < 0 else "t"] += 1
        wc, wv = 1 if mc > 0 else 0, 1 if mv > 0 else 0
        agg["win_control"] += wc
        agg["win_variant"] += wv
        if wv and not wc:
            agg["flips_pos"] += 1
        if wc and not wv:
            agg["flips_neg"] += 1
        if u["stratum"] == "loss_replay":
            agg["loss_recovery_n"] += 1
            if d > 0:
                agg["loss_recovery"] += 1
        agg["rows_lite"].append(
            {"seed": u["seed"], "seat": u["seat"], "stratum": u["stratum"],
             "opponent": u.get("opponent"), "margin_control": round(mc, 1),
             "margin_variant": round(mv, 1), "delta": round(d, 1)})
    n = max(1, agg["n"])
    out = {"n": agg["n"], "W": agg["w"], "L": agg["l"], "T": agg["t"],
           "mean_delta": round(agg["delta_sum"] / n, 2),
           "win_control": agg["win_control"], "win_variant": agg["win_variant"],
           "flips_pos": agg["flips_pos"], "flips_neg": agg["flips_neg"],
           "net_flip_wins": agg["win_variant"] - agg["win_control"],
           "loss_recovery": "%d/%d 败局 Δ>0" % (agg["loss_recovery"],
                                                agg["loss_recovery_n"]),
           "control_win_guard_ok": agg["flips_neg"] == 0,
           "rows_lite": agg["rows_lite"]}
    out["positive_arm"] = bool(out["net_flip_wins"] > 0
                               and out["control_win_guard_ok"])
    return out


def rhythm_agg(rows: List[Dict]) -> Dict:
    """逐日可售产出量均值 + 相位直方汇总。"""
    dsum = [0.0] * N_DAYS
    dn = [0] * N_DAYS
    season, n = 0.0, 0
    ph: Counter = Counter()
    for r in rows:
        rr = r.get("rhythm") or {}
        for d, v in enumerate(rr.get("daily_sellable") or []):
            if is_num(v):
                dsum[d] += float(v)
                dn[d] += 1
        if is_num(rr.get("season_sellable")):
            season += float(rr["season_sellable"])
            n += 1
        for k, v in (rr.get("harvest_phase4") or {}).items():
            ph[str(k)] += int(v)
    tot = sum(ph.values()) or 1
    return {"n_games": n,
            "daily_sellable_mean": [round(dsum[d] / dn[d], 1) if dn[d] else
                                    UNKNOWN for d in range(N_DAYS)],
            "season_sellable_mean": round(season / n, 1) if n else UNKNOWN,
            "harvest_phase4": dict(sorted(ph.items())),
            "harvest_phase4_share": {k: round(v / tot, 4)
                                     for k, v in sorted(ph.items())}}


def main():
    os.chdir(KSIM_DIR)
    from orderbook_r40 import judge_r23 as j23  # noqa: WPS433
    from orderbook_r40 import sim_bridge as sb  # noqa: WPS433
    t0 = time.perf_counter()

    main_text = rv.H1_MAIN.read_text(encoding="utf-8")
    pkg_base = rv.rs._decode_routes(main_text)
    opp_paths = [str(KSIM_DIR / rel) for rel in j23.DEFAULT_OPPONENTS]
    units = []
    for j, seed in enumerate(FOLDS):
        opp = opp_paths[j % len(opp_paths)]
        stratum = ("loss_replay" if seed in set(LOSS_FOLDS) else
                   "neutral_672000_i73")
        for seat in (0, 1):
            units.append({"seed": int(seed), "seat": seat, "opp_path": opp,
                          "opponent": Path(opp).parent.name, "stratum": stratum})

    EV.update({
        "version": RECORD_VERSION,
        "experiment": ("产线相位变体 vs H1 配对因果 A/B：检验分析38 诊断④"
                       "（残差在生产节奏）——PLANT 全流 ±1/±2 拍 + HARVEST "
                       "日内 %4 相位 ±1 拍；判决先行·不发射不提交"),
        "source": {
            "commands": ["python3 orderbook_rhythm_lab/judge_rhythm.py"],
            "base_main": str(rv.H1_MAIN),
            "base_sha256": hashlib.sha256(
                main_text.encode("utf-8")).hexdigest(),
            "corpus": {"loss_folds": LOSS_FOLDS,
                       "neutral_folds": NEUTRAL_FOLDS,
                       "neutral_spec": "672000+i*73（新中性块 n=6）",
                       "folds_per_variant": 12,
                       "strata": "26 败局回放（canonical 前 6 fold）+ 新中性块"
                                 " 672000+i*73（i=0..5）；双席 fold n=12/变体"},
            "opponents": opp_paths, "workers": WORKERS,
            "caliber": ("margin=终局 banks[our]−banks[opp]；终局钱 "
                        "farms[obs.player].money 干净口径交叉核对"),
            "criterion": "净翻胜>0 的变体为正臂；胜局对照不翻负（flips_neg==0）",
        },
        "variants": {}, "pairs": {}, "rhythm_stats": {},
        "budget": {"cap_局次": BUDGET_CAP_GAMES, "auth_局次": 0,
                   "judgment_局次": 0},
    })
    flush_evid()

    # ---- 1) 变体构建 + 量守恒审计 + 孪生三闸先行（违规即弃） ----
    built_all: Dict[str, Any] = {}
    for vid in rv.VARIANTS:
        tv0 = time.perf_counter()
        b = rv.build_variant(vid, pkg_base, main_text)
        aud = rv.audit_variant(b, pkg_base)
        table_rids = sorted(set(r["route"] for r in b["table"]),
                            key=lambda k: int(k))
        by_events = Counter(r["route"] for r in b["table"]
                            if r.get("status") == "moved")
        twin_rids = [r for r, _ in by_events.most_common(3)] or table_rids[:3]
        twin = rv.twin_check(b, pkg_base, twin_rids) if twin_rids else {
            "verdict": "NO_OP", "checks": []}
        kept = bool(twin.get("verdict") == "PASS"
                    and aud.get("conservation_ok") and b["stats"]["moved"] > 0)
        p = rv.BUILD_DIR / ("variant_%s_main.py" % vid)
        p.write_text(b["main_text"], encoding="utf-8")
        EV["variants"][vid] = {
            "spec": b["spec"], "phase_shift": {
                "kind": b["spec"]["kind"], "delta_step": b["spec"]["delta"],
                "delta_phase4": b["spec"]["delta"] % 4,
                "same_day": b["spec"]["same_day"]},
            "stats": b["stats"], "conservation": {
                "ok": aud["conservation_ok"], "note": aud["conservation_note"],
                "n_table_rows": aud["n_table_rows"]},
            "twin": {"verdict": twin.get("verdict"),
                     "twin_rids": twin_rids,
                     "n_checks": len(twin.get("checks") or []),
                     "n_violation": sum(1 for c in (twin.get("checks") or [])
                                        if not c.get("ok"))},
            "main_path": str(p), "kept": kept,
            "elapsed_s": round(time.perf_counter() - tv0, 2)}
        built_all[vid] = b
        if not kept:
            ANOMALIES.append("%s 弃（twin=%s cons=%s moved=%d）" % (
                vid, twin.get("verdict"), aud.get("conservation_ok"),
                b["stats"]["moved"]))
        print("variant", vid, "twin", twin.get("verdict"), "kept", kept,
              "moved", b["stats"]["moved"], "clamped", b["stats"]["clamped"],
              flush=True)
        flush_evid()

    kept = [vid for vid in rv.VARIANTS if EV["variants"][vid]["kept"]]
    if not kept:
        EV["verdict"] = {"criterion": EV["source"]["criterion"],
                         "positive_variants": [],
                         "verdict": "节奏维关闭（相位变体全被孪生三闸判弃/无正臂）"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        print("ABORT: 无 feasibility 通过变体", flush=True)
        return EV

    # ---- 2) sim_bridge 对照认证 30/30（不过即停） ----
    auth = sb.sim_bridge(
        {"n_games": 30, "min_checked": 30,
         "record_path": str(MODULE_DIR / "evidence" / "sim_auth_record.json")},
        list(REPLAY_26[:26]) + [2026092901, 2026092902, 2026092903,
                                2026092904][:4])
    auth_lite = {k: auth.get(k) for k in
                 ("loaded", "consistency", "wall_speedup", "consistency_ok",
                  "degraded", "degraded_reason", "engine", "timing", "version")}
    (MODULE_DIR / "evidence" / "sim_auth.json").write_text(
        json.dumps(auth_lite, ensure_ascii=False, indent=1, default=str)
        + "\n", encoding="utf-8")
    EV["source"]["sim_auth"] = auth_lite
    EV["budget"]["auth_局次"] = 30
    print("sim auth:", auth_lite.get("consistency_ok"),
          auth_lite.get("consistency"), flush=True)
    if not auth_lite.get("consistency_ok"):
        EV["verdict"] = {"verdict": "ABORT：sim_bridge 对照认证未过 30/30"}
        EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
        flush_evid()
        return EV
    flush_evid()
    run_cfg = {"engine": "auto", "bridge": auth, "workers": WORKERS}

    # ---- 3) control 共享（trace） ----
    rows_ctl = _play(units, "control", str(rv.H1_MAIN), run_cfg)
    EV["budget"]["judgment_局次"] += len(rows_ctl)
    ctl = {(int(r["seed"]), int(r["seat"])): r for r in rows_ctl}
    for r in rows_ctl:
        if r.get("error"):
            ANOMALIES.append("control 红局 %s s%d: %s" % (
                r["seed"], r["seat"], r["error"]))
            continue
        tm = (r.get("reads") or {}).get("terminal_money")
        if is_num(tm) and isinstance(r.get("banks"), list):
            banks0 = float(r["banks"][int(r["seat"])])
            if abs(float(tm) - banks0) > 0.5:
                ANOMALIES.append("终局钱口径交叉核对不一致 %s s%d: tm=%s "
                                 "banks=%s" % (r["seed"], r["seat"], tm,
                                               banks0))
    ctl_rhythm = rhythm_agg(rows_ctl)
    EV["rhythm_stats"]["control"] = ctl_rhythm
    print("control played", len(rows_ctl), "games", flush=True)
    flush_evid()

    # ---- 4) 各变体配对（逐变体边跑边写） ----
    ledger = {"version": RECORD_VERSION,
              "written_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              "units": [], "variant_stats": {}}
    for vid in kept:
        tv1 = time.perf_counter()
        rows_var = _play(units, vid, EV["variants"][vid]["main_path"], run_cfg)
        EV["budget"]["judgment_局次"] += len(rows_var)
        var = {(int(r["seed"]), int(r["seat"])): r for r in rows_var}
        for r in rows_var:
            if r.get("error"):
                ANOMALIES.append("%s 红局 %s s%d: %s" % (
                    vid, r["seed"], r["seat"], r["error"]))
        stats = pair_stats(ctl, var, units)
        stats["elapsed_s"] = round(time.perf_counter() - tv1, 2)
        EV["pairs"][vid] = {k: v for k, v in stats.items()}
        EV["rhythm_stats"][vid] = rhythm_agg(rows_var)
        EV["rhythm_stats"][vid]["control_season"] = \
            ctl_rhythm.get("season_sellable")
        ledger["variant_stats"][vid] = {k: v for k, v in stats.items()
                                        if k != "rows_lite"}
        for row in stats["rows_lite"]:
            ledger["units"].append(dict(row, variant=vid))
        print("pair", vid, "W-L-T", stats["W"], stats["L"], stats["T"],
              "d", stats["mean_delta"], "netflip", stats["net_flip_wins"],
              "flips_neg", stats["flips_neg"], "pos", stats["positive_arm"],
              flush=True)
        flush_evid()

    positive = [vid for vid in kept if EV["pairs"][vid]["positive_arm"]]
    EV["verdict"] = {
        "criterion": EV["source"]["criterion"],
        "positive_variants": positive,
        "verdict": ("PROD_ARM_CANDIDATE: %s" % positive) if positive
        else "节奏维关闭（无净翻胜>0 且不翻负的相位变体）",
        "per_variant": {vid: {"net_flip_wins": EV["pairs"][vid]["net_flip_wins"],
                              "flips_neg": EV["pairs"][vid]["flips_neg"],
                              "mean_delta": EV["pairs"][vid]["mean_delta"]}
                        for vid in kept},
    }
    EV["budget"]["total_局次"] = (EV["budget"]["auth_局次"]
                                 + EV["budget"]["judgment_局次"])
    EV["budget"]["within_cap"] = bool(
        EV["budget"]["judgment_局次"] <= BUDGET_CAP_GAMES)
    EV["elapsed_s"] = round(time.perf_counter() - t0, 1)
    ledger["verdict"] = EV["verdict"]
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    LEDGER_PATH.write_text(json.dumps(ledger, ensure_ascii=False, indent=1,
                                      default=str) + "\n", encoding="utf-8")
    flush_evid()
    print("DONE", EV["elapsed_s"], "s budget", EV["budget"], flush=True)
    return EV


if __name__ == "__main__":
    main()
