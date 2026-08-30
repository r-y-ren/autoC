"""Paired shadow-vs-active comparison for the v9 sector router.

Development-only A/B harness: both routing configs play the SAME
(opponent, seed, seat) cells on the official engine, each on a freshly
imported module (no cross-game state).  Reports per-config telemetry
(movement/effective ratio, overdue, harvest, feed buys) plus paired
reward deltas so the efficiency gate can be judged on measured numbers
before any outcome ablation is spent.  Output may only land under the
repo's .tmp-v9/ development root.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
REPO_ROOT = SOFTWARE_ROOT.parent.parent
DEV_OUTPUT_ROOT = REPO_ROOT / ".tmp-v9"
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.arena import run_match
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.online_pool import (crop_rotator_agent,
                                    self_feed_ranch_agent,
                                    template_wheat_agent,
                                    two_quad_denser_agent,
                                    wheat_straw_monster_agent)

CANDIDATE = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v9" / "main.py"
OPPONENTS = {
    "wheat_straw_monster": wheat_straw_monster_agent,
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "two_quad_denser": two_quad_denser_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "cow_baron": cow_baron_agent,
}
ADDITIVE = ("moving_turns", "effective_ops", "pass_count",
            "cross_quadrant_switches", "water_overdue", "feed_overdue",
            "care_overdue")
CUMULATIVE = ("wheat_harvested", "external_feed_bought", "shed_overflow")


def validate_output(path: Path) -> Path:
    root = DEV_OUTPUT_ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise ValueError("routing comparisons must write under .tmp-v9")
    if resolved.suffix.lower() != ".json":
        raise ValueError("routing comparison output must be a JSON file")
    return resolved


def parse_seeds(spec: str) -> list[int]:
    values = [int(part) for part in spec.split(",") if part.strip()]
    if not values or len(values) != len(set(values)):
        raise ValueError("seeds must be a non-empty unique list")
    return values


def load_module(routing_active: bool, serial: int):
    spec = importlib.util.spec_from_file_location(f"v9_route_{serial}", CANDIDATE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.V9_WHEAT_FARM_ENABLED = False   # wheat class rejected (r2)
    module.V9_SHADOW_ROUTING = not routing_active
    module.reset_telemetry()
    return module


def telemetry_totals(snapshot: dict) -> dict:
    totals = {field: 0.0 for field in ADDITIVE + CUMULATIVE}
    for player in snapshot.get("players", {}).values():
        days = list(player.get("days", {}).values())
        for field in ADDITIVE:
            totals[field] += sum(float(day.get(field, 0) or 0) for day in days)
        for field in CUMULATIVE:
            totals[field] += max((float(day.get(field, 0) or 0)
                                  for day in days), default=0.0)
    effective = totals["effective_ops"]
    totals["movement_to_effective_ratio"] = (
        round(totals["moving_turns"] / effective, 4) if effective else None)
    return totals


def play_cell(routing_active: bool, opponent, opponent_name: str,
              seed: int, seat: str, serial: int) -> dict:
    module = load_module(routing_active, serial)
    if seat == "AB":
        result = run_match(module.agent, opponent, seed,
                           label_a="cand", label_b=opponent_name)
        index = 0
    else:
        result = run_match(opponent, module.agent, seed,
                           label_a=opponent_name, label_b="cand")
        index = 1
    return {
        "reward": float(result["rewards"][index]),
        "statuses": result["statuses"],
        "telemetry": telemetry_totals(module.telemetry_snapshot()),
    }


def run_comparison(seeds: list[int], opponents: list[str]) -> dict:
    cells = []
    serial = 0
    for name in opponents:
        opponent = OPPONENTS[name]
        for seed in seeds:
            for seat in ("AB", "BA"):
                serial += 1
                shadow = play_cell(False, opponent, name, seed, seat, serial)
                serial += 1
                active = play_cell(True, opponent, name, seed, seat, serial)
                cells.append({
                    "opponent": name, "seed": seed, "seat": seat,
                    "shadow": shadow, "active": active,
                    "reward_diff": round(active["reward"] - shadow["reward"], 1),
                })

    def agg(side: str) -> dict:
        ratios = [c[side]["telemetry"]["movement_to_effective_ratio"]
                  for c in cells if c[side]["telemetry"]["movement_to_effective_ratio"] is not None]
        summary = {field: round(sum(c[side]["telemetry"][field] for c in cells), 1)
                   for field in ADDITIVE + CUMULATIVE}
        summary["games"] = len(cells)
        summary["avg_reward"] = round(sum(c[side]["reward"] for c in cells)
                                      / len(cells), 1)
        summary["avg_ratio"] = round(sum(ratios) / len(ratios), 4) if ratios else None
        return summary

    return {"cells": cells, "shadow": agg("shadow"), "active": agg("active")}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", default="101,102")
    parser.add_argument("--pool", default=",".join(OPPONENTS))
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        out = validate_output(args.out)
        seeds = parse_seeds(args.seeds)
        unknown = [n for n in (p.strip() for p in args.pool.split(",")) if n] \
            and [n for n in (p.strip() for p in args.pool.split(",")) if n
                 and n not in OPPONENTS]
        opponents = [n.strip() for n in args.pool.split(",") if n.strip()]
        if unknown:
            raise ValueError(f"unknown opponents: {sorted(set(unknown))}")
        comparison = run_comparison(seeds, opponents)
        payload = {
            "schema_version": "v9-routing-comparison/1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "kind": "development-only",
            "candidate": {"path": str(CANDIDATE),
                          "sha256": hashlib.sha256(
                              CANDIDATE.read_bytes()).hexdigest()},
            "config": {"seeds": seeds, "opponents": opponents,
                       "wheat_farm": False},
            "summary": {"shadow": comparison["shadow"],
                        "active": comparison["active"]},
            "cells": comparison["cells"],
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        temp = out.with_name(f".{out.name}.{os.getpid()}.tmp")
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2)
                        + "\n", encoding="utf-8")
        os.replace(temp, out)

        print(f"wrote {out} ({len(comparison['cells'])} cells)")
        for side in ("shadow", "active"):
            s = comparison[side]
            print(f"{side:>7}: ratio={s['avg_ratio']} "
                  f"moves={s['moving_turns']:.0f} ops={s['effective_ops']:.0f} "
                  f"pass={s['pass_count']:.0f} "
                  f"overdue(w/f/c)={s['water_overdue']:.0f}/"
                  f"{s['feed_overdue']:.0f}/{s['care_overdue']:.0f} "
                  f"harvest={s['wheat_harvested']:.0f} "
                  f"feedbuy={s['external_feed_bought']:.0f} "
                  f"reward={s['avg_reward']}")
        diffs = [c["reward_diff"] for c in comparison["cells"]]
        wins = sum(d > 0 for d in diffs)
        losses = sum(d < 0 for d in diffs)
        print(f"paired active-vs-shadow: {wins}W-{losses}L-"
              f"{len(diffs) - wins - losses}T, "
              f"net {round(sum(diffs), 1)}")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"COMPARISON FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
