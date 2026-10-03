#!/usr/bin/env python3
"""双固件顺序编译（蓝图验收 hw-fw 入口）。

用法：python3 build_all.py
要求本机已装 PlatformIO Core（pio 在 PATH）；任一工程编译失败 → 退出码非 0。
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

PROJECTS = ["esp32_link", "nrf24_link"]


def main() -> int:
    pio = shutil.which("pio") or shutil.which("platformio")
    if pio is None:
        print("PlatformIO Core 未安装（pio 不在 PATH）——固件编译须在装有 PlatformIO 的机器执行")
        return 2
    here = Path(__file__).resolve().parent
    failed = []
    for proj in PROJECTS:
        print(f"=== pio run -d {proj} ===")
        rc = subprocess.call([pio, "run", "-d", str(here / proj)])
        if rc != 0:
            failed.append(proj)
    if failed:
        print(f"FIRMWARE BUILD FAIL: {failed}")
        return 1
    print("FIRMWARE BUILD OK（esp32_link + nrf24_link）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
