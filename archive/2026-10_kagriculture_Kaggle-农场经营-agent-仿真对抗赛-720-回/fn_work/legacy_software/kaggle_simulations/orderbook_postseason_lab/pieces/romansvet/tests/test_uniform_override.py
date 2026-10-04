"""Focused tests for the board-independent LIVE250 override experiment."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ACTIONRL = ROOT / "S/actionrl"
sys.path.insert(0, str(ACTIONRL))
PATH = ACTIONRL / "uniform_override.py"
SPEC = importlib.util.spec_from_file_location("uniform_override", PATH)
UO = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = UO
SPEC.loader.exec_module(UO)


def test_requested_uniform_programs_are_exact():
    assert [v.name for v in UO.VARIANTS] == [f"U{i}" for i in range(1, 7)]
    assert [int(UO.program(v)[0].sum()) for v in UO.VARIANTS] == [15, 9, 50, 15, 15, 18]
    u4 = UO.program(UO.VARIANTS[3])
    assert set(u4[1][u4[0]].tolist()) == {6}  # v1 decode: 6 - 4 = +2
    u6_mask, u6_values = UO.program(UO.VARIANTS[5])
    assert np.all(u6_values[10:13, :5] == 8)
    assert np.all(u6_mask[10:13, 8]) and np.all(u6_values[10:13, 8] == 4)


def test_split_contract_and_paired_summary():
    assert UO.SPLITS == (("train", 0, 150), ("dev", 150, 200),
                         ("sealed", 200, 250), ("total", 0, 250))
    base = np.asarray([[90, 100], [110, 100], [120, 100]])
    final = np.asarray([[101, 100], [99, 100], [130, 100]])
    got = UO.summarize(base, final)
    assert (got["flips_plus"], got["flips_minus"], got["net"]) == (1, 1, 0)
    assert got["incumbent_wins"] == got["wins"] == 2
    assert got["delta_ours"] == got["delta_margin"]
    assert got["delta_theirs"] == 0


def test_all_live250_boards_resolve_in_chronological_order():
    boards = UO.select_all_boards()
    assert len(boards) == 250
    assert [b.game_index for b in boards] == list(range(250))
    assert boards[0].ep == "110946917"
    assert boards[-1].ep == "111567092"
