"""Probe which WHEAT_FARM entry condition binds in real episodes.

The r1 paired ablation measured 88 byte-identical ties: the opt-in mode
never fired once.  This development probe replays real games with the flag
on and records, per day, each gate component so the binding constraint is
measured instead of guessed.  Output goes to stdout only (dev tooling).
"""
from __future__ import annotations

import importlib.util
import os
import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOFTWARE_ROOT = HERE.parent
if str(SOFTWARE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOFTWARE_ROOT))

from kgenv.arena import run_match
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.online_pool import (self_feed_ranch_agent,
                                    template_wheat_agent,
                                    two_quad_denser_agent)

WRAPPER = HERE / "v9_wheat_on_candidate.py"
OPPONENTS = {
    "cow_baron": cow_baron_agent,
    "expansionist": expansionist_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "two_quad_denser": two_quad_denser_agent,
    "template_wheat": template_wheat_agent,
}
CONDITIONS = ("day_window", "herd12", "cash800", "wheat12",
              "price36", "opp_wheat10", "demand2")


def load_probe_core():
    spec = importlib.util.spec_from_file_location("probe_wheat_on", WRAPPER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module._core


def build_probe_agent(core, records):
    def probe_agent(obs):
        day = obs.get("day", -1)
        hour = obs.get("hour", -1)
        if hour == 0 and 5 <= day <= 14:
            farms = obs.get("farms", []) or []
            player = obs.get("player", 0)
            mine = core._farm_scan(farms[player])
            opp = None
            for i, farm in enumerate(farms):
                if i != player:
                    opp = core._farm_scan(farm)
                    break
            prices = (obs.get("market", {}) or {}).get("prices", {}) or {}
            shops = (obs.get("town", {}) or {}).get("unlocked_shops", []) or []
            demand = core._town_daily_demand(shops)
            records.append({
                "day": day,
                "day_window": 6 <= day <= 12,
                "herd12": mine["herd"] >= core.WHEAT_FARM_HERD_FLOOR,
                "cash800": mine["money"] >= core.WHEAT_FARM_CASH_REDLINE,
                "wheat12": mine["wheat"] >= core.WHEAT_FARM_ENTRY_WHEAT_MIN,
                "price36": prices.get("WHEAT", 25) <= core.WHEAT_FARM_FEED_MAX_PRICE,
                "opp_wheat10": opp is None or
                opp["wheat"] <= core.WHEAT_FARM_OPP_WHEAT_MAX,
                "demand2": demand.get("WHEAT", 1) >= 2,
                "herd": mine["herd"], "money": mine["money"],
                "wheat": mine["wheat"], "opp_wheat": (opp or {}).get("wheat", 0),
            })
        return core.agent(obs)
    return probe_agent


def main() -> int:
    core = load_probe_core()
    records = []
    probe = build_probe_agent(core, records)
    games = 0
    for name, opponent in OPPONENTS.items():
        for seed in (101, 102):
            run_match(probe, opponent, seed,
                      label_a="probe", label_b=name)
            games += 1
            run_match(opponent, probe, seed,
                      label_a=name, label_b="probe")
            games += 1

    by_day = defaultdict(list)
    for rec in records:
        by_day[rec["day"]].append(rec)
    print(f"games={games} day-records={len(records)}")
    header = "day | n  | " + " | ".join(f"{c:>10}" for c in CONDITIONS) + " | ALL"
    print(header)
    for day in sorted(by_day):
        rows = by_day[day]
        counts = [sum(1 for r in rows if r[c]) for c in CONDITIONS]
        all_held = sum(1 for r in rows if all(r[c] for c in CONDITIONS))
        print(f"{day:3d} | {len(rows):2d} | " +
              " | ".join(f"{v:>10}" for v in counts) + f" | {all_held}")

    window = [r for r in records if r["day_window"]]
    print(f"\nwindow day6-12 cells={len(window)}, "
          f"all-conditions-held={sum(1 for r in window if all(r[c] for c in CONDITIONS))}")
    for cond in CONDITIONS:
        held = sum(1 for r in window if r[cond])
        print(f"  {cond:>12}: {held}/{len(window)}")

    others = [c for c in CONDITIONS if c != "herd12"]
    for threshold in (4, 6, 8, 10, 12):
        passed = sum(1 for r in window
                     if r["herd"] >= threshold and all(r[c] for c in others))
        herd_ge = sum(1 for r in window if r["herd"] >= threshold)
        print(f"  entry-with herd>={threshold:2d}: all-others-and-herd "
              f"{passed:3d}/{len(window)}   (herd alone {herd_ge:3d})")
    by_day_herd = defaultdict(list)
    for r in window:
        by_day_herd[r["day"]].append(r["herd"])
    stats = []
    for day in sorted(by_day_herd):
        vals = sorted(by_day_herd[day])
        stats.append(f"d{day}: med={vals[len(vals)//2]} max={vals[-1]}")
    print("  herd-per-day: " + " | ".join(stats))

    near = [r for r in window
            if sum(r[c] for c in CONDITIONS) >= 6]
    print(f"\nnear-miss cells (>=6/7 conditions): {len(near)}")
    for rec in near[:12]:
        blockers = [c for c in CONDITIONS if not rec[c]]
        print(f"  d{rec['day']:2d} herd={rec['herd']:2d} cash={rec['money']:7.0f} "
              f"wheat={rec['wheat']:2d} opp_wheat={rec['opp_wheat']:2d} "
              f"blocked_by={blockers}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
