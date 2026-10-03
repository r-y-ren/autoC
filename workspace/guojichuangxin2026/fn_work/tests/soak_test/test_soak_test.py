"""soak_test 单测（--quick 微缩长跑）。"""
from __future__ import annotations


def test_quick_soak(tmp_path):
    from soak_test.soak_test import soak_test
    r = soak_test(quick=True)
    assert r["sessions"] >= 3 and r["ok"] is True
    assert r["frames_total"] >= 3 * 15
    from pathlib import Path
    assert Path(r["report"]).exists()
    Path(r["report"]).unlink()
