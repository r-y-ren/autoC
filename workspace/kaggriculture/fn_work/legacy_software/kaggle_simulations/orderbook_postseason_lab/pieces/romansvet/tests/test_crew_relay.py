"""CREWRELAY1: CREW_RELAY_ON -- OFF 3-board parity vs master + hire cap (the relay never changes the day's crew)."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3.core import ops as O, plan as P

BASE = '05ff0f5f'   # master at branch time
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v, m=None):
    return tuple(np.asarray(a) for a in P.build_day(np, v, m or _macro(plant_target=TGT)))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def _run(monkeypatch, v):
    """(plan, hire bill of the final pass)."""
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


def test_off_three_board_parity():
    assert P.CREW_RELAY_ON is False and P.RELAY_FILL_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def test_relay_plants_more_with_the_off_crew(monkeypatch):
    v = _view(day=22, money=40_000, nquad=3, n_wh=10)
    p_off, bill_off = _run(monkeypatch, v)
    monkeypatch.setattr(P, 'CREW_RELAY_ON', True)
    p_on, bill_on = _run(monkeypatch, v)
    assert int(np.sum(p_on[0] == O.OP_PLANT)) > int(np.sum(p_off[0] == O.OP_PLANT))
    assert bill_on == bill_off            # hard rule: the relay never buys a hand
    # zero staffing room -> no relay tile at all (plant fewer, never hire)
    monkeypatch.setattr(P, 'CREW_RELAY_TURNS', 10_000)
    monkeypatch.setattr(P, 'CREW_RELAY_EVE', False)
    monkeypatch.setattr(P, 'CREW_RELAY_H1', False)
    monkeypatch.setattr(P, 'CREW_RELAY_H23', False)
    p_z, bill_z = _run(monkeypatch, v)
    assert bill_z == bill_off
    assert int(np.sum(p_z[0] == O.OP_PLANT)) == int(np.sum(p_off[0] == O.OP_PLANT))


def test_growing_relay_tiles_never_buy_a_hand(monkeypatch):
    # later day: relay tiles planted d20-21 are still growing on d23 -> the
    # enumeration is credited their turns, so the crew can only shrink vs no credit
    v = _view(day=23, money=40_000, nquad=3, n_wh=10)
    monkeypatch.setattr(P, 'CREW_RELAY_ON', True)
    P._CR_MEM.update(last=-1, plants={})
    _, bill0 = _run(monkeypatch, v)
    P._CR_MEM.update(last=21, plants={20: np.array([30, 30, 0, 0, 0]), 21: np.array([30, 30, 0, 0, 0])})
    assert P._cr_alive(np, 23) == 120
    P._CR_MEM.update(last=21, plants={20: np.array([30, 30, 0, 0, 0]), 21: np.array([30, 30, 0, 0, 0])})
    _, bill1 = _run(monkeypatch, v)
    assert bill1 <= bill0
    P._CR_MEM.update(last=-1, plants={})


def test_outside_window_is_off(monkeypatch):
    v = _view(day=15, money=20_000, nquad=3, n_wh=20)
    d_off = _pin.digest(_plan(v))
    a = _plan(v)
    monkeypatch.setattr(P, 'CREW_RELAY_ON', True)
    b = _plan(v)
    # the evening row exists (item columns filled) but carries no order: op and qty rows all zero
    assert not np.any(b[3][O.TURN_PRESTOCK]) and not np.any(b[5][O.TURN_PRESTOCK])
    b4 = b[4].copy(); b4[O.TURN_PRESTOCK] = a[4][O.TURN_PRESTOCK]
    assert all(np.array_equal(x, y) for x, y in zip(a[:4] + (a[5],), b[:4] + (b[5],)))
    assert np.array_equal(a[4], b4)
    monkeypatch.setattr(P, 'CREW_RELAY_EVE', False)
    assert _pin.digest(_plan(v)) == d_off


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
