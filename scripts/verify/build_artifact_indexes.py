#!/usr/bin/env python3
"""Build deterministic indexes for campaign artifacts and acceptance runs."""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
SOFTWARE_ROOT = REPO_ROOT / "workspace" / "software"
INDEX_PATHS = {
    "ablations": SOFTWARE_ROOT / "exports" / "ablations" / "index.json",
    "external": SOFTWARE_ROOT / "exports" / "external" / "index.json",
    "online": SOFTWARE_ROOT / "exports" / "online" / "index.json",
    "acceptance": REPO_ROOT / "workspace" / "acceptance" / "index.json",
}

DECISIONS = {
    "workspace/software/exports/ablations/mf_vs_v102_dev.json":
        ("rejected_noop", "development", True),
    "workspace/software/exports/ablations/mf_vs_v102_reg.json":
        ("rejected_noop", "regression", True),
    "workspace/software/exports/ablations/mg_vs_v102_dev.json":
        ("accepted_development", "development", False),
    "workspace/software/exports/ablations/mg_vs_v102_reg.json":
        ("accepted_development", "regression", False),
    "workspace/software/exports/external/v48-seed101-smoke.json":
        ("historical_v10.2_only", "external_toolchain_smoke", True),
    "workspace/software/exports/external/v48-seed101-ratings.json":
        ("historical_v10.2_only", "descriptive_rating_smoke", True),
}

ACCEPTANCE_SUPERSEDES = {
    "run-30": ["run-26", "run-27", "run-28"],
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _repo_path(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _git(root: Path, *args: str) -> str | None:
    result = subprocess.run(["git", *args], cwd=root, text=True,
                            capture_output=True, check=False, timeout=30)
    return result.stdout.strip() if result.returncode == 0 else None


def _git_metadata(root: Path, relative: str) -> tuple[bool, str | None, str | None]:
    tracked = _git(root, "ls-files", "--error-unmatch", "--", relative) is not None
    if not tracked:
        return False, None, None
    if _git(root, "diff", "--quiet", "HEAD", "--", relative) is None:
        raise ValueError(f"tracked artifact is dirty: {relative}")
    source_commit = _git(root, "log", "-1", "--format=%H", "--", relative)
    blob_oid = _git(root, "rev-parse", f"HEAD:{relative}")
    return True, source_commit or None, blob_oid or None


def _load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    return value if isinstance(value, dict) else {}


def _common_entry(path: Path, root: Path) -> dict[str, Any]:
    relative = _repo_path(path, root)
    tracked, source_commit, blob_oid = _git_metadata(root, relative)
    return {
        "path": relative,
        "sha256": _sha256(path),
        "artifact_id": path.stem,
        "milestone": None,
        "candidate_sha256": None,
        "baseline_sha256": None,
        "source_commit": source_commit,
        "git_blob_oid": blob_oid,
        "decision": "historical_unclassified",
        "evidence_scope": "unspecified",
        "produced_at": None,
        "supersedes": [],
        "immutable": True,
        "historical_only": True,
        "repository_tracked": tracked,
    }


def _ablation_entries(root: Path) -> list[dict[str, Any]]:
    directory = root / "workspace" / "software" / "exports" / "ablations"
    entries = []
    for path in sorted(directory.glob("*.json")):
        if path.name == "index.json":
            continue
        payload = _load_json(path)
        entry = _common_entry(path, root)
        identity = payload.get("identity", {})
        candidate = identity.get("candidate", {}) if isinstance(identity, dict) else {}
        champion = identity.get("champion", {}) if isinstance(identity, dict) else {}
        entry.update({
            "milestone": payload.get("label") or path.stem,
            "candidate_sha256": candidate.get("sha256"),
            "baseline_sha256": champion.get("sha256"),
            "produced_at": payload.get("generated_at"),
        })
        override = DECISIONS.get(entry["path"])
        if override:
            entry["decision"], entry["evidence_scope"], entry["historical_only"] = override
        entries.append(entry)
    return entries


def _external_entries(root: Path) -> list[dict[str, Any]]:
    directory = root / "workspace" / "software" / "exports" / "external"
    entries = []
    for path in sorted(directory.glob("*.json")):
        if path.name == "index.json":
            continue
        payload = _load_json(path)
        entry = _common_entry(path, root)
        identity = payload.get("identity", {})
        candidate = identity.get("candidate", {}) if isinstance(identity, dict) else {}
        if not isinstance(candidate, dict):
            candidate = {}
        entry.update({
            "milestone": "P1 external H2H and BT toolchain",
            "candidate_sha256": candidate.get("sha256"),
            "produced_at": payload.get("generated_at"),
        })
        override = DECISIONS.get(entry["path"])
        if override:
            entry["decision"], entry["evidence_scope"], entry["historical_only"] = override
            entry["candidate_sha256"] = entry["candidate_sha256"] or \
                "360714f1c175c81c75ad53a60782512077c237d963780227c4544a0b5d7cc93f"
        entries.append(entry)
    return entries


def _online_entries(root: Path) -> list[dict[str, Any]]:
    directory = root / "workspace" / "software" / "exports" / "online"
    entries = []
    for path in sorted(p for p in directory.iterdir() if p.is_file()):
        if path.name == "index.json":
            continue
        payload = _load_json(path) if path.suffix == ".json" else {}
        entry = _common_entry(path, root)
        is_ledger = "ledger" in path.stem
        entry.update({
            "milestone": f"online {path.stem}",
            "candidate_sha256": payload.get("candidate_sha256"),
            "decision": "online_observation" if is_ledger else "derived_analysis",
            "evidence_scope": "online_public" if is_ledger else "online_derived",
            "produced_at": payload.get("recorded_at_utc") or
                           payload.get("submitted_at_utc") or
                           payload.get("generated_at"),
        })
        entries.append(entry)
    return entries


def _acceptance_entries(root: Path) -> list[dict[str, Any]]:
    directory = root / "workspace" / "acceptance"
    entries = []
    for path in sorted(directory.glob("run-*.json"),
                       key=lambda p: int(p.stem.split("-")[1])):
        payload = _load_json(path)
        entry = _common_entry(path, root)
        scope = payload.get("scope")
        result = payload.get("result")
        scoped_current = path.stem in {"run-30", "run-31"}
        entry.update({
            "milestone": payload.get("campaign", {}).get("competition_id"),
            "decision": ("acceptance_scoped_pass" if scoped_current and result == "pass"
                         else f"acceptance_{result}" if result else "acceptance_unknown"),
            "evidence_scope": scope or "legacy_full_run",
            "produced_at": payload.get("generated_at"),
            "supersedes": ACCEPTANCE_SUPERSEDES.get(path.stem, []),
            "historical_only": not scoped_current,
        })
        entries.append(entry)
    return entries


def build_indexes(root: Path = REPO_ROOT) -> dict[str, dict[str, Any]]:
    builders = {
        "ablations": _ablation_entries,
        "external": _external_entries,
        "online": _online_entries,
        "acceptance": _acceptance_entries,
    }
    return {
        name: {
            "schema_version": "artifact-index/1.0",
            "collection": name,
            "generated_by": "scripts/verify/build_artifact_indexes.py",
            "entries": builder(root),
        }
        for name, builder in builders.items()
    }


def validate_indexes(root: Path = REPO_ROOT) -> dict[str, int]:
    expected = build_indexes(root)
    counts = {}
    for name, path in INDEX_PATHS.items():
        actual = json.loads(path.read_text(encoding="utf-8"))
        if actual != expected[name]:
            raise ValueError(f"stale artifact index: {_repo_path(path, root)}")
        counts[name] = len(actual["entries"])
    return counts


def main() -> int:
    indexes = build_indexes(REPO_ROOT)
    for name, payload in indexes.items():
        path = INDEX_PATHS[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        print(f"[artifact-index] {name}: {len(payload['entries'])} -> "
              f"{_repo_path(path, REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
