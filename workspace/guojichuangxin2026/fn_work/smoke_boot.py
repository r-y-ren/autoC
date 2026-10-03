"""sw-boot 一键启动冒烟（scaffold 期=桩链编译自检+桩清单报告）。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    r = subprocess.run([sys.executable, "-m", "compileall", "-q", str(HERE / "src")])
    src_files = [p for p in (HERE / "src").rglob("*.py") if p.name != "__init__.py"]
    stubs = [p for p in src_files if "unimplemented:fn:" in p.read_text(encoding="utf-8")]
    print(f"[smoke_boot] compile rc={r.returncode}；桩 {len(stubs)}/{len(src_files)}（实现期清零）")
    return r.returncode


if __name__ == "__main__":
    raise SystemExit(main())
