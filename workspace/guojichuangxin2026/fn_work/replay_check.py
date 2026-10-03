"""R1 验收 CLI：python replay_check.py --run <运行目录>。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="replay_check")
    p.add_argument("--run", required=True)
    a = p.parse_args()
    from src.run_ingest.replay_check import replay_check

    return replay_check(a.run)


if __name__ == "__main__":
    raise SystemExit(main())
