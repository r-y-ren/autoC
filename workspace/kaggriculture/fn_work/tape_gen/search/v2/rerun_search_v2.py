"""T5 适应度 v2 重搜跑批驱动（search/v2/ 产物生成器）。

分阶段混合适应度（R5 v2 用户裁决 2026-09-23）：

* 粗筛 = v1 底表复用（search/coarse_table.json，320 候选×8 局 seated
  不重算——登记文件 sha256 与 coarse_reused）；
* 精评 = top-12（K 帽 12）留出 51 局 seated + h2h 臂 4 局/候选
  （seed 101/201 × AB/BA 席，vs 纯 v48 官方真引擎，M1 同通道）；
* 混合分 = 0.5×留出胜率 + 0.5×h2h 互胜 − λ×模块数（λ=0.02）；
* 微轴精化与 finalists 同混 h2h；裁决 = 混合分（finalist_rows[0]）。
* 墙钟硬帽 9000s（2.5h）——超帽由 evaluate_ablation_tree 截断留痕。

产物（本目录）：config_space.{json,md} / split_train_holdout.json /
coarse_table.json（复用面重挂）/ fine_table.json / refinement_table.json /
h2h_summary.json / ablation_ledger.jsonl / runtime_stats.json /
final_selection.json / holdout_margin_table.csv。
账本行全确定性（无墙钟；墙钟与引擎局数计数入 runtime_stats.json）。

打包裁决规则（registered）：混合分冠军若与 v48 外壳缺省配置面一致 →
直接打包；否则取混合分序最高的**可打包** finalist（登记 package_
selection 行——打包手术面只换库的既定约束）。M1 重走随 candidate/
更新（run_m1_m2_gates lines=m1+h2h）。

用法：python rerun_search_v2.py [--package-and-gates]
"""

from __future__ import annotations

import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_TAPE_GEN_ROOT = _HERE.parents[1]                 # fn_work/tape_gen
_CAMPAIGN_ROOT = _HERE.parents[4]                 # workspace/kaggriculture
_SRC = _TAPE_GEN_ROOT / "src"
for p in (str(_SRC),):
    if p not in sys.path:
        sys.path.insert(0, p)

from search_reflector_configs.define_config_space import define_config_space  # noqa: E402
from search_reflector_configs.evaluate_ablation_tree import (  # noqa: E402
    H2HEvaluator,
    SeatedEvaluator,
    evaluate_ablation_tree,
    mixed_score,
)
from search_reflector_configs.search_reflector_configs import _ledger_line  # noqa: E402
from select_on_holdout.split_train_holdout import split_train_holdout  # noqa: E402

V1_SEARCH = _TAPE_GEN_ROOT / "search"
V1_SPLIT_SHA = "ebbde29c8986d6fe20f0e854445bce5957d21d702fc4842e7aa16a12e27b4f35"
LAMBDA_SPARSE = 0.02
TIERS_V2 = {
    "coarse_games": 8,
    "coarse_subsample_seed": 20260923,
    "fine_top_k": 12,
    "refinement": True,
    "finalists_n": 3,
    "wall_clock_budget_s": 9000.0,   # 2.5h 硬帽
}


def _canonical(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"))


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _margin_csv(winner_row) -> str:
    rows = [("candidate_id", "episode_id", "opponent", "me_seat",
             "result", "margin", "h2h_component")]
    for g in winner_row["games"]:
        rows.append((winner_row["candidate_id"], str(g["episode_id"]),
                     str(g["opponent"]), str(g["me_seat"]),
                     "W" if g["win"] else ("D" if g["draw"] else "L"),
                     f"{g['margin']:.1f}", "-"))
    return "\n".join(",".join(r) for r in rows) + "\n"


def run_search() -> dict:
    started = time.monotonic()
    ledger = []

    # ---- 1. 空间（与 v1 同库面 → space_sha256 应一致）----
    space = define_config_space({"output_dir": str(_HERE), "write": True})
    ledger.append(_ledger_line("config_space", {
        "n_pieces": space["n_pieces"], "n_switches": space["n_switches"],
        "base_space_size": space["base_space_size"],
        "refinement_fanout": space["refinement_fanout"],
        "space_sha256": space["space_sha256"],
        "lambda_sparse": LAMBDA_SPARSE}))

    # ---- 2. 分离复算（同种子确定性；与 v1 一致性 fail-closed 校验）----
    split = split_train_holdout({"output_dir": str(_HERE)})
    if split["split_sha256"] != V1_SPLIT_SHA:
        raise ValueError(f"split 与 v1 不一致——粗筛底表复用失效 "
                         f"(fail-closed): {split['split_sha256']}")
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
        "split_sha256": split["split_sha256"],
        "identical_to_v1": True}))

    # ---- 3. v1 粗筛底表复用（登记）----
    v1_coarse_path = V1_SEARCH / "coarse_table.json"
    v1_sha = _sha256_file(v1_coarse_path)
    v1_rows = json.loads(v1_coarse_path.read_text(encoding="utf-8"))
    coarse_rows = {row["candidate_id"]: row for row in v1_rows}
    coarse_source = f"v1 search/coarse_table.json sha256={v1_sha}"
    ledger.append(_ledger_line("coarse_reuse", {
        "source": coarse_source,
        "n_rows": len(coarse_rows),
        "policy": "v2 粗筛留出流 seated 不变——复用 v1 底表不重算"}))

    # ---- 4. 树评估 v2（精评留出+h2h 臂；h2h 新算）----
    evaluator = SeatedEvaluator()
    h2h = H2HEvaluator()
    evaluation = evaluate_ablation_tree({
        "candidates": space["candidates"],
        "games": split["train"]["games"],
        "fine_games": split["holdout"]["games"],
        "coarse_rows": coarse_rows,
        "coarse_source": coarse_source,
        "evaluator": evaluator,
        "h2h_runner": h2h,
        "lambda_sparse": LAMBDA_SPARSE,
        "tiers": TIERS_V2})
    b = evaluation["budget"]
    ledger.append(_ledger_line("ablation_tiers", {
        "n_coarse_candidates": b["n_coarse_candidates"],
        "n_coarse_games": b["n_coarse_games"],
        "coarse_reused": b["coarse_reused"],
        "coarse_source": b["coarse_source"],
        "n_fine_candidates": b["n_fine_candidates"],
        "n_fine_games": b["n_fine_games"],
        "h2h_games": evaluation["h2h_games"],
        "n_h2h_games_per_candidate": b["n_h2h_games_per_candidate"],
        "n_h2h_candidates": b["n_h2h_candidates"],
        "h2h_missing": b["h2h_missing"],
        "n_refinement_candidates": b["n_refinement_candidates"],
        "budget_exhausted": b["budget_exhausted"],
        "mixed_weights": evaluation["mixed_weights"],
        "finalists": evaluation["finalists"]}))
    for row in evaluation["fine"]:
        ledger.append(_ledger_line("fine_eval", {
            "candidate_id": row["candidate_id"],
            "holdout_winrate": row["winrate"],
            "h2h_winrate": (row["h2h"] or {}).get("winrate"),
            "h2h_margin_mean": (row["h2h"] or {}).get("margin_mean"),
            "score": row["score"],
            "margin_mean": row["margin_mean"],
            "enabled_modules": row["enabled_modules"], "n": row["n"]}))
    for row in evaluation["refinement"]:
        ledger.append(_ledger_line("refinement_eval", {
            "candidate_id": row["candidate_id"],
            "holdout_winrate": row["winrate"],
            "h2h_winrate": (row["h2h"] or {}).get("winrate"),
            "score": row["score"],
            "margin_mean": row["margin_mean"],
            "enabled_modules": row["enabled_modules"], "n": row["n"]}))
    for row in evaluation["finalist_rows"]:
        ledger.append(_ledger_line("finalist_row", {
            "candidate_id": row["candidate_id"],
            "holdout_winrate": row["winrate"],
            "h2h_winrate": (row["h2h"] or {}).get("winrate"),
            "score": row["score"],
            "enabled_modules": row["enabled_modules"],
            "switches": row["switches"],
            "thresholds": row["thresholds"]}))

    # ---- 5. 混合分裁决（v2：留出 seated + h2h 双臂；非 v1 纯留出）----
    ranked = evaluation["finalist_rows"]        # 已按 (-score, mods, id) 序
    winner = ranked[0]
    final = {
        "candidate_id": winner["candidate_id"],
        "piece": winner["piece"],
        "switches": winner["switches"],
        "thresholds": winner["thresholds"],
        "enabled_modules": winner["enabled_modules"],
        "holdout": {
            "n_games": winner["n"], "wins": winner["wins"],
            "draws": winner["draws"], "losses": winner["losses"],
            "winrate": winner["winrate"],
            "margin_mean": winner["margin_mean"],
            "margin_table": [
                {"episode_id": g["episode_id"], "opponent": g["opponent"],
                 "me_seat": g["me_seat"],
                 "result": "W" if g["win"] else (
                     "D" if g["draw"] else "L"),
                 "margin": g["margin"]} for g in winner["games"]]},
        "h2h": {
            "n_games": (winner["h2h"] or {}).get("n"),
            "winrate": (winner["h2h"] or {}).get("winrate"),
            "margin_mean": (winner["h2h"] or {}).get("margin_mean"),
            "games": [
                {"seed": g["seed"], "me_seat": g["me_seat"],
                 "margin": g["margin"],
                 "finals": g["finals"]} for g in
                (winner["h2h"] or {}).get("games", [])]},
        "mixed": {
            "weights": evaluation["mixed_weights"],
            "formula": "0.5*holdout_winrate + 0.5*h2h_winrate "
                       "- lambda_sparse*enabled_modules",
            "lambda_sparse": LAMBDA_SPARSE,
            "score": winner["score"]},
        "finalists_report": [
            {"candidate_id": r["candidate_id"], "holdout_winrate":
             r["winrate"], "h2h_winrate": (r["h2h"] or {}).get("winrate"),
             "mixed_score": r["score"], "enabled_modules":
             r["enabled_modules"]} for r in ranked],
        "proof": {
            "decided_on": "holdout_seated_plus_engine_h2h_mixed (v2)",
            "ranking_key": "(-mixed_score, enabled_modules, candidate_id)",
            "v1_decision": "holdout_only",
        },
    }
    final["selection_sha256"] = hashlib.sha256(
        _canonical(final).encode("utf-8")).hexdigest()
    ledger.append(_ledger_line("final_selection", {
        "candidate_id": final["candidate_id"],
        "piece": final["piece"],
        "switches": final["switches"],
        "thresholds": final["thresholds"],
        "enabled_modules": final["enabled_modules"],
        "holdout_winrate": final["holdout"]["winrate"],
        "holdout_margin_mean": final["holdout"]["margin_mean"],
        "h2h_winrate": final["h2h"]["winrate"],
        "mixed_score": final["mixed"]["score"],
        "selection_sha256": final["selection_sha256"]}))

    # ---- 6. 落盘（确定性面：表+账本；实测面：runtime）----
    (_HERE / "coarse_table.json").write_text(
        _canonical(evaluation["coarse"]) + "\n", encoding="utf-8")
    (_HERE / "fine_table.json").write_text(
        _canonical(evaluation["fine"]) + "\n", encoding="utf-8")
    (_HERE / "refinement_table.json").write_text(
        _canonical(evaluation["refinement"]) + "\n", encoding="utf-8")
    (_HERE / "ablation_ledger.jsonl").write_text(
        "".join(_canonical(line) + "\n" for line in ledger),
        encoding="utf-8")
    (_HERE / "final_selection.json").write_text(
        _canonical(final) + "\n", encoding="utf-8")
    (_HERE / "holdout_margin_table.csv").write_text(
        _margin_csv(winner), encoding="utf-8")
    h2h_summary = [
        {"candidate_id": r["candidate_id"], "holdout_winrate": r["winrate"],
         "h2h_winrate": (r["h2h"] or {}).get("winrate"),
         "h2h_wins": (r["h2h"] or {}).get("wins"),
         "h2h_n": (r["h2h"] or {}).get("n"),
         "h2h_margin_mean": (r["h2h"] or {}).get("margin_mean"),
         "mixed_score": r["score"], "enabled_modules":
         r["enabled_modules"]}
        for r in evaluation["fine"] + evaluation["refinement"]
        if r["h2h"] is not None]
    h2h_summary.sort(key=lambda r: (-r["mixed_score"],
                                    r["enabled_modules"],
                                    r["candidate_id"]))
    (_HERE / "h2h_summary.json").write_text(
        _canonical(h2h_summary) + "\n", encoding="utf-8")
    runtime = {
        "wall_clock_s": round(time.monotonic() - started, 3),
        "wall_clock_budget_s": TIERS_V2["wall_clock_budget_s"],
        "budget_exhausted": b["budget_exhausted"],
        "h2h_missing": b["h2h_missing"],
        "seated_evaluator_stats": dict(evaluator.stats),
        "h2h_evaluator_stats": dict(h2h.stats),
    }
    (_HERE / "runtime_stats.json").write_text(
        _canonical(runtime) + "\n", encoding="utf-8")

    return {"final": final, "evaluation": evaluation,
            "runtime": runtime, "ledger": ledger}


def run_package_and_gates(final: dict) -> dict:
    """打包（新最终件换库）+ M1/M2-h2h 重走（≥16 局对纯 v48）。"""
    from assemble_and_gate.build_candidate_package import (
        PackageError,
        build_candidate_package,
    )
    from assemble_and_gate.run_m1_m2_gates import run_m1_m2_gates

    out = {}
    # 打包裁决规则：冠军可打包则冠军；否则混合分序最高的可打包 finalist
    # （逐 finalist 用完整行构造 selection 试打包 skip_write，成功者真打包；
    #   拒绝原因全登记——打包手术面只换库的既定约束）。
    report = json.loads((_HERE / "final_selection.json"
                         ).read_text(encoding="utf-8"))
    tables = []
    for name in ("fine_table.json", "refinement_table.json"):
        tables += json.loads((_HERE / name).read_text(encoding="utf-8"))
    rows_by_id = {t["candidate_id"]: t for t in tables}
    ranked = sorted(report["finalists_report"],
                    key=lambda r: (-r["mixed_score"],
                                   r["enabled_modules"], r["candidate_id"]))
    pkg_sel, rejected = None, {}
    for row in ranked:
        cand = rows_by_id[row["candidate_id"]]
        sel = {
            "candidate_id": cand["candidate_id"], "piece": cand["piece"],
            "switches": cand["switches"], "thresholds": cand["thresholds"],
            "enabled_modules": cand["enabled_modules"],
            "holdout": {"n_games": cand["n"], "wins": cand["wins"],
                        "draws": cand["draws"], "losses": cand["losses"],
                        "winrate": cand["winrate"],
                        "margin_mean": cand["margin_mean"],
                        "margin_table": []},
            "finalists_report": [row],
        }
        try:
            build_candidate_package({"selection": sel, "skip_write": True})
            pkg_sel = sel
            break
        except PackageError as exc:
            rejected[row["candidate_id"]] = str(exc)[:200]
    if pkg_sel is None:
        raise RuntimeError(f"无可打包 finalist（配置面全部越界）: {rejected}")
    manifest = build_candidate_package({
        "selection": pkg_sel, "output_dir": str(_TAPE_GEN_ROOT / "candidate"),
        "package_id": "tapegen-c2"})
    out["package"] = manifest
    out["package_rule"] = {
        "selected": pkg_sel["candidate_id"],
        "mixed_winner": report["candidate_id"],
        "fallback_applied": pkg_sel["candidate_id"] !=
        report["candidate_id"],
        "rejected": rejected}

    gates = run_m1_m2_gates({
        "package_main": str(_TAPE_GEN_ROOT / "candidate" / "main.py"),
        "package_tar": str(_TAPE_GEN_ROOT / "candidate"
                           / "submission.tar.gz"),
        "output_dir": str(_TAPE_GEN_ROOT / "candidate" / "gates"),
        "lines": ["m1", "h2h"], "write": True})
    out["gates"] = gates
    _append_package_selection_ledger(out)
    return out


def _append_package_selection_ledger(pkg: dict) -> None:
    """打包回退裁决 + M1 重走数字 → 账本 package_selection 行（幂等）。"""
    ledger_path = _HERE / "ablation_ledger.jsonl"
    existing = [json.loads(line) for line in
                ledger_path.read_text(encoding="utf-8").splitlines()
                if line.strip()]
    if any(line["record"] == "package_selection" for line in existing):
        return
    gates = pkg["gates"]
    m1 = gates["m1"]
    h2h_line = gates["m2"]["lines"]["h2h"]["result"]
    line = _ledger_line("package_selection", {
        "selected": pkg["package_rule"]["selected"],
        "mixed_winner": pkg["package_rule"]["mixed_winner"],
        "fallback_applied": pkg["package_rule"]["fallback_applied"],
        "rejected": pkg["package_rule"]["rejected"],
        "rule": "混合分冠军可打包则冠军；否则混合分序最高的可打包 "
                "finalist（打包手术面=只换库的既定约束，fail-closed 拒绝"
                "原因全登记）",
        "package_main_sha256":
            pkg["package"]["products"]["main_py"]["sha256"],
        "package_tar_sha256":
            pkg["package"]["products"]["submission_tar_gz"]["sha256"],
        "m1_rerun": {
            "games": m1["games"], "wins": m1["wins"], "ties": m1["ties"],
            "losses": m1["losses"],
            "win_rate_half_ties": m1["win_rate_half_ties"],
            "avg_margin": m1["avg_margin"], "passed": m1["passed"],
            "grading": gates["grading"]["m1"]},
        "m2_h2h_line": {
            "games": h2h_line["games"], "wins": h2h_line["wins"],
            "win_fraction_strict": h2h_line["win_fraction_strict"],
            "avg_margin": h2h_line["avg_margin"],
            "passed": gates["m2"]["lines"]["h2h"]["passed"]},
    })
    with ledger_path.open("a", encoding="utf-8") as fh:
        fh.write(_canonical(line) + "\n")


def main() -> int:
    argv = sys.argv[1:]
    result = run_search()
    final = result["final"]
    print(json.dumps({
        "final": {k: final[k] for k in ("candidate_id", "piece",
                                        "switches", "thresholds",
                                        "enabled_modules", "selection_sha256")},
        "holdout_winrate": final["holdout"]["winrate"],
        "h2h_winrate": final["h2h"]["winrate"],
        "mixed_score": final["mixed"]["score"],
        "budget": result["evaluation"]["budget"],
        "runtime": result["runtime"],
    }, ensure_ascii=False, indent=1))
    if "--package-and-gates" in argv:
        pkg = run_package_and_gates(final)
        print(json.dumps({
            "package_rule": pkg["package_rule"],
            "package_products": pkg["package"]["products"],
            "grading": pkg["gates"]["grading"],
            "m1": {k: pkg["gates"]["m1"][k] for k in
                   ("games", "wins", "ties", "losses",
                    "win_rate_half_ties", "win_fraction_strict",
                    "avg_margin", "passed")},
            "m2_h2h": {"passed": pkg["gates"]["m2"]["lines"]["h2h"]["passed"],
                       "summary": {k: pkg["gates"]["m2"]["lines"]["h2h"]
                                   ["result"][k] for k in
                                   ("games", "wins", "win_fraction_strict",
                                    "avg_margin")}},
        }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except SystemExit:
        raise
    except Exception:                        # noqa: BLE001
        traceback.print_exc()
        raise SystemExit(2)
