"""`brain.MELON_GENE_ON`: give the zero-init crop log-share readout a slope.

The identity half is the point of the switch: `cm`/`cb` are zero in every
shipped theta, `0.0 * CROP_MIX_GAIN` is `0.0`, and the ON branch differs from
the OFF branch only by that multiply -- so B decodes byte-identically with the
switch OFF *and* with it ON, and the whole macro is compared, not just the
plant target.

The live half is the measurement the 2026-09-09 gene-slope check asks for:
at the training sigma a +-1-sigma value on `cb[I_MELON]` must move the day-0
melon tile count.  OFF it cannot (the measured first-tile boundary at B is
+2.0487 nats of log-share and one sigma of the ungained readout is 0.01).
"""
from __future__ import annotations

import os
import sys

import _pin

# `kagg3` FIRST, out of the tree this process is meant to measure: the
# shared fixtures below do their own `sys.path.insert(0, "src")` and import
# `kagg3` on the way in, so a module that imported one of them first loaded
# THIS tree into a `--digests` subprocess and pinned the tree against itself
# (`tests/_pin.py`).
_pin.bootstrap()

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain
from kagg3.core import policy as PO
from kagg3.sim import rollout
from kagg3.sim.state import build_tables, initial_state

THETA = "artifacts/kagg2_games/thetas/flow193_g100_hr.npy"
CB = PO.offset("cb")
IM = spec.I_MELON


def _b():
    th = np.load(THETA).astype(np.float32)
    out = np.zeros(PO.N_PARAMS, np.float32)
    out[:th.size] = th
    return out


def _dawns():
    """Five pinned day-0 dawns: the engine cold start and four warm starts."""
    tb = build_tables(np)
    out = {}
    for name, nq, mo in (("cold", 1, spec.STARTING_MONEY),
                         ("q2", 2, spec.STARTING_MONEY),
                         ("q1_8k", 1, 8000),
                         ("q2_12k", 2, 12000),
                         ("q3", 3, spec.STARTING_MONEY)):
        st = initial_state(np, np.asarray([nq, nq], np.int32),
                           np.asarray([mo, mo], np.int32))
        out[name] = rollout.policy_obs(
            st, 0, np.int32(0), rollout.prices_of(np, tb, st.mkt_inv))
    return out


def _macro(theta, po):
    m = brain.decide(np, theta, po)
    return [np.asarray(getattr(m, f)) for f in m._fields]


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(brain, "MELON_GENE_ON", True)


def test_off_is_the_shipped_default():
    assert brain.MELON_GENE_ON is False


def test_zero_gene_is_byte_identical(on):
    """B (cm/cb zero) decodes the identical macro with the switch ON."""
    theta, dawns = _b(), _dawns()
    assert np.all(theta[PO.offset("cm"):] == 0.0)
    for name, po in dawns.items():
        brain.MELON_GENE_ON = False
        off = _macro(theta, po)
        brain.MELON_GENE_ON = True
        got = _macro(theta, po)
        for a, b in zip(off, got):
            np.testing.assert_array_equal(a, b, err_msg=name)


def test_off_ignores_a_one_sigma_gene():
    """OFF, one sigma on `cb[melon]` cannot move a single tile."""
    theta, dawns = _b(), _dawns()
    for sigma in (0.01, 0.02):
        for po in dawns.values():
            base = int(np.asarray(brain.decide(np, theta, po).plant_target)[IM])
            th = theta.copy()
            th[CB + IM] = sigma
            assert int(np.asarray(brain.decide(np, th, po).plant_target)[IM]) == base


def test_on_one_sigma_moves_the_melon_count(on):
    """ON, +1 sigma at 0.01 and 0.02 adds melon tiles on most boards."""
    theta, dawns = _b(), _dawns()
    for sigma in (0.01, 0.02):
        moved = 0
        for po in dawns.values():
            base = int(np.asarray(brain.decide(np, theta, po).plant_target)[IM])
            th = theta.copy()
            th[CB + IM] = sigma
            got = int(np.asarray(brain.decide(np, th, po).plant_target)[IM])
            moved += got >= base + 1
        assert moved >= 4, (sigma, moved)


def test_on_is_monotone_and_signed(on):
    """The gene is a slope, not a coin flip: more gene, no fewer melon."""
    theta, dawns = _b(), _dawns()
    for po in dawns.values():
        prev = -1
        for z in (-0.02, -0.01, 0.0, 0.01, 0.02, 0.04):
            th = theta.copy()
            th[CB + IM] = z
            got = int(np.asarray(brain.decide(np, th, po).plant_target)[IM])
            assert got >= prev
            prev = got
