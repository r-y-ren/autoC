"""connect_sitl 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/run_ingest/connect_sitl.py 实现期落测试")


def test_connect_sitl():
    pass
