"""Frozen regression line for the Kaggriculture eval matrix.

Pure functions over an already-played game stream + Elo table -- no engine
calls -- so the gate is unit-testable without running episodes.

Two invariants (frozen at m0-skeleton, campaign K-03 wave 1):

1. Elo ordering is strictly descending:
   submission > baseline_wheat > greedy_carrot > starter > pass > random
2. The submission bot is undefeated against the frozen opponent pool
   (0 losses in every game it plays, including head-to-head vs baseline).

m1 wave-2 amendment (documented, data-driven): the m0 line read
"... > starter > random > pass", but random and pass never actually played
each other in the m0 sub-matrix (opponents only faced contenders), so their
relative order was an artifact of opponents-dict iteration order in the
Elo stream.  The m1 full matrix plays every pair, including random vs
pass, and pass beats random 100% (the random agent earns ~$0 vs pass's
$3000 start) -- e.g. gate run 2026-08-28: pass 1128.9 > random 1061.0 with
pass W2 L14 vs random W0 L16.  The clause is therefore corrected to
pass > random; every meaningful invariant (submission dominance,
baseline > greedy > starter ordering, submission undefeated vs the frozen
pool) is unchanged.

m1 wave 2 note: the matrix now also contains strong opponents (cow_baron,
melon_hoarder, expansionist).  They are deliberately OUTSIDE the frozen
line -- both invariants are evaluated on the frozen-subset game stream
(games between frozen-pool players only, with the Elo table recomputed on
that subset), so the m0 freeze keeps its exact meaning while the pool
grows around it.  Submission losses to non-frozen opponents are the
business of the failure-mode analysis (exports/failure_modes.md), not of
this gate.

scripts/run_eval.py --assert-regression evaluates these after a run and
exits non-zero with a diff table on violation.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional, Set

SUBMISSION = "submission"

# Frozen ladder order (strict >, ties or inversions fail the gate).
# m1 wave-2 amendment: pass/random swapped (see module docstring) -- the m0
# order was an iteration artifact; head-to-head data says pass > random.
EXPECTED_ELO_ORDER: List[str] = [
    "submission",
    "baseline_wheat",
    "greedy_carrot",
    "starter",
    "pass",
    "random",
]

FROZEN_POOL: Set[str] = set(EXPECTED_ELO_ORDER)


def frozen_games(games: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Games between frozen-pool players only (the m0 game stream)."""
    return [g for g in games
            if set(g.get("players") or []) <= FROZEN_POOL]


def _ratings_from_rows(ranked_rows: Iterable[Dict[str, Any]]) -> Dict[str, float]:
    """Accept EloTable.ranked() rows or plain {"name","rating"} dicts."""
    ratings: Dict[str, float] = {}
    for row in ranked_rows:
        ratings[row["name"]] = float(row["rating"])
    return ratings


def submission_losses(games: List[Dict[str, Any]],
                      pool: Optional[Set[str]] = None) -> List[Dict[str, Any]]:
    """Games the submission bot lost (it may sit on either side).

    Only opponents inside `pool` count (default: the frozen pool).  Losses
    to m1 wave-2 strong opponents do not violate the frozen line.
    """
    pool = FROZEN_POOL if pool is None else pool
    lost = []
    for g in games:
        players = list(g.get("players") or [])
        winner = g.get("winner_label")
        if SUBMISSION in players and winner is not None and winner != SUBMISSION:
            opponent = players[1] if players[0] == SUBMISSION else players[0]
            if opponent in pool:
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
