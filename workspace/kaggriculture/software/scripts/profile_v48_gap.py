"""Behavioural gap profile: our submission vs an external opponent.

Runs paired episodes with full step recording, extracts per-player profiles
via kgenv.replay_profile, and prints a side-by-side economy comparison to
locate WHERE the bank deficit against a top-tier public agent concentrates.

Output stays under repo scratch (.tmp-intel/).

Example:
    python scripts/profile_v48_gap.py --seeds 101
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
REPO_ROOT = os.path.dirname(os.path.dirname(SOFTWARE_ROOT))
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import load_submission_agent  # noqa: E402
from kgenv.engine import FULL_EPISODE_STEPS  # noqa: E402
from kgenv.replay_profile import extract_episode_profiles  # noqa: E402

from kaggle_environments import make  # noqa: E402

OPPONENTS_DIR = os.path.join(
    SOFTWARE_ROOT, "kaggle_simulations", "opponents")
SUBMISSION_MAIN = os.path.join(
    SOFTWARE_ROOT, "kaggle_simulations", "agent", "main.py")


def run_recorded(agent_a, agent_b, seed: int, out_path: Path):
    env = make("kaggriculture",
               configuration={"episodeSteps": int(FULL_EPISODE_STEPS),
                              "seed": int(seed), "actTimeout": 60.0},
               debug=True)
    env.run([agent_a, agent_b])
    out_path.write_text(json.dumps(env.toJSON()), encoding="utf-8")
    return env


def fmt_wing(v: dict) -> str:
    return ", ".join(f"{k}:{v2.get('quoted_revenue', 0):.0f}"
                     for k, v2 in sorted(v.items(),
                                         key=lambda kv: -kv[1].get(
                                             "quoted_revenue", 0))[:6])


def side_by_side(pa: dict, pb: dict, la: str, lb: str) -> list[str]:
    lines = []
    rows = [
        ("final_money", pa["money"]["final"], pb["money"]["final"]),
        ("min_money", pa["money"]["min"], pb["money"]["min"]),
        ("sell_total_quoted", pa["sells"]["total_quoted_revenue"],
         pb["sells"]["total_quoted_revenue"]),
        ("sell_crop_rev", pa["sells"]["crop_quoted_revenue"],
         pb["sells"]["crop_quoted_revenue"]),
        ("sell_animal_rev", pa["sells"]["animal_quoted_revenue"],
         pb["sells"]["animal_quoted_revenue"]),
        ("sell_fert_rev", pa["sells"]["fertilizer_quoted_revenue"],
         pb["sells"]["fertilizer_quoted_revenue"]),
        ("endgame_gain", pa["endgame"]["gain"], pb["endgame"]["gain"]),
        ("hires_total", pa["hires"]["total"], pb["hires"]["total"]),
        ("feed_qty", pa["external_buys"]["feed_qty"],
         pb["external_buys"]["feed_qty"]),
        ("fert_bought", pa["external_buys"]["fertilizer_qty"],
         pb["external_buys"]["fertilizer_qty"]),
        ("quadrants_final", pa["land"]["quadrants_final"],
         pb["land"]["quadrants_final"]),
    ]
    lines.append(f"{'metric':<20}{la:>18}{lb:>18}")
    for name, va, vb in rows:
        lines.append(f"{name:<20}{va:>18}{vb:>18}")
    lines.append(f"\n{la} herd final: {pa['herd']['final']}")
    lines.append(f"{lb} herd final: {pb['herd']['final']}")
    lines.append(f"{la} tile-day share: {pa['crops']['tile_day_share']}")
    lines.append(f"{lb} tile-day share: {pb['crops']['tile_day_share']}")
    lines.append(f"{la} sells: {fmt_wing(pa['sells']['per_item'])}")
    lines.append(f"{lb} sells: {fmt_wing(pb['sells']['per_item'])}")
    lines.append(f"{la} unlock days: {pa['land']['quadrant_unlock_day']}")
    lines.append(f"{lb} unlock days: {pb['land']['quadrant_unlock_day']}")
    return lines


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seeds", default="101")
    parser.add_argument("--opponent", default="v48_main.py")
    args = parser.parse_args(argv)

    cand = load_submission_agent(SUBMISSION_MAIN)
    opp = load_submission_agent(os.path.join(OPPONENTS_DIR, args.opponent))
    scratch = Path(REPO_ROOT) / ".tmp-intel"
    scratch.mkdir(exist_ok=True)

    for seed in (int(s) for s in args.seeds.split(",") if s.strip()):
        replay_path = scratch / f"profile_s{seed}.json"
        env = run_recorded(cand, opp, seed, replay_path)
        profiles = extract_episode_profiles(
            json.loads(replay_path.read_text(encoding="utf-8")),
            episode_id=seed, source_url="local://h2h", capture_date="",
            strict=False)
        players = profiles.get("players") or profiles.get("profiles") or []
        if len(players) != 2:
            print(f"seed {seed}: unexpected profile shape: "
                  f"{list(profiles.keys())}")
            continue
        print(f"\n===== seed {seed} "
              f"rewards={env.steps[-1][0]['reward']}/"
              f"{env.steps[-1][1]['reward']} =====")
        for line in side_by_side(players[0], players[1], "ours", "v48"):
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
