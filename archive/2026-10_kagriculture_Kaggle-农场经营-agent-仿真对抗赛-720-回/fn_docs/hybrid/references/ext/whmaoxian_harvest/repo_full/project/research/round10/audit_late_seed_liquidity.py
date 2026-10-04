"""Read-only proof that V9's final day-zero wheat seeds fund next-step plants."""

from __future__ import annotations

import gzip
import hashlib
import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
V9 = ROOT / "submissions" / "release_v9" / "main.py"
REPLAY = ROOT / "research" / "round10" / "v9_public_replays" / "112476879.json.gz"
OUT = ROOT / "research" / "round10" / "late_seed_liquidity_audit.json"
V9_SHA = "6b13532fbc2b55b59c6cae8ed8d5cd29fe82d18a7d7e044ed130217e3d1c09d3"


def plants(action, crop):
    commands = [action.get("farmer"), *(action.get("hands") or [])]
    return sum(c == ["PLANT", crop] for c in commands)


def buys(action, crop):
    return sum(o[2] for o in action.get("market", []) if o[:2] == ["BUY_SEED", crop])


def main():
    assert hashlib.sha256(V9.read_bytes()).hexdigest() == V9_SHA
    namespace = runpy.run_path(str(V9))
    routes = namespace["_IMPL"].chassis.routes
    route_audit = []
    for route, tape in routes.items():
        row = {
            "route": route,
            "step19_buy_seed_wheat": buys(tape[19], "WHEAT"),
            "step20_plant_wheat": plants(tape[20], "WHEAT"),
            "step20_buy_seed_wheat": buys(tape[20], "WHEAT"),
            "step21_plant_wheat": plants(tape[21], "WHEAT"),
            "step21_buy_seed_wheat": buys(tape[21], "WHEAT"),
            "step22_to23_buy_seed_wheat": sum(buys(tape[t], "WHEAT") for t in (22, 23)),
            "step24_hire_requests": sum(o == ["HIRE"] for o in tape[24].get("market", [])),
        }
        assert tuple(row.values())[1:] == (1, 1, 2, 2, 0, 0, 3)
        route_audit.append(row)

    with gzip.open(REPLAY, "rt", encoding="utf-8") as f:
        replay = json.load(f)
    assert replay["info"]["seed"] == 1392039591
    state = []
    for step in (19, 20, 21, 22, 23, 24):
        before = replay["steps"][step][0]["observation"]
        after = replay["steps"][step + 1][0]["observation"]
        action = replay["steps"][step + 1][0]["action"]
        state.append(
            {
                "step": step,
                "before_seeds": before["private"]["seeds"]["WHEAT"],
                "plant_wheat_requests": plants(action, "WHEAT"),
                "buy_seed_wheat_requests": buys(action, "WHEAT"),
                "after_seeds": after["private"]["seeds"]["WHEAT"],
                "before_cash": before["farms"][0]["money"],
                "after_cash": after["farms"][0]["money"],
            }
        )
    assert state[1]["before_seeds"] == 1 and state[1]["after_seeds"] == 2
    assert state[2]["before_seeds"] == 2 and state[2]["after_seeds"] == 0
    assert state[4]["after_cash"] == 1

    data = {
        "v9_sha256": V9_SHA,
        "route_count": len(route_audit),
        "all_routes_same_late_seed_sequence": True,
        "representative_route": route_audit[0],
        "replay_episode": 112476879,
        "replay_compressed_sha256": hashlib.sha256(REPLAY.read_bytes()).hexdigest(),
        "replay_trace": state,
        "counterfactual_if_step20_buy2_reduced_to_buy1": {
            "step21_wheat_seeds_at_start": 1,
            "step21_wheat_plant_requests": 2,
            "official_atomic_plant_rule_blocks_all_requests": True,
            "cash_saved": 10,
        },
    }
    OUT.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
