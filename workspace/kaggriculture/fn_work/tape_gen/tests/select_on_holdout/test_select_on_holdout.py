"""select_on_holdout 真实测试（R5：只在留出集裁决）。

tmp 假评估器注入：训练强/留出弱的候选不得因训练成绩胜出（选择只看
留出）；同分稀疏优先；留出占比 fail-closed；产物三件落盘。
"""

import csv
import json

import pytest
from select_on_holdout.select_on_holdout import select_on_holdout


def _candidate(cid, piece, mask):
    switches = {name: bit == "1" for name, bit in zip(
        ("clone_preempt", "slot_reorder", "market_maker",
         "terminal_forced", "dead_price_guard"), mask)}
    return {"id": cid, "piece": piece, "switches": switches,
            "thresholds": {"clone_streak_required": 24,
                           "dead_guard_ratio": 0.5},
            "enabled_modules": sum(1 for v in switches.values() if v)}


def _games(n, prefix=7000):
    return [{"episode_id": prefix + i, "opp_seat": 0, "me_seat": 1,
             "opponent": f"holdopp{i}", "replay_path": f"/tmp/h-{i}.json"}
            for i in range(n)]


def _holdout_ranker(winrates):
    """假 ranker：按 id 查留出胜率，per-game 明细全胜/全负构造。"""
    def ranker(payload):
        table = []
        for c in payload["candidates"]:
            wr = winrates[c["id"]]
            wins = round(wr * len(payload["games"]))
            rows = [{"episode_id": g["episode_id"],
                     "opponent": g["opponent"], "me_seat": 1,
                     "win": i < wins, "draw": False,
                     "margin": 50.0 if i < wins else -50.0,
                     "finals": [100.0, 150.0] if i < wins
                     else [150.0, 100.0]}
                    for i, g in enumerate(payload["games"])]
            n = len(rows)
            table.append({
                "candidate_id": c["id"], "games": rows, "n": n,
                "wins": wins, "draws": 0, "losses": n - wins,
                "winrate": wins / n,
                "margin_mean": (wins - (n - wins)) * 50.0 / n,
                "score": wins / n - 0.02 * c["enabled_modules"],
                "enabled_modules": c["enabled_modules"],
                "piece": c["piece"], "switches": c["switches"],
                "thresholds": c["thresholds"]})
        table.sort(key=lambda r: (-r["score"], r["enabled_modules"],
                                  r["candidate_id"]))
        return {"table": table, "ranking": [r["candidate_id"]
                                            for r in table],
                "lambda_sparse": 0.02}
    return ranker


def test_selection_uses_holdout_only(tmp_path):
    # A 训练侧强（train_score 高）但留出 0.2；B 留出 0.6 —— B 必胜
    final_ids = {"a#11111", "b#00000"}
    result = select_on_holdout({
        "finalists": [_candidate("a#11111", "route:default", "11111"),
                      _candidate("b#00000", "variant:v1", "00000")],
        "holdout_games": _games(10),
        "n_games_total": 20,
        "ranker": _holdout_ranker({"a#11111": 0.2, "b#00000": 0.6}),
        "lambda_sparse": 0.02,
        "train_rows": {"a#11111": {"score": 0.9, "winrate": 0.9},
                       "b#00000": {"score": 0.3, "winrate": 0.3}},
        "output_dir": str(tmp_path)})
    assert result["final"]["candidate_id"] == "b#00000"
    assert result["proof"]["decided_on"] == "holdout_only"
    # 报告含训练侧成绩但不影响裁决（A 训练 0.9 仍输）
    report = {r["candidate_id"]: r for r in result["finalists_report"]}
    assert report["a#11111"]["train_winrate"] == 0.9
    assert report["a#11111"]["holdout_winrate"] == 0.2


def test_selection_tie_prefers_sparser(tmp_path):
    result = select_on_holdout({
        "finalists": [_candidate("s#01100", "route:default", "01100"),
                      _candidate("s#00000", "route:default", "00000")],
        "holdout_games": _games(8),
        "n_games_total": 16,
        "ranker": _holdout_ranker({"s#01100": 0.5, "s#00000": 0.5}),
        "lambda_sparse": 0.02, "output_dir": str(tmp_path)})
    assert result["final"]["candidate_id"] == "s#00000"


def test_holdout_margin_table_written(tmp_path):
    result = select_on_holdout({
        "finalists": [_candidate("m#10000", "variant:v2", "10000")],
        "holdout_games": _games(5),
        "n_games_total": 10,
        "ranker": _holdout_ranker({"m#10000": 0.6}),
        "lambda_sparse": 0.02, "output_dir": str(tmp_path)})
    final = json.loads((tmp_path / "final_selection.json").read_text(
        encoding="utf-8"))
    assert final["candidate_id"] == "m#10000"
    assert final["holdout"]["n_games"] == 5
    assert len(final["holdout"]["margin_table"]) == 5
    assert {row["result"] for row in final["holdout"]["margin_table"]} \
        <= {"W", "L", "D"}
    csv_text = (tmp_path / "holdout_margin_table.csv").read_text(
        encoding="utf-8")
    rows = list(csv.reader(csv_text.strip().splitlines()))
    assert rows[0][0] == "candidate_id" and len(rows) == 6
    assert json.loads((tmp_path / "holdout_table.json").read_text(
        encoding="utf-8"))[0]["candidate_id"] == "m#10000"


def test_fail_closed_holdout_fraction():
    with pytest.raises(ValueError, match="留出局不足"):
        select_on_holdout({
            "finalists": [_candidate("x#00000", "p", "00000")],
            "holdout_games": _games(2), "n_games_total": 100,
            "ranker": _holdout_ranker({"x#00000": 0.5})})
    with pytest.raises(ValueError, match="fail-closed"):
        select_on_holdout({"finalists": [], "holdout_games": _games(5),
                           "n_games_total": 10})
    with pytest.raises(ValueError, match="fail-closed"):
        select_on_holdout({
            "finalists": [_candidate("y#00000", "p", "00000")],
            "holdout_games": []})
