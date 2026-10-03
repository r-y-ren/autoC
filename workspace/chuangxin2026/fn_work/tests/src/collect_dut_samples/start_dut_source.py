# start_dut_source 桩阶段测试（与被测函数同名镜像）
import pytest

from src.collect_dut_samples.start_dut_source import start_dut_source


def test_start_dut_source_stub():
    assert callable(start_dut_source)
    with pytest.raises(NotImplementedError):
        start_dut_source({})
