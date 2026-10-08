# collect_dashboard 桩阶段测试（同名镜像）
import pytest

from src.serve_console.collect_dashboard import collect_dashboard


def test_collect_dashboard_stub():
    assert callable(collect_dashboard)
    with pytest.raises(NotImplementedError):
        collect_dashboard()
