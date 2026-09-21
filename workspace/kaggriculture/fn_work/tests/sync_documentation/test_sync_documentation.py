"""sync_documentation 顶层镜像测试：三叶编排+gap_table §一 8 项对账（tmp 假树全注入，不触真 doc_fixes）。"""

import pytest
from conftest import FN_DOCS_README, PROBES_STATE, build_fake_campaign

from sync_documentation.sync_documentation import (
    GAP_TABLE_ITEMS,
    ReconciliationError,
    reconcile_gap_table,
    sync_documentation,
)


@pytest.fixture()
def tree(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    return campaign, tmp_path / "doc_fixes"


def test_orchestration_pass_and_artifacts(tree, capsys):
    campaign, fixes = tree
    verdict = sync_documentation(campaign_root=campaign, doc_fixes_root=fixes,
                                 probes_state=PROBES_STATE)
    assert verdict["passed"] is True
    # 三叶产物齐（修正副本+注册/勘误/策略/收口报告）
    names = {p.name for p in fixes.rglob("*") if p.is_file()}
    assert {"README.md", "diff_registry.json", "codemap_errata.md",
            "probes_policy.md", "sync_report.md"} <= names
    assert len([n for n in names if n.endswith(".md") and n[0].isdigit()]) == 6
    assert verdict["leaves"]["fix_bc_track_records"]["diff_count"] == 9
    assert verdict["leaves"]["retire_codemap_with_errata"]["errata_count"] == 4
    assert verdict["leaves"]["codify_probes_policy"]["summary_count"] == 6
    # 对账 8 项全过+口径表述
    assert len(verdict["reconciliation"]["items"]) == 8
    assert verdict["reconciliation"]["criteria"].startswith("修正副本覆盖")
    # 收口报告 PASS 横幅+8 项表
    report = (fixes / "sync_report.md").read_text(encoding="utf-8")
    assert "PASS（8/8 清零）" in report
    assert "| 8 |" in report and "CODEMAP" in report  # #8（CODEMAP 面）行在表
    assert "## 裁决: PASS" in report
    # 战后动作（bc diff 套用/CODEMAP 退役/probes 白名单）
    joined = "\n".join(verdict["postwar_actions"])
    assert "diff_registry" in joined and "fn-close" in joined and "!**/*.md" in joined
    # 实跑播报含 8 项对账行与裁决行
    out = capsys.readouterr().out
    assert out.count("对账 #") == 8
    assert "裁决: PASS (8/8)" in out


def test_reconciliation_fail_closes_and_reports(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    # 破坏 #6 锚点：fn_docs README 抽走『席位错位』
    (campaign / "fn_docs/README.md").write_text(
        FN_DOCS_README.replace("席位错位", "口X错位"), encoding="utf-8")
    fixes = tmp_path / "doc_fixes"
    with pytest.raises(ReconciliationError, match="6"):
        sync_documentation(campaign_root=campaign, doc_fixes_root=fixes,
                           probes_state=PROBES_STATE)
    # 报告先行落盘，FAIL 如实
    report = (fixes / "sync_report.md").read_text(encoding="utf-8")
    assert "FAIL" in report and "✗" in report


def test_reconcile_pure_function_shape(tree):
    campaign, fixes = tree
    sync_documentation(campaign_root=campaign, doc_fixes_root=fixes,
                       probes_state=PROBES_STATE)
    recon = reconcile_gap_table(campaign, fixes)
    assert [i["id"] for i in recon["items"]] == [g["id"] for g in GAP_TABLE_ITEMS] == list(range(1, 9))
    # 空锚面 → 对应项全红
    empty = reconcile_gap_table(campaign, fixes.parent / "nowhere")
    assert empty["passed"] is False
    assert all(not i["passed"] for i in empty["items"] if i["id"] == 8)


def test_old_tree_untouched_by_orchestration(tree):
    campaign, fixes = tree
    readme = campaign / "software/bc_track/README.md"
    before = readme.read_text(encoding="utf-8")
    sync_documentation(campaign_root=campaign, doc_fixes_root=fixes,
                       probes_state=PROBES_STATE)
    assert readme.read_text(encoding="utf-8") == before
