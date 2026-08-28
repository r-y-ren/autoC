"""Single-episode runner on the OFFICIAL kaggle-environments engine.

run_episode() plays two agents against each other on kaggriculture and
returns a structured result (winner / rewards / per-day money series).
Agents are plain callables f(obs) -> action dict, matching the official
Quick-Start agent signature; the strings "pass", "random" and "starter"
resolve to the engine's built-in agents.
"""

from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional, Union

from kaggle_environments import make

from kaggle_environments.envs.kaggriculture.kaggriculture import agents as builtin_agents

AgentRef = Union[str, Callable[[dict], dict]]

FULL_EPISODE_STEPS = 720  # 24 turns x 30 days (official default)


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
        "error_logs": [str(l) for l in getattr(env, "logs", []) if l] if hasattr(env, "logs") else [],
    }


def episode_contract_ok(result: Dict[str, Any]) -> bool:
    """Validate a run_episode result against the output contract."""
    return (
        isinstance(result.get("rewards"), list)
        and len(result["rewards"]) == 2
        and all(isinstance(r, (int, float)) for r in result["rewards"])
        and result.get("statuses") == ["DONE", "DONE"]
        and result.get("winner") in (0, 1, None)
        and isinstance(result.get("turns_played"), int)
        and result["turns_played"] > 0
    )
