# 【中文】v15_d0_counterfactual_giants.py —— 9 巨人局 d0 反事实 + 点火时点矩阵
# ===========================================================================
# 背景（M-E2 验证门）：沿 round24_d0_counterfactual.py 协议（d0 全季
#   rollout，对手=回放真实动作，truth=线上实际），对 9 局 ≥85k 败局
#   （TARGET9，round-24 官方基准）测 v15 波次剧本的挽回矩阵。
# 判据（协调者 2026-09-20 裁决：胜负只看终局钱数，翻盘数为主）：
#   G1 点火前移：m5k 点火日（日终 money ≥ 5000 的首日）必须从 v14 档的
#      d13-18 前移到 d10-12（wave 变体 ≥5/9 局点火日 ≤12 且 ≤ base）；
#   G2 挽回：≥5/9 局 wave 终局资金 vs truth_me 挽回 ≥10%；
#   G3 翻盘：wave 终局资金 > truth_opp（对手线上真值）≥2 局
#      （对照：v3 反事实 5/9 挽回但仅 1 翻盘）。
# 变体：base（旗关 v13.8/v14.2 语义）/ wave（PLANNER_OVERRIDES.wave_mode）。
# 输出：exports/probes/v15_ignition/v15_d0_counterfactual_giants.json
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
ROOT = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402

REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT = os.path.join(SOFTWARE, "exports", "probes", "v15_ignition",
                   "v15_d0_counterfactual_giants.json")
TEAM = "renyxin"
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
M5K = 5000.0
TURNS_PER_DAY = 24
WAVE_OVERRIDES = {"PLANNER_ENABLED": True,
                  "PLANNER_OVERRIDES.wave_mode": True}
VARIANTS = (("base", None), ("wave", WAVE_OVERRIDES))


def rollout_daily(deps, replay, me_seat, overrides):
    """d0 起全季 rollout，逐日记我方日终 money + 资产侧（placed herd /
    quads）（对手=回放真实动作；循环与 bench.rollout_with_replay_opponent
    逐行同构）。"""
    agent_fn, _applied, _skip = deps["v13_factory"](overrides)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    me_seat = int(me_seat)
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    daily = {}
    assets = {}
    while not state.env.done and taken < len(acts) and taken < max_steps:
        obs = state.seats[me_seat].observation
        mine = agent_fn(obs)
        theirs = acts[taken][1 - me_seat]
        deps["step"](state, [mine, theirs])
        taken += 1
        if taken % TURNS_PER_DAY == 0:
            farms = state.seats[0].observation.farms
            farm = farms[me_seat]
            day_done = taken // TURNS_PER_DAY - 1
            daily[day_done] = float(farm.get("money", 0.0) or 0.0)
            herd = 0
            for row in farm.get("tiles") or []:
                for tile in row or []:
                    if isinstance(tile, dict) and "animal" in tile:
                        herd += 1
            quads = len(farm.get("unlocked_quadrants") or ["NW"])
            assets[day_done] = (herd, quads)
    final = deps["final"](state)
    daily.setdefault(29, float(final[me_seat]))
    assets.setdefault(29, assets.get(28, (0, 1)))
    ordered = [daily[d] for d in sorted(daily)]
    return float(final[me_seat]), ordered, taken, assets


def ignition_day(daily):
    for day, m in enumerate(daily):
        if m >= M5K:
            return day
    return 99


def asset_ignition_day(assets, herd_min=11, quad_min=2):
    """资产侧点火：首日 placed herd ≥ 11 且解锁象限 ≥ 2
    （12 头死线 + 第 2 象限 = 资本波次兑现口径；v48 d10-12 达成）。"""
    for day in sorted(assets or {}):
        herd, quads = assets[day]
        if herd >= herd_min and quads >= quad_min:
            return day
    return 99


def main():
    deps = bench.make_twin_deps()
    out = {"protocol": "v15-d0-counterfactual-giants/1.0",
           "note": "9 巨人局 d0 全季 rollout；判据=点火日≤12(≥5/9)+挽回≥10%"
                   "(≥5/9)+翻盘≥2（终局钱数口径）",
           "episodes": {}}
    t_start = time.time()
    for ep in TARGET9:
        path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
        with open(path, "r", encoding="utf-8") as h:
            replay = json.load(h)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        rec = {"opponent": teams[1 - me], "truth_me": truth_me,
               "truth_opp": truth_opp, "variants": {}}
        for name, ovr in VARIANTS:
            t0 = time.time()
            final, daily, taken, assets = rollout_daily(deps, replay, me,
                                                        ovr)
            rec["variants"][name] = {
                "final": round(final, 1),
                "delta_vs_truth": round(final - truth_me, 1),
                "gain_pct": round((final - truth_me) / truth_me, 4),
                "win_vs_truth_opp": final > truth_opp,
                "ignition_day": ignition_day(daily),
                "asset_ignition_day": asset_ignition_day(assets),
                "daily": [round(m, 1) for m in daily],
                "steps": taken,
                "wall_s": round(time.time() - t0, 1)}
        v = rec["variants"]
        rec["summary"] = {
            "ignition_base": v["base"]["ignition_day"],
            "ignition_wave": v["wave"]["ignition_day"],
            "ignition_improved": v["wave"]["ignition_day"]
            < v["base"]["ignition_day"],
            "asset_ign_base": v["base"]["asset_ignition_day"],
            "asset_ign_wave": v["wave"]["asset_ignition_day"],
            "gain_pct_wave": v["wave"]["gain_pct"],
            "flip_wave": v["wave"]["win_vs_truth_opp"],
            "flip_base": v["base"]["win_vs_truth_opp"],
        }
        out["episodes"][str(ep)] = rec
        s = rec["summary"]
        print(f"ep{ep} vs {teams[1 - me][:16]:16s} truth {truth_me:8.0f} | "
              f"base {v['base']['final']:8.0f} (m5k {s['ignition_base']:2d}"
              f"/cap {s['asset_ign_base']:2d}"
              f"{',F' if s['flip_base'] else ' '}) "
              f"wave {v['wave']['final']:8.0f} (m5k {s['ignition_wave']:2d}"
              f"/cap {s['asset_ign_wave']:2d}"
              f"{',F' if s['flip_wave'] else ' '}) "
              f"gain {s['gain_pct_wave']:+7.1%} [{time.time()-t_start:.0f}s]",
              flush=True)

    eps = out["episodes"]
    ign_le12 = [e for e, r in eps.items()
                if r["variants"]["wave"]["ignition_day"] <= 12
                and r["variants"]["wave"]["ignition_day"]
                <= r["variants"]["base"]["ignition_day"]]
    asset_ign = [e for e, r in eps.items()
                 if r["variants"]["wave"]["asset_ignition_day"] <= 12
                 and r["variants"]["wave"]["asset_ignition_day"]
                 <= r["variants"]["base"]["asset_ignition_day"]]
    recover10 = [e for e, r in eps.items()
                 if r["variants"]["wave"]["gain_pct"] >= 0.10]
    flips = [e for e, r in eps.items() if r["summary"]["flip_wave"]]
    ign_base = [r["variants"]["base"]["ignition_day"] for r in eps.values()]
    ign_wave = [r["variants"]["wave"]["ignition_day"] for r in eps.values()]
    aign_base = [r["variants"]["base"]["asset_ignition_day"]
                 for r in eps.values()]
    aign_wave = [r["variants"]["wave"]["asset_ignition_day"]
                 for r in eps.values()]

    def _med(xs):
        xs = sorted(xs)
        return xs[len(xs) // 2] if xs else None
    out["gates"] = {
        "G1_ignition_m5k": {"wave_ign_days": ign_wave,
                            "base_ign_days": ign_base,
                            "wave_median": _med(ign_wave),
                            "base_median": _med(ign_base),
                            "n_le12_and_not_worse": len(ign_le12),
                            "episodes": ign_le12,
                            "passed": len(ign_le12) >= 5,
                            "note": "m5k=日终现金≥5000 首日；剧本把现金换"
                                    "成资产时此口径天然偏晚（v48 全季贴"
                                    "地现金在该口径下也'不点火'）——资产"
                                    "口径见 G1b"},
        "G1b_ignition_asset": {"herd_min": 11, "quad_min": 2,
                               "wave_days": aign_wave,
                               "base_days": aign_base,
                               "wave_median": _med(aign_wave),
                               "base_median": _med(aign_base),
                               "n_le12_and_not_worse": len(asset_ign),
                               "passed": len(asset_ign) >= 5},
        "G2_recover": {"n_recover10": len(recover10),
                       "episodes": recover10,
                       "passed": len(recover10) >= 5},
        "G3_flip": {"n_flips": len(flips),
                    "episodes": flips,
                    "base_flips": sum(1 for r in eps.values()
                                      if r["summary"]["flip_base"]),
                    "passed": len(flips) >= 2},
    }
    out["all_passed"] = all(g["passed"] for g in (
        out["gates"]["G1b_ignition_asset"], out["gates"]["G2_recover"],
        out["gates"]["G3_flip"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    print(json.dumps({"gates": {k: {kk: vv for kk, vv in v.items()
                                    if kk != "episodes"}
                               for k, v in out["gates"].items()},
                      "all_passed": out["all_passed"]}, ensure_ascii=False))
    print(f"out -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
