"""m2c one-time holdout contract tests; no real environment games run."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from kgenv.eval_contract import ContractError, STANDARD_MATRIX_ORDER, canonical_sha256
from kgenv.holdout_contract import (
    HISTORICAL_SEEDS,
    candidate_confirmatory,
    canonical_holdout_pairs,
    canonical_holdout_schedule,
    create_or_load_attempt,
    project_holdout_metrics,
    validate_holdout_payload,
    validate_holdout_seeds,
)
from scripts import run_holdout

SEEDS = list(range(10001, 10009))


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


def _fixture_payload():
    games = [_export_game(item) for item in canonical_holdout_schedule(SEEDS)]
    evaluation = {
        "pairs": canonical_holdout_pairs(),
        "seeds": SEEDS,
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
        "submission_sha256": "c" * 64,
        "git_ref": "deadbeef",
        "dirty": False,
        "input_sha256": canonical_sha256(evaluation),
    }
    confirmatory = candidate_confirmatory(games)
    return {
        "schema_version": "2.0",
        "generated_at": "2026-08-28T00:00:00+00:00",
        "run_kind": "official_holdout",
        "seed_domain": "holdout",
        "identity": identity,
        "evaluation_input": evaluation,
        "engine": {"package": "kaggle-environments", "version": "test", "scenario": "kaggriculture", "episode_steps": 720},
        "config": {
            "rounds": 8,
            "seeds": SEEDS,
            "matrix_order": list(STANDARD_MATRIX_ORDER),
            "pairs": canonical_holdout_pairs(),
            "seat_orders": ["AB", "BA"],
            "expected_games": 576,
        },
        "opponent_pool_names": list(STANDARD_MATRIX_ORDER[1:]),
        "games": games,
        "abnormal_games": 0,
        "integrity": {"expected_games": 576, "actual_games": 576, "abnormal_games": 0, "ab_games": 288, "ba_games": 288, "missing_mirrors": 0},
        "confirmatory": confirmatory,
        "elo": {"role": "descriptive_only", "order_sensitive": True, "k": 32.0, "start": 1200.0, "table": []},
        "holdout": {
            "protocol": {
                "full_matrix": True, "seed_count": 8,
                "seat_orders": ["AB", "BA"], "one_time": True,
                "resume_exact_attempt_only": True,
                "candidate_change_invalidates": True,
                "candidate_source": "frozen_git_blob",
            },
            "frozen_candidate": {"path": identity["submission_path"], "sha256": identity["submission_sha256"], "git_ref": "frozenref"},
            "input_closure": {"sha256": closure["sha256"], "before": closure, "after": closure},
            "attempt": {"index": 1, "attempt_id": "attempt", "status": "published", "started_at": "2026-08-28T00:00:00Z", "completed_at": "2026-08-28T01:00:00Z", "published": True, "invalidated": False, "invalidation_reason": None},
            "seed_manifest": {"attempt_id": "attempt", "seeds": SEEDS, "sha256": canonical_sha256(SEEDS)},
            "candidate_hash_match": {"frozen": identity["submission_sha256"], "before": identity["submission_sha256"], "after": identity["submission_sha256"], "pass": True},
            "seed_domain_isolation": {"historical_count": len(HISTORICAL_SEEDS), "overlap_count": 0, "pass": True},
        },
        "runtime_seconds": 1.0,
    }


def test_frozen_snapshot_executes_manifest_git_blob_not_worktree(monkeypatch, tmp_path):
    frozen = b"def agent(obs): return {'frozen': True}\n"
    candidate = tmp_path / "main.py"
    candidate.write_bytes(b"def agent(obs): return {'worktree': True}\n")
    manifest = {
        "candidate": {
            "path": str(candidate), "sha256": run_holdout._sha256_bytes(frozen),
            "git_ref": "frozen-ref",
        }
    }
    monkeypatch.setattr(run_holdout, "_load_frozen_blob", lambda value: frozen)
    with run_holdout.frozen_candidate_snapshot(manifest, {"run": "holdout"}) as snapshot:
        assert snapshot.snapshot_path.read_bytes() == frozen
        candidate.write_bytes(b"changed again")
        snapshot.verify_candidate_unchanged()
        assert snapshot.identity["submission_sha256"] == run_holdout._sha256_bytes(frozen)


def test_interrupted_seed_allocation_is_consumed_without_redraw(tmp_path):
    path = tmp_path / "attempt.json"
    path.write_text(json.dumps({
        "schema_version": "1.0", "attempt_id": "x", "status": "allocating",
        "candidate_sha256": "a" * 64, "frozen_manifest_sha256": "b" * 64,
        "evaluator_closure": {"files": {}, "sha256": "d" * 64},
        "seeds": None, "completed_games": 0,
    }), encoding="utf-8")
    with pytest.raises(ContractError, match="consumed|redrawn"):
        create_or_load_attempt(
            path, candidate_sha256="a" * 64,
            frozen_manifest_sha256="b" * 64,
            evaluator_closure={"files": {}, "sha256": "d" * 64},
            randbelow=lambda upper: pytest.fail("interrupted allocation must not redraw"),
        )
    state = json.loads(path.read_text(encoding="utf-8"))
    assert state["status"] == "invalidated"
    assert state["seeds"] is None


def test_nested_holdout_claims_are_semantically_bound():
    mutations = [
        lambda p: p["config"].update(seeds=list(reversed(SEEDS))),
        lambda p: p.update(opponent_pool_names=[]),
        lambda p: p["holdout"]["candidate_hash_match"].update(pass_=False),
        lambda p: p["holdout"]["seed_domain_isolation"].update(overlap_count=1),
        lambda p: p["holdout"]["attempt"].update(invalidated=True),
        lambda p: p["holdout"]["input_closure"]["before"]["repository"].update(sha256="0" * 64),
        lambda p: p["holdout"]["protocol"].update(one_time=False),
        lambda p: p["engine"].update(version="forged"),
        lambda p: p["holdout"]["seed_manifest"].update(attempt_id="other"),
    ]
    for mutate in mutations:
        payload = _fixture_payload()
        mutate(payload)
        if "pass_" in payload["holdout"]["candidate_hash_match"]:
            payload["holdout"]["candidate_hash_match"]["pass"] = False
        with pytest.raises(ContractError):
            validate_holdout_payload(payload)


def test_seat_records_include_every_opponent_breakdown():
    records = _fixture_payload()["confirmatory"]["seat_records"]
    assert set(records) == {"AB", "BA"}
    for seat in ("AB", "BA"):
        assert records[seat]["games"] == 64
        assert set(records[seat]["by_opponent"]) == set(STANDARD_MATRIX_ORDER[1:])
        assert all(row["games"] == 8 for row in records[seat]["by_opponent"].values())


def test_authoritative_generation_commits_with_one_directory_rename(monkeypatch, tmp_path):
    payload = _fixture_payload()
    staged = tmp_path / "private" / "staged"
    published = tmp_path / "public" / "published"
    metrics = tmp_path / "metrics.json"
    metrics.write_text(json.dumps({"metrics": {}}), encoding="utf-8")
    monkeypatch.setattr(run_holdout, "STAGED_GENERATION", staged)
    monkeypatch.setattr(run_holdout, "PUBLISHED_GENERATION", published)
    monkeypatch.setattr(run_holdout, "METRICS_PATH", metrics)
    monkeypatch.setattr(run_holdout, "GEN_EXPORT", published / "eval_results.json")
    monkeypatch.setattr(run_holdout, "GEN_REPLAY", published / "replay_log.jsonl")
    monkeypatch.setattr(run_holdout, "GEN_MANIFEST", published / "seed_manifest.json")
    monkeypatch.setattr(run_holdout, "GEN_METRICS", published / "software_metrics.json")
    staged_result = run_holdout._stage_generation(
        payload, payload["holdout"]["seed_manifest"], payload["games"]
    )
    assert staged_result == staged
    assert not published.exists()
    run_holdout._commit_generation(staged)
    assert published.is_dir()
    assert not staged.exists()
    assert run_holdout._validate_generation(published)["run_kind"] == "official_holdout"


def test_projection_failure_leaves_authoritative_generation_recoverable(monkeypatch, tmp_path):
    source = tmp_path / "published.json"
    target = tmp_path / "projection.json"
    source.write_text('{"generation": 1}', encoding="utf-8")
    target.write_text('{"generation": 0}', encoding="utf-8")
    original_replace = run_holdout.os.replace
    monkeypatch.setattr(run_holdout.os, "replace", lambda *args: (_ for _ in ()).throw(OSError("crash")))
    with pytest.raises(OSError):
        run_holdout._atomic_project(source, target)
    assert json.loads(source.read_text(encoding="utf-8")) == {"generation": 1}
    assert json.loads(target.read_text(encoding="utf-8")) == {"generation": 0}
    monkeypatch.setattr(run_holdout.os, "replace", original_replace)
    run_holdout._atomic_project(source, target)
    assert json.loads(target.read_text(encoding="utf-8")) == {"generation": 1}


def test_holdout_schedule_is_full_matrix_and_seat_balanced():
    schedule = canonical_holdout_schedule(SEEDS)
    assert len(schedule) == 576
    assert sum(item["seat"] == "AB" for item in schedule) == 288
    assert sum(item["seat"] == "BA" for item in schedule) == 288
    mirrors = {(item["a"], item["b"], item["seed"]): set() for item in schedule}
    for item in schedule:
        mirrors[(item["a"], item["b"], item["seed"])].add(item["seat"])
    assert len(mirrors) == 288
    assert all(seats == {"AB", "BA"} for seats in mirrors.values())


@pytest.mark.parametrize("seed", sorted(HISTORICAL_SEEDS))
def test_every_historical_seed_is_rejected(seed):
    seeds = SEEDS[:-1] + [seed]
    with pytest.raises(ContractError, match="historical"):
        validate_holdout_seeds(seeds)


def test_attempt_is_persisted_then_resumed_without_redraw(tmp_path):
    path = tmp_path / "attempt.json"
    draws = iter(range(1, 9))
    closure = {"files": {}, "sha256": "d" * 64}
    first, created = create_or_load_attempt(
        path,
        candidate_sha256="a" * 64,
        frozen_manifest_sha256="b" * 64,
        evaluator_closure=closure,
        randbelow=lambda upper: next(draws),
        now=lambda: "2026-08-28T00:00:00Z",
    )
    assert created is True
    assert first["status"] == "running"
    assert first["seeds"] == SEEDS
    second, created = create_or_load_attempt(
        path,
        candidate_sha256="a" * 64,
        frozen_manifest_sha256="b" * 64,
        evaluator_closure=closure,
        randbelow=lambda upper: pytest.fail("resume must not redraw seeds"),
    )
    assert created is False
    assert second["seeds"] == first["seeds"]


def test_published_or_identity_changed_attempt_cannot_resume(tmp_path):
    path = tmp_path / "attempt.json"
    closure = {"files": {}, "sha256": "d" * 64}
    draws = iter(range(1, 9))
    state, _ = create_or_load_attempt(
        path, candidate_sha256="a" * 64, frozen_manifest_sha256="b" * 64,
        evaluator_closure=closure, randbelow=lambda upper: next(draws),
    )
    state["status"] = "published"
    path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(ContractError, match="published"):
        create_or_load_attempt(path, candidate_sha256="a" * 64,
                               frozen_manifest_sha256="b" * 64,
                               evaluator_closure=closure)
    state["status"] = "running"
    path.write_text(json.dumps(state), encoding="utf-8")
    with pytest.raises(ContractError, match="candidate"):
        create_or_load_attempt(path, candidate_sha256="e" * 64,
                               frozen_manifest_sha256="b" * 64,
                               evaluator_closure=closure)


def test_full_payload_schema_and_semantics_pass():
    payload = _fixture_payload()
    run_holdout._schema_validate(payload)
    report = validate_holdout_payload(payload)
    assert report == {
        "expected_games": 576, "actual_games": 576, "abnormal_games": 0,
        "ab_games": 288, "ba_games": 288, "missing_mirrors": 0,
        "candidate_games": 128, "valid": True,
    }
    assert payload["confirmatory"]["overall_record"] == {
        "games": 128, "W": 128, "L": 0, "T": 0,
        "score_rate": 1.0, "wilson95": [0.9709, 1.0],
    }
    assert payload["confirmatory"]["order_independent_statistic"]["unit_count"] == 64


def test_holdout_semantics_reject_missing_mirror_abnormal_and_cross_totals():
    payload = _fixture_payload()
    payload["games"] = payload["games"][:-1]
    payload["integrity"]["actual_games"] = 575
    with pytest.raises(ContractError, match="schedule|576"):
        validate_holdout_payload(payload)

    payload = _fixture_payload()
    payload["games"][0]["statuses"] = ["INVALID", "DONE"]
    payload["games"][0]["contract_ok"] = False
    with pytest.raises(ContractError, match="abnormal|DONE"):
        validate_holdout_payload(payload)

    payload = _fixture_payload()
    payload["confirmatory"]["overall_record"]["W"] -= 1
    with pytest.raises(ContractError, match="overall_record"):
        validate_holdout_payload(payload)


def test_candidate_statistics_are_order_independent():
    games = _fixture_payload()["games"]
    assert candidate_confirmatory(games) == candidate_confirmatory(list(reversed(games)))


def test_metrics_projection_is_traceable_to_validated_export():
    payload = _fixture_payload()
    metrics = project_holdout_metrics(payload, "f" * 64)
    required = {
        "holdout_protocol", "holdout_seed_manifest", "holdout_candidate_hash_match",
        "holdout_seed_domain_isolation", "holdout_run_status", "holdout_schedule",
        "holdout_seat_split", "holdout_abnormal_summary", "holdout_integrity_pass",
        "confirmatory_overall_record", "confirmatory_pair_records",
        "confirmatory_seat_records", "confirmatory_wilson_intervals",
        "confirmatory_order_independent_statistics", "confirmatory_elo_appendix",
        "confirmatory_export_traceability",
    }
    assert set(metrics) == required
    trace = metrics["confirmatory_export_traceability"]["value"]
    assert trace["export_sha256"] == "f" * 64
    assert trace["validated_schema"] == "2.0"
    assert all(row["method"].startswith("workspace/software/exports/eval_results.json#") for row in metrics.values())


def test_checkpoint_must_be_exact_schedule_prefix(monkeypatch, tmp_path):
    state = {"attempt_id": "x", "completed_games": 1}
    schedule = canonical_holdout_schedule(SEEDS)
    checkpoint = tmp_path / "games.json"
    checkpoint.write_text(json.dumps({"attempt_id": "x", "games": [_export_game(schedule[1])]}), encoding="utf-8")
    monkeypatch.setattr(run_holdout, "GAMES_PATH", checkpoint)
    with pytest.raises(ContractError, match="prefix"):
        run_holdout._load_checkpoint(state, schedule)


def test_verify_published_never_runs_matches(monkeypatch, tmp_path):
    payload = _fixture_payload()
    published = tmp_path / "published"
    published.mkdir()
    monkeypatch.setattr(run_holdout, "PUBLISHED_GENERATION", published)
    monkeypatch.setattr(run_holdout, "_load_frozen", lambda required: ({}, "x"))
    monkeypatch.setattr(run_holdout, "_reconcile_published_state", lambda: payload)
    monkeypatch.setattr(run_holdout, "_input_closure", lambda: payload["holdout"]["input_closure"]["before"])
    monkeypatch.setattr(run_holdout, "run_match", lambda *args, **kwargs: pytest.fail("verification must not run games"))
    assert run_holdout.verify_published(True)["actual_games"] == 576


def test_invalid_generation_never_replaces_existing_projections(monkeypatch, tmp_path):
    targets = [tmp_path / name for name in ("eval.json", "replay.jsonl", "manifest.json", "metrics.json")]
    for target in targets:
        target.write_text("old", encoding="utf-8")
    targets[3].write_text(json.dumps({"metrics": {}}), encoding="utf-8")
    original = [target.read_text(encoding="utf-8") for target in targets]
    monkeypatch.setattr(run_holdout, "FORMAL_EXPORT", targets[0])
    monkeypatch.setattr(run_holdout, "FORMAL_REPLAY", targets[1])
    monkeypatch.setattr(run_holdout, "PUBLIC_MANIFEST", targets[2])
    monkeypatch.setattr(run_holdout, "METRICS_PATH", targets[3])
    monkeypatch.setattr(run_holdout, "STAGED_GENERATION", tmp_path / "staged")
    payload = _fixture_payload()
    payload["confirmatory"]["overall_record"]["W"] -= 1
    with pytest.raises(ContractError):
        run_holdout._stage_generation(
            payload, payload["holdout"]["seed_manifest"], payload["games"]
        )
    assert [target.read_text(encoding="utf-8") for target in targets] == original
