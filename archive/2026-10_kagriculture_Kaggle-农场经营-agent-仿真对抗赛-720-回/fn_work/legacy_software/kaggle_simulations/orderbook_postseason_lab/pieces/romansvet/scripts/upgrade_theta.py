"""Rewrite an older-layout theta at this build's layout, meaning intact.

    python scripts/upgrade_theta.py OLD.npy NEW.npy

The policy layout only ever grows at the tail (`core/policy.SHAPES`), and every
appended block decodes to its own no-op at zero, so an upgrade is a zero pad --
with the one documented exception `policy.pad` handles, the hire-bias day
buckets, which carry the season-constant bias of a pre-4,848 theta rather than
zeroing it. This script is `policy.pad` and a file: the same function
`policy.unpack` decodes a short theta with and the same one `scripts/train.py
--init-theta` applies in memory, so an upgraded file and the original play
identically wherever both are accepted.

The point of writing the padded file out is the places that will not pad for
you -- `scripts/package_submission.py` ships `theta.npy` as it finds it, and a
judge run wants one artifact to point at. Verify with
`tests/test_forecast_feature.py::test_upgraded_theta_decodes_identically` and,
for the current tail block `gp`,
`tests/test_global_product.py::test_upgraded_theta_decides_identically`.

Refuses a theta already at or past the current length: there is nothing to add,
and a longer one was written by a newer layout this build cannot interpret.
"""
import argparse
import sys

sys.path.insert(0, "src")
import numpy as np

from kagg3.core import policy as PO


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="the theta to upgrade")
    ap.add_argument("dst", help="where to write the upgraded theta")
    ap.add_argument("--force", action="store_true",
                    help="write even if the source is already this layout")
    a = ap.parse_args()

    old = np.load(a.src).astype(np.float32)
    if old.ndim != 1:
        raise SystemExit(f"{a.src}: expected a flat theta, got shape {old.shape}")
    n = int(old.shape[0])
    if n > PO.N_PARAMS:
        raise SystemExit(
            f"{a.src}: {n} params, longer than this build's layout of "
            f"{PO.N_PARAMS}. That checkpoint was written by a newer policy "
            f"layout; nothing here can interpret the extra block.")
    if n == PO.N_PARAMS and not a.force:
        raise SystemExit(f"{a.src}: already {n} params, nothing to upgrade "
                         f"(pass --force to copy it anyway).")

    new = PO.pad(old).astype(np.float32)
    assert new.shape == (PO.N_PARAMS,)
    assert np.array_equal(new[:n], old), "pad moved a trained coordinate"
    np.save(a.dst, new)
    added = [name for name, shape in PO.SHAPES
             if PO.offset(name) >= n]
    print(f"{a.src}: {n} -> {PO.N_PARAMS} params -> {a.dst}")
    print(f"  blocks appended: {', '.join(added) or '(none)'}")
    print(f"  |theta| {float(np.linalg.norm(old)):.4f} -> "
          f"{float(np.linalg.norm(new)):.4f}")


if __name__ == "__main__":
    main()
