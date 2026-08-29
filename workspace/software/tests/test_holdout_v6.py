"""Attempt-4 (v6) holdout contract pins.

Mirrors test_holdout_r4.py: the V4 registry excludes every previously
published seed (54 total), the 11-agent matrix (with wheat_straw_monster)
yields 55 official pairs / 880 games, and the metrics prefix is v6_.
"""

from kgenv.holdout_contract import (
    HISTORICAL_SEEDS_V3,
    HISTORICAL_SEEDS_V4,
    HOLDOUT_V4_MATRIX_ORDER,
    HOLDOUT_V4_OFFICIAL_PAIRS,
    PUBLISHED_ATTEMPT_IDS,
    PUBLISHED_HOLDOUT_SEEDS_V3,
    attempt_metrics_prefix,
    historical_seeds,
    holdout_expected_games,
    holdout_matrix_order,
    holdout_official_pairs,
)


def test_registry_v4_is_exactly_54_and_adds_only_attempt3_seeds():
    assert len(HISTORICAL_SEEDS_V4) == 54
    assert HISTORICAL_SEEDS_V4 - HISTORICAL_SEEDS_V3 == set(PUBLISHED_HOLDOUT_SEEDS_V3)
    assert len(historical_seeds(4)) == 54


def test_registry_v4_seeds_match_published_attempt3_generation():
    import json
    from pathlib import Path

    published = json.loads(
        (Path(__file__).resolve().parents[1] / "exports" / "holdout"
         / "published" / "seed_manifest.json").read_text(encoding="utf-8"))
    assert set(PUBLISHED_HOLDOUT_SEEDS_V3) == set(published["seeds"])
    assert published["attempt_index"] == 3
    assert PUBLISHED_ATTEMPT_IDS[3] == published["attempt_id"]


def test_v4_matrix_has_eleven_agents_and_55_pairs():
    assert len(HOLDOUT_V4_MATRIX_ORDER) == 11
    assert HOLDOUT_V4_MATRIX_ORDER[-1] == "wheat_straw_monster"
    assert len(HOLDOUT_V4_OFFICIAL_PAIRS) == 55
    assert holdout_matrix_order(4) == HOLDOUT_V4_MATRIX_ORDER
    assert holdout_official_pairs(4) == HOLDOUT_V4_OFFICIAL_PAIRS
    # 55 pairs x 8 seeds x AB/BA
    assert holdout_expected_games(4) == 880


def test_attempt4_metrics_prefix_is_v6():
    assert attempt_metrics_prefix(4) == "v6_"
