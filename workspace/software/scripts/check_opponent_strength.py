"""Strength gate for certified opponent-pool members.

Plays every certified opponent against the frozen weak pool (pass / random /
starter / greedy_carrot) at fixed seeds and asserts the hard requirement:

    each pool addition holds a >= 50% win rate vs greedy_carrot AND vs the
    whole weak pool below it (i.e. it really is a STRONG opponent).

Covers the m1 wave-2 strong opponents (cow_baron / melon_hoarder /
expansionist) and the m2 online-style opponents (campaign III reconstructions
of ladder archetypes from the replay-profile corpus; see
kgenv/bots/online_pool.py for parameter provenance), including the r3-1
scale_ranch reconstruction of the round-2 winner archetype.

Usage:
    python scripts/check_opponent_strength.py [--rounds 3] [--quick]
        [--family strong|online|all]

Exit 0 = all strong; exit 1 = somebody is still weak (diff printed).
The output doubles as audit evidence for exports/eval_audit.md.
"""

from __future__ import annotations

import argparse
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SOFTWARE_ROOT = os.path.dirname(HERE)
if SOFTWARE_ROOT not in sys.path:
    sys.path.insert(0, SOFTWARE_ROOT)

from kgenv.arena import run_match  # noqa: E402
from kgenv.bots import (ONLINE_STYLE_OPPONENTS, STRONG_OPPONENTS,  # noqa: E402
                        baseline_wheat_agent, greedy_carrot_agent)
from kgenv.bots.cow_baron import cow_baron_agent  # noqa: E402
from kgenv.bots.expansionist import expansionist_agent  # noqa: E402
from kgenv.bots.melon_hoarder import melon_hoarder_agent  # noqa: E402
from kgenv.bots.online_pool import (crop_rotator_agent,  # noqa: E402
                                    near_band_diversified_agent,
                                    scale_ranch_agent,
                                    self_feed_ranch_agent,
                                    template_wheat_agent,
                                    wheat_straw_monster_agent)
from kgenv.engine import FULL_EPISODE_STEPS  # noqa: E402

STRONG_BOTS = {
    "cow_baron": cow_baron_agent,
    "melon_hoarder": melon_hoarder_agent,
    "expansionist": expansionist_agent,
}
ONLINE_BOTS = {
    "crop_rotator": crop_rotator_agent,
    "template_wheat": template_wheat_agent,
    "self_feed_ranch": self_feed_ranch_agent,
    "near_band_diversified": near_band_diversified_agent,
    "scale_ranch": scale_ranch_agent,
    "wheat_straw_monster": wheat_straw_monster_agent,
}
WEAK_POOL = {
    "pass": "pass",
    "random": "random",
    "starter": "starter",
    "greedy_carrot": greedy_carrot_agent,
}
HARD_GAUGE = "greedy_carrot"   # the hard requirement is vs this one


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rounds", type=int, default=3,
                    help="seeds per strong-vs-weak pairing")
    ap.add_argument("--quick", action="store_true",
                    help="single seed, single opponent (smoke only)")
    ap.add_argument("--family", choices=("strong", "online", "all"),
                    default="all",
                    help="which opponent family to certify (default: all)")
    args = ap.parse_args()

    rounds = 1 if args.quick else max(1, args.rounds)
    seeds = list(range(101, 101 + rounds))
    certified: dict = {}
    if args.family in ("strong", "all") or args.quick:
        certified.update({k: v for k, v in STRONG_BOTS.items()
                          if k in STRONG_OPPONENTS})
    if args.family in ("online", "all") or args.quick:
        certified.update({k: v for k, v in ONLINE_BOTS.items()
                          if k in ONLINE_STYLE_OPPONENTS})
    pool = WEAK_POOL if not args.quick else {HARD_GAUGE: WEAK_POOL[HARD_GAUGE]}

    failures = []
    records = {}
    t0 = time.perf_counter()
    for sname, sbot in certified.items():
        for wname, wbot in pool.items():
            w = l = t = 0
            margins = []
            for s in seeds:
                res = run_match(sbot, wbot, seed=s, label_a=sname,
                                label_b=wname, episode_steps=FULL_EPISODE_STEPS,
                                collect_daily=False)
                if res["winner_label"] == sname:
                    w += 1
                elif res["winner_label"] == wname:
                    l += 1
                else:
                    t += 1
                margins.append(res["rewards"][0] - res["rewards"][1])
                print(f"  {sname} vs {wname} seed={s}: "
                      f"{res['rewards'][0]:.0f}:{res['rewards'][1]:.0f} "
                      f"winner={res['winner_label']}")
            n = len(seeds)
            wr = (w + 0.5 * t) / n
            verdict = "STRONG" if wr >= 0.5 else "WEAK"
            if wr < 0.5:
                failures.append(f"{sname} vs {wname}: win_rate={wr:.2f} "
                                f"(W{w} L{l} T{t}) < 0.5")
            records.setdefault(sname, {})[wname] = {
                "games": n, "W": w, "L": l, "T": t, "win_rate": round(wr, 4)}
            print(f"[{verdict}] {sname} vs {wname}: W{w} L{l} T{t} "
                  f"win_rate={wr:.2f} avg_margin={sum(margins)/n:+.0f}\n")

    dt = time.perf_counter() - t0
    if failures:
        print(f"strength gate FAILED ({len(failures)}):")
        for f in failures:
            print(f"  {f}")
        return 1
    print(f"strength gate PASS: all {len(certified)} certified opponents "
          f"({', '.join(sorted(certified))}) hold >=50% vs every weak-pool "
          f"bot ({rounds} seed(s) each, {dt:.0f}s, baseline_wheat reference "
          f"Elo 1245.8 / greedy_carrot 1162.2 from m0)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
