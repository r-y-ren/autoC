"""The submission package must stay a deterministic product of the sources.

Multi-module era (v13.1+): `build.py --check` rebuilds the tar.gz in
memory, byte-compares it with the on-disk archive and re-runs the
structural checks (cross-module duplicate-name precheck, `agent` as
main.py's final def, 64-byte submission marker).  main.py is a thin
loader -- no build step is needed after editing src/*; packaging is only
for submission.
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


def test_package_members_are_exactly_entry_nine_modules_and_planner():
    """P3 (2026-09-19, layout pkg.2-dtsp): members = main.py + src/ nine
    modules + planner/ six files (fixed order) + the fingerprint-verified
    planner/scene/ pair.  Packaging contract details (scene sha256 against
    the P1 registration, size cap, determinism) are pinned by
    tests/test_p3_integration.py::TestPackaging."""
    import tarfile
    archive = SOFTWARE / "kaggle_simulations" / "agent" / "submission.tar.gz"
    with tarfile.open(archive) as tf:
        names = sorted(tf.getnames())
    assert names == sorted(
        ["main.py"] + [f"src/{m}.py" for m in (
            "constants", "telemetry", "observer", "strategy", "mission",
            "solver", "executor", "market", "entry")]
        + [f"planner/{p}" for p in (
            "__init__.py", "twin.py", "plans.py", "opponents.py",
            "select.py", "runtime.py")]
        + ["planner/scene/kaggriculture.py",
           "planner/scene/kaggriculture.json"])
