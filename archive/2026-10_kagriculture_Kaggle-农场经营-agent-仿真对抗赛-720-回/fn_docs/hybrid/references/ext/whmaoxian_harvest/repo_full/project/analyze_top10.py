"""Summarize visible farm development in the ten study episodes."""
from collections import Counter
import gzip
import json
from pathlib import Path

root = Path(__file__).parent / "research/top10"
rows = []
for r in json.loads((root / "index.json").read_text()):
    if r["split"] != "study":
        continue
    d = json.loads(gzip.decompress((root / f"{r['episode_id']}.json.gz").read_bytes()))
    p = r["seat"]
    snapshots = []
    for t in (24, 144, 240, 480, 719):
        f = d["steps"][t][p]["observation"]["farms"][p]
        counts = Counter(x.get("animal") or x.get("crop") or x.get("kind")
                         for row in f["tiles"] for x in row if isinstance(x, dict))
        snapshots.append({"step": t, "money": f["money"], "land": len(f["unlocked_quadrants"]),
                          "hands": len(f["hands"]), "counts": dict(counts)})
    rows.append({**r, "shops": d["steps"][-1][p]["observation"]["town"],
                 "snapshots": snapshots,
                 "opening": [step[p]["action"]["market"] for step in d["steps"][1:4]]})
    print(r["rank"], r["team"], snapshots[2], d["rewards"][p])
(root / "production_summary.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
