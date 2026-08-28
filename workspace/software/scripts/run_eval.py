"""Local A/B evaluation: contenders x opponent pool on the official engine.

Usage (from workspace/software or repo root):
    python scripts/run_eval.py [--rounds 4] [--quick]

Quick mode shrinks the matrix for smoke purposes; default mode plays a full
round-robin subset, computes Elo ratings (win/loss/tie only, mirroring the
official ladder semantics), writes exports/eval_results.json (validated by
exports/schema.json) and a per-game replay log (复盘日志) under exports/logs/.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import (SOFTWARE_ROOT as ARENA_ROOT, load_submission_agent,
                         run_match, summarize_games, write_replay_log)
from kgenv.bots.baseline import baseline_wheat_agent, greedy_carrot_agent
from kgenv.elo import EloTable
from kgenv.engine import FULL_EPISODE_STEPS
from kgenv import official_engine_version

EXPORTS_DIR = os.path.join(SOFTWARE_ROOT, "exports")
SCHEMA_VERSION = "1.0"


def build_players():
    """Contenders (ours) and the opponent pool (>=3 distinct styles)."""
    submission = load_submission_agent()
    contenders = {
        "submission": submission,        # enhanced bot (main.py)
        "baseline_wheat": baseline_wheat_agent,
    }
    opponents = {
        "pass": "pass",                  # engine built-ins
        "random": "random",
        "starter": "starter",            # official deterministic carrot loop
        "greedy_carrot": greedy_carrot_agent,
    }
    return contenders, opponents


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=4,
                    help="seeds per contender-vs-opponent pairing")
    ap.add_argument("--quick", action="store_true",
                    help="tiny matrix for smoke tests")
    args = ap.parse_args()

    contenders, opponents = build_players()
    everyone = dict(contenders)
    everyone.update(opponents)

    rounds = 1 if args.quick else max(1, args.rounds)
    seeds = list(range(101, 101 + rounds))

    games = []
    t0 = time.perf_counter()

    # contenders vs opponent pool
    for cname, cbot in contenders.items():
        for oname, obot in opponents.items():
            for s in seeds:
                res = run_match(cbot, obot, seed=s, label_a=cname, label_b=oname,
                                episode_steps=FULL_EPISODE_STEPS, collect_daily=False)
                games.append(res)
                print(f"[{len(games):02d}] {cname} vs {oname} seed={s}: "
                      f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
                      f"winner={res['winner_label']}")
    # head-to-head A/B between our own contenders (double seeds)
    for s in seeds + [x + 500 for x in seeds]:
        res = run_match(contenders["submission"], contenders["baseline_wheat"],
                        seed=s, label_a="submission", label_b="baseline_wheat",
                        episode_steps=FULL_EPISODE_STEPS, collect_daily=False)
        games.append(res)
        print(f"[{len(games):02d}] submission vs baseline_wheat seed={s}: "
              f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
              f"winner={res['winner_label']}")

    runtime = time.perf_counter() - t0

    # Elo over the recorded stream (order = play order, as recorded)
    table = EloTable(k=32.0, start=1200.0)
    for g in games:
        if g["winner_label"] == g["players"][0]:
            score = 1.0
        elif g["winner_label"] == g["players"][1]:
            score = 0.0
        else:
            score = 0.5
        table.record(g["players"][0], g["players"][1], score)

    h2h = []
    pairs = [(c, o) for c in contenders for o in opponents] + \
            [("submission", "baseline_wheat")]
    for a, b in pairs:
        h2h.append(summarize_games(games, a, b))

    os.makedirs(EXPORTS_DIR, exist_ok=True)
    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "engine": {
            "package": "kaggle-environments",
            "version": official_engine_version(),
            "scenario": "kaggriculture",
            "episode_steps": FULL_EPISODE_STEPS,
        },
        "config": {"rounds": rounds, "seeds": seeds,
                   "contenders": list(contenders), "opponents": list(opponents)},
        "games": [{
            "p0": g["players"][0], "p1": g["players"][1], "seed": g["seed"],
            "rewards": g["rewards"], "winner": g["winner_label"],
            "turns": g["turns_played"], "elapsed_seconds": g["elapsed_seconds"],
        } for g in games],
        "head_to_head": h2h,
        "elo": {"k": 32.0, "start": 1200.0, "table": table.ranked()},
        "runtime_seconds": round(runtime, 2),
    }
    out_path = os.path.join(EXPORTS_DIR, "eval_results.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    log_path = write_replay_log(os.path.join(EXPORTS_DIR, "logs"), games)

    print(f"\n=== Elo table ({len(games)} games, {result['runtime_seconds']}s) ===")
    for row in table.ranked():
        print(f"  {row['name']:<16} rating={row['rating']:7.1f} "
              f"record W{row['record']['W']} L{row['record']['L']} T{row['record']['T']}")
    for row in h2h:
        print(f"  {row['pair']:<32} games={row['games']} "
              f"W{row['wins']} L{row['losses']} T{row['ties']} "
              f"win_rate={row['win_rate']} avg_turns={row['avg_turns']}")
    print(f"\nwrote {out_path}")
    print(f"wrote {log_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
