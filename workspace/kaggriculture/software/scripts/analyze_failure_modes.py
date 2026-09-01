"""Failure-mode probe: submission vs the FULL pool, multi-seed, deep logging.

m1 wave 2 deliverable behind exports/failure_modes.md.  Plays the submission
bot against every pool opponent (strong ones included) at fresh seeds with
per-day money + shared-market price collection, then mines the replay log
for:

  * losses and near-losses (smallest final margins),
  * suppression windows (days where the submission trails on money),
  * shared-market glut evidence (FERTILIZER $1-crash day, MELON gate
    lockouts, EGG price floor) -- the market is SHARED, so opponent
    composition changes our revenue curve, not just theirs.

The measured evidence lands in exports/failure_probe_report.md; the curated
failure-mode entries (root-cause hypotheses + improvement directions, each
gated on measured triggers) land in exports/failure_modes.md, and a machine
summary in exports/failure_modes_summary.json (embedded by run_eval.py).

Usage:
    python scripts/analyze_failure_modes.py [--rounds 8] [--quick]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import load_submission_agent, run_match, write_replay_log
from kgenv.bots.baseline import baseline_wheat_agent, greedy_carrot_agent
from kgenv.bots.cow_baron import cow_baron_agent
from kgenv.bots.expansionist import expansionist_agent
from kgenv.bots.melon_hoarder import melon_hoarder_agent
from kgenv.engine import FULL_EPISODE_STEPS

EXPORTS = os.path.join(SOFTWARE_ROOT, "exports")

OPPONENTS = {
    "pass": "pass",
    "random": "random",
    "starter": "starter",
    "greedy_carrot": greedy_carrot_agent,
    "baseline_wheat": baseline_wheat_agent,
    "expansionist": expansionist_agent,
    "melon_hoarder": melon_hoarder_agent,
    "cow_baron": cow_baron_agent,
}


# --------------------------------------------------------------------------
# analysis helpers (pure functions over replay-log entries)
# --------------------------------------------------------------------------

def _segments(behind: List[int]) -> List[List[int]]:
    """Contiguous day ranges where the submission trails."""
    segs: List[List[int]] = []
    for d in behind:
        if segs and d == segs[-1][-1] + 1:
            segs[-1].append(d)
        else:
            segs.append([d])
    return segs


def analyze_game(entry: Dict) -> Dict:
    """Accepts a raw run_match result OR a replay-log line (normalized)."""
    rewards = entry["rewards"]
    sub_money, opp_money = rewards[0], rewards[1]
    winner = entry.get("winner_label")
    if winner is None:
        winner = entry.get("winner")
    daily_raw = entry.get("daily_money") or []
    pairs: List = []
    prices: List[Dict] = []
    for d in daily_raw:
        if isinstance(d, dict):          # raw run_match format
            pairs.append(d.get("money", [0.0, 0.0]))
            prices.append(d.get("prices") or {})
        else:                            # replay-log format ([m0, m1])
            pairs.append(d)
    if not prices:
        prices = entry.get("daily_prices") or [{} for _ in pairs]
    gaps = [(p[0] - p[1]) if isinstance(p, (list, tuple)) and len(p) == 2
            else 0.0 for p in pairs]
    behind = [i for i, g in enumerate(gaps) if g < 0]
    min_gap = min(gaps) if gaps else None
    min_day = gaps.index(min_gap) if gaps else None
    fert_crash = next((i for i, p in enumerate(prices)
                       if (p or {}).get("FERTILIZER", 100) <= 5), None)
    melon_floor = min((p or {}).get("MELON", 250) for p in prices) \
        if prices else None
    melon_gate_days = sum(1 for p in prices
                          if (p or {}).get("MELON", 250) < 150)
    egg_floor = min((p or {}).get("EGG", 50) for p in prices) if prices else None
    return {
        "players": entry["players"],
        "opponent": entry["players"][1],
        "seed": entry["seed"],
        "winner": winner,
        "sub_money": sub_money,
        "opp_money": opp_money,
        "margin": round(sub_money - opp_money, 1),
        "result": "WIN" if winner == "submission"
        else ("LOSS" if winner == entry["players"][1] else "TIE"),
        "min_gap": round(min_gap, 1) if min_gap is not None else None,
        "min_gap_day": min_day,
        "days_behind": len(behind),
        "suppression_segments": _segments(behind),
        "fert_price_crash_day": fert_crash,
        "melon_price_floor": melon_floor,
        "melon_days_below_gate150": melon_gate_days,
        "egg_price_floor": egg_floor,
        "gaps": [round(g, 0) for g in gaps],
    }


def summarize_opponent(games: List[Dict]) -> Dict:
    wins = sum(1 for g in games if g["result"] == "WIN")
    losses = sum(1 for g in games if g["result"] == "LOSS")
    ties = len(games) - wins - losses
    margins = [g["margin"] for g in games]
    closest = min(games, key=lambda g: g["margin"])
    return {
        "opponent": games[0]["opponent"],
        "games": len(games), "wins": wins, "losses": losses, "ties": ties,
        "win_rate": round((wins + 0.5 * ties) / len(games), 3),
        "avg_margin": round(sum(margins) / len(margins), 0),
        "min_margin": round(min(margins), 0),
        "closest_seed": closest["seed"],
        "worst_days_behind": max(g["days_behind"] for g in games),
        "fert_crash_days": sorted({g["fert_price_crash_day"] for g in games
                                   if g["fert_price_crash_day"] is not None}),
    }


# --------------------------------------------------------------------------
# curated failure-mode entries: trigger predicates over measured stats
# --------------------------------------------------------------------------

def _fm_strong_opponent_losses(stats: List[Dict]) -> List[Dict]:
    fms = []
    for s in stats:
        if s["losses"] == 0:
            continue
        fms.append({
            "id": f"FM-{len(fms) + 1}",
            "trigger_opponent": s["opponent"],
            "situation": (f"submission lost {s['losses']}/{s['games']} games "
                          f"vs {s['opponent']} (win rate {s['win_rate']}); "
                          f"avg margin {s['avg_margin']:+.0f}, closest seed "
                          f"{s['closest_seed']}"),
        })
    return fms


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=8,
                    help="seeds per opponent (default 8: seeds 201-208)")
    ap.add_argument("--quick", action="store_true",
                    help="2 seeds x strong opponents only (smoke)")
    ap.add_argument("--from-log", action="store_true",
                    help="re-analyze the existing failure_probe_log.jsonl "
                         "instead of playing new games")
    args = ap.parse_args()

    if args.from_log:
        log_file = os.path.join(EXPORTS, "logs", "failure_probe_log.jsonl")
        with open(log_file, encoding="utf-8") as f:
            games = [json.loads(line) for line in f if line.strip()]
        seeds = sorted({g["seed"] for g in games})
        dt = 0.0
        log_path = log_file
    else:
        submission = load_submission_agent()
        if args.quick:
            plan = {"cow_baron": OPPONENTS["cow_baron"],
                    "melon_hoarder": OPPONENTS["melon_hoarder"]}
            rounds = 2
        else:
            plan = OPPONENTS
            rounds = max(2, args.rounds)
        seeds = list(range(201, 201 + rounds))

        games = []
        t0 = time.perf_counter()
        for oname, obot in plan.items():
            for s in seeds:
                res = run_match(submission, obot, seed=s,
                                label_a="submission", label_b=oname,
                                episode_steps=FULL_EPISODE_STEPS,
                                collect_daily=True)
                games.append(res)
                print(f"[{len(games):02d}] submission vs {oname} seed={s}: "
                      f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
                      f"winner={res['winner_label']}")
        dt = time.perf_counter() - t0
        log_path = write_replay_log(os.path.join(EXPORTS, "logs"), games,
                                    filename="failure_probe_log.jsonl")

    analyzed = [analyze_game(g) for g in games]
    by_opp: Dict[str, List[Dict]] = {}
    for a in analyzed:
        by_opp.setdefault(a["opponent"], []).append(a)
    stats = [summarize_opponent(v) for _, v in
             sorted(by_opp.items(), key=lambda kv: -max(
                 g["margin"] * -1 for g in kv[1]))]
    # order stats by threat: most losses, then smallest avg margin
    stats.sort(key=lambda s: (-s["losses"], s["avg_margin"]))

    # ---- measured evidence report --------------------------------------------
    lines = [
        "# Failure probe: measured evidence (auto-generated)",
        "",
        f"- generated: {time.strftime('%Y-%m-%d %H:%M:%S')} by "
        f"scripts/analyze_failure_modes.py",
        f"- probe: submission (p0) vs each pool opponent, seeds "
        f"{seeds[0]}..{seeds[-1]}, full {FULL_EPISODE_STEPS}-step episodes",
        f"- games: {len(games)} in {dt:.0f}s; replay log: "
        f"exports/logs/failure_probe_log.jsonl",
        "",
        "## Per-opponent summary (most threatening first)",
        "",
        "| opponent | W-L-T | win rate | avg margin | min margin | "
        "closest seed | days behind (worst) | FERT $<=5 crash day |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for s in stats:
        crash = ",".join(str(d) for d in s["fert_crash_days"]) or "-"
        lines.append(
            f"| {s['opponent']} | {s['wins']}-{s['losses']}-{s['ties']} | "
            f"{s['win_rate']} | {s['avg_margin']:+.0f} | "
            f"{s['min_margin']:+.0f} | {s['closest_seed']} | "
            f"{s['worst_days_behind']} | {crash} |")

    lines += ["", "## Closest / lost games (evidence detail)", ""]
    worst = sorted(analyzed, key=lambda a: a["margin"])[:6]
    for a in worst:
        segs = "; ".join(f"d{s[0]}-d{s[-1]}" for s in a["suppression_segments"]
                        [:4]) or "never behind"
        lines += [
            f"### submission vs {a['opponent']} seed={a['seed']} -- "
            f"{a['result']} (margin {a['margin']:+.0f})",
            f"- final: {a['sub_money']:.0f} vs {a['opp_money']:.0f}; "
            f"min gap {a['min_gap']:+.0f} on day {a['min_gap_day']}; "
            f"days behind: {a['days_behind']} ({segs})",
            f"- market: FERT<=5 from day {a['fert_price_crash_day']}; "
            f"MELON floor {a['melon_price_floor']} "
            f"({a['melon_days_below_gate150']} days < gate 150); "
            f"EGG floor {a['egg_price_floor']}",
            f"- money gap by day (sub - opp): "
            f"{[int(g) for g in a['gaps'][::3]]} (every 3rd day)",
            "",
        ]
    report_path = os.path.join(EXPORTS, "failure_probe_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    # ---- machine summary for eval_results.json embedding ---------------------
    losses = [a for a in analyzed if a["result"] == "LOSS"]
    summary = {
        "generated_by": "scripts/analyze_failure_modes.py",
        "probe_seeds": seeds,
        "probe_games": len(games),
        "submission_losses": len(losses),
        "loss_opponents": sorted({a["opponent"] for a in losses}),
        "closest_opponent": stats[0]["opponent"] if stats else None,
        "closest_min_margin": stats[0]["min_margin"] if stats else None,
        "per_opponent": stats,
    }
    with open(os.path.join(EXPORTS, "failure_probe_summary.json"), "w",
              encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"\nwrote {report_path}")
    print(f"wrote {log_path}")
    print(f"wrote {os.path.join(EXPORTS, 'failure_probe_summary.json')}")
    for s in stats:
        print(f"  vs {s['opponent']:<16} {s['wins']}-{s['losses']}-"
              f"{s['ties']} avg_margin={s['avg_margin']:+.0f} "
              f"min={s['min_margin']:+.0f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
