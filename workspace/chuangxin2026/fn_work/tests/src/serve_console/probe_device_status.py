# probe_device_status 桩阶段测试（同名镜像）
import pytest

from src.serve_console.probe_device_status import probe_device_status


def test_probe_device_status_stub():
    assert callable(probe_device_status)
    with pytest.raises(NotImplementedError):
        probe_device_status()
