#!/usr/bin/env python3
"""验收入口：python scripts/eval_jamming_cls.py（R7/sw-ai：训练→分组 CV→预测并列真值）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linkbench.train.trainer import train_model  # noqa: E402


def main() -> int:
    data_dir = sys.argv[1] if len(sys.argv) > 1 else "runs/dataset_v1"
    res = train_model(data_dir, "models", backend="auto")
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
