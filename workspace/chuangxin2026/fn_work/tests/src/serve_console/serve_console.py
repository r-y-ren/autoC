# serve_console 桩阶段测试（与被测函数同名镜像）
import pytest

from src.serve_console.serve_console import serve_console


def test_serve_console_stub():
    assert callable(serve_console)
    with pytest.raises(NotImplementedError):
        serve_console(selftest=True)
