"""refresh_frozen_values 真实测试：白名单圈禁 + 双口径注记 + 越界拒绝。

对齐 fn_docs/responsibility.md migrate_snapshot_suite 块 refresh 节：
① refresh 只许动白名单文件/断言（tmp 副本 + 逐字节越界改动检测）；
② 每处更新留双口径注记（旧值/新值/原因=R2/R3 修复）且落进文件正文；
③ 影响清单外冻结值变动/越界文件/空授权 → fail-closed ValueError 零写入；
④ 受保护冻结字面量（旗关整局以外的白名单内跨口径锚）刷新后仍在场。
"""

import shutil
from pathlib import Path

import pytest

from migrate_snapshot_suite.refresh_frozen_values import (
    DEFAULT_IMPACT_LIST,
    SUITE_FILES,
    WHITELIST,
    check_protected_anchors,
    refresh_frozen_values,
)
from shared.discover_campaign_roots import discover_campaign_roots


@pytest.fixture(scope="module")
def source_suite():
    roots = discover_campaign_roots(start_path=Path(__file__))
    return roots["campaign_root"] / "snapshot_tests"


def _make_tmp_copy(source_suite, tmp_path):
    for name in SUITE_FILES:
        shutil.copyfile(source_suite / name, tmp_path / name)
    return tmp_path


def _snapshot_bytes(directory):
    return {name: (directory / name).read_bytes() for name in SUITE_FILES}


def test_refresh_touches_only_whitelisted_files(source_suite, tmp_path):
    """① 白名单圈禁：只有三件被改写，其余件（含 README/旗关整局/评级/
    契约/台账四测试文件与 conftest 原件）逐字节不变。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    before = _snapshot_bytes(work)
    changed, _annotations = refresh_frozen_values(DEFAULT_IMPACT_LIST, work)
    assert sorted(changed) == sorted(WHITELIST)
    after = _snapshot_bytes(work)
    for name in SUITE_FILES:
        if name in WHITELIST:
            assert after[name] != before[name], f"{name} 应被刷新"
        else:
            assert after[name] == before[name], f"越界改动: {name}"


def test_refresh_annotations_dual_caliber(source_suite, tmp_path):
    """② 双口径注记：注记与影响清单一一对应，键完整（旧值/新值/原因），
    且注记正文落入迁移副本（旧值/新值/原因三要素可见）。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    changed, annotations = refresh_frozen_values(DEFAULT_IMPACT_LIST, work)
    assert changed and len(annotations) == len(DEFAULT_IMPACT_LIST)
    for note in annotations:
        assert set(note) == {"kind", "file", "locator",
                             "old_value", "new_value", "reason"}
        assert note["kind"] in ("value", "xfail_convert")
        assert note["file"] in WHITELIST
        assert note["reason"] in ("R2", "R3")
        assert note["old_value"] and note["new_value"]
    # 注记正文落进文件（抽查三件各一处：R2 错位→seated、R3 35→65、K1）
    r2 = (work / "test_counterexample_r2.py").read_text(encoding="utf-8")
    assert ("旧值 [1570.0, 3000.0]" in r2
            and "新值 [3000.0, 1570.0]" in r2 and "R2 修复" in r2)
    planner = (work / "test_planner_select_characterization.py") \
        .read_text(encoding="utf-8")
    assert "旧值 35.0" in planner and "新值 65.0" in planner
    assert "旧值 1001.5" in planner and "新值 1003.0" in planner
    assert planner.count("双口径注记") >= 5


def test_refresh_rejects_out_of_whitelist_file(source_suite, tmp_path):
    """③a 影响清单含白名单外文件 → ValueError，且零写入（fail-closed）。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    before = _snapshot_bytes(work)
    bad = list(DEFAULT_IMPACT_LIST) + [{
        "file": "test_agent_characterization.py",
        "locator": "test_flagoff_final_rewards_frozen",
        "reason": "R2"}]
    with pytest.raises(ValueError, match="白名单"):
        refresh_frozen_values(bad, work)
    assert _snapshot_bytes(work) == before


def test_refresh_rejects_unauthorized_edit(source_suite, tmp_path):
    """③b 编辑表中存在、清单未授权（影响清单外冻结值变动）→ ValueError
    零写入。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    before = _snapshot_bytes(work)
    partial = [e for e in DEFAULT_IMPACT_LIST
               if e["locator"]
               != "test_aggregate_trimmed_mean_name_order_cut"]
    with pytest.raises(ValueError, match="影响清单外冻结值变动被拒"):
        refresh_frozen_values(partial, work)
    assert _snapshot_bytes(work) == before


def test_refresh_rejects_empty_authorization_entry(source_suite, tmp_path):
    """③c 清单项无对应修复点（空授权）→ ValueError 零写入。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    padded = list(DEFAULT_IMPACT_LIST) + [{
        "file": "test_counterexample_r3.py",
        "locator": "test_reference_implementation_sanity",
        "reason": "R3"}]
    with pytest.raises(ValueError, match="无对应修复点"):
        refresh_frozen_values(padded, work)


def test_refresh_protected_literals_survive(source_suite, tmp_path):
    """④ 受保护冻结字面量刷新后仍在场/旧字面量已退役：回放真值与错位
    负锚、反例输入构造、模块常量、worst_case/weighted/退化尺寸锚。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    refresh_frozen_values(DEFAULT_IMPACT_LIST, work)
    assert check_protected_anchors(work) == []
    planner = (work / "test_planner_select_characterization.py") \
        .read_text(encoding="utf-8")
    # 旧名字序断言已替换为值序新断言
    assert "assert aggregate_scores(CASE_A) == 35.0" not in planner
    assert "assert aggregate_scores(CASE_A) == 65.0" in planner
    # 迁移产物零字面战役路径（环境名 "kaggriculture" 是环境 id，不算）
    for name in WHITELIST:
        text = (work / name).read_text(encoding="utf-8")
        assert "workspace/" not in text and "autoC" not in text


def test_refresh_reapply_fails_closed_on_refreshed_copy(source_suite,
                                                        tmp_path):
    """幂等防御：对已刷新副本重复应用 → 锚不再唯一命中，ValueError。"""
    work = _make_tmp_copy(source_suite, tmp_path)
    refresh_frozen_values(DEFAULT_IMPACT_LIST, work)
    with pytest.raises(ValueError, match="锚文本命中 0 次"):
        refresh_frozen_values(DEFAULT_IMPACT_LIST, work)


def test_refresh_rejects_incomplete_copy(source_suite, tmp_path):
    """副本缺件 → ValueError（先复制九文件再刷新）。"""
    partial = tmp_path / "partial"
    partial.mkdir()
    shutil.copyfile(source_suite / "test_counterexample_r2.py",
                    partial / "test_counterexample_r2.py")
    with pytest.raises(ValueError, match="迁移副本缺件"):
        refresh_frozen_values(DEFAULT_IMPACT_LIST, partial)
