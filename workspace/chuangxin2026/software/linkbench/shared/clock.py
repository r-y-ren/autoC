"""统一时钟：全平台时间戳唯一来源（主机单调钟，ms）。"""

from __future__ import annotations


def now_ms() -> int:
    """返回主机单调时钟毫秒值（跨三路数据流对齐的基准）。"""
    raise NotImplementedError("unimplemented:fn:now_ms")
