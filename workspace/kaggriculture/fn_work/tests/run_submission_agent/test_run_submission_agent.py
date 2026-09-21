"""run_submission_agent 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.run_submission_agent import run_submission_agent


def test_run_submission_agent_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:run_submission_agent"):
        run_submission_agent({})
