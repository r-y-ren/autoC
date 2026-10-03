"""设备总线主循环：模块发现→健康监测→帧路由→缺席/失健自动降级（run_device_bus 块）。"""
from __future__ import annotations

import queue
import threading
import time

from run_device_bus.discover_device_module import discover_device_module
from run_device_bus.health_check_module import health_check_module
from run_device_bus.route_device_frames import route_device_frames


class DeviceBus:
    """总线句柄：注册/订阅/健康查询；模块缺席自动挂回放源（帧等价、source 标注）。"""

    def __init__(self, module_configs, replay_configs=None):
        self.registry = discover_device_module(module_configs)
        self.replay = replay_configs or {}
        self.source_mode = {name: ("device" if v["present"] else "replay")
                            for name, v in self.registry.items()}
        self.stats = {name: {"fps": 0.0, "errors": 0, "latency_ms": 0.0}
                      for name in self.registry}
        self._subs: dict[str, list] = {}
        self._q = queue.Queue(maxsize=512)
        self._stop = threading.Event()
        self._router = threading.Thread(target=self._route_loop, daemon=True)
        self._router.start()

    def subscribe(self, topic, cb):
        self._subs.setdefault(topic, []).append(cb)

    def publish(self, frame):
        try:
            self._q.put_nowait(frame)
        except queue.Full:
            if frame.get("topic") == "spectrum":
                self.stats[frame.get("src_module", "?")]["errors"] += 1
            else:
                self._q.put(frame)          # 事件帧阻塞保送达

    def tick_health(self, module_name):
        h = health_check_module(self.stats.get(module_name))
        if h["action"] == "degrade" and self.source_mode.get(module_name) == "device":
            self.source_mode[module_name] = "replay"      # 降级：设备→回放
        elif h["action"] == "restore" and self.source_mode.get(module_name) == "replay" \
                and self.registry.get(module_name, {}).get("present"):
            self.source_mode[module_name] = "device"      # 恢复切回
        return h

    def _route_loop(self):
        def pump():
            while not self._stop.is_set():
                try:
                    fr = self._q.get(timeout=0.2)
                except queue.Empty:
                    return
                route_device_frames([fr], self._subs)
        while not self._stop.is_set():
            pump()

    def close(self):
        self._stop.set()
        self._router.join(timeout=1.0)


def run_device_bus(module_configs, replay_configs=None):
    """装配并返回总线句柄（探测失败不阻断：降级+日志）。"""
    return DeviceBus(module_configs, replay_configs)
