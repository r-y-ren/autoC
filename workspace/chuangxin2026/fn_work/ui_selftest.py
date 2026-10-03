#!/usr/bin/env python3
# Web 操控台无头自检（蓝图验收 sw-ui-boot）——桩阶段：导入链+自检入口存在
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
fail = []
try:
    from src.serve_console.serve_console import serve_console
    assert callable(serve_console)
    print("[ok] import serve_console")
except Exception as exc:
    fail.append(f"import serve_console: {exc}")

if fail:
    print("UI SELFTEST FAIL:"); [print("  -", f) for f in fail]; sys.exit(1)
print("UI SELFTEST OK (skeleton)"); sys.exit(0)
