"""Compare a public action trace with frozen local releases; no private code access."""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path

from kaggle_environments.agent import get_last_callable


ROOT = Path(__file__).resolve().parents[2]
REPLAY = ROOT / "research/round10/public_replays/112478088.json.gz"
EPISODE = json.loads(gzip.decompress(REPLAY.read_bytes()))
SEAT = next(i for i, a in enumerate(EPISODE["info"]["Agents"]) if a["Name"] == "MauoXX")
LISTING = json.loads((ROOT / "research/round10/new_submission_episodes.json").read_text(encoding="utf-8"))
assert LISTING["submission_id"] == 56493753
assert any(e["id"] == EPISODE["info"]["EpisodeId"] and
           any(a["submissionId"] == 56493753 for a in e["agents"])
           for e in LISTING["first_episodes"])


def compare(relative_path: str, turns: int = 719) -> dict:
    source = ROOT / relative_path
    entry = get_last_callable(source.read_text(encoding="utf-8"), path=str(source))
    mismatches = []
    examples = []
    for turn in range(turns):
        state = EPISODE["steps"][turn][SEAT]
        observation = dict(state["observation"], step=turn)
        actual = entry(observation, EPISODE["configuration"])
        # Replay steps contain the state *after* the preceding action.
        public_action = EPISODE["steps"][turn + 1][SEAT]["action"]
        if actual != public_action:
            mismatches.append(turn)
            if len(examples) < 2:
                examples.append({"turn": turn, "actual": str(actual)[:300],
                                 "public": str(public_action)[:300]})
    return {"source": relative_path, "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "turns": turns, "matched": turns - len(mismatches),
            "mismatches": mismatches, "examples": examples}


def main() -> None:
    results = [compare(path) for path in (
        "submissions/release_v8/main.py",
        "submissions/release_v9/main.py",
    )]
    destination = ROOT / "research/round10/new_submission_fingerprint.json"
    destination.write_text(json.dumps({"episode_id": EPISODE["info"]["EpisodeId"],
                                       "submission_id": 56493753,
                                       "compressed_replay_sha256": hashlib.sha256(REPLAY.read_bytes()).hexdigest(),
                                       "seat": SEAT, "results": results}, indent=2),
                           encoding="utf-8")
    print(json.dumps(results))


if __name__ == "__main__":
    main()
