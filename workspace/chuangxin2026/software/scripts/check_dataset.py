#!/usr/bin/env python3
"""验收入口：python scripts/check_dataset.py runs/（R6/sw-dataset）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linkbench.dataset.indexer import check_dataset  # noqa: E402


def main() -> int:
    runs_dir = sys.argv[1] if len(sys.argv) > 1 else "runs/"
    idx = check_dataset(runs_dir)
    print(idx)
    return 0 if not idx.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
