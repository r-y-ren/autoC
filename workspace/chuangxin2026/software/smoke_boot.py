#!/usr/bin/env python3
"""一键启动冒烟（蓝图验收 sw-boot）。

桩阶段（m0）检查项：
  1) Python >= 3.10
  2) linkbench 全包编译（compileall）
  3) 全部子模块可导入（重依赖均为惰性导入，缺失只告警不失败）
  4) scenarios/*.yaml 语法可解析（pyyaml）
  5) 桩标记统一性（unimplemented:fn: 锚点可 grep）
退出码：0=冒烟通过；1=失败（附原因）。
"""

from __future__ import annotations

import compileall
import importlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent           # software/
SUBPKGS = ["gen", "calibrate", "dut", "record", "runner", "dataset",
           "train", "predict", "demo", "report", "ui", "sitl", "instruments", "shared"]
REQUIRED_DEPS = ["yaml"]                          # 冒烟硬依赖（场景解析）
OPTIONAL_DEPS = ["numpy", "matplotlib", "serial", "sigmf",
                 "fastapi", "uvicorn", "websockets", "requests"]


def main() -> int:
    failures: list[str] = []

    if sys.version_info < (3, 10):
        failures.append(f"Python >= 3.10 required, got {sys.version.split()[0]}")

    print("[1/5] compileall linkbench ...")
    if compileall.compile_dir(str(ROOT / "linkbench"), quiet=1) is not True:
        failures.append("compileall failed")

    print("[2/5] import check ...")
    sys.path.insert(0, str(ROOT))
    import linkbench
    print(f"      linkbench {linkbench.__version__}")
    for sub in SUBPKGS:
        try:
            importlib.import_module(f"linkbench.{sub}")
        except Exception as exc:               # noqa: BLE001 —— 冒烟要报全量
            failures.append(f"import linkbench.{sub}: {exc}")

    print("[3/5] required deps ...")
    for dep in REQUIRED_DEPS:
        try:
            importlib.import_module(dep)
        except Exception as exc:               # noqa: BLE001
            failures.append(f"missing required dep '{dep}': {exc}  → pip install -r requirements.txt")

    print("[4/5] scenario fixtures ...")
    try:
        import yaml
        for yml in sorted((ROOT / "scenarios").glob("*.yaml")):
            yaml.safe_load(yml.read_text(encoding="utf-8"))
            print(f"      ok {yml.name}")
    except Exception as exc:                   # noqa: BLE001
        failures.append(f"scenario parse: {exc}")

    print("[5/5] stub markers ...")
    markers = sum(p.read_text(encoding="utf-8").count("unimplemented:fn:")
                  for p in (ROOT / "linkbench").rglob("*.py"))
    print(f"      unimplemented:fn: × {markers}")
    if markers == 0:
        failures.append("no stub markers found (skeleton invariant broken)")

    print("[info] optional deps status:")
    for dep in OPTIONAL_DEPS:
        try:
            importlib.import_module(dep)
            print(f"      ok   {dep}")
        except Exception:                      # noqa: BLE001
            print(f"      miss {dep}（实现期再装）")

    if failures:
        print("\nSMOKE BOOT FAIL:")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nSMOKE BOOT OK（桩阶段冒烟通过）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
