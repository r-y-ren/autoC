"""CLI：python -m linkbench.train --data runs/dataset_v1 --out models [--backend auto]"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.train")
    p.add_argument("--data", required=True)
    p.add_argument("--out", default="models")
    p.add_argument("--backend", default="auto", choices=["auto", "toolbox", "local"])
    args = p.parse_args(argv)
    from linkbench.train.trainer import train_model
    res = train_model(args.data, args.out, backend=args.backend)
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
