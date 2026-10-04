"""Diagnostic counterfactuals against frozen public action traces, NOT live agents."""
import argparse
import contextlib
import gzip
import io
import json
import time
from pathlib import Path

with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments import make

ROOT = Path(__file__).parent


def tape_policy(actions):
    def replay(obs, config=None):
        return actions[min(int(obs.step), len(actions) - 1)]
    return replay


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate")
    parser.add_argument("--split", choices=["study", "heldout"], default="study")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    index = json.loads((ROOT / "research/top10/index.json").read_text())
    study_ids = {r["episode_id"] for r in index if r["split"] == "study"}
    records = [r for r in index if r["split"] == args.split
               and (args.split == "study" or r["episode_id"] not in study_ids)][:args.limit]
    out = Path(args.output)
    rows = []
    for row in records:
        eid = row["episode_id"]
        game = json.loads(gzip.decompress((ROOT / f"research/top10/{eid}.json.gz").read_bytes()))
        cfg = dict(game["configuration"])
        cfg["seed"] = game["info"]["seed"]
        players = [tape_policy([step[p]["action"] for step in game["steps"][1:]]) for p in range(2)]
        # Keep the ranked player's tape as opponent; replace its historical rival.
        seat = 1 - row["seat"]
        if args.candidate:
            players[seat] = args.candidate
        env = make("kaggriculture", configuration=cfg, debug=True)
        start = time.perf_counter()
        env.run(players)
        final = env.steps[-1]
        assert [s.status for s in final] == ["DONE", "DONE"]
        errors = [v.get("stderr") for logs in env.logs for v in logs if isinstance(v, dict) and v.get("stderr")]
        assert not errors, errors[:2]
        rewards = [s.reward for s in final]
        if not args.candidate:
            assert rewards == game["rewards"], (eid, rewards, game["rewards"])
        r = {**row, "candidate": args.candidate, "candidate_seat": seat,
             "money": rewards[seat], "opponent_money": rewards[1-seat],
             "delta": rewards[seat]-rewards[1-seat], "original_rewards": game["rewards"],
             "seconds": time.perf_counter()-start,
             "max_action_seconds": max(v.get("duration", 0) for logs in env.logs for v in logs if isinstance(v, dict))}
        rows.append(r)
        out.write_text(json.dumps({"kind": "frozen_trace_diagnostic_not_live_top10", "results": rows}, indent=2), encoding="utf-8")
        print(eid, row["team"], round(r["delta"]), flush=True)


if __name__ == "__main__":
    main()
