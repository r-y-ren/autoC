#!/usr/bin/env python3
"""H-03 会话状态播报（SessionStart 钩子）。

向会话注入一行 additionalContext：全局阶段 + 各战役阶段/重试计数（熔断醒目提示）。
恒 exit 0；状态缺失时输出引导语而非报错（fail-closed 引导交给守卫）。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flow_state as fs  # noqa: E402


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def main() -> int:
    try:
        state = fs.load_state(project_root())
        if state is None:
            raise ValueError("no state")
        if fs.is_v2(state):
            parts = [f"全局={state.get('phase', '?')}"]
            camps = fs.campaigns(state)
            if not camps:
                parts.append("战役=无（新战役：init_state --campaign <id> --phase decide）")
            for cid, c in sorted(camps.items()):
                retry = c.get("retry") or {}
                trip = "⚠熔断" if retry.get("tripped") else ""
                parts.append(f"{cid}={c.get('phase', '?')}"
                             f"(重试{retry.get('count', 0)}/{retry.get('max', '-')}{trip})")
            msg = f"[autoC] {' '.join(parts)}（/status 查看详情；阶段流转只能经 init_state.py）"
        else:
            retry = state.get("retry") or {}
            trip = "[⚠ 熔断已触发：停止自动重试，升级人工]" if retry.get("tripped") else ""
            campaign = state.get("campaign")
            cname = campaign.get("name", "无") if isinstance(campaign, dict) else "无"
            msg = (f"[autoC] 当前阶段={state.get('phase', '?')} 战役={cname} "
                   f"重试={retry.get('count', 0)}/{retry.get('max', '-')} {trip} "
                   f"（v1 单战役状态；升级：init_state --campaign <id> --phase <p>）")
    except Exception:  # noqa: BLE001
        msg = "[autoC] 守卫状态缺失：运行 python scripts/guard/init_state.py 引导（在此之前写入守卫 fail-closed）"

    print(json.dumps({"additionalContext": msg}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
