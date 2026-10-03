"""probe_px4_env 单测。"""
from __future__ import annotations


def test_missing_px4_dir_not_ready():
    from batch_eval.probe_px4_env import probe_px4_env
    r = probe_px4_env({"px4_dir": ""})
    assert r["ready"] is False and any("px4_dir" in m for m in r["missing"])


def test_ready_path_with_fake_tree(tmp_path, monkeypatch):
    import shutil as sh
    from batch_eval.probe_px4_env import probe_px4_env
    (tmp_path / "Makefile").write_text("all:\n", encoding="utf-8")
    monkeypatch.setattr(sh, "which", lambda c: "/usr/bin/" + c if c != "bogus" else None)
    r = probe_px4_env({"px4_dir": str(tmp_path)})
    assert r["ready"] is True
