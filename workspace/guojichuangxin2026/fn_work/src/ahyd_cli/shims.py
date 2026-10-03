"""console_scripts 垫片：demo/eval/replay-check/sdr-check 四入口。"""
from __future__ import annotations


def _boot_ok():
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2] if (Path(__file__).resolve().parents[2] / "src").exists() else Path.cwd()
    sys.path.insert(0, str(root / "src")) if (root / "src").exists() else None
    from boot_selfcheck.boot_selfcheck import boot_selfcheck
    r = boot_selfcheck()
    if not r["pass"]:
        raise SystemExit(f"boot 自检未过: {r}")


def demo_main() -> int:
    """ahyd-demo：三步自检→起平台服务。"""
    import argparse
    import sys
    from pathlib import Path
    p = argparse.ArgumentParser(prog="ahyd-demo")
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--skip-boot", action="store_true")
    a = p.parse_args()
    root = Path(__file__).resolve().parents[2]
    if (root / "src" / "run_ground_station").exists():
        sys.path.insert(0, str(root / "src"))
    if not a.skip_boot:
        _boot_ok()
    from run_ground_station.run_ground_station import run_ground_station
    run_ground_station({"port": a.port})
    return 0


def eval_main() -> int:
    import argparse
    p = argparse.ArgumentParser(prog="ahyd-eval")
    p.add_argument("--scenario", required=True)
    p.add_argument("--runs", type=int, default=30)
    a = p.parse_args()
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    if (root / "src" / "shared").exists():
        sys.path.insert(0, str(root / "src"))
    from shared.run_eval import run_eval
    print(run_eval(a.scenario, a.runs))
    return 0


def replay_main() -> int:
    import argparse
    p = argparse.ArgumentParser(prog="ahyd-replay-check")
    p.add_argument("--run", required=True)
    a = p.parse_args()
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    if (root / "src" / "run_ingest").exists():
        sys.path.insert(0, str(root / "src"))
    from run_ingest.replay_check import replay_check
    return replay_check(a.run)


def sdr_main() -> int:
    import sys
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    if (root / "src" / "run_spectrum_monitor").exists():
        sys.path.insert(0, str(root / "src"))
    from run_spectrum_monitor.sdr_check import sdr_check
    return sdr_check()
