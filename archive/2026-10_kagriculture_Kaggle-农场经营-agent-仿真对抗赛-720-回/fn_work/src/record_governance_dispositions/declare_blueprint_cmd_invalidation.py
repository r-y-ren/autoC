"""蓝图 2 条失效验收 cmd 的留档声明（指向不存在文件+09-01 后 /accept 静默事实；物理修订=战后 /attack，本函数只声明）。

上游: R4, R17, R21（详见 fn_docs/responsibility.md）

实现要点：
- 输出=<战役根>/fn_docs/blueprint_cmd_invalidation.md（测试经 output_path 重定向
  tmp，不写战役树）。确定性渲染（无时间戳）；失效事实逐条来自传入 cmd_list。
- 失效判据（fail-closed）：cmd 指向的文件在战役根下不存在才可声明失效；若路径
  实际存在，声明与事实不符即 ValueError——不许为存在的文件留失效声明。
- 静默事实（R17 留档核心）：最后一次触碰 doc-compile/doc-consistency 的全量
  /accept = acceptance/run-29（2026-09-01）；此后 run-30/run-31 均 scoped 检查单，
  两条 cmd 既未执行也无正式失效登记=被静默旁路。默认常量来自上述入库记录，
  亦可经 silent_fact 参数覆盖（测试注入）。
- 处置=战后经 /attack 修订蓝图一并处置；本函数只声明，不改蓝图文件
  （blueprint.md 属契约面，蓝图修订须重过 schema 校验+用户确认，不在本叶职权）。
"""

from __future__ import annotations

from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = [
    "DEFAULT_INVALID_CMDS",
    "DEFAULT_SILENT_FACT",
    "DISPOSITION",
    "default_output_path",
    "render_invalidation_declaration",
    "declare_blueprint_cmd_invalidation",
]

# 蓝图验收清单中已失效的 2 条 cmd（blueprint.md acceptance.checklist 原文事实；
# missing_path 为战役根相对路径）
DEFAULT_INVALID_CMDS = [
    {
        "id": "doc-compile",
        "cmd": "typst compile --root workspace/kaggriculture workspace/kaggriculture/docs/report.typ workspace/kaggriculture/docs/report.pdf",
        "missing_path": "docs/report.typ",
        "reason": "report.typ 从未入库（docs/ 下不存在），cmd 自蓝图订立即不可执行",
    },
    {
        "id": "doc-consistency",
        "cmd": "python workspace/kaggriculture/docs/check_report_metrics.py",
        "missing_path": "docs/check_report_metrics.py",
        "reason": "check_report_metrics.py 从未入库（docs/ 下不存在），cmd 自蓝图订立即不可执行",
    },
]

# 09-01 后 /accept 静默事实（源: acceptance/run-29..run-31 入库记录）
DEFAULT_SILENT_FACT = {
    "last_full_touch": {
        "run": "acceptance/run-29",
        "generated_at": "2026-09-01T08:08:31",
        "doc_compile": "fail（evidence: doc-compile.log）",
        "doc_consistency": "pass（但检查脚本本身不存在——口径存疑的 pass）",
    },
    "post_runs": [
        {"run": "acceptance/run-30", "generated_at": "2026-09-01T08:12:37+08:00",
         "scope": "p1-r5 scoped 检查单（8 项）", "contains_doc_cmds": False},
        {"run": "acceptance/run-31", "generated_at": "2026-09-01T04:05:02+00:00",
         "scope": "p2 scoped 检查单（11 项）", "contains_doc_cmds": False},
    ],
    "fact": "2026-09-01 之后全部 /accept 均为 scoped 检查单，doc-compile/doc-consistency "
            "两条 cmd 既未被执行、也无正式失效登记——失效状态被静默旁路而非显式处置。",
}

# 处置口径（R17：战后随 /attack 修订蓝图一并处置）
DISPOSITION = (
    "战后经 /attack 修订蓝图：两条失效 cmd 随蓝图修订一并移除或替换为可执行等价项，"
    "并重过 schema 校验+用户确认。本声明只留档，不改蓝图文件。"
)

_REQUIRED_CMD_KEYS = ("id", "cmd", "missing_path")


def default_output_path() -> Path:
    """失效声明默认输出路径：<战役根>/fn_docs/blueprint_cmd_invalidation.md（不写盘）。"""
    campaign_root = discover_campaign_roots()["campaign_root"]
    return campaign_root / "fn_docs" / "blueprint_cmd_invalidation.md"


def _validate_cmds(invalid_cmds: list, campaign_root: Path) -> None:
    """失效声明事实门（fail-closed）：缺键、非 dict、或 missing_path 实际存在即抛。"""
    if not isinstance(invalid_cmds, list) or not invalid_cmds:
        raise ValueError(f"invalid_cmds 必须为非空 list，实得 {invalid_cmds!r}")
    for entry in invalid_cmds:
        if not isinstance(entry, dict):
            raise ValueError(f"cmd 条目必须为 dict，实得 {entry!r}")
        miss = [k for k in _REQUIRED_CMD_KEYS if not entry.get(k)]
        if miss:
            raise ValueError(f"cmd {entry.get('id', '?')} 缺失键: {miss}")
        target = campaign_root / entry["missing_path"]
        if target.exists():
            raise ValueError(
                f"cmd {entry['id']} 的目标路径实际存在（{target}），"
                "不得为其留失效声明——失效判据与事实不符，拒绝渲染。"
            )


def render_invalidation_declaration(invalid_cmds: list, silent_fact: dict) -> str:
    """确定性渲染蓝图失效声明（无时间戳；事实全部来自传入清单与静默事实记录）。"""
    lines: list[str] = []
    lines.append("# 蓝图失效验收 cmd 留档声明（R17）")
    lines.append("")
    lines.append("## 失效 cmd 清单（2 条）")
    lines.append("")
    lines.append("| id | cmd（蓝图原文） | 指向路径（战役根相对） | 判定 |")
    lines.append("|---|---|---|---|")
    for entry in invalid_cmds:
        lines.append(
            f"| {entry['id']} | `{entry['cmd']}` | {entry['missing_path']} | 不存在 |"
        )
    lines.append("")
    for entry in invalid_cmds:
        lines.append(f"### {entry['id']}")
        lines.append("")
        lines.append(f"- cmd: `{entry['cmd']}`")
        lines.append(f"- 指向: `{entry['missing_path']}`（战役根下不存在，本声明落档时实测）")
        if entry.get("reason"):
            lines.append(f"- 失效原因: {entry['reason']}")
        lines.append("")
    lines.append("## 09-01 后 /accept 静默事实")
    lines.append("")
    touch = silent_fact.get("last_full_touch", {})
    lines.append(f"- 最后一次触碰两条 cmd 的 /accept: {touch.get('run', '—')}"
                 f"（{touch.get('generated_at', '—')}）——doc-compile={touch.get('doc_compile', '—')}；"
                 f"doc-consistency={touch.get('doc_consistency', '—')}。")
    for run in silent_fact.get("post_runs", []):
        lines.append(f"- 其后 {run.get('run', '—')}（{run.get('generated_at', '—')}）: "
                     f"{run.get('scope', '—')}，含 doc cmds={run.get('contains_doc_cmds')}。")
    if silent_fact.get("fact"):
        lines.append(f"- 事实定性: {silent_fact['fact']}")
    lines.append("")
    lines.append("## 处置")
    lines.append("")
    lines.append(f"- {DISPOSITION}")
    lines.append("")
    lines.append("## 记录元信息")
    lines.append("")
    lines.append(
        "- 生成器: fn_work/src/record_governance_dispositions/declare_blueprint_cmd_invalidation.py"
        "（record_governance_dispositions 编排叶）"
    )
    lines.append(
        "- 事实源: blueprint.md acceptance.checklist 原文 + acceptance/run-29..31 入库记录；"
        "本叶只声明，不动蓝图（蓝图修订须经 schema 校验+用户确认，战后 /attack 职权）。"
    )
    lines.append("")
    return "\n".join(lines)


def declare_blueprint_cmd_invalidation(
    invalid_cmds: list,
    *,
    silent_fact: dict | None = None,
    campaign_root: Path | None = None,
    output_path: Path | None = None,
) -> dict:
    """生成蓝图失效验收 cmd 的留档声明文档。

    Args:
        invalid_cmds: 失效 cmd 清单（id/cmd/missing_path[，reason]）；
            missing_path 在战役根下实际存在即 ValueError（fail-closed）。
        silent_fact: 09-01 后 /accept 静默事实（None=用入库记录默认值）。
        campaign_root: 战役根（None=按目录特征程序化发现，R20）。
        output_path: 输出路径（None=<战役根>/fn_docs/blueprint_cmd_invalidation.md）。

    Returns:
        裁决 dict：{"output_path", "invalidated", "silent_fact", "disposition"}。
    """
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    if silent_fact is None:
        silent_fact = DEFAULT_SILENT_FACT
    _validate_cmds(invalid_cmds, campaign_root)
    if output_path is None:
        output_path = campaign_root / "fn_docs" / "blueprint_cmd_invalidation.md"
    text = render_invalidation_declaration(invalid_cmds, silent_fact)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(text, encoding="utf-8", newline="\n")
    return {
        "output_path": output_path,
        "invalidated": [
            {"id": e["id"], "missing_path": e["missing_path"]} for e in invalid_cmds
        ],
        "silent_fact": silent_fact,
        "disposition": DISPOSITION,
    }
