"""search_reflector_configs（L0，R4）。职责与验收详见 fn_work/tape_gen/fn_docs/responsibility.md。

顶层编排（空间定义 → 对手级分离 → 树评估（预算分级）→ 留出裁决 → 消融
账本）。

* 输入：候选库 + 评估预算（payload：library_dir / store_path /
  lambda_sparse / tiers / seeds / wall_clock_budget_s / output_dir /
  evaluator 可注入）。
* 输出：选定配置（select_on_holdout 产物，只在留出集裁决）+ 消融账本
  （search/ablation_ledger.jsonl——每选择留痕，JSONL 逐行 content_sha256
  自证）+ 分级表（coarse/fine/refinement）+ 留出逐局边际表（经
  select_on_holdout 落盘）。
* 错误语义：预算耗尽 → 取已评最优并标注（evaluate_ablation_tree 内
  部处理，本层如实透传 budget_exhausted）；留出不足 → fail-closed 上抛。
* 账本纪律（R7 预演）：账本行全确定性（无墙钟/时间戳）；墙钟与 rollout
  计数入 runtime_stats.json（实测字段，独立于确定性链）。
* 复用真实 seated 评估基建：SeatedEvaluator（twin 孪生通道 +
  rollout_with_replay_opponent 双席注入修复版；反射层真值=v48 深读档
  modules/ 只读 import）。
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from search_reflector_configs.define_config_space import define_config_space
from search_reflector_configs.evaluate_ablation_tree import (
    SeatedEvaluator,
    evaluate_ablation_tree,
)
from select_on_holdout.select_on_holdout import select_on_holdout
from select_on_holdout.split_train_holdout import split_train_holdout

_CAMPAIGN_ROOT = Path(__file__).resolve().parents[4]
_TAPE_GEN_ROOT = _CAMPAIGN_ROOT / "fn_work" / "tape_gen"
DEFAULT_OUTPUT_DIR = _TAPE_GEN_ROOT / "search"

DEFAULT_TIERS = {
    "coarse_games": 8,
    "coarse_subsample_seed": 20260923,
    "fine_top_k": 6,
    "refinement": True,
    "finalists_n": 3,
    "wall_clock_budget_s": 7200.0,
}


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _ledger_line(record: str, content: dict) -> dict:
    body = {"record": record, **content}
    body["content_sha256"] = hashlib.sha256(
        _canonical(body).encode("utf-8")).hexdigest()
    return body


def search_reflector_configs(payload=None):
    """意图级签名；真值在责任文档。

    返回 {space（空间登记摘要）, split（分离证明摘要）, evaluation
    （分级摘要+finalists）, selection（最终件+留出逐局边际表）, ledger
    （账本行列表）, runtime（墙钟/rollout 计数——实测字段）, paths}。
    产物：search/{config_space.json,md, split_train_holdout.json,
    coarse_table.json, fine_table.json, refinement_table.json,
    ablation_ledger.jsonl, runtime_stats.json} + select_on_holdout 三件。
    """
    payload = dict(payload or {})
    started = time.monotonic()
    output_dir = Path(payload.get("output_dir") or DEFAULT_OUTPUT_DIR)
    lambda_sparse = float(payload.get("lambda_sparse") or 0.02)
    tiers = dict(DEFAULT_TIERS)
    tiers.update(payload.get("tiers") or {})
    ledger = []

    evaluator = payload.get("evaluator")
    owns_evaluator = evaluator is None
    if evaluator is None:
        evaluator = SeatedEvaluator(
            library_dir=payload.get("library_dir"),
            modules_path=payload.get("modules_path"))

    # ---- 1. 空间定义（R4）----
    space = define_config_space({
        "library_dir": payload.get("library_dir"),
        "output_dir": str(output_dir), "write": True})
    ledger.append(_ledger_line("config_space", {
        "n_pieces": space["n_pieces"], "n_switches": space["n_switches"],
        "base_space_size": space["base_space_size"],
        "refinement_fanout": space["refinement_fanout"],
        "space_sha256": space["space_sha256"],
        "lambda_sparse": lambda_sparse}))

    # ---- 2. 对手级分离（R5）----
    split = split_train_holdout({
        "store_path": payload.get("store_path"),
        "replay_dirs": payload.get("replay_dirs"),
        "seed": payload.get("split_seed"),
        "holdout_fraction": payload.get("holdout_fraction"),
        "min_holdout_games": payload.get("min_holdout_games"),
        "forced_train_opponents": payload.get("forced_train_opponents"),
        "output_dir": str(output_dir)})
    ledger.append(_ledger_line("split_train_holdout", {
        "seed": split["seed"],
        "n_train_games": split["proof"]["n_train_games"],
        "n_holdout_games": split["proof"]["n_holdout_games"],
        "n_train_opponents": split["proof"]["n_train_opponents"],
        "n_holdout_opponents": split["proof"]["n_holdout_opponents"],
        "holdout_opponent_fraction":
            split["proof"]["holdout_opponent_fraction"],
        "intersection": split["proof"]["intersection"],
        "mining_sources_in_holdout":
            split["proof"]["mining_sources_in_holdout"],
        "split_sha256": split["split_sha256"]}))

    # ---- 3. 树评估：预算分级（R4）----
    evaluation = evaluate_ablation_tree({
        "candidates": space["candidates"],
        "games": split["train"]["games"],
        "evaluator": evaluator,
        "lambda_sparse": lambda_sparse,
        "tiers": tiers})
    ledger.append(_ledger_line("ablation_tiers", {
        "n_coarse_candidates": evaluation["budget"]["n_coarse_candidates"],
        "n_coarse_games": evaluation["budget"]["n_coarse_games"],
        "coarse_subsample": evaluation["subsample"],
        "n_fine_candidates": evaluation["budget"]["n_fine_candidates"],
        "n_fine_games": evaluation["budget"]["n_fine_games"],
        "n_refinement_candidates":
            evaluation["budget"]["n_refinement_candidates"],
        "budget_exhausted": evaluation["budget"]["budget_exhausted"],
        "finalists": evaluation["finalists"]}))
    for row in evaluation["coarse"][:10]:
        ledger.append(_ledger_line("coarse_eval", {
            "candidate_id": row["candidate_id"],
            "winrate": row["winrate"], "score": row["score"],
            "enabled_modules": row["enabled_modules"],
            "n": row["n"]}))
    for row in evaluation["fine"]:
        ledger.append(_ledger_line("fine_eval", {
            "candidate_id": row["candidate_id"],
            "winrate": row["winrate"], "score": row["score"],
            "margin_mean": row["margin_mean"],
            "enabled_modules": row["enabled_modules"], "n": row["n"]}))
    for row in evaluation["refinement"]:
        ledger.append(_ledger_line("refinement_eval", {
            "candidate_id": row["candidate_id"],
            "winrate": row["winrate"], "score": row["score"],
            "margin_mean": row["margin_mean"],
            "enabled_modules": row["enabled_modules"], "n": row["n"]}))

    # ---- 4. 留出裁决（R5，只在留出集）----
    finalists = [c for c in space["candidates"]
                 if c["id"] in set(evaluation["finalists"])]
    missing = set(evaluation["finalists"]) - {c["id"] for c in finalists}
    if missing:  # refinement 变体作 finalist（id 带微轴后缀）
        for row in evaluation["finalist_rows"]:
            if row["candidate_id"] in missing:
                finalists.append({
                    "id": row["candidate_id"], "piece": row["piece"],
                    "switches": row["switches"],
                    "thresholds": row["thresholds"],
                    "enabled_modules": row["enabled_modules"]})
    finalists.sort(key=lambda c: c["id"])
    train_rows = {row["candidate_id"]: row
                  for row in evaluation["finalist_rows"]}
    selection = select_on_holdout({
        "finalists": finalists,
        "holdout_games": split["holdout"]["games"],
        "n_games_total": (split["proof"]["n_train_games"]
                          + split["proof"]["n_holdout_games"]),
        "evaluator": evaluator,
        "lambda_sparse": lambda_sparse,
        "train_rows": train_rows,
        "output_dir": str(output_dir)})
    ledger.append(_ledger_line("holdout_eval", {
        "finalists": [row["candidate_id"]
                      for row in selection["holdout_table"]],
        "holdout_ranking": selection["finalists_report"]}))
    ledger.append(_ledger_line("final_selection", {
        "candidate_id": selection["final"]["candidate_id"],
        "piece": selection["final"]["piece"],
        "switches": selection["final"]["switches"],
        "thresholds": selection["final"]["thresholds"],
        "enabled_modules": selection["final"]["enabled_modules"],
        "holdout_winrate": selection["final"]["holdout"]["winrate"],
        "holdout_margin_mean":
            selection["final"]["holdout"]["margin_mean"],
        "holdout_score": selection["final"]["holdout"]["score"],
        "selection_sha256": selection["final"]["selection_sha256"]}))

    # ---- 5. 落盘（账本=确定性；runtime=实测）----
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "coarse_table.json").write_text(
        _canonical(evaluation["coarse"]) + "\n", encoding="utf-8")
    (output_dir / "fine_table.json").write_text(
        _canonical(evaluation["fine"]) + "\n", encoding="utf-8")
    (output_dir / "refinement_table.json").write_text(
        _canonical(evaluation["refinement"]) + "\n", encoding="utf-8")
    ledger_path = output_dir / "ablation_ledger.jsonl"
    ledger_path.write_text(
        "".join(_canonical(line) + "\n" for line in ledger),
        encoding="utf-8")

    runtime = {
        "wall_clock_s": round(time.monotonic() - started, 3),
        "wall_clock_budget_s": tiers["wall_clock_budget_s"],
        "budget_exhausted": evaluation["budget"]["budget_exhausted"],
    }
    if owns_evaluator:
        runtime["evaluator_stats"] = dict(evaluator.stats)
    (output_dir / "runtime_stats.json").write_text(
        _canonical(runtime) + "\n", encoding="utf-8")

    return {
        "space": {k: v for k, v in space.items()
                  if k != "candidates"},
        "split": {"proof": split["proof"], "seed": split["seed"],
                  "split_sha256": split["split_sha256"]},
        "evaluation": evaluation,
        "selection": selection,
        "ledger": ledger,
        "runtime": runtime,
        "paths": {"output_dir": str(output_dir),
                  "ledger": str(ledger_path)},
    }
