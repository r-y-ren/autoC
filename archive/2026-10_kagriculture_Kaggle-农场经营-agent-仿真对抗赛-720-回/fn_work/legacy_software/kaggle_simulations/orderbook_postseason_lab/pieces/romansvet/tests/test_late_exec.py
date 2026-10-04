"""ENDFIX1 LATE_EXEC_ON: final-harvest-day DIG + same-day replant; OFF parity."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3 import spec
from kagg3.core import brain, ops as O, plan as P

PRE_SWITCH = '27314036'


def _final_view(day=22, crop=spec.I_STRAWBERRY, held=2, delta=0):
    v = _view(day=day, money=20_000, nquad=4)
    v.kind[:] = spec.KIND_LOCKED
    v.kind[0] = spec.KIND_PLANT
    v.occ[0] = crop
    last_age = spec.CROP_FIRST_YIELD_DAY[crop] + (spec.CROP_MAX_YIELD[crop] - 1) * spec.CROP_INTERVAL[crop]
    v.t_day[0] = day - last_age - delta
    v.t_yield[0] = held
    return v


def _own_digests():
    target = np.array([1, 0, 0, 0, 0], np.int32)
    boards = [('opening', _view(day=0, money=3_000)),
              ('final', _final_view()),
              ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]
    return {name: _pin.digest(P.build_day(np, v, _macro(plant_target=target)))
            for name, v in boards}


def _derive(v, m):
    return P._derive(np, v, m, P.default_price_table(), np.int32(0),
                     np.bool_(v.day == 29), np.int32(0), ask_fill=True)


def test_off_three_board_parity(monkeypatch):
    monkeypatch.setattr(P, 'LATE_EXEC_ON', False)  # default True since SHIP_LE; OFF == pre-switch tree
    assert _own_digests() == _pin.tree_digests(__file__, ref=PRE_SWITCH)


def test_final_slot_boundary_and_brain(monkeypatch):
    assert bool(P._final_slots(np, _final_view(delta=0))[0])
    assert bool(P._final_slots(np, _final_view(delta=1, held=0))[0])
    assert not bool(P._final_slots(np, _final_view(delta=-1))[0])
    v = _final_view()
    monkeypatch.setattr(P, 'LATE_EXEC_ON', False)
    assert int(brain.n_free_slots(np, v)) == 0
    monkeypatch.setattr(P, 'LATE_EXEC_ON', True)
    assert int(brain.n_free_slots(np, v)) == 1
    monkeypatch.setattr(P, 'LATE_EXEC_DAY0', 23)
    assert int(brain.n_free_slots(np, v)) == 0


def test_final_day_harvest_dig_plant_water(monkeypatch):
    v = _final_view()
    m = _macro(plant_target=np.array([1, 0, 0, 0, 0], np.int32))
    monkeypatch.setattr(P, 'LATE_EXEC_ON', False)
    off = _derive(v, m)
    assert O.OP_DIG not in off.chain_op[0] and O.OP_PLANT not in off.chain_op[0]
    monkeypatch.setattr(P, 'LATE_EXEC_ON', True)
    ch = [int(x) for x in _derive(v, m).chain_op[0]]
    i = ch.index(O.OP_HARVEST)
    assert ch[i:i + 4] == [O.OP_HARVEST, O.OP_DIG, O.OP_PLANT, O.OP_WATER]


def test_no_dig_without_planting(monkeypatch):
    monkeypatch.setattr(P, 'LATE_EXEC_ON', True)
    d = _derive(_final_view(), _macro(plant_target=np.zeros(5, np.int32)))
    assert O.OP_DIG not in d.chain_op[0] and O.OP_HARVEST in d.chain_op[0]


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
