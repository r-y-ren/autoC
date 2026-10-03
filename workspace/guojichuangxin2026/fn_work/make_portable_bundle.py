"""便携包 CLI：python make_portable_bundle.py [--out dist]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="make_portable_bundle")
    p.add_argument("--out", default="dist")
    a = p.parse_args()
    from src.make_portable_bundle.make_portable_bundle import make_portable_bundle

    print(make_portable_bundle(a.out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
