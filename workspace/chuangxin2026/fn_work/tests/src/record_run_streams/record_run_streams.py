# record_run_streams 桩阶段测试（与被测函数同名镜像）
import pytest

from src.record_run_streams.record_run_streams import record_run_streams


def test_record_run_streams_stub():
    assert callable(record_run_streams)
    with pytest.raises(NotImplementedError):
        record_run_streams(None, 0.0, None)
