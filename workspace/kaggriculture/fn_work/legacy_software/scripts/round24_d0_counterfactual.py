# 【中文】round24_d0_counterfactual.py —— 全季（d0 起）反事实 + 胜局回归
# ===========================================================================
# 背景（round-24 v3 证据链 #4 二段）：mid-game 注入矩阵
#   （round24_counterfactual_probe.py）暴露两个口径问题——
#   a) 中途重启伪影：至少 ep110699710 从 d6 重启的 v13.8 不喂继承畜群
#      （FEED ops 0-2 vs 线上 5/1/5，herd d15→0），restart 路径线上不存在；
#   b) 基线差：线上真值含 DTSP v2 每黎明重规划，纯 v13.8 基线与真值差
#      ±3k-51k，把旋钮效应淹没。
# 本段口径：从 d0 初始态全季 rollout（与 quickwin/bench 同协议）——agent
#   从头连续运行（无重启伪影），对手=回放真实动作（非自适应单变量口径），
#   真值=线上实际（含 DTSP）。测"若执行器带 G 旋钮从 d0 打同对手"的终局差。
# 变体：base（纯 v13.8）/ V_LAND / V_WALLET / V_COMB（旗舰）。
# 回归面：13 胜局跑 base 与 V_COMB，量化旗舰对胜局的损伤。
# 输出：exports/probes/round24_forensics/round24_d0_counterfactual.json
# ===========================================================================

from __future__ import annotations

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE = os.path.dirname(HERE)
if SOFTWARE not in sys.path:
    sys.path.insert(0, SOFTWARE)

import planner_offline_bench as bench                      # noqa: E402

ROOT = os.path.dirname(SOFTWARE)
REPLAY_DIR = os.path.join(ROOT, "references", "data", "online-replays",
                          "round24")
OUT = os.path.join(SOFTWARE, "exports", "probes", "round24_forensics",
                   "round24_d0_counterfactual.json")
TEAM = "renyxin"
TARGET9 = (110687913, 110677576, 110684532, 110694473, 110702221,
           110699710, 110685617, 110841464, 110701172)
WINS13 = (110681129, 110682284, 110683437, 110686759, 110690133,
          110691193, 110692292, 110693383, 110695554, 110696787,
          110697778, 110698875, 110790899)

V_LAND = {"LAND_PLAN.2": (11, 2700)}
V_WALLET = {"LIQUIDITY_FLOOR": 150, "COW_BUY_RESERVE": 150}
V_COMB = {**V_LAND, **V_WALLET, "ANIMAL_PACE": ((6, 3), (3, 2))}
LOSS_VARIANTS = (("base", None), ("V_LAND", V_LAND), ("V_WALLET", V_WALLET),
                 ("V_COMB", V_COMB))
WIN_VARIANTS = (("base", None), ("V_COMB", V_COMB))


def rollout_from_d0(deps, replay, me_seat, overrides):
    agent_fn, _applied, _skip = deps["v13_factory"](overrides)
    state = deps["build"](replay, 0)
    acts = deps["transition_actions"](replay)
    final, taken = bench.rollout_with_replay_opponent(
        deps, state, me_seat, agent_fn, acts, 0)
    return float(final[me_seat]), taken


def main():
    deps = bench.make_twin_deps()
    out = {"protocol": "round24-d0-counterfactual/1.0",
           "note": "d0 全季 rollout，对手=回放真实动作（非自适应）；"
                   "truth=线上实际（含 DTSP v2）",
           "losses": {}, "wins": {}}
    t_start = time.time()
    for ep in TARGET9 + WINS13:
        path = os.path.join(REPLAY_DIR, f"episode-{ep}-replay.json")
        with open(path, "r", encoding="utf-8") as h:
            replay = json.load(h)
        teams = list((replay.get("info") or {}).get("TeamNames") or [])
        me = teams.index(TEAM)
        truth_me = float(replay["rewards"][me])
        truth_opp = float(replay["rewards"][1 - me])
        variants = LOSS_VARIANTS if ep in TARGET9 else WIN_VARIANTS
        rec = {"opponent": teams[1 - me], "truth_me": truth_me,
               "truth_opp": truth_opp, "variants": {}}
        for name, ovr in variants:
            t0 = time.time()
            final, taken = rollout_from_d0(deps, replay, me, ovr)
            rec["variants"][name] = {
                "final": round(final, 1),
                "delta_vs_truth": round(final - truth_me, 1),
                "gain_pct": round((final - truth_me) / truth_me, 4),
                "win_vs_truth_opp": final > truth_opp,
                "wall_s": round(time.time() - t0, 1),
                "steps": taken}
        tgt = "losses" if ep in TARGET9 else "wins"
        out[tgt][str(ep)] = rec
        vs = rec["variants"]
        print(f"ep{ep} [{'L9' if ep in TARGET9 else 'W'}] vs "
              f"{teams[1 - me][:18]:18s} truth {truth_me:8.0f} | "
              + " ".join(f"{n} {vs[n]['final']:8.0f} "
                         f"({vs[n]['delta_vs_truth']:+7.0f})" for n, _ in
                         variants)
              + f"  [{time.time()-t_start:.0f}s]")

    # 证据门（d0 全季口径）：≥5/9 局 V_COMB 挽回 ≥10% 终局资金
    def gate(name):
        hits = []
        rows = {}
        for ep, rec in out["losses"].items():
            v = rec["variants"].get(name)
            if not v:
                continue
            rows[ep] = v["gain_pct"]
            if v["gain_pct"] >= 0.10:
                hits.append(ep)
        best = {}
        for ep, rec in out["losses"].items():
            cands = [vv["gain_pct"] for vv in rec["variants"].values()]
            best[ep] = max(cands)
        hits_best = [ep for ep, p in best.items() if p >= 0.10]
        return {"per_episode": rows, "hits": hits, "n_hits": len(hits),
                "passed": len(hits) >= 5}, \
               {"per_episode": best, "hits": hits_best,
                "n_hits": len(hits_best), "passed": len(hits_best) >= 5}
    g_comb, g_best = gate("V_COMB")
    out["gate_V_COMB_d0"] = g_comb
    out["gate_best_variant_d0"] = g_best
    # 胜局回归：V_COMB 对 13 胜局的终局差
    reg = {ep: round(v["variants"]["V_COMB"]["delta_vs_truth"], 1)
           for ep, v in out["wins"].items()}
    out["win_regression_V_COMB"] = {
        "per_episode": reg,
        "n_hurt": sum(1 for v in reg.values() if v < -1000),
        "n_hurt_over_5pct": sum(
            1 for ep, v in reg.items()
            if v / out["wins"][ep]["truth_me"] < -0.05)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as h:
        json.dump(out, h, ensure_ascii=False, indent=1)
    print(f"\n证据门(d0) V_COMB：{g_comb['n_hits']}/9 "
          f"({'PASS' if g_comb['passed'] else 'FAIL'} -> {g_comb['hits']})")
    print(f"证据门(d0) best-variant 上界：{g_best['n_hits']}/9 "
          f"({'PASS' if g_best['passed'] else 'FAIL'} -> {g_best['hits']})")
    hurt = sum(1 for v in reg.values() if v < -1000)
    print(f"胜局回归 V_COMB：13 局中 {hurt} 局损伤 >1k，"
          f"{out['win_regression_V_COMB']['n_hurt_over_5pct']} 局 >5%")
    print(f"wrote {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
