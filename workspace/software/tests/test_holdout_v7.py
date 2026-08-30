"""Attempt-5 (v7.2) holdout contract pins.

Mirrors test_holdout_v6.py: the V5 registry excludes every previously
published seed (62 total), the 12-agent matrix (with two_quad_denser)
yields 66 official pairs / 1056 games, and the metrics prefix is v72_.
"""

from kgenv.holdout_contract import (
    HISTORICAL_SEEDS_V4,
    HISTORICAL_SEEDS_V5,
    HOLDOUT_V5_MATRIX_ORDER,
    HOLDOUT_V5_OFFICIAL_PAIRS,
    PUBLISHED_HOLDOUT_SEEDS_V4,
    attempt_metrics_prefix,
    candidate_expected_games,
    historical_seeds,
    holdout_expected_games,
    holdout_matrix_order,
    holdout_official_pairs,
)

# the eight seeds published by the attempt-4 generation (seed_manifest at
# exports/holdout/published, attempt_index 4, id f31da15e...)


def test_registry_v5_is_exactly_62_and_adds_only_attempt4_seeds():
    assert len(HISTORICAL_SEEDS_V5) == 62
    assert HISTORICAL_SEEDS_V5 - HISTORICAL_SEEDS_V4 == \
        set(PUBLISHED_HOLDOUT_SEEDS_V4)
    assert len(historical_seeds(5)) == 62


def test_v5_matrix_has_twelve_agents_and_66_pairs():
    assert len(HOLDOUT_V5_MATRIX_ORDER) == 12
    assert HOLDOUT_V5_MATRIX_ORDER[-1] == "two_quad_denser"
    assert len(HOLDOUT_V5_OFFICIAL_PAIRS) == 66
    assert holdout_matrix_order(5) == HOLDOUT_V5_MATRIX_ORDER
    assert holdout_official_pairs(5) == HOLDOUT_V5_OFFICIAL_PAIRS
    # 66 pairs x 8 seeds x AB/BA
    assert holdout_expected_games(5) == 1056
    # candidate games: 11 opponents x 8 seeds x AB/BA
    assert candidate_expected_games(5) == 176


def test_attempt5_metrics_prefix_is_v72():
    assert attempt_metrics_prefix(5) == "v72_"
