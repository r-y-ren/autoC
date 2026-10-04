"""`plan.Q4_VRP_ON` [Q4VRP1]: the fourth quadrant funded by the VRP's banked hire saving.

Claims: OFF by default; ON without a release and with a purse under the gap is byte-identical
to OFF; a bank release that covers the price buys Q4 on a purse that alone cannot; the
visible-only funding ignores the release.
"""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np

from kagg3.core import ops as O
from kagg3.core import plan as P

from test_q4_prog import _board, _plan, _land
from test_endroute import _digest


def _with(**kw):
    old = {k: getattr(P, k) for k in kw}
    for k, v in kw.items():
        setattr(P, k, v)
    return old


def test_off_by_default():
    assert P.Q4_VRP_ON is False and P.Q4_VRP_RELEASE == 0 and P.Q4_VRP_FUND == "true"


def test_parity_and_bank_release():
    v = _board(12, 3, money=600)
    off = _plan(v)
    old = _with(Q4_VRP_ON=True, Q4_VRP_DAY=10, Q4_VRP_RESERVE=0, Q4_VRP_RELEASE=0, Q4_VRP_FUND="true")
    try:
        on0 = _plan(v)
        assert _digest(on0) == _digest(off) and _land(off) == 0
        P.Q4_VRP_RELEASE = 4000
        on = _plan(v)
        assert _land(on) == 1                       # the bank pays the land
        P.Q4_VRP_FUND = "visible"
        assert _land(_plan(v)) == 0                 # visible-only ignores the release
        P.Q4_VRP_FUND = "true"
        P.Q4_VRP_DAY = 13
        assert _land(_plan(v)) == 0                 # before the window
    finally:
        _with(**old)
