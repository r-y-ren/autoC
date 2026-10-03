# load_scenario 桩阶段测试（与被测函数同名镜像）
import pytest

from src.shared.load_scenario import load_scenario


def test_load_scenario_stub():
    assert callable(load_scenario)
    with pytest.raises(NotImplementedError):
        load_scenario(None)
