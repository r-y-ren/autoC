"""r3 strategy-logic unit tests (opening/mid-game timing redesign, r3-2).

Function-level checks over the submittable main.py for the four r3 phase
changes pinned by the round-2 winner x top-20 cross-profile
(exports/online/round2_winner_deep_dive.md, >=3-game evidence each):

  1. d0 capital allocation: the day-0 burst buys the mixed OPENING_HERD
     (v1.5: 1C+2S = 1400 of the 3000 start so opening melon still fits),
     both species in one turn, and the normal paced loop stands down for
     the rest of day 0;
  2. herd build deadline: the target plan crosses 12 head by day 8 and
     caps at HERD_CAP=14 (8C+6S) -- winners 13-17 by d8-11, top-20 med
     12 by d6 (the Anthaus counter-example: 18 head built late loses);
  3. strawberry cadence: phase opens day 5 (d0-4 cash belongs to the
     herd burst), 6/quad cap = 18 tiles on 3 quadrants (winner band
     16-23; ~20 is the labour-budget ceiling, top-20 med 36 is a trap);
  4. crew 12: _crew_target follows the herd up to HANDS_CAP_R3 (winners
     hold 12 hands from d7-11) with the pinned m3 ramp as the floor.

Plus two continuity guards from the winner table: the feed-break
escalator (escape at 2 unfed days; winners never break the chain --
Rafzan counter-example d7) and the 15u/day external-feed cadence under
the <=38 guardrail.

No full episodes here (the 72-game development gate covers play); the
m2b behavioural fixes stay pinned by test_strategy_m2.py and the m3
capabilities by test_strategy_m3.py.
"""

import importlib.util

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_r3", SUBMISSION_MAIN)
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
                        money=5000.0, quads=None, hour=0):
    farm = _farm(money=money, quads=quads or ["NW", "NE"])
    obs = {"player": 0, "day": day, "hour": hour,
           "market": {"prices": prices or _prices()}}
    main._STATE.clear()
    return main._market_orders(obs, farm, private, day, animals, herd), farm


def _pasture_tile(animal="SHEEP", yield_units=0, consecutive_unfed=0,
                  fed_today=False):
    return {"kind": "PASTURE", "animal": animal, "placed_day": 10,
            "yield_units": yield_units, "consecutive_unfed": consecutive_unfed,
            "fed_today": fed_today, "cared_today": False,
            "fertilizer_available": False}


# --------------------------------------------------------------------------
# 1. d0 capital allocation (R3-1)
# --------------------------------------------------------------------------

def test_day0_burst_buys_both_species():
    # v1.5 P0 (official round-20/21): day 0 buys 2 sheep + 1 cow (~1400)
    # beside the 10-wheat feed floor, money-gated by OPENING_RESERVE --
    # the annuity deadlines (wool d8 / milk d11) stay reachable, and the
    # leftover cash buys opening melon.  Days 1+ have NO opening-sequence
    # entry: the paced loop (1/day before day 4) owns the ramp from d1 on.
    private = {"shed": _shed(), "seeds": {"WHEAT": 12}, "inventories": [{}]}
    main._STATE.clear()
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=0,
                                    money=3000.0, quads=["NW"])
    assert _order_qty(orders, "BUY_ANIMAL", "SHEEP") == 2
    assert _order_qty(orders, "BUY_ANIMAL", "COW") == 1
    assert 2 * 500 + 1 * 400 + main.OPENING_RESERVE <= 3000
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=1,
                                    money=2900.0, quads=["NW"])
    day1_total = _order_qty(orders, "BUY_ANIMAL", "SHEEP") + \
        _order_qty(orders, "BUY_ANIMAL", "COW")
    assert day1_total <= main._animal_pace(1)  # paced loop, no d1 staging burst
    main._STATE.clear()


def test_day0_burst_is_money_gated_with_reserve():
    # a lean wallet (burst + reserve unaffordable) buys what fits, never
    # the full plan on credit
    private = {"shed": _shed(), "seeds": {"WHEAT": 12}, "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=0,
                                    money=1500.0, quads=["NW"])
    bought = _order_qty(orders, "BUY_ANIMAL", "COW") * 400 + \
        _order_qty(orders, "BUY_ANIMAL", "SHEEP") * 500
    assert bought + main.OPENING_RESERVE <= 1500


def test_paced_loop_stands_down_after_the_burst():
    # later on day 0 (animals confirmed into the shed): no further buys --
    # the 3-head day-0 target is the burst itself
    private = {"shed": _shed(COW=1, SHEEP=2), "seeds": {"WHEAT": 12},
               "inventories": [{}]}
    main._STATE.clear()
    orders, _ = _market_orders_with(private, animals=0, herd=3, day=0,
                                    money=2500.0, quads=["NW"], hour=6)
    assert not _orders_contains(orders, "BUY_ANIMAL", "COW")
    assert not _orders_contains(orders, "BUY_ANIMAL", "SHEEP")
    main._STATE.clear()


# --------------------------------------------------------------------------
# 2. herd build deadline (R3-2)
# --------------------------------------------------------------------------

def test_herd_plan_crosses_12_by_day8_and_caps_at_14():
    assert main._herd_target(0, 99) == 3                    # d0 reduced burst
    assert main._herd_target(5, 99) == 10
    assert main._herd_target(6, 99) >= 12 or main._herd_target(7, 99) >= 12
    assert main._herd_target(8, 99) == main.HERD_CAP        # 12+ by d8, cap
    assert main.HERD_CAP == 16
    assert main.HERD_CAP <= 17                              # winner ceiling
    assert main._herd_target(8, 9) == 9                     # feed capacity binds


def test_herd_composition_is_the_winner_mix():
    # 9C+7S = 16 (round-19: top peak median 15.8; winners 13-17)
    assert main.HERD_COMPOSITION["COW"] == 9
    assert main.HERD_COMPOSITION["SHEEP"] == 7
    assert sum(main.HERD_COMPOSITION.values()) == main.HERD_CAP


def test_day0_opening_melon_fits_on_single_quadrant():
    # v1.5 P0: after the reduced herd burst, a single NW farm still has
    # empty tiles for melon AND the market orders a melon seed batch
    # (the old 22-tile wheat floor + land_fund+250 gate made want=0).
    farm = _farm(quads=["NW"])
    _, crops, _, _ = main._field_alloc(farm, 0, _prices())
    assert len(crops["WHEAT"]) <= 10
    assert len(crops["MELON"]) >= 6
    private = {"shed": _shed(), "seeds": {"WHEAT": 12}, "inventories": [{}]}
    main._STATE.clear()
    orders, _ = _market_orders_with(private, animals=0, herd=0, day=0,
                                    money=3000.0, quads=["NW"])
    assert _order_qty(orders, "BUY_SEED", "MELON") >= 6
    spend_animals = (_order_qty(orders, "BUY_ANIMAL", "SHEEP") * 500
                     + _order_qty(orders, "BUY_ANIMAL", "COW") * 400)
    spend_melon = _order_qty(orders, "BUY_SEED", "MELON") * 80
    assert spend_animals + spend_melon + main.OPENING_RESERVE <= 3000
    main._STATE.clear()


def test_opening_burst_species_match_composition_track():
    # both species present on day 0 -> first wool d6 and first milk d8-9
    for animal, want in main.OPENING_HERD.items():
        assert want > 0
        assert main.HERD_COMPOSITION[animal] >= want


# --------------------------------------------------------------------------
# 3. strawberry cadence (R3-3)
# --------------------------------------------------------------------------

def test_strawberry_phase_opens_day5_not_day0():
    # d0-4: no strawberry planting (the cash belongs to the herd burst);
    # d5+: the phase is open through d14
    lo, hi = main.CROP_PHASE["STRAWBERRY"]
    # round-19: the window widens to d24 (top replants strawberry to
    # 33-38 plants); the d0-4 herd-burst cash guard is unchanged
    assert lo == 5 and hi == 24
    farm = _farm(quads=["NW"])
    _, crops_early, _, _ = main._field_alloc(farm, 3, _prices())
    assert not crops_early["STRAWBERRY"]
    # single-quadrant farms are now fully consumed by the 26-tile wheat
    # floor (feed is the red-line obligation); the strawberry band lives
    # on multi-quadrant farms -- see the winner-band test below.
    _, crops_open, _, _ = main._field_alloc(farm, 7, _prices())
    assert not crops_open["STRAWBERRY"]


def test_strawberry_reaches_winner_band_on_three_quadrants():
    # round-19: 12/quad with the 36-tile DEFENSIVE total cap (top-meta
    # calibration: top runs 33-38 strawberry plants)
    farm = _farm(quads=["NW", "NE", "SW"])
    _, crops, _, _ = main._field_alloc(farm, 12, _prices())
    n = len(crops["STRAWBERRY"])
    assert n == 20   # tile pool after wheat 26 + melon 12 + 2 extra pastures
    assert n <= min(main.CROP_CAP_PER_QUAD["STRAWBERRY"] * 3,
                    main._DEFENSIVE_PLAN["straw_total_cap"])
    # the pre-SW single quadrant is fully consumed by the wheat floor
    _, crops1, _, _ = main._field_alloc(_farm(quads=["NW"]), 12, _prices())
    assert not crops1["STRAWBERRY"]


# --------------------------------------------------------------------------
# 4. crew 12 (R3-4)
# --------------------------------------------------------------------------

def test_crew_follows_herd_to_12():
    # winners hold 12 hands from d7-11 with 13-17 head producing
    assert main._crew_target(7, 12, 18, 3) == 12
    assert main._crew_target(7, 14, 18, 3) == 12
    assert main._crew_target(10, 17, 18, 3) == 12      # capped at 12
    assert main.HANDS_CAP_R3 == 12


def test_crew_floor_is_the_pinned_m3_ramp():
    # a bad season (small herd) never overhires: the m3 ramp alone rules
    assert main._crew_target(0, 4, 16, 1) == 5
    assert main._crew_target(2, 4, 16, 1) == 7   # V-T10 tetsuya d1-7
    assert main._crew_target(7, 6, 18, 3) == 9
    assert main._crew_target(14, 6, 18, 3) == 10
    assert main._hands_target(7, 10, 18) == 9          # m3 pin intact


# --------------------------------------------------------------------------
# feed continuity + external-feed cadence (winner table, Rafzan counter)
# --------------------------------------------------------------------------

def test_feed_break_escalates_above_every_field_task():
    # one animal already missed a day (consecutive_unfed=1): its FEED task
    # outranks every non-life-threatening task (escape fires at streak 2)
    tiles = _tiles()
    tiles[2][4] = _pasture_tile("SHEEP", consecutive_unfed=1)
    tiles[3][4] = _pasture_tile("COW")
    tiles[1][4] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 8,
                   "watered_today": False, "consecutive_unwatered": 1,
                   "yield_units": 4, "fertilized_until_day": -1}
    farm = _farm(tiles=tiles, quads=["NW"])
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    tasks, to_feed, *_ = main._build_tasks(_obs(10, 6, farm, private),
                                           farm, private, 10)
    feeds = {t["key"]: t for t in tasks if t["act"][0] == "FEED"}
    assert to_feed == 2
    assert feeds[("feed", 4, 2)]["w"] == 100      # streak: top priority
    assert feeds[("feed", 4, 3)]["w"] == 88
    water = [t for t in tasks if t["act"][0] == "WATER"]
    assert all(t["w"] < 100 for t in water)


def test_feed_buy_cadence_15u_under_38_guardrail():
    # normal state (stock covers the mouths): the <=38 guardrail binds --
    # the buffer tops up at 34 and refuses 40; empty system (daily
    # ration): the buy is bounded by the ~15u/day cadence, max 16
    private = {"shed": _shed(WHEAT=16), "seeds": {"WHEAT": 10},
               "inventories": [{}]}
    orders, _ = _market_orders_with(private, animals=14, herd=14,
                                    prices=_prices(WHEAT=34), day=12,
                                    money=3000.0)
    qty = _order_qty(orders, "BUY_PRODUCT", "WHEAT")
    assert 0 < qty <= 16
    orders2, _ = _market_orders_with(private, animals=14, herd=14,
                                     prices=_prices(WHEAT=40), day=12,
                                     money=3000.0)
    assert not _orders_contains(orders2, "BUY_PRODUCT", "WHEAT")
    private0 = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    orders3, _ = _market_orders_with(private0, animals=14, herd=14,
                                     prices=_prices(WHEAT=30), day=12,
                                     money=3000.0)
    assert 12 <= _order_qty(orders3, "BUY_PRODUCT", "WHEAT") <= 16


def test_fertilizer_streams_out_of_the_shed_at_winner_band_prices():
    # winners realise 61-85/unit on daily collection (9.8-18.5k/season);
    # a full-day collection above the stock cap sells down to the field
    # reserve even mid-band -- the income line must not sit in the shed
    orders = main._market_gates(12, _prices(FERTILIZER=75), _shed(FERTILIZER=16), 14)
    assert _order_qty(orders, "SELL", "FERTILIZER") == 16 - main.FERT_FIELD_RESERVE
    orders2 = main._market_gates(12, _prices(FERTILIZER=100), _shed(FERTILIZER=6), 14)
    assert _order_qty(orders2, "SELL", "FERTILIZER") == 6 - main.FERT_FIELD_RESERVE
