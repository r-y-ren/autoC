# -*- coding: utf-8 -*-
# 【中文】panel_v4b.py —— v4b 轻量轮 panel 门（临时脚本，落 tmp/）
# ===========================================================================
# 口径同 gates/panel_gate.py（合成语料：双席纯 v48 驱动孪生整季回放，
# seated 通道 d0 注入 v4b vs 纯 v48，同席位终局资金 ratio），轻量轮 4 局
# （判据 ≥0.98，任务下限 ≥3 局；v4b 预期 ratio=1.0 按构造——行为级≡纯
# v48 + P2 零触发）；通道保真=纯 v48 注入 == 语料真值。
# 产物：tmp/probes_v4b/panel_v4b.json。
# ===========================================================================
from __future__ import annotations

import json
import os
import sys
import time

sys.dont_write_bytecode = True
_HERE = os.path.dirname(os.path.abspath(__file__))
_HYB = os.path.dirname(_HERE)
for _p in (_HERE, os.path.join(_HYB, "gates")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import gate_common as gc  # noqa: E402
import panel_gate  # noqa: E402

V4B_MAIN = os.path.join(_HYB, "v4b", "main.py")
OUT_DIR = os.path.join(_HERE, "probes_v4b")
CORPUS_SEEDS = (11, 22, 33, 47)
RATIO_FLOOR = 0.98


def main() -> int:
    print("== panel v4b（d0 全季反事实资金，seated 通道，轻量轮 4 局）==",
          flush=True)
    t0 = time.perf_counter()
    corpus = panel_gate.build_corpus(CORPUS_SEEDS)

    games = []
    for entry in corpus:
        rec = {"seed": entry["seed"], "corpus_finals": entry["finals"],
               "seats": {}}
        for seat in (0, 1):
            t1 = time.perf_counter()
            finals_v48 = panel_gate.inject(entry["replay"], seat, gc.BASE_MAIN)
            finals_v4b = panel_gate.inject(entry["replay"], seat, V4B_MAIN)
            self_ok = abs(finals_v48[seat] - entry["finals"][seat]) < 1e-6
            ratio = (finals_v4b[seat] / finals_v48[seat]
                     if finals_v48[seat] else None)
            rec["seats"][str(seat)] = {
                "v48_money": finals_v48[seat], "v4b_money": finals_v4b[seat],
                "ratio": round(ratio, 6) if ratio is not None else None,
                "money_equal": finals_v4b[seat] == finals_v48[seat],
                "self_consistency_ok": self_ok,
                "wall_s": round(time.perf_counter() - t1, 1)}
            print(f"  [inject seed={entry['seed']} me_seat={seat}] "
                  f"v48={finals_v48[seat]:10.1f} v4b={finals_v4b[seat]:10.1f} "
                  f"ratio={ratio:.6f} self_consistent={self_ok}", flush=True)
        s0, s1 = rec["seats"]["0"], rec["seats"]["1"]
        game_ratio = ((s0["v4b_money"] + s1["v4b_money"])
                      / (s0["v48_money"] + s1["v48_money"]))
        rec["game_ratio"] = round(game_ratio, 6)
        rec["game_ratio_ok"] = game_ratio >= RATIO_FLOOR
        games.append(rec)

    total_v4b = sum(s["v4b_money"] for g in games for s in g["seats"].values())
    total_v48 = sum(s["v48_money"] for g in games for s in g["seats"].values())
    global_ratio = total_v4b / total_v48
    report = {
        "protocol": "v4b-panel-light/1.0",
        "corpus": {"kind": "engine-synthesized",
                   "driver": "pure v48 both seats, full season, fixed seeds",
                   "seeds": list(CORPUS_SEEDS), "n_games": len(games),
                   "floor": 3},
        "injection": {"point": 0, "channel": "rollout_with_replay_opponent "
                                         "seated（显式 me_seat）"},
        "games": games,
        "totals": {"v4b_money": round(total_v4b, 1),
                   "v48_money": round(total_v48, 1)},
        "global_ratio": round(global_ratio, 6),
        "all_self_consistency_ok": all(s["self_consistency_ok"]
                                       for g in games
                                       for s in g["seats"].values()),
        "all_seats_money_equal": all(s["money_equal"] for g in games
                                     for s in g["seats"].values()),
    }
    report["gate"] = {
        "criterion": f"per-game and global money ratio >= {RATIO_FLOOR} "
                     f"(v4b vs pure v48 injected, same seat)",
        "n_games": len(games), "n_games_floor_ok": len(games) >= 3,
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
    out = gc.write_json(os.path.join(OUT_DIR, "panel_v4b.json"), report)
    print(f"panel passed = {report['gate']['passed']} "
          f"(global={report['global_ratio']:.6f}, per_game="
          f"{report['gate']['per_game_ratios']}, "
          f"all_seats_money_equal={report['all_seats_money_equal']}) -> {out}",
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
