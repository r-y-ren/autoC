"""m3 strategy-logic unit tests (rotation ranch + online-pool rebuild).

Function-level checks over the submittable main.py for the six m3
capabilities (blueprint campaign III m3-strategy):

  1. price-keyed rotation: phase windows, per-crop price floors, the
     wheat feed floor vs the wheat money tranche;
  2. guardrailed external feed buying (normal cap / starvation cap);
  3. labour rhythm: 9-10/day ramp at profile intensity, dawn burst,
     cash cushion;
  4. quadrant expansion: NE day 4+, SW day 7+, fund-gated, never a 4th
     quadrant, herd subordinated while the fund is pending;
  5. endgame: hoard-dump window (day 26/28 tranches), wool cut-loss on a
     dying curve, doomsday stop-feeding with held-yield harvest;
  6. dead-price freeze (red line): per-species buy freezes and per-crop
     planting freezes, plus the interleaved species buy order.

No full episodes are played here (the development gate covers play);
these pin the planning logic so regressions surface in pytest before any
arena run.  The m2b behavioural fixes are pinned by test_strategy_m2.py.
"""

import importlib.util
import json

import pytest

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_m3", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def _shed(**kw):
    base = {item: 0 for item in ("WHEAT", "CARROT", "TOMATO", "STRAWBERRY",
                                 "MELON", "EGG", "MILK", "WOOL", "FERTILIZER",
                                 "GOOSE", "COW", "SHEEP")}
    base.update(kw)
    return base


def _prices(**kw):
    base = {"WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
            "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200, "FERTILIZER": 100}
    base.update(kw)
    return base


def _orders_contains(orders, op, item):
    return any(o[0] == op and o[1] == item for o in orders)


def _order_qty(orders, op, item):
    for o in orders:
        if o[0] == op and o[1] == item:
            return o[2]
    return 0


def _tiles(quadrants=("NW",)):
    """10x10 board with the given quadrants empty, rest LOCKED."""
    def tile(x, y):
        quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
        return None if quad in quadrants else "LOCKED"
    return [[tile(x, y) for x in range(10)] for y in range(10)]


def _farm(tiles=None, money=5000.0, farmer=(4, 4), hands=(), quads=None):
    quads = quads or ["NW"]
    return {
        "money": money,
        "tiles": tiles if tiles is not None else _tiles(tuple(quads)),
        "farmer": list(farmer),
        "hands": [list(hand) for hand in hands],
        "unlocked_quadrants": quads,
        "hires_today": 0,
    }


def _obs(day, hour, farm, private, prices=None, player=0):
    other = _farm(money=3000.0)
    farms = [farm, other] if player == 0 else [other, farm]
    return {
        "player": player,
        "day": day,
        "hour": hour,
        "farms": farms,
        "private": private,
        "market": {"prices": prices or _prices()},
    }


def _market_orders_with(private, animals=6, herd=6, prices=None, day=8,
                        money=5000.0, quads=None):
    farm = _farm(money=money, quads=quads or ["NW", "NE"])
    obs = {"player": 0, "day": day, "hour": 0, "market": {"prices": prices or _prices()}}
    main._STATE.clear()
    return main._market_orders(obs, farm, private, day, animals, herd), farm


# --------------------------------------------------------------------------
# 1. price-keyed rotation (FM-O1)
# --------------------------------------------------------------------------

def test_rotation_plants_melon_above_its_price_floor():
    # V-T9: with the tetsuya single-quadrant form (wheat 9 + strawberry 11
    # fill the ~20 NW cells first) the melon rim needs a second quadrant;
    # two quadrants carry the full 6/quad band on the far rim.
    farm = _farm(quads=["NW", "NE"])
    builds, crops, _, _ = main._field_alloc(farm, 5, _prices(MELON=250))
    # two quadrants leave 9 rim cells after the strawberry block
    # aggressive ruling 2026-09-04: MELON line cap restored to the
    # V-T9-evidence value 12, so the 9 rim cells bind before the cap
    assert len(crops["MELON"]) == 9
    assert len(crops["MELON"]) <= main.LINE_CAPS["MELON"]
    # dead melon curve: the planting freezes (red line)
    builds2, crops2, _, _ = main._field_alloc(farm, 5, _prices(MELON=100))
    assert not crops2["MELON"]


def test_rotation_phase_windows():
    farm = _farm()
    _, crops_mid, _, _ = main._field_alloc(farm, 12, _prices())
    assert len(crops_mid["STRAWBERRY"]) == 11   # V-T9: wheat 9 + melon 6
    # share the single quadrant first (tetsuya single-quad form)
    _, crops_late, _, _ = main._field_alloc(farm, 16, _prices())
    assert not crops_late["STRAWBERRY"]      # phase 0-14 closed
    # V-T7 (2026-09-02): carrot is the ENDGAME rotation -- it claims no
    # tiles at d16 (the SW wheat field keeps the mid-game) and its full
    # per-quad cap from CARROT_ENDGAME_FROM.
    assert not crops_late["CARROT"]
    _, crops_end, _, _ = main._field_alloc(farm, 24, _prices())
    assert len(crops_end["CARROT"]) == main.CROP_CAP_PER_QUAD["CARROT"]
    _, crops_early, _, _ = main._field_alloc(farm, 12, _prices())
    assert not crops_early["CARROT"]         # phase 15-26 not open


def test_rotation_freezes_each_crop_under_its_floor():
    farm = _farm()
    _, crops, _, _ = main._field_alloc(farm, 8, _prices(STRAWBERRY=40,
                                                        MELON=250))
    assert not crops["STRAWBERRY"]           # < 55 floor
    assert crops["MELON"]
    _, crops2, _, _ = main._field_alloc(farm, 20, _prices(CARROT=20))
    assert not crops2["CARROT"]              # < 28 floor


def test_wheat_is_feed_floor_and_money_crop():
    farm = _farm(quads=["NW", "NE", "SW"])
    _, cheap, _, _ = main._field_alloc(farm, 8, _prices(WHEAT=25))
    _, dear, _, _ = main._field_alloc(farm, 8, _prices(WHEAT=31))
    base = main._wheat_cap(8, 25)
    assert len(cheap["WHEAT"]) == base       # feed floor exactly
    # money tranche activates at >= 30: extra wheat tiles are planned
    # (v6: 3 quads -- at 2 quads the wider strawberry field crowds the
    # tranche out entirely, the structural no-op the v6-B gate measured)
    assert len(dear["WHEAT"]) > len(cheap["WHEAT"])
    assert len(dear["WHEAT"]) <= base + main.WHEAT_MONEY_CAP_PER_QUAD * 3


# --------------------------------------------------------------------------
# 2. guardrailed external feed buying (FM-O3)
# --------------------------------------------------------------------------

def test_feed_buy_guardrail_binds_in_normal_state():
    # short but not starving: buys at 34, refuses 40 (cap FEED_BUY_MAX_PRICE)
    private = {"shed": _shed(WHEAT=7), "seeds": {"WHEAT": 10},
               "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=6, herd=6,
                                    prices=_prices(WHEAT=34))
    assert _orders_contains(orders, "BUY_PRODUCT", "WHEAT")
    orders2, _ = _market_orders_with(private, animals=6, herd=6,
                                     prices=_prices(WHEAT=40))
    assert not _orders_contains(orders2, "BUY_PRODUCT", "WHEAT")


def test_starvation_buys_above_the_guardrail():
    # truly starving (stock < mouths): dear wheat is still cheaper than a
    # lost animal (m2b cap 85)
    private = {"shed": _shed(WHEAT=0), "seeds": {"WHEAT": 10},
               "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=6, herd=6,
                                    prices=_prices(WHEAT=60))
    assert _orders_contains(orders, "BUY_PRODUCT", "WHEAT")


def test_wheat_sell_gate_has_cash_flow_fallback():
    # surplus at a weak bid: held when cash is healthy, sold when the
    # capex plan is starving (gate must never block liquidity)
    private = {"shed": _shed(WHEAT=30), "seeds": {"WHEAT": 10},
               "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=6, herd=6,
                                    prices=_prices(WHEAT=21), money=5000.0)
    assert not _orders_contains(orders, "SELL", "WHEAT")
    orders2, _ = _market_orders_with(private, animals=6, herd=6,
                                     prices=_prices(WHEAT=21), money=400.0)
    assert _orders_contains(orders2, "SELL", "WHEAT")


# --------------------------------------------------------------------------
# 3. labour rhythm (FM-O2)
# --------------------------------------------------------------------------

def test_hands_ramp_reaches_profile_intensity():
    # top-20 median 9.4/day, leader 9.7-9.9 -> 10 by day 12, lean opening
    assert main._hands_target(0, 0, 0) == 5
    assert main._hands_target(2, 0, 0) == 7   # V-T10 tetsuya d1-7
    assert main._hands_target(4, 6, 12) == 8
    assert main._hands_target(7, 10, 18) == 9
    assert main._hands_target(14, 11, 18) == 10
    assert main._hands_target(28, 11, 10) == 10   # held through the dump


def _first_obs_from_engine(seed=5):
    from kgenv.gym_env import KaggricultureGym
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    return env.reset(seed=seed)


def test_dawn_hire_burst_reaches_plan_intensity():
    obs = json.loads(json.dumps(_first_obs_from_engine()))
    obs["day"] = 14
    obs["hour"] = 0
    farm = obs["farms"][0]
    farm["hands"] = []
    farm["money"] = 5000.0
    main._STATE.clear()
    action = main.agent(obs)
    hires = [o for o in action["market"] if o[0] == "HIRE"]
    assert len(hires) == main.HIRE_BURST      # burst, not one-per-turn
    main._STATE.clear()


def test_hire_burst_keeps_cash_cushion():
    obs = json.loads(json.dumps(_first_obs_from_engine()))
    obs["day"] = 14
    obs["hour"] = 0
    farm = obs["farms"][0]
    farm["hands"] = []
    farm["money"] = 20.0                      # cannot afford a crew
    main._STATE.clear()
    action = main.agent(obs)
    assert not [o for o in action["market"] if o[0] == "HIRE"]
    main._STATE.clear()


# --------------------------------------------------------------------------
# 4. quadrant expansion (FM-O2)
# --------------------------------------------------------------------------

def test_ne_quadrant_due_day4_and_fund_gated():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    orders, _ = _market_orders_with(private, day=3, money=5000.0,
                                    quads=["NW"])
    assert not _orders_contains(orders, "BUY_LAND", None) if False else \
        not any(o[0] == "BUY_LAND" for o in orders)
    orders2, _ = _market_orders_with(private, day=4, money=1600.0,
                                     quads=["NW"])
    assert not any(o[0] == "BUY_LAND" for o in orders2)   # fund 1700
    orders3, _ = _market_orders_with(private, day=4, money=1800.0,
                                     quads=["NW"])
    assert any(o[0] == "BUY_LAND" for o in orders3)


def test_sw_quadrant_due_day7():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    orders, _ = _market_orders_with(private, day=6, money=9000.0,
                                    quads=["NW", "NE"])
    assert not any(o[0] == "BUY_LAND" for o in orders)
    orders2, _ = _market_orders_with(private, day=7, money=2800.0,
                                     quads=["NW", "NE"])
    assert any(o[0] == "BUY_LAND" for o in orders2)


def test_fourth_quadrant_never_bought():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    orders, _ = _market_orders_with(private, day=20, money=12000.0,
                                    quads=["NW", "NE", "SW"])
    assert not any(o[0] == "BUY_LAND" for o in orders)


def test_herd_subordinated_to_pending_land_fund():
    # day 5: the NE fund (1700) is pending and unaffordable -> herd buys
    # need fund + cost + reserve, so a lean wallet buys no animals
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=5,
                                    money=1300.0, quads=["NW"])
    assert not any(o[0] == "BUY_LAND" for o in orders)
    assert not _orders_contains(orders, "BUY_ANIMAL", "SHEEP")
    # past the pending window the block lapses (no deadlock).  v10 M-E:
    # the sheep must also clear the liquidity floor after this turn's
    # seed spend (600 of strawberry), so the lean 1300 wallet defers the
    # animal rather than take the post-purchase wallet below the dawn
    # crew bill, and a funded 2000 wallet buys.
    orders2, _ = _market_orders_with(private, animals=0, herd=0, day=9,
                                     money=1300.0, quads=["NW"])
    assert not _orders_contains(orders2, "BUY_ANIMAL", "SHEEP")
    orders3, _ = _market_orders_with(private, animals=0, herd=0, day=9,
                                     money=4000.0, quads=["NW"])
    assert _orders_contains(orders3, "BUY_ANIMAL", "SHEEP")


# --------------------------------------------------------------------------
# 5. endgame: hoard-dump window + doomsday stop-feeding (FM-O4)
# --------------------------------------------------------------------------

def test_wool_dumps_in_endgame_window_from_day26():
    held = _shed(WOOL=15)
    assert _order_qty(main._market_gates(26, _prices(WOOL=40), held, 8),
                      "SELL", "WOOL") == 12
    assert _order_qty(main._market_gates(28, _prices(WOOL=10), held, 8),
                      "SELL", "WOOL") == 12


def test_wool_holds_before_the_window_when_curve_unclear():
    # day 24, weak bid: no cut-loss trigger yet (price < WOOL_CUT_LOSS)
    orders = main._market_gates(24, _prices(WOOL=40), _shed(WOOL=15), 8)
    assert not _orders_contains(orders, "SELL", "WOOL")


def test_wool_cut_loss_on_dying_curve():
    # day 19, price 50 (>= 45 cut-loss): realize down to a small buffer
    assert _order_qty(main._market_gates(19, _prices(WOOL=50),
                                         _shed(WOOL=20), 8),
                      "SELL", "WOOL") == 8


def test_premium_goods_dump_in_endgame_tranches():
    orders = main._market_gates(28, _prices(STRAWBERRY=30, MELON=20),
                                _shed(STRAWBERRY=20, MELON=10), 8)
    assert _orders_contains(orders, "SELL", "STRAWBERRY")
    assert _orders_contains(orders, "SELL", "MELON")


def _pasture_tile(animal="SHEEP", yield_units=3):
    return {"kind": "PASTURE", "animal": animal, "placed_day": 10,
            "yield_units": yield_units, "consecutive_unfed": 0,
            "fed_today": False, "cared_today": False,
            "fertilizer_available": False}


def test_stop_feed_from_day28_but_harvest_held_yield():
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", yield_units=3)
    tiles[3][4] = _pasture_tile("COW", yield_units=0)
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    tasks27, to_feed27, *_ = main._build_tasks(_obs(27, 6, farm, private),
                                               farm, private, 27)
    assert any(t["act"][0] == "FEED" for t in tasks27)
    assert to_feed27 == 2
    tasks28, to_feed28, *_ = main._build_tasks(_obs(28, 6, farm, private),
                                               farm, private, 28)
    assert not any(t["act"][0] == "FEED" for t in tasks28)   # stop-feeding
    assert not any(t["act"][0] == "CARE" for t in tasks28)
    assert to_feed28 == 0
    # held yield is still harvested for the dump
    harvests = [t for t in tasks28 if t["act"][0] == "HARVEST"]
    assert any(t["x"] == 4 and t["y"] == 2 for t in harvests)


# --------------------------------------------------------------------------
# 6. dead-price freeze, generalized (red line)
# --------------------------------------------------------------------------

def test_sheep_buy_freezes_when_wool_curve_dead():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    main._MARKET_MEM.clear()   # isolate from earlier wool-crash EMA state
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=12,
                                    money=9000.0, prices=_prices(WOOL=60))
    assert not _orders_contains(orders, "BUY_ANIMAL", "SHEEP")
    # r4-P2: wool 150 only buys sheep when a yarn store absorbs the flow
    # (zero-absorption markets freeze below base price 190)
    farm = _farm(money=9000.0, quads=["NW", "NE"])
    obs = {"player": 0, "day": 12, "hour": 0,
           "market": {"prices": _prices(WOOL=150)},
           "town": {"unlocked_shops": ["YARN_STORE"]}}
    main._STATE.clear()
    main._MARKET_MEM.clear()   # branch §5.4 curve gate reads the EMA
    orders2 = main._market_orders(obs, farm, private, 12, 0, 0)
    assert _orders_contains(orders2, "BUY_ANIMAL", "SHEEP")
    main._STATE.clear()


def test_cow_buy_freezes_when_milk_curve_dead():
    # m2b demand-drought rule generalized through the species loop
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP")
    tiles[3][4] = _pasture_tile("SHEEP")
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": 12, "hour": 0,
           "market": {"prices": _prices(MILK=60, WOOL=200)}}
    main._STATE.clear()
    orders = main._market_orders(obs, farm, private, 12, 2, 2)
    assert not _orders_contains(orders, "BUY_ANIMAL", "COW")
    # r4-P2: milk 150 needs an absorbing town to resume scaling
    obs["market"]["prices"] = _prices(MILK=150, WOOL=200)
    obs["town"] = {"unlocked_shops": ["SMOOTHIE_SHOP"]}
    main._STATE.clear()
    orders2 = main._market_orders(obs, farm, private, 12, 2, 2)
    assert _orders_contains(orders2, "BUY_ANIMAL", "COW")
    main._STATE.clear()


def test_species_interleave_by_relative_deficit():
    # one sheep placed: cows (0/5) are relatively further behind than
    # sheep (1/6) -> the next buy is a COW (premium-milk window on time)
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP")
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": 6, "hour": 0,
           "market": {"prices": _prices(MILK=200, WOOL=210)}}
    main._STATE.clear()
    orders = main._market_orders(obs, farm, private, 6, 1, 1)
    assert _orders_contains(orders, "BUY_ANIMAL", "COW")
    main._STATE.clear()


# --------------------------------------------------------------------------
# fertilizer value gate (FM-4 generalized)
# --------------------------------------------------------------------------

def test_fert_value_gate_keeps_premium_boosts_only():
    # dear fert: strawberry still fertilized, wheat is not (sack is sold)
    prices = _prices(FERTILIZER=90)
    tiles = _tiles()
    tiles[1][4] = {"kind": "PLANT", "crop": "STRAWBERRY", "planted_day": 4,
                   "watered_today": False, "consecutive_unwatered": 0,
                   "yield_units": 0, "fertilized_until_day": -1}
    tiles[2][4] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 4,
                   "watered_today": False, "consecutive_unwatered": 0,
                   "yield_units": 0, "fertilized_until_day": -1}
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(FERTILIZER=6), "seeds": {}, "inventories": [{}]}
    tasks, *_ = main._build_tasks(_obs(6, 6, farm, private, prices),
                                  farm, private, 6)
    fert_tasks = {(t["x"], t["y"]) for t in tasks if t["act"][0] == "FERTILIZE"}
    assert (4, 1) in fert_tasks        # strawberry
    assert (4, 2) not in fert_tasks    # wheat left unfertilized at 90 fert


def test_field_alloc_carves_declared_extras():
    # aggressive wave C: declared extras (B2 probe / V2 ambush / V4
    # mirror) carve unclaimed empties straight into the rotation.
    farm = _farm(quads=["NW", "NE"])
    builds, crops, _, _ = main._field_alloc(
        farm, 1, _prices(),
        plan={"straw_d1_probe": 3, "iv2_carrot": 8,
              "iv4_mirror": {"crop": "MELON", "tiles": 2}})
    assert len(crops["STRAWBERRY"]) >= 3
    assert len(crops["CARROT"]) >= 8
    assert len(crops["MELON"]) >= 2
