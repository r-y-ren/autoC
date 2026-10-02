"""`plan.RESIDUAL_ON`: the residual action head [ACTIONRL].

The `test_off_*` half is the identity half, and it is the same contract
`test_melon_plate.py` holds the programmable plate to: `RESIDUAL_ON = False` is
read at TRACE time by `residual_on`, which short-circuits before it imports a
module or touches the disk, so `_residual_override` is never called and the
expression the planner builds is character for character the one it built
before the head existed.  `PIN` below is literally `test_melon_plate.PIN` --
digests taken off the **pre-switch master tree** (`d35fcfb9`) at the SHIPPED
switch defaults.  The head has to leave them where the plate left them.

The `test_on_*` half pins the four clamps.  They are asserted in the planner
and not trusted from the net, because a half-trained head writing a negative
`plant_target` would be a silent invariant break rather than an error
(ACTIONRL1 section 1: there is no plan validator).
"""
from __future__ import annotations

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_melon_plate import PIN
from test_route_early import PIN_SEEDS, _digest, _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.core import plan as P


def _fn(d_plant=0, d_animal=0, d_hire=0, hold_num=2, box=None):
    """A constant head, in `RESIDUAL_FN`'s wire format."""
    def fn(feats, macro_fields):
        if box is not None:
            box.append((np.asarray(feats), dict(macro_fields)))
        return {
            "d_plant": np.full(spec.N_CROPS, d_plant, np.int32),
            "d_animal": np.full(spec.N_ANIMALS, d_animal, np.int32),
            "d_hire": np.int32(d_hire),
            "hold_num": np.full(spec.N_PRODUCTS, hold_num, np.int32),
        }
    return fn


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "RESIDUAL_ON", False)
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    monkeypatch.setattr(P, "RESIDUAL_HEAD", "")


def _on(monkeypatch, **kw):
    monkeypatch.setattr(P, "RESIDUAL_ON", True)
    monkeypatch.setattr(P, "RESIDUAL_FN", _fn(**kw))


# =========================================================================
# OFF: byte-identical to the planner the head was cut into
# =========================================================================

def test_off_plan_is_byte_identical_to_the_pre_switch_planner(off):
    """The contract: OFF every expression is the one it replaced, so the
    shipped theta decodes byte for byte and the ESR package is untouched."""
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS[:2])
    assert got == PIN


def test_off_is_the_shipped_default():
    assert P.RESIDUAL_ON is False
    assert P.RESIDUAL_FN is None
    assert P.RESIDUAL_HEAD == ""
    assert not P.residual_on()


def test_off_never_calls_the_override(off, monkeypatch):
    """`residual_on` is the only gate and it is read at trace time."""
    called = []
    monkeypatch.setattr(P, "_residual_override",
                        lambda *a, **k: called.append(1) or (a[2], None, None))
    _plan(*_seeded_case(0))
    assert called == []


def test_off_short_circuits_before_the_head_is_loaded(monkeypatch):
    """A head named at OFF is not even imported -- the switch, not the path,
    is what turns the feature on."""
    monkeypatch.setattr(P, "RESIDUAL_ON", False)
    monkeypatch.setattr(P, "RESIDUAL_HEAD", "/nonexistent/head.npz")
    monkeypatch.setattr(P, "_residual_head_module",
                        lambda: pytest.fail("loaded at OFF"))
    assert P.residual_on() is False


def test_on_without_a_head_is_still_off(monkeypatch):
    """`RESIDUAL_ON` alone decides nothing: with no head there is nothing to
    apply, and the planner must not half-enable itself."""
    monkeypatch.setattr(P, "RESIDUAL_ON", True)
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    monkeypatch.setattr(P, "RESIDUAL_HEAD", "")
    assert P.residual_on() is False


def test_identity_head_is_byte_identical(monkeypatch):
    """A head that asks for nothing (`init_params`' no-op action on every
    slot) plans the shipped day to the byte -- which is what makes the first
    PPO rollout an unbiased sample of the frozen agent."""
    _on(monkeypatch, d_plant=0, d_animal=0, d_hire=0, hold_num=2)
    got = tuple(_digest(_plan(*_seeded_case(s))) for s in PIN_SEEDS[:2])
    assert got == PIN


# =========================================================================
# ON: the four clamps
# =========================================================================

def _ovr(day=5, **kw):
    macro = _macro(plant_target=np.asarray([2, 3, 0, 1, 0], np.int32),
                   animal_want=np.asarray([1, 0, 2], np.int32),
                   hold=np.full(spec.N_PRODUCTS, 10, np.int32))
    P.RESIDUAL_FN = _fn(**kw)
    return P._residual_override(np, _view(day=day), macro)


def test_plant_delta_is_clipped_to_four(monkeypatch):
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    m, _, _ = _ovr(d_plant=99)
    assert [int(x) for x in m.plant_target] == [6, 7, 4, 5, 4]


def test_plant_target_never_goes_negative(monkeypatch):
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    m, _, _ = _ovr(d_plant=-99)
    assert [int(x) for x in m.plant_target] == [0, 0, 0, 0, 0]


def test_day_zero_keeps_the_pinned_opening(monkeypatch):
    """`RESIDUAL_FIRST_DAY`: the d0 package is measured as one and the head
    does not get a vote on its mix."""
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    m, _, _ = _ovr(day=0, d_plant=4)
    assert [int(x) for x in m.plant_target] == [2, 3, 0, 1, 0]
    m, _, _ = _ovr(day=1, d_plant=4)
    assert [int(x) for x in m.plant_target] == [6, 7, 4, 5, 4]


def test_animal_delta_is_clipped_and_floored(monkeypatch):
    """GOOSE included -- it is end-to-end in the shipped planner."""
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    m, _, _ = _ovr(d_animal=9)
    assert [int(x) for x in m.animal_want] == [3, 2, 4]
    m, _, _ = _ovr(d_animal=-9)
    assert [int(x) for x in m.animal_want] == [0, 0, 0]


@pytest.mark.parametrize("num,want", [(0, 0), (1, 5), (2, 10), (7, 10)])
def test_hold_fraction_is_zero_half_or_one(monkeypatch, num, want):
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    m, _, _ = _ovr(hold_num=num)
    assert [int(x) for x in m.hold] == [want] * spec.N_PRODUCTS


def test_hire_delta_is_clipped_to_two(monkeypatch):
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    assert int(_ovr(d_hire=9)[1]) == 2
    assert int(_ovr(d_hire=-9)[1]) == -2


def test_hire_clamp_is_the_affordable_prefix():
    """`_residual_hire` is `min(h_star + d, max affordable)` -- affordability
    is the one thing no head repeals (`test_cash_reserve.py`)."""
    afford = [True] * (spec.MAX_HANDS + 1)
    assert int(P._residual_hire(np, np.int32(3), np.int32(2), afford)) == 5
    assert int(P._residual_hire(np, np.int32(3), np.int32(-2), afford)) == 1
    assert int(P._residual_hire(np, np.int32(0), np.int32(-2), afford)) == 0
    assert int(P._residual_hire(np, np.int32(spec.MAX_HANDS), np.int32(2),
                                afford)) == spec.MAX_HANDS
    poor = [True, True, True] + [False] * (spec.MAX_HANDS - 2)
    assert int(P._residual_hire(np, np.int32(2), np.int32(2), poor)) == 2


# =========================================================================
# The features the head sees
# =========================================================================

def test_features_are_the_declared_width():
    f = P._residual_features(np, _view(day=7))
    assert f.shape == (P.RESIDUAL_N_FEAT,) == (64,)
    assert f.dtype == np.float32
    assert np.all(np.isfinite(f))


def test_features_match_the_head_module():
    """One width, two consumers: a head trained against another is another
    head, and the mismatch has to be an import-time error, not a silent
    reshape in the submission."""
    mod = P._residual_head_module()
    assert mod.N_FEAT == P.RESIDUAL_N_FEAT


def test_the_head_sees_the_day_and_the_macro(monkeypatch):
    """`RESIDUAL_FN(obs_features, macro_fields)`: the fields it may rewrite,
    plus the day it is rewriting."""
    box = []
    monkeypatch.setattr(P, "RESIDUAL_FN", None)
    _ovr(day=11, box=box)
    feats, fields = box[0]
    assert feats.shape == (P.RESIDUAL_N_FEAT,)
    assert int(fields["day"]) == 11
    for k in ("plant_target", "animal_want", "hold", "press", "crew_target"):
        assert k in fields


def test_numpy_head_runs_without_jax(monkeypatch):
    """The file-agent path: `head.numpy_fn` is pure numpy, so the package --
    which `forbidden_imports` forbids from importing jax -- can fly it."""
    mod = P._residual_head_module()
    fn = mod.numpy_fn(mod.init_params(0))
    out = fn(P._residual_features(np, _view(day=4)), {})
    assert out["d_plant"].shape == (spec.N_CROPS,)
    assert out["d_animal"].shape == (spec.N_ANIMALS,)
    assert out["hold_num"].shape == (spec.N_PRODUCTS,)
    # A fresh head is the identity residual: every slot's no-op wins.
    assert not np.any(out["d_plant"]) and not np.any(out["d_animal"])
    assert int(out["d_hire"]) == 0
    assert np.all(out["hold_num"] == 2)
