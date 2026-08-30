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

    holdout_root = Path(__file__).resolve().parents[1] / "exports" / "holdout"
    # The published directory now carries the attempt-4 (v6) generation:
    # 8 fresh OS-entropy seeds, disjoint from the 54-seed V4 registry,
    # under the attempt-4 id with the frozen v6 candidate (127c277e).
    PUBLISHED_HOLDOUT_SEEDS_V4 = frozenset({
        1908158035, 1035303213, 1934605933, 1094392752,
        802628522, 14410071, 618616204, 1252513065,
    })
    published = json.loads(
        (holdout_root / "published" / "seed_manifest.json")
        .read_text(encoding="utf-8"))
    assert published["attempt_index"] == 4
    assert published["attempt_id"] == "f31da15e9d3160fcd6d4fb8b"
    assert set(PUBLISHED_HOLDOUT_SEEDS_V4) == set(published["seeds"])
    assert not set(PUBLISHED_HOLDOUT_SEEDS_V4) & HISTORICAL_SEEDS_V4
    published_results = json.loads(
        (holdout_root / "published" / "eval_results.json")
        .read_text(encoding="utf-8"))
    assert published_results["identity"]["submission_sha256"].startswith("127c277e")
    # The attempt-3 generation it displaced stays byte-archived with the
    # V3 published seeds pinned by the contract constants.
    archived = json.loads(
        (holdout_root / "attempt-3" / "seed_manifest.json")
        .read_text(encoding="utf-8"))
    assert archived["attempt_index"] == 3
    assert set(PUBLISHED_HOLDOUT_SEEDS_V3) == set(archived["seeds"])
    assert PUBLISHED_ATTEMPT_IDS[3] == archived["attempt_id"]


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
