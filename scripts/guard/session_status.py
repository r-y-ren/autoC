#!/usr/bin/env python3
"""H-03 会话状态播报（SessionStart 钩子）。

向会话注入一行 additionalContext：当前阶段/战役/重试计数（熔断醒目提示）。
恒 exit 0；状态缺失时输出引导语而非报错（fail-closed 引导交给守卫）。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


def project_root() -> Path:
    env = os.environ.get("ZCODE_PROJECT_DIR")
    return Path(env).resolve() if env else Path(__file__).resolve().parents[2]


def main() -> int:
    state_file = project_root() / ".flow" / "state.json"
    try:
        st = json.loads(state_file.read_text(encoding="utf-8"))
        retry = st.get("retry") or {}
        trip = "[⚠ 熔断已触发：停止自动重试，升级人工]" if retry.get("tripped") else ""
        msg = (f"[autoC] 当前阶段={st.get('phase', '?')} "
               f"战役={ (st.get('campaign') or {}).get('name', '无') if isinstance(st.get('campaign'), dict) else '无' } "
               f"重试={retry.get('count', 0)}/{retry.get('max', '-')} {trip} "
               f"（/status 查看详情；阶段流转只能经 init_state.py）")
    except Exception:  # noqa: BLE001
        msg = "[autoC] 守卫状态缺失：运行 python scripts/guard/init_state.py 引导（在此之前写入守卫 fail-closed）"

    print(json.dumps({"additionalContext": msg}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
