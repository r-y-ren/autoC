"""retire_codemap_with_errata 镜像测试：勘误记录 schema+退役标记（产物仅落 tmp）。"""

import pytest

from sync_documentation.retire_codemap_with_errata import (
    VERIFIED_ERRATA,
    retire_codemap_with_errata,
)


def test_default_four_errata_written(tmp_path):
    result = retire_codemap_with_errata(doc_fixes_root=tmp_path)
    doc = (tmp_path / "codemap_errata.md").read_text(encoding="utf-8")
    assert result["errata_count"] == 4
    assert result["errata_ids"] == ["E1", "E2", "E3", "E4"]
    # 4 勘误逐条四要素（原文/实况/证据/修正口径）
    for e in VERIFIED_ERRATA:
        assert f"### {e['id']}（CODEMAP L{e['codemap_line']}，主题: {e['subject']}）" in doc
        assert e["reality"][:40] in doc
        assert e["correction"][:30] in doc
    # 退役标记：时点+替代面+清单漂移附注
    assert "## 退役标记" in doc
    assert "fn-close" in doc
    assert "responsibility.md" in doc
    assert "包 docstring" in doc
    assert result["retire_when"].startswith("战后 fn-close")


def test_errata_content_matches_verified_reality():
    # 内建勘误与实测事实绑定（E1 路径损坏/E2 零消费/E3 计数 51/E4 两套）
    by_id = {e["id"]: e for e in VERIFIED_ERRATA}
    assert "路径损坏" in by_id["E1"]["reality"]
    assert "src/market.py 与 scripts/ 零消费" in by_id["E2"]["reality"]
    assert "51" in by_id["E3"]["reality"]
    assert "两套" in by_id["E4"]["reality"]


def test_injected_errata_list_honored(tmp_path):
    custom = [{
        "id": "EX", "codemap_line": 1, "subject": "demo",
        "claim": "原文 A", "reality": "实况 B", "evidence": "证据 C",
        "correction": "口径 D",
    }]
    result = retire_codemap_with_errata(custom, doc_fixes_root=tmp_path)
    doc = (tmp_path / "codemap_errata.md").read_text(encoding="utf-8")
    assert result["errata_count"] == 1 and result["errata_ids"] == ["EX"]
    assert "实况 B" in doc and "口径 D" in doc
    assert "E1" not in doc


def test_fail_closed_empty_or_malformed(tmp_path):
    with pytest.raises(ValueError, match="空"):
        retire_codemap_with_errata([], doc_fixes_root=tmp_path)
    with pytest.raises(ValueError, match="必备键"):
        retire_codemap_with_errata([{"id": "E1"}], doc_fixes_root=tmp_path)
    assert not (tmp_path / "codemap_errata.md").exists()
