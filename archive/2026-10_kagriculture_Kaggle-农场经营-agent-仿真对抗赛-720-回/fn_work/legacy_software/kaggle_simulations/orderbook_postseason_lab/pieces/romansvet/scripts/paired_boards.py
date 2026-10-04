#!/usr/bin/env python3
"""Paired OFF-vs-ON table on `(seed, opponent, seat)`, with honest seats.

The scratchpad tool this grew out of pairs two `eval_vs_baselines.py` CSVs row
by row and reports a one-sample t on the per-game differences. That t is the
number every local verdict in the campaign log was read off -- and it is
inflated, for the reason section 3 of `docs/2026-09-08-training-plateau-
diagnosis.md` gives: the evaluator plays every board from **both seats**, so
the row count is twice the number of independent boards, and the two mirrored
games are strongly correlated (same market draw, frequently the same outcome).
Dividing by `sqrt(2 * boards)` when the evidence is `boards` inflates t by up
to `sqrt(2)`; the review's probe took ten independent outcomes from t = 3.00 to
t = 4.36 by duplicating each into a second seat and nothing else.

`--group-seats` averages a board's two seat differences into one observation
before taking the spread, which is the grouping `paired_stats()` in
`src/kagg3/es/train.py` now applies inside the gate. The means -- win rates,
mean margins, W/L counts -- are read off the games either way and do not move;
only `sd`, `t` and the `n` the t was computed on change. Both columns are
printed together (`t` and `tg`) so an old verdict can be re-read beside its
grouped self rather than replaced by it.

    scripts/paired_boards.py off.csv on.csv [--group-seats]
"""
from __future__ import annotations

import argparse
import csv
import math
from collections import OrderedDict


def load(path):
    out = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            out[(r["seed"], r["opponent"], r["seat"])] = (
                float(r["mine"]), float(r["theirs"]))
    return out


def short(o):
    if "kaggriculture2" in o:
        return "kagg2"
    return o.rstrip("/").split("/")[-2].replace("opponent_tape_", "tape ")


def _t(values):
    """One-sample t on `values`, and the n it was computed on."""
    n = len(values)
    if n == 0:
        return float("nan"), 0
    mean = sum(values) / n
    sd = (math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1))
          if n > 1 else 0.0)
    if sd <= 0:
        return (float("nan") if mean == 0 else math.copysign(float("inf"), mean)), n
    return mean / (sd / math.sqrt(n)), n


def stats(rows, keys=None):
    """`rows` are `(off_mine, off_theirs, on_mine, on_theirs)` per game.

    `keys` are the matching `(seed, opponent, seat)` tuples; given, the grouped
    statistic is computed alongside the row-wise one.
    """
    n = len(rows)
    if n == 0:
        return None
    d = [(a_m - a_t) - (b_m - b_t) for (b_m, b_t, a_m, a_t) in rows]
    mean = sum(d) / n
    sd = math.sqrt(sum((x - mean) ** 2 for x in d) / (n - 1)) if n > 1 else 0.0
    t = mean / (sd / math.sqrt(n)) if sd > 0 else float("nan")
    tg, ng, sdg = t, n, sd
    if keys is not None:
        # One observation per board: the mean of that board's seats.
        by_board = OrderedDict()
        for k, x in zip(keys, d):
            by_board.setdefault(k[:2], []).append(x)
        per = [sum(v) / len(v) for v in by_board.values()]
        tg, ng = _t(per)
        m = sum(per) / len(per)
        sdg = (math.sqrt(sum((x - m) ** 2 for x in per) / (len(per) - 1))
               if len(per) > 1 else 0.0)
    w_off = sum(1 for (b_m, b_t, a_m, a_t) in rows if b_m > b_t) / n * 100
    w_on = sum(1 for (b_m, b_t, a_m, a_t) in rows if a_m > a_t) / n * 100
    d_ours = sum(a_m - b_m for (b_m, b_t, a_m, a_t) in rows) / n
    d_theirs = sum(a_t - b_t for (b_m, b_t, a_m, a_t) in rows) / n
    won = sum(1 for (b_m, b_t, a_m, a_t) in rows if a_m > a_t and b_m <= b_t)
    lost = sum(1 for (b_m, b_t, a_m, a_t) in rows if a_m <= a_t and b_m > b_t)
    ident = sum(1 for x in d if x == 0)
    return dict(n=n, w_off=w_off, w_on=w_on, d=mean, sd=sd, t=t,
                tg=tg, ng=ng, sdg=sdg,
                d_ours=d_ours, d_theirs=d_theirs, won=won, lost=lost,
                ident=ident)


def main(off_path, on_path, group_seats=False):
    off, on = load(off_path), load(on_path)
    keys = sorted(set(off) & set(on))
    print(f"OFF {off_path}  ({len(off)} rows)")
    print(f"ON  {on_path}  ({len(on)} rows)")
    boards = len({k[:2] for k in keys})
    print(f"paired on (seed, opponent, seat): {len(keys)}"
          f"  boards (seed, opponent): {boards}")
    groups = OrderedDict()
    for k in keys:
        groups.setdefault(short(k[1]), []).append(k)
    groups["ALL"] = keys
    extra = f"{'nb':>6}{'tg':>7}" if group_seats else ""
    hdr = (f"{'opponent':<12}{'n':>5}{'win OFF':>9}{'win ON':>8}"
           f"{'d margin':>10}{'sd':>9}{'t':>7}" + extra
           + f"{'d ours':>9}{'d theirs':>10}{'W':>4}{'L':>4}{'=':>4}")
    print(hdr)
    print("-" * len(hdr))
    for name, ks in groups.items():
        rows = [(off[k][0], off[k][1], on[k][0], on[k][1]) for k in ks]
        s = stats(rows, ks if group_seats else None)
        grouped = f"{s['ng']:>6}{s['tg']:>7.2f}" if group_seats else ""
        print(f"{name:<12}{s['n']:>5}{s['w_off']:>8.1f}%{s['w_on']:>7.1f}%"
              f"{s['d']:>10.0f}{s['sd']:>9.0f}{s['t']:>7.2f}" + grouped
              + f"{s['d_ours']:>9.0f}{s['d_theirs']:>10.0f}"
              f"{s['won']:>4}{s['lost']:>4}{s['ident']:>4}")
    print("W/L = games won that OFF lost / lost that OFF won; = identical margins")
    if group_seats:
        print("nb/tg = boards, and the t with a board's two seats averaged "
              "into one observation (the honest one).")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("off_csv")
    ap.add_argument("on_csv")
    ap.add_argument("--group-seats", action="store_true",
                    help="also report the t with a board's two mirrored seats "
                         "averaged into one observation, which is what the "
                         "gate's paired_stats() now does. The row-wise t is "
                         "kept beside it so old verdicts stay readable.")
    a = ap.parse_args()
    main(a.off_csv, a.on_csv, a.group_seats)
