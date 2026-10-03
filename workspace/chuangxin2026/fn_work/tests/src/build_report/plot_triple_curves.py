# plot_triple_curves 桩阶段测试（与被测函数同名镜像）
import pytest

from src.build_report.plot_triple_curves import plot_triple_curves


def test_plot_triple_curves_stub():
    assert callable(plot_triple_curves)
    with pytest.raises(NotImplementedError):
        plot_triple_curves(None, None)
