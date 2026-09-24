# -*- coding: utf-8 -*-
"""closedloop —— R15 闭环副证（R9 市场耦合补丁口径：对手可反应）。

方法：twin 引擎（kaggle_simulations.agent.planner.twin）自回放头建初态，
双席皆活体 callable（变体 vs 原版 L3），逐转移 twin.step 推进至终局——
对手席可对市场态（含我方变体抛压）反应，补开环"录像重放不反应"面。

口径：每镜像局双定向（变体@seat0 / 变体@seat1）→ 互胜率 = 变体胜局数 /
(局数×2)；margin = 变体席资金 − L3 席资金（定向内视角）。引擎/装载异常
→ 全新装载重跑一次（仍败=该定向红，fail-closed 留痕不中断）。
"""
from __future__ import annotations

import time

from . import _base as B
from orderbook_surge_lab import corpus as _surge_corpus
from orderbook_surge_lab import phase_b as _surge_b

_TWIN = None


def _twin():
    global _TWIN
    if _TWIN is None:
        import sys
        if B._SOFTWARE not in sys.path:
            sys.path.insert(0, B._SOFTWARE)
        from kaggle_simulations.agent.planner import twin
        _TWIN = twin
    return _TWIN


def _obs_dict(state, seat):
    """twin 席位观测 → callable 可读纯 dict（R14 phase_b._obs_dict 同款）。"""
    obs0 = state.seats[0].observation
    mine = state.seats[seat].observation
    return {
        "farms": obs0.farms, "market": obs0.market, "town": obs0.town,
        "day": mine.day, "hour": mine.hour, "step": obs0.step,
        "player": seat, "private": mine.private,
        "remainingOverageTime": 60.0,
    }


def duel(replay, variant_main, l3_main, variant_seat, wall_timeout=900.0):
    """单局单定向直接对打：变体@variant_seat vs 原版 L3@对席，活体双驱。

    输出：{margin, finals, status, steps_n, wall_s}——margin=变体席−L3 席；
    异常上抛（编排层重跑一次）。
    """
    twin = _twin()
    bundle = twin.load_engine()
    state = twin.new_state_from_replay_head(replay, bundle)
    callables = {}
    for seat, main in ((variant_seat, variant_main), (1 - variant_seat, l3_main)):
        callables[seat] = _surge_b.load_l3_callable(main)
    taken = 0
    t0 = time.perf_counter()
    while not state.env.done and taken < 720:
        if taken % 120 == 0 and time.perf_counter() - t0 > wall_timeout:
            raise TimeoutError(f"duel 超时 {wall_timeout}s @taken={taken}")
        pair = [None, None]
        for seat in (0, 1):
            pair[seat] = callables[seat](_obs_dict(state, seat))
        twin.step(state, pair)
        taken += 1
    finals = twin.final_money(state)
    return {"margin": finals[variant_seat] - finals[1 - variant_seat],
            "finals": finals,
            "status": "DONE" if state.env.done else "INCOMPLETE",
            "steps_n": taken, "wall_s": round(time.perf_counter() - t0, 2)}


def closedloop_probe(positive_variants, mirror5, l3_main_path,
                     log=None, budget=None):
    """闭环副证编排：逐开环 POSITIVE 变体 × 镜像局 × 双定向。

    输入：positive_variants=[{id, main_path,...}]、mirror5=镜像局条目列表。
    输出：{per_variant: {vid: {games, runs, wins, rate, margins,
    median_margin, red_runs}}, summary}——互胜 ≥0.5 且中位 margin ≥0
    （无系统性负）由 judge 消费；本层只产数据。
    """
    log = log or (lambda msg: None)
    t0 = time.perf_counter()
    per_variant = {}
    n_runs = 0
    for v in positive_variants:
        vid = v["id"]
        runs, wins, margins, red_runs = 0, 0, [], 0
        games_rec = []
        for g in mirror5:
            ep = g.get("episode")
            rec = {"episode": ep, "orientations": {}}
            try:
                replay = _surge_corpus.load_replay(g["path"])
            except Exception as exc:
                rec["orientations"]["load"] = {"error": repr(exc), "red": True}
                red_runs += 2
                games_rec.append(rec)
                continue
            for vseat in (0, 1):
                key = f"variant@seat{vseat}"
                res = None
                last_exc = None
                for _attempt in range(2):        # 异常→全新装载重跑一次
                    try:
                        res = duel(replay, v["main_path"], l3_main_path, vseat)
                        break
                    except Exception as exc:
                        last_exc = exc
                n_runs += 1
                runs += 1
                if res is None:
                    rec["orientations"][key] = {
                        "error": f"{type(last_exc).__name__}: {last_exc}",
                        "red": True}
                    red_runs += 1
                    continue
                rec["orientations"][key] = {
                    "margin": round(res["margin"], 1), "status": res["status"],
                    "steps_n": res["steps_n"], "wall_s": res["wall_s"],
                    "red": res["status"] != "DONE",
                }
                if res["status"] == "DONE":
                    margins.append(round(res["margin"], 1))
                    wins += 1 if res["margin"] > 0 else 0
                else:
                    red_runs += 1
            games_rec.append(rec)
        n_valid = len(margins)
        sorted_m = sorted(margins)
        median = (sorted_m[n_valid // 2] if n_valid % 2
                  else round((sorted_m[n_valid // 2 - 1]
                              + sorted_m[n_valid // 2]) / 2, 1)) if n_valid else None
        per_variant[vid] = {
            "id": vid, "games": games_rec,
            "n_mirror_games": len(mirror5), "runs": runs, "wins": wins,
            "rate": round(wins / runs, 3) if runs else None,
            "margins": margins, "median_margin": median,
            "red_runs": red_runs,
        }
        log(f"[closedloop] {vid}: wins={wins}/{runs} median={median}")
    return {"per_variant": per_variant,
            "summary": {"n_variants": len(positive_variants),
                        "n_runs": n_runs,
                        "wall_s": round(time.perf_counter() - t0, 1)}}
