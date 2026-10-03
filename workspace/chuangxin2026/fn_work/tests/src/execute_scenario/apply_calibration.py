# apply_calibration 桩阶段测试（同名镜像）
import pytest

from src.execute_scenario.apply_calibration import apply_calibration


def test_apply_calibration_stub():
    assert callable(apply_calibration)
    with pytest.raises(NotImplementedError):
        apply_calibration(0.0, 2422000000)
