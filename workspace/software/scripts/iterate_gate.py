"""Fail-closed AB/BA iteration gate for candidate submissions."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(SOFTWARE_ROOT))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import SUBMISSION_MAIN, load_submission_agent, run_match
from kgenv.bots.baseline import baseline_wheat_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.bots.online_pool import (crop_rotator_agent,
                                    near_band_diversified_agent,
                                    self_feed_ranch_agent,
                                    template_wheat_agent)
from kgenv.engine import FULL_EPISODE_STEPS
from kgenv.eval_contract import (ContractError, build_ab_ba_schedule,
                                 candidate_snapshot, validate_gate_run)

LOG_PATH = os.path.join(SOFTWARE_ROOT, "exports", "logs",
                        "iteration_gate_log.jsonl")
GATE_OPPONENTS = ["cow_baron", "melon_hoarder"]
GUARD_OPPONENTS = ["expansionist", "baseline_wheat"]
# m2 online-style opponents (campaign III): certified ladder-archetype
# reconstructions -- required in the complete gate alongside the wave-2 set
ONLINE_OPPONENTS = [
    "crop_rotator",
    "template_wheat",
    "self_feed_ranch",
    "near_band_diversified",
]
REQUIRED_OPPONENTS = GATE_OPPONENTS + GUARD_OPPONENTS + ONLINE_OPPONENTS
OPPONENTS = {
    "cow_baron": cow_baron_agent,
    "melon_hoarder": melon_hoarder_agent,
    "expansionist": expansionist_agent,
    "baseline_wheat": baseline_wheat_agent,
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "near_band_diversified": near_band_diversified_agent,
}


def play_set(agent, opponents: dict, seeds, collect_daily=False):
    """Play every candidate/opponent/seed in both seat orders."""
    schedule = build_ab_ba_schedule(
        [("cand", name) for name in opponents], seeds, "development")
    games = []
    for item in schedule:
        opponent = opponents[item["b"]]
        if item["seat"] == "AB":
            result = run_match(agent, opponent, seed=item["seed"],
                               label_a="cand", label_b=item["b"],
                               episode_steps=FULL_EPISODE_STEPS,
                               collect_daily=collect_daily)
        else:
            result = run_match(opponent, agent, seed=item["seed"],
                               label_a=item["b"], label_b="cand",
                               episode_steps=FULL_EPISODE_STEPS,
                               collect_daily=collect_daily)
        result["seat"] = item["seat"]
        result["seed_domain"] = item["seed_domain"]
        games.append(result)
    return games


def summarize_gate_games(games, opponents):
    summaries = {}
    for name in opponents:
        selected = [g for g in games if name in g["players"]]
        wins = sum(g["winner_label"] == "cand" for g in selected)
        losses = sum(g["winner_label"] == name for g in selected)
        ties = sum(g["winner_label"] is None for g in selected)
        margins = []
        seats = {"AB": 0, "BA": 0}
        for game in selected:
            candidate_index = game["players"].index("cand")
            margins.append(game["rewards"][candidate_index] -
                           game["rewards"][1 - candidate_index])
            seats[game["seat"]] += 1
        count = len(selected)
        summaries[name] = {
            "games": count,
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "win_rate": round((wins + 0.5 * ties) / count, 4) if count else None,
            "avg_margin": round(sum(margins) / count, 1) if count else None,
            "min_margin": round(min(margins), 1) if margins else None,
            "seats": seats,
        }
    return summaries


def gate_verdict(games, opponents, seeds, require_complete):
    contract = validate_gate_run(
        games, opponents, seeds, require_complete=require_complete,
        required_opponents=REQUIRED_OPPONENTS)
    summaries = summarize_gate_games(games, opponents)
    threshold_pool = GATE_OPPONENTS + ONLINE_OPPONENTS
    thresholds_ok = all(
        summaries[name]["win_rate"] is not None and
        summaries[name]["win_rate"] >= 0.5
        for name in threshold_pool if name in summaries)
    guards_ok = all(summaries[name]["losses"] == 0
                    for name in GUARD_OPPONENTS if name in summaries)
    if require_complete:
        thresholds_ok = thresholds_ok and all(
            name in summaries for name in threshold_pool)
        guards_ok = guards_ok and all(name in summaries for name in GUARD_OPPONENTS)
    performance_pass = thresholds_ok and guards_ok
    formal_pass = bool(contract["formal_pass"] and performance_pass)
    return summaries, {
        **contract,
        "performance_pass": performance_pass,
        "formal_pass": formal_pass,
        "pass": formal_pass,
    }


def _export_game(game):
    return {
        "p0": game["players"][0],
        "p1": game["players"][1],
        "seed": game["seed"],
        "seed_domain": game["seed_domain"],
        "seat": game["seat"],
        "statuses": game["statuses"],
        "contract_ok": game["contract_ok"],
        "rewards": game["rewards"],
        "winner": game["winner_label"],
        "turns": game["turns_played"],
        "elapsed_seconds": game["elapsed_seconds"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate", default=SUBMISSION_MAIN)
    parser.add_argument("--label", default="cand")
    parser.add_argument("--note", default="")
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--first-seed", type=int, default=101)
    parser.add_argument("--vs-incumbent", action="store_true")
    parser.add_argument("--opponents", default="")
    parser.add_argument("--require-complete", action="store_true")
    parser.add_argument("--no-log", action="store_true")
    args = parser.parse_args()

    custom_subset = bool(args.opponents)
    opponent_names = ([name.strip() for name in args.opponents.split(",") if name.strip()]
                      if custom_subset else list(REQUIRED_OPPONENTS))
    unknown = [name for name in opponent_names if name not in OPPONENTS]
    if unknown:
        print(f"unknown opponents: {unknown}", file=sys.stderr)
        return 2
    formal_mode = not custom_subset
    if args.require_complete and custom_subset:
        print("--require-complete cannot be combined with --opponents; "
              "custom subsets are exploratory", file=sys.stderr)
        return 2
    require_complete = formal_mode or args.require_complete
    if require_complete and (args.first_seed != 101 or args.rounds != 4):
        print("complete gate requires --first-seed 101 --rounds 4", file=sys.stderr)
        return 2
    seeds = list(range(args.first_seed, args.first_seed + max(1, args.rounds)))

    contract_input = {
        "mode": "gate",
        "opponents": opponent_names,
        "seeds": seeds,
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
        "episode_steps": FULL_EPISODE_STEPS,
    }
    try:
        with candidate_snapshot(REPO_ROOT, args.candidate, contract_input) as snapshot:
            identity = snapshot.identity
            candidate = load_submission_agent(str(snapshot.snapshot_path))
            started = time.perf_counter()
            games = play_set(candidate, {name: OPPONENTS[name] for name in opponent_names}, seeds)
            summaries, gate = gate_verdict(games, opponent_names, seeds, require_complete)

            if args.vs_incumbent and os.path.abspath(args.candidate) != os.path.abspath(SUBMISSION_MAIN):
                incumbent = load_submission_agent(SUBMISSION_MAIN)
                incumbent_games = play_set(candidate, {"incumbent": incumbent}, seeds)
                summaries["vs_incumbent"] = summarize_gate_games(
                    incumbent_games, ["incumbent"]
                )["incumbent"]

            elapsed = round(time.perf_counter() - started, 2)
            verdict = "PASS" if gate["formal_pass"] else (
                "EXPLORATORY" if gate["mode"] == "exploratory" else "FAIL"
            )
            snapshot.verify_unchanged()

            print(f"=== iteration gate: {args.label} ({args.candidate}) ===")
            for name, result in summaries.items():
                print(f"  vs {name:<16} W{result['wins']} L{result['losses']} "
                      f"T{result['ties']} wr={result['win_rate']} seats={result['seats']}")
            print(f"  contract: expected={gate['expected_games']} actual={gate['actual_games']} "
                  f"abnormal={gate['abnormal_games']} mode={gate['mode']}")
            print(f"  VERDICT: {verdict}")

            if not args.no_log:
                os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
                entry = {
                    "schema_version": "2.0",
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "label": args.label,
                    "candidate_path": os.path.relpath(args.candidate, SOFTWARE_ROOT),
                    "note": args.note,
                    "identity": identity,
                    "config": contract_input,
                    "games": [_export_game(game) for game in games],
                    "results": summaries,
                    "gate": gate,
                    "verdict": verdict,
                    "elapsed_seconds": elapsed,
                }
                snapshot.verify_unchanged()
                line = (json.dumps(entry, ensure_ascii=False) + "\n").encode("utf-8")
                previous = open(LOG_PATH, "rb").read() if os.path.exists(LOG_PATH) else b""
                temp_path = f"{LOG_PATH}.{os.getpid()}.tmp"
                try:
                    with open(temp_path, "wb") as stream:
                        stream.write(previous)
                        stream.write(line)
                        stream.flush()
                        os.fsync(stream.fileno())
                    os.replace(temp_path, LOG_PATH)
                finally:
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
                print(f"  logged -> {os.path.relpath(LOG_PATH, SOFTWARE_ROOT)}")

            snapshot.verify_candidate_unchanged()
            if gate["formal_pass"]:
                return 0
            return 3 if gate["mode"] == "exploratory" else 1
    except (ContractError, RuntimeError, OSError, ValueError) as exc:
        print(f"VERDICT: FAIL ({exc})", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
