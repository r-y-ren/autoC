# ws_stream_feed 桩阶段测试（同名镜像）
import pytest

from src.serve_console.ws_stream_feed import ws_stream_feed


def test_ws_stream_feed_stub():
    assert callable(ws_stream_feed)
    with pytest.raises(NotImplementedError):
        import asyncio
        asyncio.run(ws_stream_feed(None, None))
