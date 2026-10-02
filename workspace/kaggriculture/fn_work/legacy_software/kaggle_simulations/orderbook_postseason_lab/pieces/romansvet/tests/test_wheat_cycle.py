"""WHEATCYCLE1: WHEAT_CYCLE_ON / _CARROT_ON / _H3_ON -- OFF 3-board parity vs master + behaviour."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3 import spec
from kagg3.core import ops as O, plan as P

BASE = '0d97fa1a'   # master at branch time
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v, m=None):
    return tuple(np.asarray(a) for a in P.build_day(np, v, m or _macro(plant_target=TGT)))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def _n(p, op):
    return int(np.sum(p[0] == op))


def _fert_view(age, crop=spec.I_WHEAT, t_fert=-1, yld=1):
    v = _view(day=15, money=20_000, nquad=3, n_wh=8, age=age, yld=yld)
    shed = v.shed.copy(); shed[spec.I_FERT] = 30
    occ = v.occ.copy(); occ[:8] = crop
    tf = v.t_fert.copy(); tf[:8] = t_fert
    pr = np.array(v.price).copy(); pr[spec.I_FERT] = 10     # fixture fert quote 100 > 2 wheat
    return v._replace(shed=shed, occ=occ, t_fert=tf, price=pr)


def test_off_three_board_parity():
    assert not (P.WHEAT_CYCLE_ON or P.WHEAT_CYCLE_CARROT_ON or P.WHEAT_CYCLE_H3_ON)
    assert P.WHEAT_CYCLE_RP_ON  # sub-knob of H3 only
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def test_wheat_fert_moves_from_age1_to_age2(monkeypatch):
    v1 = _fert_view(age=1)
    assert _n(_plan(v1), O.OP_FERTILIZE) > 0                  # OFF fertilizes at age 1
    monkeypatch.setattr(P, 'WHEAT_CYCLE_ON', True)
    assert _n(_plan(v1), O.OP_FERTILIZE) == 0                 # ON waits ...
    assert _n(_plan(_fert_view(age=2, yld=1)), O.OP_FERTILIZE) > 0   # ... for the age-2 stop


def test_carrot_knob(monkeypatch):
    v1 = _fert_view(age=1, crop=spec.I_CARROT)
    off = _n(_plan(v1), O.OP_FERTILIZE)
    monkeypatch.setattr(P, 'WHEAT_CYCLE_ON', True)            # wheat knob leaves carrot alone
    assert _n(_plan(v1), O.OP_FERTILIZE) == off
    monkeypatch.setattr(P, 'WHEAT_CYCLE_CARROT_ON', True)
    assert _n(_plan(v1), O.OP_FERTILIZE) == 0


def test_h3_harvests_fertilized_wheat_at_age3(monkeypatch):
    v3 = _fert_view(age=3, t_fert=15 + 1, yld=3)             # fert at age 2 covers ages 2-4
    assert _n(_plan(v3), O.OP_HARVEST) == 0                   # OFF waits for age 4
    monkeypatch.setattr(P, 'WHEAT_CYCLE_H3_ON', True)
    p = _plan(v3)
    assert _n(p, O.OP_HARVEST) >= 1
    # ... and replants the freed tile on the same stop (WHEAT_CYCLE_RP_ON)
    assert _n(p, O.OP_PLANT) >= _n(_plan(v3), O.OP_HARVEST)
    # unfertilized age-3 wheat is left alone
    assert _n(_plan(_fert_view(age=3, t_fert=-1, yld=2)), O.OP_HARVEST) == 0


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
