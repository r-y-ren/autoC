#!/usr/bin/env python3
"""Measure a Kaggle opponent's market footprint into a `kaggle_flow` table.

Why
---
`kagg3.es.kagg2_flow` replays kagg2's measured per-day SELL / BUY_PRODUCT units
against the live quote curve, so the policy trains against the *price path* a
real opponent makes rather than against a planner that only looks like one. The
opponents that actually beat us on Kaggle are not kagg2: the 2026-08-30 autopsy
puts them at 12-14 hands by day 10, ~196 tiles planted (137 wheat, 37
strawberry), ~9 cows / 4 sheep and ~98k final money. Their supply mix -- and so
their quotes -- is a market our training has never seen.

This script builds the same kind of table for them, from Kaggle replays.

How
---
Executed units, not requested ones. A replay records the *orders* a seat queued
(`steps[t][seat]["action"]["market"]`), and the engine fills them one unit at a
time in lockstep with the other seat, stopping on an empty shed or an empty
purse. Only the fills move `market["inventory"]`, so only the fills are the
footprint. `scripts/replay_profile.py` already reconstructs that lockstep phase
exactly (it cross-checks itself against the observed money deltas), so this
reuses its `_simulate_market` verbatim rather than re-deriving the rules; the
per-day accumulators it fills (`item_unit_day`, `item_buy_day`) are the table.

Day is `(t - 1) // 24`, the profiler's own definition: `steps[t]["action"]` is
the action that *produced* `steps[t]["observation"]`, so the engine step during
that transition is `t - 1`.

Output is the mean over the replays, rounded to int32, in `spec` product order,
written as JSON for `kagg3.es.kaggle_flow` to load.

    python scripts/replay_flow.py --ours "OurTeam" \
        replays/flow30d_g2520_L_*.json -o src/kagg3/es/kaggle_flow_table.json
"""

import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))

import replay_profile as RP  # noqa: E402

#: `spec.PRODUCTS` order, which is the column order of every flow table. Taken
#: from the profiler so the two files cannot drift apart silently;
#: `_check_product_order` pins both against `spec`.
PRODUCTS = list(RP.PRODUCTS)
N_DAYS = 30


def _check_product_order():
    from kagg3 import spec
    if list(spec.PRODUCTS) != PRODUCTS:
        raise SystemExit(f"product order drift: spec {list(spec.PRODUCTS)} vs "
                         f"replay_profile {PRODUCTS}")
    if int(spec.N_DAYS) != N_DAYS:
        raise SystemExit(f"spec.N_DAYS is {spec.N_DAYS}, not {N_DAYS}")


def flow_from_replay(path, ours_name="OurTeam"):
    """Per-day SELL / BUY_PRODUCT units for each seat of one replay.

    -> (teams, ours_seat, [(sell, buy) per seat]) with `sell`/`buy` as
    `[N_DAYS][n_products]` lists of ints.

    Only the market phase is reconstructed -- the profiler's tile diffs and
    unit-op counting are skipped, which is most of its cost and none of this
    table.
    """
    with open(path) as fh:
        rep = json.load(fh)
    info = rep.get("info", {}) or {}
    teams = info.get("TeamNames") or [a.get("Name") for a in info.get("Agents", [])]
    if not teams or len(teams) != 2:
        raise ValueError(f"{path}: expected two TeamNames, got {teams!r}")
    ours_seat = teams.index(ours_name) if ours_name in teams else None
    steps = rep["steps"]

    accs = [RP.SeatAcc(), RP.SeatAcc()]
    prev_obs0 = prev_priv = None
    for t in range(len(steps)):
        s = steps[t]
        obs0 = s[0]["observation"]
        privs = [s[0]["observation"].get("private", {}) or {},
                 s[1]["observation"].get("private", {}) or {}]
        if prev_obs0 is not None:
            day = (t - 1) // RP.TURNS_PER_DAY
            RP._simulate_market(steps, t, prev_obs0, prev_priv, obs0, accs, day)
        prev_obs0, prev_priv = obs0, privs

    out = []
    for a in accs:
        # Bucket 30 is the profiler's overflow lane for a longer-than-season
        # replay. A 30-day game never fills it; refuse rather than silently
        # dropping units if one ever does.
        for p in PRODUCTS:
            if a.item_unit_day[p][N_DAYS] or a.item_buy_day[p][N_DAYS]:
                raise ValueError(f"{path}: units past day {N_DAYS - 1}")
        sell = [[a.item_unit_day[p][d] for p in PRODUCTS] for d in range(N_DAYS)]
        buy = [[a.item_buy_day[p][d] for p in PRODUCTS] for d in range(N_DAYS)]
        out.append((sell, buy))
    return teams, ours_seat, out


def opponent_flow(path, ours_name="OurTeam"):
    """The non-`ours_name` seat's (sell, buy) tables for one replay."""
    teams, ours_seat, per_seat = flow_from_replay(path, ours_name)
    if ours_seat is None:
        raise ValueError(f"{path}: no seat is {ours_name!r}; teams are {teams!r}")
    opp = 1 - ours_seat
    return teams[opp], per_seat[opp]


def _mean_round(tables):
    """[G][D][P] ints -> [D][P] ints, the mean over games rounded half up.

    Integer arithmetic throughout, so the table is a deterministic function of
    the replays and not of a float's last bit.
    """
    n = len(tables)
    return [[int((sum(g[d][p] for g in tables) * 2 + n) // (2 * n))
             for p in range(len(PRODUCTS))] for d in range(N_DAYS)]


def _season_totals(tables, i):
    """Mean (un-rounded) season total of product `i` over the games."""
    return sum(sum(g[d][i] for d in range(N_DAYS)) for g in tables) / len(tables)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("paths", nargs="+", help="Kaggle replay JSONs")
    ap.add_argument("--ours", default="OurTeam",
                    help="our team name in info.TeamNames; the OTHER seat is "
                         "the one measured")
    ap.add_argument("-o", "--out", default="-", help="JSON out, or - for stdout")
    args = ap.parse_args()

    _check_product_order()

    sells, buys, sources, opps = [], [], [], []
    for p in args.paths:
        team, (sell, buy) = opponent_flow(p, args.ours)
        sells.append(sell)
        buys.append(buy)
        sources.append(os.path.basename(p))
        opps.append(team)
        sys.stderr.write(".")
        sys.stderr.flush()
    sys.stderr.write("\n")

    sell = _mean_round(sells)
    buy = _mean_round(buys)
    doc = {
        "products": PRODUCTS,
        "days": N_DAYS,
        "sell": sell,
        "buy": buy,
        "sell_totals": [sum(row[p] for row in sell) for p in range(len(PRODUCTS))],
        "buy_totals": [sum(row[p] for row in buy) for p in range(len(PRODUCTS))],
        "n_games": len(sources),
        "sources": sources,
        "opponents": sorted(set(opps)),
        "measured": datetime.date.today().isoformat(),
    }

    from kagg3.es import kagg2_flow as K2F
    sys.stderr.write("\nper-product season totals, mean over %d game(s)\n"
                     % len(sources))
    sys.stderr.write("%-12s %9s %9s   %9s %9s   %s\n"
                     % ("product", "kaggleS", "kagg2S", "kaggleB", "kagg2B",
                        "raw sell/buy"))
    for i, name in enumerate(PRODUCTS):
        sys.stderr.write("%-12s %9d %9d   %9d %9d   %.1f / %.1f\n"
                         % (name, doc["sell_totals"][i], K2F.SELL_TOTALS[i],
                            doc["buy_totals"][i], K2F.BUY_TOTALS[i],
                            _season_totals(sells, i), _season_totals(buys, i)))
    sys.stderr.write("%-12s %9d %9d   %9d %9d\n"
                     % ("TOTAL", sum(doc["sell_totals"]), sum(K2F.SELL_TOTALS),
                        sum(doc["buy_totals"]), sum(K2F.BUY_TOTALS)))
    busiest = max(max(max(r) for r in sell), max(max(r) for r in buy))
    sys.stderr.write("busiest day %d units (kagg2 %d)\n"
                     % (busiest, K2F.MAX_DAY_UNITS))

    text = json.dumps(doc, indent=1, sort_keys=True) + "\n"
    if args.out == "-":
        sys.stdout.write(text)
    else:
        with open(args.out, "w") as fh:
            fh.write(text)
        sys.stderr.write("wrote %s\n" % args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
