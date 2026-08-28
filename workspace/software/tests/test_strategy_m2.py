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


def test_last_day_liquidates_everything():
    orders = main._market_gates(29, _prices(), _shed(MILK=30, WHEAT=10,
                                                     FERTILIZER=8), 8)
    for item in ("MILK", "WHEAT", "FERTILIZER"):
        assert _orders_contains(orders, "SELL", item)


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
    assert main._herd_target(0, 99) == 4
    assert main._herd_target(8, 999) == main.HERD_CAP
    assert main._herd_target(8, 9) == 9        # feed capacity binds
    assert main._herd_target(25, 99) == main.HERD_CAP


def test_wheat_cap_grows_with_price():
    assert main._wheat_cap(1, 25) == 16
    assert main._wheat_cap(5, 25) == 18
    assert main._wheat_cap(5, 40) == 22        # dear wheat -> farm more


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
    main._note_buys(0, 5, 10, 2)
    assert main._buy_pace(0, 5, 11) == 2          # same episode, later hour
    assert main._buy_pace(0, 0, 0) == 0           # new episode clock
    main._STATE.clear()


def test_buy_pace_day_rollover():
    main._STATE.clear()
    main._note_buys(1, 3, 2, 2)
    assert main._buy_pace(1, 4, 0) == 0
    main._STATE.clear()


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
    # healthy milk: scaling resumes
    orders2 = _market_orders_with(private, animals=8, herd=8,
                                  prices=_prices(MILK=150), day=12, money=9000.0)
    assert _orders_contains(orders2, "BUY_ANIMAL", "COW")
