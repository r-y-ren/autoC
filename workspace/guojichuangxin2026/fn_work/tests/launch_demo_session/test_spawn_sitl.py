"""spawn_sitl 单测（synthetic 实跑 + px4 路径 monkeypatch）。"""
from __future__ import annotations

import pytest

from launch_demo_session.spawn_sitl import SitlError, SyntheticSITL, spawn_sitl


def test_synthetic_mode_streams_and_injects():
    h = spawn_sitl({"name": "lowbat_headwind"}, "synthetic")
    assert h["mode"] == "synthetic"
    conn = h["conn"]
    hb = conn.recv_match(blocking=True, type="HEARTBEAT", timeout=1)
    assert hb is not None
    got = [conn.recv_match() for _ in range(10)]
    assert any(m is not None and m.get_type() == "ATTITUDE" for m in got)
    ack = conn.inject_scenario("lowbat_headwind", "mid", {"sim_battery_drain_x": 2.2})
    assert ack["applied"]


def test_px4_path_errors_and_process(monkeypatch, tmp_path):
    with pytest.raises(SitlError, match="px4_dir"):
        spawn_sitl({"name": "x", "airframe": "gz_x500"}, "px4")
    import subprocess as sp

    class FakeProc:
        poll = lambda self: None          # noqa: E731
        def kill(self): pass
    monkeypatch.setattr(sp, "Popen", lambda *a, **kw: FakeProc())
    h = spawn_sitl({"name": "x", "px4_dir": str(tmp_path)}, "px4")
    assert h["mode"] == "px4" and h["endpoint"].startswith("udpin:")  # PX4 广播口监听
