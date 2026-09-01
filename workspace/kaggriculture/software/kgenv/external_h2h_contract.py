"""Formal, fail-closed validation for external black-box H2H evidence.

External evidence is deliberately separate from development gates and holdout
artifacts.  The validator re-derives all material claims from the game rows and
from bytes on disk; it never treats a reported aggregate as authoritative.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import os
import re
import zipfile
from pathlib import Path
from typing import Any, Iterable, Sequence

from .eval_contract import ContractError, canonical_sha256

SCHEMA_VERSION = "external-h2h/2.0"
FULL_EPISODE_STEPS = 720
ENGINE_NAME = "kaggle-environments"
ENGINE_VERSIONS = frozenset({"1.32.7", "1.32.7+nodeps"})
RUNTIME_ENGINE_MEMBERS = (
    "__init__.py",
    "core.py",
    "agent.py",
    "utils.py",
    "errors.py",
    "status_codes.json",
    "envs/kaggriculture/kaggriculture.py",
    "envs/kaggriculture/kaggriculture.json",
)


def _digest(value: Any) -> str:
    return canonical_sha256(value)


def _sha256(path: Path) -> str:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError as exc:
        raise ContractError(f"cannot read evidence file {path}: {exc}") from exc


def _resolve(path: str, base: Path) -> Path:
    value = Path(path)
    return value if value.is_absolute() else (base / value).resolve()


def _canonical_repo_root(base: Path) -> Path:
    """Resolve the repository root used by the production contract."""
    candidate = base.resolve()
    if (candidate / "workspace" / "software").is_dir():
        return candidate
    if candidate.name == "software" and (candidate.parent.parent / "workspace" / "software").is_dir():
        return candidate.parent.parent
    raise ContractError("cannot locate canonical repository root")


def _canonical_paths(repo_root: Path) -> dict[str, Path]:
    software = repo_root / "workspace" / "software"
    return {
        "active": software / "active_candidate.json",
        "wheel": software / "vendor" / "kaggle_environments-1.32.7+nodeps-py3-none-any.whl",
        "schema": software / "exports" / "external_h2h_schema.json",
        "validator": software / "kgenv" / "external_h2h_contract.py",
        "probe": software / "scripts" / "h2h_external_probe.py",
        "verify": software / "scripts" / "check_external_h2h.py",
        "provenance": software / "kaggle_simulations" / "opponents" / "PROVENANCE.md",
        "candidate": software / "kaggle_simulations" / "agent" / "main.py",
        "arena": software / "kgenv" / "arena.py",
        "engine": software / "kgenv" / "engine.py",
        "eval_contract": software / "kgenv" / "eval_contract.py",
        "init": software / "kgenv" / "__init__.py",
        "economy": software / "kgenv" / "economy.py",
        "redlines": software / "kgenv" / "redlines.py",
        "gym_env": software / "kgenv" / "gym_env.py",
        "elo": software / "kgenv" / "elo.py",
    }


RUNTIME_CLOSURE_KEYS = ("active", "candidate", "wheel", "schema", "validator", "probe", "verify",
                        "provenance", "arena", "engine", "eval_contract", "init", "economy",
                        "redlines", "gym_env", "elo")


def canonical_external_digest(payload: dict[str, Any]) -> str:
    """Digest the complete payload while excluding the self-referential digest."""
    copy_payload = copy.deepcopy(payload)
    digests = copy_payload.get("digests")
    if isinstance(digests, dict):
        digests.pop("canonical_payload_sha256", None)
    return _digest(copy_payload)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ContractError(message)


def _finite_number(value: Any, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ContractError(f"{field} must be a finite number")
    number = float(value)
    if not math.isfinite(number):
        raise ContractError(f"{field} must be a finite number")
    return number


def _record(winner: str | None, candidate: str, margin: float) -> dict[str, Any]:
    if winner == candidate:
        outcome = "W"
    elif winner is None:
        outcome = "T"
    else:
        outcome = "L"
    return {"outcome": outcome, "margin": float(margin)}


def _aggregate(games: Sequence[dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    def one(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
        wins = sum(row["winner"] == candidate_id for row in rows)
        losses = sum(row["winner"] is not None and row["winner"] != candidate_id for row in rows)
        ties = sum(row["winner"] is None for row in rows)
        margins = [float(row["margin"]) for row in rows]
        return {
            "games": len(rows), "W": wins, "L": losses, "T": ties,
            "score_rate": round((wins + 0.5 * ties) / len(rows), 6) if rows else None,
            "margin": {
                "mean": round(sum(margins) / len(margins), 6) if margins else None,
                "total": round(sum(margins), 6) if margins else 0.0,
                "min": min(margins) if margins else None,
                "max": max(margins) if margins else None,
            },
        }

    by_opponent: dict[str, Any] = {}
    for opponent in sorted({row["opponent_id"] for row in games}):
        by_opponent[opponent] = one([row for row in games if row["opponent_id"] == opponent])
    by_seat = {seat: one([row for row in games if row["seat"] == seat]) for seat in ("AB", "BA")}
    return {"overall": one(games), "by_opponent": by_opponent, "by_seat": by_seat}


def summarize_external_games(games: Sequence[dict[str, Any]], candidate_id: str) -> dict[str, Any]:
    """Build the canonical aggregate representation used by the contract."""
    return _aggregate(games, candidate_id)


def _provenance_entry(provenance_text: str, opponent_id: str) -> dict[str, str]:
    heading = re.search(rf"^##\s+{re.escape(opponent_id)}_main\.py\s*$", provenance_text, re.MULTILINE)
    if not heading:
        raise ContractError(f"provenance has no canonical entry for opponent {opponent_id}")
    section = provenance_text[heading.end():].split("\n## ", 1)[0]
    values = {}
    for label in ("Opponent ID", "Author", "Source", "Source URL", "Acquired at", "SHA-256", "Use restriction"):
        match = re.search(rf"^-\s+{re.escape(label)}:\s*(.+?)\s*$", section, re.MULTILINE)
        if not match:
            raise ContractError(f"provenance missing {label} for opponent {opponent_id}")
        values[label] = match.group(1).split("（", 1)[0].strip()
    _require(values["Opponent ID"] == opponent_id, f"provenance opponent id mismatch for {opponent_id}")
    return values


def _active_entry(active: dict[str, Any], role: str) -> dict[str, Any]:
    if role == "working":
        entry = active.get("working")
    elif role == "frozen":
        entry = active.get("last_promoted_frozen")
    elif role == "published":
        entry = active.get("published_holdout")
    else:
        raise ContractError(f"unsupported candidate role {role!r}")
    if not isinstance(entry, dict):
        raise ContractError(f"active candidate has no {role} entry")
    return entry


def _validate_active_candidate(candidate: dict[str, Any], software_root: Path, *, strict: bool = False) -> None:
    repo_root = _canonical_repo_root(software_root)
    canonical = _canonical_paths(repo_root)
    if strict:
        contract = canonical["active"]
        _require(candidate.get("active_candidate_contract") ==
                 "workspace/software/active_candidate.json",
                 "active candidate contract must use canonical relative path")
    else:
        contract = _resolve(candidate["active_candidate_contract"], software_root)
    try:
        active = json.loads(contract.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise ContractError(f"cannot read active candidate contract: {exc}") from exc
    entry = _active_entry(active, candidate["role"])
    expected_sha = entry.get("sha256") or entry.get("candidate_sha256")
    _require(expected_sha == candidate["sha256"], "candidate identity does not match active candidate SHA")
    expected_status = entry.get("status")
    if candidate["role"] == "working":
        _require(candidate["status"] == "development" and expected_status == "development",
                 "working external evidence must remain development-only")
    elif candidate["role"] == "frozen":
        _require(expected_status == "frozen", "frozen candidate role/status mismatch")
    entry_path = entry.get("path")
    if strict:
        canonical_candidate = repo_root / "workspace" / "software" / "kaggle_simulations" / "agent" / "main.py"
        actual_candidate = _resolve(str(candidate["path"]), repo_root)
        _require(actual_candidate == canonical_candidate.resolve(),
                 "candidate path must be canonical active submission path")
        _require(candidate.get("path") ==
                 "workspace/software/kaggle_simulations/agent/main.py",
                 "candidate path must use canonical relative path")
        _require(candidate["id"] == candidate["role"],
                 "candidate id must match candidate role")
        expected_status = {"working": "development", "frozen": "frozen", "published": "published"}[candidate["role"]]
        _require(candidate["status"] == expected_status and entry.get("status") == expected_status,
                 "candidate role/status mismatch")
    if entry_path:
        actual = _resolve(str(candidate["path"]), repo_root if strict else software_root)
        declared = _resolve(str(entry_path), contract.parent)
        _require(os.path.normcase(str(actual)) == os.path.normcase(str(declared)),
                 "candidate path does not match active candidate contract")


def _validate_opponents(opponents: Any, base: Path, *, strict: bool = False,
                        provenance_sha: str | None = None, provenance_text: str | None = None) -> list[dict[str, Any]]:
    _require(isinstance(opponents, list) and opponents, "opponent list is required")
    ids: set[str] = set()
    repo_root = _canonical_repo_root(base)
    provenance_path = _canonical_paths(repo_root)["provenance"]
    provenance_sha = _sha256(provenance_path)
    provenance_text = provenance_path.read_text(encoding="utf-8")
    for opponent in opponents:
        _require(isinstance(opponent, dict), "opponent entries must be objects")
        for key in ("id", "path", "sha256", "provenance", "license", "use_restriction"):
            _require(key in opponent, f"opponent missing {key}")
        oid = opponent["id"]
        _require(isinstance(oid, str) and oid and oid not in ids, "opponent ids must be unique")
        ids.add(oid)
        path = _resolve(opponent["path"], base)
        _require(_sha256(path) == opponent["sha256"], f"opponent {oid} SHA drift")
        if strict:
            canonical_provenance = _provenance_entry(provenance_text, oid)
            canonical_path = repo_root / "workspace" / "software" / "kaggle_simulations" / "opponents" / path.name
            _require(path == canonical_path.resolve(), f"opponent {oid} path is not canonical")
            expected_relative = f"workspace/software/kaggle_simulations/opponents/{path.name}"
            _require(opponent["path"] == expected_relative,
                     f"opponent {oid} path must use canonical relative path")
            _require(canonical_provenance["SHA-256"] == opponent["sha256"],
                     f"provenance SHA missing for opponent {oid}")
            provenance = opponent["provenance"]
            _require(isinstance(provenance, dict), f"opponent {oid} provenance missing")
            expected_payload = {
                "author": canonical_provenance["Author"],
                "source": canonical_provenance["Source"],
                "source_url": canonical_provenance["Source URL"],
                "acquired_at": canonical_provenance["Acquired at"],
            }
            _require(provenance == expected_payload,
                     f"opponent {oid} provenance payload does not match canonical provenance")
            _require(opponent["use_restriction"] == canonical_provenance["Use restriction"],
                     f"opponent {oid} use restriction does not match canonical provenance")
        else:
            provenance = opponent["provenance"]
            _require(isinstance(provenance, dict), f"opponent {oid} provenance missing")
            for key in ("author", "source", "source_url", "acquired_at"):
                _require(isinstance(provenance.get(key), str) and provenance[key],
                         f"opponent {oid} provenance missing {key}")
        license_info = opponent["license"]
        _require(isinstance(license_info, dict) and isinstance(license_info.get("status"), str),
                 f"opponent {oid} license restriction missing")
        _require(isinstance(opponent["use_restriction"], str) and opponent["use_restriction"],
                 f"opponent {oid} use restriction missing")
    return opponents


def _validate_game(game: dict[str, Any], candidate: dict[str, Any], opponents: dict[str, dict[str, Any]],
                   seeds: set[int], seen_ids: set[str], *, strict: bool = False) -> None:
    required = ("game_id", "opponent_id", "seed", "seat", "players", "candidate_seat",
                "statuses", "contract_ok", "rewards", "winner", "margin", "episode_steps",
                "states", "completion_ok", "activity", "abnormal_reason", "elapsed_seconds")
    _require(isinstance(game, dict), "game entries must be objects")
    _require(all(key in game for key in required), "game missing required field")
    gid = game["game_id"]
    _require(isinstance(gid, str) and gid and gid not in seen_ids, "duplicate or empty game_id")
    seen_ids.add(gid)
    oid = game["opponent_id"]
    _require(oid in opponents, f"game references unknown opponent {oid!r}")
    _require(game["seed"] in seeds, "game seed outside explicit seed list")
    _require(game["seat"] in ("AB", "BA"), "invalid seat assignment")
    expected_players = [candidate["id"], oid] if game["seat"] == "AB" else [oid, candidate["id"]]
    _require(game["players"] == expected_players and game["candidate_seat"] == expected_players.index(candidate["id"]),
             "game player/seat assignment mismatch")
    _require(game["statuses"] == ["DONE", "DONE"] and game["contract_ok"] is True,
             "abnormal game cannot be external evidence")
    rewards = game["rewards"]
    _require(isinstance(rewards, list) and len(rewards) == 2,
             "invalid game rewards")
    rewards = [_finite_number(value, "game rewards") for value in rewards]
    expected_winner = expected_players[0] if rewards[0] > rewards[1] else expected_players[1] if rewards[1] > rewards[0] else None
    _require(game["winner"] == expected_winner, "winner is inconsistent with rewards")
    candidate_seat = game["candidate_seat"]
    expected_margin = rewards[candidate_seat] - rewards[1 - candidate_seat]
    _require(_finite_number(game["margin"], "margin") == expected_margin,
             "margin is inconsistent with rewards")
    _require(game["episode_steps"] == FULL_EPISODE_STEPS and game["states"] == FULL_EPISODE_STEPS and
             game["completion_ok"] is True, "720-state completion is required")
    elapsed_seconds = _finite_number(game.get("elapsed_seconds"), "elapsed_seconds")
    _require(elapsed_seconds >= 0, "elapsed_seconds must be non-negative")
    activity = game["activity"]
    _require(isinstance(activity, dict), "activity diagnostics are required")
    starting_money = _finite_number(activity.get("starting_money"), "activity starting_money")
    _require(activity.get("states") == game["states"] and activity.get("decisions") == game["states"] - 1,
             "activity state/decision totals are inconsistent")
    expected_completion = game["states"] == FULL_EPISODE_STEPS and game["states"] - 1 == FULL_EPISODE_STEPS - 1
    _require(activity.get("completion_ok") is expected_completion,
             "activity completion flag is inconsistent")
    _require(activity.get("contract_status") == "producer_attested" and
             activity.get("independently_recomputed") is False,
             "activity contract must disclose producer-attested trace status")
    seats = activity.get("seats")
    _require(isinstance(seats, list) and len(seats) == 2,
             "activity requires two per-seat diagnostics")
    for seat_index, seat_diag in enumerate(seats):
        _require(isinstance(seat_diag, dict), "activity seat diagnostics must be objects")
        required_activity = ("decisions", "non_pass_decisions", "effective_commands",
                             "max_pass_streak", "non_pass_trace", "state_change_trace",
                             "reward_delta", "pass_only", "reasons", "policy", "evidence")
        _require(all(key in seat_diag for key in required_activity),
                 "activity seat diagnostics require trace-backed numeric fields")
        for key in ("decisions", "non_pass_decisions", "effective_commands", "max_pass_streak"):
            value = seat_diag[key]
            _require(isinstance(value, int) and not isinstance(value, bool) and value >= 0,
                     f"activity {key} must be a non-negative integer")
        decisions = seat_diag["decisions"]
        non_pass_trace = seat_diag["non_pass_trace"]
        state_change_trace = seat_diag["state_change_trace"]
        _require(isinstance(non_pass_trace, list) and len(non_pass_trace) == decisions and
                 all(isinstance(value, bool) for value in non_pass_trace),
                 "activity non_pass_trace must contain one boolean per decision")
        _require(isinstance(state_change_trace, list) and len(state_change_trace) == decisions and
                 all(isinstance(value, bool) for value in state_change_trace),
                 "activity state_change_trace must contain one boolean per decision")
        recomputed_non_pass = sum(non_pass_trace)
        recomputed_changes = sum(state_change_trace)
        pass_streak = recomputed_max_streak = 0
        for non_pass in non_pass_trace:
            pass_streak = 0 if non_pass else pass_streak + 1
            recomputed_max_streak = max(recomputed_max_streak, pass_streak)
        _require(decisions == activity["decisions"] and
                 seat_diag["non_pass_decisions"] == recomputed_non_pass and
                 seat_diag["effective_commands"] == recomputed_changes and
                 seat_diag["max_pass_streak"] == recomputed_max_streak,
                 "activity numeric fields do not match decision traces")
        reward_delta = _finite_number(seat_diag["reward_delta"], "activity reward_delta")
        _require(reward_delta == rewards[seat_index] - starting_money,
                 "activity reward_delta is inconsistent with game reward and starting_money")
        _require(isinstance(seat_diag["pass_only"], bool) and
                 seat_diag["pass_only"] is (recomputed_non_pass == 0),
                 "activity pass_only is inconsistent")
        _require(isinstance(seat_diag["evidence"], dict), "activity evidence is required")
        evidence = seat_diag["evidence"]
        evidence_keys = ("action_count", "non_pass_action_count", "state_change_count",
                         "state_count", "reward_delta", "non_pass_trace",
                         "state_change_trace")
        for key in (*evidence_keys, "evidence_digest"):
            _require(key in evidence, f"activity evidence missing {key}")
        evidence_values = {key: evidence[key] for key in evidence_keys}
        _require(evidence["evidence_digest"] == _digest(evidence_values),
                 "activity evidence digest mismatch")
        evidence_reward_delta = _finite_number(evidence["reward_delta"],
                                                "activity evidence reward_delta")
        _require(evidence["action_count"] == decisions and
                 evidence["non_pass_action_count"] == recomputed_non_pass and
                 evidence["state_change_count"] == recomputed_changes and
                 evidence["state_count"] == activity["states"] and
                 evidence_reward_delta == reward_delta and
                 evidence["non_pass_trace"] == non_pass_trace and
                 evidence["state_change_trace"] == state_change_trace,
                 "activity numeric fields and traces do not match evidence")
        _require(isinstance(seat_diag["reasons"], list) and
                 all(isinstance(reason, str) for reason in seat_diag["reasons"]),
                 "activity reasons are required")
        policy = seat_diag["policy"]
        _require(isinstance(policy, dict), "activity policy is required")
        min_non_pass_ratio = _finite_number(policy.get("min_non_pass_ratio"),
                                             "activity min_non_pass_ratio")
        _require(0.0 <= min_non_pass_ratio <= 1.0,
                 "activity min_non_pass_ratio must be between zero and one")
        max_pass_streak = policy.get("max_pass_streak")
        _require(isinstance(max_pass_streak, int) and not isinstance(max_pass_streak, bool) and
                 max_pass_streak >= 0, "activity policy max_pass_streak must be non-negative")
        min_reward_delta = policy.get("min_reward_delta")
        if min_reward_delta is not None:
            min_reward_delta = _finite_number(min_reward_delta, "activity min_reward_delta")
        _require(isinstance(policy.get("require_effective_state_change"), bool),
                 "activity require_effective_state_change must be boolean")
        expected_reasons = []
        if seat_diag["pass_only"]:
            expected_reasons.append("pass_only")
            if reward_delta == 0:
                expected_reasons.append("zero_reward_delta")
        if decisions == 0 or recomputed_non_pass / decisions < min_non_pass_ratio:
            expected_reasons.append("low_decision_coverage")
        if recomputed_max_streak > max_pass_streak:
            expected_reasons.append("excessive_pass_streak")
        if policy["require_effective_state_change"] and recomputed_changes == 0:
            expected_reasons.append("no_effective_state_change")
        if min_reward_delta is not None and reward_delta < min_reward_delta:
            expected_reasons.append("below_configured_reward_delta")
        _require(seat_diag["reasons"] == expected_reasons,
                 "activity reasons are inconsistent with diagnostics")
    expected_activity_ok = all(not seat["reasons"] for seat in seats)
    _require(activity.get("activity_ok") is expected_activity_ok and
             activity.get("ok") is (expected_completion and expected_activity_ok),
             "activity verdict is inconsistent")
    _require(game["abnormal_reason"] is None, "abnormal reason must be null for normal evidence")


def validate_external_h2h(payload: dict[str, Any], *, software_root: str | os.PathLike[str] | None = None) -> dict[str, Any]:
    """Validate a formal external H2H payload and return derived integrity counts."""
    _require(isinstance(payload, dict) and payload.get("schema_version") == SCHEMA_VERSION,
             "unsupported external H2H schema_version")
    scope = payload.get("evidence_scope")
    _require(isinstance(scope, dict) and scope.get("kind") == "external_black_box_stress" and
             scope.get("development_only") is True and scope.get("formal_promotion_eligible") is False and
             scope.get("holdout_evidence") is False, "external evidence scope cannot claim promotion or holdout")
    base = Path(software_root or Path.cwd()).resolve()
    strict = software_root is not None
    repo_root = _canonical_repo_root(base)
    canonical = _canonical_paths(repo_root)
    engine = payload.get("engine")
    _require(isinstance(engine, dict) and engine.get("name") == ENGINE_NAME and
             engine.get("version") in ENGINE_VERSIONS and engine.get("scenario") == "kaggriculture",
             "engine mismatch")
    wheel = canonical["wheel"]
    if strict:
        _require(engine.get("wheel_path") ==
                 "workspace/software/vendor/kaggle_environments-1.32.7+nodeps-py3-none-any.whl",
                 "engine wheel path must use canonical relative path")
        _require(_sha256(wheel) == engine.get("wheel_sha256"), "engine wheel SHA drift")
        try:
            with zipfile.ZipFile(wheel) as archive:
                metadata = archive.read("kaggle_environments-1.32.7+nodeps.dist-info/METADATA").decode("utf-8")
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            raise ContractError(f"cannot inspect vendored engine metadata: {exc}") from exc
        _require(re.search(r"^Name:\s*kaggle-environments\s*$", metadata, re.MULTILINE) and
                 re.search(r"^Version:\s*1\.32\.7(?:\+nodeps)?\s*$", metadata, re.MULTILINE),
                 "vendored engine metadata identity mismatch")
        attestation = engine.get("runtime_attestation")
        _require(isinstance(attestation, dict) and
                 attestation.get("matches_vendored_wheel") is True,
                 "runtime engine attestation is required")
        try:
            import kaggle_environments
            package_root = Path(kaggle_environments.__file__).resolve().parent
            members = RUNTIME_ENGINE_MEMBERS
            with zipfile.ZipFile(wheel) as archive:
                expected_files = {
                    member: hashlib.sha256(
                        archive.read(f"kaggle_environments/{member}")).hexdigest()
                    for member in members
                }
        except (OSError, KeyError, zipfile.BadZipFile) as exc:
            raise ContractError(f"cannot verify runtime engine sources: {exc}") from exc
        actual_files = {member: _sha256(package_root / member) for member in members}
        _require(attestation.get("package_root") == str(package_root) and
                 attestation.get("files") == expected_files and
                 actual_files == expected_files,
                 "runtime engine sources do not match vendored wheel")
    else:
        wheel = _resolve(engine.get("wheel_path", ""), base)
        _require(_sha256(wheel) == engine.get("wheel_sha256"), "engine wheel SHA drift")
    candidate = payload.get("candidate")
    _require(isinstance(candidate, dict), "candidate identity is required")
    for key in ("id", "path", "sha256", "role", "status", "active_candidate_contract"):
        _require(key in candidate, f"candidate missing {key}")
    candidate_path = _resolve(candidate["path"], base)
    _require(_sha256(candidate_path) == candidate["sha256"], "candidate SHA drift")
    _validate_active_candidate(candidate, base, strict=strict)
    opponents = _validate_opponents(payload.get("opponents"), base, strict=strict)
    opponent_map = {row["id"]: row for row in opponents}
    domain = payload.get("seed_domain")
    _require(isinstance(domain, dict) and isinstance(domain.get("name"), str) and domain["name"] and
             domain.get("name") != "holdout" and domain.get("holdout") is False, "invalid external seed domain")
    seeds = domain.get("seeds")
    _require(isinstance(seeds, list) and seeds and
             all(isinstance(seed, int) and not isinstance(seed, bool) for seed in seeds) and
             len(set(seeds)) == len(seeds), "external seed list must be non-empty and unique integer values")
    schedule = payload.get("schedule")
    _require(isinstance(schedule, dict) and schedule.get("policy") == "paired_ab_ba" and
             schedule.get("seat_orders") == ["AB", "BA"] and schedule.get("opponent_ids") == [row["id"] for row in opponents] and
             schedule.get("expected_games") == len(opponents) * len(seeds) * 2, "external schedule mismatch")
    games = payload.get("games")
    _require(isinstance(games, list), "games must be an array")
    seen_ids: set[str] = set()
    for game in games:
        _validate_game(game, candidate, opponent_map, set(seeds), seen_ids)
    expected_keys = {(oid, seed, seat) for oid in opponent_map for seed in seeds for seat in ("AB", "BA")}
    observed_keys = {(row["opponent_id"], row["seed"], row["seat"]) for row in games}
    _require(observed_keys == expected_keys and len(games) == len(expected_keys), "schedule missing or duplicate games")
    grouped = {}
    for row in games:
        grouped.setdefault((row["opponent_id"], row["seed"]), set()).add(row["seat"])
    for (opponent_id, seed), seats_for_seed in grouped.items():
        _require(seats_for_seed == {"AB", "BA"},
                 f"each pair and seed requires AB and BA: {opponent_id}/{seed}")
    closure = payload.get("input_closure")
    _require(isinstance(closure, dict) and closure.get("algorithm") == "sha256-path-map-v1" and
             closure.get("unchanged") is True and closure.get("before") == closure.get("after"),
             "input closure algorithm or before/after mismatch")
    if strict:
        required_paths = {canonical[key].relative_to(repo_root).as_posix()
                          for key in RUNTIME_CLOSURE_KEYS}
        required_paths.update(Path(row["path"]).as_posix() for row in opponents)
    else:
        required_paths = set(closure.get("before", {}).get("files", {}))
    for phase in ("before", "after"):
        entry = closure.get(phase)
        _require(isinstance(entry, dict) and entry.get("sha256") == _digest(entry.get("files")),
                 f"input closure {phase} hash mismatch")
        _require(set(entry.get("files", {})) == required_paths,
                 "input closure must contain the complete canonical source set")
        for filename, expected_sha in entry.get("files", {}).items():
            _require(_sha256(_resolve(filename, repo_root)) == expected_sha, f"input closure SHA drift: {filename}")
    digest = payload.get("digests")
    _require(isinstance(digest, dict) and digest.get("algorithm") == "canonical-json-sha256" and
             digest.get("canonical_payload_sha256") == canonical_external_digest(payload),
             "canonical external digest mismatch")
    command = payload.get("command")
    _require(isinstance(command, dict) and isinstance(command.get("argv"), list) and command["argv"],
             "command parameters are required")
    expected_summary = summarize_external_games(games, candidate["id"])
    _require(payload.get("summary") == expected_summary, "summary aggregate is inconsistent with games")
    return {"valid": True, "expected_games": len(expected_keys), "actual_games": len(games),
            "opponents": len(opponents), "seeds": len(seeds),
            "ab_games": sum(row["seat"] == "AB" for row in games),
            "ba_games": sum(row["seat"] == "BA" for row in games), "abnormal_games": 0}


def schema_validate_external(payload: dict[str, Any], schema_path: str | os.PathLike[str]) -> None:
    """Run the structural JSON Schema before semantic validation in the CLI."""
    try:
        import jsonschema
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
        jsonschema.validate(payload, schema, format_checker=jsonschema.FormatChecker())
    except ImportError as exc:
        raise ContractError("jsonschema is required for external schema validation") from exc
    except (OSError, ValueError) as exc:
        raise ContractError(f"cannot read external schema: {exc}") from exc
    except jsonschema.ValidationError as exc:
        raise ContractError(f"external JSON Schema validation failed: {exc.message}") from exc
