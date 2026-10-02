"""[ESNEW1] `plan.ESNEW_THETA`: None and zeros both reproduce the shipped plan
byte for byte on recorded seeded days; a nonzero band row moves the plan."""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_route_early import _digest, _plan, _seeded_case

from kagg3.core import plan as P

DAYS = (0, 3, 7)   # three recorded seeded days (PIN_SEEDS subset)


@pytest.mark.parametrize("seed", DAYS)
def test_zeros_equal_shipped(seed, monkeypatch):
    view, macro = _seeded_case(seed)
    monkeypatch.setattr(P, "ESNEW_THETA", None)
    base = _digest(_plan(view, macro))
    monkeypatch.setattr(P, "ESNEW_THETA", np.zeros((P.ESNEW_BANDS, P.ESNEW_W), np.float32))
    assert _digest(_plan(view, macro)) == base
    small = np.full((P.ESNEW_BANDS, P.ESNEW_W), 0.49, np.float32)
    monkeypatch.setattr(P, "ESNEW_THETA", small)
    assert _digest(_plan(view, macro)) == base


def test_nonzero_moves_some_day(monkeypatch):
    th = np.zeros((P.ESNEW_BANDS, P.ESNEW_W), np.float32)
    th[:, 0:5] = 4.0
    th[:, 9:18] = 500.0
    moved = 0
    for seed in range(12):
        view, macro = _seeded_case(seed)
        monkeypatch.setattr(P, "ESNEW_THETA", None)
        base = _digest(_plan(view, macro))
        monkeypatch.setattr(P, "ESNEW_THETA", th)
        moved += _digest(_plan(view, macro)) != base
    assert moved >= 1
