"""FILLWORK1: FILL_WORK_ON -- OFF 3-board parity vs 1bf12f80, fill plants more with the SAME final-pass hire bill,
capped by FILL_WORK_MAX, growing fill tiles never raise the bill, outside the window = OFF."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3.core import ops as O, plan as P

BASE = '1bf12f80'
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v):
    return tuple(np.asarray(a) for a in P.build_day(np, v, _macro(plant_target=TGT)))


def _run(monkeypatch, v):
    seen = []
    der = P._derive

    def spy(xp, view, macro, price_table, hire_bill, *a, **k):
        if k.get('ask_fill'):
            seen.append(int(np.asarray(hire_bill)))
        return der(xp, view, macro, price_table, hire_bill, *a, **k)
    monkeypatch.setattr(P, '_derive', spy)
    p = _plan(v)
    monkeypatch.setattr(P, '_derive', der)
    return p, seen[-1]


def _plants(p, crop=None):
    m = p[0] == O.OP_PLANT
    if crop is not None:
        m = m & (p[1] == crop)
    return int(np.sum(m))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def test_off_three_board_parity():
    assert P.FILL_WORK_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def test_fill_plants_more_with_the_off_crew(monkeypatch):
    v = _view(day=15, money=40_000, nquad=3, n_wh=10)
    p_off, bill_off = _run(monkeypatch, v)
    monkeypatch.setattr(P, 'FILL_WORK_ON', True)
    monkeypatch.setattr(P, 'FILL_WORK_MAX', 4)
    p_on, bill_on = _run(monkeypatch, v)
    assert bill_on == bill_off                      # never buys a hand
    assert 0 < _plants(p_on) - _plants(p_off) <= 4  # capped per day
    monkeypatch.setattr(P, 'FILL_WORK_MAX', 1)
    p_1, _ = _run(monkeypatch, v)
    assert _plants(p_1) - _plants(p_off) <= 1
    monkeypatch.setattr(P, 'FILL_WORK_TURNS', 10_000)  # no staffing room -> no fill
    p_z, bill_z = _run(monkeypatch, v)
    assert bill_z == bill_off and _plants(p_z) == _plants(p_off)


def test_carrot_rule(monkeypatch):
    v = _view(day=15, money=40_000, nquad=3, n_wh=10)
    p_off, _ = _run(monkeypatch, v)
    monkeypatch.setattr(P, 'FILL_WORK_ON', True)
    monkeypatch.setattr(P, 'FILL_WORK_MAX', 4)
    monkeypatch.setattr(P, 'FILL_WORK_CROP', 'carrot')
    p_on, _ = _run(monkeypatch, v)
    assert _plants(p_on, 1) > _plants(p_off, 1)
    assert _plants(p_on, 0) <= _plants(p_off, 0)


def test_growing_fill_tiles_never_buy_a_hand(monkeypatch):
    v = _view(day=13, money=40_000, nquad=3, n_wh=10)
    _, bill0 = _run(monkeypatch, v)
    monkeypatch.setattr(P, 'FILL_WORK_ON', True)
    monkeypatch.setattr(P, 'FILL_WORK_TURNS', 10_000)  # no new fill: only the later-day credit acts
    _, bill1 = _run(monkeypatch, v)
    assert bill1 <= bill0


def test_outside_window_is_off(monkeypatch):
    v = _view(day=27, money=40_000, nquad=4, n_wh=28)
    p_off = _plan(v)
    monkeypatch.setattr(P, 'FILL_WORK_ON', True)
    monkeypatch.setattr(P, 'FILL_WORK_H23', False)
    p_on = _plan(v)
    assert all(np.array_equal(a, b) for a, b in zip(p_off, p_on))


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
