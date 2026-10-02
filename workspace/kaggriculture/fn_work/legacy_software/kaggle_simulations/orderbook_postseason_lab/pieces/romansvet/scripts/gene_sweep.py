"""Which head genes are trapped? Usage:

    python scripts/gene_sweep.py artifacts/run/theta.npy [--genes 0-22] [--abs-pairs 32]

Genes 0..17 are head biases (gb2), 18..20 the unblock block (gb5), 21..22 the
development block (gb6).
"""
import argparse, sys
sys.path.insert(0, "src")
import numpy as np

from kagg3.core import policy as PO
from kagg3.es.train import Config, Trainer
from kagg3.es import sweep as S


def pad_theta(theta: np.ndarray) -> np.ndarray:
    """Pad an old-layout theta to PO.N_PARAMS with `PO.pad`, which is
    `PO.unpack`'s own pad; reject a theta longer than the current layout."""
    if theta.shape[0] > PO.N_PARAMS:
        raise ValueError(
            f"theta has {theta.shape[0]} params, longer than PO.N_PARAMS={PO.N_PARAMS}"
        )
    return PO.pad(theta)

# "(dead)" = nothing in `brain.decide` reads the output any more, and
# PLANNER_V3_1 section 2 masks the parameter column out of the ES perturbation
# and update (`policy.DEAD_HEAD` / `DEAD_AUX`). A fresh lineage therefore leaves
# those columns at their init and sweeping one is a null-effect sanity row; only
# a pre-mask checkpoint still carries trained noise there. Live: 1, 5, 6, 7 and
# aux 19, 20.
GENE_NAMES = {0: "hire(dead)", 1: "land", 2: "fertilize(dead)", 3: "feed(dead)",
              4: "care(dead)", 5: "dev", 6: "animal_share", 7: "crop_sharp",
              8: "ord_wheat(dead)", 9: "ord_fert(dead)", 10: "ord_seeds(dead)",
              11: "ord_animal(dead)", 12: "ord_land(dead)",
              13: "head13(dead)", 14: "head14(dead)", 15: "head15(dead)",
              16: "head16(dead)", 17: "head17(dead)",
              18: "fert_buy(dead)", 19: "land_afford", 20: "free_urgency",
              21: "compact", 22: "dev_weight"}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("theta")
    ap.add_argument("--genes", default="0-22")
    ap.add_argument("--abs-pairs", type=int, default=32)
    ap.add_argument("--n-archetypes", type=int, default=4)
    ap.add_argument("--chunk", type=int, default=1024)
    args = ap.parse_args()
    lo, hi = (int(x) for x in args.genes.split("-"))
    theta = pad_theta(np.load(args.theta).astype(np.float32))
    tr = Trainer(Config(pop=2, episodes=2, chunk=args.chunk, abs_pairs=args.abs_pairs,
                        n_archetypes=args.n_archetypes), seed=0)
    rows = S.sweep(tr, theta, range(lo, hi + 1))
    print(f"base {rows[0]['base']:,.0f} coins vs {len(tr.archetypes)} archetypes x {args.abs_pairs} pairs x 2 seats")
    print(f"{'gene':>4} {'name':16} {'verdict':9} " + " ".join(f"{d:>7}" for d in S.DELTAS))
    for r in rows:
        print(f"{r['gene']:>4} {GENE_NAMES[r['gene']]:16} {r['verdict']:9} "
              + " ".join(f"{r['scores'][d] - r['base']:>+7.0f}" for d in S.DELTAS))
