"""evaluate_ablation_tree 真实测试（R4：预算分级+稀疏惩罚评分；
v2：分阶段混合适应度）。

tmp 假评估器注入（不触引擎/回放）：验证 score=winrate−λ×模块数、
粗筛每候选 ≤N 局、top-K 精评、同分取稀疏、确定性、预算耗尽语义
（零评估 fail-closed；部分评估取已评最优并标注）。
v2：混合分=0.5×留出胜率+0.5×h2h 互胜−λ×模块数（h2h 臂可注入假
runner）、fine_games 独立于粗筛局集、coarse_rows 底表复用登记、
fine_top_k≤12 契约帽、h2h 截断留痕、含 h2h 臂的确定性。
"""

import time

import pytest
from search_reflector_configs.evaluate_ablation_tree import (
    DEFAULT_H2H_GAMES,
    FINE_TOP_K_CAP,
    evaluate_ablation_tree,
    mixed_score,
)


def _candidate(cid, piece, mask):
    switches = {name: bit == "1" for name, bit in zip(
        ("clone_preempt", "slot_reorder", "market_maker",
         "terminal_forced", "dead_price_guard"), mask)}
    return {"id": cid, "piece": piece, "switches": switches,
            "thresholds": {"clone_streak_required": 24,
                           "dead_guard_ratio": 0.5},
            "enabled_modules": sum(1 for v in switches.values() if v)}


def _games(n, prefix=3000):
    return [{"episode_id": prefix + i, "opp_seat": 0, "me_seat": 1,
             "opponent": f"opp{i}", "replay_path": f"/tmp/fake-{i}.json"}
            for i in range(n)]


def _fake_evaluator(winrates, calls=None, sleep_s=0.0):
    """candidate×games → 行集；胜率查表后按局数量化（wins=round(wr×n)，
    winrate=wins/n——与真实评估器同口径）；可记录调用、可注入延时。"""
    def evaluator(candidate, games):
        if calls is not None:
            calls.append((candidate["id"], len(games)))
        if sleep_s:
            time.sleep(sleep_s)
        n = len(games)
        key = candidate["id"].split("+")[0]
        wins = round(winrates[key] * n)
        rows = [{"episode_id": g["episode_id"],
                 "opponent": g["opponent"], "me_seat": g["me_seat"],
                 "win": i < wins, "draw": False,
                 "margin": (100.0 if i < wins else -100.0)}
                for i, g in enumerate(games)]
        return {"candidate_id": candidate["id"], "games": rows,
                "n": n, "wins": wins, "draws": 0, "losses": n - wins,
                "winrate": wins / n if n else 0.0,
                "margin_mean": (2 * wins - n) * 100.0 / n if n else 0.0}
    return evaluator


def test_score_sparse_penalty_math():
    # 10 局：a#00000 wr=.5→5 胜 score=.5；a#11000 wr=.7→7 胜 score=.7−.04
    winrates = {"a#00000": 0.5, "a#11000": 0.7}
    result = evaluate_ablation_tree({
        "candidates": [_candidate("a#00000", "route:default", "00000"),
                       _candidate("a#11000", "route:default", "11000")],
        "games": _games(10),
        "evaluator": _fake_evaluator(winrates),
        "lambda_sparse": 0.02,
        "tiers": {"coarse_games": 10, "fine_top_k": 2, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    by_id = {row["candidate_id"]: row for row in result["fine"]}
    assert by_id["a#00000"]["winrate"] == pytest.approx(0.5)
    assert by_id["a#00000"]["score"] == pytest.approx(0.5)
    assert by_id["a#11000"]["winrate"] == pytest.approx(0.7)
    assert by_id["a#11000"]["score"] == pytest.approx(0.7 - 0.02 * 2)
    assert result["finalists"][0] == "a#11000"


def test_same_fitness_prefers_sparser_branch():
    # 同适应度（10 局 6 胜=0.6）：2 模块 vs 3 模块 → 稀疏者 score 更高
    winrates = {"p#11000": 0.6, "p#11100": 0.6}
    result = evaluate_ablation_tree({
        "candidates": [_candidate("p#11000", "variant:v0", "11000"),
                       _candidate("p#11100", "variant:v0", "11100")],
        "games": _games(10),
        "evaluator": _fake_evaluator(winrates),
        "lambda_sparse": 0.02,
        "tiers": {"coarse_games": 10, "fine_top_k": 2, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    row = {r["candidate_id"]: r for r in result["fine"]}
    assert row["p#11000"]["winrate"] == row["p#11100"]["winrate"]
    assert row["p#11000"]["score"] > row["p#11100"]["score"]
    assert result["finalists"][0] == "p#11000"


def test_budget_tiers_coarse_then_fine():
    winrates = {"a#00000": 0.7, "a#00001": 0.4, "a#10000": 0.6,
                "a#01000": 0.5}
    calls = []
    candidates = [_candidate("a#00000", "route:default", "00000"),
                  _candidate("a#00001", "route:default", "00001"),
                  _candidate("a#10000", "route:default", "10000"),
                  _candidate("a#01000", "route:default", "01000")]
    result = evaluate_ablation_tree({
        "candidates": candidates, "games": _games(20),
        "evaluator": _fake_evaluator(winrates, calls),
        "tiers": {"coarse_games": 8, "fine_top_k": 2, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    # 粗筛：每候选恰好 ≤8 局（预算纪律）
    assert sorted(c for c in calls if c[1] == 8) == \
        [("a#00000", 8), ("a#00001", 8), ("a#01000", 8), ("a#10000", 8)]
    assert result["budget"]["n_coarse_candidates"] == 4
    assert result["budget"]["n_coarse_games"] == 8
    # 精评：top-2（粗筛 0.75 / 0.605）在全 20 训练局
    fine_ids = {row["candidate_id"] for row in result["fine"]}
    assert fine_ids == {"a#00000", "a#10000"}
    assert ("a#00000", 20) in calls and ("a#10000", 20) in calls
    assert result["budget"]["n_fine_games"] == 20


def test_refinement_only_around_best_with_module_gate():
    # 最佳配置 dead_price_guard 关 → 死价比率微轴不生成；clone_preempt
    # 开 → streak 微轴生成 1 个变体（模块门控）
    winrates = {"a#10000": 0.8, "a#00000": 0.5}
    calls = []
    result = evaluate_ablation_tree({
        "candidates": [_candidate("a#10000", "route:default", "10000"),
                       _candidate("a#00000", "route:default", "00000")],
        "games": _games(12),
        "evaluator": _fake_evaluator(winrates, calls),
        "tiers": {"coarse_games": 4, "fine_top_k": 2, "refinement": True,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    refined_ids = [row["candidate_id"] for row in result["refinement"]]
    assert refined_ids == ["a#10000+clone_streak_required=16"]
    assert result["budget"]["n_refinement_candidates"] == 1
    assert any(cid.startswith("a#10000+clone") and n == 12
               for cid, n in calls)


def test_determinism_with_injected_evaluator():
    winrates = {"a#00000": 0.6, "a#11111": 0.6, "a#11000": 0.55}
    candidates = [_candidate("a#00000", "route:default", "00000"),
                  _candidate("a#11111", "route:default", "11111"),
                  _candidate("a#11000", "route:default", "11000")]

    def run():
        return evaluate_ablation_tree({
            "candidates": candidates, "games": _games(16),
            "evaluator": _fake_evaluator(winrates),
            "tiers": {"coarse_games": 6, "fine_top_k": 3,
                      "refinement": True, "finalists_n": 2,
                      "wall_clock_budget_s": 60}})
    a, b = run(), run()
    assert a["finalists"] == b["finalists"]
    assert [r["candidate_id"] for r in a["coarse"]] == \
        [r["candidate_id"] for r in b["coarse"]]
    assert a["subsample"] == b["subsample"]


def test_budget_exhaustion_partial_takes_evaluated_best():
    # 40 候选（3 个分块）+ 每次评估 5ms 延时 + 近零预算：首块已评、后续
    # 截断 → budget_exhausted=true，finalists 来自已评候选
    candidates = [_candidate(f"c{i:02d}#10000", "route:default", "10000")
                  for i in range(40)]
    winrates = {c["id"]: 0.5 + (i % 5) / 50 for i, c in
                enumerate(candidates)}
    result = evaluate_ablation_tree({
        "candidates": candidates, "games": _games(4),
        "evaluator": _fake_evaluator(winrates, sleep_s=0.005),
        "tiers": {"coarse_games": 4, "fine_top_k": 3, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 0.05}})
    assert result["budget"]["budget_exhausted"] is True
    assert 0 < result["budget"]["n_coarse_candidates"] < 40
    assert len(result["finalists"]) >= 1


def test_budget_exhaustion_zero_evaluated_fail_closed():
    winrates = {"a#00000": 0.9}
    with pytest.raises(ValueError, match="预算耗尽"):
        evaluate_ablation_tree({
            "candidates": [_candidate("a#00000", "route:default", "00000")],
            "games": _games(10),
            "evaluator": _fake_evaluator(winrates),
            "tiers": {"coarse_games": 4, "wall_clock_budget_s": 0.0}})


def test_fail_closed_empty_inputs():
    with pytest.raises(ValueError, match="fail-closed"):
        evaluate_ablation_tree({"candidates": [], "games": _games(4),
                                "evaluator": _fake_evaluator({})})
    with pytest.raises(ValueError, match="fail-closed"):
        evaluate_ablation_tree({
            "candidates": [_candidate("a#00000", "p", "00000")],
            "games": [], "evaluator": _fake_evaluator({})})


# ---------------------------------------------------------------------------
# v2：分阶段混合适应度（h2h 臂 + fine_games + 粗筛底表复用 + 契约帽）
# ---------------------------------------------------------------------------
def _fake_h2h_runner(winrates, calls=None, sleep_s=0.0):
    """假 h2h 臂：winrates 查表（键=candidate id 去微轴后缀），行集与
    H2HEvaluator 同形（seed/me_seat 明细；无墙钟字段）。"""
    def runner(candidate, games):
        if calls is not None:
            calls.append((candidate["id"], [tuple(g) for g in games]))
        if sleep_s:
            time.sleep(sleep_s)
        n = len(games)
        key = candidate["id"].split("+")[0]
        wins = round(winrates.get(key, 0.0) * n)
        rows = [{"seed": int(seed), "opponent": "pure_v48",
                 "me_seat": int(seat), "win": i < wins, "draw": False,
                 "margin": 50.0 if i < wins else -50.0,
                 "finals": [0.0, 0.0], "statuses": ["DONE", "DONE"],
                 "turns": 720}
                for i, (seed, seat) in enumerate(games)]
        return {"candidate_id": candidate["id"], "games": rows, "n": n,
                "wins": wins, "draws": 0, "losses": n - wins,
                "winrate": wins / n,
                "margin_mean": (2 * wins - n) * 50.0 / n,
                "all_done": True}
    return runner


def test_mixed_score_math_and_degenerate():
    cand = _candidate("a#11000", "route:default", "11000")  # 2 模块
    seated = {"winrate": 0.9}
    h2h = {"winrate": 0.25}
    assert mixed_score(seated, h2h, cand, 0.02) == \
        pytest.approx(0.5 * 0.9 + 0.5 * 0.25 - 0.02 * 2)
    # h2h=None → v1 语义退化
    assert mixed_score(seated, None, cand, 0.02) == \
        pytest.approx(0.9 - 0.02 * 2)
    assert mixed_score({"winrate": 0.5}, {"winrate": 0.5}, cand, 0.0) == \
        pytest.approx(0.5)


def test_fine_stage_v2_holdout_and_h2h_arm_changes_selection():
    # 耦合假说行为：seated 强但 h2h=0 的候选（v1 会选）被混合分降级
    winrates = {"a#11000": 0.9, "a#00100": 0.8, "a#00000": 0.7}
    h2h_rates = {"a#11000": 0.0, "a#00100": 1.0, "a#00000": 0.25}
    seated_calls, h2h_calls = [], []
    candidates = [_candidate("a#11000", "route:default", "11000"),
                  _candidate("a#00100", "route:default", "00100"),
                  _candidate("a#00000", "route:default", "00000")]
    result = evaluate_ablation_tree({
        "candidates": candidates,
        "games": _games(12),                # 粗筛局集
        "fine_games": _games(6, prefix=4000),  # v2 精评 seated 局集=留出
        "evaluator": _fake_evaluator(winrates, seated_calls),
        "h2h_runner": _fake_h2h_runner(h2h_rates, h2h_calls),
        "lambda_sparse": 0.02,
        "tiers": {"coarse_games": 8, "fine_top_k": 3, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    # 粗筛在粗筛局集（≤8 局）；精评 seated 在留出 6 局
    assert sorted(n for _, n in seated_calls) == [6, 6, 6, 8, 8, 8]
    # h2h 臂：恰 top-3 候选 × 缺省局规格
    assert sorted(cid for cid, _ in h2h_calls) == \
        ["a#00000", "a#00100", "a#11000"]
    assert all(games == [tuple(g) for g in DEFAULT_H2H_GAMES]
               for _, games in h2h_calls)
    # 混合分排序（seated 臂 6 局量化：0.8/0.9→round→5/6；0.7→4/6）：
    # B(.5×5/6+.5×1−.02) > C(.5×4/6+.5×.25) > A(.5×5/6+.5×0−.04)
    by_id = {row["candidate_id"]: row for row in result["fine"]}
    assert by_id["a#00100"]["score"] == pytest.approx(
        0.5 * (5 / 6) + 0.5 * 1.0 - 0.02 * 1)
    assert by_id["a#11000"]["score"] == pytest.approx(
        0.5 * (5 / 6) + 0.5 * 0.0 - 0.02 * 2)
    assert result["finalists"][0] == "a#00100"   # v1 会选 a#11000
    assert result["budget"]["h2h_arm"] is True
    assert result["budget"]["n_h2h_candidates"] == 3
    assert result["budget"]["h2h_missing"] == []


def test_h2h_budget_truncation_annotated():
    # h2h 臂逐候选 30ms + 近零预算：部分候选截断 → h2h_missing 留痕，
    # 其 score 退化 v1 语义（seated−λ×mods），budget_exhausted=true
    winrates = {f"c{i}#10000": 0.6 for i in range(3)}
    candidates = [_candidate(f"c{i}#10000", "route:default", "10000")
                  for i in range(3)]
    result = evaluate_ablation_tree({
        "candidates": candidates, "games": _games(8),
        "fine_games": _games(4, prefix=5000),
        "evaluator": _fake_evaluator(winrates),
        "h2h_runner": _fake_h2h_runner({}, sleep_s=0.03),
        "tiers": {"coarse_games": 4, "fine_top_k": 3, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 0.05}})
    assert result["budget"]["budget_exhausted"] is True
    missing = result["budget"]["h2h_missing"]
    assert 0 < len(missing) < 3
    by_id = {row["candidate_id"]: row for row in result["fine"]}
    for cid in missing:
        assert by_id[cid]["h2h"] is None
        assert by_id[cid]["score"] == pytest.approx(
            by_id[cid]["winrate"] - 0.02 * by_id[cid]["enabled_modules"])


def test_coarse_rows_reuse_registered_and_equivalent():
    winrates = {"a#10000": 0.8, "a#00000": 0.5}
    h2h_rates = {"a#10000": 0.5, "a#00000": 0.5}
    candidates = [_candidate("a#10000", "route:default", "10000"),
                  _candidate("a#00000", "route:default", "00000")]
    base = evaluate_ablation_tree({
        "candidates": candidates, "games": _games(10),
        "evaluator": _fake_evaluator(winrates),
        "h2h_runner": _fake_h2h_runner(h2h_rates),
        "tiers": {"coarse_games": 10, "fine_top_k": 2, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    reused_rows = {row["candidate_id"]: row for row in base["coarse"]}
    calls = []
    result = evaluate_ablation_tree({
        "candidates": candidates, "games": _games(10),
        "fine_games": _games(6, prefix=4000),
        "coarse_rows": reused_rows,
        "coarse_source": "v1 coarse_table sha256=<test>",
        "evaluator": _fake_evaluator(winrates, calls),
        "h2h_runner": _fake_h2h_runner(h2h_rates),
        "tiers": {"coarse_games": 10, "fine_top_k": 2, "refinement": False,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    # 复用登记：粗筛零评估（只剩 6 局精评 seated 调用）
    assert result["budget"]["coarse_reused"] is True
    assert result["budget"]["coarse_source"] == \
        "v1 coarse_table sha256=<test>"
    assert calls and {n for _, n in calls} == {6}
    # 等价性：finalists 与粗筛序与全量重跑一致
    assert result["finalists"] == base["finalists"]
    assert [r["candidate_id"] for r in result["coarse"]] == \
        [r["candidate_id"] for r in base["coarse"]]
    assert result["subsample"] == base["subsample"]


def test_fine_top_k_cap_fail_closed():
    with pytest.raises(ValueError, match="帽"):
        evaluate_ablation_tree({
            "candidates": [_candidate("a#00000", "p", "00000")],
            "games": _games(4),
            "evaluator": _fake_evaluator({}),
            "tiers": {"coarse_games": 4,
                      "fine_top_k": FINE_TOP_K_CAP + 1}})


def test_determinism_with_h2h_arm():
    winrates = {"a#00000": 0.6, "a#10000": 0.55, "a#11000": 0.52}
    h2h_rates = {"a#00000": 0.25, "a#10000": 0.75, "a#11000": 0.5}
    candidates = [_candidate("a#00000", "route:default", "00000"),
                  _candidate("a#10000", "route:default", "10000"),
                  _candidate("a#11000", "route:default", "11000")]

    def run():
        return evaluate_ablation_tree({
            "candidates": candidates, "games": _games(10),
            "fine_games": _games(6, prefix=4000),
            "evaluator": _fake_evaluator(winrates),
            "h2h_runner": _fake_h2h_runner(h2h_rates),
            "tiers": {"coarse_games": 6, "fine_top_k": 3,
                      "refinement": True, "finalists_n": 2,
                      "wall_clock_budget_s": 60}})
    a, b = run(), run()
    assert a["finalists"] == b["finalists"]
    assert [r["candidate_id"] for r in a["fine"]] == \
        [r["candidate_id"] for r in b["fine"]]
    assert a["h2h_games"] == b["h2h_games"] == \
        [list(g) for g in DEFAULT_H2H_GAMES]
    assert a["fine"] == b["fine"]          # 含 h2h 行的整行一致（无墙钟）


def test_refinement_variant_gets_h2h_arm_too():
    winrates = {"a#10000": 0.8, "a#00000": 0.5}
    h2h_calls = []
    result = evaluate_ablation_tree({
        "candidates": [_candidate("a#10000", "route:default", "10000"),
                       _candidate("a#00000", "route:default", "00000")],
        "games": _games(8), "fine_games": _games(6, prefix=4000),
        "evaluator": _fake_evaluator(winrates),
        "h2h_runner": _fake_h2h_runner({"a#10000": 0.5}, h2h_calls),
        "tiers": {"coarse_games": 4, "fine_top_k": 2, "refinement": True,
                  "finalists_n": 2, "wall_clock_budget_s": 60}})
    refined = [row for row in result["refinement"]]
    assert len(refined) == 1
    assert refined[0]["h2h"] is not None
    assert any(cid.startswith("a#10000+") for cid, _ in h2h_calls)
