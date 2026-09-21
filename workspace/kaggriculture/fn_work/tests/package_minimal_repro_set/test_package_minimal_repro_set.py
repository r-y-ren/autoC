"""package_minimal_repro_set 真实测试：顶层编排——tmp 假战役树实跑三叶+MANIFEST
落盘+裁决（ok/complete 分离、缺失降 complete 不降 ok）、预算超标 fail-closed
（不截断、manifest 记 violations）、注入桩编排序、manifest 确定性。"""

import json

import pytest

from package_minimal_repro_set.collect_gate_golden_files import (
    collect_gate_golden_files,
)
from package_minimal_repro_set.enforce_size_budget import (
    SizeBudgetExceeded,
    enforce_size_budget,
)
from package_minimal_repro_set.package_minimal_repro_set import (
    MANIFEST_SCHEMA,
    package_minimal_repro_set,
)


def _fake_campaign(tmp_path):
    """tmp 假战役树：四类源齐一含缺失（与 collect 镜像测试同构，本地复制免跨包导入）。"""
    root = tmp_path / "camp"
    root.mkdir(parents=True)
    (root / "blueprint.md").write_text("bp", encoding="utf-8")
    golden = root / "software/exports/probes/planner_flagoff/golden_v138.json"
    golden.parent.mkdir(parents=True)          # 目录在、文件缺（本机现实：gitignored）
    replay = root / "references/data/online-replays/round23/episode-110634204-replay.json"
    replay.parent.mkdir(parents=True)
    twin_files = {
        "software/exports/twin/p1_fidelity_summary.md": "# twin\n",
        "software/exports/probes/twin_fidelity/fidelity_report.json":
            '{"schema": "twin-fidelity/1.0"}',
        "software/exports/replay_profiles/index.json": '{"profiles": []}',
        "software/exports/replay_profiles/exclusions.json": "[]",
    }
    seed_files = {
        "software/kgenv/bots/__init__.py": "ROSTER = ()\n",
        "software/kgenv/eval_contract.py": "DEVELOPMENT_SEEDS = frozenset(range(101, 105))\n",
        "software/kgenv/holdout_contract.py": "HOLDOUT_SEED_COUNT = 8\n",
    }
    for rel, text in {**twin_files, **seed_files}.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def test_orchestrates_real_leaves_on_fake_tree(tmp_path):
    root = _fake_campaign(tmp_path)
    verdict = package_minimal_repro_set(campaign_root=root)

    # 本机现实：golden/灾难局/语料台账缺失 → complete=false 但机制 ok=true
    assert verdict["ok"] is True
    assert verdict["complete"] is False
    assert verdict["counts"]["collected"] == 7        # twin 4 + 种子 3
    assert verdict["counts"]["missing"] == 3          # golden+灾难局+corpus manifest
    assert verdict["checks"]["size_budget"]["ok"] is True

    # MANIFEST 落盘且自洽（schema/registry/预算定桩）
    manifest = json.loads(
        (root / "fn_work/minimal_repro_set/MANIFEST.json").read_text(encoding="utf-8"))
    assert manifest["schema"] == MANIFEST_SCHEMA
    assert manifest["verdict"]["ok"] is True and manifest["verdict"]["complete"] is False
    assert len(manifest["registry"]) == 10
    assert manifest["budget"]["per_file_max_bytes"] == 2 * 1024 * 1024
    # 声明落盘且 missing 件带补齐通道
    dep = (root / "fn_work/minimal_repro_set/LOCAL_CORPUS_DEPENDENCIES.md")
    dep_text = dep.read_text(encoding="utf-8")
    assert "golden_v138.json" in dep_text and "重跑" in dep_text
    assert verdict["declaration"]["written"] is True
    # collected 件物理到位
    dest_root = root / "fn_work/minimal_repro_set"
    copied = [p for p in dest_root.rglob("*") if p.is_file()
              and p.name not in ("MANIFEST.json", "LOCAL_CORPUS_DEPENDENCIES.md")]
    assert len(copied) == 7


def test_budget_violation_fails_closed_without_truncation(tmp_path):
    root = _fake_campaign(tmp_path)

    def exploding_checker(file_set, budget):
        raise SizeBudgetExceeded([{
            "kind": "per_file", "source_path": file_set[0]["source_path"],
            "size": file_set[0]["size"], "limit": 1}])

    verdict = package_minimal_repro_set(campaign_root=root,
                                        budget_checker=exploding_checker)
    assert verdict["ok"] is False                      # 超预算即失败
    assert verdict["checks"]["size_budget"]["ok"] is False
    assert verdict["checks"]["size_budget"]["violations"][0]["source_path"].endswith(
        ".md")
    # 不静默截断：7 件照常复制落位，manifest 登记 violations 与失败裁决
    manifest = json.loads((root / "fn_work/minimal_repro_set/MANIFEST.json")
                          .read_text(encoding="utf-8"))
    assert manifest["verdict"]["ok"] is False
    assert manifest["verdict"]["checks"]["size_budget"]["violations"]
    dest_root = root / "fn_work/minimal_repro_set"
    copied = [p for p in dest_root.rglob("*") if p.is_file()
              and p.name not in ("MANIFEST.json", "LOCAL_CORPUS_DEPENDENCIES.md")]
    assert len(copied) == 7


def test_injected_stub_order_and_wiring(tmp_path):
    calls = []

    def collector(category_list, *, campaign_root=None, dest_dir=None):
        calls.append("collect")
        file_set = [{"category": "opponent_seed_definitions",
                     "source_path": "software/kgenv/eval_contract.py",
                     "dest_path": "fn_work/minimal_repro_set/opponent_seed_definitions/kgenv/eval_contract.py",
                     "sha256": "a" * 64, "size": 10, "status": "collected",
                     "note": "", "backfill": ""}]
        registry = list(file_set)
        (dest_dir / "opponent_seed_definitions").mkdir(parents=True, exist_ok=True)
        return file_set, registry

    def budget_checker(file_set, budget):
        calls.append("budget")
        return enforce_size_budget(file_set, budget)

    def declarer(dependency_scan, *, campaign_root=None, output_path=None, **kw):
        calls.append("declare")
        assert "missing_files" in dependency_scan   # registry missing 件传入声明
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text("dep", encoding="utf-8")
        return {"output_path": str(output_path), "written": True, "document": "dep",
                "conclusions": [], "missing_files": dependency_scan["missing_files"],
                "skip_items": [], "environmental_bullets": [], "sources": []}

    verdict = package_minimal_repro_set(
        campaign_root=tmp_path, output_root=tmp_path / "out",
        collector=collector, budget_checker=budget_checker, dependency_declarer=declarer)
    assert calls == ["collect", "budget", "declare"]  # 编排序
    assert verdict["ok"] is True and verdict["complete"] is True  # 注入集无缺失
    assert (tmp_path / "out/MANIFEST.json").is_file()


def test_category_subset_and_unknown_propagates(tmp_path):
    root = _fake_campaign(tmp_path)
    verdict = package_minimal_repro_set(["opponent_seed_definitions"],
                                        campaign_root=root)
    assert verdict["counts"]["collected"] == 3
    assert verdict["counts"]["missing"] == 0
    assert verdict["complete"] is True
    with pytest.raises(ValueError, match="未知最小集类别"):
        package_minimal_repro_set(["bogus"], campaign_root=root)


def test_manifest_deterministic_byte_identical(tmp_path):
    root = _fake_campaign(tmp_path)
    package_minimal_repro_set(campaign_root=root)
    first = (root / "fn_work/minimal_repro_set/MANIFEST.json").read_bytes()
    package_minimal_repro_set(campaign_root=root)     # 二跑覆盖
    second = (root / "fn_work/minimal_repro_set/MANIFEST.json").read_bytes()
    assert first == second                            # 无时钟字段，逐字节一致


def test_real_leaf_importable_and_stub_replaced():
    """旧桩 NotImplementedError 标记已被真实实现取代（占位改真实）。"""
    import inspect
    from package_minimal_repro_set.package_minimal_repro_set import (
        package_minimal_repro_set as fn,
    )
    assert "NotImplementedError" not in inspect.getsource(fn)
    assert collect_gate_golden_files is not None
