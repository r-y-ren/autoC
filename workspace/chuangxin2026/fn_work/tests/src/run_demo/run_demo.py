# run_demo 桩阶段测试（与被测函数同名镜像）
import pytest

from src.run_demo.run_demo import run_demo


def test_run_demo_stub():
    assert callable(run_demo)
    with pytest.raises(NotImplementedError):
        run_demo()
