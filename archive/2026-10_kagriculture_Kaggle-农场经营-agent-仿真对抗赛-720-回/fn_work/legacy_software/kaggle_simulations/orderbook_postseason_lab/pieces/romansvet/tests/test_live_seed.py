"""Exact live seeds are keyed to episodes, never to list position."""
from __future__ import annotations

import csv
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
os.environ.setdefault("JAX_PLATFORMS", "cpu")
sys.path.insert(0, str(ROOT / "src"))
sys.path.append(str(ROOT / "scripts"))

import eval_vs_baselines as E  # noqa: E402


def test_live_seeds_follow_episode_ids_not_file_order(tmp_path):
    seeds = tmp_path / "live.seeds"
    seeds.write_text("# replay seeds\n222 17\n111 9\nunused 31\n")
    opponents = [
        "/tmp/opponent_tape_111/main.py",
        "/tmp/opponent_tape_222/main.py",
    ]
    got = E.seeds_from_file(seeds, opponents, games=1)
    assert [[int(seed) for seed in row] for row in got] == [[9], [17]]


@pytest.mark.parametrize("contents, message", [
    ("111 9\n111 10\n", "duplicate seed key"),
    ("111 nope\n", "invalid seed"),
    ("111 -1\n", "outside"),
    ("111\n", "expected KEY SEED"),
])
def test_bad_seed_files_fail_loudly(tmp_path, contents, message):
    seeds = tmp_path / "bad.seeds"
    seeds.write_text(contents)
    with pytest.raises(ValueError, match=message):
        E.seeds_from_file(seeds, ["/tmp/opponent_tape_111/main.py"], games=1)


def test_missing_episode_and_multiple_games_are_refused(tmp_path):
    seeds = tmp_path / "live.seeds"
    seeds.write_text("111 9\n")
    with pytest.raises(ValueError, match="missing seeds for 222"):
        E.seeds_from_file(seeds, ["/tmp/opponent_tape_222/main.py"], games=1)
    with pytest.raises(ValueError, match="requires --games 1"):
        E.seeds_from_file(seeds, ["/tmp/opponent_tape_111/main.py"], games=2)


def test_one_board_cli_uses_the_recorded_seed(tmp_path):
    """One real-engine board exercises argument parsing through CSV output."""
    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no smoke theta")
    seeds, output = tmp_path / "live.seeds", tmp_path / "out.csv"
    seeds.write_text("pass 2054568632\n")
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "eval_vs_baselines.py"),
         "--theta", str(theta), "--games", "1", "--seats", "1",
         "--opponents", "pass", "--workers", "1",
         "--seed-file", str(seeds), "--csv", str(output)],
        cwd=ROOT, check=True, timeout=600,
        env=dict(os.environ, JAX_PLATFORMS="cpu"))
    with output.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
    assert rows[0]["seed"] == "2054568632"
    assert rows[0]["opponent"] == "pass"

