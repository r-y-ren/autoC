# render_static_pages 桩阶段测试（同名镜像）
import pytest

from src.serve_console.render_static_pages import render_static_pages


def test_render_static_pages_stub():
    assert callable(render_static_pages)
    with pytest.raises(NotImplementedError):
        render_static_pages(None)
