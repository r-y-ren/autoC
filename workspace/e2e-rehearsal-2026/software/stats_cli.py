#!/usr/bin/env python3
"""统计 CLI（e2e-rehearsal-2026 m1 / 票 01）：读 CSV → 输出统计 JSON。

外部行为（冻结于 interface/contract.md，测试见 tests/test_stats_cli.py）：
- 输入：`--csv <路径>`，UTF-8（容忍 BOM）CSV，首行为表头；
- 输出（stdout）：统计 JSON——行数/列数/列名/数值列清单/数值列 count+mean+max；
- `--check` 自检模式：统计合法（含语义自检，见 sanity_problems）→ 输出 JSON 且退出码 0；
  输入异常或自检不过 → stderr 报因、退出码非 0；
- 纯 Python stdlib，零第三方依赖。

统计 JSON 形状（示例）：
{
  "source": "sample.csv",
  "rows": 6,
  "cols": 3,
  "columns": ["name", "score", "hours"],
  "numeric_columns": ["score", "hours"],
  "numeric": {"score": {"count": 6, "mean": 88.0, "max": 95.0}, ...}
}

数值列判定：该列所有非空单元格均可解析为有限浮点，且至少有一个非空值；
空单元格视为缺失值，不参与 count/mean/max。
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from pathlib import Path

EXIT_OK = 0
EXIT_FAIL = 2


class StatsError(Exception):
    """输入异常（文件缺失/空文件/无数据行/行列不齐等）。"""


def _parse_number(text: str):
    """解析单个单元格：空串=缺失(None)；可解析的有限浮点=float；否则=非数值哨兵 False。"""
    t = text.strip()
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        return False
    return v if math.isfinite(v) else False


def compute_stats(csv_path) -> dict:
    """读 CSV 计算统计。输入异常抛 StatsError；正常返回统计 dict（形状见模块 docstring）。"""
    path = Path(csv_path)
    if not path.is_file():
        raise StatsError(f"CSV 文件不存在或不可读: {path}")
    try:
        with path.open("r", encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.reader(fh))
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        raise StatsError(f"CSV 读取失败: {e}") from e

    if not rows:
        raise StatsError("空文件（连表头都没有）")
    header = rows[0]
    if not any(cell.strip() for cell in header):
        raise StatsError("表头为空行")
    data = rows[1:]
    if not data:
        raise StatsError("无数据行（仅表头）")
    cols = len(header)

    for i, row in enumerate(data, start=2):
        if len(row) != cols:
            raise StatsError(
                f"第 {i} 行字段数 {len(row)} 与表头列数 {cols} 不一致（行列不齐）"
            )

    stats = {
        "source": path.name,
        "rows": len(data),
        "cols": cols,
        "columns": list(header),
        "numeric_columns": [],
        "numeric": {},
    }
    for idx, name in enumerate(header):
        values = []
        is_numeric = True
        for row in data:
            parsed = _parse_number(row[idx])
            if parsed is False:
                is_numeric = False
                break
            if parsed is not None:
                values.append(parsed)
        if is_numeric and values:
            stats["numeric_columns"].append(name)
            stats["numeric"][name] = {
                "count": len(values),
                "mean": sum(values) / len(values),
                "max": max(values),
            }
    return stats


def sanity_problems(stats: dict) -> list:
    """语义自检（--check 判定核）：返回问题清单，空列表=通过。"""
    problems = []
    if stats.get("rows", 0) < 1:
        problems.append("rows < 1：无数据行")
    if stats.get("cols", 0) < 1:
        problems.append("cols < 1：无列")
    if not stats.get("numeric_columns"):
        problems.append("无数值列：无法给出数值列均值/最大值")
    for name in stats.get("numeric_columns", []):
        entry = stats.get("numeric", {}).get(name, {})
        for key in ("mean", "max"):
            v = entry.get(key)
            if not isinstance(v, (int, float)) or not math.isfinite(v):
                problems.append(f"数值列 {name} 的 {key} 非有限数: {v!r}")
    return problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="读 CSV 输出统计 JSON（行/列/数值列均值与最大值）")
    ap.add_argument("--csv", required=True, help="输入 CSV 路径（首行表头，UTF-8）")
    ap.add_argument(
        "--check",
        action="store_true",
        help="自检模式：输出合法统计并以退出码 0 结束；输入异常以非 0 退出",
    )
    args = ap.parse_args(argv)

    try:
        stats = compute_stats(args.csv)
    except StatsError as e:
        print(f"[stats_cli] 输入异常: {e}", file=sys.stderr)
        return EXIT_FAIL

    if args.check:
        problems = sanity_problems(stats)
        if problems:
            print("[stats_cli] 自检未过:", file=sys.stderr)
            for p in problems:
                print(f"  - {p}", file=sys.stderr)
            return EXIT_FAIL

    print(json.dumps(stats, ensure_ascii=False, indent=2))
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main())
