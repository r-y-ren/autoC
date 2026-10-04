"""`plan.FEEDROOM_ON` [FEEDROOM1]: when the shed-room clip binds the feed wheat,
the animals that escape tonight (`must_feed`) are fed before bank/care-only feeds.

Fixture = our seat's d21 dawn on mc10nys0n (MC10TRACE1, Stack A arm;
`S/feedroom1/fixture.py`): shed 100/100, 12 wheat, room 0, ten hungry animals
(5 cows, the goose, 4 sheep). OFF the 12 wheat go to 5 hungry animals and 7
not-hungry bank-3 sheep (the trace's end-of-day feeds exactly); ON all ten
hungry animals are fed. OFF the planner is byte-identical (`test_route_early`'s
seeded cases under `test_care_ride`'s pins).
"""
from __future__ import annotations

from pathlib import Path

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_care_ride import PIN, _pins as _care_pins
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import plan as P

FIX = Path(__file__).parent / "data" / "feedroom1_mc10_d21.npz"


def _view(wheat=None):
    z = np.load(FIX)
    shed = z["shed"].copy()
    if wheat is not None:
        shed[spec.I_WHEAT] = wheat
    return z, P.DayView(
        day=z["day"], kind=z["kind"], occ=z["occ"], t_day=z["t_day"], t_water=z["t_water"],
        t_cons=z["t_cons"], t_yield=z["t_yield"], t_fert=np.full(spec.N_TILES, -1, np.int32),
        t_cared=z["t_cared"], t_favail=np.zeros(spec.N_TILES, np.int32), shed=shed,
        seeds=z["seeds"], money=z["money"], nquad=z["nquad"], price=z["price"],
        mkt_inv=z["mkt_inv"], t_bank=z["t_bank"])


def _want_feed(view, monkeypatch):
    """The planner's final `want_feed` (last `_derive` pass of the day)."""
    box, d0 = [], P._derive

    def spy(*a, **k):
        box.append(d0(*a, **k))
        return box[-1]
    monkeypatch.setattr(P, "_derive", spy)
    P.build_day(np, view, _macro())
    monkeypatch.setattr(P, "_derive", d0)
    return np.asarray(box[-1].want_feed)


def _hungry(z):
    an = (z["kind"] == spec.KIND_COOP) | (z["kind"] == spec.KIND_PASTURE)
    return an & (z["t_cons"] >= 1)


def test_default_is_off():
    assert P.FEEDROOM_ON is False


def test_off_plan_is_byte_identical(monkeypatch):
    _care_pins(monkeypatch, False, care_fill=True)
    monkeypatch.setattr(P, "FEEDROOM_ON", False)
    assert tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS) == PIN


def test_fixture_is_room_bound():
    z, v = _view()
    assert int(np.asarray(v.shed).sum()) == spec.SHED_CAPACITY
    assert int(_hungry(z).sum()) == 10 and int(z["shed"][spec.I_WHEAT]) == 12


def test_off_feeds_not_hungry_sheep_before_hungry_cows(monkeypatch):
    monkeypatch.setattr(P, "FEEDROOM_ON", False)
    z, v = _view()
    wf, hun = _want_feed(v, monkeypatch), _hungry(z)
    assert int((wf & hun).sum()) == 5 and int((wf & ~hun).sum()) == 7
    # the trace's own end-of-day feeds on the hungry tiles
    assert (wf & hun).tolist() == (z["fed_eod"].astype(bool) & hun).tolist()


def test_on_feeds_every_hungry_animal(monkeypatch):
    monkeypatch.setattr(P, "FEEDROOM_ON", True)
    z, v = _view()
    wf, hun = _want_feed(v, monkeypatch), _hungry(z)
    assert int((wf & hun).sum()) == 10, "a hungry animal was left to escape"
    assert int(wf.sum()) == 12, "the switch must not buy or invent wheat"
    cows = hun & (z["occ"] == spec.ANIMALS.index("COW"))
    assert int((wf & cows).sum()) == 5


@pytest.mark.parametrize("wheat", [40])
def test_on_is_inert_when_wheat_covers_the_herd(monkeypatch, wheat):
    _, v = _view(wheat=wheat)
    monkeypatch.setattr(P, "FEEDROOM_ON", False)
    off = _digest(_plan(v))
    monkeypatch.setattr(P, "FEEDROOM_ON", True)
    assert _digest(_plan(v)) == off
