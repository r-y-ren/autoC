"""基线机器语境声明生成：历史口径（"990+2 仅主力机"）与 fn_work 通用口径并列、数据依赖项 skip 标注缺什么、CRLF/LF 双兼容策略。

上游: R6, R20（详见 fn_docs/responsibility.md）

实现要点：
- 输出=<战役根>/fn_docs/machine_context.md（declare 叶输出物；测试经 output_path
  重定向 tmp，不写战役树）。文档确定性渲染：同一 records 两次生成逐字节一致
  （无时间戳/主机名），本机实测数字全部来自传入的 baseline_run_records
  （数据纪律：不编造数字）。
- 历史口径为固定事实块（源: fn_docs/behavior_inventory.md §5）：Windows 主力机
  实测 992 collected 中 990 绿+2 非绿基线（"990+2"）仅在"Windows 主力机+语料
  在机"成立；本 Linux 机同 commit 实测 976P/8F/8S，8F 全环境性（CRLF 工件×3
  =test_build_determinism/test_p3::TestPackaging/test_artifact_indexes、
  gitignored 数据缺机×3、Windows-only 断言×2=normcase/Path.is_absolute），
  8S 全为语料缺机。
- 通用口径 = 本机实测数（collected/passed/failed/skipped + 汇总行原文）+
  数据依赖项 skip 清单（逐项标注缺什么，缺即显式 skip 不冒充绿）+ CRLF/LF
  双兼容策略（仓外 .gitattributes 不可加→工件侧 fn_work/artifacts LF 重建双 sha
  登记 + 测试侧双平台断言工具）。
- Windows 主力机复检为人工/跨机事项（R6 验收"同 commit 在 Windows 主力机基线
  不回退"），本机不可执行——声明文档显式登记该边界，不静默。
"""

from __future__ import annotations

from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "HISTORICAL_BASELINE",
    "OLD_TREE_ENVIRONMENTAL_TAXONOMY",
    "default_output_path",
    "declare_machine_context",
]

# 历史口径固定事实（源: fn_docs/behavior_inventory.md §5，R6 声明核心；
# 只复述源文档明言内容，不发明分项拆分——数据纪律）
HISTORICAL_BASELINE = {
    "label": "990+2",
    "claim": '"990+2" 基线仅在 Windows 主力机 + 语料在机成立（口径原文见源文档）',
    "source": "fn_docs/behavior_inventory.md §5（分片 E：测试基线实测）",
    "posix_same_commit": "本 Linux 机同 commit 实测 976 passed / 8 failed / 8 skipped（992 collected）",
}

# 旧树 8F/8S 环境性分类（历史事实，declare 渲染的固定节）
OLD_TREE_ENVIRONMENTAL_TAXONOMY = [
    {"class": "CRLF 工件×3", "items": [
        "test_build_determinism", "test_p3::TestPackaging", "test_artifact_indexes"],
     "cause": "Windows autocrlf 机构建提交的登记 sha 为 CRLF 字节口径，POSIX fresh clone 盘上为 LF"},
    {"class": "gitignored 数据缺机×3", "items": ["（语料/参考数据不在库内）"],
     "cause": "复现链依赖 machine-local gitignored 语料，缺机即挂"},
    {"class": "Windows-only 断言×2", "items": [
        "normcase 大小写折叠语义", 'Path("C:/…").is_absolute() 语义'],
     "cause": "断言依赖 Windows 特有语义，POSIX 上必然为假"},
    {"class": "语料缺机 skip×8", "items": ["（8 skipped 全为语料缺机）"],
     "cause": "数据依赖项显式 skip（缺语料），非代码缺陷"},
]


def default_output_path() -> Path:
    """声明文档默认输出路径：<战役根>/fn_docs/machine_context.md（不写盘）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "fn_docs" / "machine_context.md"


def _section_local_run(records: dict) -> list[str]:
    local = records.get("local_run") or {}
    lines = ["## fn_work 通用口径（本机实测）", ""]
    if not local:
        lines.append("（无本机实测记录传入——本节留空，禁止编造数字。）")
        return lines + [""]
    lines.append(f"- 运行命令: `{local.get('command', '—')}`")
    lines.append(f"- 平台: {local.get('platform', '—')}；Python: {local.get('python', '—')}")
    lines.append(f"- 汇总行原文: `{local.get('summary_line', '—')}`")
    for key, label in (("collected", "collected"), ("passed", "passed"),
                       ("failed", "failed"), ("skipped", "skipped")):
        if local.get(key) is not None:
            lines.append(f"- {label}: {local[key]}")
    return lines + [""]


def _section_data_skips(records: dict) -> list[str]:
    skips = records.get("data_dependency_skips") or []
    lines = ["## 数据依赖项 skip 清单（缺什么逐项标注）", ""]
    if not skips:
        lines.append("- 本次运行 0 个数据依赖 skip（本机无缺失项触发；历史口径的语料缺机 "
                     "skip×8 见上节旧树分类）。")
        return lines + [""]
    lines.append("| 项 | 缺什么 |")
    lines.append("|---|---|")
    for item in skips:
        lines.append(f"| {item.get('item', '—')} | {item.get('missing', '—')} |")
    return lines + [""]


def _section_crlf_strategy(records: dict) -> list[str]:
    crlf = records.get("crlf_lf_strategy") or {}
    lines = ["## CRLF/LF 双兼容策略（仓外 .gitattributes 不可加，一切靠工件+测试双兼容）", ""]
    lines.append("- 工件侧：旧树 index 冻结不改；exports 工件类在 "
                 "`fn_work/artifacts/` 以 LF 规范化重建，双 sha 登记"
                 "（legacy=CRLF 口径原值 / LF=规范化重算值），POSIX 校验走 LF 值。")
    if crlf:
        lines.append(f"- 实测计数: {crlf}")
    lines.append("- 测试侧：路径等价断言用 `paths_equivalent`（normcase 双平台封装）、"
                 "绝对路径判断用 `is_absolute_cross_platform`（补盘符/UNC 语义）；"
                 "打包二进制件与 CRLF 无关，不重建仅登记。")
    return lines + [""]


def _section_assertion_strategy(records: dict) -> list[str]:
    assertion = records.get("assertion_strategy") or {}
    lines = ["## 断言双平台化（Windows-only 模式扫描）", ""]
    if assertion:
        lines.append(f"- 扫描与修正: {assertion}")
    else:
        lines.append("- 扫描报告未传入（见 portable_test_baseline 顶层裁决的 assertions 节）。")
    return lines + [""]


def render_machine_context(baseline_run_records: dict) -> str:
    """确定性渲染声明文档全文（同一 records 逐字节一致，无时间戳/主机名）。"""
    records = baseline_run_records or {}
    lines = [
        "# 测试基线机器语境声明（machine_context）",
        "",
        "> R6 声明物：历史口径与通用口径并列——任何“绿基线”结论必须先读本文档"
        "确认机器语境。实测数字只来自当次运行记录，禁止编造。",
        "",
        "## 历史口径（“990+2”仅主力机）",
        "",
        f"- 基线标签: {HISTORICAL_BASELINE['label']}",
        f"- 口径: {HISTORICAL_BASELINE['claim']}",
        f"- 同 commit POSIX 对照: {HISTORICAL_BASELINE['posix_same_commit']}",
        f"- 来源: {HISTORICAL_BASELINE['source']}",
        "",
        "### 旧树环境性失败/skip 分类（历史事实）",
        "",
    ]
    for tax in OLD_TREE_ENVIRONMENTAL_TAXONOMY:
        items = "、".join(tax["items"])
        lines.append(f"- **{tax['class']}**: {items}——{tax['cause']}")
    lines.append("")
    lines.extend(_section_local_run(records))
    lines.extend(_section_data_skips(records))
    lines.extend(_section_crlf_strategy(records))
    lines.extend(_section_assertion_strategy(records))
    windows = records.get("windows_main_machine_recheck")
    lines.extend([
        "## Windows 主力机复检边界（人工/跨机事项）",
        "",
        "- R6 验收要求“同 commit 在 Windows 主力机基线不回退”——该复检只能在 "
        "Windows 主力机执行，本机不可代跑；重建/修正后首次 Windows 复跑若回退，"
        "portable_test_baseline 裁决即失败（fail-closed）。",
    ])
    if windows:
        lines.append(f"- 备注: {windows}")
    return "\n".join(lines) + "\n"


def declare_machine_context(baseline_run_records, output_path=None) -> Path:
    """生成基线机器语境声明文档。

    Args:
        baseline_run_records: 基线运行记录 dict（local_run 实测数/
            data_dependency_skips 缺什么清单/crlf_lf_strategy 计数/
            assertion_strategy 扫描计数/windows_main_machine_recheck 备注；
            缺省节渲染为显式留空说明，不编造）。
        output_path: 输出路径；None=<战役根>/fn_docs/machine_context.md。

    Returns:
        写成的文档 Path（确定性字节：同 records 重跑逐字节一致）。
    """
    target = Path(output_path) if output_path is not None else default_output_path()
    if not isinstance(baseline_run_records, dict):
        raise TypeError(
            f"baseline_run_records 须为 dict（运行记录），得到 {type(baseline_run_records).__name__}")
    content = render_machine_context(baseline_run_records)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(content.encode("utf-8"))
    reread = target.read_bytes()
    if reread != content.encode("utf-8"):
        raise RuntimeError(f"声明文档写出后复核不一致: {target}")
    return target
