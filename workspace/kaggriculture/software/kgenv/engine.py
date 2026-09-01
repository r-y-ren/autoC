"""Single-episode runner on the OFFICIAL kaggle-environments engine.

run_episode() plays two agents against each other on kaggriculture and
returns a structured result (winner / rewards / per-day money series).
Agents are plain callables f(obs) -> action dict, matching the official
Quick-Start agent signature; the strings "pass", "random" and "starter"
resolve to the engine's built-in agents.
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Union

from kaggle_environments import make

from kaggle_environments.envs.kaggriculture.kaggriculture import agents as builtin_agents

AgentRef = Union[str, Callable[[dict], dict]]

FULL_EPISODE_STEPS = 720  # 24 turns x 30 days (official default)


@dataclass(frozen=True)
class ActivityPolicy:
    """Liveness policy over DECISION actions, never automatic farm drift.

    Defaults (configurable, not hard-coded score constants): at least 5% of
    decisions must be non-PASS, no PASS run may exceed 96 decisions (two
    in-game days), pass-only is always fatal, and a zero reward delta is
    fatal ONLY combined with pass-only.  A score-tail baseline
    (min_reward_delta) can be enabled for release gates without touching
    the structural rules.  Effective state changes are reported as an
    audited metric; gating on them is opt-in (farm state can move for
    reasons a decision-liveness gate must not punish, e.g. opponent-driven
    market drift visible in shared state).
    """

    min_non_pass_ratio: float = 0.05
    max_pass_streak: int = 96
    min_reward_delta: float | None = None
    require_effective_state_change: bool = False


def _action_is_non_pass(action: Any) -> bool:
    if not isinstance(action, dict):
        return False
    unit_actions = [action.get("farmer", ["PASS"])]
    unit_actions.extend(action.get("hands", []) if isinstance(action.get("hands", []), list)
                        else [])
    market = action.get("market", [])
    if isinstance(market, list) and market:
        return True
    return any(isinstance(item, list) and item and item[0] != "PASS"
               for item in unit_actions)


def _longest_pass_streak(actions: List[Any]) -> int:
    streak = longest = 0
    for action in actions:
        if _action_is_non_pass(action):
            streak = 0
        else:
            streak += 1
            longest = max(longest, streak)
    return longest


def activity_diagnostics(*, states: int, seat_actions: List[List[Any]],
                         seat_state_changes: List[List[bool]],
                         rewards: List[float], starting_money: float,
                         policy: ActivityPolicy | None = None,
                         expected_states: int = FULL_EPISODE_STEPS) -> Dict[str, Any]:
    """Build auditable per-seat liveness diagnostics independent of completion."""
    policy = policy or ActivityPolicy()
    decisions = max(0, int(states) - 1)
    completion_ok = states == int(expected_states) and decisions == int(expected_states) - 1
    seats = []
    for seat in range(2):
        actions = seat_actions[seat] if seat < len(seat_actions) else []
        changes = seat_state_changes[seat] if seat < len(seat_state_changes) else []
        non_pass_trace = [_action_is_non_pass(action) for action in actions]
        state_change_trace = [bool(value) for value in changes]
        non_pass = sum(non_pass_trace)
        effective = sum(state_change_trace)
        reward_delta = float(rewards[seat]) - float(starting_money)
        pass_only = non_pass == 0
        ratio = non_pass / decisions if decisions else 0.0
        streak = _longest_pass_streak(actions)
        reasons = []
        if pass_only:
            reasons.append("pass_only")
            if reward_delta == 0:
                reasons.append("zero_reward_delta")
        if ratio < policy.min_non_pass_ratio:
            reasons.append("low_decision_coverage")
        if streak > policy.max_pass_streak:
            reasons.append("excessive_pass_streak")
        if policy.require_effective_state_change and effective == 0:
            reasons.append("no_effective_state_change")
        if policy.min_reward_delta is not None and reward_delta < policy.min_reward_delta:
            reasons.append("below_configured_reward_delta")
        seats.append({"non_pass_decisions": non_pass,
                      "non_pass_ratio": round(ratio, 4),
                      "longest_pass_streak": streak,
                      "effective_state_changes": effective,
                      "non_pass_trace": non_pass_trace,
                      "state_change_trace": state_change_trace,
                      "reward_delta": reward_delta, "pass_only": pass_only,
                      "failure_reasons": reasons})
    activity_ok = all(not seat["failure_reasons"] for seat in seats)
    return {"states": int(states), "decisions": decisions,
            "starting_money": float(starting_money),
            "completion_ok": completion_ok, "activity_ok": activity_ok,
            "ok": completion_ok and activity_ok, "policy": {
                "min_non_pass_ratio": policy.min_non_pass_ratio,
                "max_pass_streak": policy.max_pass_streak,
                "min_reward_delta": policy.min_reward_delta,
                "require_effective_state_change":
                    policy.require_effective_state_change,
            }, "seats": seats}


def _seat_state_changed(before: Any, after: Any, seat: int) -> bool:
    try:
        b = before["observation"]
        a = after["observation"]
        return (b["farms"][seat] != a["farms"][seat]
                or b.get("private") != a.get("private"))
    except (KeyError, IndexError, TypeError, AttributeError):
        return False


def _resolve(agent: AgentRef) -> Any:
    if isinstance(agent, str):
        if agent in builtin_agents:
            return builtin_agents[agent]
        raise ValueError(f"unknown built-in agent: {agent!r}")
    return agent


def _obs_dict(obs: Any) -> Dict[str, Any]:
    """Convert a kaggle Struct observation into a plain nested dict."""
    if hasattr(obs, "to_dict"):
        return obs.to_dict()
    if isinstance(obs, dict):
        return obs
    return dict(obs)


def run_episode(agent0: AgentRef, agent1: AgentRef, seed: int,
                episode_steps: int = FULL_EPISODE_STEPS,
                collect_daily: bool = True,
                act_timeout: float = 60.0) -> Dict[str, Any]:
    """Play one episode and return a structured match result.

    The episode is fully deterministic for a given (seed, agents) pair:
    weed spawns and town-shop draws are keyed off the episode seed.
    """
    t0 = time.perf_counter()
    env = make(
        "kaggriculture",
        configuration={"episodeSteps": int(episode_steps), "seed": int(seed),
                       "actTimeout": act_timeout},
        debug=True,
    )
    env.run([_resolve(agent0), _resolve(agent1)])
    elapsed = time.perf_counter() - t0

    final = env.steps[-1]
    rewards = [float(s["reward"]) for s in final]
    statuses = [s["status"] for s in final]
    seat_actions = [[], []]
    seat_changes = [[], []]
    for index in range(1, len(env.steps)):
        for seat in (0, 1):
            seat_actions[seat].append(env.steps[index][seat].get("action") or {})
            seat_changes[seat].append(
                _seat_state_changed(env.steps[index - 1][seat],
                                    env.steps[index][seat], seat))
    starting_money = float(getattr(env.configuration, "startingMoney", 3000))
    activity = activity_diagnostics(
        states=len(env.steps), seat_actions=seat_actions,
        seat_state_changes=seat_changes, rewards=rewards,
        starting_money=starting_money, expected_states=int(episode_steps))

    if statuses[0] != "DONE" or statuses[1] != "DONE":
        winner = None
        note = f"non-terminal statuses: {statuses}"
    elif rewards[0] > rewards[1]:
        winner, note = 0, ""
    elif rewards[1] > rewards[0]:
        winner, note = 1, ""
    else:
        winner, note = None, "tie"

    daily: List[Dict[str, Any]] = []
    if collect_daily:
        seen_steps = env.steps
        per_day: Dict[int, List[float]] = {}
        prices_per_day: Dict[int, Dict[str, int]] = {}
        for step_states in seen_steps:
            try:
                obs0 = step_states[0]["observation"]
                day = int(obs0.get("day", 0))
                farms = obs0.get("farms", [])
                if len(farms) >= 2:
                    money = [float(farms[0].get("money", 0.0)),
                             float(farms[1].get("money", 0.0))]
                    per_day[day] = money  # keep the last snapshot of each day
                    market = obs0.get("market", {}) or {}
                    prices_per_day[day] = dict(market.get("prices", {}) or {})
            except (KeyError, IndexError, AttributeError, TypeError):
                continue
        daily = [{"day": d, "money": per_day[d],
                  "prices": prices_per_day.get(d, {})} for d in sorted(per_day)]

    return {
        "seed": int(seed),
        "episode_steps": int(episode_steps),
        "rewards": rewards,
        "statuses": statuses,
        "winner": winner,
        "note": note,
        "turns_played": len(env.steps),
        "elapsed_seconds": round(elapsed, 3),
        "daily_money": daily,
        "activity": activity,
        "error_logs": [str(l) for l in getattr(env, "logs", []) if l] if hasattr(env, "logs") else [],
    }


def episode_contract_ok(result: Dict[str, Any]) -> bool:
    """Validate completion, and enforce liveness on release-length episodes."""
    activity = result.get("activity")
    release_activity_ok = (
        isinstance(activity, dict)
        and activity.get("completion_ok") is True
        and (result.get("episode_steps") != FULL_EPISODE_STEPS
             or activity.get("activity_ok") is True)
    )
    return (
        isinstance(result.get("rewards"), list)
        and len(result["rewards"]) == 2
        and all(isinstance(r, (int, float)) and not isinstance(r, bool)
                and math.isfinite(float(r)) for r in result["rewards"])
        and result.get("statuses") == ["DONE", "DONE"]
        and result.get("winner") in (0, 1, None)
        and isinstance(result.get("turns_played"), int)
        and result["turns_played"] == result.get("episode_steps")
        and release_activity_ok
    )
