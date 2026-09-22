"""Unit tests for the seed-variance statistics (kgenv.variance) and the
frozen-pool semantics of the regression gate (kgenv.regression, m1 wave 2).
"""

import math

from kgenv.regression import (EXPECTED_ELO_ORDER, FROZEN_POOL,
                              check_regression, frozen_games,
                              submission_losses)
from kgenv.variance import (margin_stats, most_volatile_pair, pair_variance,
                            t95, wilson_ci)


def _game(a, b, winner, seed, ra=1.0, rb=0.0):
    return {"players": [a, b], "winner_label": winner, "seed": seed,
            "rewards": [ra, rb], "turns_played": 720}


# ------------------------------------------------------------------ wilson

def test_wilson_known_values():
    # 4/4 wins: one-sided-ish interval, lower bound well above 0.5
    lo, hi = wilson_ci(4.0, 4)
    assert 0.51 < lo < 0.9 and 0.83 < hi <= 1.0
    # 0/4: upper bound still below 0.5
    lo, hi = wilson_ci(0.0, 4)
    assert lo == 0.0 and 0.1 < hi < 0.49
    # 2/4 (ties as half wins): centred on 0.5, symmetric
    lo, hi = wilson_ci(2.0, 4)
    assert abs((lo + hi) / 2 - 0.5) < 1e-9
    # degenerate
    assert wilson_ci(0, 0) == (None, None)


def test_wilson_shrinks_with_n():
    lo4, hi4 = wilson_ci(10, 10)
    lo40, hi40 = wilson_ci(100, 100)
    assert lo40 > lo4  # more evidence -> tighter lower bound


def test_t95_table():
    assert math.isclose(t95(2), 12.706, rel_tol=1e-3)
    assert math.isclose(t95(4), 3.182, rel_tol=1e-3)
    assert t95(100) == 1.96  # normal approximation
    assert math.isnan(t95(1))


# ------------------------------------------------------------ margin stats

def test_margin_stats_basic():
    ms = margin_stats([100.0, 200.0, 300.0, 400.0])
    assert ms["n"] == 4 and ms["mean"] == 250.0
    assert ms["min"] == 100.0 and ms["max"] == 400.0
    # t(4)=3.182 * std(129.1)/2 = ~205 -> CI contains the mean
    assert ms["ci95_lo"] < 250.0 < ms["ci95_hi"]
    assert margin_stats([])["mean"] is None


# ------------------------------------------------------------ pair variance

def test_pair_variance_counts_and_flips():
    games = [
        _game("a", "b", "a", 101, 10.0, 0.0),
        _game("a", "b", "b", 102, 0.0, 5.0),
        _game("a", "b", None, 103, 3.0, 3.0),
    ]
    r = pair_variance(games, "a", "b")
    assert r["games"] == 3 and (r["wins"], r["losses"], r["ties"]) == (1, 1, 1)
    assert r["win_rate"] == 0.5
    assert r["outcome_flips_across_seeds"] is True
    assert r["seeds"] == [101, 102, 103]
    # other pairings are ignored
    assert pair_variance(games, "a", "c")["games"] == 0


def test_most_volatile_prefers_flips_then_ci_width():
    stable = pair_variance([_game("a", "b", "a", s) for s in (1, 2, 3, 4)],
                           "a", "b")
    flipping = pair_variance([
        _game("c", "d", "c", 1), _game("c", "d", "d", 2),
        _game("c", "d", "c", 3), _game("c", "d", "d", 4)], "c", "d")
    assert most_volatile_pair([stable, flipping])["pair"] == "c vs d"
    assert most_volatile_pair([]) is None


# ------------------------------------------------------- frozen-pool gate

def test_frozen_games_filters_strong_opponents():
    games = [
        _game("submission", "greedy_carrot", "submission", 1),
        _game("submission", "cow_baron", "cow_baron", 2),       # non-frozen
        _game("melon_hoarder", "starter", "melon_hoarder", 3),  # non-frozen
    ]
    assert len(frozen_games(games)) == 1


def test_submission_loss_to_strong_opponent_does_not_break_gate():
    # dominance ladder among the frozen six + a submission LOSS to cow_baron
    games = []
    seed = 0
    for i, stronger in enumerate(EXPECTED_ELO_ORDER):
        for weaker in EXPECTED_ELO_ORDER[i + 1:]:
            games.append(_game(stronger, weaker, stronger, seed))
            seed += 1
    games.append(_game("submission", "cow_baron", "cow_baron", 99, 100.0,
                       500.0))

    from kgenv.elo import EloTable
    frozen = frozen_games(games)
    table = EloTable(k=32.0, start=1200.0)
    for g in frozen:
        score = 1.0 if g["winner_label"] == g["players"][0] else \
            (0.0 if g["winner_label"] == g["players"][1] else 0.5)
        table.record(g["players"][0], g["players"][1], score)
    report = check_regression(frozen, table.ranked())
    assert report["ok"] is True
    assert report["submission_losses"] == 0
    # the loss is still visible when the caller widens the pool explicitly
    wide = FROZEN_POOL | {"cow_baron"}
    assert len(submission_losses(games, pool=wide)) == 1


def test_submission_loss_to_frozen_pool_breaks_gate():
    games = [_game("pass", "submission", "pass", 99, 4000.0, 3000.0)]
    assert len(submission_losses(games)) == 1
    assert FROZEN_POOL == set(EXPECTED_ELO_ORDER)


def test_pass_beats_random_on_merit_in_elo():
    """m1 amendment evidence: with head-to-head games played (the full
    matrix does this), pass out-rates random on merit -- the old m0 order
    (random > pass) was a sub-matrix iteration artifact."""
    from kgenv.elo import EloTable
    t = EloTable(k=32.0, start=1200.0)
    for _ in range(4):
        t.record("pass", "random", 1.0)   # pass keeps its $3000, random ~$0
    for _ in range(4):
        t.record("starter", "pass", 1.0)
        t.record("starter", "random", 1.0)
    ratings = {r["name"]: r["rating"] for r in t.ranked()}
    assert ratings["pass"] > ratings["random"]
