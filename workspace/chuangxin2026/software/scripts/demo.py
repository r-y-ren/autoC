#!/usr/bin/env python3
"""验收入口：python scripts/demo.py --quick（R8/sw-demo：一键演示，UI 演示卡片同底层）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linkbench.demo.demo import demo  # noqa: E402


def main() -> int:
    quick = "--full" not in sys.argv
    report = demo(quick=quick)
    print(f"report: {report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
