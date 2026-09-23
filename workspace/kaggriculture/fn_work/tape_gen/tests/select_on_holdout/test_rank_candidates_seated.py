"""rank_candidates_seated 真实测试（R5：seated 适应度表）。

tmp 假评估器注入：验证表计算（win/draw/loss、winrate 平局 0.5、
margin_mean）、排序（score+稀疏破平）、per-game 明细与评估器契约。
"""

import pytest
from select_on_holdout.rank_candidates_seated import rank_candidates_seated


def _candidate(cid, piece, mask):
    switches = {name: bit == "1" for name, bit in zip(
        ("clone_preempt", "slot_reorder", "market_maker",
         "terminal_forced", "dead_price_guard"), mask)}
    return {"id": cid, "piece": piece, "switches": switches,
            "thresholds": {"clone_streak_required": 24,
                           "dead_guard_ratio": 0.5},
            "enabled_modules": sum(1 for v in switches.values() if v)}


def _games(n):
    return [{"episode_id": 5000 + i, "opp_seat": 0, "me_seat": 1,
             "opponent": f"opp{i}", "replay_path": f"/tmp/x-{i}.json"}
            for i in range(n)]


def _rows(spec):
    """spec = [(win, draw, margin), ...] → 行集。"""
    rows = [{"episode_id": 5000 + i, "opponent": f"opp{i}", "me_seat": 1,
             "win": w, "draw": d, "margin": m, "finals": [0.0, 0.0]}
            for i, (w, d, m) in enumerate(spec)]
    wins = sum(1 for r in rows if r["win"])
    draws = sum(1 for r in rows if r["draw"] and not r["win"])
    n = len(rows)
    return {"games": rows, "n": n, "wins": wins, "draws": draws,
            "losses": n - wins - draws,
            "winrate": (wins + 0.5 * draws) / n if n else 0.0,
            "margin_mean": sum(r["margin"] for r in rows) / n if n else 0.0}


def test_table_math_and_ordering():
    table_by_id = {
        "a#00000": _rows([(True, False, 120.0), (False, False, -80.0),
                          (False, True, 0.0)]),        # winrate=0.5+draw→.5
        "a#11000": _rows([(True, False, 10.0), (True, False, 5.0),
                          (False, False, -5.0)]),      # winrate=2/3
        "a#11111": _rows([(True, False, 1.0), (True, False, 1.0),
                          (True, False, 1.0)]),        # winrate=1.0
    }
    seen = []

    def evaluator(candidate, games):
        seen.append((candidate["id"], len(games)))
        row = dict(table_by_id[candidate["id"]])
        row["candidate_id"] = candidate["id"]
        return row

    result = rank_candidates_seated({
        "candidates": [_candidate("a#00000", "route:default", "00000"),
                       _candidate("a#11000", "route:default", "11000"),
                       _candidate("a#11111", "route:default", "11111")],
        "games": _games(3), "evaluator": evaluator, "lambda_sparse": 0.02})
    by_id = {row["candidate_id"]: row for row in result["table"]}
    # winrate：平局 0.5（0.5 = (1+0.5)/3）
    assert by_id["a#00000"]["winrate"] == pytest.approx(0.5)
    assert by_id["a#00000"]["margin_mean"] == pytest.approx(40.0 / 3)
    # score = winrate − λ×模块数：a#11111 = 1−0.10=0.90 居首
    assert by_id["a#11111"]["score"] == pytest.approx(1.0 - 0.02 * 5)
    assert by_id["a#11000"]["score"] == pytest.approx(2 / 3 - 0.04)
    assert result["ranking"][0] == "a#11111"
    # 评估器收到 (candidate, games) 全量
    assert sorted(seen) == [("a#00000", 3), ("a#11000", 3), ("a#11111", 3)]


def test_same_fitness_sparser_first():
    rows = _rows([(True, False, 5.0), (False, False, -5.0)])  # 0.5
    other = _rows([(True, False, 3.0), (False, False, -3.0)])  # 0.5

    def evaluator(candidate, games):
        row = dict(rows if candidate["id"] == "b#01000" else other)
        row["candidate_id"] = candidate["id"]
        return row

    result = rank_candidates_seated({
        "candidates": [_candidate("b#11000", "p", "11000"),
                       _candidate("b#01000", "p", "01000")],
        "games": _games(2), "evaluator": evaluator})
    assert result["ranking"] == ["b#01000", "b#11000"]  # 同分取稀疏


def test_batch_evaluator_protocol_supported():
    rows = _rows([(True, False, 7.0)])

    class BatchEval:
        def batch(self, candidates, games):
            out = {}
            for c in candidates:
                row = dict(rows)
                row["candidate_id"] = c["id"]
                out[c["id"]] = row
            return out

    result = rank_candidates_seated({
        "candidates": [_candidate("c#00000", "p", "00000")],
        "games": _games(1), "evaluator": BatchEval(),
        "lambda_sparse": 0.02})
    assert result["table"][0]["winrate"] == 1.0
    assert result["table"][0]["score"] == pytest.approx(1.0)


def test_fail_closed_empty():
    with pytest.raises(ValueError, match="fail-closed"):
        rank_candidates_seated({"candidates": [], "games": _games(2),
                                "evaluator": lambda c, g: {}})
    with pytest.raises(ValueError, match="fail-closed"):
        rank_candidates_seated({
            "candidates": [_candidate("d#00000", "p", "00000")],
            "games": [], "evaluator": lambda c, g: {}})
