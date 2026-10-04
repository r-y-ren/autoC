import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "S/actionrl"))

import head as HEAD
import live_gate_labels as LABELS
import live_gate_policy as POLICY


def _gate(a=1.01, b=0.0):
    n, p = 6, HEAD.N_FEAT + 2
    return {
        "slots": np.asarray([0, 1, 2, 3, 4, 8]),
        "values": np.asarray([8, 8, 8, 8, 8, 4]),
        "mean": np.zeros((n, p), np.float32),
        "scale": np.ones((n, p), np.float32),
        "w_flip": np.zeros((n, p + 1), np.float32),
        "w_break": np.zeros((n, p + 1), np.float32),
        "threshold_flip": np.full(n, a, np.float32),
        "threshold_break": np.full(n, b, np.float32),
    }


def test_label_schema_contains_required_outcomes():
    path = ROOT / "S/actionrl/live_gate_labels.jsonl"
    row = json.loads(path.open().readline())
    required = {"ep", "day", "slot", "win_before", "win_after",
                "margin_before", "margin_after", "ours_before", "ours_after",
                "theirs_before", "theirs_after", "feature_index", "features"}
    assert required <= row.keys()
    assert len(row["features"]) == HEAD.N_FEAT + 2


def test_gate_feature_vector_has_no_board_identifier():
    out = LABELS.gate_features(np.arange(HEAD.N_FEAT, dtype=np.float32))
    assert out.shape == (66,)
    np.testing.assert_array_equal(out[-2:], out[:2])


def test_abstain_is_byte_identical_to_head_actions():
    base = np.arange(HEAD.V1.N_SLOT, dtype=np.int32)
    acts, decision = POLICY.gated_actions(
        base, np.zeros(HEAD.N_FEAT, np.float32), 10, _gate())
    assert decision is None
    assert acts.tobytes() == base.tobytes()


def test_outside_target_dawns_always_abstains():
    base = np.zeros(HEAD.V1.N_SLOT, np.int32)
    acts, decision = POLICY.gated_actions(
        base, np.zeros(HEAD.N_FEAT, np.float32), 9, _gate(a=0.0, b=1.0))
    assert decision is None
    np.testing.assert_array_equal(acts, base)


def test_gate_changes_at_most_one_slot_per_dawn():
    base = np.zeros(HEAD.V1.N_SLOT, np.int32)
    acts, decision = POLICY.gated_actions(
        base, np.zeros(HEAD.N_FEAT, np.float32), 11, _gate(a=0.0, b=1.0))
    assert decision is not None
    assert np.count_nonzero(acts != base) <= 1
