"""Order-independent Bradley-Terry/Davidson batch rating tests."""

from __future__ import annotations

import copy
import json
import random

import pytest

from kgenv.bradley_terry import RatingError, fit_ratings, tier_from_interval


def _game(a: str, b: str, seed: int, outcome: str, seat="AB") -> dict:
    winner = a if outcome == "A" else b if outcome == "B" else None
    rewards = ([2.0, 1.0] if outcome == "A" else
               [1.0, 2.0] if outcome == "B" else [1.0, 1.0])
    return {"game_id": f"{a}-{b}-{seed}-{seat}-{outcome}",
            "players": [a, b], "seed": seed, "seat": seat,
            "winner": winner, "winner_label": winner, "rewards": rewards,
            "statuses": ["DONE", "DONE"], "contract_ok": True}


def _balanced_synthetic() -> list[dict]:
    games = []
    patterns = {("A", "B"): "AAAAAAABBB", ("A", "C"): "AAAAAAAABB",
                ("B", "C"): "AAAAAAABBB"}
    seed = 1
    for (a, b), outcomes in patterns.items():
        for index, outcome in enumerate(outcomes):
            seat = "AB" if index % 2 == 0 else "BA"
            if seat == "AB":
                games.append(_game(a, b, seed, outcome, seat))
            else:
                flipped = "B" if outcome == "A" else "A"
                games.append(_game(b, a, seed, flipped, seat))
            seed += 1
    return games


def test_bt_recovers_known_synthetic_order_and_zero_sum_identity():
    report = fit_ratings(_balanced_synthetic(), bootstrap_samples=0)
    abilities = {row["agent"]: row["ability"] for row in report["agents"]}
    assert abilities["A"] > abilities["B"] > abilities["C"]
    assert sum(abilities.values()) == pytest.approx(0.0, abs=1e-9)
    assert report["model"] == "bradley-terry"
    assert report["converged"] is True
    assert report["iterations"] > 0
    assert report["log_likelihood"] < 0


def test_fit_is_invariant_to_input_shuffle_and_ab_ba_player_order():
    games = _balanced_synthetic()
    shuffled = copy.deepcopy(games)
    random.Random(77).shuffle(shuffled)
    first = fit_ratings(games, bootstrap_samples=40, bootstrap_seed=919)
    second = fit_ratings(shuffled, bootstrap_samples=40, bootstrap_seed=919)
    assert first == second
    assert first["seat_counts"] == {"AB": 15, "BA": 15}


def test_ties_select_davidson_and_estimate_positive_tie_parameter():
    games = _balanced_synthetic()
    games.extend([_game("A", "B", 100 + i, "T", "AB" if i % 2 == 0 else "BA")
                  for i in range(40)])
    report = fit_ratings(games, bootstrap_samples=0)
    assert report["model"] == "davidson"
    assert report["converged"] is True
    assert report["tie_parameter"] > 0
    assert report["tie_parameter_parameterization"] == "nu = exp(log_nu)"
    pair = next(row for row in report["pairwise_probabilities"]
                if row["a"] == "A" and row["b"] == "B")
    assert pair["p_tie"] > 0
    assert pair["p_a_win"] + pair["p_tie"] + pair["p_b_win"] == pytest.approx(1.0)


def test_disconnected_comparison_graph_is_rejected():
    games = [_game("A", "B", 1, "A"), _game("C", "D", 2, "A")]
    with pytest.raises(RatingError, match="disconnect|global ranking"):
        fit_ratings(games, bootstrap_samples=0)


def test_complete_separation_uses_disclosed_regularization():
    games = [_game("A", "B", seed, "A", "AB" if seed % 2 else "BA")
             for seed in range(1, 9)]
    report = fit_ratings(games, bootstrap_samples=0, regularization=0.2)
    assert report["separation_detected"] is True
    assert report["regularization"] == {"type": "zero-mean Gaussian MAP", "lambda": 0.2,
                                        "disclosed_for_separation": True}
    assert all(abs(row["ability"]) < 20 for row in report["agents"])


def test_clustered_bootstrap_is_deterministic_by_seed():
    games = _balanced_synthetic()
    first = fit_ratings(games, bootstrap_samples=60, bootstrap_seed=1234)
    second = fit_ratings(list(reversed(games)), bootstrap_samples=60, bootstrap_seed=1234)
    assert first["bootstrap"] == second["bootstrap"]
    assert [row["ci95"] for row in first["agents"]] == [row["ci95"] for row in second["agents"]]
    assert first["bootstrap"]["cluster_unit"] == "seed"


def test_tier_requires_ci_to_clear_preregistered_margin():
    assert tier_from_interval([0.31, 0.72], margin=0.3) == "higher"
    assert tier_from_interval([-0.72, -0.31], margin=0.3) == "lower"
    assert tier_from_interval([-0.1, 0.1], margin=0.3) == "same"
    assert tier_from_interval([0.1, 0.5], margin=0.3) == "uncertain"


def test_pair_counts_must_match_games_when_both_are_supplied():
    games = _balanced_synthetic()
    bad_counts = [{"a": "A", "b": "B", "wins_a": 99, "wins_b": 0, "ties": 0}]
    with pytest.raises(RatingError, match="aggregate|pair counts|games"):
        fit_ratings(games, pair_counts=bad_counts, bootstrap_samples=0)
    incomplete = [{"a": "A", "b": "B", "wins_a": 7, "wins_b": 3, "ties": 0}]
    with pytest.raises(RatingError, match="aggregate|pair counts|games"):
        fit_ratings(games, pair_counts=incomplete, bootstrap_samples=0)


def test_pair_counts_only_fit_is_supported():
    counts = [
        {"a": "A", "b": "B", "wins_a": 7, "wins_b": 3, "ties": 0},
        {"a": "A", "b": "C", "wins_a": 8, "wins_b": 2, "ties": 0},
        {"a": "B", "b": "C", "wins_a": 7, "wins_b": 3, "ties": 0},
    ]
    report = fit_ratings(pair_counts=counts, bootstrap_samples=0)
    assert [row["agent"] for row in report["agents"]] == ["A", "B", "C"]
    assert len(report["pairwise_probabilities"]) == 3


def test_connected_graph_reports_unobserved_pair_probability():
    games = [_game("A", "B", 1, "A"), _game("B", "C", 2, "A")]
    report = fit_ratings(games, bootstrap_samples=0, regularization=0.2)
    assert any(row["a"] == "A" and row["b"] == "C"
               for row in report["pairwise_probabilities"])


def test_bt_cli_accepts_pair_counts_only(tmp_path):
    source = tmp_path / "counts.json"
    output = tmp_path / "ratings.json"
    source.write_text(json.dumps({"pair_counts": [
        {"a": "A", "b": "B", "wins_a": 7, "wins_b": 3, "ties": 0},
        {"a": "A", "b": "C", "wins_a": 8, "wins_b": 2, "ties": 0},
        {"a": "B", "b": "C", "wins_a": 7, "wins_b": 3, "ties": 0},
    ]}), encoding="utf-8")
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0"]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["game_count"] == 0
    assert report["bootstrap"]["cluster_unit"] == "seed"
    assert report["bootstrap"]["samples_used"] == 0


def test_bt_cli_rejects_nonconverged_without_publishing(tmp_path):
    source = tmp_path / "games.json"
    output = tmp_path / "ratings.json"
    output.write_text("old", encoding="utf-8")
    source.write_text(json.dumps({"games": _balanced_synthetic()}), encoding="utf-8")
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0", "--max-iterations", "1"]) != 0
    assert output.read_text(encoding="utf-8") == "old"


def test_small_sample_has_no_inferential_ci_or_tier():
    games = [_game("A", "B", 1, "A"), _game("B", "A", 1, "B")]
    report = fit_ratings(games, bootstrap_samples=20)
    assert report["inference_status"] == "insufficient_data"
    assert all(row["ci95"] == [None, None] for row in report["agents"])
    assert all(row["tier"] == "insufficient_data" for row in report["agents"])
    assert all(row["tier"] == "insufficient_data" for row in report["pairwise_probabilities"])
    assert all(row["probability_status"] == "regularized_descriptive"
               for row in report["pairwise_probabilities"])


def test_pair_counts_reject_bool_float_string_negative_and_reverse_duplicate():
    invalid = [
        [{"a": "A", "b": "B", "wins_a": True, "wins_b": 1, "ties": 0}],
        [{"a": "A", "b": "B", "wins_a": 1.5, "wins_b": 1, "ties": 0}],
        [{"a": "A", "b": "B", "wins_a": "1", "wins_b": 1, "ties": 0}],
        [{"a": "A", "b": "B", "wins_a": -1, "wins_b": 1, "ties": 0}],
        [{"a": "A", "b": "B", "wins_a": 1, "wins_b": 0, "ties": 0},
         {"a": "B", "b": "A", "wins_a": 0, "wins_b": 1, "ties": 0}],
    ]
    for counts in invalid:
        with pytest.raises(RatingError, match="pair counts|integer|negative|duplicate"):
            fit_ratings(pair_counts=counts, bootstrap_samples=0)


def test_each_pair_and_seed_requires_both_seats():
    games = [_game("A", "B", 1, "A", "AB"), _game("A", "B", 2, "A", "AB"),
             _game("B", "A", 1, "B", "BA")]
    with pytest.raises(RatingError, match="seed|AB|BA|pair"):
        fit_ratings(games, bootstrap_samples=0, require_ab_ba=True)


def test_strict_pairing_uses_first_game_order_not_lexical_order():
    games = [_game("working", "v48", 101, "B", "AB"),
             _game("v48", "working", 101, "A", "BA")]
    report = fit_ratings(games, bootstrap_samples=0, require_ab_ba=True)
    assert report["seat_counts"] == {"AB": 1, "BA": 1}


    games = _balanced_synthetic()
    for value in (0, -1, True, float("nan"), float("inf")):
        with pytest.raises(RatingError, match="min_seed_clusters|integer|finite|positive"):
            fit_ratings(games, bootstrap_samples=0, min_seed_clusters=value)


def test_strict_pairing_is_invariant_to_row_order():
    games = [_game("working", "v48", 101, "B", "AB"),
             _game("v48", "working", 101, "A", "BA")]
    first = fit_ratings(games, bootstrap_samples=0, require_ab_ba=True)
    second = fit_ratings(list(reversed(games)), bootstrap_samples=0, require_ab_ba=True)
    assert first == second


def test_rating_games_require_finite_rewards_and_consistent_winner():
    base = _game("A", "B", 1, "A")
    invalid = [
        {key: value for key, value in base.items() if key != "rewards"},
        {**base, "rewards": [float("nan"), 1.0]},
        {**base, "winner": "B", "winner_label": "B"},
        {**base, "winner": "A", "winner_label": "B"},
    ]
    for game in invalid:
        with pytest.raises(RatingError, match="reward|winner"):
            fit_ratings([game], bootstrap_samples=0)


def test_strict_bootstrap_resamples_complete_seed_clusters():
    games = []
    for seed in range(1, 9):
        outcome = "A" if seed <= 5 else "B"
        games.extend([_game("working", "v48", seed, outcome, "AB"),
                      _game("v48", "working", seed, "B" if outcome == "A" else "A", "BA")])
    report = fit_ratings(games, bootstrap_samples=40, bootstrap_seed=77,
                         require_ab_ba=True, regularization=0.2)
    assert report["bootstrap"]["samples_used"] == 40
    assert report["bootstrap"]["failed_disconnected"] == 0
    assert report["inference_status"] == "inferential"
    assert all(None not in row["ci95"] for row in report["agents"])


def test_strict_pair_seed_rejects_duplicate_or_misordered_seats():
    duplicate = [_game("A", "B", 1, "A", "AB"), _game("A", "B", 1, "A", "AB")]
    with pytest.raises(RatingError, match="exactly|duplicate|AB|BA|players"):
        fit_ratings(duplicate, bootstrap_samples=0, require_ab_ba=True)
    misordered = [_game("A", "B", 1, "A", "AB"), _game("A", "B", 1, "A", "BA")]
    with pytest.raises(RatingError, match="players|order|AB|BA"):
        fit_ratings(misordered, bootstrap_samples=0, require_ab_ba=True)
    extra = [_game("A", "B", 1, "A", "AB"), _game("B", "A", 1, "B", "BA"),
             _game("A", "B", 1, "A", "AB")]
    with pytest.raises(RatingError, match="exactly|duplicate|AB|BA"):
        fit_ratings(extra, bootstrap_samples=0, require_ab_ba=True)


def test_rating_parameters_reject_invalid_values():
    games = _balanced_synthetic()
    invalid = [
        {"bootstrap_samples": True}, {"bootstrap_samples": 1.5}, {"bootstrap_samples": -1},
        {"max_iterations": True}, {"max_iterations": 1.5}, {"max_iterations": 0},
        {"regularization": float("nan")}, {"regularization": float("inf")}, {"regularization": -1.0},
        {"tier_margin": float("nan")}, {"tier_margin": float("inf")}, {"tier_margin": -1.0},
        {"bootstrap_seed": True}, {"bootstrap_seed": 1.5},
    ]
    for kwargs in invalid:
        params = {"bootstrap_samples": 0}
        params.update(kwargs)
        with pytest.raises(RatingError, match="finite|integer|non-negative|positive"):
            fit_ratings(games, **params)
    with pytest.raises(RatingError, match="seed|integer"):
        fit_ratings([_game("A", "B", 1, "A"),
                     {**_game("A", "B", 2, "A"), "seed": True}], bootstrap_samples=0)


def test_bt_cli_allow_nonconverged_is_explicitly_unpublishable(tmp_path):
    source = tmp_path / "games.json"
    output = tmp_path / "ratings.json"
    source.write_text(json.dumps({"games": _balanced_synthetic()}), encoding="utf-8")
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0", "--max-iterations", "1",
                                  "--allow-nonconverged"]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["publishable"] is False
    assert report["publication_status"] == "diagnostic_only_nonconverged"


def test_bt_cli_writes_descriptive_report(tmp_path):
    source = tmp_path / "games.json"
    output = tmp_path / "ratings.json"
    source.write_text(json.dumps({"games": _balanced_synthetic()}), encoding="utf-8")
    from scripts import fit_bradley_terry
    assert fit_bradley_terry.main(["--input", str(source), "--output", str(output),
                                  "--bootstrap", "0"]) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["descriptive_only"] is True
    assert report["holdout_generalization_claim"] is False
    assert report["model"] == "bradley-terry"
