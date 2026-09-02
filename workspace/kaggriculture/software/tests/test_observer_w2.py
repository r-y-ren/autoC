"""W2 observer tests (opp_supply_observer_design.md v2, OBS stage).

Covers: the OBSERVER_ENABLED flag gating every footprint (V1-style:
flag-off == hooks-stubbed-off, byte-identical actions), the Ch0->flow
seamless switch (integer flow published under _market_flow's shape), the
E1/E6 floor-sell dual ledger, warm-up suppression, the unlock-day absorb
window (E3), est_opp_supply_horizon's real form, the V0-frozen confidence
caps, the snapshot/reset API, and the validator's pure scoring.
"""
import importlib
import json
import os
import sys

SOFTWARE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE, "kaggle_simulations", "agent"))
sys.path.insert(0, SOFTWARE)

main = importlib.import_module("main")

from kgenv.engine import run_episode  # noqa: E402


def _obs(day, inv, prices, shops, player=0, private=None, opp_money=3000.0):
    farms = [{"tiles": [[None] * 5 for _ in range(5)],
              "money": 3000.0, "hands": [], "farmer": [2, 2],
              "unlocked_quadrants": ["NW"]},
             {"tiles": [[None] * 5 for _ in range(5)],
              "money": opp_money, "hands": [], "farmer": [2, 2],
              "unlocked_quadrants": ["NW"]}]
    return {"player": player, "day": day, "hour": 0, "farms": farms,
            "market": {"inventory": dict(inv), "prices": dict(prices)},
            "town": {"unlocked_shops": list(shops)},
            "private": private or {}}


ITEMS = ("WHEAT", "MILK", "WOOL", "EGG", "STRAWBERRY", "MELON", "CARROT",
         "FERTILIZER")


def _inv(**over):
    base = {i: 10000 for i in ITEMS}
    base.update(over)
    return base


def _prices(**over):
    base = {i: 100 for i in ITEMS}
    base.update(over)
    return base


def _reset():
    main._OPP_OBSERVER.clear()
    main._MARKET_MEM.clear()
    main.reset_observer()
    main.OBSERVER_ENABLED = True


# --------------------------------------------------------------------------
# V1-style: the flag gates the observer's ENTIRE footprint
# --------------------------------------------------------------------------

def test_flag_off_equals_hooks_stubbed_off():
    main._OPP_OBSERVER.clear()
    main._MARKET_MEM.clear()
    main._STATE.clear()
    main._ROUTE_STATE.clear()
    main._TARGETS.clear()
    main._PLAN_MEM.clear()
    main._STAGE_MEM.clear()
    main._MISSION_SHADOW.clear()
    main._SELL_PLAN_MEM.clear()
    main._INTERFERENCE_MEM.clear()
    del main._INTERFERENCE_LOG[:]
    main.OBSERVER_ENABLED = False

    def run_and_collect():
        actions = []

        def wrapped(obs):
            action = main.agent(obs)
            actions.append(json.dumps(action, sort_keys=True))
            return action

        run_episode(wrapped, wrapped, 7, episode_steps=96)
        return actions

    baseline = run_and_collect()

    real_update = main._opp_observer_update
    real_note = main._opp_note_orders
    main._opp_observer_update = lambda *a, **k: None
    main._opp_note_orders = lambda *a, **k: None
    try:
        stubbed = run_and_collect()
    finally:
        main._opp_observer_update = real_update
        main._opp_note_orders = real_note
        main.OBSERVER_ENABLED = True
    assert baseline == stubbed            # zero residue when disabled
    assert len(baseline) > 90


# --------------------------------------------------------------------------
# Ch0 seamless switch / dual ledger / warm-up / E3 window
# --------------------------------------------------------------------------

def test_ch0_flow_published_and_read_by_market_flow():
    _reset()
    # day 0: warm-up pass (snapshots only, no flow)
    main._opp_observer_update(_obs(0, _inv(), _prices(), ["SMOOTHIE_SHOP"]),
                              {})
    assert main._market_flow(0, 0, _prices()) == {}
    # day 1: WE sell 3 MILK above floor; MILK inventory drops by
    # 3 (our sells) + 7 (SMOOTHIE is a MULTI-item shop: 6 draws x 1 MILK
    # + center 1) = 10
    main._opp_note_orders(0, 0, 23, [["SELL", "MILK", 3]],
                          _prices(MILK=160))
    inv1 = _inv(MILK=10000 - 4, STRAWBERRY=10000 - 7)
    main._opp_observer_update(_obs(1, inv1, _prices(MILK=158),
                                   ["SMOOTHIE_SHOP"]), {})
    flow = main._market_flow(0, 1, _prices(MILK=158))
    assert flow.get("MILK") == 0.0          # Ch0 exact: no opponent flow
    # opponent nets +5 WHEAT (they sold 5): inventory +5 - 0 ours - 1 center
    inv1b = _inv(WHEAT=10000 + 5 - 1, MILK=10000 - 16)
    main._opp_note_orders(0, 1, 23, [], _prices())
    main._opp_observer_update(_obs(2, inv1b, _prices(), ["SMOOTHIE_SHOP"]),
                              {})
    flow = main._market_flow(0, 2, _prices())
    assert flow.get("WHEAT") == 5.0
    assert main.est_opp_net("WHEAT", days=1) == 5.0
    _reset()


def test_floor_sells_dual_ledger_excluded_from_ch0():
    _reset()
    main._opp_observer_update(_obs(0, _inv(), _prices(), []), {})
    # WE dump 10 WHEAT at the $1 floor: money moves, inventory does not
    main._opp_note_orders(0, 0, 23, [["SELL", "WHEAT", 10]],
                          _prices(WHEAT=1))
    st = main._OPP_OBSERVER[0]
    assert st["sold_floor"].get("WHEAT") == 10
    assert st["sold_today"].get("WHEAT", 0) == 0
    # inventory moves only by the center draw (1) -> Ch0 sees NO opp flow
    main._opp_observer_update(_obs(1, _inv(WHEAT=10000 - 1),
                                   _prices(WHEAT=1), []), {})
    flow = main._market_flow(0, 1, _prices(WHEAT=1))
    assert flow.get("WHEAT") == 0.0
    _reset()


def test_unlock_day_absorb_uses_yesterday_shops():
    _reset()
    # day 0 warm-up with no shops
    main._opp_observer_update(_obs(0, _inv(), _prices(), []), {})
    # day 1 window: no shops yet, no trades -> only the center draw (1/item)
    main._opp_note_orders(0, 0, 23, [], _prices())
    # YARN_STORE unlocks at EOD of day 1 -> visible in day-2 observation,
    # but the day-2 account's window is day 1 (before the unlock)
    main._opp_observer_update(_obs(1, _inv(WHEAT=10000 - 1,
                                            WOOL=10000 - 1), _prices(),
                                   []), {})
    main._opp_note_orders(0, 1, 23, [], _prices())
    main._opp_observer_update(_obs(2, _inv(WHEAT=10000 - 2,
                                            WOOL=10000 - 2), _prices(),
                                   ["YARN_STORE"]), {})
    flow = main._market_flow(0, 2, _prices())
    # WOOL center-only on the day-1 window: -1 draw, no shop absorb yet
    assert flow.get("WOOL") == 0.0
    # day-3 window DOES include YARN (13/day absorb, no trades)
    main._opp_note_orders(0, 2, 23, [], _prices())
    main._opp_observer_update(_obs(3, _inv(WOOL=10000 - 2 - 13), _prices(),
                                   ["YARN_STORE"]), {})
    flow = main._market_flow(0, 3, _prices())
    assert flow.get("WOOL") == 0.0
    _reset()


def test_supply_horizon_real_form():
    _reset()
    main._opp_observer_update(_obs(0, _inv(), _prices(), []), {})
    st = main._OPP_OBSERVER[0]
    st["held"]["MILK"] = 7
    st["prod_horizon"] = {"MILK": [3, 2, 1, 0, 0, 0, 0]}
    assert main.est_opp_supply_horizon("MILK", 1) == 10
    assert main.est_opp_supply_horizon("MILK", 3) == 13
    assert main.est_opp_supply_horizon("MILK", 7) == 13
    _reset()


def test_conf_caps_frozen_from_v0():
    _reset()
    main._opp_observer_update(_obs(0, _inv(), _prices(), []), {})
    st = main._OPP_OBSERVER[0]
    st["conf"] = {item: 1.0 for item in ITEMS}
    assert main.est_opp_conf("WHEAT") == 0.4       # V0 MAE 52 -> capped
    assert main.est_opp_conf("MILK") == 0.4
    assert main.est_opp_conf("EGG") == 1.0
    # P4-tier consumers require conf >= 0.5 -> capped items fall back
    assert main.est_opp_conf("WHEAT") < 0.5
    _reset()


def test_snapshot_and_reset_api():
    _reset()
    main._opp_observer_update(_obs(0, _inv(), _prices(), []), {})
    snap = main.observer_snapshot(0)
    assert snap is not None and "held" in snap
    snap["held"]["MILK"] = 999                    # deep copy: no leak
    assert main._OPP_OBSERVER[0]["held"].get("MILK", 0) != 999
    main.reset_observer()
    assert main.observer_snapshot(0) is None
    _reset()


# --------------------------------------------------------------------------
# validator pure scoring
# --------------------------------------------------------------------------

def _load_validator():
    spec = importlib.util.spec_from_file_location(
        "ov0", os.path.join(SOFTWARE, "scripts",
                            "observer_v0_validator.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_v0_score_gates_math():
    ov0 = _load_validator()
    samples = []
    # 19 exact + 1 off (95% exactly), buys/floor/warm-up excluded
    for day in range(2, 21):
        samples.append({"seat": 0, "day": day, "item": "MILK",
                        "ch0_net": 4, "submitted_net": 4,
                        "had_buys": False, "price": 160,
                        "est_held": 4, "true_held": 4})
    samples.append({"seat": 0, "day": 22, "item": "MILK", "ch0_net": 5,
                    "submitted_net": 4, "had_buys": False, "price": 160,
                    "est_held": 5, "true_held": 5})
    verdict = ov0.score(samples)
    assert verdict["gate1_ch0_exact"]["share"] == 0.95
    assert verdict["gate1_ch0_exact"]["pass"] is True
    assert verdict["gate2_turning"]["n_series"] == 1
    assert verdict["overall_pass"] is True
