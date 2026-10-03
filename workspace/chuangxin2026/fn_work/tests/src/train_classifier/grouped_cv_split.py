# grouped_cv_split 桩阶段测试（与被测函数同名镜像）
import pytest

from src.train_classifier.grouped_cv_split import grouped_cv_split


def test_grouped_cv_split_stub():
    assert callable(grouped_cv_split)
    with pytest.raises(NotImplementedError):
        grouped_cv_split('i')
