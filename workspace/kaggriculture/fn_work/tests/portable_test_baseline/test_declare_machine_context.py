"""declare_machine_context 真实测试：双口径并列渲染、skip 缺什么清单、确定性字节、tmp 重定向与默认路径、类型门。"""

from pathlib import Path

import pytest

from portable_test_baseline.declare_machine_context import (
    HISTORICAL_BASELINE,
    declare_machine_context,
    default_output_path,
    render_machine_context,
)

_RECORDS = {
    "local_run": {
        "command": "python -m pytest fn_work/tests -q",
        "platform": "Linux-6.x-x86_64",
        "python": "3.12",
        "summary_line": "976 passed, 8 failed, 8 skipped in 64.00s",
        "collected": 992,
        "passed": 976,
        "failed": 8,
        "skipped": 8,
    },
    "data_dependency_skips": [
        {"item": "test_replay_corpus_full", "missing": "gitignored 语料目录 corpus/raw（~GB）不在库内"},
    ],
    "crlf_lf_strategy": "exports index 类 5 件：LF 重建 100、CRLF 变体 79 条双 sha 登记",
    "assertion_strategy": "扫描 51 文件，命中 0、改写 0、残留 0",
    "windows_main_machine_recheck": "本机不可执行，需 Windows 主力机复跑同 commit",
}


def test_renders_dual_scopes_and_skip_list(tmp_path):
    out = tmp_path / "machine_context.md"
    path = declare_machine_context(_RECORDS, output_path=out)
    assert path == out and out.is_file()
    text = out.read_text(encoding="utf-8")
    # 历史口径（"990+2 仅主力机"）与通用口径（本机实测数）并列
    assert "990+2" in text
    assert HISTORICAL_BASELINE["claim"][:10] in text
    assert "fn_docs/behavior_inventory.md" in text
    assert "976 passed, 8 failed, 8 skipped in 64.00s" in text
    # 旧树环境性分类（CRLF×3 / 数据缺机×3 / Windows-only 断言×2 / 语料 skip×8）
    assert "test_artifact_indexes" in text
    assert "normcase" in text
    assert 'Path("C:/…").is_abs' 'olute()' in text  # 拼接：避免自命中扫描器 token
    assert "语料缺机 skip×8" in text
    # skip 清单缺什么逐项标注
    assert "test_replay_corpus_full" in text
    assert "corpus/raw" in text
    # CRLF/LF 双兼容策略 + Windows 复检边界
    assert ".gitattributes" in text
    assert "Windows 主力机复跑" in text or "Windows 主力机执行" in text


def test_deterministic_bytes_same_records(tmp_path):
    text1 = render_machine_context(_RECORDS)
    text2 = render_machine_context(_RECORDS)
    assert text1 == text2
    out1 = tmp_path / "a" / "mc.md"
    out2 = tmp_path / "b" / "mc.md"
    declare_machine_context(_RECORDS, output_path=out1)
    declare_machine_context(_RECORDS, output_path=out2)
    assert out1.read_bytes() == out2.read_bytes()


def test_empty_records_render_explicit_placeholders(tmp_path):
    out = tmp_path / "mc.md"
    declare_machine_context({}, output_path=out)
    text = out.read_text(encoding="utf-8")
    assert "禁止编造" in text
    assert "无本机实测记录传入" in text
    assert "0 个数据依赖 skip" in text


def test_default_output_path_is_campaign_fn_docs():
    from shared.discover_campaign_roots import discover_campaign_roots
    campaign_root = discover_campaign_roots()["campaign_root"]
    expected = Path(campaign_root) / "fn_docs" / "machine_context.md"
    assert default_output_path() == expected
    # 只算路径不写盘（本测试不触战役树）
    assert not expected.exists() or expected.read_bytes()


def test_rejects_non_dict_records(tmp_path):
    with pytest.raises(TypeError, match="dict"):
        declare_machine_context(["not", "a", "dict"], output_path=tmp_path / "x.md")


def test_skips_table_only_when_provided(tmp_path):
    out = tmp_path / "mc.md"
    declare_machine_context({"data_dependency_skips": [
        {"item": "t_full", "missing": "缺 references/intel-notebooks 语料"}]},
        output_path=out)
    text = out.read_text(encoding="utf-8")
    assert "| t_full | 缺 references/intel-notebooks 语料 |" in text
