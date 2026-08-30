"""v8 wheat-economy pins (regime change W1: buy-to-cap seed supply).

The v6/v7 wheat field decayed 16->0 across every online game (harvested
tiles never replanted: the `seeds < 6 -> buy 12` cadence supplies at most
~2.4 seeds/day while a cycling 20-30-tile field needs 5-7.5) while the
allocation cap already permits 27-39 tiles -- the binding constraint was
seed supply, not the plan.  W1 keeps the cap ladder byte-identical and
buys seeds to the standing replant cycle instead.
"""

import importlib.util
import sys
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
AGENT_V8 = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v8" / "main.py"


def _load():
    spec = importlib.util.spec_from_file_location(f"v8_{id([])}", AGENT_V8)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _farm(quads=("NW", "NE", "SW"), wheat=0, money=1000.0):
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    half = 5
    for y in range(10):
        for x in range(10):
            q = ("N" if y < half else "S") + ("W" if x < half else "E")
            if q in quads:
                tiles[y][x] = None
    placed = 0
    for y in range(10):
        for x in range(10):
            if placed >= wheat:
                break
            if tiles[y][x] is None:
                tiles[y][x] = {"kind": "PLANT", "crop": "WHEAT",
                               "planted_day": 5, "yield_units": 1}
                placed += 1
    return {"tiles": tiles, "money": money,
            "unlocked_quadrants": list(quads), "farmer": [4, 4],
            "hands": [], "hires_today": 0}


def _obs(farm, day=10, wheat_price=33, seeds=None):
    return {"player": 0, "day": day, "hour": 0,
            "market": {"prices": {"WHEAT": wheat_price, "CARROT": 35,
                                  "TOMATO": 60, "STRAWBERRY": 120,
                                  "MELON": 250, "EGG": 50, "MILK": 160,
                                  "WOOL": 200, "FERTILIZER": 100}},
            "town": {"unlocked_shops": []},
            "farms": [farm, farm],
            "private": {"shed": {}, "seeds": seeds or {},
                        "inventories": [{}]}}


def _wheat_orders(mod, farm, day=10, wheat_price=33, seeds=None, plan=None):
    obs = _obs(farm, day, wheat_price, seeds)
    if plan is None:
        plan = dict(mod._DEFENSIVE_PLAN)
        plan["wheat_volume_ok"] = True      # the v8 volume regime, gate OPEN
    orders = mod._market_orders(obs, farm, obs["private"], day,
                                animals_to_feed=8, herd_total=12,
                                plan=plan)
    return [o for o in orders if o[0] == "BUY_SEED" and o[1] == "WHEAT"]


def test_cap_ladder_unchanged_from_v72():
    # W1 touches seed supply only; the cap ladder stays byte-identical
    mod = _load()
    assert [mod._wheat_cap(10, p) for p in (25, 30, 34, 36, 41, 42)] == \
        [18, 18, 18, 22, 22, 30]


def test_seed_buy_tracks_the_replant_cycle():
    mod = _load()
    # price 33, 3 quads: effective cap = 18 + 3*3 = 27; 10 alive, 0 seeds
    # -> buy 17 to cover a full replant cycle in one order
    orders = _wheat_orders(mod, _farm(wheat=10), wheat_price=33)
    assert orders and orders[0][2] == 17
    # stocked to the cycle: no order
    orders = _wheat_orders(mod, _farm(wheat=10), wheat_price=33,
                           seeds={"WHEAT": 17})
    assert not orders
    # mid-game thin seeds buy to the cycle, not the old 12 floor
    # (cap 18 - 0 alive - 3 held = 15 wanted)
    orders = _wheat_orders(mod, _farm(wheat=0), wheat_price=25,
                           seeds={"WHEAT": 3})
    assert orders and orders[0][2] == 15
    # the OPENING (day <= 2) keeps the herd's budget: at most 12
    orders = _wheat_orders(mod, _farm(wheat=0), day=1, wheat_price=33,
                           seeds={"WHEAT": 0})
    assert orders and orders[0][2] == 12
    # batch ceiling 24 even when the cycle wants more
    orders = _wheat_orders(mod, _farm(wheat=0, money=5000.0),
                           wheat_price=45, seeds={"WHEAT": 0})
    assert orders and orders[0][2] == 24


def test_seed_buy_scales_to_wallet_and_day_bounded():
    mod = _load()
    # working-capital semantics: a 100-coin wallet still buys 8 seeds
    # ((100-20)//10), a sub-30 wallet buys nothing (the herd eats first)
    orders = _wheat_orders(mod, _farm(wheat=10, money=100.0),
                           wheat_price=33)
    assert orders and orders[0][2] == 8
    assert not _wheat_orders(mod, _farm(wheat=10, money=25.0),
                             wheat_price=33)
    # past the last plantable window: no order
    assert not _wheat_orders(mod, _farm(wheat=10), day=24, wheat_price=33)


def test_straw_total_cap_drops_to_12():
    # v8-W2: 12-tile strawberry side line (corpus top-12 band 6-12)
    mod = _load()
    assert mod._DEFENSIVE_PLAN["straw_total_cap"] == 12


def test_wheat_field_sustains_across_harvest_cycle():
    # the v6/v7 failure signature: harvested wheat was never replanted
    # (16 -> 7 -> 0 across rounds 3-4).  With buy-to-cap seeds the plan
    # room refills: alloc wants `cap` wheat whenever alive drops.  The
    # W3 gate splits the outcome on the opponent's visible wheat field.
    mod = _load()
    farm = _farm(wheat=0)
    plan_open = dict(mod._DEFENSIVE_PLAN)
    plan_open["wheat_volume_ok"] = True
    builds, crop_map, n, cap = mod._field_alloc(
        farm, 14, {"WHEAT": 33}, plan_open)
    assert len(crop_map["WHEAT"]) == 18 + mod.WHEAT_MONEY_CAP_PER_QUAD * 3
    # gate SHUT (wheat-flooding opponent): the v7.2 feed floor exactly
    builds, crop_map, n, cap = mod._field_alloc(
        farm, 14, {"WHEAT": 33}, mod._DEFENSIVE_PLAN)
    assert len(crop_map["WHEAT"]) == 18
