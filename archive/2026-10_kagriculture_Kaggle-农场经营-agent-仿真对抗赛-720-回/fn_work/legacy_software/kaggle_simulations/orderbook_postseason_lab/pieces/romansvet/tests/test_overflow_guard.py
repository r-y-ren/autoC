"""Overflow rescue: pinned OFF plans and actual engine transfer/sale semantics."""
import _pin
_pin.bootstrap()
import copy
import importlib.util
from pathlib import Path
import sys
import types

import numpy as np
import pytest
from kagg3 import spec
from kagg3.core import plan as P, ops as O
from kagg3.agent import render, runtime
if "--digests" not in sys.argv:
    from kagg3.agent import overflow
from test_route_early import _view
from test_budget_order import _macro

BASE = '64a8b76f06fd2fd810fffbb57cd43a999f237a4c'


def _digests():
    P.OVERFLOW_GUARD_ON = False
    return {str(d): _pin.digest(P.build_day(np, _view(day=d, n_ripe=16,
        n_coop=6, wheat=12, fert=8, nquad=3), _macro())) for d in (0, 13, 29)}


def test_off_three_board_parity():
    assert _digests() == _pin.tree_digests(__file__, BASE)


@pytest.fixture
def engine():
    # Import just the pinned engine, without loading unrelated environments.
    import sysconfig
    pkgdir = Path(sysconfig.get_paths()['purelib']) / 'kaggle_environments'
    pkg = types.ModuleType('kaggle_environments'); pkg.__path__ = [str(pkgdir)]
    sys.modules.setdefault('kaggle_environments', pkg)
    sp = importlib.util.spec_from_file_location('overflow_test_engine',
        pkgdir/'envs/kaggriculture/kaggriculture.py')
    module = importlib.util.module_from_spec(sp); sp.loader.exec_module(module)
    return module


def _plan():
    return tuple(np.zeros((spec.MAX_UNITS if i < 3 else 24,
        24 if i < 3 else spec.MAX_MARKET_ORDERS), np.int32) for i in range(6))


def _obs(engine, inventories, positions=None, shed=None, day=20, hour=18):
    positions = positions or [[4, 4] for _ in inventories]
    farm = engine._new_farm(10, 3000)
    farm['farmer'], farm['hands'] = positions[0], positions[1:]
    return dict(day=day, hour=hour, player=0, farms=[farm],
        private=dict(shed=shed or {}, inventories=copy.deepcopy(inventories), seeds={}),
        market=dict(inventory={p:spec.MARKET_I0 for p in spec.PRODUCTS}))


def _step(engine, plan, obs):
    action=render.turn_action(plan, obs['hour'], len(obs['farms'][0]['hands']))
    farm, private=obs['farms'][0], obs['private']
    for u,a in enumerate([action['farmer'],*action['hands']]):
        engine._apply_unit_action(farm,private,u,a,10,obs['day'],24,100)
    sold=0
    for op,item,n in action['market']:
        assert op=='SELL'
        for _ in range(n):
            sold+=int(engine._commit_unit(op,item,10,farm,private,obs['market'],100))
    obs['hour']+=1
    return sold


def test_carry_is_banked_and_sold_on_the_same_hour(engine):
    obs=_obs(engine,[{'WHEAT':80},{'MILK':30}],[[8,4],[4,4]])
    plan=_plan(); overflow.guard(plan,obs,[])
    assert _step(engine,plan,obs)==10
    engine._drop_inventories_to_shed(obs['private'],100)
    assert sum(obs['private']['shed'].values())==100


def test_return_walk_and_pending_do_not_dispatch_duplicate_rescues(engine):
    obs=_obs(engine,[{'WHEAT':110}],[[7,4]])
    plan=_plan(); pending=[]; sold=0
    for _ in range(3):
        overflow.guard(plan,obs,pending)
        sold+=_step(engine,plan,obs)
    assert sold==10
    assert not any(obs['private']['inventories'][0].get(p,0)<0 for p in spec.PRODUCTS)
    engine._drop_inventories_to_shed(obs['private'],100)
    assert sum(obs['private']['shed'].values())==100


def test_existing_sale_and_nonoverflow_are_identity(engine):
    obs=_obs(engine,[{'WHEAT':95}],shed={'MILK':15})
    plan=_plan(); plan[3][18,0]=O.MO_SELL; plan[4][18,0]=spec.I_MILK; plan[5][18,0]=15
    before=_pin.digest(plan); overflow.guard(plan,obs,[])
    assert _pin.digest(plan)==before


def test_never_diverts_unfinished_harvest_or_feed(engine):
    obs=_obs(engine,[{'WHEAT':110}])
    plan=_plan(); plan[0][0,20]=O.OP_HARVEST
    before=_pin.digest(plan); overflow.guard(plan,obs,[])
    assert _pin.digest(plan)==before
    plan[0][0,20]=O.OP_FEED
    before=_pin.digest(plan); overflow.guard(plan,obs,[])
    assert _pin.digest(plan)==before


def test_full_market_row_blocks_rescue(engine):
    obs=_obs(engine,[{'WHEAT':110}]); plan=_plan()
    plan[3][18,:]=O.MO_HIRE
    before=_pin.digest(plan); overflow.guard(plan,obs,[])
    assert _pin.digest(plan)==before


def test_drop_before_sell_retains_overflow_in_hand(engine):
    obs=_obs(engine,[{'WHEAT':20}],shed={'MILK':95},day=29)
    plan=_plan(); plan[0][0,18]=O.OP_DROP
    plan[3][18,0]=O.MO_SELL; plan[4][18,0]=spec.I_MILK; plan[5][18,0]=95
    overflow.guard(plan,obs,[])
    assert plan[0][0,18]==O.OP_PLACE
    assert _step(engine,plan,obs)==95
    assert obs['private']['inventories'][0]['WHEAT']==15
    engine._drop_inventories_to_shed(obs['private'],100)
    assert sum(obs['private']['shed'].values())==20


def test_no_runtime_guard_call_when_off(monkeypatch,engine):
    obs=_obs(engine,[{}]); rt=runtime.Runtime(None)
    rt.plan=_plan(); rt.day=obs['day']
    monkeypatch.setattr(P,'OVERFLOW_GUARD_ON',False)
    def forbidden(*args): raise AssertionError('OFF called guard')
    monkeypatch.setattr(runtime,'overflow_guard',forbidden)
    assert rt.act(obs)==render.turn_action(rt.plan,obs['hour'],0)


def test_runtime_guard_survives_hidden_source_imports(monkeypatch, engine):
    import builtins
    obs = _obs(engine, [{'WHEAT': 110}])
    rt = runtime.Runtime(None); rt.plan = _plan(); rt.day = obs['day']
    monkeypatch.setattr(P, 'OVERFLOW_GUARD_ON', True)
    original = builtins.__import__
    def no_source_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name.startswith('kagg3') or level:
            raise ImportError('file-agent harness hides the source namespace')
        return original(name, globals, locals, fromlist, level)
    monkeypatch.setattr(builtins, '__import__', no_source_import)
    action = rt.act(obs)
    assert action['farmer'] == ['PLACE', 'WHEAT', 10]
    assert action['market'] == [['SELL', 'WHEAT', 10]]


def test_simultaneous_drops_share_capacity_before_sale(engine):
    obs = _obs(engine, [{'WHEAT': 20}, {'WOOL': 10}], shed={'MILK': 95}, day=29)
    plan = _plan(); plan[0][:2, 18] = O.OP_DROP
    plan[3][18, 0] = O.MO_SELL; plan[4][18, 0] = spec.I_MILK; plan[5][18, 0] = 95
    overflow.guard(plan, obs, [])
    assert _step(engine, plan, obs) == 95
    total = sum(obs['private']['shed'].values()) + sum(sum(v.values()) for v in obs['private']['inventories'])
    assert total == 30  # all cargo survives both unit actions


def test_known_feed_consumption_does_not_trigger_a_sale(engine):
    obs = _obs(engine, [{'WHEAT': 100}, {'WHEAT': 1}], [[4,4],[4,5]])
    obs['farms'][0]['tiles'][5][4] = engine._new_animal('COW', 0)
    plan = _plan(); plan[0][1,18] = O.OP_FEED
    before = _pin.digest(plan)
    overflow.guard(plan, obs, [])
    assert _pin.digest(plan) == before
    assert _step(engine, plan, obs) == 0
    engine._drop_inventories_to_shed(obs['private'], 100)
    assert sum(obs['private']['shed'].values()) == 100


def test_forced_shed_sale_preserves_queued_feed_pickup(engine):
    obs = _obs(engine, [{'MILK': 100}, {}], shed={'WHEAT':1, 'MILK':10})
    plan = _plan(); plan[0][1,18] = O.OP_PICKUP
    plan[1][1,18] = spec.I_WHEAT; plan[2][1,18] = 1
    plan[0][1,19] = O.OP_FEED
    overflow.guard(plan, obs, [])
    action = render.turn_action(plan, 18, 1)
    assert action['market'] == [['SELL', 'MILK', 10]]
    assert _step(engine, plan, obs) == 10
    assert obs['private']['inventories'][1]['WHEAT'] == 1


def test_animal_placement_consumes_capacity_without_forced_sale(engine):
    obs = _obs(engine, [{'WHEAT':100},{'COW':1}], [[4,4],[4,5]])
    obs['farms'][0]['tiles'][5][4] = {'kind':'PASTURE'}
    plan = _plan(); plan[0][1,18] = O.OP_PLACE; plan[1][1,18] = spec.I_COW; plan[2][1,18] = 1
    before = _pin.digest(plan); overflow.guard(plan, obs, [])
    assert _pin.digest(plan) == before
    assert _step(engine,plan,obs) == 0
    engine._drop_inventories_to_shed(obs['private'],100)
    assert sum(obs['private']['shed'].values()) == 100


def test_repeated_pickups_cannot_create_fictitious_shed_room(engine):
    obs = _obs(engine, [{},{},{'WOOL':8}], shed={'MILK':95,'WHEAT':5},day=29)
    plan = _plan(); plan[0][:2,18] = O.OP_PICKUP
    plan[1][:2,18] = spec.I_WHEAT; plan[2][:2,18] = 5
    plan[0][2,18] = O.OP_DROP
    plan[3][18,0] = O.MO_SELL; plan[4][18,0] = spec.I_MILK; plan[5][18,0] = 95
    overflow.guard(plan,obs,[])
    assert plan[0][2,18] == O.OP_PLACE
    assert _step(engine,plan,obs) == 95
    assert obs['private']['inventories'][2]['WOOL'] == 3


def test_pending_delivery_is_not_also_counted_as_a_shed_sale(engine):
    obs = _obs(engine, [{'WHEAT':110}], shed={'WHEAT':10},hour=20)
    plan = _plan(); plan[0][0,22] = O.OP_PLACE
    plan[1][0,22] = spec.I_WHEAT; plan[2][0,22] = 10
    plan[3][22,0] = O.MO_SELL; plan[4][22,0] = spec.I_WHEAT; plan[5][22,0] = 10
    pending = [(22,spec.I_WHEAT,10)]
    overflow.guard(plan,obs,pending)
    # Ten pending carried units plus ten actual shed units, not the same sale twice.
    assert render.turn_action(plan,20,0)['market'] == [['SELL','WHEAT',10]]


if __name__=='__main__':
    for name,digest in _digests().items(): print(name,digest)
