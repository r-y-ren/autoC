"""Arena: match running, submission loading, and replay logs.

Loads the submittable main.py exactly the way the Kaggle Validation Episode
would (file-based agent), runs matches on the official engine, and writes
one JSON replay-log entry per game (复盘日志) for post-hoc analysis with the
redline checker.
"""

from __future__ import annotations

import importlib.util
import json
import os
from typing import Any, Callable, Dict, List, Optional

from .engine import AgentRef, run_episode, episode_contract_ok, FULL_EPISODE_STEPS

SOFTWARE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBMISSION_MAIN = os.path.join(SOFTWARE_ROOT, "kaggle_simulations", "agent", "main.py")


def load_submission_agent(path: str = SUBMISSION_MAIN) -> Callable[[dict], dict]:
    """Import main.py from its file path and return its last-defined callable.

    This mirrors kaggle_environments.agent.get_last_callable semantics (the
    submission entry point), without going through the agent process runner.
    """
    path = os.path.abspath(path)
    spec = importlib.util.spec_from_file_location(f"submission_{abs(hash(path))}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    candidates = [v for k, v in vars(module).items()
                  if callable(v) and getattr(v, "__module__", None) == module.__name__]
    named = getattr(module, "agent", None)
    if callable(named):
        return named
    if candidates:
        return candidates[-1]
    raise ValueError(f"no agent callable found in {path}")


def run_match(a: AgentRef, b: AgentRef, seed: int,
              episode_steps: int = FULL_EPISODE_STEPS,
              label_a: str = "A", label_b: str = "B",
              collect_daily: bool = True) -> Dict[str, Any]:
    """Run one rated match and tag it with contender names."""
    res = run_episode(a, b, seed, episode_steps=episode_steps,
                      collect_daily=collect_daily)
    winner_label = None
    if res["winner"] == 0:
        winner_label = label_a
    elif res["winner"] == 1:
        winner_label = label_b
    res["players"] = [label_a, label_b]
    res["winner_label"] = winner_label
    res["contract_ok"] = episode_contract_ok(res)
    return res


def write_replay_log(out_dir: str, results: List[Dict[str, Any]],
                     filename: str = "replay_log.jsonl") -> str:
    """Persist one JSON line per game (复盘日志)."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, filename)
    with open(path, "w", encoding="utf-8") as f:
        for r in results:
            entry = {
                "players": r.get("players"),
                "winner": r.get("winner_label"),
                "seed": r.get("seed"),
                "rewards": r.get("rewards"),
                "turns": r.get("turns_played"),
                "episode_steps": r.get("episode_steps"),
                "elapsed_seconds": r.get("elapsed_seconds"),
                "daily_money": [d.get("money") for d in (r.get("daily_money") or [])],
                "daily_prices": [d.get("prices") for d in (r.get("daily_money") or [])],
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return path


def summarize_games(games: List[Dict[str, Any]], a: str, b: str) -> Dict[str, Any]:
    """Head-to-head W/L/T (from a's perspective) + timing stats."""
    w = l = t = 0
    turns: List[int] = []
    for g in games:
        if g.get("players") != [a, b]:
            continue
        if g["winner_label"] == a:
            w += 1
        elif g["winner_label"] == b:
            l += 1
        else:
            t += 1
        turns.append(g["turns_played"])
    n = w + l + t
    return {
        "pair": f"{a} vs {b}",
        "games": n,
        "wins": w,
        "losses": l,
        "ties": t,
        "win_rate": round((w + 0.5 * t) / n, 4) if n else None,
        "avg_turns": round(sum(turns) / len(turns), 1) if turns else None,
    }
