"""WOOLFIRST1: d0--2 herd = 2 cows + 3 sheep, wool reservation void; OFF byte parity."""
from __future__ import annotations

import os
import sys
import types

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro, _view

from kagg3.core import ops as O
from kagg3.core import plan as P
from kagg3 import spec

BASE = "8c81fd87"


def _target(want, day):
    return P._wool_first(np, types.SimpleNamespace(day=np.int32(day)),
                         _macro(animal_want=np.asarray(want, np.int32))).animal_want.tolist()


def test_defaults_ship_off():
    assert P.WOOL_FIRST_ON is False
    assert (P.WOOL_FIRST_COWS, P.WOOL_FIRST_SHEEP, P.WOOL_FIRST_GEESE, P.WOOL_FIRST_SELL) == (2, 3, 0, True)


@pytest.mark.parametrize("day", [0, 1, 2])
def test_opening_herd_is_two_cows_three_sheep_no_geese(day, monkeypatch):
    assert _target([1, 4, 1], day) == [0, 2, 3]
    assert _target([0, 1, 5], day) == [0, 2, 3]
    monkeypatch.setattr(P, "WOOL_FIRST_GEESE", -1)
    assert _target([1, 4, 1], day) == [1, 2, 3]


def test_late_days_untouched():
    assert _target([1, 4, 1], 3) == [1, 4, 1]


def test_opening_herd_reaches_the_purchase_row(monkeypatch):
    monkeypatch.setattr(P, "WOOL_FIRST_ON", True)
    macro = _macro(animal_want=np.asarray([1, 4, 1], np.int32))
    op, arg, qty = P.build_day(np, _view(5_000), macro)[3:6]
    buy = op == O.MO_BUY_ANIMAL
    assert int(qty[buy & (arg == P._A_SHEEP)].sum()) == 3
    assert int(qty[buy & (arg == spec.ANIMALS.index("COW"))].sum()) <= 2


def test_wool_hold_void_off_terminal(monkeypatch):
    monkeypatch.setattr(P, "WOOL_FIRST_ON", True)
    hold = np.full(spec.N_PRODUCTS, 150, np.int32)
    out = P._sell_hold(np, None, hold, np.bool_(False), day=5)
    assert out[spec.I_WOOL] == 0 and out[spec.I_MILK] == 150


PIN_BOARDS = (("d0", 0, 3_000), ("d2", 2, 1_200), ("d10", 10, 20_000))


def _digests():
    out = {}
    for name, day, money in PIN_BOARDS:
        view = _view(money)._replace(day=np.int32(day))
        out[name] = _pin.digest(P.build_day(np, view, _macro()))
    return out


def test_off_is_byte_identical_to_master_on_three_boards(monkeypatch):
    monkeypatch.setattr(P, "WOOL_FIRST_ON", False)
    assert _digests() == _pin.tree_digests(__file__, BASE)


if __name__ == "__main__":
    want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    import kagg3
    assert os.path.abspath(kagg3.__file__).startswith(want + os.sep)
    for key, value in _digests().items():
        print(key, value)
