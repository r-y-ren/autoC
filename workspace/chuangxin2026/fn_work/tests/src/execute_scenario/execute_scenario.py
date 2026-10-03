# execute_scenario 桩阶段测试（与被测函数同名镜像）
import pytest

from src.execute_scenario.execute_scenario import execute_scenario


def test_execute_scenario_stub():
    assert callable(execute_scenario)
    with pytest.raises(NotImplementedError):
        execute_scenario(None)
