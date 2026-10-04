"""Mechanism audit for the V9 step-zero wheat round trip.

This calls the official kaggriculture _process_market function on standalone
initial states.  Public opening actions are used only as fixed scenarios, not
as identity, episode, or seed features for any proposed agent.
"""

from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace

from kaggle_environments.envs.kaggriculture import kaggriculture as engine


ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "research" / "round10"
V9 = ROOT / "submissions" / "release_v9" / "main.py"
V9_SHA256 = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"
assert hashlib.sha256(V9.read_bytes()).hexdigest() == V9_SHA256

CHOICES = tuple((buy, buy - 5) for buy in range(5, 41, 5))


def own_action(buy: int, sell: int):
    orders = [["BUY_PRODUCT", "WHEAT", buy]]
    if sell:
        orders.append(["SELL", "WHEAT", sell])
    orders.append(["BUY_SEED", "WHEAT", 1])
    return {"farmer": ["PASS"], "hands": [], "market": orders}


def settle(my_action, rival_action, my_seat: int, config=None):
    config = config or {}
    board = int(config.get("boardSize", 10))
    cash = float(config.get("startingMoney", 3000))
    market = engine._new_market()
    farms = [engine._new_farm(board, cash) for _ in range(2)]
    privates = [engine._new_private() for _ in range(2)]
    actions = [None, None]
    actions[my_seat], actions[1 - my_seat] = my_action, rival_action
    states = [
        SimpleNamespace(
            action=actions[i],
            observation=SimpleNamespace(market=market, farms=farms, private=privates[i]),
        )
        for i in range(2)
    ]
    engine._process_market(states, SimpleNamespace(configuration=config))
    return {
        "own_cash": farms[my_seat]["money"],
        "rival_cash": farms[1 - my_seat]["money"],
        "margin_cash": farms[my_seat]["money"] - farms[1 - my_seat]["money"],
        "own_wheat": privates[my_seat]["shed"]["WHEAT"],
        "own_seed": privates[my_seat]["seeds"]["WHEAT"],
        "market_wheat_inventory": market["inventory"]["WHEAT"],
    }


def public_scenarios():
    selection = json.loads((RESEARCH / "recent_episode_selection.json").read_text(encoding="utf-8"))
    out = []
    for entry in selection["episodes"]:
        episode = entry["episode_id"]
        path = RESEARCH / "public_replays" / f"{episode}.json.gz"
        with gzip.open(path, "rt", encoding="utf-8") as f:
            replay = json.load(f)
        assert len(replay["steps"]) > 1
        assert replay["configuration"].get("marketParams") in ({}, None)
        seat = int(entry["seat"])
        action = replay["steps"][1][seat]["action"]
        assert isinstance(action.get("market"), list)
        out.append(
            {
                "label": f"{entry['team']}@{episode}",
                "team": entry["team"],
                "episode_id": episode,
                "replay_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "rival_action": action,
                "config": replay["configuration"],
                "source_seat": seat,
                "kind": "public",
            }
        )
    return out


def pressure_scenarios():
    out = []
    for qty in (0, 3, 5, 10, 15, 20, 30, 50):
        orders = [["BUY_PRODUCT", "WHEAT", qty]] if qty else []
        out.append(
            {
                "label": f"pure_buy_{qty}",
                "rival_action": {"market": orders},
                "config": {},
                "kind": "pressure",
            }
        )
    for buy, sell in ((10, 10), (10, 5), (15, 10), (20, 15), (30, 25)):
        out.append(
            {
                "label": f"wash_{buy}_{sell}",
                "rival_action": {
                    "market": [["BUY_PRODUCT", "WHEAT", buy], ["SELL", "WHEAT", sell]]
                },
                "config": {},
                "kind": "pressure",
            }
        )
    for qty in (3, 5, 10, 20, 30):
        out.append(
            {
                "label": f"cow_then_buy_{qty}",
                "rival_action": {
                    "market": [["BUY_ANIMAL", "COW", 1], ["BUY_PRODUCT", "WHEAT", qty]]
                },
                "config": {},
                "kind": "pressure",
            }
        )
    return out


def main():
    scenarios = public_scenarios() + pressure_scenarios()
    rows = []
    for scenario in scenarios:
        for seat in (0, 1):
            outcomes = {}
            for buy, sell in CHOICES:
                outcomes[f"{buy}/{sell}"] = settle(
                    own_action(buy, sell), scenario["rival_action"], seat, scenario["config"]
                )
                assert outcomes[f"{buy}/{sell}"]["own_wheat"] == 5
                assert outcomes[f"{buy}/{sell}"]["own_seed"] == 1
            base = outcomes["20/15"]
            deltas = {
                choice: {
                    "own_cash": value["own_cash"] - base["own_cash"],
                    "margin_cash": value["margin_cash"] - base["margin_cash"],
                }
                for choice, value in outcomes.items()
            }
            rows.append(
                {
                    "scenario": {k: v for k, v in scenario.items() if k != "config"},
                    "my_seat": seat,
                    "outcomes": outcomes,
                    "deltas_vs_v9": deltas,
                }
            )

    summary = {}
    for kind in ("public", "pressure"):
        subset = [r for r in rows if r["scenario"]["kind"] == kind]
        summary[kind] = {"rows": len(subset), "choices": {}}
        for buy, sell in CHOICES:
            choice = f"{buy}/{sell}"
            if choice == "20/15":
                continue
            cash = [r["deltas_vs_v9"][choice]["own_cash"] for r in subset]
            margin = [r["deltas_vs_v9"][choice]["margin_cash"] for r in subset]
            summary[kind]["choices"][choice] = {
                "own_cash_min": min(cash),
                "own_cash_max": max(cash),
                "own_cash_mean": sum(cash) / len(cash),
                "cash_better": sum(d > 0 for d in cash),
                "cash_equal": sum(d == 0 for d in cash),
                "cash_worse": sum(d < 0 for d in cash),
                "margin_min": min(margin),
                "margin_max": max(margin),
                "margin_mean": sum(margin) / len(margin),
            }
    output = {"v9_sha256": V9_SHA256, "choices": CHOICES, "summary": summary, "rows": rows}
    target = RESEARCH / "opening_trade_model_results.json"
    target.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2))
    print(target)


if __name__ == "__main__":
    main()
