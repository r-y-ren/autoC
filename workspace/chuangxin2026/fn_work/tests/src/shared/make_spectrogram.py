# make_spectrogram 桩阶段测试（与被测函数同名镜像）
import pytest

from src.shared.make_spectrogram import make_spectrogram


def test_make_spectrogram_stub():
    assert callable(make_spectrogram)
    with pytest.raises(NotImplementedError):
        make_spectrogram(None)
