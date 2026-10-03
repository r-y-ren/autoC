# predict_style 桩阶段测试（与被测函数同名镜像）
import pytest

from src.predict_style.predict_style import predict_style


def test_predict_style_stub():
    assert callable(predict_style)
    with pytest.raises(NotImplementedError):
        predict_style('m', 's')
