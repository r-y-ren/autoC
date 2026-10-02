"""`--replay-dir` has to write games `scripts/replay_profile.py` can read.

The flag exists so a won/lost split can be profiled off the very games the
`--csv` scored, so the contract under test is not "a file appeared" but "the
profiler reads it and agrees with the CSV": our seat found by name, the same
final money, the same land. `env.toJSON()` is not quite a Kaggle replay --
`info` carries only the seed -- and the seat names the dump adds are the whole
of the difference, so a regression there is silent everywhere else.

One engine game, against `pass`, because the dump's shape does not depend on
who is in the other chair.
"""
from __future__ import annotations

import csv
import json
import os
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT / "scripts"))

import replay_profile as RP

#: What the CSV looked like before the flag existed; `--replay-dir` must not
#: touch it.
CSV_HEADER = ["seed", "opponent", "seat", "mine", "theirs",
              "moves", "move_turns", "noops", "unsold", "quads"]


@pytest.fixture(scope="module")
def dumped(tmp_path_factory):
    theta = ROOT / "artifacts" / "theta.npy"
    if not theta.exists():
        pytest.skip("no theta yet")
    d = tmp_path_factory.mktemp("replaydump")
    out, csv_path = d / "replays", d / "games.csv"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "eval_vs_baselines.py"),
         "--theta", str(theta), "--games", "1", "--opponents", "pass",
         "--workers", "2", "--seed-base", "7",
         "--csv", str(csv_path), "--replay-dir", str(out)],
        cwd=ROOT, check=True, timeout=600)
    with open(csv_path, newline="") as fh:
        rows = list(csv.DictReader(fh))
    return out, rows


def test_the_csv_is_the_csv_it_always_was(dumped):
    _, rows = dumped
    assert list(rows[0].keys()) == CSV_HEADER
    # Both seats of the one seed, as usual.
    assert sorted(r["seat"] for r in rows) == ["0", "1"]


def test_every_game_lands_in_the_directory_as_parseable_json(dumped):
    out, rows = dumped
    for r in rows:
        path = out / f"{r['seed']}_{r['seat']}.json"
        assert path.exists(), sorted(os.listdir(out))
        rep = json.loads(path.read_text())
        seat = int(r["seat"])
        assert rep["info"]["TeamNames"][seat] == "ours"
        assert rep["info"]["TeamNames"][1 - seat] == "pass"
        assert len(rep["steps"]) > 1 and len(rep["rewards"]) == 2


def test_the_profiler_reads_the_dump_and_agrees_with_the_csv(dumped):
    out, rows = dumped
    for r in rows:
        profiled = RP.profile_replay(str(out / f"{r['seed']}_{r['seat']}.json"), "ours")
        assert len(profiled) == 2
        ours = [p for p in profiled if p["ours"] == 1]
        assert len(ours) == 1 and ours[0]["seat"] == int(r["seat"])
        theirs = [p for p in profiled if p["ours"] == 0][0]
        assert ours[0]["final_money"] == pytest.approx(float(r["mine"]))
        assert theirs["final_money"] == pytest.approx(float(r["theirs"]))
        assert ours[0]["quads_end"] == int(float(r["quads"]))
