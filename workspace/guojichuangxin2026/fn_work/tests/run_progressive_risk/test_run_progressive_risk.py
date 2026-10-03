"""run_progressive_risk 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/run_progressive_risk/run_progressive_risk.py 实现期落测试")


def test_run_progressive_risk():
    pass
