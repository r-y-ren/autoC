# plan_steps 桩阶段测试（与被测函数同名镜像）
import pytest

from src.execute_scenario.plan_steps import plan_steps


def test_plan_steps_stub():
    assert callable(plan_steps)
    with pytest.raises(NotImplementedError):
        plan_steps(None)
