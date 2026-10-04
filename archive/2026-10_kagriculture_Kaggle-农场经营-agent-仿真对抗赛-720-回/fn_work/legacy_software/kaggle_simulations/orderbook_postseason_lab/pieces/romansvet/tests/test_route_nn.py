"""ROUTENN1: ROUTE_NN_ON -- OFF 3-board parity vs master; ON hire head moves the crew within +-2 (affordable);
dispatch env: a free unit gets a legal job from the observation, a planned unit is never touched."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3.core import plan as P

BASE = 'b2571784'   # master at branch time
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _plan(v, m=None):
    return tuple(np.asarray(a) for a in P.build_day(np, v, m or _macro(plant_target=TGT)))


def _own_digests():
    return {n: _pin.digest(_plan(v)) for n, v in _boards()}


def test_off_three_board_parity():
    assert P.ROUTE_NN_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def _units(p):
    return int(np.sum(np.any(np.asarray(p[0]) != P.O.OP_PASS, axis=1)))


def test_hire_head_moves_crew(monkeypatch):
    v = _view(day=15, money=20_000, nquad=3, n_wh=20)
    base = _plan(v)
    monkeypatch.setattr(P, 'ROUTE_NN_ON', True)
    seen = {}
    for d in (-2, 0, 2):
        monkeypatch.setattr(P, 'ROUTE_NN_HIRE_FN', lambda h, d=d: d)
        seen[d] = _plan(v)
    assert _pin.digest(seen[0]) == _pin.digest(base)          # delta 0 == OFF
    assert _units(seen[-2]) < _units(seen[0]) <= _units(seen[2])


def _obs():
    tiles = [[None] * 10 for _ in range(10)]
    tiles[3][3] = dict(kind='PLANT', crop='WHEAT', planted_day=12, watered_today=False, consecutive_unwatered=1,
                       yield_units=0, fertilized_until_day=-1)
    tiles[5][5] = dict(kind='PLANT', crop='CARROT', planted_day=10, watered_today=True, consecutive_unwatered=0,
                       yield_units=2, fertilized_until_day=-1)
    farm = dict(farmer=[0, 0], hands=[[4, 3]], money=5000, tiles=tiles)
    opp = dict(farmer=[0, 0], hands=[], money=4000, tiles=[[None] * 10 for _ in range(10)])
    return dict(day=15, hour=20, step=15 * 24 + 20, player=0, farms=[farm, opp],
                market=dict(prices=dict(WHEAT=20, CARROT=40)),
                private=dict(seeds={}, shed={}, inventories=[{}, {}]))


class _RT:
    pass


def test_dispatch_env(monkeypatch):
    from kagg3.agent import route_nn as RN      # lazy: the parity subprocess runs this file on master's src
    p = RN.init_params(0)
    p['pass_b'][:] = -10.0                        # never PASS: take the best legal task
    monkeypatch.setattr(RN, 'PARAMS', p)
    monkeypatch.setattr(RN, 'SAMPLE_RNG', None)
    rec = []
    monkeypatch.setattr(RN, 'RECORD', rec)
    ops = np.full((2, 24), P.O.OP_PASS, np.int32)
    ops[0, 22] = P.O.OP_EAST                        # the farmer still has planned work -> untouched
    plan = (ops, np.zeros_like(ops), np.zeros_like(ops), np.zeros(24, np.int32))
    act = dict(farmer=['PASS'], hands=[['PASS']], market=[])
    out = RN.step(_RT(), _obs(), act, plan)
    assert out['farmer'] == ['PASS']
    cmd = out['hands'][0]
    assert cmd[0] in ('WEST', 'EAST', 'NORTH', 'SOUTH', 'WATER', 'HARVEST')
    assert len(rec) == 1 and rec[0]['kind'] == 0 and rec[0]['a'] > 0
    assert rec[0]['mask'][0] == 1 and rec[0]['mask'].sum() >= 3      # PASS + water + harvest candidates
    lg = RN.dispatch_logits(np, p, rec[0]['glob'], rec[0]['hand'], rec[0]['tasks'], rec[0]['mask'])
    assert np.all(lg[rec[0]['mask'] == 0] < -1e8)


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
