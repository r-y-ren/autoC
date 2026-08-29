"""One-time holdout state, statistics, validation, and metrics projection."""

from __future__ import annotations

import hashlib
import json
import math
import os
import secrets
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence

from .eval_contract import (
    ContractError,
    STANDARD_MATRIX_ORDER,
    STANDARD_OFFICIAL_PAIRS,
    assert_games_normal,
    build_ab_ba_schedule,
    canonical_sha256,
    file_sha256,
)
from .variance import wilson_ci

HOLDOUT_SCHEMA_VERSION = "2.0"
HOLDOUT_SEED_COUNT = 8
HOLDOUT_EXPECTED_GAMES = 576
HOLDOUT_EXPECTED_SEATS = 288
CANDIDATE_EXPECTED_GAMES = 128
HISTORICAL_SEEDS = frozenset(
    {1, 2, 3, 7, 8, 9, 42}
    | set(range(101, 105))
    | set(range(201, 209))
    | set(range(601, 605))
    | set(range(701, 705))
)
# Attempt 2 (campaign III m4-holdout-v2) forbids every previously published
# or observed seed on top of the development/regression domains:
#  - the 8 holdout seeds published by attempt 1 (eval_results.json 92.9% run)
#  - the 3 seeds of real online public episodes (round-1 ledger)
PUBLISHED_HOLDOUT_SEEDS_V1 = frozenset({
    1434909129, 415651673, 68483508, 141000100,
    801695889, 291593029, 1616180299, 1369595171,
})
ONLINE_EPISODE_SEEDS = frozenset({1957338404, 912426123, 771861982})
HISTORICAL_SEEDS_V2 = frozenset(
    HISTORICAL_SEEDS | PUBLISHED_HOLDOUT_SEEDS_V1 | ONLINE_EPISODE_SEEDS
)
assert len(HISTORICAL_SEEDS_V2) == 38
PUBLISHED_HOLDOUT_ATTEMPT_V1_ID = "41c7771a63b90d3e66cb40c7"
HOLDOUT_V2_MATRIX_ORDER = (
    "submission", "cow_baron", "melon_hoarder", "expansionist",
    "baseline_wheat", "crop_rotator", "template_wheat",
    "self_feed_ranch", "near_band_diversified",
)
HOLDOUT_V2_OFFICIAL_PAIRS = tuple(
    (HOLDOUT_V2_MATRIX_ORDER[i], HOLDOUT_V2_MATRIX_ORDER[j])
    for i in range(len(HOLDOUT_V2_MATRIX_ORDER))
    for j in range(i + 1, len(HOLDOUT_V2_MATRIX_ORDER))
)


def holdout_matrix_order(attempt_index: int) -> tuple[str, ...]:
    """Canonical full-pool matrix order for a holdout attempt generation."""
    if attempt_index == 1:
        return STANDARD_MATRIX_ORDER
    if attempt_index == 2:
        return HOLDOUT_V2_MATRIX_ORDER
    raise ContractError(f"unknown holdout attempt generation: {attempt_index!r}")


def holdout_official_pairs(attempt_index: int) -> tuple[tuple[str, str], ...]:
    if attempt_index == 1:
        return STANDARD_OFFICIAL_PAIRS
    if attempt_index == 2:
        return HOLDOUT_V2_OFFICIAL_PAIRS
    raise ContractError(f"unknown holdout attempt generation: {attempt_index!r}")


def historical_seeds(attempt_index: int) -> frozenset[int]:
    """Every seed that a fresh attempt generation must exclude."""
    if attempt_index == 1:
        return HISTORICAL_SEEDS
    if attempt_index == 2:
        return HISTORICAL_SEEDS_V2
    raise ContractError(f"unknown holdout attempt generation: {attempt_index!r}")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write_json(path: Path, payload: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    data = (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with tempfile.NamedTemporaryFile(
        "wb", suffix=".tmp", prefix=f".{path.name}.", dir=path.parent, delete=False
    ) as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
        staged = Path(stream.name)
    try:
        os.replace(staged, path)
    finally:
        staged.unlink(missing_ok=True)


def generate_holdout_seeds(
    randbelow: Callable[[int], int] | None = None,
    *,
    count: int = HOLDOUT_SEED_COUNT,
    excluded: Iterable[int] = HISTORICAL_SEEDS_V2,
) -> list[int]:
    """Generate opaque, unique positive seeds outside every prior evidence domain."""
    draw = randbelow or secrets.randbelow
    forbidden = {int(value) for value in excluded}
    result: list[int] = []
    while len(result) < count:
        value = 10_000 + int(draw(2_000_000_000 - 10_000))
        if value not in forbidden and value not in result:
            result.append(value)
    return result


def validate_holdout_seeds(seeds: Sequence[int], *, attempt_index: int = 2) -> None:
    if len(seeds) != HOLDOUT_SEED_COUNT or len(set(seeds)) != HOLDOUT_SEED_COUNT:
        raise ContractError("holdout requires exactly 8 unique seeds")
    if any(not isinstance(seed, int) or seed <= 0 for seed in seeds):
        raise ContractError("holdout seeds must be positive integers")
    overlap = sorted(set(seeds) & historical_seeds(attempt_index))
    if overlap:
        raise ContractError(f"holdout seeds overlap historical evidence: {overlap}")


def canonical_holdout_pairs(*, attempt_index: int = 2) -> list[list[str]]:
    return [list(pair) for pair in holdout_official_pairs(attempt_index)]


def canonical_holdout_schedule(seeds: Sequence[int], *, attempt_index: int = 2) -> list[dict[str, Any]]:
    validate_holdout_seeds(seeds, attempt_index=attempt_index)
    return build_ab_ba_schedule(holdout_official_pairs(attempt_index), seeds, "holdout")


def hash_input_closure(root: Path, relative_paths: Sequence[str]) -> dict[str, Any]:
    files: dict[str, str] = {}
    for relative in sorted(set(relative_paths)):
        path = (Path(root) / relative).resolve()
        if not path.is_file():
            raise ContractError(f"holdout input-closure file missing: {relative}")
        files[relative.replace("\\", "/")] = file_sha256(path)
    return {"files": files, "sha256": canonical_sha256(files)}


def create_or_load_attempt(
    state_path: Path,
    *,
    candidate_sha256: str,
    frozen_manifest_sha256: str,
    evaluator_closure: dict[str, Any],
    attempt_index: int = 2,
    randbelow: Callable[[int], int] | None = None,
    now: Callable[[], str] = utc_now,
) -> tuple[dict[str, Any], bool]:
    """Create durable attempt metadata before drawing seeds, or resume it exactly."""
    state_path = Path(state_path)
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        if state.get("status") in {"published", "invalidated"}:
            raise ContractError(f"holdout attempt is already {state['status']}")
        if state.get("status") not in {"running"}:
            if state.get("status") == "allocating":
                state.update(
                    status="invalidated",
                    invalidated_at=now(),
                    invalidation_reason=(
                        "seed allocation was interrupted; entropy outcome is unknown"
                    ),
                )
                atomic_write_json(state_path, state)
                raise ContractError(
                    "holdout seed allocation was interrupted; attempt is consumed and seeds must not be redrawn"
                )
            raise ContractError("persisted holdout attempt has an invalid status")
        if state.get("attempt_index", 2) != attempt_index:
            raise ContractError("persisted holdout attempt belongs to another generation")
        if state.get("candidate_sha256") != candidate_sha256:
            raise ContractError("persisted holdout candidate does not match frozen candidate")
        if state.get("frozen_manifest_sha256") != frozen_manifest_sha256:
            raise ContractError("persisted frozen manifest identity changed")
        if state.get("evaluator_closure") != evaluator_closure:
            raise ContractError("persisted evaluator input closure changed")
        validate_holdout_seeds(state.get("seeds") or [], attempt_index=attempt_index)
        return state, False

    created_at = now()
    attempt_id = canonical_sha256(
        {
            "attempt_index": attempt_index,
            "candidate_sha256": candidate_sha256,
            "frozen_manifest_sha256": frozen_manifest_sha256,
            "evaluator_closure_sha256": evaluator_closure.get("sha256"),
            "created_at": created_at,
        }
    )[:24]
    if attempt_index == 2 and attempt_id == PUBLISHED_HOLDOUT_ATTEMPT_V1_ID:
        raise ContractError("attempt id collision with the published attempt 1 id")
    state = {
        "schema_version": "1.0",
        "attempt_id": attempt_id,
        "attempt_index": attempt_index,
        "status": "allocating",
        "created_at": created_at,
        "candidate_sha256": candidate_sha256,
        "frozen_manifest_sha256": frozen_manifest_sha256,
        "evaluator_closure": evaluator_closure,
        "seeds": None,
        "completed_games": 0,
    }
    atomic_write_json(state_path, state)
    seeds = generate_holdout_seeds(randbelow, excluded=historical_seeds(attempt_index))
    state.update(
        status="running",
        seeds=seeds,
        seed_manifest_sha256=canonical_sha256(seeds),
        schedule_sha256=canonical_sha256(
            canonical_holdout_schedule(seeds, attempt_index=attempt_index)
        ),
        started_at=now(),
    )
    atomic_write_json(state_path, state)
    return state, True


def invalidate_attempt(state_path: Path, reason: str) -> dict[str, Any]:
    state = json.loads(Path(state_path).read_text(encoding="utf-8"))
    state.update(status="invalidated", invalidated_at=utc_now(), invalidation_reason=reason)
    atomic_write_json(Path(state_path), state)
    return state


def _score(game: dict[str, Any], name: str) -> float:
    if game["winner"] == name:
        return 1.0
    if game["winner"] is None:
        return 0.5
    return 0.0


def _record(games: Sequence[dict[str, Any]], name: str) -> dict[str, int]:
    return {
        "W": sum(game["winner"] == name for game in games),
        "L": sum(game["winner"] not in (None, name) for game in games),
        "T": sum(game["winner"] is None for game in games),
    }


def _record_row(games: Sequence[dict[str, Any]], name: str) -> dict[str, Any]:
    record = _record(games, name)
    count = len(games)
    score = record["W"] + 0.5 * record["T"]
    lo, hi = wilson_ci(score, count)
    return {
        "games": count,
        "W": record["W"],
        "L": record["L"],
        "T": record["T"],
        "score_rate": round(score / count, 6) if count else None,
        "wilson95": [lo, hi] if lo is not None else None,
    }


def candidate_confirmatory(games: Sequence[dict[str, Any]],
                           opponents: Sequence[str]) -> dict[str, Any]:
    """Order-independent candidate W/L/T and paired AB/BA score statistic."""
    selected = [game for game in games if "submission" in game["players"]]
    opponents = list(opponents)
    overall = _record_row(selected, "submission")
    pair_records = []
    seat_records: dict[str, Any] = {}
    paired_units = []
    for opponent in opponents:
        pair_games = [game for game in selected if opponent in game["players"]]
        pair_records.append({"opponent": opponent, **_record_row(pair_games, "submission")})
        for seed in sorted({game["seed"] for game in pair_games}):
            unit = [game for game in pair_games if game["seed"] == seed]
            if len(unit) != 2 or {game["seat"] for game in unit} != {"AB", "BA"}:
                raise ContractError(f"candidate pair {opponent} seed {seed} lacks AB/BA mirror")
            paired_units.append(
                {"opponent": opponent, "seed": seed,
                 "score": sum(_score(game, "submission") for game in unit) / 2.0}
            )
    for seat in ("AB", "BA"):
        seat_games = [game for game in selected if game["seat"] == seat]
        seat_records[seat] = {
            **_record_row(seat_games, "submission"),
            "by_opponent": {
                opponent: _record_row(
                    [game for game in seat_games if opponent in game["players"]],
                    "submission",
                )
                for opponent in opponents
            },
        }

    values = [unit["score"] for unit in paired_units]
    n = len(values)
    estimate = sum(values) / n if n else None
    if n > 1:
        variance = sum((value - estimate) ** 2 for value in values) / (n - 1)
        half = 1.998 * math.sqrt(variance / n)
        interval = [round(max(0.0, estimate - half), 6),
                    round(min(1.0, estimate + half), 6)]
    else:
        interval = None
    statistic = {
        "method": "mean per-(opponent,seed) AB/BA score; Student-t 95% CI",
        "order_independent": True,
        "tie_policy": "tie=0.5 game score",
        "unit_count": n,
        "estimate": round(estimate, 6) if estimate is not None else None,
        "ci95": interval,
        "input_sha256": canonical_sha256(paired_units),
        "fit_status": "ok" if n == 64 else "invalid",
    }
    return {
        "overall_record": overall,
        "pair_records": pair_records,
        "seat_records": seat_records,
        "wilson_intervals": {
            "confidence": 0.95,
            "method": "Wilson score; tie=0.5",
            "overall": overall["wilson95"],
            "pairs": {row["opponent"]: row["wilson95"] for row in pair_records},
        },
        "order_independent_statistic": statistic,
    }


def validate_holdout_payload(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != HOLDOUT_SCHEMA_VERSION:
        raise ContractError("holdout semantic validation requires schema 2.0")
    if payload.get("run_kind") != "official_holdout" or payload.get("seed_domain") != "holdout":
        raise ContractError("formal holdout requires run_kind=official_holdout and holdout domain")
    attempt = payload.get("holdout", {}).get("attempt") or {}
    attempt_index = attempt.get("index")
    matrix_order = holdout_matrix_order(attempt_index)
    expected_pairs = [list(pair) for pair in holdout_official_pairs(attempt_index)]
    forbidden_seeds = historical_seeds(attempt_index)
    evaluation = payload.get("evaluation_input") or {}
    seeds = evaluation.get("seeds") or []
    validate_holdout_seeds(seeds, attempt_index=attempt_index)
    if evaluation.get("pairs") != expected_pairs:
        raise ContractError("holdout requires the canonical 36-pair full matrix")
    if evaluation.get("seat_orders") != ["AB", "BA"]:
        raise ContractError("holdout requires AB/BA seats")
    if evaluation.get("run_kind") != "official_holdout":
        raise ContractError("holdout evaluation input run kind mismatch")
    schedule = canonical_holdout_schedule(seeds, attempt_index=attempt_index)
    if len(schedule) != HOLDOUT_EXPECTED_GAMES:
        raise ContractError("holdout schedule must contain 576 games")
    config = payload.get("config") or {}
    if config.get("seeds") != seeds or config.get("pairs") != evaluation.get("pairs"):
        raise ContractError("holdout config seeds/pairs differ from evaluation input")
    if config.get("seat_orders") != ["AB", "BA"] or config.get("rounds") != 8:
        raise ContractError("holdout config rounds/seats are not canonical")
    if config.get("matrix_order") != list(matrix_order):
        raise ContractError("holdout matrix order is not canonical")
    if config.get("expected_games") != HOLDOUT_EXPECTED_GAMES:
        raise ContractError("holdout config expected game count is not 576")
    if payload.get("opponent_pool_names") != list(matrix_order[1:]):
        raise ContractError("holdout opponent pool is not canonical")

    identity = payload.get("identity") or {}
    holdout = payload.get("holdout") or {}
    frozen = holdout.get("frozen_candidate") or {}
    if identity.get("submission_sha256") != frozen.get("sha256"):
        raise ContractError("holdout candidate SHA does not match frozen candidate")
    if identity.get("input_sha256") != canonical_sha256(evaluation):
        raise ContractError("holdout evaluation input hash mismatch")
    closure = holdout.get("input_closure") or {}
    if closure.get("before") != closure.get("after"):
        raise ContractError("holdout evaluator input closure changed during run")
    before = closure.get("before") or {}
    repository = before.get("repository") or {}
    runtime_engine = before.get("runtime_engine") or {}
    if repository.get("sha256") != canonical_sha256(repository.get("files") or {}):
        raise ContractError("holdout repository closure digest mismatch")
    runtime_body = {key: value for key, value in runtime_engine.items() if key != "sha256"}
    if runtime_engine.get("sha256") != canonical_sha256(runtime_body):
        raise ContractError("holdout runtime-engine closure digest mismatch")
    closure_body = {key: value for key, value in before.items() if key != "sha256"}
    digest = canonical_sha256(closure_body)
    if before.get("sha256") != digest or closure.get("sha256") != digest:
        raise ContractError("holdout evaluator closure digest mismatch")
    protocol = holdout.get("protocol") or {}
    expected_protocol = {
        "full_matrix": True,
        "seed_count": HOLDOUT_SEED_COUNT,
        "seat_orders": ["AB", "BA"],
        "one_time": True,
        "resume_exact_attempt_only": True,
        "candidate_change_invalidates": True,
        "candidate_source": "frozen_git_blob",
    }
    if attempt_index == 2:
        expected_protocol["historical_seed_exclusion_count"] = len(HISTORICAL_SEEDS_V2)
    if protocol != expected_protocol:
        raise ContractError("holdout protocol differs from the preregistered contract")
    engine = payload.get("engine") or {}
    if (
        runtime_engine.get("wheel_match") is not True
        or runtime_engine.get("distribution_version") != engine.get("version")
        or engine.get("scenario") != "kaggriculture"
        or engine.get("episode_steps") != 720
    ):
        raise ContractError("holdout engine claim differs from the verified runtime closure")
    if (
        attempt.get("index") not in (1, 2)
        or attempt.get("status") != "published"
        or attempt.get("published") is not True
        or attempt.get("invalidated") is not False
        or attempt.get("invalidation_reason") is not None
    ):
        raise ContractError("holdout must be a single valid published attempt")
    if (
        attempt_index == 2
        and attempt.get("attempt_id") == PUBLISHED_HOLDOUT_ATTEMPT_V1_ID
    ):
        raise ContractError("attempt 2 must not reuse the published attempt 1 id")
    hash_match = holdout.get("candidate_hash_match") or {}
    expected_sha = frozen.get("sha256")
    if (
        hash_match.get("pass") is not True
        or hash_match.get("frozen") != expected_sha
        or hash_match.get("before") != expected_sha
        or hash_match.get("after") != expected_sha
    ):
        raise ContractError("holdout candidate hash-match claim is inconsistent")
    isolation = holdout.get("seed_domain_isolation") or {}
    if (
        isolation.get("pass") is not True
        or isolation.get("overlap_count") != 0
        or isolation.get("historical_count") != len(forbidden_seeds)
    ):
        raise ContractError("holdout seed-domain isolation did not pass")
    seed_manifest = holdout.get("seed_manifest") or {}
    if seed_manifest.get("attempt_id") != attempt.get("attempt_id"):
        raise ContractError("public seed manifest attempt differs from holdout attempt")
    if seed_manifest.get("seeds") != seeds:
        raise ContractError("public seed manifest differs from evaluated seeds")
    if seed_manifest.get("sha256") != canonical_sha256(seeds):
        raise ContractError("public seed manifest hash mismatch")
    if (
        attempt_index == 2
        and seed_manifest.get("historical_seed_exclusion_count") != len(HISTORICAL_SEEDS_V2)
    ):
        raise ContractError("public seed manifest exclusion registry must list 38 seeds")

    games = payload.get("games")
    if not isinstance(games, list):
        raise ContractError("holdout games must be an array")
    assert_games_normal(
        games, require_export_fields=True, expected_domain="holdout", allowed_seeds=set(seeds)
    )
    expected = [(item["p0"], item["p1"], item["seed"], item["seat"]) for item in schedule]
    observed = [(game["p0"], game["p1"], game["seed"], game["seat"]) for game in games]
    if observed != expected:
        raise ContractError(f"holdout schedule mismatch: expected 576, observed {len(games)}")
    integrity = payload.get("integrity") or {}
    expected_integrity = {
        "expected_games": HOLDOUT_EXPECTED_GAMES,
        "actual_games": HOLDOUT_EXPECTED_GAMES,
        "abnormal_games": 0,
        "ab_games": HOLDOUT_EXPECTED_SEATS,
        "ba_games": HOLDOUT_EXPECTED_SEATS,
        "missing_mirrors": 0,
    }
    if any(integrity.get(key) != value for key, value in expected_integrity.items()):
        raise ContractError("holdout integrity totals are inconsistent")

    calculated = candidate_confirmatory(games, list(matrix_order[1:]))
    confirmatory = payload.get("confirmatory") or {}
    for key, value in calculated.items():
        if confirmatory.get(key) != value:
            raise ContractError(f"holdout confirmatory {key} is inconsistent with games")
    if calculated["overall_record"]["games"] != CANDIDATE_EXPECTED_GAMES:
        raise ContractError("candidate must have 128 holdout games")
    if calculated["order_independent_statistic"]["fit_status"] != "ok":
        raise ContractError("paired holdout statistic is incomplete")
    return {**expected_integrity, "candidate_games": CANDIDATE_EXPECTED_GAMES, "valid": True}


def project_holdout_metrics(payload: dict[str, Any], export_sha256: str,
                            *, prefix: str = "m4_") -> dict[str, Any]:
    """Project a validated holdout export into shard metrics keys.

    Attempt 1 projected to the legacy ``holdout_*``/``confirmatory_*`` names;
    attempt 2 (m4-holdout-v2) projects to ``m4_*`` per
    workspace/docs/metrics-keys-r3.md while the legacy keys stay frozen as
    historical evidence of the 92.9% run.
    """
    validate_holdout_payload(payload)
    holdout = payload["holdout"]
    confirmatory = payload["confirmatory"]
    trace = {
        "export_sha256": export_sha256,
        "source": "workspace/software/exports/eval_results.json",
        "validated_schema": HOLDOUT_SCHEMA_VERSION,
    }
    values = {
        f"{prefix}holdout_protocol": holdout["protocol"],
        f"{prefix}holdout_seed_manifest": holdout["seed_manifest"],
        f"{prefix}holdout_candidate_hash_match": holdout["candidate_hash_match"],
        f"{prefix}holdout_seed_domain_isolation": holdout["seed_domain_isolation"],
        f"{prefix}holdout_run_status": holdout["attempt"],
        f"{prefix}holdout_schedule": {key: payload["integrity"][key] for key in ("expected_games", "actual_games")},
        f"{prefix}holdout_seat_split": {key: payload["integrity"][key] for key in ("ab_games", "ba_games", "missing_mirrors")},
        f"{prefix}holdout_abnormal_summary": {"abnormal_games": payload["integrity"]["abnormal_games"]},
        f"{prefix}holdout_integrity_pass": True,
        f"{prefix}confirmatory_overall_record": confirmatory["overall_record"],
        f"{prefix}confirmatory_pair_records": confirmatory["pair_records"],
        f"{prefix}confirmatory_seat_records": confirmatory["seat_records"],
        f"{prefix}confirmatory_wilson_intervals": confirmatory["wilson_intervals"],
        f"{prefix}confirmatory_order_independent_statistics": confirmatory["order_independent_statistic"],
        f"{prefix}confirmatory_elo_appendix": payload["elo"],
    }
    pointers = {
        f"{prefix}holdout_protocol": "/holdout/protocol",
        f"{prefix}holdout_seed_manifest": "/holdout/seed_manifest",
        f"{prefix}holdout_candidate_hash_match": "/holdout/candidate_hash_match",
        f"{prefix}holdout_seed_domain_isolation": "/holdout/seed_domain_isolation",
        f"{prefix}holdout_run_status": "/holdout/attempt",
        f"{prefix}holdout_schedule": "/integrity",
        f"{prefix}holdout_seat_split": "/integrity",
        f"{prefix}holdout_abnormal_summary": "/integrity/abnormal_games",
        f"{prefix}holdout_integrity_pass": "/integrity",
        f"{prefix}confirmatory_overall_record": "/confirmatory/overall_record",
        f"{prefix}confirmatory_pair_records": "/confirmatory/pair_records",
        f"{prefix}confirmatory_seat_records": "/confirmatory/seat_records",
        f"{prefix}confirmatory_wilson_intervals": "/confirmatory/wilson_intervals",
        f"{prefix}confirmatory_order_independent_statistics": "/confirmatory/order_independent_statistic",
        f"{prefix}confirmatory_elo_appendix": "/elo",
    }
    values[f"{prefix}confirmatory_export_traceability"] = {**trace, "json_pointers": pointers}
    return {
        key: {"value": value, "unit": "holdout-evidence", "method": f"{trace['source']}#{pointers.get(key, '/confirmatory_export_traceability')}"}
        for key, value in values.items()
    }
