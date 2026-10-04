"""codify_probes_policy 镜像测试：策略文档+6 份摘要一致性核对（注入 probes_state，产物仅落 tmp）。"""

import pytest
from conftest import PROBES_STATE

from sync_documentation.codify_probes_policy import (
    POLICY_RULES,
    ProbesPolicyViolation,
    codify_probes_policy,
)


def test_policy_doc_and_all_tracked_check(tmp_path):
    path, report = codify_probes_policy(PROBES_STATE, doc_fixes_root=tmp_path)
    doc = (tmp_path / "probes_policy.md").read_text(encoding="utf-8")
    assert path.endswith("probes_policy.md")
    # 策略规则显式化
    for rule in POLICY_RULES:
        assert rule[:2] in doc  # "P1"/"P2"/"P3" 编号+正文前缀
    assert "结论 .md 全入库" in doc and "数据中间物 gitignore" in doc
    # 6 份摘要核对表全入库
    assert report["summary_count"] == 6
    assert report["summary_check"] == "all_tracked"
    for s in PROBES_STATE["summaries"]:
        assert s["relpath"] in doc
    assert "twin_fidelity/engine_cache" in doc  # 数据中间物面


def test_rule_gap_listed_with_postwar_action(tmp_path):
    _, report = codify_probes_policy(PROBES_STATE, doc_fixes_root=tmp_path)
    doc = (tmp_path / "probes_policy.md").read_text(encoding="utf-8")
    # 规则面缺口（新 .md 会被忽略）→ 不一致清单+postwar_action，如实列出
    assert len(report["inconsistencies"]) == 1
    assert "check-ignore" in report["inconsistencies"][0]
    assert len(report["postwar_actions"]) == 1
    assert report["postwar_actions"][0].startswith("postwar_action")
    assert "不一致清单" in doc and "战后动作" in doc
    assert "git add -f" in doc


def test_consistent_state_no_inconsistency(tmp_path):
    state = dict(PROBES_STATE)
    state["rule_ignores_new_summary_md"] = False
    _, report = codify_probes_policy(state, doc_fixes_root=tmp_path)
    doc = (tmp_path / "probes_policy.md").read_text(encoding="utf-8")
    assert report["inconsistencies"] == []
    assert "（空——现存态与规则面均一致）" in doc


def test_fail_closed_untracked_summary(tmp_path):
    state = dict(PROBES_STATE)
    state["summaries"] = list(state["summaries"])
    state["summaries"][0] = dict(state["summaries"][0], tracked=False)
    with pytest.raises(ProbesPolicyViolation, match="P1 违规"):
        codify_probes_policy(state, doc_fixes_root=tmp_path)
    assert not (tmp_path / "probes_policy.md").exists()


def test_fail_closed_bad_state(tmp_path):
    with pytest.raises(ValueError, match="必备键"):
        codify_probes_policy({"summaries": []}, doc_fixes_root=tmp_path)
    with pytest.raises(ValueError, match="为空"):
        codify_probes_policy({"summaries": [], "rule_ignores_new_summary_md": False},
                             doc_fixes_root=tmp_path)
