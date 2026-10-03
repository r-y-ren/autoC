# collect_dut_samples 桩阶段测试（与被测函数同名镜像）
import pytest

from src.collect_dut_samples.collect_dut_samples import collect_dut_samples


def test_collect_dut_samples_stub():
    assert callable(collect_dut_samples)
    with pytest.raises(NotImplementedError):
        collect_dut_samples([], 0.0)
