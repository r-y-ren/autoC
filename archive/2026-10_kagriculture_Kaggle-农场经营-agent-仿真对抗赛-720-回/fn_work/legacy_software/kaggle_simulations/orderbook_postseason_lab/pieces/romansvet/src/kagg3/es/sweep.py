"""Trapped-gene detection by head-bias shifts.

Shifting a bias by delta moves that output by delta in every state, so it
is the cleanest single-gene counterfactual that stays a plain theta. A gene
whose every shift scores below the base is "trapped": its payoff is coupled
to another decision the planner makes for it (fertilize -> market buy was
the 2026-08-23 case).

Genes 0..17 are the head biases `gb2`; 18..20 are the unblock block `gb5`;
21..22 are the development block `gb6` (compact, dev_weight).
"""
from __future__ import annotations

import numpy as np

from ..core import policy as PO

DELTAS = (-3.0, -1.0, -0.3, 0.3, 1.0, 3.0)
N_AUX_END = PO.N_HEAD_OUT + PO.N_AUX_OUT
N_GENES = N_AUX_END + PO.N_DEV_OUT


def gene_offset(g):
    if g < PO.N_HEAD_OUT:
        return PO.offset("gb2") + g
    if g < N_AUX_END:
        return PO.offset("gb5") + (g - PO.N_HEAD_OUT)
    if g < N_GENES:
        return PO.offset("gb6") + (g - N_AUX_END)
    raise IndexError(g)


def shifted(theta, g, delta):
    out = np.array(theta, np.float32, copy=True)
    out[gene_offset(g)] += delta
    return out


def classify(base, scores, tol):
    up_pos = any(s > base + tol for d, s in scores.items() if d > 0)
    up_neg = any(s > base + tol for d, s in scores.items() if d < 0)
    all_down = all(s < base - tol for s in scores.values())
    if all_down:
        return "trapped"
    if up_pos and not up_neg:
        return "uphill+"
    if up_neg and not up_pos:
        return "uphill-"
    return "flat"


def sweep(tr, theta, genes, deltas=DELTAS, tol=500.0):
    base, _ = tr.absolute_eval(np.asarray(theta))
    rows = []
    for g in genes:
        scores = {float(d): tr.absolute_eval(shifted(theta, g, d))[0] for d in deltas}
        rows.append({"gene": int(g), "base": base, "scores": scores,
                     "verdict": classify(base, scores, tol)})
    return rows
