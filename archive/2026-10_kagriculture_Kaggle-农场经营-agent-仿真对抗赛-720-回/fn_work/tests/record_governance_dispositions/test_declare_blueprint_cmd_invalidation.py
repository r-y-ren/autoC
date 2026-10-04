"""declare_blueprint_cmd_invalidation 真实测试：失效判据 fail-closed、静默事实与处置渲染、确定性字节。"""

from pathlib import Path

import pytest

from record_governance_dispositions.declare_blueprint_cmd_invalidation import (
    DEFAULT_INVALID_CMDS,
    DEFAULT_SILENT_FACT,
    DISPOSITION,
    declare_blueprint_cmd_invalidation,
    render_invalidation_declaration,
)

_CMDS = [
    {
        "id": "doc-compile",
        "cmd": "typst compile --root C C/docs/report.typ C/docs/report.pdf",
        "missing_path": "docs/report.typ",
        "reason": "从未入库",
    },
    {
        "id": "doc-consistency",
        "cmd": "python C/docs/check_report_metrics.py",
        "missing_path": "docs/check_report_metrics.py",
    },
]


def test_declares_invalidation_with_silent_fact(tmp_path):
    out = tmp_path / "out" / "blueprint_cmd_invalidation.md"
    verdict = declare_blueprint_cmd_invalidation(_CMDS, campaign_root=tmp_path, output_path=out)
    assert verdict["output_path"] == out and out.is_file()
    text = out.read_text(encoding="utf-8")
    assert "doc-compile" in text and "doc-consistency" in text
    assert "docs/report.typ" in text and "docs/check_report_metrics.py" in text
    assert "不存在" in text  # 判定列
    assert "run-29" in text and "2026-09-01" in text  # 静默事实
    assert "scoped" in text and "静默旁路" in text
    assert "/attack" in text  # 处置=战后修订
    assert [e["id"] for e in verdict["invalidated"]] == ["doc-compile", "doc-consistency"]


def test_existing_target_rejects_declaration(tmp_path):
    # 失效判据与事实不符：目标文件实际存在即拒绝
    victim = tmp_path / "docs" / "report.typ"
    victim.parent.mkdir()
    victim.write_text("// exists", encoding="utf-8")
    with pytest.raises(ValueError, match="不得为其留失效声明"):
        declare_blueprint_cmd_invalidation(
            _CMDS, campaign_root=tmp_path, output_path=tmp_path / "x.md"
        )
    # 缺键清单同样 fail-closed
    with pytest.raises(ValueError, match="缺失键"):
        declare_blueprint_cmd_invalidation(
            [{"id": "x", "cmd": "y"}], campaign_root=tmp_path, output_path=tmp_path / "x.md"
        )
    with pytest.raises(ValueError, match="非空 list"):
        declare_blueprint_cmd_invalidation([], campaign_root=tmp_path, output_path=tmp_path / "x.md")


def test_default_constants_quote_blueprint_facts():
    assert [c["id"] for c in DEFAULT_INVALID_CMDS] == ["doc-compile", "doc-consistency"]
    assert all(not c["missing_path"].startswith("/") for c in DEFAULT_INVALID_CMDS)
    assert DEFAULT_SILENT_FACT["last_full_touch"]["run"] == "acceptance/run-29"
    assert DEFAULT_SILENT_FACT["post_runs"] and all(
        not r["contains_doc_cmds"] for r in DEFAULT_SILENT_FACT["post_runs"]
    )
    assert "/attack" in DISPOSITION


def test_deterministic_render(tmp_path):
    text1 = render_invalidation_declaration(_CMDS, DEFAULT_SILENT_FACT)
    text2 = render_invalidation_declaration(_CMDS, DEFAULT_SILENT_FACT)
    assert text1 == text2
