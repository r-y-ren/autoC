"""replay_check 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/run_ingest/replay_check.py 实现期落测试")


def test_replay_check():
    pass
