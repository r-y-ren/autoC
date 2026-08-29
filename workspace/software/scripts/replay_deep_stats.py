"""Per-day unit-op deep statistics from Kaggriculture replays (campaign III r3-1).

kgenv.replay_profile.py extracts market-level flows; this module adds the
farmer/hand unit-op axis needed for the round-2 winner cross-profiling:

  * CARE / FEED / WATER / HARVEST counts per day  (unit ops, market excluded)
  * PLANT counts per crop per day                 (rotation ramp timing)
  * BUY_ANIMAL counts per day                     (herd build trajectory)
  * external WHEAT feed buys per day (qty + spend)
  * sells per day per item (qty + revenue)
  * day-end herd composition + money + crop tiles (same sampling as
    replay_profile: last observation of each day)

r3-P0 adds the SUCCESS-CALIBER axis (``--success-json``): the same counts
re-measured from observation state transitions via
kgenv.replay_profile.extract_success_metrics -- effective CARE/FEED/WATER/
HARVEST (flag flips + yield moves), HIRE successes vs silent no-money
rejects, per-order market fills with realized prices and slippage, animal
escapes, care-lapse weed-outs, shed-capacity discards, capped-production
tile-days and per-worker movement/effective-op economics.  The request
tables above are kept byte-identical for continuity with the r3-1 exports.

Pure: reads a replay dict, returns plain JSON-serialisable dicts.  Used by
the r3-1 round-2 winner deep dive (exports/online/round2_winner_deep_dive.md)
and reusable by later waves for any raw replay.

Usage:
    python scripts/replay_deep_stats.py PATH [PATH ...] [--json OUT]
                                         [--success-json OUT]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.replay_profile import (  # noqa: E402
    HOURS_PER_DAY,
    _crops_from_counts,
    _herd_from_counts,
    _tile_counts,
    extract_success_metrics,
    load_replay,
)

UNIT_OPS = ("CARE", "FEED", "WATER", "HARVEST", "DIG")
DAYS = 30


def _blank_day_record() -> dict[str, Any]:
    return {
        "money_end": None,
        "unit_ops": Counter(),
        "plants": Counter(),
        "animal_buys": Counter(),
        "feed_buy_qty": 0,
        "feed_buy_spend": 0.0,
        "sells_qty": Counter(),
        "sells_revenue": Counter(),
    }


def extract_deep_stats(replay: dict) -> dict:
    """Per-player per-day unit-op and flow table for one replay (both seats)."""
    info = replay.get("info") or {}
    teams = list(info.get("TeamNames") or ["?", "?"])
    steps = replay["steps"]
    players = []
    for pl in (0, 1):
        days: dict[int, dict] = defaultdict(_blank_day_record)
        quadrant_day: dict[str, int] = {}
        for t, step in enumerate(steps):
            entry = step[pl]
            obs = entry.get("observation") or {}
            farms = obs.get("farms") or []
            if len(farms) <= pl:
                continue
            farm = farms[pl] or {}
            day = obs.get("day", t // HOURS_PER_DAY)
            rec = days[day]
            money = farm.get("money")
            if isinstance(money, (int, float)):
                rec["money_end"] = float(money)
            for q in farm.get("unlocked_quadrants") or []:
                quadrant_day.setdefault(q, day)
            act = entry.get("action") or {}
            for unit in [act.get("farmer") or []] + (act.get("hands") or []):
                if not unit:
                    continue
                op = unit[0]
                if op in UNIT_OPS:
                    rec["unit_ops"][op] += 1
                elif op == "PLANT" and len(unit) >= 2:
                    rec["plants"][unit[1]] += 1
            prices = (obs.get("market") or {}).get("prices") or {}
            for order in act.get("market") or []:
                if not isinstance(order, list) or not order:
                    continue
                if order[0] == "HIRE":
                    rec["unit_ops"]["HIRE"] += 1
                elif order[0] == "BUY_ANIMAL" and len(order) >= 3:
                    rec["animal_buys"][order[1]] += int(order[2])
                elif order[0] == "BUY_PRODUCT" and len(order) >= 3 \
                        and order[1] == "WHEAT":
                    qty = int(order[2])
                    rec["feed_buy_qty"] += qty
                    rec["feed_buy_spend"] += qty * float(prices.get("WHEAT", 0))
                elif order[0] == "SELL" and len(order) >= 3 and order[1] in prices:
                    qty = int(order[2])
                    price = float(prices[order[1]])
                    rec["sells_qty"][order[1]] += qty
                    rec["sells_revenue"][order[1]] += qty * price
            if obs.get("hour") == HOURS_PER_DAY - 1 or t == len(steps) - 1:
                counts = _tile_counts(farm.get("tiles"))
                rec["herd_end"] = _herd_from_counts(counts)
                rec["crops_end"] = _crops_from_counts(counts)
                rec["hands_end"] = len(farm.get("hands") or [])
        players.append(_finalise(pl, teams, days, quadrant_day,
                                 replay.get("rewards")))
    return {
        "protocol": "replay-deep-stats/1.0",
        "episode_id": info.get("EpisodeId"),
        "teams": teams,
        "rewards": replay.get("rewards"),
        "players": players,
    }


def _finalise(pl, teams, days, quadrant_day, rewards) -> dict[str, Any]:
    totals = {
        "CARE": 0, "FEED": 0, "WATER": 0, "HARVEST": 0, "HIRE": 0,
        "feed_buy_qty": 0, "feed_buy_spend": 0.0,
    }
    table = []
    peak_herd = {}
    for day in sorted(days):
        rec = days[day]
        for op in ("CARE", "FEED", "WATER", "HARVEST", "HIRE"):
            totals[op] += rec["unit_ops"][op]
        totals["feed_buy_qty"] += rec["feed_buy_qty"]
        totals["feed_buy_spend"] += rec["feed_buy_spend"]
        herd = rec.get("herd_end", {})
        live = {k: v for k, v in herd.items() if k != "EMPTY_STRUCTURE"}
        head = sum(live.values())
        for animal, n in live.items():
            peak_herd[animal] = max(peak_herd.get(animal, 0), n)
        table.append({
            "day": day,
            "money_end": rec["money_end"],
            "hands": rec.get("hands_end"),
            "herd": herd,
            "herd_head": head,
            "crops": rec.get("crops_end", {}),
            "care": rec["unit_ops"]["CARE"],
            "feed_ops": rec["unit_ops"]["FEED"],
            "water": rec["unit_ops"]["WATER"],
            "harvest": rec["unit_ops"]["HARVEST"],
            "hires": rec["unit_ops"]["HIRE"],
            "plants": dict(rec["plants"]),
            "animal_buys": dict(rec["animal_buys"]),
            "feed_buy_qty": rec["feed_buy_qty"],
            "sells_qty": dict(rec["sells_qty"]),
            "sells_revenue": {k: round(v, 1)
                              for k, v in rec["sells_revenue"].items()},
        })
    money = [row["money_end"] for row in table if row["money_end"] is not None]

    def at(day: int):
        return money[day] if day < len(money) else None

    return {
        "seat": pl,
        "team": teams[pl] if pl < len(teams) else "?",
        "reward": rewards[pl] if rewards and pl < len(rewards) else None,
        "totals": {
            "care": totals["CARE"],
            "feed_ops": totals["FEED"],
            "water": totals["WATER"],
            "harvest": totals["HARVEST"],
            "hires": totals["HIRE"],
            "feed_buy_qty": totals["feed_buy_qty"],
            "feed_buy_spend": round(totals["feed_buy_spend"], 1),
        },
        "money": {
            "by_day": [round(m, 1) for m in money],
            "day12": at(12), "day18": at(18), "day24": at(24),
            "ramp_d12_d24": round(at(24) - at(12), 1)
            if at(12) is not None and at(24) is not None else None,
        },
        "peak_herd": peak_herd,
        "peak_herd_head": sum(peak_herd.values()),
        "quadrant_unlock_day": quadrant_day,
        "table": table,
    }


def _success_summary_lines(success: dict) -> list[str]:
    """One console line per player: success caliber vs request caliber."""
    lines = []
    ep = success["episode"]
    for p in success["players"]:
        care, feed = p["ops"]["CARE"], p["ops"]["FEED"]
        water, harvest = p["ops"]["WATER"], p["ops"]["HARVEST"]
        hire = p["hire"]
        sells = p["market"]["SELL"]
        buys = p["market"]["BUY_PRODUCT"]
        workers = p["workers"]
        integrity = "attr_ok" if p["integrity"]["attribution_valid"] else (
            f"attr_mismatch={p['integrity']['mismatch_steps']}")
        lines.append(
            f"ep{ep['episode_id']} seat{p['seat']} {p['team']}: "
            f"CARE_eff={care['successes']}/{care['requests']} "
            f"(dup={care['failures']['already_served']}) "
            f"FEED_eff={feed['successes']}/{feed['requests']} "
            f"(nores={feed['failures']['no_resource']}) "
            f"WATER_eff={water['successes']}/{water['requests']} "
            f"HARVEST_eff={harvest['successes']}/{harvest['requests']} "
            f"HIRE_eff={hire['successes']}/{hire['requests']} "
            f"(rejected={hire['no_money_rejects']}) "
            f"SELL_fill={sells['filled_qty']}/{sells['requested_qty']} "
            f"BUY_fill={buys['filled_qty']}/{buys['requested_qty']} "
            f"escapes={p['escapes']['count']} "
            f"weeds_lapse={p['weeds']['care_lapse']} "
            f"shed_overflow={p['shed_overflow']['discarded_units']}u "
            f"cap_tile_days={p['animal_cap_waste']['capped_tile_days']} "
            f"move_share={workers['movement_share']} "
            f"moves_per_op={workers['moves_per_effective_op']} [{integrity}]"
        )
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", help="replay JSON file(s)")
    parser.add_argument("--json", default="",
                        help="optional output path for the combined JSON dump")
    parser.add_argument("--success-json", default="",
                        help="optional output path for the success-caliber "
                             "metrics dump (state-diff measurement)")
    args = parser.parse_args()

    combined = []
    success_combined = []
    for path in args.paths:
        replay = load_replay(path)
        stats = extract_deep_stats(replay)
        combined.append(stats)
        for player in stats["players"]:
            t = player["totals"]
            print(
                f"ep{stats['episode_id']} seat{player['seat']} "
                f"{player['team']}: reward={player['reward']} "
                f"CARE={t['care']} FEED_ops={t['feed_ops']} hires={t['hires']} "
                f"feed_ext={t['feed_buy_qty']}u@{round(t['feed_buy_spend'], 0)} "
                f"peak_herd={player['peak_herd']} "
                f"quads={player['quadrant_unlock_day']} "
                f"d12={player['money']['day12']} d24={player['money']['day24']} "
                f"ramp={player['money']['ramp_d12_d24']}"
            )
        if args.success_json:
            success = extract_success_metrics(replay, strict=False)
            success_combined.append(success)
            for line in _success_summary_lines(success):
                print("  [success] " + line)
    if args.json:
        target = Path(args.json)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(combined, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"wrote {target}")
    if args.success_json:
        target = Path(args.success_json)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps(success_combined, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"wrote {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
