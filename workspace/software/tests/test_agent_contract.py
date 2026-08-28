"""Agent interface contract tests.

Validates the submittable main.py agent (and the local baselines) against
the official action schema, on a real engine observation, for both seats,
plus determinism and a short live episode (also through the gym wrapper).
"""

import json

import pytest

from kgenv.arena import load_submission_agent
from kgenv.bots.baseline import baseline_wheat_agent, greedy_carrot_agent
from kgenv.gym_env import KaggricultureGym

LEGAL_UNIT_OPS = {"NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST",
                  "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "FEED",
                  "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP", "PLACE",
                  "PASS"}
LEGAL_MARKET_OPS = {"BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL", "HIRE",
                    "BUY_LAND"}
CROPS = {"WHEAT", "CARROT", "TOMATO", "STRAWBERRY", "MELON"}


def first_obs(player=0, seed=5):
    """Grab a genuine initial observation from the official engine."""
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    obs = env.reset(seed=seed)
    return obs


def check_action_schema(action):
    assert isinstance(action, dict), action
    assert set(action) <= {"farmer", "hands", "market"}
    farmer = action.get("farmer", ["PASS"])
    assert isinstance(farmer, list) and farmer, farmer
    assert farmer[0] in LEGAL_UNIT_OPS, farmer
    if farmer[0] == "PLANT":
        assert farmer[1] in CROPS
    hands = action.get("hands", [])
    assert isinstance(hands, list)
    for h in hands:
        assert isinstance(h, list) and h and h[0] in LEGAL_UNIT_OPS, h
    market = action.get("market", [])
    assert isinstance(market, list) and len(market) <= 10
    for o in market:
        assert isinstance(o, list) and len(o) >= 1
        assert o[0] in LEGAL_MARKET_OPS, o
        if o[0] in ("BUY_SEED", "BUY_ANIMAL", "SELL", "BUY_PRODUCT"):
            assert len(o) == 3
            assert isinstance(o[2], (int, float)) and o[2] > 0
        if o[0] == "BUY_SEED":
            assert o[1] in CROPS


BOTS = {
    "submission": load_submission_agent(),
    "baseline_wheat": baseline_wheat_agent,
    "greedy_carrot": greedy_carrot_agent,
}


@pytest.mark.parametrize("name", sorted(BOTS))
def test_agent_returns_legal_action(name):
    obs = first_obs()
    action = BOTS[name](json.loads(json.dumps(obs)))
    check_action_schema(action)


@pytest.mark.parametrize("name", sorted(BOTS))
def test_agent_deterministic(name):
    obs = json.loads(json.dumps(first_obs(seed=9)))
    a1 = BOTS[name](obs)
    a2 = BOTS[name](obs)
    assert a1 == a2


def test_submission_agent_both_seats():
    # seat 1 observation: same schema, no crash
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    env.reset(seed=2)
    obs0 = json.loads(json.dumps(env._env.steps[-1][0]["observation"]))
    obs1 = json.loads(json.dumps(env._env.steps[-1][1]["observation"]))
    check_action_schema(BOTS["submission"](obs0))
    check_action_schema(BOTS["submission"](obs1))
    assert obs1["player"] == 1


def test_submission_short_episode_vs_starter():
    # a real short episode must complete without INVALID status
    from kgenv.engine import run_episode
    res = run_episode(BOTS["submission"], "starter", seed=13, episode_steps=72)
    assert res["statuses"] == ["DONE", "DONE"]
    assert all(r > 0 for r in res["rewards"])  # money never goes negative


def test_gym_wrapper_steps():
    env = KaggricultureGym(opponent="starter", episode_steps=48)
    obs = env.reset(seed=4)
    assert "farms" in obs
    terminated = False
    for _ in range(48):
        action = BOTS["submission"](json.loads(json.dumps(env.observation)))
        check_action_schema(action)
        obs, reward, terminated, info = env.step(action)
        if terminated:
            break
    assert info["day"] >= 1
    assert len(info["money"]) == 2
    assert isinstance(reward, float)
