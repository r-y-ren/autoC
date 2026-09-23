"""select_on_holdout（L0，R5）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

holdout 选择器顶层编排：候选集 + 分离 → **只在留出集裁决**的最终件 +
留出逐局边际表。

* 裁决面：finalists（训练侧评估的幸存者）仅在留出局上重演（
  rank_candidates_seated；评估器可注入）；排序键 (-score,
  enabled_modules, candidate_id)——留出胜率优先、同分取更稀疏枝、再
  按候选 id 确定性破平。训练侧成绩只入报告（finalists_report），不进
  裁决键。
* fail-closed：留出局不足（< 请求占比×总局数，缺省 30%）抛
  ValueError（"留出局不足"）——无论 finalists 多少。
* 产物（output_dir）：holdout_table.json（全 finalists 留出逐局明细）+
  final_selection.json（最终件：库件+配置+留出胜率/边际+对手逐局边际
  表）+ holdout_margin_table.csv（人读逐局边际表）。

确定性：裁决与产物均无墙钟、无随机；同输入同输出。
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

from select_on_holdout.rank_candidates_seated import rank_candidates_seated

DEFAULT_OUTPUT_DIR = None  # 缺省不落盘（编排层指定 search/）


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _margin_table_csv(final_row):
    rows = [("candidate_id", "episode_id", "opponent", "me_seat",
             "result", "margin", "me_final", "opp_final")]
    for game in final_row["games"]:
        me_final = game["finals"][game["me_seat"]]
        opp_final = game["finals"][1 - game["me_seat"]]
        result = "W" if game["win"] else ("D" if game["draw"] else "L")
        rows.append((final_row["candidate_id"],
                     str(game["episode_id"]), str(game["opponent"]),
                     str(game["me_seat"]), result,
                     f"{game['margin']:.1f}", f"{me_final:.1f}",
                     f"{opp_final:.1f}"))
    return "\n".join(",".join(row) for row in rows) + "\n"


def select_on_holdout(payload=None):
    """意图级签名；真值在责任文档。

    payload：{finalists（候选对象列表）, holdout_games, n_games_total
    （缺省=len(holdout_games)+len(train_games)，占比校验用）,
    holdout_fraction_min=0.30, evaluator/ranker（可注入；缺省
    rank_candidates_seated）, lambda_sparse=0.02, train_rows（可选，
    finalis 训练侧成绩，只入报告）, output_dir}。
    返回 {final（最终件+留出逐局边际表）, holdout_table, finalists_report,
    proof}；final 含 holdout winrate/margin_mean/score 与配置全量。
    """
    payload = dict(payload or {})
    finalists = payload.get("finalists") or []
    holdout_games = payload.get("holdout_games") or []
    if not finalists:
        raise ValueError("select_on_holdout needs finalists (fail-closed)")
    if not holdout_games:
        raise ValueError("select_on_holdout needs holdout games "
                         "(fail-closed)")
    lambda_sparse = float(payload.get("lambda_sparse") or 0.02)
    fraction_min = float(payload.get("holdout_fraction_min") or 0.30)
    n_total = int(payload.get("n_games_total")
                  or (len(holdout_games)
                      + int(payload.get("n_train_games") or 0)))
    if n_total <= 0:
        n_total = len(holdout_games)
    if len(holdout_games) / n_total < fraction_min - 1e-9:
        raise ValueError(
            f"留出局不足: {len(holdout_games)}/{n_total} < "
            f"{fraction_min:.0%} (fail-closed)")

    ranker = payload.get("ranker") or (lambda p: rank_candidates_seated(p))
    ranked = ranker({
        "candidates": finalists,
        "games": holdout_games,
        "evaluator": payload.get("evaluator"),
        "lambda_sparse": lambda_sparse,
        "library_dir": payload.get("library_dir"),
        "modules_path": payload.get("modules_path"),
    })
    table = ranked["table"]
    winner = table[0]

    train_rows = payload.get("train_rows") or {}
    finalists_report = [
        {
            "candidate_id": row["candidate_id"],
            "holdout_score": row["score"],
            "holdout_winrate": row["winrate"],
            "holdout_margin_mean": row["margin_mean"],
            "train_score": train_rows.get(row["candidate_id"], {}).get(
                "score"),
            "train_winrate": train_rows.get(row["candidate_id"], {}).get(
                "winrate"),
        }
        for row in table
    ]

    final = {
        "candidate_id": winner["candidate_id"],
        "piece": winner["piece"],
        "switches": winner["switches"],
        "thresholds": winner.get("thresholds"),
        "enabled_modules": winner["enabled_modules"],
        "holdout": {
            "n_games": winner["n"],
            "wins": winner["wins"],
            "draws": winner["draws"],
            "losses": winner["losses"],
            "winrate": winner["winrate"],
            "margin_mean": winner["margin_mean"],
            "score": winner["score"],
            "margin_table": [
                {"episode_id": g["episode_id"], "opponent": g["opponent"],
                 "me_seat": g["me_seat"],
                 "result": "W" if g["win"] else ("D" if g["draw"] else "L"),
                 "margin": g["margin"]}
                for g in winner["games"]
            ],
        },
        "finalists_report": finalists_report,
    }
    final["selection_sha256"] = hashlib.sha256(
        _canonical(final).encode("utf-8")).hexdigest()

    result = {
        "final": final,
        "holdout_table": table,
        "finalists_report": finalists_report,
        "lambda_sparse": lambda_sparse,
        "proof": {
            "decided_on": "holdout_only",
            "n_holdout_games": len(holdout_games),
            "n_games_total": n_total,
            "holdout_game_fraction": len(holdout_games) / n_total,
            "ranking_key": "(-holdout_score, enabled_modules, "
                           "candidate_id)",
        },
    }

    output_dir = payload.get("output_dir")
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        (output_dir / "holdout_table.json").write_text(
            _canonical(table) + "\n", encoding="utf-8")
        (output_dir / "final_selection.json").write_text(
            _canonical(final) + "\n", encoding="utf-8")
        (output_dir / "holdout_margin_table.csv").write_text(
            _margin_table_csv(winner), encoding="utf-8")
        result["paths"] = {
            "holdout_table": str(output_dir / "holdout_table.json"),
            "final_selection": str(output_dir / "final_selection.json"),
            "margin_csv": str(output_dir / "holdout_margin_table.csv"),
        }
    return result
