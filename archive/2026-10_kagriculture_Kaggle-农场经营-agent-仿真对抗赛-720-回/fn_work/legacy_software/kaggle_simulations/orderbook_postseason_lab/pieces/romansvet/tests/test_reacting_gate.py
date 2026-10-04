import json
import sys
from pathlib import Path
from types import SimpleNamespace


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "S" / "actionrl"))

import eval_vs_baselines as ev
from live_manifest import load_band3_manifest
from town_inject import load_schedule


def _state(day, shops):
    return SimpleNamespace(observation={
        "day": day, "step": day * 24,
        "town": {"unlocked_shops": list(shops)},
    })


def test_explicit_town_is_the_exact_tape_schedule():
    rows = load_band3_manifest(
        ROOT / "S/actionrl/live250_ids.txt",
        ROOT / "S/band3/live250_epseat.txt",
        ROOT / "S/band3/live250_epseat.txt.seeds",
        ROOT / "S/winjudge/town_live250.json",
        ROOT / "artifacts/tape_actions_town",
    )
    board = rows[0]
    registry = load_schedule(ROOT / "S/winjudge/town_live250.json", board.ep)
    assert tuple(map(tuple, registry)) == board.town


def test_town_prefix_assertion_accepts_exact_schedule_and_rejects_drift():
    schedule = ((2, "BAKERY"), (4, "YARN_STORE"))
    exact = [[_state(0, []), _state(0, [])],
             [_state(2, ["BAKERY"]), _state(2, ["BAKERY"])],
             [_state(5, ["BAKERY", "YARN_STORE"]),
              _state(5, ["BAKERY", "YARN_STORE"])]]
    ev._assert_town_prefix(exact, schedule)
    exact[-1][1].observation["town"]["unlocked_shops"] = ["BAKERY"]
    try:
        ev._assert_town_prefix(exact, schedule)
    except AssertionError as exc:
        assert "town prefix mismatch" in str(exc)
    else:
        raise AssertionError("town drift was not detected")
