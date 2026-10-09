#!/usr/bin/env python3
"""S-18 契约版本一致性校验（升级票01 补全：脚本侧防错配，2026-09-16）。

比较工作区 config/contract_version.yaml 与上游分支（@{u}）同名文件的 schema_version：
  本地 < 上游 → 另一台机器已推进契约，先 pull 再开工（错配风险）
  本地 > 上游 → 本机契约未同步，commit 后 push
  相等/无上游/无 git → OK 或跳过
恒 exit 0（advisory；阻断语义由人执行 pull/push 决定）。用法：开工前手动运行，
或由 SessionStart 播报提示后运行。

多库拆分后口径（2026-10-09，spec r-y-ren/autoC#2）：契约版本只随**主库**（工作流面）走，
"上游"仅指主库上游分支；各项目仓库（workspace/<cid> 等）无契约文件，不参与本比对。
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def local_version() -> int | None:
    try:
        import yaml
        cfg = yaml.safe_load((ROOT / "config" / "contract_version.yaml").read_text(encoding="utf-8")) or {}
        return int(cfg.get("schema_version", 0))
    except Exception:  # noqa: BLE001
        return None


def upstream_version() -> int | None:
    def git(*args: str) -> str | None:
        try:
            r = subprocess.run(["git", "-C", str(ROOT), *args], capture_output=True, text=True, timeout=15)
            return r.stdout.strip() if r.returncode == 0 else None
        except Exception:  # noqa: BLE001
            return None

    if git("rev-parse", "--is-inside-work-tree") != "true":
        return None
    up = git("rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if not up or "HEAD" in up:
        print("[contract_check] 无上游分支，跳过远端比对")
        return None
    content = git("show", f"{up}:config/contract_version.yaml")
    if content is None:
        return None
    try:
        import yaml
        return int((yaml.safe_load(content) or {}).get("schema_version", 0))
    except Exception:  # noqa: BLE001
        return None


def main() -> int:
    lv = local_version()
    if lv is None:
        print("[contract_check] ⚠ 本地 config/contract_version.yaml 缺失或不可读")
        return 0
    uv = upstream_version()
    if uv is None:
        print(f"[contract_check] 本地契约 v{lv}（上游不可比，跳过）")
        return 0
    if lv < uv:
        print(f"[contract_check] ⚠ 本地 v{lv} < 上游 v{uv}——另一台机器已推进契约，先 git pull --rebase 再开工")
    elif lv > uv:
        print(f"[contract_check] ⚠ 本地 v{lv} > 上游 v{uv}——本机契约变更未同步，commit 后 git push")
    else:
        print(f"[contract_check] 契约一致 v{lv}（本地=上游）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
