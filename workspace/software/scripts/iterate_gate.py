"""Iteration gate harness (m2 wave 3): head-to-head gate checks for candidate
submission versions BEFORE they replace kaggle_simulations/agent/main.py.

Usage (from workspace/software or repo root):
    python scripts/iterate_gate.py --candidate exports/candidates/v2a_dairy.py \
        --label v2a-dairy --rounds 4 --note "FM-1 dairy conversion"

Plays the candidate (loaded from an arbitrary file path, exactly like the
arena loads the submission) against the two m2 gate opponents (cow_baron,
melon_hoarder) plus the m1 guard opponents (expansionist, baseline_wheat)
over N fixed seeds, optionally head-to-head vs the incumbent main.py
(--vs-incumbent), and appends one JSON line per invocation to
exports/logs/iteration_gate_log.jsonl:

    {ts, label, candidate_path, note, rounds, seeds, results{...},
     gate{...}, verdict}

Gate semantics (merge pre-check, m2):
  * vs cow_baron win rate >= 0.5 over the seeds
  * vs melon_hoarder win rate >= 0.5 over the seeds
  * no loss vs expansionist / baseline_wheat on these seeds
The FULL merge gate additionally requires full-pool Elo #1 via run_eval.py
and the frozen regression gate -- that runs separately on the merged file.
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

from kgenv.arena import (SOFTWARE_ROOT as ARENA_ROOT, SUBMISSION_MAIN,
                         load_submission_agent, run_match)
from kgenv.bots.baseline import baseline_wheat_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.engine import FULL_EPISODE_STEPS

LOG_PATH = os.path.join(SOFTWARE_ROOT, "exports", "logs",
                        "iteration_gate_log.jsonl")

GATE_OPPONENTS = ["cow_baron", "melon_hoarder"]      # >= 50% win rate required
GUARD_OPPONENTS = ["expansionist", "baseline_wheat"]  # no losses allowed

OPPONENTS = {
    "cow_baron": cow_baron_agent,
    "melon_hoarder": melon_hoarder_agent,
    "expansionist": expansionist_agent,
    "baseline_wheat": baseline_wheat_agent,
}


def play_set(agent, opponents: dict, seeds, collect_daily=False):
    """agent vs each opponent over seeds; returns per-opponent summaries."""
    out = {}
    for name, opp in opponents.items():
        w = l = t = 0
        margins = []
        for s in seeds:
            res = run_match(agent, opp, seed=s, label_a="cand", label_b=name,
                            episode_steps=FULL_EPISODE_STEPS,
                            collect_daily=collect_daily)
            if res["winner_label"] == "cand":
                w += 1
            elif res["winner_label"] == name:
                l += 1
            else:
                t += 1
            margins.append(res["rewards"][0] - res["rewards"][1])
        n = w + l + t
        out[name] = {
            "games": n, "wins": w, "losses": l, "ties": t,
            "win_rate": round((w + 0.5 * t) / n, 4) if n else None,
            "avg_margin": round(sum(margins) / len(margins), 1) if margins else None,
            "min_margin": round(min(margins), 1) if margins else None,
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", default=SUBMISSION_MAIN,
                    help="path to the candidate agent file")
    ap.add_argument("--label", default="cand", help="short label for the log")
    ap.add_argument("--note", default="", help="one-line change summary")
    ap.add_argument("--rounds", type=int, default=4, help="seeds per pairing")
    ap.add_argument("--first-seed", type=int, default=101)
    ap.add_argument("--vs-incumbent", action="store_true",
                    help="also play candidate vs the current main.py")
    ap.add_argument("--opponents", default="",
                    help="comma list to override (default gate+guard set)")
    ap.add_argument("--no-log", action="store_true")
    args = ap.parse_args()

    candidate = load_submission_agent(args.candidate)
    seeds = list(range(args.first_seed, args.first_seed + max(1, args.rounds)))

    opp_names = (args.opponents.split(",") if args.opponents
                 else GATE_OPPONENTS + GUARD_OPPONENTS)
    opponents = {n: OPPONENTS[n] for n in opp_names}

    t0 = time.perf_counter()
    results = play_set(candidate, opponents, seeds)

    incumbent = None
    if args.vs_incumbent and os.path.abspath(args.candidate) != os.path.abspath(SUBMISSION_MAIN):
        incumbent = load_submission_agent(SUBMISSION_MAIN)
        results["vs_incumbent"] = play_set(candidate, {"incumbent": incumbent},
                                           seeds)["incumbent"]

    elapsed = round(time.perf_counter() - t0, 2)

    gate = {}
    for name in GATE_OPPONENTS:
        if name in results:
            gate[f"wr_vs_{name}"] = results[name]["win_rate"]
            gate[f"pass_vs_{name}"] = (results[name]["win_rate"] or 0) >= 0.5
    guard_ok = all(results[n]["losses"] == 0 for n in GUARD_OPPONENTS
                   if n in results)
    gate["guard_no_losses"] = guard_ok
    if incumbent is not None:
        gate["wr_vs_incumbent"] = results["vs_incumbent"]["win_rate"]
        gate["pass_vs_incumbent"] = (results["vs_incumbent"]["win_rate"] or 0) > 0.5
    gate["pass"] = (all(v for k, v in gate.items() if k.startswith("pass_"))
                    and guard_ok)

    print(f"=== iteration gate: {args.label} ({args.candidate}) ===")
    for name, r in results.items():
        print(f"  vs {name:<16} W{r['wins']} L{r['losses']} T{r['ties']} "
              f"wr={r['win_rate']} avg_margin={r['avg_margin']:+.0f} "
              f"min={r['min_margin']:+.0f}")
    print(f"  gate: {json.dumps(gate)}  [{elapsed}s]")
    print(f"  VERDICT: {'PASS' if gate['pass'] else 'FAIL'}")

    if not args.no_log:
        os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
        entry = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "label": args.label,
            "candidate_path": os.path.relpath(args.candidate, ARENA_ROOT),
            "note": args.note,
            "rounds": len(seeds),
            "seeds": seeds,
            "results": results,
            "gate": gate,
            "verdict": "PASS" if gate["pass"] else "FAIL",
            "elapsed_seconds": elapsed,
        }
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"  logged -> {os.path.relpath(LOG_PATH, ARENA_ROOT)}")
    return 0 if gate["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
