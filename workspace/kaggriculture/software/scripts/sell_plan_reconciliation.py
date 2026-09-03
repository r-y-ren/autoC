#!/usr/bin/env python
"""Reconcile sell plans against real commits from the official engine.

The official Kaggriculture ``_process_market`` remains the resolver.  The
ledger wraps its ``_commit_unit`` and records every attempted unit with the
engine's actual quote and return value.  An action market list or a pre-turn
spot quote is never treated as a fill.

Usage:
  python scripts/sell_plan_reconciliation.py [--seeds 7,8]
      [--episode-steps 720] [--out exports/probes/sell_plan_reconciliation.json]
      [--min-coverage 0.80] [--max-abs-deviation-pct 15]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import json
import statistics
import subprocess
import sys
from pathlib import Path
from typing import Any

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
from kgenv.engine import run_episode  # noqa: E402
from scripts.market_ledger import OfficialMarketLedger  # noqa: E402

AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"
ENGINE_PACKAGE = "kaggle-environments"


def load_module(path=AGENT_MAIN):
    spec = importlib.util.spec_from_file_location("recon_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_module_state(module):
    for name in ("_MISSION_SHADOW", "_ROUTE_STATE", "_STATE", "_TARGETS",
                 "_PLAN_MEM", "_STAGE_MEM", "_MARKET_MEM", "_OPP_OBSERVER",
                 "_INTERFERENCE_LOG", "_INTERFERENCE_MEM", "_SELL_PLAN_MEM",
                 "_REPLAN_MEM", "_D29_SELL_QUEUE", "_SELL_BATCH_EMITTED",
                 "_SELL_BATCH_ORDER_KEYS", "_EOD_SELL_EMITTED",
                 "_EOD_SELL_ORDER_KEYS", "_INTERFERENCE_ORDER_KEYS",
                 "_LINEAR_PRESSURE_MEM"):
        state = getattr(module, name, None)
        if isinstance(state, (dict, set)):
            state.clear()
        elif isinstance(state, list):
            del state[:]
    if hasattr(module, "reset_telemetry"):
        module.reset_telemetry()


def _stats(values):
    if not values:
        return None
    ordered = sorted(float(v) for v in values)
    return {
        "n": len(ordered),
        "mean_pct": round(statistics.mean(ordered), 2),
        "median_pct": round(statistics.median(ordered), 2),
        "p90_pct": round(ordered[int(0.9 * (len(ordered) - 1))], 2),
        "p90_abs_pct": round(sorted(abs(v) for v in ordered)
                              [int(0.9 * (len(ordered) - 1))], 2),
    }


def _plan_qty(line: dict[str, Any]) -> int:
    batches = line.get("batches") or []
    if batches:
        return max(0, sum(int(q) for q in batches))
    try:
        return max(0, int(line.get("qty_today", 0)))
    except (TypeError, ValueError):
        return 0


def _fill_rows(records: dict[str, Any]) -> list[dict[str, Any]]:
    """Return successful official SELL commits only."""
    return [row for row in records.get("ledger", [])
            if row.get("op") == "SELL" and row.get("success") is True]


def summarize(records, *, min_coverage: float = 0.80,
              max_abs_deviation_pct: float = 15.0):
    """Aggregate real fills by plan and item.

    The legacy ``sales``/``planned_clear`` shape remains accepted for focused
    unit tests and old callers, but live records use ``ledger`` and
    ``planned_clear`` entries with seed/player/day/quantity fields.
    """
    fills = _fill_rows(records)
    plans = records.get("planned_clear", [])
    by_plan: dict[str, dict[str, Any]] = {}
    plan_keys: dict[tuple[Any, ...], str] = {}
    for index, plan in enumerate(plans):
        key_tuple = (plan.get("seed"), plan.get("player"), plan.get("day"),
                     plan.get("item"))
        key = "|".join("" if value is None else str(value)
                       for value in key_tuple)
        if key in by_plan:
            key = f"{key}|{index}"
        plan_keys[key_tuple] = key
        by_plan[key] = {
            "seed": plan.get("seed"), "player": plan.get("player"),
            "day": plan.get("day"), "item": plan.get("item"),
            "planned_qty": int(plan.get("planned_qty", 0)),
            "planned_price": plan.get("planned_price"),
            "fill_qty": 0, "fill_value": 0.0,
        }

    deviations = []
    fills_by_key: dict[tuple[Any, ...], list[dict[str, Any]]] = {}
    for fill in fills:
        key_tuple = (fill.get("seed"), fill.get("player"), fill.get("day"),
                     fill.get("item"))
        fills_by_key.setdefault(key_tuple, []).append(fill)

    assigned_fill_ids: set[int] = set()
    for plan in plans:
        key_tuple = (plan.get("seed"), plan.get("player"), plan.get("day"),
                     plan.get("item"))
        key = plan_keys.get(key_tuple)
        if key is None:
            continue
        row = by_plan[key]
        # Official commits are already in engine order. Assign at most the
        # planned quantity; same-key excess remains a real unplanned fill.
        for fill in fills_by_key.get(key_tuple, []):
            if row["fill_qty"] >= row["planned_qty"]:
                break
            fill_id = id(fill)
            if fill_id in assigned_fill_ids:
                continue
            assigned_fill_ids.add(fill_id)
            row["fill_qty"] += 1
            row["fill_value"] += float(fill["unit_price"])
            if row["planned_price"] not in (None, 0):
                deviations.append((float(fill["unit_price"])
                                   - float(row["planned_price"]))
                                  / max(1.0, float(row["planned_price"])) * 100)

    def finish(row):
        row["fill_value"] = round(row.pop("fill_value"), 2)
        row["weighted_avg_fill_price"] = round(
            row["fill_value"] / row["fill_qty"], 2) if row["fill_qty"] else None
        row["unfilled_qty"] = max(0, row["planned_qty"] - row["fill_qty"])
        row["coverage"] = (round(row["fill_qty"] / row["planned_qty"], 4)
                            if row["planned_qty"] else None)
        row["covered"] = row["fill_qty"] > 0
        return row

    finished_plans = [finish(row) for row in by_plan.values()]
    item_acc: dict[str, dict[str, Any]] = {}
    for plan in finished_plans:
        item = plan["item"]
        row = item_acc.setdefault(item, {
            "item": item, "planned_qty": 0, "fill_qty": 0,
            "fill_value": 0.0, "planned_lines": 0, "covered_lines": 0,
        })
        row["planned_qty"] += plan["planned_qty"]
        row["fill_qty"] += plan["fill_qty"]
        row["fill_value"] += plan["fill_value"]
        row["planned_lines"] += 1
        row["covered_lines"] += int(plan["covered"])
    by_item = []
    for row in item_acc.values():
        row["fill_value"] = round(row["fill_value"], 2)
        row["weighted_avg_fill_price"] = round(
            row["fill_value"] / row["fill_qty"], 2) if row["fill_qty"] else None
        row["unfilled_qty"] = max(0, row["planned_qty"] - row["fill_qty"])
        row["coverage"] = (round(row["covered_lines"] / row["planned_lines"], 4)
                            if row["planned_lines"] else None)
        by_item.append(row)

    # Compatibility path for the old pure aggregation fixture.
    if not fills and records.get("sales"):
        deviations = [float(row["deviation_pct"]) for row in records["sales"]]
    old_plans = plans
    covered_lines = sum(1 for row in old_plans if row.get("sold") or
                        row.get("fill_qty", 0) > 0)
    line_coverage = (round(covered_lines / len(old_plans), 4)
                     if old_plans else None)
    if fills:
        line_coverage = (round(sum(1 for row in finished_plans
                                   if row["fill_qty"] > 0) /
                               len(finished_plans), 4)
                         if finished_plans else None)
    hold_moves = [h["move_pct"] for h in records.get("holds", [])
                  if h.get("move_pct") is not None]
    planned_qty = sum(int(row.get("planned_qty", 0)) for row in finished_plans)
    fill_qty = sum(int(row["fill_qty"]) for row in finished_plans)
    actual_sales = len(fills) if fills else len(records.get("sales", []))
    fill_coverage = round(fill_qty / planned_qty, 4) if planned_qty else None
    coverage_for_gate = (fill_coverage if fills else line_coverage)
    abs_stats = _stats([abs(value) for value in deviations])
    gate = {
        "status": "PASS" if (coverage_for_gate is not None
                               and coverage_for_gate >= min_coverage
                               and abs_stats is not None
                               and abs_stats["p90_pct"] <= max_abs_deviation_pct)
                  else "FAIL",
        "thresholds": {
            "min_coverage": float(min_coverage),
            "max_p90_abs_deviation_pct": float(max_abs_deviation_pct),
        },
        "measured": {
            "coverage": coverage_for_gate,
            "p90_abs_deviation_pct": (abs_stats["p90_pct"]
                                       if abs_stats else None),
        },
    }
    return {
        "sales": actual_sales,
        "official_successful_sell_fills": len(fills),
        "official_ledger_attempts": len(records.get("ledger", [])),
        "planned_clear_lines": len(old_plans),
        "planned_qty": planned_qty,
        "fill_qty": fill_qty,
        "unfilled_qty": max(0, planned_qty - fill_qty),
        "coverage": (fill_coverage if fills else line_coverage),
        "line_coverage": line_coverage,
        "fill_coverage": fill_coverage,
        "price_deviation_pct": _stats(deviations),
        "by_item_deviation_pct": _legacy_item_deviations(records, fills),
        "by_plan": finished_plans,
        "by_item": by_item,
        "hold_lines": len(records.get("holds", [])),
        "hold_move_pct": _stats(hold_moves),
        "unplanned_successful_sell_fills": max(0, len(fills) - fill_qty),
        "gate": gate,
    }


def _legacy_item_deviations(records, fills):
    if records.get("sales") and not fills:
        out = {}
        for row in records["sales"]:
            out.setdefault(row["item"], []).append(row["deviation_pct"])
        return {item: _stats(values) for item, values in out.items()}
    return {}


def _source_metadata(module):
    def sha256(path):
        return hashlib.sha256(Path(path).read_bytes()).hexdigest()

    try:
        git_revision = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=str(SOFTWARE),
            stderr=subprocess.DEVNULL, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        git_revision = None
    try:
        engine_version = importlib.metadata.version(ENGINE_PACKAGE)
    except importlib.metadata.PackageNotFoundError:
        engine_version = None
    import kaggle_environments.envs.kaggriculture.kaggriculture as engine
    engine_path = Path(importlib.util.find_spec(
        "kaggle_environments.envs.kaggriculture.kaggriculture").origin)
    src_dir = AGENT_MAIN.parent / "src"
    strategy_files = [AGENT_MAIN] + sorted(src_dir.glob("*.py"))
    strategy_hash = hashlib.sha256()
    for path in strategy_files:
        strategy_hash.update(path.name.encode("utf-8"))
        strategy_hash.update(path.read_bytes())
    return {
        "strategy_source": str(AGENT_MAIN.parent.relative_to(SOFTWARE)),
        "strategy_files": [str(path.relative_to(SOFTWARE))
                           for path in strategy_files],
        "strategy_source_sha256": strategy_hash.hexdigest(),
        "git_revision": git_revision,
        "engine_package": ENGINE_PACKAGE,
        "engine_version": engine_version,
        "engine_source": str(engine_path),
        "engine_source_sha256": sha256(engine_path),
        "engine_process": "official _process_market + official _commit_unit",
    }


def run(seeds, episode_steps):
    module = load_module()
    records = {"ledger": [], "planned_clear": [], "holds": []}
    hold_tracking = []

    for seed in seeds:
        reset_module_state(module)
        agent_callable = getattr(module, "agent")

        def make_wrapped(module, agent_callable, seed):
            def wrapped(obs):
                action = agent_callable(obs)
                try:
                    record_turn(module, obs, action, records,
                                hold_tracking, seed)
                except Exception:
                    pass
                return action
            return wrapped

        wrapped = make_wrapped(module, agent_callable, seed)
        ledger = OfficialMarketLedger(seed=seed)
        # run_episode uses the real kaggle-environments environment.  The
        # installed context observes its market commits without replacing the
        # resolver or using action/spot inference.
        with ledger.installed():
            run_episode(wrapped, wrapped, seed, episode_steps=episode_steps)
        records["ledger"].extend(ledger.rows)

        for hold in hold_tracking:
            if hold.get("episode") != seed or hold.get("resolved"):
                continue
            later = [row for row in hold_tracking
                     if row["episode"] == seed and row["item"] == hold["item"]
                     and row["seat"] == hold["seat"]
                     and row["day"] == hold["day"] + 2]
            if later:
                move = (later[0]["price"] - hold["price"])
                move /= max(1.0, hold["price"])
                records["holds"].append({
                    "item": hold["item"], "day": hold["day"],
                    "move_pct": round(move * 100, 2),
                })
                hold["resolved"] = True
                later[0]["resolved"] = True
    return records


def record_turn(module, obs, action, records, hold_tracking, seed):
    """Record plan declarations; actual fills arrive from OfficialMarketLedger."""
    player = module._get(obs, "player", 0)
    day = module._get(obs, "day", 0)
    hour = module._get(obs, "hour", 0)
    plan = module.sell_plan_shadow(player)
    if plan is None or plan.get("day") != day:
        return
    lines = plan.get("lines") or {}
    prices = module._get(module._get(obs, "market", {}) or {},
                         "prices", {}) or {}
    if hour == 0:
        for item, line in lines.items():
            if line.get("verdict") == "clear" and _plan_qty(line) > 0:
                records["planned_clear"].append({
                    "seed": seed, "player": player, "item": item,
                    "day": day, "planned_qty": _plan_qty(line),
                    "planned_price": line.get("planned_price"),
                    "sold": False,
                })
            elif line.get("verdict") == "hold":
                hold_tracking.append({
                    "item": item, "day": day, "seat": player,
                    "episode": seed,
                    # Baseline for hold quality only, never a fill price.
                    "price": module._get(prices, item, 0.0) or 0.0,
                    "resolved": False,
                })


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default="7,8")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--min-coverage", type=float, default=0.80)
    ap.add_argument("--max-abs-deviation-pct", type=float, default=15.0)
    ap.add_argument("--out", default=str(
        SOFTWARE / "exports" / "probes" / "sell_plan_reconciliation.json"))
    args = ap.parse_args()
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    records = run(seeds, args.episode_steps)
    summary = summarize(records, min_coverage=args.min_coverage,
                        max_abs_deviation_pct=args.max_abs_deviation_pct)
    payload = {
        "schema": "sell-plan-reconciliation/2.0",
        "summary": summary,
        "seeds": seeds,
        "episode_steps": args.episode_steps,
        "metadata": _source_metadata(load_module()),
        "method": {
            "fills": "successful official _commit_unit SELL calls",
            "excluded_as_fills": ["action.market", "pre-turn spot price"],
            "thresholds": {
                "min_coverage": args.min_coverage,
                "max_p90_abs_deviation_pct": args.max_abs_deviation_pct,
            },
        },
        "ledger": records["ledger"],
        "planned_clear": records["planned_clear"],
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[sell-plan-reconciliation] {len(seeds)} episodes -> {out}")
    return 0 if summary["gate"]["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
