"""discover_device_module 单测。"""
from __future__ import annotations


def test_absent_modules_recorded_not_blocking():
    from run_device_bus.discover_device_module import discover_device_module
    reg = discover_device_module([{"name": "sdr", "type": "usrp"},
                                  {"name": "jetson", "type": "ssh", "host": ""}])
    assert set(reg) == {"sdr", "jetson"}
    assert all(v["present"] is False for v in reg.values())   # 本机无 uhd/空 host→缺席
    assert reg["sdr"]["module"] is None


def test_unknown_type_absent():
    from run_device_bus.discover_device_module import discover_device_module
    reg = discover_device_module([{"name": "x", "type": "nonexistent"}])
    assert reg["x"]["present"] is False
