#!/usr/bin/env python3
"""引导/变更 .flow/state.json —— 守卫状态的唯一合法写入者。

用法：
  python scripts/guard/init_state.py                 # 引导（不存在则创建 idle 状态）
  python scripts/guard/init_state.py --phase collect # 阶段流转（由阶段命令调用）
  python scripts/guard/init_state.py --phase idle --reset  # 复位并清零重试计数

字段说明见 docs/DESIGN.md 第 4/6 节；phase 合法值：
  idle | collect | decide | deliver | verify | archive
"""

from __future__ import annotations

import argparse
import json
import datetime
from pathlib import Path

PHASES = ["idle", "collect", "decide", "deliver", "verify", "archive"]

ROOT = Path(__file__).resolve().parents[2]
STATE_FILE = ROOT / ".flow" / "state.json"


def default_retry_max() -> int:
    """retry.max 单一事实来源：config/budget.yaml → circuit_breaker.repair_max_retries。"""
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "config" / "budget.yaml").read_text(encoding="utf-8"))
        return int((((cfg or {}) or {}).get("circuit_breaker") or {}).get("repair_max_retries"))
    except Exception:  # noqa: BLE001
        return 3


def fresh_retry() -> dict:
    return {"count": 0, "max": default_retry_max(), "tripped": False}


def main() -> int:
    ap = argparse.ArgumentParser(description="autoC 守卫状态引导/流转")
    ap.add_argument("--phase", default=None, choices=PHASES, help="目标阶段（缺省=保持/引导为 idle）")
    ap.add_argument("--reset", action="store_true", help="清零重试计数与熔断标记")
    ap.add_argument("--by", default="manual", help="变更来源记录（命令名/角色名）")
    args = ap.parse_args()

    state = None
    if STATE_FILE.exists():
        try:
            state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            state = None
    if not isinstance(state, dict):
        state = {"schema_version": 1, "phase": "idle", "campaign": None, "extra_allow": [],
                 "retry": fresh_retry()}

    if args.phase:
        state["phase"] = args.phase
    if args.reset or not state.get("retry"):
        state["retry"] = fresh_retry()
    state["updated_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    state["updated_by"] = args.by

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"[init_state] phase={state['phase']} by={args.by} -> {STATE_FILE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
