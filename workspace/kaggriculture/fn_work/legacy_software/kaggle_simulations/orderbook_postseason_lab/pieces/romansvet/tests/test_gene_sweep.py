"""A gene every nudge of which is worse is coupled to something the planner
hides; find those automatically instead of by hand-forcing heads."""
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

from kagg3.core import policy as PO
from kagg3.es import sweep as S


def test_shifted_moves_exactly_one_bias():
    th = np.zeros(PO.N_PARAMS, np.float32)
    out = S.shifted(th, 2, 1.5)
    assert out[PO.offset("gb2") + 2] == 1.5
    assert np.count_nonzero(out) == 1
    assert np.count_nonzero(th) == 0            # input untouched


def test_genes_past_the_head_land_in_gb5():
    th = np.zeros(PO.N_PARAMS, np.float32)
    out = S.shifted(th, PO.N_HEAD_OUT + 1, -2.0)     # land_afford
    assert out[PO.offset("gb5") + 1] == -2.0
    assert np.count_nonzero(out) == 1
    assert S.N_GENES == PO.N_HEAD_OUT + PO.N_AUX_OUT + PO.N_DEV_OUT


def test_genes_past_the_aux_block_land_in_gb6():
    # The development block is appended like every block before it, so the
    # sweep's gene numbering extends rather than shifting.
    th = np.zeros(PO.N_PARAMS, np.float32)
    out = S.shifted(th, S.N_AUX_END + 1, 2.0)        # dev_weight
    assert out[PO.offset("gb6") + 1] == 2.0
    assert np.count_nonzero(out) == 1
    with pytest.raises(IndexError):
        S.gene_offset(S.N_GENES)


def test_classify():
    base = 50_000.0
    assert S.classify(base, {-1.0: 45_000, 1.0: 44_000}, tol=500) == "trapped"
    assert S.classify(base, {-1.0: 45_000, 1.0: 56_000}, tol=500) == "uphill+"
    assert S.classify(base, {-1.0: 57_000, 1.0: 44_000}, tol=500) == "uphill-"
    assert S.classify(base, {-1.0: 50_200, 1.0: 49_900}, tol=500) == "flat"


def test_sweep_reports_one_row_per_head_index():
    from kagg3.es.train import Config, Trainer
    tr = Trainer(Config(pop=4, episodes=4, chunk=8, abs_pairs=2, n_archetypes=2), seed=0)
    rows = S.sweep(tr, np.asarray(tr.theta), [1, 2], deltas=(-1.0, 1.0))
    assert [r["gene"] for r in rows] == [1, 2]
    assert set(rows[0]) >= {"gene", "base", "scores", "verdict"}
