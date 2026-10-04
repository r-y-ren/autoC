"""Screen existing thetas with the calibrated flow level (scale 1.30, shift +2).

The 2026-08-28 scoreboard sweep found this single level ranks the real engine
at rho 0.99 with near-zero level bias; this scores arbitrary .npy thetas (or
pool.npy rows) with it so real-engine evaluations can be spent on the most
promising ones. Read-only: touches nothing under artifacts/.
"""
import argparse, os, sys
import numpy as np
import jax.numpy as jnp
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fidelity_scoreboard import build_trainer, abs_batch


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("paths", nargs="+", help=".npy thetas; pool.npy files expand to rows")
    ap.add_argument("--resume", default="artifacts/flow4")
    ap.add_argument("--scale", type=int, default=1300)
    ap.add_argument("--shift", type=int, default=2)
    ap.add_argument("--seed", type=int, default=61)
    args = ap.parse_args()
    tr = build_trainer(args.resume, args.seed, quiet=True)
    f = tr.flow_rung
    items = []
    for p in args.paths:
        a = np.load(p).astype(np.float32)
        if a.ndim == 2:
            items += [(f"{p}[{i}]", a[i]) for i in range(a.shape[0])]
        else:
            items.append((p, a))
    rows = []
    for name, th in items:
        m, ai, _ = abs_batch(tr, jnp.asarray(th), args.scale, args.shift)
        d = (m[:, 0] - m[:, 1])[ai == f]
        rows.append((float(d.mean()), float((d > 0).mean()), name))
        print(f"{rows[-1][0]:9.0f} {rows[-1][1]:.3f} {name}", flush=True)
    print("# sorted, best first")
    for mg, w, name in sorted(rows, reverse=True):
        print(f"{mg:9.0f} {w:.3f} {name}")


if __name__ == "__main__":
    main()
