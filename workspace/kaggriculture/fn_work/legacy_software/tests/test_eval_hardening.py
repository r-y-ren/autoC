"""m2a evaluation-fidelity regressions."""

from __future__ import annotations

import json

import pytest

from kgenv import arena
from kgenv.eval_contract import (
    ContractError,
    STANDARD_MATRIX_ORDER,
    atomic_publish_bundle,
    atomic_publish_json,
    build_ab_ba_schedule,
    canonical_sha256,
    file_sha256,
    game_abnormal_reason,
    order_independent_standings,
    resolve_output_path,
    validate_eval_result,
    validate_gate_run,
    validate_seed_domain,
)
from kgenv.variance import margin_stats, t95


def _game(p0: str, p1: str, seed: int, seat: str = "AB", winner=None,
          rewards=None) -> dict:
    winner = p0 if winner is None else winner
    rewards = [2.0, 1.0] if rewards is None else rewards
    return {
        "players": [p0, p1],
        "p0": p0,
        "p1": p1,
        "seed": seed,
        "seat": seat,
        "seed_domain": "development",
        "statuses": ["DONE", "DONE"],
        "contract_ok": True,
        "winner_label": winner,
        "winner": winner,
        "rewards": rewards,
        "turns_played": 720,
        "turns": 720,
        "episode_steps": 720,
        "elapsed_seconds": 0.1,
    }


def test_schedule_contains_ab_and_ba_for_every_pair_seed():
    schedule = build_ab_ba_schedule([("cand", "opp")], [301, 302], "holdout")
    assert [(g["p0"], g["p1"], g["seed"], g["seat"]) for g in schedule] == [
        ("cand", "opp", 301, "AB"),
        ("opp", "cand", 301, "BA"),
        ("cand", "opp", 302, "AB"),
        ("opp", "cand", 302, "BA"),
    ]
    assert {g["seed_domain"] for g in schedule} == {"holdout"}


@pytest.mark.parametrize("seed", [101, 104, 201, 208])
def test_known_development_and_regression_seeds_cannot_be_holdout(seed):
    with pytest.raises(ContractError, match="holdout"):
        validate_seed_domain([seed], "holdout")


def test_episode_contract_rejects_early_done_result():
    from kgenv.engine import episode_contract_ok

    result = {
        "rewards": [1.0, 0.0], "statuses": ["DONE", "DONE"],
        "winner": 0, "turns_played": 719, "episode_steps": 720,
    }
    assert episode_contract_ok(result) is False


def test_run_match_raises_instead_of_turning_invalid_episode_into_tie(monkeypatch):
    invalid = {
        "seed": 1,
        "episode_steps": 720,
        "rewards": [0.0, 0.0],
        "statuses": ["INVALID", "DONE"],
        "winner": None,
        "note": "timeout",
        "turns_played": 1,
        "elapsed_seconds": 60.0,
        "daily_money": [],
        "error_logs": ["timeout"],
    }
    monkeypatch.setattr(arena, "run_episode", lambda *args, **kwargs: invalid.copy())
    with pytest.raises(arena.AbnormalMatchError, match="INVALID"):
        arena.run_match("pass", "pass", seed=1)


def test_summarizer_rejects_contract_failure_instead_of_counting_tie():
    bad = _game("a", "b", 101)
    bad.update(contract_ok=False, winner_label=None)
    with pytest.raises(arena.AbnormalMatchError, match="contract"):
        arena.summarize_games([bad], "a", "b")


def test_complete_gate_requires_full_development_seed_domain():
    games = []
    opponents = ["cow_baron", "melon_hoarder", "expansionist", "baseline_wheat"]
    for opponent in opponents:
        games.extend([_game("cand", opponent, 101, "AB"),
                      _game(opponent, "cand", 101, "BA")])
    with pytest.raises(ContractError, match="101-104|development seeds"):
        validate_gate_run(games, opponents, [101], require_complete=True)


def test_complete_gate_requires_all_opponents_both_seats_and_expected_games():
    opponents = ["cow_baron", "melon_hoarder", "expansionist", "baseline_wheat"]
    seeds = [101, 102, 103, 104]
    games = []
    for opponent in opponents:
        for seed in seeds:
            games.extend([
                _game("cand", opponent, seed, "AB"),
                _game(opponent, "cand", seed, "BA"),
            ])
    report = validate_gate_run(games, opponents, seeds, require_complete=True)
    assert report["complete"] is True
    assert report["expected_games"] == 32
    with pytest.raises(ContractError, match="expected|seat|schedule"):
        validate_gate_run(games[:-1], opponents, seeds, require_complete=True)


def test_exploratory_subset_can_never_be_formal_pass():
    games = [_game("cand", "cow_baron", 101, "AB"),
             _game("cow_baron", "cand", 101, "BA")]
    report = validate_gate_run(games, ["cow_baron"], [101], require_complete=False)
    assert report["mode"] == "exploratory"
    assert report["formal_pass"] is False


def test_quick_output_cannot_target_formal_export(tmp_path):
    from scripts.run_eval import resolve_output_path

    formal = tmp_path / "eval_results.json"
    with pytest.raises(ContractError, match="quick|development"):
        resolve_output_path(False, str(formal), str(tmp_path))
    assert resolve_output_path(False, "", str(tmp_path)).endswith("eval_results.dev.json")


def test_atomic_publish_preserves_previous_file_when_validation_fails(tmp_path):
    target = tmp_path / "eval_results.json"
    target.write_text('{"old": true}\n', encoding="utf-8")
    with pytest.raises(ContractError):
        atomic_publish_json(target, {"new": True}, lambda _: (_ for _ in ()).throw(
            ContractError("semantic failure")))
    assert json.loads(target.read_text(encoding="utf-8")) == {"old": True}
    assert not list(tmp_path.glob("*.tmp"))


def test_atomic_publish_replaces_only_after_validation(tmp_path):
    target = tmp_path / "eval_results.json"
    target.write_text('{"old": true}\n', encoding="utf-8")
    atomic_publish_json(target, {"new": True}, lambda payload: payload["new"])
    assert json.loads(target.read_text(encoding="utf-8")) == {"new": True}


def test_confirmatory_standings_are_independent_of_game_order():
    games = [_game("a", "b", 101, "AB"), _game("b", "a", 101, "BA")]
    games[0].update(winner_label="a", winner="a", rewards=[2.0, 1.0])
    games[1].update(winner_label="a", winner="a", rewards=[1.0, 2.0])
    games.extend([_game("b", "c", 102, "AB"), _game("c", "b", 102, "BA")])
    games[2].update(winner_label="b", winner="b", rewards=[2.0, 1.0])
    games[3].update(winner_label="b", winner="b", rewards=[1.0, 2.0])
    assert order_independent_standings(games) == order_independent_standings(
        list(reversed(games)))
    assert order_independent_standings(games)[0]["name"] == "a"


def test_official_rejects_self_reported_single_pair_and_seed():
    evaluation_input = {
        "pairs": [["submission", "opp"]],
        "seeds": [101],
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
    }
    payload = {
        "schema_version": "2.0", "run_kind": "official", "seed_domain": "development",
        "evaluation_input": evaluation_input,
        "identity": {"submission_path": "main.py", "submission_sha256": "a" * 64,
                     "git_ref": "deadbeef", "dirty": False,
                     "input_sha256": canonical_sha256(evaluation_input)},
        "config": {"seeds": [101], "pairs": [["submission", "opp"]],
                   "expected_games": 2, "seat_orders": ["AB", "BA"]},
    }
    with pytest.raises(ContractError, match="standard|matrix|official"):
        validate_eval_result(payload, require_official=True)


def test_eval_semantics_reject_cross_field_totals_and_identity_hash():
    evaluation_input = {
        "pairs": [["submission", "opp"]],
        "seeds": [101],
        "seed_domain": "development",
        "seat_orders": ["AB", "BA"],
    }
    games = [
        {**_game("submission", "opp", 101, "AB"),
         "p0": "submission", "p1": "opp", "winner": "submission",
         "turns": 720, "elapsed_seconds": 0.1},
        {**_game("opp", "submission", 101, "BA"),
         "p0": "opp", "p1": "submission", "winner": "opp",
         "turns": 720, "elapsed_seconds": 0.1},
    ]
    payload = {
        "schema_version": "2.0",
        "run_kind": "development",
        "seed_domain": "development",
        "evaluation_input": evaluation_input,
        "identity": {
            "submission_path": "main.py",
            "submission_sha256": "a" * 64,
            "git_ref": "deadbeef",
            "dirty": False,
            "input_sha256": canonical_sha256(evaluation_input),
        },
        "config": {"seeds": [101], "pairs": [["submission", "opp"]],
                   "expected_games": 2, "seat_orders": ["AB", "BA"]},
        "games": games,
        "head_to_head": [{"pair": "submission vs opp", "games": 2,
                          "wins": 1, "losses": 1, "ties": 0,
                          "win_rate": 0.5, "avg_turns": 720.0}],
        "abnormal_games": 0,
        "integrity": {"expected_games": 2, "actual_games": 2, "abnormal_games": 0},
        "confirmatory": {"method": "paired seat-balanced W/L/T", "order_independent": True},
        "elo": {"role": "descriptive_only", "order_sensitive": True,
                "k": 32.0, "start": 1200.0, "table": []},
        "failure_modes": None,
    }
    validate_eval_result(payload, require_official=False)
    payload["head_to_head"][0]["wins"] = 2
    with pytest.raises(ContractError, match="head_to_head"):
        validate_eval_result(payload, require_official=False)
    payload["head_to_head"][0]["wins"] = 1
    payload["identity"]["input_sha256"] = "0" * 64
    with pytest.raises(ContractError, match="input_sha256"):
        validate_eval_result(payload, require_official=False)


def test_malformed_game_fields_and_fake_tie_are_rejected():
    missing = _game("a", "b", 101)
    del missing["contract_ok"]
    assert "contract_ok" in game_abnormal_reason(missing)
    fake_tie = _game("a", "b", 101, rewards=[3.0, 2.0])
    fake_tie.update(winner=None, winner_label=None)
    assert "inconsistent" in (game_abnormal_reason(fake_tie) or "")
    with pytest.raises(ContractError, match="winner|tie|rewards"):
        validate_gate_run([fake_tie], ["b"], [101], False)


def test_resolve_output_path_rejects_case_alias_on_windows():
    with pytest.raises(ContractError, match="formal"):
        resolve_output_path(False, "C:/tmp/EVAL_RESULTS.JSON", "C:/tmp")


def test_atomic_bundle_rolls_back_both_outputs_when_replay_validation_fails(tmp_path):
    export = tmp_path / "eval_results.json"
    replay = tmp_path / "replay_log.jsonl"
    export.write_text("old-export", encoding="utf-8")
    replay.write_text("old-replay", encoding="utf-8")
    with pytest.raises(ContractError):
        atomic_publish_bundle(
            [(export, b"new-export"), (replay, b"new-replay")],
            lambda: (_ for _ in ()).throw(ContractError("replay failure")))
    assert export.read_text(encoding="utf-8") == "old-export"
    assert replay.read_text(encoding="utf-8") == "old-replay"


def test_run_eval_summarizer_rejects_abnormal_game():
    from scripts import run_eval

    bad = _game("a", "b", 101)
    bad.update(statuses=["INVALID", "DONE"], contract_ok=False,
               winner=None, winner_label=None, rewards=[0.0, 0.0])
    with pytest.raises(ContractError, match="abnormal|non-DONE"):
        run_eval.summarize_pair([bad], "a", "b")


def test_iterate_gate_verifies_identity_after_incumbent_games(monkeypatch, tmp_path):
    import contextlib
    import sys
    from scripts import iterate_gate

    events = []
    candidate = tmp_path / "candidate.py"
    candidate.write_text("def agent(obs): return {}\n", encoding="utf-8")

    class Snapshot:
        snapshot_path = candidate
        identity = {"submission_sha256": "a" * 64, "git_ref": "x",
                    "dirty": False, "input_sha256": "b" * 64}

        def verify_unchanged(self):
            events.append("verify")

        def verify_candidate_unchanged(self):
            events.append("verify_candidate")

    @contextlib.contextmanager
    def fake_snapshot(*args, **kwargs):
        events.append("snapshot")
        yield Snapshot()

    def fake_play(*args, **kwargs):
        events.append("play")
        return []

    summaries = {
        name: {"games": 0, "wins": 0, "losses": 0, "ties": 0,
               "win_rate": 1.0, "avg_margin": 0.0, "min_margin": 0.0,
               "seats": {"AB": 0, "BA": 0}}
        for name in iterate_gate.REQUIRED_OPPONENTS
    }
    gate = {"formal_pass": True, "mode": "official", "expected_games": 32,
            "actual_games": 32, "abnormal_games": 0}

    monkeypatch.setattr(iterate_gate, "candidate_snapshot", fake_snapshot)
    monkeypatch.setattr(iterate_gate, "load_submission_agent", lambda path: object())
    monkeypatch.setattr(iterate_gate, "play_set", fake_play)
    monkeypatch.setattr(iterate_gate, "gate_verdict", lambda *args: (dict(summaries), dict(gate)))
    monkeypatch.setattr(
        sys, "argv",
        ["iterate_gate.py", "--candidate", str(candidate), "--vs-incumbent",
         "--no-log", "--require-complete"],
    )

    assert iterate_gate.main() == 0
    assert events.count("play") == 2
    assert events.index("verify") > max(i for i, event in enumerate(events) if event == "play")
    assert events[-1] == "verify_candidate"


def test_iterate_gate_allows_its_atomic_log_then_rechecks_candidate(monkeypatch, tmp_path):
    import contextlib
    import sys
    from scripts import iterate_gate

    events = []
    candidate = tmp_path / "candidate.py"
    candidate.write_text("def agent(obs): return {}\n", encoding="utf-8")
    log_path = tmp_path / "iteration_gate_log.jsonl"
    log_path.write_text('{"old": true}\n', encoding="utf-8")

    class Snapshot:
        snapshot_path = candidate
        identity = {"submission_sha256": "a" * 64, "git_ref": "x",
                    "dirty": False, "input_sha256": "b" * 64}

        def verify_unchanged(self):
            events.append("verify")

        def verify_candidate_unchanged(self):
            events.append("verify_candidate")

    @contextlib.contextmanager
    def fake_snapshot(*args, **kwargs):
        yield Snapshot()

    summaries = {
        name: {"games": 0, "wins": 0, "losses": 0, "ties": 0,
               "win_rate": 1.0, "avg_margin": 0.0, "min_margin": 0.0,
               "seats": {"AB": 0, "BA": 0}}
        for name in iterate_gate.REQUIRED_OPPONENTS
    }
    gate = {"formal_pass": True, "mode": "official", "expected_games": 32,
            "actual_games": 32, "abnormal_games": 0}

    monkeypatch.setattr(iterate_gate, "LOG_PATH", str(log_path))
    monkeypatch.setattr(iterate_gate, "candidate_snapshot", fake_snapshot)
    monkeypatch.setattr(iterate_gate, "load_submission_agent", lambda path: object())
    monkeypatch.setattr(iterate_gate, "play_set", lambda *args, **kwargs: [])
    monkeypatch.setattr(iterate_gate, "gate_verdict", lambda *args: (summaries, gate))
    monkeypatch.setattr(
        sys, "argv", ["iterate_gate.py", "--candidate", str(candidate),
                      "--require-complete"],
    )

    assert iterate_gate.main() == 0
    assert events[-2:] == ["verify", "verify_candidate"]
    lines = log_path.read_text(encoding="utf-8").splitlines()
    assert json.loads(lines[0]) == {"old": True}
    assert json.loads(lines[1])["verdict"] == "PASS"
    assert not list(tmp_path.glob("*.tmp"))


def test_t95_uses_correct_intermediate_degrees_of_freedom():
    assert t95(12) == pytest.approx(2.201, rel=1e-3)
    assert t95(15) == pytest.approx(2.145, rel=1e-3)


def test_single_observation_margin_ci_is_null():
    stats = margin_stats([42.0])
    assert stats["std"] is None
    assert stats["ci95_lo"] is None
    assert stats["ci95_hi"] is None


def test_llm_game_context_rebuilds_provider_and_budget_per_game():
    from scripts.run_llm_ab import create_game_context

    created = []

    class FakeProvider:
        name = "fake"

        def __init__(self):
            from kgenv.bots.llm_provider import Budget
            self.budget = Budget(2, 1.0)

        @property
        def configured(self):
            return True

        def suggest(self, prompt, context):
            return None

    def factory():
        provider = FakeProvider()
        created.append(provider)
        return provider

    first = create_game_context(factory)
    first.provider.inner.budget.spend(0.1)
    second = create_game_context(factory)
    assert len(created) == 2
    assert first.provider is not second.provider
    assert first.provider.inner.budget.calls == 1
    assert second.provider.inner.budget.calls == 0


def test_llm_provider_configuration_requires_all_real_provider_inputs():
    from kgenv.bots.llm_provider import OpenAICompatProvider

    provider = OpenAICompatProvider(base_url="https://example.test", api_key="", model="m")
    assert provider.configured is False
    provider = OpenAICompatProvider(base_url="https://example.test", api_key="k", model="m")
    assert provider.configured is True
