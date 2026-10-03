"""CLI：python -m linkbench.runner --scenario scenarios/gb42590_noise.yaml"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.runner")
    p.add_argument("--scenario", required=True)
    args = p.parse_args(argv)
    from linkbench.runner.runner import run_scenario
    res = run_scenario(args.scenario)
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
