"""Normalize an explicit replay/teacher-seat list into BC source manifests."""

import argparse
import gzip
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("index", type=Path, help="JSONL: path, episode_id, seat, submission_id")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sources = {}
    identities = set()
    for line in args.index.read_text().splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        replay_path = args.index.parent / item["path"]
        opener = gzip.open if replay_path.suffix == ".gz" else open
        with opener(replay_path, "rt") as stream:
            replay = json.load(stream)
        episode, seat, submission = int(item["episode_id"]), int(item["seat"]), int(item["submission_id"])
        if seat not in (0, 1):
            raise ValueError("seat must be 0 or 1")
        if replay.get("module_version") != "1.32.7" or len(replay.get("steps", [])) != 720:
            raise ValueError(f"replay {episode} must contain all 720 states under engine 1.32.7")
        if (submission, episode, seat) in identities:
            continue
        identities.add((submission, episode, seat))
        directory = args.output / str(submission)
        destination = directory / "replays" / f"{episode}.json.gz"
        destination.parent.mkdir(parents=True, exist_ok=True)
        normalized = json.dumps(replay, separators=(",", ":")).encode()
        compressed = gzip.compress(normalized, mtime=0)
        if destination.exists() and destination.read_bytes() != compressed:
            raise ValueError(f"conflicting existing replay {episode}")
        destination.write_bytes(compressed)
        sources.setdefault(submission, []).append(
            {
                "episode_id": episode,
                "target_seat": seat,
                "target_submission_id": submission,
                "replay_path": str(destination.relative_to(directory)),
                "replay_sha256": hashlib.sha256(compressed).hexdigest(),
                "replay_bytes": len(compressed),
            }
        )
    for submission, rows in sources.items():
        manifest = {"source": {"submission_id": submission}, "episode_count": len(rows), "episodes": rows}
        (args.output / str(submission) / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"sources": len(sources), "teacher_trajectories": len(identities)}))


if __name__ == "__main__":
    main()
