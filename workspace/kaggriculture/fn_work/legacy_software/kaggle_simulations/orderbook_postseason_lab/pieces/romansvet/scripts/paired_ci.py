"""Paired confidence interval of challenger-minus-incumbent coins over
matched (seed, seat) games. Usage:

    python scripts/paired_ci.py CHALLENGER.csv INCUMBENT.csv --opponent starter

Both files are `eval_vs_baselines.py --csv` output: a header row, then one row
per game. Columns are read by name, so the section-7 metrics that ride after
`theirs` are ignored here -- including the planner-side ones, which a packaged
file agent (`--me`) leaves empty.
"""
from __future__ import annotations

import argparse
import csv
import math


def _rows(path, opponent):
    """The rows of `path` played against `opponent` -- a name or a file path,
    matched against the CSV's opponent column exactly."""
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            if r["opponent"] == opponent:
                yield r


def load(path, opponent, metric):
    """(seed, seat) -> own coins (`coins`) or own - opponent coins (`margin`)."""
    out = {}
    for r in _rows(path, opponent):
        m, t = float(r["mine"]), float(r["theirs"])
        out[(int(r["seed"]), int(r["seat"]))] = m if metric == "coins" else m - t
    return out


def _opponents(path):
    """Every opponent name that appears in `path` -- what the no-match message
    needs to tell the caller which name to pass."""
    with open(path, newline="") as fh:
        return {r["opponent"] for r in csv.DictReader(fh)}


def win_rate(path, opponent):
    """(wins, games), a tie counting half -- the same rule
    `eval_vs_baselines.py` scores with, so one summary cannot carry two
    definitions of one number."""
    n = 0.0
    w = 0.0
    for r in _rows(path, opponent):
        mine, theirs = float(r["mine"]), float(r["theirs"])
        n += 1
        w += 1.0 if mine > theirs else (0.5 if mine == theirs else 0.0)
    return w, int(n)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("challenger")
    ap.add_argument("incumbent")
    ap.add_argument("--opponent", default="starter")
    ap.add_argument("--metric", choices=("coins", "margin"), default="coins",
                    help="own coins, or own minus opponent coins (use margin vs kagg2)")
    args = ap.parse_args()
    a, b = load(args.challenger, args.opponent, args.metric), load(args.incumbent, args.opponent, args.metric)
    keys = sorted(set(a) & set(b))
    if not keys:
        # A paired interval over zero pairs is not a small sample, it is a
        # mistake in the call -- almost always a different `--opponent` name
        # than the CSVs were written with, or two files generated from
        # different `--seed-base` values, which share no (seed, seat) key.
        raise SystemExit(
            f"paired_ci: no matched (seed, seat) games between "
            f"{args.challenger} and {args.incumbent} for opponent "
            f"'{args.opponent}'.\n"
            f"  {args.challenger}: {len(a)} rows vs '{args.opponent}', "
            f"opponents present: {sorted(_opponents(args.challenger))}\n"
            f"  {args.incumbent}: {len(b)} rows vs '{args.opponent}', "
            f"opponents present: {sorted(_opponents(args.incumbent))}\n"
            f"  If both files have rows, the seed bases differ "
            f"(eval_vs_baselines.py --seed-base) and no seed is shared.")
    diffs = [a[k] - b[k] for k in keys]
    n = len(diffs)
    mean = sum(diffs) / n
    sd = math.sqrt(sum((d - mean) ** 2 for d in diffs) / (n - 1)) if n > 1 else float("nan")
    half = 1.96 * sd / math.sqrt(n) if n > 1 else float("nan")
    print(f"n={n} paired games vs {args.opponent} ({args.metric}): challenger - incumbent = "
          f"{mean:+.0f} coins, 95% CI [{mean - half:+.0f}, {mean + half:+.0f}]")
    for label, path in (("challenger", args.challenger), ("incumbent", args.incumbent)):
        w, g = win_rate(path, args.opponent)
        print(f"  {label}: {w:g}/{g} wins vs {args.opponent}")
