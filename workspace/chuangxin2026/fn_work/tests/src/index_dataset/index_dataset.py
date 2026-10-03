# index_dataset 桩阶段测试（与被测函数同名镜像）
import pytest

from src.index_dataset.index_dataset import index_dataset


def test_index_dataset_stub():
    assert callable(index_dataset)
    with pytest.raises(NotImplementedError):
        index_dataset('runs')
