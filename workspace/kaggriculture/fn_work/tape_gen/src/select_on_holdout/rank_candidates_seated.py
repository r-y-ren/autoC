"""rank_candidates_seated（L1，R5）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

seated 适应度表（孪生整季重演，真实对手流）。

* 评估原语复用 R4 侧件（search_reflector_configs.evaluate_ablation_tree
  的 SeatedEvaluator/_call_evaluator）：候选注入我席 vs 对手真实动作流
  （rollout_with_replay_opponent），逐局 胜/平/负+边际（我−对手）；
  winrate 平局计 0.5。评估器可注入（payload["evaluator"]，测试用假评
  估器——契约 candidate×games → 行集，同 SeatedEvaluator.__call__）。
* 排序：score = winrate − λ×启用模块数（稀疏惩罚与 R4 同式同缺省 λ=
  0.02，登记可调）；排序键 (-score, enabled_modules, candidate_id)——
  同适应度取更稀疏枝（R5 与 R4 共用同一可证稀疏优先）。
* 行含 per-game 明细（episode_id/opponent/me_seat/win/draw/margin/
  finals）——select_on_holdout 以此生成留出逐局边际表。

确定性：候选序确定、无墙钟；表为纯投影（同输入同输出）。
"""

from __future__ import annotations

from search_reflector_configs.evaluate_ablation_tree import (
    _call_evaluator,
    score_row,
)


def rank_candidates_seated(payload=None):
    """意图级签名；真值在责任文档。

    payload：{candidates, games, evaluator（可注入；缺省真实
    SeatedEvaluator——经 evaluate_ablation_tree 构造）, lambda_sparse=
    0.02, library_dir, modules_path}。
    返回 {table（逐候选：winrate/margin_mean/wins/draws/losses/score/
    per-game 明细，按排序键降序）, ranking（有序 candidate_id）,
    lambda_sparse}。
    """
    payload = dict(payload or {})
    candidates = payload.get("candidates") or []
    games = payload.get("games") or []
    if not candidates or not games:
        raise ValueError("rank_candidates_seated needs candidates and "
                         "games (fail-closed)")
    lambda_sparse = float(payload.get("lambda_sparse") or 0.02)
    evaluator = payload.get("evaluator")
    if evaluator is None:
        from search_reflector_configs.evaluate_ablation_tree import \
            SeatedEvaluator
        evaluator = SeatedEvaluator(library_dir=payload.get("library_dir"),
                                    modules_path=payload.get("modules_path"))

    rows_by_id = _call_evaluator(evaluator, candidates, games)
    candidates_by_id = {c["id"]: c for c in candidates}

    table = []
    for cid, entry in rows_by_id.items():
        candidate = candidates_by_id[cid]
        row = dict(entry)
        row["score"] = score_row(entry, candidate, lambda_sparse)
        row["enabled_modules"] = candidate["enabled_modules"]
        row["piece"] = candidate["piece"]
        row["switches"] = candidate["switches"]
        row["thresholds"] = candidate.get("thresholds")
        table.append(row)
    table.sort(key=lambda r: (-r["score"], r["enabled_modules"],
                              r["candidate_id"]))
    return {
        "lambda_sparse": lambda_sparse,
        "table": table,
        "ranking": [row["candidate_id"] for row in table],
    }
