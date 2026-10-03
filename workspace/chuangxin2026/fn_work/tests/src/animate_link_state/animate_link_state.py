# animate_link_state 桩阶段测试（与被测函数同名镜像）
import pytest

from src.animate_link_state.animate_link_state import animate_link_state


def test_animate_link_state_stub():
    assert callable(animate_link_state)
    with pytest.raises(NotImplementedError):
        animate_link_state(None, None)
