"""Frozen regression line for the Kaggriculture eval matrix.

Pure functions over an already-played game stream + Elo table -- no engine
calls -- so the gate is unit-testable without running episodes.

Two invariants (frozen at m0-skeleton, campaign K-03 wave 1):

1. Elo ordering is strictly descending:
   submission > baseline_wheat > greedy_carrot > starter > random > pass
2. The submission bot is undefeated against the frozen opponent pool
   (0 losses in every game it plays, including head-to-head vs baseline).

scripts/run_eval.py --assert-regression evaluates these after a run and
exits non-zero with a diff table on violation.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List

SUBMISSION = "submission"

# Frozen ladder order (strict >, ties or inversions fail the gate).
EXPECTED_ELO_ORDER: List[str] = [
    "submission",
    "baseline_wheat",
    "greedy_carrot",
    "starter",
    "random",
    "pass",
]


def _ratings_from_rows(ranked_rows: Iterable[Dict[str, Any]]) -> Dict[str, float]:
    """Accept EloTable.ranked() rows or plain {"name","rating"} dicts."""
    ratings: Dict[str, float] = {}
    for row in ranked_rows:
        ratings[row["name"]] = float(row["rating"])
    return ratings


def submission_losses(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Games the submission bot lost (it may sit on either side)."""
    lost = []
    for g in games:
        players = list(g.get("players") or [])
        winner = g.get("winner_label")
        if SUBMISSION in players and winner is not None and winner != SUBMISSION:
            lost.append(g)
    return lost


def check_regression(games: List[Dict[str, Any]],
                     ranked_rows: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    """Evaluate both frozen invariants.

    Returns {"ok": bool, "failures": [str, ...], "diff_table": [str, ...],
             "ratings": {...}, "submission_losses": int}.
    """
    ratings = _ratings_from_rows(ranked_rows)
    failures: List[str] = []
    diff: List[str] = []

    # Invariant 1: strict Elo ordering.
    diff.append("expected order : " + " > ".join(EXPECTED_ELO_ORDER))
    diff.append("actual ratings : " + " > ".join(
        f"{name}={ratings[name]:.1f}" for name in EXPECTED_ELO_ORDER
        if name in ratings))
    for stronger, weaker in zip(EXPECTED_ELO_ORDER, EXPECTED_ELO_ORDER[1:]):
        rs, rw = ratings.get(stronger), ratings.get(weaker)
        if rs is None or rw is None:
            failures.append(
                f"elo order: missing rating for "
                f"{'stronger' if rs is None else 'weaker'} player "
                f"'{weaker if rs is None else stronger}'")
            diff.append(f"ORDER MISS    : {stronger} vs {weaker}: "
                        f"rating missing ({rs}, {rw})")
        elif not rs > rw:
            failures.append(
                f"elo order: expected {stronger} > {weaker}, "
                f"got {stronger}={rs:.1f}, {weaker}={rw:.1f}")
            diff.append(f"ORDER VIOLATION: {stronger}={rs:.1f} !> {weaker}={rw:.1f}")

    # Invariant 2: submission undefeated vs the frozen pool.
    losses = submission_losses(games)
    if losses:
        failures.append(
            f"undefeated: submission lost {len(losses)} game(s) "
            f"vs the frozen opponent pool")
        for g in losses:
            diff.append(
                f"LOSS          : {g.get('players')} seed={g.get('seed')} "
                f"winner={g.get('winner_label')} rewards={g.get('rewards')}")

    return {
        "ok": not failures,
        "failures": failures,
        "diff_table": diff,
        "ratings": ratings,
        "submission_losses": len(losses),
    }


def format_verdict(report: Dict[str, Any]) -> str:
    """One-line verdict for logs."""
    if report["ok"]:
        return (f"regression: PASS (elo order "
                f"{' > '.join(EXPECTED_ELO_ORDER)}; submission 0 losses)")
    return (f"regression: FAIL ({len(report['failures'])} violation(s): "
            + "; ".join(report["failures"]) + ")")
