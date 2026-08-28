"""Elo rating math for local agent evaluation.

Follows the same spirit as the official ladder: only win/loss/tie matters
(never the coin margin); K scales the update; expected score uses the
logistic curve.  This mirrors the Evaluation page's description of skill
ratings and Bradley-Terry-style convergence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

DEFAULT_RATING = 1200.0
DEFAULT_K = 32.0


def expected_score(ra: float, rb: float) -> float:
    """Expected score of player A (1 = win, 0.5 = tie) against player B."""
    return 1.0 / (1.0 + 10.0 ** ((rb - ra) / 400.0))


def update(ra: float, rb: float, score_a: float, k: float = DEFAULT_K) -> Tuple[float, float]:
    """One-match rating update; score_a in {0.0, 0.5, 1.0}. Returns (ra', rb')."""
    ea = expected_score(ra, rb)
    ra2 = ra + k * (score_a - ea)
    rb2 = rb + k * ((1.0 - score_a) - (1.0 - ea))
    return ra2, rb2


@dataclass
class EloTable:
    """Maintains ratings over a recorded game stream (order-sensitive)."""

    k: float = DEFAULT_K
    start: float = DEFAULT_RATING
    ratings: Dict[str, float] = field(default_factory=dict)
    wins: Dict[str, Dict[str, int]] = field(default_factory=dict)  # name -> {W,L,T}
    played: Dict[str, int] = field(default_factory=dict)

    def _ensure(self, name: str) -> None:
        self.ratings.setdefault(name, self.start)
        self.wins.setdefault(name, {"W": 0, "L": 0, "T": 0})
        self.played.setdefault(name, 0)

    def record(self, a: str, b: str, score_a: float) -> None:
        """score_a: 1.0 A won, 0.0 B won, 0.5 tie."""
        assert score_a in (0.0, 0.5, 1.0)
        self._ensure(a)
        self._ensure(b)
        ra, rb = self.ratings[a], self.ratings[b]
        ra2, rb2 = update(ra, rb, score_a, self.k)
        self.ratings[a], self.ratings[b] = ra2, rb2
        self.played[a] += 1
        self.played[b] += 1
        if score_a == 1.0:
            self.wins[a]["W"] += 1
            self.wins[b]["L"] += 1
        elif score_a == 0.0:
            self.wins[b]["W"] += 1
            self.wins[a]["L"] += 1
        else:
            self.wins[a]["T"] += 1
            self.wins[b]["T"] += 1

    def ranked(self) -> List[Dict[str, object]]:
        rows = [
            {
                "name": name,
                "rating": round(r, 1),
                "played": self.played.get(name, 0),
                "record": dict(self.wins.get(name, {"W": 0, "L": 0, "T": 0})),
            }
            for name, r in self.ratings.items()
        ]
        rows.sort(key=lambda row: (-row["rating"], row["name"]))
        return rows

    def win_rate(self, name: str) -> Optional[float]:
        n = self.played.get(name, 0)
        if n == 0:
            return None
        w = self.wins[name]
        return (w["W"] + 0.5 * w["T"]) / n
