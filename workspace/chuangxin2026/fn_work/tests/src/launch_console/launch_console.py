# launch_console 桩阶段测试（同名镜像）
import pytest

from src.launch_console.launch_console import launch_console


def test_launch_console_stub():
    assert callable(launch_console)
    with pytest.raises(NotImplementedError):
        launch_console(selftest=True)
