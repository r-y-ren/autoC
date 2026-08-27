#!/usr/bin/env python3
"""S-07 守卫回归测试：把 Phase 0 的冒烟场景固化为可重复执行的测试。

在隔离的临时工程目录中运行 guard_path.py（经 ZCODE_PROJECT_DIR 指向），
不触碰真实 .flow/state.json。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / "scripts" / "guard" / "guard_path.py"

# (phase, 目标相对路径, 期望被拒?, 说明)  phase="__none__" 表示不写状态文件
CASES = [
    ("idle",     "docs/test.md",                   False, "idle 放行普通工程文件"),
    ("idle",     "archive/x.md",                   True,  "idle 也不允许写 archive/"),
    ("idle",     ".flow/state.json",               True,  "state.json 仅脚本可写"),
    ("collect",  "kb/competitions/cumcm/meta.md",  False, "collect 放行 kb/competitions/"),
    ("collect",  "kb/raw/x.html",                  False, "collect 放行 kb/raw/"),
    ("collect",  "workspace/blueprint.md",         True,  "collect 拒写 workspace/"),
    ("deliver",  "workspace/software/app.py",      False, "deliver 放行 workspace/software/"),
    ("deliver",  "workspace/acceptance/r.json",    True,  "deliver 拒写验收区（角色边界）"),
    ("deliver",  "kb/tech/x.md",                   True,  "deliver 拒写 kb/"),
    ("deliver",  "workspace/metrics.json",         True,  "deliver 拒写顶层 metrics.json（分片汇总生成物）"),
    ("deliver",  "workspace/software/metrics.json", False, "deliver 放行角色指标分片"),
    ("verify",   "workspace/acceptance/r.json",    False, "verify 放行验收区"),
    ("verify",   "workspace/software/app.py",      True,  "verify 拒写工程区"),
    ("archive",  "workspace/software/app.py",      True,  "archive 态全拒（归档走脚本）"),
    ("__none__", "docs/test.md",                   True,  "fail-closed：无状态全拒"),
    ("__none__", ".flow/tmp.txt",                  False, "fail-closed：仍放行 .flow/ 自身"),
]


def run_case(tmp: Path, phase: str, rel: str) -> int:
    state_file = tmp / ".flow" / "state.json"
    if state_file.exists():
        state_file.unlink()
    if phase != "__none__":
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps({
            "schema_version": 1, "phase": phase, "campaign": None,
            "extra_allow": [], "retry": {"count": 0, "max": 3, "tripped": False},
        }), encoding="utf-8")
    payload = json.dumps({
        "tool_name": "Write",
        "tool_input": {"file_path": str((tmp / rel).resolve())},
    })
    env = dict(os.environ, ZCODE_PROJECT_DIR=str(tmp))
    proc = subprocess.run(
        [sys.executable, str(GUARD)], input=payload, capture_output=True,
        text=True, env=env, timeout=15)
    return proc.returncode


def main() -> int:
    passed = 0
    with tempfile.TemporaryDirectory(prefix="autoc_guard_test_") as td:
        tmp = Path(td)
        for phase, rel, expect_deny, note in CASES:
            code = run_case(tmp, phase, rel)
            denied = code == 2
            ok = denied == expect_deny and code in (0, 2)
            passed += ok
            mark = "PASS" if ok else "FAIL"
            print(f"{mark} [{phase or 'NO-STATE':9s}] {rel:38s} 期望{'拒' if expect_deny else '行'} "
                  f"实际 exit={code}  # {note}")
    print(f"[test_guard] {passed}/{len(CASES)} 通过")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
