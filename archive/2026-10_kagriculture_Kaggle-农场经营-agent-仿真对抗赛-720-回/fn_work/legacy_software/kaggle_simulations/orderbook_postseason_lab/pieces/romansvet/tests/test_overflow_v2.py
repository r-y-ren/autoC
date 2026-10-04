"""OVERFLOW3: projected-overflow banking (plan.OVERFLOW_GUARD_V2) on the pinned engine."""
import _pin
_pin.bootstrap()
import numpy as np
from kagg3 import spec
from kagg3.core import plan as P, ops as O
from kagg3.agent import overflow, render, runtime
from test_overflow_guard import engine, _plan, _obs, _step  # noqa: F401


def _wheat_tile(day, n=6):
    return {'consecutive_unwatered': 0, 'crop': 'WHEAT', 'fertilized_until_day': -1, 'kind': 'PLANT',
            'max_lifespan_step': (day + 2) * 24, 'planted_day': day - 3, 'watered_today': True,
            'yield_units': n}


def _run_day(engine, plan, obs, v2=True):
    pending, sold = [], 0
    while obs['hour'] < 24:
        overflow.guard(plan, obs, pending)
        if v2:
            overflow.guard_v2(plan, obs, pending)
        sold += _step(engine, plan, obs)
    before = sum(obs['private']['shed'].values()) + sum(sum(v.values()) for v in obs['private']['inventories'])
    engine._drop_inventories_to_shed(obs['private'], 100)
    return sold, before - sum(obs['private']['shed'].values())


def _harvest_case(engine):
    obs = _obs(engine, [{'WHEAT': 50}, {'MILK': 50}], [[1, 5], [0, 0]], hour=14)
    obs['farms'][0]['tiles'][0][0] = _wheat_tile(obs['day'])
    plan = _plan()                           # unit 0 idle 3 tiles from the shed
    plan[0][1, 14:] = O.OP_WATER             # unit 1 busy far away ...
    plan[0][1, 21] = O.OP_HARVEST            # ... and harvests 6 at hour 21: visible only at 22
    return obs, plan


def test_v1_misses_the_projected_harvest(engine):
    obs, plan = _harvest_case(engine)
    sold, lost = _run_day(engine, plan, obs, v2=False)
    assert (sold, lost) == (0, 6)


def test_v2_banks_the_projected_harvest(engine):
    obs, plan = _harvest_case(engine)
    sold, lost = _run_day(engine, plan, obs)
    assert (sold, lost) == (6, 0)
    assert plan[0][1, 21] == O.OP_HARVEST     # the harvest itself is untouched


def test_enroute_insert_shifts_ops_and_drops_one_pass(engine):
    obs = _obs(engine, [{'WHEAT': 110}], [[4, 4]], hour=15)
    plan = _plan()
    plan[0][0, 15:18] = O.OP_WEST
    plan[0][0, 18] = O.OP_WATER
    plan[0][0, 19:] = O.OP_PASS
    plan[0][0, 20:] = O.OP_WATER                # a busy tail: finished-carrier rule can't fire
    overflow.guard_v2(plan, obs, [])
    assert plan[0][0, 15] == O.OP_PLACE and plan[2][0, 15] == 10
    assert list(plan[0][0, 16:20]) == [O.OP_WEST] * 3 + [O.OP_WATER]
    assert list(plan[0][0, 20:]) == [O.OP_WATER] * 4
    assert plan[3][15, 0] == O.MO_SELL and plan[5][15, 0] == 10


def test_under_capacity_is_identity(engine):
    obs, plan = _harvest_case(engine)
    obs['private']['inventories'][1] = {'MILK': 40}
    before = _pin.digest(plan)
    overflow.guard_v2(plan, obs, [])
    assert _pin.digest(plan) == before


def test_runtime_skips_v2_when_off(monkeypatch, engine):
    obs = _obs(engine, [{'WHEAT': 110}]); rt = runtime.Runtime(None)
    rt.plan = _plan(); rt.day = obs['day']
    monkeypatch.setattr(P, 'OVERFLOW_GUARD_V2', False)  # default True since SHIP_OG2
    def forbidden(*a): raise AssertionError('V2 called while OFF')
    monkeypatch.setattr(runtime, 'overflow_guard_v2', forbidden)
    rt.act(obs)
