"""BOEY2 switch [BOEY_PKG_ON]: Boey's opening as one package, then our planner + router
(docs/strategy/2026-09-27-boey2.md).

Claims: OFF by default and byte-identical to the BOEY1 digests (cc94afdb build_day on five days); ON, the
package writes its switch sets and OFF restores them; the d0 plate plants melon + wheat and no carrot; the
herd component is dropped with BOEY_PKG_HERD=False; never Q4.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan as P

from test_boey1 import CASES, _plan
from test_endroute import _digest
from test_q4_prog import _plants, _land


@pytest.fixture
def pkg(monkeypatch):
    """ON for the test, then OFF + one sync so the written sets are restored for later tests."""
    monkeypatch.setattr(P, "BOEY_PKG_ON", True)
    yield
    P.BOEY_PKG_ON = False
    P.boey_pkg_sync()


def test_off_by_default():
    assert P.BOEY_PKG_ON is False and P._BOEY_PKG_BASE is None
    assert "BOEY_PKG_ON" not in P.SWITCH_GENES


@pytest.mark.parametrize("case,dig", CASES)
def test_off_byte_identical(case, dig):
    assert _digest(_plan(*case)) == dig


def test_sync_writes_and_restores(pkg):
    _plan(0, 1, 3000, (4, 3, 0, 0, 0))
    assert P.BOEY_NO_TOMATO_ON is True and P.WOOL_FIRST_ON is True and P.GEESE_TARGET == 7
    assert P.NONV_MELON_SKIP == (10, 29) and P.NONV_MELON_TO == "WHEAT" and P.BOEY_EARLY_WHEAT_DAYS == (0, 9)
    P.BOEY_PKG_HERD = False
    try:
        _plan(0, 1, 3000, (4, 3, 0, 0, 0))
        assert P.WOOL_FIRST_ON is False and P.GEESE_TARGET == 0 and P.BOEY_NO_TOMATO_ON is True
    finally:
        P.BOEY_PKG_HERD = True
    P.BOEY_PKG_ON = False
    P.boey_pkg_sync()
    assert P.BOEY_NO_TOMATO_ON is False and P.WOOL_FIRST_ON is False and P.NONV_MELON_SKIP is None


def test_plate_d0(pkg):
    got = _plants(_plan(0, 1, 3000, (11, 8, 0, 0, 0)))
    assert got[spec.I_MELON] == P.BOEY_PKG_MELON and got[spec.I_CARROT] == 0 and got[spec.I_WHEAT] > 0


def test_never_q4(pkg):
    assert _land(_plan(12, 3, 90000, (2, 1, 0, 0, 0))) == 0
