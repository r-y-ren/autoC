"""observe_opponent_state 桩标记占位测试：仅断言统一 NotImplementedError 标记，无行为断言。"""

import pytest

from run_submission_agent.observe_opponent_state import observe_opponent_state


def test_observe_opponent_state_stub_marker():
    with pytest.raises(NotImplementedError, match="unimplemented:fn:observe_opponent_state"):
        observe_opponent_state({}, 0)
