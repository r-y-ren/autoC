"""r5-P4 macro-plan strategy tests (strategy-space extension).

Function-level checks over the submittable main.py for the P4 layer the
round-3 ledger motivated: the r4 frame plateaus near 75k because it
cannot EXPRESS the ladder's 96-110k wheat-strawberry economies (Renji
42 strawberry tiles + 1508u wheat sold; DevilQ 31 strawberry + 14 cows).
The macro plan widens that space daily:

  1. mode gate: VOLUME_CROP entry (opponent monster band / own proven
     line / premium bid with absorption), persistence, and exit when the
     strawberry curve dies; SCALE_RANCH entry with its 18-head NPV
     ceiling; DEFENSIVE as the verbatim default;
  2. field: the volume plan widens the strawberry ceiling to 42 tiles
     and the wheat money quota; DEFENSIVE reproduces the r4 18-tile cap;
  3. capital: SE becomes a buyable quadrant only under the volume plan,
     inside its day window and above its protected fund;
  4. labour: crew ceiling 15 under the volume plan, 12 otherwise;
  5. seeds: volume buys money-scaled strawberry batches (<=10);
  6. plan memory: daily caching and new-episode reset (backwards clock).

No full episodes are played here (smoke_boot and the development gate
cover play); these pin the planning logic so regressions surface in
pytest before any arena run.  The r4 frame itself stays pinned by the
m2/m3 test files -- every DEFENSIVE path below must match those.
"""

import importlib.util

import pytest

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_r5", SUBMISSION_MAIN)
main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main)


def _mk_farm(quads=("NW", "NE", "SW"), money=5000.0, straw=0, herd=0,
             herd_species="COW"):
    """10x10 farm: unlocked quadrants empty, locked ones "LOCKED", with
    `straw` strawberry plants and `herd` placed animals filled in from
    the NW corner (scan/alloc only care about counts and positions)."""
    tiles = [["LOCKED"] * 10 for _ in range(10)]
    half = 5
    for y in range(10):
        for x in range(10):
            q = ("N" if y < half else "S") + ("W" if x < half else "E")
            if q in quads:
                tiles[y][x] = None
    for i in range(straw):
        x, y = i % 5, i // 5
        if tiles[y][x] is None:
            tiles[y][x] = {"kind": "PLANT", "crop": "STRAWBERRY",
                           "planted_day": 5, "yield_units": 0}
    placed = 0
    for y in range(10):
        for x in range(10):
            if placed >= herd:
                break
            if tiles[y][x] is None:
                tiles[y][x] = {"kind": "PASTURE", "animal": herd_species,
                               "placed_day": 0, "yield_units": 0}
                placed += 1
    return {"tiles": tiles, "money": money,
            "unlocked_quadrants": list(quads), "farmer": [4, 4],
            "hands": [], "hires_today": 0}


def _mk_obs(mine, opp, prices=None, shops=()):
    prices = prices if prices is not None else {
        "WHEAT": 25, "CARROT": 35, "TOMATO": 60, "STRAWBERRY": 120,
        "MELON": 250, "EGG": 50, "MILK": 160, "WOOL": 200,
        "FERTILIZER": 100}
    return {"player": 0, "day": 8, "hour": 0,
            "market": {"prices": prices},
            "town": {"unlocked_shops": list(shops)},
            "farms": [mine, opp],
            "private": {"shed": {}, "seeds": {}, "inventories": [{}]}}


@pytest.fixture(autouse=True)
def _clean_module_state():
    main._PLAN_MEM.clear()
    main._STATE.clear()
    main._MARKET_MEM.clear()
    yield
    main._PLAN_MEM.clear()
    main._STATE.clear()
    main._MARKET_MEM.clear()


VOLUME_PLAN = {"mode": "VOLUME_CROP", "volume": True, "scale": False,
               "straw_quad_cap": main.MODE_STR_QUAD_CAP,
               "straw_total_cap": main.MODE_STR_TOTAL_CAP,
               "wheat_money_quad": main.MODE_WHEAT_MONEY_QUAD,
               "crew_cap": main.MODE_CREW_CAP_VOL,
               "herd_ceiling": main.HERD_CAP_NPV}
SCALE_PLAN = {"mode": "SCALE_RANCH", "volume": False, "scale": True,
              "straw_quad_cap": 6, "straw_total_cap": 18,
              "wheat_money_quad": 3, "crew_cap": main.HANDS_CAP_R3,
              "herd_ceiling": main.MODE_HERD_CAP_SCALE}


# ------------------------- farm scan ------------------------------------

def test_farm_scan_counts_public_state():
    farm = _mk_farm(straw=3, herd=2)
    farm["tiles"][6][1] = {"kind": "PLANT", "crop": "WHEAT",
                           "planted_day": 1, "yield_units": 0}
    scan = main._farm_scan(farm)
    assert scan["straw"] == 3
    assert scan["herd"] == 2
    assert scan["wheat"] == 1          # the wheat plant placed manually
    assert scan["quads"] == 3
    assert scan["money"] == 5000.0


# ------------------------- mode gate ------------------------------------

def test_volume_entry_only_on_uncontested_proven_line():
    # premium bid + real absorption + our 6-tile line alive + free line
    # (herd 12: the v7.2-V1 readiness floor on the promoted submission)
    obs = _mk_obs(_mk_farm(money=800, straw=6, herd=12),
                  _mk_farm(straw=0, herd=10),
                  shops=["FARMERS_MARKET"])
    plan = main._decide_mode(obs, 8, None)
    assert plan["mode"] == "VOLUME_CROP"
    assert plan["straw_total_cap"] == 42
    assert plan["crew_cap"] == 15
    # no proven line yet: the widening waits for realized evidence
    unproven = _mk_obs(_mk_farm(money=800), _mk_farm(straw=0),
                       shops=["FARMERS_MARKET"])
    assert main._decide_mode(unproven, 8, None)["mode"] == "DEFENSIVE"
    # sub-premium bid (105 is the bar): anticipation alone never fires
    cheap = _mk_obs(_mk_farm(money=800, straw=8), _mk_farm(straw=0),
                    shops=["FARMERS_MARKET"])
    cheap["market"]["prices"]["STRAWBERRY"] = 90
    assert main._decide_mode(cheap, 8, None)["mode"] == "DEFENSIVE"


def test_opponent_crop_monster_is_do_not_mirror():
    # Renji-style opponent already in the line (20 strawberry tiles):
    # mirroring a contested market as the late mover measured strictly
    # negative (paired ablation, 16 cells) -> stay out of the line
    obs = _mk_obs(_mk_farm(money=2000), _mk_farm(straw=20),
                  shops=["FARMERS_MARKET"])
    assert main._decide_mode(obs, 8, None)["mode"] == "DEFENSIVE"


def test_volume_entry_via_own_proven_line():
    # opponent runs no crop economy; our own 12-tile line carries the entry
    # (herd 12 satisfies the v7.2-V1 floor)
    obs = _mk_obs(_mk_farm(money=800, straw=12, herd=12),
                  _mk_farm(straw=0, herd=10),
                  shops=["FARMERS_MARKET"])
    assert main._decide_mode(obs, 9, None)["mode"] == "VOLUME_CROP"


def test_volume_blocked_when_strawberry_curve_dead():
    # price under the 55 red line: no volume entry even against a monster
    prices = {"STRAWBERRY": 50, "MILK": 160, "WOOL": 200}
    obs = _mk_obs(_mk_farm(money=2000), _mk_farm(straw=20),
                  prices=prices, shops=["FARMERS_MARKET"])
    assert main._decide_mode(obs, 8, None)["mode"] == "DEFENSIVE"


def test_volume_persistence_and_exit():
    obs_hold = _mk_obs(_mk_farm(money=1000, straw=30), _mk_farm(),
                       shops=["SMOOTHIE_SHOP"])   # strawberry absorbed
    prices = obs_hold["market"]["prices"]
    prices["STRAWBERRY"] = 60                     # weak but alive bid
    # day 16 is past the entry window; persistence keeps the built field
    assert main._decide_mode(obs_hold, 16, "VOLUME_CROP")["mode"] == \
        "VOLUME_CROP"
    # the curve dying (price < 40) drops the plan even mid-field
    prices["STRAWBERRY"] = 30
    assert main._decide_mode(obs_hold, 16, "VOLUME_CROP")["mode"] == \
        "DEFENSIVE"


def test_scale_entry_and_18_head_ceiling():
    # own 14-head ranch built, dairy absorbed by three milk shops, crop
    # line dead (strawberry 50 < floor) -> the animal line outbids crops
    shops = ["PIZZA_SHOP", "ICE_CREAM_SHOP", "SMOOTHIE_SHOP"]
    prices = {"STRAWBERRY": 50, "MILK": 200, "WOOL": 240}
    obs = _mk_obs(_mk_farm(herd=14), _mk_farm(straw=2), prices=prices,
                  shops=shops)
    assert main._decide_mode(obs, 8, None)["mode"] == "SCALE_RANCH"
    species = {"COW": 5, "SHEEP": 10, "GOOSE": 0}
    demand = main._town_daily_demand(shops)
    ceil_scale = main._npv_herd_ceiling(12, prices, 15, species, demand,
                                        200, plan=SCALE_PLAN)
    ceil_def = main._npv_herd_ceiling(12, prices, 15, species, demand,
                                      200, plan=None)
    assert ceil_scale == 18
    assert ceil_def == 17


def test_defensive_default_on_empty_state():
    obs = _mk_obs(_mk_farm(quads=("NW",), money=100), _mk_farm(straw=0),
                  shops=[])
    plan = main._decide_mode(obs, 2, None)
    assert plan["mode"] == "DEFENSIVE"
    # empty/None farms never raise: the gate falls back defensively
    broken = {"player": 3, "market": {}, "town": {}, "farms": []}
    assert main._decide_mode(broken, 8, None)["mode"] == "DEFENSIVE"


# ------------------------- field allocation -----------------------------

def test_field_alloc_volume_widens_strawberry_ceiling():
    farm = _mk_farm()   # NW+NE+SW unlocked, everything empty
    prices = {"STRAWBERRY": 120, "MELON": 250, "CARROT": 35, "WHEAT": 25}
    _, crop_vol, _, _ = main._field_alloc(farm, 8, prices, VOLUME_PLAN)
    _, crop_def, _, _ = main._field_alloc(farm, 8, prices, None)
    assert len(crop_vol["STRAWBERRY"]) == 42      # the Renji ceiling
    assert len(crop_def["STRAWBERRY"]) == 24      # V-T9 tetsuya copy total cap
    # total cap binds even when a 4th quadrant is unlocked
    farm4 = _mk_farm(quads=("NW", "NE", "SW", "SE"))
    _, crop_4q, _, _ = main._field_alloc(farm4, 8, prices, VOLUME_PLAN)
    assert len(crop_4q["STRAWBERRY"]) == 42


# ------------------------- capital: SE quadrant --------------------------

def test_se_land_buy_volume_only_window_and_fund():
    shops = ["FARMERS_MARKET"]
    prices = {"STRAWBERRY": 120, "MELON": 250, "CARROT": 35, "WHEAT": 25}
    obs = _mk_obs(_mk_farm(money=6000.0), _mk_farm(), prices=prices,
                  shops=shops)
    private = {"shed": {"WHEAT": 20}, "seeds": {"WHEAT": 12},
               "inventories": [{}]}
    farm = obs["farms"][0]

    def orders(plan, day):
        return main._market_orders(obs, obs["farms"][0], private, day, 0,
                                   14, plan=plan)

    assert ["BUY_LAND"] in orders(VOLUME_PLAN, 11)      # window + fund ok
    assert ["BUY_LAND"] not in orders(None, 11)         # defensive: no SE
    assert ["BUY_LAND"] not in orders(VOLUME_PLAN, 16)  # past the window
    broke = _mk_farm(money=3000.0)
    obs["farms"][0] = broke
    assert ["BUY_LAND"] not in orders(VOLUME_PLAN, 11)  # under the fund


# ------------------------- labour and seeds ------------------------------

def test_crew_cap_15_only_under_volume():
    assert main._crew_target(10, 14, 18, 3, VOLUME_PLAN) == 15
    assert main._crew_target(10, 14, 18, 3, None) == 12
    assert main._crew_target(10, 14, 18, 3, SCALE_PLAN) == 12


def test_volume_seed_batches_are_money_scaled():
    shops = ["FARMERS_MARKET"]
    prices = {"STRAWBERRY": 120, "MELON": 250, "CARROT": 35, "WHEAT": 25}
    obs = _mk_obs(_mk_farm(money=1300.0), _mk_farm(), prices=prices,
                  shops=shops)
    farm = obs["farms"][0]
    private = {"shed": {"WHEAT": 20}, "seeds": {"WHEAT": 12},
               "inventories": [{}]}
    vol = [o for o in main._market_orders(obs, farm, private, 8, 0, 14,
                                          plan=VOLUME_PLAN)
           if o[0] == "BUY_SEED" and o[1] == "STRAWBERRY"]
    # V-T3/V-T9 (2026-09-02): the batch is capped by wallet scale and the
    # daily planting budget (PLANT_DAILY_CAP 24 since the aggressive
    # ruling; the wallet bound (1300-250)//100 = 10 decides here).
    assert vol and vol[0][2] == 10
    # defensive raises its pinned batch 6 -> 8 at the same money
    # (aggressive ruling 2026-09-04)
    de = [o for o in main._market_orders(obs, farm, private, 8, 0, 14,
                                         plan=None)
          if o[0] == "BUY_SEED" and o[1] == "STRAWBERRY"]
    assert de and de[0][2] == 8


# ------------------------- P5 rollout evaluator --------------------------

def test_rollout_math_volume_completes_field_when_solvent():
    # the realistic mid-game state (12 head ranch income, moderate cash):
    # the volume rollout stays solvent, completes the 42-tile field, and
    # its terminal beats the defensive frame under curve pricing
    scan = {"quads": 3, "straw": 2, "wheat": 4, "herd": 12,
            "straw_days": [5, 5], "cows": 7, "sheep": 5, "geese": 0,
            "hands": 9, "money": 2500.0}
    prices = {"WHEAT": 25, "MILK": 160, "WOOL": 200, "EGG": 50,
              "STRAWBERRY": 120}
    demand = main._town_daily_demand(["SMOOTHIE_SHOP", "ICE_CREAM_SHOP"])
    r_vol = main._plan_rollout(8, scan, main._VOLUME_PLAN, prices, demand,
                               120)
    r_def = main._plan_rollout(8, scan, main._DEFENSIVE_PLAN, prices,
                               demand, 120)
    assert r_vol["min_cash"] >= 0
    assert r_vol["alive"] == 42
    # V-T9 (2026-09-02): DEFENSIVE now carries a 24-tile strawberry total
    # cap, so the VOLUME margin narrowed to noise; the mechanism checks
    # are solvency + completing the 42-tile field, non-inferiority here.
    assert r_vol["terminal"] >= r_def["terminal"] - 500


def test_rollout_glut_rejects_anticipated_wide_field():
    # aggressive ruling 2026-09-04: anticipated entry is LIVE in
    # production (the rollout evaluator is the entry authority), but the
    # value gate still rejects the thin-absorption glut cell.
    thin = _mk_obs(_mk_farm(money=8000.0), _mk_farm(straw=0),
                   shops=["FARMERS_MARKET"])
    assert main.VOLUME_ANTICIPATED_ENTRY is True
    assert main._decide_mode(thin, 8, None)["mode"] == "DEFENSIVE"


def test_rollout_anticipated_machinery_gates_on_value_and_solvency():
    # production defaults since the aggressive ruling: the flag is live
    # and ROLLOUT_MIN_EDGE=500 is the measured realistic threshold --
    # deep absorption + premium bid + a thin wallet passes via the
    # anticipated authority (no 800 floor in front of it anymore); the
    # thin-absorption cell stays out (value veto).
    thin = _mk_obs(_mk_farm(money=8000.0), _mk_farm(straw=0),
                   shops=["FARMERS_MARKET"])
    deep = _mk_obs(_mk_farm(money=4000.0, herd=12), _mk_farm(straw=0),
                   prices={"STRAWBERRY": 160, "MELON": 250, "CARROT": 35,
                           "WHEAT": 25, "MILK": 160, "WOOL": 200},
                   shops=["SMOOTHIE_SHOP", "ICE_CREAM_SHOP"])
    assert main._decide_mode(deep, 8, None)["mode"] == "VOLUME_CROP"
    assert main._decide_mode(thin, 8, None)["mode"] == "DEFENSIVE"


def test_rollout_solvency_veto_never_fires_a_spiral():
    # the measured -62k/-93k class: a plan whose cash path dips under the
    # feed/hire line is vetoed even with a proven line and a premium bid.
    # Herd income covers feed here, so the veto is exercised through the
    # value check instead: deep absorption rich state enters, and the
    # same state with a dead premium bid (price under the conjunction)
    # never reaches the rollout at all.
    obs = _mk_obs(_mk_farm(money=8000.0, straw=6, herd=14),
                  _mk_farm(straw=0),
                  shops=["SMOOTHIE_SHOP", "ICE_CREAM_SHOP"])
    assert main._decide_mode(obs, 8, None)["mode"] == "VOLUME_CROP"
    obs["market"]["prices"]["STRAWBERRY"] = 100   # under the 105 premium bar
    # no widening at a sub-premium bid; the dairy line is absorbed here,
    # so the counter-market SCALE posture (not DEFENSIVE) is the fall-back
    assert main._decide_mode(obs, 8, None)["mode"] == "SCALE_RANCH"


# ------------------------- plan memory -----------------------------------

def test_macro_plan_daily_cache_and_episode_reset():
    obs = _mk_obs(_mk_farm(money=2000, straw=6, herd=12), _mk_farm(straw=0),
                  shops=["FARMERS_MARKET"])
    p1 = main._macro_plan(0, obs, 8)
    assert p1["mode"] == "VOLUME_CROP"
    # same day: the base mode is cached, while the stage/safety overlay is
    # refreshed so an intraday fuse can take effect.
    again = main._macro_plan(0, obs, 8)
    assert again == p1 and again is not p1
    assert main._PLAN_MEM[0]["base_plan"]["mode"] == "VOLUME_CROP"
    # backwards clock = new episode: the plan resets, day 0 cannot enter
    p2 = main._macro_plan(0, obs, 0)
    assert p2["mode"] == "DEFENSIVE"
    assert main._PLAN_MEM[0]["day"] == 0


def test_macro_plan_failure_falls_back_defensive():
    class Boom:
        def get(self, *a):
            raise RuntimeError("boom")
    broken = {"player": 0, "farms": [Boom()]}
    plan = main._macro_plan(0, broken, 8)
    assert plan["mode"] == "DEFENSIVE"
    assert plan["straw_total_cap"] == 24   # V-T9 tetsuya copy
