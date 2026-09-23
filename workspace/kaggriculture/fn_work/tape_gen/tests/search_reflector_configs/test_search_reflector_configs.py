"""search_reflector_configs 真实测试（R4 L0 编排：空间→分离→树评估→
留出裁决→消融账本）。

tmp 伪造世界（库面+轨迹库+回放占位）+ 假评估器注入：验证编排次序、
账本 JSONL 完整性（逐行 content_sha256 自证）、产物落盘、留出裁决与
确定性。不触引擎/网络。
"""

import json

import pytest
from search_reflector_configs.search_reflector_configs import (
    search_reflector_configs,
)

STEP = {"farmer": ["PASS"], "hands": [], "market": []}


def _fake_world(tmp_path):
    library = tmp_path / "library"
    library.mkdir(parents=True)
    routes = {"default": [dict(STEP) for _ in range(4)],
              "fork_s73_e72": [dict(STEP) for _ in range(4)]}
    variants = {f"v{i}": [dict(STEP) for _ in range(4)] for i in range(3)}
    (library / "routes.json").write_text(json.dumps(routes),
                                         encoding="utf-8")
    (library / "market_variants.json").write_text(json.dumps(variants),
                                                  encoding="utf-8")

    replay_dir = tmp_path / "rounds" / "round27"
    replay_dir.mkdir(parents=True)
    lines = []
    for i in range(24):  # 24 对手各 1 局（>30% 留出下限可满足）
        eid = 2000 + i
        (replay_dir / f"episode-{eid}-replay.json").write_text("{}",
                                                               encoding="utf-8")
        lines.append(json.dumps({
            "episode_id": eid, "seat": i % 2, "team": f"Opp{i:03d}",
            "opponent": "renyxin", "result": "W", "final_margin": 1.0,
            "actions": [dict(STEP)]}))
    store = tmp_path / "trajectory_store.jsonl"
    store.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"library_dir": str(library), "store_path": str(store),
            "replay_dirs": [str(replay_dir)]}


def _piece_bias_evaluator(calls):
    """假评估器：胜率=f(件,模块数)——variant:v0 且模块多者略优，
    route:default 全 0.5 基线；确定性。"""
    def evaluator(candidate, games):
        calls.append(candidate["id"])
        n = len(games)
        if candidate["piece"] == "variant:v0":
            wr = 0.5 + 0.05 * candidate["enabled_modules"] / 5
        elif candidate["piece"] == "route:fork_s73_e72":
            wr = 0.55
        else:
            wr = 0.5
        wins = round(wr * n)
        rows = [{"episode_id": g["episode_id"], "opponent": g["opponent"],
                 "me_seat": g["me_seat"], "win": i < wins, "draw": False,
                 "margin": 10.0 if i < wins else -10.0,
                 "finals": [0.0, 0.0]} for i, g in enumerate(games)]
        return {"candidate_id": candidate["id"], "games": rows, "n": n,
                "wins": wins, "draws": 0, "losses": n - wins,
                "winrate": wins / n,
                "margin_mean": (2 * wins - n) * 10.0 / n}
    return evaluator


def _payload(tmp_path, evaluator):
    world = _fake_world(tmp_path)
    return {**world, "output_dir": str(tmp_path / "search"),
            "evaluator": evaluator, "lambda_sparse": 0.02,
            "min_holdout_games": 5,
            "tiers": {"coarse_games": 4, "fine_top_k": 3,
                      "refinement": True, "finalists_n": 2,
                      "wall_clock_budget_s": 300}}


def test_orchestration_artifacts_and_ledger(tmp_path):
    calls = []
    result = search_reflector_configs(_payload(tmp_path,
                                               _piece_bias_evaluator(calls)))
    out = tmp_path / "search"
    # 空间=5 件×32=160（伪造库面 2 路由+3 变体）
    assert result["space"]["base_space_size"] == 160
    # 分离：留出 ≥30% 对手且不相交
    proof = result["split"]["proof"]
    assert proof["intersection"] == []
    assert proof["holdout_opponent_fraction"] >= 0.30
    # 预算分级：粗筛全 160 候选 ×4 局；精评 top-3 全训练局
    assert result["evaluation"]["budget"]["n_coarse_candidates"] == 160
    assert result["evaluation"]["budget"]["n_coarse_games"] == 4
    assert result["evaluation"]["budget"]["n_fine_candidates"] == 3
    # 最终件只在留出集裁决（holdout 胜率在场）
    final = result["selection"]["final"]
    assert "holdout_winrate" in json.dumps(final["holdout"]) or \
        final["holdout"]["winrate"] >= 0.0
    assert result["selection"]["proof"]["decided_on"] == "holdout_only"
    # 产物落盘
    for name in ("config_space.json", "config_space.md",
                 "split_train_holdout.json", "coarse_table.json",
                 "fine_table.json", "ablation_ledger.jsonl",
                 "runtime_stats.json", "final_selection.json",
                 "holdout_margin_table.csv"):
        assert (out / name).is_file(), name
    # 账本：JSONL 逐行可解析、record 面齐全、content_sha256 自证
    records = [json.loads(line) for line in
               (out / "ablation_ledger.jsonl").read_text(
                   encoding="utf-8").splitlines() if line]
    kinds = {r["record"] for r in records}
    assert {"config_space", "split_train_holdout", "ablation_tiers",
            "coarse_eval", "fine_eval", "holdout_eval",
            "final_selection"} <= kinds
    import hashlib
    for record in records:
        body = {k: v for k, v in record.items()
                if k != "content_sha256"}
        digest = hashlib.sha256(json.dumps(
            body, ensure_ascii=False, sort_keys=True,
            separators=(",", ":")).encode("utf-8")).hexdigest()
        assert digest == record["content_sha256"]
    # runtime 实测字段（墙钟登记）
    runtime = json.loads((out / "runtime_stats.json").read_text(
        encoding="utf-8"))
    assert runtime["wall_clock_s"] >= 0.0
    assert "budget_exhausted" in runtime


def test_orchestration_deterministic_tables(tmp_path):
    a = search_reflector_configs(_payload(tmp_path / "a",
                                          _piece_bias_evaluator([])))
    b = search_reflector_configs(_payload(tmp_path / "b",
                                          _piece_bias_evaluator([])))
    assert a["selection"]["final"]["candidate_id"] == \
        b["selection"]["final"]["candidate_id"]
    ledger_a = (tmp_path / "a" / "search" / "ablation_ledger.jsonl"
                ).read_text(encoding="utf-8")
    ledger_b = (tmp_path / "b" / "search" / "ablation_ledger.jsonl"
                ).read_text(encoding="utf-8")
    # 归一化 tmp 绝对路径（分离账本行含 replay_path；真实管线同机同径，
    # 双跑逐字节一致的判据不受影响）
    def norm(text):
        return text.replace(str(tmp_path / "a"), "<A>") \
                   .replace(str(tmp_path / "b"), "<A>")
    assert norm(ledger_a) == norm(ledger_b)  # 账本逐字节一致（无墙钟）


def test_orchestration_budget_exhaustion_zero_eval_fail_closed(tmp_path):
    # 零预算：零评估即 fail-closed（无已评最优可取，不得静默产出空选择）
    world = _fake_world(tmp_path)
    with pytest.raises(ValueError, match="预算耗尽"):
        search_reflector_configs({
            **world, "output_dir": str(tmp_path / "search"),
            "evaluator": _piece_bias_evaluator([]), "lambda_sparse": 0.02,
            "min_holdout_games": 5,
            "tiers": {"coarse_games": 2, "fine_top_k": 2,
                      "refinement": False, "finalists_n": 2,
                      "wall_clock_budget_s": 0.0}})


def test_orchestration_fail_closed_no_holdout(tmp_path):
    # 2 对手 → 留出 1 局 < min_holdout_games → fail-closed 上抛
    world = _fake_world(tmp_path)
    store = tmp_path / "tiny_store.jsonl"
    lines = []
    replay_dir = tmp_path / "rounds" / "round27"
    for i in range(2):
        eid = 9000 + i
        (replay_dir / f"episode-{eid}-replay.json").write_text("{}",
                                                               encoding="utf-8")
        lines.append(json.dumps({
            "episode_id": eid, "seat": 0, "team": f"Only{i}",
            "opponent": "renyxin", "result": "W", "final_margin": 1.0,
            "actions": [dict(STEP)]}))
    store.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="fail-closed"):
        search_reflector_configs({
            "library_dir": world["library_dir"], "store_path": str(store),
            "replay_dirs": [str(replay_dir)],
            "output_dir": str(tmp_path / "out"),
            "evaluator": _piece_bias_evaluator([]),
            "tiers": {"coarse_games": 2, "wall_clock_budget_s": 60}})
