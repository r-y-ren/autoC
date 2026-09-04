"""m2 strategy-logic unit tests (dairy engine + selective-intervention gates).

Pure-function tests over the submittable main.py: milk gate schedule,
market-gate hold/release/defend semantics, herd/wheat planning caps, the
feed-buy phantom-shortfall guard, the buy-pace episode-state reset, and the
dawn hire burst.  These pin the behaviours measured in the m2 iteration log
(exports/logs/iteration_gate_log.jsonl) so regressions surface in pytest
before any arena run.
"""

import importlib.util
import json
import os

import pytest

from kgenv.arena import SUBMISSION_MAIN

spec = importlib.util.spec_from_file_location("main_m2", SUBMISSION_MAIN)
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


def _farm(tiles=None, money=5000.0, farmer=(4, 4), hands=(), quads=None):
    return {
        "money": money,
        "tiles": tiles or _nw_tiles(),
        "farmer": list(farmer),
        "hands": [list(hand) for hand in hands],
        "unlocked_quadrants": quads or ["NW"],
        "hires_today": 0,
    }


def _obs(day, hour, farm, private, player=0):
    other = _farm(money=3000.0)
    farms = [farm, other] if player == 0 else [other, farm]
    return {
        "player": player,
        "day": day,
        "hour": hour,
        "farms": farms,
        "private": private,
        "market": {"prices": _prices()},
    }


# --------------------------------------------------------------------------
# milk gate schedule
# --------------------------------------------------------------------------

def test_milk_gate_decays_late_season():
    gates = [main._milk_gate(d) for d in range(30)]
    assert gates[0] == gates[23] == 105
    assert gates[24] == 100 and gates[26] == 90 and gates[28] == 80
    assert all(gates[i] >= gates[i + 1] for i in range(23, 29))


# --------------------------------------------------------------------------
# selective-intervention market gates
# --------------------------------------------------------------------------

def test_milk_holds_below_gate():
    orders = main._market_gates(10, _prices(MILK=104), _shed(MILK=20), 8)
    assert not _orders_contains(orders, "SELL", "MILK")


def test_milk_releases_at_gate_band():
    orders = main._market_gates(10, _prices(MILK=110), _shed(MILK=20), 8)
    assert _orders_contains(orders, "SELL", "MILK")
    assert _order_qty(orders, "SELL", "MILK") == 20  # clear-through, cap 20


def test_milk_clears_hard_at_peak():
    orders = main._market_gates(9, _prices(MILK=180), _shed(MILK=26), 8)
    assert _order_qty(orders, "SELL", "MILK") == 24  # peak tranche cap


def test_milk_pressure_guard_drains_before_discard_cliff():
    # 78 shed items with 40 milk: drain to a working buffer even mid-band
    orders = main._market_gates(12, _prices(MILK=70), _shed(MILK=40, WHEAT=38), 8)
    assert _order_qty(orders, "SELL", "MILK") == 25


def test_market_gates_never_emit_zero_quantity_pressure_sell():
    orders = main._market_gates(12, _prices(MILK=70),
                                _shed(MILK=10, WHEAT=65), 8)
    assert not _orders_contains(orders, "SELL", "MILK")
    assert all(order[2] > 0 for order in orders if order[0] == "SELL")


def test_agent_never_emits_nonpositive_quantity_order():
    private = {"shed": _shed(MILK=10, WHEAT=65),
               "seeds": {"WHEAT": 10}, "inventories": [{}]}
    action = main.agent(_obs(12, 5, _farm(), private))
    quantity_orders = [order for order in action["market"] if len(order) == 3]
    assert quantity_orders
    assert all(order[2] > 0 for order in quantity_orders)


def test_last_day_liquidates_everything():
    orders = main._market_gates(29, _prices(), _shed(MILK=30, WHEAT=10,
                                                     FERTILIZER=8, CARROT=2,
                                                     EGG=3), 8)
    for item in ("MILK", "WHEAT", "FERTILIZER", "CARROT", "EGG"):
        assert _orders_contains(orders, "SELL", item)


def test_last_day_never_emits_capital_or_buy_orders():
    private = {"shed": _shed(MILK=4), "seeds": {"WHEAT": 0},
               "inventories": [{}]}
    action = main.agent(_obs(29, 0, _farm(money=10000.0), private))
    assert action["market"]
    assert all(order[0] == "SELL" for order in action["market"])


def test_last_day_carried_product_returns_and_sells_before_new_harvest():
    tiles = _nw_tiles()
    tiles[0][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 24,
                   "watered_today": True, "consecutive_unwatered": 0,
                   "yield_units": 4, "fertilized_until_day": -1}
    private = {"shed": _shed(), "seeds": {"WHEAT": 0},
               "inventories": [{"MILK": 3}]}
    action = main.agent(_obs(29, 10, _farm(tiles=tiles, farmer=(4, 4)), private))
    assert action["farmer"] == ["DROP"]
    assert ["SELL", "MILK", 3] in action["market"]
    assert action["farmer"] != ["HARVEST"]


def test_last_day_skips_harvest_that_cannot_return_to_shed_in_time():
    tiles = _nw_tiles()
    tiles[0][0] = {"kind": "PLANT", "crop": "WHEAT", "planted_day": 24,
                   "watered_today": True, "consecutive_unwatered": 0,
                   "yield_units": 4, "fertilized_until_day": -1}
    farm = _farm(tiles=tiles, farmer=(0, 0))
    private = {"shed": _shed(), "seeds": {"WHEAT": 0}, "inventories": [{}]}
    tasks, *_ = main._build_tasks(_obs(29, 22, farm, private), farm, private, 29)
    assert not any(task["act"][0] == "HARVEST" for task in tasks)


def test_last_day_return_task_stays_with_its_loaded_carrier():
    farm = _farm(farmer=(0, 0), hands=((4, 4),))
    private = {"shed": _shed(), "seeds": {"WHEAT": 0},
               "inventories": [{}, {"MILK": 2}]}
    obs = _obs(29, 10, farm, private)
    tasks, *_ = main._build_tasks(obs, farm, private, 29)
    actions = main._schedule_units(obs, farm, private, 29, tasks)
    assert actions == [["PASS"], ["DROP"]]


def test_fertilizer_hoard_is_bounded():
    # above the stock cap: sells down toward the field reserve even below gate
    orders = main._market_gates(10, _prices(FERTILIZER=40),
                                _shed(FERTILIZER=20), 8)
    assert _order_qty(orders, "SELL", "FERTILIZER") == 20 - main.FERT_FIELD_RESERVE


def test_fertilizer_releases_above_gate():
    orders = main._market_gates(10, _prices(FERTILIZER=80),
                                _shed(FERTILIZER=10), 8)
    assert _order_qty(orders, "SELL", "FERTILIZER") == 10 - main.FERT_FIELD_RESERVE


# --------------------------------------------------------------------------
# planning caps
# --------------------------------------------------------------------------

def test_herd_target_ramps_and_caps():
    assert main._herd_target(0, 99) == 3
    assert main._herd_target(8, 999) == main.HERD_CAP
    assert main._herd_target(8, 9) == 9        # feed capacity binds
    assert main._herd_target(25, 99) == main.HERD_CAP


def test_wheat_cap_grows_with_price():
    # v1.5 P0: d0-1 feed floor 10 so a single quadrant keeps melon room;
    # from d2 the 22/26 floor and dear-wheat bands are unchanged.
    assert main._wheat_cap(0, 25) == 10
    assert main._wheat_cap(1, 25) == 10
    assert main._wheat_cap(2, 25) == 22
    assert main._wheat_cap(5, 25) == 26
    assert main._wheat_cap(5, 40) == 30        # dear wheat -> farm more


# --------------------------------------------------------------------------
# feed-buy phantom-shortfall guard (measured -8k/season before the fix)
# --------------------------------------------------------------------------

def _nw_tiles():
    """10x10 board, NW quadrant unlocked and empty (25 farmable tiles)."""
    return [[(None if (x < 5 and y < 5) else "LOCKED") for x in range(10)]
            for y in range(10)]


def _market_orders_with(private, animals=6, herd=6, prices=None, day=8, money=5000.0):
    farm = {"money": money, "unlocked_quadrants": ["NW", "NE"], "tiles": _nw_tiles()}
    obs = {"player": 0, "day": day, "hour": 0, "market": {"prices": prices or _prices()}}
    main._STATE.clear()
    return main._market_orders(obs, farm, private, day, animals, herd)


def test_no_phantom_feed_buy_when_carriers_hold_wheat():
    private = {"shed": _shed(WHEAT=0),
               "seeds": {"WHEAT": 10},
               "inventories": [{"WHEAT": 9}, {}, {}, {}]}
    orders = _market_orders_with(private, animals=6)
    assert not _orders_contains(orders, "BUY_PRODUCT", "WHEAT")


def test_feed_buy_triggers_on_true_system_shortfall():
    private = {"shed": _shed(WHEAT=0),
               "seeds": {"WHEAT": 10},
               "inventories": [{}, {}, {}]}
    orders = _market_orders_with(private, animals=6)
    assert _orders_contains(orders, "BUY_PRODUCT", "WHEAT")


# --------------------------------------------------------------------------
# buy-pace episode state
# --------------------------------------------------------------------------

def test_buy_pace_resets_across_episodes():
    main._STATE.clear()
    assert main._buy_pace(0, 5, 10, 4) == 0
    main._note_buy_order(0, 5, 10, 2)
    assert main._buy_pace(0, 5, 11, 6) == 2       # actual herd delta confirms
    assert main._buy_pace(0, 0, 0, 0) == 0        # new episode clock
    main._STATE.clear()


def test_buy_pace_day_rollover():
    main._STATE.clear()
    assert main._buy_pace(1, 3, 2, 5) == 0
    main._note_buy_order(1, 3, 2, 2)
    assert main._buy_pace(1, 4, 0, 7) == 0
    main._STATE.clear()


def test_failed_buy_order_does_not_consume_daily_pace():
    main._STATE.clear()
    assert main._buy_pace(0, 5, 0, 4) == 0
    main._note_buy_order(0, 5, 0, 2)
    assert main._buy_pace(0, 5, 1, 4) == 0        # order failed: no cow delta
    main._note_buy_order(0, 5, 1, 2)
    assert main._buy_pace(0, 5, 2, 6) == 2        # retry succeeded
    main._STATE.clear()


def test_buy_confirmation_state_isolated_by_seat_and_episode():
    main._STATE.clear()
    assert main._buy_pace(0, 2, 0, 4) == 0
    assert main._buy_pace(1, 2, 0, 7) == 0
    main._note_buy_order(0, 2, 0, 2)
    main._note_buy_order(1, 2, 0, 1)
    assert main._buy_pace(0, 2, 1, 6) == 2
    assert main._buy_pace(1, 2, 1, 7) == 0
    assert main._buy_pace(0, 0, 0, 0) == 0
    assert main._buy_pace(1, 0, 0, 0) == 0
    main._STATE.clear()


def test_pickup_tasks_reserve_shed_inventory_across_carriers():
    tiles = _nw_tiles()
    for x, y in ((3, 3), (2, 3), (3, 2), (1, 3), (3, 1), (2, 2), (1, 2)):
        tiles[y][x] = {"kind": "PASTURE", "animal": "COW", "placed_day": 10,
                       "yield_units": 0, "consecutive_unfed": 0,
                       "fed_today": False, "cared_today": False,
                       "fertilizer_available": False}
    farm = _farm(tiles=tiles, hands=((5, 4), (4, 5), (5, 5)))
    private = {"shed": _shed(WHEAT=6), "seeds": {"WHEAT": 0},
               "inventories": [{}, {}, {}, {}]}
    tasks, *_ = main._build_tasks(_obs(12, 0, farm, private), farm, private, 12)
    pickups = [task["act"] for task in tasks if task["act"][:2] == ["PICKUP", "WHEAT"]]
    assert len(pickups) == 2
    assert sum(action[2] for action in pickups) == 6
    assert all(action[2] > 0 for action in pickups)


# --------------------------------------------------------------------------
# dawn hire burst (measured: one-per-turn left us at 3 hands vs plan 5)
# --------------------------------------------------------------------------

def _first_obs_from_engine(seed=5):
    from kgenv.gym_env import KaggricultureGym
    env = KaggricultureGym(opponent="pass", episode_steps=48)
    return env.reset(seed=seed)


def test_dawn_hire_burst_up_to_plan():
    obs = json.loads(json.dumps(_first_obs_from_engine()))
    obs["day"] = 12
    farm = obs["farms"][0]
    farm["hands"] = []
    farm["money"] = 5000.0
    obs["hour"] = 0
    main._STATE.clear()
    action = main.agent(obs)
    hires = [o for o in action["market"] if o[0] == "HIRE"]
    assert len(hires) >= 2       # burst, not one-per-turn
    main._STATE.clear()


def test_no_hire_after_dawn_window():
    obs = json.loads(json.dumps(_first_obs_from_engine()))
    obs["day"] = 12
    obs["hour"] = 5
    farm = obs["farms"][0]
    farm["hands"] = []
    farm["money"] = 5000.0
    main._STATE.clear()
    action = main.agent(obs)
    assert not [o for o in action["market"] if o[0] == "HIRE"]
    main._STATE.clear()


# --------------------------------------------------------------------------
# demand-drought herd freeze
# --------------------------------------------------------------------------

def test_herd_freezes_when_milk_collapses():
    private = {"shed": _shed(), "seeds": {"WHEAT": 10}, "inventories": [{}]}
    # milk crashed to 40: target must not exceed the current herd
    orders = _market_orders_with(private, animals=8, herd=8,
                                 prices=_prices(MILK=40), day=12, money=9000.0)
    assert not _orders_contains(orders, "BUY_ANIMAL", "COW")
    # healthy milk + an absorbing town (r4-P2: scale-up requires the town
    # to eat the flow): scaling resumes above the m2b 90-floor
    farm = _farm(money=9000.0, quads=["NW", "NE"])
    obs = {"player": 0, "day": 12, "hour": 0,
           "market": {"prices": _prices(MILK=150)},
           "town": {"unlocked_shops": ["PIZZA_SHOP", "SMOOTHIE_SHOP"]}}
    main._STATE.clear()
    orders2 = main._market_orders(obs, farm, private, 12, 8, 8)
    assert _orders_contains(orders2, "BUY_ANIMAL", "COW")
