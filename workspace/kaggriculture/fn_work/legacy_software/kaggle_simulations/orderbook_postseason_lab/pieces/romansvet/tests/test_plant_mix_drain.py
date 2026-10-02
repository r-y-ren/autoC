"""H1: tilt the plant mix towards unclaimed town appetite
(`brain.PLANT_MIX_DRAIN_ON`).

`residual_drain`'s `share` column is the fraction of the town's remaining
season appetite for a product that the supply on **both** boards has not
claimed. The `absorb` gate already reads it, but only as a hard threshold at
the clip floor; this switch adds it as a soft logit on the crop softmax, which
is H1's "plant into demand nobody is serving" without naming a crop.

The switch is OFF by default and these tests toggle it explicitly.
"""
from __future__ import annotations

import os
import pathlib
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, "src")

import numpy as np
import pytest

from kagg3 import spec
from kagg3.core import brain

FIXTURE = ROOT / "tests" / "data" / "trajectory_obs.npz"
THETA = ROOT / "artifacts" / "theta.npy"

pytestmark = pytest.mark.skipif(not FIXTURE.is_file() or not THETA.is_file(),
                                reason="needs the trajectory fixture and a trained theta")


def _obs(limit=400):
    d = np.load(FIXTURE)
    n = min(limit, len(d["day"]))
    return [brain.PolicyObs(**{f: d[f][i] for f in brain.PolicyObs._fields
                               if f in d.files}) for i in range(n)]


def _targets(theta, obs):
    return [np.asarray(brain.decide(np, theta, o).plant_target) for o in obs]


def _share(o):
    """The `share` column the switch reads, for one observation."""
    return np.asarray(brain.features(np, o)[2])[:spec.N_CROPS, 1]


def test_switch_off_is_the_champion_decode_bit_for_bit(monkeypatch):
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_ON", False)
    theta = np.load(THETA)
    obs = _obs()
    a = _targets(theta, obs)
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_GAIN", 7.5)   # must not be read
    for x, y in zip(a, _targets(theta, obs)):
        assert np.array_equal(x, y)


def test_switch_on_moves_tiles_towards_unclaimed_appetite(monkeypatch):
    """Averaged over the fixture, the tiles the day plants sit on a higher
    `share` with the switch on -- and at least one day actually moves."""
    theta = np.load(THETA)
    obs = _obs()
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_ON", False)
    off = _targets(theta, obs)
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_ON", True)
    on = _targets(theta, obs)

    moved = sum(1 for a, b in zip(off, on) if not np.array_equal(a, b))
    assert moved > 0, "the switch decodes the same mix on every fixture day"

    def weighted(ts):
        num = den = 0.0
        for t, o in zip(ts, obs):
            s = _share(o)
            num += float(np.dot(t, s))
            den += float(t.sum())
        return num / max(den, 1.0)

    assert weighted(on) > weighted(off)


def test_the_gain_is_the_only_thing_the_switch_adds(monkeypatch):
    """Gain 0 with the switch on is the switch off, so the constant is the
    whole intervention and nothing else in `decide` moved."""
    theta = np.load(THETA)
    obs = _obs(64)
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_ON", False)
    off = _targets(theta, obs)
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_ON", True)
    monkeypatch.setattr(brain, "PLANT_MIX_DRAIN_GAIN", 0.0)
    for x, y in zip(off, _targets(theta, obs)):
        assert np.array_equal(x, y)
