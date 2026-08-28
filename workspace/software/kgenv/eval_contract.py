"""Evaluation schedules, semantic validation, identity, and publication."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable, Iterator, Sequence

DEVELOPMENT_SEEDS = frozenset(range(101, 105))
REGRESSION_SEEDS = frozenset(range(201, 209))
KNOWN_NON_HOLDOUT_SEEDS = DEVELOPMENT_SEEDS | REGRESSION_SEEDS
SEED_DOMAINS = frozenset({"development", "regression", "holdout"})
STANDARD_MATRIX_ORDER = (
    "submission", "cow_baron", "melon_hoarder", "expansionist",
    "baseline_wheat", "greedy_carrot", "starter", "random", "pass",
)
STANDARD_OFFICIAL_PAIRS = tuple(
    (STANDARD_MATRIX_ORDER[i], STANDARD_MATRIX_ORDER[j])
    for i in range(len(STANDARD_MATRIX_ORDER))
    for j in range(i + 1, len(STANDARD_MATRIX_ORDER))
)


class ContractError(ValueError):
    """An evaluation cannot be trusted as formal evidence."""


def canonical_sha256(value: Any) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def bytes_sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: str | os.PathLike[str]) -> str:
    return bytes_sha256(Path(path).read_bytes())


def _git_value(root: Path, args: list[str]) -> str:
    return subprocess.run(["git", *args], cwd=root, capture_output=True,
                          text=True, check=True, timeout=10).stdout.strip()


def repo_state(repo_root: str | os.PathLike[str]) -> dict[str, Any]:
    root = Path(repo_root).resolve()
    try:
        return {
            "git_ref": _git_value(root, ["rev-parse", "HEAD"]),
            "dirty": bool(_git_value(root, ["status", "--porcelain"])),
        }
    except (OSError, subprocess.SubprocessError) as exc:
        raise ContractError(f"cannot capture repository identity: {exc}") from exc


def git_identity(repo_root: str | os.PathLike[str], submission_path: str | os.PathLike[str],
                 contract_input: dict[str, Any]) -> dict[str, Any]:
    path = Path(submission_path).resolve()
    state = repo_state(repo_root)
    return {
        "submission_path": str(path),
        "submission_sha256": file_sha256(path),
        **state,
        "input_sha256": canonical_sha256(contract_input),
    }


@dataclass(frozen=True)
class CandidateSnapshot:
    source_path: Path
    snapshot_path: Path
    identity: dict[str, Any]
    repo_root: Path

    def verify_unchanged(self) -> None:
        if file_sha256(self.source_path) != self.identity["submission_sha256"]:
            raise ContractError("candidate source SHA changed during evaluation")
        if file_sha256(self.snapshot_path) != self.identity["submission_sha256"]:
            raise ContractError("loaded candidate snapshot SHA mismatch")
        state = repo_state(self.repo_root)
        if state["git_ref"] != self.identity["git_ref"] or state["dirty"] != self.identity["dirty"]:
            raise ContractError("git ref/dirty state changed during evaluation")


@contextmanager
def candidate_snapshot(repo_root: str | os.PathLike[str],
                       submission_path: str | os.PathLike[str],
                       contract_input: dict[str, Any]) -> Iterator[CandidateSnapshot]:
    source = Path(submission_path).resolve()
    data = source.read_bytes()
    state = repo_state(repo_root)
    with tempfile.TemporaryDirectory(prefix="m2a_candidate_") as temp:
        snapshot_path = Path(temp) / source.name
        snapshot_path.write_bytes(data)
        identity = {
            "submission_path": str(source),
            "submission_sha256": bytes_sha256(data),
            **state,
            "input_sha256": canonical_sha256(contract_input),
        }
        snapshot = CandidateSnapshot(source, snapshot_path, identity,
                                     Path(repo_root).resolve())
        if file_sha256(snapshot_path) != identity["submission_sha256"]:
            raise ContractError("candidate snapshot write verification failed")
        yield snapshot


def validate_seed_domain(seeds: Sequence[int], seed_domain: str) -> None:
    if seed_domain not in SEED_DOMAINS:
        raise ContractError(f"unknown seed domain: {seed_domain!r}")
    if not seeds or len(set(seeds)) != len(seeds):
        raise ContractError("seed list must be non-empty and unique")
    values = {int(seed) for seed in seeds}
    if seed_domain == "development" and not values <= DEVELOPMENT_SEEDS:
        raise ContractError("development seeds must stay within 101-104")
    if seed_domain == "regression" and not values <= REGRESSION_SEEDS:
        raise ContractError("regression seeds must stay within 201-208")
    if seed_domain == "holdout" and values & KNOWN_NON_HOLDOUT_SEEDS:
        bad = sorted(values & KNOWN_NON_HOLDOUT_SEEDS)
        raise ContractError(f"holdout contains development/regression seeds: {bad}")


def build_ab_ba_schedule(pairs: Iterable[tuple[str, str]], seeds: Sequence[int],
                         seed_domain: str) -> list[dict[str, Any]]:
    validate_seed_domain(seeds, seed_domain)
    schedule: list[dict[str, Any]] = []
    for a, b in pairs:
        if not a or not b or a == b:
            raise ContractError(f"invalid pair: {(a, b)!r}")
        for seed in seeds:
            schedule.append({"a": a, "b": b, "p0": a, "p1": b,
                             "seed": int(seed), "seat": "AB",
                             "seed_domain": seed_domain})
            schedule.append({"a": a, "b": b, "p0": b, "p1": a,
                             "seed": int(seed), "seat": "BA",
                             "seed_domain": seed_domain})
    return schedule


def game_abnormal_reason(game: dict[str, Any], *, require_export_fields: bool = False,
                         expected_domain: str | None = None,
                         allowed_seeds: set[int] | None = None) -> str | None:
    required = ["players", "seed", "seat", "seed_domain", "statuses",
                "contract_ok", "winner_label", "rewards"]
    if require_export_fields:
        required.extend(["p0", "p1", "winner", "turns"])
    missing = [key for key in required if key not in game]
    if missing:
        return f"missing required game fields: {missing}"
    players = game["players"]
    if not isinstance(players, list) or len(players) != 2 or players[0] == players[1]:
        return f"invalid players {players!r}"
    if require_export_fields and [game["p0"], game["p1"]] != players:
        return "players do not match p0/p1"
    if game["seat"] not in ("AB", "BA"):
        return f"invalid seat {game['seat']!r}"
    if game["statuses"] != ["DONE", "DONE"]:
        return f"non-DONE statuses {game['statuses']!r}"
    if game["contract_ok"] is not True:
        return "contract_ok is not true"
    rewards = game["rewards"]
    if (not isinstance(rewards, list) or len(rewards) != 2 or
            any(not isinstance(value, (int, float)) for value in rewards)):
        return f"invalid rewards {rewards!r}"
    expected_winner = (players[0] if rewards[0] > rewards[1] else
                       players[1] if rewards[1] > rewards[0] else None)
    if game["winner_label"] != expected_winner:
        return "winner_label is inconsistent with players/rewards"
    if require_export_fields and game["winner"] != expected_winner:
        return "winner is inconsistent with winner_label/rewards"
    if expected_winner is None and rewards[0] != rewards[1]:
        return "tie requires equal rewards"
    if expected_domain is not None and game["seed_domain"] != expected_domain:
        return "game seed_domain differs from top-level seed_domain"
    if allowed_seeds is not None and game["seed"] not in allowed_seeds:
        return "game seed is outside configured seed set"
    return None


def assert_games_normal(games: Sequence[dict[str, Any]], *, require_export_fields=False,
                        expected_domain=None, allowed_seeds=None) -> None:
    for index, game in enumerate(games):
        reason = game_abnormal_reason(
            game, require_export_fields=require_export_fields,
            expected_domain=expected_domain, allowed_seeds=allowed_seeds)
        if reason:
            raise ContractError(f"abnormal game {index}: {reason}")


def _observed_schedule(games: Sequence[dict[str, Any]]) -> list[tuple[str, str, int, str]]:
    return [(str(game["players"][0]), str(game["players"][1]),
             int(game["seed"]), str(game["seat"])) for game in games]


def validate_gate_run(games: Sequence[dict[str, Any]], opponents: Sequence[str],
                      seeds: Sequence[int], require_complete: bool,
                      required_opponents: Sequence[str] | None = None) -> dict[str, Any]:
    validate_seed_domain(seeds, "development")
    assert_games_normal(games, expected_domain="development",
                        allowed_seeds=set(seeds))
    required = list(required_opponents or (
        "cow_baron", "melon_hoarder", "expansionist", "baseline_wheat"))
    selected = list(opponents)
    if require_complete and list(seeds) != sorted(DEVELOPMENT_SEEDS):
        raise ContractError("complete gate requires all development seeds 101-104")
    if require_complete and selected != required:
        raise ContractError(f"complete gate requires opponents {required}, got {selected}")
    formal = require_complete and selected == required
    schedule = build_ab_ba_schedule([("cand", name) for name in selected],
                                    seeds, "development")
    expected = [(item["p0"], item["p1"], item["seed"], item["seat"])
                for item in schedule]
    observed = _observed_schedule(games)
    if observed != expected:
        raise ContractError(f"gate schedule mismatch: expected {len(expected)} games, "
                            f"observed {len(observed)}")
    return {"mode": "official" if formal else "exploratory", "complete": formal,
            "formal_pass": formal, "expected_games": len(expected),
            "actual_games": len(observed), "abnormal_games": 0}


def order_independent_standings(games: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    assert_games_normal(games)
    records: dict[str, dict[str, int]] = {}
    for game in games:
        players = game["players"]
        winner = game["winner_label"]
        for name in players:
            records.setdefault(name, {"W": 0, "L": 0, "T": 0})
        if winner is None:
            records[players[0]]["T"] += 1
            records[players[1]]["T"] += 1
        else:
            loser = players[1] if winner == players[0] else players[0]
            records[winner]["W"] += 1
            records[loser]["L"] += 1
    rows = []
    for name, record in records.items():
        count = sum(record.values())
        rate = (record["W"] + 0.5 * record["T"]) / count if count else None
        rows.append({"name": name, "games": count, "record": record,
                     "score_rate": round(rate, 6) if rate is not None else None})
    rows.sort(key=lambda row: (-(row["score_rate"] or 0.0), row["name"]))
    return rows


def _official_schedule() -> list[dict[str, Any]]:
    return build_ab_ba_schedule(STANDARD_OFFICIAL_PAIRS, sorted(DEVELOPMENT_SEEDS), "development")


def _canonical_official_input() -> dict[str, Any]:
    return {
        "pairs": [list(pair) for pair in STANDARD_OFFICIAL_PAIRS],
        "seeds": sorted(DEVELOPMENT_SEEDS),
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
        "episode_steps": 720,
        "run_kind": "official",
    }


def validate_eval_result(payload: dict[str, Any], require_official: bool = False) -> dict[str, Any]:
    if payload.get("schema_version") != "2.0":
        raise ContractError("semantic validation requires schema_version 2.0")
    if require_official and payload.get("run_kind") != "official":
        raise ContractError("formal export must have run_kind=official")
    seed_domain = payload.get("seed_domain")
    evaluation_input = payload.get("evaluation_input")
    config = payload.get("config")
    identity = payload.get("identity")
    if not all(isinstance(value, dict) for value in (evaluation_input, config, identity)):
        raise ContractError("evaluation_input, config, and identity are required objects")
    seeds = evaluation_input.get("seeds")
    validate_seed_domain(seeds or [], seed_domain)
    if config.get("seeds") != seeds:
        raise ContractError("config.seeds must equal evaluation_input.seeds")
    if config.get("pairs") != evaluation_input.get("pairs"):
        raise ContractError("config.pairs must equal evaluation_input.pairs")
    if config.get("seat_orders") != evaluation_input.get("seat_orders"):
        raise ContractError("config.seat_orders must equal evaluation_input.seat_orders")
    if identity.get("input_sha256") != canonical_sha256(evaluation_input):
        raise ContractError("identity input_sha256 does not match evaluation_input")
    if not isinstance(identity.get("submission_sha256"), str) or len(identity["submission_sha256"]) != 64:
        raise ContractError("identity submission_sha256 must be a SHA-256 digest")
    if not identity.get("git_ref") or not isinstance(identity.get("dirty"), bool):
        raise ContractError("identity git_ref and dirty are required")
    if evaluation_input.get("seed_domain") != seed_domain:
        raise ContractError("evaluation_input seed_domain mismatch")
    if evaluation_input.get("seat_orders") != ["AB", "BA"]:
        raise ContractError("evaluation requires AB/BA seat orders")

    if require_official:
        canonical = _canonical_official_input()
        if evaluation_input != canonical:
            raise ContractError("official evaluation must use the standard full matrix and seeds 101-104")
        if config.get("matrix_order") != list(STANDARD_MATRIX_ORDER):
            raise ContractError("official config.matrix_order is not canonical")
        regression = payload.get("regression_gate")
        if not isinstance(regression, dict) or regression.get("ok") is not True:
            raise ContractError("official export requires a passing regression_gate")

    pairs = [tuple(pair) for pair in evaluation_input.get("pairs", [])]
    if not pairs:
        raise ContractError("evaluation pairs are required")
    schedule = build_ab_ba_schedule(pairs, seeds, seed_domain)
    games = payload.get("games")
    if not isinstance(games, list):
        raise ContractError("games must be an array")
    assert_games_normal(games, require_export_fields=True,
                        expected_domain=seed_domain, allowed_seeds=set(seeds))
    expected = [(item["p0"], item["p1"], item["seed"], item["seat"])
                for item in schedule]
    if _observed_schedule(games) != expected:
        raise ContractError(f"official schedule mismatch: expected {len(expected)}, "
                            f"observed {len(games)}")
    if config.get("expected_games") != len(expected):
        raise ContractError("config expected_games does not match pair x seed x AB/BA")
    integrity = payload.get("integrity")
    if not isinstance(integrity, dict):
        raise ContractError("integrity is required")
    expected_integrity = {"expected_games": len(expected), "actual_games": len(games),
                          "abnormal_games": 0}
    if any(integrity.get(key) != value for key, value in expected_integrity.items()):
        raise ContractError("integrity totals do not match evaluated games")

    summaries = {row.get("pair"): row for row in payload.get("head_to_head", [])}
    for a, b in pairs:
        selected = [game for game in games if {game["p0"], game["p1"]} == {a, b}]
        wins = sum(game["winner"] == a for game in selected)
        losses = sum(game["winner"] == b for game in selected)
        ties = sum(game["winner"] is None for game in selected)
        row = summaries.get(f"{a} vs {b}")
        totals = () if row is None else (row.get("games"), row.get("wins"),
                                         row.get("losses"), row.get("ties"))
        if totals != (len(selected), wins, losses, ties):
            raise ContractError(f"head_to_head totals mismatch for {a} vs {b}")
        expected_rate = round((wins + 0.5 * ties) / len(selected), 4)
        if row.get("win_rate") != expected_rate:
            raise ContractError(f"head_to_head win_rate mismatch for {a} vs {b}")
    confirmatory = payload.get("confirmatory")
    if not isinstance(confirmatory, dict) or confirmatory.get("order_independent") is not True:
        raise ContractError("confirmatory order-independent statistic is required")
    elo = payload.get("elo") or {}
    if elo.get("role") != "descriptive_only" or elo.get("order_sensitive") is not True:
        raise ContractError("Elo must be explicitly descriptive and order-sensitive")
    return {**expected_integrity, "valid": True}


def _same_path(left: Path, right: Path) -> bool:
    left, right = left.resolve(), right.resolve()
    if left.exists() and right.exists():
        try:
            return os.path.samefile(left, right)
        except OSError:
            pass
    return os.path.normcase(str(left)) == os.path.normcase(str(right))


def resolve_output_path(official: bool, requested: str,
                        exports_dir: str | os.PathLike[str]) -> str:
    exports = Path(exports_dir).resolve()
    formal = exports / "eval_results.json"
    target = Path(requested).resolve() if requested else (
        formal if official else exports / "eval_results.dev.json")
    if not official and _same_path(target, formal):
        raise ContractError("development runs cannot target the formal eval export")
    if official and not _same_path(target, formal):
        raise ContractError("official runs must target exports/eval_results.json")
    return str(target)


def atomic_publish_json(target: str | os.PathLike[str], payload: dict[str, Any],
                        validator: Callable[[dict[str, Any]], Any]) -> None:
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    atomic_publish_bundle([(Path(target), data)], lambda: validator(payload))


def atomic_publish_bundle(items: Sequence[tuple[Path, bytes]],
                          validator: Callable[[], Any]) -> None:
    """Stage, validate, and replace a group with backup-based rollback."""
    staged: list[tuple[Path, Path]] = []
    backups: dict[Path, Path | None] = {}
    replaced: list[Path] = []
    try:
        for target, data in items:
            target = Path(target).resolve()
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile("wb", suffix=".tmp",
                                             prefix=f".{target.name}.",
                                             dir=target.parent, delete=False) as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
                staged.append((target, Path(stream.name)))
        validator()
        for target, _ in staged:
            if target.exists():
                backup = target.with_name(f".{target.name}.{os.getpid()}.bak")
                shutil.copy2(target, backup)
                backups[target] = backup
            else:
                backups[target] = None
        for target, temp_path in staged:
            os.replace(temp_path, target)
            replaced.append(target)
        staged.clear()
    except Exception:
        for target in reversed(replaced):
            backup = backups.get(target)
            if backup is None:
                target.unlink(missing_ok=True)
            elif backup.exists():
                os.replace(backup, target)
                backups[target] = None
        raise
    finally:
        for _, temp_path in staged:
            temp_path.unlink(missing_ok=True)
        for backup in backups.values():
            if backup is not None:
                backup.unlink(missing_ok=True)
