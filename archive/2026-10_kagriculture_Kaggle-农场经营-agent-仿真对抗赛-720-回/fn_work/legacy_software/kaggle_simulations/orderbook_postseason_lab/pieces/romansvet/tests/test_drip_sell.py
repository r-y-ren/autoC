"""DRIPSELL1: DRIP_SELL_ON splits the LOT4 (turn 17) row into small post-draw lots."""
import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import ops as O
from kagg3.core import plan as P

T, MO = spec.TURNS_PER_DAY, 10
M, W, S = spec.I_MILK, spec.I_WOOL, spec.I_STRAWBERRY


def _rows():
    op = np.zeros((T, MO), np.int32); arg = np.zeros((T, MO), np.int32); qty = np.zeros((T, MO), np.int32)
    op[:, :] = O.MO_NONE
    lot = np.zeros(spec.N_PRODUCTS, np.int32); lot[M] = 5; lot[W] = 2; lot[S] = 3
    op[17, :spec.N_PRODUCTS] = np.where(lot > 0, O.MO_SELL, O.MO_NONE); arg[17, :spec.N_PRODUCTS] = np.arange(spec.N_PRODUCTS); qty[17, :spec.N_PRODUCTS] = lot
    op[1, 0] = O.MO_SELL; arg[1, 0] = M; qty[1, 0] = 4          # a dawn lot already selling milk on turn 1
    op[1, 1] = O.MO_BUY_PRODUCT; arg[1, 1] = spec.I_WHEAT; qty[1, 1] = 9
    return op, arg, qty


@pytest.fixture
def knobs(monkeypatch):
    def set_(**kw):
        for k, v in kw.items():
            monkeypatch.setattr(P, k, v)
    return set_


def _units(op, arg, qty, t, p):
    return int(qty[t][(op[t] == O.MO_SELL) & (arg[t] == p)].sum())


def test_off_gate_is_identity(knobs):
    op, arg, qty = _rows()
    o2, a2, q2 = P._drip_sell(np, op, arg, qty, False)
    assert (o2 == op).all() and (a2 == arg).all() and (q2 == qty).all()


def test_split_lot1_all_products(knobs):
    knobs(DRIP_SELL_LOT=1, DRIP_SELL_TURNS="1:5:9:13:21", DRIP_SELL_PRODUCTS="SMW")
    op, arg, qty = _rows()
    o, a, q = P._drip_sell(np, op, arg, qty, True)
    # milk 5: 1 merged into the turn-1 SELL (4 -> 5), then 5, 9, 13, 21 -> 0 left on 17
    assert _units(o, a, q, 1, M) == 5 and [_units(o, a, q, t, M) for t in (5, 9, 13, 21)] == [1, 1, 1, 1]
    assert _units(o, a, q, 17, M) == 0 and not ((o[17] == O.MO_SELL) & (a[17] == M)).any()
    # wool 2: turns 1 and 5, nothing left
    assert [_units(o, a, q, t, W) for t in (1, 5, 9, 17)] == [1, 1, 0, 0]
    # strawberry 3: turns 1, 5, 9
    assert [_units(o, a, q, t, S) for t in (1, 5, 9, 13, 17)] == [1, 1, 1, 0, 0]
    # the turn-1 wheat buy survives; units conserved
    assert o[1, 1] == O.MO_BUY_PRODUCT and q[1, 1] == 9
    for p, n in ((M, 5 + 4), (W, 2), (S, 3)):
        assert sum(_units(o, a, q, t, p) for t in range(T)) == n


def test_lot2_milk_wool_only(knobs):
    knobs(DRIP_SELL_LOT=2, DRIP_SELL_TURNS="5:9", DRIP_SELL_PRODUCTS="MW")
    op, arg, qty = _rows()
    o, a, q = P._drip_sell(np, op, arg, qty, True)
    assert [_units(o, a, q, t, M) for t in (5, 9, 17)] == [2, 2, 1]
    assert [_units(o, a, q, t, W) for t in (5, 17)] == [2, 0]
    assert _units(o, a, q, 17, S) == 3


def test_full_row_moves_nothing(knobs):
    knobs(DRIP_SELL_LOT=2, DRIP_SELL_TURNS="5", DRIP_SELL_PRODUCTS="M")
    op, arg, qty = _rows()
    op[5, :] = O.MO_BUY_SEED; qty[5, :] = 1
    o, a, q = P._drip_sell(np, op, arg, qty, True)
    assert _units(o, a, q, 17, M) == 5 and (o[5] == O.MO_BUY_SEED).all()


def test_defaults_off():
    assert P.DRIP_SELL_ON is False
