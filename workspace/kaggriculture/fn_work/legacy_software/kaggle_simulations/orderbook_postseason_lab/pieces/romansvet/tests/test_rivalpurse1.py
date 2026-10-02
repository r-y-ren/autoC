"""RIVALPURSE1: residual feature 2 (rival purse) is 0 unless RESIDUAL_RIVAL_PURSE_ON."""
from __future__ import annotations

import numpy as np

from kagg3.agent import parse
from kagg3.core import plan as P
from test_live_program import _obs


def test_rival_purse_feature_switch(monkeypatch):
    view = parse.parse_view(_obs(), 0)
    monkeypatch.setattr(P, "SELL_SLOT_MIRROR_GATE_ON", False)
    monkeypatch.setattr(P, "RESIDUAL_RIVAL_PURSE_ON", False)
    off = P._residual_features(np, view)
    assert off.shape == (P.RESIDUAL_N_FEAT,) and off[2] == 0.0      # the shipped (dead) input
    monkeypatch.setattr(P, "RESIDUAL_RIVAL_PURSE_ON", True)
    on = P._residual_features(np, view)
    assert np.isclose(on[2], 1.0)                                   # 10,000 / 1e4
    np.testing.assert_array_equal(np.delete(on, 2), np.delete(off, 2))
