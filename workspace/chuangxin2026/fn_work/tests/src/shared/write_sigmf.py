# write_sigmf 桩阶段测试（与被测函数同名镜像）
import pytest

from src.shared.write_sigmf import write_sigmf


def test_write_sigmf_stub():
    assert callable(write_sigmf)
    with pytest.raises(NotImplementedError):
        write_sigmf(None, None, [])
