"""Download public top-submission episodes and preserve provenance (read-only API)."""
import concurrent.futures
import gzip
import json
from pathlib import Path
import requests

TOP = [(1, "DSM", 3127.5, 56401245), (2, "Vadim Vasilenko", 3072.5, 56396983),
       (3, "THIRD FARM CLUB", 3067.4, 56395336), (4, "Majkel1337", 3064.2, 56407295),
       (5, "SpaTaro", 3045.2, 56352346), (6, "Unknown Mother-Goose", 3039.7, 56390472),
       (7, "QQ", 3010.8, 56327925), (8, "Orbital Terraformer", 3006.1, 56263779),
       (9, "Yannik Schiffner", 3001.0, 56392345), (10, "Kaggledew Valley", 2997.2, 56403652)]
OUT = Path(__file__).parent / "research/top10"


def fetch_team(item):
    rank, team, rating, submission = item
    response = requests.post("https://www.kaggle.com/api/i/competitions.EpisodeService/ListEpisodes",
                             json={"submissionId": submission}, timeout=60)
    response.raise_for_status()
    data = response.json()
    (OUT / f"rank{rank}_episodes.json").write_text(json.dumps(data), encoding="utf-8")
    rows = []
    for e in data["episodes"]:
        if e.get("state") != "COMPLETED" or len(e.get("agents", [])) != 2:
            continue
        own = next((a for a in e["agents"] if a["submissionId"] == submission), None)
        if own is None or all(a["submissionId"] == submission for a in e["agents"]):
            continue
        rows.append({"rank": rank, "team": team, "rating_snapshot": rating,
                     "submission_id": submission, "episode_id": e["id"],
                     "seat": own.get("index", 0), "agents": e["agents"],
                     "time": e["endTime"], "split": "study" if not rows else "heldout"})
        if len(rows) == 3:
            break
    return rows


def download(eid):
    dest = OUT / f"{eid}.json.gz"
    if not dest.exists():
        response = requests.get(f"https://www.kaggle.com/competitions/episodes/{eid}/replay.json", timeout=90)
        response.raise_for_status()
        obj = response.json()
        assert len(obj["steps"]) == 720 and obj["info"]["EpisodeId"] == eid
        dest.write_bytes(gzip.compress(response.content))
    return eid


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        rows = [r for batch in pool.map(fetch_team, TOP) for r in batch]
        (OUT / "index.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
        for eid in pool.map(download, sorted({r["episode_id"] for r in rows})):
            print("Downloaded", eid, flush=True)
