"""Read-only audit of the frozen V9 technical games for capital timing.

This intentionally does not build a candidate: the proposed fourth-land and
extra-animal interventions have not passed a physical-activity dependency check.
"""

from __future__ import annotations

import collections
import gzip
import hashlib
import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "experiments" / "round9_market_slack.py"
RECORDS = ROOT / "submissions" / "candidate_v9" / "validation" / "real-observations.jsonl.gz"
EXPECTED_SHA256 = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
DAYS = (4, 5, 6, 7, 8, 9, 10, 11, 15, 18)


def main() -> None:
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    assert digest == EXPECTED_SHA256, (digest, EXPECTED_SHA256)
    games: dict[int, list[dict]] = collections.defaultdict(list)
    with gzip.open(RECORDS, "rt", encoding="utf-8") as handle:
        for line in handle:
            row = json.loads(line)
            games[int(row["game_index"])].append(row)
    assert len(games) == 2
    result = {
        "source_path": str(SOURCE.relative_to(ROOT)),
        "source_sha256": digest,
        "observations_path": str(RECORDS.relative_to(ROOT)),
        "games": [],
    }
    namespace = runpy.run_path(str(SOURCE))
    route_land = {}
    for route_id, tape in namespace["_IMPL"].chassis.routes.items():
        route_land[str(route_id)] = [
            step for step, action in enumerate(tape)
            if any(order and order[0] == "BUY_LAND" for order in action.get("market") or [])
        ]
    result["route_count"] = len(route_land)
    result["route_land_timelines"] = route_land
    for game_index, rows in sorted(games.items()):
        rows.sort(key=lambda r: int(r["obs"]["step"]))
        land = []
        for row in rows:
            obs = row["obs"]
            action = row["expected_action"]
            farm = obs["farms"][int(obs["player"])]
            if any(order and order[0] == "BUY_LAND" for order in action.get("market") or []):
                land.append(
                    {
                        "step": int(obs["step"]),
                        "day": int(obs["day"]),
                        "hour": int(obs["hour"]),
                        "quadrants_before": len(farm["unlocked_quadrants"]),
                        "money_before": farm["money"],
                        "market_orders": action["market"],
                    }
                )
        checkpoints = {}
        for day in DAYS:
            obs = next(row["obs"] for row in rows if int(row["obs"]["step"]) == day * 24 + 23)
            farm = obs["farms"][int(obs["player"])]
            animals = collections.Counter(
                tile["animal"]
                for tile_row in farm["tiles"]
                for tile in tile_row
                if isinstance(tile, dict) and tile.get("animal")
            )
            crops = collections.Counter(
                tile["crop"]
                for tile_row in farm["tiles"]
                for tile in tile_row
                if isinstance(tile, dict) and tile.get("crop")
            )
            checkpoints[str(day)] = {
                "money": farm["money"],
                "quadrants": len(farm["unlocked_quadrants"]),
                "hands": len(farm["hands"]),
                "animals_on_land": dict(animals),
                "crops_on_land": dict(crops),
            }
        result["games"].append(
            {
                "game_index": game_index,
                "seed": rows[0]["seed"],
                "observations": len(rows),
                "buy_land_requests": land,
                "checkpoints": checkpoints,
            }
        )
    output = Path(__file__).with_name("early_capital_evidence.json")
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
