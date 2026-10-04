"""SHEEPFIRST1: d0--2 sheep target, with cow-swap and additive modes."""
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

BASE = "ed3cd697"


def _target(want, day, n=3, mode="swap"):
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(P, "SHEEP_FIRST_N", n)
        mp.setattr(P, "SHEEP_FIRST_MODE", mode)
        return P._sheep_first(
            np, types.SimpleNamespace(day=np.int32(day)),
            _macro(animal_want=np.asarray(want, np.int32)),
        ).animal_want.tolist()


def test_defaults_ship_off():
    assert P.SHEEP_FIRST_ON is False
    assert P.SHEEP_FIRST_N == 3
    assert P.SHEEP_FIRST_MODE == "swap"


@pytest.mark.parametrize("day", [0, 1, 2])
def test_swap_replaces_cows_until_the_sheep_target(day):
    assert _target([1, 4, 1], day) == [1, 2, 3]
    assert _target([1, 4, 4], day) == [1, 4, 4]
    assert _target([1, 1, 1], day, n=4) == [1, 0, 4]


def test_add_keeps_the_decoded_herd_and_late_days_are_untouched():
    assert _target([1, 4, 1], 2, mode="add") == [1, 4, 3]
    assert _target([1, 4, 1], 3, mode="add") == [1, 4, 1]
    assert _target([1, 4, 1], 3, mode="swap") == [1, 4, 1]


@pytest.mark.parametrize("mode,n", [("other", 3), ("swap", -1)])
def test_bad_configuration_is_refused(mode, n):
    with pytest.raises(ValueError):
        _target([1, 4, 1], 0, n=n, mode=mode)


def test_opening_target_reaches_the_existing_purchase_row(monkeypatch):
    monkeypatch.setattr(P, "SHEEP_FIRST_ON", True)
    monkeypatch.setattr(P, "SHEEP_FIRST_N", 3)
    monkeypatch.setattr(P, "SHEEP_FIRST_MODE", "swap")
    macro = _macro(animal_want=np.asarray([1, 4, 1], np.int32))
    op, arg, qty = P.build_day(np, _view(5_000), macro)[3:6]
    sheep = (op == O.MO_BUY_ANIMAL) & (arg == P._A_SHEEP)
    assert int(qty[sheep].sum()) == 3


PIN_BOARDS = (
    ("d0", 0, 3_000),
    ("d2", 2, 1_200),
    ("d10", 10, 20_000),
)


def _digests():
    out = {}
    for name, day, money in PIN_BOARDS:
        view = _view(money)._replace(day=np.int32(day))
        out[name] = _pin.digest(P.build_day(np, view, _macro()))
    return out


def test_off_is_byte_identical_to_master_on_three_boards(monkeypatch):
    monkeypatch.setattr(P, "SHEEP_FIRST_ON", False)
    assert _digests() == _pin.tree_digests(__file__, BASE)


if __name__ == "__main__":
    want = os.path.abspath(sys.argv[sys.argv.index("--digests") + 1])
    import kagg3
    assert os.path.abspath(kagg3.__file__).startswith(want + os.sep)
    for key, value in _digests().items():
        print(key, value)
