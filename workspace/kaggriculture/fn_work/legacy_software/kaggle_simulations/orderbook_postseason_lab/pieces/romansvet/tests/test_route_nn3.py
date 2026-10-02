"""ROUTENN3: ROUTE_NN3_ON -- OFF 3-board parity vs master; init params reproduce the plan (argmax KEEP);
a forced deviation takes another unit's planned stop and moves both units to the QUEUE executor."""
import _pin
_pin.bootstrap()
import numpy as np
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3.core import plan as P

BASE = '6da0b9ea'   # master at branch time
TGT = np.array([2, 1, 0, 0, 0], np.int32)


def _boards():
    return [('opening', _view(day=0, money=3_000)),
            ('mid', _view(day=15, money=20_000, nquad=3, n_wh=20)),
            ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]


def _own_digests():
    return {n: _pin.digest(tuple(np.asarray(a) for a in P.build_day(np, v, _macro(plant_target=TGT))))
            for n, v in _boards()}


def test_off_three_board_parity():
    assert P.ROUTE_NN3_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=BASE)


def _obs(hour):
    tiles = [[None] * 10 for _ in range(10)]
    for x in (2, 6):
        tiles[3][x] = dict(kind='PLANT', crop='WHEAT', planted_day=12, watered_today=False, consecutive_unwatered=1,
                           yield_units=0, fertilized_until_day=-1)
    farm = dict(farmer=[4, 4], hands=[[5, 4]], money=5000, tiles=tiles)
    opp = dict(farmer=[0, 0], hands=[], money=4000, tiles=[[None] * 10 for _ in range(10)])
    return dict(day=15, hour=hour, step=15 * 24 + hour, player=0, farms=[farm, opp],
                market=dict(prices=dict(WHEAT=20)), private=dict(seeds={}, shed={}, inventories=[{}, {}]))


def _plan():
    O = P.O
    ops = np.full((2, 24), O.OP_PASS, np.int32)
    ops[0, 1:3] = O.OP_WEST; ops[0, 3] = O.OP_NORTH; ops[0, 4] = O.OP_WATER        # farmer -> (2,3) water
    ops[1, 1] = O.OP_EAST; ops[1, 2] = O.OP_NORTH; ops[1, 3] = O.OP_WATER          # hand -> (6,3) water
    z = np.zeros_like(ops)
    return (ops, z, z, np.zeros((24, 10), np.int32), np.zeros((24, 10), np.int32), np.zeros((24, 10), np.int32))


class _RT:
    pass


def _run(p, hours):
    from kagg3.agent import route_nn3 as RN
    from kagg3.agent import render
    RN.PARAMS, RN.SAMPLE_RNG, RN.RECORD = p, None, []
    rt, plan, outs = _RT(), _plan(), []
    for h in hours:
        act = render.turn_action(plan, h, 1)
        outs.append((act, RN.step(rt, _obs(h), act, plan)))
    rec = RN.RECORD
    RN.PARAMS, RN.RECORD = None, None
    return outs, rec, rt


def test_init_keeps_plan():
    from kagg3.agent import route_nn3 as RN
    outs, rec, _ = _run(RN.init_params(0), range(0, 2))     # static obs: positions valid for h0-1
    assert all(a == b for a, b in outs)
    assert rec and all(r['a'] == 0 for r in rec)


def test_forced_deviation_queue():
    from kagg3.agent import route_nn3 as RN
    p = RN.init_params(0)
    p['pass_b'][:] = -20.0                      # never KEEP
    outs, rec, rt = _run(p, [0, 1])
    assert outs[0][0] == outs[0][1]             # h0 = plan (hire spawn occupancy)
    assert rec[0]['a'] > 0 and rec[0]['mask'][0] == 1
    assert rt._rn3['mode'].get(0) == 'q' or rt._rn3['mode'].get(1) == 'q'
    assert rt._rn3['taken']
    lg = RN.logits(np, p, rec[0]['glob'], rec[0]['hand'], rec[0]['tasks'], rec[0]['mask'])
    assert np.all(lg[rec[0]['mask'] == 0] < -1e8)


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
