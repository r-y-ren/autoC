"""RESALE1: late intraday wheat resale runtime layer (agent/resale.py)."""
import numpy as np

from kagg3 import spec
from kagg3.agent import resale as R
from kagg3.core import plan as P


def test_off_by_default():
    assert P.RESALE_ON is False


def test_round_trip_on_unchanged_pot_is_zero_and_drain_pays():
    for pot in (9600, 9800, 10000, 10300):
        assert R.margin(pot, 60, 0) == 0
        assert R.margin(pot, 60, 22) >= 0
    assert R.margin(9800, 100, 22) > 0


def test_town_drain_counts_wheat_shops_every_four_steps():
    # h4 -> h21 covers ticks at h4, 8, 12, 16, 20; BAKERY and PIZZA_SHOP each take 1 wheat, YARN_STORE none
    assert R.town_drain(["BAKERY", "PIZZA_SHOP", "YARN_STORE"], 20 * 24 + 4, 20 * 24 + 21) == 10
    # the town centre adds one at h0
    assert R.town_drain([], 20 * 24, 20 * 24 + 1) == 1


def _obs(day, hour, shed_w=0, money=50000, pot=9800, other=0):
    shed = dict.fromkeys(spec.ITEMS, 0)
    shed["WHEAT"] = shed_w
    shed["MILK"] = other
    return {"step": day * 24 + hour, "day": day, "hour": hour, "player": 0,
            "farms": [{"money": money}, {"money": 0}],
            "private": {"shed": shed, "inventories": [{}]},
            "market": {"inventory": {"WHEAT": pot}},
            "town": {"unlocked_shops": ["BAKERY", "PIZZA_SHOP", "FARMERS_MARKET"]}}


def _plan():
    z = np.zeros((1, 24), np.int32)
    return (z, z, z)


def test_buy_then_sell_back(monkeypatch):
    monkeypatch.setattr(P, "RESALE_ON", True)
    st = {}
    act = {"farmer": ["PASS"], "hands": [], "market": []}
    R.step(st, _obs(20, 0), act, _plan())
    a = R.step(st, _obs(20, 4, other=10), act, _plan())
    k = 100 - 10 - P.RESALE_RESERVE
    assert a["market"] == [["BUY_PRODUCT", "WHEAT", k]]
    assert R.step(st, _obs(20, 10, shed_w=k, other=10), act, _plan()) is act      # no pressure: hold
    a = R.step(st, _obs(20, 21, shed_w=k, other=10), {**act, "market": [["SELL", "WHEAT", 5]]}, _plan())
    assert a["market"] == [["SELL", "WHEAT", 5 + k]]
    assert st["held"] == 0 and st["sold"] == k


def test_no_buy_outside_window_or_without_margin(monkeypatch):
    monkeypatch.setattr(P, "RESALE_ON", True)
    act = {"farmer": ["PASS"], "hands": [], "market": []}
    st = {}
    R.step(st, _obs(10, 0), act, _plan())
    assert R.step(st, _obs(10, 4), act, _plan()) is act
    monkeypatch.setattr(P, "RESALE_X", 1e9)
    st = {}
    R.step(st, _obs(20, 0), act, _plan())
    assert R.step(st, _obs(20, 4), act, _plan()) is act


def test_shed_pressure_releases_early(monkeypatch):
    monkeypatch.setattr(P, "RESALE_ON", True)
    st = {}
    act = {"farmer": ["PASS"], "hands": [], "market": []}
    R.step(st, _obs(20, 0), act, _plan())
    R.step(st, _obs(20, 4), act, _plan())
    held = st["held"]
    # a unit carries 30 units: room = 100 - held - 30 - reserve < 0 -> release the deficit now
    o = _obs(20, 9, shed_w=held)
    o["private"]["inventories"] = [{"MILK": 30}]
    a = R.step(st, o, act, _plan())
    need = -(100 - held - 30 - P.RESALE_RESERVE)
    assert a["market"] == [["SELL", "WHEAT", need]]
