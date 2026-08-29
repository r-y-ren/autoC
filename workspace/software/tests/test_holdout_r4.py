"""Attempt-3 (r3-3 r4-holdout) contract tests; no real games.

Covers the 10-agent matrix, the 46-seed historical exclusion registry
(cross-verified against the attempt-2 published artifact), and the r4_
metrics projection for the 720-game one-time holdout of candidate 9298751f.
"""

from __future__ import annotations

import json

import pytest

from kgenv.eval_contract import ContractError, canonical_sha256
from kgenv.holdout_contract import (
    HISTORICAL_SEEDS_V2,
    HISTORICAL_SEEDS_V3,
    HOLDOUT_V3_MATRIX_ORDER,
    PUBLISHED_HOLDOUT_ATTEMPT_V2_ID,
    PUBLISHED_HOLDOUT_SEEDS_V2,
    attempt_metrics_prefix,
    candidate_confirmatory,
    canonical_holdout_pairs,
    canonical_holdout_schedule,
    candidate_expected_games,
    candidate_paired_units,
    holdout_expected_games,
    holdout_expected_seats,
    holdout_matrix_order,
    historical_seeds,
    project_holdout_metrics,
    validate_holdout_payload,
    validate_holdout_seeds,
)
from scripts import run_holdout

SEEDS = list(range(10001, 10009))
# the 8 attempt-2 seeds exactly as declared in the r3-3 task order and
# published in the attempt-2 generation's public seed manifest
TASK_DECLARED_ATTEMPT2_SEEDS = [
    1118713940, 1814022456, 816612609, 1479804102,
    1767831484, 12762553, 1780740672, 1897543897,
]


def _export_game(item):
    winner = item["a"]
    rewards = [2.0, 1.0] if item["p0"] == winner else [1.0, 2.0]
    return {
        "players": [item["p0"], item["p1"]],
        "p0": item["p0"],
        "p1": item["p1"],
        "seed": item["seed"],
        "seed_domain": "holdout",
        "seat": item["seat"],
        "statuses": ["DONE", "DONE"],
        "contract_ok": True,
        "rewards": rewards,
        "winner": winner,
        "winner_label": winner,
        "turns": 720,
        "elapsed_seconds": 0.01,
    }


def _fixture_payload(attempt_index: int = 3):
    order = holdout_matrix_order(attempt_index)
    seeds = SEEDS
    games = [
        _export_game(item)
        for item in canonical_holdout_schedule(seeds, attempt_index=attempt_index)
    ]
    opponents = list(order[1:])
    evaluation = {
        "pairs": canonical_holdout_pairs(attempt_index=attempt_index),
        "seeds": seeds,
        "seed_domain": "holdout",
        "seat_orders": ["AB", "BA"],
        "episode_steps": 720,
        "run_kind": "official_holdout",
    }
    repository_files = {"runner.py": "a" * 64}
    repository = {"files": repository_files, "sha256": canonical_sha256(repository_files)}
    runtime_body = {
        "package_root": "installed",
        "distribution_version": "test",
        "vendored_wheel_sha256": "e" * 64,
        "wheel_match": True,
        "file_count": 1,
        "files": {"engine.py": "f" * 64},
    }
    runtime_engine = {**runtime_body, "sha256": canonical_sha256(runtime_body)}
    closure_body = {"repository": repository, "runtime_engine": runtime_engine}
    closure = {**closure_body, "sha256": canonical_sha256(closure_body)}
    identity = {
        "submission_path": "workspace/software/kaggle_simulations/agent/main.py",
        "submission_sha256": "9298751f124f02fc13a52f040af33fba2b3c9f5e8223599a830b8a3462cdd64c",
        "git_ref": "164439779b293a3d455e6920e631d911dfa2cdb4",
        "dirty": False,
        "input_sha256": canonical_sha256(evaluation),
    }
    confirmatory = candidate_confirmatory(games, opponents)
    isolation_count = len(historical_seeds(attempt_index))
    protocol = {
        "full_matrix": True, "seed_count": 8,
        "seat_orders": ["AB", "BA"], "one_time": True,
        "resume_exact_attempt_only": True,
        "candidate_change_invalidates": True,
        "candidate_source": "frozen_git_blob",
        "historical_seed_exclusion_count": isolation_count,
    }
    manifest = {
        "attempt_id": f"attempt{attempt_index}",
        "attempt_index": attempt_index,
        "seeds": seeds,
        "sha256": canonical_sha256(seeds),
        "historical_seed_exclusion_count": isolation_count,
        "overlap_with_historical": [],
    }
    return {
        "schema_version": "2.0",
        "generated_at": "2026-08-29T00:00:00+00:00",
        "run_kind": "official_holdout",
        "seed_domain": "holdout",
        "identity": identity,
        "evaluation_input": evaluation,
        "engine": {"package": "kaggle-environments", "version": "test", "scenario": "kaggriculture", "episode_steps": 720},
        "config": {
            "rounds": 8,
            "seeds": seeds,
            "matrix_order": list(order),
            "pairs": canonical_holdout_pairs(attempt_index=attempt_index),
            "seat_orders": ["AB", "BA"],
            "expected_games": holdout_expected_games(attempt_index),
        },
        "opponent_pool_names": opponents,
        "games": games,
        "abnormal_games": 0,
        "integrity": {
            "expected_games": holdout_expected_games(attempt_index),
            "actual_games": holdout_expected_games(attempt_index),
            "abnormal_games": 0,
            "ab_games": holdout_expected_seats(attempt_index),
            "ba_games": holdout_expected_seats(attempt_index),
            "missing_mirrors": 0,
        },
        "confirmatory": confirmatory,
        "elo": {"role": "descriptive_only", "order_sensitive": True, "k": 32.0, "start": 1200.0, "table": []},
        "holdout": {
            "protocol": protocol,
            "frozen_candidate": {"path": identity["submission_path"], "sha256": identity["submission_sha256"], "git_ref": identity["git_ref"]},
            "input_closure": {"sha256": closure["sha256"], "before": closure, "after": closure},
            "attempt": {"index": attempt_index, "attempt_id": f"attempt{attempt_index}", "status": "published", "started_at": "2026-08-29T00:00:00Z", "completed_at": "2026-08-29T01:00:00Z", "published": True, "invalidated": False, "invalidation_reason": None},
            "seed_manifest": manifest,
            "candidate_hash_match": {"frozen": identity["submission_sha256"], "before": identity["submission_sha256"], "after": identity["submission_sha256"], "pass": True},
            "seed_domain_isolation": {"historical_count": isolation_count, "overlap_count": 0, "pass": True},
        },
        "runtime_seconds": 1.0,
    }


def _attempt2_seed_manifest():
    """Locate the real attempt-2 public seed manifest (archive or live)."""
    for directory in (
        run_holdout.ARCHIVE_ROOT / "attempt-2",
        run_holdout.PUBLISHED_GENERATION,
    ):
        path = directory / "seed_manifest.json"
        if path.is_file():
            manifest = json.loads(path.read_text(encoding="utf-8"))
            if manifest.get("attempt_index") == 2:
                return manifest
    return None


def test_registry_v3_is_exactly_46_and_adds_only_attempt2_seeds():
    assert len(HISTORICAL_SEEDS_V2) == 38
    assert len(PUBLISHED_HOLDOUT_SEEDS_V2) == 8
    assert len(HISTORICAL_SEEDS_V3) == 46
    assert HISTORICAL_SEEDS_V2 < HISTORICAL_SEEDS_V3
    assert not set(PUBLISHED_HOLDOUT_SEEDS_V2) & HISTORICAL_SEEDS_V2
    assert len(historical_seeds(3)) == 46


def test_registry_v3_matches_task_declaration_and_published_artifact():
    assert sorted(TASK_DECLARED_ATTEMPT2_SEEDS) == sorted(PUBLISHED_HOLDOUT_SEEDS_V2)
    manifest = _attempt2_seed_manifest()
    if manifest is None:
        pytest.skip("attempt-2 generation not present in this checkout")
    assert sorted(manifest["seeds"]) == sorted(PUBLISHED_HOLDOUT_SEEDS_V2)
    assert not set(manifest["seeds"]) & HISTORICAL_SEEDS_V2


def test_attempt2_published_generation_still_validates():
    source = None
    for directory in (
        run_holdout.ARCHIVE_ROOT / "attempt-2",
        run_holdout.PUBLISHED_GENERATION,
    ):
        path = directory / "eval_results.json"
        if path.is_file():
            payload = json.loads(path.read_text(encoding="utf-8"))
            if payload["holdout"]["attempt"]["index"] == 2:
                source = payload
                break
    if source is None:
        pytest.skip("attempt-2 generation not present in this checkout")
    report = validate_holdout_payload(source)
    assert report["actual_games"] == 576
    assert report["candidate_games"] == 128


def test_attempt3_matrix_is_the_ten_agent_full_pool():
    order = holdout_matrix_order(3)
    assert list(order) == list(HOLDOUT_V3_MATRIX_ORDER)
    assert order[0] == "submission"
    assert order[-1] == "scale_ranch"
    assert len(order) == 10
    assert len(canonical_holdout_pairs(attempt_index=3)) == 45
    assert holdout_expected_games(3) == 720
    assert holdout_expected_seats(3) == 360
    assert candidate_expected_games(3) == 144
    assert candidate_paired_units(3) == 72
    assert attempt_metrics_prefix(3) == "r4_"


def test_attempt3_schedule_is_full_matrix_and_seat_balanced():
    schedule = canonical_holdout_schedule(SEEDS, attempt_index=3)
    assert len(schedule) == 720
    assert sum(item["seat"] == "AB" for item in schedule) == 360
    assert sum(item["seat"] == "BA" for item in schedule) == 360
    mirrors: dict[tuple[str, str, int], set[str]] = {}
    for item in schedule:
        mirrors.setdefault((item["a"], item["b"], item["seed"]), set()).add(item["seat"])
    assert len(mirrors) == 360
    assert all(seats == {"AB", "BA"} for seats in mirrors.values())
    names = {name for item in schedule for name in (item["a"], item["b"])}
    assert names == set(HOLDOUT_V3_MATRIX_ORDER)


@pytest.mark.parametrize("seed", sorted(HISTORICAL_SEEDS_V3))
def test_every_historical_seed_v3_is_rejected_for_attempt3(seed):
    seeds = SEEDS[:-1] + [seed]
    with pytest.raises(ContractError, match="historical"):
        validate_holdout_seeds(seeds, attempt_index=3)


def test_generated_attempt3_seeds_never_collide_with_any_exclusion():
    from kgenv.holdout_contract import generate_holdout_seeds

    forbidden_values = sorted(HISTORICAL_SEEDS_V3 - HISTORICAL_SEEDS_V2)
    assert len(forbidden_values) == 8
    collision_draws = [value - 10_000 for value in forbidden_values * 3]
    draws = iter(collision_draws + list(range(1, 9)))
    seeds = generate_holdout_seeds(
        lambda upper: next(draws), excluded=historical_seeds(3)
    )
    assert seeds == SEEDS
    assert not set(seeds) & HISTORICAL_SEEDS_V3


def test_attempt3_fixture_payload_passes_schema_and_semantics():
    payload = _fixture_payload()
    run_holdout._schema_validate(payload)
    report = validate_holdout_payload(payload)
    assert report == {
        "expected_games": 720, "actual_games": 720, "abnormal_games": 0,
        "ab_games": 360, "ba_games": 360, "missing_mirrors": 0,
        "candidate_games": 144, "valid": True,
    }
    overall = payload["confirmatory"]["overall_record"]
    assert overall["games"] == 144 and overall["W"] == 144
    assert overall["score_rate"] == 1.0
    statistic = payload["confirmatory"]["order_independent_statistic"]
    assert statistic["unit_count"] == 72
    assert statistic["fit_status"] == "ok"
    assert len(payload["confirmatory"]["pair_records"]) == 9


def test_attempt3_seat_records_break_down_every_opponent():
    records = _fixture_payload()["confirmatory"]["seat_records"]
    for seat in ("AB", "BA"):
        assert records[seat]["games"] == 72
        assert set(records[seat]["by_opponent"]) == set(HOLDOUT_V3_MATRIX_ORDER[1:])
        assert all(row["games"] == 8 for row in records[seat]["by_opponent"].values())


def test_attempt3_candidate_statistics_are_order_independent():
    games = _fixture_payload()["games"]
    opponents = list(HOLDOUT_V3_MATRIX_ORDER[1:])
    assert candidate_confirmatory(games, opponents) == candidate_confirmatory(
        list(reversed(games)), opponents
    )


def test_attempt3_rejects_prior_generation_identity_and_wrong_pool():
    payload = _fixture_payload()
    payload["holdout"]["attempt"].update(attempt_id=PUBLISHED_HOLDOUT_ATTEMPT_V2_ID)
    with pytest.raises(ContractError, match="prior generation"):
        validate_holdout_payload(payload)

    payload = _fixture_payload()
    payload["config"].update(matrix_order=list(HOLDOUT_V3_MATRIX_ORDER[:-1]))
    payload["opponent_pool_names"] = list(HOLDOUT_V3_MATRIX_ORDER[1:-1])
    with pytest.raises(ContractError, match="matrix order"):
        validate_holdout_payload(payload)

    payload = _fixture_payload()
    payload["holdout"]["protocol"].update(historical_seed_exclusion_count=38)
    payload["holdout"]["seed_manifest"].update(historical_seed_exclusion_count=38)
    payload["holdout"]["seed_domain_isolation"].update(historical_count=38)
    with pytest.raises(ContractError):
        validate_holdout_payload(payload)


def test_attempt3_projection_uses_r4_prefix_and_keeps_history():
    payload = _fixture_payload()
    metrics = project_holdout_metrics(payload, "f" * 64, prefix="r4_")
    required = {
        "r4_holdout_protocol", "r4_holdout_seed_manifest", "r4_holdout_candidate_hash_match",
        "r4_holdout_seed_domain_isolation", "r4_holdout_run_status", "r4_holdout_schedule",
        "r4_holdout_seat_split", "r4_holdout_abnormal_summary", "r4_holdout_integrity_pass",
        "r4_confirmatory_overall_record", "r4_confirmatory_pair_records",
        "r4_confirmatory_seat_records", "r4_confirmatory_wilson_intervals",
        "r4_confirmatory_order_independent_statistics", "r4_confirmatory_elo_appendix",
        "r4_confirmatory_export_traceability",
    }
    assert set(metrics) == required
    trace = metrics["r4_confirmatory_export_traceability"]["value"]
    assert trace["export_sha256"] == "f" * 64
    assert metrics["r4_holdout_seed_domain_isolation"]["value"]["historical_count"] == 46


def test_staging_attempt4_generation_preserves_prior_metrics_history(tmp_path, monkeypatch):
    payload = _fixture_payload(attempt_index=4)
    history = {
        "holdout_protocol": {"value": "attempt-1-history"},
        "m4_confirmatory_overall_record": {"value": "attempt-2-history"},
        "r4_holdout_protocol": {"value": "attempt-3-history"},
    }
    metrics_path = tmp_path / "metrics.json"
    metrics_path.write_text(json.dumps({"metrics": history}), encoding="utf-8")
    monkeypatch.setattr(run_holdout, "METRICS_PATH", metrics_path)
    staged = tmp_path / "staged"
    monkeypatch.setattr(run_holdout, "STAGED_GENERATION", staged)
    monkeypatch.setattr(run_holdout, "PUBLISHED_GENERATION", tmp_path / "published")
    monkeypatch.setattr(run_holdout, "GEN_EXPORT", tmp_path / "published" / "eval_results.json")
    monkeypatch.setattr(run_holdout, "GEN_REPLAY", tmp_path / "published" / "replay_log.jsonl")
    monkeypatch.setattr(run_holdout, "GEN_MANIFEST", tmp_path / "published" / "seed_manifest.json")
    monkeypatch.setattr(run_holdout, "GEN_METRICS", tmp_path / "published" / "software_metrics.json")
    run_holdout._stage_generation(
        payload, payload["holdout"]["seed_manifest"], payload["games"]
    )
    shard = json.loads((staged / "software_metrics.json").read_text(encoding="utf-8"))
    assert shard["metrics"]["holdout_protocol"] == {"value": "attempt-1-history"}
    assert shard["metrics"]["m4_confirmatory_overall_record"] == {"value": "attempt-2-history"}
    assert shard["metrics"]["r4_holdout_protocol"] == {"value": "attempt-3-history"}
    assert "v6_holdout_protocol" in shard["metrics"]
    assert "v6_confirmatory_export_traceability" in shard["metrics"]
    assert "r5-P6 v6-holdout" in shard["milestone"]
