"""launch_demo_session 单测（实现期落测试体，scaffold 期占位跳过）。"""
import pytest

pytestmark = pytest.mark.skip(reason="scaffold 桩：src/launch_demo_session/launch_demo_session.py 实现期落测试")


def test_launch_demo_session():
    pass
