# 【中文】v143_sellrace_gates.py —— v14.3-sellrace 四道验证门（2026-09-20）
# ===========================================================================
# 任务包门（09-27 冻结前最后一刀）：
#   a) 近失带翻盘门：round-24 近失带 4 局（110741693/-3,124、110689244/
#      -1,031、110678765/-363、110679941/-10,615），d0 口径孪生反事实
#      （对手=回放真实动作、真值=线上实际），v14.3 旋钮变体翻盘
#      （final > 对手线上真值）≥2/4 局。base（旗关）逐局并跑作诚实背景。
#   b) 巨人 9 局挽回矩阵不回退：TARGET9（round-24 九巨人败局）v14.2 运行
#      点（DTSP runtime 黎明钩子 K=6×H=1d 不变）+ sellrace 预置，挽回
#      ≥10% 终局资金 ≥5/9 局（v3 复裁基线 5/9）。
#   c) 胜局回归：WINS13 全量 13 局（≥8 抽样线之上不挑样本）同协议，
#      对真值损伤 >5% 局数 ≤1。
#   d) v48 h2h 8 局 sanity：submission main.py 命名空间 + sellrace 预置
#      vs 解码 v48 真源码，4 种子 × 双席位，均值 margin ≥ -84.7k
#      （v15 E1 基线；此刀对 v48 应无感，只防误伤）。
# 预置语义（与发射态 main.py _SELLRACE_SHIP=True 严格一致）：
#   * 键不在 DTSP governed 全名面内 → 逐黎明 apply_overrides 不触碰预置值；
#   * fail-open restore_pristine 清寄存器=预置死亡（安全回落 v14.2），
#     failopen 计数照实记录；
#   * 不加新轴进计划空间：plans.py 键面零改动。
# CLI：--gates a,b,c,d（默认全跑）| --smoke（a 缩 1 局 ×1 变体 + b/c 缩 1 局
#   + d 缩 1 局，摇通用）；输出 exports/probes/v143_sellrace/gates.json。
# 纪律：stdlib-only、全离线、确定性；逐局结果全量落盘（不挑样本）。
# ===========================================================================

from __future__ import annotations

import argparse
import importlib.util
import json
import os
import sys
import time
from datetime import timezone, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(SCRIPT_DIR)
ROOT = os.path.dirname(SOFTWARE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402
from kgenv.arena import (SUBMISSION_MAIN, run_episode)     # noqa: E402
from kaggle_simulations.agent.planner import runtime as _runtime  # noqa: E402

REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT = os.path.join(SOFTWARE, "exports", "probes", "v143_sellrace",
                   "gates.json")
V48_PATH = os.path.join(ROOT, "references", "data", "intel-notebooks",
                        "v48build", "main.py")
TEAM = "renyxin"

NEAR_MISS = (110741693, 110689244, 110678765, 110679941)
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
WINS13 = (110681129, 110682284, 110683437, 110686759, 110690133,
          110691193, 110692292, 110693383, 110695554, 110696787,
          110697778, 110698875, 110790899)
H2H_SEEDS = (101, 102, 103, 104)
H2H_SEATS = (0, 1)

# v14.3 旋钮变体（任务包第 1/2 项：售卖前移 + day-11 放羊承诺全开；
# CARE 攒量系 v14.2 在役语义零改码——见 market/mission 模块头）。
V143_KNOBS = {"PLANNER_ENABLED": True,
              "PLANNER_OVERRIDES.sellrace_mode": True,
              "PLANNER_OVERRIDES.d11_sheep_commit": 1}
_PRESET = {"sellrace_mode": True, "d11_sheep_commit": 1}

V3_RUNTIME_CONFIG = {
    "enabled": True,
    "seed": 1,
    "budget_cap_s": 0.85,
    "rollout_models": ("pessimistic_fill",),
    "ladder": ((6, 1), (4, 2), (3, 3), (2, 4), (1, 6)),
}
RECOVER_PCT = 0.10
HURT_PCT = -0.05
NEAR_MISS_MIN_FLIPS = 2
GIANTS_MIN_HITS = 5          # v3 复裁基线 5/9，不回退
WIN_HURT_MAX = 1
V48_MARGIN_FLOOR = -84700.0  # v15 E1 wave 口径均值（sanity 下限）


def load_replay(ep):
    path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def rollout_with_replay_opponent_seated(deps, state, me_seat, agent_fn,
                                        opp_actions, start_step,
                                        pre_step=None):
    """席位正确版 rollout（mine→seats[me_seat]、theirs→seats[1-me_seat]）。

    bench.rollout_with_replay_opponent 恒把 mine 放 seat 0——对 me_seat=1
    的局，我方 agent 的动作会落在对手农场（本席由回放 seat-0 动作驱动），
    终局读取 final[me] 实为对手磁带的钱（2026-09-20 v14.3 门禁期发现，
    见 JOURNAL）。本函数按席位放置动作，me_seat=0 时与 bench 逐字节同。
    pre_step(obs, ns, day, hour)：逐回合前置回调（DTSP runtime 黎明钩子
    由 gates b/c 经此注入）。"""
    taken = 0
    max_steps = int(getattr(state.env.configuration, "episodeSteps", 720))
    me = int(me_seat)
    while not state.env.done and start_step + taken < len(opp_actions) \
            and taken < max_steps:
        obs = state.seats[me].observation
        if pre_step is not None:
            pre_step(obs, taken)
        mine = agent_fn(obs) if agent_fn is not None else None
        theirs = opp_actions[start_step + taken][1 - me]
        pair = [theirs, theirs]
        pair[me] = mine
        deps["step"](state, pair)
        taken += 1
    return deps["final"](state), taken


def rollout_knobs(deps, replay, me_seat, overrides):
    """d0 全季 rollout，旋钮变体（无 runtime——bench 单变量口径）。"""
    agent_fn, _applied, skipped = deps["v13_factory"](overrides)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    final, taken = rollout_with_replay_opponent_seated(
        deps, state, me_seat, agent_fn, acts, 0)
    return {"final_me": float(final[me_seat]), "steps": taken,
            "applied": len(_applied or []), "skipped": len(skipped or [])}


def rollout_runtime_preset(deps, replay, me_seat, preset=True):
    """v14.2 运行点（DTSP runtime 黎明钩子）+ sellrace 预置。

    预置在建命名空间时打入一次；engaged 黎明的 apply_overrides 只写
    governed 全名面（不含预置键）→ 预置存活；fail-open restore 清寄存器
    → 预置死亡（与发射态 main.py 语义一致）。"""
    _runtime.reset_state()
    ns, _applied, _skipped = bench.build_v13_namespace(None)
    if preset:
        ns["PLANNER_ENABLED"] = True
        if isinstance(ns.get("PLANNER_OVERRIDES"), dict):
            ns["PLANNER_OVERRIDES"].update(_PRESET)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    me = int(me_seat)

    def _pre_step(obs, taken_idx):
        day = int(getattr(obs, "day", taken_idx // 24))
        hour = int(getattr(obs, "hour", taken_idx % 24))
        _runtime.dawn_hook(obs, ns, V3_RUNTIME_CONFIG, player=me,
                           day=day, hour=hour)

    final, taken = rollout_with_replay_opponent_seated(
        deps, state, me, ns["agent"], acts, 0, pre_step=_pre_step)
    trace = _runtime.trace()
    return {"final_me": float(final[me]), "steps": taken,
            "dawns": len(trace.get("dawns") or []),
            "failopens": len(trace.get("failopens") or []),
            "engaged": bool(trace.get("engaged"))}


def load_v48_agent():
    spec = importlib.util.spec_from_file_location(
        "v143_v48_opponent", os.path.abspath(V48_PATH))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.agent


def load_submission_with_preset():
    """main.py 命名空间 + sellrace 预置（= _SELLRACE_SHIP=True 发射态）。"""
    spec = importlib.util.spec_from_file_location(
        "v143_ship_candidate", os.path.abspath(SUBMISSION_MAIN))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.PLANNER_ENABLED = True
    module.PLANNER_OVERRIDES.update(_PRESET)
    return module.agent


def seat_daily(res, seat):
    daily = res.get("daily_money") or []
    return [entry.get("money", [None, None])[seat] for entry in daily
            if isinstance(entry, dict)]


def gate_a(deps, smoke):
    eps = NEAR_MISS[:1] if smoke else NEAR_MISS
    rows = {}
    flips = 0
    t0 = time.time()
    for ep in eps:
        replay = load_replay(ep)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        rec = {"opponent": teams[1 - me], "truth_me": truth_me,
               "truth_opp": truth_opp, "variants": {}}
        for name, ovr in (("base", None), ("v143", V143_KNOBS)):
            res = rollout_knobs(deps, replay, me, ovr)
            rec["variants"][name] = {
                "final": round(res["final_me"], 1),
                "flip": res["final_me"] > truth_opp,
                "delta_vs_truth": round(res["final_me"] - truth_me, 1),
                "steps": res["steps"]}
        rows[str(ep)] = rec
        flip = rec["variants"]["v143"]["flip"]
        flips += int(flip)
        print(f"[a:near-miss] ep{ep} vs {teams[1-me][:16]:16s} "
              f"truth {truth_me:8.0f}/{truth_opp:8.0f} | "
              f"base {rec['variants']['base']['final']:8.0f} | "
              f"v143 {rec['variants']['v143']['final']:8.0f} "
              f"{'FLIP' if flip else 'lose'}  [{time.time()-t0:.0f}s]")
        del replay
    return {"episodes": rows, "n_flips": flips, "n": len(eps),
            "min_flips": NEAR_MISS_MIN_FLIPS,
            "passed": flips >= NEAR_MISS_MIN_FLIPS and len(eps) == 4}


def gate_bc(deps, which, smoke, arm="v143"):
    eps = (TARGET9 if which == "b" else WINS13)
    eps = eps[:1] if smoke else eps
    rows = {}
    hits = 0
    hurts = 0
    failopens = 0
    t0 = time.time()
    for ep in eps:
        replay = load_replay(ep)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        res = rollout_runtime_preset(deps, replay, me,
                                     preset=(arm == "v143"))
        gain = (res["final_me"] - truth_me) / truth_me if truth_me else 0.0
        hurt = gain < HURT_PCT
        if which == "b":
            hit = res["final_me"] >= truth_me * (1.0 + RECOVER_PCT)
            hits += int(hit)
        else:
            hits += 0
            hurts += int(hurt)
        failopens += int(res["failopens"])
        rows[str(ep)] = {
            "opponent": teams[1 - me], "truth_me": truth_me,
            "truth_opp": truth_opp,
            (arm + "_final"): round(res["final_me"], 1),
            "gain_pct": round(gain, 4),
            "beats_truth_opp": res["final_me"] > truth_opp,
            "recover_hit": (res["final_me"] > truth_me * (1.0 + RECOVER_PCT))
            if which == "b" else None,
            "hurt_over_5pct": hurt,
            "dawns": res["dawns"], "engaged": res["engaged"],
            "failopens": res["failopens"]}
        print(f"[{which}:{arm}] ep{ep} vs {teams[1-me][:16]:16s} truth "
              f"{truth_me:8.0f} {arm} {res['final_me']:8.0f} "
              f"({gain*100:+6.1f}%) failopen={res['failopens']} "
              f"[{time.time()-t0:.0f}s]")
        del replay
    if which == "b":
        passed = hits >= GIANTS_MIN_HITS and len(eps) == 9 and failopens == 0
        return {"arm": arm, "episodes": rows, "n_recover_hits": hits,
                "n": len(eps), "baseline": "v3 复裁 5/9（席位错位通道，须以 base 臂重测归因）",
                "min_hits": GIANTS_MIN_HITS,
                "failopens": failopens, "passed": passed}
    passed = (hurts <= WIN_HURT_MAX and len(eps) == len(WINS13)
              and failopens == 0)
    return {"arm": arm, "episodes": rows, "n_hurt_over_5pct": hurts,
            "n": len(eps), "max_hurt": WIN_HURT_MAX,
            "failopens": failopens, "passed": passed}


def gate_d(smoke):
    seeds = H2H_SEEDS[:1] if smoke else H2H_SEEDS
    seats = H2H_SEATS
    our_fn = load_submission_with_preset()
    v48_fn = load_v48_agent()
    rows = {}
    margins = []
    t0 = time.time()
    for seed in seeds:
        for seat in seats:
            if seat == 0:
                res = run_episode(our_fn, v48_fn, seed, collect_daily=True)
            else:
                res = run_episode(v48_fn, our_fn, seed, collect_daily=True)
            rewards = res["rewards"]
            mine = float(rewards[seat])
            theirs = float(rewards[1 - seat])
            margin = mine - theirs
            margins.append(margin)
            rows[f"seed{seed}_seat{seat}"] = {
                "our_money": mine, "v48_money": theirs,
                "margin": round(margin, 1), "win": mine > theirs,
                "statuses": res.get("statuses")}
            print(f"[d:v48h2h] seed{seed} seat{seat} our {mine:9.0f} "
                  f"v48 {theirs:9.0f} margin {margin:+10.0f} "
                  f"[{time.time()-t0:.0f}s]")
    mean_margin = sum(margins) / len(margins) if margins else 0.0
    return {"games": rows, "mean_margin": round(mean_margin, 1),
            "floor": V48_MARGIN_FLOOR,
            "passed": bool(margins) and mean_margin >= V48_MARGIN_FLOOR}


def main(argv=None):
    ap = argparse.ArgumentParser(description="v14.3-sellrace 四道验证门")
    ap.add_argument("--gates", default="a,b,c,d")
    ap.add_argument("--arm", choices=("v143", "base"), default="v143",
                    help="b/c 门的臂：v143=runtime+预置，base=纯 v14.2 runtime")
    ap.add_argument("--out", default=None, help="输出 json 路径（默认 OUT）")
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args(argv)
    selected = [g.strip() for g in args.gates.split(",") if g.strip()]
    out = {"protocol": "v143-sellrace-gates/1.0",
           "generated_at_utc": datetime.now(timezone.utc).isoformat(),
           "knob_variant": V143_KNOBS, "arm": getattr(args, "arm", "v143"),
           "gates": {}}
    deps = None
    all_pass = True
    for g in selected:
        if g in ("a", "b", "c") and deps is None:
            deps = bench.make_twin_deps()
        if g == "a":
            res = gate_a(deps, args.smoke)
        elif g == "b":
            res = gate_bc(deps, "b", args.smoke, arm=args.arm)
        elif g == "c":
            res = gate_bc(deps, "c", args.smoke, arm=args.arm)
        elif g == "d":
            res = gate_d(args.smoke)
        else:
            print(f"unknown gate {g!r}")
            return 2
        out["gates"][g] = res
        all_pass = all_pass and bool(res["passed"])
        print(f"[gate {g}] {'PASS' if res['passed'] else 'FAIL'} "
              f"({json.dumps({k: v for k, v in res.items()
                              if k not in ('episodes', 'games')},
                             ensure_ascii=False)})")
    out_path = args.out or OUT
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as handle:
        json.dump(out, handle, ensure_ascii=False, indent=1)
    print(f"ALL {'PASS' if all_pass else 'FAIL'} -> {out_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
