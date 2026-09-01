"""Formal external H2H evidence contract regressions."""

from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

import pytest

from kgenv.eval_contract import ContractError, canonical_sha256
from kgenv.external_h2h_contract import (
    canonical_external_digest,
    schema_validate_external,
    summarize_external_games,
    validate_external_h2h,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _activity(rewards=(10.0, 10.0)) -> dict:
    seats = [
        {"decisions": 719, "non_pass_decisions": 100, "effective_commands": 80,
         "max_pass_streak": 10, "non_pass_trace": ([True] + [False] * 10) * 61 + [True] * 39 + [False] * 9,
         "state_change_trace": [True] * 80 + [False] * 639, "reward_delta": rewards[0], "pass_only": False,
         "reasons": [], "policy": {"min_non_pass_ratio": 0.05,
                                     "max_pass_streak": 96,
                                     "min_reward_delta": None,
                                     "require_effective_state_change": False}},
        {"decisions": 719, "non_pass_decisions": 110, "effective_commands": 90,
         "max_pass_streak": 9, "non_pass_trace": ([True] + [False] * 9) * 67 + [True] * 43 + [False] * 6,
         "state_change_trace": [True] * 90 + [False] * 629, "reward_delta": rewards[1], "pass_only": False,
         "reasons": [], "policy": {"min_non_pass_ratio": 0.05,
                                     "max_pass_streak": 96,
                                     "min_reward_delta": None,
                                     "require_effective_state_change": False}},
    ]
    for seat in seats:
        evidence = {"action_count": seat["decisions"], "non_pass_action_count": seat["non_pass_decisions"],
                    "state_change_count": seat["effective_commands"], "state_count": 720,
                    "reward_delta": seat["reward_delta"],
                    "non_pass_trace": seat["non_pass_trace"],
                    "state_change_trace": seat["state_change_trace"]}
        seat["evidence"] = {**evidence, "evidence_digest": canonical_sha256(evidence)}
    return {"states": 720, "decisions": 719, "starting_money": 0.0, "completion_ok": True,
            "activity_ok": True, "ok": True, "contract_status": "producer_attested",
            "independently_recomputed": False, "seats": seats}


def _fixture(tmp_path: Path) -> tuple[dict, Path]:
    candidate = tmp_path / "main.py"
    opponent = tmp_path / "v48_main.py"
    wheel = tmp_path / "engine.whl"
    candidate.write_text("def agent(obs): return {}\n", encoding="utf-8")
    opponent.write_text("def agent(obs): return {}\n# external\n", encoding="utf-8")
    wheel.write_bytes(b"wheel")
    candidate_id, opponent_id = "working", "v48"
    games = []
    outcomes = [(101, "AB", candidate_id), (101, "BA", opponent_id),
                (102, "AB", None), (102, "BA", candidate_id)]
    for seed, seat, winner in outcomes:
        players = ([candidate_id, opponent_id] if seat == "AB"
                   else [opponent_id, candidate_id])
        candidate_seat = players.index(candidate_id)
        rewards = ([10.0, 10.0] if winner is None else
                    [20.0, 10.0] if players[0] == winner else [10.0, 20.0])
        games.append({
            "game_id": f"working--v48--{seed}--{seat}", "opponent_id": opponent_id,
            "seed": seed, "seat": seat, "players": players, "candidate_seat": candidate_seat,
            "statuses": ["DONE", "DONE"], "contract_ok": True, "rewards": rewards,
            "winner": winner, "margin": rewards[candidate_seat] - rewards[1 - candidate_seat],
            "episode_steps": 720, "states": 720, "completion_ok": True,
            "activity": _activity(rewards), "abnormal_reason": None, "elapsed_seconds": 0.01,
        })
    closure_files = {str(candidate): _sha(candidate), str(opponent): _sha(opponent),
                     str(wheel): _sha(wheel)}
    closure = {"files": closure_files, "sha256": canonical_sha256(closure_files)}
    payload = {
        "schema_version": "external-h2h/2.0",
        "generated_at": "2026-08-31T00:00:00+00:00",
        "evidence_scope": {"kind": "external_black_box_stress", "development_only": True,
                           "formal_promotion_eligible": False, "holdout_evidence": False,
                           "limitations": ["not a holdout generalization claim"]},
        "engine": {"name": "kaggle-environments", "version": "1.32.7",
                   "scenario": "kaggriculture", "wheel_path": str(wheel),
                   "wheel_sha256": _sha(wheel),
                   "runtime_attestation": {
                       "package_root": str(tmp_path / "runtime"),
                       "files": {key: f"{index:x}" * 64 for index, key in enumerate((
                           "__init__.py", "core.py", "agent.py", "utils.py", "errors.py",
                           "status_codes.json", "envs/kaggriculture/kaggriculture.py",
                           "envs/kaggriculture/kaggriculture.json"))},
                       "matches_vendored_wheel": True}},
        "candidate": {"id": candidate_id, "path": str(candidate), "sha256": _sha(candidate),
                      "role": "working", "status": "development",
                      "active_candidate_contract": str(tmp_path / "active_candidate.json")},
        "opponents": [{"id": opponent_id, "path": str(opponent), "sha256": _sha(opponent),
                       "provenance": {"author": "kaitofukami", "source": "Kaggle notebook snapshot",
                                      "source_url": "https://www.kaggle.com/example",
                                      "acquired_at": "2026-08-31"},
                       "license": {"status": "no-explicit-reuse-license", "spdx": None},
                       "use_restriction": "read-only black-box stress opponent; not-for-submission"}],
        "seed_domain": {"name": "external-development-v1", "seeds": [101, 102], "holdout": False},
        "schedule": {"policy": "paired_ab_ba", "seat_orders": ["AB", "BA"],
                     "opponent_ids": [opponent_id], "expected_games": 4},
        "games": games, "summary": summarize_external_games(games, candidate_id),
        "input_closure": {"algorithm": "sha256-path-map-v1", "before": closure,
                          "after": copy.deepcopy(closure), "unchanged": True},
        "command": {"argv": ["python", "h2h_external_probe.py", "--seeds", "101,102"],
                    "cwd": str(tmp_path), "parameters": {"seeds": [101, 102], "opponents": [opponent_id]}},
        "digests": {"algorithm": "canonical-json-sha256", "canonical_payload_sha256": ""},
    }
    payload["digests"]["canonical_payload_sha256"] = canonical_external_digest(payload)
    active = {"schema_version": "1.0", "working": {"label": "test", "status": "development",
             "path": str(candidate), "sha256": _sha(candidate), "git_ref": "deadbeef",
             "holdout_status": "not_run"}}
    Path(payload["candidate"]["active_candidate_contract"]).write_text(
        json.dumps(active), encoding="utf-8")
    return payload, candidate


def _redigest(payload: dict) -> None:
    payload["digests"]["canonical_payload_sha256"] = canonical_external_digest(payload)


def test_external_contract_schema_and_semantics_pass(tmp_path):
    payload, _ = _fixture(tmp_path)
    schema_validate_external(payload, Path(__file__).parents[1] / "exports" / "external_h2h_schema.json")
    report = validate_external_h2h(payload)
    assert report == {"valid": True, "expected_games": 4, "actual_games": 4,
                      "opponents": 1, "seeds": 2, "ab_games": 2, "ba_games": 2,
                      "abnormal_games": 0}


@pytest.mark.parametrize("mutate,match", [
    (lambda p: p["games"].pop(), "schedule|missing"),
    (lambda p: p["games"].__setitem__(1, copy.deepcopy(p["games"][0])), "duplicate|game_id"),
    (lambda p: [g.update(seat="AB") for g in p["games"]], "seat|schedule"),
    (lambda p: p["games"][0].update(statuses=["INVALID", "DONE"], contract_ok=False,
                                    winner=None, abnormal_reason=None), "abnormal"),
    (lambda p: p["summary"]["overall"].update(W=99), "summary|aggregate"),
    (lambda p: p["candidate"].update(sha256="0" * 64), "candidate.*SHA|identity"),
    (lambda p: p["engine"].update(version="0.0.0"), "engine"),
    (lambda p: p["opponents"][0].update(provenance={}), "provenance"),
    (lambda p: p["seed_domain"].update(seeds=[101, 101]), "seed"),
    (lambda p: p["input_closure"].update(unchanged=False), "closure"),
])
def test_external_contract_fail_closed_mutations(tmp_path, mutate, match):
    payload, _ = _fixture(tmp_path)
    mutate(payload)
    _redigest(payload)
    with pytest.raises(ContractError, match=match):
        validate_external_h2h(payload)


def test_external_contract_detects_file_sha_drift(tmp_path):
    payload, candidate = _fixture(tmp_path)
    candidate.write_text("changed", encoding="utf-8")
    with pytest.raises(ContractError, match="candidate.*SHA|closure.*SHA"):
        validate_external_h2h(payload)


def test_external_contract_rejects_holdout_or_promotion_claim(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["seed_domain"].update(name="holdout", holdout=True)
    payload["evidence_scope"].update(formal_promotion_eligible=True, holdout_evidence=True)
    _redigest(payload)
    with pytest.raises(ContractError, match="external|holdout|promotion"):
        validate_external_h2h(payload)


def test_external_contract_requires_canonical_roots_and_full_closure(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["candidate"]["active_candidate_contract"] = str(tmp_path / "fake-active.json")
    _redigest(payload)
    with pytest.raises(ContractError, match="canonical|active candidate"):
        validate_external_h2h(payload, software_root=Path(__file__).parents[1])
    payload, _ = _fixture(tmp_path)
    payload["input_closure"]["before"]["files"].pop(next(iter(payload["input_closure"]["before"]["files"])))
    payload["input_closure"]["after"] = copy.deepcopy(payload["input_closure"]["before"])
    _redigest(payload)
    with pytest.raises(ContractError, match="closure|canonical|required"):
        validate_external_h2h(payload, software_root=Path(__file__).parents[1])


def test_external_contract_recomputes_activity_not_three_booleans(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["games"][0]["activity"] = {"completion_ok": True, "activity_ok": True, "ok": True}
    _redigest(payload)
    with pytest.raises(ContractError, match="activity"):
        validate_external_h2h(payload)


def test_external_contract_rejects_inconsistent_activity_numbers(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["games"][0]["activity"]["seats"][0]["effective_commands"] = -1
    _redigest(payload)
    with pytest.raises(ContractError, match="activity"):
        validate_external_h2h(payload)


def test_external_contract_rejects_forged_activity_with_unchanged_digest(tmp_path):
    # 2026-09-01 迁移改写：旧版借用历史 v48 证据（其 candidate SHA 是冻结 v10.2，
    # 与工作树 development main.py 必然不同，过去靠路径解析失败报 evidence 撞正则）。
    # 现用自洽夹具表达同一语义：篡改 activity 且不重算 digest → 必须被拒。
    payload, _ = _fixture(tmp_path)
    payload["games"][0]["activity"]["seats"][0]["non_pass_decisions"] += 1
    with pytest.raises(ContractError, match="activity|digest|evidence|canonical"):
        validate_external_h2h(payload, software_root=Path(__file__).parents[1])


def test_external_contract_rejects_forged_producer_attested_aggregate_after_redigest(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["games"][0]["activity"]["seats"][0]["non_pass_decisions"] += 1
    _redigest(payload)
    with pytest.raises(ContractError, match="trace|activity"):
        validate_external_h2h(payload)


@pytest.mark.parametrize("field", ["rewards", "margin", "elapsed_seconds"])
def test_external_contract_rejects_nonfinite_game_numbers(tmp_path, field):
    payload, _ = _fixture(tmp_path)
    if field == "rewards":
        payload["games"][0][field][0] = float("nan")
    else:
        payload["games"][0][field] = float("inf")
    _redigest(payload)
    with pytest.raises(ContractError, match="finite|reward|margin|elapsed"):
        validate_external_h2h(payload)


def test_external_contract_rejects_nonfinite_activity_numbers(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["games"][0]["activity"]["starting_money"] = float("nan")
    _redigest(payload)
    with pytest.raises(ContractError, match="finite|starting_money"):
        validate_external_h2h(payload)


def test_external_probe_rejects_output_alias_before_play():
    from scripts import h2h_external_probe
    candidate = {"path": "workspace/software/kaggle_simulations/agent/main.py"}
    opponent = {"path": "workspace/software/kaggle_simulations/opponents/v48_main.py"}
    closure = {"files": {"workspace/software/kgenv/engine.py": "x"}}
    with pytest.raises(ContractError, match="output target|exports/external"):
        h2h_external_probe._reject_output_alias(
            h2h_external_probe.REPO_ROOT / candidate["path"], candidate, [opponent], closure)
    with pytest.raises(ContractError, match="output target|exports/external"):
        h2h_external_probe._reject_output_alias(
            h2h_external_probe.REPO_ROOT / "workspace/software/kgenv/engine.py",
            candidate, [opponent], closure)


def test_external_tools_reject_repository_outputs_outside_external_exports():
    from scripts import fit_bradley_terry, h2h_external_probe
    protected = Path(__file__).parents[1] / "exports" / "eval_results.json"
    with pytest.raises(ContractError, match="exports/external"):
        h2h_external_probe._reject_repository_output(protected)
    with pytest.raises(Exception, match="exports/external"):
        fit_bradley_terry._reject_repository_output(protected)


def test_fit_cli_rejects_historical_external_input_after_active_sha_changes(tmp_path):
    source = Path(__file__).parents[1] / "exports" / "external" / "v48-seed101-smoke.json"
    output = tmp_path / "ratings.json"
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0", "--require-ab-ba"]) != 0
    assert not output.exists()


def test_fit_cli_rejects_redigested_forged_formal_input(tmp_path):
    payload = json.loads((Path(__file__).parents[1] / "exports" / "external" / "v48-seed101-smoke.json").read_text(encoding="utf-8"))
    payload["games"][0]["activity"]["seats"][0]["effective_commands"] += 1
    _redigest(payload)
    source = tmp_path / "forged.json"
    output = tmp_path / "ratings.json"
    source.write_text(json.dumps(payload), encoding="utf-8")
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0"]) != 0
    assert not output.exists()


def test_external_contract_rejects_forged_closure_algorithm(tmp_path):
    payload, _ = _fixture(tmp_path)
    payload["input_closure"]["algorithm"] = "forged-algorithm"
    _redigest(payload)
    with pytest.raises(ContractError, match="closure|algorithm"):
        validate_external_h2h(payload)


def test_external_cli_rejects_forged_provenance_payload(tmp_path):
    source = Path(__file__).parents[1] / "exports" / "external" / "v48-seed101-smoke.json"
    payload = json.loads(source.read_text(encoding="utf-8"))
    payload["opponents"][0]["provenance"]["author"] = "forged-author"
    _redigest(payload)
    forged = tmp_path / "forged.json"
    forged.write_text(json.dumps(payload), encoding="utf-8")
    from scripts import check_external_h2h
    assert check_external_h2h.main(["--input", str(forged)]) != 0


def test_external_runtime_closure_contains_canonical_import_chain():
    payload = json.loads((Path(__file__).parents[1] / "exports" / "external" / "v48-seed101-smoke.json").read_text(encoding="utf-8"))
    files = set(payload["input_closure"]["before"]["files"])
    for required in (
        "workspace/software/kgenv/arena.py",
        "workspace/software/kgenv/engine.py",
        "workspace/software/kgenv/eval_contract.py",
        "workspace/software/kgenv/__init__.py",
        "workspace/software/kgenv/economy.py",
        "workspace/software/kgenv/redlines.py",
        "workspace/software/kgenv/gym_env.py",
        "workspace/software/kgenv/elo.py",
    ):
        assert required in files
