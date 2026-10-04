#!/usr/bin/env python3
"""Append ONE row to S/pipeline/ledger.tsv from a cycle's artefacts.

    python S/pipeline/ledger.py <cycle> <run> <centre.npy> <gens> <hold_d> \
        <pool511.txt> <hiband.txt> <clone.txt|-> <self.txt|-> <promoted> <ship_ready>

Every column is a number someone can check later; nothing here is a judgement.
A missing input file becomes `-`, never a zero.
"""
from __future__ import annotations

import hashlib
import os
import re
import sys

import numpy as np

R = "/mnt/e/_work/kaggriculture3"
LEDGER = os.path.join(R, "S", "pipeline", "ledger.tsv")
COLS = ["utc", "cycle", "run", "centre", "md5", "gens", "hold_d",
        "pool_n", "pool_dmargin", "pool_se", "pool_t", "pool_dtheirs",
        "pool_flips", "pool_signp", "hiband_dmargin", "hiband_t",
        "clone_dmargin", "clone_t", "self_t", "promoted", "ship_ready"]


def legrow(path, want):
    if not path or path == "-" or not os.path.exists(path):
        return None
    for ln in open(path):
        f = ln.split()
        if f and f[0] == want and len(f) >= 12:
            try:
                return dict(n=f[1], dmargin=f[3], se=f[4], t=f[5],
                            dtheirs=f[8], flips=f[-2], signp=f[-1])
            except IndexError:
                return None
    return None


def grab(path, pat, *groups):
    if not path or path == "-" or not os.path.exists(path):
        return ["-"] * len(groups)
    m = re.search(pat, open(path).read())
    return [m.group(g) for g in groups] if m else ["-"] * len(groups)


def main(cycle, run, centre, gens, hold, pool, hib, clone, selfp, promoted, ship):
    from datetime import datetime, timezone
    th = np.load(centre).reshape(-1)
    p = legrow(pool, "POOLED511") or legrow(pool, "POOLED278") or {}
    # HIBAND's own reader prints `cand  ... mean margin +N`; the paired cell is
    # the `HIBAND` row when a base leg of the same set exists.
    h = legrow(hib, "HIBAND") or {}
    c = grab(clone, r"V48CLONE\s+\d+ boards\s+dmargin\s+([-+]\d+)\s+se\s+\d+\s+t\s+([-+][\d.]+)", 1, 2)
    s = grab(selfp, r"t\s+([-+][\d.]+)", 1)
    row = [datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), cycle, run,
           os.path.relpath(centre, R), hashlib.md5(th.tobytes()).hexdigest()[:8],
           gens, hold,
           p.get("n", "-"), p.get("dmargin", "-"), p.get("se", "-"), p.get("t", "-"),
           p.get("dtheirs", "-"), p.get("flips", "-"), p.get("signp", "-"),
           h.get("dmargin", "-"), h.get("t", "-"), c[0], c[1], s[0], promoted, ship]
    new = not os.path.exists(LEDGER)
    with open(LEDGER, "a") as fh:
        if new:
            fh.write("\t".join(COLS) + "\n")
        fh.write("\t".join(str(x) for x in row) + "\n")
    print("ledger += " + "\t".join(str(x) for x in row))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(*sys.argv[1:12]))
