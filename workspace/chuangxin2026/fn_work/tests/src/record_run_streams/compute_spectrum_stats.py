# compute_spectrum_stats 桩阶段测试（与被测函数同名镜像）
import pytest

from src.record_run_streams.compute_spectrum_stats import compute_spectrum_stats


def test_compute_spectrum_stats_stub():
    assert callable(compute_spectrum_stats)
    with pytest.raises(NotImplementedError):
        compute_spectrum_stats(None, 1e6)
