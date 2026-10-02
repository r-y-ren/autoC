"""ENGMIX1: the ENGINE-gated wheat-share cells ride `ENGINE_GATE_SET` on the
existing `WHEAT_VOLUME_ON/NUM/DEN` switch (no new plan code).

Claims: the switch is OFF by default; the gate writes the wheat-share set and
restores it exactly (whole-plan digests equal the untouched ones = OFF parity);
ON, `_wheat_mix` moves NUM/DEN of the non-wheat tiles onto WHEAT with the total
preserved (100 % share at NUM == DEN).
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import plan as P

from test_engine_gate import _digests, _reset
from test_endroute import _macro

SET = "WHEAT_VOLUME_ON=True;WHEAT_VOLUME_NUM=2;WHEAT_VOLUME_DEN=3"


def test_off_by_default():
    assert P.WHEAT_VOLUME_ON is False and P.ENGINE_GATE_ON is False


def test_gate_apply_restore_parity():
    base = _digests()
    old = (P.WHEAT_VOLUME_ON, P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN)
    _reset(SET)
    try:
        P.engine_gate_apply(True)
        assert (P.WHEAT_VOLUME_ON, P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN) == (True, 2, 3)
        P.engine_gate_apply(False)
        assert (P.WHEAT_VOLUME_ON, P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN) == old
        assert _digests() == base
    finally:
        _reset("")


def test_wheat_share_total_preserved():
    m = _macro()
    t = np.array([2, 3, 1, 4, 2], np.int32)          # wheat index 0 > 0
    m = m._replace(plant_target=t)
    old = (P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN)
    try:
        for num, den in ((1, 3), (2, 3), (1, 1)):
            P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN = num, den
            out = np.asarray(P._wheat_mix(np, m).plant_target)
            assert out.sum() == t.sum()
            assert out[P.spec.I_WHEAT] == t[0] + 10 - (10 * (den - num)) // den
        assert np.asarray(P._wheat_mix(np, m._replace(plant_target=t * np.array([0, 1, 1, 1, 1]))).plant_target).tolist() == [0, 3, 1, 4, 2]
    finally:
        P.WHEAT_VOLUME_NUM, P.WHEAT_VOLUME_DEN = old
