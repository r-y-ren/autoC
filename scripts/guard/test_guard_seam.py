#!/usr/bin/env python3
"""S-19 守卫缝回归测试（升级票10/评审修复，2026-09-16）。

以构造 state 直接调 guard_path.decide()，钉住升级引入的战役阶段放行面：
  verify：acceptance/**、docs/**（K-12 /ppt 窗口）、JOURNAL.md（阶段记行）放行；其余拒
  decide：strategy/（票07 grill-notes）+ strategy.md/blueprint.md/JOURNAL.md 放行；近名路径拒
  deliver：specs/（票09 planner）放行；acceptance/metrics.json 仍拒
不变量：archive 拒、state.json 拒、未登记战役根拒。
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import guard_path as g  # noqa: E402


def state_with(phase: str) -> dict:
    return {"schema_version": 2, "phase": "idle",
            "campaigns": {"demo": {"phase": phase, "root": "workspace/demo"}}}


# (rel, phase, expect_allowed, note)
CASES = [
    ("workspace/demo/docs/ppt_brief.md", "verify", True, "verify docs/ 放行（K-12 简报）"),
    ("workspace/demo/docs/ppt/exports/x.pptx", "verify", True, "verify docs/ppt/ 深层子树放行"),
    ("workspace/demo/acceptance/r1.json", "verify", True, "verify acceptance 照旧"),
    ("workspace/demo/JOURNAL.md", "verify", True, "verify JOURNAL.md 记行放行（review-fix）"),
    ("workspace/demo/software/x.py", "verify", False, "verify software/ 仍拒"),
    ("workspace/demo/blueprint.md", "verify", False, "verify 蓝图仍拒"),
    ("workspace/demo/strategy/grill-notes.md", "decide", True, "decide strategy/ 放行（票07）"),
    ("workspace/demo/strategy.md", "decide", True, "decide strategy.md 照旧"),
    ("workspace/demo/strategy-evil.md", "decide", False, "近名路径不误吞"),
    ("workspace/demo/software/x.py", "decide", False, "decide software 仍拒"),
    ("workspace/demo/specs/tickets.md", "deliver", True, "deliver specs/ 放行（票09 planner）"),
    ("workspace/demo/acceptance/r1.json", "deliver", False, "deliver acceptance 只读不变"),
    ("workspace/demo/metrics.json", "deliver", False, "deliver 顶层 metrics 汇总物禁写不变"),
    ("workspace/demo/x.md", "archive", False, "archive 全拒不变"),
    (".flow/state.json", "deliver", False, "state.json 永拒不变"),
    ("workspace/ghost/x.md", "deliver", False, "未登记战役根拒不变"),
]


def main() -> int:
    passed = 0
    for rel, phase, expect, note in CASES:
        ok, _ = g.decide(rel, state_with(phase))
        good = ok == expect
        passed += good
        print(f"{'PASS' if good else 'FAIL'} {rel:44s} [{phase}] 期望{'放行' if expect else '拒'} "
              f"实际{'放行' if ok else '拒'}  # {note}")
    print(f"[test_guard_seam] {passed}/{len(CASES)} 通过")
    return 0 if passed == len(CASES) else 1


if __name__ == "__main__":
    sys.exit(main())
