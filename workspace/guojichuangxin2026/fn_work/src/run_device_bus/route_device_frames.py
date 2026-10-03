"""设备帧按主题分发（帧头统一 source=device|replay 标记）（run_device_bus 块）。"""
from __future__ import annotations


def route_device_frames(frame_stream, subscriptions):
    """frame_stream: 帧可迭代（含 topic 与 source）；subscriptions: {topic: [回调,...]}。

    背压策略：spectrum 类帧异常时丢弃保序（事件类全发）。返回路由统计。
    """
    stats = {"routed": 0, "dropped_backpressure": 0, "by_topic": {}}
    for fr in frame_stream:
        topic = fr.get("topic", "unknown")
        stats["by_topic"][topic] = stats["by_topic"].get(topic, 0) + 1
        subs = subscriptions.get(topic, [])
        dead = []
        for i, cb in enumerate(subs):
            try:
                cb(fr)
            except Exception:
                if topic == "spectrum":
                    stats["dropped_backpressure"] += 1   # 频谱帧可抽稀
                    dead.append(i)
                else:
                    raise                                # 事件帧不吞
        for i in reversed(dead):
            subs.pop(i)
        stats["routed"] += 1
    return stats
