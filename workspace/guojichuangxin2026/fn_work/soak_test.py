"""长跑 CLI：python soak_test.py [--duration 3600] [--quick]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="soak_test")
    p.add_argument("--duration", type=float, default=3600.0)
    p.add_argument("--quick", action="store_true")
    a = p.parse_args()
    from src.soak_test.soak_test import soak_test

    print(soak_test(a.duration, a.quick))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
