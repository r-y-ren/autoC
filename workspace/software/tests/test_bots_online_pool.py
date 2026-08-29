"""Unit + contract tests for the m2 online-style opponents (campaign III)
and the r3-1 scale_ranch next-band opponent.

Two layers, mirroring test_bots_variants.py:

(a) generic contract tests -- legal actions on real engine observations,
    determinism, hostile-observation safety, short real episode;
(b) parameter-discipline tests -- each bot's observable behaviour must match
    the SAME-PLAYER >=3-game consistent profile parameters it was built from
    (hire cadence, rotation triggers, external-feed price guardrails, sell
    gates, endgame liquidation window, quadrant expansion timing), plus the
    exploratory flag discipline for the 2-game near-band bot.  scale_ranch
    knobs cite >=3-game top-20 findings that cross-validate the round-2
    winners' trajectories (r3-1 deep dive).

Strength itself (>=50% vs the frozen weak pool) is certified by
scripts/check_opponent_strength.py, not by these unit tests.
"""

import json

import pytest

from kgenv.bots.online_pool import (
    CROP_ROTATOR_PARAMS,
    NEAR_BAND_PARAMS,
    ONLINE_STYLE_OPPONENTS,
    SCALE_RANCH_PARAMS,
    SELF_FEED_RANCH_PARAMS,
    TEMPLATE_WHEAT_PARAMS,
    crop_rotator_agent,
    near_band_diversified_agent,
    scale_ranch_agent,
    self_feed_ranch_agent,
    template_wheat_agent,
)
from kgenv.gym_env import KaggricultureGym

LEGAL_UNIT_OPS = {"NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER", "HARVEST",
                  "FERTILIZE", "DIG", "BUILD_COOP", "BUILD_PASTURE", "FEED",
                  "CARE", "COLLECT_FERTILIZER", "PICKUP", "DROP", "PLACE",
                  "PASS"}

NEW_BOTS = {
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "near_band_diversified": near_band_diversified_agent,
    "scale_ranch": scale_ranch_agent,
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
              prices=None, hands=(), farmer=(4, 4), inventories=None,
              quads=("NW",)):
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
                   "unlocked_quadrants": list(quads), "hires_today": 0}],
        "private": private,
        "market": {"prices": base_prices},
    }


def three_quad_tiles():
    """NW + NE + SW unlocked (75 tiles), all empty."""
    return [[None if not (x >= 5 and y >= 5) else "LOCKED" for x in range(10)]
            for y in range(10)]


def market_orders(action, op):
    return [o for o in action["market"] if o[0] == op]


def seed_qty(action, crop):
    return sum(o[2] for o in market_orders(action, "BUY_SEED") if o[1] == crop)


# ---------------------------------------------------------------- contract

@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_online_bot_legal_action_on_real_obs(name):
    obs = json.loads(json.dumps(first_obs()))
    check_action_schema(NEW_BOTS[name](obs))


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_online_bot_deterministic(name):
    obs = json.loads(json.dumps(first_obs(seed=9)))
    assert NEW_BOTS[name](obs) == NEW_BOTS[name](obs)


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_online_bot_never_crashes_on_hostile_obs(name):
    check_action_schema(NEW_BOTS[name]({"player": 0, "farms": []}))
    weird = synth_obs(tiles=[["LOCKED"] * 10 for _ in range(10)])
    check_action_schema(NEW_BOTS[name](weird))


@pytest.mark.parametrize("name", sorted(NEW_BOTS))
def test_online_bot_short_episode_done(name):
    from kgenv.engine import run_episode
    res = run_episode(NEW_BOTS[name], "starter", seed=13, episode_steps=72)
    assert res["statuses"] == ["DONE", "DONE"]
    assert all(r > 0 for r in res["rewards"])


def test_online_style_registry_matches_bots_module():
    from kgenv.bots import ONLINE_STYLE_OPPONENTS as registry
    assert tuple(sorted(registry)) == tuple(sorted(NEW_BOTS))
    assert set(ONLINE_STYLE_OPPONENTS) == set(NEW_BOTS)


# ------------------------------------------------- exploratory flag discipline

def test_only_near_band_bot_carries_exploratory_params():
    assert NEAR_BAND_PARAMS["exploratory_params"] is True
    assert "2 games" in NEAR_BAND_PARAMS["provenance"] \
        or "2 games" in NEAR_BAND_PARAMS.get("exploratory_note", "")
    for params in (CROP_ROTATOR_PARAMS, TEMPLATE_WHEAT_PARAMS,
                   SELF_FEED_RANCH_PARAMS, SCALE_RANCH_PARAMS):
        assert params["exploratory_params"] is False


# ---------------------------------------------------------------- crop_rotator

def test_crop_rotator_hires_scale_with_quadrants():
    # 1 unlocked quadrant -> crew of 4 (Crop Dusta ramp 4/8/12)
    act = crop_rotator_agent(synth_obs(day=8, hands=()))
    assert market_orders(act, "HIRE")
    full = crop_rotator_agent(synth_obs(day=8, hands=[(0, 1)] * 4))
    assert not market_orders(full, "HIRE")
    # 3 quadrants -> crew of 12
    three = crop_rotator_agent(
        synth_obs(day=14, tiles=three_quad_tiles(), hands=(),
                  quads=("NW", "NE", "SW")))
    assert market_orders(three, "HIRE")


def test_crop_rotator_wheat_share_adapts_to_price():
    # 3 quadrants + full crew: high wheat price -> 0.62 share (seed deficit
    # beyond 30 seeds), low wheat price -> 0.22 share (deficit covered)
    dear = crop_rotator_agent(synth_obs(
        day=6, tiles=three_quad_tiles(), hands=[(0, 1)] * 11,
        quads=("NW", "NE", "SW"), seeds={"WHEAT": 30},
        prices={"WHEAT": 45, "STRAWBERRY": 10, "MELON": 10, "TOMATO": 10}))
    cheap = crop_rotator_agent(synth_obs(
        day=6, tiles=three_quad_tiles(), hands=[(0, 1)] * 11,
        quads=("NW", "NE", "SW"), seeds={"WHEAT": 30},
        prices={"WHEAT": 22, "STRAWBERRY": 10, "MELON": 10, "TOMATO": 10}))
    assert seed_qty(dear, "WHEAT") > 0
    assert seed_qty(cheap, "WHEAT") == 0


def test_crop_rotator_rotation_trigger_is_price_and_phase():
    # strawberry above its floor price -> in the rotation; below -> out
    dear = crop_rotator_agent(synth_obs(day=2, money=8000,
                                        prices={"STRAWBERRY": 200}))
    cheap = crop_rotator_agent(synth_obs(day=2, money=8000,
                                         prices={"STRAWBERRY": 40}))
    assert seed_qty(dear, "STRAWBERRY") > 0
    assert seed_qty(cheap, "STRAWBERRY") == 0
    # tomato is a late phase (day >= 15) even at a strong price
    early = crop_rotator_agent(synth_obs(day=10, money=8000,
                                         prices={"TOMATO": 120}))
    late = crop_rotator_agent(synth_obs(day=16, money=8000,
                                        prices={"TOMATO": 120}))
    assert seed_qty(early, "TOMATO") == 0
    assert seed_qty(late, "TOMATO") > 0


def test_crop_rotator_feed_guardrail():
    tiles = three_quad_tiles()
    tiles[3][3] = {"kind": "PASTURE", "animal": "COW", "placed_day": 2,
                   "yield_units": 0, "consecutive_unfed": 0,
                   "fed_today": False, "cared_today": False,
                   "fertilizer_available": False}
    dear = crop_rotator_agent(synth_obs(day=10, tiles=tiles,
                                        prices={"WHEAT": 50}))
    cheap = crop_rotator_agent(synth_obs(day=10, tiles=tiles,
                                         prices={"WHEAT": 38}))
    assert not [o for o in market_orders(dear, "BUY_PRODUCT")
                if o[1] == "WHEAT"]
    assert [o for o in market_orders(cheap, "BUY_PRODUCT") if o[1] == "WHEAT"]


def test_crop_rotator_milk_gate_holds_and_releases():
    def milk_sells(price):
        act = crop_rotator_agent(synth_obs(day=12, shed={"MILK": 8},
                                           prices={"MILK": price}))
        return [o for o in market_orders(act, "SELL") if o[1] == "MILK"]
    assert milk_sells(80) == []                       # below gate 100: hoard
    assert milk_sells(120) == [["SELL", "MILK", 8]]   # above gate: tranche


def test_crop_rotator_endgame_liquidation_window():
    act = crop_rotator_agent(synth_obs(
        day=28, shed={"MILK": 6, "WHEAT": 12, "STRAWBERRY": 5},
        prices={"MILK": 5, "WHEAT": 5, "STRAWBERRY": 5}))
    sells = {o[1]: o[2] for o in market_orders(act, "SELL")}
    assert sells.get("MILK") == 6 and sells.get("WHEAT") == 12
    assert sells.get("STRAWBERRY") == 5
    assert not [o for o in act["market"] if o[0] in
                ("HIRE", "BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "BUY_LAND")]


def test_crop_rotator_quadrant_expansion_timing():
    early = crop_rotator_agent(synth_obs(day=1, money=3000))
    assert not market_orders(early, "BUY_LAND")       # before min-day 4
    on_time = crop_rotator_agent(synth_obs(day=6, money=3000))
    assert market_orders(on_time, "BUY_LAND")         # NE ~day 5 (1000+350)


# ---------------------------------------------------------------- template_wheat

def test_template_wheat_share_is_locked_42_percent():
    dear = template_wheat_agent(synth_obs(
        day=6, tiles=three_quad_tiles(), hands=[(0, 1)] * 10,
        quads=("NW", "NE", "SW"), prices={"WHEAT": 45}))
    cheap = template_wheat_agent(synth_obs(
        day=6, tiles=three_quad_tiles(), hands=[(0, 1)] * 10,
        quads=("NW", "NE", "SW"), prices={"WHEAT": 18}))
    # the template's wheat field does not follow the price (locked 0.42)
    assert seed_qty(dear, "WHEAT") == seed_qty(cheap, "WHEAT")
    assert seed_qty(dear, "WHEAT") > 0


def test_template_wheat_fixed_feed_cadence_once_per_morning():
    tiles = three_quad_tiles()
    for x, y in ((2, 2), (2, 3), (3, 2)):
        tiles[y][x] = {"kind": "PASTURE", "animal": "COW", "placed_day": 2,
                       "yield_units": 0, "consecutive_unfed": 0,
                       "fed_today": False, "cared_today": False,
                       "fertilizer_available": False}
    dawn = template_wheat_agent(synth_obs(day=10, hour=0, tiles=tiles))
    buys = [o for o in market_orders(dawn, "BUY_PRODUCT") if o[1] == "WHEAT"]
    assert buys and buys[0][2] == 15                  # the fixed daily ration
    afternoon = template_wheat_agent(synth_obs(day=10, hour=8, tiles=tiles))
    assert not [o for o in market_orders(afternoon, "BUY_PRODUCT")
                if o[1] == "WHEAT"]


def test_template_wheat_dump_priced_strawberry_gate():
    def straw_sells(price):
        act = template_wheat_agent(synth_obs(day=12, shed={"STRAWBERRY": 20},
                                             prices={"STRAWBERRY": price}))
        return [o for o in market_orders(act, "SELL") if o[1] == "STRAWBERRY"]
    assert straw_sells(18) == []                      # below dump gate 22
    assert straw_sells(30) == [["SELL", "STRAWBERRY", 20]]


def test_template_wheat_hire_ramp():
    early = template_wheat_agent(synth_obs(day=2, hands=()))
    mid = template_wheat_agent(synth_obs(day=8, hands=[(0, 1)] * 5))
    assert market_orders(early, "HIRE")
    assert market_orders(mid, "HIRE")                 # ramp target 9 by day 6
    full = template_wheat_agent(synth_obs(day=20, hands=[(0, 1)] * 11))
    assert not market_orders(full, "HIRE")            # ramp target 11


def test_template_wheat_herd_is_8_cows_4_sheep():
    act = template_wheat_agent(synth_obs(day=2, money=5000))
    animals = {o[1] for o in market_orders(act, "BUY_ANIMAL")}
    assert animals == {"COW", "SHEEP"}                # the template herd mix


# ---------------------------------------------------------------- self_feed_ranch

def test_self_feed_premium_milk_gate():
    def milk_sells(price):
        act = self_feed_ranch_agent(synth_obs(day=14, shed={"MILK": 7},
                                              prices={"MILK": price}))
        return [o for o in market_orders(act, "SELL") if o[1] == "MILK"]
    assert milk_sells(150) == []                      # Milan holds for 200
    assert milk_sells(210) == [["SELL", "MILK", 7]]


def test_self_feed_external_feed_is_gap_fill_only():
    tiles = three_quad_tiles()
    for x, y in ((2, 2), (2, 3), (3, 2), (3, 3)):
        tiles[y][x] = {"kind": "PASTURE", "animal": "SHEEP", "placed_day": 2,
                       "yield_units": 0, "consecutive_unfed": 0,
                       "fed_today": False, "cared_today": False,
                       "fertilizer_available": False}
    # own wheat in the shed covers the herd -> no external purchase
    stocked = self_feed_ranch_agent(synth_obs(day=12, tiles=tiles,
                                              shed={"WHEAT": 20}))
    assert not [o for o in market_orders(stocked, "BUY_PRODUCT")
                if o[1] == "WHEAT"]
    empty = self_feed_ranch_agent(synth_obs(day=12, tiles=tiles))
    buys = [o for o in market_orders(empty, "BUY_PRODUCT") if o[1] == "WHEAT"]
    assert buys and buys[0][2] <= 5                   # gap-fill cadence cap


def test_self_feed_buys_small_external_fertilizer():
    tiles = three_quad_tiles()
    tiles[1][1] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 10,
                   "watered_today": False, "consecutive_unwatered": 0,
                   "yield_units": 1, "max_lifespan_step": 360,
                   "fertilized_until_day": -1}
    act = self_feed_ranch_agent(synth_obs(day=14, tiles=tiles,
                                          prices={"FERTILIZER": 50}))
    assert ["BUY_PRODUCT", "FERTILIZER", 1] in act["market"]


def test_self_feed_herd_is_6_cows_6_sheep():
    act = self_feed_ranch_agent(synth_obs(day=2, money=5000))
    animals = {o[1] for o in market_orders(act, "BUY_ANIMAL")}
    assert animals == {"COW", "SHEEP"}


# ------------------------------------------------------------ near_band_diversified

def test_near_band_strawberry_led_rotation():
    farm = dict(tiles=three_quad_tiles(), hands=[(0, 1)] * 10,
                quads=("NW", "NE", "SW"))
    act = near_band_diversified_agent(synth_obs(
        day=2, money=8000, prices={"STRAWBERRY": 240}, **farm))
    assert seed_qty(act, "STRAWBERRY") >= 12          # the leading money crop
    starved = near_band_diversified_agent(synth_obs(
        day=2, money=8000, prices={"STRAWBERRY": 30}, **farm))
    assert seed_qty(starved, "STRAWBERRY") == 0       # below floor price 70


def test_near_band_takes_the_fourth_quadrant():
    early = near_band_diversified_agent(synth_obs(
        day=11, money=8000, quads=("NW", "NE", "SW"), tiles=three_quad_tiles()))
    assert not market_orders(early, "BUY_LAND")       # SE min-day 12
    on_time = near_band_diversified_agent(synth_obs(
        day=14, money=8000, quads=("NW", "NE", "SW"), tiles=three_quad_tiles()))
    assert market_orders(on_time, "BUY_LAND")         # SE 4000 + 900 reserve


def test_near_band_endgame_starts_a_day_earlier():
    # heavy dumper: liquidation window opens at day 27 (template uses 28)
    act = near_band_diversified_agent(synth_obs(
        day=27, shed={"STRAWBERRY": 9, "MILK": 4}, prices={"STRAWBERRY": 3,
                                                           "MILK": 3}))
    sells = {o[1]: o[2] for o in market_orders(act, "SELL")}
    assert sells.get("STRAWBERRY") == 9 and sells.get("MILK") == 4
    assert not [o for o in act["market"] if o[0] in
                ("HIRE", "BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "BUY_LAND")]


def test_near_band_herd_is_diversified():
    act = near_band_diversified_agent(synth_obs(day=2, money=6000))
    animals = {o[1] for o in market_orders(act, "BUY_ANIMAL")}
    assert animals == {"COW", "SHEEP", "GOOSE"}       # 8/3/2 mixed herd


# ------------------------------------------------------------------ scale_ranch

def fed_cow(x, y, placed=2):
    return {"kind": "PASTURE", "animal": "COW", "placed_day": placed,
            "yield_units": 0, "consecutive_unfed": 0,
            "fed_today": True, "cared_today": False,
            "fertilizer_available": False}


def test_scale_ranch_day0_herd_burst_keeps_seed_floor():
    # the round-2 winner split: day-0 cash goes to animals FIRST, wheat seeds
    # from the leftovers -- the seed order must be money-floor capped so the
    # same turn's animal buys keep their budget (3000 - 2 cows - 2 sheep
    # leaves ~300 above the 1100 floor -> strawberry seeds excluded, small
    # wheat order only)
    act = scale_ranch_agent(synth_obs(day=0, hour=1, money=3000,
                                      prices={"STRAWBERRY": 240}))
    assert {o[1] for o in market_orders(act, "BUY_ANIMAL")} == {"COW", "SHEEP"}
    straw = [o for o in market_orders(act, "BUY_SEED") if o[1] == "STRAWBERRY"]
    assert not straw                                  # phase starts day 5
    wheat = [o for o in market_orders(act, "BUY_SEED") if o[1] == "WHEAT"]
    assert wheat and sum(o[2] for o in wheat) * 10 + 1800 <= 3000 - 1100 + 10


def test_scale_ranch_herd_is_8_cows_6_sheep():
    act = scale_ranch_agent(synth_obs(day=2, money=9000))
    animals = {o[1] for o in market_orders(act, "BUY_ANIMAL")}
    assert animals == {"COW", "SHEEP"}                # 8+6 = 14 head target


def test_scale_ranch_crew_ramps_to_12_by_day_7():
    early = scale_ranch_agent(synth_obs(day=2, hands=()))
    assert market_orders(early, "HIRE")
    full = scale_ranch_agent(synth_obs(day=20, hands=[(0, 1)] * 12))
    assert not market_orders(full, "HIRE")            # cap 12 (winners' crew)


def test_scale_ranch_strawberry_phase_opens_day_5():
    early = scale_ranch_agent(synth_obs(day=3, money=8000,
                                        prices={"STRAWBERRY": 240}))
    assert seed_qty(early, "STRAWBERRY") == 0         # not before day 5
    late = scale_ranch_agent(synth_obs(day=6, money=8000,
                                       prices={"STRAWBERRY": 240}))
    assert seed_qty(late, "STRAWBERRY") > 0           # the mid-game engine


def test_scale_ranch_cares_fed_animals_above_routine_tasks():
    # full-coverage CARE discipline: a unit standing on a fed, uncared cow
    # with no co-located urgent task must CARE (weight 70 beats water 42)
    tiles = three_quad_tiles()
    tiles[2][2] = fed_cow(2, 2)
    act = scale_ranch_agent(synth_obs(day=12, hour=10, tiles=tiles,
                                      farmer=(2, 2), hands=[(0, 1)] * 3,
                                      quads=("NW", "NE", "SW")))
    assert act["farmer"] == ["CARE"]


def test_scale_ranch_premium_milk_gate():
    def milk_sells(price):
        act = scale_ranch_agent(synth_obs(day=14, shed={"MILK": 9},
                                          prices={"MILK": price}))
        return [o for o in market_orders(act, "SELL") if o[1] == "MILK"]
    assert milk_sells(150) == []                      # hold for premium 190
    assert milk_sells(210) == [["SELL", "MILK", 9]]


def test_scale_ranch_endgame_liquidation_day_28():
    act = scale_ranch_agent(synth_obs(
        day=28, shed={"MILK": 8, "STRAWBERRY": 12, "WHEAT": 10},
        prices={"MILK": 5, "STRAWBERRY": 5, "WHEAT": 5}))
    sells = {o[1]: o[2] for o in market_orders(act, "SELL")}
    assert sells.get("MILK") == 8 and sells.get("STRAWBERRY") == 12
    assert not [o for o in act["market"] if o[0] in
                ("HIRE", "BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "BUY_LAND")]


# ---------------------------------------------------------------- shared weights

@pytest.mark.parametrize("name,params", [
    ("crop_rotator", CROP_ROTATOR_PARAMS),
    ("template_wheat", TEMPLATE_WHEAT_PARAMS),
    ("self_feed_ranch", SELF_FEED_RANCH_PARAMS),
    ("near_band_diversified", NEAR_BAND_PARAMS),
    ("scale_ranch", SCALE_RANCH_PARAMS),
])
def test_every_param_set_documents_provenance(name, params):
    assert params["name"] == name
    assert params["provenance"]
    for key in ("hire_mode", "hire_cap", "target_quads", "herd",
                "money_crop_caps", "sell_gates", "sell_tranches",
                "feed_gate", "endgame_start"):
        assert key in params, f"{name} missing {key}"
