"""Exact-board manifest parsing and rollout-input contracts."""
from __future__ import annotations

import json
import os
import pathlib
import sys

os.environ.setdefault("JAX_PLATFORMS", "cpu")
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "S" / "actionrl"))

import live_manifest as LM  # noqa: E402
import numpy as np  # noqa: E402


def _layout(tmp_path, n=6, live="live250"):
    actionrl = tmp_path / "S/actionrl"
    band3 = tmp_path / "S/band3"
    winjudge = tmp_path / "S/winjudge"
    tapes = tmp_path / "artifacts/tape_actions_town"
    for path in (actionrl, band3, winjudge, tapes):
        path.mkdir(parents=True, exist_ok=True)
    eps = [str(100 + i) for i in range(n)]
    (actionrl / f"{live}_ids.txt").write_text("".join(e + "\n" for e in eps))
    (band3 / f"{live}_epseat.txt").write_text(
        "".join(f"{e} {i % 2}\n" for i, e in enumerate(eps)))
    # Reverse sidecar order: joining by key, rather than position, is load
    # bearing for the LIVESEED format.
    (band3 / f"{live}_epseat.txt.seeds").write_text(
        "".join(f"{e} {1000 + i}\n" for i, e in reversed(list(enumerate(eps)))))
    towns = {e: [[3, "BAKERY"], [6, "PET_CAFE"]] for e in eps}
    (winjudge / f"town_{live}.json").write_text(json.dumps(towns))
    for e in eps:
        (tapes / f"{e}.npz").touch()
    return actionrl / f"{live}_ids.txt", eps


def test_band3_layout_is_joined_by_episode_and_keeps_chronology(tmp_path):
    ids, eps = _layout(tmp_path)
    rows = LM.load_manifest(ids)
    assert [r.ep for r in rows] == eps
    assert [r.seed for r in rows] == list(range(1000, 1000 + len(eps)))
    assert [r.our_seat for r in rows] == [1, 0, 1, 0, 1, 0]
    assert rows[0].town == ((3, "BAKERY"), (6, "PET_CAFE"))


def test_chronological_split_is_configurable_and_has_no_overlap(tmp_path):
    ids, _ = _layout(tmp_path)
    rows = LM.load_manifest(ids)
    train = LM.chronological_split(rows, 3, 2, 1, "train")
    dev = LM.chronological_split(rows, 3, 2, 1, "dev")
    sealed = LM.chronological_split(rows, 3, 2, 1, "sealed")
    assert [r.ep for r in train] == ["100", "101", "102"]
    assert [r.ep for r in dev] == ["103", "104"]
    assert [r.ep for r in sealed] == ["105"]
    assert not ({r.ep for r in train} & {r.ep for r in dev + sealed})


def test_one_tiny_recorded_seat_rollout_input(tmp_path):
    ids, _ = _layout(tmp_path)
    rows = LM.load_manifest(ids)
    theta = np.arange(7, dtype=np.float32)
    inp = LM.rollout_inputs(rows, theta, indices=[1], key_seed=9)
    assert inp.thetas.shape == (1, 2, 7)
    np.testing.assert_array_equal(inp.thetas[0, 0], theta)
    assert inp.words.shape[0:2] == (1, 30)
    assert inp.seats.tolist() == [0]       # opponent was recorded in seat 1
    assert inp.ctl.tolist() == [[1, 1]]    # tape table follows manifest index
    assert inp.keys.shape == (1, 2)


def test_live302_companions_and_explicit_split(tmp_path):
    ids, eps = _layout(tmp_path, n=302, live="live302")
    split = tmp_path / "S/actionrl/live302_split.json"
    split.write_text(json.dumps({"train": list(range(250)),
                                 "dev": list(range(250, 302))}))
    rows = LM.load_manifest(ids)
    assert len(rows) == 302
    assert len(LM.split_from_json(rows, split, "train")) == 250
    assert len(LM.split_from_json(rows, split, "dev")) == 52
    assert [r.ep for r in rows[:250]] == eps[:250]


def test_repo_live302_has_live250_prefix():
    live250 = (ROOT / "S/actionrl/live250_ids.txt").read_bytes()
    first250 = b"".join(
        (ROOT / "S/actionrl/live302_ids.txt").read_bytes().splitlines(keepends=True)[:250])
    assert first250 == live250
