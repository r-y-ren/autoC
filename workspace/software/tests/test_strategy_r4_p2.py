"""r4-P2 shop-conditional market-control unit tests (campaign III round 3).

Pins the P2 layer contract:
  * town demand model: shop draws 6x/day (12+1 for a single-product shop,
    7 for each product of a multi-product shop, 1 base for the center);
  * analytic price engine: the embedded MARKET_PARAMS mirror reproduces
    the official market_price on the inversion round-trip;
  * dump-rate limiting: tranches cap at 2*D + 4 when the town is known,
    and stay UNcapped for the legacy 4-argument call (r3 semantics);
  * three-mode rule: yarn-absorbed wool HOLDS below the gate; zero-
    absorption wool cut-losses on a measured dying flow; liquidity and
    overflow pressure release small tranches at 0.5-0.6 base;
  * demand-conditioned scale-up: species buys need an absorbing shop to
    run the m2b 90-floor; zero-absorption markets freeze below ~base.
"""

import importlib.util

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_r4p2", SUBMISSION_MAIN)
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


def _qty(orders, item):
    for o in orders:
        if o[0] == "SELL" and o[1] == item:
            return o[2]
    return 0


# -------------------------------------------------------------------------- #
# town demand model
# -------------------------------------------------------------------------- #

def test_yarn_store_absorbs_13_wool_per_day():
    d = main._town_daily_demand(["YARN_STORE"])
    assert d["WOOL"] == 13            # 6 draws x 2 + center 1
    assert d["MILK"] == 1             # center only


def test_multi_product_shop_absorbs_7_per_product():
    d = main._town_daily_demand(["SMOOTHIE_SHOP"])
    assert d["STRAWBERRY"] == 7       # 6 x 1 + 1
    assert d["MILK"] == 7


def test_no_shops_leaves_center_only_demand():
    d = main._town_daily_demand([])
    for item in main.BASE_PRICE:
        if item != "FERTILIZER":
            assert d[item] == 1
    assert d.get("FERTILIZER", 0) == 0


# -------------------------------------------------------------------------- #
# analytic price engine
# -------------------------------------------------------------------------- #

def test_price_offset_roundtrip_matches_official_curves():
    from kaggle_environments.envs.kaggriculture.kaggriculture import market_price as _mp
    ok = 0
    for item, params in main.MARKET_PARAMS_EMB.items():
        for off in (-400, -100, -10, 0, 10, 60, 200):
            mine = round(main._price_at_offset(item, off))
            official = _mp(item, main.MARKET_I0_EMB + off)
            assert abs(mine - official) <= 1, (item, off, mine, official)
            # inversion round-trip: price -> offset -> price
            back = main._offset_from_price(item, official)
            assert abs(main._price_at_offset(item, back) - official) <= 2, \
                (item, off, official, back)
            ok += 1
    assert ok >= 60


def test_project_price_extrapolates_flow():
    # wool at 200 (offset 0) with +2 units/day glut: 7 days out the sq
    # curve sits below today
    assert main._project_price("WOOL", 200, 2.0, 7) < 200
    # wool at 200 with town eating 5/day: scarcity side, price rises
    assert main._project_price("WOOL", 200, -5.0, 7) > 200


def test_market_flow_ema_accumulates_across_days():
    main._MARKET_MEM.clear()
    f0 = main._market_flow(0, 10, _prices(MILK=160))
    assert f0 == {}                        # first day: baseline only
    f1 = main._market_flow(0, 11, _prices(MILK=150))
    assert f1.get("MILK", 0) > 0           # price fell -> glut flow positive
    f2 = main._market_flow(0, 12, _prices(MILK=150))
    assert abs(f2.get("MILK", 0)) < f1["MILK"]   # EMA decays on a flat day


# -------------------------------------------------------------------------- #
# dump-rate limiter and the three-mode rule
# -------------------------------------------------------------------------- #

def test_tranche_capped_to_town_absorption():
    # milk at the peak band with 26 held, no shop demand beyond the center:
    # the tranche must not exceed 2*D + 4 = 6
    orders = main._market_gates(9, _prices(MILK=180), _shed(MILK=26), 8,
                                town_shops=[], money=9000.0, flow={})
    assert _qty(orders, "MILK") == 6
    # legacy call (no town info): r3 semantics, cap 24
    orders_legacy = main._market_gates(9, _prices(MILK=180), _shed(MILK=26), 8)
    assert _qty(orders_legacy, "MILK") == 24


def test_absorbed_wool_holds_below_gate():
    # yarn store drawn, wool 130 < gate 150: hold (town mean-reverts)
    orders = main._market_gates(12, _prices(WOOL=130), _shed(WOOL=20), 8,
                                town_shops=["YARN_STORE"], money=9000.0,
                                flow={})
    assert _qty(orders, "WOOL") == 0


def test_zero_absorption_wool_cuts_on_dying_flow():
    # no yarn store, price 120, measured glut flow +3/day: the 7-day
    # projection is below today -> realize before the sq cliff
    orders = main._market_gates(12, _prices(WOOL=120), _shed(WOOL=20), 8,
                                town_shops=["BAKERY"], money=9000.0,
                                flow={"WOOL": 3.0})
    assert _qty(orders, "WOOL") > 0


def test_liquidity_pressure_releases_small_milk_tranche():
    orders = main._market_gates(12, _prices(MILK=85), _shed(MILK=12), 8,
                                town_shops=[], money=800.0, flow={})
    assert 0 < _qty(orders, "MILK") <= 6


def test_overflow_pressure_releases_premium_tranche():
    # shed 87 near the discard cliff at a soft bid: goods must LEAVE the
    # shed (the m2b discard-cliff guard clears down toward a buffer)
    shed = _shed(STRAWBERRY=30, WHEAT=57)
    orders = main._market_gates(12, _prices(STRAWBERRY=75), shed, 8,
                                town_shops=[], money=9000.0, flow={})
    assert _qty(orders, "STRAWBERRY") > 0


# -------------------------------------------------------------------------- #
# demand-conditioned scale-up
# -------------------------------------------------------------------------- #

def _farm(money=9000.0, quads=("NW", "NE")):
    def tile(x, y):
        quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
        return None if quad in quads else "LOCKED"
    return {"money": money,
            "tiles": [[tile(x, y) for x in range(10)] for y in range(10)],
            "farmer": [4, 4], "hands": [], "unlocked_quadrants": list(quads),
            "hires_today": 0}


def test_species_buy_frozen_below_base_without_absorption():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": 12, "hour": 0,
           "market": {"prices": _prices(WOOL=150)},
           "town": {"unlocked_shops": ["BAKERY"]}}   # no wool shop
    main._STATE.clear()
    orders = main._market_orders(obs, _farm(), private, 12, 0, 0)
    assert not any(o[0] == "BUY_ANIMAL" and o[1] == "SHEEP" for o in orders)
    main._STATE.clear()


def test_species_buy_resumes_with_absorbing_shop():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": 12, "hour": 0,
           "market": {"prices": _prices(WOOL=150)},
           "town": {"unlocked_shops": ["YARN_STORE"]}}
    main._STATE.clear()
    orders = main._market_orders(obs, _farm(), private, 12, 0, 0)
    assert any(o[0] == "BUY_ANIMAL" and o[1] == "SHEEP" for o in orders)
    main._STATE.clear()
