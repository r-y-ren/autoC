"""open_run_dir 单测。"""
from __future__ import annotations

import json

from shared.open_run_dir import open_run_dir


def test_creates_layout_and_manifest(tmp_path):
    d = open_run_dir(str(tmp_path), "motor_fail", seed=7, config_snapshot={"a": 1})
    assert d.is_dir() and (d / "raw").is_dir() and (d / "frames").is_dir()
    m = json.loads((d / "manifest.json").read_text(encoding="utf-8"))
    assert m["scenario"] == "motor_fail" and m["seed"] == 7
    assert m["config_snapshot"] == {"a": 1} and m["host"]["name"]


def test_same_second_collision_suffix(tmp_path, monkeypatch):
    a = open_run_dir(str(tmp_path), "s")
    b = open_run_dir(str(tmp_path), "s")
    assert a != b and b.name.endswith("+2")
