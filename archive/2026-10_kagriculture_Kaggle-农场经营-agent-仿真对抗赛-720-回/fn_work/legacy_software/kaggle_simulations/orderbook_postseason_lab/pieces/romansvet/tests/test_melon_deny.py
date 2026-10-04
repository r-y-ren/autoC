"""MELON_DENY: early plate plus a deterministic melon release row."""
from __future__ import annotations

import _pin

_pin.bootstrap()

import numpy as np
import pytest
from test_budget_order import _macro
from test_route_early import PIN_SEEDS, _plan, _seeded_case, _view

from kagg3 import spec
from kagg3.core import plan as P

PRE_SWITCH = "784a5ccbd70a97401e55797ac2acb5f136480bab"


@pytest.fixture
def off(monkeypatch):
    monkeypatch.setattr(P, "MELON_DENY_ON", False)


def _own_digests():
    return {str(seed): _pin.digest(_plan(*_seeded_case(seed)))
            for seed in PIN_SEEDS[:2]}


def test_off_is_default_and_byte_identical_to_pre_switch(off):
    assert P.MELON_DENY_ON is False
    assert _own_digests() == _pin.tree_digests(__file__, ref=PRE_SWITCH)


def test_off_returns_original_hold_object(off):
    hold = np.arange(spec.N_PRODUCTS, dtype=np.int32)
    assert P._sell_hold(np, np.asarray(P.default_price_table()), hold,
                        np.bool_(False), day=10) is hold


def test_plate_rebalances_only_d0_through_d2(monkeypatch):
    monkeypatch.setattr(P, "MELON_DENY_PLATE", 8)
    target = np.zeros(spec.N_CROPS, np.int32)
    target[spec.I_CARROT] = 6
    target[spec.I_WHEAT] = 6
    macro = _macro(plant_target=target)
    for day in (0, 1, 2):
        got = P._melon_deny_plate(np, _view(day=day), macro).plant_target
        assert int(got[spec.I_MELON]) == 8
        assert int(got.sum()) == int(target.sum())
    for day in (3, 10):
        got = P._melon_deny_plate(np, _view(day=day), macro).plant_target
        assert np.array_equal(got, target)


def test_dump_sets_only_melon_hold_to_zero_after_release(monkeypatch):
    monkeypatch.setattr(P, "MELON_DENY_ON", True)
    monkeypatch.setattr(P, "MELON_DENY_DUMP_DAY", 10)
    monkeypatch.setattr(P, "MELON_DENY_HOLD", 2)
    hold = np.full(spec.N_PRODUCTS, 77, np.int32)
    pt = np.asarray(P.default_price_table())
    before = P._sell_hold(np, pt, hold, np.bool_(False), day=11)
    after = P._sell_hold(np, pt, hold, np.bool_(False), day=12)
    assert int(before[spec.I_MELON]) == spec.COIN_CAP
    assert int(after[spec.I_MELON]) == 0
    assert np.array_equal(np.delete(after, spec.I_MELON),
                          np.delete(hold, spec.I_MELON))


if __name__ == "__main__":
    for name, digest in _own_digests().items():
        print(name, digest)
