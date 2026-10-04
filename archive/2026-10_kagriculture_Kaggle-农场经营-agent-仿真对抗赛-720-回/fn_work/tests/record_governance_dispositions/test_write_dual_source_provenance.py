"""write_dual_source_provenance 真实测试：双源渲染、证据门、单源断言扫描（tmp 战役根）、确定性字节。"""

from pathlib import Path

import pytest

from record_governance_dispositions.write_dual_source_provenance import (
    DEFAULT_RECORD_FILES,
    ONLINE_REF_RULE,
    SOURCE_A_MARKERS,
    SOURCE_B_MARKERS,
    render_provenance_record,
    scan_single_source_assertions,
    write_dual_source_provenance,
)

_EVIDENCE = {
    "artifact_sha256": "dadee25a9840313218384208c53b2c4752f82c3209cc654632e0b96c65e2664a",
    "artifact_bytes": 107008,
    "online_ref": 56400478,
    "original_attribution": "两账号间未定",
    "sources": [
        {
            "key": "A",
            "account": "kaitofukami",
            "notebook": "40/40 Early Floor | 39/46 Top-10 | v48 Fast Routes",
            "acquired_date": "2026-08-31",
            "channel": "kaggle kernels pull（首拉）",
            "artifact_sha256_evidence": "dadee25a…（与 notebook §7 公布值一致）",
            "record_file": "software/kaggle_simulations/opponents/PROVENANCE.md",
            "license": "无显式许可",
        },
        {
            "key": "B",
            "account": "ahmedberatozer",
            "notebook": "kaggriculture-v48-clear-the-queue",
            "acquired_date": "2026-09-20",
            "channel": "kaggle kernels pull（拉回）",
            "artifact_sha256_evidence": "base=提交包解码真源码 dadee25a…",
            "record_file": "software/kaggle_simulations/v48plus/README.md",
            "license": "Apache-2.0（声明待核）",
        },
    ],
}


def _make_campaign(tmp_path: Path) -> Path:
    """tmp 战役根：两记录文件（各单源）+ 对外文档面一件干净 md。"""
    prov = tmp_path / "software/kaggle_simulations/opponents/PROVENANCE.md"
    prov.parent.mkdir(parents=True)
    prov.write_text("Author: kaitofukami\nSHA-256: dadee25a…\n", encoding="utf-8")
    readme = tmp_path / "software/kaggle_simulations/v48plus/README.md"
    readme.parent.mkdir(parents=True, exist_ok=True)
    readme.write_text("V48: Ahmed Berat Ozer, Apache-2.0\n", encoding="utf-8")
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "guide.md").write_text("内部指南，与血统无关。\n", encoding="utf-8")
    return tmp_path


def test_writes_dual_source_record_with_scan(tmp_path):
    camp = _make_campaign(tmp_path)
    out = tmp_path / "out" / "provenance_dadee25a.md"
    verdict = write_dual_source_provenance(_EVIDENCE, campaign_root=camp, output_path=out)
    assert verdict["output_path"] == out and out.is_file()
    text = out.read_text(encoding="utf-8")
    # 双源齐备 + 各自日期/通道/许可现状
    assert "kaitofukami" in text and "ahmedberatozer" in text
    assert "2026-08-31" in text and "2026-09-20" in text
    assert "无显式许可" in text and "Apache-2.0" in text
    # 原创归属未定声明 + 在跑资产引用规则
    assert "两账号间未定" in text
    assert "56400478" in text and "双源并列" in text
    # 单源断言扫描：两记录文件均判残留，docs 面干净
    scan = verdict["scan"]
    assert [r["path"] for r in scan["residuals"]] == list(DEFAULT_RECORD_FILES)
    assert scan["counts"]["docs/guide.md"] == "unrelated"
    assert "残留清单" in text and "docs/guide.md" in text
    assert "旧树冻结" in text  # 处置：战后物理统一


def test_scan_classifies_dual_and_missing(tmp_path):
    camp = _make_campaign(tmp_path)
    # 把 v48plus README 改成双源提及 → dual-source
    (camp / "software/kaggle_simulations/v48plus/README.md").write_text(
        "V48: Ahmed Berat Ozer（Apache-2.0）；kaitofukami 08-31 首拉同 sha。\n",
        encoding="utf-8",
    )
    scan = scan_single_source_assertions(camp)
    assert scan["counts"]["software/kaggle_simulations/opponents/PROVENANCE.md"] == "single-source(A)"
    assert scan["counts"]["software/kaggle_simulations/v48plus/README.md"] == "dual-source"
    assert scan["dual"] == ["software/kaggle_simulations/v48plus/README.md"]
    # 缺失文件按 missing/unrelated 计，不炸
    scan2 = scan_single_source_assertions(tmp_path / "empty")
    assert all(c == "missing" for c in scan2["counts"].values())


def test_evidence_gate_fail_closed(tmp_path):
    camp = _make_campaign(tmp_path)
    bad = dict(_EVIDENCE, sources=[_EVIDENCE["sources"][0]])  # 只有一源
    with pytest.raises(ValueError, match="恰 2 个源"):
        write_dual_source_provenance(bad, campaign_root=camp, output_path=tmp_path / "x.md")
    bad2 = dict(_EVIDENCE, original_attribution="")
    with pytest.raises(ValueError, match="缺失顶层键.*original_attribution"):
        write_dual_source_provenance(bad2, campaign_root=camp, output_path=tmp_path / "x.md")
    bad3 = dict(_EVIDENCE)
    bad3["sources"] = [dict(_EVIDENCE["sources"][0]), {"key": "B", "account": "b"}]  # 源B缺键
    with pytest.raises(ValueError, match="源 B 证据缺失键"):
        write_dual_source_provenance(bad3, campaign_root=camp, output_path=tmp_path / "x.md")


def test_deterministic_bytes_and_marker_constants(tmp_path):
    camp = _make_campaign(tmp_path)
    scan = scan_single_source_assertions(camp)
    assert render_provenance_record(_EVIDENCE, scan) == render_provenance_record(_EVIDENCE, scan)
    assert SOURCE_A_MARKERS == ("kaitofukami",)
    assert any("berat ozer" == m for m in SOURCE_B_MARKERS)
    assert "禁止单源断言" in ONLINE_REF_RULE and "双源并列" in ONLINE_REF_RULE
