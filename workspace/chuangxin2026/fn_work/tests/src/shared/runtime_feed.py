# RuntimeFeed 桩阶段测试（同名镜像）
import pytest

from src.shared.runtime_feed import RuntimeFeed


def test_RuntimeFeed_stub():
    f = RuntimeFeed()
    with pytest.raises(NotImplementedError):
        f.publish({})
    with pytest.raises(NotImplementedError):
        f.snapshot()
    with pytest.raises(NotImplementedError):
        f.subscribe()
