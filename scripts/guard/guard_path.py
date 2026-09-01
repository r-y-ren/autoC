#!/usr/bin/env python3
"""L2 写入路径守卫（ZCode PreToolUse 钩子，stdlib-only）。

职责：按 .flow/state.json 声明的阶段，拦截越界的 Write/Edit 工具调用。
不管辖 Bash 写入（由 L3 git 审计兜底）；不校验内容（内容校验归 linter/schema）。

## v2 多战役策略表（2026-09-01，单一事实来源在本文件 + flow_state.py）

全局阶段（state.phase，慢循环/工程态）：
  idle     工程自举/开发态：除 archive/** 与 .flow/state.json 外放行
  collect  慢循环收集态：仅放行 kb/**

战役阶段（state.campaigns[<cid>].phase，按最长 root 匹配路由，可多战役并行）：
  decide   决策态：仅放行 <root>/{strategy.md, blueprint.md, JOURNAL.md}
  deliver  工程交付态：放行 <root>/** 但 <root>/acceptance/** 与 <root>/metrics.json 只读
  verify   验收态：仅放行 <root>/acceptance/**
  archive  归档态：全拒（归档由 scripts/verify/archive_campaign.py 经 Bash 执行）
  idle     已登记未开工：该战役子树全拒

全局不变量（任何阶段）：
  - archive/** 永远只读（归档不可变）
  - .flow/state.json 永远拒写（状态只属于脚本，见 init_state.py）
  - workspace/<未登记id>/** 拒写（战役目录只能经 init_state 登记/创建）

Fail-closed：state.json 缺失/损坏时仅放行 .flow/**（且不含 state.json）。
全新克隆的引导步骤：python scripts/guard/init_state.py

v1 兼容：无 campaigns 键的旧状态按单战役平铺策略处理（root 恒为 workspace），
保证未迁移仓库/历史测试夹具不失效；升级经 init_state --campaign。

约定：退出码 0=放行、2=阻断（原因写 stderr）、其他=错误；
stdin 为钩子输入 JSON：{"tool_name": "...", "tool_input": {"file_path": "..."} }。
项目根之外的写入不归本守卫管辖（放行）。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_state as fs  # noqa: E402

STATE_DENY = ".flow/state.json"
GLOBAL_DENY = ["archive"]
FAIL_CLOSED_ALLOW = [".flow"]

# 战役阶段策略：allow/deny 均相对战役 root（由调用方拼接）
CAMPAIGN_POLICY = {
    "decide": {"allow": ["strategy.md", "blueprint.md", "JOURNAL.md"]},
    # workspace/<cid>/metrics.json 是分片汇总生成物（merge_metrics.py 产出），角色禁写：
    # 角色只写 <root>/<role>/metrics.json 分片（K-03 前置项裁决，DESIGN §6.2）
    "deliver": {"allow": ["*"], "deny": ["acceptance", "metrics.json"]},
    "verify": {"allow": ["acceptance"]},
    "archive": {"allow": []},
    "idle": {"allow": []},
}

# v1 单战役平铺策略（root 恒为 workspace；仅兼容读取）
V1_POLICY = {
    "idle": {"allow": ["*"]},
    "collect": {"allow": ["kb"]},
    "decide": {"allow": ["workspace/strategy.md", "workspace/blueprint.md", "workspace/JOURNAL.md"]},
    "deliver": {"allow": ["workspace"], "deny": ["workspace/acceptance", "workspace/metrics.json"]},
    "verify": {"allow": ["workspace/acceptance"]},
    "archive": {"allow": []},
}

GLOBAL_POLICY = {
    "idle": {"allow": ["*"]},
    "collect": {"allow": ["kb"]},
}


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def decide(rel: str, state: dict | None) -> tuple[bool, str]:
    # 全局不变量
    if fs.under(rel, STATE_DENY):
        return False, "拒写 .flow/state.json：运行时状态只能由 scripts/guard/ 下的脚本变更"
    for d in GLOBAL_DENY:
        if fs.under(rel, d):
            return False, f"拒写 {d}/：该目录为不可变归档区/保护区"

    # fail-closed：无有效状态时仅放行 .flow/**
    if state is None:
        for a in FAIL_CLOSED_ALLOW:
            if fs.under(rel, a):
                return True, ""
        return False, "fail-closed：.flow/state.json 缺失或损坏，仅放行 .flow/**。请先运行 python scripts/guard/init_state.py"

    if fs.is_v2(state):
        return decide_v2(rel, state)

    # v1 兼容：单战役平铺
    phase = state.get("phase")
    policy = V1_POLICY.get(phase)
    if policy is None:
        return False, f"未知阶段 {phase!r}：拒绝（请用 init_state.py 修正状态）"
    return apply_policy(rel, policy, phase, extra_allow=state.get("extra_allow"))


def decide_v2(rel: str, state: dict) -> tuple[bool, str]:
    # 容器层例外优先于战役匹配：workspace/README.md 是容器文档而非战役产物
    # （legacy 战役 root=workspace 会整树吞掉，须在匹配前放行；仅全局 idle 可写）
    if rel == "workspace/readme.md":
        if state.get("phase") == "idle":
            return True, ""
        return False, "容器 README 仅全局 idle 可维护（慢循环/战役期锁工程层）"

    matched = fs.match_campaign(state, rel)
    if matched is not None:
        cid, camp, rest = matched
        phase = camp.get("phase")
        policy = CAMPAIGN_POLICY.get(phase)
        if policy is None:
            return False, f"战役 {cid} 阶段 {phase!r} 未知：拒绝（请用 init_state.py --campaign {cid} 修正）"
        ok, reason = apply_policy(rest, policy, f"campaign:{cid}/{phase}",
                                  extra_allow=camp.get("extra_allow"))
        if not ok:
            return ok, f"战役 {cid}（root={camp.get('root')}）：{reason}"
        return ok, reason

    # workspace 子树但未匹配任何战役 root：v2 下 workspace 只认战役注册表。
    if fs.under(rel, "workspace"):
        cids = sorted(fs.campaigns(state)) or "无"
        return False, (f"workspace 下未登记路径 {rel}：战役 {cids} 的 root 均不覆盖它。"
                       "新战役须先 python scripts/guard/init_state.py --campaign <id> --phase decide 登记"
                       "（legacy 平铺战役 root=workspace 全覆盖）")

    # 工程目录：只归全局 phase 管
    gphase = state.get("phase")
    gpolicy = GLOBAL_POLICY.get(gphase)
    if gpolicy is None:
        return False, f"未知全局阶段 {gphase!r}：拒绝（请用 init_state.py 修正状态）"
    return apply_policy(rel, gpolicy, gphase)


def apply_policy(rel: str, policy: dict, label: str, extra_allow=None) -> tuple[bool, str]:
    for d in policy.get("deny", []):
        if fs.under(rel, d):
            return False, f"{label} 下拒写 {d}（该子树属于其他角色/生成物）"
    allow = list(policy.get("allow", [])) + [str(a) for a in (extra_allow or [])]
    for a in allow:
        if a == "*" or fs.under(rel, a):
            return True, ""
    return False, f"{label} 的允许写根不包含 {rel}（策略见 scripts/guard/guard_path.py）"


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
        rel = fs.norm(os.path.relpath(abs_target, root))
    except ValueError:
        return 0  # 跨盘符等无法取相对路径的情况，不归本守卫管辖
    if rel.startswith(".."):
        return 0  # 项目根之外的写入不归本守卫管辖

    ok, reason = decide(rel, fs.load_state(root))
    if not ok:
        print(f"[guard_path] 阻断：{reason}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
