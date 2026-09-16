#!/usr/bin/env python3
"""报告数字核验器（e2e-rehearsal-2026 m1 / 票 03）：a3 验收 cmd。

核验内容（契约见 interface/contract.md §4/§6）：
1. docs/report.pdf 存在（PDF 存在性）；
2. docs/report.typ 存在，且按契约引用语法扫描出 >=1 个 metrics 键引用（键名扫描）；
3. 每个被引用键均存在于 software/metrics.json 顶层键。

退出码：全部通过=0；任一不满足=1（FAIL 与原因输出到 stderr）；参数/文件读写异常=2。
默认路径按战役根解析（本脚本位于 <战役根>/software/）；--pdf/--typ/--metrics 可覆盖（测试夹具用）。

纯 Python stdlib；不解析 PDF 内部结构（W1 冻结口径：键名扫描 + PDF 存在性）。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CAMPAIGN_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PDF = CAMPAIGN_ROOT / "docs" / "report.pdf"
DEFAULT_TYP = CAMPAIGN_ROOT / "docs" / "report.typ"
DEFAULT_METRICS = CAMPAIGN_ROOT / "software" / "metrics.json"

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_ERROR = 2

# 契约 §4 两种规范引用形：
#   规范形  metrics.software.<key>   （与 merge_metrics 汇总后的引用形一致）
#   取值形  metrics.<key>            （report.typ 中 json() 读分片的变量，变量名必须为 metrics）
# 取值形的键后不得紧跟 "." 或词字符，避免把 metrics.software.<key> 误切出 "software"。
_REF_CANONICAL = re.compile(r"metrics\.software\.([A-Za-z0-9_]+)")
_REF_LOCAL = re.compile(r"metrics\.([A-Za-z_][A-Za-z0-9_]*)(?![.\w])")
# 加载语句的路径字面量（如 json("../../software/metrics.json")）不是键引用：扫描前剥离，
# 否则文件名 "metrics.json" 会被取值形误捕为键 "json"（契约 §4 注明）。
_JSON_PATH_LITERAL = re.compile(r'json\(\s*"[^"]*"\s*\)')


class CheckReportError(Exception):
    """文件读写/解析异常（退出码 2）。"""


def extract_metric_refs(typ_text: str) -> set:
    """从 report.typ 文本提取被引用的 metrics 键名集合（两种规范形，自动去重）。"""
    text = _JSON_PATH_LITERAL.sub("json(...)", typ_text)
    refs = set(_REF_CANONICAL.findall(text))
    refs |= set(_REF_LOCAL.findall(text))
    return refs


def load_metrics(metrics_path: Path) -> dict:
    if not Path(metrics_path).is_file():
        raise CheckReportError(f"metrics 分片不存在: {metrics_path}")
    try:
        data = json.loads(Path(metrics_path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        raise CheckReportError(f"metrics 分片读取/解析失败: {e}") from e
    if not isinstance(data, dict):
        raise CheckReportError("metrics 分片顶层必须是 JSON 对象")
    return data


def run_checks(pdf_path: Path, typ_path: Path, metrics_path: Path):
    """判定核：返回 (problems, refs)。

    problems 为空列表 = 通过；refs = report.typ 中扫描到的全部引用键
    （含未知键——未知键同时计入 problems，fail-closed）。
    """
    keys = load_metrics(metrics_path)
    problems = []
    refs = set()

    if not Path(pdf_path).is_file():
        problems.append(f"报告 PDF 不存在: {pdf_path}")
    if not Path(typ_path).is_file():
        problems.append(f"报告 Typst 源不存在: {typ_path}")
    else:
        typ_text = Path(typ_path).read_text(encoding="utf-8")
        refs = extract_metric_refs(typ_text)
        if not refs:
            problems.append(
                "report.typ 中未发现任何 metrics 键引用（契约 §4 要求至少 1 个）"
            )
        else:
            unknown = sorted(refs - keys.keys())
            if unknown:
                problems.append(
                    "report.typ 引用了 metrics 分片中不存在的键: " + ", ".join(unknown)
                )
    return problems, refs


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description="a3 核验器：report.pdf 存在 + report.typ 引用的 metrics 键全部命中 software/metrics.json"
    )
    ap.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="报告 PDF 路径")
    ap.add_argument("--typ", type=Path, default=DEFAULT_TYP, help="报告 Typst 源路径")
    ap.add_argument(
        "--metrics", type=Path, default=DEFAULT_METRICS, help="software metrics 分片路径"
    )
    args = ap.parse_args(argv)

    try:
        problems, refs = run_checks(args.pdf, args.typ, args.metrics)
    except (CheckReportError, OSError) as e:
        print(f"[check_report] 异常: {e}", file=sys.stderr)
        return EXIT_ERROR

    if problems:
        print("[check_report] FAIL:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return EXIT_FAIL

    print(
        f"OK: 报告 PDF 存在，report.typ 的 {len(refs)} 个 metrics 键引用全部命中: "
        + ", ".join(sorted(refs))
    )
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
