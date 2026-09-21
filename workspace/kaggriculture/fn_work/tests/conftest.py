"""fn_work 测试引导：把 fn_work/src 与仓库根插入 sys.path。

src 供桩模块导入；仓库根供后续跨 import 旧树判据使用（fn-implement 期）。路径按 __file__ 上溯
程序化发现（R20 语义：不写字面战役路径、不做仓根 CWD 假设）。
"""

import sys
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
SRC_DIR = TESTS_DIR.parent / "src"


def _find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").is_file() or (candidate / ".git").exists():
            return candidate
    raise RuntimeError("repo root not found upward from " + str(start))


REPO_ROOT = _find_repo_root(TESTS_DIR)

for _path in (str(SRC_DIR), str(REPO_ROOT)):
    if _path not in sys.path:
        sys.path.insert(0, _path)
