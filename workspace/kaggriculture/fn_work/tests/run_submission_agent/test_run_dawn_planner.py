"""run_dawn_planner 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.run_dawn_planner import run_dawn_planner


def test_run_dawn_planner_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:run_dawn_planner"):
        run_dawn_planner({}, {})
