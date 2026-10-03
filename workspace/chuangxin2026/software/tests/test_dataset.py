"""R6 dataset：索引数据类+桩。"""

from __future__ import annotations

import pytest

from linkbench.dataset import indexer, sigmf_validate


def test_index_dataclass():
    idx = indexer.DatasetIndex(recordings=0)
    assert idx.groups == [] and idx.errors == []


def test_stubs():
    with pytest.raises(NotImplementedError):
        sigmf_validate.validate_recording("x")
    with pytest.raises(NotImplementedError):
        indexer.check_dataset("runs/")
