"""批量评估总控 CLI：python batch_eval.py [--runs 30] [--scenarios ...]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="batch_eval")
    p.add_argument("--runs", type=int, default=30)
    p.add_argument("--scenarios", nargs="+", default=["lowbat_headwind", "motor_fail", "link_degrade"])
    a = p.parse_args()
    from src.batch_eval.batch_eval import batch_eval

    out = batch_eval(a.scenarios, a.runs)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
