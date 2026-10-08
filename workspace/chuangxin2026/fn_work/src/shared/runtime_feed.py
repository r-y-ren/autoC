# RuntimeFeed：运行数据扇入扇出缓冲（责任文档演进轮三：shared/runtime_feed）
from __future__ import annotations


class RuntimeFeed:
    # 发布端→订阅端缓冲中转：多线程安全、限长防爆、消息三类透传
    def __init__(self, maxlen: int = 500) -> None:
        self._maxlen = maxlen

    def publish(self, msg: dict) -> None:
        # 桩——入缓冲（保序、满丢最旧不抛错）
        raise NotImplementedError("unimplemented:fn:RuntimeFeed.publish")

    def snapshot(self) -> list:
        # 桩——最近 N 条（重连续推用）
        raise NotImplementedError("unimplemented:fn:RuntimeFeed.snapshot")

    def subscribe(self):
        # 桩——返回消息迭代器（ws_stream_feed 消费）
        raise NotImplementedError("unimplemented:fn:RuntimeFeed.subscribe")
