#!/usr/bin/env python
"""M3 divergence harness (worker_route_scheduler_design.md §7 M3 gate).

Runs self-play episodes with the CURRENT submission (execution authority =
_schedule_units_v72) while solving the SAME dawn missions with the shadow
route solver (_solve_routes), then reports the divergence statistics that
gate the M4 switchover: D1 coverage, feasibility, dropped keys, feed legs,
PASS pressure and per-day mission hashes.

Read-only vs the artifact: the shadow solve happens AFTER the real action
is produced and never feeds back into it.

Usage:
  python scripts/solver_shadow_stats.py [--episodes 4] [--seeds 7,8,9,101]
      [--episode-steps 720] [--out exports/probes/solver_shadow_stats.json]
"""
import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
from kgenv.engine import run_episode  # noqa: E402

AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"


def load_module(path=AGENT_MAIN):
    spec = importlib.util.spec_from_file_location("shadow_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_module_state(module):
    for name in ("_MISSION_SHADOW", "_ROUTE_STATE", "_STATE", "_TARGETS",
                 "_PLAN_MEM", "_STAGE_MEM", "_MARKET_MEM", "_OPP_OBSERVER",
                 "_INTERFERENCE_LOG", "_REPLAN_MEM", "_D29_SELL_QUEUE"):
        state = getattr(module, name, None)
        if isinstance(state, dict):
            state.clear()
        elif isinstance(state, list):
            del state[:]
    if hasattr(module, "reset_telemetry"):
        module.reset_telemetry()


def shadow_metrics_for_turn(module, obs):
    """D1 coverage + feasibility of the shadow routes on this observation."""
    player = module._get(obs, "player", 0)
    mission = module.mission_shadow(player)
    if mission is None:
        return None
    farm = module._get(obs, "farms", [{}] * (player + 1))[player]
    private = module._get(obs, "private", {}) or {}
    res = module._solve_routes(farm, private, mission["day"],
                               mission["tasks"])
    d1 = set(mission.get("d1") or [])
    covered = set()
    for route in res["routes"]:
        for t, eta in zip(route["tasks"], route["etas"]):
            if t.get("key") in d1 and \
                    (t.get("deadline") is None or eta <= t["deadline"]):
                covered.add(t["key"])
    return {"day": mission["day"], "d1_total": len(d1),
            "d1_covered": len(covered),
            "feasible": bool(res["feasible"]),
            "dropped": len(res["dropped"]),
            "feed_legs": int(res["feed_legs"]),
            "mission_hash": mission.get("mission_hash"),
            "workers_empty": sum(1 for r in res["routes"] if not r["tasks"]),
            "workers": len(res["routes"])}


def summarize(episodes):
    days = [d for e in episodes for d in e["days"]]
    d1_total = sum(d["d1_total"] for d in days)
    d1_covered = sum(d["d1_covered"] for d in days)
    infeasible = sum(1 for d in days if not d["feasible"])
    hashes = defaultdict(set)
    for e in episodes:
        for d in e["days"]:
            hashes[(e["seed"], d["day"])].add(d["mission_hash"])
    return {
        "episodes": len(episodes),
        "days": len(days),
        "d1_total": d1_total,
        "d1_covered": d1_covered,
        "d1_coverage_rate": round(d1_covered / d1_total, 4) if d1_total else None,
        "infeasible_days": infeasible,
        "dropped_total": sum(d["dropped"] for d in days),
        "feed_legs_total": sum(d["feed_legs"] for d in days),
        "pass_rate_v72": round(
            sum(e["passes"] for e in episodes)
            / max(1, sum(e["turns"] * max(1, e["workers"]) for e in episodes)),
            4),
        "empty_route_worker_rate": round(
            sum(d["workers_empty"] for d in days)
            / max(1, sum(d["workers"] for d in days)), 4),
        # golden-hash premise: the same (seed, day) must yield one hash
        "mission_hash_stable": all(len(v) == 1 for v in hashes.values()),
    }


def make_wrapped(module, stats, state):
    # single-argument signature: kaggle's runner sizes the call by the
    # callable's arity, so extra positional params would be overwritten
    # by (observation, configuration) -- capture state via closure instead
    def wrapped(obs):
        action = module.agent(obs)
        try:
            stats["turns"] += 1
            unit_actions = [action.get("farmer")] + \
                list(action.get("hands") or [])
            stats["passes"] += sum(
                1 for a in unit_actions if not a or a[0] == "PASS")
            metrics = shadow_metrics_for_turn(module, obs)
            if metrics is not None:
                stats["workers"] = max(stats["workers"],
                                       metrics["workers"])
                if metrics["day"] not in state["seen_days"]:
                    state["seen_days"].add(metrics["day"])
                    stats["days"].append(metrics)
        except Exception:
            pass
        return action
    return wrapped


def run(seeds, episode_steps):
    module = load_module()
    episodes = []
    for seed in seeds:
        reset_module_state(module)
        stats = {"days": [], "passes": 0, "turns": 0, "workers": 1}
        state = {"seen_days": set()}
        wrapped = make_wrapped(module, stats, state)
        result = run_episode(wrapped, wrapped, seed,
                             episode_steps=episode_steps)
        episodes.append({"seed": seed, "rewards": result["rewards"],
                         "statuses": result["statuses"],
                         "turns": stats["turns"], "passes": stats["passes"],
                         "workers": stats["workers"], "days": stats["days"]})
    return episodes


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default="7,8")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--episodes", type=int, default=None,
                    help="compat alias: uses the first N seeds")
    ap.add_argument("--out", default=str(
        SOFTWARE / "exports" / "probes" / "solver_shadow_stats.json"))
    args = ap.parse_args()
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    if args.episodes:
        seeds = seeds[:args.episodes]

    episodes = run(seeds, args.episode_steps)
    summary = summarize(episodes)
    payload = {"schema": "solver-shadow-stats/1.0", "summary": summary,
               "episodes": episodes}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[solver-shadow] {len(episodes)} episodes -> {out}")


if __name__ == "__main__":
    main()
