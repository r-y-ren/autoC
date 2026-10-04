"""Cut an action tape for the sim's replay seat out of a packaged tape opponent.

    python scripts/make_tape_actions.py 105443859 [105442685 ...]
    python scripts/make_tape_actions.py --replay scratchpad/kaggle/replays/1054.json

An episode id is looked up as `artifacts/panel_opp/opponent_tape_<ep>/main.py`,
which is the *same* package `scripts/eval_vs_baselines.py --opponents` runs in
the engine, so the sim seat and the engine seat replay one artifact.  Output is
`artifacts/tape_actions/<ep>.npz` -- see `kagg3.es.tape_actions` for the layout.
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import numpy as np                                                   # noqa: E402

from kagg3.es import tape_actions as TA                              # noqa: E402

ROOT = os.path.join(os.path.dirname(__file__), "..")
PKG_DIR = os.path.join(ROOT, "artifacts", "panel_opp")
PKG = os.path.join("%s", "opponent_tape_%s", "main.py")
OUT = os.path.join(ROOT, "artifacts", "tape_actions")


def town_from_replay(path):
    """`tape_opponent.extract_town` on a raw replay, without importing it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import tape_opponent                                             # noqa: E402
    return tape_opponent.extract_town(json.load(open(path)))


def from_replay(path, seat=None, ours="OurTeam"):
    """The same extraction `tape_opponent.extract_tape` does, on a raw replay."""
    replay = json.load(open(path))
    names = list((replay.get("info") or {}).get("TeamNames") or [])
    if seat is None:
        hits = [i for i, n in enumerate(names) if n != ours]
        if len(hits) != 1:
            raise SystemExit(f"cannot infer the opponent seat from {names}; pass --seat")
        seat = hits[0]
    steps = replay["steps"]
    tape = []
    for t in range(1, len(steps)):
        a = steps[t][seat].get("action")
        if not isinstance(a, dict):
            a = {}
        tape.append({"farmer": list(a.get("farmer") or ["PASS"]),
                     "hands": [list(o or ["PASS"]) for o in (a.get("hands") or [])],
                     "market": [list(o) for o in (a.get("market") or [])]})
    return tape


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("episodes", nargs="*", help="episode ids under artifacts/panel_opp")
    ap.add_argument("--replay", help="raw replay json instead of a package")
    ap.add_argument("--seat", type=int, default=None, help="--replay only")
    ap.add_argument("--out-dir", default=OUT)
    ap.add_argument("--pkg-dir", default=PKG_DIR,
                    help="directory of `opponent_tape_<ep>/main.py` packages to "
                         "cut from (default artifacts/panel_opp). Point it at a "
                         "`--with-town` re-cut (artifacts/panel_opp_town) so the "
                         "npz and the engine seat come off ONE artifact, which "
                         "is what makes the sim seat and the engine seat agree")
    ap.add_argument("--with-town", action="store_true",
                    help="also store the recorded TOWN (the per-unlock-day shop "
                         "list) under the npz's `town` key, so `sim.eod` can pin "
                         "it instead of drawing shops. Read from the package's "
                         "`_TOWN` (cut by `tape_opponent.py --with-town`) or, "
                         "with --replay, straight off the replay. Off by "
                         "default, and a tape cut without it is the same "
                         "six-array file it always was")
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)
    jobs = []
    if args.replay:
        ep = os.path.splitext(os.path.basename(args.replay))[0]
        jobs.append((ep, from_replay(args.replay, args.seat),
                     town_from_replay(args.replay) if args.with_town else None))
    for ep in args.episodes:
        town = None
        if args.with_town:
            town = TA.town_from_package(PKG % (args.pkg_dir, ep))
            if not town:
                raise SystemExit(
                    f"--with-town: {PKG % (args.pkg_dir, ep)} carries no `_TOWN`; re-cut "
                    f"package with `scripts/tape_opponent.py --with-town`")
        jobs.append((ep, TA.tape_from_package(PKG % (args.pkg_dir, ep)), town))
    if not jobs:
        ap.error("nothing to do: pass episode ids or --replay")

    for ep, tape, town in jobs:
        try:
            ta = TA.build(tape, episode=int(ep), town=town)
        except ValueError:
            ta = TA.build(tape, town=town)
        path = os.path.join(args.out_dir, f"{ep}.npz")
        TA.save(path, ta)
        live = int(np.sum(ta.uop != 0))
        orders = int(np.sum(ta.mop != 0))
        print(f"{ep}: {len(tape)} frames -> {live} unit ops, {orders} market orders, "
              f"market hours {ta.hours}"
              + (f", town {len(TA.town_schedule(ta.town))} unlocks"
                 if ta.town is not None else "")
              + (f", DROPPED {ta.dropped[:4]}" if ta.dropped else ""))
        print(f"  wrote {path}")


if __name__ == "__main__":
    main()
