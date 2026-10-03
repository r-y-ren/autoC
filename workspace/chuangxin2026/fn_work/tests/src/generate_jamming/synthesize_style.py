# synthesize_style 桩阶段测试（与被测函数同名镜像）
import pytest

from src.generate_jamming.synthesize_style import synthesize_style


def test_synthesize_style_stub():
    assert callable(synthesize_style)
    with pytest.raises(NotImplementedError):
        synthesize_style('cw', {})
