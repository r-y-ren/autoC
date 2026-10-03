"""材料构建 CLI：python materials.py --runs <目录...>。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="materials")
    p.add_argument("--runs", nargs="+", required=True)
    a = p.parse_args()
    from src.build_materials.build_materials import build_materials

    out = build_materials(a.runs, {})
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
