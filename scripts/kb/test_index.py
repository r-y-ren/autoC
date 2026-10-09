#!/usr/bin/env python3
"""S-12 build_index 回归测试：跑批记录多行 append-only 保留（T2.1 修复的 P1）。

正则惰性匹配会在数据行行首 "|" 处断开，3 行记录只剩 1 行；修复后必须全量保留。
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_ROOT = Path(__file__).resolve().parents[2]

INDEX_WITH_3_RUNS = """# KB 总索引（瘦协调者唯一入口）

> 说明行。

## KB-1 赛事库（交付物 1）

| ID | 赛事 | 方向 | 层级 | 状态 | 关键日期 | AI 政策 | 最近核验 | 条目路径 |
|---|---|---|---|---|---|---|---|---|
<!-- 暂无条目 -->

## KB-2 科技库（交付物 2）

| ID | 名称 | 领域 | 成熟度 | 比赛映射 | 发表 | 最近核验 |
|---|---|---|---|---|---|---|
<!-- 暂无条目 -->

## 跑批记录

| 日期 | 类型 | 新增 | 更新 | 隔离 | 说明 |
|---|---|---|---|---|---|
| 2026-08-20 | tech | 5 | 2 | 0 | 首跑 |
| 2026-08-21 | tech | 3 | 1 | 1 | 有一条隔离 |
| 2026-08-22 | comp | 2 | 0 | 0 | 赛事首批 |
"""


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="autoc_idx_test_"))
    try:
        # 只拷工程面：产物树（workspace/archive 等）与 .git 整拷会打爆 /tmp 配额（2026-10-09 回归实测）
        shutil.copytree(SRC_ROOT, tmp, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(
                            ".venv", "__pycache__", "node_modules", ".git",
                            "workspace", "archive", "export", "tools",
                            "my_LLM_valut", ".flow", ".tmp"))
        (tmp / "kb" / "INDEX.md").write_text(INDEX_WITH_3_RUNS, encoding="utf-8")
        env = dict(os.environ, ZCODE_PROJECT_DIR=str(tmp))
        p = subprocess.run([sys.executable, str(tmp / "scripts/kb/build_index.py")],
                           cwd=tmp, capture_output=True, text=True, env=env, timeout=60)
        text = (tmp / "kb" / "INDEX.md").read_text(encoding="utf-8")
        kept = [ln for ln in text.splitlines() if ln.startswith("| 2026-08-")]
        ok = p.returncode == 0 and len(kept) == 3 and "关键日期" in text
        print(f"{'PASS' if ok else 'FAIL'} 跑批记录多行保留：保留 {len(kept)}/3 行；表头含关键日期列={'关键日期' in text}")
        return 0 if ok else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
