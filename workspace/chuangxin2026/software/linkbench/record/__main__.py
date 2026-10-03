"""CLI：python -m linkbench.record --dur 60 --scenario scenarios/smoke.yaml"""

from __future__ import annotations

import argparse


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="linkbench.record")
    p.add_argument("--dur", type=float, required=True)
    p.add_argument("--scenario", default="scenarios/smoke.yaml")
    args = p.parse_args(argv)
    from linkbench.record.recorder import record_run
    from linkbench.shared.scenario import load_scenario
    res = record_run(load_scenario(args.scenario), args.dur,
                     __import__("pathlib").Path("runs") / "manual")
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
