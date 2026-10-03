"""Read-only unit-action accounting for the preselected public replay sample.

This is descriptive across different worlds, not a causal or paired agent test.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import json
import statistics
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MOVES = {"NORTH", "SOUTH", "EAST", "WEST"}
FOCUS = {"FEED", "CARE", "WATER", "FERTILIZE", "HARVEST", "PLANT", "DELIVER", "PICK_UP"}
STAGES = ((0, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 29))


def replay_path(identity: str, episode_id: int) -> Path:
    directory = "v9_public_replays" if identity == "V9" else "public_replays"
    path = ROOT / directory / f"{episode_id}.json.gz"
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def count_view(entry: dict) -> dict:
    path = replay_path(entry["identity"], entry["episode_id"])
    raw = path.read_bytes()
    replay = json.loads(gzip.decompress(raw))
    seat = entry["seat"]
    by_stage: dict[str, collections.Counter] = {}
    for lo, hi in STAGES:
        stage = f"{lo}-{hi}"
        c: collections.Counter = collections.Counter()
        for tick, players in enumerate(replay["steps"]):
            if tick == 0:
                continue
            state = players[seat].get("observation") or {}
            day = int(state.get("day", (tick - 1) // 24))
            if not lo <= day <= hi:
                continue
            action = players[seat].get("action") or {}
            commands = [action.get("farmer") or ["PASS"], *(action.get("hands") or [])]
            for command in commands:
                verb = str(command[0]) if isinstance(command, list) and command else "PASS"
                c["unit_actions"] += 1
                c[verb] += 1
                if verb in MOVES:
                    c["movement"] += 1
                elif verb == "PASS":
                    c["idle"] += 1
                else:
                    c["physical_work"] += 1
            c["turns"] += 1
            for order in action.get("market") or []:
                if isinstance(order, list) and order:
                    c[f"market_{order[0]}"] += 1
        by_stage[stage] = c
    return {
        "identity": entry["identity"],
        "episode_id": entry["episode_id"],
        "seat": seat,
        "replay_sha256": hashlib.sha256(raw).hexdigest(),
        "stages": {stage: dict(c) for stage, c in by_stage.items()},
    }


def main() -> None:
    exact = json.loads((ROOT / "top_gap_exact_ledger.json").read_text(encoding="utf-8"))
    games = [count_view(entry) for entry in exact]
    aggregate: dict[str, dict] = {}
    for identity in dict.fromkeys(g["identity"] for g in games):
        chosen = [g for g in games if g["identity"] == identity]
        aggregate[identity] = {"games": len(chosen), "stages": {}}
        for lo, hi in STAGES:
            stage = f"{lo}-{hi}"
            keys = set().union(*(g["stages"][stage] for g in chosen))
            medians = {key: statistics.median(g["stages"][stage].get(key, 0) for g in chosen)
                       for key in sorted(keys)}
            fractions = {}
            for metric in ("movement", "physical_work", "idle"):
                fractions[metric] = statistics.median(
                    g["stages"][stage].get(metric, 0) /
                    max(1, g["stages"][stage].get("unit_actions", 0))
                    for g in chosen
                )
            aggregate[identity]["stages"][stage] = {
                "median_counts": medians,
                "median_action_fraction": fractions,
            }
    result = {"sample_rule": "same exact-ledger sample, not matched worlds",
              "games": games, "by_identity": aggregate}
    (ROOT / "action_efficiency.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    for identity, group in aggregate.items():
        print(identity, group["games"])
        for stage in ("6-10", "11-15", "16-20", "21-25"):
            row = group["stages"][stage]
            print(" ", stage, row["median_counts"].get("unit_actions", 0),
                  row["median_action_fraction"],
                  {verb: row["median_counts"].get(verb, 0) for verb in sorted(FOCUS)})


if __name__ == "__main__":
    main()
