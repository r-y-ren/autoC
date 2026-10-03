# calibrate_power 桩阶段测试（与被测函数同名镜像）
import pytest

from src.calibrate_power.calibrate_power import calibrate_power


def test_calibrate_power_stub():
    assert callable(calibrate_power)
    with pytest.raises(NotImplementedError):
        calibrate_power([], [])
