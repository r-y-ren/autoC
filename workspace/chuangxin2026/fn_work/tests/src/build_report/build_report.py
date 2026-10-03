# build_report 桩阶段测试（与被测函数同名镜像）
import pytest

from src.build_report.build_report import build_report


def test_build_report_stub():
    assert callable(build_report)
    with pytest.raises(NotImplementedError):
        build_report(None)
