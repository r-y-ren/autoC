#!/usr/bin/env python
"""MK-2 reconciliation harness (market_strategy_design.md §2.3, MK-2 gate).

Runs local self-play episodes with the dawn sell planner in SHADOW mode and
reconciles plan vs execution:
  * price deviation -- for every planned clear line, planned_price (the
    dawn projection) vs the spot price of the turns where the agent's
    ACCEPTED orders actually sold that item that day (realized proxy);
  * coverage -- planned clear lines that saw >=1 accepted SELL;
  * hold quality -- for planned hold lines, the spot move from plan day to
    day+2 (did holding pay?).

This is the MK-2 gate instrument: the planner stays a shadow (MK-3 switch
needs deviation in band + behaviour regression + online public games).

Usage:
  python scripts/sell_plan_reconciliation.py [--seeds 7,8] \
      [--episode-steps 720] [--out exports/probes/sell_plan_reconciliation.json]
"""
import argparse
import importlib.util
import json
import statistics
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SOFTWARE))
from kgenv.engine import run_episode  # noqa: E402

AGENT_MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"


def load_module(path=AGENT_MAIN):
    spec = importlib.util.spec_from_file_location("recon_main", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def reset_module_state(module):
    for name in ("_MISSION_SHADOW", "_ROUTE_STATE", "_STATE", "_TARGETS",
                 "_PLAN_MEM", "_STAGE_MEM", "_MARKET_MEM", "_OPP_OBSERVER",
                 "_INTERFERENCE_LOG", "_INTERFERENCE_MEM", "_SELL_PLAN_MEM",
                 "_REPLAN_MEM", "_D29_SELL_QUEUE"):
        state = getattr(module, name, None)
        if isinstance(state, dict):
            state.clear()
        elif isinstance(state, list):
            del state[:]
    if hasattr(module, "reset_telemetry"):
        module.reset_telemetry()


def summarize(records):
    """Pure aggregation (unit-tested): records are per-sale dicts."""
    def stats(values):
        if not values:
            return None
        ordered = sorted(values)
        return {"n": len(values),
                "mean_pct": round(statistics.mean(values), 2),
                "median_pct": round(statistics.median(values), 2),
                "p90_pct": round(ordered[int(0.9 * (len(ordered) - 1))], 2)}

    per_item = {}
    for rec in records["sales"]:
        per_item.setdefault(rec["item"], []).append(rec["deviation_pct"])
    deviations = {item: stats(vals) for item, vals in per_item.items()}
    all_devs = [r["deviation_pct"] for r in records["sales"]]
    planned_clear = records["planned_clear"]
    covered = sum(1 for r in planned_clear if r["sold"])
    holds = records["holds"]
    hold_moves = [h["move_pct"] for h in holds if h["move_pct"] is not None]
    return {
        "sales": len(records["sales"]),
        "price_deviation_pct": stats(all_devs),
        "by_item_deviation_pct": deviations,
        "coverage": round(covered / len(planned_clear), 4)
        if planned_clear else None,
        "planned_clear_lines": len(planned_clear),
        "hold_lines": len(holds),
        "hold_move_pct": stats(hold_moves),
    }


def run(seeds, episode_steps):
    module = load_module()
    records = {"sales": [], "planned_clear": [], "holds": []}
    hold_tracking = []          # {item, day, price, seat, episode}

    for seed in seeds:
        reset_module_state(module)
        holder = {"episode": seed}

        def make_wrapped(module=module, seed=seed):
            # single-arg signature (kaggle runner sizes calls by arity)
            def wrapped(obs):
                action = module.agent(obs)
                try:
                    record_turn(module, obs, action, records,
                                hold_tracking, seed)
                except Exception:
                    pass
                return action
            return wrapped

        wrapped = make_wrapped()
        result = run_episode(wrapped, wrapped, seed,
                             episode_steps=episode_steps)
        holder["episode"] = seed
        # resolve hold-line 2-day moves now that the episode is complete
        for h in hold_tracking:
            if h.get("episode") != seed or h.get("resolved"):
                continue
            later = [r for r in hold_tracking
                     if r["episode"] == seed and r["item"] == h["item"]
                     and r["seat"] == h["seat"] and r["day"] == h["day"] + 2]
            if later:
                move = (later[0]["price"] - h["price"]) / max(1.0, h["price"])
                records["holds"].append({"item": h["item"], "day": h["day"],
                                         "move_pct": round(move * 100, 2)})
                h["resolved"] = True
                later[0]["resolved"] = True
        del result
    return records


def record_turn(module, obs, action, records, hold_tracking, seed):
    player = module._get(obs, "player", 0)
    day = module._get(obs, "day", 0)
    hour = module._get(obs, "hour", 0)
    plan = module.sell_plan_shadow(player)
    if plan is None or plan.get("day") != day:
        return
    lines = plan.get("lines") or {}
    prices = module._get(module._get(obs, "market", {}) or {},
                         "prices", {}) or {}
    sells = [o for o in (action.get("market") or [])
             if isinstance(o, list) and o and o[0] == "SELL"]
    sold_items = {o[1] for o in sells}
    if hour == 0:
        for item, line in lines.items():
            if line.get("verdict") == "clear" and line.get("batches"):
                records["planned_clear"].append(
                    {"item": item, "day": day, "sold": False})
            elif line.get("verdict") == "hold":
                hold_tracking.append(
                    {"item": item, "day": day, "seat": player,
                     "episode": seed,
                     "price": module._get(prices, item, 0.0) or 0.0,
                     "resolved": False})
        for h in hold_tracking:
            if h["episode"] == seed and not h.get("resolved") \
                    and h["day"] == day and h["seat"] == player:
                h["price"] = module._get(prices, h["item"], 0.0) or h["price"]
    for o in sells:
        item = o[1]
        line = lines.get(item)
        spot = module._get(prices, item, 0.0)
        if line is None or spot <= 0:
            continue
        planned = line.get("planned_price") or spot
        deviation = (spot - planned) / max(1.0, planned)
        records["sales"].append({"item": item, "day": day, "hour": hour,
                                 "planned": planned, "realized": spot,
                                 "deviation_pct": round(deviation * 100, 2)})
        for rec in records["planned_clear"]:
            if rec["item"] == item and rec["day"] == day:
                rec["sold"] = True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--seeds", default="7,8")
    ap.add_argument("--episode-steps", type=int, default=720)
    ap.add_argument("--out", default=str(
        SOFTWARE / "exports" / "probes" / "sell_plan_reconciliation.json"))
    args = ap.parse_args()
    seeds = [int(s) for s in str(args.seeds).split(",") if s.strip()]
    records = run(seeds, args.episode_steps)
    summary = summarize(records)
    payload = {"schema": "sell-plan-reconciliation/1.0", "summary": summary,
               "seeds": seeds, "episode_steps": args.episode_steps}
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2),
                   encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"[sell-plan-reconciliation] {len(seeds)} episodes -> {out}")


if __name__ == "__main__":
    main()
