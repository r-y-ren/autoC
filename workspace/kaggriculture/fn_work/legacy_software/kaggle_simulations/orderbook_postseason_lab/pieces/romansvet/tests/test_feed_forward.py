"""`plan.FEED_FORWARD_ON` [FEEDKEEP1]: price the hungry animal's stream in the
feed-value gate off a forward quote (town drain `FEED_FORWARD_K` days, plus our
pipeline) instead of the spot trough. OFF is pinned on `test_route_early`'s
digests; ON feeds a hungry goose whose spot egg quote is below one wheat."""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_care_hold import _hold_board
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P


#: Digests of the pre-switch tree (65b1be1d, feedkeep1 merge base) under the `base`
#: fixture; `test_route_early.PIN` is stale on this tree (test_care_hold fails it too).
PIN_FF = ('3fbd8044be120ede', '450826459562d8b2', 'd2ab6367892807f0', '0e52c9c4aedb7523',
          '060445dd21baded5', 'ce92ddc0b587b2e2', 'a637faec8f985b8d', '7940b9239438cfff',
          'f0bacd3a98c343c5', '056e5135bbf34053', '4ea16454f9888ee6', '086d315714f4c1bc')


@pytest.fixture
def base(monkeypatch):
    for k, v in (("CARE_HOLD_ON", False), ("ROUTE_SPLIT_ON", False), ("SURVIVAL_WATER_ON", False),
                 ("TAIL_CARE_ON", False), ("FEED_MANDATORY_ON", False)):
        monkeypatch.setattr(P, k, v)


def test_default_is_off():
    assert P.FEED_FORWARD_ON is False


def test_off_plan_is_byte_identical_to_the_pre_switch_planner(base, monkeypatch):
    monkeypatch.setattr(P, "FEED_FORWARD_ON", False)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS)
    assert got == PIN_FF


def _trough(wheat_price=40):
    v = _hold_board(n_goose=3, egg=1, wheat_price=wheat_price, wheat=10, day=20)
    price = v.price.copy()
    price[spec.I_FERT] = 1
    return v._replace(price=price)


def _feeds(view):
    return int((np.asarray(_plan(view, _macro())[0]) == O.OP_FEED).sum())


def test_off_lets_the_trough_goose_go_on_forward_feeds_it(base, monkeypatch):
    view = _trough()
    monkeypatch.setattr(P, "FEED_FORWARD_ON", False)
    off = _feeds(view)
    monkeypatch.setattr(P, "FEED_FORWARD_ON", True)
    monkeypatch.setattr(P, "FEED_FORWARD_PIPE", False)
    on = _feeds(view)
    assert off == 0 and on == 3, (off, on)


def test_on_still_refuses_what_the_forward_quote_cannot_pay(base, monkeypatch):
    view = _trough(wheat_price=4000)
    monkeypatch.setattr(P, "FEED_FORWARD_ON", True)
    assert _feeds(view) == 0
