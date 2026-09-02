#!/usr/bin/env python3
"""S-07 守卫回归测试：Phase 0 冒烟场景固化 + v2 多战役路由（2026-09-01）。

在隔离的临时工程目录中运行 guard_path.py（经 ZCODE_PROJECT_DIR 指向），
不触碰真实 .flow/state.json。

用例两类：
  - phase 为 str：v1 单战役平铺状态（兼容层）
  - phase 为 dict：直接作为 state.json 内容（v2 多战役）
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

GUARD = Path(__file__).resolve().parents[2] / "scripts" / "guard" / "guard_path.py"


def v2(cid: str, cphase: str, root: str = None, gphase: str = "idle") -> dict:
    """构造 v2 状态：一个战役（默认 root=workspace/<cid>）。"""
    return {
        "schema_version": 2, "phase": gphase,
        "campaigns": {cid: {
            "phase": cphase, "root": root or f"workspace/{cid}",
            "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": [],
        }},
    }


LEGACY_KAGGRI = {
    "schema_version": 2, "phase": "idle",
    "campaigns": {
        "kaggriculture": {
            "phase": "deliver", "root": "workspace",
            "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": [],
        },
    },
}

# (state, 目标相对路径, 期望被拒?, 说明)
CASES = [
    # ---- v1 兼容（平铺）----
    ("idle",     "docs/test.md",                   False, "v1 idle 放行普通工程文件"),
    ("idle",     "archive/x.md",                   True,  "idle 也不允许写 archive/"),
    ("idle",     ".flow/state.json",               True,  "state.json 仅脚本可写"),
    ("collect",  "kb/competitions/cumcm/meta.md",  False, "v1 collect 放行 kb/"),
    ("collect",  "workspace/blueprint.md",         True,  "v1 collect 拒写 workspace/"),
    ("deliver",  "workspace/software/app.py",      False, "v1 deliver 放行 workspace/software/"),
    ("deliver",  "workspace/acceptance/r.json",    True,  "v1 deliver 拒写验收区"),
    ("deliver",  "workspace/metrics.json",         True,  "v1 deliver 拒写顶层 metrics.json"),
    ("verify",   "workspace/acceptance/r.json",    False, "v1 verify 放行验收区"),
    ("archive",  "workspace/software/app.py",      True,  "v1 archive 态全拒"),
    ("__none__", "docs/test.md",                   True,  "fail-closed：无状态全拒"),
    ("__none__", ".flow/tmp.txt",                  False, "fail-closed：仍放行 .flow/ 自身"),
    # ---- v2 单战役（新式 root=workspace/<cid>）----
    (v2("demo", "deliver"), "workspace/demo/software/app.py", False, "v2 deliver 放行本战役工程区"),
    (v2("demo", "deliver"), "workspace/demo/acceptance/r.json", True, "v2 deliver 拒写本战役验收区"),
    (v2("demo", "deliver"), "workspace/demo/metrics.json", True, "v2 deliver 拒写本战役汇总 metrics"),
    (v2("demo", "deliver"), "workspace/demo/references/data/lb.json", False, "v2 deliver 放行本战役参考资料区"),
    (v2("demo", "deliver"), "workspace/demo2/software/app.py", True, "v2 拒写未登记战役目录（即使全局 idle）"),
    (v2("demo", "deliver"), "kb/tech/x.md", True, "D14：战役活跃时全局 idle 不放行工程目录（kb 走 collect 批次）"),
    (v2("demo", "deliver"), "workspace/README.md", True, "D14：战役活跃时容器 README 锁定（仅无活跃战役的全局 idle 可维护）"),
    (v2("demo", "deliver", gphase="collect"), "workspace/README.md", True, "v2 collect 拒写容器 README"),
    # ---- D14 战役圈禁（2026-09-02）：活跃战役锁定工程面/项目根 ----
    (v2("demo", "deliver"), "docs/test.md", True, "D14：战役活跃拒写工程目录"),
    (v2("demo", "deliver"), "dataset.zip", True, "D14：战役活跃拒写项目根（含下载落盘）"),
    (v2("demo", "deliver"), "scripts/guard/x.py", True, "D14：战役活跃拒写 scripts/"),
    (v2("demo", "deliver"), ".flow/tmp.txt", False, "D14：圈禁期仍放行 .flow/**（state.json 另有不变量拒写）"),
    (v2("demo", "deliver"), ".flow/state.json", True, "D14：圈禁期 state.json 仍拒写（全局不变量优先）"),
    (v2("demo", "decide"), "workspace/demo/blueprint.md", False, "v2 decide 放行蓝图"),
    (v2("demo", "decide"), "workspace/demo/software/app.py", True, "v2 decide 拒写工程区"),
    (v2("demo", "verify"), "workspace/demo/acceptance/r.json", False, "v2 verify 放行验收区"),
    (v2("demo", "verify"), "workspace/demo/software/app.py", True, "v2 verify 拒写工程区"),
    (v2("demo", "archive"), "workspace/demo/software/app.py", True, "v2 archive 态全拒"),
    (v2("demo", "idle"), "workspace/demo/software/app.py", True, "v2 已登记未开工（idle）全拒"),
    (v2("demo", "idle"), "docs/test.md", False, "D14：无活跃战役时全局 idle 放行工程目录（工程自举态）"),
    (v2("demo", "deliver", gphase="collect"), "kb/raw/x.html", False, "v2 collect 放行 kb（与战役并行）"),
    (v2("demo", "deliver", gphase="collect"), "scripts/guard/x.py", True, "v2 collect 拒写工程目录"),
    # ---- v2 多战役并行 + legacy 最长匹配 ----
    ({**json.loads(json.dumps(LEGACY_KAGGRI)),
      "campaigns": {**LEGACY_KAGGRI["campaigns"],
                    "demo": {"phase": "verify", "root": "workspace/demo",
                             "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []}}},
     "workspace/software/app.py", False, "多战役：legacy root 覆盖平铺工程区（deliver）"),
    ({**json.loads(json.dumps(LEGACY_KAGGRI)),
      "campaigns": {**LEGACY_KAGGRI["campaigns"],
                    "demo": {"phase": "verify", "root": "workspace/demo",
                             "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []}}},
     "workspace/demo/acceptance/r.json", False, "多战役：新战役 verify 放行自己的验收区"),
    ({**json.loads(json.dumps(LEGACY_KAGGRI)),
      "campaigns": {**LEGACY_KAGGRI["campaigns"],
                    "demo": {"phase": "verify", "root": "workspace/demo",
                             "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []}}},
     "workspace/demo/software/app.py", True, "多战役：新战役 verify 拒写自己的工程区"),
    ({**json.loads(json.dumps(LEGACY_KAGGRI)),
      "campaigns": {**LEGACY_KAGGRI["campaigns"],
                    "demo": {"phase": "verify", "root": "workspace/demo",
                             "retry": {"count": 0, "max": 3, "tripped": False}, "extra_allow": []}}},
     "workspace/acceptance/run.json", True, "多战役：legacy 战役 deliver 拒写其验收区"),
    (LEGACY_KAGGRI, "workspace/README.md", True, "D14：legacy 战役活跃时容器 README 锁定（无活跃战役的全局 idle 才可维护）"),
]


def run_case(tmp: Path, state, rel: str) -> int:
    state_file = tmp / ".flow" / "state.json"
    if state_file.exists():
        state_file.unlink()
    if state != "__none__":
        payload = ({"schema_version": 1, "phase": state, "campaign": None,
                    "extra_allow": [], "retry": {"count": 0, "max": 3, "tripped": False}}
                   if isinstance(state, str) else state)
        state_file.parent.mkdir(parents=True, exist_ok=True)
        state_file.write_text(json.dumps(payload), encoding="utf-8")
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
        for state, rel, expect_deny, note in CASES:
            code = run_case(tmp, state, rel)
            denied = code == 2
            ok = denied == expect_deny and code in (0, 2)
            passed += ok
            label = state if isinstance(state, str) else "v2"
            mark = "PASS" if ok else "FAIL"
            print(f"{mark} [{label:9s}] {rel:42s} 期望{'拒' if expect_deny else '行'} "
                  f"实际 exit={code}  # {note}")
    print(f"[test_guard] {passed}/{len(CASES)} 通过")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
