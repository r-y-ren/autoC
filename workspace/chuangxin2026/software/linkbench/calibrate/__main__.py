"""CLI：python -m linkbench.calibrate"""

from __future__ import annotations


def main() -> int:
    from linkbench.calibrate.calibrate import run_calibration
    res = run_calibration(freq_hz_list=[2422000000], gain_list=[])
    print(res)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
