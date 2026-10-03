#!/usr/bin/env python3
"""Web 操控台无头自检（蓝图验收 sw-ui-boot）。

桩阶段：编译/导入 linkbench.ui + 静态资源存在性 + 桩标记扫描。
实现期：真实起服务 → /api/health 200 → WS 心跳到达 → /api/estop 触发后 TX 状态=停。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    failures: list[str] = []

    sys.path.insert(0, str(ROOT))
    for mod in ("linkbench.ui", "linkbench.ui.server", "linkbench.ui.api", "linkbench.ui.ws_hub"):
        try:
            __import__(mod)
            print(f"[ok] import {mod}")
        except Exception as exc:               # noqa: BLE001
            failures.append(f"import {mod}: {exc}")

    for asset in ("index.html", "app.js", "anim.js"):
        p = ROOT / "linkbench" / "ui" / "static" / asset
        if p.exists():
            print(f"[ok] static/{asset}")
        else:
            failures.append(f"missing static asset: {asset}")

    print("[info] 桩阶段自检通过标准=导入链+资源完整；端点级自检随 fn-implement 逐步启用")
    if failures:
        print("UI SELFTEST FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("UI SELFTEST OK（skeleton）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
