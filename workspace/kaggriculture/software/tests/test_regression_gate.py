"""Regression gate (--assert-regression) unit tests -- pure logic, no episodes.

Covers kgenv.regression.check_regression: the two frozen invariants behind
`python scripts/run_eval.py --rounds 2 --assert-regression`.
"""

from kgenv.elo import EloTable
from kgenv.regression import (EXPECTED_ELO_ORDER, check_regression,
                              format_verdict, submission_losses)


def _game(a, b, winner, seed=0):
    return {"players": [a, b], "winner_label": winner, "seed": seed,
            "rewards": [1.0, 0.0], "turns_played": 24}


def _dominance_games():
    """Every stronger player beats every weaker player once (full round-robin)."""
    games = []
    seed = 0
    for i, stronger in enumerate(EXPECTED_ELO_ORDER):
        for weaker in EXPECTED_ELO_ORDER[i + 1:]:
            games.append(_game(stronger, weaker, stronger, seed))
            seed += 1
    return games


def _ranked_for(games):
    table = EloTable(k=32.0, start=1200.0)
    for g in games:
        score = 1.0 if g["winner_label"] == g["players"][0] else \
            (0.0 if g["winner_label"] == g["players"][1] else 0.5)
        table.record(g["players"][0], g["players"][1], score)
    return table.ranked()


def test_gate_passes_on_dominance_ladder():
    games = _dominance_games()
    report = check_regression(games, _ranked_for(games))
    assert report["ok"] is True
    assert report["failures"] == []
    assert report["submission_losses"] == 0
    assert "PASS" in format_verdict(report)


def test_gate_fails_when_submission_loses():
    games = _dominance_games() + [_game("pass", "submission", "pass", seed=99)]
    report = check_regression(games, _ranked_for(games))
    assert report["ok"] is False
    assert report["submission_losses"] == 1
    assert any("undefeated" in f for f in report["failures"])
    assert any(line.startswith("LOSS") for line in report["diff_table"])
    assert "FAIL" in format_verdict(report)


def test_gate_detects_loss_with_submission_on_p1_side():
    games = [{"players": ["starter", "submission"], "winner_label": "starter",
              "seed": 7, "rewards": [5.0, 3.0], "turns_played": 24}]
    assert len(submission_losses(games)) == 1


def test_gate_fails_on_elo_order_violation():
    # no losses, but the rating table inverts baseline_wheat and greedy_carrot
    rows = [
        {"name": "submission", "rating": 1400.0},
        {"name": "greedy_carrot", "rating": 1300.0},
        {"name": "baseline_wheat", "rating": 1250.0},
        {"name": "starter", "rating": 1200.0},
        {"name": "pass", "rating": 1150.0},
        {"name": "random", "rating": 1100.0},
    ]
    report = check_regression(_dominance_games(), rows)
    assert report["ok"] is False
    order_failures = [f for f in report["failures"] if f.startswith("elo order")]
    assert len(order_failures) == 1
    assert "baseline_wheat" in order_failures[0] and "greedy_carrot" in order_failures[0]


def test_gate_fails_on_missing_player_rating():
    rows = [{"name": n, "rating": 1200.0 + i * 10}
            for i, n in enumerate(EXPECTED_ELO_ORDER[:-1])]  # "pass" missing
    report = check_regression([], rows)
    assert report["ok"] is False
    assert any("missing rating" in f for f in report["failures"])
