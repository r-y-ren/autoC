"""Local parameter scan for the opt-in v9 WHEAT_FARM mode.

This is a development-only harness. It refuses formal export locations and
loads a fresh candidate module for every game so module state cannot leak
between parameter combinations.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import itertools
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
REPO_ROOT = SOFTWARE_ROOT.parent.parent
DEV_OUTPUT_ROOT = REPO_ROOT / "workspace/kaggriculture/software/exports/probes/v9"
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.arena import run_match
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.online_pool import (
    crop_rotator_agent,
    template_wheat_agent,
    two_quad_denser_agent,
    wheat_straw_monster_agent,
)

DEFAULT_CANDIDATE = SOFTWARE_ROOT / "kaggle_simulations" / "agent_v9" / "main.py"
ALLOWED_KNOBS = {
    "herd": "WHEAT_FARM_HERD_FLOOR",
    "wheat": "WHEAT_FARM_WHEAT_CAP",
    "straw": "WHEAT_FARM_STRAW_CAP",
    "feed_max": "WHEAT_FARM_FEED_MAX_PRICE",
    "opp_wheat_max": "WHEAT_FARM_OPP_WHEAT_MAX",
    "cash": "WHEAT_FARM_CASH_REDLINE",
}
OPPONENTS = {
    "cow_baron": cow_baron_agent,
    "expansionist": expansionist_agent,
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "wheat_straw_monster": wheat_straw_monster_agent,
    "two_quad_denser": two_quad_denser_agent,
}


def parse_int_list(spec: str) -> list[int]:
    values = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            lo, hi = (int(value) for value in part.split("-", 1))
            if hi < lo:
                raise ValueError("descending ranges are not allowed")
            values.extend(range(lo, hi + 1))
        else:
            values.append(int(part))
    if not values or len(values) != len(set(values)):
        raise ValueError("integer list must be non-empty and unique")
    return values


def parse_grid(specs: list[str]) -> list[dict[str, int]]:
    axes = []
    seen = set()
    for spec in specs:
        if "=" not in spec:
            raise ValueError(f"invalid grid axis: {spec!r}")
        key, raw = (part.strip() for part in spec.split("=", 1))
        if key not in ALLOWED_KNOBS:
            raise ValueError(f"unknown grid knob: {key}")
        if key in seen:
            raise ValueError(f"duplicate grid knob: {key}")
        seen.add(key)
        axes.append((key, parse_int_list(raw)))
    if not axes:
        raise ValueError("at least one --grid axis is required")
    return [dict(zip((key for key, _ in axes), values))
            for values in itertools.product(*(vals for _, vals in axes))]


def parse_pool(spec: str) -> list[str]:
    names = [name.strip() for name in spec.split(",") if name.strip()]
    if not names:
        raise ValueError("opponent pool cannot be empty")
    unknown = sorted(set(names) - set(OPPONENTS))
    if unknown:
        raise ValueError(f"unknown opponents: {unknown}")
    return names


def validate_output(path: Path) -> Path:
    root = DEV_OUTPUT_ROOT.resolve()
    resolved = path.resolve()
    if resolved == root or root not in resolved.parents:
        raise ValueError("v9 scans must write a JSON file under probes/v9")
    if resolved.suffix.lower() != ".json":
        raise ValueError("v9 scan output must be a JSON file")
    return resolved


def load_candidate(path: Path, knobs: dict[str, int], serial: int):
    spec = importlib.util.spec_from_file_location(f"v9_scan_{serial}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.V9_WHEAT_FARM_ENABLED = True
    module.V9_SHADOW_ROUTING = True
    for key, value in knobs.items():
        setattr(module, ALLOWED_KNOBS[key], value)
    module._WHEAT_FARM_PLAN = module._wheat_farm_plan()
    module.reset_telemetry()
    return module


def telemetry_totals(snapshot: dict) -> dict:
    additive = ("moving_turns", "effective_ops", "pass_count",
                "cross_quadrant_switches")
    cumulative = ("wheat_harvested", "external_feed_bought", "shed_overflow")
    totals = {field: 0.0 for field in additive + cumulative}
    for player in snapshot.get("players", {}).values():
        days = list(player.get("days", {}).values())
        for field in additive:
            totals[field] += sum(float(day.get(field, 0) or 0)
                                 for day in days)
        for field in cumulative:
            totals[field] += max((float(day.get(field, 0) or 0)
                                  for day in days), default=0.0)
    effective = totals["effective_ops"]
    totals["movement_to_effective_ratio"] = (
        round(totals["moving_turns"] / effective, 4) if effective else None)
    return totals


def run_combo(candidate: Path, knobs: dict[str, int], opponents: list[str],
              seeds: list[int], serial: int) -> dict:
    games = []
    telemetry = []
    for opponent_name in opponents:
        opponent = OPPONENTS[opponent_name]
        for seed in seeds:
            for seat in ("AB", "BA"):
                module = load_candidate(candidate, knobs, serial + len(games))
                if seat == "AB":
                    result = run_match(module.agent, opponent, seed,
                                       label_a="candidate", label_b=opponent_name)
                    index = 0
                else:
                    result = run_match(opponent, module.agent, seed,
                                       label_a=opponent_name, label_b="candidate")
                    index = 1
                candidate_reward = float(result["rewards"][index])
                opponent_reward = float(result["rewards"][1 - index])
                games.append({"opponent": opponent_name, "seed": seed,
                              "seat": seat, "candidate_reward": candidate_reward,
                              "opponent_reward": opponent_reward,
                              "outcome": "W" if candidate_reward > opponent_reward
                              else "L" if candidate_reward < opponent_reward else "T"})
                telemetry.append(telemetry_totals(module.telemetry_snapshot()))
    wins = sum(game["outcome"] == "W" for game in games)
    losses = sum(game["outcome"] == "L" for game in games)
    ties = len(games) - wins - losses
    ratios = [row["movement_to_effective_ratio"] for row in telemetry
              if row["movement_to_effective_ratio"] is not None]
    return {
        "knobs": knobs,
        "games": len(games),
        "record": {"W": wins, "L": losses, "T": ties},
        "avg_candidate_reward": round(sum(g["candidate_reward"] for g in games) /
                                      len(games), 2),
        "avg_margin": round(sum(g["candidate_reward"] - g["opponent_reward"]
                                for g in games) / len(games), 2),
        "avg_movement_to_effective_ratio": (
            round(sum(ratios) / len(ratios), 4) if ratios else None),
        "details": games,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidate", type=Path, default=DEFAULT_CANDIDATE)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--seeds", default="101")
    parser.add_argument("--pool", default="template_wheat,wheat_straw_monster")
    parser.add_argument("--grid", action="append", default=[])
    return parser


def main(argv=None) -> int:
    args = build_parser().parse_args(argv)
    try:
        candidate = args.candidate.resolve()
        if not candidate.is_file():
            raise ValueError(f"candidate not found: {candidate}")
        out = validate_output(args.out)
        seeds = parse_int_list(args.seeds)
        opponents = parse_pool(args.pool)
        combinations = parse_grid(args.grid)
        candidate_sha = hashlib.sha256(candidate.read_bytes()).hexdigest()
        results = [run_combo(candidate, combo, opponents, seeds, i * 10000)
                   for i, combo in enumerate(combinations)]
        payload = {
            "schema_version": "v9-parameter-scan/1.0",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "kind": "development-only",
            "candidate": {"path": str(candidate), "sha256": candidate_sha},
            "config": {"seeds": seeds, "opponents": opponents,
                       "combinations": len(combinations)},
            "results": results,
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        temp = out.with_name(f".{out.name}.{os.getpid()}.tmp")
        temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
        os.replace(temp, out)
        print(f"wrote {out} ({len(results)} combinations)")
        return 0
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"SCAN FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
