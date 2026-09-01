"""Fail-closed integrity checks for offline DNA forensics artifacts."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
from pathlib import Path
from typing import Any, Mapping

from .dna_forensics import (
    ForensicsError,
    GROUPING_POLICY,
    derive_forensics,
    load_authoritative_sources,
    validate_field_validation,
)
from .eval_contract import canonical_sha256


class IntegrityError(ValueError):
    """The DNA artifact, source closure, or output boundary is invalid."""


FORBIDDEN_FIELDS = frozenset({
    "steps", "step", "action", "actions", "observation", "observations", "private",
    "market", "prices", "price", "quantity", "quantities", "qty", "requested",
    "filled", "item", "inventory", "raw_trace", "raw_traces", "trace", "traces",
    "turns", "state", "states", "raw_state", "raw_states", "action_log", "raw_action_log",
    "raw_replay", "episode_trace", "raw_episode_trace", "market_state", "observation_state",
})
DATASET_URL = "https://www.kaggle.com/datasets/destbreso/kaggriculture-replay-genomes"
SOURCE_NAMES = ("barcodes.csv", "consensus.csv", "reference_barcodes.csv", "field_validation.json")
SCHEMA_VERSION = "replay-dna/1.1"
IMPLEMENTATION_FILES = (
    "kgenv/dna_forensics.py",
    "kgenv/dna_integrity.py",
    "scripts/analyze_dna_forensics.py",
    "exports/replay_dna/dna_schema.json",
)

DIGEST_ALGORITHM = "canonical-json-sha256"
IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE_SCOPE = {
    "kind": "offline_dna_liveness_forensics",
    "offline_exploratory": True,
    "strength_claim": False,
    "promotion_eligible": False,
    "holdout_evidence": False,
    "online_evidence": False,
    "engine_activity_evidence": False,
    "extractor_status": "source_extractor_not_published",
    "identity_interpretation": (
        "IDENTICAL / SAME SOURCE means 30-band anchor equality only; "
        "it does not prove same agent or real source"),
    "grouping_policy": GROUPING_POLICY,
}


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise IntegrityError(f"cannot read source file {path}: {exc}") from exc


def _repo_root(software_root: Path) -> Path:
    root = Path(software_root).resolve()
    if root.name == "software" and root.parent.name == "workspace":
        return root.parent.parent
    if (root / "workspace" / "software").is_dir():
        return root
    raise IntegrityError("cannot locate repository root from software root")


def validate_input_path(path: str | os.PathLike[str], expected_name: str,
                        repo_root: str | os.PathLike[str] | None = None) -> Path:
    """Allow only the named local file directly under the repository .tmp-dna directory."""
    raw = str(path)
    if re.match(r"^[A-Za-z][A-Za-z0-9+.-]*://", raw):
        raise IntegrityError("DNA inputs must be local files, not URLs")
    candidate = Path(path).expanduser().resolve()
    if candidate.name != expected_name:
        raise IntegrityError(f"DNA input basename must be {expected_name}")
    if candidate.parent.name != ".tmp-dna":
        raise IntegrityError("DNA inputs must be directly under .tmp-dna")
    if repo_root is not None:
        expected_parent = Path(repo_root).resolve() / ".tmp-dna"
        if candidate.parent != expected_parent:
            raise IntegrityError("DNA input must be from the repository .tmp-dna directory")
    if not candidate.is_file():
        raise IntegrityError(f"DNA input does not exist: {candidate}")
    if any(part.lower() in {"holdout", "online", "eval", "exports"} for part in candidate.parts):
        raise IntegrityError("holdout/online/eval/export inputs are not allowed")
    return candidate


def validate_output_dir(path: str | os.PathLike[str], software_root: str | os.PathLike[str]) -> Path:
    software = Path(software_root).resolve()
    candidate = Path(path).resolve()
    expected = software / "exports" / "replay_dna"
    if candidate != expected:
        raise IntegrityError("DNA output must be exactly exports/replay_dna")
    candidate.mkdir(parents=True, exist_ok=True)
    return candidate


def assert_no_forbidden_fields(value: Any, path: str = "$") -> None:
    """Reject forbidden names at every nesting level, case-insensitively."""
    if isinstance(value, Mapping):
        for key, child in value.items():
            if not isinstance(key, str):
                raise IntegrityError(f"forbidden/non-string field at {path}")
            if key.lower() in FORBIDDEN_FIELDS:
                raise IntegrityError(f"forbidden DNA output field {key!r} at {path}")
            assert_no_forbidden_fields(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            assert_no_forbidden_fields(child, f"{path}[{index}]")


def assert_finite_numbers(value: Any, path: str = "$") -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise IntegrityError(f"non-finite DNA number at {path}")
    if isinstance(value, Mapping):
        for key, child in value.items():
            assert_finite_numbers(child, f"{path}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, child in enumerate(value):
            assert_finite_numbers(child, f"{path}[{index}]")


def canonical_artifact_digest(payload: Mapping[str, Any]) -> str:
    """Canonical SHA-256 over an artifact with its self-referential digest removed."""
    copy_payload = copy.deepcopy(dict(payload))
    digests = copy_payload.get("digests")
    if isinstance(digests, Mapping):
        digests = dict(digests)
        digests.pop("canonical_payload_sha256", None)
        copy_payload["digests"] = digests
    return canonical_sha256(copy_payload)


def _source_entry(path: Path, repo_root: Path, role: str, capture_dates: list[str]) -> dict[str, Any]:
    try:
        relative = path.relative_to(repo_root).as_posix()
    except ValueError as exc:
        raise IntegrityError(f"DNA source is outside repository root: {path}") from exc
    return {"name": path.name, "path": relative, "sha256": _sha256(path), "role": role,
            "source_url": DATASET_URL, "capture_dates": capture_dates}


def build_source_manifest(paths: Mapping[str, Path], repo_root: Path) -> list[dict[str, Any]]:
    capture_dates: list[str] = []
    try:
        import csv
        with paths["barcodes.csv"].open("r", encoding="utf-8", newline="") as stream:
            capture_dates = sorted({row["capture_batch"] for row in csv.DictReader(stream)
                                    if row.get("capture_batch")})
    except (OSError, KeyError, ValueError) as exc:
        raise IntegrityError(f"cannot inspect barcode capture dates: {exc}") from exc
    return [
        _source_entry(paths["barcodes.csv"], repo_root, "episode_barcode_samples", capture_dates),
        _source_entry(paths["consensus.csv"], repo_root, "producer_attested_consensus", capture_dates),
        _source_entry(paths["reference_barcodes.csv"], repo_root, "reference_barcodes", []),
        _source_entry(paths["field_validation.json"], repo_root, "field_specific_frequency_validation", []),
    ]


def build_implementation_manifest(implementation_root: Path = IMPLEMENTATION_ROOT) -> list[dict[str, str]]:
    software = Path(implementation_root).resolve()
    entries = []
    for relative in IMPLEMENTATION_FILES:
        path = software / relative
        if not path.is_file():
            raise IntegrityError(f"DNA implementation file is missing: {relative}")
        entries.append({"path": f"workspace/software/{relative}", "sha256": _sha256(path)})
    return entries
def _safe_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise IntegrityError(f"cannot read JSON artifact {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise IntegrityError(f"JSON artifact {path} must be an object")
    return value


def _schema_validate(payload: dict[str, Any], schema_path: Path) -> None:
    try:
        import jsonschema
        schema = _safe_json(schema_path)
        jsonschema.validate(payload, schema, format_checker=jsonschema.FormatChecker())
    except ImportError as exc:
        raise IntegrityError("jsonschema is required for DNA schema validation") from exc
    except jsonschema.ValidationError as exc:
        raise IntegrityError(f"DNA JSON Schema validation failed: {exc.message}") from exc


def validate_schema_payload(payload: dict[str, Any], schema_path: Path) -> None:
    assert_no_forbidden_fields(payload)
    assert_finite_numbers(payload)
    _schema_validate(payload, Path(schema_path))


def _relative_source_paths(report: Mapping[str, Any], repo_root: Path) -> dict[str, Path]:
    manifest = report.get("source_manifest")
    if not isinstance(manifest, list) or len(manifest) != len(SOURCE_NAMES):
        raise IntegrityError("source manifest must contain the four authoritative inputs")
    paths: dict[str, Path] = {}
    for entry in manifest:
        if not isinstance(entry, dict) or set(entry) != {
                "name", "path", "sha256", "role", "source_url", "capture_dates"}:
            raise IntegrityError("source manifest entry shape is invalid")
        name, relative = entry["name"], entry["path"]
        if name not in SOURCE_NAMES or name in paths or not isinstance(relative, str):
            raise IntegrityError("source manifest names are invalid or duplicated")
        path = (repo_root / relative).resolve()
        expected = validate_input_path(path, name, repo_root)
        if _sha256(expected) != entry["sha256"]:
            raise IntegrityError(f"source SHA drift for {name}")
        paths[name] = expected
    if set(paths) != set(SOURCE_NAMES):
        raise IntegrityError("source manifest is missing an authoritative input")
    return paths


def _recomputed_report_fields(report: Mapping[str, Any], paths: Mapping[str, Path]) -> dict[str, Any]:
    try:
        data = load_authoritative_sources(paths["barcodes.csv"], paths["consensus.csv"],
                                          paths["reference_barcodes.csv"], paths["field_validation.json"])
        derived = derive_forensics(data)
        validate_field_validation(data["field_validation"])
    except ForensicsError as exc:
        raise IntegrityError(f"source semantic validation failed: {exc}") from exc
    expected = {key: report.get(key) for key in (
        "samples", "groups", "supplied_consensus", "references", "comparisons", "summary")}
    actual = {key: derived[key] for key in expected}
    if expected != actual:
        raise IntegrityError("report analysis differs from deterministic source recomputation")
    return actual


def validate_artifacts(index_path: str | os.PathLike[str], report_path: str | os.PathLike[str],
                       schema_path: str | os.PathLike[str], *,
                       software_root: str | os.PathLike[str]) -> dict[str, Any]:
    index_file, report_file, schema_file = map(lambda value: Path(value).resolve(),
                                                (index_path, report_path, schema_path))
    software = Path(software_root).resolve()
    output = validate_output_dir(report_file.parent, software)
    if index_file.parent != output or schema_file.parent != output:
        raise IntegrityError("DNA artifacts must be colocated in exports/replay_dna")
    index, report = _safe_json(index_file), _safe_json(report_file)
    assert_no_forbidden_fields(index)
    assert_no_forbidden_fields(report)
    assert_finite_numbers(index)
    assert_finite_numbers(report)
    _schema_validate(index, schema_file)
    _schema_validate(report, schema_file)
    if index.get("artifact_kind") != "dna_index" or report.get("artifact_kind") != "dna_report":
        raise IntegrityError("DNA artifact kinds are inconsistent")
    if index.get("report_sha256") != _sha256(report_file):
        raise IntegrityError("report SHA drift")
    if index.get("digests", {}).get("canonical_payload_sha256") != canonical_artifact_digest(index):
        raise IntegrityError("index canonical digest mismatch")
    if report.get("digests", {}).get("canonical_payload_sha256") != canonical_artifact_digest(report):
        raise IntegrityError("report canonical digest mismatch")
    expected_counts = {
        "samples": report.get("summary", {}).get("sample_count"),
        "groups": report.get("summary", {}).get("group_count"),
        "comparisons": report.get("summary", {}).get("comparison_count"),
    }
    if index.get("counts") != expected_counts:
        raise IntegrityError("index/report counts mismatch")
    if index.get("evidence_scope") != report.get("evidence_scope"):
        raise IntegrityError("index/report evidence scope mismatch")
    if report.get("evidence_scope") != EVIDENCE_SCOPE:
        raise IntegrityError("DNA evidence scope is not the required offline exploratory scope")
    for field in ("schema_version", "generated_at", "command"):
        if index.get(field) != report.get(field):
            raise IntegrityError(f"index/report {field} mismatch")
    if report.get("schema_version") != SCHEMA_VERSION:
        raise IntegrityError("DNA schema version is not supported")
    for artifact in (index, report):
        if artifact.get("digests", {}).get("algorithm") != DIGEST_ALGORITHM:
            raise IntegrityError("DNA canonical digest algorithm is not supported")
    expected_command = {
        "argv": ["python", "workspace/software/scripts/analyze_dna_forensics.py"],
        "cwd": str(_repo_root(software)),
        "parameters": {
            "inputs": list(SOURCE_NAMES),
            "output_dir": "workspace/software/exports/replay_dna",
        },
    }
    if report.get("command") != expected_command:
        raise IntegrityError("DNA generation command metadata is not canonical")
    repo = _repo_root(software)
    paths = _relative_source_paths(report, repo)
    expected_manifest = build_source_manifest(paths, repo)
    if report.get("source_manifest") != expected_manifest:
        raise IntegrityError("source manifest metadata differs from authoritative inputs")
    expected_implementation = build_implementation_manifest()
    if report.get("implementation_manifest") != expected_implementation:
        raise IntegrityError("implementation manifest SHA drift")
    if index.get("implementation_manifest") != report.get("implementation_manifest"):
        raise IntegrityError("index/report implementation manifest mismatch")
    _recomputed_report_fields(report, paths)
    if index.get("source_manifest") != report.get("source_manifest"):
        raise IntegrityError("index/report source manifest mismatch")
    if index.get("report_path") != "workspace/software/exports/replay_dna/report.json":
        raise IntegrityError("report path must be canonical")
    return {"valid": True, "samples": report["summary"]["sample_count"],
            "groups": report["summary"]["group_count"],
            "comparisons": report["summary"]["comparison_count"],
            "source_files": len(paths)}
