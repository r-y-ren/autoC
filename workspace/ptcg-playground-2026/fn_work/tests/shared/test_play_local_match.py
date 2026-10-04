import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from kaggle_environments.envs.cabt import cabt

from src.shared.play_local_match import play_local_match

DECK = list(cabt.deck)


def test_match_runs_and_records_steps():
    r = play_local_match(cabt.first_agent, cabt.random_agent, DECK, DECK, seed=42)
    assert r["n_steps"] > 1
    assert r["rewards"][0] in (1, -1, 0)
    assert r["steps"][0]["active"] == "both"
    assert any(s["active"] in (0, 1) for s in r["steps"][1:])
    assert not r["failed"]


def test_seat_swap_changes_perspective():
    r1 = play_local_match(cabt.first_agent, cabt.random_agent, DECK, DECK, seed=42)
    r2 = play_local_match(cabt.random_agent, cabt.first_agent, DECK, DECK, seed=42)
    # 双席同种子：first 无论坐哪席，其 reward 应一致（席位对换对称性）
    assert r1["rewards"][0] == r2["rewards"][1]


def test_bo1_config():
    r = play_local_match(cabt.first_agent, cabt.random_agent, DECK, DECK, seed=7, config={"bo": 1})
    assert r["n_steps"] > 1
