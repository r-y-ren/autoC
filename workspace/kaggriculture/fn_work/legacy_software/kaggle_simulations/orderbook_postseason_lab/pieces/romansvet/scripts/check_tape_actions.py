"""Release gate: the sim's action-replay seat must reproduce the engine exactly.

`scripts/validate_sim.py` is this gate for *self*-play -- one theta in both
seats, engine vs sim, per-day money. This is the same gate for the seat that
matters for training: our theta in seat 0 against a recorded Kaggle opponent
replayed action-for-action in seat 1 (`es.tape_actions`, `--tape-actions`).

    python scripts/check_tape_actions.py --tape 105443859 \
        --theta artifacts/kagg2_games/thetas/flow102_g280.npy --boards 8

Measured 2026-09-05 on `flow102_g280`, 8 boards a tape, both seats compared:
tape 105443859 8/8 byte-exact, tape 105442685 7/8 (one board 4 coins apart --
`-4` to us and `+4` to the tape, from day 28; days 0-27 exact). 0.44 s a game
warm in a batch of 8, against 0.22 s for the flow rung it replaces.

`--csv` additionally prints an already-recorded paired evaluation as a third
reference; it was produced by whatever planner was checked out at the time, so
a disagreement there is a tree difference and not a simulator one, and the
engine leg run here is the parity reference.
"""

from __future__ import annotations

import argparse
import csv as _csv
import os
import sys
import time

os.environ.setdefault("JAX_PLATFORMS", "cpu")
os.environ.setdefault("XLA_PYTHON_CLIENT_PREALLOCATE", "false")
_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "scripts"))

import numpy as np                                                   # noqa: E402

from kagg3 import spec                                               # noqa: E402
from kagg3.es import tape_actions as TA                              # noqa: E402


def engine_leg(seed, opponent, theta_path):
    """Our theta in seat 0 against the packaged tape in seat 1."""
    import eval_vs_baselines as EV
    win, mine, theirs = EV._play((seed, opponent, 0, theta_path, False, None, None))[:3]
    return int(mine), int(theirs)


def sim_leg(seeds, tape, theta, tables, hi_t, lo_t):
    import jax
    import jax.numpy as jnp
    from kagg3.sim import eod, rollout
    turns = tuple(sorted(set(rollout.MARKET_TURNS) | set(tape.hours)))
    dev = TA.device(jnp, TA.stack([tape]))
    th = jnp.stack([jnp.asarray(theta), jnp.asarray(theta)])
    words = jnp.asarray(np.stack([np.stack([eod.host_stream(int(s), d)
                                            for d in range(spec.N_DAYS)])
                                  for s in seeds]))

    def one(w):
        money, daily, _ = rollout.episode(tables, th, w, hi_t, lo_t,
                                          tape=dev, tape_turns=turns)
        return money, daily
    t0 = time.time()
    f = jax.jit(jax.vmap(one))
    money, daily = f(words)
    money = np.asarray(money)
    compile_and_run = time.time() - t0
    t0 = time.time()
    money2, _ = f(words)
    money2.block_until_ready()
    warm = time.time() - t0
    return money, np.asarray(daily), compile_and_run, warm / len(seeds)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tape", default="105443859")
    ap.add_argument("--theta", default="artifacts/kagg2_games/thetas/flow102_g280.npy")
    ap.add_argument("--boards", type=int, default=8)
    ap.add_argument("--seeds", type=int, nargs="*", default=None)
    ap.add_argument("--csv", default=None, help="an eval_vs_baselines csv to read "
                                                "the board seeds (and a third reference) from")
    ap.add_argument("--no-engine", action="store_true")
    args = ap.parse_args()

    opponent = os.path.join("artifacts", "panel_opp", f"opponent_tape_{args.tape}", "main.py")
    ref = {}
    seeds = args.seeds
    if args.csv:
        with open(args.csv) as fh:
            for row in _csv.DictReader(fh):
                if args.tape in row["opponent"] and int(row["seat"]) == 0:
                    ref[int(row["seed"])] = (int(float(row["mine"])), int(float(row["theirs"])))
        seeds = seeds or list(ref)[:args.boards]
    if not seeds:
        raise SystemExit("pass --seeds or --csv")
    seeds = seeds[:args.boards]

    import jax.numpy as jnp
    from kagg3.sim import eod
    from kagg3.sim.state import build_tables
    theta = np.load(args.theta).astype(np.float32)
    tape = TA.load(os.path.join("artifacts", "tape_actions", f"{args.tape}.npz"))
    hi_t, lo_t = eod.weed_threshold()
    money, daily, t_all, t_game = sim_leg(seeds, tape, theta, build_tables(jnp),
                                          jnp.int32(hi_t), jnp.int32(lo_t))

    eng = []
    if not args.no_engine:
        for s in seeds:
            t0 = time.time()
            eng.append(engine_leg(s, opponent, args.theta))
            print(f"  engine seed {s}: {eng[-1]}  ({time.time()-t0:.1f}s)", flush=True)

    print(f"\ntape {args.tape}   theta {args.theta}   {len(seeds)} boards")
    print(f"sim: {t_all:.1f}s compile+first batch, {t_game:.3f}s/game warm\n")
    hdr = f"{'seed':>12} | {'engine mine':>11} {'engine theirs':>13} | " \
          f"{'sim mine':>9} {'sim theirs':>10} | {'d mine':>8} {'d theirs':>8}"
    print(hdr); print("-" * len(hdr))
    exact = 0
    for i, s in enumerate(seeds):
        sm, st_ = int(money[i][0]), int(money[i][1])
        if eng:
            em, et = eng[i]
            exact += (em == sm and et == st_)
            print(f"{s:>12} | {em:>11} {et:>13} | {sm:>9} {st_:>10} | "
                  f"{sm-em:>+8} {st_-et:>+8}")
        else:
            print(f"{s:>12} | {'-':>11} {'-':>13} | {sm:>9} {st_:>10} |")
        if s in ref:
            rm, rt = ref[s]
            print(f"{'  (csv ref)':>12} | {rm:>11} {rt:>13} |")
    if ref:
        cd = np.array([[int(money[i][0]) - ref[s][0], int(money[i][1]) - ref[s][1]]
                       for i, s in enumerate(seeds) if s in ref])
        nref = len(cd)
        print(f"\nvs csv reference: exact on both seats {int(np.sum(~cd.any(axis=1)))}/{nref}"
              f"   max |err| ours {np.abs(cd[:,0]).max()}  tape {np.abs(cd[:,1]).max()}")
    if eng:
        d = np.array([[int(money[i][0]) - eng[i][0], int(money[i][1]) - eng[i][1]]
                      for i in range(len(seeds))])
        print(f"\nexact on both seats: {exact}/{len(seeds)}")
        print(f"abs err  ours   median {np.median(np.abs(d[:,0])):.0f}  "
              f"max {np.abs(d[:,0]).max()}  mean {np.abs(d[:,0]).mean():.0f}")
        print(f"abs err  tape   median {np.median(np.abs(d[:,1])):.0f}  "
              f"max {np.abs(d[:,1]).max()}  mean {np.abs(d[:,1]).mean():.0f}")
    np.save("/tmp/tape_parity_daily.npy", daily)


if __name__ == "__main__":
    main()
