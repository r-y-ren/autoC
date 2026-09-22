# -*- coding: utf-8 -*-
# 【中文】panel_gate.py —— run_panel_gate（F3）：d0 全季反事实资金面板
# ===========================================================================
# 契约：fn_docs/responsibility.md —— "孪生 d0 反事实资金 ratio≥0.98（vs
#   纯 v48，同席位）"。
# 口径（如实登记）：本机无官方回放语料（references/data/online-replays/
#   gitignored 缺失）→ 用**引擎合成语料**：固定种子（11/22/33/47/58/69，
#   planner_flagoff_golden 同种子域）、双席各由纯 v48 驱动、孪生引擎
#   （vendored wheel 指纹链 fail-closed）生成 ≥6 局合成回放；官方语料
#   面板登记为主力机补测项。
# 注入：fn_work/src/run_official_bench/rollout_with_replay_opponent.py 的
#   **seated 通道**（显式 me_seat∈{0,1}，禁止恒 seat0）；对每局在 d0
#   （injection_point=0，全季）分别注入混合与纯 v48，对手席=回放动作流。
# 判据：逐局与全局资金 ratio（混合终局资金 / 纯 v48 终局资金）≥ 0.98。
# 通道保真自证：纯 v48 注入终局 == 合成语料记录终局（逐席逐局）。
# 产物：gates/out/panel_gate.json。CLI：python gates/panel_gate.py [--quick]
# ===========================================================================
from __future__ import annotations

import argparse
import json
import os
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

import gate_common as gc  # noqa: E402

CORPUS_SEEDS = (11, 22, 33, 47, 58, 69)
RATIO_FLOOR = 0.98


def build_corpus(seeds) -> list:
    """合成语料：双席各由纯 v48 驱动的整季回放（孪生引擎，固定种子）。"""
    corpus = []
    for seed in seeds:
        t0 = time.perf_counter()
        run = gc.twin_selfplay(
            [lambda: gc.load_agent(gc.BASE_MAIN),
             lambda: gc.load_agent(gc.BASE_MAIN)], seed)
        entry = {
            "seed": seed,
            "finals": run["finals"],
            "transitions": run["transitions"],
            "selfplay_action_stream_sha256": run["action_stream_sha256"],
            "wall_s": round(time.perf_counter() - t0, 1),
            "replay": run["replay"],
        }
        corpus.append(entry)
        print(f"  [corpus] seed={seed} finals={run['finals']} "
              f"transitions={run['transitions']} [{entry['wall_s']}s]",
              flush=True)
    return corpus


def inject(replay, me_seat, agent_path) -> list:
    """seated 通道 d0 注入：agent_path 的 agent 接管 me_seat 席整季
    （obs 经 dict+attr 适配，官方 Struct 读取语义）。"""
    rro = gc.load_rollout_channel()
    agent = gc.adapt_agent_for_twin(gc.load_agent(agent_path))
    return rro.rollout_with_replay_opponent(replay, 0, agent, me_seat)


def run_panel_gate(quick: bool = False) -> dict:
    print("== run_panel_gate（d0 全季反事实资金面板，seated 通道）==",
          flush=True)
    t0 = time.perf_counter()
    base_sha = gc.sha256_file(gc.BASE_MAIN)
    if base_sha != gc.BASE_SHA256:
        raise SystemExit(f"基线 v48 sha 漂移: {base_sha}")

    seeds = CORPUS_SEEDS[:2] if quick else CORPUS_SEEDS
    print(f"-- 合成语料生成（双席纯 v48 驱动，seeds={seeds}）--", flush=True)
    corpus = build_corpus(seeds)

    games = []
    for entry in corpus:
        rec = {"seed": entry["seed"], "corpus_finals": entry["finals"],
               "seats": {}}
        for seat in (0, 1):
            t1 = time.perf_counter()
            finals_v48 = inject(entry["replay"], seat, gc.BASE_MAIN)
            finals_hyb = inject(entry["replay"], seat, gc.HYB_MAIN)
            # 通道保真：纯 v48 注入 == 语料真值（同席）
            self_consistent = (
                abs(finals_v48[seat] - entry["finals"][seat]) < 1e-6)
            ratio = (finals_hyb[seat] / finals_v48[seat]
                     if finals_v48[seat] else None)
            rec["seats"][str(seat)] = {
                "v48_money": finals_v48[seat],
                "hybrid_money": finals_hyb[seat],
                "ratio": round(ratio, 6) if ratio is not None else None,
                "self_consistency_ok": self_consistent,
                "wall_s": round(time.perf_counter() - t1, 1),
            }
            print(f"  [inject seed={entry['seed']} me_seat={seat}] "
                  f"v48={finals_v48[seat]:10.1f} "
                  f"hybrid={finals_hyb[seat]:10.1f} "
                  f"ratio={ratio:.4f} "
                  f"self_consistent={self_consistent}", flush=True)
        s0, s1 = rec["seats"]["0"], rec["seats"]["1"]
        game_ratio = ((s0["hybrid_money"] + s1["hybrid_money"])
                      / (s0["v48_money"] + s1["v48_money"]))
        rec["game_ratio"] = round(game_ratio, 6)
        rec["game_ratio_ok"] = game_ratio >= RATIO_FLOOR
        rec["seat_ratios_ok"] = all(
            s["ratio"] is not None and s["ratio"] >= RATIO_FLOOR
            for s in (s0, s1))
        games.append(rec)

    total_hyb = sum(s["hybrid_money"] for g in games for s in
                    g["seats"].values())
    total_v48 = sum(s["v48_money"] for g in games for s in
                    g["seats"].values())
    global_ratio = total_hyb / total_v48
    report = {
        "protocol": "v48h-panel-gate/1.0",
        "corpus": {
            "kind": "engine-synthesized",
            "engine": "vendored twin (kaggle_environments-1.32.7+nodeps, "
                      "sha-verified scene files; fail-closed fingerprint)",
            "driver": "pure v48 both seats, full season, fixed seeds",
            "seeds": seeds,
            "n_games": len(games),
            "n_games_floor": 6,
            "official_corpus_panel": "主力机补测项（本机官方回放语料 "
                                     "gitignored 缺失，如实登记）",
        },
        "injection": {"point": 0, "meaning": "d0 全季",
                      "channel": "fn_work rollout_with_replay_opponent "
                                 "seated 通道（显式 me_seat）"},
        "games": games,
        "totals": {"hybrid_money": round(total_hyb, 1),
                   "v48_money": round(total_v48, 1)},
        "global_ratio": round(global_ratio, 6),
        "all_self_consistency_ok": all(s["self_consistency_ok"]
                                       for g in games
                                       for s in g["seats"].values()),
    }
    report["gate"] = {
        "criterion": "per-game and global money ratio >= 0.98 "
                     "(hybrid injected vs pure-v48 injected, same seat, "
                     "synthetic corpus)",
        "n_games": len(games),
        "n_games_floor_ok": len(games) >= 6,
        "per_game_ratios": {str(g["seed"]): g["game_ratio"] for g in games},
        "per_game_ok": all(g["game_ratio_ok"] for g in games),
        "global_ratio": report["global_ratio"],
        "global_ok": global_ratio >= RATIO_FLOOR,
        "self_consistency_ok": report["all_self_consistency_ok"],
    }
    report["gate"]["passed"] = (report["gate"]["per_game_ok"]
                                and report["gate"]["global_ok"]
                                and report["gate"]["n_games_floor_ok"]
                                and report["gate"]["self_consistency_ok"])
    report["wall_s"] = round(time.perf_counter() - t0, 1)
    out = gc.write_json(os.path.join(gc.OUT_DIR, "panel_gate.json"), report)
    print(f"panel_gate passed = {report['gate']['passed']} "
          f"(global_ratio={report['global_ratio']:.4f}, "
          f"per_game_ratios="
          f"{report['gate']['per_game_ratios']}) -> {out}", flush=True)
    return report


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="v48_hybrid panel gate (F3)")
    ap.add_argument("--quick", action="store_true",
                    help="2 种子冒烟（不构成门判据）")
    args = ap.parse_args()
    rep = run_panel_gate(quick=args.quick)
    print(json.dumps({"corpus": rep["corpus"], "gate": rep["gate"],
                      "totals": rep["totals"]},
                     ensure_ascii=False, indent=1))
    sys.exit(0 if rep["gate"]["passed"] else 1)
