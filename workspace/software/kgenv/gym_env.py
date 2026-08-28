"""Gym-style single-agent wrapper around the official kaggriculture engine.

Provides the classic reset()/step() loop for one learning agent while an
opponent policy (callable or engine built-in name) acts on the other side.
This is a thin adapter -- all dynamics remain the OFFICIAL engine's.

Usage:
    env = KaggricultureGym(opponent="starter", episode_steps=720)
    obs = env.reset(seed=42)
    for _ in range(720):
        action = my_policy(env.observation)
        obs, reward, terminated, info = env.step(action)
        if terminated:
            break
"""

from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Union

from kaggle_environments import make
from kaggle_environments.envs.kaggriculture.kaggriculture import agents as builtin_agents

from .engine import FULL_EPISODE_STEPS, _obs_dict, _resolve

Action = Dict[str, Any]


class KaggricultureGym:
    """Gym-style environment: control player 0, opponent plays player 1."""

    metadata = {"render_modes": ["ansi"]}

    def __init__(self, opponent: Union[str, Callable[[dict], Action]] = "pass",
                 episode_steps: int = FULL_EPISODE_STEPS,
                 act_timeout: float = 60.0):
        self.opponent = _resolve(opponent)
        self.episode_steps = int(episode_steps)
        self.act_timeout = act_timeout
        self._env = make(
            "kaggriculture",
            configuration={"episodeSteps": self.episode_steps, "actTimeout": act_timeout},
            debug=True,
        )
        self.observation: Optional[Dict[str, Any]] = None
        self.last_info: Dict[str, Any] = {}

    # ---------------------------------------------------------------- api
    @property
    def action_space(self) -> Dict[str, Any]:
        """Discrete-ish description of the joint action (not a gym.Space).

        Kept lightweight: farmer/hands unit ops plus market order ops, as in
        the official How-to-Play Actions section.
        """
        return {
            "type": "dict",
            "fields": {
                "farmer": ["NORTH", "SOUTH", "EAST", "WEST", "PLANT", "WATER",
                           "HARVEST", "FERTILIZE", "DIG", "BUILD_COOP",
                           "BUILD_PASTURE", "FEED", "CARE", "COLLECT_FERTILIZER",
                           "PICKUP", "DROP", "PLACE", "PASS"],
                "hands": "list of per-hand action lists (same ops as farmer)",
                "market": ["BUY_SEED", "BUY_ANIMAL", "BUY_PRODUCT", "SELL",
                           "HIRE", "BUY_LAND"],
            },
        }

    def reset(self, seed: Optional[int] = None) -> Dict[str, Any]:
        if seed is not None:
            self._env = make(
                "kaggriculture",
                configuration={"episodeSteps": self.episode_steps,
                               "seed": int(seed), "actTimeout": self.act_timeout},
                debug=True,
            )
        else:
            self._env.reset()
        obs0 = self._env.steps[0][0]["observation"]
        self.observation = _obs_dict(obs0)
        self.last_info = {"step": 0}
        return self.observation

    def step(self, action: Action) -> tuple:
        """Advance one turn with our action for player 0.

        The opponent observes the same pre-turn state and acts through its
        policy; both actions then hit the official interpreter together.
        """
        obs_struct = self._env.steps[-1][0]["observation"]
        obs_for_opp = _obs_dict(self._env.steps[-1][1]["observation"])
        opp_action = self.opponent(obs_for_opp) if callable(self.opponent) \
            else {"farmer": ["PASS"], "hands": [], "market": []}

        self._env.step([_sanitize(action), _sanitize(opp_action)])

        states = self._env.steps[-1]
        obs0 = states[0]["observation"]
        self.observation = _obs_dict(obs0)
        reward = float(states[0]["reward"] or 0.0)
        terminated = states[0]["status"] in ("DONE", "INVALID")
        money = [float(f.get("money", 0.0)) for f in (obs0.get("farms") or [])]
        self.last_info = {
            "step": int(obs0.get("step", len(self._env.steps))),
            "day": int(obs0.get("day", 0)),
            "hour": int(obs0.get("hour", 0)),
            "money": money,
            "status": states[0]["status"],
        }
        return self.observation, reward, terminated, self.last_info

    def render(self, mode: str = "ansi") -> str:
        if mode != "ansi":
            raise ValueError("only 'ansi' render mode is available in the headless vendor build")
        return self._env.render(mode="ansi")


def _sanitize(action: Any) -> Any:
    """Keep the action JSON-friendly (Struct -> dict fallback handled upstream)."""
    if isinstance(action, dict):
        return action
    return {"farmer": ["PASS"], "hands": [], "market": []}
