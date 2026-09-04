"""r4-P3 NPV dynamic-capital unit tests (campaign III round-3 P3).

Pins the capital-layer contract:
  * marginal-NPV herd ceiling: the 14-head plan EXTENDS toward 17 only
    when the calendar (evenings x margin > capex), the market (town
    absorbs >= 2x the species flow) and the feed line all clear -- and
    never accelerates the base plan (day-0 burst semantics intact);
  * land late cutoff: SW is not bought after LAND_LATE_CUTOFF;
  * crew drawdown: the 12-hand fib bill shrinks past CREW_LATE_DAY;
  * P4-lite terminal: an animal with no production evening, no held
    yield and day >= 26 is not fed (its wheat repays nothing).
"""

import importlib.util

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_r4p3", SUBMISSION_MAIN)
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


def test_npv_ceiling_extends_on_full_conditions():
    # day 12, healthy prices, town absorbing both flows, feed stocked
    demand = {"MILK": 13, "WOOL": 13}
    counts = {"COW": 9, "SHEEP": 7}
    assert main._npv_herd_ceiling(12, _prices(MILK=170, WOOL=210), 14,
                                  counts, demand, 40) == main.HERD_CAP_NPV


def test_npv_ceiling_blocks_on_weak_margin():
    # milk 120: margin 59 < 90 -> no expansion even with demand
    assert main._npv_herd_ceiling(12, _prices(MILK=120), 14,
                                  {"COW": 9, "SHEEP": 7},
                                  {"MILK": 13}, 40) == main.HERD_CAP


def test_npv_ceiling_blocks_without_absorption():
    # zero milk demand: scaling crashes the joint curve (r4-P2 lesson)
    assert main._npv_herd_ceiling(12, _prices(MILK=170), 14,
                                  {"COW": 9, "SHEEP": 7},
                                  {"MILK": 1}, 40) == main.HERD_CAP


def test_npv_ceiling_blocks_late_or_hungry():
    # day 17+: too few evenings repay the capex
    assert main._npv_herd_ceiling(17, _prices(MILK=200), 14,
                                  {"COW": 9, "SHEEP": 7},
                                  {"MILK": 13}, 40) == main.HERD_CAP
    # thin wheat system: the feed line cannot hold one more mouth
    assert main._npv_herd_ceiling(12, _prices(MILK=170), 14,
                                  {"COW": 9, "SHEEP": 7},
                                  {"MILK": 13}, 10) == main.HERD_CAP


def test_npv_ceiling_never_accelerates_the_base_plan():
    # the ceiling only lifts the target once the 14-head plan is DONE
    # (day-0 burst + r3 deadline semantics: _herd_target unchanged)
    assert main._herd_target(0, 99) == 4
    assert main._herd_target(8, 99) == main.HERD_CAP == 16
    assert main.HERD_CAP_NPV == 17


def _farm(money=9000.0, quads=("NW", "NE"), tiles=None):
    if tiles is None:
        def tile(x, y):
            quad = ("N" if y < 5 else "S") + ("W" if x < 5 else "E")
            return None if quad in quads else "LOCKED"
        tiles = [[tile(x, y) for x in range(10)] for y in range(10)]
    return {"money": money, "tiles": tiles, "farmer": [4, 4], "hands": [],
            "unlocked_quadrants": list(quads), "hires_today": 0}


def test_sw_land_not_bought_after_cutoff():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": main.LAND_LATE_CUTOFF + 3, "hour": 0,
           "market": {"prices": _prices()}, "town": {"unlocked_shops": []}}
    main._STATE.clear()
    orders = main._market_orders(obs, _farm(money=12000.0), private,
                                 main.LAND_LATE_CUTOFF + 3, 8, 8)
    assert not any(o[0] == "BUY_LAND" for o in orders)
    main._STATE.clear()


def test_sw_land_still_bought_in_the_window():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    obs = {"player": 0, "day": 7, "hour": 0,
           "market": {"prices": _prices()}, "town": {"unlocked_shops": []}}
    main._STATE.clear()
    orders = main._market_orders(obs, _farm(money=2800.0), private, 7, 2, 2)
    assert any(o[0] == "BUY_LAND" for o in orders)
    main._STATE.clear()


def test_crew_drawdown_past_late_day():
    # the plan-level target stays the r3 contract; the agent()-level
    # drawdown caps the DAWN hiring past CREW_LATE_DAY
    assert main._crew_target(12, 14, 18, 3) == 12      # r3 pin intact
    assert main.CREW_LATE_CAP < 12
    # simulate the agent's cap arithmetic directly
    hands_t = min(main._crew_target(26, 14, 18, 3), 12)
    if 26 >= main.CREW_LATE_DAY:
        hands_t = min(hands_t, main.CREW_LATE_CAP)
    assert hands_t == main.CREW_LATE_CAP


def _pasture(animal="COW", placed_day=0, yu=0):
    return {"kind": "PASTURE", "animal": animal, "placed_day": placed_day,
            "yield_units": yu, "consecutive_unfed": 0, "fed_today": False,
            "cared_today": False, "fertilizer_available": False}


def test_terminal_animal_not_fed_after_last_production_evening():
    # sheep placed d0 (evenings 5,8,...,26): day 27 no evening remains and
    # no held yield -> FEED task suppressed (P4-lite)
    tiles = [[("LOCKED" if not ((x < 5) and (y < 5)) else None)
              for x in range(10)] for y in range(10)]
    tiles[2][4] = _pasture("SHEEP", 0, yu=0)
    farm = _farm(tiles=tiles, quads=("NW",))
    private = {"shed": _shed(WHEAT=10), "seeds": {}, "inventories": [{}]}
    obs = {"player": 0, "day": 27, "hour": 6,
           "farms": [farm, _farm()], "private": private,
           "market": {"prices": _prices()}, "town": {"unlocked_shops": []}}
    tasks, to_feed, *_ = main._build_tasks(obs, farm, private, 27)
    assert not any(t["act"][0] == "FEED" for t in tasks)
    assert to_feed == 0
    # held yield still harvests on the terminal day
    tiles[2][4] = _pasture("SHEEP", 0, yu=4)
    obs2 = {"player": 0, "day": 27, "hour": 6,
            "farms": [farm, _farm()], "private": private,
            "market": {"prices": _prices()}, "town": {"unlocked_shops": []}}
    tasks2, *_ = main._build_tasks(obs2, farm, private, 27)
    assert any(t["act"][0] == "HARVEST" for t in tasks2)
