"""health_check_module 单测。"""
from __future__ import annotations


def test_degrade_and_restore():
    from run_device_bus.health_check_module import health_check_module
    assert health_check_module(None)["action"] == "degrade"
    bad = health_check_module({"fps": 0.2, "errors": 9, "latency_ms": 3000})
    assert bad["action"] == "degrade" and "帧率" in bad["why"]
    good = health_check_module({"fps": 5.0, "errors": 0, "latency_ms": 30})
    assert good["action"] == "restore"
