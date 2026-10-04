"""collect_gate_golden_files 真实测试：tmp 假树四类（含缺失）收集、逐件登记
{category, source_path, sha256, size, status}、缺失登记回填不中断、类别白名单
fail-closed、确定性（同树二跑 registry 逐字节一致）。"""

import hashlib
import json

import pytest

from package_minimal_repro_set.collect_gate_golden_files import (
    CATEGORY_ORDER,
    CATEGORY_SPEC,
    collect_gate_golden_files,
)


def _fake_campaign(tmp_path):
    """tmp 假战役树：四类源齐一含缺失（golden JSON 与灾难局回放不在机）。"""
    root = tmp_path / "camp"
    root.mkdir(parents=True)
    (root / "blueprint.md").write_text("bp", encoding="utf-8")
    golden = root / "software/exports/probes/planner_flagoff/golden_v138.json"
    golden.parent.mkdir(parents=True)          # 目录在、文件缺（本机现实：gitignored）
    replay = root / "references/data/online-replays/round23/episode-110634204-replay.json"
    replay.parent.mkdir(parents=True)          # 同上：目录在、回放缺
    twin_files = {
        "software/exports/twin/p1_fidelity_summary.md": "# twin\n",
        "software/exports/probes/twin_fidelity/fidelity_report.json":
            '{"schema": "twin-fidelity/1.0"}',
        "software/exports/replay_profiles/index.json": '{"profiles": []}',
        "software/exports/replay_profiles/exclusions.json": "[]",
    }
    for rel, text in twin_files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    seed_files = {
        "software/kgenv/bots/__init__.py": "ROSTER = ()\n",
        "software/kgenv/eval_contract.py": "DEVELOPMENT_SEEDS = frozenset(range(101, 105))\n",
        "software/kgenv/holdout_contract.py": "HOLDOUT_SEED_COUNT = 8\n",
    }
    for rel, text in seed_files.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def test_collect_all_categories_registers_available_and_missing(tmp_path):
    root = _fake_campaign(tmp_path)
    file_set, registry = collect_gate_golden_files(campaign_root=root)

    statuses = {(r["category"], r["status"]) for r in registry}
    # 四类全部入登记；golden/灾难局/replay-corpus 台账=missing，其余 collected
    assert ("flagoff_golden", "missing") in statuses
    assert ("disaster_replay", "missing") in statuses
    assert ("twin_fidelity_manifest", "collected") in statuses
    assert ("twin_fidelity_manifest", "missing") in statuses  # fidelity_report+corpus manifest
    assert ("opponent_seed_definitions", "collected") in statuses
    assert len(registry) == sum(len(CATEGORY_SPEC[c]["entries"]) for c in CATEGORY_ORDER)
    # file_set 只含 collected 件且逐件带四元登记
    assert all(e["status"] == "collected" for e in file_set)
    for entry in file_set:
        assert {"category", "source_path", "sha256", "size"} <= set(entry)


def test_collected_copies_and_sha_match_sources(tmp_path):
    root = _fake_campaign(tmp_path)
    file_set, _ = collect_gate_golden_files(campaign_root=root)

    twin = next(e for e in file_set
                if e["source_path"].endswith("p1_fidelity_summary.md"))
    dest = root / twin["dest_path"]
    assert dest.is_file()
    # dest_path 相对战役根：fn_work/minimal_repro_set/<category>/…（类别目录居中）
    parts = twin["dest_path"].split("/")
    assert parts[:2] == ["fn_work", "minimal_repro_set"]
    assert parts[2] == "twin_fidelity_manifest"
    raw = (root / twin["source_path"]).read_bytes()
    assert twin["sha256"] == hashlib.sha256(raw).hexdigest()
    assert twin["size"] == len(raw)
    assert dest.read_bytes() == raw                 # 物理复制逐字节一致
    # 子路径剥 software/ 前缀（防同名碰撞）
    assert "software/" not in twin["dest_path"].split("twin_fidelity_manifest/", 1)[1]


def test_missing_entries_carry_backfill_and_do_not_interrupt(tmp_path):
    root = _fake_campaign(tmp_path)
    file_set, registry = collect_gate_golden_files(campaign_root=root)

    missing = [r for r in registry if r["status"] == "missing"]
    assert {r["category"] for r in missing} == {
        "flagoff_golden", "disaster_replay", "twin_fidelity_manifest"}
    for entry in missing:
        assert entry["sha256"] is None and entry["size"] is None
        assert entry["dest_path"] is None
        assert "backfill" in entry and entry["backfill"]   # 回填办法非空
        assert "重跑" in entry["backfill"] or "回捞" in entry["backfill"]
    # 缺失不中断：twin 类其余件与种子类照常收集
    assert any(e["category"] == "twin_fidelity_manifest" for e in file_set)
    assert sum(1 for e in file_set if e["category"] == "opponent_seed_definitions") == 3


def test_backfill_recovers_after_materialization(tmp_path):
    """回填通道闭环：缺失件落位后重跑本函数即 collected（主力机语义本机模拟）。"""
    root = _fake_campaign(tmp_path)
    _, registry1 = collect_gate_golden_files(campaign_root=root)
    goldens = [r for r in registry1 if r["category"] == "flagoff_golden"]
    assert goldens and goldens[0]["status"] == "missing"

    (root / goldens[0]["source_path"]).write_text(
        json.dumps({"golden": True}), encoding="utf-8")
    file_set2, registry2 = collect_gate_golden_files(campaign_root=root)
    assert all(r["status"] == "collected" for r in registry2
               if r["category"] == "flagoff_golden")
    assert any(e["category"] == "flagoff_golden" for e in file_set2)


def test_unknown_category_fails_closed(tmp_path):
    root = _fake_campaign(tmp_path)
    with pytest.raises(ValueError, match="未知最小集类别"):
        collect_gate_golden_files(["flagoff_golden", "not_a_category"],
                                  campaign_root=root)


def test_category_subset_and_empty_list(tmp_path):
    root = _fake_campaign(tmp_path)
    file_set, registry = collect_gate_golden_files(["opponent_seed_definitions"],
                                                   campaign_root=root)
    assert {r["category"] for r in registry} == {"opponent_seed_definitions"}
    assert len(file_set) == 3
    empty_set, empty_registry = collect_gate_golden_files([], campaign_root=root)
    assert empty_set == [] and empty_registry == []


def test_deterministic_registry_ordering(tmp_path):
    root = _fake_campaign(tmp_path)
    _, registry1 = collect_gate_golden_files(campaign_root=root)
    _, registry2 = collect_gate_golden_files(campaign_root=root)
    assert registry1 == registry2                     # 固定声明序、无时钟字段
    assert [r["category"] for r in registry1][:1] == [CATEGORY_ORDER[0]]
