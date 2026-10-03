"""Read the public leaderboard without attributing a pending submission to V9."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import requests


ROOT = Path(__file__).resolve().parent
API = "https://www.kaggle.com/api/i/competitions.LeaderboardService/GetLeaderboard"
TEAM_ID = 16899200
KNOWN_V8_SUBMISSION_ID = 56481789


def main() -> None:
    response = requests.post(API, json={"competitionId": 147734}, timeout=90)
    response.raise_for_status()
    payload = response.json()
    teams = {int(team["teamId"]): team for team in payload["teams"]}
    rows = payload["publicLeaderboard"]
    own = next((row for row in rows if int(row["teamId"]) == TEAM_ID), None)
    top = [
        {
            "rank": row["rank"],
            "team": teams[int(row["teamId"])]["teamName"],
            "submission_id": row["submissionId"],
            "score": float(row["displayScore"]),
        }
        for row in rows[:10]
    ]
    own_result = None if own is None else {
        "rank": own["rank"],
        "score": float(own["displayScore"]),
        "submission_id": own["submissionId"],
        "is_known_v8_submission": int(own["submissionId"]) == KNOWN_V8_SUBMISSION_ID,
        "last_submission_date": teams[TEAM_ID].get("lastSubmissionDate"),
        "submission_count": teams[TEAM_ID].get("submissionCount"),
    }
    result = {
        "captured_at_utc": datetime.now(timezone.utc).isoformat(),
        "source": "https://www.kaggle.com/competitions/kaggriculture/leaderboard",
        "top10": top,
        "own_team": own_result,
        "v9_attribution_confirmed": False,
        "note": "A new leaderboard submission ID alone does not establish which local archive was uploaded.",
    }
    (ROOT / "public_status_latest.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(result, ensure_ascii=True))


if __name__ == "__main__":
    main()
