"""fix_bc_track_records 镜像测试：tmp 假树上验证修正副本生成+diff 注册（旧树冻结零改动）。"""

import json

import pytest
from conftest import JOURNAL_ROWS, TICKET_NAMES, build_fake_campaign

from sync_documentation.fix_bc_track_records import DocFixError, fix_bc_track_records


def ticket_name(tid: str) -> str:
    return f"{tid}-{TICKET_NAMES[tid]}.md"


@pytest.fixture()
def tree(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    return campaign, tmp_path / "doc_fixes"


def test_corrected_readme_three_diffs(tree):
    campaign, fixes = tree
    result = fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=fixes)
    copy = (fixes / "bc_track" / "README.md").read_text(encoding="utf-8")
    assert "cd workspace/kaggriculture/software" in copy
    assert "kaggressure" not in copy
    assert "不改 src/、planner/" in copy
    assert "2026-09-21 正式裁决=弃牌收刀 379b41e" in copy
    assert result["readme_diffs"] == 3 and result["ticket_diffs"] == 6
    assert result["diff_count"] == 9


def test_ticket_status_copies_align_with_journal(tree):
    campaign, fixes = tree
    fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=fixes)
    issues = fixes / "bc_track" / "issues"
    t03 = (issues / ticket_name("03")).read_text(encoding="utf-8")
    assert "closed-done（2026-09-21 正式裁决=弃牌收刀，commit 379b41e" in t03
    assert "M1 结论正式勘误置顶" in t03
    t08 = (issues / ticket_name("08")).read_text(encoding="utf-8")
    assert "closed（2026-09-21 已关账：03 弃牌直接触发" in t08
    assert "票 08 关账" in t08
    for tid in ("04", "05", "06", "07"):
        text = (issues / ticket_name(tid)).read_text(encoding="utf-8")
        assert "closed-not-triggered（2026-09-21" in text
        assert "JOURNAL 收口行⑤" in text
    t06 = (issues / ticket_name("06")).read_text(encoding="utf-8")
    assert "GPU 未租用零成本" in t06
    t07 = (issues / ticket_name("07")).read_text(encoding="utf-8")
    assert "永久关闭" in t07
    # 票面正文零改动（仅 Status 行被替换）
    src03 = (campaign / "software/bc_track/issues/03-iterate-best.md").read_text(encoding="utf-8")
    assert "**What to build:** 假票面。" in src03


def test_registry_postwar_shape_and_ledger_basis(tree):
    campaign, fixes = tree
    result = fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=fixes)
    reg = json.loads((fixes / "bc_track" / "diff_registry.json").read_text(encoding="utf-8"))
    assert reg["frozen_tree"] is True
    assert reg["postwar_execution"]["registry_only"] is True
    assert len(reg["postwar_execution"]["steps"]) >= 3
    assert reg["ledger_basis"]["formal_row_commit"] == "379b41e"
    assert reg["ledger_basis"]["formal_row_date"] == "2026-09-21"
    assert len(reg["entries"]) == 9
    for e in reg["entries"]:
        assert set(e) >= {"file", "copy", "line", "old", "new", "reason", "evidence"}
    # 01/02 出范围披露
    assert any("01/02" in n for n in reg["out_of_scope_notes"])
    # 行号按旧树原文实算（README 路径拼写在 L9：0 起 shebang 无——按内容行计数）
    readme_entry = next(e for e in reg["entries"] if e["file"].endswith("bc_track/README.md")
                        and "kaggressure" in e["old"])
    assert readme_entry["line"] == 9


def test_journal_list_input_mode(tree):
    campaign, fixes = tree
    result = fix_bc_track_records(list(JOURNAL_ROWS), campaign_root=campaign,
                                  doc_fixes_root=fixes)
    assert result["ledger"]["commit"] == "379b41e"
    assert (fixes / "bc_track" / "README.md").is_file()


def test_old_tree_frozen_zero_byte_change(tree):
    campaign, fixes = tree
    before = (campaign / "software/bc_track/README.md").read_text(encoding="utf-8")
    fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=fixes)
    after = (campaign / "software/bc_track/README.md").read_text(encoding="utf-8")
    assert before == after and "kaggressure" in after


def test_fail_closed_no_journal_closeout_row(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    (campaign / "JOURNAL.md").write_text(
        "| 日期 | 阶段 | 内容 |\n|---|---|---|\n| 2026-09-21 | deliver | 无关行 |\n",
        encoding="utf-8")
    with pytest.raises(DocFixError, match="BC 收口行"):
        fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=tmp_path / "f")


def test_fail_closed_readme_anchor_mismatch(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    (campaign / "software/bc_track/README.md").write_text(
        "# 无锚点 README\n", encoding="utf-8")
    with pytest.raises(DocFixError, match="锚点失配"):
        fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=tmp_path / "f")


def test_fail_closed_ticket_missing_or_statusless(tmp_path):
    campaign = build_fake_campaign(tmp_path)
    (campaign / "software/bc_track/issues" / ticket_name("08")).unlink()
    with pytest.raises(DocFixError, match="票面不齐"):
        fix_bc_track_records(None, campaign_root=campaign, doc_fixes_root=tmp_path / "f")
    # Status 行缺失
    campaign2 = build_fake_campaign(tmp_path)
    (campaign2 / "software/bc_track/issues" / ticket_name("05")).write_text(
        "# 05 无状态行\n", encoding="utf-8")
    with pytest.raises(DocFixError, match="Status"):
        fix_bc_track_records(None, campaign_root=campaign2, doc_fixes_root=tmp_path / "f2")
