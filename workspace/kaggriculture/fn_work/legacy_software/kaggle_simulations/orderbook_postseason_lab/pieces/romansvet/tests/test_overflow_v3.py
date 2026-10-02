"""OVERFLOW4: value-priced deposit trips (plan.OVERFLOW_GUARD_V3) on the pinned engine."""
import _pin
_pin.bootstrap()
import copy
import importlib.util
import sys
import sysconfig
import types
from pathlib import Path

import numpy as np
import pytest
from kagg3 import spec
from kagg3.core import plan as P, ops as O
from kagg3.agent import overflow, render, runtime

BASE = 'd0acc42af08ee924a6602c52b12f8116835cdcfb'


def _engine():
    pkgdir = Path(sysconfig.get_paths()['purelib']) / 'kaggle_environments'
    pkg = types.ModuleType('kaggle_environments'); pkg.__path__ = [str(pkgdir)]
    sys.modules.setdefault('kaggle_environments', pkg)
    sp = importlib.util.spec_from_file_location('overflow_v3_engine', pkgdir/'envs/kaggriculture/kaggriculture.py')
    m = importlib.util.module_from_spec(sp); sp.loader.exec_module(m)
    return m


@pytest.fixture
def engine():
    return _engine()


def _plan():
    return tuple(np.zeros((spec.MAX_UNITS if i < 3 else 24, 24 if i < 3 else spec.MAX_MARKET_ORDERS), np.int32)
                 for i in range(6))


def _obs(engine, inventories, positions, day=14, hour=14):
    farm = engine._new_farm(10, 3000)
    farm['farmer'], farm['hands'] = positions[0], positions[1:]
    return dict(day=day, hour=hour, player=0, farms=[farm],
                private=dict(shed={}, inventories=copy.deepcopy(inventories), seeds={}),
                market=dict(inventory={p: spec.MARKET_I0 for p in spec.PRODUCTS}))


def _wheat(day, age=3, n=4, watered=True, dry=0):
    return {'consecutive_unwatered': dry, 'crop': 'WHEAT', 'fertilized_until_day': -1, 'kind': 'PLANT',
            'max_lifespan_step': (day - age + 5) * 24, 'planted_day': day - age, 'watered_today': watered,
            'yield_units': n}


def _step(engine, plan, obs):
    action = render.turn_action(plan, obs['hour'], len(obs['farms'][0]['hands']))
    farm, private = obs['farms'][0], obs['private']
    for u, a in enumerate([action['farmer'], *action['hands']]):
        engine._apply_unit_action(farm, private, u, a, 10, obs['day'], 24, 100)
    sold = 0
    for op, item, n in action['market']:
        for _ in range(n):
            sold += int(engine._commit_unit(op, item, 10, farm, private, obs['market'], 100))
    obs['hour'] += 1
    return sold


def _run_day(engine, plan, obs, v3=True):
    pending, sold = [], 0
    while obs['hour'] < 24:
        overflow.guard(plan, obs, pending)
        overflow.guard_v2(plan, obs, pending)
        if v3:
            overflow.guard_v3(plan, obs, pending)
        sold += _step(engine, plan, obs)
    before = sum(obs['private']['shed'].values()) + sum(sum(v.values()) for v in obs['private']['inventories'])
    engine._drop_inventories_to_shed(obs['private'], 100)
    return sold, before - sum(obs['private']['shed'].values())


def _busy_case(engine, tile):
    """Unit 0 one step from the shed, WATERing its tile until dusk with 110 wheat aboard."""
    obs = _obs(engine, [{'WHEAT': 110}], [[3, 4]])
    obs['farms'][0]['tiles'][4][3] = tile
    plan = _plan(); plan[0][0, 14:] = O.OP_WATER
    return obs, plan


def test_v2_leaves_busy_to_dusk_overflow(engine):
    obs, plan = _busy_case(engine, _wheat(14))
    assert _run_day(engine, plan, obs, v3=False) == (0, 10)


def test_v3_displaces_zero_value_water_and_banks(engine):
    obs, plan = _busy_case(engine, _wheat(14))              # already watered today: WATER is worth 0
    assert _run_day(engine, plan, obs) == (10, 0)


def test_v3_never_displaces_a_must_water(engine):
    obs, plan = _busy_case(engine, _wheat(14, watered=False, dry=1))   # dies tonight unwatered
    plan[0][0, 14:23] = O.OP_PASS                           # the single WATER is the last op
    before = [a.copy() for a in plan]
    overflow.guard_v3(plan, obs, [])
    assert all((a == b).all() for a, b in zip(plan, before))


def test_v3_never_displaces_feed(engine):
    obs, plan = _busy_case(engine, _wheat(14))
    plan[0][0, 14:] = O.OP_FEED
    before = [a.copy() for a in plan]
    overflow.guard_v3(plan, obs, [])
    assert all((a == b).all() for a, b in zip(plan, before))


def test_v3_cuts_a_harvest_into_destruction_when_crop_keeps(engine):
    obs = _obs(engine, [{'WHEAT': 100}], [[0, 0]])
    obs['farms'][0]['tiles'][0][0] = _wheat(14, age=3, n=6)    # ripe, max-yield day is tomorrow
    plan = _plan(); plan[0][0, 14:] = O.OP_WATER; plan[0][0, 23] = O.OP_HARVEST
    sold, lost = _run_day(engine, plan, obs)
    assert (sold, lost) == (0, 0)
    assert obs['farms'][0]['tiles'][0][0]['yield_units'] == 6   # left ripe for tomorrow


def test_v3_keeps_a_harvest_that_would_rot(engine):
    obs = _obs(engine, [{'WHEAT': 100}], [[0, 0]])
    obs['farms'][0]['tiles'][0][0] = _wheat(14, age=4, n=6)    # last day before rot
    plan = _plan(); plan[0][0, 14:] = O.OP_WATER; plan[0][0, 23] = O.OP_HARVEST
    overflow.guard_v3(plan, obs, [])
    assert plan[0][0, 23] == O.OP_HARVEST


def test_under_capacity_is_identity(engine):
    obs, plan = _busy_case(engine, _wheat(14))
    obs['private']['inventories'][0] = {'WHEAT': 90}
    before = _pin.digest(plan)
    overflow.guard_v3(plan, obs, [])
    assert _pin.digest(plan) == before


def test_runtime_skips_v3_when_off(monkeypatch, engine):
    monkeypatch.setattr(P, 'OVERFLOW_GUARD_V3', False)  # default True since SHIP_OG3
    obs = _obs(engine, [{'WHEAT': 110}], [[4, 4]]); rt = runtime.Runtime(None)
    rt.plan = _plan(); rt.day = obs['day']
    def forbidden(*a): raise AssertionError('V3 called while OFF')
    monkeypatch.setattr(runtime, 'overflow_guard_v3', forbidden)
    rt.act(obs)


def _digests():
    """Guard pipeline (V1+V2, +V3 iff the tree's flag says so) over hours 10-23 on 3 boards."""
    eng = _engine(); out = {}
    for name, inv, pos, tile_at in (('busy', [{'WHEAT': 110}], [[3, 4]], (3, 4)),
                                    ('crew', [{'WHEAT': 60}, {'CARROT': 50}, {'MILK': 20}],
                                     [[3, 4], [0, 0], [9, 9]], (0, 0)),
                                    ('under', [{'WHEAT': 40}], [[1, 1]], (1, 1))):
        obs = _obs(eng, inv, pos, hour=10)
        obs['farms'][0]['tiles'][tile_at[1]][tile_at[0]] = _wheat(14)
        plan = _plan(); plan[0][:len(pos), 10:] = O.OP_WATER; plan[0][:len(pos), 23] = O.OP_HARVEST
        pending = []
        for h in range(10, 24):
            obs['hour'] = h
            overflow.guard(plan, obs, pending)
            overflow.guard_v2(plan, obs, pending)
            if getattr(P, 'OVERFLOW_GUARD_V3', False):
                overflow.guard_v3(plan, obs, pending)
        out[name] = _pin.digest(plan)
    return out


def test_off_three_board_parity(monkeypatch):
    monkeypatch.setattr(P, 'OVERFLOW_GUARD_V3', False)  # default True since SHIP_OG3; OFF == cfog2 tree
    assert _digests() == _pin.tree_digests(__file__, BASE)


if __name__ == '__main__':
    for name, digest in _digests().items():
        print(name, digest)
