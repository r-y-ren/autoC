# -*- coding: utf-8 -*-
"""openloop —— R15 开环重演主判据（重演执行复用 R14 实验室，只调用不重写）。

口径：
  - 语料：26 败局 × 双席位 + 10 胜局 × 原席位（无害臂）；
  - 对照臂：原版 L3 在飞件（官方 last-callable 全新装载，R14 同款）；
    与 R14 语料重合局的对照数据复用（evidence/judgment.json phase_b
    control margin）并抽验（spot-check 2 局重跑，漂移 >1 即弃用复用全量
    落回实测）；
  - 变体臂：变体 main 装载同款；对手席=录像开环重放（R8 先例口径，
    对手不反应——闭环副证补该面）；
  - Δ = 同局同席 margin(变体) − margin(对照)；
  - 红=fail-closed：装载/重演异常重跑一次仍败、或 status != DONE。
  - 预算 ≤1100 局次（_base.MAX_REPLAYS）：超预算截尾（预算面注记）。
"""
from __future__ import annotations

import json
import os
import random
import time

from . import _base as B
from orderbook_surge_lab import corpus as _surge_corpus
from orderbook_surge_lab import phase_b as _surge_b

SPOT_CHECK_N = 2
SPOT_DRIFT_MAX = 1.0


def load_r14_control(r14_evidence_path=B.R14_EVIDENCE):
    """R14 evidence → {(episode, seat): control_margin}（重合局对照复用面）。"""
    if not os.path.isfile(r14_evidence_path):
        return {}, None
    try:
        with open(r14_evidence_path, "r", encoding="utf-8") as fh:
            ev = json.load(fh)
    except (OSError, ValueError):
        return {}, None
    table = {}
    for g in (ev.get("phase_b") or {}).get("per_game", []):
        for seat_key, seat in (("seat0", 0), ("seat1", 1)):
            rec = ((g.get("arms") or {}).get(seat_key) or {}).get(
                _surge_b.CONTROL) or {}
            if rec.get("margin") is not None:
                table[(g.get("episode"), seat)] = float(rec["margin"])
    return table, ev.get("generated_at")


def _run_once(replay, main_path, seat):
    """单局单席重演（异常→全新装载重跑一次；仍败上抛）。"""
    last_exc = None
    for _attempt in range(2):
        try:
            callable_fn = _surge_b.load_l3_callable(main_path)
            res = _surge_b.replay_dual_seat(replay, callable_fn, seat)
            return res
        except Exception as exc:
            last_exc = exc
    raise last_exc


def openloop_replay_variants(variants, corpus, l3_main_path,
                             reuse_r14_control=True, budget=B.MAX_REPLAYS,
                             log=None):
    """逐变体开环重演编排。

    输入：variants=[{id, main_path,...}]、corpus={losses26, wins10}、
    l3_main_path（对照在飞件）。输出：
      {control, control_reuse, per_variant, summary}——
    control = {(episode, seat): {margin, source}}；
    per_variant = {vid: {games: {episode: {seats: {...}, game_delta}}}}；
    败局局级 Δ=双席位 min（保守主口径，R14 先例），胜局 Δ=原席位。
    """
    log = log or (lambda msg: None)
    t0 = time.perf_counter()
    losses = list(corpus.get("losses26") or [])
    wins = list(corpus.get("wins10") or [])
    games = [(g, (0, 1), "L") for g in losses] + \
            [(g, (g.get("seat"),), "W") for g in wins]

    # ---- 对照臂（复用 + 抽验） ---------------------------------------------
    r14_table, r14_ts = (load_r14_control() if reuse_r14_control else ({}, None))
    control, n_fresh, n_reused = {}, 0, 0
    spot_pool = []
    for g, seats, _kind in games:
        ep = g["episode"]
        for seat in seats:
            hit = r14_table.get((ep, seat)) if reuse_r14_control else None
            if hit is not None:
                control[(ep, seat)] = {"margin": hit, "source": "r14_reuse"}
                n_reused += 1
                spot_pool.append((g, seat))
            else:
                control[(ep, seat)] = None   # 待实测
    spot_pool.sort(key=lambda x: (x[0]["episode"], x[1]))
    spot = spot_pool[:SPOT_CHECK_N]
    spot_drift = []
    for g, seat in spot:
        ep = g["episode"]
        replay = _surge_corpus.load_replay(g["path"])
        res = _run_once(replay, l3_main_path, seat)
        drift = abs(res["margin"] - control[(ep, seat)]["margin"])
        spot_drift.append({"episode": ep, "seat": seat,
                           "reused": control[(ep, seat)]["margin"],
                           "remeasured": round(res["margin"], 1),
                           "drift": round(drift, 2)})
    reuse_ok = all(d["drift"] <= SPOT_DRIFT_MAX for d in spot_drift)
    if not reuse_ok:
        log("[openloop] 对照复用抽验漂移超阈 → 弃用复用，全量实测")
        control = {k: None for k in control}
        n_reused = 0
    for g, seats, _kind in games:
        ep = g["episode"]
        for seat in seats:
            if control[(ep, seat)] is None:
                replay = _surge_corpus.load_replay(g["path"])
                res = _run_once(replay, l3_main_path, seat)
                control[(ep, seat)] = {"margin": round(res["margin"], 1),
                                       "source": "fresh"}
                n_fresh += 1
    n_replays = n_fresh + len(spot)

    # ---- 变体臂 -------------------------------------------------------------
    per_variant = {}
    budget_left = budget - n_replays
    stopped = False
    for v in variants:
        vid, vmain = v["id"], v["main_path"]
        vg = {}
        for g, seats, kind in games:
            ep = g["episode"]
            if budget_left <= 0:
                stopped = True
                break
            rec = {"res": kind, "seat_recorded": g.get("seat"),
                   "seats": {}}
            red = False
            try:
                replay = _surge_corpus.load_replay(g["path"])
            except Exception as exc:
                rec["seats"]["load"] = {"error": repr(exc), "red": True}
                red = True
            if not red:
                for seat in seats:
                    if budget_left <= 0:
                        stopped = True
                        break
                    ctrl = control[(ep, seat)]
                    try:
                        res = _run_once(replay, vmain, seat)
                        budget_left -= 1
                        n_replays += 1
                        ok = res["status"] == "DONE" and ctrl is not None
                        rec["seats"][f"seat{seat}"] = {
                            "margin": round(res["margin"], 1),
                            "control": ctrl["margin"] if ctrl else None,
                            "delta": (round(res["margin"] - ctrl["margin"], 1)
                                      if ctrl is not None and ok else None),
                            "status": res["status"],
                            "red": not ok,
                        }
                        if not ok:
                            red = True
                    except Exception as exc:
                        budget_left -= 1
                        n_replays += 1
                        rec["seats"][f"seat{seat}"] = {
                            "error": f"{type(exc).__name__}: {exc}",
                            "red": True}
                        red = True
            # 局级 Δ：败局=双席位 min（保守），胜局=原席位
            deltas = [s.get("delta") for s in rec["seats"].values()
                      if isinstance(s, dict) and s.get("delta") is not None]
            rec["game_delta"] = min(deltas) if deltas else None
            rec["red"] = red
            vg[str(ep)] = rec
        per_variant[vid] = {
            "id": vid, "pair": v.get("pair"), "scale": v.get("scale"),
            "games": vg,
        }
        if stopped:
            log(f"[openloop] 预算截断 @variant={vid}")
            break
    summary = {
        "n_variants": len(variants), "n_run_variants": len(per_variant),
        "n_games": len(games), "n_replays": n_replays,
        "control_fresh": n_fresh, "control_reused": n_reused,
        "reuse_ok": reuse_ok, "spot_drift": spot_drift,
        "budget": budget, "budget_stopped": stopped,
        "wall_s": round(time.perf_counter() - t0, 1),
        "r14_evidence_ts": r14_ts,
    }
    return {"control": {f"{k[0]}/{k[1]}": v for k, v in control.items()},
            "control_reuse": {"reused": n_reused, "fresh": n_fresh,
                              "spot_drift": spot_drift, "ok": reuse_ok},
            "per_variant": per_variant, "summary": summary}
