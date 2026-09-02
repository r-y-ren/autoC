#!/usr/bin/env python3
"""多战役状态共享库（v2 状态模型，2026-09-01）。

被 guard_path.py（PreToolUse 钩子，每次写入都跑）、init_state.py、
session_status.py 与 scripts/verify/* 共用。stdlib-only，无第三方依赖。

## v2 状态模型（.flow/state.json）

{
  "schema_version": 2,
  "phase": "idle",              # 全局阶段（慢循环/工程态）：idle | collect
  "campaigns": {                # 战役注册表：多战役并行的核心
    "<cid>": {
      "phase": "deliver",       # 战役阶段：decide | deliver | verify | archive | idle
      "root": "workspace",      # 战役根（legacy 平铺战役=workspace；新战役=workspace/<cid>）
      "retry": {"count":0,"max":3,"tripped":false},
      "extra_allow": [],
      "created_at": "...", "updated_at": "...", "updated_by": "..."
    }
  }
}

v1（schema_version 1，顶层单 phase）按 legacy 平铺语义兼容读取：
root 恒为 workspace，retry 在顶层——升级由 init_state --campaign 完成。

## 路由规则（守卫与 verify 脚本一致）

写入/操作 workspace 子树时按**最长 root 匹配**定位所属战役：
  workspace/software/x.py  → legacy 战役（root=workspace）
  workspace/<cid>/x.py     → 该 cid 战役（root=workspace/<cid>，更长优先）
工程目录（config/scripts/docs/.zcode/kb/export）只归全局 phase 管。
"""

from __future__ import annotations

import datetime
import json
import re
from pathlib import Path

CAMPAIGN_PHASES = ["decide", "deliver", "verify", "archive", "idle"]
GLOBAL_PHASES = ["idle", "collect"]
# 战役活跃阶段（D14 圈禁判定，2026-09-02）：任一战役处于这些阶段时，
# 全局 idle 对工程目录/项目根锁定（战役产物圈禁在所属战役根，见 guard_path.decide_v2）
ACTIVE_CAMPAIGN_PHASES = ("decide", "deliver", "verify", "archive")
CAMPAIGN_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,31}$")
# legacy 平铺战役占用 workspace 顶层的名字，不得用作新战役 id
RESERVED_CAMPAIGN_IDS = {
    "software", "hardware", "docs", "document", "acceptance", "references",
    "strategy.md", "blueprint.md", "journal.md", "metrics.json", "readme.md",
}


def state_file(root: Path) -> Path:
    return root / ".flow" / "state.json"


def load_state(root: Path) -> dict | None:
    try:
        st = json.loads(state_file(root).read_text(encoding="utf-8"))
        return st if isinstance(st, dict) else None
    except Exception:  # noqa: BLE001
        return None


def save_state(root: Path, state: dict) -> None:
    sf = state_file(root)
    sf.parent.mkdir(parents=True, exist_ok=True)
    sf.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_v2(state: dict | None) -> bool:
    return isinstance(state, dict) and isinstance(state.get("campaigns"), dict)


def campaigns(state: dict | None) -> dict:
    """v2 返回注册表；v1 返回空 dict（legacy 语义由 resolve 另行处理）。"""
    return state.get("campaigns") if is_v2(state) else {}


def active_campaigns(state: dict | None) -> dict:
    """处于活跃阶段（decide/deliver/verify/archive）的战役 {cid: camp}（仅 v2）。"""
    return {cid: c for cid, c in campaigns(state).items()
            if isinstance(c, dict) and c.get("phase") in ACTIVE_CAMPAIGN_PHASES}


def default_retry_max(root: Path) -> int | None:
    """retry.max 单一事实来源：config/budget.yaml → circuit_breaker.repair_max_retries。"""
    try:
        import yaml
        cfg = yaml.safe_load((root / "config" / "budget.yaml").read_text(encoding="utf-8"))
        return int((((cfg or {}) or {}).get("circuit_breaker") or {}).get("repair_max_retries"))
    except Exception:  # noqa: BLE001
        return None


def fresh_retry(root: Path) -> dict:
    m = default_retry_max(root)
    return {"count": 0, "max": m if m is not None else 3, "tripped": False}


def sync_retry(root: Path, retry: dict) -> dict:
    """保留 count/tripped，max 跟随 budget 当前值（T-audit 备忘项闭合）。"""
    retry.setdefault("count", 0)
    retry.setdefault("tripped", False)
    live = default_retry_max(root)
    if live is not None:
        retry["max"] = live
    retry.setdefault("max", 3)
    return retry


def norm(rel: str) -> str:
    """相对路径标准化：小写 + 正斜杠（Windows 大小写不敏感）。"""
    return rel.replace("\\", "/").lower()


def under(rel: str, root: str) -> bool:
    """rel 是否位于 root 子树内（root 可为目录或具体文件）。"""
    root, rel = norm(root), norm(rel)
    return rel == root or rel.startswith(root + "/")


def match_campaign(state: dict, rel: str) -> tuple[str, dict, str] | None:
    """最长 root 匹配：返回 (cid, campaign_dict, rel 相对战役 root 的剩余路径)。

  仅 v2 有意义；v1/无匹配返回 None。
    """
    best: tuple[str, dict, str] | None = None
    best_len = -1
    for cid, camp in campaigns(state).items():
        if not isinstance(camp, dict) or not camp.get("root"):
            continue
        croot = norm(str(camp["root"]))
        nrel = norm(rel)
        if nrel == croot or nrel.startswith(croot + "/"):
            if len(croot) > best_len:
                rest = nrel[len(croot):].lstrip("/")
                best, best_len = (cid, camp, rest), len(croot)
    return best


def campaign_dir(root: Path, camp: dict) -> Path:
    """战役根的绝对路径。"""
    return (root / str(camp.get("root", "workspace"))).resolve()


def resolve_campaign(root: Path, state: dict | None, cid: str | None):
    """把 --campaign 参数解析为 (cid, campaign_dict)。

  - 显式 cid：v2 注册表必须含该战役；
  - 缺省 cid：v2 恰有一个战役时自动选中，多个时报错（返回错误信息）；
  - v1 状态：返回 legacy 伪战役（root=workspace，retry 引用顶层）——
    保证未迁移的仓库/测试夹具仍按平铺语义工作。
    返回 (cid, camp, error)；error 非空表示失败。
    """
    if not is_v2(state):
        if cid:
            return cid, {}, f"--campaign {cid} 需要 v2 状态（先运行 init_state --campaign {cid} ...）"
        return "(legacy)", {"phase": (state or {}).get("phase"), "root": "workspace"}, ""
    table = campaigns(state)
    if cid:
        camp = table.get(cid)
        if not isinstance(camp, dict):
            return cid, {}, f"未登记战役 {cid!r}（可用：{sorted(table) or '无'}；登记用 init_state --campaign {cid}）"
        return cid, camp, ""
    if len(table) == 1:
        return next(iter(table.items()))
    if not table:
        return None, {}, "当前无登记战役（新战役：init_state --campaign <cid> --phase decide）"
    return None, {}, f"多战役并存，必须显式 --campaign（可选：{sorted(table)}）"


def now_iso() -> str:
    return datetime.datetime.now().isoformat(timespec="seconds")
