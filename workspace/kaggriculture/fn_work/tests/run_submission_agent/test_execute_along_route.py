"""execute_along_route 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.execute_along_route import execute_along_route


def test_execute_along_route_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:execute_along_route"):
        execute_along_route({}, {})
