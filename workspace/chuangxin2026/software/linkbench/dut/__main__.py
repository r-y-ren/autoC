"""CLI：python -m linkbench.dut --watch 5 [--fake]"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.dut")
    p.add_argument("--watch", type=float, default=5.0)
    p.add_argument("--fake", action="store_true", help="无硬件合成数据模式")
    args = p.parse_args(argv)
    from linkbench.dut.collector import watch_links
    samples = watch_links(args.watch)
    print(f"samples={len(samples)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
