"""declare_local_corpus_dependencies 真实测试：注入扫描的声明文档渲染与键
（依赖结论/缺失件补齐/skip 清单/来源+读取日期）、默认扫描解析 tmp 假 fn_docs
（G23 表行/corpus_integrity 关键事实/skip 节/语料 bullet）、文档缺源降级不抛。"""

from pathlib import Path

from package_minimal_repro_set.declare_local_corpus_dependencies import (
    declare_local_corpus_dependencies,
)

_SCAN = {
    "conclusions": [
        "| G23 | 原始回放证据 gitignored：fresh clone 不可复算画像与法证结论 | 数据归宿裁决 |",
        "- 口径: \"990+2\" 基线仅在 Windows 主力机 + 语料在机成立",
    ],
    "missing_files": [
        {"category": "flagoff_golden",
         "source_path": "software/exports/probes/planner_flagoff/golden_v138.json",
         "backfill": "主力机重跑 planner_flagoff_golden.py --emit 后重跑收集"},
    ],
    "skip_items": ["- 本次运行 0 个数据依赖 skip（本机无缺失项触发）"],
    "environmental_bullets": ["- **语料缺机 skip×8**: 8 skipped 全为语料缺机"],
    "sources": [{"path": "fn_docs/behavior_inventory.md", "available": True}],
}


def test_injected_scan_renders_document_with_all_sections(tmp_path):
    result = declare_local_corpus_dependencies(
        dict(_SCAN), campaign_root=tmp_path, output_path=tmp_path / "dep.md",
        read_date="2026-09-21")

    assert result["written"] is True
    doc = result["document"]
    assert "## 1. 哪些结论依赖主力机语料" in doc
    assert "## 2. 缺失件与补齐办法" in doc
    assert "## 3. 数据依赖 skip 清单" in doc
    assert "## 5. 来源" in doc
    # 依赖结论逐条入文档（G23 行 + 基线口径）；源行自带 "- " 前缀被剥（无双横线）
    assert "G23" in doc and "不可复算画像与法证结论" in doc
    assert "990+2" in doc
    assert "\n- - " not in doc
    # 缺失件带补齐通道
    assert "golden_v138.json" in doc and "--emit" in doc
    # 引用纪律：来源+读取日期
    assert "fn_docs/behavior_inventory.md" in doc and "2026-09-21" in doc
    # 落盘内容与返回 document 一致
    assert (tmp_path / "dep.md").read_text(encoding="utf-8") == doc


def test_returned_dict_carries_structured_keys(tmp_path):
    result = declare_local_corpus_dependencies(
        dict(_SCAN), campaign_root=tmp_path, output_path=tmp_path / "dep.md",
        read_date="2026-09-21")
    for key in ("output_path", "read_date", "written", "document", "conclusions",
                "missing_files", "skip_items", "environmental_bullets", "sources"):
        assert key in result
    assert result["read_date"] == "2026-09-21"
    assert result["missing_files"] == _SCAN["missing_files"]


def test_no_missing_files_branch(tmp_path):
    scan = {k: v for k, v in _SCAN.items() if k != "missing_files"}
    result = declare_local_corpus_dependencies(
        scan, campaign_root=tmp_path, output_path=tmp_path / "dep.md")
    assert "本次收集无缺失件（最小集齐备）" in result["document"]


def test_default_scan_parses_fake_fn_docs(tmp_path):
    root = tmp_path / "camp"
    (root / "fn_docs").mkdir(parents=True)
    (root / "fn_docs/behavior_inventory.md").write_text(
        "| 编号 | 缺口 | 处置 |\n|---|---|---|\n"
        "| G23 | 原始回放证据 gitignored：21/27 Track-B 脚本本机不可跑 | 数据归宿裁决 |\n"
        "关键事实：**corpus_integrity（蓝图验收 cmd）本机实测 exit=1**"
        "（references/data/replay-corpus/manifest.json gitignored 缺失）。\n",
        encoding="utf-8")
    (root / "fn_docs/machine_context.md").write_text(
        "# 声明\n\n## 历史口径（\"990+2\"仅主力机）\n\n"
        "- 口径: \"990+2\" 基线仅在 Windows 主力机 + 语料在机成立\n\n"
        "### 旧树环境性失败/skip 分类（历史事实）\n\n"
        "- **gitignored 数据缺机×3**: 语料/参考数据不在库内\n"
        "- **语料缺机 skip×8**: 8 skipped 全为语料缺机\n"
        "- **Windows-only 断言×2**: 无关项不入声明\n\n"
        "## 数据依赖项 skip 清单（缺什么逐项标注）\n\n"
        "- 本次运行 0 个数据依赖 skip（本机无缺失项触发）。\n",
        encoding="utf-8")

    result = declare_local_corpus_dependencies(
        campaign_root=root, output_path=tmp_path / "out/dep.md")
    assert result["written"] is True
    assert any("G23" in c for c in result["conclusions"])
    assert any("corpus_integrity" in c for c in result["conclusions"])
    assert any("990+2" in c for c in result["conclusions"])
    # 语料相关 bullet 收入、无关项排除
    joined = "\n".join(result["environmental_bullets"])
    assert "语料缺机" in joined and "gitignored 数据缺机" in joined
    assert "Windows-only" not in joined
    assert any("0 个数据依赖 skip" in s for s in result["skip_items"])
    # 两文档均登记为在库来源
    assert {s["path"] for s in result["sources"]} == {
        "fn_docs/behavior_inventory.md", "fn_docs/machine_context.md"}


def test_missing_fn_docs_degrades_without_raising(tmp_path):
    root = tmp_path / "camp"
    root.mkdir()
    result = declare_local_corpus_dependencies(campaign_root=root,
                                               output_path=tmp_path / "dep.md")
    assert result["written"] is True                    # 契约"错误: 无"：降级不抛
    assert all(s["available"] is False for s in result["sources"])
    assert "本机缺失（解析降级）" in result["document"]
    assert result["conclusions"] == []


def test_default_output_path_under_campaign(tmp_path):
    root = tmp_path / "camp"
    root.mkdir()
    result = declare_local_corpus_dependencies(campaign_root=root)
    expected = (root / "fn_work/minimal_repro_set"
                / "LOCAL_CORPUS_DEPENDENCIES.md")
    assert Path(result["output_path"]) == expected
