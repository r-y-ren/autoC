"""Seed-variance statistics for the local evaluation matrix (m1 wave 2).

Pure-stdlib helpers: Wilson score intervals for win rates over small seed
samples and Student-t confidence intervals for money margins.  Used by
scripts/run_eval.py to build the variance report (anti-self-deception:
how much do outcomes move when only the seed changes?).
"""

from __future__ import annotations

import math
from typing import Dict, List, Optional, Sequence, Tuple

# two-sided 95% Student-t quantiles by degrees of freedom (n-1); normal
# approximation beyond the table
_T95 = {1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571,
        6: 2.447, 7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228,
        15: 2.131, 20: 2.086, 30: 2.042}


def t95(n: int) -> float:
    """Two-sided 95% t quantile for a sample of size n (df = n-1)."""
    if n < 2:
        return float("nan")
    return _T95.get(n - 1, 1.96)


def wilson_ci(wins: float, n: int, z: float = 1.96) -> Tuple[Optional[float],
                                                             Optional[float]]:
    """Wilson score interval for a win rate (ties count as half wins).

    Returns (lo, hi) in [0, 1], or (None, None) for n == 0.  Chosen over the
    naive Wald interval because 4-seed samples sit far from normality.
    """
    if n <= 0:
        return None, None
    p = wins / n
    denom = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return round(max(0.0, center - half), 4), round(min(1.0, center + half), 4)


def margin_stats(margins: Sequence[float]) -> Dict[str, Optional[float]]:
    """Mean/std/95% t-CI/min/max over per-seed money margins (a - b)."""
    n = len(margins)
    if n == 0:
        return {"n": 0, "mean": None, "std": None, "ci95_lo": None,
                "ci95_hi": None, "min": None, "max": None}
    mean = sum(margins) / n
    if n >= 2:
        var = sum((m - mean) ** 2 for m in margins) / (n - 1)
        std = math.sqrt(var)
        half = t95(n) * std / math.sqrt(n)
    else:
        std = 0.0
        half = 0.0
    return {
        "n": n,
        "mean": round(mean, 1),
        "std": round(std, 1),
        "ci95_lo": round(mean - half, 1),
        "ci95_hi": round(mean + half, 1),
        "min": round(min(margins), 1),
        "max": round(max(margins), 1),
    }


def pair_variance(games: List[Dict], a: str, b: str) -> Dict:
    """Variance report for one pairing: outcome spread + margin spread.

    `games` are run_match results (players == [a, b]); only exact-order
    pairings are considered, matching summarize_games semantics.
    """
    wins = losses = ties = 0
    margins: List[float] = []
    seeds: List[int] = []
    for g in games:
        if g.get("players") != [a, b]:
            continue
        wl = g.get("winner_label")
        if wl == a:
            wins += 1
        elif wl == b:
            losses += 1
        else:
            ties += 1
        rw = g.get("rewards") or [0.0, 0.0]
        margins.append(float(rw[0]) - float(rw[1]))
        seeds.append(g.get("seed"))
    n = len(margins)
    wr = (wins + 0.5 * ties) / n if n else None
    lo, hi = wilson_ci(wins + 0.5 * ties, n)
    ms = margin_stats(margins)
    mixed = n > 0 and wins > 0 and losses > 0  # outcome flips across seeds
    return {
        "pair": f"{a} vs {b}",
        "games": n,
        "seeds": seeds,
        "wins": wins, "losses": losses, "ties": ties,
        "win_rate": round(wr, 4) if wr is not None else None,
        "win_rate_ci95": [lo, hi] if lo is not None else None,
        "margin": ms,
        "outcome_flips_across_seeds": mixed,
    }


def most_volatile_pair(reports: List[Dict]) -> Optional[Dict]:
    """Pick the least stable pairing: outcome flips first (a real risk of
    drawing the opposite conclusion from another seed), then widest Wilson
    CI, then widest margin CI."""
    def key(r: Dict):
        ci = r.get("win_rate_ci95") or [0, 0]
        m = r.get("margin") or {}
        width = (ci[1] - ci[0]) if ci else 0.0
        mwidth = (m.get("ci95_hi") or 0) - (m.get("ci95_lo") or 0)
        return (1 if r.get("outcome_flips_across_seeds") else 0, width, mwidth)
    if not reports:
        return None
    return max(reports, key=key)
