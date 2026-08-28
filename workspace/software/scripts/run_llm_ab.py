"""Seat-balanced LLM A/B harness with per-game provider budgets."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import SOFTWARE_ROOT as ARENA_ROOT, SUBMISSION_MAIN, run_match
from kgenv.bots.llm_provider import provider_from_env
from kgenv.engine import FULL_EPISODE_STEPS

OUT_PATH = os.path.join(SOFTWARE_ROOT, "exports", "llm_ab_results.json")
REQUIRED_ENV = ("KG_LLM_PROVIDER", "KG_LLM_BASE_URL", "KG_LLM_API_KEY",
                "KG_LLM_MODEL")


def load_side():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"submission_ab_{time.perf_counter_ns()}", SUBMISSION_MAIN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Instrumented:
    def __init__(self, inner):
        self.inner = inner
        self.calls = 0
        self.effective_calls = 0
        self.fallbacks = 0
        self.budget_blocks = 0

    def suggest(self, prompt, context):
        budget = getattr(self.inner, "budget", None)
        if budget is not None and budget.exhausted:
            self.budget_blocks += 1
            return None
        self.calls += 1
        answer = self.inner.suggest(prompt, context)
        if answer is None:
            self.fallbacks += 1
        else:
            self.effective_calls += 1
        return answer

    @property
    def name(self):
        return getattr(self.inner, "name", "unknown")


@dataclass
class GameContext:
    on_agent: Callable
    off_agent: Callable
    provider: Instrumented
    configured: bool


def create_game_context(factory=provider_from_env) -> GameContext:
    """Create independent modules, provider, and budget for one episode."""
    inner = factory()
    provider = Instrumented(inner)
    module_on = load_side()
    module_on.LLM_PROVIDER = provider
    module_off = load_side()
    module_off.LLM_PROVIDER = None
    return GameContext(
        on_agent=module_on.agent,
        off_agent=module_off.agent,
        provider=provider,
        configured=bool(getattr(inner, "configured", False)),
    )


def _game_stats(context: GameContext) -> dict:
    budget = getattr(context.provider.inner, "budget", None)
    return {
        "provider": context.provider.name,
        "configured": context.configured,
        "suggest_calls": context.provider.calls,
        "effective_calls": context.provider.effective_calls,
        "heuristic_fallbacks": context.provider.fallbacks,
        "budget_gate_blocks": context.provider.budget_blocks,
        "budget": None if budget is None else {
            "max_calls": budget.max_calls,
            "max_seconds": budget.max_seconds,
            "calls_spent": budget.calls,
            "seconds_spent": round(budget.seconds, 3),
        },
    }


def qualifies_as_real_ab(per_game_stats: list[dict]) -> bool:
    """A real A/B requires a configured provider response in every episode."""
    return bool(per_game_stats) and all(
        stat["configured"] and stat["effective_calls"] > 0
        for stat in per_game_stats
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rounds", type=int, default=4)
    parser.add_argument("--first-seed", type=int, default=701)
    args = parser.parse_args()
    seeds = list(range(args.first_seed, args.first_seed + max(1, args.rounds)))

    games = []
    per_game_stats = []
    started = time.perf_counter()
    for seed in seeds:
        for seat in ("AB", "BA"):
            context = create_game_context()
            if seat == "AB":
                result = run_match(context.on_agent, context.off_agent, seed=seed,
                                   label_a="llm_on", label_b="llm_off",
                                   episode_steps=FULL_EPISODE_STEPS,
                                   collect_daily=False)
                on_index = 0
            else:
                result = run_match(context.off_agent, context.on_agent, seed=seed,
                                   label_a="llm_off", label_b="llm_on",
                                   episode_steps=FULL_EPISODE_STEPS,
                                   collect_daily=False)
                on_index = 1
            result["seat"] = seat
            result["llm_on_index"] = on_index
            stats = _game_stats(context)
            per_game_stats.append({"seed": seed, "seat": seat, **stats})
            games.append(result)
            print(f"seed={seed} seat={seat}: llm_on={result['rewards'][on_index]:.0f} "
                  f"llm_off={result['rewards'][1 - on_index]:.0f} "
                  f"winner={result['winner_label']} calls={stats['suggest_calls']} "
                  f"effective={stats['effective_calls']}")

    wins = sum(game["winner_label"] == "llm_on" for game in games)
    losses = sum(game["winner_label"] == "llm_off" for game in games)
    ties = sum(game["winner_label"] is None for game in games)
    margins = [game["rewards"][game["llm_on_index"]] -
               game["rewards"][1 - game["llm_on_index"]] for game in games]
    configured_all = bool(per_game_stats) and all(
        stat["configured"] for stat in per_game_stats)
    effective_calls = sum(stat["effective_calls"] for stat in per_game_stats)
    real_ab = qualifies_as_real_ab(per_game_stats)
    count = len(games)
    result = {
        "schema_version": "2.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": per_game_stats[0]["provider"] if per_game_stats else "unknown",
        "provider_configured": configured_all,
        "real_ab": real_ab,
        "config_env": {key: bool(os.environ.get(key)) for key in REQUIRED_ENV},
        "rounds": len(seeds),
        "seeds": seeds,
        "seat_orders": ["AB", "BA"],
        "games": count,
        "llm_on": {
            "wins": wins,
            "losses": losses,
            "ties": ties,
            "avg_margin": round(sum(margins) / count, 2) if count else None,
        },
        "win_rate_llm_on": (round((wins + 0.5 * ties) / count, 4)
                            if real_ab and count else None),
        "consultation_stats": {
            "suggest_calls": sum(stat["suggest_calls"] for stat in per_game_stats),
            "effective_calls": effective_calls,
            "heuristic_fallbacks": sum(
                stat["heuristic_fallbacks"] for stat in per_game_stats),
            "budget_gate_blocks": sum(
                stat["budget_gate_blocks"] for stat in per_game_stats),
        },
        "per_game_consultation_stats": per_game_stats,
        "note": ("real A/B: every game used an independently configured provider "
                 "and recorded at least one effective provider response" if real_ab else
                 "Null/incomplete/no-effective-call provider run: plumbing only; "
                 "win_rate is null and no real A/B conclusion is permitted"),
        "runtime_seconds": round(time.perf_counter() - started, 2),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as stream:
        json.dump(result, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    print(f"provider={result['provider']} configured={configured_all} "
          f"real_ab={real_ab} games={count} win_rate={result['win_rate_llm_on']}")
    print(f"wrote {os.path.relpath(OUT_PATH, ARENA_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
