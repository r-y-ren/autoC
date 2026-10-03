"""Download a small declared recent win/loss audit set for the user's v6."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import contextlib
import copy
import gzip
import io
import json
from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "research/round7"
SUBMISSION = 56416104
data = json.loads((OUT / "user_episodes.json").read_text())
teams = {row["id"]: row for row in data.get("teams", [])}
with contextlib.redirect_stdout(io.StringIO()):
    from kaggle_environments.agent import get_last_callable

rows = []
for e in sorted(data["episodes"], key=lambda e:e.get("endTime", ""), reverse=True):
    if e["state"] != "COMPLETED" or e.get("type") != "EPISODE_TYPE_PUBLIC":
        continue
    ours = [a for a in e["agents"] if a.get("submissionId") == SUBMISSION]
    rivals = [a for a in e["agents"] if a.get("submissionId") != SUBMISSION]
    if not ours or len(rivals) != 1:
        continue
    a, b = ours[0], rivals[0]
    delta = a["reward"] - b["reward"]
    rows.append({"episode_id": e["id"], "time": e["endTime"], "seat": a.get("index", 0),
                 "money": a["reward"], "opponent_money": b["reward"], "delta": delta,
                 "result": "win" if delta>0 else "loss" if delta<0 else "tie",
                 "rating_before": a["initialScore"], "rating_after": a["updatedScore"],
                 "opponent": teams.get(b["teamId"], {}).get("teamName", teams.get(b["teamId"], {}).get("name", str(b["teamId"]))),
                 "opponent_submission_id": b["submissionId"]})
selection = [r for r in rows if r["result"] == "loss"][:4] + [r for r in rows if r["result"] == "win"][:2]


def fetch(row):
    path = OUT / f"user-{row['episode_id']}.json.gz"
    if not path.exists():
        r = requests.get(f"https://www.kaggle.com/competitions/episodes/{row['episode_id']}/replay.json", timeout=60)
        r.raise_for_status()
        replay = r.json()
        assert len(replay["steps"]) == 720
        path.write_bytes(gzip.compress(r.content))
    return row


with ThreadPoolExecutor(max_workers=3) as pool:
    list(pool.map(fetch, selection))


def policy_parity(replay, seat):
    path = ROOT / "submissions/release_v6/main.py"
    fn = get_last_callable(path.read_text(encoding="utf-8"), path=str(path))
    mismatches = []
    for t in range(719):
        obs = copy.deepcopy(replay["steps"][t][seat]["observation"])
        obs["step"] = t
        act = fn(obs, replay["configuration"])
        expected = replay["steps"][t+1][seat]["action"]
        if act != expected:
            mismatches.append({"step": t, "expected_v6": act, "actual": expected})
    return {"matching_actions": 719-len(mismatches), "first_differences": mismatches[:8]}


audits = []
for row in selection:
    replay = json.loads(gzip.decompress((OUT / f"user-{row['episode_id']}.json.gz").read_bytes()))
    parity = [policy_parity(replay, p) for p in range(2)]
    development = []
    for t in [24,72,144,240,360,480,600,696,719]:
        obs = replay["steps"][t][0]["observation"]
        farms = []
        for p, farm in enumerate(obs["farms"]):
            private = replay["steps"][t][p]["observation"]["private"]
            farms.append({"money": farm["money"], "land": len(farm["unlocked_quadrants"]),
                          "mix": dict(Counter(tile.get("animal") or tile.get("crop") or tile.get("kind")
                                              for line in farm["tiles"] for tile in line if isinstance(tile, dict))),
                          "shed": private["shed"], "carried": dict(sum((Counter(inv) for inv in private["inventories"]), Counter()))})
        development.append({"step": t, "farms": farms, "shops": obs["town"]["unlocked_shops"]})
    record = {**row, "seed": replay["info"]["seed"], "names": replay["info"].get("TeamNames"),
              "statuses": replay["statuses"], "v6_action_parity_by_seat": parity, "development": development}
    audits.append(record)
    print(row["episode_id"], row["result"], row["delta"], [r["matching_actions"] for r in parity], flush=True)
    (OUT / "user_recent_audit.json").write_text(json.dumps({"selection": "most recent four losses and two wins, ordered by endTime", "games": audits}, ensure_ascii=False, indent=2), encoding="utf-8")

summary = {"submission_id": SUBMISSION, "games_in_api_response": len(rows),
           "record_all": dict(Counter(r["result"] for r in rows)),
           "record_last_50": dict(Counter(r["result"] for r in rows[:50])),
           "record_last_20": dict(Counter(r["result"] for r in rows[:20])),
           "last_50_non_ties_with_abs_margin_lt_1000": sum(0<abs(r["delta"])<1000 for r in rows[:50]),
           "latest_rating": rows[0]["rating_after"], "latest_time": rows[0]["time"],
           "peak_rating": max(r["rating_after"] for r in rows), "recent": rows[:50]}
(OUT / "user_episode_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({k:v for k,v in summary.items() if k != "recent"}, ensure_ascii=False), flush=True)
