# register_cjk_font 桩阶段测试（同名镜像）
import pytest

from src.shared.register_cjk_font import register_cjk_font


def test_register_cjk_font_stub():
    assert callable(register_cjk_font)
    with pytest.raises(NotImplementedError):
        register_cjk_font()
