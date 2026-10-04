"""Run the trainer's PINNED real gate once, standalone, in the real engine.

`RealGate` is built to be polled by a trainer that never blocks, which makes it
awkward to point at four tapes and ask what it says. This does exactly that:
one candidate, one incumbent, the pinned live-replica set, and the verdict --
plus the per-tape coins of the candidate's own leg, so the run can be checked
against an independently produced ledger (`--reference`, e.g. the CSV
`scratchpad/lossflip/run.sh` writes). `--pinned-seats 1` plays seat 0 only,
which is what the mode is worth once the town is pinned: both seats of a
pinned tape return the same coins, so the second is a re-measurement.

The point of the reference check is the property the whole mode rests on: with
`KAGG3_TOWN_SCHEDULE` pinning the end-of-day shop, a `--with-town` package
replays the live game, so a gate leg and an independently produced ledger must
agree. Measured 2026-09-09 on four band tapes, they agree on the *outcome* in
every row and in both seats, on every seed base tried, and on the coins for
most rows -- the residue is the weeds, which `_end_of_day` still keys on the
seed, and which can move a board by a fraction of a percent without changing
hands. So expect the W/L column to match exactly and a row or two of coins to
differ when the reference was taken on another seed base; a row that changes
HANDS is the thing to go and look at, because the gate counts those.

    python scripts/pinned_gate_check.py \\
        --pinned artifacts/town_schedules.json \\
        --theta artifacts/kagg2_games/thetas/flow135_g350_gpfwd.npy \\
        --opponents artifacts/panel_opp_town/opponent_tape_*/main.py \\
        --reference scratchpad/lossflip/flow135_g350.csv

Candidate and incumbent default to the same theta, which is the identity check:
0 flips, 0 drops, and a refusal (nothing moved).
"""
from __future__ import annotations

import argparse
import csv
import os
import shutil
import sys
import tempfile

os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__))), "src"))

import numpy as np

from kagg3.es.train import RealGate, pinned_tape_id, read_eval_games


def _rows_by_tape(rows):
    """`{(tape id, seat): (mine, theirs)}` from a `read_eval_games` map."""
    return {(pinned_tape_id(opp), int(seat)): v
            for (_seed, opp, seat), v in rows.items()}


def _reference(path):
    """The same shape, off an `eval_vs_baselines.py --csv`."""
    out = {}
    with open(path, newline="") as fh:
        for r in csv.DictReader(fh):
            out[(pinned_tape_id(r["opponent"]), int(r["seat"]))] = (
                float(r["mine"]), float(r["theirs"]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--pinned", required=True, help="town schedule JSON")
    ap.add_argument("--theta", required=True, help="the incumbent")
    ap.add_argument("--candidate", default=None,
                    help="the candidate (default: --theta, the identity check)")
    ap.add_argument("--opponents", nargs="+", required=True,
                    help="--with-town opponent packages (main.py)")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--seed-base", type=int, default=20260825)
    ap.add_argument("--min-flips", type=int, default=1)
    ap.add_argument("--pinned-seats", "--real-gate-pinned-seats",
                    dest="pinned_seats", type=int, choices=(1, 2), default=2,
                    help="seats of every pinned board to play, the trainer's "
                         "--real-gate-pinned-seats. 2 (default) plays each "
                         "tape in both seats; 1 plays seat 0 only, which is "
                         "the honest count -- both seats of a pinned tape "
                         "return the same coins -- and halves the wall clock")
    ap.add_argument("--metric", choices=("win", "margin"), default="win")
    ap.add_argument("--reference", default=None,
                    help="a CSV of the same games to check the candidate's "
                         "leg against, row by row")
    ap.add_argument("--run-dir", default=None,
                    help="where real_gate.log/csv go (default: a temp dir)")
    a = ap.parse_args(argv)

    run_dir = a.run_dir or tempfile.mkdtemp(prefix="pinned_gate_")
    os.makedirs(run_dir, exist_ok=True)
    inc = np.load(a.theta).astype(np.float32)
    cand = np.load(a.candidate).astype(np.float32) if a.candidate else inc
    gate = RealGate(run_dir, list(a.opponents), pinned=a.pinned,
                    workers=a.workers, seed_base=a.seed_base,
                    metric=a.metric, min_flips=a.min_flips,
                    pinned_seats=a.pinned_seats)
    # The bar has a theta but no numbers yet, which is what makes the round
    # pair: `_fresh_leg` plays the incumbent on the same set, and the verdict
    # is the flips between the two legs rather than a baseline taken unopposed.
    gate.record_theta = inc

    print(f"[pinned check] {len(a.opponents)} tapes x {gate.seats} seat"
          f"{'' if gate.seats == 1 else 's'} = "
          f"{len(a.opponents) * gate.seats} games, schedule "
          f"{gate.pinned}, run dir {run_dir}", flush=True)
    gate.propose(cand, 0)
    legs, res = [], None
    while gate.proc is not None:
        leg = gate.leg
        gate.proc.wait()
        # Read before `poll`, which launches the next leg and deletes the file.
        legs.append((leg, read_eval_games(gate.csv_path)))
        res = gate.poll()
        if res is not None:
            break
    if res is None:
        print("[pinned check] the gate produced no verdict", flush=True)
        return 2

    print(f"[pinned check] games {res.get('games')}  "
          f"win {res.get('win')}  margin {res.get('margin'):+.0f}")
    print(f"[pinned check] FLIPS +{res.get('pinned_flips')} "
          f"DROPS -{res.get('pinned_drops')}  "
          f"wins {res.get('pinned_incumbent_wins')} -> "
          f"{res.get('pinned_wins')}  accepted={res['accepted']}")
    if res.get("pinned_flipped"):
        print("[pinned check] flipped: " + " ".join(res["pinned_flipped"]))
    if res.get("pinned_dropped"):
        print("[pinned check] dropped: " + " ".join(res["pinned_dropped"]))

    cand_rows = _rows_by_tape(dict(legs[0][1] or {}))
    for (tape, seat), (mine, theirs) in sorted(cand_rows.items()):
        print(f"  {tape}/{seat}  mine {mine:9.0f}  theirs {theirs:9.0f}  "
              f"{'W' if mine > theirs else 'L'}")

    rc = 0
    if a.reference:
        ref = _reference(a.reference)
        shared = [k for k in cand_rows if k in ref]
        bad = [k for k in shared if cand_rows[k] != ref[k]]
        print(f"[pinned check] reference {a.reference}: {len(shared)} shared "
              f"rows, {len(bad)} disagree")
        for k in bad:
            print(f"  MISMATCH {k[0]}/{k[1]}: gate {cand_rows[k]} "
                  f"vs reference {ref[k]}")
        rc = 1 if bad or not shared else 0
    if not a.run_dir:
        with open(os.path.join(run_dir, "real_gate.log")) as fh:
            print("[pinned check] log:\n" + fh.read())
        shutil.rmtree(run_dir, ignore_errors=True)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
