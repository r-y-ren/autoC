#!/usr/bin/env python3
"""L2 写入路径守卫（ZCode PreToolUse 钩子，stdlib-only）。

职责：按 .flow/state.json 声明的阶段，拦截越界的 Write/Edit 工具调用。
不管辖 Bash 写入（由 L3 git 审计兜底）；不校验内容（内容校验归 linter/schema）。

阶段策略表（单一事实来源在本文件）：
  idle     工程自举/开发态：除 archive/** 与 .flow/state.json 外放行
  collect  慢循环收集态：仅放行 kb/**
  decide   决策态：仅放行 workspace/{strategy.md, blueprint.md, JOURNAL.md}
  deliver  工程交付态：放行 workspace/** 但 workspace/acceptance/** 只读
  verify   验收态：仅放行 workspace/acceptance/**
  archive  归档态：全拒（归档由 scripts/verify/archive_campaign.py 经 Bash 执行）

全局不变量（任何阶段）：
  - archive/** 永远只读（归档不可变）
  - .flow/state.json 永远拒写（状态只属于脚本，见 init_state.py）

Fail-closed：state.json 缺失/损坏时仅放行 .flow/**（且不含 state.json）。
全新克隆的引导步骤：python scripts/guard/init_state.py

约定：退出码 0=放行、2=阻断（原因写 stderr）、其他=错误；
stdin 为钩子输入 JSON：{"tool_name": "...", "tool_input": {"file_path": "..."}}。
项目根之外的写入不归本守卫管辖（放行）。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

STATE_DENY = ".flow/state.json"
GLOBAL_DENY = ["archive"]
FAIL_CLOSED_ALLOW = [".flow"]


def norm(rel: str) -> str:
    """相对路径标准化：小写 + 正斜杠（Windows 大小写不敏感）。"""
    return rel.replace("\\", "/").lower()


def under(rel: str, root: str) -> bool:
    """rel 是否位于 root 子树内（root 可为目录或具体文件）。"""
    root = norm(root)
    rel = norm(rel)
    return rel == root or rel.startswith(root + "/")


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parents[2]


def load_state(root: Path) -> dict | None:
    try:
        with open(root / ".flow" / "state.json", encoding="utf-8") as f:
            state = json.load(f)
        if isinstance(state, dict) and state.get("phase"):
            return state
    except Exception:
        pass
    return None


def decide(rel: str, state: dict | None) -> tuple[bool, str]:
    # 全局不变量
    if under(rel, STATE_DENY):
        return False, "拒写 .flow/state.json：运行时状态只能由 scripts/guard/ 下的脚本变更"
    for d in GLOBAL_DENY:
        if under(rel, d):
            return False, f"拒写 {d}/：该目录为不可变归档区/保护区"

    # fail-closed：无有效状态时仅放行 .flow/**
    if state is None:
        for a in FAIL_CLOSED_ALLOW:
            if under(rel, a):
                return True, ""
        return False, "fail-closed：.flow/state.json 缺失或损坏，仅放行 .flow/**。请先运行 python scripts/guard/init_state.py"

    phase = state.get("phase")
    policy = {
        "idle": {"allow": ["*"]},
        "collect": {"allow": ["kb"]},
        "decide": {"allow": ["workspace/strategy.md", "workspace/blueprint.md", "workspace/JOURNAL.md"]},
        # workspace/metrics.json 是分片汇总生成物（merge_metrics.py 产出），角色禁写：
        # 角色只写 workspace/<role>/metrics.json 分片（K-03 前置项裁决，DESIGN §6.2）
        "deliver": {"allow": ["workspace"], "deny": ["workspace/acceptance", "workspace/metrics.json"]},
        "verify": {"allow": ["workspace/acceptance"]},
        "archive": {"allow": []},
    }.get(phase)
    if policy is None:
        return False, f"未知阶段 {phase!r}：拒绝（请用 init_state.py 修正状态）"

    for d in policy.get("deny", []):
        if under(rel, d):
            return False, f"阶段 {phase} 下拒写 {d}（该子树属于其他角色）"

    allow = list(policy["allow"]) + [str(a) for a in state.get("extra_allow", [])]
    for a in allow:
        if a == "*" or under(rel, a):
            return True, ""
    return False, f"阶段 {phase} 的允许写根不包含 {rel}（策略见 scripts/guard/guard_path.py）"


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0  # 无法解析的钩子输入不阻断工具

    file_path = (payload.get("tool_input") or {}).get("file_path")
    if not file_path:
        return 0  # 无文件路径的调用（如纯文本编辑器操作）不归本守卫管

    root = project_root()
    target = Path(file_path)
    abs_target = target.resolve() if target.is_absolute() else (root / target).resolve()
    try:
        rel = norm(os.path.relpath(abs_target, root))
    except ValueError:
        return 0  # 跨盘符等无法取相对路径的情况，不归本守卫管辖
    if rel.startswith(".."):
        return 0  # 项目根之外的写入不归本守卫管辖

    ok, reason = decide(rel, load_state(root))
    if not ok:
        print(f"[guard_path] 阻断：{reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
