# scaled_criteria 桩阶段测试（同名镜像）
import pytest

from src.execute_scenario.scaled_criteria import scaled_criteria


def test_scaled_criteria_stub():
    assert callable(scaled_criteria)
    with pytest.raises(NotImplementedError):
        scaled_criteria(None, 2.0)
