# EstopManager 桩阶段测试（同名镜像）
import pytest

from src.shared.estop import EstopManager


def test_EstopManager_stub():
    m = EstopManager()
    with pytest.raises(NotImplementedError):
        m.arm(None)
    with pytest.raises(NotImplementedError):
        m.fire("t")
