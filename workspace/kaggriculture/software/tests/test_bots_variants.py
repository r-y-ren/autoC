"""Unit + contract tests for the m1 wave-2 strong opponents.

Each new opponent must (a) emit legal actions on real engine observations,
(b) be deterministic, (c) actually express its strategy identity on
synthetic mid-game observations (gate/hoard/expand logic), and (d) survive
a short real episode.  Strength itself (>=50% vs the frozen weak pool) is
certified by scripts/check_opponent_strength.py, not by these unit tests
(full-length episodes are too slow for pytest).
"""

import json

import pytest

from kgenv.arena import load_submission_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.gym_env import KaggricultureGym

LEGAL_UNIT_OPS = {"NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST",
                  "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "FEED",
                  "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP", "PLACE",
                  "PASS"}

NEW_BOTS = {
    "cow_baron": cow_baron_agent,
    "melon_hoarder": melon_hoarder_agent,
    "expansionist": expansionist_agent,
}


def first_obs(player=0, seed=5):
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    return env.reset(seed=seed)


def check_action_schema(action):
    assert isinstance(action, dict), action
    assert set(action) <= {"farmer", "hands", "market"}
    farmer = action.get("farmer", ["PASS"])
    assert isinstance(farmer, list) and farmer, farmer
    assert farmer[0] in LEGAL_UNIT_OPS, farmer
    for h in action.get("hands", []):
        assert isinstance(h, list) and h and h[0] in LEGAL_UNIT_OPS, h
    market = action.get("market", [])
    assert isinstance(market, list) and len(market) <= 10
    for o in market:
        assert isinstance(o, list) and o[0] in {
            "BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL", "HIRE",
            "BUY_LAND"}, o


def synth_obs(day=0, hour=0, money=3000.0, tiles=None, shed=None, seeds=None,
              prices=None, hands=(), farmer=(4, 4), inventories=None):
    """A minimal 10x10 observation: NW unlocked, everything else LOCKED."""
    if tiles is None:
        tiles = [[None if (x < 5 and y < 5) else "LOCKED" for x in range(10)]
                 for y in range(10)]
    private = {
        "shed": dict({"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0,
                      "MELON": 0, "EGG": 0, "MILK": 0, "WOOL": 0,
                      "FERTILIZER": 0, "GOOSE": 0, "COW": 0, "SHEEP": 0},
                     **(shed or {})),
        "seeds": dict({"WHEAT": 0, "CARROT": 0, "TOMATO": 0, "STRAWBERRY": 0,
                       "MELON": 0}, **(seeds or {})),
        "inventories": inventories or [{} for _ in range(1 + len(hands))],
    }
    base_prices = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
                   "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
                   "FERTILIZER": 100}
    base_prices.update(prices or {})
    return {
        "player": 0,
        "day": day, "hour": hour,
        "farms": [{"money": money, "tiles": tiles, "farmer": list(farmer),
                   "hands": [list(h) for h in hands],
                   "unlocked_quadrants": ["NW"], "hires_today": 0}],
        "private": private,
        "market": {"prices": base_prices},
    }


# ---------------------------------------------------------------- contract

@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_new_bot_legal_action_on_real_obs(name):
    obs = json.loads(json.dumps(first_obs()))
    check_action_schema(NEW_BOTS[name](obs))


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_new_bot_deterministic(name):
    obs = json.loads(json.dumps(first_obs(seed=9)))
    assert NEW_BOTS[name](obs) == NEW_BOTS[name](obs)


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_new_bot_never_crashes_on_hostile_obs(name):
    # truncated / adversarial observation -> must still return a legal action
    check_action_schema(NEW_BOTS[name]({"player": 0, "farms": []}))
    weird = synth_obs(tiles=[["LOCKED"] * 10 for _ in range(10)])
    check_action_schema(NEW_BOTS[name](weird))


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_new_bot_short_episode_done(name):
    from kgenv.engine import run_episode
    res = run_episode(NEW_BOTS[name], "starter", seed=13, episode_steps=72)
    assert res["statuses"] == ["DONE", "DONE"]
    assert all(r > 0 for r in res["rewards"])


# ---------------------------------------------------------------- cow_baron

def test_cow_baron_buys_cows_day0():
    act = cow_baron_agent(synth_obs(money=3000))
    assert ["BUY_ANIMAL", "COW", 1] in act["market"]


def test_cow_baron_feeds_via_shed_pickup():
    tiles = [[None if (x < 5 and y < 5) else "LOCKED" for x in range(10)]
             for y in range(10)]
    tiles[3][3] = {"kind": "PASTURE", "animal": "COW", "placed_day": 5,
                   "yield_units": 0, "consecutive_unfed": 0,
                   "fed_today": False, "cared_today": False,
                   "fertilizer_available": False}
    obs = synth_obs(day=10, tiles=tiles, shed={"WHEAT": 5}, farmer=(4, 4))
    act = cow_baron_agent(obs)
    assert act["farmer"][0] == "PICKUP" and act["farmer"][1] == "WHEAT"


def test_cow_baron_milk_gate_holds_and_releases():
    tiles = [[None if (x < 5 and y < 5) else "LOCKED" for x in range(10)]
             for y in range(10)]
    def sell_orders(price):
        obs = synth_obs(day=12, tiles=tiles, shed={"MILK": 8},
                        prices={"MILK": price})
        return [o for o in cow_baron_agent(obs)["market"]
                if o[0] == "SELL" and o[1] == "MILK"]
    assert sell_orders(100) == []                      # below gate: hoard
    assert sell_orders(150) == [["SELL", "MILK", 8]]   # above gate: tranche


def test_cow_baron_liquidates_on_last_day():
    obs = synth_obs(day=29, shed={"MILK": 9, "WHEAT": 4, "FERTILIZER": 3})
    act = cow_baron_agent(obs)
    sells = {o[1]: o[2] for o in act["market"] if o[0] == "SELL"}
    assert sells.get("MILK") == 9 and sells.get("FERTILIZER") == 3
    assert not any(o[0] in ("BUY_ANIMAL", "BUY_SEED", "HIRE")
                   for o in act["market"])


# ------------------------------------------------------------ melon_hoarder

def test_melon_hoarder_buys_wave1_seeds():
    act = melon_hoarder_agent(synth_obs(money=3000))
    seed_orders = [o for o in act["market"] if o[0] == "BUY_SEED"
                   and o[1] == "MELON"]
    assert seed_orders and sum(o[2] for o in seed_orders) >= 12


def test_melon_hoarder_hoards_below_gate_dumps_above():
    def sell_orders(price):
        obs = synth_obs(day=14, shed={"MELON": 30},
                        prices={"MELON": price})
        return [o for o in melon_hoarder_agent(obs)["market"]
                if o[0] == "SELL" and o[1] == "MELON"]
    assert sell_orders(150) == []                       # hoard below gate
    assert sell_orders(200) == [["SELL", "MELON", 20]]  # bounded tranche


def test_melon_hoarder_no_second_wave_when_price_collapsed():
    # day 14, melon price crashed to 90 -> no wave-2 seed buy
    obs = synth_obs(day=14, money=5000, prices={"MELON": 90})
    act = melon_hoarder_agent(obs)
    assert not any(o[0] == "BUY_SEED" and o[1] == "MELON"
                   for o in act["market"])


# ------------------------------------------------------------ expansionist

def test_expansionist_buys_land_when_saturated_and_rich():
    tiles = [[None if (x < 5 and y < 5) else "LOCKED" for x in range(10)]
             for y in range(10)]
    for x, y in ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)):
        tiles[y][x] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 8,
                       "watered_today": False, "consecutive_unwatered": 0,
                       "yield_units": 1, "max_lifespan_step": 312,
                       "fertilized_until_day": -1}
    obs = synth_obs(day=8, hour=10, money=3000, tiles=tiles,
                    seeds={"WHEAT": 30})
    act = expansionist_agent(obs)
    assert ["BUY_LAND"] in act["market"]


def test_expansionist_holds_land_when_unsaturated():
    # same money but an empty farm (estate not planted) -> no land grab yet
    obs = synth_obs(day=2, hour=10, money=3000)
    act = expansionist_agent(obs)
    assert ["BUY_LAND"] not in act["market"]


def test_expansionist_buys_goose_for_court():
    obs = synth_obs(day=2, money=1200)
    act = expansionist_agent(obs)
    assert ["BUY_ANIMAL", "GOOSE", 1] in act["market"]


def test_expansionist_harvest_waits_for_age4_watering():
    tiles = [[None if (x < 5 and y < 5) else "LOCKED" for x in range(10)]
             for y in range(10)]
    tiles[0][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 4,
                   "watered_today": False, "consecutive_unwatered": 0,
                   "yield_units": 3, "max_lifespan_step": 216,
                   "fertilized_until_day": -1}
    # farmer standing on an age-4 unwatered tile in the morning: water wins
    # (harvest must not steal the last window watering)
    obs = synth_obs(day=8, hour=5, tiles=tiles, farmer=(0, 0))
    act = expansionist_agent(obs)
    assert act["farmer"] == ["WATER"]
