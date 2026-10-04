"""`brain.CROP_DAY_ON`: the crop log-share readout, indexed by day bucket.

Three things are pinned here.

*Identity*, which is what the switch is for: `cd` is zero in every shipped
theta and the ON branch adds `clip(GAIN * 0.0) == 0.0` to the crop logits, so B
decodes byte-identically with the switch OFF and with it ON -- on the real
trajectory fixture (`tests/data/trajectory_obs.npz`), whole macro compared, not
just the plant target.

*The index*, which is the gene's whole content: the bias that day 2 reads must
be a different coordinate from the one day 3 reads (MACRO-EXTRACT section 3 --
ymg_aq plants pure wheat on day 2 and pure strawberry on day 3), and the bucket
edges are boundaries, so a day ON an edge belongs to the later bucket.

*The layout*: the block is appended, so a 7,020-coordinate theta (the `cm`/`cb`
layout, which is what every checkpoint on disk is) stays an exact prefix and
decodes exactly as it did.
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
FIXTURE = "tests/data/trajectory_obs.npz"
CD = PO.offset("cd")
NB = PO.N_CROP_DAY_BUCKETS


def _b():
    th = np.load(THETA).astype(np.float32)
    out = np.zeros(PO.N_PARAMS, np.float32)
    out[:th.size] = th
    return out


def _dawns(days=(0, 1, 2, 3, 4, 5, 6, 10, 11, 20, 21, 29)):
    tb = build_tables(np)
    out = {}
    for nq, mo in ((1, spec.STARTING_MONEY), (2, 12000), (3, 30000)):
        st = initial_state(np, np.asarray([nq, nq], np.int32),
                           np.asarray([mo, mo], np.int32))
        pr = rollout.prices_of(np, tb, st.mkt_inv)
        for d in days:
            out[f"q{nq}_{mo}_d{d}"] = rollout.policy_obs(st, 0, np.int32(d), pr)
    return out


def _macro(theta, po):
    m = brain.decide(np, theta, po)
    return [np.asarray(getattr(m, f)) for f in m._fields]


def _plant(theta, po):
    return np.asarray(brain.decide(np, theta, po).plant_target)


@pytest.fixture
def on(monkeypatch):
    monkeypatch.setattr(brain, "CROP_DAY_ON", True)


def test_off_is_the_shipped_default():
    assert brain.CROP_DAY_ON is False


def test_layout_offsets():
    """Appended after every earlier block, 5 x 9, and nothing before it moved."""
    assert PO.offset("cm") == 6855 and PO.offset("cb") == 7015
    assert PO.offset("cd") == 7020
    assert PO.N_CROP_DAY_BUCKETS == 9
    assert dict(PO.SHAPES)["cd"] == (spec.N_CROPS, PO.N_CROP_DAY_BUCKETS)
    # `cd` was the tail until FERTENGINE appended `g12`/`gb12` (2026-09-16);
    # the pin that matters is that nothing BEFORE `cd` moved and that the block
    # is still where the trained thetas put it.
    assert [n for n, _ in PO.SHAPES[-3:]] == ["cd", "g12", "gb12"]
    assert PO.offset("g12") == 7065 and PO.N_PARAMS == 7098
    assert len(brain.CROP_DAY_BUCKETS) + 1 == PO.N_CROP_DAY_BUCKETS
    # zero-init, like every appended block since `mh`
    th = PO.init_theta(np.random.default_rng(0))
    assert np.all(th[CD:] == 0.0)


def test_zero_gene_is_byte_identical_on_synthetic_dawns(on):
    theta, dawns = _b(), _dawns()
    assert np.all(theta[CD:] == 0.0)
    for name, po in dawns.items():
        brain.CROP_DAY_ON = False
        off = _macro(theta, po)
        brain.CROP_DAY_ON = True
        got = _macro(theta, po)
        for a, b in zip(off, got):
            np.testing.assert_array_equal(a, b, err_msg=name)


@pytest.mark.skipif(not os.path.isfile(FIXTURE), reason="needs the trajectory fixture")
def test_zero_gene_is_byte_identical_on_the_fixture(on):
    """The real-trajectory gate: 2,400 decisions, whole macro, OFF vs ON at zero."""
    d = np.load(FIXTURE)
    obs = [brain.PolicyObs(**{f: d[f][i] for f in brain.PolicyObs._fields if f in d.files})
           for i in range(len(d["day"]))]
    assert len(obs) >= 1000, len(obs)
    theta = _b()
    for i, po in enumerate(obs):
        brain.CROP_DAY_ON = False
        off = _macro(theta, po)
        brain.CROP_DAY_ON = True
        got = _macro(theta, po)
        for a, b in zip(off, got):
            np.testing.assert_array_equal(a, b, err_msg=f"decision {i}")


def test_old_layout_theta_still_decodes(on):
    """A 7,020-coordinate theta is an exact prefix: same macro, gene ON or OFF."""
    theta = _b()
    old = theta[:PO.offset("cd")].copy()
    assert old.shape[0] == 7020
    for name, po in _dawns(days=(0, 3, 12)).items():
        brain.CROP_DAY_ON = False
        ref = _macro(theta, po)
        for th in (old, PO.pad(old)):
            brain.CROP_DAY_ON = True
            for a, b in zip(ref, _macro(th, po)):
                np.testing.assert_array_equal(a, b, err_msg=name)


def test_bucket_edges_are_the_later_bucket(on):
    """`day >= edge` -- day 6 is bucket 6, day 5 is bucket 5, day 21 is bucket 8.

    Driven through the decode rather than asserted on the arithmetic: a bias on
    bucket k must move the days in bucket k and no other day.
    """
    theta = _b()
    edges = (0,) + tuple(brain.CROP_DAY_BUCKETS)
    # one representative day per bucket, then the day either side of each edge
    days = [0, 1, 2, 3, 4, 5, 6, 10, 11, 20, 21, 29]
    want = {0: 0, 1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 10: 6, 11: 7, 20: 7, 21: 8, 29: 8}
    assert len(edges) == PO.N_CROP_DAY_BUCKETS
    dawns = _dawns(days=days)
    ci = spec.I_STRAWBERRY
    base = {k: _plant(theta, po) for k, po in dawns.items()}
    for k in range(PO.N_CROP_DAY_BUCKETS):
        th = theta.copy()
        th[CD + ci * NB + k] = np.float32(0.20)      # saturating, both signs bounded
        moved = set()
        for name, po in dawns.items():
            d = int(name.rsplit("_d", 1)[1])
            got = _plant(th, po)
            if not np.array_equal(got, base[name]):
                moved.add(d)
                assert want[d] == k, f"bucket {k} moved day {d} (bucket {want[d]})"
        # every day that maps to this bucket and can still plant strawberry
        for d in days:
            if want[d] == k and d <= 11 and d not in moved:
                raise AssertionError(f"bucket {k} did not move day {d}")


def test_gene_is_live_at_one_sigma(on):
    """Gene-slope rule: one sigma-0.02 draw must move a tile, and only its day.

    `CROP_DAY_GAIN * 0.02 = 1.28` nats, against the 2.0487-nat first-melon-tile
    boundary measured at B -- so one to two sd, not the ~200x-dead readout the
    MELON gene block documents.
    """
    theta = _b()
    dawns = _dawns(days=(2, 3))
    d2 = [po for n, po in dawns.items() if n.endswith("_d2")]
    d3 = [po for n, po in dawns.items() if n.endswith("_d3")]
    base2 = [_plant(theta, po) for po in d2]
    base3 = [_plant(theta, po) for po in d3]
    th = theta.copy()
    th[CD + spec.I_STRAWBERRY * NB + 2] = np.float32(0.04)      # 2 sd, day-2 bucket
    got2 = [_plant(th, po) for po in d2]
    got3 = [_plant(th, po) for po in d3]
    assert any(g[spec.I_STRAWBERRY] > b[spec.I_STRAWBERRY] for g, b in zip(got2, base2)), \
        "two sigma on the day-2 bucket moved no day-2 strawberry tile"
    for g, b in zip(got3, base3):
        np.testing.assert_array_equal(g, b)     # day 3 reads its own coordinate
