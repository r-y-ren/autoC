#!/usr/bin/env python3
"""Run or verify the single frozen-candidate Kaggriculture holdout."""

from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
REPO_ROOT = SOFTWARE_ROOT.parents[1]
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv import official_engine_version
from kgenv.arena import AbnormalMatchError, run_match
from kgenv.engine import FULL_EPISODE_STEPS
from kgenv.eval_contract import (
    ContractError,
    STANDARD_MATRIX_ORDER,
    candidate_snapshot,
    canonical_sha256,
    file_sha256,
)
from kgenv.holdout_contract import (
    HISTORICAL_SEEDS,
    HOLDOUT_EXPECTED_GAMES,
    HOLDOUT_EXPECTED_SEATS,
    HOLDOUT_SCHEMA_VERSION,
    atomic_write_json,
    candidate_confirmatory,
    canonical_holdout_pairs,
    canonical_holdout_schedule,
    create_or_load_attempt,
    hash_input_closure,
    invalidate_attempt,
    project_holdout_metrics,
    utc_now,
    validate_holdout_payload,
)
from scripts.run_eval import _export_game, _validate_replay_bytes, build_players, elo_table

FROZEN_MANIFEST = SOFTWARE_ROOT / "m2b_frozen_manifest.json"
FROZEN_SNAPSHOT = SOFTWARE_ROOT / "m2b_frozen_candidate.b64"
SCHEMA_PATH = SOFTWARE_ROOT / "exports" / "holdout_schema.json"
FORMAL_EXPORT = SOFTWARE_ROOT / "exports" / "eval_results.json"
FORMAL_REPLAY = SOFTWARE_ROOT / "exports" / "logs" / "replay_log.jsonl"
PUBLIC_MANIFEST = SOFTWARE_ROOT / "exports" / "holdout" / "seed_manifest.json"
PRIVATE_DIR = REPO_ROOT / ".flow" / "holdout"
ATTEMPT_PATH = PRIVATE_DIR / "private_attempt.json"
GAMES_PATH = PRIVATE_DIR / "private_games.json"
STAGED_GENERATION = PRIVATE_DIR / "staged_generation"
PUBLISHED_GENERATION = SOFTWARE_ROOT / "exports" / "holdout" / "published"
GEN_EXPORT = PUBLISHED_GENERATION / "eval_results.json"
GEN_REPLAY = PUBLISHED_GENERATION / "replay_log.jsonl"
GEN_MANIFEST = PUBLISHED_GENERATION / "seed_manifest.json"
GEN_METRICS = PUBLISHED_GENERATION / "software_metrics.json"
METRICS_PATH = SOFTWARE_ROOT / "metrics.json"
CLOSURE_PATHS = tuple(sorted({
    "workspace/software/scripts/run_holdout.py",
    "workspace/software/scripts/run_eval.py",
    "workspace/software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl",
    "workspace/software/exports/holdout_schema.json",
    "workspace/software/m2b_frozen_manifest.json",
    "workspace/software/m2b_frozen_candidate.b64",
    *(
        path.relative_to(REPO_ROOT).as_posix()
        for path in (SOFTWARE_ROOT / "kgenv").rglob("*.py")
    ),
}))


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True,
        check=True, timeout=30,
    ).stdout.strip()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _schema_validate(payload: dict) -> None:
    import jsonschema

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(payload, schema)
    validate_holdout_payload(payload)


def _load_frozen_blob(manifest: dict) -> bytes:
    candidate = manifest.get("candidate") or {}
    snapshot = manifest.get("frozen_snapshot") or {}
    if snapshot.get("path") != FROZEN_SNAPSHOT.relative_to(REPO_ROOT).as_posix():
        raise ContractError("frozen snapshot path differs from manifest")
    if file_sha256(FROZEN_SNAPSHOT) != snapshot.get("file_sha256"):
        raise ContractError("frozen snapshot file SHA differs from manifest")
    try:
        frozen_bytes = base64.b64decode(FROZEN_SNAPSHOT.read_bytes().strip(), validate=True)
    except (OSError, ValueError) as exc:
        raise ContractError(f"cannot decode frozen candidate snapshot: {exc}") from exc
    if _sha256_bytes(frozen_bytes) != candidate.get("sha256"):
        raise ContractError("decoded frozen snapshot does not match candidate SHA")
    return frozen_bytes


@contextmanager
def frozen_candidate_snapshot(manifest: dict, evaluation_input: dict):
    candidate = manifest["candidate"]
    data = _load_frozen_blob(manifest)
    with tempfile.TemporaryDirectory(prefix="m2c_frozen_candidate_") as temp:
        snapshot_path = Path(temp) / "main.py"
        snapshot_path.write_bytes(data)
        identity = {
            "submission_path": candidate["path"],
            "submission_sha256": candidate["sha256"],
            "git_ref": candidate["git_ref"],
            "dirty": False,
            "input_sha256": canonical_sha256(evaluation_input),
        }

        class Snapshot:
            def __init__(self):
                self.snapshot_path = snapshot_path
                self.identity = identity

            def verify_candidate_unchanged(self):
                if file_sha256(snapshot_path) != candidate["sha256"]:
                    raise ContractError("immutable frozen candidate snapshot changed")
                if _sha256_bytes(_load_frozen_blob(manifest)) != candidate["sha256"]:
                    raise ContractError("frozen candidate Git blob changed")

            verify_unchanged = verify_candidate_unchanged

        snapshot = Snapshot()
        snapshot.verify_candidate_unchanged()
        yield snapshot


def _load_frozen(require_frozen: bool = True) -> tuple[dict, str]:
    if not FROZEN_MANIFEST.is_file():
        raise ContractError("frozen candidate manifest is missing")
    manifest = json.loads(FROZEN_MANIFEST.read_text(encoding="utf-8"))
    manifest_sha = file_sha256(FROZEN_MANIFEST)
    candidate = manifest.get("candidate") or {}
    candidate_path = REPO_ROOT / candidate.get("path", "")
    if not candidate_path.is_file():
        raise ContractError("frozen candidate path is missing")
    current_sha = file_sha256(candidate_path)
    if require_frozen and current_sha != candidate.get("sha256"):
        raise ContractError("current candidate SHA does not match frozen manifest")
    _load_frozen_blob(manifest)
    return manifest, manifest_sha


def _runtime_engine_closure() -> dict:
    import kaggle_environments

    package_root = Path(kaggle_environments.__file__).resolve().parent
    wheel = SOFTWARE_ROOT / "vendor" / "kaggle_environments-1.32.7+nodeps-py3-none-any.whl"
    hashes = {}
    mismatches = []
    with zipfile.ZipFile(wheel) as archive:
        members = sorted(
            name for name in archive.namelist()
            if name.startswith("kaggle_environments/") and not name.endswith("/")
        )
        member_relatives = {
            name.removeprefix("kaggle_environments/") for name in members
        }
        for member in members:
            relative = member.removeprefix("kaggle_environments/")
            installed = package_root / Path(relative)
            wheel_data = archive.read(member)
            wheel_sha = _sha256_bytes(wheel_data)
            if not installed.is_file() or file_sha256(installed) != wheel_sha:
                mismatches.append(relative)
            hashes[relative] = wheel_sha
    extras = sorted(
        path.relative_to(package_root).as_posix()
        for path in package_root.rglob("*")
        if path.is_file()
        and path.relative_to(package_root).as_posix() not in member_relatives
        and "__pycache__" not in path.parts
        and path.suffix != ".pyc"
    )
    if mismatches or extras or not hashes:
        raise ContractError(
            "installed kaggle-environments differs from vendored wheel: "
            f"mismatches={mismatches}, extras={extras}"
        )
    body = {
        "package_root": str(package_root),
        "distribution_version": importlib.metadata.version("kaggle-environments"),
        "vendored_wheel_sha256": file_sha256(wheel),
        "wheel_match": True,
        "file_count": len(hashes),
        "files": hashes,
    }
    return {**body, "sha256": canonical_sha256(body)}


def _input_closure() -> dict:
    source = hash_input_closure(REPO_ROOT, CLOSURE_PATHS)
    body = {"repository": source, "runtime_engine": _runtime_engine_closure()}
    return {**body, "sha256": canonical_sha256(body)}


def preflight(require_frozen: bool = True, *, require_clean: bool = True) -> dict:
    manifest, manifest_sha = _load_frozen(require_frozen)
    if require_clean and _git("status", "--porcelain"):
        raise ContractError("holdout preflight requires a clean tracked worktree")
    closure = _input_closure()
    candidate = manifest["candidate"]
    return {
        "candidate_path": candidate["path"],
        "candidate_sha256": candidate["sha256"],
        "frozen_git_ref": candidate["git_ref"],
        "frozen_manifest_sha256": manifest_sha,
        "evaluator_closure": closure,
        "expected_games": HOLDOUT_EXPECTED_GAMES,
        "holdout_revealed": PUBLIC_MANIFEST.exists(),
        "published": FORMAL_EXPORT.exists() and _is_published_holdout(FORMAL_EXPORT),
    }


def _is_published_holdout(path: Path) -> bool:
    try:
        return json.loads(path.read_text(encoding="utf-8")).get("run_kind") == "official_holdout"
    except (OSError, ValueError):
        return False


def _load_checkpoint(state: dict, schedule: list[dict]) -> list[dict]:
    if not GAMES_PATH.exists():
        if state.get("completed_games", 0) != 0:
            raise ContractError("holdout checkpoint is missing")
        return []
    checkpoint = json.loads(GAMES_PATH.read_text(encoding="utf-8"))
    if checkpoint.get("attempt_id") != state["attempt_id"]:
        raise ContractError("holdout checkpoint belongs to another attempt")
    games = checkpoint.get("games") or []
    completed = state.get("completed_games", 0)
    if len(games) == completed + 1:
        state["completed_games"] = len(games)
        state["updated_at"] = utc_now()
        atomic_write_json(ATTEMPT_PATH, state)
    elif len(games) != completed:
        raise ContractError("holdout checkpoint count differs from attempt state")
    expected = [(item["p0"], item["p1"], item["seed"], item["seat"]) for item in schedule[:len(games)]]
    observed = [(game["p0"], game["p1"], game["seed"], game["seat"]) for game in games]
    if observed != expected:
        raise ContractError("holdout checkpoint is not an exact schedule prefix")
    return games


def _save_checkpoint(state: dict, games: list[dict]) -> None:
    atomic_write_json(GAMES_PATH, {"attempt_id": state["attempt_id"], "games": games})
    state["completed_games"] = len(games)
    state["updated_at"] = utc_now()
    atomic_write_json(ATTEMPT_PATH, state)


def _replay_bytes(games: list[dict]) -> bytes:
    rows = []
    for game in games:
        rows.append(json.dumps({
            "players": game["players"], "winner": game["winner"],
            "seed": game["seed"], "seed_domain": game["seed_domain"],
            "seat": game["seat"], "statuses": game["statuses"],
            "contract_ok": game["contract_ok"], "rewards": game["rewards"],
            "turns": game["turns"], "elapsed_seconds": game["elapsed_seconds"],
        }, ensure_ascii=False))
    return (("\n".join(rows) + "\n") if rows else "").encode("utf-8")


def _public_seed_manifest(state: dict) -> dict:
    return {
        "schema_version": "1.0",
        "attempt_id": state["attempt_id"],
        "generated_after_freeze": True,
        "random_source": "Python secrets.randbelow (OS cryptographic entropy)",
        "revealed_at": utc_now(),
        "seeds": state["seeds"],
        "sha256": canonical_sha256(state["seeds"]),
        "historical_seed_exclusion_count": len(HISTORICAL_SEEDS),
        "overlap_with_historical": [],
    }


def _build_payload(state: dict, games: list[dict], identity: dict,
                   closure_before: dict, closure_after: dict,
                   runtime_seconds: float) -> tuple[dict, dict]:
    seeds = state["seeds"]
    evaluation_input = {
        "pairs": canonical_holdout_pairs(),
        "seeds": seeds,
        "seed_domain": "holdout",
        "seat_orders": ["AB", "BA"],
        "episode_steps": FULL_EPISODE_STEPS,
        "run_kind": "official_holdout",
    }
    if identity["input_sha256"] != canonical_sha256(evaluation_input):
        raise ContractError("candidate snapshot input hash differs from holdout schedule")
    public_manifest = _public_seed_manifest(state)
    exported_games = list(games)
    confirmatory = candidate_confirmatory(exported_games)
    table = elo_table([
        {**game, "winner_label": game["winner"]} for game in exported_games
    ]).ranked()
    frozen = json.loads(FROZEN_MANIFEST.read_text(encoding="utf-8"))["candidate"]
    payload = {
        "schema_version": HOLDOUT_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "run_kind": "official_holdout",
        "seed_domain": "holdout",
        "identity": identity,
        "evaluation_input": evaluation_input,
        "engine": {
            "package": "kaggle-environments",
            "version": official_engine_version(),
            "scenario": "kaggriculture",
            "episode_steps": FULL_EPISODE_STEPS,
        },
        "config": {
            "rounds": 8,
            "seeds": seeds,
            "matrix_order": list(STANDARD_MATRIX_ORDER),
            "pairs": canonical_holdout_pairs(),
            "seat_orders": ["AB", "BA"],
            "expected_games": HOLDOUT_EXPECTED_GAMES,
        },
        "opponent_pool_names": list(STANDARD_MATRIX_ORDER[1:]),
        "games": exported_games,
        "abnormal_games": 0,
        "integrity": {
            "expected_games": HOLDOUT_EXPECTED_GAMES,
            "actual_games": len(exported_games),
            "abnormal_games": 0,
            "ab_games": sum(game["seat"] == "AB" for game in exported_games),
            "ba_games": sum(game["seat"] == "BA" for game in exported_games),
            "missing_mirrors": 0,
        },
        "confirmatory": confirmatory,
        "elo": {
            "role": "descriptive_only",
            "order_sensitive": True,
            "k": 32.0,
            "start": 1200.0,
            "table": table,
        },
        "holdout": {
            "protocol": {
                "full_matrix": True,
                "seed_count": 8,
                "seat_orders": ["AB", "BA"],
                "one_time": True,
                "resume_exact_attempt_only": True,
                "candidate_change_invalidates": True,
                "candidate_source": "frozen_git_blob",
            },
            "frozen_candidate": {"path": frozen["path"], "sha256": frozen["sha256"], "git_ref": frozen["git_ref"]},
            "input_closure": {"sha256": closure_before["sha256"], "before": closure_before, "after": closure_after},
            "attempt": {
                "index": 1,
                "attempt_id": state["attempt_id"],
                "status": "published",
                "started_at": state["started_at"],
                "completed_at": utc_now(),
                "published": True,
                "invalidated": False,
                "invalidation_reason": None,
            },
            "seed_manifest": public_manifest,
            "candidate_hash_match": {
                "frozen": frozen["sha256"],
                "before": identity["submission_sha256"],
                "after": file_sha256(REPO_ROOT / frozen["path"]),
                "pass": frozen["sha256"] == identity["submission_sha256"] == file_sha256(REPO_ROOT / frozen["path"]),
            },
            "seed_domain_isolation": {
                "historical_count": len(HISTORICAL_SEEDS),
                "overlap_count": 0,
                "pass": True,
            },
        },
        "runtime_seconds": round(runtime_seconds, 2),
    }
    return payload, public_manifest


def _generation_bytes(payload: dict, public_manifest: dict,
                      games: list[dict]) -> dict[str, bytes]:
    export_data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    manifest_data = (json.dumps(public_manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    replay_data = _replay_bytes(games)
    shard = json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    shard.setdefault("metrics", {}).update(
        project_holdout_metrics(payload, _sha256_bytes(export_data))
    )
    shard["milestone"] = "m2c-holdout-confirm (validated one-time full-matrix holdout; historical keys retained)"
    metrics_data = (json.dumps(shard, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return {
        "eval_results.json": export_data,
        "replay_log.jsonl": replay_data,
        "seed_manifest.json": manifest_data,
        "software_metrics.json": metrics_data,
    }


def _validate_generation(directory: Path) -> dict:
    required = {
        "eval_results.json", "replay_log.jsonl", "seed_manifest.json",
        "software_metrics.json",
    }
    if not directory.is_dir() or {path.name for path in directory.iterdir()} != required:
        raise ContractError("holdout generation is incomplete")
    payload = json.loads((directory / "eval_results.json").read_text(encoding="utf-8"))
    _schema_validate(payload)
    _validate_replay_bytes(
        (directory / "replay_log.jsonl").read_bytes(), HOLDOUT_EXPECTED_GAMES
    )
    public = json.loads((directory / "seed_manifest.json").read_text(encoding="utf-8"))
    if public != payload["holdout"]["seed_manifest"]:
        raise ContractError("generation seed manifest differs from formal export")
    metrics = json.loads((directory / "software_metrics.json").read_text(encoding="utf-8"))
    trace = metrics.get("metrics", {}).get("confirmatory_export_traceability", {}).get("value", {})
    if trace.get("export_sha256") != file_sha256(directory / "eval_results.json"):
        raise ContractError("generation metrics traceability hash mismatch")
    return payload


def _stage_generation(payload: dict, public_manifest: dict,
                      games: list[dict]) -> Path:
    if PUBLISHED_GENERATION.exists():
        raise ContractError("authoritative holdout generation already exists")
    if STAGED_GENERATION.exists():
        shutil.rmtree(STAGED_GENERATION)
    STAGED_GENERATION.mkdir(parents=True)
    for name, data in _generation_bytes(payload, public_manifest, games).items():
        path = STAGED_GENERATION / name
        with path.open("wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    _validate_generation(STAGED_GENERATION)
    return STAGED_GENERATION


def _commit_generation(staged: Path) -> None:
    PUBLISHED_GENERATION.parent.mkdir(parents=True, exist_ok=True)
    if PUBLISHED_GENERATION.exists():
        raise ContractError("authoritative holdout generation already exists")
    os.replace(staged, PUBLISHED_GENERATION)


def _atomic_project(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
    shutil.copyfile(source, temp)
    os.replace(temp, target)


def _project_generation() -> None:
    _validate_generation(PUBLISHED_GENERATION)
    for source, target in (
        (GEN_EXPORT, FORMAL_EXPORT),
        (GEN_REPLAY, FORMAL_REPLAY),
        (GEN_MANIFEST, PUBLIC_MANIFEST),
        (GEN_METRICS, METRICS_PATH),
    ):
        if not target.exists() or file_sha256(source) != file_sha256(target):
            _atomic_project(source, target)


def _reconcile_published_state() -> dict:
    manifest, _ = _load_frozen(True)
    payload = _validate_generation(PUBLISHED_GENERATION)
    expected_sha = manifest["candidate"]["sha256"]
    if payload["identity"]["submission_sha256"] != expected_sha:
        raise ContractError("published generation identity differs from frozen candidate")
    if not ATTEMPT_PATH.exists():
        raise ContractError("published generation has no private attempt state")
    state = json.loads(ATTEMPT_PATH.read_text(encoding="utf-8"))
    attempt = payload["holdout"]["attempt"]
    if state.get("attempt_id") != attempt.get("attempt_id"):
        raise ContractError("published generation and private attempt differ")
    if state.get("status") not in {"running", "committing", "published"}:
        raise ContractError("published generation has an invalid private attempt state")
    state.update(
        status="published", completed_at=attempt["completed_at"],
        completed_games=HOLDOUT_EXPECTED_GAMES,
    )
    atomic_write_json(ATTEMPT_PATH, state)
    _project_generation()
    return payload


def verify_published(require_frozen: bool = True) -> dict:
    _load_frozen(require_frozen)
    if not PUBLISHED_GENERATION.is_dir():
        raise ContractError("authoritative published holdout generation is missing")
    payload = _reconcile_published_state()
    recorded_closure = payload["holdout"]["input_closure"]["before"]
    current_closure = _input_closure()
    if current_closure != recorded_closure:
        raise ContractError("current evaluator input closure differs from published holdout")
    return validate_holdout_payload(payload)



def execute(require_frozen: bool = True) -> dict:
    if PUBLISHED_GENERATION.exists():
        _load_frozen(require_frozen)
        return validate_holdout_payload(_reconcile_published_state())
    if ATTEMPT_PATH.exists():
        existing = json.loads(ATTEMPT_PATH.read_text(encoding="utf-8"))
        if existing.get("status") == "committing":
            _validate_generation(STAGED_GENERATION)
            _commit_generation(STAGED_GENERATION)
            return validate_holdout_payload(_reconcile_published_state())
    if _is_published_holdout(FORMAL_EXPORT) or PUBLIC_MANIFEST.exists():
        raise ContractError("legacy holdout projection exists without authoritative generation")
    info = preflight(require_frozen, require_clean=True)
    state, _ = create_or_load_attempt(
        ATTEMPT_PATH,
        candidate_sha256=info["candidate_sha256"],
        frozen_manifest_sha256=info["frozen_manifest_sha256"],
        evaluator_closure=info["evaluator_closure"],
    )
    schedule = canonical_holdout_schedule(state["seeds"])
    games = _load_checkpoint(state, schedule)
    evaluation_input = {
        "pairs": canonical_holdout_pairs(), "seeds": state["seeds"],
        "seed_domain": "holdout", "seat_orders": ["AB", "BA"],
        "episode_steps": FULL_EPISODE_STEPS, "run_kind": "official_holdout",
    }
    started = time.perf_counter()
    manifest, _ = _load_frozen(require_frozen)
    try:
        with frozen_candidate_snapshot(manifest, evaluation_input) as snapshot:
            contenders, opponents = build_players(str(snapshot.snapshot_path))
            players = {**contenders, **opponents}
            for index, item in enumerate(schedule[len(games):], start=len(games)):
                result = run_match(
                    players[item["p0"]], players[item["p1"]], seed=item["seed"],
                    label_a=item["p0"], label_b=item["p1"],
                    episode_steps=FULL_EPISODE_STEPS, collect_daily=False,
                )
                result["seat"] = item["seat"]
                result["seed_domain"] = "holdout"
                games.append(_export_game(result))
                _save_checkpoint(state, games)
                print(f"[{index + 1:03d}/{len(schedule)}] completed", flush=True)
            snapshot.verify_unchanged()
            closure_after = _input_closure()
            if closure_after != info["evaluator_closure"]:
                raise ContractError("holdout input closure changed during execution")
            payload, public_manifest = _build_payload(
                state, games, snapshot.identity, info["evaluator_closure"],
                closure_after, time.perf_counter() - started,
            )
            _schema_validate(payload)
            snapshot.verify_candidate_unchanged()
            staged = _stage_generation(payload, public_manifest, games)
            snapshot.verify_candidate_unchanged()
            state.update(status="committing", completed_games=len(games),
                         completed_at=payload["holdout"]["attempt"]["completed_at"])
            atomic_write_json(ATTEMPT_PATH, state)
            snapshot.verify_candidate_unchanged()
            _commit_generation(staged)
        published = _reconcile_published_state()
        return validate_holdout_payload(published)
    except AbnormalMatchError as exc:
        invalidate_attempt(ATTEMPT_PATH, str(exc))
        raise ContractError(
            "holdout attempt invalidated by an abnormal game; private state contains details"
        ) from exc
    except ContractError as exc:
        invalidate_attempt(ATTEMPT_PATH, str(exc))
        raise ContractError(
            "holdout attempt invalidated by an identity or contract failure; private state contains details"
        ) from exc
    except Exception as exc:
        state = json.loads(ATTEMPT_PATH.read_text(encoding="utf-8"))
        state.update(status="running", last_recoverable_error=type(exc).__name__,
                     updated_at=utc_now())
        atomic_write_json(ATTEMPT_PATH, state)
        raise ContractError(
            "holdout paused by a recoverable runner failure; resume the same attempt"
        ) from exc



def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--preflight", action="store_true")
    group.add_argument("--verify-published", action="store_true")
    parser.add_argument("--require-frozen", action="store_true")
    args = parser.parse_args()
    try:
        if args.verify_published:
            report = verify_published(args.require_frozen)
            print(f"PASS published holdout: {report['actual_games']}/576, abnormal=0")
        elif args.preflight:
            report = preflight(args.require_frozen, require_clean=True)
            print(json.dumps(report, ensure_ascii=False, indent=2))
        else:
            if not args.require_frozen:
                raise ContractError("real holdout execution requires --require-frozen")
            report = execute(True)
            print(f"PASS one-time holdout published: {report['actual_games']}/576")
        return 0
    except Exception as exc:  # noqa: BLE001
        print(f"HOLDOUT FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
