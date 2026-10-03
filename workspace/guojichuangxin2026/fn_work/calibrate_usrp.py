"""B210 标定 CLI：python calibrate_usrp.py [--mode dryrun|device]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="calibrate_usrp")
    p.add_argument("--mode", default="dryrun", choices=["dryrun", "device"])
    a = p.parse_args()
    from src.calibrate_usrp.calibrate_usrp import calibrate_usrp

    print(calibrate_usrp(a.mode))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
