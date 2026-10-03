"""CLI：python -m linkbench.gen --scenario scenarios/smoke.yaml [--dry-run] [--run N]"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.gen")
    p.add_argument("--scenario", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--run", type=float, default=0.0, help="实际发射秒数（0=不发射）")
    p.add_argument("--out", default="runs")
    args = p.parse_args(argv)
    from linkbench.gen.generator import generate_interference
    from linkbench.shared.scenario import load_scenario
    sc = load_scenario(args.scenario)
    res = generate_interference(sc.injection, dry_run=args.dry_run or args.run <= 0,
                                out_dir=__import__("pathlib").Path(args.out))
    print(res)
    return 0 if res.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
