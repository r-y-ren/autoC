"""Generate source-attested offline DNA forensics from explicit local inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

SOFTWARE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.dna_forensics import (  # noqa: E402
    ForensicsError,
    derive_forensics,
    load_authoritative_sources,
)
from kgenv.dna_integrity import (  # noqa: E402
    DIGEST_ALGORITHM,
    EVIDENCE_SCOPE,
    SCHEMA_VERSION,
    IntegrityError,
    assert_finite_numbers,
    assert_no_forbidden_fields,
    build_implementation_manifest,
    build_source_manifest,
    canonical_artifact_digest,
    validate_input_path,
    validate_output_dir,
    validate_schema_payload,
)


def _json_bytes(payload: dict) -> bytes:
    return (json.dumps(payload, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("wb", prefix=f".{path.name}.", suffix=".tmp",
                                     dir=path.parent, delete=False) as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--barcodes", type=Path, required=True)
    parser.add_argument("--consensus", type=Path, required=True)
    parser.add_argument("--references", type=Path, required=True)
    parser.add_argument("--field-validation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path,
                        default=SOFTWARE_ROOT / "exports" / "replay_dna")
    return parser


def main(argv=None, *, software_root: Path = SOFTWARE_ROOT) -> int:
    args = build_parser().parse_args(argv)
    software_root = Path(software_root).resolve()
    try:
        repo_root = software_root.parents[1]
        paths = {
            "barcodes.csv": validate_input_path(args.barcodes, "barcodes.csv", repo_root),
            "consensus.csv": validate_input_path(args.consensus, "consensus.csv", repo_root),
            "reference_barcodes.csv": validate_input_path(
                args.references, "reference_barcodes.csv", repo_root),
            "field_validation.json": validate_input_path(
                args.field_validation, "field_validation.json", repo_root),
        }
        output = validate_output_dir(args.output_dir, software_root)
        source_data = load_authoritative_sources(
            paths["barcodes.csv"], paths["consensus.csv"],
            paths["reference_barcodes.csv"], paths["field_validation.json"])
        derived = derive_forensics(source_data)
        manifest = build_source_manifest(paths, repo_root)
        implementation_manifest = build_implementation_manifest()
        generated_at = datetime.now(timezone.utc).isoformat()
        command = {
            "argv": ["python", "workspace/software/scripts/analyze_dna_forensics.py"],
            "cwd": str(repo_root),
            "parameters": {"inputs": list(paths),
                           "output_dir": "workspace/software/exports/replay_dna"},
        }
        report = {
            "artifact_kind": "dna_report", "schema_version": SCHEMA_VERSION,
            "generated_at": generated_at, "evidence_scope": dict(EVIDENCE_SCOPE),
            "source_manifest": manifest, "implementation_manifest": implementation_manifest,
            **derived, "command": command,
            "digests": {"algorithm": DIGEST_ALGORITHM,
                        "canonical_payload_sha256": ""},
        }
        report["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(report)
        schema_path = output / "dna_schema.json"
        if not schema_path.is_file():
            raise IntegrityError("DNA schema must exist before generating artifacts")
        validate_schema_payload(report, schema_path)
        report_data = _json_bytes(report)
        index = {
            "artifact_kind": "dna_index", "schema_version": SCHEMA_VERSION,
            "generated_at": generated_at, "evidence_scope": dict(EVIDENCE_SCOPE),
            "source_manifest": manifest, "implementation_manifest": implementation_manifest,
            "report_path": "workspace/software/exports/replay_dna/report.json",
            "report_sha256": _sha256_bytes(report_data),
            "counts": {"samples": derived["summary"]["sample_count"],
                       "groups": derived["summary"]["group_count"],
                       "comparisons": derived["summary"]["comparison_count"]},
            "command": command,
            "digests": {"algorithm": DIGEST_ALGORITHM,
                        "canonical_payload_sha256": ""},
        }
        index["digests"]["canonical_payload_sha256"] = canonical_artifact_digest(index)
        validate_schema_payload(index, schema_path)
        index_data = _json_bytes(index)
        _atomic_write(output / "report.json", report_data)
        _atomic_write(output / "index.json", index_data)
    except (OSError, ValueError, ForensicsError, IntegrityError) as exc:
        print(f"DNA forensics: FAIL ({exc})", file=sys.stderr)
        return 1
    print("DNA forensics: PASS "
          f"({derived['summary']['sample_count']} samples, "
          f"{derived['summary']['group_count']} submission groups across both seats, "
          f"{derived['summary']['comparison_count']} comparisons; offline exploratory)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
