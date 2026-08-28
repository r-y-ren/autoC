"""LLM A/B harness (m2 acceptance item m2-ab): same-seed head-to-head of the
submission with the optional LLM consultant ON vs OFF.

Usage (one command):
    python scripts/run_llm_ab.py [--rounds 4] [--first-seed 701]

Mechanics:
  * loads TWO independent module instances of kaggle_simulations/agent/main.py
    (importlib keeps them separate), sets LLM_PROVIDER on the "on" side to
    kgenv.bots.llm_provider.provider_from_env() and leaves the "off" side
    at None (the shipped default);
  * plays 2*N games (both seat orders, same seeds) at full episode length;
  * instruments the provider: suggest() call count, heuristic-fallback
    count (provider returned None/invalid), and budget-gate hits (calls
    blocked by the Reasonableness-Standard budget);
  * writes exports/llm_ab_results.json and prints a summary.

Honest-null semantics: without KG_LLM_* environment variables the factory
returns NullProvider (disabled) -- the "A" side then plays the identical
heuristic policy, so win_rate is reported as null (not a real A/B) while
games/budget/fallback counters still evidence that the harness plumbing,
budget gate and fallback path all work. No numbers are invented.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import (SOFTWARE_ROOT as ARENA_ROOT, SUBMISSION_MAIN,
                         run_match)
from kgenv.bots.llm_provider import NullProvider, provider_from_env
from kgenv.engine import FULL_EPISODE_STEPS

OUT_PATH = os.path.join(SOFTWARE_ROOT, "exports", "llm_ab_results.json")


def load_side():
    """Fresh module instance of the submission (separate globals)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        f"submission_ab_{time.perf_counter_ns()}", SUBMISSION_MAIN)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class Instrumented:
    """Wrap a provider: count calls, fallbacks (None), budget blocks."""

    def __init__(self, inner):
        self.inner = inner
        self.calls = 0
        self.fallbacks = 0
        self.budget_blocks = 0

    def suggest(self, prompt, context):
        budget = getattr(self.inner, "budget", None)
        if budget is not None and budget.exhausted:
            self.budget_blocks += 1
            return None
        self.calls += 1
        ans = self.inner.suggest(prompt, context)
        if ans is None:
            self.fallbacks += 1
        return ans

    @property
    def name(self):
        return getattr(self.inner, "name", "unknown")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=4, help="seeds per seat order")
    ap.add_argument("--first-seed", type=int, default=701)
    args = ap.parse_args()
    seeds = list(range(args.first_seed, args.first_seed + max(1, args.rounds)))

    base = provider_from_env()
    real = not isinstance(base, NullProvider)
    provider = Instrumented(base)

    mod_on = load_side()
    mod_on.LLM_PROVIDER = provider
    mod_off = load_side()
    mod_off.LLM_PROVIDER = None

    games = []
    t0 = time.perf_counter()
    for s in seeds:
        for seat in (0, 1):
            if seat == 0:
                res = run_match(mod_on.agent, mod_off.agent, seed=s,
                                label_a="llm_on", label_b="llm_off",
                                episode_steps=FULL_EPISODE_STEPS,
                                collect_daily=False)
            else:
                res = run_match(mod_off.agent, mod_on.agent, seed=s,
                                label_a="llm_off", label_b="llm_on",
                                episode_steps=FULL_EPISODE_STEPS,
                                collect_daily=False)
            res["seat"] = seat
            games.append(res)
            print(f"seed={s} seat{seat}: llm_on="
                  f"{res['rewards'][seat]:.0f} llm_off={res['rewards'][1 - seat]:.0f} "
                  f"winner={res['winner_label']}")

    elapsed = round(time.perf_counter() - t0, 2)
    wins = losses = ties = 0
    margins = []
    identical = 0
    for g in games:
        if g["winner_label"] is None:
            ties += 1
        elif g["winner_label"] == "llm_on":
            wins += 1
        else:
            losses += 1
        margins.append(g["rewards"][g["seat"]] - g["rewards"][1 - g["seat"]])
        if g["rewards"][0] == g["rewards"][1]:
            identical += 1
    n = len(games)

    budget = getattr(base, "budget", None)
    result = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "provider": provider.name,
        "provider_configured": real,
        "config_env": {k: bool(os.environ.get(k))
                       for k in ("KG_LLM_PROVIDER", "KG_LLM_BASE_URL",
                                 "KG_LLM_API_KEY", "KG_LLM_MODEL")},
        "rounds": len(seeds),
        "seeds": seeds,
        "games": n,
        "llm_on": {"wins": wins, "losses": losses, "ties": ties,
                   "avg_margin": round(sum(margins) / max(1, len(margins)), 2),
                   "reward_identical_games": identical},
        "win_rate_llm_on": (None if not real else
                            round((wins + 0.5 * ties) / max(1, n), 4)),
        "consultation_stats": {
            "suggest_calls": provider.calls,
            "heuristic_fallbacks": provider.fallbacks,
            "budget_gate_blocks": provider.budget_blocks,
            "budget": (None if budget is None else
                       {"max_calls": budget.max_calls,
                        "max_seconds": budget.max_seconds,
                        "calls_spent": budget.calls,
                        "seconds_spent": round(budget.seconds, 3)}),
        },
        "note": ("" if real else
                 "NullProvider (KG_LLM_* unset): the A side plays the same "
                 "heuristic policy, so win_rate is null by design -- this run "
                 "validates the harness plumbing, budget gate and fallback "
                 "path only. Re-run with KG_LLM_PROVIDER=openai_compat plus "
                 "KG_LLM_BASE_URL/KG_LLM_API_KEY/KG_LLM_MODEL for a real A/B."),
        "runtime_seconds": elapsed,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nprovider={provider.name} configured={real} games={n} "
          f"(W{wins} L{losses} T{ties}, identical={identical})")
    print(f"consultations: calls={provider.calls} fallbacks={provider.fallbacks} "
          f"budget_blocks={provider.budget_blocks} "
          f"budget={result['consultation_stats']['budget']}")
    print(f"win_rate_llm_on={result['win_rate_llm_on']} [{elapsed}s]")
    print(f"wrote {os.path.relpath(OUT_PATH, ARENA_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
