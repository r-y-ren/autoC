"""Success-caliber state-diff measurement tests (campaign III r3-P0).

Three layers:
  1. engine fidelity -- the ported constants and market pricing in
     kgenv.replay_profile must match the vendored kaggle-environments 1.32.7
     engine module bit-for-bit.
  2. attribution semantics -- direct unit tests of the shadow application
     rules (CARE/FEED/WATER/HARVEST/HIRE/SELL classification, blocked-plant
     atomic validation, end-of-day escapes/weed-outs/shed overflow).
  3. end-to-end -- real engine episodes replayed through
     extract_success_metrics must attribute with ZERO mismatches (the
     shadow's predicted post-state equals the recorded observation at every
     step), plus fact-anchored numbers on the round-2 online replays when
     references/data/online-replays is on disk (skipif otherwise).
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import pytest

SOFTWARE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.replay_profile import (  # noqa: E402
    S_ANIMALS,
    S_CROPS,
    S_FARMER_MOVES,
    S_LAND_ORDER,
    S_LAND_PRICES,
    S_MARKET_PARAMS,
    S_PRODUCTS,
    S_SHOPS,
    _s_apply_unit_action,
    _s_daily_refresh_animals,
    _s_daily_refresh_plants,
    _s_drop_inventories,
    _s_op_row,
    _s_end_of_day,
    _s_market_price,
    _s_new_animal,
    _s_new_uacc,
    _s_process_market,
    _s_step,
    extract_success_metrics,
)

REPO = Path(__file__).resolve().parents[3]
ROUND2_DIR = REPO / "workspace/kaggriculture/references/data/online-replays" / "round2"

kag_engine = pytest.importorskip(
    "kaggle_environments.envs.kaggriculture.kaggriculture")


# --------------------------------------------------------------------------- #
# 1. engine fidelity
# --------------------------------------------------------------------------- #
def test_ported_constants_match_vendored_engine():
    assert S_CROPS == kag_engine.CROPS
    assert S_ANIMALS == kag_engine.ANIMALS
    assert S_MARKET_PARAMS == kag_engine.MARKET_PARAMS
    assert S_PRODUCTS == kag_engine.PRODUCTS
    assert S_FARMER_MOVES == kag_engine.FARMER_MOVES
    assert S_LAND_ORDER == kag_engine.LAND_ORDER
    assert S_LAND_PRICES == kag_engine.LAND_PRICES
    assert S_SHOPS == kag_engine.SHOPS


@pytest.mark.parametrize("item", S_PRODUCTS)
@pytest.mark.parametrize("inventory", [0, 1, 500, 9999, 10000, 10001, 12000, 40000])
def test_market_price_matches_engine(item, inventory):
    assert _s_market_price(item, inventory) == \
        kag_engine.market_price(item, inventory)


def test_hire_cost_matches_engine_schedule():
    from kgenv.replay_profile import _s_hire_cost
    for n in range(0, 15):
        assert _s_hire_cost(n) == kag_engine._hire_cost(n)
    # direct schedule check: 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144
    assert [_s_hire_cost(n) for n in range(12)] == \
        [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144]


# --------------------------------------------------------------------------- #
# fixture helpers (fabricated plain-dict states)
# --------------------------------------------------------------------------- #
def _farm(money=3000.0, tiles=None, hires=0, hands=None):
    rows = tiles if tiles is not None else [[None] * 10 for _ in range(10)]
    return {
        "money": money,
        "tiles": rows,
        "unlocked_quadrants": ["NW"],
        "hires_today": hires,
        "farmer": [4, 4],
        "hands": list(hands or []),
    }


def _private(shed=None, seeds=None, inventories=None):
    return {
        "shed": dict(shed or {}),
        "seeds": dict(seeds or {}),
        "inventories": [dict(inv) for inv in (inventories or [{}])],
    }


def _market(inv=10000):
    return {
        "inventory": {item: inv for item in S_PRODUCTS},
        "prices": {item: _s_market_price(item, inv) for item in S_PRODUCTS},
    }


def _state(money0=3000.0, money1=3000.0, tiles0=None, tiles1=None,
           private0=None, private1=None, inv=10000):
    return {
        "farms": [_farm(money0, tiles0), _farm(money1, tiles1)],
        "market": _market(inv),
        "town": {"unlocked_shops": []},
        "privates": [private0 or _private(), private1 or _private()],
    }


def _cfg(**over):
    from kgenv.replay_profile import S_DEFAULT_CONFIG
    cfg = dict(S_DEFAULT_CONFIG)
    cfg.update(over)
    return cfg


# --------------------------------------------------------------------------- #
# 2. attribution semantics
# --------------------------------------------------------------------------- #
def test_care_success_duplicate_and_wrong_tile():
    farm = _farm(tiles=[[{"kind": "PASTURE", "animal": "COW",
                          "placed_day": 0, "yield_units": 0,
                          "consecutive_unfed": 0, "fed_today": False,
                          "cared_today": False, "fertilizer_available": False,
                          "pending_care_bonus": 0}]
                        + [None] * 9] + [[None] * 10 for _ in range(9)])
    acc = _s_new_uacc()
    # farmer stands at (0, 0) on the animal tile
    farm["farmer"] = [0, 0]
    _s_apply_unit_action(farm, _private(), 0, ["CARE"], 10, 0, 24, 100, acc)
    assert acc["requests"]["CARE"] == 1 and acc["success"]["CARE"] == 1
    # second CARE the same day: already served
    _s_apply_unit_action(farm, _private(), 0, ["CARE"], 10, 0, 24, 100, acc)
    assert acc["requests"]["CARE"] == 2 and acc["success"]["CARE"] == 1
    assert acc["fail"]["CARE"]["already_served"] == 1
    # CARE standing on a plant tile: wrong target
    farm["tiles"][0][0] = {"kind": "PLANT", "crop": "WHEAT",
                           "planted_day": 0, "watered_today": False,
                           "consecutive_unwatered": 1, "yield_units": 1,
                           "max_lifespan_step": 120,
                           "fertilized_until_day": -1}
    _s_apply_unit_action(farm, _private(), 0, ["CARE"], 10, 0, 24, 100, acc)
    assert acc["requests"]["CARE"] == 3 and acc["success"]["CARE"] == 1
    assert acc["fail"]["CARE"]["wrong_target"] == 1


def test_dig_clears_weed_and_op_row_aggregates_dig():
    farm = _farm(tiles=[[{"kind": "WEED"}] + [None] * 9]
                 + [[None] * 10 for _ in range(9)])
    farm["farmer"] = [0, 0]
    acc = _s_new_uacc()
    _s_apply_unit_action(farm, _private(), 0, ["DIG"], 10, 0, 24, 100, acc)
    assert acc["requests"]["DIG"] == 1 and acc["success"]["DIG"] == 1
    assert farm["tiles"][0][0] is None
    # v7: the success-calibre op table must expose DIG (was tracked per
    # step but dropped by _s_op_row, hiding the v6 DIG=0 regression)
    row = _s_op_row([acc])
    assert row["DIG"]["requests"] == 1 and row["DIG"]["successes"] == 1
    assert row["DIG"]["success_rate"] == 1.0
    # DIG on an empty tile: wrong_target
    _s_apply_unit_action(farm, _private(), 0, ["DIG"], 10, 0, 24, 100, acc)
    assert acc["fail"]["DIG"]["wrong_target"] == 1


def test_feed_requires_wheat_in_unit_inventory():
    animal = {"kind": "PASTURE", "animal": "SHEEP", "placed_day": 0,
              "yield_units": 0, "consecutive_unfed": 0, "fed_today": False,
              "cared_today": False, "fertilizer_available": False,
              "pending_care_bonus": 0}
    farm = _farm(tiles=[[animal] + [None] * 9] + [[None] * 10 for _ in range(9)])
    farm["farmer"] = [0, 0]
    # no WHEAT carried: no_resource, flag must NOT flip
    acc = _s_new_uacc()
    private = _private()
    _s_apply_unit_action(farm, private, 0, ["FEED"], 10, 0, 24, 100, acc)
    assert acc["requests"]["FEED"] == 1 and acc["success"]["FEED"] == 0
    assert acc["fail"]["FEED"]["no_resource"] == 1
    assert animal["fed_today"] is False
    # with WHEAT: success consumes one unit
    private = _private(inventories=[{"WHEAT": 2}])
    _s_apply_unit_action(farm, private, 0, ["FEED"], 10, 0, 24, 100, acc)
    assert acc["success"]["FEED"] == 1
    assert animal["fed_today"] is True
    assert private["inventories"][0] == {"WHEAT": 1}
    # repeat: already served
    _s_apply_unit_action(farm, private, 0, ["FEED"], 10, 0, 24, 100, acc)
    assert acc["fail"]["FEED"]["already_served"] == 1
    assert private["inventories"][0] == {"WHEAT": 1}  # untouched


def test_water_and_harvest_classification():
    plant = {"kind": "PLANT", "crop": "CARROT", "planted_day": 0,
             "watered_today": True, "consecutive_unwatered": 0,
             "yield_units": 4, "max_lifespan_step": 96,
             "fertilized_until_day": -1}
    farm = _farm(tiles=[[dict(plant)] + [None] * 9]
                 + [[None] * 10 for _ in range(9)])
    farm["farmer"] = [0, 0]
    acc = _s_new_uacc()
    _s_apply_unit_action(farm, _private(), 0, ["WATER"], 10, 1, 24, 100, acc)
    assert acc["fail"]["WATER"]["already_served"] == 1
    # harvest a mature carrot: yield moves to the unit inventory
    _s_apply_unit_action(farm, _private(), 0, ["HARVEST"], 10, 3, 24, 100, acc)
    assert acc["success"]["HARVEST"] == 1
    assert acc["harvest_units"]["CARROT"] == 4
    assert farm["tiles"][0][0] is None  # non-ongoing crop clears the tile
    # harvest on an empty tile: wrong target / no yield
    _s_apply_unit_action(farm, _private(), 0, ["HARVEST"], 10, 3, 24, 100, acc)
    assert acc["fail"]["HARVEST"]["wrong_target"] == 1


def test_move_blocked_at_board_edge():
    farm = _farm()
    farm["farmer"] = [0, 0]
    acc = _s_new_uacc()
    _s_apply_unit_action(farm, _private(), 0, ["NORTH"], 10, 0, 24, 100, acc)
    _s_apply_unit_action(farm, _private(), 0, ["WEST"], 10, 0, 24, 100, acc)
    assert acc["requests"]["NORTH"] == 1 and acc["success"]["NORTH"] == 0
    assert acc["requests"]["WEST"] == 1 and acc["success"]["WEST"] == 0
    assert farm["farmer"] == [0, 0]
    _s_apply_unit_action(farm, _private(), 0, ["SOUTH"], 10, 0, 24, 100, acc)
    assert acc["success"]["SOUTH"] == 1 and farm["farmer"] == [0, 1]


def test_hire_success_and_no_money_rejection():
    st = _state(money0=5.0)
    acc = [{"hire": {"requests": 0, "successes": 0, "no_money": 0,
                     "spend": 0, "failed_cost": 0},
            "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                         "no_land": 0, "spend": 0},
            "orders": []} for _ in range(2)]
    actions = [{"market": [["HIRE"], ["HIRE"]]}, {}]
    _s_process_market(st, actions, _cfg(), acc)
    # first hire costs fib(0)=1 (money 5 -> 4), second fib(1)=1 (4 -> 3)
    assert acc[0]["hire"] == {"requests": 2, "successes": 2, "no_money": 0,
                              "spend": 2, "failed_cost": 0}
    # third hire costs fib(2)=2 <= 3 ok, fourth fib(3)=3 > 1 rejected
    actions = [{"market": [["HIRE"], ["HIRE"]]}, {}]
    _s_process_market(st, actions, _cfg(), acc)
    assert acc[0]["hire"]["requests"] == 4
    assert acc[0]["hire"]["successes"] == 3
    assert acc[0]["hire"]["no_money"] == 1
    assert st["farms"][0]["hands"] != []  # hands actually spawned


def test_sell_partial_fill_and_buy_abort_reasons():
    # shed holds 2 WHEAT; a SELL of 5 fills 2 then aborts (no_stock)
    st = _state(private0=_private(shed={"WHEAT": 2}))
    acc = [{"hire": {"requests": 0, "successes": 0, "no_money": 0,
                     "spend": 0, "failed_cost": 0},
            "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                         "no_land": 0, "spend": 0},
            "orders": []} for _ in range(2)]
    _s_process_market(st, [{"market": [["SELL", "WHEAT", 5]]}, {}],
                      _cfg(), acc)
    order = acc[0]["orders"][0]
    assert order["type"] == "SELL" and order["requested"] == 5
    assert order["filled"] == 2 and order["abort"] == "no_stock"
    assert order["first_price"] is not None
    assert st["farms"][0]["money"] > 3000.0
    # BUY_PRODUCT with insufficient money: no_money abort, zero fill
    st = _state(money0=3.0)
    acc = [{"hire": {"requests": 0, "successes": 0, "no_money": 0,
                     "spend": 0, "failed_cost": 0},
            "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                         "no_land": 0, "spend": 0},
            "orders": []} for _ in range(2)]
    _s_process_market(st, [{"market": [["BUY_PRODUCT", "WHEAT", 10]]}, {}],
                      _cfg(), acc)
    order = acc[0]["orders"][0]
    assert order["filled"] == 0 and order["abort"] == "no_money"
    # BUY into a full shed: shed_full abort
    st = _state(private0=_private(shed={i: 10 for i in S_PRODUCTS[:10]}))
    st["privates"][0]["shed"]["WHEAT"] = 100
    acc = [{"hire": {"requests": 0, "successes": 0, "no_money": 0,
                     "spend": 0, "failed_cost": 0},
            "buy_land": {"requests": 0, "successes": 0, "no_money": 0,
                         "no_land": 0, "spend": 0},
            "orders": []} for _ in range(2)]
    _s_process_market(st, [{"market": [["BUY_PRODUCT", "WHEAT", 1]]}, {}],
                      _cfg(), acc)
    order = acc[0]["orders"][0]
    assert order["filled"] == 0 and order["abort"] == "shed_full"


def test_engine_drops_all_plants_when_demand_exceeds_seeds():
    # atomic PLANT validation: 2 requests > 1 seed -> BOTH become no-ops
    st = _state(private0=_private(seeds={"WHEAT": 1}))
    st["farms"][0]["farmer"] = [0, 0]
    st["farms"][0]["hands"] = [[1, 0]]
    actions = [{"farmer": ["PLANT", "WHEAT"], "hands": [["PLANT", "WHEAT"]],
                "market": []}, {}]
    _post, attr = _s_step(st, actions, 1, _cfg(), seed=1)
    u = attr["unit"][0]
    assert u["requests"]["PLANT"] == 2
    assert u["success"]["PLANT"] == 0
    assert u["fail"]["PLANT"]["no_resource"] == 2
    assert st["farms"][0]["tiles"][0][0] is None
    assert st["farms"][0]["tiles"][0][1] is None


def test_end_of_day_escape_weed_and_overflow():
    farm = _farm(tiles=[
        [dict(_s_new_animal("COW", 3), consecutive_unfed=2), None]
        + [None] * 8,
        [{"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
          "watered_today": False, "consecutive_unwatered": 2,
          "yield_units": 3, "max_lifespan_step": 120,
          "fertilized_until_day": -1}] + [None] * 9,
    ] + [[None] * 10 for _ in range(8)])
    farm["farmer"] = [0, 0]
    farm["hands"] = [[1, 0]]
    private = _private(shed={"WHEAT": 95},
                       inventories=[{"WHEAT": 8}, {"MILK": 4}])
    st = {"farms": [farm], "market": _market(), "town": {"unlocked_shops": []},
          "privates": [private]}
    events, overflow = [], [{}]
    from kgenv.replay_profile import _s_end_of_day as eod
    eod(st, 3, _cfg(), seed=7, events=events, overflow=overflow)
    types = [e["type"] for e in events]
    assert "escape" in types and "weed_care_lapse" in types
    escape = next(e for e in events if e["type"] == "escape")
    assert escape["animal"] == "COW" and escape["loss_est"] == 400
    assert escape["yield_units_lost"] == 0
    # shed had 5 room (95/100): WHEAT 8 -> 5 stored + 3 discarded,
    # then MILK 4 finds a full shed -> 4 discarded
    assert overflow[0] == {"WHEAT": 3, "MILK": 4}
    # animal escaped -> tile is a bare structure; plant weeded out
    assert farm["tiles"][0][0] == {"kind": "PASTURE"}
    assert farm["tiles"][1][0] == {"kind": "WEED"}
    # hands cleared for the next day
    assert farm["hands"] == [] and farm["hires_today"] == 0


def test_daily_refresh_production_respects_max_held():
    animal = dict(_s_new_animal("COW", 0), fed_today=True, cared_today=True,
                  yield_units=6, placed_day=0)
    farm = _farm(tiles=[[dict(animal)] + [None] * 9]
                 + [[None] * 10 for _ in range(9)])
    events = []
    # day=7 -> next_day 8: days_since_first = 8 - 0 - 8 = 0 -> production day
    _s_daily_refresh_animals(farm, 7, events)
    # capped at max_held=6 even with base 1 + accrued care bonus
    assert farm["tiles"][0][0]["yield_units"] == 6
    # care bonus accrued for the next production day (cared+fed today)
    assert farm["tiles"][0][0]["pending_care_bonus"] == 1


def test_consecutive_unwatered_weed_out_only_at_two():
    plant = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 0,
             "watered_today": False, "consecutive_unwatered": 0,
             "yield_units": 3, "max_lifespan_step": 120,
             "fertilized_until_day": -1}
    farm = _farm(tiles=[[dict(plant)] + [None] * 9]
                 + [[None] * 10 for _ in range(9)])
    events = []
    _s_daily_refresh_plants(farm, 1, 24, events)
    # 1 unwatered day: survives, counter ticks to 1
    assert farm["tiles"][0][0]["kind"] == "PLANT"
    assert farm["tiles"][0][0]["consecutive_unwatered"] == 1
    _s_daily_refresh_plants(farm, 2, 24, events)
    # second consecutive miss: weed out (engine checks AFTER the increment;
    # a fresh plant starts at 1, so one unwatered day already kills it)
    assert farm["tiles"][0][0] == {"kind": "WEED"}
    assert events and events[0]["type"] == "weed_care_lapse"


# --------------------------------------------------------------------------- #
# 3. end-to-end: real engine episodes must attribute with zero mismatches
# --------------------------------------------------------------------------- #
def _replay_from_env(env, teams=("A", "B")):
    """Normalise an engine episode into the replay JSON shape (plain dicts)."""
    steps = [[dict(s) for s in step_states] for step_states in env.steps]
    final = env.steps[-1]
    # resolve_episode_seed CLEARS configuration.seed and persists it on
    # env.info["seed"] -- the engine's end-of-day RNG reads env.info
    return json.loads(json.dumps({
        "info": {"TeamNames": list(teams), "EpisodeId": -1,
                 "seed": env.info.get("seed")},
        "statuses": [s.status for s in final],
        "rewards": [s.reward for s in final],
        "steps": steps,
    }))


@pytest.mark.parametrize("seed", [101, 202])
def test_real_episode_attributes_with_zero_mismatches(seed):
    """Cross-validation against the real engine: the shadow's predicted
    post-state must equal the recorded observation at EVERY step."""
    from kaggle_environments import make
    from kgenv.bots.baseline import baseline_wheat_agent
    from kgenv.bots.cow_baron import cow_baron_agent

    env = make("kaggriculture",
               configuration={"episodeSteps": 120, "seed": seed})
    env.run([cow_baron_agent, baseline_wheat_agent])
    assert [s.status for s in env.steps[-1]] == ["DONE", "DONE"]
    replay = _replay_from_env(env)
    out = extract_success_metrics(replay, strict=False)
    assert out["episode"]["attribution_valid"] is True, \
        out["episode"]["mismatches"][:3]
    assert out["episode"]["mismatch_steps"] == 0
    for player in out["players"]:
        assert player["integrity"]["steps_attributed"] == 119
        # requests >= successes everywhere
        for op, row in player["ops"].items():
            if row["requests"]:
                assert row["successes"] <= row["requests"]


@pytest.mark.skipif(not (ROUND2_DIR / "episode-102399852-replay.json").exists(),
                    reason="round-2 online replays not on disk")
def test_round2_fact_anchored_numbers():
    """Hand-verified 2026-08-29 success-caliber facts (r3-P0 report)."""
    from kgenv.replay_profile import load_replay
    out = extract_success_metrics(
        load_replay(ROUND2_DIR / "episode-102399852-replay.json"))
    by_team = {p["team"]: p for p in out["players"]}
    armin = by_team["arminhej96"]
    # request-caliber CARE 586 -> 334 effective (252 duplicates)
    assert armin["ops"]["CARE"]["requests"] == 586
    assert armin["ops"]["CARE"]["successes"] == 334
    assert armin["ops"]["CARE"]["failures"]["already_served"] == 252
    ours = by_team["renyxin"]
    assert ours["ops"]["CARE"]["requests"] == 162
    assert ours["ops"]["CARE"]["successes"] == 162  # no invalid CARE at all
    assert ours["escapes"]["count"] == 1
    assert ours["weeds"]["care_lapse"] == 28


@pytest.mark.skipif(not (ROUND2_DIR / "episode-102406576-replay.json").exists(),
                    reason="round-2 online replays not on disk")
def test_round2_danila_hire_requests_truncated_and_rejected():
    from kgenv.replay_profile import load_replay
    out = extract_success_metrics(
        load_replay(ROUND2_DIR / "episode-102406576-replay.json"))
    danila = next(p for p in out["players"] if p["team"] == "Danila Galkin")
    # raw replay contains 573 HIRE orders; the engine parses only <=10 per
    # turn (450 visible), of which 138 are silently rejected for no money
    assert danila["hire"]["requests"] == 450
    assert danila["hire"]["successes"] == 312
    assert danila["hire"]["no_money_rejects"] == 138
