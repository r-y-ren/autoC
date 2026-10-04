"""扫描目录（默认旧树 scripts/，只读）检出"无入口库件"：无 main/argparse/__main__ 入口标记且被其他件 import 的 .py 文件（R15 防复发断言的判据源）。

上游: R15（详见 fn_docs/responsibility.md）

实现要点：
- "无入口"判据 = 三种入口标记全缺位：``def main(...)`` / ``argparse`` 词元 /
  ``__main__`` 词元（if __name__ == "__main__" 守卫）。argparse/__main__ 按
  词元匹配，docstring 散文提及会误判"有入口"——方向为漏报（保守，防复发
  断言侧安全），如实测 G17 件 market_ledger.py 三标记全无。
- "被 import"判据 = 同目录其他 .py 的 import 面（两种形态，沿用
  archive_forensic_assets 口径）：①import/from 语句（容忍点前缀，
  ``from scripts.market_ledger import X`` 与裸 ``import market_ledger``
  均命中——旧树消费方 sell_plan_reconciliation 为点前缀形态）；②带引号
  文件名引用（importlib/subprocess 动态装载形态，旧树
  test_market_reconciliation_ledger 按 path 装载即此形态）。自身不算
  import 方。
- 平铺扫描 directory/*.py（scripts/ 为平铺目录，同 partition_script_tiers
  实际清门口径）；__init__.py 为包标记件不参判。只读源文本，零写入、
  零 import 执行。
- 输出条目 {file, importers（升序）, entry_markers（三标记布尔）}按文件名
  排序；目录缺失 ValueError fail-closed（用法错误，非域内错误——域内
  错误: 无）。
"""

from __future__ import annotations

import re
from pathlib import Path

__all__ = ["scan_for_library_misplacement", "ENTRY_MARKER_PATTERNS"]

# 三种入口标记：任一在场即"有入口"，不判库件
ENTRY_MARKER_PATTERNS = {
    "def main": re.compile(r"(?m)^[ \t]*def\s+main\s*\("),
    "argparse": re.compile(r"\bargparse\b"),
    "__main__ guard": re.compile(r"\b__main__\b"),
}

# import 面模式（mod=模块词元）：import/from 语句（容忍点前缀）+ 带引号文件名
_IMPORT_STMT_TMPL = (
    r"(?m)^[ \t]*(?:import[ \t]+(?:[\w.]*\.)?{mod}\b"
    r"|from[ \t]+(?:[\w.]*\.)?{mod}[ \t]+import\b)"
)
_FILENAME_REF_TMPL = r"[\"']{file}[\"']"


def scan_for_library_misplacement(directory) -> list:
    """扫描目录检出无入口库件（无 main/argparse/__main__ 且被 import）。

    Args:
        directory: 待扫目录（默认调用方传 <战役根>/software/scripts，只读）；
            平铺扫描 *.py，__init__.py 除外。

    Returns:
        库件清单 list[dict]，按文件名排序，每条：
        {"file": 文件名, "importers": [引用它的同目录件…],
         "entry_markers": {"def main": bool, "argparse": bool,
                           "__main__ guard": bool}}
        （三标记全 False 即"无入口"实证。）

    Raises:
        ValueError: 目录不存在或非目录（用法错误 fail-closed）。
    """
    root = Path(directory) if directory is not None else None
    if root is None or not root.is_dir():
        raise ValueError(f"扫描目录不存在或非目录: {root}")

    files = sorted(p for p in root.glob("*.py") if p.name != "__init__.py")
    sources = {p.name: p.read_text(encoding="utf-8", errors="replace")
               for p in files}
    if not sources:
        return []

    # 每件入口标记在场性
    markers = {
        name: {label: bool(pattern.search(text))
               for label, pattern in ENTRY_MARKER_PATTERNS.items()}
        for name, text in sources.items()
    }

    # import 面：目标=无入口件，宿主=同目录其他件（两种引用形态）
    targets = [Path(name) for name, m in markers.items()
               if not any(m.values())]
    hits: dict[str, list[str]] = {t.name: [] for t in targets}
    for target in targets:
        patterns = [
            re.compile(_IMPORT_STMT_TMPL.format(mod=re.escape(target.stem))),
            re.compile(_FILENAME_REF_TMPL.format(file=re.escape(target.name))),
        ]
        for host, text in sources.items():
            if host == target.name:
                continue
            if any(p.search(text) for p in patterns):
                hits[target.name].append(host)

    return [
        {"file": name, "importers": sorted(hits[name]),
         "entry_markers": markers[name]}
        for name in sorted(hits) if hits[name]
    ]
