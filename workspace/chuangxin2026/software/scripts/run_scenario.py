#!/usr/bin/env python3
"""验收入口：python scripts/run_scenario.py --scenario scenarios/gb42590_noise.yaml（R5/sw-loop/sw-gb42590）。"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from linkbench.runner.runner import run_scenario  # noqa: E402


def main() -> int:
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    res = run_scenario(args[-1] if args[0] == "--scenario" else args[0])
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
