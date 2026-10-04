"""`plan.CARE_RIDE_ON` [MILKTRACE1]: a CARE rides a survival feed for free.

`care_pays` (spot product > spot wheat) refuses a care whenever the milk quote
is under wheat, even on a tile the day feeds anyway for survival (`must_feed`),
where the care costs only its turn. ON, such a care is taken when the bank it
adds is cashed at a fire whose end-of-day falls on the every-other-day feed
cadence (`(h_next - 1 - day) % 2 == 0`: a cow on its fire night). OFF the
planner is byte-identical (pinned on `test_route_early`'s digests).
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

BASE_PRICE = np.array([25, 35, 60, 120, 250, 50, 160, 200, 100], np.int32)
COW = spec.ANIMALS.index("COW")
#: `test_route_early`'s 12 seeded cases under `ident`'s pins, digested on the
#: pre-switch tree (selfplay1 ef581fd3; `test_route_early.PIN` is stale there).
PIN = ("3fbd8044be120ede", "450826459562d8b2", "d2ab6367892807f0", "0e52c9c4aedb7523",
       "060445dd21baded5", "ce92ddc0b587b2e2", "a637faec8f985b8d", "7940b9239438cfff",
       "f0bacd3a98c343c5", "056e5135bbf34053", "4ea16454f9888ee6", "086d315714f4c1bc")


def _pins(monkeypatch, on, care_fill=False):
    monkeypatch.setattr(P, "CARE_RIDE_ON", on)
    monkeypatch.setattr(P, "CARE_HOLD_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    if not care_fill:  # the idle-tail CARE filler would care the cow whatever `care_ok` said
        monkeypatch.setattr(P, "CARE_FILL_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


@pytest.fixture
def ident(monkeypatch):
    """`test_care_hold`'s OFF pins, under which `PIN` is the planner's digest."""
    _pins(monkeypatch, False, care_fill=True)


@pytest.fixture
def off(monkeypatch):
    _pins(monkeypatch, False)


@pytest.fixture
def on(monkeypatch):
    _pins(monkeypatch, True)


def _cow_board(n=2, day=25, age=9, milk=10, wheat_price=40, wheat=10):
    """`n` cows one night from escaping (t_cons 1), milk quote under wheat.
    age 9 -> the cow fires tonight (next fire eod day+2, on the cadence);
    age 10 -> it fires tomorrow night (eod day+1, off the cadence)."""
    z = np.zeros(spec.N_TILES, np.int32)
    kind = np.full(spec.N_TILES, spec.KIND_EMPTY, np.int32)
    occ = z - 1
    t_cons = z.copy(); t_day = z.copy()
    kind[:n], occ[:n] = spec.KIND_PASTURE, COW
    t_cons[:n] = 1
    t_day[:n] = day - age
    shed = np.zeros(spec.N_ITEMS, np.int32); shed[spec.I_WHEAT] = wheat
    price = BASE_PRICE.copy(); price[spec.I_MILK] = milk; price[spec.I_WHEAT] = wheat_price
    return P.DayView(
        day=np.int32(day), kind=kind, occ=occ, t_day=t_day, t_water=z.copy(),
        t_cons=t_cons, t_yield=z.copy(), t_fert=z - 1, t_cared=z.copy(),
        t_favail=z.copy(), shed=shed,
        seeds=np.zeros(spec.N_CROPS, np.int32), money=np.int32(0),
        nquad=np.int32(1), price=price,
        mkt_inv=np.full(spec.N_PRODUCTS, spec.MARKET_I0, np.int32),
        shops=np.zeros(spec.N_SHOPS, np.int32), t_bank=z.copy())


def _ops(view):
    return set(int(x) for x in np.asarray(_plan(view, _macro())[0]).ravel())


def test_default_is_off():
    assert P.CARE_RIDE_ON is False


def test_off_plan_is_byte_identical(ident):
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_feeds_the_cow_and_refuses_the_care(off):
    ops = _ops(_cow_board())
    assert O.OP_FEED in ops, "the survival feed did not plan"
    assert O.OP_CARE not in ops


def test_on_cares_the_cow_on_its_fire_night(on):
    ops = _ops(_cow_board(age=9))
    assert O.OP_FEED in ops and O.OP_CARE in ops


def test_on_skips_a_care_whose_fire_is_off_the_cadence(on):
    ops = _ops(_cow_board(age=10))
    assert O.OP_FEED in ops
    assert O.OP_CARE not in ops

