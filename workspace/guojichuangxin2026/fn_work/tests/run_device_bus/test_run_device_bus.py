"""run_device_bus 主循环单测（拔插双态切换）。"""
from __future__ import annotations


def test_bus_assembly_and_source_mode_switch():
    from run_device_bus.run_device_bus import run_device_bus
    bus = run_device_bus([{"name": "sdr", "type": "usrp"}],
                         replay_configs={"sdr": "fixtures/x.npz"})
    assert bus.source_mode["sdr"] == "replay"          # 缺席→回放
    got = []
    bus.subscribe("spectrum", got.append)
    bus.publish({"topic": "spectrum", "source": "replay", "p": 1})
    import time
    for _ in range(50):
        if got:
            break
        time.sleep(0.02)
    assert got                                       # 路由线程送达
    bus.stats["sdr"].update({"fps": 5.0, "errors": 0, "latency_ms": 10})
    h = bus.tick_health("sdr")
    assert h["healthy"]
    bus.stats["sdr"].update({"fps": 0.0, "errors": 99, "latency_ms": 9999})
    bus.tick_health("sdr")
    assert bus.source_mode["sdr"] == "replay"         # 已在回放，维持
    # 模拟设备恢复（present=True）+健康→切回
    bus.registry["sdr"]["present"] = True
    bus.stats["sdr"].update({"fps": 5.0, "errors": 0, "latency_ms": 10})
    bus.tick_health("sdr")
    assert bus.source_mode["sdr"] == "device"
    bus.close()
