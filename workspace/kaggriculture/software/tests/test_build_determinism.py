"""The submission main.py must stay a deterministic product of agent/src/*.

Guards against hand edits drifting from the fragments: `build.py --check`
rebuilds in memory, byte-compares against the on-disk artifact and re-runs
the structural postchecks (stdlib-only imports, `agent` as the final
callable, cross-module duplicate-name precheck, disabled-scaffold
guarantee).  Run `python build.py` after editing src/* to resynchronise.
"""
import subprocess
import sys
from pathlib import Path

SOFTWARE = Path(__file__).resolve().parents[1]
BUILD = SOFTWARE / "kaggle_simulations" / "agent" / "build.py"
MAIN = SOFTWARE / "kaggle_simulations" / "agent" / "main.py"


def test_main_py_matches_deterministic_rebuild():
    result = subprocess.run(
        [sys.executable, str(BUILD), "--check"],
        capture_output=True, text=True, timeout=120,
    )
    assert result.returncode == 0, (
        f"build.py --check failed:\n{result.stdout}\n{result.stderr}")


def test_built_artifact_keeps_submission_marker():
    head = MAIN.read_bytes()[:256]
    assert b"Kaggriculture submission agent" in head
