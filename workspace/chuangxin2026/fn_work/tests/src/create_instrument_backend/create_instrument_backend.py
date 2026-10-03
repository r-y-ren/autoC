# create_instrument_backend 桩阶段测试（与被测函数同名镜像）
import pytest

from src.create_instrument_backend.create_instrument_backend import create_instrument_backend


def test_create_instrument_backend_stub():
    assert callable(create_instrument_backend)
    with pytest.raises(NotImplementedError):
        create_instrument_backend('mock')
