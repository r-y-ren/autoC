"""Metadata-locked, compact public-replay audit of V9's first episodes."""

from __future__ import annotations

from collections import Counter
import gzip
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
META = json.loads((ROOT / "v9_public_episode_audit_snapshot.json").read_text(encoding="utf-8"))
SELECTION = json.loads((ROOT / "v9_public_replay_selection.json").read_text(encoding="utf-8"))
CHECKPOINT_DAYS = (5, 10, 15, 20, 25, 29)


def tile_counts(farm: dict) -> tuple[dict, dict]:
    crops, animals = Counter(), Counter()
    for row in farm["tiles"]:
        for tile in row:
            if isinstance(tile, dict):
                if tile.get("crop"):
                    crops[tile["crop"]] += 1
                if tile.get("animal"):
                    animals[tile["animal"]] += 1
    return dict(crops), dict(animals)


def seat_digest(steps: list, seat: int) -> dict:
    plants, buys, sells, physical = Counter(), Counter(), Counter(), Counter()
    checkpoints = {}
    for step in steps:
        item = step[seat]
        obs, action = item["observation"], item.get("action") or {}
        for cmd in action.get("market") or []:
            if not cmd:
                continue
            if cmd[0] == "SELL":
                sells[cmd[1]] += cmd[2]
            if cmd[0] in ("BUY_ANIMAL", "BUY_SEED", "BUY_PRODUCT", "BUY_LAND", "HIRE"):
                buys[f"{cmd[0]}:{cmd[1] if len(cmd) > 1 else ''}"] += cmd[2] if len(cmd) > 2 else 1
        for cmd in [action.get("farmer") or []] + list(action.get("hands") or []):
            if cmd:
                physical[cmd[0]] += 1
                if cmd[0] == "PLANT":
                    plants[cmd[1]] += 1
        day, hour = int(obs["day"]), int(obs["hour"])
        if hour == 23 and day in CHECKPOINT_DAYS:
            farm = obs["farms"][seat]
            crops, animals = tile_counts(farm)
            checkpoints[str(day)] = {
                "cash_before_last_action": farm["money"],
                "land": len(farm["unlocked_quadrants"]),
                "hands": len(farm["hands"]),
                "crops": crops,
                "animals": animals,
                "shed": obs["private"].get("shed", {}),
                "market_prices": obs["market"]["prices"],
            }
    return {
        "requested_plants": dict(plants),
        "requested_buys": dict(buys),
        "requested_sells": dict(sells),
        "physical_actions": dict(physical),
        "checkpoints": checkpoints,
    }


def main() -> None:
    rows = {int(row["episode_id"]): row for row in META["episodes_chronological"]}
    output = []
    for eid in SELECTION["episode_ids"]:
        row = rows[eid]
        with gzip.open(ROOT / "v9_public_replays" / f"{eid}.json.gz", "rt", encoding="utf-8") as file:
            game = json.load(file)
        seat = int(row["seat"])
        assert int(game["info"]["EpisodeId"]) == eid
        assert int(game["rewards"][seat]) == int(row["our_reward"])
        output.append({
            "episode_id": eid,
            "seed": game["info"].get("seed"),
            "metadata": row,
            "v9": seat_digest(game["steps"], seat),
            "rival": seat_digest(game["steps"], 1 - seat),
        })
    path = ROOT / "v9_public_replay_digest.json"
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    for x in output:
        print(x["episode_id"], x["seed"], x["metadata"]["margin"])
        for label in ("v9", "rival"):
            d = x[label]
            checkpoints = d["checkpoints"]
            cash = {k: int(v["cash_before_last_action"]) for k, v in checkpoints.items()}
            stocks = {k: v["animals"] for k, v in checkpoints.items()}
            print(" ", label, "cash", cash, "animals", stocks, "plants", d["requested_plants"])
            print("   buys", {k: v for k, v in d["requested_buys"].items() if "ANIMAL" in k}, "sells", d["requested_sells"])


if __name__ == "__main__":
    main()
