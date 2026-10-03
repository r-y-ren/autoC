"""边缘基准 CLI：python bench_edge.py [--mode dryrun|deploy]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="bench_edge")
    p.add_argument("--mode", default="dryrun", choices=["dryrun", "deploy"])
    a = p.parse_args()
    from src.bench_edge.bench_edge import bench_edge

    print(bench_edge(a.mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
