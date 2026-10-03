"""CLI：python -m linkbench.dataset --check runs/"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.dataset")
    p.add_argument("--check", required=True)
    args = p.parse_args(argv)
    from linkbench.dataset.indexer import check_dataset
    idx = check_dataset(args.check)
    print(idx)
    return 0 if not idx.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
