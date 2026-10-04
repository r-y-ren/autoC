"""Generate heuristic teacher games with controlled shop diversity."""

from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
import gzip
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import time

from kaggriculture.search.reference_engine import Game, SHOPS
from .shop_scenarios import shop_sequence, override_shops

GROUPS = ("normal", "tomato", "extreme")


def play(task: tuple[int, str, str]) -> dict:
    seed, destination, group = task
    os.environ["KAGGRICULTURE_RAISE_AGENT_ERRORS"] = "1"
    from kaggriculture import search

    entry = Path(search.__file__).parent / "main.py"
    agents = []
    for seat in range(2):
        spec = importlib.util.spec_from_file_location(f"_teacher_{seed}_{seat}", entry)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        agents.append(module.agent)
    environment = Game(seed)
    sequence = shop_sequence(group, seed, list(SHOPS))
    observations = [environment.observation(seat) for seat in range(2)]
    steps = [[{"observation": obs, "action": None, "status": "ACTIVE"} for obs in observations]]
    overage = [60.0, 60.0]
    for _ in range(719):
        actions = []
        for seat in range(2):
            observations[seat]["remainingOverageTime"] = overage[seat]
            started = time.monotonic()
            actions.append(agents[seat](observations[seat]))
            overage[seat] -= max(0, time.monotonic() - started - 1.0)
            if overage[seat] < 0:
                raise RuntimeError(f"teacher exceeded overage: seed={seed}, seat={seat}")
        environment.advance(actions)
        override_shops(environment.town, sequence)
        observations = [environment.observation(seat) for seat in range(2)]
        steps.append(
            [
                {"observation": obs, "action": action, "status": "DONE" if environment.done else "ACTIVE"}
                for obs, action in zip(observations, actions, strict=True)
            ]
        )
        if environment.done:
            break
    if not environment.done or len(steps) != 720:
        raise RuntimeError(f"incomplete teacher game: seed={seed}")
    shops = Counter(observations[0]["town"]["unlocked_shops"])
    replay = {
        "module_version": "1.32.7",
        "configuration": {"seed": seed},
        "steps": steps,
        "source": "synthetic heuristic self-play",
        "scenario": group,
        "shop_sequence": sequence,
    }
    relative = f"replays/seed-{seed}.json.gz"
    output = Path(destination) / relative
    with gzip.open(output, "wt") as stream:
        json.dump(replay, stream, separators=(",", ":"))
    return {
        "seed": seed,
        "group": group,
        "path": relative,
        "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
        "tomato_count": shops["PIZZA_SHOP"] + shops["FARMERS_MARKET"],
        "maximum_same_shop": max(shops.values(), default=0),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--per-group", type=int, default=100)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed-start", type=int, default=51010000)
    args = parser.parse_args()
    if args.per_group < 1 or args.workers < 1:
        parser.error("per-group and workers must be positive")
    from kaggriculture import search

    if not (Path(search.__file__).parent / "terminal_search.so").is_file():
        parser.error("compile the search library first with scripts/build_search.py")
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "replays").mkdir(exist_ok=True)
    if (args.output / "games.jsonl").exists():
        parser.error("use a new output directory; completed data will not be overwritten")
    tasks = [
        (args.seed_start + i * args.per_group + j, str(args.output), group)
        for i, group in enumerate(GROUPS)
        for j in range(args.per_group)
    ]
    records = []
    with ProcessPoolExecutor(max_workers=args.workers, max_tasks_per_child=1) as pool:
        for future in as_completed([pool.submit(play, task) for task in tasks]):
            record = future.result()
            records.append(record)
            with (args.output / "games.jsonl").open("a") as stream:
                stream.write(json.dumps(record) + "\n")
            print(json.dumps({"completed_games": len(records), "seed": record["seed"]}), flush=True)
    result = {"games": records, "counts": dict(Counter(r["group"] for r in records)), "per_group": args.per_group}
    (args.output / "complete.json").write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
