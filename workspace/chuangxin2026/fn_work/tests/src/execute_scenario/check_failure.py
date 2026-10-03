# check_failure 桩阶段测试（与被测函数同名镜像）
import pytest

from src.execute_scenario.check_failure import check_failure


def test_check_failure_stub():
    assert callable(check_failure)
    with pytest.raises(NotImplementedError):
        check_failure([], None)
