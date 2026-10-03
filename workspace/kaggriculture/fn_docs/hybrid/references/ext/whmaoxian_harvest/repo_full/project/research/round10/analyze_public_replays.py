"""Describe public replay behavior without fitting a strategy to episode IDs."""

from __future__ import annotations

import collections
import gzip
import itertools
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CHECKPOINT_DAYS = (0, 5, 10, 15, 20, 25, 29)


def compact_dict(counter: collections.Counter) -> dict:
    return {str(key): value for key, value in counter.most_common()}


def summarize(row: dict) -> dict:
    eid = row["episode_id"]
    game = json.load(gzip.open(ROOT / "public_replays" / f"{eid}.json.gz", "rt", encoding="utf-8"))
    seat = int(row["seat"])
    markets = collections.Counter()
    buys = collections.Counter()
    sells = collections.Counter()
    planting = collections.Counter()
    first_buy = {}
    sold_by_day = collections.defaultdict(collections.Counter)
    planted_by_day = collections.defaultdict(collections.Counter)
    purchased_by_day = collections.defaultdict(collections.Counter)
    actor_actions = collections.Counter()
    hand_actions = collections.Counter()
    checkpoints = {}
    first_shops = {}

    for step in game["steps"]:
        item = step[seat]
        obs = item["observation"]
        action = item.get("action") or {}
        day, hour = int(obs["day"]), int(obs["hour"])
        for shop in obs["town"]["unlocked_shops"]:
            first_shops.setdefault(shop, day)
        for cmd in action.get("market") or []:
            if not cmd:
                continue
            op = cmd[0]
            markets[op] += 1
            if op in ("BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT"):
                buys[(op, cmd[1])] += cmd[2]
                first_buy.setdefault(f"{op}:{cmd[1]}", [day, hour])
                purchased_by_day[day][(op, cmd[1])] += cmd[2]
            elif op == "SELL":
                sells[cmd[1]] += cmd[2]
                sold_by_day[day][cmd[1]] += cmd[2]
        for cmd in [action.get("farmer") or []] + list(action.get("hands") or []):
            if not cmd:
                continue
            if cmd is action.get("farmer"):
                actor_actions[cmd[0]] += 1
            else:
                hand_actions[cmd[0]] += 1
            if cmd[0] == "PLANT":
                planting[cmd[1]] += 1
                planted_by_day[day][cmd[1]] += 1
        if hour == 23 and day in CHECKPOINT_DAYS:
            farm = obs["farms"][seat]
            crops = collections.Counter()
            animals = collections.Counter()
            for tile_row in farm["tiles"]:
                for tile in tile_row:
                    if not isinstance(tile, dict):
                        continue
                    if tile.get("crop"):
                        crops[tile["crop"]] += 1
                    if tile.get("animal"):
                        animals[tile["animal"]] += 1
            checkpoints[str(day)] = {
                "money_before_last_action": farm["money"],
                "land_quadrants": len(farm["unlocked_quadrants"]),
                "hands": len(farm["hands"]),
                "crops": compact_dict(crops),
                "animals": compact_dict(animals),
                "shed": obs["private"].get("shed", {}),
                "shops_unlocked": list(obs["town"]["unlocked_shops"]),
            }
    return {
        **row,
        "seed": game["info"].get("seed"),
        "first_shops": first_shops,
        "market_action_count": compact_dict(markets),
        "requested_buys": {f"{a}:{b}": qty for (a, b), qty in buys.most_common()},
        "first_buys_day_hour": first_buy,
        "requested_sells": compact_dict(sells),
        "requested_plants": compact_dict(planting),
        "purchased_by_day": {
            str(day): {f"{op}:{product}": q for (op, product), q in cnt.items()}
            for day, cnt in purchased_by_day.items()
        },
        "sold_by_day": {str(day): compact_dict(cnt) for day, cnt in sold_by_day.items()},
        "planted_by_day": {str(day): compact_dict(cnt) for day, cnt in planted_by_day.items()},
        "farmer_actions": compact_dict(actor_actions),
        "hand_actions": compact_dict(hand_actions),
        "checkpoints": checkpoints,
    }


def main() -> None:
    selection = json.loads((ROOT / "recent_episode_selection.json").read_text(encoding="utf-8"))["episodes"]
    summaries = [summarize(row) for row in selection]
    (ROOT / "recent_replay_actions.json").write_text(
        json.dumps(summaries, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    # 112446065 was already selected through DSM's latest-four list. Inspect
    # the other seat too, so cash comparisons use precisely the same game.
    head_to_head = summarize(
        {
            "team": "Boey",
            "rank_at_capture": 2,
            "submission_id": 56484772,
            "episode_id": 112446065,
            "end_time": "2026-09-23T12:25:35.709751500Z",
            "seat": 0,
            "reward": 136906,
            "opponent_submission_id": 56468867,
            "opponent_reward": 127039,
        }
    )
    (ROOT / "boey_dsm_headtohead_actions.json").write_text(
        json.dumps(head_to_head, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    action_sequences = {}
    for item in selection:
        key = (item["team"], item["episode_id"])
        replay = json.load(
            gzip.open(ROOT / "public_replays" / f"{item['episode_id']}.json.gz", "rt", encoding="utf-8")
        )
        action_sequences[key] = [step[item["seat"]]["action"] for step in replay["steps"]]
    similarity = {}
    for left, right in itertools.combinations(
        ("DSM", "Vadim Vasilenko", "Boey"), 2
    ):
        pairs = [
            (action_sequences[a], action_sequences[b])
            for a in action_sequences if a[0] == left
            for b in action_sequences if b[0] == right
        ]
        prefixes = []
        day_equal = {}
        for seq_a, seq_b in pairs:
            equal = [a == b for a, b in zip(seq_a, seq_b)]
            prefixes.append(next((i for i, same in enumerate(equal) if not same), len(equal)))
            for day in (0, 1, 2, 3, 5, 10, 20, 29):
                day_equal[day] = day_equal.get(day, 0) + sum(equal[day * 24 : (day + 1) * 24])
        similarity[f"{left} vs {right}"] = {
            "pair_count": len(pairs),
            "first_different_action_index_min": min(prefixes),
            "first_different_action_index_max": max(prefixes),
            "day_exact_action_fraction": {
                str(day): matches / (len(pairs) * 24) for day, matches in day_equal.items()
            },
        }
    (ROOT / "opening_similarity.json").write_text(
        json.dumps(similarity, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    for item in summaries:
        print(
            item["team"], item["episode_id"],
            "W" if item["reward"] > item["opponent_reward"] else "L",
            "plant requests", item["requested_plants"],
            "animal requests", {k: v for k, v in item["requested_buys"].items() if "ANIMAL" in k},
            "sell requests", item["requested_sells"],
            flush=True,
        )


if __name__ == "__main__":
    main()
