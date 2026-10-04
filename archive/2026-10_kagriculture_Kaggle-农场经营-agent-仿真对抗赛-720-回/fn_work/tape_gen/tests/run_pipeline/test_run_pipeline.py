"""run_pipeline 真实测试（R7：全管线编排 + 账本链哈希 + 双跑一致）。

stages 全注入（tmp 假件）：账本 T1-T4 五行、行哈希逐行咬合（prev→
line）、双跑逐字节一致、段序固定、产物落盘；非确定性段 fail-closed。
"""

import hashlib
import json

import pytest
from run_pipeline.run_pipeline import (
    STAGE_ORDER,
    _canonical,
    _sha256_text,
    run_pipeline,
)


def _fake_stages(tmp_path):
    calls = {"n": 0}

    def mine(p):
        return {"corpus_hash": "c" * 64, "store_sha256": "s" * 64,
                "summary": {"kept": 162, "games": 182},
                "paths": {"store": str(tmp_path / "store.jsonl")}}

    def library(p):
        assert p["store_path"].endswith("store.jsonl")
        return {"n_routes": 2, "routes_sha256": "r" * 64,
                "fidelity": {"all_ok": True},
                "fork_events": {"shared_prefix": 73},
                "store": {"sha256": "s" * 64},
                "paths": {"routes": str(tmp_path / "routes.json")}}

    def variants(p):
        return {"n_variants": 8, "n_rejected": 0,
                "variants_sha256": "v" * 64,
                "backbone_sha256": "b" * 64}

    def search(p):
        assert p["library_dir"]
        return {"space": {"base_space_size": 320},
                "split": {"split_sha256": "p" * 64},
                "evaluation": {"finalists": ["a", "b", "c"]},
                "selection": {"final": {
                    "candidate_id": "route:default#10000",
                    "selection_sha256": "f" * 64,
                    "holdout": {"winrate": 0.4706}}},
                "paths": {"output_dir": str(tmp_path / "search")}}

    report = tmp_path / "gate_report.json"
    report.write_text('{"canonical": true}\n', encoding="utf-8")

    def assemble(p):
        assert str(p["selection_path"]).endswith("final_selection.json")
        return {"package": {
            "products": {"main_py": {"sha256": "m" * 64, "bytes": 104998},
                         "submission_tar_gz": {"sha256": "t" * 64}},
            "selection": {"selection_sha256": "f" * 64}},
            "gates": {"paths": {"report": str(report)}},
            "grading": {"overall": "GATES_PASS"}}

    return {"mine_trajectories": mine, "build_route_library": library,
            "derive_market_variants": variants,
            "search_reflector_configs": search,
            "assemble_and_gate": assemble}


def _payload(tmp_path, stages, **over):
    payload = {"output_dir": str(tmp_path / "pipeline"),
               "stages": stages}
    payload.update(over)
    return payload


def test_ledger_stage_order_and_chain(tmp_path):
    result = run_pipeline(_payload(tmp_path, _fake_stages(tmp_path)))
    assert [line["stage"] for line in result["ledger"]] == \
        list(STAGE_ORDER)
    # 行哈希逐行咬合：line = sha256(canonical{stage,digest,prev} ∥ prev)
    prev = _sha256_text("tape_gen:genesis")
    for line in result["ledger"]:
        assert line["prev_sha256"] == prev
        expect = _sha256_text(_canonical(
            {"stage": line["stage"], "digest": line["digest"],
             "prev_sha256": prev}))
        assert line["line_sha256"] == expect
        prev = line["line_sha256"]
    assert result["chain_sha256"] == prev
    assert result["grading"] == "GATES_PASS"


def test_ledger_tamper_changes_chain(tmp_path):
    base = run_pipeline(_payload(tmp_path, _fake_stages(tmp_path)))
    first = dict(base["ledger"][0], digest=dict(
        base["ledger"][0]["digest"], kept_trajectories=999))
    expect = _sha256_text(_canonical(
        {"stage": first["stage"], "digest": first["digest"],
         "prev_sha256": first["prev_sha256"]}))
    # 篡改 digest 后行哈希必变，且后续行的 prev 咬合断裂
    assert expect != base["ledger"][0]["line_sha256"]
    second = base["ledger"][1]
    assert second["prev_sha256"] == base["ledger"][0]["line_sha256"]
    assert second["prev_sha256"] != expect


def test_products_written_and_double_run_identical(tmp_path):
    stages = _fake_stages(tmp_path)
    result = run_pipeline(_payload(tmp_path, stages, double_run=True))
    out = tmp_path / "pipeline"
    ledger_text = (out / "ledger.jsonl").read_text(encoding="utf-8")
    head = json.loads((out / "ledger_head.json").read_text(
        encoding="utf-8"))
    runtime = json.loads((out / "runtime_stats.json").read_text(
        encoding="utf-8"))
    assert head["chain_sha256"] == result["chain_sha256"]
    assert head["stage_order"] == list(STAGE_ORDER)
    assert head["grading"] == "GATES_PASS"
    assert runtime["double_run"] is True
    assert runtime["double_run_identical"] is True
    assert result["runtime"]["double_run_identical"] is True
    # 账本无墙钟字段
    assert "wall" not in ledger_text.lower()
    assert "generated" not in ledger_text.lower()
    # 行计数 = 行数
    assert head["n_lines"] == len(result["ledger"]) == 5


def test_double_run_mismatch_fail_closed(tmp_path):
    stages = _fake_stages(tmp_path)
    original = stages["mine_trajectories"]
    state = {"n": 0}

    def flaky(p):
        state["n"] += 1
        out = original(p)
        if state["n"] > 1:
            out = dict(out, corpus_hash="x" * 64)
        return out

    stages["mine_trajectories"] = flaky
    with pytest.raises(RuntimeError, match="double-run"):
        run_pipeline(_payload(tmp_path, stages, double_run=True))


def test_stage_exception_propagates(tmp_path):
    stages = _fake_stages(tmp_path)

    def boom(p):
        raise ValueError("trajectory store missing (fail-closed)")

    stages["build_route_library"] = boom
    with pytest.raises(ValueError, match="fail-closed"):
        run_pipeline(_payload(tmp_path, stages))


def test_gate_report_hash_in_chain(tmp_path):
    stages = _fake_stages(tmp_path)
    result = run_pipeline(_payload(tmp_path, stages))
    last = result["ledger"][-1]
    assert last["stage"] == "assemble_and_gate"
    expect = hashlib.sha256(
        (tmp_path / "gate_report.json").read_bytes()).hexdigest()
    assert last["digest"]["gate_report_sha256"] == expect
    assert last["digest"]["grading"] == "GATES_PASS"
    assert last["digest"]["package_main_sha256"] == "m" * 64


def test_search_digest_carries_selection_chain(tmp_path):
    stages = _fake_stages(tmp_path)
    result = run_pipeline(_payload(tmp_path, stages))
    search_line = result["ledger"][3]
    assert search_line["digest"]["selection_sha256"] == "f" * 64
    asm_line = result["ledger"][4]
    # T4 与 T3 的选择哈希跨段一致（链上对账）
    assert asm_line["digest"]["selection_sha256"] == \
        search_line["digest"]["selection_sha256"]
