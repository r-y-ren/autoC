"""route_device_frames 单测（双源同管线等价断言）。"""
from __future__ import annotations


def test_topic_routing_and_backpressure_policy():
    from run_device_bus.route_device_frames import route_device_frames
    got = {"a": [], "b": []}
    def cb_a(fr): got["a"].append(fr)
    def cb_b(fr): got["b"].append(fr)
    frames = [{"topic": "spectrum", "source": "device", "power": 1},
              {"topic": "spectrum", "source": "replay", "power": 1},
              {"topic": "event", "source": "device"}]
    stats = route_device_frames(frames, {"spectrum": [cb_a], "event": [cb_b]})
    assert len(got["a"]) == 2 and got["a"][0]["source"] == "device"
    assert got["a"][1]["source"] == "replay"          # 双源同管线
    assert got["b"] and stats["routed"] == 3


def test_bad_spectrum_subscriber_dropped_not_crash():
    from run_device_bus.route_device_frames import route_device_frames
    def boom(fr): raise RuntimeError("backpressure")
    ok = []
    stats = route_device_frames([{"topic": "spectrum"}] * 3,
                                {"spectrum": [boom, lambda f: ok.append(1)]})
    assert stats["dropped_backpressure"] >= 1 and len(ok) == 3
