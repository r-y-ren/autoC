"""R1 gen：导入链+签名存在+样式注册表形状。"""

from __future__ import annotations

import pytest

from linkbench.gen import generator, styles


def test_module_importable():
    assert callable(generator.generate_interference)


def test_style_builders_exist():
    for name in ("build_cw", "build_sweep", "build_chirp",
                 "build_bandlimited_noise", "build_partial_band", "build_pulse"):
        assert callable(getattr(styles, name)), name


def test_style_builders_are_stubs():
    with pytest.raises(NotImplementedError):
        styles.build_cw(2422e6, 0.1, 1e6)


def test_generate_interference_is_stub():
    from linkbench.shared.scenario import InjectionSpec
    with pytest.raises(NotImplementedError):
        generator.generate_interference(InjectionSpec(["cw"], 2422e6, 1e3))
