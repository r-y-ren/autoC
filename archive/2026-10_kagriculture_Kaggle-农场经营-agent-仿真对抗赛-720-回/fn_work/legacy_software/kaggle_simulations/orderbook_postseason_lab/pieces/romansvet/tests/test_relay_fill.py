"""RELAYFILL1: RELAY_FILL_ON -- OFF 3-board parity vs master + behaviour (fills spare slots in window, not outside)."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3 import spec
from kagg3.core import ops as O, plan as P

BASE = 'a6a22d8e'   # master at branch time
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v, m=None):
    return tuple(np.asarray(a) for a in P.build_day(np, v, m or _macro(plant_target=TGT)))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def _plants(plan):
    return int(np.sum(plan[0] == O.OP_PLANT))


def test_off_three_board_parity():
    assert P.RELAY_FILL_ON is False and P.RELAY_SELL_NOW is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def test_relay_fills_spare_slots_in_window(monkeypatch):
    v = _view(day=22, money=40_000, nquad=3, n_wh=10)
    off = _plants(_plan(v))
    monkeypatch.setattr(P, 'RELAY_FILL_ON', True)
    on = _plants(_plan(v))
    assert on > off, (on, off)
    # outside the window (d27: nothing reaches full yield by d28) the plan is the OFF plan
    v27 = _view(day=27, money=40_000, nquad=4, n_wh=28)
    monkeypatch.setattr(P, 'RELAY_FILL_ON', False)
    d_off = _pin.digest(_plan(v27))
    monkeypatch.setattr(P, 'RELAY_FILL_ON', True)
    assert _pin.digest(_plan(v27)) == d_off


def test_relay_zero_frac_is_off(monkeypatch):
    v = _view(day=22, money=40_000, nquad=3, n_wh=10)
    d_off = _pin.digest(_plan(v))
    monkeypatch.setattr(P, 'RELAY_FILL_ON', True)
    monkeypatch.setattr(P, 'RELAY_FRAC', 0.0)
    assert _pin.digest(_plan(v)) == d_off


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
