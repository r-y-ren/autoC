"""Machine-readable identity contract for the active Kaggriculture candidate."""

from __future__ import annotations

import base64
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


class CandidateIdentityError(ValueError):
    """The active candidate identity is missing, stale, or contradictory."""


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise CandidateIdentityError(f"cannot read identity file {path}: {exc}") from exc


def _canonical_lf_bytes(path: Path) -> bytes:
    try:
        return path.read_bytes().replace(b"\r\n", b"\n")
    except OSError as exc:
        raise CandidateIdentityError(f"cannot read identity file {path}: {exc}") from exc


def _require_working_source_match(working_path: Path, source: bytes,
                                  declared_sha: Any) -> None:
    canonical = _canonical_lf_bytes(working_path)
    if canonical != source:
        raise CandidateIdentityError(
            "working candidate bytes do not match the declared source commit")
    if hashlib.sha256(canonical).hexdigest() != declared_sha:
        raise CandidateIdentityError(
            "working canonical LF SHA does not match the declared source commit")


def _under_root(root: Path, relative: str) -> Path:
    """Resolve a manifest path that may be software-root or repo-root relative."""
    text = str(relative)
    prefix = "workspace/software/"
    if text.lower().startswith(prefix):
        return root / text[len(prefix):]
    return root / text


def _require_digest(value: Any, label: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        raise CandidateIdentityError(f"{label} must be a SHA-256 digest")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CandidateIdentityError(f"{label} must be a SHA-256 digest") from exc
    return value


def _require_git_ref(value: Any, label: str, *, root: Path,
                     require_head_ancestor: bool = False) -> str:
    if not isinstance(value, str) or len(value) != 40 or value == "0" * 40:
        raise CandidateIdentityError(f"{label} must be a non-zero 40-character git ref")
    try:
        int(value, 16)
    except ValueError as exc:
        raise CandidateIdentityError(f"{label} must be a hexadecimal git ref") from exc
    try:
        object_type = subprocess.run(
            ["git", "cat-file", "-t", value], cwd=root, text=True,
            capture_output=True, check=True, timeout=10).stdout.strip()
        if object_type != "commit":
            raise CandidateIdentityError(f"{label} must resolve to a commit")
        if require_head_ancestor:
            subprocess.run(["git", "merge-base", "--is-ancestor", value, "HEAD"],
                           cwd=root, capture_output=True, check=True, timeout=10)
    except CandidateIdentityError:
        raise
    except (OSError, subprocess.SubprocessError) as exc:
        suffix = " on the current development branch" if require_head_ancestor else ""
        raise CandidateIdentityError(f"{label} is not a verifiable git ref{suffix}") from exc
    return value


def render_readme_projection(identity: dict[str, Any]) -> str:
    """Return the exact README machine projection for this manifest."""
    working = identity["working"]
    frozen = identity["last_promoted_frozen"]
    holdout = identity["published_holdout"]
    engine = identity["engine"]
    return "\n".join([
        "<!-- ACTIVE_CANDIDATE_IDENTITY:BEGIN -->",
        f"working_candidate_sha256={working['sha256']}",
        f"working_candidate_status={working['status']}",
        f"last_promoted_frozen_sha256={frozen['sha256']}",
        f"published_holdout_candidate_sha256={holdout['candidate_sha256']}",
        f"published_holdout_attempt_index={holdout['attempt_index']}",
        f"engine={engine['package']} {engine['version']} {engine['scenario']}",
        "<!-- ACTIVE_CANDIDATE_IDENTITY:END -->",
    ])


def validate_active_candidate(payload: dict[str, Any], *,
                              software_root: str | Path,
                              readme_text: str | None = None) -> dict[str, Any]:
    """Validate the manifest and every referenced immutable identity artifact."""
    if not isinstance(payload, dict) or payload.get("schema_version") != "1.0":
        raise CandidateIdentityError("active candidate manifest schema_version must be 1.0")
    root = Path(software_root).resolve()
    for key in ("working", "last_promoted_frozen", "published_holdout", "engine", "runtime"):
        if not isinstance(payload.get(key), dict):
            raise CandidateIdentityError(f"manifest requires object {key}")

    working = payload["working"]
    if working.get("status") != "development":
        raise CandidateIdentityError("working candidate must remain development")
    working_path = root / str(working.get("path", ""))
    working_sha = _require_digest(working.get("sha256"), "working candidate SHA")
    if not working_path.is_file() or _sha256(working_path) != working_sha:
        raise CandidateIdentityError("working candidate SHA does not match main.py")
    _require_git_ref(working.get("git_ref"), "working git ref", root=root,
                     require_head_ancestor=True)
    repo_root = root.parents[1]
    source_path = f"workspace/software/{working['path']}"
    try:
        blob_oid = subprocess.run(
            ["git", "rev-parse", f"{working['git_ref']}:{source_path}"],
            cwd=repo_root, text=True, capture_output=True, check=True,
            timeout=10).stdout.strip()
    except (OSError, subprocess.SubprocessError) as exc:
        raise CandidateIdentityError("working git blob OID cannot be resolved") from exc
    if blob_oid != working.get("git_blob_oid"):
        raise CandidateIdentityError("working git blob OID does not match source commit")
    try:
        source = subprocess.run(
            ["git", "show", f"{working['git_ref']}:{source_path}"],
            cwd=repo_root, capture_output=True, check=True, timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        raise CandidateIdentityError("working source commit cannot be read") from exc
    canonical_lf_sha = hashlib.sha256(source.stdout).hexdigest()
    if canonical_lf_sha != working.get("canonical_lf_sha256"):
        raise CandidateIdentityError("working canonical LF SHA does not match source commit")
    _require_working_source_match(working_path, source.stdout,
                                  working.get("canonical_lf_sha256"))

    frozen = payload["last_promoted_frozen"]
    frozen_sha = _require_digest(frozen.get("sha256"), "frozen manifest SHA")
    frozen_path = root / str(frozen.get("manifest_path", ""))
    if not frozen_path.is_file():
        raise CandidateIdentityError("frozen manifest is missing")
    try:
        frozen_payload = json.loads(frozen_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CandidateIdentityError(f"frozen manifest cannot be read: {exc}") from exc
    recorded_frozen_sha = frozen_payload.get("candidate", {}).get("sha256")
    if recorded_frozen_sha != frozen_sha:
        raise CandidateIdentityError("frozen manifest SHA does not match candidate identity")
    frozen_git_ref = frozen_payload.get("candidate", {}).get("git_ref")
    if not frozen_git_ref or \
            str(frozen_git_ref) != str(frozen.get("git_ref", "")):
        raise CandidateIdentityError(
            "frozen git ref does not match the frozen manifest candidate")
    frozen_git_ref = _require_git_ref(frozen_git_ref, "frozen git ref", root=root)
    # Anti-circular-trust: re-derive the snapshot identity from its bytes.
    snapshot = frozen_payload.get("frozen_snapshot", {})
    snapshot_path = _under_root(root, snapshot.get("path", ""))
    if frozen.get("snapshot_path") and \
            Path(str(frozen["snapshot_path"])).is_absolute():
        snapshot_path = Path(frozen["snapshot_path"])
    if not snapshot_path.is_file():
        raise CandidateIdentityError("frozen snapshot file is missing")
    encoded = snapshot_path.read_bytes()
    if hashlib.sha256(encoded).hexdigest() != snapshot.get("file_sha256"):
        raise CandidateIdentityError("frozen snapshot file SHA mismatch")
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (ValueError, TypeError) as exc:
        raise CandidateIdentityError(
            f"frozen snapshot is not valid base64: {exc}") from exc
    if hashlib.sha256(decoded).hexdigest() != snapshot.get("decoded_sha256"):
        raise CandidateIdentityError("frozen snapshot decoded SHA mismatch")
    if snapshot.get("decoded_sha256") != frozen_sha:
        raise CandidateIdentityError("frozen snapshot SHA does not match frozen identity")
    if frozen_sha == working_sha:
        raise CandidateIdentityError("working candidate must not masquerade as frozen")

    holdout = payload["published_holdout"]
    holdout_sha = _require_digest(holdout.get("candidate_sha256"),
                                  "published holdout candidate SHA")
    if holdout_sha != frozen_sha:
        raise CandidateIdentityError("published holdout identity must match last promoted frozen")
    if holdout.get("status") != "published":
        raise CandidateIdentityError("published holdout must have status=published")
    if not isinstance(holdout.get("attempt_index"), int) or holdout["attempt_index"] < 1:
        raise CandidateIdentityError("published holdout attempt_index is required")
    export_path = root / str(holdout.get("eval_results_path", ""))
    seed_path = root / str(holdout.get("seed_manifest_path", ""))
    if not export_path.is_file() or not seed_path.is_file():
        raise CandidateIdentityError("published holdout artifacts are missing")
    try:
        export = json.loads(export_path.read_text(encoding="utf-8"))
        seed_manifest = json.loads(seed_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CandidateIdentityError(f"published holdout artifact cannot be read: {exc}") from exc
    if export.get("identity", {}).get("submission_sha256") != holdout_sha:
        raise CandidateIdentityError("published holdout export candidate SHA disagrees with frozen identity")
    if str(export.get("identity", {}).get("git_ref", "")) != str(frozen_git_ref):
        raise CandidateIdentityError(
            "published holdout git ref disagrees with the frozen manifest")
    if export.get("seed_domain") != "holdout" or seed_manifest.get("schema_version") != "1.0":
        raise CandidateIdentityError("published holdout artifacts have incompatible identity")
    if seed_manifest.get("attempt_index") != holdout.get("attempt_index") or \
            export.get("holdout", {}).get("attempt", {}).get("index") != \
            holdout.get("attempt_index") or \
            export.get("holdout", {}).get("seed_manifest", {}).get("attempt_index") != \
            holdout.get("attempt_index"):
        raise CandidateIdentityError(
            "published holdout attempt index disagrees with authoritative artifacts")
    export_seed = export.get("holdout", {}).get("seed_manifest", {})
    if export_seed != seed_manifest or \
            export.get("evaluation_input", {}).get("seeds") != seed_manifest.get("seeds"):
        raise CandidateIdentityError(
            "published holdout export seed manifest projection is stale")
    if holdout.get("seed_manifest_sha256") != _sha256(seed_path):
        raise CandidateIdentityError("published holdout seed manifest SHA mismatch")
    if holdout.get("eval_results_sha256") != _sha256(export_path):
        raise CandidateIdentityError("published holdout export SHA mismatch")

    engine = payload["engine"]
    if engine.get("package") != "kaggle-environments" or engine.get("version") != "1.32.7":
        raise CandidateIdentityError("engine identity must be kaggle-environments 1.32.7")
    if engine.get("scenario") != "kaggriculture":
        raise CandidateIdentityError("engine scenario must be kaggriculture")
    wheel_path = root / str(engine.get("vendored_wheel_path", ""))
    if engine.get("vendored_wheel_sha256") != _sha256(wheel_path):
        raise CandidateIdentityError("engine wheel SHA mismatch")
    if payload.get("online_submission_refs") != []:
        refs = payload.get("online_submission_refs")
        if not isinstance(refs, list):
            raise CandidateIdentityError("online_submission_refs must be a list")

    runtime = payload["runtime"]
    measured_runtime = runtime_identity()
    if runtime != measured_runtime:
        raise CandidateIdentityError(
            f"runtime identity mismatch: manifest={runtime}, measured={measured_runtime}")

    if readme_text is not None:
        projection = render_readme_projection(payload)
        if projection not in readme_text:
            raise CandidateIdentityError("README machine projection is stale")
        authority = re.findall(r"attempt-(\d+)[^\n]*当前权威代", readme_text)
        expected_attempt = str(holdout["attempt_index"])
        if authority != [expected_attempt]:
            raise CandidateIdentityError(
                "README authoritative holdout narrative is stale")
    return payload


def load_active_candidate(manifest_path: str | Path, *,
                          software_root: str | Path) -> dict[str, Any]:
    path = Path(manifest_path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise CandidateIdentityError(f"active candidate manifest cannot be read: {exc}") from exc
    return validate_active_candidate(payload, software_root=software_root)


def runtime_identity() -> dict[str, str]:
    """Return measured interpreter identity at the contracted granularity.

    The repo contract locks implementation + major.minor only; no patch-level
    pin exists (no lockfile evidence), so the patch version is deliberately
    not part of the identity.
    """
    major, minor = sys.version_info.major, sys.version_info.minor
    return {"implementation": platform.python_implementation(),
            "python_version": f"{major}.{minor}"}
