# 【中文】round24_counterfactual_probe.py —— 9 败局分叉点孪生反事实矩阵
# ===========================================================================
# 任务（round-24 v3 证据链 #4）：对 9 深挖局（碾压带 4 + 压制带 5）在
#   资本排程决策窗（d4/d6）与差距分叉日注入"若 G 修复"的策略变体，
#   量化终局资金挽回幅度。证据门：≥5/9 局挽回 ≥10%（终局资金口径）。
# 方法（沿 round23_disaster_dtsp_probe / planner_offline_bench 同机制）：
#   孪生从注入黎明重建状态（twin_noise 实测 0.0），我方席=变体 agent
#   （v13.8 exec 装载 + 命名空间旋钮覆盖，不改 src 现役文件），对手席=
#   回放真实动作（单变量口径）。真值=线上实际（含 DTSP v2 线上决策）。
# 变体面（全部为命名空间常量覆盖 / PLANNER_OVERRIDES 寄存器键）：
#   reactive     纯 v13.8（无覆盖）——对照"线上 DTSP 从该黎明的贡献"
#   dtsp_anchor  离线投影器选中计划的覆盖（同 bench 裁决管线，含对手史）
#   V_LAND       G3 资本排程：二地块 due 7→11（d7-d10 现金让位给买畜；
#                LAND_PLAN 消费语义实测：fund 仅从 due 起才保护）
#   V_WALLET     G3 钱包门放宽：LIQUIDITY_FLOOR 350→150、
#                COW_BUY_RESERVE 380→150（d4-d7 需 1300+→900-）
#   V_WALLET0    同上极限档（0/0）——量化雇工门风险换多少产能
#   V_PACE       G3 步速前置：ANIMAL_PACE 3/日从 d8→d6
#   V_COMB       V_LAND+V_WALLET+V_PACE（v3 旗舰组合）
#   V_ALL        V_COMB+herd_day_shift -1（日程前移，需 PLANNER_ENABLED）
# 只读探针；输出 exports/probes/round24_forensics/round24_counterfactual.json。
# ===========================================================================

from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402
from kaggle_simulations.agent.planner import plans, select  # noqa: E402
from kaggle_simulations.agent.planner import opponents      # noqa: E402

ROOT = os.path.dirname(SOFTWARE)
REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT = os.path.join(SOFTWARE, "exports", "probes", "round24_forensics",
                   "round24_counterfactual.json")
FORKS_JSON = os.path.join(SOFTWARE, "exports", "probes", "round24_forensics",
                          "round24_fork_timelines.json")
TEAM = "renyxin"
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
INJ_DAWNS = (4, 6)          # + 每局的 fork_day（差距分叉日）
PESS_DISCOUNT = 0.75
STRATEGY = "trimmed_mean"
TRIM = select.DEFAULT_TRIM_FRACTION

V_LAND = {"LAND_PLAN.2": (11, 2700)}
V_WALLET = {"LIQUIDITY_FLOOR": 150, "COW_BUY_RESERVE": 150}
V_WALLET0 = {"LIQUIDITY_FLOOR": 0, "COW_BUY_RESERVE": 0}
V_PACE = {"ANIMAL_PACE": ((6, 3), (3, 2))}
V_COMB = {**V_LAND, **V_WALLET, **V_PACE}
V_ALL = {**V_COMB, "PLANNER_ENABLED": True,
         "PLANNER_OVERRIDES.herd_day_shift": -1,
         "PLANNER_OVERRIDES.herd_start_day": 0}
VARIANTS = (("reactive", None), ("V_LAND", V_LAND), ("V_WALLET", V_WALLET),
            ("V_WALLET0", V_WALLET0), ("V_PACE", V_PACE),
            ("V_COMB", V_COMB), ("V_ALL", V_ALL))


def dtsp_anchor_overrides(deps, replay, me_seat, day):
    """离线同机制投影选择（含对手史）→ 计划旋钮覆盖。"""
    step = min(day * 24, len(deps["transition_actions"](replay)) - 2)
    state_p = deps["build"](replay, step)
    obs = bench.build_obs_summary_from_state(deps, state_p, me_seat, day)
    history = bench.extract_opponent_history(replay, 1 - me_seat, step)
    models = opponents.build_default_models(
        history=history, profile_path=None,
        pessimistic=opponents.PessimisticFill(price_discount=PESS_DISCOUNT))
    cands = plans.enumerate_plans(obs)
    jm = {s.key(): {m.name: plans.project_season(
            s, obs, m.supply_pressure(obs)) for m in models} for s in cands}
    sel = select.robust_select(jm, strategy=STRATEGY, trim_fraction=TRIM)
    spec = bench._spec_by_key(cands, sel["best"])
    return plans.plan_to_knob_overrides(spec), sel["best"]


def rollout_variant(deps, replay, me_seat, day, overrides, acts):
    step = min(day * 24, len(acts) - 2)
    agent_fn, _applied, _skip = deps["v13_factory"](overrides)
    state = deps["build"](replay, step)
    final, _taken = bench.rollout_with_replay_opponent(
        deps, state, me_seat, agent_fn, acts, step)
    return float(final[me_seat])


def main():
    with open(FORKS_JSON, "r", encoding="utf-8") as h:
        forks = {f["episode"]: f for f in json.load(h)}
    deps = bench.make_twin_deps()
    out = {"protocol": "round24-counterfactual/1.0",
           "gate": ">=5/9 episodes with >=10% terminal capital gain",
           "episodes": {}}
    for ep in TARGET9:
        path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
        with open(path, "r", encoding="utf-8") as h:
            replay = json.load(h)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        acts = deps["transition_actions"](replay)
        fork_day = forks[ep]["fork_day"] or 17
        dawns = sorted(set(INJ_DAWNS) | {fork_day})
        rec = {"opponent": teams[1 - me], "truth_me": truth_me,
               "truth_opp": truth_opp, "fork_day": forks[ep]["fork_day"],
               "dawns": {}}
        print(f"\n== ep{ep} vs {teams[1 - me]} truth {truth_me:.0f} "
              f"(opp {truth_opp:.0f}) fork {fork_day}")
        for day in dawns:
            drec = {}
            # 孪生核验（d6 一次代表即可，其余日同机制）
            if day == 6:
                state_b = deps["build"](replay, day * 24)
                deps["run_to_end"](state_b, acts[day * 24:])
                twin_final = deps["final"](state_b)
                drec["twin_noise"] = round(
                    abs(float(twin_final[me]) - truth_me), 2)
            for name, ovr in VARIANTS:
                v = rollout_variant(deps, replay, me, day, ovr, acts)
                drec[name] = round(v, 1)
            anchor_ovr, anchor_key = dtsp_anchor_overrides(
                deps, replay, me, day)
            drec["dtsp_anchor"] = round(
                rollout_variant(deps, replay, me, day, anchor_ovr, acts), 1)
            drec["anchor_plan"] = anchor_key
            rec["dawns"][str(day)] = drec
            gains = {k: round(drec[k] - truth_me)
                     for k in ("reactive", "dtsp_anchor", "V_LAND",
                               "V_WALLET", "V_WALLET0", "V_PACE",
                               "V_COMB", "V_ALL")}
            print(f"  d{day:2d} twin_noise {drec.get('twin_noise', '-')} | "
                  + " ".join(f"{k} {g:+6d}" for k, g in gains.items())
                  + f" | anchor {anchor_key[:40]}")
        out["episodes"][str(ep)] = rec

    # ---- 证据门判定（旗舰 V_COMB 与逐局最优两口径，注入窗=d6）----
    def gate(variant):
        rows = []
        for ep, rec in out["episodes"].items():
            d6 = rec["dawns"].get("6")
            if not d6 or variant not in d6:
                rows.append((ep, None))
                continue
            gain_pct = (d6[variant] - rec["truth_me"]) / rec["truth_me"]
            rows.append((ep, gain_pct))
        hit = [ep for ep, g in rows if g is not None and g >= 0.10]
        return rows, hit
    rows_c, hit_c = gate("V_COMB")
    best_pct = {}
    for ep, rec in out["episodes"].items():
        d6 = rec["dawns"].get("6") or {}
        cands = [v for k, v in d6.items()
                 if k not in ("twin_noise", "anchor_plan")
                 and isinstance(v, (int, float))]
        if cands:
            best_pct[ep] = max(cands) / rec["truth_me"] - 1.0
    hit_best = [ep for ep, p in best_pct.items() if p >= 0.10]
    out["gate_V_COMB"] = {"per_episode": {ep: round(g, 4) if g is not None
                                          else None for ep, g in rows_c},
                          "hits": hit_c, "n_hits": len(hit_c),
                          "passed": len(hit_c) >= 5}
    out["gate_best_variant"] = {"per_episode": {ep: round(p, 4)
                                                for ep, p in
                                                best_pct.items()},
                                "hits": hit_best, "n_hits": len(hit_best),
                                "passed": len(hit_best) >= 5}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    print(f"\n证据门 V_COMB：{len(hit_c)}/9 "
          f"({'PASS' if len(hit_c) >= 5 else 'FAIL'} -> {hit_c})")
    print(f"证据门 best-variant 上界：{len(hit_best)}/9 "
          f"({'PASS' if len(hit_best) >= 5 else 'FAIL'} -> {hit_best})")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
