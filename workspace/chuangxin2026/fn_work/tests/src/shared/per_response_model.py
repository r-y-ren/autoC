# per_response_model 桩阶段测试（同名镜像）
import pytest

from src.shared.per_response_model import per_response_model


def test_per_response_model_stub():
    assert callable(per_response_model)
    with pytest.raises(NotImplementedError):
        per_response_model(0.0, 10.0)
