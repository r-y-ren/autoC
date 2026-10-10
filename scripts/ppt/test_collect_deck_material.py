#!/usr/bin/env python3
"""PPT 取材器回归测试：fn-ladder 文件结构 → 内容简报 + 带来源标注的数据表。

seam：脚本命令行层 + 临时 fixture（spec #9 / issue#14 对齐）。正向=完整 fn 目录；
负向=缺文件降级点名、空实测标注、--strict 硬失败。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]
SCRIPT = "scripts/ppt/collect_deck_material.py"


def run_cm(proj: Path, *args: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(proj.parent))
    return subprocess.run([sys.executable, str(SRC_ROOT / SCRIPT), "--project", str(proj), *args],
                          capture_output=True, text=True, timeout=60, env=env)


def make_project(full: bool, empty_runs: bool = False) -> Path:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_cm_test_"))
    proj = tmp / "demo-camp"
    docs = proj / "fn_docs"
    (docs / "implementation").mkdir(parents=True)
    (docs / "README.md").write_text("零术语说明\n", encoding="utf-8")
    (docs / "requirements.md").write_text(
        "# 需求\n## R1 链路稳定\n内容\n## R2 功率可控\n内容\n", encoding="utf-8")
    (docs / "responsibility.md").write_text(
        "# 职责树\n- generate_style() 样式生成\n- execute_run() 运行\n", encoding="utf-8")
    (docs / "implementation" / "functions.md").write_text(
        "| 函数 | 状态 |\n|---|---|\n| generate_style | wired |\n| execute_run | tested |\n",
        encoding="utf-8")
    if full:
        (docs / "acceptance.md").write_text(
            "# 六道终检\n1. 编译：PASS\n2. 测试：PASS\n", encoding="utf-8")
        (docs / "results").mkdir()
        (docs / "results" / "2026-10-01-基线.json").write_text('{"per": 0.12}\n', encoding="utf-8")
    runs = proj / "fn_work" / "runs" / "demo"
    runs.mkdir(parents=True)
    if not empty_runs:
        (runs / "metrics.json").write_text('{"rssi_dbm": -70.5, "per": 0.12}\n', encoding="utf-8")
        (runs / "trace.log").write_text("throughput_mbps: 4.2\n", encoding="utf-8")
    else:
        (runs / "README.md").write_text("空跑\n", encoding="utf-8")
    return proj


def main() -> int:
    passed = 0

    # 正向：完整目录 → 四段素材 + 逐项来源
    proj = make_project(full=True)
    try:
        out = proj.parent / "out"
        p = run_cm(proj, "--out-dir", str(out))
        data = json.loads((out / "deck_material.json").read_text(encoding="utf-8"))
        goals = {g["id"] for g in data["goals"]}
        ok = p.returncode == 0 and {"R1", "R2"} <= goals
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 目标段提取：rc={p.returncode} goals={sorted(goals)}")

        funcs = {f["name"]: f["status"] for f in data["method"]["functions"]}
        ok = funcs == {"generate_style": "wired", "execute_run": "tested"}
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 方法段提取：{funcs}")

        measured = {(m["key"], m["value"]) for m in data["measured"]}
        srcs = {m["src"] for m in data["measured"]}
        ok = (("per", 0.12) in measured and ("rssi_dbm", -70.5) in measured
              and ("throughput_mbps", 4.2) in measured
              and any("metrics.json" in s for s in srcs) and any("trace.log" in s for s in srcs))
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 实测数据表带来源：{sorted(measured)} <- {sorted(srcs)}")

        ok = any("编译" in c["line"] for c in data["conclusion"]) and data["missing"] == []
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 结论段提取且零缺失：missing={data['missing']}")

        brief = (out / "deck_brief.md").read_text(encoding="utf-8")
        ok = all(h in brief for h in ("目标", "方法", "实测", "结论")) and "metrics.json" in brief
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 简报含四段与来源脚注")
    finally:
        import shutil
        shutil.rmtree(proj.parent, ignore_errors=True)

    # 负向：缺 acceptance/results → 降级点名；--strict 硬失败
    proj = make_project(full=False)
    try:
        out = proj.parent / "out"
        p = run_cm(proj, "--out-dir", str(out))
        data = json.loads((out / "deck_material.json").read_text(encoding="utf-8"))
        ok = p.returncode == 0 and any("acceptance.md" in m for m in data["missing"])
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 缺文件降级点名：rc={p.returncode} missing={data['missing']}")
        p2 = run_cm(proj, "--out-dir", str(out), "--strict")
        ok = p2.returncode == 1
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} --strict 硬失败：rc={p2.returncode}")
    finally:
        import shutil
        shutil.rmtree(proj.parent, ignore_errors=True)

    # 负向：空实测（runs 与 results 均无数据）→ 明确标注
    proj = make_project(full=False, empty_runs=True)
    try:
        out = proj.parent / "out"
        p = run_cm(proj, "--out-dir", str(out))
        data = json.loads((out / "deck_material.json").read_text(encoding="utf-8"))
        runs_empty = [m for m in data["missing"] if "实测" in m]
        ok = p.returncode == 0 and data["measured"] == [] and bool(runs_empty)
        passed += ok
        print(f"{'PASS' if ok else 'FAIL'} 空实测标注：missing={data['missing']}")
    finally:
        import shutil
        shutil.rmtree(proj.parent, ignore_errors=True)

    print(f"\n{passed}/8 PASS")
    return 0 if passed == 8 else 1


if __name__ == "__main__":
    sys.exit(main())
