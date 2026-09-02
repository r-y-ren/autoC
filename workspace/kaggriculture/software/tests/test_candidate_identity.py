"""Active-candidate identity contract regressions."""

from __future__ import annotations

import base64
import copy
import hashlib
import json
import shutil
from pathlib import Path

import pytest

from kgenv.candidate_identity import (
    CandidateIdentityError,
    _require_working_source_match,
    load_active_candidate,
    render_readme_projection,
    validate_active_candidate,
)


SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = SOFTWARE_ROOT / "active_candidate.json"


def test_working_source_commit_and_blob_identity_are_verified():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert payload["working"]["git_ref"] == \
        "8846a6c08b2b1a1f9c794d5c6584f2aaa6183787"
    assert len(payload["working"]["git_blob_oid"]) == 40
    assert len(payload["working"]["canonical_lf_sha256"]) == 64

    corrupted = copy.deepcopy(payload)
    corrupted["working"]["git_blob_oid"] = "0" * 40
    with pytest.raises(CandidateIdentityError, match="blob OID"):
        validate_active_candidate(corrupted, software_root=SOFTWARE_ROOT)

    corrupted = copy.deepcopy(payload)
    corrupted["working"]["canonical_lf_sha256"] = "0" * 64
    with pytest.raises(CandidateIdentityError, match="canonical LF SHA"):
        validate_active_candidate(corrupted, software_root=SOFTWARE_ROOT)


def test_working_bytes_must_match_declared_source_commit(tmp_path):
    source = b"print('source')\n"
    candidate = tmp_path / "main.py"
    candidate.write_bytes(source + b"\n")
    canonical_sha = hashlib.sha256(source).hexdigest()

    with pytest.raises(CandidateIdentityError, match="declared source commit"):
        _require_working_source_match(candidate, source, canonical_sha)


def test_validator_rejects_working_source_byte_divergence(monkeypatch):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    monkeypatch.setattr(
        "kgenv.candidate_identity._canonical_lf_bytes",
        lambda path: b"divergent working bytes\n")

    with pytest.raises(CandidateIdentityError, match="declared source commit"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_repository_manifest_distinguishes_working_frozen_and_published_identity():
    identity = load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT)

    assert identity["working"]["status"] == "development"
    assert identity["working"]["sha256"] != identity["last_promoted_frozen"]["sha256"]
    assert identity["published_holdout"]["candidate_sha256"] == \
        identity["last_promoted_frozen"]["sha256"]
    assert identity["published_holdout"]["attempt_index"] == 5
    assert identity["online_submission_refs"] == []


def test_validator_rejects_working_main_sha_drift(tmp_path):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    candidate = tmp_path / "main.py"
    candidate.write_text("def agent(obs): return {}\n", encoding="utf-8")
    payload["working"]["path"] = candidate.name

    with pytest.raises(CandidateIdentityError, match="working candidate SHA"):
        validate_active_candidate(payload, software_root=tmp_path)


@pytest.mark.parametrize(
    "mutate,match",
    [
        (lambda value: value["working"].update(status="frozen"),
         "working candidate.*development"),
        (lambda value: value["published_holdout"].update(
            candidate_sha256=value["working"]["sha256"]),
         "published holdout.*frozen"),
        (lambda value: value["last_promoted_frozen"].update(
            sha256="0" * 64),
         "frozen manifest.*SHA"),
    ],
)
def test_validator_rejects_contradictory_candidate_roles(mutate, match):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    mutate(payload)
    with pytest.raises(CandidateIdentityError, match=match):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_validator_rejects_stale_readme_machine_projection():
    payload = load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT)
    stale = render_readme_projection(payload).replace(
        payload["working"]["sha256"], "f" * 64)

    with pytest.raises(CandidateIdentityError, match="README.*projection"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT,
                                  readme_text=stale)


def test_runtime_identity_is_pinned_and_machine_verified():
    payload = load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT)
    assert payload["engine"]["package"] == "kaggle-environments"
    assert payload["engine"]["version"] == "1.32.7"
    assert payload["engine"]["scenario"] == "kaggriculture"
    assert len(payload["engine"]["vendored_wheel_sha256"]) == 64
    assert payload["runtime"]["implementation"] == "CPython"

    corrupted = copy.deepcopy(payload)
    corrupted["engine"]["vendored_wheel_sha256"] = "0" * 64
    with pytest.raises(CandidateIdentityError, match="engine wheel SHA"):
        validate_active_candidate(corrupted, software_root=SOFTWARE_ROOT)

    wrong_runtime = copy.deepcopy(payload)
    wrong_runtime["runtime"]["python_version"] = "0.0.0"
    with pytest.raises(CandidateIdentityError, match="runtime identity"):
        validate_active_candidate(wrong_runtime, software_root=SOFTWARE_ROOT)

    # No patch-level lock evidence exists: pinning 3.14.7 must fail on a
    # 3.14.x interpreter because the contract locks major.minor only.
    patched = copy.deepcopy(payload)
    patched["runtime"]["python_version"] = "3.14.7"
    with pytest.raises(CandidateIdentityError, match="runtime identity"):
        validate_active_candidate(patched, software_root=SOFTWARE_ROOT)

    assert load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT) \
        ["runtime"]["python_version"] == "3.14"


# --------------------------------------------------------------------------
# anti-circular-trust: snapshot bytes, git refs and attempt index must be
# re-derived from the artifacts, never taken on faith from the manifest.
# --------------------------------------------------------------------------
def _payload_with_tmp_frozen(tmp_path, *, tamper_snapshot=None,
                             tamper_manifest_field=None,
                             drop_snapshot=False, wrong_git_ref=False):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for name in ("v72_frozen_manifest.json", "v72_frozen_candidate.b64"):
        shutil.copy2(SOFTWARE_ROOT / name, tmp_path / name)
    payload["last_promoted_frozen"]["manifest_path"] = \
        str(tmp_path / "v72_frozen_manifest.json")
    if drop_snapshot:
        (tmp_path / "v72_frozen_candidate.b64").unlink()
    payload["last_promoted_frozen"]["snapshot_path"] = \
        str(tmp_path / "v72_frozen_candidate.b64")
    if tamper_snapshot is not None:
        raw = bytearray((tmp_path / "v72_frozen_candidate.b64").read_bytes())
        raw[tamper_snapshot] = \
            ord("A") if raw[tamper_snapshot] != ord("A") else ord("B")
        (tmp_path / "v72_frozen_candidate.b64").write_bytes(bytes(raw))
    if tamper_manifest_field is not None:
        frozen_manifest = json.loads(
            (tmp_path / "v72_frozen_manifest.json").read_text(encoding="utf-8"))
        tamper_manifest_field(frozen_manifest)
        (tmp_path / "v72_frozen_manifest.json").write_text(
            json.dumps(frozen_manifest, indent=1), encoding="utf-8")
    if wrong_git_ref:
        payload["last_promoted_frozen"]["git_ref"] = "0" * 40
    return payload


def test_tampered_snapshot_bytes_fail_validation(tmp_path):
    payload = _payload_with_tmp_frozen(tmp_path, tamper_snapshot=200)
    with pytest.raises(CandidateIdentityError, match="frozen snapshot"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_manifest_snapshot_file_hash_is_recomputed_not_trusted(tmp_path):
    payload = _payload_with_tmp_frozen(
        tmp_path,
        tamper_manifest_field=lambda m: m["frozen_snapshot"].update(
            file_sha256="0" * 64))
    with pytest.raises(CandidateIdentityError, match="snapshot file SHA"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_snapshot_decode_is_verified_against_frozen_sha(tmp_path):
    payload = _payload_with_tmp_frozen(
        tmp_path,
        tamper_manifest_field=lambda m: m["frozen_snapshot"].update(
            decoded_sha256="0" * 64))
    with pytest.raises(CandidateIdentityError, match="decoded SHA"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_missing_snapshot_file_fails_closed(tmp_path):
    payload = _payload_with_tmp_frozen(tmp_path, drop_snapshot=True)
    with pytest.raises(CandidateIdentityError, match="snapshot file"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_frozen_git_ref_must_match_frozen_manifest(tmp_path):
    payload = _payload_with_tmp_frozen(tmp_path, wrong_git_ref=True)
    with pytest.raises(CandidateIdentityError, match="frozen git ref"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_published_git_ref_must_agree_with_frozen_manifest(tmp_path):
    payload = _payload_with_tmp_frozen(
        tmp_path, wrong_git_ref=True,
        tamper_manifest_field=lambda m: m["candidate"].update(
            git_ref="0" * 40))
    with pytest.raises(CandidateIdentityError,
                       match="frozen git ref|published holdout git ref"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_published_attempt_index_must_match_seed_manifest():
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["published_holdout"]["attempt_index"] = 3
    with pytest.raises(CandidateIdentityError, match="attempt index"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_validator_rejects_unverifiable_or_zero_git_refs(tmp_path):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["working"]["git_ref"] = "0" * 40
    with pytest.raises(CandidateIdentityError, match="git ref|working candidate SHA"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)

    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["last_promoted_frozen"]["git_ref"] = "0" * 40
    with pytest.raises(CandidateIdentityError, match="frozen git ref"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_validator_rejects_published_attempt_not_matching_authoritative_export(tmp_path):
    payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
    payload["published_holdout"]["attempt_index"] = 999
    with pytest.raises(CandidateIdentityError, match="attempt index"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT)


def test_validator_rejects_authoritative_readme_narrative_tamper():
    payload = load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT)
    readme = (SOFTWARE_ROOT / "README.md").read_text(encoding="utf-8")
    tampered = readme.replace("attempt-5（v7.2 候选", "attempt-3（v7.2 候选")
    assert tampered != readme
    with pytest.raises(CandidateIdentityError, match="README"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT,
                                  readme_text=tampered)


def test_repo_root_identity_command_runs_and_checks_readme():
    import subprocess
    import sys

    repo_root = SOFTWARE_ROOT
    while repo_root != repo_root.parent and not (repo_root / ".git").exists():
        repo_root = repo_root.parent
    proc = subprocess.run(
        [sys.executable, str(repo_root / "workspace" / "kaggriculture" / "software" / "scripts" / "check_candidate_identity.py")],
        cwd=repo_root, capture_output=True, text=True, timeout=60)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "readme" in proc.stdout.lower()


def test_tampered_readme_narrative_fails_validation():
    payload = load_active_candidate(MANIFEST, software_root=SOFTWARE_ROOT)
    readme = (SOFTWARE_ROOT / "README.md").read_text(encoding="utf-8")
    tampered = readme.replace("published_holdout_attempt_index=5",
                              "published_holdout_attempt_index=3")
    assert tampered != readme
    with pytest.raises(CandidateIdentityError, match="README"):
        validate_active_candidate(payload, software_root=SOFTWARE_ROOT,
                                  readme_text=tampered)


def test_readme_does_not_conflict_on_published_attempt():
    readme = (SOFTWARE_ROOT / "README.md").read_text(encoding="utf-8")
    # The authoritative published/ directory is attempt-5; describing it as
    # attempt-3 contradicts the seed manifest and the active manifest.
    assert "attempt-3 权威代" not in readme
    assert "attempt-5" in readme
