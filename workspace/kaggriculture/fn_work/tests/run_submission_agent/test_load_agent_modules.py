"""load_agent_modules 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.load_agent_modules import load_agent_modules


def test_load_agent_modules_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:load_agent_modules"):
        load_agent_modules(None)
