"""打包 CLI：python build_package.py [--out dist] [--skip-build]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="build_package")
    p.add_argument("--out", default="dist")
    p.add_argument("--skip-build", action="store_true")
    a = p.parse_args()
    from src.build_package.build_package import build_package

    print(build_package(a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
