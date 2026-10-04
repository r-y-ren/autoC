"""Preserve a timestamped, public Kaggriculture leaderboard and recent replays.

The replay sample is the four most recent completed, non-self episodes for
each of the top five teams. Selection uses metadata only, before reading the
replay contents. This is research material, not an agent submission.
"""

from __future__ import annotations

import concurrent.futures
import gzip
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
BASE = "https://www.kaggle.com"
API = BASE + "/api/i/"
COMPETITION_ID = 147734
SAMPLE_PER_TEAM = 4


def post(path: str, payload: dict) -> dict:
    response = requests.post(API + path, json=payload, timeout=90)
    response.raise_for_status()
    return response.json()


def public_replay(episode_id: int) -> dict:
    destination = ROOT / "public_replays" / f"{episode_id}.json.gz"
    if destination.exists():
        raw = gzip.decompress(destination.read_bytes())
    else:
        response = requests.get(
            f"{BASE}/competitions/episodes/{episode_id}/replay.json", timeout=90
        )
        response.raise_for_status()
        raw = response.content
        obj = json.loads(raw)
        assert obj["info"]["EpisodeId"] == episode_id
        assert len(obj["steps"]) == 720
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(gzip.compress(raw))
    obj = json.loads(raw)
    assert obj["info"]["EpisodeId"] == episode_id
    assert len(obj["steps"]) == 720
    return {
        "episode_id": episode_id,
        "path": str(destination.relative_to(ROOT.parent.parent)),
        "replay_sha256": hashlib.sha256(raw).hexdigest(),
        "seed": obj["info"].get("seed"),
        "rewards": obj.get("rewards"),
    }


def main() -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    captured = datetime.now(timezone.utc).isoformat()
    data = post(
        "competitions.LeaderboardService/GetLeaderboard",
        {"competitionId": COMPETITION_ID},
    )
    teams = {int(row["teamId"]): row for row in data["teams"]}
    top = []
    for row in data["publicLeaderboard"][:20]:
        team = teams[int(row["teamId"])]
        top.append(
            {
                "rank": row["rank"],
                "team_id": row["teamId"],
                "team_name": team["teamName"],
                "submission_id": row["submissionId"],
                "display_score": float(row["displayScore"]),
                "last_submission_date": team.get("lastSubmissionDate"),
            }
        )
    snapshot = {
        "captured_at_utc": captured,
        "competition_id": COMPETITION_ID,
        "source": BASE + "/competitions/kaggriculture/leaderboard",
        "api": API + "competitions.LeaderboardService/GetLeaderboard",
        "top20": top,
    }
    (ROOT / "leaderboard_snapshot.json").write_text(
        json.dumps(snapshot, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    selection = []
    for team in top[:5]:
        listing = post(
            "competitions.EpisodeService/ListEpisodes",
            {"submissionId": team["submission_id"]},
        )
        selected = []
        for episode in listing["episodes"]:
            agents = episode.get("agents") or []
            if episode.get("state") != "COMPLETED" or len(agents) != 2:
                continue
            own = [a for a in agents if a["submissionId"] == team["submission_id"]]
            if len(own) != 1:
                continue
            if agents[0]["submissionId"] == agents[1]["submissionId"]:
                continue
            own = own[0]
            other = next(a for a in agents if a is not own)
            selected.append(
                {
                    "team": team["team_name"],
                    "rank_at_capture": team["rank"],
                    "submission_id": team["submission_id"],
                    "episode_id": episode["id"],
                    "end_time": episode.get("endTime"),
                    "seat": own.get("index", 0),
                    "reward": own.get("reward"),
                    "opponent_submission_id": other["submissionId"],
                    "opponent_reward": other.get("reward"),
                }
            )
            if len(selected) >= SAMPLE_PER_TEAM:
                break
        selection.extend(selected)
        print(team["rank"], team["team_name"], "selected", len(selected), flush=True)

    (ROOT / "recent_episode_selection.json").write_text(
        json.dumps(
            {
                "captured_at_utc": captured,
                "selection_rule": "latest four completed public non-self episodes per current top-five team, API order, before replay inspection",
                "episodes": selection,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    ids = sorted({int(item["episode_id"]) for item in selection})
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        downloads = list(pool.map(public_replay, ids))
    (ROOT / "replay_provenance.json").write_text(
        json.dumps(downloads, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("captured", captured, "replays", len(downloads), flush=True)


if __name__ == "__main__":
    main()
