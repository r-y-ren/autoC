"""EXPIRY1: dawn decay, same-day chains, funded fill, and master parity."""
import _pin
_pin.bootstrap()
import numpy as np
import pytest
from test_budget_order import _macro
from test_plant_fill_late import _view
from kagg3 import spec
from kagg3.core import brain, ops as O, plan as P

PRE_SWITCH = '855aca9ad4eda2297c3962182ca47faf08af5497'


def _expiry_view(day=20, crop=spec.I_TOMATO, held=0, delta=1):
    v = _view(day=day, money=20_000, nquad=4)
    v.kind[:] = spec.KIND_LOCKED
    v.kind[0] = spec.KIND_PLANT
    v.occ[0] = crop
    last_age = spec.CROP_FIRST_YIELD_DAY[crop] + (spec.CROP_MAX_YIELD[crop]-1)*spec.CROP_INTERVAL[crop]
    v.t_day[0] = day - last_age - delta
    v.t_yield[0] = held
    return v


def _own_digests():
    target = np.array([1, 0, 0, 0, 0], np.int32)
    boards = [('opening', _view(day=0, money=3_000)),
              ('expiry', _expiry_view()),
              ('late', _view(day=27, money=40_000, nquad=4, n_wh=28))]
    return {name: _pin.digest(P.build_day(np, v, _macro(plant_target=target)))
            for name, v in boards}


def test_off_master_three_board_parity():
    assert P.EXPIRY_SLOT_ON is False and P.ASK_FILL_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=PRE_SWITCH)


@pytest.mark.parametrize('crop', [spec.I_TOMATO, spec.I_STRAWBERRY])
@pytest.mark.parametrize('delta,held,expected', [(0,0,False),(1,0,True),(2,0,True),(1,1,False)])
def test_expiry_boundary_and_brain_agree(monkeypatch, crop, delta, held, expected):
    v = _expiry_view(crop=crop, delta=delta, held=held)
    assert bool(P._expiry_slots(np, v)[0]) == expected
    assert int(brain.n_free_slots(np, v)) == 0
    monkeypatch.setattr(P, 'EXPIRY_SLOT_ON', True)
    assert int(brain.n_free_slots(np, v)) == int(expected)
    v.kind[0] = spec.KIND_LOCKED
    assert not P._expiry_slots(np, v).any()


def _derive(v, m, bill=0, reserve=0, ask_fill=True):
    return P._derive(np, v, m, P.default_price_table(), np.int32(bill),
                     np.bool_(v.day == 29), np.int32(reserve), ask_fill=ask_fill)


def test_expiry_emits_funded_dig_plant_water(monkeypatch):
    v = _expiry_view()
    m = _macro(plant_target=np.array([1,0,0,0,0], np.int32))
    assert O.OP_PLANT not in _derive(v, m).chain_op[0]
    monkeypatch.setattr(P, 'EXPIRY_SLOT_ON', True)
    d = _derive(v, m)
    assert list(d.chain_op[0][:3]) == [O.OP_DIG, O.OP_PLANT, O.OP_WATER]
    assert int(d.seed_buy[spec.I_WHEAT]) == 1
    poor = _derive(v._replace(money=np.int32(9)), m)
    assert O.OP_PLANT not in poor.chain_op[0]
    reserved = _derive(v._replace(money=np.int32(109)), m, bill=50, reserve=50)
    assert O.OP_PLANT not in reserved.chain_op[0]


def _fill_inputs(purse=60, stock=0):
    v = _view(day=12)
    v.seeds[spec.I_CARROT] = stock
    values = np.zeros((P.BUD.N_LISTS, P.PJ.K), np.int32)
    costs = np.ones_like(values)
    values[P.BUD.L_SEED0 + spec.I_WHEAT] = 20
    values[P.BUD.L_SEED0 + spec.I_CARROT] = 80
    costs[P.BUD.L_SEED0:P.BUD.L_SEED0+spec.N_CROPS] = spec.CROP_SEED_COST[:,None]
    buys = np.zeros(P.BUD.N_LISTS, np.int32)
    buys[P.BUD.L_SEED0] = 1
    target = np.array([1,0,0,0,0], np.int32)
    return v, target, np.int32(10), values, costs, buys, np.int32(purse)


def test_fill_uses_ranked_choice_and_only_ledger_leftover():
    args = _fill_inputs(purse=70)
    target, buys = P._ask_fill(np, *args)
    assert target.tolist() == [1,3,0,0,0]
    assert int(P.BUD.spend(np, args[4], buys)) == 70
    assert np.all(buys >= args[5])
    # Stored seeds are free; the pre-existing 10-coin wheat grant stays paid.
    target, buys = P._ask_fill(np, *_fill_inputs(purse=10, stock=4))
    assert target.tolist() == [1,4,0,0,0]
    assert int(buys.sum()) == 1


def test_fill_respects_horizon_and_capacity():
    args = list(_fill_inputs(purse=1000))
    args[2] = np.int32(2)
    target, _ = P._ask_fill(np, *args)
    assert int(target.sum()) == 2
    args[0] = args[0]._replace(day=np.int32(28))
    target, buys = P._ask_fill(np, *args)
    assert np.array_equal(target, args[1])
    assert np.array_equal(buys, args[5])


def test_fill_reaches_last_slot_and_preserves_reserve(monkeypatch):
    v = _view(day=20, money=200, nquad=4)
    v.kind[:] = spec.KIND_LOCKED
    v.kind[:5] = spec.KIND_EMPTY
    m = _macro(plant_target=np.array([1,0,0,0,0], np.int32))
    base = _derive(v, m, bill=50, reserve=50)
    monkeypatch.setattr(P, 'ASK_FILL_ON', True)
    d = _derive(v, m, bill=50, reserve=50)
    assert O.OP_PLANT not in base.chain_op[4]
    assert O.OP_PLANT in d.chain_op[4]
    assert int((d.seed_buy * spec.CROP_SEED_COST).sum()) <= 100
    # The hire-scoring pass is unchanged by ASK_FILL.
    scan = _derive(v, m, bill=50, reserve=50, ask_fill=False)
    assert np.array_equal(scan.chain_op, base.chain_op)


def test_fill_never_spends_existing_nonseed_grants():
    args = list(_fill_inputs(purse=75))
    args[5][P.BUD.L_FERT] = 5
    target, buys = P._ask_fill(np, *args)
    assert target.tolist() == [1,3,0,0,0]
    assert int(buys[P.BUD.L_FERT]) == 5
    assert int(P.BUD.spend(np, args[4], buys)) == 75


def test_fill_numpy_jax_agree():
    import jax.numpy as jnp
    args = _fill_inputs(purse=93, stock=2)
    expected = P._ask_fill(np, *args)
    got = P._ask_fill(jnp, *args)
    for a, b in zip(expected, got):
        np.testing.assert_array_equal(a, np.asarray(b))
    np.testing.assert_array_equal(P._expiry_slots(np, _expiry_view()),
                                  np.asarray(P._expiry_slots(jnp, _expiry_view())))


if __name__ == '__main__':
    for name, digest in _own_digests().items():
        print(name, digest)
