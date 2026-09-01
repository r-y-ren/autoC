"""Deterministic campaign artifact index regressions."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
SCRIPT = REPO_ROOT / "scripts" / "verify" / "build_artifact_indexes.py"
spec = importlib.util.spec_from_file_location("artifact_indexes", SCRIPT)
artifact_indexes = importlib.util.module_from_spec(spec)
spec.loader.exec_module(artifact_indexes)


def _entries(collection):
    return {entry["path"]: entry for entry in
            artifact_indexes.build_indexes(REPO_ROOT)[collection]["entries"]}


def test_repository_indexes_are_deterministic_and_current():
    counts = artifact_indexes.validate_indexes(REPO_ROOT)
    assert counts == {"ablations": 47, "external": 2,
                      "online": 22, "acceptance": 31}


def test_mf_and_mg_decisions_override_mechanical_gate_wording():
    entries = _entries("ablations")
    mf = entries["workspace/software/exports/ablations/mf_vs_v102_dev.json"]
    mg = entries["workspace/software/exports/ablations/mg_vs_v102_dev.json"]

    assert mf["decision"] == "rejected_noop"
    assert mf["candidate_sha256"].startswith("cda12555")
    assert mf["historical_only"] is True
    assert mg["decision"] == "accepted_development"
    assert mg["candidate_sha256"].startswith("1bde14b0")
    assert mg["baseline_sha256"].startswith("360714f1")
    assert mg["historical_only"] is False


def test_v48_is_indexed_as_historical_v102_only():
    entries = _entries("external")
    smoke = entries[
        "workspace/software/exports/external/v48-seed101-smoke.json"]
    ratings = entries[
        "workspace/software/exports/external/v48-seed101-ratings.json"]

    assert smoke["decision"] == "historical_v10.2_only"
    assert smoke["candidate_sha256"].startswith("360714f1")
    assert ratings["decision"] == "historical_v10.2_only"
    assert ratings["historical_only"] is True


def test_acceptance_index_preserves_scope_and_untracked_status():
    entries = _entries("acceptance")
    run_29 = entries["workspace/acceptance/run-29.json"]
    run_30 = entries["workspace/acceptance/run-30.json"]
    run_31 = entries["workspace/acceptance/run-31.json"]

    assert run_29["decision"] == "acceptance_fail"
    assert run_29["repository_tracked"] is False
    assert run_30["decision"] == "acceptance_scoped_pass"
    assert run_30["supersedes"] == ["run-26", "run-27", "run-28"]
    assert "P1 external" in run_30["evidence_scope"]
    assert run_31["decision"] == "acceptance_scoped_pass"
    assert "P2 DNA" in run_31["evidence_scope"]
    assert run_31["evidence_scope"] != "legacy_full_run"
    assert run_31["historical_only"] is False


def test_dirty_tracked_artifact_fails_closed(monkeypatch, tmp_path):
    def fake_git(root, *args):
        if args[:3] == ("ls-files", "--error-unmatch", "--"):
            return "artifact.json"
        if args[:3] == ("diff", "--quiet", "HEAD"):
            return None
        raise AssertionError(args)

    monkeypatch.setattr(artifact_indexes, "_git", fake_git)
    with pytest.raises(ValueError, match="tracked artifact is dirty"):
        artifact_indexes._git_metadata(tmp_path, "artifact.json")


def test_every_entry_has_common_contract_fields():
    required = {
        "path", "sha256", "artifact_id", "milestone",
        "candidate_sha256", "baseline_sha256", "source_commit",
        "git_blob_oid", "decision", "evidence_scope", "produced_at",
        "supersedes", "immutable", "historical_only", "repository_tracked",
    }
    for payload in artifact_indexes.build_indexes(REPO_ROOT).values():
        assert payload["schema_version"] == "artifact-index/1.0"
        for entry in payload["entries"]:
            assert set(entry) == required
            assert len(entry["sha256"]) == 64
            json.dumps(entry)
