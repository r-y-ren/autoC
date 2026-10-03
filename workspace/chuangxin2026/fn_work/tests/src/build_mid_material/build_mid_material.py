# build_mid_material 桩阶段测试（同名镜像）
import pytest

from src.build_mid_material.build_mid_material import build_mid_material


def test_build_mid_material_stub():
    assert callable(build_mid_material)
    with pytest.raises(NotImplementedError):
        build_mid_material(mode='mid')
