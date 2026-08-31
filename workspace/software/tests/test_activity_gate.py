"""P0-D activity diagnostics and release-gate regressions."""

from __future__ import annotations

from kgenv.arena import load_submission_agent
from kgenv.engine import (
    ActivityPolicy,
    activity_diagnostics,
    episode_contract_ok,
    run_episode,
)
from smoke_boot import release_episode_ok


def _pass_only_result(states=720, reward=3000.0):
    decisions = states - 1
    activity = {
        "states": states,
        "decisions": decisions,
        "seats": [
            {"non_pass_decisions": 0, "effective_state_changes": 0,
             "reward_delta": 0.0, "pass_only": True,
             "failure_reasons": ["pass_only", "zero_reward_delta"]},
            {"non_pass_decisions": 0, "effective_state_changes": 0,
             "reward_delta": 0.0, "pass_only": True,
             "failure_reasons": ["pass_only", "zero_reward_delta"]},
        ],
        "ok": False,
    }
    return {"rewards": [reward, reward], "statuses": ["DONE", "DONE"],
            "winner": None, "turns_played": states, "episode_steps": 720,
            "activity": activity}


def test_done_done_3000_pass_only_is_rejected():
    result = _pass_only_result()
    assert episode_contract_ok(result) is False
    assert release_episode_ok(result, expected_steps=720) is False


def test_state_and_decision_boundaries_fail_closed():
    assert episode_contract_ok(_pass_only_result(states=718)) is False
    assert episode_contract_ok(_pass_only_result(states=719)) is False
    assert episode_contract_ok(_pass_only_result(states=720)) is False


def test_activity_policy_exposes_configurable_coverage_streak_and_tail():
    policy = ActivityPolicy(min_non_pass_ratio=0.2, max_pass_streak=10,
                            min_reward_delta=-100.0,
                            require_effective_state_change=True)
    assert policy.min_non_pass_ratio == 0.2
    assert policy.max_pass_streak == 10
    assert policy.min_reward_delta == -100.0
    assert policy.require_effective_state_change is True


def test_one_effective_action_then_all_pass_fails_on_coverage_and_streak():
    seat = [{"farmer": ["WATER"]}] + [{"farmer": ["PASS"]}] * 718
    diagnostics = activity_diagnostics(
        states=720,
        seat_actions=[seat, [{"farmer": ["PASS"]}] * 719],
        seat_state_changes=[[True] + [False] * 718, [False] * 719],
        rewards=[3050.0, 3000.0],   # non-zero delta: failure is coverage only
        starting_money=3000.0,
    )
    first = diagnostics["seats"][0]
    assert first["pass_only"] is False
    assert "low_decision_coverage" in first["failure_reasons"]
    assert "excessive_pass_streak" in first["failure_reasons"]
    assert diagnostics["activity_ok"] is False


def test_sustained_active_play_with_zero_reward_delta_is_not_a_failure():
    active = [{"farmer": ["WATER"]}] * 719
    diagnostics = activity_diagnostics(
        states=720,
        seat_actions=[active, active],
        seat_state_changes=[[True] * 719, [True] * 719],
        rewards=[3000.0, 3000.0],
        starting_money=3000.0,
    )
    assert diagnostics["activity_ok"] is True
    assert diagnostics["ok"] is True
    assert diagnostics["seats"][0]["failure_reasons"] == []


def test_pass_only_with_zero_delta_still_hard_fails():
    passes = [{"farmer": ["PASS"]}] * 719
    diagnostics = activity_diagnostics(
        states=720,
        seat_actions=[passes, passes],
        seat_state_changes=[[False] * 719, [False] * 719],
        rewards=[3000.0, 3000.0],
        starting_money=3000.0,
    )
    first = diagnostics["seats"][0]
    assert first["pass_only"] is True
    assert first["failure_reasons"][:2] == ["pass_only", "zero_reward_delta"]
    assert "low_decision_coverage" in first["failure_reasons"]
    assert diagnostics["ok"] is False


def test_configured_tail_gate_fails_low_reward_delta():
    active = [{"farmer": ["WATER"]}] * 719
    diagnostics = activity_diagnostics(
        states=720,
        seat_actions=[active, active],
        seat_state_changes=[[True] * 719, [True] * 719],
        rewards=[2800.0, 3000.0],
        starting_money=3000.0,
        policy=ActivityPolicy(min_reward_delta=-100.0),
    )
    assert "below_configured_reward_delta" in \
        diagnostics["seats"][0]["failure_reasons"]
    assert diagnostics["activity_ok"] is False


def test_real_engine_one_action_then_passes_fails_activity_gate():
    calls = [0, 0]

    def once_then_pass(obs):
        seat = obs["player"]
        calls[seat] += 1
        farmer = ["WEST"] if calls[seat] == 1 else ["PASS"]
        return {"farmer": farmer, "hands": [], "market": []}

    result = run_episode(once_then_pass, once_then_pass, seed=19,
                         episode_steps=720)
    assert result["turns_played"] == 720
    assert result["statuses"] == ["DONE", "DONE"]
    assert episode_contract_ok(result) is False
    for seat in result["activity"]["seats"]:
        assert seat["non_pass_decisions"] == 1
        assert "low_decision_coverage" in seat["failure_reasons"]
        assert "excessive_pass_streak" in seat["failure_reasons"]


def test_real_engine_sustained_commands_with_zero_delta_are_not_rejected():
    calls = [0, 0]

    def active_no_profit(obs):
        seat = obs["player"]
        calls[seat] += 1
        # WEST at x=0 is still command evidence even when the engine no-ops it.
        return {"farmer": ["WEST"], "hands": [], "market": []}

    result = run_episode(active_no_profit, active_no_profit, seed=23,
                         episode_steps=720)
    assert result["rewards"] == [3000.0, 3000.0]
    assert result["activity"]["ok"] is True
    assert episode_contract_ok(result) is True
    assert all(seat["non_pass_decisions"] == 719
               for seat in result["activity"]["seats"])


def test_normal_agent_full_game_passes_activity_gate_both_seats():
    agent = load_submission_agent()
    result = run_episode(agent, agent, seed=9, episode_steps=720)
    assert result["turns_played"] == 720
    assert result["activity"]["decisions"] == 719
    assert result["activity"]["ok"] is True
    assert episode_contract_ok(result) is True
    for seat in result["activity"]["seats"]:
        assert seat["non_pass_decisions"] > 0
        assert seat["effective_state_changes"] > 0
        assert seat["pass_only"] is False
        assert seat["failure_reasons"] == []


def test_activity_diagnostics_separates_completion_from_liveness():
    diagnostics = activity_diagnostics(
        states=720,
        seat_actions=[[{"farmer": ["PASS"]}] * 719] * 2,
        seat_state_changes=[[False] * 719] * 2,
        rewards=[3000.0, 3000.0],
        starting_money=3000.0,
    )
    assert diagnostics["states"] == 720
    assert diagnostics["decisions"] == 719
    assert diagnostics["completion_ok"] is True
    assert diagnostics["activity_ok"] is False
    assert diagnostics["ok"] is False
    assert diagnostics["seats"][0]["failure_reasons"][:2] == [
        "pass_only", "zero_reward_delta"
    ]
