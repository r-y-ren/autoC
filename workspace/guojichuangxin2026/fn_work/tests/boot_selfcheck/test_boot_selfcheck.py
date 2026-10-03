"""boot_selfcheck 单测（三步微缩版）。"""
from __future__ import annotations


def test_three_steps_pass(tmp_path):
    from boot_selfcheck.boot_selfcheck import boot_selfcheck
    report = boot_selfcheck({"runs_root": str(tmp_path), "port": 8792})
    assert report["steps"]["session"]["pass"]
    assert report["steps"]["service"]["pass"]
    assert report["steps"]["replay"]["pass"]
    assert report["pass"] is True
