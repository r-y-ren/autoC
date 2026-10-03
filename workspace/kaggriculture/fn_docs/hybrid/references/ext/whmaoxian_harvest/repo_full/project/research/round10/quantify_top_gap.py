"""Read-only economic ledger for frozen public replays, using the official engine.

The replay entry at index t contains the action executed between observations
t-1 and t.  We replay only the unit-action and market phases from the prior
observation; every resulting cash balance must match the public next state.
This avoids mistaking a requested market order for an executed transaction.
"""

from __future__ import annotations

import collections
import copy
import gzip
import json
import statistics
from pathlib import Path
from types import SimpleNamespace

from kaggle_environments.envs.kaggriculture import kaggriculture as engine


ROOT = Path(__file__).resolve().parent
STAGES = ((0, 5), (6, 10), (11, 15), (16, 20), (21, 25), (26, 29))
PRODUCTS = tuple(engine.PRODUCTS)


def stage_for_day(day: int) -> str:
    for lo, hi in STAGES:
        if lo <= day <= hi:
            return f"{lo}-{hi}"
    raise ValueError(day)


def asset_counts(farm: dict) -> tuple[dict[str, int], dict[str, int], int]:
    crops: collections.Counter[str] = collections.Counter()
    animals: collections.Counter[str] = collections.Counter()
    available = 0
    for row in farm["tiles"]:
        for tile in row:
            if tile == "LOCKED":
                continue
            available += 1
            if isinstance(tile, dict):
                if tile.get("crop"):
                    crops[tile["crop"]] += 1
                if tile.get("animal"):
                    animals[tile["animal"]] += 1
    return dict(crops), dict(animals), available


def replay_transition(prev: list[dict], current: list[dict], config: dict) -> tuple[list[dict], list[dict]]:
    """Replay physical+market phases and return exact executed transaction log.

    The official module is patched only inside this Python process and restored
    in finally.  The competition source and submission files stay untouched.
    """
    obs0 = prev[0]["observation"]
    farms = copy.deepcopy(obs0["farms"])
    market = copy.deepcopy(obs0["market"])
    privates = [copy.deepcopy(prev[i]["observation"]["private"]) for i in (0, 1)]
    actions = [current[i].get("action") or {} for i in (0, 1)]
    env = SimpleNamespace(configuration=SimpleNamespace(**config))
    states = [
        SimpleNamespace(
            observation=SimpleNamespace(farms=farms, market=market, private=privates[i]),
            action=actions[i],
        )
        for i in (0, 1)
    ]
    before_shed = [dict(private["shed"]) for private in privates]
    day = int(obs0["day"])
    board_size = int(config.get("boardSize", 10))
    turns_per_day = int(config.get("turnsPerDay", 24))
    shed_capacity = int(config.get("shedCapacity", 100))
    for seat in (0, 1):
        a = actions[seat]
        units = [a.get("farmer") or ["PASS"], *list(a.get("hands") or [])]
        demand = collections.Counter(x[1] for x in units if x and len(x) >= 2 and x[0] == "PLANT")
        blocked = {crop for crop, count in demand.items() if count > privates[seat]["seeds"].get(crop, 0)}
        for unit_index, unit_action in enumerate(units):
            if unit_action and len(unit_action) >= 2 and unit_action[0] == "PLANT" and unit_action[1] in blocked:
                unit_action = ["PASS"]
            engine._apply_unit_action(
                farms[seat], privates[seat], unit_index, unit_action,
                board_size, day, turns_per_day, shed_capacity,
            )
    delivered = []
    for seat in (0, 1):
        delivered.append({
            item: max(0, int(privates[seat]["shed"].get(item, 0) - before_shed[seat].get(item, 0)))
            for item in PRODUCTS
        })

    ledger: list[dict] = []
    by_farm = {id(farm): seat for seat, farm in enumerate(farms)}
    original_commit, original_hire, original_land = engine._commit_unit, engine._do_hire, engine._do_buy_land

    def commit(op, item, price, farm, private, market_state, shed_capacity=100):
        ok = original_commit(op, item, price, farm, private, market_state, shed_capacity)
        if ok:
            ledger.append({"seat": by_farm[id(farm)], "op": op, "item": item, "price": int(price)})
        return ok

    def hire(farm, private, size, mult=engine.FARM_HAND_COST_MULT):
        cash_before, hands_before = farm["money"], len(farm["hands"])
        original_hire(farm, private, size, mult)
        if len(farm["hands"]) > hands_before:
            ledger.append({"seat": by_farm[id(farm)], "op": "HIRE", "item": None, "price": cash_before - farm["money"]})

    def land(farm, size):
        cash_before, parcels_before = farm["money"], len(farm["unlocked_quadrants"])
        original_land(farm, size)
        if len(farm["unlocked_quadrants"]) > parcels_before:
            ledger.append({"seat": by_farm[id(farm)], "op": "BUY_LAND", "item": None, "price": cash_before - farm["money"]})

    try:
        engine._commit_unit, engine._do_hire, engine._do_buy_land = commit, hire, land
        engine._process_market(states, env)
    finally:
        engine._commit_unit, engine._do_hire, engine._do_buy_land = original_commit, original_hire, original_land

    for seat in (0, 1):
        expected = float(current[seat]["observation"]["farms"][seat]["money"])
        actual = float(farms[seat]["money"])
        if abs(actual - expected) > 1e-6:
            raise AssertionError((obs0["step"], seat, actual, expected))
    return ledger, delivered


def digest_game(game: dict, seat: int, identity: str) -> dict:
    steps = game["steps"]
    events: list[dict] = []
    delivered = collections.Counter()
    shops_by_day: dict[int, list[str]] = {}
    max_hands_by_day: dict[int, int] = collections.defaultdict(int)
    checkpoint = {}
    physical = collections.Counter()
    for t in range(1, len(steps)):
        prev, current = steps[t - 1], steps[t]
        ledger, newly_delivered = replay_transition(prev, current, game["configuration"])
        day = int(prev[seat]["observation"]["day"])
        shops_by_day[day] = list(prev[seat]["observation"]["town"]["unlocked_shops"])
        max_hands_by_day[day] = max(max_hands_by_day[day], len(prev[seat]["observation"]["farms"][seat]["hands"]))
        for event in ledger:
            if event["seat"] == seat:
                events.append({**event, "day": day})
        for product, count in newly_delivered[seat].items():
            delivered[(day, product)] += count
        action = current[seat].get("action") or {}
        for unit_action in [action.get("farmer") or []] + list(action.get("hands") or []):
            if unit_action:
                physical[(day, unit_action[0])] += 1
        if t in (1, 6 * 24, 11 * 24, 16 * 24, 21 * 24, 26 * 24, len(steps) - 1):
            obs = current[seat]["observation"]
            farm = obs["farms"][seat]
            crops, animals, available = asset_counts(farm)
            checkpoint[str(t)] = {
                "day": obs["day"], "hour": obs["hour"], "bank": farm["money"],
                "land": len(farm["unlocked_quadrants"]), "crops": crops, "animals": animals,
                "occupied_asset_tiles": sum(crops.values()) + sum(animals.values()),
                "available_tiles": available,
                "shed": obs["private"]["shed"],
                "shops": obs["town"]["unlocked_shops"],
            }
    # Include actual opening bank before the first transition.
    checkpoint["0"] = {"bank": steps[0][seat]["observation"]["farms"][seat]["money"]}
    stages = {}
    for lo, hi in STAGES:
        name = stage_for_day(lo)
        stage_events = [event for event in events if lo <= event["day"] <= hi]
        counts = collections.Counter(event["op"] for event in stage_events)
        cash = collections.Counter()
        value_by_product = collections.Counter()
        quantity_by_product = collections.Counter()
        matched_sales = 0
        for event in stage_events:
            sign = 1 if event["op"] == "SELL" else -1
            cash[event["op"]] += sign * event["price"]
            if event["op"] in ("SELL", "BUY_PRODUCT"):
                value_by_product[(event["op"], event["item"])] += event["price"]
                quantity_by_product[(event["op"], event["item"])] += 1
            if event["op"] == "SELL" and any(
                event["item"] in engine.SHOPS[shop] for shop in shops_by_day[event["day"]]
            ):
                matched_sales += event["price"]
        delivered_by_product = {
            product: sum(delivered[(day, product)] for day in range(lo, hi + 1))
            for product in PRODUCTS
        }
        stage_shops = shops_by_day.get(hi, [])
        gross_sales = sum(value for (op, _), value in value_by_product.items() if op == "SELL")
        stages[name] = {
            "net_bank_delta": sum(cash.values()), "sell_revenue": cash["SELL"],
            "buy_product_cost": -cash["BUY_PRODUCT"], "seed_cost": -cash["BUY_SEED"],
            "animal_cost": -cash["BUY_ANIMAL"], "land_cost": -cash["BUY_LAND"],
            "hire_cost": -cash["HIRE"], "executed_order_units": dict(counts),
            "sales_revenue_by_product": {product: value for (op, product), value in value_by_product.items() if op == "SELL"},
            "sales_units_by_product": {product: value for (op, product), value in quantity_by_product.items() if op == "SELL"},
            "buy_product_cost_by_product": {product: value for (op, product), value in value_by_product.items() if op == "BUY_PRODUCT"},
            "buy_product_units": {product: value for (op, product), value in quantity_by_product.items() if op == "BUY_PRODUCT"},
            "same_turn_physical_shed_deposits_excluding_night_drop": {product: n for product, n in delivered_by_product.items() if n},
            "matched_sales_share_at_execution": round(matched_sales / gross_sales, 4) if gross_sales else None,
            "shops_at_stage_end": stage_shops,
            "daily_max_hands_median": median([max_hands_by_day[day] for day in range(lo, hi + 1)]),
            "farm_action_requests": {op: sum(physical[(day, op)] for day in range(lo, hi + 1)) for op in ("PLANT", "HARVEST", "FEED", "CARE", "DROP")},
        }
    assert abs(sum(stage["net_bank_delta"] for stage in stages.values()) + checkpoint["0"]["bank"] - float(game["rewards"][seat])) < 1e-6
    return {"identity": identity, "seat": seat, "episode_id": int(game["info"]["EpisodeId"]),
            "reward": game["rewards"][seat], "rival_reward": game["rewards"][1 - seat],
            "shops_by_day": shops_by_day, "checkpoints": checkpoint, "stages": stages}


def median(values: list[float]) -> float:
    return round(float(statistics.median(values)), 2) if values else 0.0


def main() -> None:
    selection = json.loads((ROOT / "recent_episode_selection.json").read_text(encoding="utf-8"))["episodes"]
    keep = [row for row in selection if row["team"] in ("DSM", "Boey", "Vadim Vasilenko")]
    v9_selection = json.loads((ROOT / "v9_public_replay_selection.json").read_text(encoding="utf-8"))["episode_ids"]
    v9_meta = {int(row["episode_id"]): row for row in json.loads((ROOT / "v9_public_episode_audit_snapshot.json").read_text(encoding="utf-8"))["episodes_chronological"]}
    rows = []
    for row in keep:
        episode = row["episode_id"]
        with gzip.open(ROOT / "public_replays" / f"{episode}.json.gz", "rt", encoding="utf-8") as file:
            game = json.load(file)
        rows.append(digest_game(game, int(row["seat"]), row["team"]))
    for episode in v9_selection:
        meta = v9_meta[episode]
        if int(meta["opponent_submission_id"]) == 56493753:
            continue  # Self-play is not a separate opponent.
        with gzip.open(ROOT / "v9_public_replays" / f"{episode}.json.gz", "rt", encoding="utf-8") as file:
            game = json.load(file)
        rows.append(digest_game(game, int(meta["seat"]), "V9"))
    with gzip.open(ROOT / "public_replays" / "112446065.json.gz", "rt", encoding="utf-8") as file:
        head_to_head_game = json.load(file)
    head_to_head = {
        "Boey": digest_game(head_to_head_game, 0, "Boey"),
        "DSM": digest_game(head_to_head_game, 1, "DSM"),
    }
    (ROOT / "top_gap_head_to_head.json").write_text(json.dumps(head_to_head, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "top_gap_exact_ledger.json").write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    summary = {}
    for identity in ("DSM", "Boey", "Vadim Vasilenko", "V9"):
        pool = [row for row in rows if row["identity"] == identity]
        group = {"games": len(pool), "reward_median": median([row["reward"] for row in pool]), "stages": {}}
        for lo, hi in STAGES:
            name = stage_for_day(lo)
            group["stages"][name] = {
                key: median([row["stages"][name][key] for row in pool])
                for key in ("net_bank_delta", "sell_revenue", "buy_product_cost", "seed_cost", "animal_cost", "land_cost", "hire_cost", "daily_max_hands_median", "matched_sales_share_at_execution")
            }
        for t in (6 * 24, 11 * 24, 16 * 24, 21 * 24, 26 * 24, 719):
            group[f"checkpoint_{t}"] = {
                key: median([row["checkpoints"][str(t)][key] for row in pool])
                for key in ("bank", "land", "occupied_asset_tiles", "available_tiles")
            }
        summary[identity] = group
    (ROOT / "top_gap_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
