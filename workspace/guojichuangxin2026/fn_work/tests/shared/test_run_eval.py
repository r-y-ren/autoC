"""run_eval 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/shared/run_eval.py 实现期落测试")


def test_run_eval():
    pass
