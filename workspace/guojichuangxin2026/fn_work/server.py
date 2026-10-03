"""地面平台服务入口（R7/R9）：python server.py [--port 8000]。"""
from __future__ import annotations

import argparse


def main() -> int:
    p = argparse.ArgumentParser(prog="server")
    p.add_argument("--port", type=int, default=8000)
    a = p.parse_args()
    from src.run_ground_station.run_ground_station import run_ground_station

    run_ground_station({"port": a.port})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
