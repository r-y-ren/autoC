"""TCN 训练 CLI：python train.py --data <目录...>。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="train")
    p.add_argument("--data", nargs="+", required=True)
    a = p.parse_args()
    from src.run_progressive_risk.train_tcn import train_tcn

    out = train_tcn(a.data, {})
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
