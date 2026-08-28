#!/usr/bin/env python3
"""S-09 实测指标分片汇总（merge_metrics）。

K-03 前置项的落地：并发交付期各角色只写自己的分片，杜绝共写顶层文件的覆盖风险。
  workspace/software/metrics.json  ┐
  workspace/hardware/metrics.json  ┘→ 汇总为 workspace/metrics.json（生成物，角色禁写）

汇总规则（确定性）：顶层 metrics.json = {"_generated_at": ..., "software": {...}, "hardware": {...}}，
角色分片内容原样挂到各自命名空间下；文档引用形如 metrics.hardware.power_w。

用法：python scripts/verify/merge_metrics.py   （分片缺失则跳过该命名空间）
"""

from __future__ import annotations

import datetime
import json
import os
import sys
from pathlib import Path

FRAGMENTS = ["software", "hardware", "document"]
# 2026-08-28 修复：document 分片此前缺席（Kaggriculture 战役实测暴露——workspace/document/metrics.json
# 存在但顶层汇总无 document 命名空间）。document 分片承载文档侧实测（编译时长/一致性自检计数等）。


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def main() -> int:
    root = project_root()
    merged: dict = {"_generated_at": datetime.datetime.now().isoformat(timespec="seconds")}
    found = []
    for role in FRAGMENTS:
        frag = root / "workspace" / role / "metrics.json"
        if not frag.is_file():
            continue
        try:
            data = json.loads(frag.read_text(encoding="utf-8"))
        except Exception as e:  # noqa: BLE001
            print(f"[merge_metrics][warn] {role} 分片解析失败，跳过: {e}", file=sys.stderr)
            continue
        merged[role] = data
        found.append(role)

    out = root / "workspace" / "metrics.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(merged, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[merge_metrics] 分片 {found or '无'} → 汇总 {out.relative_to(root)}（角色禁写，仅本脚本生成）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
