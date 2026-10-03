# train_classifier 桩阶段测试（与被测函数同名镜像）
import pytest

from src.train_classifier.train_classifier import train_classifier


def test_train_classifier_stub():
    assert callable(train_classifier)
    with pytest.raises(NotImplementedError):
        train_classifier('d')
