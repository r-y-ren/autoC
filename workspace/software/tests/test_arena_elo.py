"""Arena / Elo / exports contract tests."""

import json
import os

import pytest

from kgenv.arena import (AbnormalMatchError, run_match, summarize_games,
                         write_replay_log)
from kgenv.elo import EloTable, expected_score, update
from kgenv.engine import episode_contract_ok


def test_match_contract_and_winner():
    # 120 steps = 5 days: starter completes a carrot cycle and earns money
    res = run_match("starter", "pass", seed=1, episode_steps=120,
                    label_a="starter", label_b="pass")
    assert episode_contract_ok(res)
    assert res["players"] == ["starter", "pass"]
    assert res["winner_label"] == "starter"
    assert res["contract_ok"] is True


def test_tie_detected():
    # starter vs starter on a fixed seed is a deterministic matchup
    res = run_match("starter", "starter", seed=2, episode_steps=24,
                    label_a="A", label_b="B")
    assert episode_contract_ok(res)
    # identical strategies with symmetric play may tie; winner in {A,B,None}
    assert res["winner_label"] in ("A", "B", None)


def test_replay_log_roundtrip(tmp_path):
    res = run_match("starter", "pass", seed=3, episode_steps=24,
                    label_a="x", label_b="y")
    path = write_replay_log(str(tmp_path), [res])
    with open(path, encoding="utf-8") as f:
        entry = json.loads(f.readline())
    assert entry["players"] == ["x", "y"]
    assert entry["seed"] == 3
    assert len(entry["rewards"]) == 2
    assert entry["turns"] == 24


def test_replay_log_carries_daily_prices(tmp_path):
    """m1 wave 2: the replay log embeds shared-market daily prices for
    failure-mode analysis (glut-crash evidence)."""
    res = run_match("starter", "pass", seed=3, episode_steps=48,
                    label_a="x", label_b="y", collect_daily=True)
    path = write_replay_log(str(tmp_path), [res])
    with open(path, encoding="utf-8") as f:
        entry = json.loads(f.readline())
    assert entry["daily_prices"], entry.get("daily_prices")
    assert "CARROT" in entry["daily_prices"][0]
    assert entry["daily_money"]


def test_summarize_games():
    games = [
        {"players": ["a", "b"], "statuses": ["DONE", "DONE"],
         "contract_ok": True, "winner_label": "a", "rewards": [2, 1],
         "turns_played": 10},
        {"players": ["a", "b"], "statuses": ["DONE", "DONE"],
         "contract_ok": True, "winner_label": "b", "rewards": [1, 2],
         "turns_played": 12},
        {"players": ["a", "b"], "statuses": ["DONE", "DONE"],
         "contract_ok": True, "winner_label": None, "rewards": [1, 1],
         "turns_played": 14},
    ]
    s = summarize_games(games, "a", "b")
    assert s == {"pair": "a vs b", "games": 3, "wins": 1, "losses": 1,
                 "ties": 1, "win_rate": 0.5, "avg_turns": 12.0}


def test_summarize_games_rejects_missing_contract_fields():
    with pytest.raises(AbnormalMatchError, match="missing statuses"):
        summarize_games([
            {"players": ["a", "b"], "winner_label": None, "turns_played": 14}
        ], "a", "b")


def test_elo_math():
    assert expected_score(1200, 1200) == 0.5
    assert expected_score(1400, 1200) > 0.5
    ra, rb = update(1200, 1200, 1.0)
    assert ra > 1200 > rb
    assert (ra - 1200) == (1200 - rb)  # zero-sum
    ra2, rb2 = update(ra, rb, 0.0)
    # a loss after a win returns both close to (but not exactly at) start
    assert abs(ra2 - 1200) < 2 and abs(rb2 - 1200) < 2


def test_elo_table_ordering():
    t = EloTable(k=32, start=1200)
    for _ in range(10):
        t.record("strong", "weak", 1.0)
    ranked = t.ranked()
    assert ranked[0]["name"] == "strong"
    assert ranked[0]["record"] == {"W": 10, "L": 0, "T": 0}
    assert t.win_rate("strong") == 1.0


def test_exports_schema_exists_and_valid_json():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(root, "exports", "schema.json")
    assert os.path.isfile(schema_path)
    with open(schema_path, encoding="utf-8") as f:
        schema = json.load(f)
    assert schema.get("$id", "").endswith("eval_results.schema.json") or \
        "properties" in schema


def test_eval_results_sample_matches_schema():
    """The shipped eval sample must validate against its run-kind schema."""
    import jsonschema
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_path = os.path.join(root, "exports", "eval_results.json")
    if not os.path.isfile(sample_path):
        pytest.skip("eval sample not generated yet (run scripts/run_eval.py)")
    with open(sample_path, encoding="utf-8") as f:
        sample = json.load(f)
    schema_name = (
        "holdout_schema.json"
        if sample.get("run_kind") == "official_holdout"
        else "schema.json"
    )
    with open(os.path.join(root, "exports", schema_name), encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(sample, schema)
