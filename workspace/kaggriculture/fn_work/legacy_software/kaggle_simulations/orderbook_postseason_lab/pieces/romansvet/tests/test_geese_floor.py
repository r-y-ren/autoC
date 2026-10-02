"""GEESE1: `plan.GEESE_TARGET` is a floor on the GOOSE lane, inert at 0."""
import types

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import plan


def _macro(want):
    m = plan.Macro(*[None] * len(plan.Macro._fields))
    return m._replace(animal_want=np.asarray(want, np.int32))


def _view(day):
    return types.SimpleNamespace(day=np.int32(day), kind=np.zeros(100, np.int32),
                                 occ=np.full(100, -1, np.int32))


@pytest.mark.parametrize("day", [0, 1, 2, 6, 29])
def test_floor_off_is_the_decode(monkeypatch, day):
    monkeypatch.setattr(plan, "GEESE_TARGET", 0)
    out = plan._geese_floor(np, _view(day), _macro([1, 3, 2]))
    assert out.animal_want.tolist() == [1, 3, 2]


def test_floor_raises_the_goose_lane_only():
    out = plan._geese_floor(np, _view(6), _macro([1, 3, 2]))
    # GEESE_TARGET is 0 by default, so name the dose explicitly.
    assert out.animal_want.tolist() == [1, 3, 2]
    with pytest.MonkeyPatch.context() as mp:
        mp.setattr(plan, "GEESE_TARGET", 4)
        out = plan._geese_floor(np, _view(6), _macro([1, 3, 2]))
        assert out.animal_want.tolist() == [4, 3, 2]
        # a decode that already wants more keeps its want: max, not a write
        out = plan._geese_floor(np, _view(6), _macro([6, 3, 2]))
        assert out.animal_want.tolist() == [6, 3, 2]
        # before GEESE_DAY0 the floor is zero
        out = plan._geese_floor(np, _view(plan.GEESE_DAY0 - 1), _macro([1, 3, 2]))
        assert out.animal_want.tolist() == [1, 3, 2]
        out = plan._geese_floor(np, _view(plan.GEESE_DAY0), _macro([1, 3, 2]))
        assert out.animal_want.tolist() == [4, 3, 2]


def test_goose_is_animal_column_zero():
    assert plan._A_GOOSE == spec.ANIMALS.index("GOOSE") == 0
    assert plan._A_GOOSE != spec.I_GOOSE
