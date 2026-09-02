#!/usr/bin/env python
"""MK-1 kill table (market strategy design §3.4) + market-facts self-check.

Kill table: for every product, invert the embedded curves
(_offset_from_price) to compute the dump size that pushes the price from
its base to each target band, and how many days that offset survives
against the town's daily absorption.  Output: exports/probes/kill_table.json.

Market facts (§3.6 prerequisites): scan official replay JSONs for the
town's realised per-day draws per item (Δmarket.inventory minus both
players' SELL/BUY units) -- verifies the "melon absorption ~1/day" forum
claim from our own corpus (single-source discipline) and observes the $1
floor-sell dynamics (sells that moved money but not inventory).

Usage:  python scripts/kill_table.py [--replays GLOB ...]
"""
import argparse
import glob
import json
import os
import sys
from collections import defaultdict

SOFTWARE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(SOFTWARE_ROOT, "kaggle_simulations", "agent"))

import main  # noqa: E402  (embedded curves live in the built artifact)


def kill_table():
    table = {}
    for item, params in main.MARKET_PARAMS_EMB.items():
        base = main.BASE_PRICE[item]
        # absorption per day with every shop unlocked is the ceiling case;
        # the realistic band is (center 1/day, all-shops)
        shops_absorb = sum(
            main.SHOP_DRAWS_PER_DAY * (2 if len(v) == 1 else 1)
            for v in main.SHOPS.values() if item in v)
        absorb_max = shops_absorb + main.CENTER_DRAWS_PER_DAY
        absorb_min = main.CENTER_DRAWS_PER_DAY
        rows = []
        for frac in (0.9, 0.75, 0.5, 0.25):
            target = max(1, int(base * frac))
            if target >= base:
                continue
            off = main._offset_from_price(item, target)
            rows.append({
                "target_price": target,
                "offset_units": round(off, 1),
                "hold_days_vs_min_absorb": round(off / absorb_min, 1),
                "hold_days_vs_max_absorb": round(off / absorb_max, 1),
            })
        table[item] = {
            "base": base,
            "absorb_per_day": {"min": absorb_min, "max": absorb_max},
            "kills": rows,
            "crash_shape": params[4],
        }
    return table


def market_facts(replay_globs):
    """Realised town draws per item per day, from replay JSON steps.

    Also counts floor sells (§3.6 prerequisite 2): SELL orders of an item
    executed while its market price sat at the $1 floor -- they move money
    but not inventory (engine `if price > 1`), the only Ch0 blind spot.
    """
    facts = defaultdict(list)   # item -> list of per-day draws
    floor_sells = defaultdict(int)   # item -> units sold at the $1 floor
    files = []
    for g in replay_globs:
        files.extend(glob.glob(g))
    for path in files:
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except (OSError, ValueError):
            continue
        steps = data.get("steps") or []
        prev_inv = {}
        for si in range(1, len(steps)):
            obs0 = steps[si][0].get("observation") or {}
            market = obs0.get("market", {}) or {}
            prices = market.get("prices", {}) or {}
            inv = dict(market.get("inventory") or {})
            player_units = defaultdict(float)
            for p in range(2):
                acts = steps[si][p].get("action") or {}
                for o in (acts.get("market") or []):
                    if isinstance(o, list) and len(o) >= 3 and o[0] in (
                            "SELL", "BUY_PRODUCT") and isinstance(o[2],
                                                                  (int, float)):
                        sign = 1 if o[0] == "SELL" else -1
                        player_units[o[1]] += sign * o[2]
                        # floor-sell: SELL executed at the $1 floor price
                        if o[0] == "SELL" and \
                                prices.get(o[1], 0) <= main.PRICE_FLOOR_EMB:
                            floor_sells[o[1]] += int(o[2])
            for item, now in inv.items():
                if item not in prev_inv:
                    continue
                draw = prev_inv[item] - now - player_units.get(item, 0)
                if si % 24 == 0 and draw:   # one sample per day boundary
                    facts[item].append(round(draw))
            prev_inv = inv
    summary = {}
    for item, draws in facts.items():
        if draws:
            summary[item] = {
                "n_days": len(draws),
                "min": min(draws), "max": max(draws),
                "mean": round(sum(draws) / len(draws), 2),
            }
    return summary, dict(floor_sells)


def main_cli():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replays", nargs="*", default=[])
    args = ap.parse_args()
    out = {"schema": "kill-table/1.0",
           "kill_table": kill_table()}
    if args.replays:
        summary, floor_sells = market_facts(args.replays)
        out["town_draw_facts"] = summary
        out["floor_sells_seen"] = floor_sells
    dest = os.path.join(SOFTWARE_ROOT, "exports", "probes",
                        "kill_table.json")
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"wrote {dest}")
    for item, rows in out["kill_table"].items():
        half = next((r for r in rows["kills"]
                     if r["target_price"] <= rows["base"] * 0.51), None)
        if half:
            print(f"{item:11s} -50% at offset {half['offset_units']:>7}u "
                  f"(hold {half['hold_days_vs_min_absorb']:>6}d vs "
                  f"min-absorb, {half['hold_days_vs_max_absorb']:>5}d vs max)")


if __name__ == "__main__":
    main_cli()
