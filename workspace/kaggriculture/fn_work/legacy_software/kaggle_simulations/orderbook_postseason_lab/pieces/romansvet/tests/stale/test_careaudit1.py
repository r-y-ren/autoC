"""`plan.CARE_FED_ON` [CAREAUDIT1]: every animal the day feeds is also cared.

The CARE op costs only its turn; the FEED spends the wheat whatever the care
does. `care_pays` (spot product > spot wheat) refuses the care on a product
trough even on a fed animal, and `CARE_RIDE_ON` admits it only on the survival
feed cadence. ON, `want_care` covers every `want_feed` tile inside the horizon
and headroom; the feed decision is unchanged. OFF the planner is byte-identical
(pinned on `test_route_early`'s digests, as `test_care_ride`).
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_care_ride import PIN, _cow_board
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case
from test_budget_order import _macro

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

SHEEP = spec.ANIMALS.index("SHEEP")


def _pins(monkeypatch, fed, care_fill=False):
    monkeypatch.setattr(P, "CARE_FED_ON", fed)
    monkeypatch.setattr(P, "CARE_RIDE_ON", False)
    monkeypatch.setattr(P, "CARE_HOLD_ON", False)
    monkeypatch.setattr(P, "ROUTE_SPLIT_ON", False)
    monkeypatch.setattr(P, "SURVIVAL_WATER_ON", False)
    monkeypatch.setattr(P, "TAIL_CARE_ON", False)
    if not care_fill:  # the idle-tail CARE filler would care the animal whatever `care_ok` said
        monkeypatch.setattr(P, "CARE_FILL_ON", False)
    monkeypatch.setattr(P, "FEED_MANDATORY_ON", False)


@pytest.fixture
def ident(monkeypatch):
    _pins(monkeypatch, False, care_fill=True)


@pytest.fixture
def off(monkeypatch):
    _pins(monkeypatch, False)


@pytest.fixture
def on(monkeypatch):
    _pins(monkeypatch, True)


def _sheep_board(**kw):
    v = _cow_board(**kw)
    occ = np.asarray(v.occ).copy(); occ[occ >= 0] = SHEEP
    price = np.asarray(v.price).copy(); price[spec.I_WOOL] = 5
    return v._replace(occ=occ, price=price)


def _ops(view):
    return set(int(x) for x in np.asarray(_plan(view, _macro())[0]).ravel())


def test_default_is_off():
    assert P.CARE_FED_ON is False


def test_off_plan_is_byte_identical(ident):
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN


def test_off_refuses_the_care_on_a_trough(off):
    for age in (9, 10):
        ops = _ops(_cow_board(age=age))
        assert O.OP_FEED in ops and O.OP_CARE not in ops


@pytest.mark.parametrize("age", [9, 10])
def test_on_cares_every_fed_cow(on, age):
    ops = _ops(_cow_board(age=age))
    assert O.OP_FEED in ops and O.OP_CARE in ops


def test_on_cares_a_fed_sheep_on_a_wool_trough(on):
    ops = _ops(_sheep_board(age=9))
    assert O.OP_FEED in ops and O.OP_CARE in ops


def test_on_skips_a_care_past_the_horizon(on):
    # day 28, cow placed d19: next fire harvest day 31 > pay_day -> the bank never cashes
    ops = _ops(_cow_board(day=28, age=9))
    assert O.OP_CARE not in ops
