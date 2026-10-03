"""inject_scenario_fault 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/shared/inject_scenario_fault.py 实现期落测试")


def test_inject_scenario_fault():
    pass
