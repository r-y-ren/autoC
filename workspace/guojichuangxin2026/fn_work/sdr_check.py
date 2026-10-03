"""R5 自检 CLI：python sdr_check.py（设备/带宽/帧率/占用率响应）。"""
from __future__ import annotations

from src.run_spectrum_monitor.sdr_check import sdr_check

if __name__ == "__main__":
    raise SystemExit(sdr_check())
