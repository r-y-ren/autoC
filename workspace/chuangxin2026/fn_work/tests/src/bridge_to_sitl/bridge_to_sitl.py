# bridge_to_sitl 桩阶段测试（与被测函数同名镜像）
import pytest

from src.bridge_to_sitl.bridge_to_sitl import bridge_to_sitl


def test_bridge_to_sitl_stub():
    assert callable(bridge_to_sitl)
    with pytest.raises(NotImplementedError):
        bridge_to_sitl('r')
