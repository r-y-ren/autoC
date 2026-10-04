"""One tracker row from one `eval_vs_baselines.py --csv` file.

`scripts/remote_eval_kagg2.sh` used to fold the per-game CSV into a TSV line
with awk. The line now carries a paired confidence interval and a Wilson
interval, which awk can express but nothing can test, so the arithmetic lives
here: stdlib only, no engine import, so `tests/test_kagg2_track_row.py` runs it
in milliseconds.

Column order is append-only. Everything through `kagg2_coins` is byte-compatible
with the rows already in `artifacts/kagg2_track.tsv`; the four columns after it
are new, so an old row parses as a new row with the tail missing.

Usage:
    python scripts/kagg2_track_row.py GAMES.csv --run p2s0 --gen 7830 \
        --kagg2 ../kaggriculture2/main.py --ts "$(date -Is)" \
        [--track artifacts/kagg2_track.tsv]
"""
from __future__ import annotations

import argparse
import csv
import math
import os

#: 95 % two-sided normal quantile -- the same constant `scripts/paired_ci.py`
#: quotes its interval with, so two summaries of one campaign cannot disagree
#: about what "95 %" means.
Z95 = 1.96

#: The tracker's TSV columns, in order. Append only: a row written before a
#: column existed is still a valid prefix of a current row.
COLUMNS = ("ts", "run", "gen", "n_games", "coins_vs_starter", "coins_vs_kagg2",
           "margin_vs_kagg2", "win_pct_vs_kagg2", "kagg2_coins",
           "margin_ci95", "win_lo", "win_hi", "joint_coins")

#: `%`-formats for `COLUMNS`, so the row is one formatted join.
FORMATS = ("%s", "%s", "%s", "%d", "%.0f", "%.0f",
           "%+.0f", "%.1f", "%.0f",
           "%.0f", "%.1f", "%.1f", "%.0f")


def read_games(path):
    """The `(seed, seat, mine, theirs)` rows of an `eval_vs_baselines.py --csv`
    file, grouped by opponent name.

    The opponent column holds whatever was passed to `--opponents` -- a builtin
    name like `starter`, or the path of a packaged agent -- and is matched
    exactly, the way `scripts/paired_ci.py` matches it.
    """
    by_opponent = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            by_opponent.setdefault(r["opponent"], []).append(
                (int(r["seed"]), int(r["seat"]), float(r["mine"]), float(r["theirs"])))
    return by_opponent


def win_score(games):
    """Wins over `games`, a tie counting half -- `eval_vs_baselines.py`'s rule."""
    return sum(1.0 if mine > theirs else (0.5 if mine == theirs else 0.0)
               for _, _, mine, theirs in games)


def wilson(wins, n, z=Z95):
    """Wilson score interval for `wins`/`n`, as a `(lo, hi)` pair of fractions.

    `wins` may be fractional -- a tie counts half here, and the interval is
    quoted on that same half-win rate rather than on a re-rounded integer, so
    the point estimate always sits inside the interval printed beside it.

    Reference values from the plan's §3.5: 0/48 -> [0.0 %, 7.4 %],
    8/16 -> [28.0 %, 72.0 %], 24/48 -> [36.4 %, 63.6 %]. Quote it so nobody
    over-reads the win column: at this margin the win rate resolves nothing.
    """
    if n <= 0:
        return (float("nan"), float("nan"))
    p = wins / n
    denom = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z / denom * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    # The clamps against `p` are algebraically no-ops -- the Wilson interval
    # always contains its own point estimate -- and are here for floating
    # point: at 0/48 the lower end comes out 7e-18 rather than 0, which prints
    # as an interval that excludes the rate it is quoted beside.
    return (max(0.0, min(p, centre - half)), min(1.0, max(p, centre + half)))


def paired_margin(games):
    """`(mean margin, 95 % half-width, n seeds)` over per-seed mean margins.

    Every seed is played in **both** seats against the same episode randomness,
    so the two games of a seed are not two independent draws: pooling all 2n of
    them and dividing the sd by sqrt(2n) prices the seat pair as new
    information it is not. Averaging a seed's seats first and taking the
    interval over seeds is the paired form.

    It is a *different* pairing from `scripts/paired_ci.py`'s, and the wider
    one: that pairs two files on `(seed, seat)` and so cancels the episode
    outright, while this pairs the two seats within one file and cancels only
    the seat. This column says how well one row pins its own margin down; a
    challenger-vs-incumbent decision still wants `paired_ci.py` over the two
    kept CSVs, which is the interval §3.5.4 gates a promotion on.

    The mean is unchanged by the pairing whenever both seats are present, which
    is why `margin_vs_kagg2` keeps the value the awk summary gave it.
    """
    per_seed = {}
    for seed, _, mine, theirs in games:
        per_seed.setdefault(seed, []).append(mine - theirs)
    diffs = [sum(v) / len(v) for v in per_seed.values()]
    n = len(diffs)
    mean = sum(diffs) / n if n else float("nan")
    if n < 2:
        return (mean, float("nan"), n)
    var = sum((d - mean) ** 2 for d in diffs) / (n - 1)
    return (mean, Z95 * math.sqrt(var) / math.sqrt(n), n)


def summarise(by_opponent, kagg2, starter="starter"):
    """The tracker row's numeric fields, as a `COLUMNS`-keyed dict.

    `joint_coins` is the two farms' coins added up. It is a diagnostic -- the
    market's temperature, which falls as the margin closes in the good
    scenarios too -- and deliberately not a gate. The gate against buying
    margin by burning the market is `coins_vs_starter`, where there is no
    market worth burning.
    """
    missing = [name for name in (starter, kagg2) if not by_opponent.get(name)]
    if missing:
        raise SystemExit(
            f"kagg2_track_row: no rows for {missing}; opponents present: "
            f"{sorted(by_opponent)}")
    s_games, k_games = by_opponent[starter], by_opponent[kagg2]
    n = len(k_games)
    mine = sum(g[2] for g in k_games) / n
    theirs = sum(g[3] for g in k_games) / n
    margin, ci95, _ = paired_margin(k_games)
    wins = win_score(k_games)
    lo, hi = wilson(wins, n)
    return {"n_games": n,
            "coins_vs_starter": sum(g[2] for g in s_games) / len(s_games),
            "coins_vs_kagg2": mine,
            "margin_vs_kagg2": margin,
            "win_pct_vs_kagg2": 100.0 * wins / n,
            "kagg2_coins": theirs,
            "margin_ci95": ci95,
            "win_lo": 100.0 * lo,
            "win_hi": 100.0 * hi,
            "joint_coins": mine + theirs}


def format_row(fields):
    """`fields` (a `summarise` dict plus `ts`/`run`/`gen`) as one TSV line."""
    return "\t".join(f % fields[c] for c, f in zip(COLUMNS, FORMATS))


def header_line():
    return "# " + "\t".join(COLUMNS)


def ensure_header(track):
    """Give `track` a commented header line if it has none.

    A new file gets one before its first row. A file written by the older
    script already opens with a bare (uncommented) 9-column header, and that
    line is left alone -- rewriting history to claim four columns those rows
    never carried would be a lie -- so the comment is appended at the point the
    format widened, and the file self-describes from there on.
    """
    if os.path.exists(track) and os.path.getsize(track) > 0:
        with open(track) as fh:
            if any(line.startswith("#") for line in fh):
                return
    with open(track, "a") as fh:
        fh.write(header_line() + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="an eval_vs_baselines.py --csv file")
    ap.add_argument("--run", required=True)
    ap.add_argument("--gen", required=True)
    ap.add_argument("--kagg2", required=True,
                    help="the opponent column's value for kagg2 (its --opponents path)")
    ap.add_argument("--starter", default="starter")
    ap.add_argument("--ts", required=True)
    ap.add_argument("--track", help="TSV to append the row to (printed either way)")
    args = ap.parse_args()

    fields = summarise(read_games(args.csv), args.kagg2, args.starter)
    fields.update(ts=args.ts, run=args.run, gen=args.gen)
    row = format_row(fields)
    if args.track:
        ensure_header(args.track)
        with open(args.track, "a") as fh:
            fh.write(row + "\n")
    print(row)
