"""批量评估 CLI（R2/R3/R4 验收）：python eval.py --scenario <名> --runs 30。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="eval")
    p.add_argument("--scenario", required=True)
    p.add_argument("--runs", type=int, default=30)
    p.add_argument("--seeds", default=None)
    a = p.parse_args()
    from src.shared.run_eval import run_eval

    out = run_eval(a.scenario, a.runs)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
