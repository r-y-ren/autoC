"""Focused unit tests for the LIVEEXPERT selection and override protocol."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "S/actionrl/live_expert.py"
SPEC = importlib.util.spec_from_file_location("live_expert", PATH)
LE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = LE
SPEC.loader.exec_module(LE)


def test_candidate_map_is_v1_and_documents_all_requested_levers():
    assert len(LE.CANDIDATES) == 8
    assert [(x.slot, x.value) for x in LE.CANDIDATES] == [
        (8, 4), (0, 8), (3, 8), (4, 8),
        (2, 8), (1, 8), (12, 0), (13, 0),
    ]
    assert all(0 <= x.slot < 18 for x in LE.CANDIDATES)
    assert "hire" in LE.CANDIDATES[0].name
    assert "wheat" in LE.CANDIDATES[1].name
    assert sum("hold" in x.name for x in LE.CANDIDATES) == 2


def test_set_override_changes_exactly_one_day_slot_and_is_copying():
    mask = np.zeros((30, 18), bool)
    values = np.zeros((30, 18), np.int32)
    got_m, got_v = LE.set_override(mask, values, 12, LE.CANDIDATES[0])
    assert not mask.any() and not values.any()
    assert np.argwhere(got_m).tolist() == [[12, 8]]
    assert int(got_v[12, 8]) == 4


def test_experiment_head_adapter_is_identity_until_programmed():
    path = ROOT / "S/actionrl/live_expert_head.py"
    spec = importlib.util.spec_from_file_location("live_expert_head_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    params = mod.HEAD.init_params(3)
    fn = mod.numpy_fn(params)
    feats = np.zeros(mod.HEAD.N_FEAT, np.float32)
    base = fn(feats, {"day": 12})
    mask = np.zeros((30, 18), bool)
    values = np.zeros((30, 18), np.int32)
    mask[12, 8] = True
    values[12, 8] = 4
    fn.set_program(mask, values)
    moved = fn(feats, {"day": 12})
    assert int(base["d_hire"]) == 0
    assert int(moved["d_hire"]) == 2
    assert not np.any(moved["d_plant"])
    trace = fn.get_trace()
    assert len(trace) == 1 and trace[0][0] == 12
    assert trace[0][1].shape == (mod.HEAD.N_FEAT,)
    assert int(trace[0][2][8]) == 2 and int(trace[0][3][8]) == 4


def test_choice_is_win_first_then_bounded_margin_with_gift_veto():
    # Row 1 has huge margin but is still a loss. Row 2 wins but gifts one coin
    # beyond the incumbent opponent purse. Row 3 is the admissible winner.
    money = np.asarray([[90, 100], [0, 1], [120, 101], [101, 100]])
    assert LE.choose_candidate(money, incumbent_theirs=100) == 3
    # Once all are losses, bounded margin decides; clipping makes the first
    # occurrence deterministic when two margins exceed the same cap.
    losses = np.asarray([[0, 30_000], [0, 25_000], [0, 50_000]])
    assert LE.choose_candidate(losses, 60_000, margin_bound=20_000) == 0


def test_training_losses_are_first_16_by_game_index():
    rows = LE.select_training_losses()
    assert len(rows) == 16
    assert [x.game_index for x in rows] == [
        14, 20, 36, 37, 40, 43, 46, 49,
        52, 54, 57, 59, 65, 68, 70, 74,
    ]
    assert rows[0].ep == "110962225"
    assert rows[-1].ep == "111015168"
    assert all(x.live_ours < x.live_theirs for x in rows)


def test_training_loss_range_selects_the_remaining_25():
    rows = LE.select_training_losses(loss_start=16, n_losses=25)
    assert len(rows) == 25
    assert rows[0].game_index > 74
    assert rows[-1].game_index < 150
    assert len({x.game_index for x in rows}) == 25
