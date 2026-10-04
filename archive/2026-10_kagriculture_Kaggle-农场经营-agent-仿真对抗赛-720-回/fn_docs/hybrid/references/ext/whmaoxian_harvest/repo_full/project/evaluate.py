"""Reproducible full games through the unmodified official environment."""
import argparse
import contextlib
import hashlib
import io
import json
import statistics
import time
from pathlib import Path

# A minimal install intentionally omits dependencies for unrelated environments.
with contextlib.redirect_stdout(io.StringIO()) as import_log:
    import kaggle_environments
    from kaggle_environments import make


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent", default="main.py")
    parser.add_argument("--opponent", default="starter")
    parser.add_argument("--seeds", type=int, nargs="+", default=[0, 1, 2])
    parser.add_argument("--both-seats", action="store_true")
    parser.add_argument("--output", default="results/baseline.json")
    parser.add_argument("--replay", action="store_true")
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for seed in args.seeds:
        for seat in ([0, 1] if args.both_seats else [0]):
            env = make("kaggriculture", configuration={"seed": seed, "episodeSteps": 720}, debug=True)
            players = [args.agent, args.opponent]
            if seat:
                players.reverse()
            start = time.perf_counter()
            env.run(players)
            state = env.steps[-1]
            statuses = [s.status for s in state]
            if statuses != ["DONE", "DONE"]:
                raise RuntimeError(f"Game failed: {statuses}")
            logs = [entry[seat] for entry in env.logs if len(entry) > seat and isinstance(entry[seat], dict)]
            errors = [log.get("stderr", "") for log in logs if log.get("stderr", "").strip()]
            all_logs = [log for entries in env.logs for log in entries if isinstance(log, dict)]
            opponent_errors = [log.get("stderr", "") for entries in env.logs
                               for i, log in enumerate(entries)
                               if i != seat and isinstance(log, dict) and log.get("stderr", "").strip()]
            if errors:
                raise RuntimeError(f"Agent stderr: {errors[:3]}")
            if opponent_errors:
                raise RuntimeError(f"Opponent stderr: {opponent_errors[:3]}")
            money = [s.observation.farms[i]["money"] for i, s in enumerate(state)]
            delta = money[seat] - money[1 - seat]
            row = {"seed": seed, "seat": seat, "money": money[seat],
                   "opponent_money": money[1-seat], "delta": delta,
                   "result": "win" if delta > 0 else "loss" if delta < 0 else "tie",
                   "statuses": statuses, "states": len(env.steps),
                   "seconds": round(time.perf_counter() - start, 3),
                   "max_action_seconds": max((log.get("duration", 0) for log in logs), default=0),
                   "max_both_players_action_seconds": max((log.get("duration", 0) for log in all_logs), default=0),
                   "final_carried": sum(sum(inv.values()) for inv in state[seat].observation.private["inventories"]),
                   "final_shed": dict(state[seat].observation.private["shed"])}
            rows.append(row)
            output.with_suffix(".progress.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
            print(json.dumps(row), flush=True)
            if args.replay:
                output.with_name(f"{output.stem}-seed{seed}-seat{seat}-replay.json").write_text(json.dumps(env.toJSON()), encoding="utf-8")
    report = {"environment_version": kaggle_environments.__version__,
              "agent": args.agent, "agent_sha256": hashlib.sha256(Path(args.agent).read_bytes()).hexdigest(),
              "opponent": args.opponent, "games": len(rows),
              "opponent_sha256": hashlib.sha256(Path(args.opponent).read_bytes()).hexdigest() if Path(args.opponent).is_file() else None,
              "wins": sum(r["result"] == "win" for r in rows),
              "ties": sum(r["result"] == "tie" for r in rows),
              "mean_money": statistics.mean(r["money"] for r in rows), "results": rows,
              "import_notices": import_log.getvalue()}
    output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Saved {output}: {report['wins']}/{report['games']} wins, mean bank {report['mean_money']:.1f}")


if __name__ == "__main__":
    main()
