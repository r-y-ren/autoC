# read_sigmf 桩阶段测试（与被测函数同名镜像）
import pytest

from src.shared.read_sigmf import read_sigmf


def test_read_sigmf_stub():
    assert callable(read_sigmf)
    with pytest.raises(NotImplementedError):
        read_sigmf(None)
