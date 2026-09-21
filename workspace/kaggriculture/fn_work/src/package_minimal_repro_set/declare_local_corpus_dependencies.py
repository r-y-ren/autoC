"""非入库语料依赖声明：哪些结论依赖主力机语料、缺什么、如何补齐——
源=G23 清单（fn_docs/behavior_inventory.md）与 fn_docs/machine_context.md 的
skip 清单，外加收集登记（MANIFEST registry）中的 missing 件回填通道。

上游: R19（详见 fn_docs/responsibility.md）

实现要点：
- 默认扫描战役 fn_docs 两文档（容错解析：G23 表行/corpus_integrity 关键事实行/
  数据依赖 skip 节/旧树环境性分类中语料相关 bullet），解析不到该源记
  available=false 但不抛（契约"错误: 无"）；dependency_scan 可注入覆盖（测试）。
- 引用纪律：声明文档逐条带来源（文档相对路径+读取日期），无凭记忆撰写。
- 输出 markdown 落 fn_work/minimal_repro_set/LOCAL_CORPUS_DEPENDENCIES.md，
  返回结构化 dict（依赖结论/缺失件+补齐/来源），供顶层裁决与测试断言。
"""

from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path

from shared.discover_campaign_roots import discover_campaign_roots

__all__ = ["declare_local_corpus_dependencies"]

DEFAULT_OUTPUT_SUBPATH = "fn_work/minimal_repro_set/LOCAL_CORPUS_DEPENDENCIES.md"

# 扫描锚点：旧树环境性分类中与语料/缺机相关的 bullet 起始标记
_DEPENDENCY_BULLET_MARKERS = ("gitignored 数据缺机", "语料缺机 skip")


def _read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return None


def _scan_behavior_inventory(text: str | None) -> list[str]:
    """G23 行 + corpus_integrity 本机实测关键事实行（逐条原文摘录）。"""
    if text is None:
        return []
    hits = []
    for line in text.splitlines():
        if re.match(r"^\|\s*G23\s*\|", line):
            hits.append(line.strip())
        elif "corpus_integrity" in line and "本机实测" in line:
            hits.append(line.strip())
    return hits


def _scan_machine_context(text: str | None) -> dict:
    """数据依赖 skip 清单节 + 旧树分类中语料相关 bullet。"""
    result: dict = {"skip_section": [], "environmental_bullets": [], "baseline_claims": []}
    if text is None:
        return result
    section = None
    for line in text.splitlines():
        heading = re.match(r"^#{2,6}\s+(.*)$", line)   # 任意 ##~###### 级标题
        if heading:
            section = heading.group(1).strip()
            continue
        if section == "数据依赖项 skip 清单（缺什么逐项标注）" and line.strip():
            result["skip_section"].append(line.strip())
        if section and section.startswith("旧树环境性失败"):
            stripped = line.strip()
            if stripped.startswith("- **") and any(
                    marker in stripped for marker in _DEPENDENCY_BULLET_MARKERS):
                result["environmental_bullets"].append(stripped)
        if section and section.startswith("历史口径") and line.strip().startswith("- 口径"):
            result["baseline_claims"].append(line.strip())
    return result


def _bullet(text: str) -> str:
    """剥源行自带的列表前缀，避免渲染出双横线。"""
    return text[2:].strip() if text.startswith("- ") else text


def _render_document(dependency_scan: dict, read_date: str) -> str:
    lines = [
        "# 非入库语料依赖声明（LOCAL_CORPUS_DEPENDENCIES）",
        "",
        "- 机制: package_minimal_repro_set → declare_local_corpus_dependencies（R19/G23）",
        "- 用途: fresh clone 持最小集复算时，显式声明哪些结论仍依赖主力机语料、"
        "缺什么、如何在主力机补齐（不冒充可复算）。",
        "",
        "## 1. 哪些结论依赖主力机语料（本机/fresh clone 不可复算）",
        "",
    ]
    for claim in dependency_scan.get("conclusions", []):
        lines.append(f"- {_bullet(claim)}")
    if not dependency_scan.get("conclusions"):
        lines.append("- （无登记项——异常：G23 清单应至少一条）")
    lines += [
        "",
        "## 2. 缺失件与补齐办法（逐件，来自收集登记）",
        "",
    ]
    for item in dependency_scan.get("missing_files", []):
        lines.append(
            f"- `{item['source_path']}`（{item['category']}）——补齐: {item['backfill']}")
    if not dependency_scan.get("missing_files"):
        lines.append("- 本次收集无缺失件（最小集齐备）。")
    lines += [
        "",
        "## 3. 数据依赖 skip 清单（缺什么逐项标注，源=fn_docs/machine_context.md）",
        "",
    ]
    for bullet in dependency_scan.get("skip_items", []):
        lines.append(f"- {_bullet(bullet)}")
    if not dependency_scan.get("skip_items"):
        lines.append("- （无数据依赖 skip 登记项）")
    lines += [
        "",
        "## 4. 环境性失败/skip 分类中语料相关项（历史事实口径）",
        "",
    ]
    for bullet in dependency_scan.get("environmental_bullets", []):
        lines.append(f"- {_bullet(bullet)}")
    lines += [
        "",
        "## 5. 来源（引用纪律）",
        "",
    ]
    for source in dependency_scan.get("sources", []):
        if isinstance(source, dict):
            avail = "在库" if source.get("available") else "本机缺失（解析降级）"
            lines.append(f"- {source.get('path', '?')} [{avail}]（读取日期 {read_date}）")
        else:
            lines.append(f"- {source}（读取日期 {read_date}）")
    lines.append("- 收集登记: fn_work/minimal_repro_set/MANIFEST.json（本函数调用方落盘）")
    lines.append("")
    return "\n".join(lines)


def declare_local_corpus_dependencies(dependency_scan=None, *, campaign_root=None,
                                      output_path=None, read_date=None) -> dict:
    """生成非入库语料依赖声明文档并落盘，返回结构化声明 dict。

    Args:
        dependency_scan: 注入的依赖扫描（测试/上游覆盖）；None 或缺键时对缺失键
            回退默认扫描（战役 fn_docs 两文档），已给键完全覆盖——顶层编排只传
            missing_files（收集 registry 的缺失件），其余键自动补默认扫描。
            已知键：conclusions / missing_files / skip_items /
            environmental_bullets / sources。
        campaign_root: 战役根；None=shared.discover_campaign_roots 发现。
        output_path: 声明文档落点；None=<战役根>/fn_work/minimal_repro_set/
            LOCAL_CORPUS_DEPENDENCIES.md。
        read_date: 来源读取日期（YYYY-MM-DD）；None=当日（引用纪律）。

    Returns:
        dict: {output_path, conclusions, missing_files, skip_items,
        environmental_bullets, sources, document, written}——document 为渲染
        全文（written=落盘是否成功；落盘失败不抛，返回 written=false）。
    """
    if campaign_root is None:
        campaign_root = discover_campaign_roots()["campaign_root"]
    campaign_root = Path(campaign_root)
    if read_date is None:
        read_date = _dt.date.today().isoformat()

    inventory_rel = "fn_docs/behavior_inventory.md"
    machine_rel = "fn_docs/machine_context.md"
    scan = dict(dependency_scan) if dependency_scan else {}
    _scan_keys = ("conclusions", "skip_items", "environmental_bullets", "sources")
    if any(key not in scan for key in _scan_keys):
        # 缺键回退默认扫描（None=全默认；部分注入=只覆盖给出的键）
        inventory_text = _read_text(campaign_root / inventory_rel)
        machine_text = _read_text(campaign_root / machine_rel)
        machine_facts = _scan_machine_context(machine_text)
        defaults = {
            "conclusions": _scan_behavior_inventory(inventory_text)
            + machine_facts["baseline_claims"],
            "skip_items": machine_facts["skip_section"],
            "environmental_bullets": machine_facts["environmental_bullets"],
            "sources": [
                {"path": inventory_rel, "available": inventory_text is not None},
                {"path": machine_rel, "available": machine_text is not None},
            ],
        }
        for key, value in defaults.items():
            scan.setdefault(key, value)

    merged = {
        "conclusions": list(scan.get("conclusions", [])),
        "missing_files": list(scan.get("missing_files", [])),
        "skip_items": list(scan.get("skip_items", [])),
        "environmental_bullets": list(scan.get("environmental_bullets", [])),
        "sources": list(scan.get("sources", [])),
    }
    document = _render_document(merged, read_date)

    if output_path is None:
        output_path = campaign_root / DEFAULT_OUTPUT_SUBPATH
    output_path = Path(output_path)
    written = False
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(document, encoding="utf-8")
        written = True
    except OSError:
        written = False

    return {
        "output_path": str(output_path),
        "read_date": read_date,
        "written": written,
        "document": document,
        **merged,
    }
