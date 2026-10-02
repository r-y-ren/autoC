"""Combine public replay tensors with both seats of the selected synthetic games."""

import argparse
import hashlib
import json
import shutil
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

from kaggriculture.data.prepare_replays import prepare


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-cache", type=Path, required=True)
    parser.add_argument("--selfplay", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--holdout-per-group", type=int, default=10)
    args = parser.parse_args()
    selected = json.loads((args.selfplay / "complete.json").read_text())
    games = selected["games"]
    groups = ("normal", "tomato", "extreme")
    if args.holdout_per_group < 1 or any(
        sum(g["group"] == group for g in games) <= args.holdout_per_group for group in groups
    ):
        raise ValueError("each group must have training games and the requested holdout games")
    if len({game["seed"] for game in games}) != len(games):
        raise ValueError("duplicate self-play seeds")
    args.output.mkdir(parents=True, exist_ok=True)
    public = json.loads((args.public_cache / "index.json").read_text())
    for row in public["episodes"]:
        src = args.public_cache / f"{row['key']}.npz"
        dst = args.output / src.name
        if not dst.exists():
            shutil.copyfile(src, dst)
        elif hashlib.sha256(src.read_bytes()).digest() != hashlib.sha256(dst.read_bytes()).digest():
            raise ValueError(f"conflicting public cache: {dst}")
    tasks = []
    validation_ids = set()
    for group in ("normal", "tomato", "extreme"):
        ordered = sorted(
            (game for game in games if game["group"] == group),
            key=lambda game: hashlib.sha256(f"51:{game['seed']}".encode()).digest(),
        )
        validation_ids.update(9_000_000_000 + game["seed"] for game in ordered[: args.holdout_per_group])
    for game in games:
        if game["group"] == "tomato" and game["tomato_count"] < 2:
            raise ValueError("tomato stratum mismatch")
        if game["group"] == "extreme" and game["maximum_same_shop"] < 3:
            raise ValueError("extreme stratum mismatch")
        for seat in range(2):
            row = {
                "episode_id": 9_000_000_000 + game["seed"],
                "target_seat": seat,
                "target_submission_id": 0,
                "replay_path": game["path"],
                "replay_sha256": game["sha256"],
            }
            tasks.append((row, str(args.selfplay), str(args.output)))
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = []
        for row in pool.map(prepare, tasks):
            row["split"] = "validation" if row["episode_id"] in validation_ids else "train"
            rows.append(row)
            if len(rows) % 20 == 0:
                print(json.dumps({"event": "prepared", "selfplay_seats": len(rows)}), flush=True)
    index = {
        "schema_version": 1,
        "seed": 50,
        "episodes": public["episodes"] + rows,
        "synthetic_provenance": selected,
        "public_provenance": public.get("manifests", {}),
    }
    temporary = args.output / "index.json.tmp"
    temporary.write_text(json.dumps(index, indent=2) + "\n")
    temporary.replace(args.output / "index.json")
    print(json.dumps({"event": "complete", "episodes": len(index["episodes"])}), flush=True)


if __name__ == "__main__":
    main()
