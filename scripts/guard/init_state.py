#!/usr/bin/env python3
"""引导/变更 .flow/state.json —— 守卫状态的唯一合法写入者。

用法（v2 多战役模型，2026-09-01 起）：
  # 全局阶段（慢循环/工程态）
  python scripts/guard/init_state.py                                  # 引导（不存在则创建 idle）
  python scripts/guard/init_state.py --phase collect                  # 慢循环收集态
  python scripts/guard/init_state.py --phase idle --reset             # 复位并清零重试计数

  # 战役级流转（多战役并行，各战役独立阶段）
  python scripts/guard/init_state.py --campaign <cid> --phase decide   # 登记/开工新战役
  python scripts/guard/init_state.py --campaign <cid> --phase deliver
  python scripts/guard/init_state.py --campaign <cid> --close          # 归档后注销战役

规则：
  - 全局 phase 合法值：idle | collect（v2 起全局不再承载战役阶段）
  - 战役 phase 合法值：decide | deliver | verify | archive | idle
  - campaign id：^[a-z0-9][a-z0-9-]{0,31}$，且不得占用 legacy 平铺目录名（RESERVED）
  - 新战役 root=workspace/<cid>（登记时创建骨架）；legacy 平铺战役 root=workspace
    （workspace/blueprint.md 在顶层即判定为 legacy）
  - v1 状态 + --campaign：自动升级 v2——顶层战役阶段与 retry 迁入该战役条目
  - retry 是战役级属性；--reset 只作用于目标战役（无 --campaign 时报错提示）

字段说明见 docs/DESIGN.md 第 4/6 节。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_state as fs  # noqa: E402

LEGACY_PHASES = ["decide", "deliver", "verify", "archive"]


def project_root() -> Path:
    import os
    env = os.environ.get("ZCODE_PROJECT_DIR") or os.environ.get("CLAUDE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


ROOT = project_root()
STATE_FILE = fs.state_file(ROOT)

SKELETON_DIRS = ["software", "hardware", "docs", "references", "acceptance"]
SKELETON_JOURNAL = "# 战役日志\n\n| 时间 | 阶段 | 动作 | 结果 |\n|---|---|---|---|\n"


def is_legacy_layout() -> bool:
    """workspace 顶层存在 blueprint.md 即 legacy 平铺战役（root=workspace）。"""
    return (ROOT / "workspace" / "blueprint.md").is_file()


def valid_cid(cid: str) -> str | None:
    if not fs.CAMPAIGN_RE.match(cid):
        return f"非法战役 id {cid!r}：须匹配 {fs.CAMPAIGN_RE.pattern}"
    if cid in fs.RESERVED_CAMPAIGN_IDS:
        return f"战役 id {cid!r} 与 legacy 平铺目录名冲突（保留名见 flow_state.RESERVED_CAMPAIGN_IDS）"
    return None


def ensure_campaign_dir(cid: str) -> Path:
    """新战役骨架：workspace/<cid>/{software,hardware,docs,references,acceptance} + JOURNAL.md。"""
    cdir = ROOT / "workspace" / cid
    cdir.mkdir(parents=True, exist_ok=True)
    for d in SKELETON_DIRS:
        (cdir / d).mkdir(exist_ok=True)
        (cdir / d / ".gitkeep").touch()
    journal = cdir / "JOURNAL.md"
    if not journal.exists():
        journal.write_text(SKELETON_JOURNAL, encoding="utf-8")
    return cdir


def upgrade_v1(state: dict, cid: str) -> dict:
    """v1 → v2：顶层战役阶段与 retry 迁入 campaigns[cid]，全局复位 idle。

    root 判定：workspace/blueprint.md 在顶层 → legacy（root=workspace），
    否则视为新战役（root=workspace/<cid>，并建骨架）。
    """
    legacy = is_legacy_layout()
    camp = {
        "phase": state.get("phase") if state.get("phase") in LEGACY_PHASES else "idle",
        "root": "workspace" if legacy else f"workspace/{cid}",
        "retry": state.get("retry") or fs.fresh_retry(ROOT),
        "extra_allow": state.get("extra_allow") or [],
        "created_at": fs.now_iso(),
        "updated_at": fs.now_iso(),
        "updated_by": "init_state(v1→v2)",
    }
    state = {
        "schema_version": 2,
        "phase": "idle",
        "campaigns": {cid: camp},
    }
    if not legacy:
        ensure_campaign_dir(cid)
    return state


def main() -> int:
    ap = argparse.ArgumentParser(description="contest-compass 守卫状态引导/流转（v2 多战役）")
    ap.add_argument("--phase", default=None,
                    help="目标阶段：全局 idle|collect；带 --campaign 时 decide|deliver|verify|archive|idle")
    ap.add_argument("--campaign", default=None, help="目标战役 id（多战役并行时逐战役流转）")
    ap.add_argument("--close", action="store_true", help="注销该战役（归档后清理注册表条目）")
    ap.add_argument("--reset", action="store_true", help="清零重试计数与熔断标记")
    ap.add_argument("--by", default="manual", help="变更来源记录（命令名/角色名）")
    args = ap.parse_args()

    if args.campaign:
        err = valid_cid(args.campaign)
        if err:
            print(f"[init_state] {err}", file=sys.stderr)
            return 2

    state = fs.load_state(ROOT)
    if state is None:
        state = {"schema_version": 1, "phase": "idle", "campaign": None,
                 "extra_allow": [], "retry": fs.fresh_retry(ROOT)}

    if args.campaign and args.close:
        if not fs.is_v2(state):
            print("[init_state] v1 状态无战役注册表，--close 无需执行", file=sys.stderr)
            return 2
        if args.campaign not in fs.campaigns(state):
            print(f"[init_state] 战役 {args.campaign!r} 不存在", file=sys.stderr)
            return 2
        del state["campaigns"][args.campaign]
        state["updated_at"] = fs.now_iso()
        state["updated_by"] = f"{args.by}(close)"
        fs.save_state(ROOT, state)
        print(f"[init_state] 战役 {args.campaign} 已注销；剩余战役：{sorted(fs.campaigns(state)) or '无'}")
        return 0

    # ---- 战役级流转 ----
    if args.campaign:
        if not fs.is_v2(state):
            state = upgrade_v1(state, args.campaign)
            print(f"[init_state] v1→v2 升级：战役 {args.campaign} root={state['campaigns'][args.campaign]['root']}")
        camp = state["campaigns"].setdefault(args.campaign, {
            "phase": "idle",
            "root": f"workspace/{args.campaign}",
            "retry": fs.fresh_retry(ROOT),
            "extra_allow": [],
            "created_at": fs.now_iso(),
        })
        if args.phase:
            if args.phase not in fs.CAMPAIGN_PHASES:
                print(f"[init_state] 战役阶段合法值：{fs.CAMPAIGN_PHASES}（idle|collect 属全局）", file=sys.stderr)
                return 2
            camp["phase"] = args.phase
        # 新战役登记时确保骨架存在（幂等；legacy root=workspace 除外）
        if camp.get("root", "").startswith("workspace/") and args.phase == "decide":
            ensure_campaign_dir(args.campaign)
        camp["retry"] = (fs.fresh_retry(ROOT) if args.reset
                         else fs.sync_retry(ROOT, camp.get("retry") or {}))
        camp["updated_at"] = fs.now_iso()
        camp["updated_by"] = args.by
        state["updated_at"] = fs.now_iso()
        state["updated_by"] = args.by
        fs.save_state(ROOT, state)
        print(f"[init_state] campaign={args.campaign} phase={camp['phase']} "
              f"root={camp['root']} by={args.by}")
        return 0

    # ---- 全局流转（无 --campaign）----
    if args.phase and args.phase in LEGACY_PHASES:
        hint = "，或用 --campaign <cid> 作用于具体战役" if fs.is_v2(state) else \
            "（v1 单战役状态；升级：init_state --campaign <id> --phase <p>）"
        print(f"[init_state] v2 全局阶段只有 idle|collect；{args.phase} 是战役阶段{hint}", file=sys.stderr)
        return 2
    if args.reset and fs.is_v2(state):
        print("[init_state] --reset 需要 --campaign <cid>（retry 是战役级属性）", file=sys.stderr)
        return 2

    if args.phase:
        state["phase"] = args.phase
    if args.reset or not state.get("retry"):
        state["retry"] = fs.fresh_retry(ROOT)
    elif isinstance(state.get("retry"), dict):
        state["retry"] = fs.sync_retry(ROOT, state["retry"])
    state["updated_at"] = fs.now_iso()
    state["updated_by"] = args.by
    fs.save_state(ROOT, state)
    camp_note = ""
    if fs.is_v2(state) and fs.campaigns(state):
        camp_note = "；战役：" + ", ".join(
            f"{cid}={c.get('phase')}" for cid, c in sorted(fs.campaigns(state).items()))
    print(f"[init_state] 全局 phase={state.get('phase')} by={args.by}{camp_note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
