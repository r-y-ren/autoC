# generate_jamming 桩阶段测试（与被测函数同名镜像）
import pytest

from src.generate_jamming.generate_jamming import generate_jamming


def test_generate_jamming_stub():
    assert callable(generate_jamming)
    with pytest.raises(NotImplementedError):
        generate_jamming(None, dry_run=True)
